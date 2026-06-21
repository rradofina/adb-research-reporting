"""Build the station-radius denominator join dry-run.

This pass physically joins the frozen candidate coordinate universe to the
cached GHSL population tiles and ACAG coarse annual PM2.5 grid. It remains a
dry run: the output is row-level denominator diagnostics, not monitor coverage.
"""

from __future__ import annotations

import csv
import json
import math
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import netCDF4
import numpy as np
import rasterio
from rasterio.windows import Window, from_bounds


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"

READINESS_CSV = GENERATED / "air-monitoring-station-radius-denominator-readiness.csv"
OPENAQ_CSV = GENERATED / "air-monitoring-openaq-station-metadata.csv"
OFFICIAL_CSV = GENERATED / "air-monitoring-regulator-station-extraction.csv"
ROUTING_COUNTRY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-tile-routing-correction-country.csv"
CORRECTED_CUSTODY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-corrected-population-tile-custody.csv"
LARGE_CUSTODY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-large-population-tile-custody.csv"
ACAG_CHECKSUM_CSV = GENERATED / "air-monitoring-station-radius-acag-coarse-checksums.csv"
METHOD_PREFREEZE_SUMMARY = GENERATED / "air-monitoring-station-radius-method-prefreeze-summary.json"
RADIUS_RULE_SUMMARY = GENERATED / "air-monitoring-station-radius-radius-rule-source-scan-summary.json"
PM25_RESOLUTION_SUMMARY = GENERATED / "air-monitoring-station-radius-pm25-resolution-decision-summary.json"
RECON_SUMMARY = GENERATED / "air-monitoring-official-openaq-reconciliation-summary.json"
GRADE_SUMMARY = GENERATED / "air-monitoring-station-grade-decision-ledger-summary.json"

OUT_ROW_CSV = GENERATED / "air-monitoring-station-radius-denominator-join-dry-run.csv"
OUT_COUNTRY_CSV = GENERATED / "air-monitoring-station-radius-denominator-join-dry-run-country.csv"
OUT_JSON = GENERATED / "air-monitoring-station-radius-denominator-join-dry-run-summary.json"
OUT_MD = PROGRAM / "station-radius-denominator-join-dry-run.md"

STATUS = "computed_station_radius_denominator_join_dry_run"
METHOD = "air_monitoring_station_radius_denominator_join_dry_run_v1"
ATTESTATION = "ai-first"
GOAL_LEVEL = "L3 station-radius denominator join dry run"
EARTH_RADIUS_KM = 6371.0088

NON_CLAIM = (
    "This denominator join dry run attaches the frozen candidate coordinate "
    "universe to cached GHSL population cells and the selected ACAG coarse "
    "annual PM2.5 grid. It reports candidate-row denominator diagnostics only. "
    "It does not validate same-station joins, does not classify complete "
    "monitor grade, does not compute unioned monitor catchment coverage, and "
    "does not support a population-served, exposure, or official monitor "
    "coverage claim."
)

ROW_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "row_type",
    "coordinate_id",
    "coordinate_key",
    "iso3",
    "country",
    "source_family",
    "source_row_id",
    "station_name",
    "latitude",
    "longitude",
    "radius_km",
    "radius_role",
    "ghsl_population_sum",
    "ghsl_positive_cells",
    "ghsl_window_count",
    "ghsl_tile_ids",
    "ghsl_population_computed",
    "acag_record_key",
    "acag_selected_vintage",
    "pm25_nearest_ugm3",
    "pm25_radius_mean_ugm3",
    "pm25_radius_cell_count",
    "pm25_computed",
    "join_stage",
    "claim_allowed",
    "validated_same_station_join_rows",
    "complete_monitor_grade_rows",
    "station_radius_ready",
    "reader_use",
    "blocking_gap",
    "non_claim",
]

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
    "population_rows_computed",
    "pm25_rows_computed",
    "candidate_population_buffer_sum",
    "candidate_population_exact_coordinate_dedup_sum",
    "mean_pm25_nearest_ugm3",
    "mean_pm25_radius_ugm3",
    "ghsl_tile_count",
    "ghsl_tile_ids",
    "country_union_population_computed",
    "coverage_claim_allowed",
    "validated_same_station_join_rows",
    "complete_monitor_grade_rows",
    "station_radius_ready",
    "reader_use",
    "blocking_gap",
    "non_claim",
]


