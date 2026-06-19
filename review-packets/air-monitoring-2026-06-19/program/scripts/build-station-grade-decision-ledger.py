#!/usr/bin/env python
"""Build a row-level station-grade decision ledger for air monitoring.

This is a no-network derivative artifact. It joins the committed exact-row
method evidence and follow-up source scans, then writes one decision row per
method-context station row. It does not promote any row to monitor-grade or
station-radius readiness.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

METHOD_EVIDENCE_CSV = GENERATED_DIR / "air-monitoring-monitor-grade-station-method-evidence.csv"
UZB_STATION_SPECIFIC_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-specific-source-evidence.csv"
UZB_STATUS_CERTIFICATION_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-status-certification-source-scan.csv"
UZB_BLOCKER_FOLLOWUP_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup.csv"
IDN_GEO_ROW_METHOD_CSV = GENERATED_DIR / "air-monitoring-indonesia-georgia-row-method-source-scan.csv"
STATION_CODE_STATUS_CSV = GENERATED_DIR / "air-monitoring-station-code-status-method-source-scan.csv"

OUT_CSV = GENERATED_DIR / "air-monitoring-station-grade-decision-ledger.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-grade-decision-ledger-summary.json"

METHOD = "air_monitoring_station_grade_decision_ledger_v1"
STATUS = "computed_station_grade_decision_ledger"
ATTESTATION = "ai-first"
GOAL_LEVEL = "L3 station-grade decision ledger"
NON_CLAIM = (
    "This decision ledger summarizes row-level evidence gates from committed "
    "source scans. It does not certify current station status, complete "
    "monitor-grade classification, same-station joins, or station-radius "
    "population coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "decision_ledger_id",
    "method_evidence_id",
    "iso3",
    "country",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "row_evidence_lane",
    "exact_official_row_found",
    "exact_station_code_or_id_source_found",
    "pm25_row_or_equipment_listed",
    "row_level_instrument_hint",
    "station_method_context_present",
    "station_code_context_present",
    "station_specific_context_present",
    "operating_or_current_context_present",
    "status_or_certification_context_present",
    "calibration_or_maintenance_context_present",
    "raw_value_sanity_issue_present",
    "test_mode_or_blocker_present",
    "stale_or_sentinel_blocker_present",
    "station_method_table_found",
    "calibration_status_available",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "decision_lane",
    "minimum_public_evidence_needed",
    "source_threads",
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
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_id(value: str) -> str:
    chars: list[str] = []
    for char in value.strip():
        if char.isalnum():
            chars.append(char)
        elif char in {"-", "_"}:
            chars.append(char)
        elif char.isspace() or char in {"/", "|", ":", ".", "#", "\\"}:
            chars.append("-")
    return "-".join("".join(chars).strip("-").split("-"))


def boolish(value: Any) -> bool:
    return str(value or "").strip().casefold() in {"true", "1", "yes", "y"}


def intish(value: Any) -> int:
    try:
        return int(float(str(value or "").strip()))
    except ValueError:
        return 0


def index_by_station(rows: list[dict[str, str]], iso3: str | None = None) -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        if iso3 and row.get("iso3") and row.get("iso3") != iso3:
            continue
        station_id = str(row.get("source_station_id", "")).strip()
        if station_id:
            output[station_id] = row
    return output


def evidence_needed(lane: str) -> str:
    if lane == "blocked_test_mode_or_stale_sentinel":
        return (
            "A public station-owner or regulator row that clears the test-mode, "
            "stale-detail, updating-data, or sentinel-value blocker and states "
            "current operating status."
        )
    if lane == "raw_value_sanity_open":
        return (
            "A public QA/status explanation for the negative or sentinel raw "
            "PM2.5 value, plus station-level method and current-status evidence."
        )
    if lane == "station_code_context_not_grade_ready":
        return (
            "A station-code method table or station-owner/regulator source that "
            "names the instrument/method class, current status, and grade basis "
            "for this exact station code."
        )
    if lane == "station_specific_context_not_grade_ready":
        return (
            "A station-specific source that moves from detail-page or update "
            "context to explicit current-status, method-class, and grade closure."
        )
    return (
        "A public station-level method, calibration/status, certification, or "
        "regulator table that connects the source context to this exact row."
    )


def reader_use(lane: str) -> str:
    return {
        "blocked_test_mode_or_stale_sentinel": (
            "Use as an exclusion or hold row. The evidence identifies a source "
            "blocker before any grade or radius assumption."
        ),
        "raw_value_sanity_open": (
            "Use as a QA follow-up row. The station row is visible, but raw-value "
            "sanity prevents status closure."
        ),
        "station_code_context_not_grade_ready": (
            "Use as a high-value method follow-up. Exact station-code context is "
            "available, but grade fields are still absent."
        ),
        "station_specific_context_not_grade_ready": (
            "Use as a station-status follow-up. Station-specific public rows "
            "exist, but the source does not certify grade."
        ),
        "method_context_not_grade_ready": (
            "Use as an open station-method lead. Method context exists without "
            "station-level status and grade closure."
        ),
    }[lane]


def decide_lane(
    base: dict[str, str],
    station_code: dict[str, str] | None,
    uzb_specific: dict[str, str] | None,
    uzb_status: dict[str, str] | None,
    uzb_blocker: dict[str, str] | None,
    idn_geo: dict[str, str] | None,
) -> str:
    if station_code and boolish(station_code.get("station_test_mode_flag")):
        return "blocked_test_mode_or_stale_sentinel"
    if uzb_blocker and (
        boolish(uzb_blocker.get("stale_detail_blocker_present"))
        or boolish(uzb_blocker.get("sentinel_pm25_blocker_present"))
        or not boolish(uzb_blocker.get("public_row_followup_resolved_blocker"))
    ):
        return "blocked_test_mode_or_stale_sentinel"
    raw_statuses = {
        base.get("exact_live_pm25_value_status", ""),
        (uzb_specific or {}).get("official_detail_pm25_value_status", ""),
        (uzb_status or {}).get("official_detail_pm25_value_status", ""),
    }
    if any(status in {"negative_raw_value", "sentinel_minus_9999"} for status in raw_statuses):
        return "raw_value_sanity_open"
    if station_code and boolish(station_code.get("exact_station_code_or_id_found")):
        return "station_code_context_not_grade_ready"
    if uzb_specific and boolish(uzb_specific.get("official_region_view_id_matches_target")):
        return "station_specific_context_not_grade_ready"
    if idn_geo and (
        boolish(idn_geo.get("same_page_method_context_candidate"))
        or boolish(idn_geo.get("station_context_candidate"))
    ):
        return "method_context_not_grade_ready"
    return "method_context_not_grade_ready"


def source_threads(
    station_code: dict[str, str] | None,
    uzb_specific: dict[str, str] | None,
    uzb_status: dict[str, str] | None,
    uzb_blocker: dict[str, str] | None,
    idn_geo: dict[str, str] | None,
) -> str:
    threads: list[str] = []
    if station_code:
        threads.append("station_code_status_method_source_scan")
    if idn_geo:
        threads.append("indonesia_georgia_row_method_source_scan")
    if uzb_specific:
        threads.append("uzbekistan_station_specific_source_evidence")
    if uzb_status:
        threads.append("uzbekistan_status_certification_source_scan")
    if uzb_blocker:
        threads.append("uzbekistan_blocker_row_followup")
    return "|".join(threads)


def build_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    generated_at = now_iso()
    base_rows = read_csv(METHOD_EVIDENCE_CSV)
    uzb_specific_rows = index_by_station(read_csv(UZB_STATION_SPECIFIC_CSV))
    uzb_status_rows = index_by_station(read_csv(UZB_STATUS_CERTIFICATION_CSV))
    uzb_blocker_rows = index_by_station(read_csv(UZB_BLOCKER_FOLLOWUP_CSV))
    idn_geo_rows = index_by_station(read_csv(IDN_GEO_ROW_METHOD_CSV))
    station_code_rows = index_by_station(read_csv(STATION_CODE_STATUS_CSV))

    output_rows: list[dict[str, Any]] = []
    for base in sorted(base_rows, key=lambda row: (row["iso3"], row["source_station_id"])):
        station_id = base["source_station_id"]
        station_code = station_code_rows.get(station_id)
        idn_geo = idn_geo_rows.get(station_id)
        uzb_specific = uzb_specific_rows.get(station_id) if base["iso3"] == "UZB" else None
        uzb_status = uzb_status_rows.get(station_id) if base["iso3"] == "UZB" else None
        uzb_blocker = uzb_blocker_rows.get(station_id) if base["iso3"] == "UZB" else None

        exact_station_code_or_id = (
            boolish((station_code or {}).get("exact_station_code_or_id_found"))
            or boolish((uzb_specific or {}).get("official_region_view_id_matches_target"))
            or boolish(base.get("exact_official_row_found"))
        )
        pm25_listed = (
            boolish((station_code or {}).get("pm25_row_or_equipment_listed"))
            or boolish(base.get("exact_pm25_signal"))
        )
        row_instrument_hint = base.get("row_evidence_lane") == "row_level_instrument_hint"
        station_code_context = boolish((station_code or {}).get("exact_station_code_or_id_found"))
        station_specific_context = boolish((uzb_specific or {}).get("target_station_id_named_in_non_api_source"))
        station_method_context = (
            row_instrument_hint
            or boolish((idn_geo or {}).get("same_page_method_context_candidate"))
            or boolish((station_code or {}).get("station_method_table_found"))
            or boolish((uzb_specific or {}).get("station_specific_equipment_context_found"))
            or intish((uzb_status or {}).get("source_level_method_context_sources")) > 0
        )
        operating_or_current_context = (
            boolish(base.get("public_current_row_observed"))
            or boolish((station_code or {}).get("station_description_operating_context"))
            or boolish((idn_geo or {}).get("same_page_current_context_candidate"))
            or boolish((uzb_specific or {}).get("station_specific_status_or_update_context_found"))
            or intish((uzb_status or {}).get("source_level_current_context_sources")) > 0
        )
        status_or_certification_context = (
            intish((uzb_status or {}).get("source_level_certification_context_sources")) > 0
            or boolish((uzb_status or {}).get("tashkent_reference_grade_context_candidate"))
            or boolish((uzb_status or {}).get("district_commissioning_context_candidate"))
        )
        calibration_or_maintenance_context = (
            intish((uzb_status or {}).get("source_level_calibration_context_sources")) > 0
            or boolish((uzb_status or {}).get("maintenance_or_training_context_rows"))
        )
        raw_statuses = {
            base.get("exact_live_pm25_value_status", ""),
            (uzb_specific or {}).get("official_detail_pm25_value_status", ""),
            (uzb_status or {}).get("official_detail_pm25_value_status", ""),
            (uzb_blocker or {}).get("detail_pm25_value_status", ""),
        }
        raw_value_issue = any(status in {"negative_raw_value", "sentinel_minus_9999"} for status in raw_statuses)
        stale_or_sentinel = boolish((uzb_blocker or {}).get("stale_detail_blocker_present")) or boolish(
            (uzb_blocker or {}).get("sentinel_pm25_blocker_present")
        )
        test_or_blocker = boolish((station_code or {}).get("station_test_mode_flag")) or stale_or_sentinel
        lane = decide_lane(base, station_code, uzb_specific, uzb_status, uzb_blocker, idn_geo)

        output_rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": ATTESTATION,
                "status": STATUS,
                "method": METHOD,
                "decision_ledger_id": clean_id(f"{base['iso3']}-{lane}-{station_id}"),
                "method_evidence_id": base["method_evidence_id"],
                "iso3": base["iso3"],
                "country": base["country"],
                "source_station_id": station_id,
                "source_station_name": base["source_station_name"],
                "source_station_type": base["source_station_type"],
                "row_evidence_lane": base["row_evidence_lane"],
                "exact_official_row_found": boolish(base.get("exact_official_row_found")),
                "exact_station_code_or_id_source_found": exact_station_code_or_id,
                "pm25_row_or_equipment_listed": pm25_listed,
                "row_level_instrument_hint": row_instrument_hint,
                "station_method_context_present": station_method_context,
                "station_code_context_present": station_code_context,
                "station_specific_context_present": station_specific_context,
                "operating_or_current_context_present": operating_or_current_context,
                "status_or_certification_context_present": status_or_certification_context,
                "calibration_or_maintenance_context_present": calibration_or_maintenance_context,
                "raw_value_sanity_issue_present": raw_value_issue,
                "test_mode_or_blocker_present": test_or_blocker,
                "stale_or_sentinel_blocker_present": stale_or_sentinel,
                "station_method_table_found": boolish((station_code or {}).get("station_method_table_found")),
                "calibration_status_available": boolish((station_code or {}).get("calibration_status_available")),
                "current_status_confirmed": boolish(base.get("current_status_confirmed")),
                "station_method_classified": boolish(base.get("station_method_classified")),
                "complete_monitor_grade_classification_available": boolish(
                    base.get("complete_monitor_grade_classification_available")
                ),
                "station_radius_grade_assumption_ready": boolish(
                    base.get("station_radius_grade_assumption_ready")
                ),
                "decision_lane": lane,
                "minimum_public_evidence_needed": evidence_needed(lane),
                "source_threads": source_threads(station_code, uzb_specific, uzb_status, uzb_blocker, idn_geo),
                "reader_use": reader_use(lane),
                "non_claim": NON_CLAIM,
            }
        )

    summary = build_summary(generated_at, output_rows)
    return output_rows, summary


def count_bool(rows: list[dict[str, Any]], field: str) -> int:
    return sum(1 for row in rows if row.get(field) is True)


def build_summary(generated_at: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_country: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_country[row["iso3"]].append(row)

    country_rows = []
    for iso3, country_group in sorted(by_country.items()):
        country_rows.append(
            {
                "iso3": iso3,
                "country": country_group[0]["country"],
                "decision_rows": len(country_group),
                "exact_station_code_or_id_source_rows": count_bool(
                    country_group, "exact_station_code_or_id_source_found"
                ),
                "station_method_context_rows": count_bool(country_group, "station_method_context_present"),
                "operating_or_current_context_rows": count_bool(
                    country_group, "operating_or_current_context_present"
                ),
                "raw_value_sanity_issue_rows": count_bool(country_group, "raw_value_sanity_issue_present"),
                "test_mode_or_blocker_rows": count_bool(country_group, "test_mode_or_blocker_present"),
                "current_status_confirmed_rows": count_bool(country_group, "current_status_confirmed"),
                "complete_monitor_grade_classification_rows": count_bool(
                    country_group, "complete_monitor_grade_classification_available"
                ),
                "station_radius_grade_assumption_ready_rows": count_bool(
                    country_group, "station_radius_grade_assumption_ready"
                ),
            }
        )

    decision_counter = Counter(row["decision_lane"] for row in rows)
    decision_counts = [
        {
            "decision_lane": lane,
            "rows": count,
            "reader_use": reader_use(lane),
            "minimum_public_evidence_needed": evidence_needed(lane),
        }
        for lane, count in decision_counter.most_common()
    ]

    blockers_first = {
        "blocked_test_mode_or_stale_sentinel": 0,
        "raw_value_sanity_open": 1,
        "station_code_context_not_grade_ready": 2,
        "station_specific_context_not_grade_ready": 3,
        "method_context_not_grade_ready": 4,
    }
    sample_rows = sorted(
        rows,
        key=lambda row: (
            blockers_first.get(str(row["decision_lane"]), 9),
            row["iso3"],
            str(row["source_station_id"]),
        ),
    )[:16]

    evidence_gate_counts = [
        {
            "gate": "Exact official row found",
            "status": "available",
            "rows": count_bool(rows, "exact_official_row_found"),
            "reader_use": "Every ledger row starts from the committed exact station-row method-evidence audit.",
        },
        {
            "gate": "Station code or station-detail ID source",
            "status": "available",
            "rows": count_bool(rows, "exact_station_code_or_id_source_found"),
            "reader_use": "Exact public station-code, station-detail ID, or official-row evidence is present.",
        },
        {
            "gate": "Method or instrument context",
            "status": "partly_available",
            "rows": count_bool(rows, "station_method_context_present"),
            "reader_use": "Method/instrument context exists, but it is not complete station-grade classification.",
        },
        {
            "gate": "Operating or current-data context",
            "status": "partly_available",
            "rows": count_bool(rows, "operating_or_current_context_present"),
            "reader_use": "The source has live-row, update, or operating context; this is not current-status certification.",
        },
        {
            "gate": "Raw-value or blocker caution",
            "status": "caution",
            "rows": sum(
                1
                for row in rows
                if row["raw_value_sanity_issue_present"] or row["test_mode_or_blocker_present"]
            ),
            "reader_use": "Rows with negative/sentinel raw values, test mode, stale detail, or updating-data blockers need explicit source resolution.",
        },
        {
            "gate": "Station method table",
            "status": "not_ready",
            "rows": count_bool(rows, "station_method_table_found"),
            "reader_use": "No row has a complete method table that classifies the exact station.",
        },
        {
            "gate": "Calibration or status record",
            "status": "not_ready",
            "rows": count_bool(rows, "calibration_status_available"),
            "reader_use": "No row has public calibration/status closure adequate for grade use.",
        },
        {
            "gate": "Current status confirmed",
            "status": "not_ready",
            "rows": count_bool(rows, "current_status_confirmed"),
            "reader_use": "Current-status certification remains unavailable in the committed public evidence.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": count_bool(rows, "complete_monitor_grade_classification_available"),
            "reader_use": "No station row is promoted to complete monitor-grade classification.",
        },
        {
            "gate": "Station-radius assumptions",
            "status": "not_ready",
            "rows": count_bool(rows, "station_radius_grade_assumption_ready"),
            "reader_use": "No row is ready for station-radius or catchment coverage assumptions.",
        },
    ]

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": ATTESTATION,
        "status": STATUS,
        "method": METHOD,
        "goal_level": GOAL_LEVEL,
        "source_inputs": [
            {
                "path": "generated\\air-monitoring-monitor-grade-station-method-evidence.csv",
                "role": "base 66-row exact station method-evidence audit",
            },
            {
                "path": "generated\\air-monitoring-uzbekistan-station-specific-source-evidence.csv",
                "role": "Uzbekistan station-detail and regional station-table context",
            },
            {
                "path": "generated\\air-monitoring-uzbekistan-status-certification-source-scan.csv",
                "role": "Uzbekistan status, certification, maintenance, and reference-grade context",
            },
            {
                "path": "generated\\air-monitoring-uzbekistan-blocker-row-followup.csv",
                "role": "exact follow-up for the three unresolved Uzbekistan blockers",
            },
            {
                "path": "generated\\air-monitoring-indonesia-georgia-row-method-source-scan.csv",
                "role": "Indonesia and Georgia exact row-method source context",
            },
            {
                "path": "generated\\air-monitoring-station-code-status-method-source-scan.csv",
                "role": "station-code/status source scan for Indonesia, Georgia, and blocker rows",
            },
        ],
        "coverage_counts": {
            "decision_rows": len(rows),
            "uzbekistan_rows": sum(1 for row in rows if row["iso3"] == "UZB"),
            "georgia_rows": sum(1 for row in rows if row["iso3"] == "GEO"),
            "indonesia_rows": sum(1 for row in rows if row["iso3"] == "IDN"),
            "exact_official_row_found_rows": count_bool(rows, "exact_official_row_found"),
            "exact_station_code_or_id_source_rows": count_bool(rows, "exact_station_code_or_id_source_found"),
            "pm25_row_or_equipment_rows": count_bool(rows, "pm25_row_or_equipment_listed"),
            "row_level_instrument_hint_rows": count_bool(rows, "row_level_instrument_hint"),
            "station_method_context_rows": count_bool(rows, "station_method_context_present"),
            "station_code_context_rows": count_bool(rows, "station_code_context_present"),
            "station_specific_context_rows": count_bool(rows, "station_specific_context_present"),
            "operating_or_current_context_rows": count_bool(rows, "operating_or_current_context_present"),
            "status_or_certification_context_rows": count_bool(
                rows, "status_or_certification_context_present"
            ),
            "calibration_or_maintenance_context_rows": count_bool(
                rows, "calibration_or_maintenance_context_present"
            ),
            "raw_value_sanity_issue_rows": count_bool(rows, "raw_value_sanity_issue_present"),
            "test_mode_or_blocker_rows": count_bool(rows, "test_mode_or_blocker_present"),
            "stale_or_sentinel_blocker_rows": count_bool(rows, "stale_or_sentinel_blocker_present"),
            "station_method_table_rows": count_bool(rows, "station_method_table_found"),
            "calibration_status_available_rows": count_bool(rows, "calibration_status_available"),
            "current_status_confirmed_rows": count_bool(rows, "current_status_confirmed"),
            "station_method_classified_rows": count_bool(rows, "station_method_classified"),
            "complete_monitor_grade_classification_rows": count_bool(
                rows, "complete_monitor_grade_classification_available"
            ),
            "station_radius_grade_assumption_ready_rows": count_bool(
                rows, "station_radius_grade_assumption_ready"
            ),
        },
        "country_rows": country_rows,
        "decision_counts": decision_counts,
        "evidence_gate_counts": evidence_gate_counts,
        "sample_rows": [
            {
                "iso3": row["iso3"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "decision_lane": row["decision_lane"],
                "row_evidence_lane": row["row_evidence_lane"],
                "raw_value_sanity_issue_present": row["raw_value_sanity_issue_present"],
                "test_mode_or_blocker_present": row["test_mode_or_blocker_present"],
                "source_threads": row["source_threads"],
                "reader_use": row["reader_use"],
            }
            for row in sample_rows
        ],
        "outputs": {
            "csv": "generated\\air-monitoring-station-grade-decision-ledger.csv",
            "summary_json": "generated\\air-monitoring-station-grade-decision-ledger-summary.json",
        },
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    rows, summary = build_rows()
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    print(f"Wrote {len(rows)} station-grade decision rows to {OUT_CSV}")
    print(json.dumps(summary["coverage_counts"], indent=2))


if __name__ == "__main__":
    main()
