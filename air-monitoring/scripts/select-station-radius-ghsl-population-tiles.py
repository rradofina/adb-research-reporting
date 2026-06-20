#!/usr/bin/env python
"""Select GHSL population tiles for the station-radius denominator gate.

This is a pre-download gate. It derives the GHSL 4326 3 arc-second tile URLs
needed by committed station-coordinate inputs, probes headers, and keeps all
population downloads, checksums, exposure rows, and station-radius claims at
zero.
"""

from __future__ import annotations

import csv
import json
import math
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"

OPENAQ_CSV = GENERATED / "air-monitoring-openaq-station-metadata.csv"
OFFICIAL_CSV = GENERATED / "air-monitoring-regulator-station-extraction.csv"
READINESS_CSV = GENERATED / "air-monitoring-station-radius-denominator-readiness.csv"

OUT_TILE_CSV = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-selection.csv"
OUT_COUNTRY_CSV = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-selection-country.csv"
OUT_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-selection-summary.json"
OUT_MD = PROGRAM / "station-radius-ghsl-population-tile-selection.md"

STATUS = "computed_station_radius_ghsl_population_tile_selection"
METHOD = "air_monitoring_station_radius_ghsl_population_tile_selection_v1"
ATTESTATION = "ai-first"
RADIUS_BUFFER_KM = 50
HEAD_TIMEOUT_SECONDS = 90
HEAD_WORKERS = 6

GHSL_BASE = (
    "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/"
    "GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_3ss/V1-0/tiles/"
)
GHSL_PREFIX = "GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0"

NON_CLAIM = (
    "This GHSL population tile-selection gate constructs and probes the public "
    "2020 GHSL 4326 3 arc-second tile URLs needed by committed station "
    "coordinates using a conservative 50 km draft-radius buffer. It does not "
    "download GHSL ZIP bodies, compute SHA-256 checksums, inspect GeoTIFF "
    "transforms, compute station-radius population, compute PM2.5 exposure, "
    "validate same-station joins, freeze radius or de-duplication rules, or "
    "promote monitor-grade rows."
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
    tiles: set[tuple[int, int]] = field(default_factory=set)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    if math.isfinite(parsed):
        return parsed
    return None


def ghsl_tile_for_point(latitude: float, longitude: float) -> tuple[int, int]:
    """Return the R/C tile for a 10-degree WGS84 grid.

    The tile grid is treated as a pre-download routing assumption and is
    explicitly revalidated only after a selected tile ZIP is downloaded and its
    GeoTIFF transform is inspected in a later gate.
    """

    lat = max(-89.999999, min(89.999999, latitude))
    lon = max(-179.999999, min(179.999999, longitude))
    row = int(math.floor((90.0 - lat) / 10.0) + 1)
    col = int(math.floor((lon + 180.0) / 10.0) + 1)
    return row, col


def tile_bounds(row: int, col: int) -> dict[str, float]:
    north = 90.0 - ((row - 1) * 10.0)
    south = north - 10.0
    west = -180.0 + ((col - 1) * 10.0)
    east = west + 10.0
    return {"south": south, "west": west, "north": north, "east": east}


def buffered_tiles(latitude: float, longitude: float, radius_km: float) -> set[tuple[int, int]]:
    lat_buffer = radius_km / 111.32
    cos_lat = max(0.15, math.cos(math.radians(latitude)))
    lon_buffer = radius_km / (111.32 * cos_lat)
    candidates = set()
    for lat in (latitude - lat_buffer, latitude + lat_buffer):
        for lon in (longitude - lon_buffer, longitude + lon_buffer):
            candidates.add(ghsl_tile_for_point(lat, lon))
    return candidates


def tile_id(row: int, col: int) -> str:
    return f"R{row}_C{col}"


def tile_url(row: int, col: int) -> str:
    ident = tile_id(row, col)
    return f"{GHSL_BASE}{GHSL_PREFIX}_{ident}.zip"


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

    for point in inputs:
        acc = readiness[point.iso3]
        acc.coordinate_rows_used += 1
        acc.unique_coordinate_points.add(f"{point.latitude:.6f},{point.longitude:.6f}")
        acc.tiles.update(buffered_tiles(point.latitude, point.longitude, RADIUS_BUFFER_KM))

    return inputs, readiness


def head_tile(row: int, col: int) -> dict[str, object]:
    url = tile_url(row, col)
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=HEAD_TIMEOUT_SECONDS) as response:
            headers = response.headers
            length = headers.get("Content-Length")
            return {
                "tile_id": tile_id(row, col),
                "http_status": response.status,
                "head_ok": response.status == 200,
                "content_type": headers.get("Content-Type", ""),
                "content_length_bytes": int(length) if length and length.isdigit() else "",
                "last_modified": headers.get("Last-Modified", ""),
                "etag": headers.get("ETag", ""),
                "retrieval_error": "",
            }
    except urllib.error.HTTPError as exc:
        return {
            "tile_id": tile_id(row, col),
            "http_status": exc.code,
            "head_ok": False,
            "content_type": "",
            "content_length_bytes": "",
            "last_modified": "",
            "etag": "",
            "retrieval_error": str(exc),
        }
    except Exception as exc:  # noqa: BLE001 - committed as retrieval evidence
        return {
            "tile_id": tile_id(row, col),
            "http_status": "",
            "head_ok": False,
            "content_type": "",
            "content_length_bytes": "",
            "last_modified": "",
            "etag": "",
            "retrieval_error": f"{type(exc).__name__}: {exc}",
        }