@dataclass(frozen=True)
class CoordinateInput:
    coordinate_id: str
    coordinate_key: str
    iso3: str
    country: str
    source_family: str
    source_row_id: str
    station_name: str
    latitude: float
    longitude: float


@dataclass
class PopulationRaster:
    tile_id: str
    source_path: str
    sha256: str
    dataset: Any


@dataclass
class Pm25Grid:
    record_key: str
    selected_vintage: str
    source_path: str
    lat: np.ndarray
    lon: np.ndarray
    pm25: np.ndarray


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def truthy(value: Any) -> bool:
    return str(value or "").strip().casefold() in {"true", "1", "yes", "y"}


def parse_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def parse_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def round_number(value: float | None, digits: int = 3) -> float | str:
    if value is None or not math.isfinite(value):
        return ""
    return round(float(value), digits)


def source_ref(path: Path) -> str:
    return str(path.relative_to(PROGRAM)).replace("\\", "/")


def radius_bands() -> list[dict[str, Any]]:
    summary = read_json(RADIUS_RULE_SUMMARY)
    counts = summary["coverage_counts"]
    values = [
        ("lower_sensitivity", float(counts["lower_sensitivity_radius_km"])),
        ("primary", float(counts["primary_radius_km"])),
        ("upper_sensitivity", float(counts["upper_sensitivity_radius_km"])),
    ]
    return [{"radius_role": role, "radius_km": radius} for role, radius in values]


def load_coordinate_inputs() -> list[CoordinateInput]:
    readiness = {row["iso3"]: row for row in read_csv(READINESS_CSV)}
    inputs: list[CoordinateInput] = []

    for index, row in enumerate(read_csv(OPENAQ_CSV), start=1):
        lat = parse_float(row.get("latitude"))
        lon = parse_float(row.get("longitude"))
        if (
            lat is None
            or lon is None
            or row.get("iso3") not in readiness
            or not truthy(row.get("station_radius_coordinate_input_available"))
            or not truthy(row.get("coordinate_in_target_country_bbox"))
        ):
            continue
        source_row_id = row.get("openaq_location_id", "") or f"openaq_{index}"
        coordinate_key = f"{row['iso3']}:{lat:.6f},{lon:.6f}"
        coordinate_id = f"openaq:{row['iso3']}:{source_row_id}:{lat:.6f}:{lon:.6f}"
        inputs.append(
            CoordinateInput(
                coordinate_id=coordinate_id,
                coordinate_key=coordinate_key,
                iso3=row["iso3"],
                country=row["country"],
                source_family="openaq",
                source_row_id=source_row_id,
                station_name=row.get("openaq_location_name", ""),
                latitude=lat,
                longitude=lon,
            )
        )

    for index, row in enumerate(read_csv(OFFICIAL_CSV), start=1):
        lat = parse_float(row.get("latitude"))
        lon = parse_float(row.get("longitude"))
        if (
            lat is None
            or lon is None
            or row.get("iso3") not in readiness
            or not truthy(row.get("coordinate_available"))
            or not truthy(row.get("pm25_signal"))
        ):
            continue
        source_row_id = row.get("source_station_id", "") or f"official_{index}"
        coordinate_key = f"{row['iso3']}:{lat:.6f},{lon:.6f}"
        coordinate_id = f"official_pm25_station:{row['iso3']}:{source_row_id}:{lat:.6f}:{lon:.6f}"
        inputs.append(
            CoordinateInput(
                coordinate_id=coordinate_id,
                coordinate_key=coordinate_key,
                iso3=row["iso3"],
                country=row["country"],
                source_family="official_pm25_station",
                source_row_id=source_row_id,
                station_name=row.get("source_station_name", ""),
                latitude=lat,
                longitude=lon,
            )
        )

    return sorted(inputs, key=lambda item: (item.iso3, item.source_family, item.source_row_id, item.latitude, item.longitude))


