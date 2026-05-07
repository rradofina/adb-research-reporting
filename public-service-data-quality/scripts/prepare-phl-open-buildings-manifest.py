"""Prepare a Philippines Open Buildings tile manifest for PSDQ.

The manifest identifies Google Open Buildings V3 S2 level-4 point shards
that intersect the Philippines boundary from the HDX/OCHA PSA-NAMRIA
administrative-boundary package.
"""

from __future__ import annotations

import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pyogrio
import requests
from shapely.geometry import shape
from shapely.ops import unary_union


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
RAW_DIR = CACHE / "open-buildings"
PHL_BOUNDARY_DIR = CACHE / "phl-boundaries"
PHL_GDB = PHL_BOUNDARY_DIR / "gdb" / "phl_adm_psa_namria_20231106_GDB.gdb"
OUT_DIR = ROOT / "generated"

TILES_URL = "https://openbuildings-public-dot-gweb-research.uw.r.appspot.com/public/tiles.geojson"
THRESHOLDS_URL = "https://storage.googleapis.com/open-buildings-data/v3/score_thresholds_s2_level_4.csv"
HDX_GDB_URL = "https://data.humdata.org/dataset/caf116df-f984-4deb-85ca-41b349d3f313/resource/314cbaea-c7a0-4ce9-a4ea-e5af2a788ac1/download/phl_adm_psa_namria_20231106_gdb.gdb.zip"

TILES_FILE = RAW_DIR / "open-buildings-v3-tiles.geojson"
THRESHOLDS_FILE = RAW_DIR / "score_thresholds_s2_level_4.csv"
MANIFEST_JSON = OUT_DIR / "psdq-phl-open-buildings-tile-manifest.json"
MANIFEST_CSV = OUT_DIR / "psdq-phl-open-buildings-tile-manifest.csv"


def now_utc() -> str:
    return datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_json(url: str) -> dict[str, Any]:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return r.json()


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ADB-Research-PSDQ/1.0"})
    with urllib.request.urlopen(req, timeout=900) as response, path.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)


def ensure_phl_gdb() -> None:
    if PHL_GDB.exists():
        return
    zip_path = PHL_BOUNDARY_DIR / "phl_adm_psa_namria_20231106_gdb.gdb.zip"
    download(HDX_GDB_URL, zip_path)
    import zipfile

    target = PHL_BOUNDARY_DIR / "gdb"
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(target)


def head_size_mb(url: str) -> float | None:
    try:
        r = requests.head(url, timeout=60)
        r.raise_for_status()
        n = r.headers.get("content-length")
        return round(int(n) / 1024 / 1024, 2) if n else None
    except Exception:
        return None


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def load_thresholds() -> dict[str, dict[str, Any]]:
    download(THRESHOLDS_URL, THRESHOLDS_FILE)
    out: dict[str, dict[str, Any]] = {}
    with THRESHOLDS_FILE.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            out[row["s2_token"]] = {
                "confidence_threshold_80_precision": parse_float(row.get("confidence_threshold_80%_precision")),
                "confidence_threshold_85_precision": parse_float(row.get("confidence_threshold_85%_precision")),
                "confidence_threshold_90_precision": parse_float(row.get("confidence_threshold_90%_precision")),
                "building_count": parse_int(row.get("building_count")),
                "building_count_85_precision": parse_int(row.get("building_count_85%_precision")),
                "building_count_90_precision": parse_int(row.get("building_count_90%_precision")),
                "num_samples": parse_int(row.get("num_samples")),
            }
    return out


def load_phl_boundary():
    ensure_phl_gdb()
    adm0 = pyogrio.read_dataframe(
        PHL_GDB,
        layer="phl_admbnda_adm0_singlepart_psa_namria_20231106",
        columns=["ADM0_PCODE"],
    )
    return unary_union(list(adm0.geometry))


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if TILES_FILE.exists():
        tiles_obj = json.loads(TILES_FILE.read_text(encoding="utf-8"))
    else:
        tiles_obj = fetch_json(TILES_URL)
        TILES_FILE.write_text(json.dumps(tiles_obj), encoding="utf-8")

    boundary_geom = load_phl_boundary()
    thresholds = load_thresholds()

    rows = []
    for feature in tiles_obj["features"]:
        geom = shape(feature["geometry"])
        if not geom.intersects(boundary_geom):
            continue
        props = feature["properties"]
        tile_id = props["tile_id"]
        polygon_url = props["tile_url"]
        point_url = polygon_url.replace("/polygons_s2_level_4_gzip/", "/points_s2_level_4_gzip/")
        rows.append(
            {
                "tile_id": tile_id,
                "polygon_url": polygon_url,
                "point_url": point_url,
                "polygon_size_mb_catalog": float(props["size_mb"]),
                "point_size_mb_head": head_size_mb(point_url),
                **thresholds.get(tile_id, {}),
            }
        )

    rows.sort(key=lambda row: row["tile_id"])
    payload = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Philippines",
        "source": {
            "open_buildings_tiles": TILES_URL,
            "open_buildings_thresholds": THRESHOLDS_URL,
            "boundary": HDX_GDB_URL,
            "boundary_source": "HDX/OCHA Philippines subnational administrative boundaries, PSA/NAMRIA, validOn 2023-11-06",
        },
        "method": "Intersect Google Open Buildings V3 tile polygons with the PSA/NAMRIA Philippines ADM0 boundary; use point CSVs for city/municipality settlement denominators.",
        "tiles": rows,
        "totals": {
            "tile_count": len(rows),
            "polygon_size_mb_catalog": round(sum(row["polygon_size_mb_catalog"] for row in rows), 2),
            "point_size_mb_head": round(sum((row["point_size_mb_head"] or 0) for row in rows), 2),
            "building_count_catalog": sum((row.get("building_count") or 0) for row in rows),
            "building_count_85_precision_catalog": sum((row.get("building_count_85_precision") or 0) for row in rows),
            "building_count_90_precision_catalog": sum((row.get("building_count_90_precision") or 0) for row in rows),
        },
        "non_claim": "Tile-level catalog counts include areas outside the Philippines where S2 tiles cross borders; downstream scripts assign points to PSA/NAMRIA ADM3 polygons.",
    }

    MANIFEST_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    with MANIFEST_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else ["tile_id"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {MANIFEST_JSON}")
    print(f"Wrote {MANIFEST_CSV}")
    print(f"{payload['totals']['tile_count']} tiles; {payload['totals']['point_size_mb_head']:.2f} MB point gzip total")


if __name__ == "__main__":
    main()