def probe_tiles(tiles: Iterable[tuple[int, int]]) -> dict[tuple[int, int], dict[str, object]]:
    selected = sorted(set(tiles))
    results: dict[tuple[int, int], dict[str, object]] = {}
    with ThreadPoolExecutor(max_workers=HEAD_WORKERS) as pool:
        futures = {pool.submit(head_tile, row, col): (row, col) for row, col in selected}
        for future in as_completed(futures):
            row, col = futures[future]
            results[(row, col)] = future.result()
    return results


def size_mb(value: object) -> str:
    if isinstance(value, int):
        return f"{value / 1_000_000:.3f}"
    return ""


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_outputs() -> dict[str, object]:
    generated_at = now_utc()
    coordinate_inputs, countries = load_coordinate_inputs()

    country_rows = []
    all_tiles: set[tuple[int, int]] = set()
    for acc in countries.values():
        if acc.coordinate_rows_used <= 0:
            continue
        all_tiles.update(acc.tiles)
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
                "ghsl_population_tiles_selected": len(acc.tiles),
                "tile_ids": "||".join(tile_id(row, col) for row, col in sorted(acc.tiles)),
                "selection_basis": "committed coordinate rows buffered by the 50 km draft maximum station-radius sweep",
                "downloaded_population_tile_files": 0,
                "sha256_checksummed_population_tile_files": 0,
                "station_radius_population_rows": 0,
                "reader_use": "Use this as the population denominator download queue; it is not a catchment result.",
                "non_claim": NON_CLAIM,
            }
        )

    head_results = probe_tiles(all_tiles)
    tile_to_countries: dict[tuple[int, int], set[str]] = defaultdict(set)
    tile_to_sources: dict[tuple[int, int], Counter[str]] = defaultdict(Counter)
    tile_to_coord_rows: Counter[tuple[int, int]] = Counter()
    for point in coordinate_inputs:
        touched = buffered_tiles(point.latitude, point.longitude, RADIUS_BUFFER_KM)
        for tile in touched:
            tile_to_countries[tile].add(point.iso3)
            tile_to_sources[tile][point.source_family] += 1
            tile_to_coord_rows[tile] += 1

    tile_rows = []
    for row, col in sorted(all_tiles):
        bounds = tile_bounds(row, col)
        head = head_results[(row, col)]
        length = head["content_length_bytes"]
        head_ok = bool(head["head_ok"])
        tile_rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "tile_id": tile_id(row, col),
                "tile_row": row,
                "tile_col": col,
                "south": bounds["south"],
                "west": bounds["west"],
                "north": bounds["north"],
                "east": bounds["east"],
                "selected_economies": "||".join(sorted(tile_to_countries[(row, col)])),
                "selected_economy_count": len(tile_to_countries[(row, col)]),
                "coordinate_rows_touching_tile": tile_to_coord_rows[(row, col)],
                "openaq_coordinate_rows_touching_tile": tile_to_sources[(row, col)]["OpenAQ"],
                "official_pm25_coordinate_rows_touching_tile": tile_to_sources[(row, col)][
                    "official_pm25_station"
                ],
                "ghsl_vintage": "2020 observed estimate",
                "ghsl_resolution": "4326 3 arc-second tile",
                "exact_file_url": tile_url(row, col),
                "head_status": head["http_status"],
                "head_ok": head_ok,
                "content_type": head["content_type"],
                "content_length_bytes": length,
                "size_mb": size_mb(length),
                "last_modified": head["last_modified"],
                "etag": head["etag"],
                "selection_status": "selected_head_ok" if head_ok else "selected_head_not_ok",
                "download_decision": "selected_for_future_checksum_not_downloaded",
                "blocking_gap": (
                    "Download the selected ZIP body, record SHA-256, inspect the GeoTIFF transform, "
                    "and freeze radius/de-duplication rules before any catchment computation."
                ),
                "retrieval_error": head["retrieval_error"],
                "non_claim": NON_CLAIM,
            }
        )

    ok_rows = [row for row in tile_rows if row["head_ok"]]
    total_bytes = sum(row["content_length_bytes"] for row in ok_rows if isinstance(row["content_length_bytes"], int))
    counts = {
        "coordinate_ready_economies": len(country_rows),
        "coordinate_rows_used": len(coordinate_inputs),
        "openaq_coordinate_rows_used": sum(row["openaq_coordinate_rows_used"] for row in country_rows),
        "official_pm25_coordinate_rows_used": sum(
            row["official_pm25_coordinate_rows_used"] for row in country_rows
        ),
        "unique_coordinate_points": sum(row["unique_coordinate_points"] for row in country_rows),
        "draft_radius_buffer_km": RADIUS_BUFFER_KM,
        "ghsl_population_tile_urls_selected": len(tile_rows),
        "ghsl_tile_head_probes": len(tile_rows),
        "ghsl_tile_head_ok": len(ok_rows),
        "ghsl_tile_head_failed": len(tile_rows) - len(ok_rows),
        "selected_tile_content_length_bytes_total": total_bytes,
        "selected_tile_content_length_mb_total": round(total_bytes / 1_000_000, 3),
        "population_denominator_files_downloaded": 0,
        "population_denominator_files_sha256_checksummed": 0,
        "station_radius_population_rows": 0,
        "station_radius_pm25_exposure_rows": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }

    gates = [
        {
            "gate": "Coordinate-driven population tile queue",
            "status": "available",
            "rows": counts["ghsl_population_tile_urls_selected"],
            "reader_use": "A bounded GHSL tile download queue now exists for coordinate-ready economies.",
        },
        {
            "gate": "Selected tile HEAD metadata",
            "status": "available" if counts["ghsl_tile_head_failed"] == 0 else "limited",
            "rows": counts["ghsl_tile_head_ok"],
            "reader_use": "HEAD probes record public URL reachability and byte counts without downloading ZIP bodies.",
        },
        {
            "gate": "Population tile ZIP downloads",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No selected GHSL ZIP body is downloaded in this gate.",
        },
        {
            "gate": "Population tile SHA-256 checksums",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No selected GHSL ZIP body is checksummed in this gate.",
        },
        {
            "gate": "GeoTIFF transform inspection",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "The 10-degree routing assumption still needs raster transform verification after download.",
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
        "goal_level": "L3 station-radius GHSL population tile-selection gate",
        "source_inputs": [
            {"path": str(OPENAQ_CSV.relative_to(PROGRAM)), "role": "OpenAQ coordinate rows"},
            {"path": str(OFFICIAL_CSV.relative_to(PROGRAM)), "role": "official PM2.5 coordinate rows"},
            {"path": str(READINESS_CSV.relative_to(PROGRAM)), "role": "station-radius readiness lanes"},
        ],
        "tile_grid_assumption": (
            "GHSL 4326 3 arc-second tile URL pattern is treated as a 10-degree WGS84 R/C grid "
            "for download queue construction; GeoTIFF transform inspection remains required after download."
        ),
        "coverage_counts": counts,
        "evidence_gate_counts": gates,
        "country_rows": country_rows,
        "tile_rows": tile_rows,
        "outputs": {
            "tile_csv": str(OUT_TILE_CSV.relative_to(PROGRAM)),
            "country_csv": str(OUT_COUNTRY_CSV.relative_to(PROGRAM)),
            "summary_json": str(OUT_SUMMARY.relative_to(PROGRAM)),
            "markdown": str(OUT_MD.relative_to(PROGRAM)),
        },
        "non_claim": NON_CLAIM,
    }

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
            "ghsl_population_tiles_selected",
            "tile_ids",
            "selection_basis",
            "downloaded_population_tile_files",
            "sha256_checksummed_population_tile_files",
            "station_radius_population_rows",
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
            "south",
            "west",
            "north",
            "east",
            "selected_economies",
            "selected_economy_count",
            "coordinate_rows_touching_tile",
            "openaq_coordinate_rows_touching_tile",
            "official_pm25_coordinate_rows_touching_tile",
            "ghsl_vintage",
            "ghsl_resolution",
            "exact_file_url",
            "head_status",
            "head_ok",
            "content_type",
            "content_length_bytes",
            "size_mb",
            "last_modified",
            "etag",
            "selection_status",
            "download_decision",
            "blocking_gap",
            "retrieval_error",
            "non_claim",
        ],
    )
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_markdown(summary), encoding="utf-8")
    return summary