def zip_member(path: Path, declared_members: str) -> str:
    declared = [item for item in str(declared_members or "").split("||") if item]
    if declared:
        return declared[0]
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.lower().endswith((".tif", ".tiff")):
                return name
    raise FileNotFoundError(f"No GeoTIFF member found in {path}")


def cache_path(value: str) -> Path:
    normalized = value.replace("\\", "/")
    if normalized.startswith(".cache/"):
        return PROGRAM / normalized
    return ROOT / normalized


def load_population_rasters() -> list[PopulationRaster]:
    rows = []
    for csv_path in (CORRECTED_CUSTODY_CSV, LARGE_CUSTODY_CSV):
        rows.extend(read_csv(csv_path))

    rasters: list[PopulationRaster] = []
    seen: set[str] = set()
    for row in rows:
        tile_id = row.get("tile_id", "")
        if (
            not tile_id
            or tile_id in seen
            or not truthy(row.get("downloaded"))
            or not truthy(row.get("transform_matches_corrected_tile_bounds"))
        ):
            continue
        path = cache_path(row.get("cache_path", ""))
        member = zip_member(path, row.get("geotiff_members", ""))
        dataset = rasterio.open(f"zip://{path.as_posix()}!{member}")
        rasters.append(
            PopulationRaster(
                tile_id=tile_id,
                source_path=str(path.relative_to(PROGRAM)).replace("\\", "/"),
                sha256=row.get("sha256", ""),
                dataset=dataset,
            )
        )
        seen.add(tile_id)
    return sorted(rasters, key=lambda item: item.tile_id)


def load_pm25_grid() -> Pm25Grid:
    selected = None
    for row in read_csv(ACAG_CHECKSUM_CSV):
        if row.get("record_key") == "v6gl03_gl_coarse_annual":
            selected = row
            break
    if selected is None:
        selected = next(row for row in read_csv(ACAG_CHECKSUM_CSV) if truthy(row.get("downloaded")))

    path = cache_path(selected["cache_path"])
    with netCDF4.Dataset(path) as dataset:
        lat = np.array(dataset.variables["lat"][:], dtype="float64")
        lon = np.array(dataset.variables["lon"][:], dtype="float64")
        pm25 = np.array(dataset.variables["PM25"][:], dtype="float64")
    pm25[pm25 < -100] = np.nan
    return Pm25Grid(
        record_key=selected["record_key"],
        selected_vintage=selected.get("selected_vintage", ""),
        source_path=str(path.relative_to(PROGRAM)).replace("\\", "/"),
        lat=lat,
        lon=lon,
        pm25=pm25,
    )


def bbox_for_radius(lat: float, lon: float, radius_km: float) -> tuple[float, float, float, float]:
    lat_buffer = radius_km / 111.32
    lon_buffer = radius_km / (111.32 * max(0.15, math.cos(math.radians(lat))))
    return lon - lon_buffer, lat - lat_buffer, lon + lon_buffer, lat + lat_buffer


def window_for_bounds(dataset: Any, west: float, south: float, east: float, north: float) -> Window | None:
    bounds = dataset.bounds
    if east < bounds.left or west > bounds.right or north < bounds.bottom or south > bounds.top:
        return None
    clipped_west = max(west, bounds.left)
    clipped_east = min(east, bounds.right)
    clipped_south = max(south, bounds.bottom)
    clipped_north = min(north, bounds.top)
    window = from_bounds(clipped_west, clipped_south, clipped_east, clipped_north, dataset.transform)
    window = window.round_offsets().round_lengths()
    row_off = max(0, int(window.row_off))
    col_off = max(0, int(window.col_off))
    height = min(dataset.height - row_off, int(window.height))
    width = min(dataset.width - col_off, int(window.width))
    if height <= 0 or width <= 0:
        return None
    return Window(col_off, row_off, width, height)


