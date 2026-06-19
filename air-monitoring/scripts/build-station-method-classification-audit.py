"""Build a strict station-method classification audit for exact PM2.5 rows.

This pass follows the station-grade decision ledger. It checks whether public
method sources now support a station-level method class without converting that
method class into complete monitor-grade, current-status, or radius readiness.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "station-method-classification-source-seed.csv"
LEDGER_CSV = GENERATED_DIR / "air-monitoring-station-grade-decision-ledger.csv"
ROW_METHOD_CSV = GENERATED_DIR / "air-monitoring-indonesia-georgia-row-method-source-scan.csv"
STATION_CODE_CSV = GENERATED_DIR / "air-monitoring-station-code-status-method-source-scan.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-method-classification-audit-summary.json"

METHOD = "air_monitoring_station_method_classification_audit_v1"
STATUS = "computed_station_method_classification_audit"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This audit classifies public method evidence for exact station rows. It "
    "does not certify current station status, complete monitor-grade status, "
    "same-station OpenAQ joins, calibration status, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "method_classification_audit_id",
    "decision_ledger_id",
    "iso3",
    "country",
    "source_station_id",
    "source_station_name",
    "decision_lane",
    "row_evidence_lane",
    "exact_station_detail_url",
    "exact_station_detail_recent_within_30_days",
    "exact_station_detail_method_terms",
    "bmkg_regulation_bam_method_context",
    "bmkg_regulation_calibration_context",
    "bmkg_bam1020_source_level_model_context",
    "georgia_network_instrument_catalog_context",
    "georgia_live_data_unverified_caution",
    "uzbekistan_instrument_hint_context",
    "raw_value_or_blocker_caution",
    "station_method_class",
    "station_method_classified",
    "instrument_model_candidate",
    "instrument_model_station_specific",
    "current_measurement_recent",
    "current_status_confirmed",
    "calibration_or_maintenance_context_present",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "audit_decision",
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


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ")
    text = text.replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("`", "'")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def boolish(value: Any) -> bool:
    return norm_key(value) in {"true", "1", "yes"}


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def extract_text(content: bytes, response_text: str, content_type: str, hint: str) -> tuple[str, str]:
    lower = f"{content_type} {hint}".lower()
    if "pdf" in lower or content[:4] == b"%PDF":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages), "pdf"
    soup = BeautifulSoup(response_text, "html.parser")
    return soup.get_text(" ", strip=True), "html"


def fetch_url(url: str, content_type_hint: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "url": url,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "content_kind": "",
        "retrieval_error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,text/plain,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
            timeout=TIMEOUT_SECONDS,
            allow_redirects=True,
        )
        result["final_url"] = response.url
        result["http_status"] = response.status_code
        result["content_type"] = response.headers.get("content-type", "")
        result["retrieval_bytes"] = len(response.content)
        result["sha256"] = hashlib.sha256(response.content).hexdigest()
        response.raise_for_status()
        text, kind = extract_text(response.content, response.text, result["content_type"], content_type_hint)
        result["text"] = normalize(text)
        result["content_kind"] = kind
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - source retrieval failure is evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def fetch_source_records(seed_rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for seed in seed_rows:
        fetched = fetch_url(seed["url"], seed["content_type_hint"])
        text = fetched["text"]
        output[seed["source_key"]] = {
            **fetched,
            "source_key": seed["source_key"],
            "source_name": seed["source_name"],
            "source_role": seed["source_role"],
            "iso3": seed["iso3"],
            "country": seed["country"],
            "matched_expected_terms": matched_terms(text, split_terms(seed["expected_terms"])),
            "matched_method_terms": matched_terms(text, split_terms(seed["method_terms"])),
            "matched_current_terms": matched_terms(text, split_terms(seed["current_terms"])),
            "matched_calibration_terms": matched_terms(text, split_terms(seed["calibration_terms"])),
            "matched_caution_terms": matched_terms(text, split_terms(seed["caution_terms"])),
            "source_note": seed["source_note"],
        }
    return output


def indexed(rows: list[dict[str, str]], key: str = "source_station_id") -> dict[str, dict[str, str]]:
    return {normalize(row.get(key)): row for row in rows if normalize(row.get(key))}


def has_terms(source_records: dict[str, dict[str, Any]], source_key: str, term_field: str) -> bool:
    record = source_records.get(source_key, {})
    return bool(record.get("retrieved") and record.get(term_field))


def source_record_rows(source_records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    fields = [
        "source_key",
        "source_name",
        "source_role",
        "iso3",
        "country",
        "url",
        "final_url",
        "retrieved",
        "http_status",
        "content_type",
        "content_kind",
        "retrieval_bytes",
        "sha256",
        "matched_expected_terms",
        "matched_method_terms",
        "matched_current_terms",
        "matched_calibration_terms",
        "matched_caution_terms",
        "retrieval_error",
        "source_note",
    ]
    return [{field: row.get(field, "") for field in fields} for row in source_records.values()]


def row_decision(
    row: dict[str, str],
    method_row: dict[str, str],
    station_code_row: dict[str, str],
    source_records: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], str, str]:
    iso3 = row["iso3"]
    bmkg_regulation_method = has_terms(source_records, "bmkg_air_quality_observation_regulation_2019", "matched_method_terms")
    bmkg_regulation_calibration = has_terms(source_records, "bmkg_air_quality_observation_regulation_2019", "matched_calibration_terms")
    bmkg_model_context = has_terms(source_records, "bmkg_sumsel_pm25_bam1020_note", "matched_method_terms")
    georgia_catalog = has_terms(source_records, "airgov_monitoring_network_catalog", "matched_method_terms")
    georgia_unverified = has_terms(source_records, "airgov_air_quality_index_method_note", "matched_caution_terms")
    raw_or_blocker = boolish(row["raw_value_sanity_issue_present"]) or boolish(row["test_mode_or_blocker_present"]) or boolish(row["stale_or_sentinel_blocker_present"])

    base = {
        "bmkg_regulation_bam_method_context": False,
        "bmkg_regulation_calibration_context": False,
        "bmkg_bam1020_source_level_model_context": False,
        "georgia_network_instrument_catalog_context": False,
        "georgia_live_data_unverified_caution": False,
        "uzbekistan_instrument_hint_context": boolish(row["row_level_instrument_hint"]),
        "raw_value_or_blocker_caution": raw_or_blocker,
        "station_method_class": "",
        "station_method_classified": False,
        "instrument_model_candidate": "",
        "instrument_model_station_specific": False,
        "current_measurement_recent": False,
        "current_status_confirmed": False,
        "calibration_or_maintenance_context_present": boolish(row["calibration_or_maintenance_context_present"]),
        "calibration_status_available": False,
        "complete_monitor_grade_classification_available": False,
        "station_radius_grade_assumption_ready": False,
    }

    if iso3 == "IDN":
        same_page_method = boolish(method_row.get("same_page_method_context_candidate"))
        recent_detail = boolish(method_row.get("exact_station_detail_recent_within_30_days"))
        if same_page_method and bmkg_regulation_method:
            base.update(
                {
                    "bmkg_regulation_bam_method_context": True,
                    "bmkg_regulation_calibration_context": bmkg_regulation_calibration,
                    "bmkg_bam1020_source_level_model_context": bmkg_model_context,
                    "station_method_class": "Beta Attenuation Monitoring (BAM)",
                    "station_method_classified": True,
                    "instrument_model_candidate": "BAM-1020 source-level context" if bmkg_model_context else "",
                    "current_measurement_recent": recent_detail,
                }
            )
            return (
                base,
                "indonesia_exact_detail_plus_bmkg_regulation_method_classified",
                "Use as a method-class upgrade for BMKG rows. The exact station detail page carries Beta Attenuation language and the official BMKG regulation states PM2.5 automatic observations use BAM. It still is not grade or status certification.",
            )
        return (
            base,
            "indonesia_method_context_incomplete_keep_open",
            "Keep open: either the exact detail page or the official method regulation was not sufficient for method classification.",
        )

    if iso3 == "GEO":
        has_hourly_pm25_observation = int(station_code_row.get("pm25_observation_rows") or 0) > 0 and bool(
            station_code_row.get("pm25_latest_timestamp")
        )
        base.update(
            {
                "georgia_network_instrument_catalog_context": georgia_catalog,
                "georgia_live_data_unverified_caution": georgia_unverified,
                "current_measurement_recent": has_hourly_pm25_observation,
            }
        )
        if georgia_catalog:
            return (
                base,
                "georgia_source_level_instrument_catalog_keep_not_station_classified",
                "Use as source-level method context only. Georgia publishes an instrument catalog and exact station-code PM2.5 rows, but not a station-code method table; the portal also warns live automatic-station data are not verified.",
            )
        return (
            base,
            "georgia_method_catalog_not_found_keep_open",
            "Keep open: the source-level Georgia instrument catalog was not retrieved or did not match method terms.",
        )

    if iso3 == "UZB":
        return (
            base,
            "uzbekistan_instrument_hint_or_blocker_keep_not_method_classified",
            "Use as carried-forward context only. Uzbekistan rows may carry station-level instrument hints, but blockers, current-status gaps, and certification gaps keep method classification and grade closure unavailable.",
        )

    return base, "unsupported_country_keep_open", "Keep open: this audit only handles Indonesia, Georgia, and Uzbekistan exact-row lanes."


def build_rows(generated_at: str, source_records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    ledger_rows = read_csv(LEDGER_CSV)
    method_rows = indexed(read_csv(ROW_METHOD_CSV))
    station_code_rows = indexed(read_csv(STATION_CODE_CSV))
    output: list[dict[str, Any]] = []
    for row in ledger_rows:
        method_row = method_rows.get(row["source_station_id"], {})
        station_code_row = station_code_rows.get(row["source_station_id"], {})
        evidence, decision, reader_use = row_decision(row, method_row, station_code_row, source_records)
        exact_url = method_row.get("exact_station_detail_url", "")
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "method_classification_audit_id": f"{row['iso3']}-method-classification-{row['source_station_id']}",
                "decision_ledger_id": row["decision_ledger_id"],
                "iso3": row["iso3"],
                "country": row["country"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "decision_lane": row["decision_lane"],
                "row_evidence_lane": row["row_evidence_lane"],
                "exact_station_detail_url": exact_url,
                "exact_station_detail_recent_within_30_days": boolish(method_row.get("exact_station_detail_recent_within_30_days")),
                "exact_station_detail_method_terms": method_row.get("exact_station_detail_method_terms", ""),
                "calibration_or_maintenance_context_present": boolish(row["calibration_or_maintenance_context_present"]),
                "current_measurement_recent": boolish(method_row.get("exact_station_detail_recent_within_30_days")) or boolish(station_code_row.get("pm25_row_or_equipment_listed")),
                "audit_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
                **evidence,
            }
        )
    return output


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        subset = [row for row in rows if row["iso3"] == iso3]
        output.append(
            {
                "iso3": iso3,
                "country": subset[0]["country"],
                "target_rows": len(subset),
                "method_classified_rows": sum(row["station_method_classified"] for row in subset),
                "current_measurement_recent_rows": sum(row["current_measurement_recent"] for row in subset),
                "source_level_instrument_catalog_rows": sum(row["georgia_network_instrument_catalog_context"] or row["bmkg_bam1020_source_level_model_context"] for row in subset),
                "unverified_or_blocker_caution_rows": sum(row["georgia_live_data_unverified_caution"] or row["raw_value_or_blocker_caution"] for row in subset),
                "current_status_confirmed_rows": 0,
                "calibration_status_available_rows": 0,
                "complete_monitor_grade_classification_rows": 0,
                "station_radius_grade_assumption_ready_rows": 0,
            }
        )
    return output


def evidence_gates(rows: list[dict[str, Any]], source_records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    retrieved = sum(row["retrieved"] for row in source_records.values())
    return [
        gate(
            "available" if retrieved == len(source_records) else "limited",
            "Method-classification sources retrieved",
            retrieved,
            "Official method and catalog sources were retrieved or the retrieval failure is recorded with URL and error.",
        ),
        gate(
            "partly_available",
            "BMKG exact rows with station method classified",
            sum(row["iso3"] == "IDN" and row["station_method_classified"] for row in rows),
            "Exact BMKG detail pages plus the official regulation support a BAM method class for Indonesia target rows.",
        ),
        gate(
            "partly_available",
            "Current measurement observed recently",
            sum(row["current_measurement_recent"] for row in rows),
            "A recent public station display or hourly PM2.5 observation is visibility evidence, not station-status certification.",
        ),
        gate(
            "caution",
            "Georgia live-data verification caution",
            sum(row["georgia_live_data_unverified_caution"] for row in rows),
            "Georgia's portal says automatic-station data shown live are not verified; this blocks grade closure.",
        ),
        gate(
            "caution",
            "Raw-value or blocker caution",
            sum(row["raw_value_or_blocker_caution"] for row in rows),
            "Rows with test-mode, stale, sentinel, negative, or other raw-value cautions must stay outside grade/radius assumptions.",
        ),
        gate("not_ready", "Current-status confirmed", 0, "No row has public station-status certification."),
        gate("not_ready", "Calibration/status available", 0, "Calibration procedure context is not row-level calibration status."),
        gate("not_ready", "Complete monitor-grade classification", 0, "No row has complete public station-grade classification."),
        gate("not_ready", "Station-radius grade assumptions", 0, "Station-radius coverage remains blocked until status and complete grade are public and row-level."),
    ]


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_rows": len(rows),
        "target_indonesia_rows": sum(row["iso3"] == "IDN" for row in rows),
        "target_georgia_rows": sum(row["iso3"] == "GEO" for row in rows),
        "target_uzbekistan_rows": sum(row["iso3"] == "UZB" for row in rows),
        "source_records_total": len(source_records),
        "source_records_retrieved": sum(row["retrieved"] for row in source_records.values()),
        "bmkg_method_classified_rows": sum(row["iso3"] == "IDN" and row["station_method_classified"] for row in rows),
        "bmkg_recent_exact_detail_rows": sum(row["iso3"] == "IDN" and row["exact_station_detail_recent_within_30_days"] for row in rows),
        "bmkg_regulation_calibration_context_rows": sum(row["iso3"] == "IDN" and row["bmkg_regulation_calibration_context"] for row in rows),
        "bmkg_bam1020_source_level_model_context_rows": sum(row["iso3"] == "IDN" and row["bmkg_bam1020_source_level_model_context"] for row in rows),
        "georgia_source_level_catalog_rows": sum(row["iso3"] == "GEO" and row["georgia_network_instrument_catalog_context"] for row in rows),
        "georgia_live_data_unverified_caution_rows": sum(row["iso3"] == "GEO" and row["georgia_live_data_unverified_caution"] for row in rows),
        "uzbekistan_instrument_hint_rows": sum(row["iso3"] == "UZB" and row["uzbekistan_instrument_hint_context"] for row in rows),
        "raw_value_or_blocker_caution_rows": sum(row["raw_value_or_blocker_caution"] for row in rows),
        "current_measurement_recent_rows": sum(row["current_measurement_recent"] for row in rows),
        "current_status_confirmed_rows": 0,
        "calibration_status_available_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    sample_fields = [
        "iso3",
        "source_station_id",
        "source_station_name",
        "station_method_class",
        "station_method_classified",
        "current_measurement_recent",
        "raw_value_or_blocker_caution",
        "audit_decision",
    ]
    sample_rows = [
        *[row for row in rows if row["iso3"] == "IDN"][:6],
        *[row for row in rows if row["iso3"] == "GEO"][:6],
        *[row for row in rows if row["iso3"] == "UZB"][:4],
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-method classification audit",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "public method/catalog source seed for this audit"},
            {"path": str(LEDGER_CSV.relative_to(PROGRAM_DIR)), "role": "66-row station-grade decision ledger"},
            {"path": str(ROW_METHOD_CSV.relative_to(PROGRAM_DIR)), "role": "exact BMKG station-detail method evidence"},
            {"path": str(STATION_CODE_CSV.relative_to(PROGRAM_DIR)), "role": "Georgia station-code and Uzbekistan blocker context"},
        ],
        "coverage_counts": counts,
        "country_rows": country_rows(rows),
        "decision_counts": [
            {"decision": key, "rows": value}
            for key, value in sorted(Counter(row["audit_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gates(rows, source_records),
        "source_records": source_record_rows(source_records),
        "station_sample_rows": [{field: row[field] for field in sample_fields} for row in sample_rows],
        "outputs": {"csv": str(OUT_CSV.relative_to(PROGRAM_DIR)), "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR))},
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    source_records = fetch_source_records(read_csv(SEED_CSV))
    rows = build_rows(generated_at, source_records)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, source_records))
    counts = Counter(row["audit_decision"] for row in rows)
    print(
        "Built station-method classification audit: "
        f"{len(rows)} rows; "
        f"{sum(row['station_method_classified'] for row in rows)} method-classified rows; "
        "0 complete grade rows; "
        f"decisions={dict(counts)}."
    )


if __name__ == "__main__":
    main()
