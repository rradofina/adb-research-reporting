"""Scan exact station-code/status sources for unresolved monitor-grade rows.

This pass is deliberately narrow. It follows the Indonesia/Georgia row-method
source scan and the Uzbekistan blocker follow-up, then checks whether stricter
public station-code sources close the remaining method/status/grade gates.

The scan stores selected fields and retrieval hashes only. It does not commit
raw HTML, JavaScript, or full API payloads.
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
from urllib.parse import urlencode

import requests


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "station-code-status-method-source-seed.csv"
METHOD_EVIDENCE_CSV = GENERATED_DIR / "air-monitoring-monitor-grade-station-method-evidence.csv"
ROW_METHOD_SOURCE_CSV = GENERATED_DIR / "air-monitoring-indonesia-georgia-row-method-source-scan.csv"
UZB_BLOCKER_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup.csv"
UZB_BLOCKER_SUMMARY_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup-summary.json"
OUT_CSV = GENERATED_DIR / "air-monitoring-station-code-status-method-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-station-code-status-method-source-scan-summary.json"

METHOD = "air_monitoring_station_code_status_method_source_scan_v1"
STATUS = "computed_station_code_status_method_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This scan checks exact station-code or station-ID public sources for "
    "method/status closure. It does not convert API presence, station "
    "descriptions, PM2.5 equipment rows, live values, HORIBA hints, or BMKG "
    "method context into current-status confirmation, complete monitor-grade "
    "classification, or station-radius readiness."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "station_code_status_scan_id",
    "upstream_evidence_id",
    "upstream_source",
    "iso3",
    "country",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "station_code_source_lane",
    "source_record_keys",
    "exact_station_code_or_id_found",
    "station_address",
    "latitude",
    "longitude",
    "station_equipment_count",
    "pollutant_list",
    "pm25_row_or_equipment_listed",
    "pm25_observation_rows",
    "pm25_latest_value",
    "pm25_latest_timestamp",
    "station_description_operating_context",
    "station_description_excerpt",
    "station_test_mode_flag",
    "bmkg_payload_station_link_found",
    "bmkg_payload_xml_filename_found",
    "uzbekistan_blocker_type",
    "uzbekistan_detail_age_days",
    "uzbekistan_detail_pm25_value_status",
    "uzbekistan_region_updating_data_status",
    "source_context_terms",
    "station_method_table_found",
    "instrument_model_available",
    "calibration_status_available",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "source_scan_decision",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def current_utc_hour() -> str:
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return now.strftime("%Y-%m-%dT%H:00:00")


def fetch_url(url: str, accept: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "url": url,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "json": None,
        "error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": accept,
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
        if "json" in result["content_type"].lower() or accept == "application/json":
            result["json"] = response.json()
            result["text"] = normalize(json.dumps(result["json"], ensure_ascii=False))
        else:
            result["text"] = normalize(response.text)
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def source_record(source_key: str, seed: dict[str, str], fetched: dict[str, Any], retrieval_url: str) -> dict[str, Any]:
    text = fetched.get("text", "")
    return {
        "source_key": source_key,
        "source_role": seed["source_role"],
        "iso3": seed["iso3"],
        "country": seed["country"],
        "url": seed["url"],
        "retrieval_url": retrieval_url,
        "final_url": fetched["final_url"],
        "retrieved": fetched["retrieved"],
        "http_status": fetched["http_status"],
        "content_type": fetched["content_type"],
        "retrieval_bytes": fetched["retrieval_bytes"],
        "sha256": fetched["sha256"],
        "matched_expected_terms": matched_terms(text, split_terms(seed["expected_terms"])),
        "matched_method_terms": matched_terms(text, split_terms(seed["method_terms"])),
        "matched_current_terms": matched_terms(text, split_terms(seed["current_terms"])),
        "matched_standard_terms": matched_terms(text, split_terms(seed["standard_terms"])),
        "matched_caution_terms": matched_terms(text, split_terms(seed["caution_terms"])),
        "error": fetched["error"],
        "source_note": seed["source_note"],
    }


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(METHOD_EVIDENCE_CSV)
    targets = [
        row
        for row in rows
        if row["iso3"] in {"IDN", "GEO"} and row["row_evidence_lane"] == "row_level_pm25_portal_or_api"
    ]
    targets.sort(key=lambda row: (row["iso3"], row["source_station_id"]))
    return targets


def indexed(rows: list[dict[str, str]], key: str = "source_station_id") -> dict[str, dict[str, str]]:
    return {normalize(row.get(key)): row for row in rows if normalize(row.get(key))}


def station_objects_by_code(api_payload: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(api_payload, list):
        return {}
    output: dict[str, dict[str, Any]] = {}
    for row in api_payload:
        if isinstance(row, dict) and normalize(row.get("code")):
            output[normalize(row["code"])] = row
    return output


def substance_name(equipment_row: dict[str, Any]) -> str:
    substance = equipment_row.get("substance") or {}
    return normalize(substance.get("name"))


def substance_rows(station: dict[str, Any]) -> list[dict[str, Any]]:
    rows = station.get("stationequipment_set") or []
    return [row for row in rows if isinstance(row, dict)]


def pm25_equipment(station: dict[str, Any]) -> dict[str, Any] | None:
    for row in substance_rows(station):
        if substance_name(row) == "PM2.5":
            return row
    return None


def latest_pm25_observation(pm25: dict[str, Any] | None) -> tuple[str, str, int]:
    if not pm25:
        return "", "", 0
    rows = pm25.get("data1hour_set") or []
    if not isinstance(rows, list) or not rows:
        return "", "", 0
    latest = rows[-1] if isinstance(rows[-1], dict) else {}
    value = latest.get("value", latest.get("value1", ""))
    timestamp = latest.get("date_time") or latest.get("observ_date_time") or latest.get("observ_start_date_time") or latest.get("date") or ""
    return normalize(value), normalize(timestamp), len(rows)


def clean_excerpt(value: Any, limit: int = 260) -> str:
    text = normalize(re.sub(r"<[^>]+>", " ", str(value or "")))
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def operating_context(text: str) -> bool:
    lower = norm_key(text)
    return any(term in lower for term in ["operating since", "operated since", "in operation since"])


def build_georgia_rows(
    generated_at: str,
    targets: list[dict[str, str]],
    stations: dict[str, dict[str, Any]],
    source_key: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in [row for row in targets if row["iso3"] == "GEO"]:
        station = stations.get(target["source_station_id"], {})
        pm25 = pm25_equipment(station)
        pm25_value, pm25_timestamp, pm25_rows = latest_pm25_observation(pm25)
        pollutants = [substance_name(row) for row in substance_rows(station) if substance_name(row)]
        description = clean_excerpt(station.get("description_short_en") or station.get("description_short_ge"))
        test_mode = "test mode" in norm_key(target["source_station_name"]) or "test mode" in norm_key(station.get("settlement_en"))
        code_found = bool(station)
        has_pm25 = bool(pm25)
        has_operating_context = operating_context(description)
        if test_mode:
            decision = "georgia_station_code_test_mode_keep_blocked"
            reader_use = (
                "Use as explicit exclusion pressure: the public station-code row is present and lists PM2.5, "
                "but the target name says working in test mode."
            )
        elif code_found and has_pm25 and has_operating_context:
            decision = "georgia_station_code_pm25_equipment_context_keep_not_grade_ready"
            reader_use = (
                "Use as a stronger Georgia row-context source: the public API returns the exact station code, "
                "PM2.5 equipment/substance rows, and operating-description language. It still lacks instrument "
                "model, calibration/status, and grade certification fields."
            )
        elif code_found and has_pm25:
            decision = "georgia_station_code_pm25_equipment_without_status_keep_open"
            reader_use = (
                "Use as station-code PM2.5 context only. The API row lacks operating-description language or "
                "complete method/status closure."
            )
        else:
            decision = "georgia_station_code_not_found_keep_open"
            reader_use = "The target station code was not found in the retrieved public API payload."
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "station_code_status_scan_id": f"GEO-station-code-status-{target['source_station_id']}",
                "upstream_evidence_id": target["method_evidence_id"],
                "upstream_source": str(METHOD_EVIDENCE_CSV.relative_to(PROGRAM_DIR)),
                "iso3": "GEO",
                "country": target["country"],
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "source_station_type": target["source_station_type"],
                "station_code_source_lane": "georgia_airgov_station_code_api",
                "source_record_keys": source_key,
                "exact_station_code_or_id_found": code_found,
                "station_address": normalize(station.get("address_en") or station.get("st_full_address_en")),
                "latitude": station.get("lat", ""),
                "longitude": station.get("long", ""),
                "station_equipment_count": station.get("equipment_count", ""),
                "pollutant_list": "|".join(pollutants),
                "pm25_row_or_equipment_listed": has_pm25,
                "pm25_observation_rows": pm25_rows,
                "pm25_latest_value": pm25_value,
                "pm25_latest_timestamp": pm25_timestamp,
                "station_description_operating_context": has_operating_context,
                "station_description_excerpt": description,
                "station_test_mode_flag": test_mode,
                "bmkg_payload_station_link_found": False,
                "bmkg_payload_xml_filename_found": False,
                "uzbekistan_blocker_type": "",
                "uzbekistan_detail_age_days": "",
                "uzbekistan_detail_pm25_value_status": "",
                "uzbekistan_region_updating_data_status": False,
                "source_context_terms": "station_code|PM2.5_equipment|operating_description" if has_operating_context else "station_code|PM2.5_equipment",
                "station_method_table_found": False,
                "instrument_model_available": False,
                "calibration_status_available": False,
                "current_status_confirmed": False,
                "station_method_classified": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "source_scan_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def build_indonesia_rows(
    generated_at: str,
    targets: list[dict[str, str]],
    row_method_rows: dict[str, dict[str, str]],
    bmkg_text: str,
    source_key: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in [row for row in targets if row["iso3"] == "IDN"]:
        prior = row_method_rows.get(target["source_station_id"], {})
        station_id = target["source_station_id"]
        link_found = f"/kualitas-udara/pm25/{station_id}" in bmkg_text or station_id in bmkg_text
        xml_found = f"{station_id}.xml" in bmkg_text
        context_terms = []
        if link_found:
            context_terms.append("station_link")
        if xml_found:
            context_terms.append("nuxt_payload_xml_filename")
        if boolish(prior.get("same_page_method_context_candidate")):
            context_terms.append("same_page_method_context")
        decision = "indonesia_bmkg_payload_station_code_context_keep_not_grade_ready"
        reader_use = (
            "Use as BMKG row-context evidence: the portal source exposes the exact station link/payload key "
            "and the prior detail-page scan found same-page method context. It still lacks a station-level "
            "method table, calibration/status record, and grade classification."
        )
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "station_code_status_scan_id": f"IDN-station-code-status-{station_id}",
                "upstream_evidence_id": target["method_evidence_id"],
                "upstream_source": str(ROW_METHOD_SOURCE_CSV.relative_to(PROGRAM_DIR)),
                "iso3": "IDN",
                "country": target["country"],
                "source_station_id": station_id,
                "source_station_name": target["source_station_name"],
                "source_station_type": target["source_station_type"],
                "station_code_source_lane": "indonesia_bmkg_portal_payload",
                "source_record_keys": source_key,
                "exact_station_code_or_id_found": link_found or xml_found,
                "station_address": "",
                "latitude": "",
                "longitude": "",
                "station_equipment_count": "",
                "pollutant_list": "PM2.5",
                "pm25_row_or_equipment_listed": boolish(target["exact_pm25_signal"]),
                "pm25_observation_rows": 1 if target["exact_live_pm25_value_status"] == "positive_raw_value" else 0,
                "pm25_latest_value": target["exact_live_pm25_value_raw"],
                "pm25_latest_timestamp": prior.get("exact_station_detail_timestamp_raw", ""),
                "station_description_operating_context": False,
                "station_description_excerpt": "",
                "station_test_mode_flag": False,
                "bmkg_payload_station_link_found": link_found,
                "bmkg_payload_xml_filename_found": xml_found,
                "uzbekistan_blocker_type": "",
                "uzbekistan_detail_age_days": "",
                "uzbekistan_detail_pm25_value_status": "",
                "uzbekistan_region_updating_data_status": False,
                "source_context_terms": "|".join(context_terms),
                "station_method_table_found": False,
                "instrument_model_available": False,
                "calibration_status_available": False,
                "current_status_confirmed": False,
                "station_method_classified": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "source_scan_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def build_uzbekistan_rows(generated_at: str, source_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    blockers = read_csv(UZB_BLOCKER_CSV)
    source_keys = [record["source_key"] for record in source_records if str(record["source_key"]).startswith("prior_uzbekistan")]
    for row in blockers:
        blocker_type = "sentinel_pm25" if boolish(row["sentinel_pm25_blocker_present"]) else "stale_detail"
        decision = "uzbekistan_exact_blocker_still_unresolved_keep_blocked"
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "station_code_status_scan_id": f"UZB-station-code-status-{row['source_station_id']}",
                "upstream_evidence_id": row["blocker_followup_id"],
                "upstream_source": str(UZB_BLOCKER_CSV.relative_to(PROGRAM_DIR)),
                "iso3": "UZB",
                "country": "Uzbekistan",
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "source_station_type": "official Uzhydromet station-detail page",
                "station_code_source_lane": "uzbekistan_blocker_followup_carried_forward",
                "source_record_keys": "|".join(source_keys),
                "exact_station_code_or_id_found": boolish(row["region_row_view_id_matches_target"]) and boolish(row["detail_page_retrieved"]),
                "station_address": row["region_row_address"],
                "latitude": "",
                "longitude": "",
                "station_equipment_count": "",
                "pollutant_list": "PM2.5",
                "pm25_row_or_equipment_listed": bool(row["detail_pm25_value"]),
                "pm25_observation_rows": 1 if row["detail_pm25_value"] else 0,
                "pm25_latest_value": row["detail_pm25_value"],
                "pm25_latest_timestamp": row["detail_updated_raw"],
                "station_description_operating_context": False,
                "station_description_excerpt": row["reader_use"],
                "station_test_mode_flag": False,
                "bmkg_payload_station_link_found": False,
                "bmkg_payload_xml_filename_found": False,
                "uzbekistan_blocker_type": blocker_type,
                "uzbekistan_detail_age_days": row["detail_updated_age_days"],
                "uzbekistan_detail_pm25_value_status": row["detail_pm25_value_status"],
                "uzbekistan_region_updating_data_status": boolish(row["region_row_updating_data_status"]),
                "source_context_terms": "exact_station_id|detail_page|region_row" + ("|horiba_hint" if boolish(row["region_row_horiba_context"]) else ""),
                "station_method_table_found": False,
                "instrument_model_available": False,
                "calibration_status_available": False,
                "current_status_confirmed": False,
                "station_method_classified": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "source_scan_decision": decision,
                "reader_use": (
                    "Use as a carried-forward blocker. The exact public row remains unresolved and must stay "
                    "out of monitor-grade and station-radius assumptions."
                ),
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def prior_uzbekistan_source_records() -> list[dict[str, Any]]:
    payload = read_json(UZB_BLOCKER_SUMMARY_JSON)
    records = []
    for record in payload.get("source_records", []):
        records.append(
            {
                "source_key": f"prior_uzbekistan_blocker_{record.get('source_key')}",
                "source_role": record.get("source_role", ""),
                "iso3": "UZB",
                "country": "Uzbekistan",
                "url": record.get("url", ""),
                "retrieval_url": record.get("url", ""),
                "final_url": record.get("final_url", ""),
                "retrieved": record.get("retrieved", False),
                "http_status": record.get("http_status", ""),
                "content_type": record.get("content_type", ""),
                "retrieval_bytes": record.get("retrieval_bytes", 0),
                "sha256": record.get("sha256", ""),
                "matched_expected_terms": [],
                "matched_method_terms": [],
                "matched_current_terms": [],
                "matched_standard_terms": [],
                "matched_caution_terms": [],
                "error": record.get("error", ""),
                "source_note": "Carried forward from the committed Uzbekistan blocker-row follow-up source record.",
            }
        )
    return records


def fetch_source_records(generated_at: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    seeds = {row["source_key"]: row for row in read_csv(SEED_CSV)}
    fetched: dict[str, dict[str, Any]] = {}
    records: list[dict[str, Any]] = []

    hour = current_utc_hour()
    airgov_params = urlencode(
        {
            "from_date_time": hour,
            "to_date_time": hour,
            "station_code": "all",
            "municipality_id": "all",
            "substance": "all",
            "last_data": "true",
            "chart": "false",
            "format": "json",
        }
    )
    airgov_seed = seeds["airgov_station_code_hourly_api"]
    airgov_url = f"{airgov_seed['url']}?{airgov_params}"
    fetched["airgov_station_code_hourly_api"] = fetch_url(airgov_url, "application/json")
    records.append(source_record("airgov_station_code_hourly_api", airgov_seed, fetched["airgov_station_code_hourly_api"], airgov_url))

    bmkg_seed = seeds["bmkg_pm25_portal_nuxt_payload"]
    fetched["bmkg_pm25_portal_nuxt_payload"] = fetch_url(bmkg_seed["url"], "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    records.append(source_record("bmkg_pm25_portal_nuxt_payload", bmkg_seed, fetched["bmkg_pm25_portal_nuxt_payload"], bmkg_seed["url"]))

    records.extend(prior_uzbekistan_source_records())
    return fetched, records


def country_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        subset = [row for row in rows if row["iso3"] == iso3]
        output.append(
            {
                "iso3": iso3,
                "country": subset[0]["country"],
                "target_rows": len(subset),
                "exact_station_code_or_id_rows": sum(row["exact_station_code_or_id_found"] for row in subset),
                "pm25_row_or_equipment_rows": sum(row["pm25_row_or_equipment_listed"] for row in subset),
                "station_operating_description_context_rows": sum(row["station_description_operating_context"] for row in subset),
                "test_mode_or_blocker_rows": sum(row["station_test_mode_flag"] or bool(row["uzbekistan_blocker_type"]) for row in subset),
                "station_method_table_rows": sum(row["station_method_table_found"] for row in subset),
                "current_status_confirmed_rows": 0,
                "station_method_classified_rows": 0,
                "complete_monitor_grade_classification_rows": 0,
                "station_radius_grade_assumption_ready_rows": 0,
            }
        )
    return output


def gate(status: str, gate_name: str, rows: int, reader_use_text: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use_text}


def evidence_gates(rows: list[dict[str, Any]], source_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        gate(
            "available",
            "Exact station code or ID found",
            sum(row["exact_station_code_or_id_found"] for row in rows),
            "Every target remains traceable to an exact public station code, link, payload key, or station-detail ID.",
        ),
        gate(
            "available",
            "Georgia station-code API rows",
            sum(row["station_code_source_lane"] == "georgia_airgov_station_code_api" and row["exact_station_code_or_id_found"] for row in rows),
            "Georgia improves from alias context to exact public station-code API rows.",
        ),
        gate(
            "partly_available",
            "Georgia PM2.5 equipment rows",
            sum(row["iso3"] == "GEO" and row["pm25_row_or_equipment_listed"] for row in rows),
            "The air.gov.ge station-code objects list PM2.5 among station substances for all target Georgia rows.",
        ),
        gate(
            "partly_available",
            "Georgia operating-description context",
            sum(row["iso3"] == "GEO" and row["station_description_operating_context"] for row in rows),
            "Most Georgia station-code descriptions say the automatic station has been operating or in operation since a named month/year.",
        ),
        gate(
            "caution",
            "Test-mode or blocker rows",
            sum(row["station_test_mode_flag"] or bool(row["uzbekistan_blocker_type"]) for row in rows),
            "One Georgia row is explicitly test-mode and all three Uzbekistan rows remain stale or sentinel blockers.",
        ),
        gate(
            "not_ready",
            "Station method table",
            0,
            "No public source in this pass gives a complete station-code method table with instrument/method classification.",
        ),
        gate(
            "not_ready",
            "Calibration/status evidence",
            0,
            "No row has explicit public calibration, maintenance, or operating-status closure adequate for grade use.",
        ),
        gate(
            "not_ready",
            "Current-status confirmed",
            0,
            "API presence, station descriptions, and live values are not treated as station-status certification.",
        ),
        gate(
            "not_ready",
            "Complete monitor-grade classification",
            0,
            "No row has complete public station-grade classification.",
        ),
        gate(
            "not_ready",
            "Station-radius grade assumptions",
            0,
            "Station-radius coverage remains blocked until current status, method class, and grade are public and row-level.",
        ),
    ]


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_rows": len(rows),
        "target_georgia_rows": sum(row["iso3"] == "GEO" for row in rows),
        "target_indonesia_rows": sum(row["iso3"] == "IDN" for row in rows),
        "target_uzbekistan_blocker_rows": sum(row["iso3"] == "UZB" for row in rows),
        "source_records_total": len(source_records),
        "source_records_retrieved_or_carried_forward": sum(bool(row["retrieved"]) for row in source_records),
        "exact_station_code_or_id_rows": sum(row["exact_station_code_or_id_found"] for row in rows),
        "georgia_station_code_api_rows": sum(row["station_code_source_lane"] == "georgia_airgov_station_code_api" and row["exact_station_code_or_id_found"] for row in rows),
        "georgia_pm25_equipment_rows": sum(row["iso3"] == "GEO" and row["pm25_row_or_equipment_listed"] for row in rows),
        "georgia_pm25_hourly_observation_rows": sum(row["iso3"] == "GEO" and int(row["pm25_observation_rows"] or 0) > 0 for row in rows),
        "georgia_operating_description_context_rows": sum(row["iso3"] == "GEO" and row["station_description_operating_context"] for row in rows),
        "georgia_test_mode_rows": sum(row["iso3"] == "GEO" and row["station_test_mode_flag"] for row in rows),
        "indonesia_bmkg_payload_station_code_rows": sum(row["iso3"] == "IDN" and row["exact_station_code_or_id_found"] for row in rows),
        "indonesia_bmkg_xml_filename_rows": sum(row["iso3"] == "IDN" and row["bmkg_payload_xml_filename_found"] for row in rows),
        "uzbekistan_unresolved_blocker_rows": sum(row["iso3"] == "UZB" and bool(row["uzbekistan_blocker_type"]) for row in rows),
        "station_method_table_rows": 0,
        "instrument_model_available_rows": sum(row["instrument_model_available"] for row in rows),
        "calibration_status_available_rows": 0,
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    sample_fields = [
        "iso3",
        "source_station_id",
        "source_station_name",
        "station_code_source_lane",
        "pm25_row_or_equipment_listed",
        "pm25_observation_rows",
        "station_description_operating_context",
        "station_test_mode_flag",
        "source_scan_decision",
    ]
    prioritized = sorted(
        rows,
        key=lambda row: (
            row["iso3"] != "GEO",
            row["source_scan_decision"] == "georgia_station_code_test_mode_keep_blocked",
            not row["station_description_operating_context"],
            row["iso3"],
            row["source_station_id"],
        ),
    )
    sample_rows = [
        *[row for row in prioritized if row["iso3"] == "GEO"][:8],
        *[row for row in rows if row["iso3"] == "IDN"][:4],
        *[row for row in rows if row["iso3"] == "UZB"],
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 station-code status/method source scan",
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "public endpoint/page source seed for the live scan",
            },
            {
                "path": str(METHOD_EVIDENCE_CSV.relative_to(PROGRAM_DIR)),
                "role": "source of the 38 Indonesia/Georgia exact PM2.5 portal/API target rows",
            },
            {
                "path": str(ROW_METHOD_SOURCE_CSV.relative_to(PROGRAM_DIR)),
                "role": "prior Indonesia/Georgia row-method source context",
            },
            {
                "path": str(UZB_BLOCKER_CSV.relative_to(PROGRAM_DIR)),
                "role": "prior exact Uzbekistan blocker-row follow-up carried into this stricter scan",
            },
        ],
        "coverage_counts": counts,
        "country_rows": country_rows(rows),
        "decision_counts": [
            {"decision": key, "rows": value}
            for key, value in sorted(Counter(row["source_scan_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gates(rows, source_records),
        "source_records": source_records,
        "station_sample_rows": [{field: row[field] for field in sample_fields} for row in sample_rows],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    targets = target_rows()
    row_method_rows = indexed(read_csv(ROW_METHOD_SOURCE_CSV))
    fetched, source_records = fetch_source_records(generated_at)
    airgov_payload = fetched["airgov_station_code_hourly_api"].get("json")
    stations = station_objects_by_code(airgov_payload)
    bmkg_text = fetched["bmkg_pm25_portal_nuxt_payload"].get("text", "")
    rows = [
        *build_georgia_rows(generated_at, targets, stations, "airgov_station_code_hourly_api"),
        *build_indonesia_rows(generated_at, targets, row_method_rows, bmkg_text, "bmkg_pm25_portal_nuxt_payload"),
        *build_uzbekistan_rows(generated_at, source_records),
    ]
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, source_records))
    counts = Counter(row["source_scan_decision"] for row in rows)
    print(
        "Built station-code status/method source scan: "
        f"{len(rows)} rows; "
        f"{sum(row['iso3'] == 'GEO' and row['exact_station_code_or_id_found'] for row in rows)} Georgia station-code API rows; "
        f"{sum(row['iso3'] == 'IDN' and row['exact_station_code_or_id_found'] for row in rows)} Indonesia payload rows; "
        f"{sum(row['iso3'] == 'UZB' and bool(row['uzbekistan_blocker_type']) for row in rows)} Uzbekistan blockers carried forward; "
        "0 complete grade rows; "
        f"decisions={dict(counts)}."
    )


if __name__ == "__main__":
    main()
