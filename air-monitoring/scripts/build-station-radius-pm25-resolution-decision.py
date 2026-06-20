#!/usr/bin/env python
"""Freeze the PM2.5 grid-resolution decision before a station-radius dry run.

This derivative gate reads already-committed ACAG checksum/version artifacts
and freezes the PM2.5 resolution lane. It does not compute exposure rows.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "air-monitoring"
GENERATED = PROGRAM / "generated"

ACAG_VERSION_SUMMARY = GENERATED / "air-monitoring-station-radius-acag-version-decision-summary.json"
ACAG_CHECKSUM_SUMMARY = GENERATED / "air-monitoring-station-radius-acag-coarse-checksums-summary.json"
METHOD_PREFREEZE_SUMMARY = GENERATED / "air-monitoring-station-radius-method-prefreeze-summary.json"
RADIUS_RULE_SUMMARY = GENERATED / "air-monitoring-station-radius-radius-rule-source-scan-summary.json"

OUT_CSV = GENERATED / "air-monitoring-station-radius-pm25-resolution-decision.csv"
OUT_JSON = GENERATED / "air-monitoring-station-radius-pm25-resolution-decision-summary.json"
OUT_MD = PROGRAM / "station-radius-pm25-resolution-decision.md"

METHOD = "air_monitoring_station_radius_pm25_resolution_decision_v1"
STATUS = "computed_station_radius_pm25_resolution_decision"
ATTESTATION = "ai-first"
GOAL_LEVEL = "L3 station-radius PM2.5 resolution decision gate"
NON_CLAIM = (
    "This PM2.5 resolution decision freezes the coarse annual ACAG grid lane "
    "for a future denominator dry run. It does not compute PM2.5 exposure, "
    "station buffers, catchment population, monitor coverage, validated "
    "same-station joins, or complete monitor-grade classification."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "decision_id",
    "decision_role",
    "decision_status",
    "selected",
    "acag_record_key",
    "source_role",
    "observed_version",
    "selected_vintage",
    "selected_resolution",
    "grid_family",
    "object_url",
    "cache_path",
    "sha256",
    "file_size_bytes",
    "dimensions",
    "variables",
    "pm25_variable",
    "radius_rule_context",
    "reader_use",
    "blocking_gap",
    "claim_guardrail",
    "non_claim",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_resolution_from_key(s3_key: str) -> str:
    match = re.search(r"(\d+)p(\d+)", s3_key)
    if not match:
        return "unknown"
    return f"{match.group(1)}.{match.group(2)} degree"


def row_from_checksum(generated_at: str, row: dict[str, Any], role: str, selected: bool) -> dict[str, Any]:
    resolution = parse_resolution_from_key(str(row.get("s3_key", "")))
    grid_family = "global_coarse" if ".GL." in str(row.get("s3_key", "")) else "asia_coarse"
    return {
        "generated_at": generated_at,
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "decision_id": f"{row['record_key']}_pm25_resolution",
        "decision_role": role,
        "decision_status": "frozen_for_dry_run" if selected else "frozen_consistency_lane",
        "selected": selected,
        "acag_record_key": row["record_key"],
        "source_role": row["source_role"],
        "observed_version": row["observed_version"],
        "selected_vintage": row["selected_vintage"],
        "selected_resolution": resolution,
        "grid_family": grid_family,
        "object_url": row["object_url"],
        "cache_path": row["cache_path"],
        "sha256": row["sha256"],
        "file_size_bytes": row["file_size_bytes"],
        "dimensions": row["dimensions"],
        "variables": row["variables"],
        "pm25_variable": row["pm25_variable_candidates"],
        "radius_rule_context": "4 km primary diagnostic; 0.5 km and 50 km sensitivity bands",
        "reader_use": (
            "Use the check-summed 2023 V6.GL.03 global coarse PM2.5 grid as the "
            "first dry-run pollutant surface."
            if selected
            else "Retain the check-summed 2023 V6.GL.03 Asia coarse grid as a consistency lane."
        ),
        "blocking_gap": (
            "Population/PM2.5 denominator join dry run, station identity joins, "
            "complete monitor-grade rows, and exposure/catchment outputs remain open."
        ),
        "claim_guardrail": (
            "Coarse annual gridded PM2.5 is a contextual pollutant surface for a "
            "dry-run denominator, not a station measurement or neighborhood-scale "
            "concentration claim."
        ),
        "non_claim": NON_CLAIM,
    }


def write_md(path: Path, summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    decision = summary["pm25_resolution_decision"]
    lines = [
        "# Air Monitoring Station-Radius PM2.5 Resolution Decision",
        "",
        "attestation_chain: ai-first",
        "",
        "## Status",
        "",
        (
            "This gate freezes the PM2.5 grid-resolution lane before any station-radius "
            "denominator dry run. The selected first dry-run surface is "
            f"{decision['selected_version']} {decision['selected_vintage']} "
            f"{decision['selected_resolution']} PM2.5."
        ),
        "",
        "## Evidence Counts",
        "",
        "| Check | Count |",
        "|---|---:|",
        f"| Check-summed coarse PM2.5 files | {counts['checksummed_coarse_pm25_files']} |",
        f"| Files with PM25(lat,lon) metadata | {counts['files_with_pm25_lat_lon']} |",
        f"| Selected primary dry-run PM2.5 surface | {counts['selected_primary_pm25_surfaces']} |",
        f"| Consistency-lane PM2.5 surfaces | {counts['consistency_lane_pm25_surfaces']} |",
        f"| PM2.5 exposure rows | {counts['station_radius_pm25_exposure_rows']} |",
        "",
        "## Frozen Resolution Decision",
        "",
        "| Element | Value |",
        "|---|---|",
        f"| Selected version | {decision['selected_version']} |",
        f"| Selected vintage | {decision['selected_vintage']} |",
        f"| Selected resolution | {decision['selected_resolution']} |",
        f"| Primary dry-run file | {decision['primary_dry_run_record_key']} |",
        f"| Consistency lane | {decision['consistency_lane_record_key']} |",
        f"| Deferred lanes | {decision['deferred_lanes']} |",
        f"| Claim guardrail | {decision['claim_guardrail']} |",
        "",
        "## Decision Rows",
        "",
        "| Decision | Role | Status | Grid | File | Reader use |",
        "|---|---|---|---|---|---|",
    ]
    for row in summary["decision_rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["decision_id"],
                    row["decision_role"],
                    row["decision_status"],
                    row["grid_family"],
                    row["acag_record_key"],
                    row["reader_use"],
                ]
            )
            + " |"
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
    for row in summary["evidence_gate_counts"]:
        lines.append(f"| {row['gate']} | {row['status']} | {row['rows']} | {row['reader_use']} |")
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
            "python air-monitoring\\scripts\\build-station-radius-pm25-resolution-decision.py",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def build_outputs() -> dict[str, Any]:
    generated_at = now_utc()
    version_summary = read_json(ACAG_VERSION_SUMMARY)
    checksum_summary = read_json(ACAG_CHECKSUM_SUMMARY)
    method_summary = read_json(METHOD_PREFREEZE_SUMMARY)
    radius_summary = read_json(RADIUS_RULE_SUMMARY)

    checksum_rows = checksum_summary["checksum_rows"]
    global_rows = [row for row in checksum_rows if row["record_key"] == "v6gl03_gl_coarse_annual"]
    asia_rows = [row for row in checksum_rows if row["record_key"] == "v6gl03_as_coarse_annual"]
    if len(global_rows) != 1 or len(asia_rows) != 1:
        raise RuntimeError("Expected one global coarse row and one Asia coarse row from ACAG checksum summary")

    decision_rows = [
        row_from_checksum(generated_at, global_rows[0], "primary_dry_run_pm25_surface", True),
        row_from_checksum(generated_at, asia_rows[0], "regional_consistency_pm25_surface", False),
    ]
    counts = {
        "checksummed_coarse_pm25_files": checksum_summary["coverage_counts"]["sha256_checksummed_files"],
        "files_with_pm25_lat_lon": checksum_summary["coverage_counts"]["files_with_lat_lon_coordinate_variables"],
        "selected_primary_pm25_surfaces": 1,
        "consistency_lane_pm25_surfaces": 1,
        "selected_vintage": version_summary["coverage_counts"]["selected_vintage"],
        "visible_latest_v6gl03_year": version_summary["coverage_counts"]["visible_latest_v6gl03_year"],
        "fine_resolution_second_wave_or_deferred_objects": version_summary["coverage_counts"]["fine_resolution_second_wave_or_deferred_objects"],
        "radius_rule_frozen": radius_summary["coverage_counts"]["radius_rule_frozen"],
        "primary_radius_km": radius_summary["coverage_counts"]["primary_radius_km"],
        "lower_sensitivity_radius_km": radius_summary["coverage_counts"]["lower_sensitivity_radius_km"],
        "upper_sensitivity_radius_km": radius_summary["coverage_counts"]["upper_sensitivity_radius_km"],
        "coordinate_rows_used": method_summary["coverage_counts"]["coordinate_rows_used"],
        "population_tile_files_in_custody": method_summary["coverage_counts"]["population_tile_files_in_custody"],
        "station_radius_population_rows": 0,
        "station_radius_pm25_exposure_rows": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }
    decision = {
        "status": "pm25_resolution_frozen_not_joined",
        "selected_version": "V6.GL.03",
        "selected_vintage": 2023,
        "selected_resolution": "0.10 degree coarse annual",
        "primary_dry_run_record_key": "v6gl03_gl_coarse_annual",
        "consistency_lane_record_key": "v6gl03_as_coarse_annual",
        "deferred_lanes": "fine-resolution ACAG objects and visible 2024 V6.GL.03 annual objects",
        "claim_guardrail": (
            "Use the grid only as a coarse annual contextual PM2.5 denominator for "
            "a dry run. Do not report station catchment exposure, monitor coverage, "
            "or neighborhood-scale measured concentration from this gate."
        ),
    }
    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": GOAL_LEVEL,
        "source_inputs": {
            "acag_version_summary": str(ACAG_VERSION_SUMMARY.relative_to(PROGRAM)).replace("\\", "/"),
            "acag_checksum_summary": str(ACAG_CHECKSUM_SUMMARY.relative_to(PROGRAM)).replace("\\", "/"),
            "method_prefreeze_summary": str(METHOD_PREFREEZE_SUMMARY.relative_to(PROGRAM)).replace("\\", "/"),
            "radius_rule_summary": str(RADIUS_RULE_SUMMARY.relative_to(PROGRAM)).replace("\\", "/"),
        },
        "coverage_counts": counts,
        "pm25_resolution_decision": decision,
        "evidence_gate_counts": [
            {
                "gate": "ACAG current-version decision",
                "status": "available",
                "rows": version_summary["coverage_counts"]["evidence_rows"],
                "reader_use": "Confirms V6.GL.03 2023 coarse PM2.5 objects are the pinned first-wave lane.",
            },
            {
                "gate": "ACAG coarse checksum custody",
                "status": "available",
                "rows": counts["checksummed_coarse_pm25_files"],
                "reader_use": "Confirms the two coarse NetCDF files are downloaded, check-summed, and metadata-opened.",
            },
            {
                "gate": "Radius rule",
                "status": "available",
                "rows": radius_summary["coverage_counts"]["rule_selected_evidence_rows"],
                "reader_use": "Confirms the 4 km primary and 0.5/50 km sensitivity bands are source-frozen.",
            },
            {
                "gate": "PM2.5 denominator join",
                "status": "not_computed",
                "rows": 0,
                "reader_use": "No station-radius PM2.5 exposure rows are computed in this decision gate.",
            },
        ],
        "decision_rows": decision_rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }
    write_csv(OUT_CSV, decision_rows)
    write_json(OUT_JSON, summary)
    write_md(OUT_MD, summary)
    return summary


def main() -> int:
    summary = build_outputs()
    counts = summary["coverage_counts"]
    decision = summary["pm25_resolution_decision"]
    print(
        "Built station-radius PM2.5 resolution decision: "
        f"{decision['selected_version']} {decision['selected_vintage']} "
        f"{decision['selected_resolution']}; "
        f"{counts['checksummed_coarse_pm25_files']} coarse files in custody; "
        f"{counts['station_radius_pm25_exposure_rows']} PM2.5 exposure rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