def local_distance_mask(
    dataset: Any,
    window: Window,
    lat: float,
    lon: float,
    radius_km: float,
) -> np.ndarray:
    row_start = int(window.row_off)
    col_start = int(window.col_off)
    height = int(window.height)
    width = int(window.width)
    rows = np.arange(row_start, row_start + height, dtype="float64") + 0.5
    cols = np.arange(col_start, col_start + width, dtype="float64") + 0.5
    x_values = dataset.transform.c + dataset.transform.a * cols
    y_values = dataset.transform.f + dataset.transform.e * rows
    cos_lat = max(0.15, math.cos(math.radians(lat)))
    dx = (x_values[None, :] - lon) * 111.32 * cos_lat
    dy = (y_values[:, None] - lat) * 111.32
    return (dx * dx + dy * dy) <= radius_km * radius_km


def sample_population(
    point: CoordinateInput,
    radius_km: float,
    rasters: list[PopulationRaster],
) -> dict[str, Any]:
    west, south, east, north = bbox_for_radius(point.latitude, point.longitude, radius_km)
    total = 0.0
    positive_cells = 0
    window_count = 0
    tile_ids: list[str] = []

    for raster in rasters:
        dataset = raster.dataset
        window = window_for_bounds(dataset, west, south, east, north)
        if window is None:
            continue
        values = dataset.read(1, window=window, masked=True)
        mask = local_distance_mask(dataset, window, point.latitude, point.longitude, radius_km)
        data = np.asarray(values.filled(np.nan), dtype="float64")
        selected = data[mask]
        selected = selected[np.isfinite(selected) & (selected > 0)]
        if selected.size:
            total += float(selected.sum())
            positive_cells += int(selected.size)
            tile_ids.append(raster.tile_id)
        window_count += 1

    return {
        "ghsl_population_sum": total,
        "ghsl_positive_cells": positive_cells,
        "ghsl_window_count": window_count,
        "ghsl_tile_ids": "||".join(sorted(set(tile_ids))),
        "ghsl_population_computed": window_count > 0,
    }


def haversine_distance(lat_grid: np.ndarray, lon_grid: np.ndarray, lat: float, lon: float) -> np.ndarray:
    lat1 = np.radians(lat)
    lat2 = np.radians(lat_grid)
    dlat = lat2 - lat1
    dlon = np.radians(lon_grid - lon)
    a = np.sin(dlat / 2.0) ** 2 + math.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    return 2.0 * EARTH_RADIUS_KM * np.arcsin(np.minimum(1.0, np.sqrt(a)))


def sample_pm25(point: CoordinateInput, radius_km: float, grid: Pm25Grid) -> dict[str, Any]:
    lat_index = int(np.abs(grid.lat - point.latitude).argmin())
    lon_index = int(np.abs(grid.lon - point.longitude).argmin())
    nearest = float(grid.pm25[lat_index, lon_index])
    if not math.isfinite(nearest):
        nearest_value: float | None = None
    else:
        nearest_value = nearest

    west, south, east, north = bbox_for_radius(point.latitude, point.longitude, radius_km)
    lat_mask = (grid.lat >= south) & (grid.lat <= north)
    lon_mask = (grid.lon >= west) & (grid.lon <= east)
    lat_values = grid.lat[lat_mask]
    lon_values = grid.lon[lon_mask]
    radius_mean: float | None = None
    cell_count = 0
    if lat_values.size and lon_values.size:
        lat_mesh, lon_mesh = np.meshgrid(lat_values, lon_values, indexing="ij")
        distances = haversine_distance(lat_mesh, lon_mesh, point.latitude, point.longitude)
        within = distances <= radius_km
        subset = grid.pm25[np.ix_(lat_mask, lon_mask)]
        values = subset[within]
        values = values[np.isfinite(values)]
        cell_count = int(values.size)
        if values.size:
            radius_mean = float(values.mean())

    return {
        "pm25_nearest_ugm3": nearest_value,
        "pm25_radius_mean_ugm3": radius_mean,
        "pm25_radius_cell_count": cell_count,
        "pm25_computed": nearest_value is not None,
    }


