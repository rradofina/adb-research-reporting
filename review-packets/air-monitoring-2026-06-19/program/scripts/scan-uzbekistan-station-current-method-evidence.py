"""Scan Uzbekistan target station rows for current API and method evidence.

This networked scan follows the 28 Uzbekistan rows from the exact-row
method-evidence audit. It joins them back to the public Uzhydromet maps API by
station ID, records whether each station is still present, whether it carries a
station-level HORIBA marker, how old the API reading date is, and whether the
raw PM2.5 value is usable as a sanity signal.

The scan deliberately does not promote rows to current-status confirmed,
station-method classified, complete monitor-grade, or station-radius-ready
without explicit station-level status and grade documentation.
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


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

INPUT_CSV = GENERATED_DIR / "air-monitoring-monitor-grade-station-method-evidence.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-current-method-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-station-current-method-scan-summary.json"

METHOD = "air_monitoring_uzbekistan_station_current_method_scan_v1"
STATUS = "computed_uzbekistan_station_current_method_scan"
API_URL = "https://monitoring.meteo.uz/api/maps"
MAP_URL = "https://monitoring.meteo.uz/en/map"
USER_AGENT = "ADB-Research-Factory/1.0 uzbekistan-station-current-method-scan"
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This scan checks public Uzhydromet API station rows for station presence, "
    "HORIBA markers, reading-date age, and raw-value sanity. It does not "
    "certify current operating status, reference-grade method, monitor-grade "
    "classification, or station-radius coverage readiness."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "method_evidence_id",
    "iso3",
    "country",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "api_station_found",
    "api_station_name",
    "api_alias",
    "api_region_id",
    "api_station_category",
    "api_is_horiba",
    "api_si",
    "api_station_level_horiba_marker",
    "api_method_marker_terms",
    "api_reading_date_raw",
    "api_reading_date_iso",
    "api_reading_age_days",
    "api_reading_age_lane",
    "api_reading_within_7_days",
    "api_reading_within_30_days",
    "api_reading_within_90_days",
    "api_pm25_value_raw",
    "api_pm25_value_status",
    "api_pollutants_listed",
    "api_pollutant_count",
    "current_api_presence_confirmed",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "review_decision",
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


def fetch_json(url: str) -> tuple[dict[str, Any], dict[str, Any]]:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json,*/*"},
        timeout=TIMEOUT_SECONDS,
        allow_redirects=True,
    )
    record = {
        "url": url,
        "final_url": response.url,
        "retrieved": response.ok,
        "http_status": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "retrieval_bytes": len(response.content),
        "sha256": hashlib.sha256(response.content).hexdigest(),
    }
    response.raise_for_status()
    return response.json(), record


def parse_php_title(raw: Any) -> str:
    text = str(raw or "")
    if not text:
        return ""
    for key in ("en", "ru", "uz", "oz"):
        match = re.search(rf's:2:"{key}";s:\d+:"([^"]*)"', text)
        if match:
            return normalize(match.group(1))
    return normalize(text)


def normalize(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\xa0", " ")).strip()


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def parse_reading_date(value: Any) -> str:
    text = normalize(value)
    if not text:
        return ""
    try:
        parsed = datetime.strptime(text, "%d.%m.%Y").date()
    except ValueError:
        return ""
    return parsed.isoformat()


def days_between(generated_at: str, date_iso: str) -> int | None:
    if not date_iso:
        return None
    generated_date = datetime.fromisoformat(generated_at.replace("Z", "+00:00")).date()
    reading_date = datetime.fromisoformat(date_iso).date()
    return (generated_date - reading_date).days


def age_lane(age_days: int | None) -> str:
    if age_days is None:
        return "missing_reading_date"
    if age_days < 0:
        return "future_reading_date"
    if age_days <= 7:
        return "within_7_days"
    if age_days <= 30:
        return "within_30_days"
    if age_days <= 90:
        return "within_90_days"
    if age_days <= 365:
        return "within_365_days"
    return "older_than_365_days"


def live_value_status(value: Any) -> str:
    clean = normalize(value)
    if not clean:
        return "missing_raw_value"
    try:
        number = float(clean)
    except ValueError:
        return "nonnumeric_raw_value"
    if number == -9999:
        return "sentinel_minus_9999"
    if number < 0:
        return "negative_raw_value"
    if number == 0:
        return "zero_raw_value"
    return "positive_raw_value"


def pollutant_keys(station: dict[str, Any]) -> list[str]:
    keys = []
    for key in ("PM2.5", "PM10", "SO2", "CO", "NO2", "NO", "NOX", "NH3", "O3", "C6H6O"):
        if normalize(station.get(key)) not in {"", "-"}:
            keys.append(key)
    return keys


def api_station_index(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for group in payload.get("data") or []:
        for station in group.get("stations") or []:
            station_id = normalize(station.get("id"))
            if station_id:
                output[station_id] = station
    return output


def marker_terms(station: dict[str, Any] | None, method_row: dict[str, str]) -> list[str]:
    terms = []
    if not station:
        return terms
    if as_bool(station.get("is_horiba")):
        terms.append("is_horiba")
    if "horiba" in normalize(station.get("Si")).lower():
        terms.append("Si=horiba")
    if "horiba" in normalize(method_row.get("source_station_type")).lower():
        terms.append("source_station_type=HORIBA")
    return terms


def review_decision(row: dict[str, Any]) -> str:
    if not row["api_station_found"]:
        return "target_station_missing_from_current_api_keep_open"
    if row["api_reading_age_lane"] in {"missing_reading_date", "future_reading_date"}:
        return "api_row_has_no_usable_reading_date_keep_open"
    if row["api_reading_age_lane"] in {"older_than_365_days", "within_365_days", "within_90_days"}:
        return "api_row_present_but_reading_date_not_current_keep_open"
    if row["api_pm25_value_status"] in {"negative_raw_value", "sentinel_minus_9999", "missing_raw_value", "nonnumeric_raw_value"}:
        return "api_row_present_with_raw_value_caution_keep_open"
    return "api_row_present_horiba_marker_recent_value_keep_not_grade_ready"


def reader_use(row: dict[str, Any]) -> str:
    if not row["api_station_found"]:
        return "Use as a blocker: the target station ID was not found in the current public API response."
    if row["api_reading_age_lane"] in {"older_than_365_days", "within_365_days", "within_90_days"}:
        return (
            "Use as station-presence evidence with a stale-reading caution. "
            "The API still names the station and HORIBA marker, but the reading date is not current-status proof."
        )
    if row["api_pm25_value_status"] in {"negative_raw_value", "sentinel_minus_9999"}:
        return (
            "Use as station-presence evidence with a raw-value caution. "
            "The HORIBA marker is present, but the PM2.5 value needs source-specific QA."
        )
    return (
        "Use as station-presence and station-level HORIBA-marker evidence only. "
        "It still needs explicit current-status and method-grade documentation."
    )


def target_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row["iso3"] == "UZB" and row["row_evidence_lane"] == "row_level_instrument_hint"
    ]


def build_rows(generated_at: str, method_rows: list[dict[str, str]], api_rows: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in sorted(method_rows, key=lambda item: int(item["source_station_id"])):
        station = api_rows.get(row["source_station_id"])
        date_raw = normalize(station.get("date")) if station else ""
        date_iso = parse_reading_date(date_raw)
        age_days = days_between(generated_at, date_iso)
        terms = marker_terms(station, row)
        pollutants = pollutant_keys(station or {})
        out = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "method_evidence_id": row["method_evidence_id"],
            "iso3": row["iso3"],
            "country": row["country"],
            "source_station_id": row["source_station_id"],
            "source_station_name": row["source_station_name"],
            "source_station_type": row["source_station_type"],
            "api_station_found": station is not None,
            "api_station_name": parse_php_title(station.get("title")) if station else "",
            "api_alias": normalize(station.get("alias")) if station else "",
            "api_region_id": normalize(station.get("region_id")) if station else "",
            "api_station_category": parse_php_title(station.get("category_title")) if station else "",
            "api_is_horiba": as_bool(station.get("is_horiba")) if station else False,
            "api_si": normalize(station.get("Si")) if station else "",
            "api_station_level_horiba_marker": bool(terms),
            "api_method_marker_terms": "|".join(terms),
            "api_reading_date_raw": date_raw,
            "api_reading_date_iso": date_iso,
            "api_reading_age_days": age_days if age_days is not None else "",
            "api_reading_age_lane": age_lane(age_days),
            "api_reading_within_7_days": age_days is not None and 0 <= age_days <= 7,
            "api_reading_within_30_days": age_days is not None and 0 <= age_days <= 30,
            "api_reading_within_90_days": age_days is not None and 0 <= age_days <= 90,
            "api_pm25_value_raw": normalize(station.get("PM2.5")) if station else "",
            "api_pm25_value_status": live_value_status(station.get("PM2.5")) if station else "missing_raw_value",
            "api_pollutants_listed": "; ".join(pollutants),
            "api_pollutant_count": len(pollutants),
            "current_api_presence_confirmed": station is not None,
            "current_status_confirmed": False,
            "station_method_classified": False,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
            "review_decision": "",
            "reader_use": "",
            "non_claim": NON_CLAIM,
        }
        out["review_decision"] = review_decision(out)
        out["reader_use"] = reader_use(out)
        output.append(out)
    return output


def age_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lanes = [
        ("within_7_days", "Fresh live-reading support if source policy confirms this as current."),
        ("within_30_days", "Recent API reading, but still not an explicit station-status statement."),
        ("within_90_days", "Stale for current-status use; keep as API-presence evidence only."),
        ("within_365_days", "Old reading date; keep blocked for current-status interpretation."),
        ("older_than_365_days", "Very old reading date; do not treat API presence as active status."),
        ("missing_reading_date", "No reading date; current-status interpretation blocked."),
        ("future_reading_date", "Date sanity error; current-status interpretation blocked."),
    ]
    counts = Counter(row["api_reading_age_lane"] for row in rows)
    return [{"api_reading_age_lane": lane, "rows": counts[lane], "reader_use": use} for lane, use in lanes if counts[lane]]


def sample_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = [
        "method_evidence_id",
        "source_station_id",
        "source_station_name",
        "api_station_name",
        "api_reading_date_iso",
        "api_reading_age_days",
        "api_reading_age_lane",
        "api_pm25_value_raw",
        "api_pm25_value_status",
        "api_method_marker_terms",
        "review_decision",
        "reader_use",
    ]
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            -1 if row["api_reading_age_days"] == "" else int(row["api_reading_age_days"]),
            row["source_station_id"],
        ),
        reverse=True,
    )
    return [{field: row[field] for field in fields} for row in sorted_rows[:12]]


def summary(generated_at: str, rows: list[dict[str, Any]], source_record: dict[str, Any], api_station_count: int) -> dict[str, Any]:
    counts = {
        "target_uzbekistan_instrument_hint_rows": len(rows),
        "api_station_rows_returned": api_station_count,
        "target_station_rows_found_in_current_api": sum(row["api_station_found"] for row in rows),
        "station_level_horiba_marker_rows": sum(row["api_station_level_horiba_marker"] for row in rows),
        "api_reading_date_rows": sum(bool(row["api_reading_date_iso"]) for row in rows),
        "api_reading_within_7_days_rows": sum(row["api_reading_within_7_days"] for row in rows),
        "api_reading_within_30_days_rows": sum(row["api_reading_within_30_days"] for row in rows),
        "api_reading_within_90_days_rows": sum(row["api_reading_within_90_days"] for row in rows),
        "api_reading_older_than_365_days_rows": sum(row["api_reading_age_lane"] == "older_than_365_days" for row in rows),
        "positive_raw_pm25_value_rows": sum(row["api_pm25_value_status"] == "positive_raw_value" for row in rows),
        "zero_raw_pm25_value_rows": sum(row["api_pm25_value_status"] == "zero_raw_value" for row in rows),
        "negative_raw_pm25_value_rows": sum(row["api_pm25_value_status"] == "negative_raw_value" for row in rows),
        "sentinel_raw_pm25_value_rows": sum(row["api_pm25_value_status"] == "sentinel_minus_9999" for row in rows),
        "missing_raw_pm25_value_rows": sum(row["api_pm25_value_status"] == "missing_raw_value" for row in rows),
        "current_api_presence_confirmed_rows": sum(row["current_api_presence_confirmed"] for row in rows),
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    gates = [
        {
            "gate": "Target station row found in live API",
            "status": "available",
            "rows": counts["target_station_rows_found_in_current_api"],
            "reader_use": "The 28 target station IDs are still present in the public Uzhydromet API response.",
        },
        {
            "gate": "Station-level HORIBA marker",
            "status": "partly_available",
            "rows": counts["station_level_horiba_marker_rows"],
            "reader_use": "The station row carries HORIBA marker fields, but this is not complete reference-method classification.",
        },
        {
            "gate": "API reading date within 30 days",
            "status": "partly_available",
            "rows": counts["api_reading_within_30_days_rows"],
            "reader_use": "Recent enough for follow-up priority, but still not an explicit active/current station-status statement.",
        },
        {
            "gate": "API reading date older than 365 days",
            "status": "caution",
            "rows": counts["api_reading_older_than_365_days_rows"],
            "reader_use": "Very old API reading dates show why API presence cannot be treated as current operating status.",
        },
        {
            "gate": "Positive raw PM2.5 value",
            "status": "partly_available",
            "rows": counts["positive_raw_pm25_value_rows"] + counts["zero_raw_pm25_value_rows"],
            "reader_use": "A nonnegative raw value is a sanity signal only, not status or grade certification.",
        },
        {
            "gate": "Negative or sentinel raw PM2.5 value",
            "status": "caution",
            "rows": counts["negative_raw_pm25_value_rows"] + counts["sentinel_raw_pm25_value_rows"],
            "reader_use": "Negative and sentinel values require source-specific QA before any current-reading interpretation.",
        },
        {
            "gate": "Current-status confirmed",
            "status": "not_ready",
            "rows": counts["current_status_confirmed_rows"],
            "reader_use": "No target row has an explicit active/current station-status statement.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": counts["complete_monitor_grade_classification_rows"],
            "reader_use": "No target row has complete station-level method/grade classification.",
        },
        {
            "gate": "Station-radius grade assumptions",
            "status": "not_ready",
            "rows": counts["station_radius_grade_assumption_ready_rows"],
            "reader_use": "Station-radius coverage remains blocked until station-grade assumptions are validated.",
        },
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Uzbekistan station current/method source scan",
        "source_records": [
            {
                **source_record,
                "role": "public Uzhydromet maps API used to re-check target station rows by station ID",
                "source_page_url": MAP_URL,
            }
        ],
        "coverage_counts": counts,
        "age_lane_rows": age_rows(rows),
        "evidence_gate_counts": gates,
        "station_sample_rows": sample_rows(rows),
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    method_rows = target_rows(read_csv(INPUT_CSV))
    payload, source_record = fetch_json(API_URL)
    api_rows = api_station_index(payload)
    rows = build_rows(generated_at, method_rows, api_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary(generated_at, rows, source_record, len(api_rows)))
    counts = Counter(row["api_reading_age_lane"] for row in rows)
    print(
        "Built Uzbekistan station current/method scan: "
        f"{len(rows)} target rows; "
        f"{sum(row['api_station_found'] for row in rows)} API rows found; "
        f"{sum(row['api_station_level_horiba_marker'] for row in rows)} HORIBA markers; "
        f"{counts['within_30_days']} within 30 days; "
        f"{counts['older_than_365_days']} older than 365 days."
    )


if __name__ == "__main__":
    main()
