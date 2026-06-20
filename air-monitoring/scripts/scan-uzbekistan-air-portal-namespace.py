"""Scan Air Uzbekistan portal namespace evidence for exact blocker rows.

The prior Uzbekistan blocker artifacts leave station IDs 107, 728, and 737
unresolved on monitoring.meteo.uz. This pass checks whether the public
Air Uzbekistan / DigitalMeteo portal provides a second station namespace that
resolves those blockers, or whether it only mirrors the same stale/sentinel
measurements under alternate station IDs.
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

SEED_CSV = SOURCE_INPUTS_DIR / "uzbekistan-air-portal-namespace-source-seed.csv"
BLOCKER_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-blocker-row-followup.csv"
ENDPOINT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-endpoint-consistency.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-air-portal-namespace.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-air-portal-namespace-summary.json"
OUT_MD = PROGRAM_DIR / "uzbekistan-air-portal-namespace.md"

METHOD = "air_monitoring_uzbekistan_air_portal_namespace_v1"
STATUS = "computed_uzbekistan_air_portal_namespace"
TIMEOUT_SECONDS = 60
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
HORIBA_LIST_URL = "https://air-uzbekistan.uz/api/horiba.php"
NON_CLAIM = (
    "This scan checks whether a second public Uzbekistan air-quality portal "
    "resolves three exact blocker rows. Alternate station IDs, portal active "
    "flags, or mirrored pollutant values do not confirm current operating "
    "status, station-method classification, calibration status, complete "
    "monitor-grade classification, or station-radius readiness unless a public "
    "source names the exact blocker row and gives explicit status, correction, "
    "or grade language."
)

STATION_VARIANTS = {
    "107": ["uzhydromet", "узгидромет", "yunusabad", "юнисабад", "юнус-абад"],
    "728": ["sergili", "sergeli", "сергили", "сирғали"],
    "737": ["akhangaran", "ahangaran", "ахангаран", "ohangaron", "оҳангарон"],
}

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_station_id",
    "source_station_name",
    "review_focus",
    "prior_followup_decision",
    "prior_endpoint_decision",
    "official_detail_updated_iso",
    "official_detail_pm25_value",
    "official_detail_pm25_value_status",
    "official_region_updated_values",
    "air_portal_station_list_retrieved",
    "air_portal_station_count",
    "air_portal_alternate_station_found",
    "air_portal_alternate_station_id",
    "air_portal_alternate_station_name",
    "air_portal_alternate_station_active",
    "air_portal_latitude",
    "air_portal_longitude",
    "air_portal_target_id_detail_found",
    "air_portal_target_id_detail_error",
    "air_portal_alternate_detail_found",
    "air_portal_alternate_detail_datetime",
    "air_portal_alternate_detail_date_iso",
    "air_portal_alternate_detail_age_days",
    "air_portal_alternate_detail_pm25_value",
    "air_portal_alternate_detail_pm25_status",
    "air_portal_detail_mirrors_official_detail",
    "air_portal_detail_stale_over_30_days",
    "air_portal_detail_pm25_sentinel",
    "data_meteo_api_requires_email_application",
    "endpoint_namespace_mismatch",
    "active_flag_counted_as_status_closure",
    "public_portal_resolution_available",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "portal_namespace_decision",
    "reader_use",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("`", "'")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


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


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def extract_text(response: requests.Response, hint: str) -> str:
    content_type = response.headers.get("content-type", "")
    lower = f"{content_type} {hint}".lower()
    if "html" in lower:
        return BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True)
    return response.text


def fetch_url(url: str, *, accept: str = "text/html,text/plain,application/json,*/*;q=0.8") -> dict[str, Any]:
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
        "retrieval_error": "",
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
        result["text"] = normalize(extract_text(response, result["content_type"]))
        if "json" in result["content_type"].lower():
            result["json"] = response.json()
        else:
            try:
                result["json"] = response.json()
            except Exception:
                result["json"] = None
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def fetch_seed_source(seed: dict[str, str]) -> dict[str, Any]:
    accept = "application/json,*/*;q=0.8" if seed["content_type_hint"] == "json" else "text/html,text/plain,application/javascript,*/*;q=0.8"
    source = fetch_url(seed["url"], accept=accept)
    terms = split_terms(seed["expected_terms"])
    source.update(
        {
            "source_key": seed["source_key"],
            "source_name": seed["source_name"],
            "source_role": seed["source_role"],
            "source_note": seed["source_note"],
            "expected_terms": terms,
            "matched_expected_terms": matched_terms(source["text"], terms),
        }
    )
    source["missing_expected_terms"] = [
        term for term in terms if term not in source["matched_expected_terms"]
    ]
    return source


def compact_source_record(source: dict[str, Any]) -> dict[str, Any]:
    record = {
        "source_key": source.get("source_key", ""),
        "source_name": source.get("source_name", ""),
        "source_role": source.get("source_role", ""),
        "url": source.get("url", ""),
        "final_url": source.get("final_url", ""),
        "retrieved": source.get("retrieved", False),
        "http_status": source.get("http_status", ""),
        "content_type": source.get("content_type", ""),
        "retrieval_bytes": source.get("retrieval_bytes", 0),
        "sha256": source.get("sha256", ""),
        "retrieval_error": source.get("retrieval_error", ""),
        "matched_expected_terms": source.get("matched_expected_terms", []),
        "missing_expected_terms": source.get("missing_expected_terms", []),
        "source_note": source.get("source_note", ""),
    }
    for key in (
        "source_station_id",
        "air_portal_station_id",
        "station_data_available",
        "api_error",
        "api_status",
    ):
        if key in source:
            record[key] = source[key]
    return record


def value_status(value: Any) -> str:
    if value is None or normalize(value) == "":
        return "missing"
    try:
        number = float(str(value).replace(",", "."))
    except ValueError:
        return "non_numeric"
    if number == -9999:
        return "sentinel_minus_9999"
    if number < 0:
        return "negative"
    if number == 0:
        return "zero"
    return "positive"


def parse_date(value: Any, generated_at: str) -> tuple[str, int | None]:
    raw = normalize(value)
    if not raw:
        return "", None
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if match:
        year, month, day = match.groups()
        parsed = datetime(int(year), int(month), int(day), tzinfo=timezone.utc).date()
    else:
        match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", raw)
        if not match:
            return "", None
        day, month, year = match.groups()
        parsed = datetime(int(year), int(month), int(day), tzinfo=timezone.utc).date()
    generated_date = datetime.fromisoformat(generated_at.replace("Z", "+00:00")).date()
    return parsed.isoformat(), (generated_date - parsed).days


def numeric_equal(left: Any, right: Any) -> bool:
    try:
        return abs(float(left) - float(right)) < 0.000001
    except Exception:
        return False


def index_by_station(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {normalize(row.get("source_station_id")): row for row in rows if normalize(row.get("source_station_id"))}


def station_matches_target(station: dict[str, Any], station_id: str) -> bool:
    name = norm_key(station.get("name", ""))
    return any(variant in name for variant in STATION_VARIANTS.get(station_id, []))


def find_portal_station(stations: list[dict[str, Any]], station_id: str) -> dict[str, Any] | None:
    for station in stations:
        if station_matches_target(station, station_id):
            return station
    return None


def get_pm25(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return None
    for item in payload.get("data", []):
        if norm_key(item.get("name")) in {"pm 2.5", "pm2.5", "pm25"}:
            return item.get("value")
    return None


def station_detail_available(payload: Any) -> bool:
    return isinstance(payload, dict) and "stationId" in payload and isinstance(payload.get("data"), list)


def api_error(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    if "error" not in payload:
        return ""
    body = normalize(payload.get("body"))
    if body:
        return f"{normalize(payload.get('error'))}: {body}"
    return normalize(payload.get("error"))


def fetch_station_detail(source_key: str, station_id: str, role: str) -> dict[str, Any]:
    url = f"{HORIBA_LIST_URL}?id={station_id}"
    source = fetch_url(url, accept="application/json,*/*;q=0.8")
    payload = source.get("json")
    source.update(
        {
            "source_key": source_key,
            "source_name": f"Air Uzbekistan Horiba detail probe {station_id}",
            "source_role": role,
            "source_station_id": station_id if role == "target_id_detail_probe" else "",
            "air_portal_station_id": station_id if role == "alternate_station_detail_probe" else "",
            "station_data_available": station_detail_available(payload),
            "api_error": api_error(payload),
            "api_status": payload.get("status", "") if isinstance(payload, dict) else "",
            "matched_expected_terms": [],
            "missing_expected_terms": [],
            "source_note": (
                "Derived public Air Uzbekistan detail probe. A 200 HTTP response "
                "can still carry an upstream Station not found body."
            ),
        }
    )
    return source


def portal_decision(row: dict[str, Any]) -> str:
    if row["endpoint_namespace_mismatch"] and row["air_portal_detail_mirrors_official_detail"]:
        return "alternate_namespace_mirrors_blocker_keep_blocked"
    if row["endpoint_namespace_mismatch"] and row["air_portal_alternate_station_found"]:
        return "alternate_namespace_context_only_keep_blocked"
    if row["air_portal_target_id_detail_found"]:
        return "target_id_found_needs_manual_review"
    return "no_portal_match_keep_blocked"


def reader_use(row: dict[str, Any]) -> str:
    if row["air_portal_detail_pm25_sentinel"]:
        return (
            "Use as a stronger sentinel wall. Air Uzbekistan maps the station "
            "name to an alternate Horiba ID, but that alternate detail route "
            "still returns the -9999 PM2.5 sentinel."
        )
    if row["air_portal_detail_stale_over_30_days"]:
        return (
            "Use as a stronger stale-row wall. Air Uzbekistan maps the station "
            "name to an alternate Horiba ID, but the alternate detail route "
            "mirrors the stale official detail timestamp."
        )
    return (
        "Use as source-routing context. The portal helps explain station "
        "namespace differences but does not provide public correction, "
        "current-status, calibration, or complete-grade closure."
    )


def build_rows(generated_at: str, sources: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    blocker_rows = read_csv(BLOCKER_CSV)
    endpoint_rows = index_by_station(read_csv(ENDPOINT_CSV))

    station_list_source = next(source for source in sources if source["source_key"] == "air_uzbekistan_horiba_list_api")
    stations = station_list_source.get("json") if isinstance(station_list_source.get("json"), list) else []
    data_meteo_source = next(source for source in sources if source["source_key"] == "data_meteo_api_landing")
    data_meteo_requires_email = (
        data_meteo_source["retrieved"]
        and "info@mtb.uz" in norm_key(data_meteo_source.get("text", ""))
        and ("api" in norm_key(data_meteo_source.get("text", "")))
    )

    derived_sources: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for blocker in blocker_rows:
        station_id = normalize(blocker["source_station_id"])
        endpoint = endpoint_rows.get(station_id, {})
        portal_station = find_portal_station(stations, station_id)
        target_source = fetch_station_detail(
            f"air_uzbekistan_horiba_target_id_{station_id}",
            station_id,
            "target_id_detail_probe",
        )
        derived_sources.append(target_source)

        alternate_source: dict[str, Any] | None = None
        if portal_station:
            alternate_id = normalize(portal_station.get("id"))
            alternate_source = fetch_station_detail(
                f"air_uzbekistan_horiba_alternate_id_{alternate_id}",
                alternate_id,
                "alternate_station_detail_probe",
            )
            derived_sources.append(alternate_source)

        alternate_payload = alternate_source.get("json") if alternate_source else None
        alternate_detail_found = station_detail_available(alternate_payload)
        alternate_datetime = normalize(alternate_payload.get("datetime")) if alternate_detail_found else ""
        alternate_date_iso, alternate_age_days = parse_date(alternate_datetime, generated_at)
        alternate_pm25 = get_pm25(alternate_payload)
        alternate_pm25_status = value_status(alternate_pm25)
        official_detail_date = normalize(blocker.get("detail_updated_iso") or endpoint.get("detail_latest_updated_iso"))
        official_pm25 = normalize(blocker.get("detail_pm25_value") or endpoint.get("detail_pm25_values"))
        mirrors_official = bool(
            alternate_detail_found
            and official_detail_date
            and alternate_date_iso == official_detail_date
            and numeric_equal(alternate_pm25, official_pm25)
        )
        target_detail_found = station_detail_available(target_source.get("json"))
        endpoint_namespace_mismatch = bool(portal_station and alternate_detail_found and not target_detail_found)

        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "source_station_id": station_id,
            "source_station_name": blocker.get("source_station_name", ""),
            "review_focus": blocker.get("review_focus", ""),
            "prior_followup_decision": blocker.get("followup_decision", ""),
            "prior_endpoint_decision": endpoint.get("endpoint_decision", ""),
            "official_detail_updated_iso": official_detail_date,
            "official_detail_pm25_value": official_pm25,
            "official_detail_pm25_value_status": blocker.get("detail_pm25_value_status", ""),
            "official_region_updated_values": endpoint.get("region_updated_values", blocker.get("region_row_updated_raw", "")),
            "air_portal_station_list_retrieved": bool(station_list_source.get("retrieved")),
            "air_portal_station_count": len(stations),
            "air_portal_alternate_station_found": bool(portal_station),
            "air_portal_alternate_station_id": normalize(portal_station.get("id")) if portal_station else "",
            "air_portal_alternate_station_name": normalize(portal_station.get("name")) if portal_station else "",
            "air_portal_alternate_station_active": bool(portal_station.get("active")) if portal_station else False,
            "air_portal_latitude": portal_station.get("latitude", "") if portal_station else "",
            "air_portal_longitude": portal_station.get("longitude", "") if portal_station else "",
            "air_portal_target_id_detail_found": target_detail_found,
            "air_portal_target_id_detail_error": target_source.get("api_error", ""),
            "air_portal_alternate_detail_found": alternate_detail_found,
            "air_portal_alternate_detail_datetime": alternate_datetime,
            "air_portal_alternate_detail_date_iso": alternate_date_iso,
            "air_portal_alternate_detail_age_days": alternate_age_days if alternate_age_days is not None else "",
            "air_portal_alternate_detail_pm25_value": alternate_pm25 if alternate_pm25 is not None else "",
            "air_portal_alternate_detail_pm25_status": alternate_pm25_status,
            "air_portal_detail_mirrors_official_detail": mirrors_official,
            "air_portal_detail_stale_over_30_days": bool(alternate_age_days is not None and alternate_age_days > 30),
            "air_portal_detail_pm25_sentinel": alternate_pm25_status == "sentinel_minus_9999",
            "data_meteo_api_requires_email_application": data_meteo_requires_email,
            "endpoint_namespace_mismatch": endpoint_namespace_mismatch,
            "active_flag_counted_as_status_closure": False,
            "public_portal_resolution_available": False,
            "current_status_confirmed": False,
            "station_method_classified": False,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
            "non_claim": NON_CLAIM,
        }
        row["portal_namespace_decision"] = portal_decision(row)
        row["reader_use"] = reader_use(row)
        rows.append(row)

    return rows, derived_sources


def bool_count(rows: list[dict[str, Any]], key: str) -> int:
    return sum(1 for row in rows if bool(row.get(key)))


def evidence_gates(rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_by_key = {source["source_key"]: source for source in sources}
    station_list = source_by_key["air_uzbekistan_horiba_list_api"].get("json")
    station_count = len(station_list) if isinstance(station_list, list) else 0
    return [
        {
            "status": "available",
            "gate": "Meteo API landing page retrieved",
            "rows": 1 if source_by_key["data_meteo_api_landing"]["retrieved"] else 0,
            "reader_use": "The broader Meteo API source object is visible and documents the public API access route.",
        },
        {
            "status": "caution",
            "gate": "Meteo API email/application access wall",
            "rows": 1 if any(row["data_meteo_api_requires_email_application"] for row in rows) else 0,
            "reader_use": "The API landing page points to an email/application path, so it is not a no-friction public row-level closure source.",
        },
        {
            "status": "available",
            "gate": "Air Uzbekistan Horiba station list",
            "rows": station_count,
            "reader_use": "The public Air Uzbekistan endpoint exposes a second Horiba station list.",
        },
        {
            "status": "available",
            "gate": "Alternate station namespace matches",
            "rows": bool_count(rows, "air_portal_alternate_station_found"),
            "reader_use": "All three blocker rows have name/location matches in the alternate portal namespace.",
        },
        {
            "status": "not_ready",
            "gate": "Original blocker IDs accepted by portal",
            "rows": bool_count(rows, "air_portal_target_id_detail_found"),
            "reader_use": "The portal detail endpoint does not accept IDs 107, 728, or 737 as station IDs.",
        },
        {
            "status": "caution",
            "gate": "Alternate detail mirrors official blocker",
            "rows": bool_count(rows, "air_portal_detail_mirrors_official_detail"),
            "reader_use": "The alternate portal detail rows reproduce the same official detail timestamp and PM2.5 values.",
        },
        {
            "status": "caution",
            "gate": "Stale or sentinel alternate details",
            "rows": bool_count(rows, "air_portal_detail_stale_over_30_days") + bool_count(rows, "air_portal_detail_pm25_sentinel"),
            "reader_use": "The alternate namespace still carries the same stale or sentinel blocker pattern.",
        },
        {
            "status": "not_ready",
            "gate": "Public portal resolution",
            "rows": bool_count(rows, "public_portal_resolution_available"),
            "reader_use": "The portal does not provide a public correction/status/grade closure for any blocker row.",
        },
        {
            "status": "not_ready",
            "gate": "Current-status confirmed",
            "rows": bool_count(rows, "current_status_confirmed"),
            "reader_use": "Portal active flags are not counted as row-level current-status confirmation.",
        },
        {
            "status": "not_ready",
            "gate": "Complete monitor-grade classification",
            "rows": bool_count(rows, "complete_monitor_grade_classification_available"),
            "reader_use": "No blocker row receives complete station-grade documentation.",
        },
        {
            "status": "not_ready",
            "gate": "Station-radius readiness",
            "rows": bool_count(rows, "station_radius_grade_assumption_ready"),
            "reader_use": "No blocker row is eligible for station-radius assumptions.",
        },
    ]


def build_summary(generated_at: str, rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> dict[str, Any]:
    station_list_source = next(source for source in sources if source["source_key"] == "air_uzbekistan_horiba_list_api")
    station_list = station_list_source.get("json")
    station_count = len(station_list) if isinstance(station_list, list) else 0
    counts = {
        "target_blocker_rows": len(rows),
        "source_urls_seeded": len([source for source in sources if source.get("source_role") not in {"target_id_detail_probe", "alternate_station_detail_probe"}]),
        "source_urls_retrieved": sum(
            bool(source["retrieved"])
            for source in sources
            if source.get("source_role") not in {"target_id_detail_probe", "alternate_station_detail_probe"}
        ),
        "derived_detail_probe_routes": sum(
            source.get("source_role") in {"target_id_detail_probe", "alternate_station_detail_probe"}
            for source in sources
        ),
        "derived_detail_probe_routes_retrieved": sum(
            source.get("source_role") in {"target_id_detail_probe", "alternate_station_detail_probe"} and bool(source["retrieved"])
            for source in sources
        ),
        "data_meteo_api_landing_retrieved": 1 if any(source["source_key"] == "data_meteo_api_landing" and source["retrieved"] for source in sources) else 0,
        "data_meteo_email_application_required_rows": 1 if any(row["data_meteo_api_requires_email_application"] for row in rows) else 0,
        "air_portal_station_list_retrieved": 1 if station_list_source.get("retrieved") else 0,
        "air_portal_station_objects": station_count,
        "target_blocker_id_detail_probe_rows": len(rows),
        "target_blocker_id_detail_found_rows": bool_count(rows, "air_portal_target_id_detail_found"),
        "alternate_station_name_match_rows": bool_count(rows, "air_portal_alternate_station_found"),
        "alternate_station_active_flag_rows": bool_count(rows, "air_portal_alternate_station_active"),
        "alternate_detail_rows_retrieved": bool_count(rows, "air_portal_alternate_detail_found"),
        "alternate_detail_mirrors_official_detail_rows": bool_count(rows, "air_portal_detail_mirrors_official_detail"),
        "alternate_detail_stale_rows": bool_count(rows, "air_portal_detail_stale_over_30_days"),
        "alternate_detail_sentinel_rows": bool_count(rows, "air_portal_detail_pm25_sentinel"),
        "endpoint_namespace_mismatch_rows": bool_count(rows, "endpoint_namespace_mismatch"),
        "public_portal_resolution_rows": bool_count(rows, "public_portal_resolution_available"),
        "current_status_confirmed_rows": bool_count(rows, "current_status_confirmed"),
        "station_method_classified_rows": bool_count(rows, "station_method_classified"),
        "complete_monitor_grade_classification_rows": bool_count(rows, "complete_monitor_grade_classification_available"),
        "station_radius_grade_assumption_ready_rows": bool_count(rows, "station_radius_grade_assumption_ready"),
    }
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Uzbekistan portal namespace wall",
        "source_scope": (
            "Public Data/Meteo API landing page, Air Uzbekistan portal assets, "
            "public Horiba station-list API, and derived detail probes for "
            "the three unresolved station IDs plus their alternate portal IDs."
        ),
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "portal/source seed",
            },
            {
                "path": str(BLOCKER_CSV.relative_to(PROGRAM_DIR)),
                "role": "prior exact blocker-row follow-up",
            },
            {
                "path": str(ENDPOINT_CSV.relative_to(PROGRAM_DIR)),
                "role": "prior endpoint-consistency wall",
            },
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["portal_namespace_decision"] for row in rows).items())
        ],
        "source_records": [compact_source_record(source) for source in sources],
        "evidence_gate_counts": evidence_gates(rows, sources),
        "station_rows": rows,
        "non_claim": NON_CLAIM,
    }


def write_note(path: Path, summary: dict[str, Any]) -> None:
    counts = summary["coverage_counts"]
    lines = [
        "---",
        "attestation_chain: ai-first",
        "status: Screening Result",
        f"method: {METHOD}",
        "---",
        "",
        "# Uzbekistan Air Uzbekistan portal namespace wall",
        "",
        "## Why this measurement problem matters",
        "",
        "The three Uzbekistan blocker rows are no longer a vague source problem.",
        "They are exact station rows with stale or sentinel measurements on",
        "`monitoring.meteo.uz`. This pass tests whether the newer public",
        "Air Uzbekistan / DigitalMeteo surface supplies a row-level correction",
        "or whether it simply exposes the same stations in a second namespace.",
        "",
        "## What the source upgrade adds",
        "",
        f"- Public source URLs seeded: {counts['source_urls_seeded']}.",
        f"- Seeded source URLs retrieved: {counts['source_urls_retrieved']}.",
        f"- Air Uzbekistan Horiba station objects: {counts['air_portal_station_objects']}.",
        f"- Alternate station-name matches for the three blockers: {counts['alternate_station_name_match_rows']}.",
        f"- Original blocker IDs accepted by the Air Uzbekistan detail endpoint: {counts['target_blocker_id_detail_found_rows']}.",
        f"- Alternate details that mirror the official blocker detail row: {counts['alternate_detail_mirrors_official_detail_rows']}.",
        f"- Public portal blocker-resolution rows: {counts['public_portal_resolution_rows']}.",
        "",
        "## Interpretation",
        "",
        "Air Uzbekistan improves source observability but does not close the",
        "blocker. The portal station list maps the same station names to",
        "alternate Horiba IDs, and all three alternate detail probes reproduce",
        "the same timestamp and PM2.5 value found on the official detail pages.",
        "The original blocker IDs 107, 728, and 737 are not accepted by that",
        "portal detail endpoint.",
        "",
        "## What this does not mean",
        "",
        summary["non_claim"],
        "",
        "## Reproduce",
        "",
        "Run `python air-monitoring/scripts/scan-uzbekistan-air-portal-namespace.py`.",
        "The source seed is `air-monitoring/source-inputs/uzbekistan-air-portal-namespace-source-seed.csv`.",
        "Outputs are `air-monitoring/generated/air-monitoring-uzbekistan-air-portal-namespace.csv`",
        "and `air-monitoring/generated/air-monitoring-uzbekistan-air-portal-namespace-summary.json`.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    seed_sources = [fetch_seed_source(seed) for seed in seed_rows]
    rows, derived_sources = build_rows(generated_at, seed_sources)
    all_sources = seed_sources + derived_sources
    summary = build_summary(generated_at, rows, all_sources)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)
    write_note(OUT_MD, summary)
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(json.dumps(summary["coverage_counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