def row_reader_use(radius_role: str) -> str:
    if radius_role == "primary":
        return "Candidate-row denominator diagnostic for the source-frozen 4 km PM2.5 neighborhood-scale band."
    if radius_role == "lower_sensitivity":
        return "Candidate-row denominator diagnostic for the lower 0.5 km sensitivity band."
    return "Candidate-row denominator diagnostic for the 50 km upper sensitivity band; not a service area."


def build_row(
    generated_at: str,
    point: CoordinateInput,
    radius: dict[str, Any],
    population: dict[str, Any],
    pm25: dict[str, Any],
    grid: Pm25Grid,
    validated_join_rows: int,
    complete_grade_rows: int,
) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "row_type": "candidate_coordinate_radius",
        "coordinate_id": point.coordinate_id,
        "coordinate_key": point.coordinate_key,
        "iso3": point.iso3,
        "country": point.country,
        "source_family": point.source_family,
        "source_row_id": point.source_row_id,
        "station_name": point.station_name,
        "latitude": round_number(point.latitude, 6),
        "longitude": round_number(point.longitude, 6),
        "radius_km": radius["radius_km"],
        "radius_role": radius["radius_role"],
        "ghsl_population_sum": round_number(population["ghsl_population_sum"], 3),
        "ghsl_positive_cells": population["ghsl_positive_cells"],
        "ghsl_window_count": population["ghsl_window_count"],
        "ghsl_tile_ids": population["ghsl_tile_ids"],
        "ghsl_population_computed": population["ghsl_population_computed"],
        "acag_record_key": grid.record_key,
        "acag_selected_vintage": grid.selected_vintage,
        "pm25_nearest_ugm3": round_number(pm25["pm25_nearest_ugm3"], 3),
        "pm25_radius_mean_ugm3": round_number(pm25["pm25_radius_mean_ugm3"], 3),
        "pm25_radius_cell_count": pm25["pm25_radius_cell_count"],
        "pm25_computed": pm25["pm25_computed"],
        "join_stage": "candidate_coordinate_denominator_join",
        "claim_allowed": False,
        "validated_same_station_join_rows": validated_join_rows,
        "complete_monitor_grade_rows": complete_grade_rows,
        "station_radius_ready": False,
        "reader_use": row_reader_use(radius["radius_role"]),
        "blocking_gap": (
            "The denominator join is physical, but same-station identity, monitor-grade "
            "classification, and unioned country catchment coverage remain blocked."
        ),
        "non_claim": NON_CLAIM,
    }


