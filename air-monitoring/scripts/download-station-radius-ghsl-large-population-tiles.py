#!/usr/bin/env python
"""Download, hash, and inspect deferred large corrected GHSL population tiles.

This gate follows the corrected-queue first-wave custody gate. It targets only
the large corrected GHSL population tiles that were deliberately deferred by
the 60 MB first-wave rule. It closes file custody for those selected tiles
before any station-radius catchment, population, PM2.5 exposure, join, grade,
or map computation is attempted.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"
CACHE = PROGRAM / ".cache" / "station-radius-ghsl-population-tiles"

BASE_SCRIPT = Path(__file__).with_name("download-station-radius-ghsl-corrected-population-tiles.py")
FIRST_WAVE_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-corrected-population-tile-custody-summary.json"

OUT_CSV = GENERATED / "air-monitoring-station-radius-ghsl-large-population-tile-custody.csv"
OUT_SUMMARY = GENERATED / "air-monitoring-station-radius-ghsl-large-population-tile-custody-summary.json"
OUT_MD = PROGRAM / "station-radius-ghsl-large-population-tile-custody.md"

STATUS = "computed_station_radius_ghsl_large_population_tile_custody"
METHOD = "air_monitoring_station_radius_ghsl_large_population_tile_custody_v1"
ATTESTATION = "ai-first"
CHUNK_SIZE = 1024 * 1024
DOWNLOAD_TIMEOUT = (30, 900)

NON_CLAIM = (
    "This large-tile GHSL custody gate downloads, hashes, and inspects only the "
    "three corrected selected population tiles deferred by the first-wave size "
    "threshold. It does not compute station-radius population, compute PM2.5 "
    "exposure, validate same-station joins, freeze radius or de-duplication "
    "rules, or promote monitor-grade rows."
)

FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "tile_id",
    "corrected_selected_economies",
    "corrected_coordinate_rows_touching_tile",
    "exact_file_url",
    "corrected_bounds",
    "first_wave_decision",
    "head_ok",
    "head_status",
    "head_content_length_bytes",
    "head_size_mb",
    "head_last_modified",
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


def load_base_module() -> Any:
    spec = importlib.util.spec_from_file_location("corrected_ghsl_custody", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base_module()


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_row_from_first_wave(row: dict[str, Any]) -> dict[str, Any]:
    west, south, east, north = [float(part) for part in str(row["corrected_bounds"]).split(",")]
    enriched = dict(row)
    enriched.update(
        {
            "corrected_west": west,
            "corrected_south": south,
            "corrected_east": east,
            "corrected_north": north,
        }
    )
    return enriched


def deferred_large_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        source_row_from_first_wave(row)
        for row in summary.get("tile_custody_rows", [])
        if str(row.get("download_decision", "")).startswith("deferred")
    ]
    return sorted(rows, key=lambda row: str(row["tile_id"]))


def download_large_zip(url: str, path: Path) -> dict[str, Any]:
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

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with requests.get(url, headers=BASE.headers(), timeout=DOWNLOAD_TIMEOUT, stream=True) as response:
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


def blocking_gap(row: dict[str, Any]) -> str:
    if not BASE.truthy(row["downloaded"]):
        return "The large corrected selected tile still lacks ZIP custody and remains a denominator blocker."
    if not BASE.truthy(row["geotiff_opened"]):
        return "The large ZIP is downloaded and hashed, but the GeoTIFF payload has not opened cleanly."
    if not BASE.truthy(row["transform_matches_corrected_tile_bounds"]):
        return "The large GeoTIFF opened, but its bounds do not match the corrected GHSL tile origin."
    return (
        "Large-tile file custody and corrected-bound inspection are closed for this tile, "
        "but catchment radius, de-duplication, station joins, and grade assumptions remain open."
    )


def build_row(generated_at: str, source_row: dict[str, Any]) -> dict[str, Any]:
    tile_id = str(source_row["tile_id"])
    url = str(source_row["exact_file_url"])
    path = BASE.cache_path(tile_id, url)
    probe = BASE.probe_url(tile_id, url)
    download = download_large_zip(url, path)
    downloaded = BASE.truthy(download.get("downloaded"))
    metadata = BASE.inspect_zip_and_raster(path, source_row) if downloaded else {}
    size_matches = (
        downloaded
        and BASE.int_value(probe.get("custody_size_bytes")) > 0
        and BASE.int_value(download.get("file_size_bytes")) == BASE.int_value(probe.get("custody_size_bytes"))
    )

    row = {field: "" for field in FIELDS}
    row.update(
        {
            "generated_at": generated_at,
            "attestation_chain": ATTESTATION,
            "status": STATUS,
            "method": METHOD,
            "tile_id": tile_id,
            "corrected_selected_economies": source_row.get("corrected_selected_economies", ""),
            "corrected_coordinate_rows_touching_tile": source_row.get("corrected_coordinate_rows_touching_tile", 0),
            "exact_file_url": url,
            "corrected_bounds": source_row.get("corrected_bounds", ""),
            "first_wave_decision": source_row.get("download_decision", ""),
            "head_ok": probe.get("head_ok", False),
            "head_status": probe.get("head_status", ""),
            "head_content_length_bytes": probe.get("head_content_length_bytes", 0),
            "head_size_mb": probe.get("head_size_mb", ""),
            "head_last_modified": probe.get("head_last_modified", ""),
            "custody_probe_source": probe.get("custody_probe_source", "none"),
            "custody_size_bytes": probe.get("custody_size_bytes", 0),
            "custody_size_mb": probe.get("custody_size_mb", ""),
            "download_decision": "large_corrected_tile_full_custody_download",
            "downloaded": downloaded,
            "downloaded_this_run": BASE.truthy(download.get("downloaded_this_run")),
            "downloaded_from_prior_cache": BASE.truthy(download.get("downloaded_from_prior_cache")),
            "cache_path": str(path.relative_to(PROGRAM)).replace("\\", "/") if downloaded else "",
            "file_size_bytes": download.get("file_size_bytes", 0),
            "size_matches_custody_probe": size_matches,
            "sha256": download.get("sha256", ""),
            "reader_use": (
                "Use this row as large corrected GHSL population denominator file-custody evidence; "
                "do not compute catchments until radius, de-duplication, join, and grade rules are frozen."
            ),
            "retrieval_error": download.get("retrieval_error", "") or metadata.get("metadata_error", ""),
            "non_claim": NON_CLAIM,
        }
    )
    row.update(metadata)
    row["blocking_gap"] = blocking_gap(row)
    return row


def evidence_gates(counts: dict[str, Any]) -> list[dict[str, Any]]:
    full_custody_closed = counts["remaining_large_tile_blockers"] == 0
    return [
        {
            "gate": "Deferred large corrected tile queue",
            "status": "available",
            "rows": counts["large_corrected_tile_rows"],
            "reader_use": "The prior custody gate defines the large selected GHSL tiles that still need full file custody.",
        },
        {
            "gate": "Large corrected tile current URL probes",
            "status": "available" if counts["current_head_ok_large_tiles"] == counts["large_corrected_tile_rows"] else "limited",
            "rows": counts["current_head_ok_large_tiles"],
            "reader_use": "HEAD probes confirm the large GHSL files are reachable and size-observed before download.",
        },
        {
            "gate": "Large corrected population ZIP custody",
            "status": "available" if counts["downloaded_large_population_tile_files"] == counts["large_corrected_tile_rows"] else "limited",
            "rows": counts["downloaded_large_population_tile_files"],
            "reader_use": "Large ZIP files are downloaded or reused from ignored cache and may now join the first-wave custody set.",
        },
        {
            "gate": "Large corrected population SHA-256 checksums",
            "status": "available" if counts["sha256_checksummed_large_population_tile_files"] == counts["downloaded_large_population_tile_files"] else "limited",
            "rows": counts["sha256_checksummed_large_population_tile_files"],
            "reader_use": "Hashes make the large-file custody reproducible without committing raw ZIP bodies.",
        },
        {
            "gate": "Large corrected-bound GeoTIFF inspection",
            "status": "available" if counts["large_geotiff_transform_mismatch_corrected_bounds"] == 0 and counts["large_geotiff_opened_files"] else "limited",
            "rows": counts["large_geotiff_transform_matches_corrected_bounds"],
            "reader_use": "Opened large rasters must match the corrected GHSL tile bounds before catchments are computed.",
        },
        {
            "gate": "Full corrected GHSL population file custody",
            "status": "available" if full_custody_closed else "limited",
            "rows": counts["corrected_tile_files_in_custody_after_large_pass"],
            "reader_use": "First-wave plus large-tile file custody should cover all 21 corrected selected GHSL population tiles.",
        },
        {
            "gate": "Station-radius population computation",
            "status": "not_computed",
            "rows": 0,
            "reader_use": "No catchment population, PM2.5 exposure, join, grade, or map is computed here.",
        },
    ]


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    first_wave = read_json(FIRST_WAVE_SUMMARY)
    source_rows = deferred_large_rows(first_wave)
    rows = [build_row(generated_at, row) for row in source_rows]

    downloaded_rows = [row for row in rows if BASE.truthy(row["downloaded"])]
    checksum_rows = [row for row in rows if row["sha256"]]
    geotiff_rows = [row for row in rows if BASE.truthy(row["geotiff_opened"])]
    match_rows = [row for row in rows if BASE.truthy(row["transform_matches_corrected_tile_bounds"])]
    downloaded_bytes = sum(BASE.int_value(row["file_size_bytes"]) for row in downloaded_rows)
    first_counts = first_wave["coverage_counts"]
    first_wave_downloaded = BASE.int_value(first_counts.get("downloaded_population_tile_files"))
    total_corrected_tiles = BASE.int_value(first_counts.get("corrected_tile_rows"))

    counts = {
        "large_corrected_tile_rows": len(rows),
        "current_head_ok_large_tiles": sum(1 for row in rows if BASE.truthy(row["head_ok"])),
        "downloaded_large_population_tile_files": len(downloaded_rows),
        "downloaded_large_population_tile_files_this_run": sum(1 for row in downloaded_rows if BASE.truthy(row["downloaded_this_run"])),
        "downloaded_large_population_tile_files_from_prior_cache": sum(1 for row in downloaded_rows if BASE.truthy(row["downloaded_from_prior_cache"])),
        "sha256_checksummed_large_population_tile_files": len(checksum_rows),
        "downloaded_large_size_bytes_total": downloaded_bytes,
        "downloaded_large_size_mb_total": round(downloaded_bytes / 1_000_000, 3),
        "large_zip_files_opened": sum(1 for row in rows if BASE.truthy(row["zip_opened"])),
        "large_geotiff_opened_files": len(geotiff_rows),
        "large_geotiff_transform_matches_corrected_bounds": len(match_rows),
        "large_geotiff_transform_mismatch_corrected_bounds": len(geotiff_rows) - len(match_rows),
        "remaining_large_tile_blockers": len(rows) - len(downloaded_rows),
        "first_wave_corrected_tile_files_in_custody": first_wave_downloaded,
        "corrected_tile_files_in_custody_after_large_pass": first_wave_downloaded + len(downloaded_rows),
        "corrected_tile_files_required": total_corrected_tiles,
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
        "goal_level": "L3 station-radius GHSL large corrected population tile custody gate",
        "source_gate": str(FIRST_WAVE_SUMMARY.relative_to(PROGRAM)).replace("\\", "/"),
        "target_rule": "Download and inspect only corrected selected GHSL population tiles deferred by the 60 MB first-wave rule.",
        "cache_policy": (
            "Raw GHSL ZIP files are stored under air-monitoring/.cache/station-radius-ghsl-population-tiles/ "
            "and are not committed; rerun this script to rehydrate the large corrected tiles from public GHSL URLs."
        ),
        "coverage_counts": counts,
        "evidence_gate_counts": evidence_gates(counts),
        "large_tile_custody_rows": rows,
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
    rows = summary["large_tile_custody_rows"]
    lines = [
        "# Station-radius GHSL large population tile custody gate",
        "",
        f"`attestation_chain: {summary['attestation_chain']}`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        (
            "This pass targets the corrected selected GHSL population tiles that "
            "were too large for the first-wave custody gate. It downloads or "
            "reuses those large ZIP files, records SHA-256 hashes, and checks "
            "opened GeoTIFF bounds against the corrected GHSL tile origin."
        ),
        "",
        "## Target rule",
        "",
        str(summary["target_rule"]),
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
            "## Large tile custody rows",
            "",
            "| Tile | Economies | Probe | Downloaded | SHA-256 | Corrected bounds match |",
            "|---|---|---|---:|---|---:|",
        ]
    )
    for row in rows:
        probe = row["custody_probe_source"]
        if row["custody_size_mb"]:
            probe = f"{probe} {row['custody_size_mb']} MB"
        sha = f"`{row['sha256']}`" if row["sha256"] else ""
        lines.append(
            "| {tile} | {economies} | {probe} | {downloaded} | {sha} | {match} |".format(
                tile=row["tile_id"],
                economies=row["corrected_selected_economies"],
                probe=probe,
                downloaded=row["downloaded"],
                sha=sha,
                match=row["transform_matches_corrected_tile_bounds"],
            )
        )
    lines.extend(["", "## Cache policy", "", str(summary["cache_policy"]), "", "## Non-claim", "", str(summary["non_claim"]), ""])
    return "\n".join(lines)


def main() -> int:
    if not FIRST_WAVE_SUMMARY.exists():
        raise FileNotFoundError(FIRST_WAVE_SUMMARY)
    summary = build_outputs()
    counts = summary["coverage_counts"]
    print(
        "Built GHSL large corrected population tile custody gate: "
        f"{counts['large_corrected_tile_rows']} large tiles; "
        f"{counts['current_head_ok_large_tiles']} current HEAD-OK probes; "
        f"{counts['downloaded_large_population_tile_files']} downloaded; "
        f"{counts['sha256_checksummed_large_population_tile_files']} hashes; "
        f"{counts['large_geotiff_transform_matches_corrected_bounds']} corrected-bound matches; "
        f"{counts['corrected_tile_files_in_custody_after_large_pass']}/"
        f"{counts['corrected_tile_files_required']} corrected tile files in custody; "
        f"{counts['station_radius_population_rows']} catchment rows."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
