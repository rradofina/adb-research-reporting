"""Build the station-radius coverage-claim gate.

This is a derivative, no-network gate. It reads the committed station-radius
denominator/country-union artifacts plus the station identity and grade ledgers,
then records whether any economy can support a station-radius coverage claim.
The current answer is deliberately expected to be no until identity, grade, and
claim-permission gates all close.
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

COUNTRY_UNION_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-station-radius-country-unioned-catchment-dry-run-summary.json"
DENOMINATOR_JOIN_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-join-dry-run-summary.json"
READINESS_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-station-radius-denominator-readiness-summary.json"
CANDIDATE_REVIEW_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-review-summary.json"
CANDIDATE_CROSSWALK_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json"
STATION_METHOD_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-station-method-classification-audit-summary.json"
STATION_GRADE_LEDGER_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-station-grade-decision-ledger-summary.json"
BMKG_NEAR_CLOSURE_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-bmkg-near-closure-ledger-summary.json"
BMKG_CERTIFICATE_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-bmkg-certificate-status-targeted-source-scan-summary.json"
UZB_BLOCKER_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup-summary.json"
UZB_ENDPOINT_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-endpoint-consistency-summary.json"
UZB_AIR_PORTAL_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-air-portal-namespace-summary.json"
GEORGIA_REPORT_EXPORT_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-georgia-report-export-ladder-summary.json"
GEORGIA_FREQUENCY_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-georgia-report-frequency-matrix-summary.json"
GEORGIA_INDICATOR_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-georgia-indicator-endpoint-mismatch-summary.json"

OUT_CSV = GENERATED_DIR / "air-monitoring-station-radius-coverage-claim-gate.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-radius-coverage-claim-gate-summary.json"
OUT_MD = PROGRAM_DIR / "station-radius-coverage-claim-gate.md"

METHOD = "air_monitoring_station_radius_coverage_claim_gate_v1"
STATUS = "computed_station_radius_coverage_claim_gate"
ATTESTATION = "ai-first"
NON_CLAIM = (
    "This gate decides whether the current station-radius denominator evidence "
    "may be described as monitor coverage. It does not validate same-station "
    "joins, does not certify complete monitor grade, does not estimate people "
    "served by monitors, and does not create an exposure or regulatory-coverage "
    "claim."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "claim_gate_id",
    "iso3",
    "country",
    "radius_km",
    "coordinate_rows",
    "openaq_coordinate_rows",
    "official_pm25_coordinate_rows",
    "unioned_population_sum",
    "row_level_candidate_population_buffer_sum",
    "row_to_union_population_multiplier",
    "denominator_geometry_gate",
    "station_identity_gate",
    "monitor_grade_gate",
    "station_radius_readiness_gate",
    "coverage_claim_gate",
    "coverage_claim_allowed",
    "release_decision",
    "reader_use",
    "blocking_gaps",
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
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDNAMES})


def truthy(value: Any) -> bool:
    return str(value).strip().casefold() in {"true", "1", "yes"}


def number(value: Any) -> float:
    try:
        return float(str(value or "0").strip() or 0)
    except ValueError:
        return 0.0


def integer(value: Any) -> int:
    return int(round(number(value)))


def count_from(summary: dict[str, Any], *keys: str) -> int:
    current: Any = summary
    for key in keys:
        if not isinstance(current, dict):
            return 0
        current = current.get(key, 0)
    return integer(current)


def gate_row(status: str, gate: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate, "rows": rows, "reader_use": reader_use}


def source_input(path: Path, role: str) -> dict[str, str]:
    return {"path": str(path.relative_to(PROGRAM_DIR)).replace("\\", "/"), "role": role}


def build_country_rows(generated_at: str, country_union: dict[str, Any]) -> list[dict[str, Any]]:
    primary_rows = [
        row
        for row in country_union.get("country_rows", country_union.get("top_primary_radius_country_rows", []))
        if str(row.get("radius_role")) == "primary"
    ]
    output: list[dict[str, Any]] = []
    for row in primary_rows:
        denominator_ready = truthy(row.get("country_union_population_computed"))
        identity_ready = integer(row.get("validated_same_station_join_rows")) > 0
        grade_ready = integer(row.get("complete_monitor_grade_rows")) > 0
        radius_ready = truthy(row.get("station_radius_ready"))
        claim_allowed = (
            denominator_ready
            and identity_ready
            and grade_ready
            and radius_ready
            and truthy(row.get("coverage_claim_allowed"))
        )
        gaps = []
        if not identity_ready:
            gaps.append("validated same-station identity")
        if not grade_ready:
            gaps.append("complete monitor-grade evidence")
        if not radius_ready:
            gaps.append("station-radius readiness")
        if not claim_allowed:
            gaps.append("coverage-claim permission")
        release_decision = "claim_allowed" if claim_allowed else "block_coverage_claim"
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "claim_gate_id": f"{row.get('iso3')}-station-radius-coverage-claim-gate",
                "iso3": row.get("iso3", ""),
                "country": row.get("country", ""),
                "radius_km": row.get("radius_km", ""),
                "coordinate_rows": row.get("coordinate_rows", 0),
                "openaq_coordinate_rows": row.get("openaq_coordinate_rows", 0),
                "official_pm25_coordinate_rows": row.get("official_pm25_coordinate_rows", 0),
                "unioned_population_sum": row.get("unioned_population_sum", ""),
                "row_level_candidate_population_buffer_sum": row.get("row_level_candidate_population_buffer_sum", ""),
                "row_to_union_population_multiplier": row.get("row_to_union_population_multiplier", ""),
                "denominator_geometry_gate": "computed" if denominator_ready else "blocked",
                "station_identity_gate": "available" if identity_ready else "blocked",
                "monitor_grade_gate": "available" if grade_ready else "blocked",
                "station_radius_readiness_gate": "available" if radius_ready else "blocked",
                "coverage_claim_gate": "allowed" if claim_allowed else "blocked",
                "coverage_claim_allowed": claim_allowed,
                "release_decision": release_decision,
                "reader_use": (
                    "May support a station-radius coverage claim."
                    if claim_allowed
                    else "Show as denominator geometry only; do not describe as monitor coverage or people served."
                ),
                "blocking_gaps": "||".join(gaps),
                "non_claim": NON_CLAIM,
            }
        )
    return output


def build_summary(generated_at: str, rows: list[dict[str, Any]], inputs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    country_union = inputs["country_union"]
    denominator_join = inputs["denominator_join"]
    readiness = inputs["readiness"]
    candidate_review = inputs["candidate_review"]
    candidate_crosswalk = inputs["candidate_crosswalk"]
    station_method = inputs["station_method"]
    station_grade = inputs["station_grade"]
    bmkg_near = inputs["bmkg_near"]
    bmkg_certificate = inputs["bmkg_certificate"]
    uzb_blocker = inputs["uzb_blocker"]
    uzb_endpoint = inputs["uzb_endpoint"]
    uzb_air_portal = inputs["uzb_air_portal"]
    georgia_export = inputs["georgia_export"]
    georgia_frequency = inputs["georgia_frequency"]
    georgia_indicator = inputs["georgia_indicator"]

    country_union_counts = country_union.get("coverage_counts", {})
    denom_counts = denominator_join.get("coverage_counts", {})
    readiness_counts = readiness.get("coverage_counts", {})
    review_counts = candidate_review.get("coverage_counts", {})
    crosswalk_counts = candidate_crosswalk.get("coverage_counts", {})
    method_counts = station_method.get("coverage_counts", {})
    grade_counts = station_grade.get("coverage_counts", {})
    bmkg_near_counts = bmkg_near.get("counts", {})
    bmkg_certificate_counts = bmkg_certificate.get("coverage_counts", {})

    claim_allowed_rows = sum(1 for row in rows if truthy(row["coverage_claim_allowed"]))
    release_counter = Counter(row["release_decision"] for row in rows)

    counts = {
        "primary_radius_country_rows_checked": len(rows),
        "coordinate_economies": count_from(country_union, "coverage_counts", "coordinate_economies"),
        "country_union_rows_computed": count_from(country_union, "coverage_counts", "country_union_rows_computed"),
        "country_union_population_rows_computed": count_from(
            country_union, "coverage_counts", "country_union_population_rows_computed"
        ),
        "country_union_pm25_rows_computed": count_from(country_union, "coverage_counts", "country_union_pm25_rows_computed"),
        "denominator_join_rows": count_from(denominator_join, "coverage_counts", "candidate_coordinate_radius_rows"),
        "ghsl_population_rows_computed": count_from(denominator_join, "coverage_counts", "population_rows_computed"),
        "acag_pm25_rows_computed": count_from(denominator_join, "coverage_counts", "pm25_rows_computed"),
        "validated_same_station_join_rows": max(
            count_from(country_union, "coverage_counts", "validated_same_station_join_rows"),
            count_from(readiness, "coverage_counts", "validated_same_station_join_rows"),
            count_from(candidate_review, "coverage_counts", "validated_same_station_rows"),
            count_from(candidate_crosswalk, "coverage_counts", "validated_same_station_rows"),
        ),
        "candidate_review_rows": count_from(candidate_review, "coverage_counts", "near_plus_name_candidate_rows"),
        "candidate_crosswalk_source_scan_rows": count_from(candidate_crosswalk, "coverage_counts", "is_monitor_candidate_rows_scanned"),
        "complete_monitor_grade_rows": max(
            count_from(country_union, "coverage_counts", "complete_monitor_grade_rows"),
            count_from(readiness, "coverage_counts", "complete_monitor_grade_rows"),
            count_from(station_method, "coverage_counts", "complete_monitor_grade_classification_rows"),
            count_from(station_grade, "coverage_counts", "complete_monitor_grade_classification_rows"),
        ),
        "station_method_classified_rows": count_from(station_method, "coverage_counts", "bmkg_method_classified_rows"),
        "current_status_confirmed_rows": count_from(station_method, "coverage_counts", "current_status_confirmed_rows"),
        "calibration_status_available_rows": count_from(station_method, "coverage_counts", "calibration_status_available_rows"),
        "station_radius_ready_economies": max(
            count_from(country_union, "coverage_counts", "station_radius_ready_economies"),
            count_from(readiness, "coverage_counts", "station_radius_ready_economies"),
        ),
        "station_radius_ready_rows": max(
            count_from(station_method, "coverage_counts", "station_radius_grade_assumption_ready_rows"),
            count_from(station_grade, "coverage_counts", "station_radius_grade_assumption_ready_rows"),
        ),
        "claim_allowed_country_rows": claim_allowed_rows,
        "coverage_claim_allowed": claim_allowed_rows > 0,
    }

    blocker_context = {
        "bmkg_target_rows": integer(bmkg_near_counts.get("bmkg_target_rows", 0)),
        "bmkg_method_classified_rows": integer(bmkg_near_counts.get("station_method_classified_rows", 0)),
        "bmkg_dashboard_current_online_rows": integer(bmkg_near_counts.get("dashboard_current_online_rows", 0)),
        "bmkg_station_specific_inspection_log_rows": max(
            integer(bmkg_near_counts.get("station_specific_inspection_log_rows", 0)),
            integer(bmkg_certificate_counts.get("station_specific_inspection_log_rows", 0)),
        ),
        "bmkg_station_specific_calibration_certificate_rows": max(
            integer(bmkg_near_counts.get("station_specific_calibration_certificate_rows", 0)),
            integer(bmkg_certificate_counts.get("station_specific_calibration_certificate_rows", 0)),
        ),
        "bmkg_calibration_status_rows": max(
            integer(bmkg_near_counts.get("calibration_status_rows", 0)),
            integer(bmkg_certificate_counts.get("calibration_status_available_rows", 0)),
        ),
        "uzbekistan_unresolved_blocker_rows": max(
            0,
            count_from(uzb_blocker, "coverage_counts", "target_blocker_rows")
            - count_from(uzb_blocker, "coverage_counts", "public_row_followup_resolved_rows"),
        ),
        "uzbekistan_endpoint_mismatch_rows": max(
            count_from(uzb_endpoint, "coverage_counts", "date_status_mismatch_rows"),
            count_from(uzb_endpoint, "coverage_counts", "region_detail_status_mismatch_rows"),
        ),
        "uzbekistan_air_portal_resolution_rows": count_from(uzb_air_portal, "coverage_counts", "public_portal_resolution_rows"),
        "georgia_verified_report_closure_rows": max(
            count_from(georgia_export, "coverage_counts", "verified_report_closure_rows"),
            count_from(georgia_frequency, "coverage_counts", "verified_report_closure_rows"),
        ),
        "georgia_indicator_exact_station_code_rows": count_from(georgia_indicator, "coverage_counts", "exact_target_station_code_matches"),
    }

    evidence_gate_counts = [
        gate_row(
            "computed",
            "Country-unioned denominator geometry",
            counts["country_union_population_rows_computed"],
            "GHSL cells are unioned once per economy/radius band; this is geometry only.",
        ),
        gate_row(
            "computed",
            "ACAG PM2.5 context",
            counts["country_union_pm25_rows_computed"],
            "Coarse grid-cell context exists for some union cells, but it is not exposure.",
        ),
        gate_row(
            "blocked",
            "Validated same-station identity",
            counts["validated_same_station_join_rows"],
            "No public crosswalk or shared station-ID evidence validates official/OpenAQ rows as the same station.",
        ),
        gate_row(
            "partly_available",
            "Station-method classification",
            counts["station_method_classified_rows"],
            "BMKG method rows are classified, but method classification is not complete monitor-grade evidence.",
        ),
        gate_row(
            "blocked",
            "Current status confirmed",
            counts["current_status_confirmed_rows"],
            "Visibility or dashboard status is not station-status certification in the grade ledger.",
        ),
        gate_row(
            "blocked",
            "Calibration/status record",
            counts["calibration_status_available_rows"],
            "No row-level calibration-status record is available.",
        ),
        gate_row(
            "blocked",
            "Complete monitor-grade rows",
            counts["complete_monitor_grade_rows"],
            "No station row has complete public monitor-grade closure.",
        ),
        gate_row(
            "blocked",
            "Station-radius readiness",
            counts["station_radius_ready_economies"],
            "No economy is ready for a station-radius coverage claim.",
        ),
        gate_row(
            "blocked",
            "Coverage claim permission",
            counts["claim_allowed_country_rows"],
            "The publication surface may show denominator diagnostics only.",
        ),
    ]

    top_rows = sorted(rows, key=lambda row: number(row["unioned_population_sum"]), reverse=True)[:8]

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-radius coverage-claim gate",
        "claim_rule": {
            "rule": "A station-radius coverage claim is allowed only when denominator geometry is computed, validated same-station identity rows exist, complete monitor-grade rows exist, station-radius readiness is true, and the coverage-claim flag is true for the row/economy.",
            "allowed": counts["coverage_claim_allowed"],
            "current_decision": "block_coverage_claim",
        },
        "source_inputs": [
            source_input(COUNTRY_UNION_SUMMARY_JSON, "country-unioned catchment denominator dry run"),
            source_input(DENOMINATOR_JOIN_SUMMARY_JSON, "row-level denominator join dry run"),
            source_input(READINESS_SUMMARY_JSON, "station-radius readiness wall"),
            source_input(CANDIDATE_REVIEW_SUMMARY_JSON, "candidate same-station review worksheet"),
            source_input(CANDIDATE_CROSSWALK_SUMMARY_JSON, "candidate public crosswalk source scan"),
            source_input(STATION_METHOD_SUMMARY_JSON, "station-method classification audit"),
            source_input(STATION_GRADE_LEDGER_SUMMARY_JSON, "station-grade decision ledger"),
            source_input(BMKG_NEAR_CLOSURE_SUMMARY_JSON, "BMKG near-closure ledger"),
            source_input(BMKG_CERTIFICATE_SUMMARY_JSON, "BMKG targeted certificate/status source scan"),
            source_input(UZB_BLOCKER_SUMMARY_JSON, "Uzbekistan blocker-row follow-up"),
            source_input(UZB_ENDPOINT_SUMMARY_JSON, "Uzbekistan endpoint consistency check"),
            source_input(UZB_AIR_PORTAL_SUMMARY_JSON, "Uzbekistan Air Uzbekistan portal namespace wall"),
            source_input(GEORGIA_REPORT_EXPORT_SUMMARY_JSON, "Georgia report/export verification ladder"),
            source_input(GEORGIA_FREQUENCY_SUMMARY_JSON, "Georgia report-frequency matrix"),
            source_input(GEORGIA_INDICATOR_SUMMARY_JSON, "Georgia indicator endpoint mismatch scan"),
        ],
        "coverage_counts": counts,
        "blocker_context_counts": blocker_context,
        "release_decision_counts": [
            {"release_decision": decision, "rows": count}
            for decision, count in sorted(release_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "evidence_gate_counts": evidence_gate_counts,
        "display_rows": top_rows,
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
        "# Station-radius coverage-claim gate",
        "",
        "`attestation_chain: ai-first`",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## What this adds",
        "",
        "This derivative gate reads the committed denominator, country-union, station-identity, and monitor-grade artifacts and decides whether the public surface may use station-radius coverage language.",
        "",
        "It currently blocks the claim. The denominator geometry is computed, but the identity and grade prerequisites remain at zero.",
        "",
        "## Mechanical rule",
        "",
        summary["claim_rule"]["rule"],
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
    lines.extend(["", "## Largest blocked denominator rows", "", "| Economy | Unioned denominator | Decision | Missing gates |", "|---|---:|---|---|"])
    for row in summary["display_rows"]:
        lines.append(
            "| "
            f"{row['country']} (`{row['iso3']}`) | "
            f"{row['unioned_population_sum']} | "
            f"{row['release_decision']} | "
            f"{row['blocking_gaps'].replace('||', ', ')} |"
        )
    lines.extend(["", "## Non-claim", "", summary["non_claim"], ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = {
        "country_union": read_json(COUNTRY_UNION_SUMMARY_JSON),
        "denominator_join": read_json(DENOMINATOR_JOIN_SUMMARY_JSON),
        "readiness": read_json(READINESS_SUMMARY_JSON),
        "candidate_review": read_json(CANDIDATE_REVIEW_SUMMARY_JSON),
        "candidate_crosswalk": read_json(CANDIDATE_CROSSWALK_SUMMARY_JSON),
        "station_method": read_json(STATION_METHOD_SUMMARY_JSON),
        "station_grade": read_json(STATION_GRADE_LEDGER_SUMMARY_JSON),
        "bmkg_near": read_json(BMKG_NEAR_CLOSURE_SUMMARY_JSON),
        "bmkg_certificate": read_json(BMKG_CERTIFICATE_SUMMARY_JSON),
        "uzb_blocker": read_json(UZB_BLOCKER_SUMMARY_JSON),
        "uzb_endpoint": read_json(UZB_ENDPOINT_SUMMARY_JSON),
        "uzb_air_portal": read_json(UZB_AIR_PORTAL_SUMMARY_JSON),
        "georgia_export": read_json(GEORGIA_REPORT_EXPORT_SUMMARY_JSON),
        "georgia_frequency": read_json(GEORGIA_FREQUENCY_SUMMARY_JSON),
        "georgia_indicator": read_json(GEORGIA_INDICATOR_SUMMARY_JSON),
    }
    generated_at = now_iso()
    rows = build_country_rows(generated_at, inputs["country_union"])
    summary = build_summary(generated_at, rows, inputs)

    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_markdown(summary)

    counts = summary["coverage_counts"]
    print(
        "Built station-radius coverage-claim gate: "
        f"{counts['primary_radius_country_rows_checked']} country rows checked; "
        f"{counts['country_union_population_rows_computed']} unioned denominators; "
        f"{counts['validated_same_station_join_rows']} validated joins; "
        f"{counts['complete_monitor_grade_rows']} complete-grade rows; "
        f"coverage_claim_allowed={str(counts['coverage_claim_allowed']).lower()}."
    )


if __name__ == "__main__":
    main()