def render_markdown(summary: dict[str, object]) -> str:
    counts = summary["coverage_counts"]
    gates = summary["evidence_gate_counts"]
    country_rows = summary["country_rows"]
    tile_rows = summary["tile_rows"]
    lines = [
        "# Station-radius GHSL population tile-selection gate",
        "",
        f"`attestation_chain: {summary['attestation_chain']}`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        (
            "This pass turns committed station coordinates into a bounded GHSL "
            "population tile download queue. It probes the selected public tile "
            "URLs for header metadata, but it does not download population ZIP "
            "bodies or compute catchment population."
        ),
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        label = key.replace("_", " ")
        lines.append(f"| {label} | {value} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for gate in gates:
        lines.append(f"| {gate['gate']} | {gate['rows']} | {gate['status']} |")
    lines.extend(
        [
            "",
            "## Country queue",
            "",
            "| Economy | Coordinate rows | GHSL tiles | Tile IDs |",
            "|---|---:|---:|---|",
        ]
    )
    for row in country_rows:
        lines.append(
            "| {country} ({iso3}) | {coords} | {tiles} | `{ids}` |".format(
                country=row["country"],
                iso3=row["iso3"],
                coords=row["coordinate_rows_used"],
                tiles=row["ghsl_population_tiles_selected"],
                ids=row["tile_ids"],
            )
        )
    lines.extend(
        [
            "",
            "## Selected tile URLs",
            "",
            "| Tile | Economies | Size MB | HEAD |",
            "|---|---|---:|---|",
        ]
    )
    for row in tile_rows:
        size = row["size_mb"] or ""
        lines.append(
            "| `{tile}` | {economies} | {size} | {status} |".format(
                tile=row["tile_id"],
                economies=row["selected_economies"],
                size=size,
                status=row["head_status"] or "not ok",
            )
        )
    lines.extend(
        [
            "",
            "## Non-claim",
            "",
            str(summary["non_claim"]),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    for path in [OPENAQ_CSV, OFFICIAL_CSV, READINESS_CSV]:
        if not path.exists():
            raise FileNotFoundError(path)
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built GHSL population tile-selection gate: "
        f"{counts['coordinate_ready_economies']} economies; "
        f"{counts['coordinate_rows_used']} coordinate rows; "
        f"{counts['ghsl_population_tile_urls_selected']} tiles selected; "
        f"{counts['ghsl_tile_head_ok']} HEAD ok; "
        f"{counts['population_denominator_files_downloaded']} downloads."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
