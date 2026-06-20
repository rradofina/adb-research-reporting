#!/usr/bin/env python
"""Download and checksum the first-wave selected GHSL population tiles.

This gate follows the GHSL tile-selection gate. It downloads only selected
tile rows whose HEAD metadata already closed, records SHA-256 hashes, inspects
the ZIP and GeoTIFF transform, and keeps failed selected tiles visible as
blockers. It does not compute station-radius population or exposure.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import rasterio
import requests


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"
CACHE = PROGRAM / ".cache" / "station-radius-ghsl-population-tiles"

INPUT_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-selection-summary.json"
OUT_CSV = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-checksums.csv"
OUT_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-population-tile-checksums-summary.json"
OUT_MD = PROGRAM / "station-radius-ghsl-population-tile-checksums.md"

STATUS = "computed_station_radius_ghsl_population_tile_checksums"
METHOD = "air_monitoring_station_radius_ghsl_population_tile_checksums_v1"
ATTESTATION = "ai-first"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 180
CHUNK_SIZE = 1024 * 1024
MAX_FIRST_WAVE_MB = 60.0

NON_CLAIM = (
    "This GHSL population tile checksum gate downloads, hashes, and inspects "
    "only selected GHSL tile ZIP files whose HEAD metadata already closed and "
    "whose recorded size is within the first-wave custody threshold. It does "
    "not download selected HEAD-failed tiles, compute station-radius "
    "population, compute PM2.5 exposure, validate same-station joins, freeze "
    "radius or de-duplication rules, or promote monitor-grade rows."
)

FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "tile_id",
    "selected_economies",
    "coordinate_rows_touching_tile",
    "head_ok",
    "expected_size_bytes",
    "expected_size_mb",
    "exact_file_url",
    "download_decision",
    "downloaded",
    "downloaded_this_run",
    "cache_path",
    "file_size_bytes",
    "size_matches_expected",
    "sha256",
    "http_status",
    "content_type",
    "last_modified",
    "zip_opened",
    "zip_member_count",
    "geotiff_member_count",
    "geotiff_members",
    "geotiff_opened",
    "raster_width",
    "raster_height",
    "raster_count",
    "raster_crs",
    "raster_transform",
    "raster_bounds",
    "raster_dtype",
    "raster_nodata",
    "transform_matches_10_degree_tile_bounds",
    "reader_use",
    "blocking_gap",
    "retrieval_error",
    "non_claim",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def int_value(value: Any) -> int:
    try:
        if value in ("", None):
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def float_value(value: Any) -> float:
    try:
        if value in ("", None):
            return 0.0
        parsed = float(value)
    except (TypeError, ValueError):
        return 0.0
    return parsed if math.isfinite(parsed) else 0.0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_path(tile_id: str, url: str) -> Path:
    filename = Path(url).name or f"{tile_id}.zip"
    return CACHE / filename


def should_download(row: dict[str, Any]) -> tuple[bool, str]:
    if not bool_value(row.get("head_ok")):
        return False, "blocked_selected_tile_head_not_ok"
    expected_mb = float_value(row.get("size_mb"))
    if expected_mb <= 0:
        return False, "blocked_selected_tile_missing_size_metadata"
    if expected_mb > MAX_FIRST_WAVE_MB:
        return False, "deferred_selected_tile_over_first_wave_size_threshold"
    return True, "selected_first_wave_download_candidate"


def download_zip(url: str, path: Path, expected_size: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "downloaded": False,
        "downloaded_this_run": False,
        "file_size_bytes": 0,
        "sha256": "",
        "http_status": "",
        "content_type": "",
        "last_modified": "",
        "retrieval_error": "",
    }
    if path.exists() and (expected_size <= 0 or path.stat().st_size == expected_size):
        result.update(
            {
                "downloaded": True,
                "downloaded_this_run": False,
                "file_size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
        return result

    path.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": USER_AGENT, "Accept": "application/zip,*/*", "Connection": "close"}
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS, stream=True) as response:
            result["http_status"] = response.status_code
            result["content_type"] = response.headers.get("content-type", "")
            result["last_modified"] = response.headers.get("last-modified", "")
            response.raise_for_status()
            digest = hashlib.sha256()
            bytes_written = 0
            with tmp_path.open("wb") as handle:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if not chunk:
                        continue
                    handle.write(chunk)
                    digest.update(chunk)
                    bytes_written += len(chunk)
            tmp_path.replace(path)
            result.update(
                {
                    "downloaded": True,
                    "downloaded_this_run": True,
                    "file_size_bytes": bytes_written,
                    "sha256": digest.hexdigest(),
                }
            )
    except Exception as exc:  # noqa: BLE001 - stored as retrieval evidence
        if tmp_path.exists():
            tmp_path.unlink()
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def inspect_zip_and_raster(path: Path, source_row: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "zip_opened": False,
        "zip_member_count": 0,
        "geotiff_member_count": 0,
        "geotiff_members": "",
        "geotiff_opened": False,
        "raster_width": "",
        "raster_height": "",
        "raster_count": "",
        "raster_crs": "",
        "raster_transform": "",
        "raster_bounds": "",
        "raster_dtype": "",
        "raster_nodata": "",
        "transform_matches_10_degree_tile_bounds": False,
        "metadata_error": "",
    }
    try:
        with zipfile.ZipFile(path) as archive:
            members = archive.namelist()
            tiffs = [name for name in members if name.lower().endswith((".tif", ".tiff"))]
            result.update(
                {
                    "zip_opened": True,
                    "zip_member_count": len(members),
                    "geotiff_member_count": len(tiffs),
                    "geotiff_members": "||".join(tiffs),
                }
            )
    except Exception as exc:  # noqa: BLE001 - stored as retrieval evidence
        result["metadata_error"] = f"{type(exc).__name__}: {exc}"
        return result

    if not result["geotiff_members"]:
        return result

    first_tiff = str(result["geotiff_members"]).split("||")[0]
    raster_url = f"zip://{path.as_posix()}!{first_tiff}"
    try:
        with rasterio.open(raster_url) as dataset:
            bounds = dataset.bounds
            transform = dataset.transform
            expected_west = float_value(source_row.get("west"))
            expected_east = float_value(source_row.get("east"))
            expected_south = float_value(source_row.get("south"))
            expected_north = float_value(source_row.get("north"))
            transform_matches = (
                abs(bounds.left - expected_west) < 0.02
                and abs(bounds.right - expected_east) < 0.02
                and abs(bounds.bottom - expected_south) < 0.02
                and abs(bounds.top - expected_north) < 0.02
            )
            result.update(
                {
                    "geotiff_opened": True,
                    "raster_width": dataset.width,
                    "raster_height": dataset.height,
                    "raster_count": dataset.count,
                    "raster_crs": str(dataset.crs),
                    "raster_transform": "|".join(f"{value:.12g}" for value in transform),
                    "raster_bounds": (
                        f"{bounds.left:.8f},{bounds.bottom:.8f},"
                        f"{bounds.right:.8f},{bounds.top:.8f}"
                    ),
                    "raster_dtype": "||".join(str(dtype) for dtype in dataset.dtypes),
                    "raster_nodata": "" if dataset.nodata is None else dataset.nodata,
                    "transform_matches_10_degree_tile_bounds": transform_matches,
                }
            )
    except Exception as exc:  # noqa: BLE001 - stored as retrieval evidence
        result["metadata_error"] = f"{type(exc).__name__}: {exc}"
    return result


def build_row(generated_at: str, source_row: dict[str, Any]) -> dict[str, Any]:
    expected_size = int_value(source_row.get("content_length_bytes"))
    do_download, decision = should_download(source_row)
    path = cache_path(str(source_row["tile_id"]), str(source_row["exact_file_url"]))
    download = download_zip(str(source_row["exact_file_url"]), path, expected_size) if do_download else {}
    downloaded = bool(download.get("downloaded"))
    metadata = inspect_zip_and_raster(path, source_row) if downloaded else {}
    size_matches = bool(downloaded and expected_size and int_value(download.get("file_size_bytes")) == expected_size)

    blocking_gap = (
        "Selected HEAD-failed tiles must still be retried; all downloaded ZIPs "
        "need checksum and transform inspection before radius/de-duplication "
        "rules can be frozen."
    )
    if downloaded and metadata.get("geotiff_opened"):
        if metadata.get("transform_matches_10_degree_tile_bounds"):
            blocking_gap = (
                "First-wave tile custody and transform inspection are complete "
                "for this row, but selected HEAD-failed tiles, radius rules, "
                "station joins, and grade gates remain open before any "
                "catchment computation."
            )
        else:
            blocking_gap = (
                "The ZIP is downloaded, hashed, and readable, but the GeoTIFF "
                "bounds do not match the simple 10-degree routing assumption. "
                "Revise or verify tile-routing rules before any catchment "
                "computation."
            )

    row = {field: "" for field in FIELDS}
    row.update(
        {
            "generated_at": generated_at,
            "attestation_chain": ATTESTATION,
            "status": STATUS,
            "method": METHOD,
            "tile_id": source_row["tile_id"],
            "selected_economies": source_row["selected_economies"],
            "coordinate_rows_touching_tile": source_row["coordinate_rows_touching_tile"],
            "head_ok": bool_value(source_row.get("head_ok")),
            "expected_size_bytes": expected_size,
            "expected_size_mb": round(expected_size / 1_000_000, 3) if expected_size else "",
            "exact_file_url": source_row["exact_file_url"],
            "download_decision": decision,
            "downloaded": downloaded,
            "downloaded_this_run": bool(download.get("downloaded_this_run")),
            "cache_path": str(path.relative_to(PROGRAM)).replace("\\", "/") if downloaded else "",
            "file_size_bytes": download.get("file_size_bytes", 0),
            "size_matches_expected": size_matches,
            "sha256": download.get("sha256", ""),
            "http_status": download.get("http_status", ""),
            "content_type": download.get("content_type", ""),
            "last_modified": download.get("last_modified", ""),
            "reader_use": (
                "Use downloaded rows as the first-wave checksummed GHSL population denominator custody ledger; "
                "do not use blocked rows as denominator evidence."
            ),
            "blocking_gap": blocking_gap,
            "retrieval_error": download.get("retrieval_error", "") or metadata.get("metadata_error", ""),
            "non_claim": NON_CLAIM,
        }
    )
    row.update(metadata)
    return row


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    selection = read_json(INPUT_SUMMARY)
    rows = [build_row(generated_at, row) for row in selection.get("tile_rows", [])]
    download_candidate_rows = [row for row in rows if row["download_decision"] == "selected_first_wave_download_candidate"]
    downloaded_rows = [row for row in rows if row["downloaded"]]
    head_blocked_rows = [row for row in rows if row["download_decision"] == "blocked_selected_tile_head_not_ok"]
    checksum_rows = [row for row in rows if row["sha256"]]
    geotiff_rows = [row for row in rows if row["geotiff_opened"]]
    transform_match_rows = [row for row in rows if row["transform_matches_10_degree_tile_bounds"]]
    downloaded_bytes = sum(int_value(row["file_size_bytes"]) for row in downloaded_rows)

    counts = {
        "selected_tile_rows": len(rows),
        "first_wave_download_candidate_rows": len(download_candidate_rows),
        "downloaded_population_tile_files": len(downloaded_rows),
        "downloaded_population_tile_files_this_run": sum(1 for row in downloaded_rows if row["downloaded_this_run"]),
        "sha256_checksummed_population_tile_files": len(checksum_rows),
        "downloaded_size_bytes_total": downloaded_bytes,
        "downloaded_size_mb_total": round(downloaded_bytes / 1_000_000, 3),
        "zip_files_opened": sum(1 for row in rows if row["zip_opened"]),
        "geotiff_members_found": sum(int_value(row["geotiff_member_count"]) for row in rows),
        "geotiff_transform_inspected_files": len(geotiff_rows),
        "geotiff_transform_matches_10_degree_tile_bounds": len(transform_match_rows),
        "geotiff_transform_mismatch_files": len(geotiff_rows) - len(transform_match_rows),
        "selected_head_not_ok_blocked_tiles": len(head_blocked_rows),
        "station_radius_population_rows": 0,
        "station_radius_pm25_exposure_rows": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }

    gates = [
        {
            "gate": "Selected GHSL tile queue",
            "status": "available",
            "rows": counts["selected_tile_rows"],
            "reader_use": "The previous gate bounded the population denominator URL queue.",
        },
        {
            "gate": "First-wave downloadable tiles",
            "status": "available",
            "rows": counts["first_wave_download_candidate_rows"],
            "reader_use": "Only selected rows with closed HEAD metadata and size <= 60 MB are downloaded here.",
        },
        {
            "gate": "Population tile ZIP downloads",
            "status": "available"
            if counts["downloaded_population_tile_files"] == counts["first_wave_download_candidate_rows"]
            else "limited",
            "rows": counts["downloaded_population_tile_files"],
            "reader_use": "Downloaded ZIP bodies stay in the ignored cache; hashes are committed.",
        },
        {
            "gate": "Population tile SHA-256 checksums",
            "status": "available"
            if counts["sha256_checksummed_population_tile_files"] == counts["downloaded_population_tile_files"]
            else "limited",
            "rows": counts["sha256_checksummed_population_tile_files"],
            "reader_use": "Checksums support reproducible file custody for downloaded first-wave tiles.",
        },
        {
            "gate": "GeoTIFF transform inspection",
            "status": "available"
            if counts["geotiff_transform_inspected_files"] == counts["downloaded_population_tile_files"]
            else "limited",
            "rows": counts["geotiff_transform_inspected_files"],
            "reader_use": "Raster bounds and transforms are inspected before any catchment calculation.",
        },
        {
            "gate": "10-degree routing assumption check",
            "status": "available"
            if counts["geotiff_transform_mismatch_files"] == 0 and counts["geotiff_transform_inspected_files"] > 0
            else "limited",
            "rows": counts["geotiff_transform_matches_10_degree_tile_bounds"],
            "reader_use": "Downloaded rasters must match the routing assumption before the selected-tile method can be frozen.",
        },
        {
            "gate": "Selected HEAD-failed tile blockers",
            "status": "limited",
            "rows": counts["selected_head_not_ok_blocked_tiles"],
            "reader_use": "These selected tiles remain in the queue and must not disappear from the method.",
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
        "goal_level": "L3 station-radius GHSL population tile checksum and transform gate",
        "first_wave_rule": (
            "Download only selected GHSL tile rows with successful HEAD metadata and recorded size "
            f"at or below {MAX_FIRST_WAVE_MB:.0f} MB; keep all other selected tile rows as blockers."
        ),
        "cache_policy": (
            "Raw GHSL ZIP files are stored under air-monitoring/.cache/station-radius-ghsl-population-tiles/ "
            "and are not committed; rerun this script to rehydrate them from public GHSL tile URLs."
        ),
        "coverage_counts": counts,
        "evidence_gate_counts": gates,
        "tile_checksum_rows": rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM)).replace("\\", "/"),
            "summary_json": str(OUT_SUMMARY.relative_to(PROGRAM)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }

    write_csv(OUT_CSV, rows)
    write_json(OUT_SUMMARY, summary)
    OUT_MD.write_text(render_markdown(summary), encoding="utf-8")
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    counts = summary["coverage_counts"]
    rows = summary["tile_checksum_rows"]
    lines = [
        "# Station-radius GHSL population tile checksum gate",
        "",
        f"`attestation_chain: {summary['attestation_chain']}`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        (
            "This pass downloads and hashes the first wave of selected GHSL "
            "population tile ZIP files, then inspects the GeoTIFF transform "
            "inside each downloaded ZIP. Selected tiles whose HEAD probes did "
            "not close remain explicit blockers."
        ),
        "",
        "## First-wave rule",
        "",
        str(summary["first_wave_rule"]),
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
            "## Tile custody rows",
            "",
            "| Tile | Economies | Decision | Downloaded | SHA-256 | GeoTIFF opened | Bounds match |",
            "|---|---|---|---:|---|---:|---:|",
        ]
    )
    for row in rows:
        sha = f"`{row['sha256']}`" if row["sha256"] else ""
        lines.append(
            "| {tile} | {economies} | {decision} | {downloaded} | {sha} | {opened} | {match} |".format(
                tile=row["tile_id"],
                economies=row["selected_economies"],
                decision=row["download_decision"],
                downloaded=row["downloaded"],
                sha=sha,
                opened=row["geotiff_opened"],
                match=row["transform_matches_10_degree_tile_bounds"],
            )
        )
    lines.extend(["", "## Cache policy", "", str(summary["cache_policy"]), "", "## Non-claim", "", str(summary["non_claim"]), ""])
    return "\n".join(lines)


def main() -> int:
    if not INPUT_SUMMARY.exists():
        raise FileNotFoundError(INPUT_SUMMARY)
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built GHSL population tile checksum gate: "
        f"{counts['selected_tile_rows']} selected tiles; "
        f"{counts['first_wave_download_candidate_rows']} first-wave candidates; "
        f"{counts['downloaded_population_tile_files']} downloaded; "
        f"{counts['sha256_checksummed_population_tile_files']} hashes; "
        f"{counts['geotiff_transform_inspected_files']} GeoTIFF transforms; "
        f"{counts['selected_head_not_ok_blocked_tiles']} selected HEAD blockers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
