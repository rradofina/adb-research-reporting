"""Build a BMKG near-closure ledger from existing evidence walls.

This synthesis pass reads the committed BMKG method, station-page, dashboard,
grade-basis, public-context, and installation/audit artifacts. It does not
fetch new sources. Its purpose is to show which rows are close to
monitor-grade closure and which exact evidence gates still block them.
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

METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
STATION_STATUS_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-specific-status-audit.csv"
DASHBOARD_STATUS_CSV = GENERATED_DIR / "air-monitoring-bmkg-dashboard-status-source-scan.csv"
GRADE_BASIS_CSV = GENERATED_DIR / "air-monitoring-bmkg-grade-basis-source-scan.csv"
STATION_CONTEXT_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-public-context-source-scan.csv"
INSTALL_AUDIT_CSV = GENERATED_DIR / "air-monitoring-bmkg-installation-audit-source-scan.csv"

OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-near-closure-ledger.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-near-closure-ledger-summary.json"
OUT_MD = PROGRAM_DIR / "bmkg-near-closure-ledger.md"

METHOD = "air_monitoring_bmkg_near_closure_ledger_v1"
STATUS = "computed_bmkg_near_closure_ledger"
NON_CLAIM = (
    "This ledger synthesizes existing BMKG public evidence gates. It does not "
    "certify station-specific inspection logs, calibration certificates, "
    "calibration status, complete monitor-grade classification, same-station "
    "OpenAQ joins, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_near_closure_id",
    "source_station_id",
    "source_station_name",
    "station_method_class",
    "method_classified",
    "detail_page_display_found",
    "detail_timestamp_iso",
    "detail_value_ug_m3",
    "detail_category_raw",
    "station_page_bam_method_text_found",
    "dashboard_status_raw",
    "dashboard_timestamp_iso",
    "dashboard_timestamp_age_hours",
    "dashboard_current_status_confirmed",
    "dashboard_delayed",
    "source_level_grade_basis_available",
    "source_level_daily_log_or_inspection_sources",
    "source_level_periodic_calibration_rule_sources",
    "source_level_calibration_service_sources",
    "source_level_certificate_context_sources",
    "station_unit_or_exact_context_sources",
    "city_or_deployment_context_sources",
    "exact_station_audit_calibration_sources",
    "pm25_installation_deployment_sources",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "visible_evidence_gate_count",
    "blocking_gate_count",
    "near_closure_lane",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def by_station(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("source_station_id", ""): row for row in rows if row.get("source_station_id")}


def boolish(value: Any) -> bool:
    return str(value or "").strip().casefold() in {"true", "1", "yes"}


def integer(value: Any) -> int:
    try:
        return int(float(str(value or "0").strip() or 0))
    except ValueError:
        return 0


def number_text(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        parsed = float(text)
        return f"{parsed:g}"
    except ValueError:
        return text


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def lane_for(row: dict[str, Any]) -> tuple[str, str]:
    if row["complete_monitor_grade_classification_available"]:
        return ("complete_grade_ready", "Complete monitor-grade evidence is present.")
    if row["exact_station_audit_calibration_sources"] > 0 and row["dashboard_current_status_confirmed"]:
        return (
            "nearest_exact_audit_context_certificate_missing",
            "Exact station audit/calibration context and current dashboard status are visible, but no station-specific PM2.5 certificate or calibration-status record is public.",
        )
    if row["dashboard_delayed"]:
        return (
            "dashboard_delayed_certificate_missing",
            "The row has station-page/method evidence, but the current dashboard lane is delayed and certificate/status closure remains absent.",
        )
    if row["station_unit_or_exact_context_sources"] > 0:
        return (
            "station_unit_context_certificate_missing",
            "Station-unit or exact public context exists, but it is not a certificate, inspection log, calibration-status record, or complete-grade closure.",
        )
    if row["pm25_installation_deployment_sources"] > 0:
        return (
            "pm25_deployment_context_certificate_missing",
            "Official PM2.5 installation or deployment context exists, but it is not station-specific certificate/status closure.",
        )
    if row["dashboard_current_status_confirmed"]:
        return (
            "current_method_visible_certificate_missing",
            "The station has current dashboard-status and method visibility, but no station-specific inspection, certificate, or calibration-status record.",
        )
    return (
        "method_visible_status_certificate_missing",
        "Method and station-page evidence are visible, but public current-status and certificate closure remain absent.",
    )


def build_rows() -> list[dict[str, Any]]:
    method_rows = [
        row
        for row in read_csv(METHOD_CLASSIFICATION_CSV)
        if row.get("iso3") == "IDN" and row.get("source_station_id", "").startswith("pm25_")
    ]
    station_status = by_station(read_csv(STATION_STATUS_CSV))
    dashboard = by_station(read_csv(DASHBOARD_STATUS_CSV))
    grade_basis = by_station(read_csv(GRADE_BASIS_CSV))
    station_context = by_station(read_csv(STATION_CONTEXT_CSV))
    install_audit = by_station(read_csv(INSTALL_AUDIT_CSV))

    generated_at = now_iso()
    rows: list[dict[str, Any]] = []
    for method_row in sorted(method_rows, key=lambda row: row.get("source_station_id", "")):
        station_id = method_row["source_station_id"]
        status_row = station_status.get(station_id, {})
        dashboard_row = dashboard.get(station_id, {})
        grade_row = grade_basis.get(station_id, {})
        context_row = station_context.get(station_id, {})
        install_row = install_audit.get(station_id, {})

        source_level_grade_basis_available = any(
            integer(grade_row.get(field)) > 0
            for field in [
                "source_level_method_basis_sources",
                "source_level_technical_standard_sources",
                "source_level_daily_log_or_inspection_sources",
                "source_level_periodic_calibration_rule_sources",
                "source_level_calibration_service_sources",
                "source_level_certificate_request_or_output_sources",
            ]
        )
        station_unit_or_exact_context_sources = integer(context_row.get("station_unit_or_exact_context_sources"))
        exact_station_audit_calibration_sources = integer(install_row.get("exact_station_audit_calibration_sources"))
        pm25_installation_deployment_sources = integer(install_row.get("pm25_installation_deployment_sources"))
        dashboard_status_raw = dashboard_row.get("dashboard_status_raw", "")

        gates = {
            "method_classified": boolish(method_row.get("station_method_classified")),
            "detail_page_display_found": boolish(status_row.get("page_public_measurement_display_found")),
            "station_page_bam_method_text_found": boolish(status_row.get("page_bam_method_text_found")),
            "dashboard_current_status_confirmed": boolish(dashboard_row.get("current_status_confirmed")),
            "source_level_grade_basis_available": source_level_grade_basis_available,
            "source_level_calibration_rule_available": any(
                integer(grade_row.get(field)) > 0
                for field in [
                    "source_level_periodic_calibration_rule_sources",
                    "source_level_calibration_service_sources",
                    "source_level_certificate_request_or_output_sources",
                ]
            ),
            "station_specific_context_available": (
                station_unit_or_exact_context_sources > 0
                or exact_station_audit_calibration_sources > 0
                or pm25_installation_deployment_sources > 0
            ),
        }
        closure_flags = {
            "station_specific_inspection_log_found": any(
                boolish(row.get("station_specific_inspection_log_found"))
                for row in [status_row, grade_row, context_row, install_row]
            ),
            "station_specific_calibration_certificate_found": any(
                boolish(row.get("station_specific_calibration_certificate_found"))
                for row in [status_row, grade_row, context_row, install_row]
            ),
            "calibration_status_available": any(
                boolish(row.get("calibration_status_available"))
                for row in [status_row, grade_row, context_row, install_row]
            ),
            "complete_monitor_grade_classification_available": any(
                boolish(row.get("complete_monitor_grade_classification_available"))
                for row in [method_row, status_row, dashboard_row, grade_row, context_row, install_row]
            ),
            "station_radius_grade_assumption_ready": any(
                boolish(row.get("station_radius_grade_assumption_ready"))
                for row in [method_row, status_row, dashboard_row, grade_row, context_row, install_row]
            ),
        }

        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "bmkg_near_closure_id": f"IDN-bmkg-near-closure-{station_id}",
            "source_station_id": station_id,
            "source_station_name": method_row.get("source_station_name", ""),
            "station_method_class": method_row.get("station_method_class", ""),
            "method_classified": gates["method_classified"],
            "detail_page_display_found": gates["detail_page_display_found"],
            "detail_timestamp_iso": status_row.get("detail_timestamp_iso", ""),
            "detail_value_ug_m3": number_text(status_row.get("detail_value_ug_m3")),
            "detail_category_raw": status_row.get("detail_category_raw", ""),
            "station_page_bam_method_text_found": gates["station_page_bam_method_text_found"],
            "dashboard_status_raw": dashboard_status_raw,
            "dashboard_timestamp_iso": dashboard_row.get("dashboard_timestamp_iso", ""),
            "dashboard_timestamp_age_hours": number_text(dashboard_row.get("dashboard_timestamp_age_hours")),
            "dashboard_current_status_confirmed": gates["dashboard_current_status_confirmed"],
            "dashboard_delayed": boolish(dashboard_row.get("explicit_dashboard_delayed")),
            "source_level_grade_basis_available": source_level_grade_basis_available,
            "source_level_daily_log_or_inspection_sources": integer(grade_row.get("source_level_daily_log_or_inspection_sources")),
            "source_level_periodic_calibration_rule_sources": integer(grade_row.get("source_level_periodic_calibration_rule_sources")),
            "source_level_calibration_service_sources": integer(grade_row.get("source_level_calibration_service_sources")),
            "source_level_certificate_context_sources": integer(grade_row.get("source_level_certificate_request_or_output_sources")),
            "station_unit_or_exact_context_sources": station_unit_or_exact_context_sources,
            "city_or_deployment_context_sources": integer(context_row.get("city_or_deployment_context_sources")),
            "exact_station_audit_calibration_sources": exact_station_audit_calibration_sources,
            "pm25_installation_deployment_sources": pm25_installation_deployment_sources,
            "station_specific_inspection_log_found": closure_flags["station_specific_inspection_log_found"],
            "station_specific_calibration_certificate_found": closure_flags["station_specific_calibration_certificate_found"],
            "calibration_status_available": closure_flags["calibration_status_available"],
            "complete_monitor_grade_classification_available": closure_flags["complete_monitor_grade_classification_available"],
            "station_radius_grade_assumption_ready": closure_flags["station_radius_grade_assumption_ready"],
            "visible_evidence_gate_count": sum(1 for value in gates.values() if value),
            "blocking_gate_count": sum(1 for value in closure_flags.values() if not value),
            "non_claim": NON_CLAIM,
        }
        lane, reader_use = lane_for(row)
        row["near_closure_lane"] = lane
        row["reader_use"] = reader_use
        rows.append(row)
    return rows


def gate_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gates = [
        ("Station method classified", "method_classified", "available", "BMKG row is classified as BAM from public method evidence."),
        ("Station detail display", "detail_page_display_found", "available", "Exact BMKG station page exposes a PM2.5 display snapshot."),
        ("Station-page BAM method text", "station_page_bam_method_text_found", "available", "Exact station page includes BAM method text."),
        ("Current dashboard status", "dashboard_current_status_confirmed", "partly_available", "Official CEWS dashboard gives current ONLINE status for most rows."),
        ("Source-level grade basis", "source_level_grade_basis_available", "available", "BMKG rules/services provide source-level method, inspection, and calibration context."),
        ("Station-unit/exact public context", "station_unit_or_exact_context_sources", "partly_available", "Some rows have station-unit or exact public context outside the telemetry page."),
        ("Exact audit/calibration context", "exact_station_audit_calibration_sources", "partly_available", "Only exact audit/calibration context, not a certificate, is counted here."),
        ("Station-specific inspection log", "station_specific_inspection_log_found", "not_ready", "No public station-specific inspection log is available."),
        ("Station-specific calibration certificate", "station_specific_calibration_certificate_found", "not_ready", "No public station-specific PM2.5 calibration certificate is available."),
        ("Calibration status record", "calibration_status_available", "not_ready", "No row-level calibration-status record is available."),
        ("Complete monitor-grade closure", "complete_monitor_grade_classification_available", "not_ready", "No row satisfies the complete-grade gate."),
        ("Station-radius readiness", "station_radius_grade_assumption_ready", "not_ready", "No row can support station-radius assumptions from the current evidence."),
    ]
    out: list[dict[str, Any]] = []
    for label, field, status, note in gates:
        if field in {"station_unit_or_exact_context_sources", "exact_station_audit_calibration_sources"}:
            count = sum(1 for row in rows if integer(row.get(field)) > 0)
        else:
            count = sum(1 for row in rows if boolish(row.get(field)))
        out.append({"gate": label, "status": status, "rows": count, "note": note})
    return out


def write_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    top_rows = sorted(
        rows,
        key=lambda row: (
            -integer(row["visible_evidence_gate_count"]),
            -integer(row["exact_station_audit_calibration_sources"]),
            row["source_station_name"],
        ),
    )[:10]
    lines = [
        "# BMKG near-closure ledger",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This synthesis combines the committed BMKG method, station-page, dashboard, grade-basis, station-context, and installation/audit artifacts into one row-level closure ledger. It is a map of evidence gates, not a monitor-grade promotion.",
        "",
        "## Summary counts",
        "",
        "| Measure | Count |",
        "|---|---:|",
    ]
    for key, value in summary["counts"].items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines.extend(
        [
            "",
            "## Evidence gates",
            "",
            "| Gate | Rows | Status |",
            "|---|---:|---|",
        ]
    )
    for gate in summary["evidence_gate_counts"]:
        lines.append(f"| {gate['gate']} | {gate['rows']} | {gate['status']} |")
    lines.extend(
        [
            "",
            "## Nearest rows",
            "",
            "| Station | Visible gates | Lane | Missing closure |",
            "|---|---:|---|---|",
        ]
    )
    for row in top_rows:
        lines.append(
            "| "
            f"{row['source_station_name']} (`{row['source_station_id']}`) | "
            f"{row['visible_evidence_gate_count']} | "
            f"{row['near_closure_lane']} | "
            "station-specific certificate/calibration-status/complete-grade evidence |"
        )
    lines.extend(["", "## Non-claim", "", NON_CLAIM, ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_csv(OUT_CSV, rows, FIELDNAMES)
    lane_counter = Counter(row["near_closure_lane"] for row in rows)
    counts = {
        "bmkg_target_rows": len(rows),
        "station_method_classified_rows": sum(1 for row in rows if boolish(row["method_classified"])),
        "detail_page_display_rows": sum(1 for row in rows if boolish(row["detail_page_display_found"])),
        "dashboard_current_online_rows": sum(1 for row in rows if boolish(row["dashboard_current_status_confirmed"])),
        "dashboard_delayed_rows": sum(1 for row in rows if boolish(row["dashboard_delayed"])),
        "source_level_grade_basis_rows": sum(1 for row in rows if boolish(row["source_level_grade_basis_available"])),
        "station_unit_or_exact_context_rows": sum(1 for row in rows if integer(row["station_unit_or_exact_context_sources"]) > 0),
        "exact_audit_calibration_context_rows": sum(1 for row in rows if integer(row["exact_station_audit_calibration_sources"]) > 0),
        "pm25_installation_deployment_context_rows": sum(1 for row in rows if integer(row["pm25_installation_deployment_sources"]) > 0),
        "station_specific_inspection_log_rows": sum(1 for row in rows if boolish(row["station_specific_inspection_log_found"])),
        "station_specific_calibration_certificate_rows": sum(1 for row in rows if boolish(row["station_specific_calibration_certificate_found"])),
        "calibration_status_rows": sum(1 for row in rows if boolish(row["calibration_status_available"])),
        "complete_monitor_grade_rows": sum(1 for row in rows if boolish(row["complete_monitor_grade_classification_available"])),
        "station_radius_ready_rows": sum(1 for row in rows if boolish(row["station_radius_grade_assumption_ready"])),
    }
    summary = {
        "generated_at": rows[0]["generated_at"] if rows else now_iso(),
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "inputs": [
            str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            str(STATION_STATUS_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            str(DASHBOARD_STATUS_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            str(GRADE_BASIS_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            str(STATION_CONTEXT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
            str(INSTALL_AUDIT_CSV.relative_to(PROGRAM_DIR)).replace("\\", "/"),
        ],
        "counts": counts,
        "lane_counts": [
            {"lane": lane, "rows": count}
            for lane, count in sorted(lane_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": gate_counts(rows),
        "display_rows": sorted(
            rows,
            key=lambda row: (
                -integer(row["visible_evidence_gate_count"]),
                -integer(row["exact_station_audit_calibration_sources"]),
                row["source_station_name"],
            ),
        ),
        "non_claim": NON_CLAIM,
    }
    write_json(OUT_JSON, summary)
    write_markdown(rows, summary)
    print(
        "Built BMKG near-closure ledger: "
        f"{counts['bmkg_target_rows']} rows; "
        f"{counts['dashboard_current_online_rows']} current ONLINE rows; "
        f"{counts['exact_audit_calibration_context_rows']} exact audit/calibration context row; "
        f"{counts['station_specific_calibration_certificate_rows']} certificates; "
        f"{counts['complete_monitor_grade_rows']} complete-grade rows."
    )


if __name__ == "__main__":
    main()