def country_rows(
    generated_at: str,
    row_records: list[dict[str, Any]],
    coordinates: list[CoordinateInput],
    validated_join_rows: int,
    complete_grade_rows: int,
) -> list[dict[str, Any]]:
    coord_by_country = defaultdict(list)
    for point in coordinates:
        coord_by_country[point.iso3].append(point)

    grouped: dict[tuple[str, float], list[dict[str, Any]]] = defaultdict(list)
    for row in row_records:
        grouped[(str(row["iso3"]), float(row["radius_km"]))].append(row)

    country_name = {point.iso3: point.country for point in coordinates}
    results: list[dict[str, Any]] = []
    for (iso3, radius_km), rows in sorted(grouped.items()):
        points = coord_by_country[iso3]
        role = str(rows[0]["radius_role"]) if rows else ""
        unique_values: dict[str, float] = {}
        for row in rows:
            key = str(row["coordinate_key"])
            value = parse_float(row.get("ghsl_population_sum")) or 0.0
            unique_values.setdefault(key, value)
        nearest_values = [parse_float(row.get("pm25_nearest_ugm3")) for row in rows]
        nearest_values = [value for value in nearest_values if value is not None and math.isfinite(value)]
        mean_values = [parse_float(row.get("pm25_radius_mean_ugm3")) for row in rows]
        mean_values = [value for value in mean_values if value is not None and math.isfinite(value)]
        tile_ids = sorted(
            {
                tile
                for row in rows
                for tile in str(row.get("ghsl_tile_ids", "")).split("||")
                if tile
            }
        )
        population_sum = sum(parse_float(row.get("ghsl_population_sum")) or 0.0 for row in rows)
        dedup_sum = sum(unique_values.values())
        results.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "row_type": "country_radius_summary",
                "iso3": iso3,
                "country": country_name.get(iso3, ""),
                "radius_km": radius_km,
                "radius_role": role,
                "coordinate_rows": len(rows),
                "unique_coordinate_points": len({point.coordinate_key for point in points}),
                "openaq_coordinate_rows": sum(1 for point in points if point.source_family == "openaq"),
                "official_pm25_coordinate_rows": sum(
                    1 for point in points if point.source_family == "official_pm25_station"
                ),
                "population_rows_computed": sum(1 for row in rows if truthy(row.get("ghsl_population_computed"))),
                "pm25_rows_computed": sum(1 for row in rows if truthy(row.get("pm25_computed"))),
                "candidate_population_buffer_sum": round_number(population_sum, 3),
                "candidate_population_exact_coordinate_dedup_sum": round_number(dedup_sum, 3),
                "mean_pm25_nearest_ugm3": round_number(float(np.mean(nearest_values)) if nearest_values else None, 3),
                "mean_pm25_radius_ugm3": round_number(float(np.mean(mean_values)) if mean_values else None, 3),
                "ghsl_tile_count": len(tile_ids),
                "ghsl_tile_ids": "||".join(tile_ids),
                "country_union_population_computed": False,
                "coverage_claim_allowed": False,
                "validated_same_station_join_rows": validated_join_rows,
                "complete_monitor_grade_rows": complete_grade_rows,
                "station_radius_ready": False,
                "reader_use": (
                    "Country summary of row-level candidate denominators. Exact duplicate coordinate "
                    "points are collapsed in one diagnostic column, but overlapping buffers are not "
                    "unioned and this is not monitor coverage."
                ),
                "blocking_gap": (
                    "Country-level unioned catchments, station identity validation, and monitor-grade "
                    "evidence remain blocked."
                ),
                "non_claim": NON_CLAIM,
            }
        )
    return results


def evidence_gates(counts: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "Coordinate input universe",
            "status": "computed",
            "rows": counts["coordinate_rows_used"],
            "reader_use": "Frozen OpenAQ and official PM2.5 coordinate rows were physically joined to denominators.",
        },
        {
            "gate": "Radius bands",
            "status": "computed",
            "rows": counts["radius_bands_computed"],
            "reader_use": "The source-frozen 0.5 km, 4 km, and 50 km bands are evaluated at row level.",
        },
        {
            "gate": "GHSL population denominator join",
            "status": "computed_dry_run",
            "rows": counts["population_rows_computed"],
            "reader_use": "GHSL cells are summed inside candidate-row buffers, not unioned into country coverage.",
        },
        {
            "gate": "ACAG PM2.5 denominator join",
            "status": "computed_dry_run",
            "rows": counts["pm25_rows_computed"],
            "reader_use": "The selected coarse annual ACAG grid is sampled as contextual PM2.5, not station measurement.",
        },
        {
            "gate": "Validated same-station joins",
            "status": "not_ready",
            "rows": counts["validated_same_station_join_rows"],
            "reader_use": "No candidate official/OpenAQ proximity row is promoted to station identity.",
        },
        {
            "gate": "Complete monitor-grade rows",
            "status": "not_ready",
            "rows": counts["complete_monitor_grade_rows"],
            "reader_use": "No coordinate row can yet be used as complete regulatory-grade evidence.",
        },
        {
            "gate": "Unioned country catchment coverage",
            "status": "not_computed",
            "rows": 0,
            "reader_use": "Overlapping buffers are not unioned; the public surface must not report people covered.",
        },
    ]


