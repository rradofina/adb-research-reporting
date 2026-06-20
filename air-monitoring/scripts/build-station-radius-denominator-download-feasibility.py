"""Build a no-download feasibility gate for station-radius denominators.

This pass reads the file-manifest prefreeze and classifies each visible file,
object, or unresolved route into a download decision lane. It does not download
or checksum denominator files; the output is a reviewer-readable decision
matrix before any raster or grid enters the evidence package.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

MANIFEST_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-file-manifest-prefreeze-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-denominator-download-feasibility.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-download-feasibility-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-denominator-download-feasibility.md"

METHOD = "air_monitoring_station_radius_denominator_download_feasibility_v1"
STATUS = "computed_station_radius_denominator_download_feasibility"
NON_CLAIM = (
    "This feasibility gate classifies exact denominator file/object records by "
    "download risk, version drift, source role, and next evidence action. It "
    "does not download or checksum GHSL, WorldPop, or ACAG files; does not "
    "select a final population denominator; does not compute station-radius "
    "population or PM2.5 exposure; does not validate same-station joins; and "
    "does not promote monitor-grade rows."
)

OUTPUT_FIELDS = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "manifest_key",
    "source_key",
    "source_name",
    "source_family",
    "source_role",
    "denominator_type",
    "candidate_role",
    "source_plan_version",
    "resolved_version",
    "vintage",
    "resolution",
    "geography_scope",
    "file_format",
    "route_type",
    "manifest_status",
    "exact_file_url",
    "s3_key",
    "content_length_bytes",
    "size_mb",
    "size_class",
    "exact_route_visible",
    "source_plan_version_drift",
    "unresolved_shared_folder",
    "download_feasibility",
    "selection_role",
    "first_wave_candidate",
    "denominator_gate_closer",
    "reader_use",
    "proposed_action",
    "blocking_gap",
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


def as_int(value: Any) -> int:
    try:
        if value in (None, ""):
            return 0
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def size_class(size_bytes: int) -> str:
    if size_bytes <= 0:
        return "unknown_size"
    if size_bytes <= 1_000_000:
        return "tiny_under_1mb"
    if size_bytes <= 10_000_000:
        return "small_under_10mb"
    if size_bytes <= 100_000_000:
        return "moderate_under_100mb"
    if size_bytes <= 500_000_000:
        return "large_under_500mb"
    if size_bytes <= 1_000_000_000:
        return "very_large_under_1gb"
    return "giant_over_1gb"


def classify(record: dict[str, Any]) -> dict[str, Any]:
    manifest_key = str(record.get("manifest_key", ""))
    source_family = str(record.get("source_family", ""))
    denominator_type = str(record.get("denominator_type", ""))
    candidate_role = str(record.get("candidate_role", ""))
    route_type = str(record.get("route_type", ""))
    manifest_status = str(record.get("manifest_status", ""))
    size_bytes = as_int(record.get("content_length_bytes"))
    version_drift = "version_drift" in candidate_role or "V6.GL.03" in str(record.get("resolved_version", ""))
    unresolved = "shared_folder" in route_type or "shared_folder" in manifest_status
    exact_visible = bool(record.get("exact_file_url") or record.get("s3_key")) and not unresolved

    decision = {
        "download_feasibility": "review_required",
        "selection_role": "not_selected",
        "first_wave_candidate": False,
        "denominator_gate_closer": False,
        "reader_use": "Retain as a manifest record until a narrower method decision selects or rejects it.",
        "proposed_action": "Review before any download.",
        "blocking_gap": "No download or checksum has been performed.",
    }

    if unresolved:
        decision.update(
            {
                "download_feasibility": "blocked_unresolved_shared_folder",
                "selection_role": "blocked_manifest_gap",
                "reader_use": "The source route exists, but the public evidence still lacks exact file names, sizes, and object metadata.",
                "proposed_action": "Resolve a public file manifest or documented object name before using this route.",
                "blocking_gap": "Shared-folder routes are not reproducible file manifests.",
            }
        )
    elif denominator_type == "context_metadata":
        decision.update(
            {
                "download_feasibility": "metadata_download_feasible_not_denominator",
                "selection_role": "metadata_coverage_check_candidate",
                "first_wave_candidate": True,
                "reader_use": "This small metadata CSV can check WorldPop source coverage, but it is not a gridded population denominator.",
                "proposed_action": "Download or cache only as metadata, then record a SHA-256 if it becomes an input.",
                "blocking_gap": "Metadata does not close the population-raster denominator gate.",
            }
        )
    elif source_family == "GHSL" and "tile_route_example" in candidate_role:
        decision.update(
            {
                "download_feasibility": "route_test_candidate_not_selected_denominator",
                "selection_role": "safe_population_route_test_only",
                "first_wave_candidate": True,
                "reader_use": "This small GHSL tile proves a tractable route exists, but it is only a global tile example and is not selected for any DMC catchment.",
                "proposed_action": "Use only as a route/checksum test, then build a DMC-intersecting tile list before denominator use.",
                "blocking_gap": "A route-test tile is not a selected population denominator.",
            }
        )
    elif source_family == "GHSL" and denominator_type == "population":
        decision.update(
            {
                "download_feasibility": "defer_large_population_archive",
                "selection_role": "defer_until_dmc_tile_selection",
                "reader_use": "The exact GHSL archive is visible, but the global ZIP is too large for a first checksum loop when a tile route exists.",
                "proposed_action": "Derive a DMC-intersecting tile list or a narrower source subset before download.",
                "blocking_gap": "The package still lacks a selected gridded population denominator and radius method.",
            }
        )
    elif source_family == "WorldPop" and denominator_type == "population":
        decision.update(
            {
                "download_feasibility": "defer_large_population_archive",
                "selection_role": "sensitivity_archive_deferred",
                "reader_use": "The WorldPop archive is exact and public, but it is a multi-gigabyte sensitivity source rather than the first denominator pull.",
                "proposed_action": "Use the metadata table first, then look for a country or tiled extraction route before the full archive.",
                "blocking_gap": "Sensitivity population archive is not selected and not checksummed.",
            }
        )
    elif source_family == "ACAG" and "coarse" in candidate_role and size_bytes <= 10_000_000:
        role = "primary_pm25_first_wave_candidate" if "asia" in candidate_role else "global_pm25_sanity_candidate"
        decision.update(
            {
                "download_feasibility": "conditional_pm25_checksum_candidate_after_version_decision",
                "selection_role": role,
                "first_wave_candidate": True,
                "reader_use": "The ACAG coarse NetCDF is small enough for a checksum test, but it is V6.GL.03 while the source-plan route named V6.GL.02.04/V5.",
                "proposed_action": "Resolve whether V6.GL.03 is an acceptable current substitute or only a supplement; if accepted, download and record SHA-256 before inspecting variables.",
                "blocking_gap": "ACAG version drift must be recorded before this object enters the denominator workflow.",
            }
        )
    elif source_family == "ACAG" and "asia_fine" in candidate_role:
        decision.update(
            {
                "download_feasibility": "second_wave_pm25_candidate_after_coarse_validation",
                "selection_role": "fine_pm25_second_wave_candidate",
                "reader_use": "The Asia fine-resolution ACAG object is feasible after the coarse object validates the route and method.",
                "proposed_action": "Defer until the ACAG version decision and coarse-file checksum/variable inspection are complete.",
                "blocking_gap": "Fine-resolution PM2.5 should not be the first file in a version-drifted workflow.",
            }
        )
    elif source_family == "ACAG" and "global_fine" in candidate_role:
        decision.update(
            {
                "download_feasibility": "defer_large_pm25_object_until_method_selected",
                "selection_role": "global_fine_pm25_deferred",
                "reader_use": "The global fine ACAG object is exact, but it is much larger than the regional coarse candidates and still carries version drift.",
                "proposed_action": "Defer until a regional pilot proves the version, variables, and catchment workflow.",
                "blocking_gap": "A large current-version object is not a first-wave denominator input.",
            }
        )

    if decision["denominator_gate_closer"]:
        decision["blocking_gap"] = "This row would close only after download, checksum, and method validation."

    return {
        "content_length_bytes": size_bytes,
        "size_mb": round(size_bytes / 1_000_000, 3) if size_bytes else 0,
        "size_class": size_class(size_bytes),
        "exact_route_visible": exact_visible,
        "source_plan_version_drift": version_drift,
        "unresolved_shared_folder": unresolved,
        **decision,
    }


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def build_rows(generated_at: str, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in manifest.get("manifest_records", []):
        classification = classify(record)
        row = {field: "" for field in OUTPUT_FIELDS}
        for field in OUTPUT_FIELDS:
            if field in record:
                row[field] = record[field]
        row.update(classification)
        row.update(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "non_claim": NON_CLAIM,
            }
        )
        rows.append(row)
    return rows


def build_summary(generated_at: str, rows: list[dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    decisions = Counter(row["download_feasibility"] for row in rows)
    roles = Counter(row["selection_role"] for row in rows)
    size_classes = Counter(row["size_class"] for row in rows)
    first_wave = [row for row in rows if row["first_wave_candidate"]]
    conditional_pm25 = [
        row
        for row in rows
        if row["download_feasibility"] == "conditional_pm25_checksum_candidate_after_version_decision"
    ]
    metadata_or_route = [
        row
        for row in rows
        if row["download_feasibility"]
        in {"metadata_download_feasible_not_denominator", "route_test_candidate_not_selected_denominator"}
    ]
    large_population = [row for row in rows if row["download_feasibility"] == "defer_large_population_archive"]
    deferred_pm25 = [
        row
        for row in rows
        if row["download_feasibility"]
        in {"second_wave_pm25_candidate_after_coarse_validation", "defer_large_pm25_object_until_method_selected"}
    ]
    unresolved = [row for row in rows if row["unresolved_shared_folder"]]
    counts = {
        "manifest_records_reviewed": len(rows),
        "exact_file_or_object_records_visible": sum(1 for row in rows if row["exact_route_visible"]),
        "safe_under_10mb_records": sum(1 for row in rows if 0 < row["content_length_bytes"] <= 10_000_000),
        "first_wave_download_candidates": len(first_wave),
        "conditional_pm25_checksum_candidates": len(conditional_pm25),
        "metadata_or_route_test_candidates": len(metadata_or_route),
        "population_denominator_selected_for_download": 0,
        "large_population_archives_deferred": len(large_population),
        "moderate_or_large_pm25_objects_deferred": len(deferred_pm25),
        "acag_version_decision_required_records": sum(1 for row in rows if row["source_plan_version_drift"]),
        "unresolved_shared_folder_routes": len(unresolved),
        "denominator_files_downloaded": 0,
        "denominator_files_sha256_checksummed": 0,
        "validated_same_station_join_rows": 0,
        "complete_monitor_grade_rows": 0,
        "station_radius_ready_economies": 0,
    }
    gates = [
        gate(
            "available_prefreeze" if first_wave else "not_ready",
            "First-wave checksum candidates identified",
            len(first_wave),
            "Small objects or metadata/route-test files are identified, but no file is downloaded in this pass.",
        ),
        gate(
            "not_ready",
            "Population denominator selected for catchment use",
            counts["population_denominator_selected_for_download"],
            "The only small GHSL item is a route-test tile; global GHSL and WorldPop archives are deferred until a DMC/tile subset is selected.",
        ),
        gate(
            "caution",
            "ACAG V6.GL.03 version decision",
            counts["acag_version_decision_required_records"],
            "Current AWS objects are exact and small enough in coarse form, but they cannot silently replace V6.GL.02.04/V5 source-plan routes.",
        ),
        gate(
            "not_ready",
            "Large archive download deferral",
            counts["large_population_archives_deferred"] + counts["moderate_or_large_pm25_objects_deferred"],
            "Large population archives and fine PM2.5 objects are visible but not first-wave downloads.",
        ),
        gate(
            "not_ready",
            "Downloaded files and SHA-256 checksums",
            counts["denominator_files_sha256_checksummed"],
            "The feasibility gate only classifies records; checksum evidence remains zero.",
        ),
        gate(
            "not_ready",
            "Station-radius analysis",
            counts["station_radius_ready_economies"],
            "Blocked until selected files are downloaded, checksummed, inspected, joined, grade-gated, and linked to frozen radius rules.",
        ),
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius denominator download feasibility gate",
        "source_inputs": [
            {
                "path": str(MANIFEST_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
                "role": "station-radius denominator file-manifest prefreeze summary",
            }
        ],
        "coverage_counts": counts,
        "download_feasibility_counts": [
            {"decision": key, "records": value}
            for key, value in sorted(decisions.items(), key=lambda item: (-item[1], item[0]))
        ],
        "selection_role_counts": [
            {"role": key, "records": value}
            for key, value in sorted(roles.items(), key=lambda item: (-item[1], item[0]))
        ],
        "size_class_counts": [
            {"size_class": key, "records": value}
            for key, value in sorted(size_classes.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": gates,
        "feasibility_records": [{field: row.get(field, "") for field in OUTPUT_FIELDS} for row in rows],
        "manifest_prefreeze_counts": manifest.get("coverage_counts", {}),
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
        "# Station-radius denominator download-feasibility gate",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This pass turns the prefreeze manifest into a download decision matrix. It names the small first-wave candidates, separates route tests from denominator inputs, defers multi-gigabyte population archives, and keeps ACAG version drift visible before any checksum or map.",
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Download feasibility", "", "| Decision | Records |", "|---|---:|"])
    for row in summary["download_feasibility_counts"]:
        lines.append(f"| {row['decision']} | {row['records']} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for gate_row in summary["evidence_gate_counts"]:
        lines.append(f"| {gate_row['gate']} | {gate_row['rows']} | {gate_row['status']} |")
    lines.extend(
        [
            "",
            "## Decision records",
            "",
            "| Manifest key | Size MB | Decision | Selection role | First wave | Proposed action |",
            "|---|---:|---|---|---|---|",
        ]
    )
    for row in summary["feasibility_records"]:
        first_wave = "yes" if row["first_wave_candidate"] else "no"
        lines.append(
            f"| {row['manifest_key']} | {row['size_mb']} | {row['download_feasibility']} | "
            f"{row['selection_role']} | {first_wave} | {row['proposed_action']} |"
        )
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    manifest = read_json(MANIFEST_JSON)
    rows = build_rows(generated_at, manifest)
    summary = build_summary(generated_at, rows, manifest)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["coverage_counts"]
    print(
        "Built station-radius denominator download-feasibility gate: "
        f"{counts['manifest_records_reviewed']} manifest rows reviewed; "
        f"{counts['first_wave_download_candidates']} first-wave candidates; "
        f"{counts['conditional_pm25_checksum_candidates']} conditional PM2.5 checksum candidates; "
        f"{counts['population_denominator_selected_for_download']} selected population denominators; "
        f"{counts['denominator_files_downloaded']} files downloaded."
    )


if __name__ == "__main__":
    main()
