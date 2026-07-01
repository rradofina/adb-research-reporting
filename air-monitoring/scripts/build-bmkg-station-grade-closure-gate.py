#!/usr/bin/env python
"""Build a strict BMKG station-grade closure gate.

This is a no-network derivative artifact. It reads the committed BMKG
near-closure ledger, targeted certificate/status scan, and PPID/PTSP access
route scan, then decides whether any BMKG PM2.5 row can be promoted to
complete monitor-grade or station-radius grade-assumption readiness.
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

NEAR_CLOSURE_CSV = GENERATED_DIR / "air-monitoring-bmkg-near-closure-ledger.csv"
CERTIFICATE_STATUS_CSV = GENERATED_DIR / "air-monitoring-bmkg-certificate-status-targeted-source-scan.csv"
PPID_ACCESS_CSV = GENERATED_DIR / "air-monitoring-bmkg-ppid-access-route-scan.csv"

OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-grade-closure-gate.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-station-grade-closure-gate-summary.json"
OUT_MD = PROGRAM_DIR / "bmkg-station-grade-closure-gate.md"

METHOD = "air_monitoring_bmkg_station_grade_closure_gate_v1"
STATUS = "computed_bmkg_station_grade_closure_gate"
ATTESTATION = "ai-first"
NON_CLAIM = (
    "This gate decides whether committed BMKG public evidence is sufficient for "
    "station-grade promotion. It does not certify station-specific inspection "
    "logs, PM2.5 calibration certificates, calibration status, complete "
    "monitor-grade classification, same-station OpenAQ joins, or station-radius "
    "coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "closure_gate_id",
    "source_station_id",
    "source_station_name",
    "station_method_class",
    "method_classified",
    "detail_page_display_found",
    "station_page_bam_method_text_found",
    "dashboard_status_raw",
    "dashboard_current_status_confirmed",
    "dashboard_delayed",
    "source_level_grade_basis_available",
    "station_unit_or_exact_context_sources",
    "exact_station_audit_calibration_sources",
    "pm25_installation_deployment_sources",
    "targeted_certificate_status_decision",
    "targeted_source_count",
    "targeted_exact_station_calibration_language_sources",
    "ppid_public_pm25_display_route_available",
    "ppid_source_level_calibration_service_route_available",
    "ppid_source_level_certificate_request_context_available",
    "ppid_raw_data_exclusion_context_available",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "explicit_station_grade_evidence_found",
    "current_status_gate",
    "inspection_log_gate",
    "calibration_certificate_gate",
    "calibration_status_gate",
    "explicit_station_grade_gate",
    "complete_monitor_grade_gate",
    "station_radius_grade_assumption_gate",
    "closure_decision",
    "promoted_to_complete_monitor_grade",
    "station_radius_grade_assumption_ready",
    "admissible_public_evidence_needed",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boolish(value: Any) -> bool:
    return str(value or "").strip().casefold() in {"true", "1", "yes", "y"}


def integer(value: Any) -> int:
    try:
        return int(float(str(value or "0").strip() or 0))
    except ValueError:
        return 0


def index_by_station(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["source_station_id"]: row for row in rows if row.get("source_station_id")}


def gate(value: bool) -> str:
    return "pass" if value else "blocked"


def closure_decision(row: dict[str, Any]) -> tuple[str, str, str]:
    if boolish(row["promoted_to_complete_monitor_grade"]):
        return (
            "complete_monitor_grade_ready",
            "All strict station-grade gates passed.",
            "Use this row for monitor-grade assumptions only after the same-station identity gate is also satisfied.",
        )
    if boolish(row["dashboard_delayed"]):
        return (
            "dashboard_delayed_grade_blocked",
            "A public station-owner or regulator record that confirms current operating status for this exact station, plus station-specific inspection, PM2.5 calibration certificate/status, or explicit station-grade evidence.",
            "Keep this row as a delayed-status follow-up; do not use it for grade or radius assumptions.",
        )
    if integer(row["exact_station_audit_calibration_sources"]) > 0 or integer(row["targeted_exact_station_calibration_language_sources"]) > 0:
        return (
            "exact_audit_context_certificate_status_missing",
            "A public target-station inspection log, PM2.5 calibration certificate/status record, or explicit grade record tied to the same exact station name or ID.",
            "Use this as the highest-value BMKG follow-up row because exact audit or calibration-language context exists but closure evidence is still absent.",
        )
    if integer(row["station_unit_or_exact_context_sources"]) > 0:
        return (
            "station_unit_context_certificate_status_missing",
            "A public station-owner or regulator source that turns station-unit context into row-level inspection, PM2.5 calibration certificate/status, or explicit grade evidence.",
            "Use this as a station-unit follow-up row; context exists, but certificate/status closure does not.",
        )
    if integer(row["pm25_installation_deployment_sources"]) > 0:
        return (
            "deployment_context_certificate_status_missing",
            "A public station-owner or regulator source that links the deployment context to station-specific inspection, PM2.5 calibration certificate/status, or explicit grade evidence.",
            "Use this as a deployment-context follow-up row; installation evidence is not a grade record.",
        )
    return (
        "method_display_dashboard_context_certificate_status_missing",
        "A public target-station inspection log, PM2.5 calibration certificate/status record, or explicit station-grade record for this exact BMKG row.",
        "Use this as a general BMKG grade follow-up row; method, display, dashboard, and source-level context are visible but not sufficient.",
    )


def build_rows() -> list[dict[str, Any]]:
    near_rows = read_csv(NEAR_CLOSURE_CSV)
    certificate_rows = index_by_station(read_csv(CERTIFICATE_STATUS_CSV))
    ppid_rows = index_by_station(read_csv(PPID_ACCESS_CSV))
    generated_at = now_iso()
    out: list[dict[str, Any]] = []

    for near in sorted(near_rows, key=lambda row: row.get("source_station_id", "")):
        station_id = near["source_station_id"]
        cert = certificate_rows.get(station_id, {})
        ppid = ppid_rows.get(station_id, {})

        station_specific_inspection_log_found = any(
            boolish(row.get("station_specific_inspection_log_found"))
            for row in [near, cert, ppid]
        )
        station_specific_calibration_certificate_found = any(
            boolish(row.get("station_specific_calibration_certificate_found"))
            for row in [near, cert, ppid]
        )
        calibration_status_available = any(
            boolish(row.get("calibration_status_available"))
            for row in [near, cert, ppid]
        )
        explicit_station_grade_evidence_found = any(
            boolish(row.get("complete_monitor_grade_classification_available"))
            for row in [near, cert, ppid]
        )

        method_classified = boolish(near.get("method_classified"))
        detail_page_display_found = boolish(near.get("detail_page_display_found"))
        station_page_bam_method_text_found = boolish(near.get("station_page_bam_method_text_found"))
        dashboard_current_status_confirmed = boolish(near.get("dashboard_current_status_confirmed"))
        dashboard_delayed = boolish(near.get("dashboard_delayed"))
        source_level_grade_basis_available = boolish(near.get("source_level_grade_basis_available"))
        has_station_grade_closure_source = any(
            [
                station_specific_inspection_log_found,
                station_specific_calibration_certificate_found,
                calibration_status_available,
                explicit_station_grade_evidence_found,
            ]
        )
        promoted = all(
            [
                method_classified,
                detail_page_display_found,
                station_page_bam_method_text_found,
                dashboard_current_status_confirmed,
                source_level_grade_basis_available,
                has_station_grade_closure_source,
            ]
        )

        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": ATTESTATION,
            "status": STATUS,
            "method": METHOD,
            "closure_gate_id": f"IDN-bmkg-station-grade-closure-{station_id}",
            "source_station_id": station_id,
            "source_station_name": near.get("source_station_name", ""),
            "station_method_class": near.get("station_method_class", ""),
            "method_classified": method_classified,
            "detail_page_display_found": detail_page_display_found,
            "station_page_bam_method_text_found": station_page_bam_method_text_found,
            "dashboard_status_raw": near.get("dashboard_status_raw", ""),
            "dashboard_current_status_confirmed": dashboard_current_status_confirmed,
            "dashboard_delayed": dashboard_delayed,
            "source_level_grade_basis_available": source_level_grade_basis_available,
            "station_unit_or_exact_context_sources": integer(near.get("station_unit_or_exact_context_sources")),
            "exact_station_audit_calibration_sources": integer(near.get("exact_station_audit_calibration_sources")),
            "pm25_installation_deployment_sources": integer(near.get("pm25_installation_deployment_sources")),
            "targeted_certificate_status_decision": cert.get("certificate_status_decision", ""),
            "targeted_source_count": integer(cert.get("targeted_source_count")),
            "targeted_exact_station_calibration_language_sources": integer(cert.get("exact_station_calibration_language_sources")),
            "ppid_public_pm25_display_route_available": boolish(ppid.get("public_pm25_display_route_available")),
            "ppid_source_level_calibration_service_route_available": boolish(ppid.get("source_level_calibration_service_route_available")),
            "ppid_source_level_certificate_request_context_available": boolish(ppid.get("source_level_certificate_request_context_available")),
            "ppid_raw_data_exclusion_context_available": boolish(ppid.get("raw_data_exclusion_context_available")),
            "station_specific_inspection_log_found": station_specific_inspection_log_found,
            "station_specific_calibration_certificate_found": station_specific_calibration_certificate_found,
            "calibration_status_available": calibration_status_available,
            "explicit_station_grade_evidence_found": explicit_station_grade_evidence_found,
            "current_status_gate": gate(dashboard_current_status_confirmed),
            "inspection_log_gate": gate(station_specific_inspection_log_found),
            "calibration_certificate_gate": gate(station_specific_calibration_certificate_found),
            "calibration_status_gate": gate(calibration_status_available),
            "explicit_station_grade_gate": gate(explicit_station_grade_evidence_found),
            "complete_monitor_grade_gate": gate(promoted),
            "station_radius_grade_assumption_gate": "blocked",
            "promoted_to_complete_monitor_grade": promoted,
            "station_radius_grade_assumption_ready": False,
            "non_claim": NON_CLAIM,
        }
        decision, evidence_needed, reader_use = closure_decision(row)
        row["closure_decision"] = decision
        row["admissible_public_evidence_needed"] = evidence_needed
        row["reader_use"] = reader_use
        out.append(row)
    return out


def evidence_gate_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    definitions = [
        ("Method classified as BAM", "method_classified", "pass", "BMKG method evidence supports the method class."),
        ("Station detail display", "detail_page_display_found", "pass", "Public exact station pages expose PM2.5 display rows."),
        ("Station-page BAM method text", "station_page_bam_method_text_found", "pass", "Exact station pages include BAM method text."),
        ("Current dashboard status", "dashboard_current_status_confirmed", "partly_pass", "Most rows have current ONLINE dashboard status; delayed rows stay blocked."),
        ("Source-level grade basis", "source_level_grade_basis_available", "pass", "Source-level standards, SOP, inspection, calibration, and service context exists."),
        ("PPID public PM2.5 display route", "ppid_public_pm25_display_route_available", "pass", "PPID/access-route evidence maps public display back to target rows."),
        ("Station-specific inspection log", "station_specific_inspection_log_found", "blocked", "No committed public source exposes a target-station inspection log."),
        ("Station-specific PM2.5 calibration certificate", "station_specific_calibration_certificate_found", "blocked", "No committed public source exposes a target-station PM2.5 calibration certificate."),
        ("Calibration status record", "calibration_status_available", "blocked", "No committed public source exposes row-level calibration status."),
        ("Explicit station-grade evidence", "explicit_station_grade_evidence_found", "blocked", "No committed public source explicitly promotes a target row to complete station grade."),
        ("Complete monitor-grade gate", "promoted_to_complete_monitor_grade", "blocked", "No target row satisfies the strict closure rule."),
        ("Station-radius grade assumption gate", "station_radius_grade_assumption_ready", "blocked", "No BMKG row can support station-radius grade assumptions from this evidence."),
    ]
    output: list[dict[str, Any]] = []
    for label, field, status, note in definitions:
        output.append(
            {
                "gate": label,
                "status": status,
                "rows": sum(1 for row in rows if boolish(row.get(field))),
                "reader_use": note,
            }
        )
    return output


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    decision_counter = Counter(row["closure_decision"] for row in rows)
    counts = {
        "bmkg_target_rows": len(rows),
        "method_classified_rows": sum(1 for row in rows if boolish(row["method_classified"])),
        "detail_page_display_rows": sum(1 for row in rows if boolish(row["detail_page_display_found"])),
        "station_page_bam_method_text_rows": sum(1 for row in rows if boolish(row["station_page_bam_method_text_found"])),
        "dashboard_current_online_rows": sum(1 for row in rows if boolish(row["dashboard_current_status_confirmed"])),
        "dashboard_delayed_rows": sum(1 for row in rows if boolish(row["dashboard_delayed"])),
        "source_level_grade_basis_rows": sum(1 for row in rows if boolish(row["source_level_grade_basis_available"])),
        "ppid_public_pm25_display_route_rows": sum(1 for row in rows if boolish(row["ppid_public_pm25_display_route_available"])),
        "ppid_source_level_calibration_service_route_rows": sum(1 for row in rows if boolish(row["ppid_source_level_calibration_service_route_available"])),
        "ppid_source_level_certificate_request_context_rows": sum(1 for row in rows if boolish(row["ppid_source_level_certificate_request_context_available"])),
        "station_specific_inspection_log_rows": sum(1 for row in rows if boolish(row["station_specific_inspection_log_found"])),
        "station_specific_calibration_certificate_rows": sum(1 for row in rows if boolish(row["station_specific_calibration_certificate_found"])),
        "calibration_status_rows": sum(1 for row in rows if boolish(row["calibration_status_available"])),
        "explicit_station_grade_evidence_rows": sum(1 for row in rows if boolish(row["explicit_station_grade_evidence_found"])),
        "complete_monitor_grade_rows": sum(1 for row in rows if boolish(row["promoted_to_complete_monitor_grade"])),
        "station_radius_grade_assumption_ready_rows": sum(1 for row in rows if boolish(row["station_radius_grade_assumption_ready"])),
    }
    return {
        "generated_at": rows[0]["generated_at"] if rows else now_iso(),
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG strict station-grade closure gate",
        "source_scope": (
            "No-network synthesis of committed BMKG near-closure, targeted "
            "certificate/status, and PPID/PTSP access-route evidence."
        ),
        "source_inputs": [
            {"path": str(NEAR_CLOSURE_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "BMKG near-closure row ledger"},
            {"path": str(CERTIFICATE_STATUS_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "targeted certificate/status row scan"},
            {"path": str(PPID_ACCESS_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": "PPID/PTSP access-route row scan"},
        ],
        "closure_rule": (
            "A BMKG row passes only when method, exact station display, station-page "
            "BAM text, current dashboard status, source-level grade basis, and at "
            "least one station-specific inspection, PM2.5 calibration "
            "certificate/status, or explicit station-grade record are present."
        ),
        "counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(decision_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": evidence_gate_counts(rows),
        "display_rows": rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            "markdown": str(OUT_MD.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        },
        "non_claim": NON_CLAIM,
    }


def write_markdown(summary: dict[str, Any]) -> None:
    rows = summary["display_rows"]
    top_rows = sorted(
        rows,
        key=lambda row: (
            -integer(row["exact_station_audit_calibration_sources"]),
            -integer(row["station_unit_or_exact_context_sources"]),
            -integer(row["pm25_installation_deployment_sources"]),
            row["source_station_name"],
        ),
    )[:12]
    lines = [
        "# BMKG station-grade closure gate",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This no-network gate turns the BMKG near-closure, targeted certificate/status, and PPID/PTSP access-route artifacts into a strict station-grade decision table. It asks whether any of the 22 BMKG PM2.5 rows can be promoted from public display and method context to complete monitor-grade evidence.",
        "",
        "The answer remains no. Current display, source-level method/standard context, PPID display routes, and certificate-request context are visible, but no committed public source gives a target-station inspection log, PM2.5 calibration certificate/status record, or explicit station-grade record.",
        "",
        "## Closure rule",
        "",
        summary["closure_rule"],
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in summary["counts"].items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(["", "## Closure decisions", "", "| Decision | Rows |", "|---|---:|"])
    for row in summary["decision_counts"]:
        lines.append(f"| {row['decision']} | {row['rows']} |")
    lines.extend(["", "## Evidence gates", "", "| Gate | Rows | Status |", "|---|---:|---|"])
    for row in summary["evidence_gate_counts"]:
        lines.append(f"| {row['gate']} | {row['rows']} | {row['status']} |")
    lines.extend(["", "## Highest-value follow-up rows", "", "| Station | Dashboard | Decision | Needed public evidence |", "|---|---|---|---|"])
    for row in top_rows:
        lines.append(
            "| "
            f"{row['source_station_name']} (`{row['source_station_id']}`) | "
            f"{row['dashboard_status_raw']} | "
            f"{row['closure_decision']} | "
            f"{row['admissible_public_evidence_needed']} |"
        )
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    summary = build_summary(rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)
    counts = summary["counts"]
    print(
        "Built BMKG station-grade closure gate: "
        f"{counts['bmkg_target_rows']} target rows; "
        f"{counts['dashboard_current_online_rows']} current ONLINE rows; "
        f"{counts['station_specific_inspection_log_rows']} inspection-log rows; "
        f"{counts['station_specific_calibration_certificate_rows']} certificate rows; "
        f"{counts['complete_monitor_grade_rows']} complete-grade rows."
    )


if __name__ == "__main__":
    main()