def write_markdown(path: Path, summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    gates = summary["evidence_gate_counts"]
    top = summary["top_primary_radius_country_rows"]
    lines = [
        "# Air Monitoring Station-Radius Denominator Join Dry Run",
        "",
        "attestation_chain: ai-first",
        "",
        "## Status",
        "",
        (
            "This dry run physically joins the frozen candidate coordinate universe to "
            "cached GHSL population cells and the selected ACAG V6.GL.03 2023 coarse "
            "annual PM2.5 grid. It is a denominator diagnostic, not a monitor-coverage result."
        ),
        "",
        "## Evidence Counts",
        "",
        "| Check | Count |",
        "|---|---:|",
        f"| Candidate coordinate rows | {counts['coordinate_rows_used']} |",
        f"| Unique coordinate points | {counts['unique_coordinate_points']} |",
        f"| Radius bands computed | {counts['radius_bands_computed']} |",
        f"| Candidate coordinate-radius rows | {counts['candidate_coordinate_radius_rows']} |",
        f"| GHSL population rows computed | {counts['population_rows_computed']} |",
        f"| ACAG PM2.5 rows computed | {counts['pm25_rows_computed']} |",
        f"| Country radius summaries | {counts['country_radius_summary_rows']} |",
        f"| Validated same-station joins | {counts['validated_same_station_join_rows']} |",
        f"| Complete monitor-grade rows | {counts['complete_monitor_grade_rows']} |",
        "",
        "## Primary 4 km Diagnostic Rows",
        "",
        (
            "These rows show the largest non-unioned exact-coordinate-deduplicated "
            "candidate population sums at the source-frozen 4 km band. They are "
            "not people covered by monitors."
        ),
        "",
        "| Economy | Coordinate rows | Unique points | Candidate population, exact-coordinate dedup | Mean nearest PM2.5 | GHSL tiles |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in top:
        lines.append(
            "| "
            f"{row['iso3']} | "
            f"{row['coordinate_rows']} | "
            f"{row['unique_coordinate_points']} | "
            f"{row['candidate_population_exact_coordinate_dedup_sum']} | "
            f"{row['mean_pm25_nearest_ugm3']} | "
            f"{row['ghsl_tile_count']} |"
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
    for gate in gates:
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
            "python air-monitoring\\scripts\\build-station-radius-denominator-join-dry-run.py",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    radii = radius_bands()
    coordinates = load_coordinate_inputs()
    rasters = load_population_rasters()
    grid = load_pm25_grid()
    recon = read_json(RECON_SUMMARY)
    grade = read_json(GRADE_SUMMARY)
    method_prefreeze = read_json(METHOD_PREFREEZE_SUMMARY)
    pm25_resolution = read_json(PM25_RESOLUTION_SUMMARY)
    validated_join_rows = parse_int(recon["coverage_counts"].get("validated_same_station_rows"))
    complete_grade_rows = parse_int(grade["coverage_counts"].get("complete_monitor_grade_classification_rows"))

    row_records: list[dict[str, Any]] = []
    for point in coordinates:
        for radius in radii:
            population = sample_population(point, float(radius["radius_km"]), rasters)
            pm25 = sample_pm25(point, float(radius["radius_km"]), grid)
            row_records.append(
                build_row(
                    generated_at,
                    point,
                    radius,
                    population,
                    pm25,
                    grid,
                    validated_join_rows,
                    complete_grade_rows,
                )
            )

    country_records = country_rows(
        generated_at,
        row_records,
        coordinates,
        validated_join_rows,
        complete_grade_rows,
    )

    source_counter = Counter(point.source_family for point in coordinates)
    primary_radius = next(radius["radius_km"] for radius in radii if radius["radius_role"] == "primary")
    primary_country_rows = [
        row for row in country_records if float(row["radius_km"]) == float(primary_radius)
    ]
    top_primary = sorted(
        primary_country_rows,
        key=lambda row: parse_float(row.get("candidate_population_exact_coordinate_dedup_sum")) or 0,
        reverse=True,
    )[:8]

    counts = {
        "coordinate_economies": len({point.iso3 for point in coordinates}),
        "coordinate_rows_used": len(coordinates),
        "unique_coordinate_points": len({point.coordinate_key for point in coordinates}),
        "openaq_coordinate_rows_used": source_counter["openaq"],
        "official_pm25_coordinate_rows_used": source_counter["official_pm25_station"],
        "radius_bands_computed": len(radii),
        "candidate_coordinate_radius_rows": len(row_records),
        "population_rows_computed": sum(1 for row in row_records if truthy(row.get("ghsl_population_computed"))),
        "pm25_rows_computed": sum(1 for row in row_records if truthy(row.get("pm25_computed"))),
        "country_radius_summary_rows": len(country_records),
        "population_raster_tiles_opened": len(rasters),
        "acag_pm25_surface_opened": 1,
        "primary_radius_km": primary_radius,
        "lower_sensitivity_radius_km": next(radius["radius_km"] for radius in radii if radius["radius_role"] == "lower_sensitivity"),
        "upper_sensitivity_radius_km": next(radius["radius_km"] for radius in radii if radius["radius_role"] == "upper_sensitivity"),
        "country_union_population_rows": 0,
        "country_union_population_computed": False,
        "validated_same_station_join_rows": validated_join_rows,
        "complete_monitor_grade_rows": complete_grade_rows,
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
            {"path": source_ref(OPENAQ_CSV), "role": "OpenAQ PM2.5 candidate coordinate rows"},
            {"path": source_ref(OFFICIAL_CSV), "role": "official PM2.5 candidate coordinate rows"},
            {"path": source_ref(ROUTING_COUNTRY_CSV), "role": "corrected GHSL country tile envelope"},
            {"path": source_ref(CORRECTED_CUSTODY_CSV), "role": "first-wave corrected GHSL tile custody"},
            {"path": source_ref(LARGE_CUSTODY_CSV), "role": "large corrected GHSL tile custody"},
            {"path": source_ref(ACAG_CHECKSUM_CSV), "role": "ACAG coarse PM2.5 checksum ledger"},
            {"path": source_ref(RADIUS_RULE_SUMMARY), "role": "source-frozen radius bands"},
            {"path": source_ref(PM25_RESOLUTION_SUMMARY), "role": "PM2.5 grid-resolution decision"},
        ],
        "method_notes": [
            "Population cells are summed inside row-level circular buffers using cached GHSL R2023A 2020 3 arc-second tiles.",
            "Distance masks use a local equirectangular approximation, appropriate for this dry-run radius scale.",
            "Country summaries include an exact-coordinate deduplicated diagnostic, but overlapping buffers are not unioned.",
            "PM2.5 values come from the selected ACAG V6.GL.03 2023 0.10 degree global coarse annual file.",
        ],
        "coverage_counts": counts,
        "evidence_gate_counts": evidence_gates(counts),
        "radius_bands": radii,
        "population_tile_records": [
            {
                "tile_id": raster.tile_id,
                "cache_path": raster.source_path,
                "sha256": raster.sha256,
            }
            for raster in rasters
        ],
        "pm25_surface": {
            "record_key": grid.record_key,
            "selected_vintage": grid.selected_vintage,
            "cache_path": grid.source_path,
            "resolution_decision_status": pm25_resolution["status"],
        },
        "prefreeze_counts": method_prefreeze["coverage_counts"],
        "top_primary_radius_country_rows": top_primary,
        "country_rows": country_records,
        "sample_coordinate_radius_rows": row_records[:12],
        "outputs": {
            "coordinate_radius_csv": source_ref(OUT_ROW_CSV),
            "country_csv": source_ref(OUT_COUNTRY_CSV),
            "summary_json": source_ref(OUT_JSON),
            "evidence_md": source_ref(OUT_MD),
        },
        "non_claim": NON_CLAIM,
    }

    write_csv(OUT_ROW_CSV, row_records, ROW_FIELDS)
    write_csv(OUT_COUNTRY_CSV, country_records, COUNTRY_FIELDS)
    write_json(OUT_JSON, summary)
    write_markdown(OUT_MD, summary)

    for raster in rasters:
        raster.dataset.close()

    return summary


def main() -> None:
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built station-radius denominator join dry run: "
        f"{counts['candidate_coordinate_radius_rows']} coordinate-radius rows, "
        f"{counts['country_radius_summary_rows']} country-radius summaries, "
        f"{counts['population_rows_computed']} GHSL joins, "
        f"{counts['pm25_rows_computed']} ACAG joins, "
        f"{counts['station_radius_ready_economies']} ready economies."
    )


if __name__ == "__main__":
    main()
