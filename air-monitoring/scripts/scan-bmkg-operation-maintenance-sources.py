"""Scan BMKG operation and maintenance sources for the 22 BMKG PM2.5 rows.

The station-method classification audit upgraded 22 exact Indonesia/BMKG rows
to a BAM method class. This pass asks a narrower follow-up question: do public
BMKG operation, daily-inspection, calibration-procedure, or service-tariff
sources close station-level current status, station-specific inspection logs,
station-specific calibration certificates, or complete monitor-grade status?

The script records source-level operation and maintenance context, but keeps
grade/radius gates closed unless public evidence is station-specific.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-operation-maintenance-source-seed.csv"
METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-operation-maintenance-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-operation-maintenance-source-scan-summary.json"

METHOD = "air_monitoring_bmkg_operation_maintenance_source_scan_v1"
STATUS = "computed_bmkg_operation_maintenance_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This scan records public BMKG operation, maintenance, calibration-procedure, "
    "and service-tariff context for the 22 BMKG BAM method-classified rows. It "
    "does not certify station current status, station-specific inspection logs, "
    "station-specific calibration certificates, complete monitor-grade status, "
    "same-station OpenAQ joins, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_operation_maintenance_scan_id",
    "method_classification_audit_id",
    "source_station_id",
    "source_station_name",
    "exact_station_detail_url",
    "exact_station_detail_retrieved",
    "exact_station_detail_timestamp_raw",
    "exact_station_detail_timestamp_iso",
    "exact_station_detail_recent_within_30_days",
    "exact_station_detail_value_raw",
    "exact_station_detail_method_terms",
    "daily_inspection_sop_context",
    "daily_inspection_procedure_context",
    "maintenance_check_context",
    "calibration_procedure_context",
    "calibration_service_tariff_context",
    "regional_bam1020_model_context",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "current_status_confirmed",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "operation_maintenance_decision",
    "reader_use",
    "non_claim",
]


MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "mei": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "agu": 8,
    "sep": 9,
    "oct": 10,
    "okt": 10,
    "nov": 11,
    "dec": 12,
    "des": 12,
}


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
    text = text.replace("\u200b", "")
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


def extract_text(content: bytes, response_text: str, content_type: str, hint: str) -> tuple[str, BeautifulSoup | None]:
    lower = f"{content_type} {hint}".lower()
    if "pdf" in lower or content[:4] == b"%PDF":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages), None
    soup = BeautifulSoup(response_text, "html.parser")
    return soup.get_text(" ", strip=True), soup


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
        text, _ = extract_text(response.content, response.text, result["content_type"], content_type_hint)
        result["text"] = normalize(text)
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def parse_bmkg_timestamp(text: str) -> tuple[str, str]:
    match = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4}),\s+(\d{1,2})\.(\d{2})\s+WIB", text)
    if not match:
        return "", ""
    day, month_raw, year, hour, minute = match.groups()
    month = MONTHS.get(month_raw.casefold())
    if not month:
        return match.group(0), ""
    parsed = datetime(int(year), month, int(day), int(hour), int(minute), tzinfo=timezone(timedelta(hours=7)))
    return match.group(0), parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_bmkg_value(text: str, station_name: str) -> str:
    station = re.escape(normalize(station_name))
    pattern = rf"(\d+(?:[,.]\d+)?)\s*(?:ug/m\^3|µg/m\^3|ug/m3|µg/m3)\s+di\s+{station}"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return match.group(1).replace(",", ".")
    generic = re.search(r"(\d+(?:[,.]\d+)?)\s*(?:ug/m\^3|µg/m\^3|ug/m3|µg/m3)", text, flags=re.IGNORECASE)
    return generic.group(1).replace(",", ".") if generic else ""


def iso_date_recent_within_30_days(value: str, generated_at: str) -> bool:
    if not value:
        return False
    try:
        observed = datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        generated = datetime.fromisoformat(generated_at.replace("Z", "+00:00")).date()
    except ValueError:
        return False
    age = (generated - observed).days
    return 0 <= age <= 30


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(METHOD_CLASSIFICATION_CSV)
    output = [
        row
        for row in rows
        if row["iso3"] == "IDN"
        and boolish(row["station_method_classified"])
        and row["station_method_class"] == "Beta Attenuation Monitoring (BAM)"
    ]
    output.sort(key=lambda row: row["source_station_id"])
    return output


def build_seed_source_rows(seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for seed in seed_rows:
        fetched = fetch_url(seed["url"], seed["content_type_hint"])
        text = fetched["text"]
        expected_terms = split_terms(seed["expected_terms"])
        method_terms = split_terms(seed["method_terms"])
        operation_terms = split_terms(seed["operation_terms"])
        maintenance_terms = split_terms(seed["maintenance_terms"])
        calibration_terms = split_terms(seed["calibration_terms"])
        status_terms = split_terms(seed["status_terms"])
        caution_terms = split_terms(seed["caution_terms"])
        output.append(
            {
                "source_key": seed["source_key"],
                "source_name": seed["source_name"],
                "source_role": seed["source_role"],
                "url": seed["url"],
                "final_url": fetched["final_url"],
                "retrieved": fetched["retrieved"],
                "http_status": fetched["http_status"],
                "content_type": fetched["content_type"],
                "retrieval_bytes": fetched["retrieval_bytes"],
                "sha256": fetched["sha256"],
                "retrieval_error": fetched["retrieval_error"],
                "text": text,
                "expanded_for_station_id": "",
                "expanded_for_station_name": "",
                "matched_expected_terms": matched_terms(text, expected_terms),
                "matched_method_terms": matched_terms(text, method_terms),
                "matched_operation_terms": matched_terms(text, operation_terms),
                "matched_maintenance_terms": matched_terms(text, maintenance_terms),
                "matched_calibration_terms": matched_terms(text, calibration_terms),
                "matched_status_terms": matched_terms(text, status_terms),
                "matched_caution_terms": matched_terms(text, caution_terms),
                "source_note": seed["source_note"],
            }
        )
    return output


def detail_source_for(row: dict[str, str]) -> dict[str, Any]:
    fetched = fetch_url(row["exact_station_detail_url"], "html")
    text = fetched["text"]
    return {
        "source_key": f"bmkg_pm25_detail_{row['source_station_id']}",
        "source_name": f"BMKG PM2.5 station-detail page for {row['source_station_name']}",
        "source_role": "official_station_detail_page",
        "url": row["exact_station_detail_url"],
        "final_url": fetched["final_url"],
        "retrieved": fetched["retrieved"],
        "http_status": fetched["http_status"],
        "content_type": fetched["content_type"],
        "retrieval_bytes": fetched["retrieval_bytes"],
        "sha256": fetched["sha256"],
        "retrieval_error": fetched["retrieval_error"],
        "text": text,
        "expanded_for_station_id": row["source_station_id"],
        "expanded_for_station_name": row["source_station_name"],
        "matched_expected_terms": matched_terms(text, [row["source_station_name"], "PM2.5"]),
        "matched_method_terms": matched_terms(text, ["Beta Attenuation Monitoring", "Beta Attenuation", "sinar beta"]),
        "matched_operation_terms": matched_terms(text, ["Data Terakhir", "WIB", "Konsentrasi PM2.5"]),
        "matched_maintenance_terms": [],
        "matched_calibration_terms": [],
        "matched_status_terms": [],
        "matched_caution_terms": [],
        "source_note": "Exact BMKG station-detail page; use as current public display and method text, not as station-status certification.",
    }


def source_by_key(source_rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for source in source_rows:
        if source["source_key"] == key:
            return source
    return {}


def source_has(source: dict[str, Any], *fields: str) -> bool:
    return bool(source.get("retrieved")) and any(source.get(field) for field in fields)


def build_station_rows(generated_at: str, targets: list[dict[str, str]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    daily_sop = source_by_key(source_rows, "bmkg_bam1020_daily_inspection_sop_2023")
    regulation = source_by_key(source_rows, "bmkg_air_quality_observation_regulation_2019")
    calibration_tariff = source_by_key(source_rows, "bmkg_jateng_pnbp_calibration_tariff")
    sumsel_note = source_by_key(source_rows, "bmkg_sumsel_pm25_bam1020_note")

    output: list[dict[str, Any]] = []
    detail_sources = {source["expanded_for_station_id"]: source for source in source_rows if source["source_role"] == "official_station_detail_page"}
    for row in targets:
        detail = detail_sources.get(row["source_station_id"], {})
        detail_text = detail.get("text", "")
        timestamp_raw, timestamp_iso = parse_bmkg_timestamp(detail_text)
        detail_recent = iso_date_recent_within_30_days(timestamp_iso, generated_at)
        detail_value = parse_bmkg_value(detail_text, row["source_station_name"]) if detail_text else ""
        detail_method_terms = "|".join(detail.get("matched_method_terms", []))

        daily_context = source_has(daily_sop, "matched_expected_terms", "matched_method_terms")
        daily_procedure = source_has(daily_sop, "matched_operation_terms")
        maintenance_context = source_has(daily_sop, "matched_maintenance_terms")
        calibration_procedure = source_has(regulation, "matched_calibration_terms")
        calibration_service = source_has(calibration_tariff, "matched_calibration_terms")
        regional_model = source_has(sumsel_note, "matched_method_terms")

        if detail.get("retrieved") and daily_context and (calibration_procedure or calibration_service):
            decision = "bmkg_operation_and_calibration_context_keep_not_status_certified"
            reader_use = (
                "Use as source-level BMKG operation and calibration-context evidence for BAM rows. "
                "The evidence still does not provide a station-specific inspection log, calibration "
                "certificate, public current-status certification, or complete grade basis."
            )
        elif detail.get("retrieved"):
            decision = "bmkg_station_detail_only_keep_not_status_certified"
            reader_use = (
                "The exact station detail page is visible, but source-level operation or calibration "
                "context did not retrieve cleanly enough to close any grade/status gate."
            )
        else:
            decision = "bmkg_station_detail_retrieval_gap_keep_open"
            reader_use = (
                "The exact station detail page did not retrieve in this pass, so the row remains open "
                "for source follow-up."
            )

        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "bmkg_operation_maintenance_scan_id": f"IDN-bmkg-operation-maintenance-{row['source_station_id']}",
                "method_classification_audit_id": row["method_classification_audit_id"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "exact_station_detail_url": row["exact_station_detail_url"],
                "exact_station_detail_retrieved": bool(detail.get("retrieved")),
                "exact_station_detail_timestamp_raw": timestamp_raw,
                "exact_station_detail_timestamp_iso": timestamp_iso,
                "exact_station_detail_recent_within_30_days": detail_recent,
                "exact_station_detail_value_raw": detail_value,
                "exact_station_detail_method_terms": detail_method_terms,
                "daily_inspection_sop_context": daily_context,
                "daily_inspection_procedure_context": daily_procedure,
                "maintenance_check_context": maintenance_context,
                "calibration_procedure_context": calibration_procedure,
                "calibration_service_tariff_context": calibration_service,
                "regional_bam1020_model_context": regional_model,
                "station_specific_inspection_log_found": False,
                "station_specific_calibration_certificate_found": False,
                "current_status_confirmed": False,
                "calibration_status_available": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "operation_maintenance_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def source_record_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = [
        "source_key",
        "source_name",
        "source_role",
        "url",
        "final_url",
        "retrieved",
        "http_status",
        "content_type",
        "retrieval_bytes",
        "sha256",
        "expanded_for_station_id",
        "expanded_for_station_name",
        "matched_expected_terms",
        "matched_method_terms",
        "matched_operation_terms",
        "matched_maintenance_terms",
        "matched_calibration_terms",
        "matched_status_terms",
        "matched_caution_terms",
        "retrieval_error",
        "source_note",
    ]
    return [{field: row.get(field, "") for field in fields} for row in source_rows]


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def evidence_gates(rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        gate(
            "available" if all(row["retrieved"] for row in source_rows) else "limited",
            "Public BMKG sources retrieved",
            sum(row["retrieved"] for row in source_rows),
            "Includes exact station detail pages plus source-level SOP, regulation, tariff, and instrument-note pages.",
        ),
        gate(
            "available",
            "Exact BMKG station pages still visible",
            sum(row["exact_station_detail_retrieved"] for row in rows),
            "Exact station-detail pages remain public source rows for the 22 BMKG targets.",
        ),
        gate(
            "available",
            "Recent public measurement display",
            sum(row["exact_station_detail_recent_within_30_days"] for row in rows),
            "Recent display is evidence of public measurement visibility, not station-status certification.",
        ),
        gate(
            "partly_available",
            "Daily inspection SOP context",
            sum(row["daily_inspection_sop_context"] for row in rows),
            "The BMKG SOP describes daily BAM-1020 checks in the BMKG environment.",
        ),
        gate(
            "partly_available",
            "Maintenance/check context",
            sum(row["maintenance_check_context"] for row in rows),
            "Maintenance and daily-check terms support source-level operation context only.",
        ),
        gate(
            "partly_available",
            "Calibration procedure or service context",
            sum(row["calibration_procedure_context"] or row["calibration_service_tariff_context"] for row in rows),
            "Public BMKG materials mention calibration procedure or BAM calibration service context, not row-level certificates.",
        ),
        gate(
            "not_ready",
            "Station-specific inspection log",
            0,
            "No public source gives the target station's inspection log.",
        ),
        gate(
            "not_ready",
            "Station-specific calibration certificate/status",
            0,
            "No public source gives a calibration certificate or calibration-status record for a target row.",
        ),
        gate(
            "not_ready",
            "Complete monitor-grade and radius closure",
            0,
            "Current-status, calibration-status, complete grade, and station-radius readiness remain blocked.",
        ),
    ]


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> dict[str, Any]:
    context_sources = [source for source in source_rows if source["source_role"] != "official_station_detail_page"]
    detail_sources = [source for source in source_rows if source["source_role"] == "official_station_detail_page"]
    counts = {
        "target_bmkg_rows": len(rows),
        "context_source_records": len(context_sources),
        "context_source_records_retrieved": sum(source["retrieved"] for source in context_sources),
        "exact_station_detail_records": len(detail_sources),
        "exact_station_detail_records_retrieved": sum(source["retrieved"] for source in detail_sources),
        "exact_station_detail_recent_within_30_days_rows": sum(row["exact_station_detail_recent_within_30_days"] for row in rows),
        "daily_inspection_sop_context_rows": sum(row["daily_inspection_sop_context"] for row in rows),
        "daily_inspection_procedure_context_rows": sum(row["daily_inspection_procedure_context"] for row in rows),
        "maintenance_check_context_rows": sum(row["maintenance_check_context"] for row in rows),
        "calibration_procedure_context_rows": sum(row["calibration_procedure_context"] for row in rows),
        "calibration_service_tariff_context_rows": sum(row["calibration_service_tariff_context"] for row in rows),
        "regional_bam1020_model_context_rows": sum(row["regional_bam1020_model_context"] for row in rows),
        "station_specific_inspection_log_rows": 0,
        "station_specific_calibration_certificate_rows": 0,
        "current_status_confirmed_rows": 0,
        "calibration_status_available_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    sample_fields = [
        "source_station_id",
        "source_station_name",
        "exact_station_detail_timestamp_raw",
        "exact_station_detail_value_raw",
        "daily_inspection_sop_context",
        "maintenance_check_context",
        "calibration_procedure_context",
        "calibration_service_tariff_context",
        "operation_maintenance_decision",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG operation/maintenance source scan",
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "public BMKG operation, maintenance, calibration, and model-context source seed",
            },
            {
                "path": str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)),
                "role": "22 BMKG rows method-classified as BAM in the station-method classification audit",
            },
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": key, "rows": value}
            for key, value in sorted(Counter(row["operation_maintenance_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gates(rows, source_rows),
        "station_sample_rows": [{field: row[field] for field in sample_fields} for row in rows[:12]],
        "source_records": source_record_rows(source_rows),
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    targets = target_rows()
    seed_rows = read_csv(SEED_CSV)
    seed_sources = build_seed_source_rows(seed_rows)
    detail_sources = [detail_source_for(row) for row in targets]
    source_rows = [*seed_sources, *detail_sources]
    rows = build_station_rows(generated_at, targets, source_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, source_rows))
    print(
        "Built BMKG operation/maintenance source scan: "
        f"{len(rows)} BMKG rows; "
        f"{sum(source['retrieved'] for source in source_rows)}/{len(source_rows)} source records retrieved; "
        f"{sum(row['daily_inspection_sop_context'] for row in rows)} daily-SOP context rows; "
        "0 station-specific calibration/status rows; "
        f"decisions={dict(Counter(row['operation_maintenance_decision'] for row in rows))}."
    )


if __name__ == "__main__":
    main()
