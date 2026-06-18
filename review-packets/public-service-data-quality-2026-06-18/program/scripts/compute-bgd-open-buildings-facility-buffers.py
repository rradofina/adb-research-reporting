"""Compute nearest-facility Open Buildings counts for Bangladesh PSDQ.

This script uses Open Buildings V3 point CSV shards and assigns each building
point inside Bangladesh to its nearest coordinate-ready DGHS facility within
1, 3, and 5 km. Assignment to the nearest facility avoids double-counting
buildings across overlapping buffers.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from shapely import contains_xy, prepare
from shapely.geometry import shape
from sklearn.neighbors import BallTree


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "open-buildings"
POINT_DIR = CACHE / "points"
OUT_DIR = ROOT / "generated"
MANIFEST_JSON = OUT_DIR / "psdq-bgd-open-buildings-tile-manifest.json"
FACILITY_EXTRACT = OUT_DIR / "psdq-bgd-facility-coordinate-extract.csv"
BGD_BOUNDARY = CACHE / "geoBoundaries-BGD-ADM0.geojson"

FACILITY_OUT_CSV = OUT_DIR / "psdq-bgd-open-buildings-facility-buffers.csv"
ADMIN_OUT_CSV = OUT_DIR / "psdq-bgd-open-buildings-admin-summary.csv"
SUMMARY_OUT_JSON = OUT_DIR / "psdq-bgd-open-buildings-buffer-summary.json"

EARTH_RADIUS_KM = 6371.0088
RADII_KM = (1.0, 3.0, 5.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tiles", nargs="*", default=None, help="Optional tile_id subset for smoke runs.")
    parser.add_argument("--chunk-size", type=int, default=500_000)
    parser.add_argument("--max-rows-per-tile", type=int, default=None, help="Debug cap; do not use for final results.")
    parser.add_argument("--workers", type=int, default=1, help="Tile-level worker processes.")
    parser.add_argument("--progress-every", type=int, default=2_000_000, help="Rows between progress messages per tile.")
    return parser.parse_args()


def load_manifest(selected: list[str] | None) -> list[dict[str, Any]]:
    obj = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    tiles = obj["tiles"]
    if selected:
        wanted = set(selected)
        tiles = [tile for tile in tiles if tile["tile_id"] in wanted]
    return tiles


def load_boundary():
    obj = json.loads(BGD_BOUNDARY.read_text(encoding="utf-8"))
    boundary = shape(obj["features"][0]["geometry"])
    prepare(boundary)
    return boundary


def load_facilities() -> pd.DataFrame:
    df = pd.read_csv(FACILITY_EXTRACT)
    df = df[df["has_valid_coordinate"] == 1].copy()
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)
    return df


def point_path(tile_id: str) -> Path:
    return POINT_DIR / f"{tile_id}_buildings.csv.gz"


def init_count_arrays(n: int) -> dict[str, np.ndarray]:
    arrays: dict[str, np.ndarray] = {}
    for mode in ("all", "p85", "p90"):
        for radius in RADII_KM:
            arrays[f"buildings_nearest_{int(radius)}km_{mode}"] = np.zeros(n, dtype=np.int64)
    return arrays


def add_counts(arrays: dict[str, np.ndarray], facility_idx: np.ndarray, distance_km: np.ndarray, confidence: np.ndarray, tile: dict[str, Any]) -> None:
    p85 = tile.get("confidence_threshold_85_precision")
    p90 = tile.get("confidence_threshold_90_precision")
    masks = {
        "all": np.ones(len(distance_km), dtype=bool),
        "p85": confidence >= (p85 if p85 is not None else 1.0),
        "p90": confidence >= (p90 if p90 is not None else 1.0),
    }
    for mode, confidence_mask in masks.items():
        for radius in RADII_KM:
            mask = confidence_mask & (distance_km <= radius)
            if not np.any(mask):
                continue
            counts = np.bincount(facility_idx[mask], minlength=len(arrays[f"buildings_nearest_{int(radius)}km_{mode}"]))
            arrays[f"buildings_nearest_{int(radius)}km_{mode}"] += counts


def iter_building_chunks(path: Path, chunk_size: int):
    return pd.read_csv(
        path,
        compression="gzip",
        usecols=["latitude", "longitude", "confidence"],
        dtype={"latitude": "float64", "longitude": "float64", "confidence": "float64"},
        chunksize=chunk_size,
    )


def write_facility_output(facilities: pd.DataFrame, arrays: dict[str, np.ndarray]) -> None:
    out = facilities.copy()
    for name, values in arrays.items():
        out[name] = values
    out.to_csv(FACILITY_OUT_CSV, index=False)


def write_admin_output(facility_rows: pd.DataFrame) -> list[dict[str, Any]]:
    count_cols = [col for col in facility_rows.columns if col.startswith("buildings_nearest_")]
    grouped = (
        facility_rows.groupby(["division_name", "district_name", "upazila_name"], dropna=False)
        .agg(
            coordinate_facilities=("id", "count"),
            clinical_tier_facilities=("is_clinical_tier", "sum"),
            **{col: (col, "sum") for col in count_cols},
        )
        .reset_index()
    )
    grouped = grouped.sort_values("buildings_nearest_3km_p85", ascending=False)
    grouped.to_csv(ADMIN_OUT_CSV, index=False)
    return json.loads(grouped.to_json(orient="records"))


def process_tile(
    tile: dict[str, Any],
    chunk_size: int,
    max_rows_per_tile: int | None,
    progress_every: int,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    tile_id = tile["tile_id"]
    path = point_path(tile_id)
    if not path.exists():
        raise FileNotFoundError(f"Missing point shard for tile {tile_id}: {path}")

    boundary = load_boundary()
    min_lon, min_lat, max_lon, max_lat = boundary.bounds
    facilities = load_facilities()
    facility_rad = np.radians(facilities[["latitude", "longitude"]].to_numpy())
    tree = BallTree(facility_rad, metric="haversine")
    arrays = init_count_arrays(len(facilities))

    processed = 0
    inside_bgd = 0
    assigned_5km = 0
    last_progress_bucket = -1
    print(f"Processing tile {tile_id}...", flush=True)
    for chunk in iter_building_chunks(path, chunk_size):
        if max_rows_per_tile is not None and processed >= max_rows_per_tile:
            break
        if max_rows_per_tile is not None:
            chunk = chunk.head(max(0, max_rows_per_tile - processed))

        processed += len(chunk)
        chunk = chunk.dropna(subset=["latitude", "longitude", "confidence"])
        if chunk.empty:
            continue

        lon = chunk["longitude"].to_numpy(dtype=float)
        lat = chunk["latitude"].to_numpy(dtype=float)
        in_bbox = (lon >= min_lon) & (lon <= max_lon) & (lat >= min_lat) & (lat <= max_lat)
        if not np.any(in_bbox):
            continue

        bbox_idx = np.flatnonzero(in_bbox)
        in_country_subset = contains_xy(boundary, lon[bbox_idx], lat[bbox_idx])
        if not np.any(in_country_subset):
            continue

        country_idx = bbox_idx[in_country_subset]
        points = np.radians(np.column_stack([lat[country_idx], lon[country_idx]]))
        confidence = chunk["confidence"].to_numpy(dtype=float)[country_idx]
        inside_bgd += len(points)

        dist_rad, idx = tree.query(points, k=1)
        distance_km = dist_rad[:, 0] * EARTH_RADIUS_KM
        facility_idx = idx[:, 0]
        assigned_5km += int(np.sum(distance_km <= 5.0))
        add_counts(arrays, facility_idx, distance_km, confidence, tile)

        progress_bucket = processed // progress_every if progress_every > 0 else 0
        if progress_bucket != last_progress_bucket and progress_bucket > 0:
            last_progress_bucket = progress_bucket
            print(
                f"Tile {tile_id}: {processed:,} rows, {inside_bgd:,} inside Bangladesh, "
                f"{assigned_5km:,} within 5 km",
                flush=True,
            )

    print(
        f"Finished tile {tile_id}: {processed:,} rows, {inside_bgd:,} inside Bangladesh, "
        f"{assigned_5km:,} within 5 km",
        flush=True,
    )
    return (
        {
            "tile_id": tile_id,
            "rows_processed": int(processed),
            "inside_bangladesh": int(inside_bgd),
            "assigned_within_5km": int(assigned_5km),
            "confidence_threshold_85_precision": tile.get("confidence_threshold_85_precision"),
            "confidence_threshold_90_precision": tile.get("confidence_threshold_90_precision"),
        },
        arrays,
    )


def merge_count_arrays(target: dict[str, np.ndarray], source: dict[str, np.ndarray]) -> None:
    for name, values in source.items():
        target[name] += values


def main() -> None:
    args = parse_args()
    tiles = load_manifest(args.tiles)
    if not tiles:
        raise SystemExit("No Open Buildings tiles selected.")

    facilities = load_facilities()
    arrays = init_count_arrays(len(facilities))

    tile_stats = []
    workers = max(1, min(args.workers, len(tiles)))
    if workers == 1:
        for tile in tiles:
            tile_stat, tile_arrays = process_tile(tile, args.chunk_size, args.max_rows_per_tile, args.progress_every)
            tile_stats.append(tile_stat)
            merge_count_arrays(arrays, tile_arrays)
    else:
        print(f"Processing {len(tiles)} tiles with {workers} workers...", flush=True)
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(process_tile, tile, args.chunk_size, args.max_rows_per_tile, args.progress_every): tile["tile_id"]
                for tile in tiles
            }
            completed: dict[str, dict[str, Any]] = {}
            for future in as_completed(futures):
                tile_id = futures[future]
                tile_stat, tile_arrays = future.result()
                completed[tile_id] = tile_stat
                merge_count_arrays(arrays, tile_arrays)
                print(f"Merged tile {tile_id}.", flush=True)
            tile_stats = [completed[tile["tile_id"]] for tile in tiles]

    write_facility_output(facilities, arrays)
    facility_rows = facilities.copy()
    for name, values in arrays.items():
        facility_rows[name] = values
    admin_rows = write_admin_output(facility_rows)

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "source": "Google Open Buildings V3 point CSVs + DGHS public facilities JSON endpoint",
        "method": "Open Buildings points inside Bangladesh are assigned to the nearest coordinate-ready DGHS facility if the nearest facility is within 1, 3, or 5 km. p85/p90 counts apply Google tile-specific precision thresholds.",
        "tiles": tile_stats,
        "facilities": int(len(facilities)),
        "totals": {name: int(values.sum()) for name, values in arrays.items()},
        "top_admin_by_3km_p85": admin_rows[:20],
        "outputs": {
            "facility_csv": str(FACILITY_OUT_CSV.relative_to(ROOT)),
            "admin_csv": str(ADMIN_OUT_CSV.relative_to(ROOT)),
        },
        "non_claim": "Nearest-facility building counts are settlement-exposure denominators, not population, households, poverty, verified catchment populations, travel time, or service demand.",
    }
    SUMMARY_OUT_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {FACILITY_OUT_CSV}")
    print(f"Wrote {ADMIN_OUT_CSV}")
    print(f"Wrote {SUMMARY_OUT_JSON}")


if __name__ == "__main__":
    main()
