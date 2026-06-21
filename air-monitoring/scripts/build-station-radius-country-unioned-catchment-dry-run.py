"""Build the station-radius country-unioned catchment dry run.

The prior denominator join dry run attaches every candidate coordinate-radius
row to GHSL and ACAG denominators. This pass removes within-country overlap in
the candidate buffers so the reader can see how much duplicate row-level buffer
mass is created before any coverage claim is allowed.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from rasterio.windows import Window, bounds as window_bounds


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"

JOIN_SCRIPT = Path(__file__).with_name("build-station-radius-denominator-join-dry-run.py")
JOIN_COUNTRY_CSV = GENERATED / "air-monitoring-station-radius-denominator-join-dry-run-country.csv"
JOIN_SUMMARY_JSON = GENERATED / "air-monitoring-station-radius-denominator-join-dry-run-summary.json"

OUT_COUNTRY_CSV = GENERATED / "air-monitoring-station-radius-country-unioned-catchment-dry-run.csv"
OUT_JSON = GENERATED / "air-monitoring-station-radius-country-unioned-catchment-dry-run-summary.json"
OUT_MD = PROGRAM / "station-radius-country-unioned-catchment-dry-run.md"

STATUS = "computed_station_radius_country_unioned_catchment_dry_run"
METHOD = "air_monitoring_station_radius_country_unioned_catchment_dry_run_v1"
ATTESTATION = "ai-first"
GOAL_LEVEL = "L3 station-radius country-unioned catchment dry run"
BLOCK_SIZE = 512

NON_CLAIM = (
    "This country-unioned catchment dry run counts each GHSL population cell at "
    "most once within an economy and radius band. It is still a candidate "
    "denominator diagnostic. It does not validate same-station joins, does not "
    "classify complete monitor grade, does not prove regulatory monitor "
    "coverage, and does not support a population-served or exposure claim."
)

COUNTRY_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "row_type",
    "iso3",
    "country",
    "radius_km",
    "radius_role",
    "coordinate_rows",
    "unique_coordinate_points",
    "openaq_coordinate_rows",
    "official_pm25_coordinate_rows",
    "source_family_mix",
    "unioned_population_sum",
    "unioned_positive_cells",
    "unioned_population_tiles",
    "unioned_population_tile_count",
    "unioned_population_windows_scanned",
    "unioned_population_windows_with_cells",
    "row_level_candidate_population_buffer_sum",
    "row_level_exact_coordinate_dedup_sum",
    "row_to_union_population_multiplier",
    "exact_dedup_to_union_population_multiplier",
    "population_overlap_removed_from_row_sum",
    "population_overlap_removed_from_exact_dedup_sum",
    "unioned_pm25_cell_mean_ugm3",
    "unioned_pm25_cell_count",
    "unioned_pm25_computed",
    "country_union_population_computed",
    "coverage_claim_allowed",
    "validated_same_station_join_rows",
    "complete_monitor_grade_rows",
    "station_radius_ready",
    "reader_use",
    "blocking_gap",
    "non_claim",
]


def load_join_module() -> Any:
    spec = importlib.util.spec_from_file_location("station_radius_denominator_join", JOIN_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import {JOIN_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


JOIN = load_join_module()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_ref(path: Path) -> str:
    return str(path.relative_to(PROGRAM)).replace("\\", "/")


def parse_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        parsed = float(str(value).strip())
        if not math.isfinite(parsed):
            return None
        return parsed
    except (TypeError, ValueError):
        return None


def round_number(value: float | None, digits: int = 3) -> float | str:
    if value is None or not math.isfinite(value):
        return ""
    return round(float(value), digits)


def intersects(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    aw, a_s, ae, an = a
    bw, b_s, be, bn = b
    return not (ae < bw or aw > be or an < b_s or a_s > bn)


def clipped_tile_bbox(
    dataset: Any,
    bbox: tuple[float, float, float, float],
) -> tuple[float, float, float, float] | None:
    west, south, east, north = bbox
    bounds = dataset.bounds
    if east < bounds.left or west > bounds.right or north < bounds.bottom or south > bounds.top:
        return None
    return (
        max(west, bounds.left),
        max(south, bounds.bottom),
        min(east, bounds.right),
        min(north, bounds.top),
    )


def block_windows_for_point_windows(
    dataset: Any,
    point_windows: list[tuple[Any, tuple[float, float, float, float], Window]],
) -> list[Window]:
    block_keys: set[tuple[int, int]] = set()
    for _, _, window in point_windows:
        row_start = int(window.row_off) // BLOCK_SIZE * BLOCK_SIZE
        col_start = int(window.col_off) // BLOCK_SIZE * BLOCK_SIZE
        row_end = math.ceil((int(window.row_off) + int(window.height)) / BLOCK_SIZE) * BLOCK_SIZE
        col_end = math.ceil((int(window.col_off) + int(window.width)) / BLOCK_SIZE) * BLOCK_SIZE
        for row_off in range(row_start, min(row_end, dataset.height), BLOCK_SIZE):
            for col_off in range(col_start, min(col_end, dataset.width), BLOCK_SIZE):
                block_keys.add((row_off, col_off))

    windows = []
    for row_off, col_off in sorted(block_keys):
        windows.append(
            Window(
                col_off,
                row_off,
                min(BLOCK_SIZE, dataset.width - col_off),
                min(BLOCK_SIZE, dataset.height - row_off),
            )
        )
    return windows


def point_window_mask(block_window: Window, point_window: Window) -> np.ndarray:
    rows = np.arange(
        int(block_window.row_off),
        int(block_window.row_off) + int(block_window.height),
        dtype="int64",
    )
    cols = np.arange(
        int(block_window.col_off),
        int(block_window.col_off) + int(block_window.width),
        dtype="int64",
    )
    row_ok = (rows >= int(point_window.row_off)) & (
        rows < int(point_window.row_off) + int(point_window.height)
    )
    col_ok = (cols >= int(point_window.col_off)) & (
        cols < int(point_window.col_off) + int(point_window.width)
    )
    return row_ok[:, None] & col_ok[None, :]


def unioned_population(
    points: list[Any],
    radius_km: float,
    rasters: list[Any],
) -> dict[str, Any]:
    point_boxes = [
        (point, JOIN.bbox_for_radius(point.latitude, point.longitude, radius_km))
        for point in points
    ]

    total = 0.0
    positive_cells = 0
    windows_scanned = 0
    windows_with_cells = 0
    tile_ids: list[str] = []

    for raster in rasters:
        dataset = raster.dataset
        tile_bbox = (dataset.bounds.left, dataset.bounds.bottom, dataset.bounds.right, dataset.bounds.top)
        tile_point_boxes = [(point, bbox) for point, bbox in point_boxes if intersects(bbox, tile_bbox)]
        if not tile_point_boxes:
            continue
        tile_point_windows = []
        for point, bbox in tile_point_boxes:
            clipped = clipped_tile_bbox(dataset, bbox)
            if clipped is None:
                continue
            point_window = JOIN.window_for_bounds(dataset, *clipped)
            if point_window is not None:
                tile_point_windows.append((point, bbox, point_window))
        if not tile_point_windows:
            continue

        tile_has_cells = False
        for window in block_windows_for_point_windows(dataset, tile_point_windows):
            block_bbox = window_bounds(window, dataset.transform)
            block_point_windows = [
                (point, bbox, point_window)
                for point, bbox, point_window in tile_point_windows
                if intersects(bbox, block_bbox)
            ]
            if not block_point_windows:
                continue

            mask = np.zeros((int(window.height), int(window.width)), dtype=bool)
            for point, _, point_window in block_point_windows:
                point_mask = JOIN.local_distance_mask(dataset, window, point.latitude, point.longitude, radius_km)
                mask |= point_mask & point_window_mask(window, point_window)
            if not mask.any():
                continue

            values = dataset.read(1, window=window, masked=True)
            data = np.asarray(values.filled(np.nan), dtype="float64")
            selected = data[mask]
            selected = selected[np.isfinite(selected) & (selected > 0)]
            windows_scanned += 1
            if selected.size:
                total += float(selected.sum())
                positive_cells += int(selected.size)
                windows_with_cells += 1
                tile_has_cells = True

        if tile_has_cells:
            tile_ids.append(raster.tile_id)

    return {
        "unioned_population_sum": total,
        "unioned_positive_cells": positive_cells,
        "unioned_population_tiles": "||".join(sorted(set(tile_ids))),
        "unioned_population_tile_count": len(set(tile_ids)),
        "unioned_population_windows_scanned": windows_scanned,
        "unioned_population_windows_with_cells": windows_with_cells,
        "country_union_population_computed": windows_scanned > 0,
    }


def unioned_pm25(points: list[Any], radius_km: float, grid: Any) -> dict[str, Any]:
    bboxes = [JOIN.bbox_for_radius(point.latitude, point.longitude, radius_km) for point in points]
    west = min(bbox[0] for bbox in bboxes)
    south = min(bbox[1] for bbox in bboxes)
    east = max(bbox[2] for bbox in bboxes)
    north = max(bbox[3] for bbox in bboxes)

    lat_mask = (grid.lat >= south) & (grid.lat <= north)
    lon_mask = (grid.lon >= west) & (grid.lon <= east)
    lat_values = grid.lat[lat_mask]
    lon_values = grid.lon[lon_mask]
    if not lat_values.size or not lon_values.size:
        return {
            "unioned_pm25_cell_mean_ugm3": None,
            "unioned_pm25_cell_count": 0,
            "unioned_pm25_computed": False,
        }

    lat_mesh, lon_mesh = np.meshgrid(lat_values, lon_values, indexing="ij")
    union_mask = np.zeros(lat_mesh.shape, dtype=bool)
    for point in points:
        distances = JOIN.haversine_distance(lat_mesh, lon_mesh, point.latitude, point.longitude)
        union_mask |= distances <= radius_km

    values = grid.pm25[np.ix_(lat_mask, lon_mask)][union_mask]
    values = values[np.isfinite(values)]
    if not values.size:
        return {
            "unioned_pm25_cell_mean_ugm3": None,
            "unioned_pm25_cell_count": 0,
            "unioned_pm25_computed": False,
        }
    return {
        "unioned_pm25_cell_mean_ugm3": float(values.mean()),
        "unioned_pm25_cell_count": int(values.size),
        "unioned_pm25_computed": True,
    }


def ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def evidence_gates(counts: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "Country-unioned GHSL catchment denominator",
            "status": "computed_dry_run",
            "rows": counts["country_union_rows_computed"],
            "reader_use": "Each GHSL population cell is counted at most once within an economy/radius band.",
        },
        {
            "gate": "Row-level denominator comparison",
            "status": "computed",
            "rows": counts["row_level_country_radius_rows_read"],
            "reader_use": "The dry run preserves the prior buffer-sum and exact-coordinate-dedup diagnostics for comparison.",
        },
        {
            "gate": "ACAG PM2.5 union-cell context",
            "status": "computed_dry_run",
            "rows": counts["country_union_pm25_rows_computed"],
            "reader_use": "PM2.5 is averaged across coarse ACAG cells inside candidate buffers; it is contextual, not exposure.",
        },
        {
            "gate": "Validated same-station joins",
            "status": "not_ready",
            "rows": counts["validated_same_station_join_rows"],
            "reader_use": "No official/OpenAQ proximity row is promoted to a same-station identity.",
        },
        {
            "gate": "Complete monitor-grade rows",
            "status": "not_ready",
            "rows": counts["complete_monitor_grade_rows"],
            "reader_use": "No coordinate row is promoted to complete regulatory-grade evidence.",
        },
        {
            "gate": "Coverage claim",
            "status": "blocked",
            "rows": 0,
            "reader_use": "The public surface may show denominator geometry, not people served or protected by monitors.",
        },
    ]


def row_reader_use(radius_role: str) -> str:
    if radius_role == "primary":
        return "Primary 4 km country-unioned candidate catchment denominator; not monitor coverage."
    if radius_role == "lower_sensitivity":
        return "Lower 0.5 km sensitivity country-unioned denominator; not monitor coverage."
    return "Upper 50 km sensitivity country-unioned denominator; not a service area."


def write_markdown(path: Path, summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    top = summary["top_primary_radius_country_rows"]
    lines = [
        "# Air Monitoring Station-Radius Country-Unioned Catchment Dry Run",
        "",
        "attestation_chain: ai-first",
        "",
        "## Status",
        "",
        (
            "This pass turns the row-level denominator join into a country-unioned "
            "candidate catchment diagnostic. It removes overlap among candidate "
            "buffers within each economy/radius band, but it remains outside any "
            "coverage or exposure claim."
        ),
        "",
        "## Evidence Counts",
        "",
        "| Check | Count |",
        "|---|---:|",
        f"| Country-radius union rows | {counts['country_union_rows_computed']} |",
        f"| Coordinate rows represented | {counts['coordinate_rows_used']} |",
        f"| Unique coordinate points represented | {counts['unique_coordinate_points']} |",
        f"| Radius bands computed | {counts['radius_bands_computed']} |",
        f"| GHSL tiles opened | {counts['population_raster_tiles_opened']} |",
        f"| ACAG PM2.5 union rows computed | {counts['country_union_pm25_rows_computed']} |",
        f"| Validated same-station joins | {counts['validated_same_station_join_rows']} |",
        f"| Complete monitor-grade rows | {counts['complete_monitor_grade_rows']} |",
        f"| Coverage claim allowed | {counts['coverage_claim_allowed']} |",
        "",
        "## Primary 4 km Unioned Diagnostic Rows",
        "",
        (
            "These rows compare the prior row-level buffer sum with the new unioned "
            "GHSL-cell denominator. The difference is duplicate candidate-buffer "
            "mass, not people newly covered or uncovered by monitors."
        ),
        "",
        "| Economy | Coordinates | Unioned population | Row buffer sum | Row/union multiplier | Mean ACAG PM2.5 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in top:
        lines.append(
            "| "
            f"{row['iso3']} | "
            f"{row['coordinate_rows']} | "
            f"{row['unioned_population_sum']} | "
            f"{row['row_level_candidate_population_buffer_sum']} | "
            f"{row['row_to_union_population_multiplier']} | "
            f"{row['unioned_pm25_cell_mean_ugm3']} |"
        )
    lines.extend(
        [
            "",
            "## Gate Ledger",
            "",
            "| Gate | Status | Rows | Reader use |",
            "|---|---|---:|---|",
        ]
    )
    for gate in summary["evidence_gate_counts"]:
        lines.append(f"| {gate['gate']} | {gate['status']} | {gate['rows']} | {gate['reader_use']} |")
    lines.extend(
        [
            "",
            "## What This Does Not Mean",
            "",
            summary["non_claim"],
            "",
            "## Reproduce",
            "",
            "```powershell",
            "python air-monitoring\\scripts\\build-station-radius-country-unioned-catchment-dry-run.py",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    join_summary = json.loads(JOIN_SUMMARY_JSON.read_text(encoding="utf-8"))
    join_country_rows = read_csv(JOIN_COUNTRY_CSV)
    join_country_by_key = {
        (row["iso3"], float(row["radius_km"])): row
        for row in join_country_rows
    }

    radii = JOIN.radius_bands()
    coordinates = JOIN.load_coordinate_inputs()
    rasters = JOIN.load_population_rasters()
    grid = JOIN.load_pm25_grid()
    by_country: dict[str, list[Any]] = defaultdict(list)
    for point in coordinates:
        by_country[point.iso3].append(point)

    rows: list[dict[str, Any]] = []
    for iso3, points in sorted(by_country.items()):
        country = points[0].country
        source_counter = Counter(point.source_family for point in points)
        for radius in radii:
            radius_km = float(radius["radius_km"])
            population = unioned_population(points, radius_km, rasters)
            pm25 = unioned_pm25(points, radius_km, grid)
            prior = join_country_by_key.get((iso3, radius_km), {})
            row_sum = parse_float(prior.get("candidate_population_buffer_sum")) or 0.0
            exact_sum = parse_float(prior.get("candidate_population_exact_coordinate_dedup_sum")) or 0.0
            union_sum = float(population["unioned_population_sum"])
            rows.append(
                {
                    "generated_at": generated_at,
                    "attestation_chain": ATTESTATION,
                    "status": STATUS,
                    "method": METHOD,
                    "row_type": "country_unioned_candidate_catchment",
                    "iso3": iso3,
                    "country": country,
                    "radius_km": radius_km,
                    "radius_role": radius["radius_role"],
                    "coordinate_rows": len(points),
                    "unique_coordinate_points": len({point.coordinate_key for point in points}),
                    "openaq_coordinate_rows": source_counter["openaq"],
                    "official_pm25_coordinate_rows": source_counter["official_pm25_station"],
                    "source_family_mix": "||".join(sorted(source_counter)),
                    "unioned_population_sum": round_number(union_sum, 3),
                    "unioned_positive_cells": population["unioned_positive_cells"],
                    "unioned_population_tiles": population["unioned_population_tiles"],
                    "unioned_population_tile_count": population["unioned_population_tile_count"],
                    "unioned_population_windows_scanned": population["unioned_population_windows_scanned"],
                    "unioned_population_windows_with_cells": population["unioned_population_windows_with_cells"],
                    "row_level_candidate_population_buffer_sum": round_number(row_sum, 3),
                    "row_level_exact_coordinate_dedup_sum": round_number(exact_sum, 3),
                    "row_to_union_population_multiplier": round_number(ratio(row_sum, union_sum), 3),
                    "exact_dedup_to_union_population_multiplier": round_number(ratio(exact_sum, union_sum), 3),
                    "population_overlap_removed_from_row_sum": round_number(max(0.0, row_sum - union_sum), 3),
                    "population_overlap_removed_from_exact_dedup_sum": round_number(max(0.0, exact_sum - union_sum), 3),
                    "unioned_pm25_cell_mean_ugm3": round_number(pm25["unioned_pm25_cell_mean_ugm3"], 3),
                    "unioned_pm25_cell_count": pm25["unioned_pm25_cell_count"],
                    "unioned_pm25_computed": pm25["unioned_pm25_computed"],
                    "country_union_population_computed": population["country_union_population_computed"],
                    "coverage_claim_allowed": False,
                    "validated_same_station_join_rows": join_summary["coverage_counts"]["validated_same_station_join_rows"],
                    "complete_monitor_grade_rows": join_summary["coverage_counts"]["complete_monitor_grade_rows"],
                    "station_radius_ready": False,
                    "reader_use": row_reader_use(str(radius["radius_role"])),
                    "blocking_gap": (
                        "Unioned denominator geometry now exists, but same-station validation, complete "
                        "monitor-grade evidence, and a coverage-claim gate remain blocked."
                    ),
                    "non_claim": NON_CLAIM,
                }
            )

    for raster in rasters:
        raster.dataset.close()

    primary_radius = next(radius["radius_km"] for radius in radii if radius["radius_role"] == "primary")
    primary_rows = [row for row in rows if float(row["radius_km"]) == float(primary_radius)]
    top_primary = sorted(
        primary_rows,
        key=lambda row: parse_float(row.get("unioned_population_sum")) or 0.0,
        reverse=True,
    )[:8]

    counts = {
        "coordinate_economies": len(by_country),
        "coordinate_rows_used": len(coordinates),
        "unique_coordinate_points": len({point.coordinate_key for point in coordinates}),
        "openaq_coordinate_rows_used": sum(1 for point in coordinates if point.source_family == "openaq"),
        "official_pm25_coordinate_rows_used": sum(
            1 for point in coordinates if point.source_family == "official_pm25_station"
        ),
        "radius_bands_computed": len(radii),
        "row_level_country_radius_rows_read": len(join_country_rows),
        "country_union_rows_computed": len(rows),
        "country_union_population_rows_computed": sum(
            1 for row in rows if str(row.get("country_union_population_computed")).casefold() == "true"
        ),
        "country_union_pm25_rows_computed": sum(
            1 for row in rows if str(row.get("unioned_pm25_computed")).casefold() == "true"
        ),
        "population_raster_tiles_opened": join_summary["coverage_counts"]["population_raster_tiles_opened"],
        "acag_pm25_surface_opened": join_summary["coverage_counts"]["acag_pm25_surface_opened"],
        "primary_radius_km": primary_radius,
        "lower_sensitivity_radius_km": next(
            radius["radius_km"] for radius in radii if radius["radius_role"] == "lower_sensitivity"
        ),
        "upper_sensitivity_radius_km": next(
            radius["radius_km"] for radius in radii if radius["radius_role"] == "upper_sensitivity"
        ),
        "validated_same_station_join_rows": join_summary["coverage_counts"]["validated_same_station_join_rows"],
        "complete_monitor_grade_rows": join_summary["coverage_counts"]["complete_monitor_grade_rows"],
        "station_radius_ready_economies": 0,
        "coverage_claim_allowed": False,
    }
    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": GOAL_LEVEL,
        "source_inputs": [
            {"path": source_ref(JOIN_SUMMARY_JSON), "role": "row-level denominator join dry-run summary"},
            {"path": source_ref(JOIN_COUNTRY_CSV), "role": "row-level country-radius denominator diagnostics"},
            {"path": source_ref(JOIN.JOIN_SCRIPT if hasattr(JOIN, "JOIN_SCRIPT") else JOIN_SCRIPT), "role": "denominator join helper script"},
        ],
        "method_notes": [
            "For each economy/radius band, GHSL population cells are counted once if their cell center falls inside at least one candidate coordinate buffer.",
            f"Population union masks are evaluated in {BLOCK_SIZE} by {BLOCK_SIZE} raster blocks to avoid loading full GHSL tiles.",
            "The comparison columns retain the row-level buffer sum and exact-coordinate deduplicated sum from the prior dry run.",
            "The ACAG PM2.5 field is a coarse grid-cell context mean inside the same candidate union, not exposure or station measurement.",
        ],
        "coverage_counts": counts,
        "evidence_gate_counts": evidence_gates(counts),
        "radius_bands": radii,
        "top_primary_radius_country_rows": top_primary,
        "country_rows": rows,
        "outputs": {
            "country_union_csv": source_ref(OUT_COUNTRY_CSV),
            "summary_json": source_ref(OUT_JSON),
            "evidence_md": source_ref(OUT_MD),
        },
        "non_claim": NON_CLAIM,
    }

    write_csv(OUT_COUNTRY_CSV, rows, COUNTRY_FIELDS)
    write_json(OUT_JSON, summary)
    write_markdown(OUT_MD, summary)
    return summary


def main() -> None:
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built station-radius country-unioned catchment dry run: "
        f"{counts['country_union_rows_computed']} country-radius rows, "
        f"{counts['country_union_population_rows_computed']} population unions, "
        f"{counts['country_union_pm25_rows_computed']} ACAG union rows, "
        f"{counts['station_radius_ready_economies']} ready economies."
    )


if __name__ == "__main__":
    main()
