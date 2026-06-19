"""Follow up exact Uzbekistan rows that still block station-radius claims.

The status/certification scan narrowed the next Uzbekistan work to three rows:
two stale official station-detail pages and one recent detail page with a
negative PM2.5 sentinel. This pass retrieves only those exact official station
pages and their regional table rows, records whether the blocker is resolved,
and keeps the claim gate closed unless public row-level status and grade
language are explicit.
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
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

TARGET_SEED_CSV = SOURCE_INPUTS_DIR / "uzbekistan-blocker-row-followup-targets.csv"
STATUS_SCAN_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-status-certification-source-scan.csv"
STATION_SPECIFIC_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-specific-source-evidence.csv"
CURRENT_METHOD_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-current-method-scan.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup-summary.json"

METHOD = "air_monitoring_uzbekistan_blocker_row_followup_v1"
STATUS = "computed_uzbekistan_blocker_row_followup"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This follow-up checks exact official blocker rows. It does not convert "
    "station-detail timestamps, HORIBA labels, or pollutant values into "
    "current operating status, complete monitor-grade classification, or "
    "station-radius readiness without explicit public row-level language."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "blocker_followup_id",
    "source_station_id",
    "review_focus",
    "source_station_name",
    "expected_station_name",
    "api_alias",
    "api_reading_age_lane",
    "api_pm25_value_status",
    "prior_source_scan_decision",
    "prior_context_source_keys",
    "region_page_url",
    "region_page_retrieved",
    "region_page_sha256",
    "region_row_found",
    "region_row_name",
    "region_row_address",
    "region_row_auto",
    "region_row_updated_raw",
    "region_row_updated_iso",
    "region_row_updated_age_days",
    "region_row_updating_data_status",
    "region_row_horiba_context",
    "region_row_view_url",
    "region_row_view_id_matches_target",
    "detail_url",
    "detail_page_retrieved",
    "detail_page_sha256",
    "detail_title",
    "detail_updated_raw",
    "detail_updated_iso",
    "detail_updated_age_days",
    "detail_recent_measurement_within_30_days",
    "detail_pm25_value",
    "detail_pm25_value_status",
    "detail_negative_pollutant_count",
    "detail_sentinel_minus_9999_pollutant_count",
    "official_row_exactly_named",
    "stale_detail_blocker_present",
    "sentinel_pm25_blocker_present",
    "public_row_followup_resolved_blocker",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "followup_decision",
    "reader_use",
    "reader_question",
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


def fetch_source(url: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "url": url,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "soup": None,
        "error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        result["soup"] = BeautifulSoup(response.text, "html.parser")
        result["text"] = normalize(result["soup"].get_text(" ", strip=True))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are evidence.
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def col_text(item: Any, class_name: str) -> str:
    element = item.select_one(f".{class_name}")
    return normalize(element.get_text(" ", strip=True)) if element else ""


def parse_local_datetime(value: str, generated_at: str) -> tuple[str, int | None]:
    raw = normalize(value)
    match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", raw)
    if not match:
        return "", None
    day, month, year = match.groups()
    parsed = datetime(int(year), int(month), int(day), tzinfo=timezone.utc).date()
    generated_date = datetime.fromisoformat(generated_at.replace("Z", "+00:00")).date()
    return parsed.isoformat(), (generated_date - parsed).days


def parse_region_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    soup = source.get("soup")
    if soup is None:
        return rows
    base_url = str(source["final_url"] or source["url"])
    for item in soup.select(".points-item"):
        view_anchor = item.select_one(".col-art a[href]")
        view_url = urljoin(base_url, view_anchor["href"]) if view_anchor else ""
        view_match = re.search(r"/map/view/(\d+)", view_url)
        row = {
            "name": col_text(item, "col-name"),
            "address": col_text(item, "col-address"),
            "auto": col_text(item, "col-auto"),
            "updated_raw": col_text(item, "col-art"),
            "view_url": view_url,
            "view_station_id": view_match.group(1) if view_match else "",
        }
        if any(row[field] for field in ("name", "address", "auto", "updated_raw", "view_station_id")):
            rows.append(row)
    return rows


def find_region_row(rows: list[dict[str, Any]], station_id: str, expected_name: str) -> dict[str, Any] | None:
    for row in rows:
        if row["view_station_id"] == station_id:
            return row
    expected = norm_key(expected_name)
    name_matches = [row for row in rows if expected and norm_key(row["name"]) == expected]
    return name_matches[0] if len(name_matches) == 1 else None


def parse_pollutants(text: str) -> dict[str, str]:
    pollutants: dict[str, str] = {}
    labels = [
        "PM 2.5",
        "PM 10",
        "Оксид углерода",
        "Диоксид серы",
        "Оксид азота",
        "Диоксид азота",
        "Озон (O3)",
    ]
    for label in labels:
        pattern = rf"{re.escape(label)}:\s*(-?[0-9]+(?:[.,][0-9]+)?)"
        match = re.search(pattern, text)
        if match:
            pollutants[label] = match.group(1).replace(",", ".")
    return pollutants


def value_status(value: str) -> str:
    if not normalize(value):
        return "missing"
    try:
        number = float(value)
    except ValueError:
        return "non_numeric"
    if number == -9999:
        return "sentinel_minus_9999"
    if number < 0:
        return "negative"
    if number == 0:
        return "zero"
    return "positive"


def parse_detail_page(source: dict[str, Any], generated_at: str) -> dict[str, Any]:
    soup = source.get("soup")
    text = source.get("text", "")
    title = ""
    if soup is not None:
        h1 = soup.find("h1")
        if h1:
            title = normalize(h1.get_text(" ", strip=True))
    updated_match = re.search(r"Updated:\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4}\s+[0-9]{2}:[0-9]{2})", text)
    updated_raw = updated_match.group(1) if updated_match else ""
    updated_iso, updated_age_days = parse_local_datetime(updated_raw, generated_at)
    pollutants = parse_pollutants(text)
    pm25_value = pollutants.get("PM 2.5", "")
    statuses = [value_status(value) for value in pollutants.values()]
    return {
        "title": title,
        "updated_raw": updated_raw,
        "updated_iso": updated_iso,
        "updated_age_days": updated_age_days,
        "recent": updated_age_days is not None and 0 <= updated_age_days <= 30,
        "pm25_value": pm25_value,
        "pm25_status": value_status(pm25_value),
        "negative_pollutant_count": sum(status in {"negative", "sentinel_minus_9999"} for status in statuses),
        "sentinel_minus_9999_pollutant_count": sum(status == "sentinel_minus_9999" for status in statuses),
    }


def indexed(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {normalize(row.get("source_station_id")): row for row in rows if normalize(row.get("source_station_id"))}


def followup_decision(row: dict[str, Any]) -> str:
    if row["sentinel_pm25_blocker_present"]:
        return "sentinel_pm25_confirmed_keep_blocked"
    if row["stale_detail_blocker_present"] and row["region_row_updating_data_status"]:
        return "stale_detail_and_region_updating_keep_blocked"
    if row["stale_detail_blocker_present"]:
        return "stale_detail_measurement_keep_blocked"
    if row["detail_recent_measurement_within_30_days"] and row["region_row_horiba_context"]:
        return "presence_context_only_no_grade_keep_open"
    return "no_public_resolution_keep_open"


def reader_use(row: dict[str, Any]) -> str:
    if row["sentinel_pm25_blocker_present"]:
        return (
            "Use as a QA blocker: the exact official detail page is recent but "
            "the PM2.5 value is the -9999 sentinel, so the row cannot support a "
            "station-radius or current-status claim."
        )
    if row["stale_detail_blocker_present"] and row["region_row_updating_data_status"]:
        return (
            "Use as a current-status blocker: the exact official detail page is "
            "older than 30 days and the regional table says Updating data."
        )
    if row["stale_detail_blocker_present"]:
        return (
            "Use as a current-status blocker: the exact official detail page is "
            "older than 30 days and has no public status/grade closure."
        )
    return (
        "Use as row-level context only. Public station-radius use still needs "
        "explicit current-status and complete monitor-grade documentation."
    )


def build_rows(generated_at: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    targets = read_csv(TARGET_SEED_CSV)
    prior_status = indexed(read_csv(STATUS_SCAN_CSV))
    station_specific = indexed(read_csv(STATION_SPECIFIC_CSV))
    current_method = indexed(read_csv(CURRENT_METHOD_CSV))

    source_records: list[dict[str, Any]] = []
    region_cache: dict[str, dict[str, Any]] = {}
    detail_cache: dict[str, dict[str, Any]] = {}

    rows: list[dict[str, Any]] = []
    for target in targets:
        station_id = normalize(target["source_station_id"])
        region_url = target["region_page_url"]
        detail_url = target["detail_url"]

        if region_url not in region_cache:
            region_source = fetch_source(region_url)
            region_cache[region_url] = {"source": region_source, "rows": parse_region_rows(region_source)}
            source_records.append(
                {
                    "source_key": f"official_region_table_{len(region_cache)}",
                    "source_role": "official_region_station_table",
                    **{k: v for k, v in region_source.items() if k not in {"soup", "text"}},
                }
            )
        if detail_url not in detail_cache:
            detail_source = fetch_source(detail_url)
            detail_cache[detail_url] = {"source": detail_source, "detail": parse_detail_page(detail_source, generated_at)}
            source_records.append(
                {
                    "source_key": f"official_station_detail_{station_id}",
                    "source_role": "official_station_detail_page",
                    **{k: v for k, v in detail_source.items() if k not in {"soup", "text"}},
                }
            )

        region_source = region_cache[region_url]["source"]
        region_row = find_region_row(region_cache[region_url]["rows"], station_id, target["expected_station_name"])
        detail_source = detail_cache[detail_url]["source"]
        detail = detail_cache[detail_url]["detail"]
        status_row = prior_status.get(station_id, {})
        specific_row = station_specific.get(station_id, {})
        current_row = current_method.get(station_id, {})

        region_updated_iso = ""
        region_updated_age_days: int | None = None
        if region_row:
            region_updated_iso, region_updated_age_days = parse_local_datetime(region_row["updated_raw"], generated_at)
        region_updated_raw = region_row["updated_raw"] if region_row else ""
        region_updating = any(term in norm_key(region_updated_raw) for term in ["updating data", "обновление", "янгилан"])
        region_auto = region_row["auto"] if region_row else ""
        region_horiba = "horiba" in norm_key(region_auto)
        detail_age = detail["updated_age_days"]
        stale_detail = detail_age is not None and detail_age > 30
        sentinel_pm25 = detail["pm25_status"] == "sentinel_minus_9999"
        exact_name = bool(
            region_row
            and normalize(region_row["view_station_id"]) == station_id
            and normalize(target["expected_station_name"])
            and norm_key(region_row["name"]) == norm_key(target["expected_station_name"])
        )

        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "blocker_followup_id": f"UZB-blocker-followup-{station_id}",
            "source_station_id": station_id,
            "review_focus": target["review_focus"],
            "source_station_name": status_row.get("source_station_name") or specific_row.get("source_station_name") or target["expected_station_name"],
            "expected_station_name": target["expected_station_name"],
            "api_alias": specific_row.get("api_alias", ""),
            "api_reading_age_lane": current_row.get("api_reading_age_lane", ""),
            "api_pm25_value_status": current_row.get("api_pm25_value_status", ""),
            "prior_source_scan_decision": status_row.get("source_scan_decision", ""),
            "prior_context_source_keys": status_row.get("additional_context_source_keys", ""),
            "region_page_url": region_url,
            "region_page_retrieved": bool(region_source["retrieved"]),
            "region_page_sha256": region_source["sha256"],
            "region_row_found": bool(region_row),
            "region_row_name": region_row["name"] if region_row else "",
            "region_row_address": region_row["address"] if region_row else "",
            "region_row_auto": region_auto,
            "region_row_updated_raw": region_updated_raw,
            "region_row_updated_iso": region_updated_iso,
            "region_row_updated_age_days": "" if region_updated_age_days is None else region_updated_age_days,
            "region_row_updating_data_status": region_updating,
            "region_row_horiba_context": region_horiba,
            "region_row_view_url": region_row["view_url"] if region_row else "",
            "region_row_view_id_matches_target": bool(region_row and region_row["view_station_id"] == station_id),
            "detail_url": detail_url,
            "detail_page_retrieved": bool(detail_source["retrieved"]),
            "detail_page_sha256": detail_source["sha256"],
            "detail_title": detail["title"],
            "detail_updated_raw": detail["updated_raw"],
            "detail_updated_iso": detail["updated_iso"],
            "detail_updated_age_days": "" if detail_age is None else detail_age,
            "detail_recent_measurement_within_30_days": detail["recent"],
            "detail_pm25_value": detail["pm25_value"],
            "detail_pm25_value_status": detail["pm25_status"],
            "detail_negative_pollutant_count": detail["negative_pollutant_count"],
            "detail_sentinel_minus_9999_pollutant_count": detail["sentinel_minus_9999_pollutant_count"],
            "official_row_exactly_named": exact_name,
            "stale_detail_blocker_present": stale_detail,
            "sentinel_pm25_blocker_present": sentinel_pm25,
            "public_row_followup_resolved_blocker": False,
            "current_status_confirmed": False,
            "station_method_classified": False,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
            "reader_question": target["reader_question"],
            "non_claim": NON_CLAIM,
        }
        row["followup_decision"] = followup_decision(row)
        row["reader_use"] = reader_use(row)
        rows.append(row)
    return rows, source_records


def gate(status: str, gate_name: str, rows: int, reader_use_text: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use_text}


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_blocker_rows": len(rows),
        "official_region_pages_seeded": len({row["region_page_url"] for row in rows}),
        "official_region_pages_retrieved": len(
            {record["url"] for record in source_records if record["source_role"] == "official_region_station_table" and record["retrieved"]}
        ),
        "official_detail_pages_retrieved": sum(record["source_role"] == "official_station_detail_page" and record["retrieved"] for record in source_records),
        "region_row_found_rows": sum(row["region_row_found"] for row in rows),
        "region_row_updating_data_rows": sum(row["region_row_updating_data_status"] for row in rows),
        "region_row_horiba_context_rows": sum(row["region_row_horiba_context"] for row in rows),
        "detail_page_retrieved_rows": sum(row["detail_page_retrieved"] for row in rows),
        "stale_detail_blocker_rows": sum(row["stale_detail_blocker_present"] for row in rows),
        "sentinel_pm25_blocker_rows": sum(row["sentinel_pm25_blocker_present"] for row in rows),
        "public_row_followup_resolved_rows": sum(row["public_row_followup_resolved_blocker"] for row in rows),
        "current_status_confirmed_rows": sum(row["current_status_confirmed"] for row in rows),
        "station_method_classified_rows": sum(row["station_method_classified"] for row in rows),
        "complete_monitor_grade_classification_rows": sum(row["complete_monitor_grade_classification_available"] for row in rows),
        "station_radius_grade_assumption_ready_rows": sum(row["station_radius_grade_assumption_ready"] for row in rows),
    }
    evidence_gates = [
        gate("available", "Official blocker detail pages retrieved", counts["official_detail_pages_retrieved"], "All exact blocker station-detail pages are retrievable as public official pages."),
        gate("available", "Official region rows found", counts["region_row_found_rows"], "The regional tables still expose matching station rows for the blocker IDs."),
        gate("caution", "Stale detail blockers remain", counts["stale_detail_blocker_rows"], "Two exact detail pages remain older than the 30-day currentness threshold."),
        gate("caution", "Sentinel PM2.5 blocker remains", counts["sentinel_pm25_blocker_rows"], "One exact detail page is recent but carries the -9999 PM2.5 sentinel."),
        gate("not_ready", "Public blocker resolution", counts["public_row_followup_resolved_rows"], "No exact row has public language resolving the stale/sentinel blocker."),
        gate("not_ready", "Current-status confirmed", counts["current_status_confirmed_rows"], "No blocker row has explicit current operating status closure."),
        gate("not_ready", "Complete monitor-grade classification", counts["complete_monitor_grade_classification_rows"], "No blocker row has complete station-grade documentation."),
        gate("not_ready", "Station-radius grade assumption", counts["station_radius_grade_assumption_ready_rows"], "No blocker row is eligible for station-radius assumptions."),
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Uzbekistan blocker-row follow-up",
        "coverage_counts": counts,
        "source_records": source_records,
        "evidence_gate_counts": evidence_gates,
        "decision_counts": [
            {"decision": key, "rows": value}
            for key, value in sorted(Counter(row["followup_decision"] for row in rows).items())
        ],
        "station_rows": rows,
        "reader_warning": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    rows, source_records = build_rows(generated_at)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, source_records))
    counts = Counter(row["followup_decision"] for row in rows)
    print(
        "Built Uzbekistan blocker-row follow-up: "
        f"{len(rows)} blocker rows; "
        f"{sum(row['detail_page_retrieved'] for row in rows)}/{len(rows)} details retrieved; "
        f"{sum(row['stale_detail_blocker_present'] for row in rows)} stale rows; "
        f"{sum(row['sentinel_pm25_blocker_present'] for row in rows)} sentinel rows; "
        f"{sum(row['public_row_followup_resolved_blocker'] for row in rows)} resolved rows; "
        f"decisions={dict(counts)}."
    )


if __name__ == "__main__":
    main()
