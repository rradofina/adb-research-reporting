"""Download and checksum the approved ACAG coarse PM2.5 pilot objects.

This pass follows the ACAG version-decision gate. It downloads only the two
approved 2023 V6.GL.03 coarse NetCDF objects into the ignored local cache,
computes SHA-256 hashes, inspects NetCDF dimensions/variables, and writes a
committed checksum/metadata ledger. It does not compute PM2.5 exposure or
station-radius catchments.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from netCDF4 import Dataset


logging.disable(logging.WARNING)

PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
CACHE_DIR = PROGRAM_DIR / ".cache" / "station-radius-acag-coarse-checksums"

VERSION_DECISION_JSON = GENERATED_DIR / "air-monitoring-station-radius-acag-version-decision-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-acag-coarse-checksums.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-acag-coarse-checksums-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-acag-coarse-checksums.md"

METHOD = "air_monitoring_station_radius_acag_coarse_checksums_v1"
STATUS = "computed_station_radius_acag_coarse_checksums"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 120
CHUNK_SIZE = 1024 * 512
NON_CLAIM = (
    "This ACAG coarse checksum pass downloads and hashes only the two approved "
    "2023 V6.GL.03 coarse PM2.5 pilot objects and inspects NetCDF metadata. It "
    "does not download fine-resolution PM2.5 files; does not select or download "
    "a population denominator; does not compute PM2.5 exposure, station "
    "catchments, or station-radius population; does not validate same-station "
    "joins; and does not promote monitor-grade rows."
)

OUTPUT_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "record_key",
    "source_role",
    "observed_version",
    "selected_vintage",
    "s3_key",
    "object_url",
    "expected_size_bytes",
    "expected_etag",
    "downloaded",
    "downloaded_this_run",
    "cache_path",
    "file_size_bytes",
    "size_matches_expected",
    "sha256",
    "http_status",
    "content_type",
    "last_modified",
    "netcdf_opened",
    "netcdf_format",
    "dimension_count",
    "dimensions",
    "variable_count",
    "variables",
    "coordinate_variables",
    "pm25_variable_candidates",
    "global_attributes",
    "metadata_decision",
    "reader_use",
    "blocking_gap",
    "retrieval_error",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in OUTPUT_FIELDS})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def object_url(s3_key: str) -> str:
    return "https://satpmdata.s3.amazonaws.com/" + quote(s3_key, safe="/.")


def cache_file_for_key(s3_key: str) -> Path:
    return CACHE_DIR / Path(s3_key).name


def download_object(url: str, cache_path: Path, expected_size: int) -> dict[str, Any]:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "downloaded": False,
        "downloaded_this_run": False,
        "http_status": "",
        "content_type": "",
        "last_modified": "",
        "file_size_bytes": 0,
        "sha256": "",
        "retrieval_error": "",
    }
    if cache_path.exists() and (expected_size <= 0 or cache_path.stat().st_size == expected_size):
        result.update(
            {
                "downloaded": True,
                "downloaded_this_run": False,
                "file_size_bytes": cache_path.stat().st_size,
                "sha256": sha256_file(cache_path),
            }
        )
        return result

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/x-netcdf,application/octet-stream,*/*",
        "Connection": "close",
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS, stream=True)
        result["http_status"] = response.status_code
        result["content_type"] = response.headers.get("content-type", "")
        result["last_modified"] = response.headers.get("last-modified", "")
        response.raise_for_status()
        tmp_path = cache_path.with_suffix(cache_path.suffix + ".tmp")
        digest = hashlib.sha256()
        bytes_written = 0
        with tmp_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if not chunk:
                    continue
                handle.write(chunk)
                digest.update(chunk)
                bytes_written += len(chunk)
        tmp_path.replace(cache_path)
        result.update(
            {
                "downloaded": True,
                "downloaded_this_run": True,
                "file_size_bytes": bytes_written,
                "sha256": digest.hexdigest(),
            }
        )
    except Exception as exc:  # noqa: BLE001 - retained in output.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def inspect_netcdf(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "netcdf_opened": False,
        "netcdf_format": "",
        "dimension_count": 0,
        "dimensions": "",
        "variable_count": 0,
        "variables": "",
        "coordinate_variables": "",
        "pm25_variable_candidates": "",
        "global_attributes": "",
        "metadata_error": "",
    }
    try:
        with Dataset(path, "r") as dataset:
            dimensions = [f"{name}:{len(dim)}" for name, dim in dataset.dimensions.items()]
            variables = []
            coordinate_vars = []
            pm25_candidates = []
            for name, variable in dataset.variables.items():
                dims = ",".join(variable.dimensions)
                units = str(getattr(variable, "units", "") or "")
                long_name = str(getattr(variable, "long_name", "") or getattr(variable, "description", "") or "")
                variables.append(f"{name}({dims})[{units}]")
                lower = f"{name} {units} {long_name}".casefold()
                if name.casefold() in {"lat", "latitude", "lon", "longitude", "time"}:
                    coordinate_vars.append(name)
                if "pm25" in lower or "pm2.5" in lower or "fine particulate" in lower:
                    pm25_candidates.append(name)
            attrs = [name for name in dataset.ncattrs()]
            result.update(
                {
                    "netcdf_opened": True,
                    "netcdf_format": dataset.data_model,
                    "dimension_count": len(dimensions),
                    "dimensions": "||".join(dimensions),
                    "variable_count": len(variables),
                    "variables": "||".join(variables),
                    "coordinate_variables": "||".join(coordinate_vars),
                    "pm25_variable_candidates": "||".join(pm25_candidates),
                    "global_attributes": "||".join(attrs),
                }
            )
    except Exception as exc:  # noqa: BLE001 - retained in output.
        result["metadata_error"] = f"{type(exc).__name__}: {exc}"
    return result


def selected_rows(version_decision: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    allowed_decisions = {
        "approved_current_version_first_wave_checksum_candidate",
        "approved_current_version_global_sanity_checksum_candidate",
    }
    for row in version_decision.get("acag_rows", []):
        if row.get("decision") not in allowed_decisions:
            continue
        if not row.get("target_2023_object"):
            continue
        output.append(row)
    return output


def build_row(generated_at: str, source: dict[str, Any]) -> dict[str, Any]:
    s3_key = str(source["target_2023_object"])
    expected_size = int(source.get("target_2023_size_bytes") or 0)
    url = object_url(s3_key)
    cache_path = cache_file_for_key(s3_key)
    download = download_object(url, cache_path, expected_size)
    metadata = inspect_netcdf(cache_path) if download["downloaded"] else {}
    size_matches = bool(download["downloaded"] and expected_size and download["file_size_bytes"] == expected_size)
    metadata_opened = bool(metadata.get("netcdf_opened"))
    pm25_candidates = str(metadata.get("pm25_variable_candidates", ""))
    coordinate_vars = str(metadata.get("coordinate_variables", ""))
    metadata_decision = "metadata_ready_for_method_freeze" if size_matches and metadata_opened else "metadata_not_ready"
    if not pm25_candidates or "lat" not in coordinate_vars.casefold() or "lon" not in coordinate_vars.casefold():
        metadata_decision = "metadata_opened_but_variable_review_required" if metadata_opened else metadata_decision

    row = {field: "" for field in OUTPUT_FIELDS}
    row.update(
        {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "record_key": source["record_key"],
            "source_role": source["source_role"],
            "observed_version": source["observed_version"],
            "selected_vintage": source["selected_vintage"],
            "s3_key": s3_key,
            "object_url": url,
            "expected_size_bytes": expected_size,
            "expected_etag": source.get("target_2023_etag", ""),
            "downloaded": download["downloaded"],
            "downloaded_this_run": download["downloaded_this_run"],
            "cache_path": str(cache_path.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "file_size_bytes": download["file_size_bytes"],
            "size_matches_expected": size_matches,
            "sha256": download["sha256"],
            "http_status": download["http_status"],
            "content_type": download["content_type"],
            "last_modified": download["last_modified"],
            "metadata_decision": metadata_decision,
            "reader_use": "Use this checksum and NetCDF metadata to freeze the next PM2.5 denominator processing step.",
            "blocking_gap": "Population denominator selection, radius rules, station joins, and grade gates remain open.",
            "retrieval_error": download["retrieval_error"] or metadata.get("metadata_error", ""),
            "non_claim": NON_CLAIM,
        }
    )
    row.update(metadata)
    return row


def build_summary(generated_at: str, rows: list[dict[str, Any]], version_decision: dict[str, Any]) -> dict[str, Any]:
    counts = {
        "approved_coarse_candidate_files": len(rows),
        "downloaded_files": sum(1 for row in rows if row["downloaded"]),
        "downloaded_this_run": sum(1 for row in rows if row["downloaded_this_run"]),
        "sha256_checksummed_files": sum(1 for row in rows if row["sha256"]),
        "size_matches_expected_files": sum(1 for row in rows if row["size_matches_expected"]),
        "netcdf_files_opened": sum(1 for row in rows if row["netcdf_opened"]),
        "files_with_pm25_variable_candidates": sum(1 for row in rows if row["pm25_variable_candidates"]),
        "files_with_lat_lon_coordinate_variables": sum(
            1
            for row in rows
            if "lat" in str(row["coordinate_variables"]).casefold()
            and "lon" in str(row["coordinate_variables"]).casefold()
        ),
        "population_denominator_files_selected": 0,
        "population_denominator_files_downloaded": 0,
        "station_radius_pm25_exposure_rows": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }
    gates = [
        {
            "gate": "Approved coarse ACAG files downloaded",
            "status": "available" if counts["downloaded_files"] == len(rows) else "not_ready",
            "rows": counts["downloaded_files"],
            "reader_use": "Only the two selected 2023 V6.GL.03 coarse PM2.5 objects are cached locally.",
        },
        {
            "gate": "SHA-256 checksum ledger",
            "status": "available" if counts["sha256_checksummed_files"] == len(rows) else "not_ready",
            "rows": counts["sha256_checksummed_files"],
            "reader_use": "The raw NetCDF files stay in the ignored cache; committed artifacts retain hashes and source URLs.",
        },
        {
            "gate": "NetCDF variable metadata",
            "status": "available" if counts["netcdf_files_opened"] == len(rows) else "not_ready",
            "rows": counts["netcdf_files_opened"],
            "reader_use": "Dimensions and variables are inspectable before any exposure computation.",
        },
        {
            "gate": "Population denominator selection",
            "status": "not_ready",
            "rows": counts["population_denominator_files_selected"],
            "reader_use": "No GHSL or WorldPop denominator has been selected or downloaded in this pass.",
        },
        {
            "gate": "Station-radius exposure computation",
            "status": "not_ready",
            "rows": counts["station_radius_pm25_exposure_rows"],
            "reader_use": "No PM2.5 exposure or catchment map is computed here.",
        },
        {
            "gate": "Station joins and monitor-grade closure",
            "status": "not_ready",
            "rows": counts["validated_same_station_join_rows"] + counts["complete_monitor_grade_rows"],
            "reader_use": "Station identity and monitor-grade gates remain separate blockers.",
        },
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius ACAG coarse PM2.5 checksum and metadata gate",
        "source_inputs": [
            {
                "path": str(VERSION_DECISION_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
                "role": "station-radius ACAG version-decision summary",
            }
        ],
        "cache_policy": "Raw NetCDF files are stored under air-monitoring/.cache/station-radius-acag-coarse-checksums/ and are not committed; rerun the script to rehydrate them from public S3 object URLs.",
        "coverage_counts": counts,
        "evidence_gate_counts": gates,
        "checksum_rows": [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows],
        "upstream_counts": version_decision.get("coverage_counts", {}),
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    lines = [
        "# Station-radius ACAG coarse checksum gate",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass downloads the two approved 2023 ACAG V6.GL.03 coarse NetCDF objects into the ignored local cache, computes SHA-256 hashes, and records NetCDF dimensions and variables before any exposure or catchment computation.",
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
            "## Checksum rows",
            "",
            "| Record | Size bytes | SHA-256 | Dimensions | PM2.5 variable candidates | Decision |",
            "|---|---:|---|---|---|---|",
        ]
    )
    for row in summary["checksum_rows"]:
        lines.append(
            f"| {row['record_key']} | {row['file_size_bytes']} | `{row['sha256']}` | "
            f"{row['dimensions']} | {row['pm25_variable_candidates']} | {row['metadata_decision']} |"
        )
    lines.extend(["", "## Cache policy", "", summary["cache_policy"], "", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    version_decision = read_json(VERSION_DECISION_JSON)
    rows = [build_row(generated_at, row) for row in selected_rows(version_decision)]
    summary = build_summary(generated_at, rows, version_decision)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["coverage_counts"]
    print(
        "Built ACAG coarse checksum gate: "
        f"{counts['approved_coarse_candidate_files']} approved files; "
        f"{counts['downloaded_files']} downloaded; "
        f"{counts['sha256_checksummed_files']} SHA-256 hashes; "
        f"{counts['netcdf_files_opened']} NetCDF files opened; "
        f"{counts['station_radius_pm25_exposure_rows']} exposure rows."
    )


if __name__ == "__main__":
    main()
