"""Check whether BMKG public PM2.5 APIs add status/certificate evidence.

The previous BMKG passes showed exact station pages, BAM method text, and
source-level SOP/calibration context, but no station-specific status or
certificate closure. This pass follows the official Nuxt app's public token
flow and compares the PM2.5 list/detail APIs for the same 22 target station
codes. The claim gate stays closed unless the API payload exposes explicit
station operational-status, inspection, calibration, certificate, or grade
fields.
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
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SOURCE_SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-api-parity-source-seed.csv"
TARGET_STATUS_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-specific-status-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-api-parity-status.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-api-parity-status-summary.json"

METHOD = "air_monitoring_bmkg_api_parity_status_v1"
STATUS = "computed_bmkg_api_parity_status"
TIMEOUT_SECONDS = 60
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This pass records official BMKG public API telemetry and field presence. "
    "It does not convert a public app token, PM2.5 values, air-quality condition "
    "labels, coordinates, or hourly observations into station operational-status "
    "certification, station-specific inspection logs, calibration certificates, "
    "complete monitor-grade classification, or station-radius readiness."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_station_id",
    "source_station_name",
    "api_list_found",
    "api_list_station_name",
    "api_list_pm25_value",
    "api_list_condition_label",
    "api_list_hour",
    "api_list_lat",
    "api_list_lon",
    "api_detail_retrieved",
    "api_detail_date_raw",
    "api_detail_observation_count",
    "api_detail_latest_hour",
    "api_detail_latest_pm25_value",
    "api_detail_lat",
    "api_detail_lon",
    "api_coordinates_available",
    "api_list_detail_coordinate_match",
    "api_payload_has_station_status_field",
    "api_payload_has_inspection_field",
    "api_payload_has_calibration_field",
    "api_payload_has_certificate_field",
    "api_payload_has_grade_field",
    "api_payload_has_method_field",
    "api_condition_is_air_quality_label_only",
    "current_status_confirmed",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "api_parity_decision",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ")
    text = text.replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("`", "'")
    return re.sub(r"\s+", " ", text).strip()


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


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def fetch_json(
    session: requests.Session,
    url: str,
    *,
    token: str = "",
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "url": url,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "json": None,
        "text": "",
        "error": "",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json,*/*;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    if token:
        headers["X-API-KEY"] = token
    try:
        response = session.get(url, timeout=TIMEOUT_SECONDS, headers=headers, allow_redirects=True)
        result["final_url"] = response.url
        result["http_status"] = response.status_code
        result["content_type"] = response.headers.get("content-type", "")
        result["retrieval_bytes"] = len(response.content)
        result["sha256"] = sha256(response.content)
        result["text"] = normalize(response.text)
        response.raise_for_status()
        payload = response.json()
        result["json"] = payload
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are evidence.
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def seed_url(rows: list[dict[str, str]], key: str) -> str:
    for row in rows:
        if row.get("source_key") == key:
            return normalize(row.get("url"))
    raise KeyError(key)


def station_code_from_file(value: Any) -> str:
    return normalize(value).removesuffix(".xml")


def as_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def coordinate_match(left: Any, right: Any) -> bool:
    lval = as_float(left)
    rval = as_float(right)
    if lval is None or rval is None:
        return False
    return abs(lval - rval) <= 0.00001


def payload_keys(payload: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(payload, dict):
        for key, value in payload.items():
            keys.add(str(key).casefold())
            keys.update(payload_keys(value))
    elif isinstance(payload, list):
        for item in payload:
            keys.update(payload_keys(item))
    return keys


def has_any_key(keys: set[str], terms: list[str]) -> bool:
    return any(any(term in key for term in terms) for key in keys)


def latest_observation(data: Any) -> dict[str, Any]:
    if not isinstance(data, list):
        return {}
    observations = [item for item in data if isinstance(item, dict) and "JAM" in item]
    if not observations:
        return {}
    return max(observations, key=lambda item: as_float(item.get("JAM")) if as_float(item.get("JAM")) is not None else -1)


def source_record(
    source_key: str,
    role: str,
    source: dict[str, Any],
    **extra: Any,
) -> dict[str, Any]:
    return {
        "source_key": source_key,
        "source_role": role,
        "url": source.get("url", ""),
        "final_url": source.get("final_url", ""),
        "retrieved": source.get("retrieved", False),
        "http_status": source.get("http_status", ""),
        "content_type": source.get("content_type", ""),
        "retrieval_bytes": source.get("retrieval_bytes", 0),
        "sha256": source.get("sha256", ""),
        "error": source.get("error", ""),
        **extra,
    }


def build(generated_at: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_seed = read_csv(SOURCE_SEED_CSV)
    targets = read_csv(TARGET_STATUS_CSV)
    session = requests.Session()

    auth_url = seed_url(source_seed, "bmkg_public_auth_token_refresh")
    list_url = seed_url(source_seed, "bmkg_pm25_list_api")
    detail_template = seed_url(source_seed, "bmkg_pm25_detail_api_template")

    source_records: list[dict[str, Any]] = []
    auth_source = fetch_json(session, auth_url)
    auth_json = auth_source.get("json") if isinstance(auth_source.get("json"), dict) else {}
    token = normalize(auth_json.get("token")) if isinstance(auth_json, dict) else ""
    source_records.append(
        source_record(
            "bmkg_public_auth_token_refresh",
            "official_public_app_token",
            auth_source,
            token_obtained=bool(token),
            token_length=len(token),
            token_expires_at=auth_json.get("expiresAt", "") if isinstance(auth_json, dict) else "",
            token_persisted=False,
        )
    )

    list_source = fetch_json(session, list_url, token=token)
    source_records.append(source_record("bmkg_pm25_list_api", "official_pm25_list_api", list_source))
    list_payload = list_source.get("json") if isinstance(list_source.get("json"), list) else []
    list_by_station_id = {
        station_code_from_file(item.get("nama_file")): item
        for item in list_payload
        if isinstance(item, dict) and station_code_from_file(item.get("nama_file"))
    }

    rows: list[dict[str, Any]] = []
    station_rows: list[dict[str, Any]] = []
    total_hourly_observations = 0

    for target in targets:
        station_id = normalize(target.get("source_station_id"))
        station_name = normalize(target.get("source_station_name"))
        detail_url = detail_template.replace("{source_station_id}", station_id)
        detail_source = fetch_json(session, detail_url, token=token)
        source_records.append(
            source_record(
                f"bmkg_pm25_detail_api_{station_id}",
                "official_pm25_detail_api",
                detail_source,
                source_station_id=station_id,
            )
        )
        list_item = list_by_station_id.get(station_id, {})
        detail_payload = detail_source.get("json") if isinstance(detail_source.get("json"), dict) else {}
        detail_data = detail_payload.get("data", []) if isinstance(detail_payload, dict) else []
        latest = latest_observation(detail_data)
        hourly_count = len(detail_data) if isinstance(detail_data, list) else 0
        total_hourly_observations += hourly_count
        keys = payload_keys(detail_payload) | payload_keys(list_item)

        has_status = has_any_key(keys, ["status_operasi", "operasional", "operating_status", "station_status"])
        has_inspection = has_any_key(keys, ["inspection", "inspeksi", "pemeriksaan_harian", "log_pemeriksaan"])
        has_calibration = has_any_key(keys, ["calibration", "kalibrasi", "calibrated"])
        has_certificate = has_any_key(keys, ["certificate", "sertifikat", "cert"])
        has_grade = has_any_key(keys, ["reference_grade", "regulatory_grade", "monitor_grade", "grade"])
        has_method = has_any_key(keys, ["method", "metode", "instrument", "alat", "bam"])

        list_lat = list_item.get("LAT", "") if isinstance(list_item, dict) else ""
        list_lon = list_item.get("LON", "") if isinstance(list_item, dict) else ""
        detail_lat = detail_payload.get("lat", "") if isinstance(detail_payload, dict) else ""
        detail_lon = detail_payload.get("lon", "") if isinstance(detail_payload, dict) else ""
        coordinates_available = all(as_float(value) is not None for value in [list_lat, list_lon, detail_lat, detail_lon])
        coordinate_matches = coordinate_match(list_lat, detail_lat) and coordinate_match(list_lon, detail_lon)

        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "source_station_id": station_id,
            "source_station_name": station_name,
            "api_list_found": bool(list_item),
            "api_list_station_name": normalize(list_item.get("LOKASI")) if isinstance(list_item, dict) else "",
            "api_list_pm25_value": list_item.get("PM25", "") if isinstance(list_item, dict) else "",
            "api_list_condition_label": normalize(list_item.get("KONDISI")) if isinstance(list_item, dict) else "",
            "api_list_hour": list_item.get("JAM", "") if isinstance(list_item, dict) else "",
            "api_list_lat": list_lat,
            "api_list_lon": list_lon,
            "api_detail_retrieved": bool(detail_source.get("retrieved")),
            "api_detail_date_raw": normalize(detail_payload.get("tanggal")) if isinstance(detail_payload, dict) else "",
            "api_detail_observation_count": hourly_count,
            "api_detail_latest_hour": latest.get("JAM", ""),
            "api_detail_latest_pm25_value": latest.get("PM25", ""),
            "api_detail_lat": detail_lat,
            "api_detail_lon": detail_lon,
            "api_coordinates_available": coordinates_available,
            "api_list_detail_coordinate_match": coordinate_matches,
            "api_payload_has_station_status_field": has_status,
            "api_payload_has_inspection_field": has_inspection,
            "api_payload_has_calibration_field": has_calibration,
            "api_payload_has_certificate_field": has_certificate,
            "api_payload_has_grade_field": has_grade,
            "api_payload_has_method_field": has_method,
            "api_condition_is_air_quality_label_only": bool(list_item.get("KONDISI")) if isinstance(list_item, dict) else False,
            "current_status_confirmed": False,
            "station_specific_inspection_log_found": False,
            "station_specific_calibration_certificate_found": False,
            "calibration_status_available": False,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
        }
        if not row["api_detail_retrieved"] or not row["api_list_found"]:
            row["api_parity_decision"] = "api_route_missing_keep_blocked"
            row["reader_use"] = "Use as an API availability blocker: the target station was not complete across BMKG API surfaces."
        elif has_status or has_inspection or has_calibration or has_certificate or has_grade:
            row["api_parity_decision"] = "api_status_field_present_needs_manual_review"
            row["reader_use"] = "Use as a follow-up row: the API payload includes a possible status, inspection, calibration, certificate, or grade field that needs manual interpretation."
        else:
            row["api_parity_decision"] = "api_telemetry_visible_no_status_fields_keep_blocked"
            row["reader_use"] = (
                "Use as API parity evidence: BMKG list/detail endpoints expose live PM2.5 telemetry, "
                "coordinates, date/hour, and air-quality condition labels, but no station-status, "
                "inspection, calibration, certificate, grade, or method fields for this target row."
            )
        row["non_claim"] = NON_CLAIM
        rows.append(row)
        station_rows.append(row)

    list_station_ids = set(list_by_station_id)
    target_station_ids = {normalize(row.get("source_station_id")) for row in targets}
    extra_api_station_rows = [
        {
            "source_station_id": station_id,
            "source_station_name": normalize(item.get("LOKASI")),
            "pm25_value": item.get("PM25", ""),
            "condition": normalize(item.get("KONDISI")),
        }
        for station_id, item in sorted(list_by_station_id.items())
        if station_id not in target_station_ids
    ]

    counts = Counter()
    counts["target_bmkg_rows"] = len(rows)
    counts["source_routes_retrieved"] = sum(1 for source in source_records if source["retrieved"])
    counts["auth_token_endpoint_retrieved"] = 1 if auth_source.get("retrieved") else 0
    counts["auth_token_obtained"] = 1 if token else 0
    counts["pm25_list_api_retrieved"] = 1 if list_source.get("retrieved") else 0
    counts["pm25_list_api_station_rows"] = len(list_payload)
    counts["pm25_list_api_extra_station_rows"] = len(extra_api_station_rows)
    counts["target_station_files_in_list_api_rows"] = sum(bool(row["api_list_found"]) for row in rows)
    counts["target_detail_api_routes_retrieved"] = sum(bool(row["api_detail_retrieved"]) for row in rows)
    counts["target_detail_api_data_rows"] = sum(int(row["api_detail_observation_count"]) > 0 for row in rows)
    counts["target_detail_api_hourly_observation_rows"] = total_hourly_observations
    counts["api_detail_coordinate_rows"] = sum(
        as_float(row.get("api_detail_lat")) is not None and as_float(row.get("api_detail_lon")) is not None
        for row in rows
    )
    counts["api_coordinate_rows"] = sum(bool(row["api_coordinates_available"]) for row in rows)
    counts["api_list_detail_coordinate_match_rows"] = sum(bool(row["api_list_detail_coordinate_match"]) for row in rows)
    counts["api_air_quality_condition_label_rows"] = sum(bool(row["api_condition_is_air_quality_label_only"]) for row in rows)
    counts["api_station_status_field_rows"] = sum(bool(row["api_payload_has_station_status_field"]) for row in rows)
    counts["api_inspection_field_rows"] = sum(bool(row["api_payload_has_inspection_field"]) for row in rows)
    counts["api_calibration_field_rows"] = sum(bool(row["api_payload_has_calibration_field"]) for row in rows)
    counts["api_certificate_field_rows"] = sum(bool(row["api_payload_has_certificate_field"]) for row in rows)
    counts["api_grade_field_rows"] = sum(bool(row["api_payload_has_grade_field"]) for row in rows)
    counts["api_method_field_rows"] = sum(bool(row["api_payload_has_method_field"]) for row in rows)
    counts["current_status_confirmed_rows"] = 0
    counts["station_specific_inspection_log_rows"] = 0
    counts["station_specific_calibration_certificate_rows"] = 0
    counts["calibration_status_available_rows"] = 0
    counts["complete_monitor_grade_classification_rows"] = 0
    counts["station_radius_grade_assumption_ready_rows"] = 0

    sorted_station_rows = sorted(
        station_rows,
        key=lambda row: as_float(row.get("api_detail_latest_pm25_value")) or -1,
        reverse=True,
    )
    decision_counts = [
        {"decision": decision, "rows": count}
        for decision, count in Counter(row["api_parity_decision"] for row in rows).most_common()
    ]
    evidence_gates = [
        {
            "gate": "Public app token obtained",
            "status": "available" if token else "not_ready",
            "rows": counts["auth_token_obtained"],
            "reader_use": "The official Nuxt app token flow can be reproduced without persisting the transient token.",
        },
        {
            "gate": "PM2.5 list API retrieved",
            "status": "available" if list_source.get("retrieved") else "not_ready",
            "rows": counts["pm25_list_api_station_rows"],
            "reader_use": "The list API exposes public station file, location, coordinate, hour, PM2.5, and condition rows.",
        },
        {
            "gate": "Target station files in list API",
            "status": "available",
            "rows": counts["target_station_files_in_list_api_rows"],
            "reader_use": "Target BMKG station codes are visible as official PM2.5 XML file rows in the list API.",
        },
        {
            "gate": "Target detail APIs retrieved",
            "status": "available",
            "rows": counts["target_detail_api_routes_retrieved"],
            "reader_use": "Expanded station detail APIs return public date/hour PM2.5 time series for target rows.",
        },
        {
            "gate": "Coordinate fields visible",
            "status": "available",
            "rows": counts["api_detail_coordinate_rows"],
            "reader_use": "Coordinates are visible in station detail APIs, but that is not status or grade certification.",
        },
        {
            "gate": "List/detail coordinate parity",
            "status": "partly_available",
            "rows": counts["api_list_detail_coordinate_match_rows"],
            "reader_use": "Most target rows match between list and detail API coordinates; one target detail route is not present in the list API.",
        },
        {
            "gate": "Air-quality condition labels",
            "status": "available",
            "rows": counts["api_air_quality_condition_label_rows"],
            "reader_use": "KONDISI labels classify PM2.5 air quality, not station operating status.",
        },
        {
            "gate": "Station-status API fields",
            "status": "not_ready",
            "rows": counts["api_station_status_field_rows"],
            "reader_use": "No target API payload exposes an explicit station operational-status field.",
        },
        {
            "gate": "Calibration/certificate API fields",
            "status": "not_ready",
            "rows": counts["api_calibration_field_rows"] + counts["api_certificate_field_rows"],
            "reader_use": "No target API payload exposes calibration status or certificate fields.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Telemetry fields do not provide complete station-level monitor-grade classification.",
        },
        {
            "gate": "Station-radius readiness",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "API telemetry does not make any BMKG row station-radius ready.",
        },
    ]

    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 candidate evidence hardening",
        "source_scope": (
            "Official BMKG public Nuxt token flow, PM2.5 list API, and PM2.5 detail APIs "
            "for the 22 BMKG station-specific status-audit target rows."
        ),
        "coverage_counts": dict(counts),
        "decision_counts": decision_counts,
        "evidence_gate_counts": evidence_gates,
        "station_rows": sorted_station_rows,
        "station_sample_rows": sorted_station_rows[:12],
        "extra_api_station_rows": extra_api_station_rows,
        "source_records": source_records,
        "non_claim": NON_CLAIM,
    }
    return rows, summary


def main() -> None:
    generated_at = now_iso()
    rows, summary = build(generated_at)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")
    print(json.dumps(summary["coverage_counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
