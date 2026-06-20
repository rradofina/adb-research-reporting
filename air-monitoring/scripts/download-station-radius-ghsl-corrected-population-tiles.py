#!/usr/bin/env python
"""Probe, download, hash, and inspect corrected-queue GHSL population tiles.

This gate follows the GHSL tile-routing correction gate. It uses the corrected
21-tile population queue, preserves already downloaded retained ZIP custody,
retries corrected first-wave download candidates, and compares opened raster
bounds against the corrected GHSL origin. It does not compute station-radius
population, exposure, joins, or maps.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import rasterio
import requests


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"
CACHE = PROGRAM / ".cache" / "station-radius-ghsl-population-tiles"

ROUTING_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-tile-routing-correction-summary.json"

OUT_CSV = GENERATED / "air-monitoring-station-radius-ghsl-corrected-population-tile-custody.csv"
OUT_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-corrected-population-tile-custody-summary.json"
OUT_MD = PROGRAM / "station-radius-ghsl-corrected-population-tile-custody.md"

STATUS = "computed_station_radius_ghsl_corrected_population_tile_custody"
METHOD = "air_monitoring_station_radius_ghsl_corrected_population_tile_custody_v1"
ATTESTATION = "ai-first"
MAX_FIRST_WAVE_MB = 60.0
CHUNK_SIZE = 1024 * 1024
PROBE_TIMEOUT = (20, 45)
DOWNLOAD_TIMEOUT = (30, 180)
MAX_PROBE_WORKERS = 5
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)

NON_CLAIM = (
    "This corrected-queue GHSL population tile custody gate probes the corrected "
    "tile URLs, reuses or downloads ZIP files, records SHA-256 hashes, and "
    "checks opened GeoTIFF bounds against the corrected GHSL tile origin. It "
    "does not compute station-radius population, compute PM2.5 exposure, "
    "validate same-station joins, freeze radius or de-duplication rules, or "
    "promote monitor-grade rows."
)

FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "tile_id",
    "correction_status",
    "corrected_selected_economies",
    "corrected_coordinate_rows_touching_tile",
    "exact_file_url",
    "corrected_bounds",
    "prior_head_ok",
    "prior_head_status",
    "prior_size_mb",
    "prior_downloaded",
    "prior_sha256",
    "prior_geotiff_opened",
    "head_probe_attempted",
    "head_ok",
    "head_status",
    "head_content_length_bytes",
    "head_size_mb",
    "head_content_type",
    "head_last_modified",
    "head_error",
    "range_probe_attempted",
    "range_ok",
    "range_status",
    "range_content_length_bytes",
    "range_total_size_bytes",
    "range_size_mb",
    "range_content_range",
    "range_error",
    "custody_probe_source",
    "custody_size_bytes",
    "custody_size_mb",
    "download_decision",
    "downloaded",
    "downloaded_this_run",
    "downloaded_from_prior_cache",
    "cache_path",
    "file_size_bytes",
    "size_matches_custody_probe",
    "sha256",
    "sha256_matches_prior",
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
    "transform_matches_corrected_tile_bounds",
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


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() == "true"


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


def round_float(value: float, digits: int = 8) -> float:
    return round(value, digits)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cache_path(tile_id: str, url: str) -> Path:
    filename = Path(url).name or f"{tile_id}.zip"
    return CACHE / filename


def parse_total_from_content_range(value: str) -> int:
    match = re.search(r"/(\d+)$", value or "")
    return int(match.group(1)) if match else 0


def headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    base = {"User-Agent": USER_AGENT, "Accept": "application/zip,*/*", "Connection": "close"}
    if extra:
        base.update(extra)
    return base


def probe_url(tile_id: str, url: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "tile_id": tile_id,
        "head_probe_attempted": True,
        "head_ok": False,
        "head_status": "",
        "head_content_length_bytes": 0,
        "head_size_mb": "",
        "head_content_type": "",
        "head_last_modified": "",
        "head_error": "",
        "range_probe_attempted": False,
        "range_ok": False,
        "range_status": "",
        "range_content_length_bytes": 0,
        "range_total_size_bytes": 0,
        "range_size_mb": "",
        "range_content_range": "",
        "range_error": "",
        "custody_probe_source": "none",
        "custody_size_bytes": 0,
        "custody_size_mb": "",
    }

    try:
        response = requests.head(url, headers=headers(), allow_redirects=True, timeout=PROBE_TIMEOUT)
        result["head_status"] = response.status_code
        result["head_content_type"] = response.headers.get("content-type", "")
        result["head_last_modified"] = response.headers.get("last-modified", "")
        head_length = int_value(response.headers.get("content-length"))
        result["head_content_length_bytes"] = head_length
        result["head_size_mb"] = round(head_length / 1_000_000, 3) if head_length else ""
        result["head_ok"] = response.status_code == 200 and head_length > 0
        response.close()
    except Exception as exc:  # noqa: BLE001 - stored as public retrieval evidence
        result["head_error"] = f"{type(exc).__name__}: {exc}"

    if result["head_ok"]:
        result["custody_probe_source"] = "head"
        result["custody_size_bytes"] = result["head_content_length_bytes"]
        result["custody_size_mb"] = result["head_size_mb"]
        return result

    result["range_probe_attempted"] = True
    try:
        with requests.get(
            url,
            headers=headers({"Range": "bytes=0-0"}),
            allow_redirects=True,
            stream=True,
            timeout=PROBE_TIMEOUT,
        ) as response:
            result["range_status"] = response.status_code
            result["range_content_range"] = response.headers.get("content-range", "")
            content_length = int_value(response.headers.get("content-length"))
            total_size = parse_total_from_content_range(result["range_content_range"]) or content_length
            result["range_content_length_bytes"] = content_length
            result["range_total_size_bytes"] = total_size
            result["range_size_mb"] = round(total_size / 1_000_000, 3) if total_size else ""
            result["range_ok"] = response.status_code in (200, 206) and total_size > 0
    except Exception as exc:  # noqa: BLE001 - stored as public retrieval evidence
        result["range_error"] = f"{type(exc).__name__}: {exc}"

    if result["range_ok"]:
        result["custody_probe_source"] = "range"
        result["custody_size_bytes"] = result["range_total_size_bytes"]
        result["custody_size_mb"] = result["range_size_mb"]
    return result


def decide_download(source_row: dict[str, Any], probe: dict[str, Any], path: Path) -> str:
    if path.exists() and path.stat().st_size > 0:
        return "retained_corrected_queue_cached_zip"
    size_bytes = int_value(probe.get("custody_size_bytes"))
    if size_bytes <= 0:
        if truthy(source_row.get("prior_head_ok")):
            return "blocked_current_probe_failed_prior_head_ok"
        return "blocked_current_probe_not_ok"
    size_mb = size_bytes / 1_000_000
    if size_mb > MAX_FIRST_WAVE_MB:
        return "deferred_corrected_tile_over_first_wave_size_threshold"
    return "corrected_first_wave_download_candidate"


def download_zip(url: str, path: Path, expected_size: int, decision: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "downloaded": False,
        "downloaded_this_run": False,
        "downloaded_from_prior_cache": False,
        "file_size_bytes": 0,
        "sha256": "",
        "http_status": "",
        "content_type": "",
        "last_modified": "",
        "retrieval_error": "",
    }

    if path.exists() and path.stat().st_size > 0:
        result.update(
            {
                "downloaded": True,
                "downloaded_this_run": False,
                "downloaded_from_prior_cache": True,
                "file_size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
        return result

    if decision != "corrected_first_wave_download_candidate":
        return result

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with requests.get(url, headers=headers(), timeout=DOWNLOAD_TIMEOUT, stream=True) as response:
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
                    "downloaded_from_prior_cache": False,
                    "file_size_bytes": bytes_written,
                    "sha256": digest.hexdigest(),
                }
            )
    except Exception as exc:  # noqa: BLE001 - stored as public retrieval evidence
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
        "transform_matches_corrected_tile_bounds": False,
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
    except Exception as exc:  # noqa: BLE001 - stored as public metadata evidence
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
            expected_west = float_value(source_row.get("corrected_west"))
            expected_east = float_value(source_row.get("corrected_east"))
            expected_south = float_value(source_row.get("corrected_south"))
            expected_north = float_value(source_row.get("corrected_north"))
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
                    "transform_matches_corrected_tile_bounds": transform_matches,
                }
            )
    except Exception as exc:  # noqa: BLE001 - stored as public metadata evidence
        result["metadata_error"] = f"{type(exc).__name__}: {exc}"
    return result


def corrected_bounds_text(row: dict[str, Any]) -> str:
    return (
        f"{float_value(row.get('corrected_west')):.8f},"
        f"{float_value(row.get('corrected_south')):.8f},"
        f"{float_value(row.get('corrected_east')):.8f},"
        f"{float_value(row.get('corrected_north')):.8f}"
    )


def blocking_gap(row: dict[str, Any]) -> str:
    if not row["downloaded"]:
        if row["download_decision"].startswith("blocked"):
            return (
                "The corrected tile remains selected but current public probe or download custody did not close. "
                "It must stay visible as a denominator blocker."
            )
        if row["download_decision"].startswith("deferred"):
            return "The corrected tile is selected but exceeds the first-wave size threshold."
        return "The corrected tile is not in custody."
    if not row["geotiff_opened"]:
        return "The ZIP is downloaded and hashed, but the GeoTIFF payload has not opened cleanly."
    if not row["transform_matches_corrected_tile_bounds"]:
        return "The GeoTIFF opened, but its bounds do not match the corrected GHSL tile origin."
    return (
        "Corrected-queue file custody and corrected-bound inspection are closed for this tile, "
        "but catchment radius, de-duplication, station joins, and grade assumptions remain open."
    )


def build_row(generated_at: str, source_row: dict[str, Any], probe: dict[str, Any]) -> dict[str, Any]:
    tile_id = str(source_row["tile_id"])
    path = cache_path(tile_id, str(source_row["exact_file_url"]))
    decision = decide_download(source_row, probe, path)
    download = download_zip(str(source_row["exact_file_url"]), path, int_value(probe.get("custody_size_bytes")), decision)
    downloaded = truthy(download.get("downloaded"))
    metadata = inspect_zip_and_raster(path, source_row) if downloaded else {}
    size_matches = (
        downloaded
        and int_value(probe.get("custody_size_bytes")) > 0
        and int_value(download.get("file_size_bytes")) == int_value(probe.get("custody_size_bytes"))
    )
    sha = str(download.get("sha256", ""))
    prior_sha = str(source_row.get("prior_sha256", ""))

    row = {field: "" for field in FIELDS}
    row.update(
        {
            "generated_at": generated_at,
            "attestation_chain": ATTESTATION,
            "status": STATUS,
            "method": METHOD,
            "tile_id": tile_id,
            "correction_status": source_row.get("correction_status", ""),
            "corrected_selected_economies": source_row.get("corrected_selected_economies", ""),
            "corrected_coordinate_rows_touching_tile": source_row.get("corrected_coordinate_rows_touching_tile", 0),
            "exact_file_url": source_row.get("exact_file_url", ""),
            "corrected_bounds": corrected_bounds_text(source_row),
            "prior_head_ok": source_row.get("prior_head_ok", ""),
            "prior_head_status": source_row.get("prior_head_status", ""),
            "prior_size_mb": source_row.get("prior_size_mb", ""),
            "prior_downloaded": source_row.get("prior_downloaded", ""),
            "prior_sha256": prior_sha,
            "prior_geotiff_opened": source_row.get("prior_geotiff_opened", ""),
            "head_probe_attempted": probe.get("head_probe_attempted", False),
            "head_ok": probe.get("head_ok", False),
            "head_status": probe.get("head_status", ""),
            "head_content_length_bytes": probe.get("head_content_length_bytes", 0),
            "head_size_mb": probe.get("head_size_mb", ""),
            "head_content_type": probe.get("head_content_type", ""),
            "head_last_modified": probe.get("head_last_modified", ""),
            "head_error": probe.get("head_error", ""),
            "range_probe_attempted": probe.get("range_probe_attempted", False),
            "range_ok": probe.get("range_ok", False),
            "range_status": probe.get("range_status", ""),
            "range_content_length_bytes": probe.get("range_content_length_bytes", 0),
            "range_total_size_bytes": probe.get("range_total_size_bytes", 0),
            "range_size_mb": probe.get("range_size_mb", ""),
            "range_content_range": probe.get("range_content_range", ""),
            "range_error": probe.get("range_error", ""),
            "custody_probe_source": probe.get("custody_probe_source", "none"),
            "custody_size_bytes": probe.get("custody_size_bytes", 0),
            "custody_size_mb": probe.get("custody_size_mb", ""),
            "download_decision": decision,
            "downloaded": downloaded,
            "downloaded_this_run": truthy(download.get("downloaded_this_run")),
            "downloaded_from_prior_cache": truthy(download.get("downloaded_from_prior_cache")),
            "cache_path": str(path.relative_to(PROGRAM)).replace("\\", "/") if downloaded else "",
            "file_size_bytes": download.get("file_size_bytes", 0),
            "size_matches_custody_probe": size_matches,
            "sha256": sha,
            "sha256_matches_prior": bool(sha and prior_sha and sha == prior_sha),
            "http_status": download.get("http_status", ""),
            "content_type": download.get("content_type", ""),
            "last_modified": download.get("last_modified", ""),
            "reader_use": (
                "Use downloaded rows as corrected-queue GHSL population denominator custody evidence; "
                "do not use blocked rows for catchment denominators."
            ),
            "retrieval_error": download.get("retrieval_error", "") or metadata.get("metadata_error", ""),
            "non_claim": NON_CLAIM,
        }
    )
    row.update(metadata)
    row["blocking_gap"] = blocking_gap(row)
    return row


def corrected_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in summary.get("tile_rows", []) if truthy(row.get("corrected_selected"))]
    return sorted(rows, key=lambda row: (int_value(row.get("tile_row")), int_value(row.get("tile_col"))))


def probe_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    probes: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=MAX_PROBE_WORKERS) as executor:
        futures = {
            executor.submit(probe_url, str(row["tile_id"]), str(row["exact_file_url"])): str(row["tile_id"])
            for row in rows
        }
        for future in as_completed(futures):
            tile_id = futures[future]
            try:
                probes[tile_id] = future.result()
            except Exception as exc:  # noqa: BLE001 - stored as public retrieval evidence
                probes[tile_id] = {
                    "tile_id": tile_id,
                    "head_probe_attempted": True,
                    "head_ok": False,
                    "head_error": f"{type(exc).__name__}: {exc}",
                    "range_probe_attempted": False,
                    "range_ok": False,
                    "range_error": "",
                    "custody_probe_source": "none",
                    "custody_size_bytes": 0,
                    "custody_size_mb": "",
                }
    return probes


def evidence_gates(counts: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "Corrected GHSL tile queue",
            "status": "available",
            "rows": counts["corrected_tile_rows"],
            "reader_use": "The corrected routing gate defines the denominator URL queue used here.",
        },
        {
            "gate": "Current public URL probes",
            "status": "available" if counts["current_probe_size_available_tiles"] == counts["corrected_tile_rows"] else "limited",
            "rows": counts["current_probe_size_available_tiles"],
            "reader_use": "HEAD or range probes provide current file-size custody before download decisions.",
        },
        {
            "gate": "Corrected first-wave eligible tiles",
            "status": "available",
            "rows": counts["corrected_first_wave_eligible_rows"],
            "reader_use": "Only corrected selected rows with current size <= 60 MB are eligible for this custody pass.",
        },
        {
            "gate": "Corrected population tile ZIP custody",
            "status": "available" if counts["downloaded_population_tile_files"] == counts["corrected_tile_rows"] else "limited",
            "rows": counts["downloaded_population_tile_files"],
            "reader_use": "Downloaded ZIP files are hashed and inspected, but raw ZIP bodies stay in the ignored cache.",
        },
        {
            "gate": "Corrected population tile SHA-256 checksums",
            "status": "available" if counts["sha256_checksummed_population_tile_files"] == counts["downloaded_population_tile_files"] else "limited",
            "rows": counts["sha256_checksummed_population_tile_files"],
            "reader_use": "Hashes make downloaded file custody reproducible without committing raw ZIP bodies.",
        },
        {
            "gate": "Corrected-bound GeoTIFF inspection",
            "status": "available" if counts["geotiff_transform_mismatch_corrected_bounds"] == 0 and counts["geotiff_opened_files"] else "limited",
            "rows": counts["geotiff_transform_matches_corrected_bounds"],
            "reader_use": "Opened rasters must match the corrected tile origin before catchments are computed.",
        },
        {
            "gate": "Deferred large corrected tiles",
            "status": "limited" if counts["deferred_corrected_selected_tiles"] else "available",
            "rows": counts["deferred_corrected_selected_tiles"],
            "reader_use": "Large selected tiles need a separate full-custody pass before catchments are complete.",
        },
        {
            "gate": "Blocked corrected selected tiles",
            "status": "limited" if counts["blocked_corrected_selected_tiles"] else "available",
            "rows": counts["blocked_corrected_selected_tiles"],
            "reader_use": "Blocked selected tiles remain visible as denominator blockers.",
        },
        {
            "gate": "Station-radius population computation",
            "status": "not_computed",
            "rows": 0,
            "reader_use": "No catchment population, PM2.5 exposure, or map is computed here.",
        },
    ]


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    routing = read_json(ROUTING_SUMMARY)
    source_rows = corrected_rows(routing)
    probes = probe_rows(source_rows)
    rows = [build_row(generated_at, row, probes[str(row["tile_id"])]) for row in source_rows]

    downloaded_rows = [row for row in rows if truthy(row["downloaded"])]
    current_probe_rows = [row for row in rows if int_value(row["custody_size_bytes"]) > 0]
    first_wave_eligible_rows = [
        row
        for row in rows
        if int_value(row["custody_size_bytes"]) > 0
        and float_value(row["custody_size_mb"]) <= MAX_FIRST_WAVE_MB
    ]
    first_wave_candidate_rows = [
        row for row in rows if row["download_decision"] == "corrected_first_wave_download_candidate"
    ]
    blocked_rows = [row for row in rows if str(row["download_decision"]).startswith("blocked")]
    checksum_rows = [row for row in rows if row["sha256"]]
    geotiff_rows = [row for row in rows if truthy(row["geotiff_opened"])]
    match_rows = [row for row in rows if truthy(row["transform_matches_corrected_tile_bounds"])]
    downloaded_bytes = sum(int_value(row["file_size_bytes"]) for row in downloaded_rows)

    counts = {
        "corrected_tile_rows": len(rows),
        "retained_corrected_tile_rows": sum(1 for row in rows if row["correction_status"] == "retained_by_corrected_origin"),
        "added_corrected_tile_rows": sum(1 for row in rows if row["correction_status"] == "added_by_corrected_origin"),
        "current_head_ok_tiles": sum(1 for row in rows if truthy(row["head_ok"])),
        "current_range_ok_tiles": sum(1 for row in rows if truthy(row["range_ok"])),
        "current_probe_size_available_tiles": len(current_probe_rows),
        "corrected_first_wave_eligible_rows": len(first_wave_eligible_rows),
        "corrected_first_wave_download_candidate_rows": len(first_wave_candidate_rows),
        "downloaded_population_tile_files": len(downloaded_rows),
        "downloaded_population_tile_files_this_run": sum(1 for row in downloaded_rows if truthy(row["downloaded_this_run"])),
        "downloaded_population_tile_files_from_prior_cache": sum(1 for row in downloaded_rows if truthy(row["downloaded_from_prior_cache"])),
        "sha256_checksummed_population_tile_files": len(checksum_rows),
        "sha256_matches_prior_rows": sum(1 for row in rows if truthy(row["sha256_matches_prior"])),
        "downloaded_size_bytes_total": downloaded_bytes,
        "downloaded_size_mb_total": round(downloaded_bytes / 1_000_000, 3),
        "zip_files_opened": sum(1 for row in rows if truthy(row["zip_opened"])),
        "geotiff_opened_files": len(geotiff_rows),
        "geotiff_transform_matches_corrected_bounds": len(match_rows),
        "geotiff_transform_mismatch_corrected_bounds": len(geotiff_rows) - len(match_rows),
        "blocked_corrected_selected_tiles": len(blocked_rows),
        "deferred_corrected_selected_tiles": sum(1 for row in rows if str(row["download_decision"]).startswith("deferred")),
        "station_radius_population_rows": 0,
        "station_radius_pm25_exposure_rows": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }

    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius GHSL corrected population tile custody gate",
        "first_wave_rule": (
            "Probe the corrected selected GHSL tile URLs; download only rows with current public size "
            f"at or below {MAX_FIRST_WAVE_MB:.0f} MB; reuse retained cached ZIPs; keep all unresolved "
            "corrected selected rows as blockers."
        ),
        "cache_policy": (
            "Raw GHSL ZIP files are stored under air-monitoring/.cache/station-radius-ghsl-population-tiles/ "
            "and are not committed; rerun this script to rehydrate them from public GHSL tile URLs."
        ),
        "coverage_counts": counts,
        "evidence_gate_counts": evidence_gates(counts),
        "tile_custody_rows": rows,
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
    rows = summary["tile_custody_rows"]
    lines = [
        "# Station-radius GHSL corrected population tile custody gate",
        "",
        f"`attestation_chain: {summary['attestation_chain']}`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        (
            "This pass moves from the corrected routing queue to corrected tile "
            "custody. It probes the corrected GHSL URLs, reuses retained cached "
            "ZIP files, retries first-wave candidates, records SHA-256 hashes, "
            "and checks opened raster bounds against the corrected origin."
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
            "## Corrected queue custody rows",
            "",
            "| Tile | Correction | Economies | Probe | Decision | Downloaded | SHA-256 | Corrected bounds match |",
            "|---|---|---|---|---|---:|---|---:|",
        ]
    )
    for row in rows:
        sha = f"`{row['sha256']}`" if row["sha256"] else ""
        probe = row["custody_probe_source"]
        if row["custody_size_mb"]:
            probe = f"{probe} {row['custody_size_mb']} MB"
        lines.append(
            "| {tile} | {status} | {economies} | {probe} | {decision} | {downloaded} | {sha} | {match} |".format(
                tile=row["tile_id"],
                status=row["correction_status"],
                economies=row["corrected_selected_economies"],
                probe=probe,
                decision=row["download_decision"],
                downloaded=row["downloaded"],
                sha=sha,
                match=row["transform_matches_corrected_tile_bounds"],
            )
        )
    lines.extend(["", "## Cache policy", "", str(summary["cache_policy"]), "", "## Non-claim", "", str(summary["non_claim"]), ""])
    return "\n".join(lines)


def main() -> int:
    if not ROUTING_SUMMARY.exists():
        raise FileNotFoundError(ROUTING_SUMMARY)
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built GHSL corrected population tile custody gate: "
        f"{counts['corrected_tile_rows']} corrected tiles; "
        f"{counts['current_probe_size_available_tiles']} current size probes; "
        f"{counts['corrected_first_wave_eligible_rows']} first-wave eligible; "
        f"{counts['corrected_first_wave_download_candidate_rows']} download candidates this run; "
        f"{counts['downloaded_population_tile_files']} downloaded; "
        f"{counts['sha256_checksummed_population_tile_files']} hashes; "
        f"{counts['geotiff_transform_matches_corrected_bounds']} corrected-bound matches; "
        f"{counts['station_radius_population_rows']} catchment rows."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
