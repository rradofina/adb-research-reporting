#!/usr/bin/env python
"""Derive a corrected GHSL tile-routing rule from inspected rasters.

This gate follows the GHSL population tile checksum gate. It uses only
downloaded GeoTIFF bounds already recorded by the checksum gate to estimate the
actual GHSL R/C grid origin, then recomputes the station-radius tile queue. It
does not download additional tiles or compute catchment population.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"

OPENAQ_CSV = GENERATED / "air-monitoring-openaq-station-metadata.csv"
OFFICIAL_CSV = GENERATED / "air-monitoring-regulator-station-extraction.csv"
READINESS_CSV = GENERATED / "air-monitoring-station-radius-denominator-readiness.csv"
SELECTION_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-selection-summary.json"
CHECKSUM_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-checksums-summary.json"

OUT_TILE_CSV = GENERATED / "air-monitoring-station-radius-ghsl-tile-routing-correction.csv"
OUT_COUNTRY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-tile-routing-correction-country.csv"
OUT_ORIGIN_CSV = GENERATED / "air-monitoring-station-radius-ghsl-tile-routing-correction-origin.csv"
OUT_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-tile-routing-correction-summary.json"
OUT_MD = PROGRAM / "station-radius-ghsl-tile-routing-correction.md"

STATUS = "computed_station_radius_ghsl_tile_routing_correction"
METHOD = "air_monitoring_station_radius_ghsl_tile_routing_correction_v1"
ATTESTATION = "ai-first"
RADIUS_BUFFER_KM = 50
TILE_SIZE_DEGREES = 10.0

GHSL_BASE = (
    "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/"
    "GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_3ss/V1-0/tiles/"
)
GHSL_PREFIX = "GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0"

NON_CLAIM = (
    "This GHSL tile-routing correction gate derives an observed R/C grid "
    "origin from already downloaded GHSL GeoTIFF bounds, recomputes the "
    "station-coordinate tile queue with the same 50 km draft buffer, and "
    "records which selected tile IDs are retained, added, or removed. It does "
    "not download newly added tiles, retry HEAD probes, compute station-radius "
    "population, compute PM2.5 exposure, validate same-station joins, freeze "
    "radius or de-duplication rules, or promote monitor-grade rows."
)


@dataclass(frozen=True)
class CoordinateInput:
    iso3: str
    country: str
    source_family: str
    source_row_id: str
    station_name: str
    latitude: float
    longitude: float


@dataclass
class CountryAccumulator:
    iso3: str
    country: str
    readiness_lane: str = ""
    openaq_rows: int = 0
    official_pm25_rows: int = 0
    coordinate_rows_used: int = 0
    unique_coordinate_points: set[str] = field(default_factory=set)
    previous_tiles: set[tuple[int, int]] = field(default_factory=set)
    corrected_tiles: set[tuple[int, int]] = field(default_factory=set)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() == "true"


def parse_float(value: Any) -> float | None:
    if value in ("", None):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def parse_tile_id(value: str) -> tuple[int, int]:
    row_text, col_text = value.split("_")
    return int(row_text[1:]), int(col_text[1:])


def tile_id(row: int, col: int) -> str:
    return f"R{row}_C{col}"


def tile_url(row: int, col: int) -> str:
    return f"{GHSL_BASE}{GHSL_PREFIX}_{tile_id(row, col)}.zip"


def tile_key_from_id(value: str) -> tuple[int, int]:
    return parse_tile_id(value)


def round_float(value: float, digits: int = 8) -> float:
    return round(value, digits)


def derive_origin_rows(checksum_summary: dict[str, Any], generated_at: str) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    for row in checksum_summary.get("tile_checksum_rows", []):
        if not truthy(row.get("geotiff_opened")) or not row.get("raster_bounds"):
            continue
        tile_row, tile_col = parse_tile_id(str(row["tile_id"]))
        left, bottom, right, top = [float(part) for part in str(row["raster_bounds"]).split(",")]
        north_origin = top + ((tile_row - 1) * TILE_SIZE_DEGREES)
        west_origin = left - ((tile_col - 1) * TILE_SIZE_DEGREES)
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "tile_id": row["tile_id"],
                "tile_row": tile_row,
                "tile_col": tile_col,
                "raster_west": round_float(left),
                "raster_south": round_float(bottom),
                "raster_east": round_float(right),
                "raster_north": round_float(top),
                "derived_north_origin": round_float(north_origin, 10),
                "derived_west_origin": round_float(west_origin, 10),
                "simple_grid_expected_west": -180.0 + ((tile_col - 1) * TILE_SIZE_DEGREES),
                "simple_grid_expected_south": 90.0 - (tile_row * TILE_SIZE_DEGREES),
                "simple_grid_expected_east": -180.0 + (tile_col * TILE_SIZE_DEGREES),
                "simple_grid_expected_north": 90.0 - ((tile_row - 1) * TILE_SIZE_DEGREES),
                "raster_width": row.get("raster_width", ""),
                "raster_height": row.get("raster_height", ""),
                "raster_crs": row.get("raster_crs", ""),
                "sha256": row.get("sha256", ""),
                "reader_use": "Use these rows to derive the corrected GHSL R/C tile-routing origin before selecting tiles for catchment work.",
                "non_claim": NON_CLAIM,
            }
        )
    if not rows:
        raise ValueError("No opened GHSL GeoTIFF rows available to derive routing origin.")

    north_values = [float(row["derived_north_origin"]) for row in rows]
    west_values = [float(row["derived_west_origin"]) for row in rows]
    origin = {
        "observed_north_origin": statistics.mean(north_values),
        "observed_west_origin": statistics.mean(west_values),
        "north_origin_min": min(north_values),
        "north_origin_max": max(north_values),
        "west_origin_min": min(west_values),
        "west_origin_max": max(west_values),
        "north_origin_range_degrees": max(north_values) - min(north_values),
        "west_origin_range_degrees": max(west_values) - min(west_values),
    }
    for row in rows:
        row["mean_north_origin"] = round_float(origin["observed_north_origin"], 10)
        row["mean_west_origin"] = round_float(origin["observed_west_origin"], 10)
        row["north_origin_delta_from_mean"] = round_float(
            float(row["derived_north_origin"]) - origin["observed_north_origin"],
            10,
        )
        row["west_origin_delta_from_mean"] = round_float(
            float(row["derived_west_origin"]) - origin["observed_west_origin"],
            10,
        )
    return rows, origin


def previous_tile_for_point(latitude: float, longitude: float) -> tuple[int, int]:
    lat = max(-89.999999, min(89.999999, latitude))
    lon = max(-179.999999, min(179.999999, longitude))
    row = int(math.floor((90.0 - lat) / TILE_SIZE_DEGREES) + 1)
    col = int(math.floor((lon + 180.0) / TILE_SIZE_DEGREES) + 1)
    return row, col


def corrected_tile_for_point(latitude: float, longitude: float, origin: dict[str, float]) -> tuple[int, int]:
    row = int(math.floor((origin["observed_north_origin"] - latitude) / TILE_SIZE_DEGREES) + 1)
    col = int(math.floor((longitude - origin["observed_west_origin"]) / TILE_SIZE_DEGREES) + 1)
    return row, col


def previous_tile_bounds(row: int, col: int) -> dict[str, float]:
    north = 90.0 - ((row - 1) * TILE_SIZE_DEGREES)
    south = north - TILE_SIZE_DEGREES
    west = -180.0 + ((col - 1) * TILE_SIZE_DEGREES)
    east = west + TILE_SIZE_DEGREES
    return {"south": south, "west": west, "north": north, "east": east}


def corrected_tile_bounds(row: int, col: int, origin: dict[str, float]) -> dict[str, float]:
    north = origin["observed_north_origin"] - ((row - 1) * TILE_SIZE_DEGREES)
    south = north - TILE_SIZE_DEGREES
    west = origin["observed_west_origin"] + ((col - 1) * TILE_SIZE_DEGREES)
    east = west + TILE_SIZE_DEGREES
    return {"south": south, "west": west, "north": north, "east": east}


def buffered_tiles(latitude: float, longitude: float, tile_fn) -> set[tuple[int, int]]:
    lat_buffer = RADIUS_BUFFER_KM / 111.32
    cos_lat = max(0.15, math.cos(math.radians(latitude)))
    lon_buffer = RADIUS_BUFFER_KM / (111.32 * cos_lat)
    candidates = set()
    for lat in (latitude - lat_buffer, latitude + lat_buffer):
        for lon in (longitude - lon_buffer, longitude + lon_buffer):
            candidates.add(tile_fn(lat, lon))
    return candidates


def load_coordinate_inputs() -> tuple[list[CoordinateInput], dict[str, CountryAccumulator]]:
    readiness = {
        row["iso3"]: CountryAccumulator(
            iso3=row["iso3"],
            country=row["country"],
            readiness_lane=row["readiness_lane"],
        )
        for row in read_csv(READINESS_CSV)
    }
    inputs: list[CoordinateInput] = []

    for row in read_csv(OPENAQ_CSV):
        lat = parse_float(row.get("latitude"))
        lon = parse_float(row.get("longitude"))
        if (
            lat is None
            or lon is None
            or not truthy(row.get("station_radius_coordinate_input_available"))
            or not truthy(row.get("coordinate_in_target_country_bbox"))
        ):
            continue
        iso3 = row["iso3"]
        if iso3 not in readiness:
            continue
        inputs.append(
            CoordinateInput(
                iso3=iso3,
                country=row["country"],
                source_family="OpenAQ",
                source_row_id=row.get("openaq_location_id", ""),
                station_name=row.get("openaq_location_name", ""),
                latitude=lat,
                longitude=lon,
            )
        )
        readiness[iso3].openaq_rows += 1

    for row in read_csv(OFFICIAL_CSV):
        lat = parse_float(row.get("latitude"))
        lon = parse_float(row.get("longitude"))
        if lat is None or lon is None or not truthy(row.get("coordinate_available")):
            continue
        if not truthy(row.get("pm25_signal")):
            continue
        iso3 = row["iso3"]
        if iso3 not in readiness:
            continue
        inputs.append(
            CoordinateInput(
                iso3=iso3,
                country=row["country"],
                source_family="official_pm25_station",
                source_row_id=row.get("source_station_id", ""),
                station_name=row.get("source_station_name", ""),
                latitude=lat,
                longitude=lon,
            )
        )
        readiness[iso3].official_pm25_rows += 1
    return inputs, readiness


def tile_ids(values: Iterable[tuple[int, int]]) -> str:
    return "||".join(tile_id(row, col) for row, col in sorted(set(values)))


def source_row_lookup(selection_summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["tile_id"]): row for row in selection_summary.get("tile_rows", [])}


def checksum_row_lookup(checksum_summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(row["tile_id"]): row for row in checksum_summary.get("tile_checksum_rows", [])}


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    selection = read_json(SELECTION_SUMMARY)
    checksum = read_json(CHECKSUM_SUMMARY)
    origin_rows, origin = derive_origin_rows(checksum, generated_at)
    coordinate_inputs, countries = load_coordinate_inputs()

    previous_tile_to_countries: dict[tuple[int, int], set[str]] = defaultdict(set)
    corrected_tile_to_countries: dict[tuple[int, int], set[str]] = defaultdict(set)
    previous_tile_to_sources: dict[tuple[int, int], Counter[str]] = defaultdict(Counter)
    corrected_tile_to_sources: dict[tuple[int, int], Counter[str]] = defaultdict(Counter)
    previous_tile_coord_rows: Counter[tuple[int, int]] = Counter()
    corrected_tile_coord_rows: Counter[tuple[int, int]] = Counter()
    previous_tiles: set[tuple[int, int]] = set()
    corrected_tiles: set[tuple[int, int]] = set()

    for point in coordinate_inputs:
        acc = countries[point.iso3]
        acc.coordinate_rows_used += 1
        acc.unique_coordinate_points.add(f"{point.latitude:.6f},{point.longitude:.6f}")
        old_touched = buffered_tiles(point.latitude, point.longitude, previous_tile_for_point)
        new_touched = buffered_tiles(
            point.latitude,
            point.longitude,
            lambda lat, lon: corrected_tile_for_point(lat, lon, origin),
        )
        acc.previous_tiles.update(old_touched)
        acc.corrected_tiles.update(new_touched)
        previous_tiles.update(old_touched)
        corrected_tiles.update(new_touched)
        for tile in old_touched:
            previous_tile_to_countries[tile].add(point.iso3)
            previous_tile_to_sources[tile][point.source_family] += 1
            previous_tile_coord_rows[tile] += 1
        for tile in new_touched:
            corrected_tile_to_countries[tile].add(point.iso3)
            corrected_tile_to_sources[tile][point.source_family] += 1
            corrected_tile_coord_rows[tile] += 1

    previous_lookup = source_row_lookup(selection)
    checksum_lookup = checksum_row_lookup(checksum)
    all_tiles = sorted(previous_tiles | corrected_tiles)
    retained_tiles = previous_tiles & corrected_tiles
    added_tiles = corrected_tiles - previous_tiles
    removed_tiles = previous_tiles - corrected_tiles

    tile_rows: list[dict[str, Any]] = []
    for row, col in all_tiles:
        ident = tile_id(row, col)
        previous_selected = (row, col) in previous_tiles
        corrected_selected = (row, col) in corrected_tiles
        previous_row = previous_lookup.get(ident, {})
        checksum_row = checksum_lookup.get(ident, {})
        previous_bounds = previous_tile_bounds(row, col)
        corrected_bounds = corrected_tile_bounds(row, col, origin)
        if corrected_selected and previous_selected:
            correction_status = "retained_by_corrected_origin"
        elif corrected_selected:
            correction_status = "added_by_corrected_origin"
        else:
            correction_status = "removed_by_corrected_origin"
        tile_rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "tile_id": ident,
                "tile_row": row,
                "tile_col": col,
                "previous_selected": previous_selected,
                "corrected_selected": corrected_selected,
                "correction_status": correction_status,
                "previous_selected_economies": "||".join(sorted(previous_tile_to_countries[(row, col)])),
                "corrected_selected_economies": "||".join(sorted(corrected_tile_to_countries[(row, col)])),
                "previous_coordinate_rows_touching_tile": previous_tile_coord_rows[(row, col)],
                "corrected_coordinate_rows_touching_tile": corrected_tile_coord_rows[(row, col)],
                "previous_openaq_coordinate_rows_touching_tile": previous_tile_to_sources[(row, col)]["OpenAQ"],
                "corrected_openaq_coordinate_rows_touching_tile": corrected_tile_to_sources[(row, col)]["OpenAQ"],
                "previous_official_pm25_coordinate_rows_touching_tile": previous_tile_to_sources[(row, col)][
                    "official_pm25_station"
                ],
                "corrected_official_pm25_coordinate_rows_touching_tile": corrected_tile_to_sources[(row, col)][
                    "official_pm25_station"
                ],
                "previous_south": previous_bounds["south"],
                "previous_west": previous_bounds["west"],
                "previous_north": previous_bounds["north"],
                "previous_east": previous_bounds["east"],
                "corrected_south": round_float(corrected_bounds["south"]),
                "corrected_west": round_float(corrected_bounds["west"]),
                "corrected_north": round_float(corrected_bounds["north"]),
                "corrected_east": round_float(corrected_bounds["east"]),
                "exact_file_url": tile_url(row, col),
                "prior_head_ok": previous_row.get("head_ok", ""),
                "prior_head_status": previous_row.get("head_status", ""),
                "prior_content_length_bytes": previous_row.get("content_length_bytes", ""),
                "prior_size_mb": previous_row.get("size_mb", ""),
                "prior_downloaded": checksum_row.get("downloaded", ""),
                "prior_sha256": checksum_row.get("sha256", ""),
                "prior_geotiff_opened": checksum_row.get("geotiff_opened", ""),
                "prior_raster_bounds": checksum_row.get("raster_bounds", ""),
                "reader_use": "Use corrected-selected rows as the next GHSL population tile queue; newly added rows still need HEAD/download custody before catchments.",
                "non_claim": NON_CLAIM,
            }
        )

    country_rows: list[dict[str, Any]] = []
    for acc in countries.values():
        if acc.coordinate_rows_used <= 0:
            continue
        added = acc.corrected_tiles - acc.previous_tiles
        removed = acc.previous_tiles - acc.corrected_tiles
        retained = acc.corrected_tiles & acc.previous_tiles
        country_rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "iso3": acc.iso3,
                "country": acc.country,
                "readiness_lane": acc.readiness_lane,
                "openaq_coordinate_rows_used": acc.openaq_rows,
                "official_pm25_coordinate_rows_used": acc.official_pm25_rows,
                "coordinate_rows_used": acc.coordinate_rows_used,
                "unique_coordinate_points": len(acc.unique_coordinate_points),
                "previous_tile_count": len(acc.previous_tiles),
                "corrected_tile_count": len(acc.corrected_tiles),
                "retained_tile_count": len(retained),
                "added_tile_count": len(added),
                "removed_tile_count": len(removed),
                "previous_tile_ids": tile_ids(acc.previous_tiles),
                "corrected_tile_ids": tile_ids(acc.corrected_tiles),
                "added_tile_ids": tile_ids(added),
                "removed_tile_ids": tile_ids(removed),
                "reader_use": "Country-level queue-change ledger for the corrected GHSL tile-routing origin.",
                "non_claim": NON_CLAIM,
            }
        )

    corrected_tile_ids = {tile_id(row, col) for row, col in corrected_tiles}
    retained_tile_ids = {tile_id(row, col) for row, col in retained_tiles}
    added_tile_ids = {tile_id(row, col) for row, col in added_tiles}
    removed_tile_ids = {tile_id(row, col) for row, col in removed_tiles}
    corrected_rows = [row for row in tile_rows if row["corrected_selected"]]
    downloaded_retained = [
        row for row in corrected_rows if truthy(row.get("prior_downloaded")) and row["tile_id"] in retained_tile_ids
    ]
    downloaded_removed = [
        row for row in tile_rows if truthy(row.get("prior_downloaded")) and row["tile_id"] in removed_tile_ids
    ]
    corrected_known_head_ok = [row for row in corrected_rows if truthy(row.get("prior_head_ok"))]
    corrected_known_head_not_ok = [
        row for row in corrected_rows if row.get("prior_head_ok") not in ("", None) and not truthy(row.get("prior_head_ok"))
    ]
    corrected_unknown_head = [
        row for row in corrected_rows if row.get("prior_head_ok") in ("", None)
    ]

    counts = {
        "coordinate_ready_economies": len(country_rows),
        "coordinate_rows_used": len(coordinate_inputs),
        "openaq_coordinate_rows_used": sum(row["openaq_coordinate_rows_used"] for row in country_rows),
        "official_pm25_coordinate_rows_used": sum(row["official_pm25_coordinate_rows_used"] for row in country_rows),
        "origin_observation_rows": len(origin_rows),
        "observed_north_origin": round_float(origin["observed_north_origin"], 10),
        "observed_west_origin": round_float(origin["observed_west_origin"], 10),
        "north_origin_range_degrees": round_float(origin["north_origin_range_degrees"], 10),
        "west_origin_range_degrees": round_float(origin["west_origin_range_degrees"], 10),
        "previous_tile_urls_selected": len(previous_tiles),
        "corrected_tile_urls_selected": len(corrected_tiles),
        "retained_previous_tile_urls": len(retained_tiles),
        "added_corrected_tile_urls": len(added_tiles),
        "removed_previous_tile_urls": len(removed_tiles),
        "corrected_tile_prior_head_ok": len(corrected_known_head_ok),
        "corrected_tile_prior_head_not_ok": len(corrected_known_head_not_ok),
        "corrected_tile_prior_head_unknown": len(corrected_unknown_head),
        "downloaded_population_tiles_retained_by_corrected_routing": len(downloaded_retained),
        "downloaded_population_tiles_removed_by_corrected_routing": len(downloaded_removed),
        "station_radius_population_rows": 0,
        "station_radius_pm25_exposure_rows": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }

    gates = [
        {
            "gate": "Observed GHSL raster origin",
            "status": "available",
            "rows": counts["origin_observation_rows"],
            "reader_use": "Opened GeoTIFF bounds provide an empirical origin for R/C routing.",
        },
        {
            "gate": "Origin consistency check",
            "status": "available"
            if counts["north_origin_range_degrees"] < 0.0001 and counts["west_origin_range_degrees"] < 0.0001
            else "limited",
            "rows": counts["origin_observation_rows"],
            "reader_use": "Derived origins should be nearly identical across opened tiles before rerouting the queue.",
        },
        {
            "gate": "Corrected GHSL tile queue",
            "status": "available",
            "rows": counts["corrected_tile_urls_selected"],
            "reader_use": "The corrected queue replaces the simple-grid queue for future HEAD/download work.",
        },
        {
            "gate": "Retained selected tile URLs",
            "status": "available",
            "rows": counts["retained_previous_tile_urls"],
            "reader_use": "Retained rows keep any prior HEAD or checksum evidence attached.",
        },
        {
            "gate": "New corrected tile URLs needing custody",
            "status": "limited" if counts["added_corrected_tile_urls"] else "available",
            "rows": counts["added_corrected_tile_urls"],
            "reader_use": "Added rows need HEAD metadata, download feasibility, and checksums before catchment use.",
        },
        {
            "gate": "Removed previous tile URLs",
            "status": "limited" if counts["removed_previous_tile_urls"] else "available",
            "rows": counts["removed_previous_tile_urls"],
            "reader_use": "Removed rows should not be used as population denominator tiles under the corrected origin.",
        },
        {
            "gate": "Station-radius population computation",
            "status": "not_computed",
            "rows": 0,
            "reader_use": "No catchment population, PM2.5 exposure, or map is computed here.",
        },
    ]

    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius GHSL population tile-routing correction gate",
        "routing_rule": (
            "Use the mean origin derived from opened GHSL GeoTIFF bounds: "
            f"north_origin={counts['observed_north_origin']}, "
            f"west_origin={counts['observed_west_origin']}, "
            "then assign R/C with floor((north_origin - latitude)/10)+1 and "
            "floor((longitude - west_origin)/10)+1 before applying the same 50 km draft buffer."
        ),
        "coverage_counts": counts,
        "evidence_gate_counts": gates,
        "added_corrected_tile_ids": sorted(added_tile_ids),
        "removed_previous_tile_ids": sorted(removed_tile_ids),
        "retained_previous_tile_ids": sorted(retained_tile_ids),
        "origin_rows": origin_rows,
        "country_rows": country_rows,
        "tile_rows": tile_rows,
        "outputs": {
            "tile_csv": str(OUT_TILE_CSV.relative_to(PROGRAM)).replace("\\", "/"),
            "country_csv": str(OUT_COUNTRY_CSV.relative_to(PROGRAM)).replace("\\", "/"),
            "origin_csv": str(OUT_ORIGIN_CSV.relative_to(PROGRAM)).replace("\\", "/"),
            "summary_json": str(OUT_SUMMARY.relative_to(PROGRAM)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }

    write_csv(
        OUT_ORIGIN_CSV,
        origin_rows,
        [
            "generated_at",
            "attestation_chain",
            "status",
            "method",
            "tile_id",
            "tile_row",
            "tile_col",
            "raster_west",
            "raster_south",
            "raster_east",
            "raster_north",
            "derived_north_origin",
            "derived_west_origin",
            "mean_north_origin",
            "mean_west_origin",
            "north_origin_delta_from_mean",
            "west_origin_delta_from_mean",
            "simple_grid_expected_west",
            "simple_grid_expected_south",
            "simple_grid_expected_east",
            "simple_grid_expected_north",
            "raster_width",
            "raster_height",
            "raster_crs",
            "sha256",
            "reader_use",
            "non_claim",
        ],
    )
    write_csv(
        OUT_COUNTRY_CSV,
        country_rows,
        [
            "generated_at",
            "attestation_chain",
            "status",
            "method",
            "iso3",
            "country",
            "readiness_lane",
            "openaq_coordinate_rows_used",
            "official_pm25_coordinate_rows_used",
            "coordinate_rows_used",
            "unique_coordinate_points",
            "previous_tile_count",
            "corrected_tile_count",
            "retained_tile_count",
            "added_tile_count",
            "removed_tile_count",
            "previous_tile_ids",
            "corrected_tile_ids",
            "added_tile_ids",
            "removed_tile_ids",
            "reader_use",
            "non_claim",
        ],
    )
    write_csv(
        OUT_TILE_CSV,
        tile_rows,
        [
            "generated_at",
            "attestation_chain",
            "status",
            "method",
            "tile_id",
            "tile_row",
            "tile_col",
            "previous_selected",
            "corrected_selected",
            "correction_status",
            "previous_selected_economies",
            "corrected_selected_economies",
            "previous_coordinate_rows_touching_tile",
            "corrected_coordinate_rows_touching_tile",
            "previous_openaq_coordinate_rows_touching_tile",
            "corrected_openaq_coordinate_rows_touching_tile",
            "previous_official_pm25_coordinate_rows_touching_tile",
            "corrected_official_pm25_coordinate_rows_touching_tile",
            "previous_south",
            "previous_west",
            "previous_north",
            "previous_east",
            "corrected_south",
            "corrected_west",
            "corrected_north",
            "corrected_east",
            "exact_file_url",
            "prior_head_ok",
            "prior_head_status",
            "prior_content_length_bytes",
            "prior_size_mb",
            "prior_downloaded",
            "prior_sha256",
            "prior_geotiff_opened",
            "prior_raster_bounds",
            "reader_use",
            "non_claim",
        ],
    )
    write_json(OUT_SUMMARY, summary)
    OUT_MD.write_text(render_markdown(summary), encoding="utf-8")
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    counts = summary["coverage_counts"]
    lines = [
        "# Station-radius GHSL tile-routing correction gate",
        "",
        f"`attestation_chain: {summary['attestation_chain']}`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        (
            "This pass uses the four opened GHSL GeoTIFF bounds from the "
            "checksum gate to derive the actual R/C tile-routing origin. It "
            "then reruns the existing 50 km coordinate buffer against that "
            "origin and records how the selected population tile queue changes."
        ),
        "",
        "## Routing rule",
        "",
        str(summary["routing_rule"]),
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for gate in summary["evidence_gate_counts"]:
        lines.append(f"| {gate['gate']} | {gate['rows']} | {gate['status']} |")
    lines.extend(
        [
            "",
            "## Queue changes",
            "",
            f"- Retained previous tile IDs: `{ '||'.join(summary['retained_previous_tile_ids']) }`",
            f"- Added corrected tile IDs: `{ '||'.join(summary['added_corrected_tile_ids']) or 'none' }`",
            f"- Removed previous tile IDs: `{ '||'.join(summary['removed_previous_tile_ids']) or 'none' }`",
            "",
            "## Origin evidence",
            "",
            "| Tile | Raster bounds | Derived north origin | Derived west origin |",
            "|---|---|---:|---:|",
        ]
    )
    for row in summary["origin_rows"]:
        bounds = "{west},{south},{east},{north}".format(
            west=row["raster_west"],
            south=row["raster_south"],
            east=row["raster_east"],
            north=row["raster_north"],
        )
        lines.append(
            f"| {row['tile_id']} | `{bounds}` | {row['derived_north_origin']} | {row['derived_west_origin']} |"
        )
    lines.extend(
        [
            "",
            "## Corrected tile queue",
            "",
            "| Tile | Status | Corrected economies | Corrected coordinate rows | Prior HEAD | Prior downloaded |",
            "|---|---|---|---:|---:|---:|",
        ]
    )
    for row in summary["tile_rows"]:
        if not row["corrected_selected"] and row["correction_status"] != "removed_by_corrected_origin":
            continue
        lines.append(
            "| {tile} | {status} | {economies} | {rows} | {head} | {downloaded} |".format(
                tile=row["tile_id"],
                status=row["correction_status"],
                economies=row["corrected_selected_economies"] or row["previous_selected_economies"],
                rows=row["corrected_coordinate_rows_touching_tile"],
                head=row["prior_head_ok"],
                downloaded=row["prior_downloaded"],
            )
        )
    lines.extend(["", "## Non-claim", "", str(summary["non_claim"]), ""])
    return "\n".join(lines)


def main() -> int:
    for path in [OPENAQ_CSV, OFFICIAL_CSV, READINESS_CSV, SELECTION_SUMMARY, CHECKSUM_SUMMARY]:
        if not path.exists():
            raise FileNotFoundError(path)
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built GHSL tile-routing correction gate: "
        f"{counts['origin_observation_rows']} origin rows; "
        f"{counts['previous_tile_urls_selected']} previous tiles; "
        f"{counts['corrected_tile_urls_selected']} corrected tiles; "
        f"{counts['added_corrected_tile_urls']} added; "
        f"{counts['removed_previous_tile_urls']} removed; "
        f"{counts['station_radius_population_rows']} catchment rows."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
