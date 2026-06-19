"""Scan Georgia air.gov.ge report pages for verified station-code evidence.

The station-method classification audit kept Georgia at source-level catalog
context because the live air.gov.ge data are not verified. The air.gov.ge
method note says verified data are available in reports, so this pass checks
the official monthly report route for the 16 target station codes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "georgia-report-verification-source-seed.csv"
METHOD_CLASSIFICATION_CSV = GENERATED_DIR / "air-monitoring-station-method-classification-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-georgia-report-verification-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-georgia-report-verification-source-scan-summary.json"

METHOD = "air_monitoring_georgia_report_verification_source_scan_v1"
STATUS = "computed_georgia_report_verification_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
REPORT_MONTH = "2026-05"
NON_CLAIM = (
    "This scan checks whether official air.gov.ge report pages provide verified "
    "station-code PM2.5 evidence for the 16 Georgia target rows. It does not "
    "certify station method, current status, complete monitor-grade status, "
    "same-station OpenAQ joins, or station-radius coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "georgia_report_verification_scan_id",
    "method_classification_audit_id",
    "source_station_id",
    "source_station_name",
    "report_month",
    "monthly_report_url",
    "monthly_report_retrieved",
    "station_code_in_monthly_report",
    "station_name_or_alias_in_monthly_report",
    "pm25_column_in_monthly_report",
    "monthly_report_not_verified_label_present",
    "monthly_report_verified_label_without_not_verified",
    "aqi_note_live_data_unverified_caution",
    "aqi_note_verified_reports_claim",
    "network_catalog_instrument_context",
    "current_measurement_recent_from_prior_audit",
    "verified_report_closure_available",
    "station_method_classified",
    "current_status_confirmed",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "report_verification_decision",
    "reader_use",
    "non_claim",
]


ALIASES = {
    "01005": ["Tazakendi"],
    "AGMS": ["Agmashenebeli"],
    "BTUM": ["Abuseridze"],
    "KUTS": ["Asatiani"],
    "KZBG": ["Kazbegi"],
    "ORN01": ["Gelovani"],
    "ORN02": ["Friendship"],
    "ORN03": ["Central Park", "6 May Park"],
    "ORN04": ["Ninoshvili"],
    "ORN05": ["Zugdidi"],
    "ORN06": ["Mestia"],
    "ORN07": ["Telavi"],
    "ORN08": ["Akhaltsikhe"],
    "RST18": ["Batumi Street"],
    "TSRT": ["Tsereteli"],
    "VRKT": ["Varketili"],
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
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
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
                "Accept": "text/html,text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        soup = BeautifulSoup(response.text, "html.parser")
        result["text"] = normalize(soup.get_text(" ", strip=True))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(METHOD_CLASSIFICATION_CSV)
    output = [row for row in rows if row["iso3"] == "GEO"]
    output.sort(key=lambda row: row["source_station_id"])
    return output


def build_source_rows(seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for seed in seed_rows:
        fetched = fetch_url(seed["url"], seed["content_type_hint"])
        text = fetched["text"]
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
                "matched_expected_terms": matched_terms(text, split_terms(seed["expected_terms"])),
                "matched_pm25_terms": matched_terms(text, split_terms(seed["pm25_terms"])),
                "matched_verification_terms": matched_terms(text, split_terms(seed["verification_terms"])),
                "matched_caution_terms": matched_terms(text, split_terms(seed["caution_terms"])),
                "source_note": seed["source_note"],
            }
        )
    return output


def source_by_key(source_rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for source in source_rows:
        if source["source_key"] == key:
            return source
    return {}


def station_name_or_alias_present(row: dict[str, str], text: str) -> bool:
    lower = norm_key(text)
    candidates = [row["source_station_name"], *ALIASES.get(row["source_station_id"], [])]
    return any(norm_key(candidate) in lower for candidate in candidates if candidate)


def verified_label_without_not_verified(text: str) -> bool:
    lower = norm_key(text)
    return "verified data" in lower and "not verified data" not in lower


def build_station_rows(generated_at: str, targets: list[dict[str, str]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    report = source_by_key(source_rows, "airgov_monthly_report_2026_05_all_targets")
    aqi_note = source_by_key(source_rows, "airgov_air_quality_index_method_note")
    network = source_by_key(source_rows, "airgov_monitoring_network_catalog")
    report_text = report.get("text", "")
    aqi_text = aqi_note.get("text", "")
    network_context = bool(network.get("retrieved") and network.get("matched_pm25_terms"))
    report_not_verified = "not verified data" in norm_key(report_text)
    report_verified = verified_label_without_not_verified(report_text)
    aqi_live_unverified = bool(aqi_note.get("retrieved") and "not verified" in norm_key(aqi_text))
    aqi_verified_reports = bool(aqi_note.get("retrieved") and "verified data is available in the reports" in norm_key(aqi_text))

    output: list[dict[str, Any]] = []
    for row in targets:
        code_present = row["source_station_id"] in report_text
        alias_present = station_name_or_alias_present(row, report_text)
        pm25_present = "PM2.5" in report_text and code_present
        if code_present and pm25_present and report_not_verified:
            decision = "monthly_report_pm25_present_but_not_verified_keep_open"
            reader_use = (
                "The official monthly report page exposes the target station code and PM2.5 columns, "
                "but the same page carries a Not Verified Data label. Keep the row out of verified "
                "grade/status closure."
            )
        elif code_present and pm25_present and report_verified:
            decision = "monthly_report_pm25_verified_label_needs_station_method_status"
            reader_use = (
                "The report page appears to carry a verified-data label for the station code and PM2.5, "
                "but station method/current-status/grade evidence still must be checked separately."
            )
        elif code_present:
            decision = "monthly_report_station_code_without_pm25_closure_keep_open"
            reader_use = "The report page names the station code, but PM2.5 or verification closure is incomplete."
        else:
            decision = "monthly_report_station_code_not_found_keep_open"
            reader_use = "The report page did not expose this station code in the fetched text."

        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "georgia_report_verification_scan_id": f"GEO-report-verification-{row['source_station_id']}",
                "method_classification_audit_id": row["method_classification_audit_id"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "report_month": REPORT_MONTH,
                "monthly_report_url": report.get("url", ""),
                "monthly_report_retrieved": bool(report.get("retrieved")),
                "station_code_in_monthly_report": code_present,
                "station_name_or_alias_in_monthly_report": alias_present,
                "pm25_column_in_monthly_report": pm25_present,
                "monthly_report_not_verified_label_present": report_not_verified,
                "monthly_report_verified_label_without_not_verified": report_verified,
                "aqi_note_live_data_unverified_caution": aqi_live_unverified,
                "aqi_note_verified_reports_claim": aqi_verified_reports,
                "network_catalog_instrument_context": network_context,
                "current_measurement_recent_from_prior_audit": boolish(row["current_measurement_recent"]),
                "verified_report_closure_available": False,
                "station_method_classified": False,
                "current_status_confirmed": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "report_verification_decision": decision,
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
        "matched_expected_terms",
        "matched_pm25_terms",
        "matched_verification_terms",
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
            "available" if all(source["retrieved"] for source in source_rows) else "limited",
            "Official Georgia report/method sources retrieved",
            sum(source["retrieved"] for source in source_rows),
            "The scan retrieved the report page, AQI method note, and monitoring-network catalog.",
        ),
        gate(
            "available",
            "Station code appears in monthly report",
            sum(row["station_code_in_monthly_report"] for row in rows),
            "The official report route exposes exact station codes for the target rows.",
        ),
        gate(
            "available",
            "PM2.5 column appears in monthly report",
            sum(row["pm25_column_in_monthly_report"] for row in rows),
            "The report table includes PM2.5 columns for the target station-code rows.",
        ),
        gate(
            "caution",
            "Monthly report carries Not Verified Data label",
            sum(row["monthly_report_not_verified_label_present"] for row in rows),
            "The report route still carries a not-verified label in the fetched page.",
        ),
        gate(
            "partly_available",
            "AQI note distinguishes live data and reports",
            sum(row["aqi_note_verified_reports_claim"] for row in rows),
            "The AQI note says live automatic-station data are not verified and verified data are available in reports.",
        ),
        gate(
            "partly_available",
            "Network instrument catalog context",
            sum(row["network_catalog_instrument_context"] for row in rows),
            "The network catalog gives source-level instrument context, not station-specific method/status closure.",
        ),
        gate(
            "not_ready",
            "Verified report closure",
            0,
            "No target row is promoted because the fetched report page carries a not-verified label.",
        ),
        gate(
            "not_ready",
            "Station method/status/grade closure",
            0,
            "No station-code method table, current-status certificate, or complete monitor-grade row was found.",
        ),
        gate(
            "not_ready",
            "Station-radius grade assumptions",
            0,
            "Catchment/radius analysis remains blocked until method/status/grade evidence closes.",
        ),
    ]


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_georgia_rows": len(rows),
        "source_records": len(source_rows),
        "source_records_retrieved": sum(source["retrieved"] for source in source_rows),
        "station_code_in_monthly_report_rows": sum(row["station_code_in_monthly_report"] for row in rows),
        "station_name_or_alias_in_monthly_report_rows": sum(row["station_name_or_alias_in_monthly_report"] for row in rows),
        "pm25_column_in_monthly_report_rows": sum(row["pm25_column_in_monthly_report"] for row in rows),
        "monthly_report_not_verified_label_rows": sum(row["monthly_report_not_verified_label_present"] for row in rows),
        "monthly_report_verified_label_without_not_verified_rows": sum(row["monthly_report_verified_label_without_not_verified"] for row in rows),
        "aqi_note_live_data_unverified_caution_rows": sum(row["aqi_note_live_data_unverified_caution"] for row in rows),
        "aqi_note_verified_reports_claim_rows": sum(row["aqi_note_verified_reports_claim"] for row in rows),
        "network_catalog_instrument_context_rows": sum(row["network_catalog_instrument_context"] for row in rows),
        "current_measurement_recent_from_prior_audit_rows": sum(row["current_measurement_recent_from_prior_audit"] for row in rows),
        "verified_report_closure_available_rows": 0,
        "station_method_classified_rows": 0,
        "current_status_confirmed_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    sample_fields = [
        "source_station_id",
        "source_station_name",
        "station_code_in_monthly_report",
        "pm25_column_in_monthly_report",
        "monthly_report_not_verified_label_present",
        "report_verification_decision",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Georgia report verification source scan",
        "report_month": REPORT_MONTH,
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "public Georgia report, AQI method-note, and monitoring-network source seed",
            },
            {
                "path": str(METHOD_CLASSIFICATION_CSV.relative_to(PROGRAM_DIR)),
                "role": "16 Georgia rows from the station-method classification audit",
            },
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": key, "rows": value}
            for key, value in sorted(Counter(row["report_verification_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gates(rows, source_rows),
        "station_sample_rows": [{field: row[field] for field in sample_fields} for row in rows],
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
    source_rows = build_source_rows(read_csv(SEED_CSV))
    rows = build_station_rows(generated_at, targets, source_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, source_rows))
    print(
        "Built Georgia report verification scan: "
        f"{len(rows)} Georgia rows; "
        f"{sum(source['retrieved'] for source in source_rows)}/{len(source_rows)} sources retrieved; "
        f"{sum(row['station_code_in_monthly_report'] for row in rows)} station-code report rows; "
        f"{sum(row['monthly_report_not_verified_label_present'] for row in rows)} not-verified caution rows; "
        "0 verified closure rows; "
        f"decisions={dict(Counter(row['report_verification_decision'] for row in rows))}."
    )


if __name__ == "__main__":
    main()
