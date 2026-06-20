"""Scan the official BMKG CEWS PM2.5 dashboard for current status evidence.

The BMKG station-detail and API passes made telemetry visible but did not expose
an explicit status field. The regional source scan found one station-specific
ONLINE row outside those central pages. This pass uses the official BMKG climate
page and its embedded CEWS PM2.5 dashboard, which contains a public
``dashboardData`` object with station names, coordinates, latest timestamp,
PM2.5 value, category, and status.

The dashboard can support current dashboard-status evidence when a target row has
an exact dashboard location match, explicit ``ONLINE`` status, and a recent
timestamp. It still does not certify station-specific inspection logs,
calibration certificates, complete monitor-grade classification, same-station
OpenAQ joins, or station-radius readiness.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-dashboard-status-source-seed.csv"
BMKG_STATUS_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-specific-status-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-dashboard-status-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-dashboard-status-source-scan-summary.json"

METHOD = "air_monitoring_bmkg_dashboard_status_source_scan_v1"
STATUS = "computed_bmkg_dashboard_status_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 120
CURRENTNESS_WINDOW_HOURS = 30 * 24
NON_CLAIM = (
    "This scan records the official BMKG climate-information parent page and "
    "the embedded CEWS PM2.5 dashboardData object for the 22 BMKG target rows. "
    "A dashboard row with explicit ONLINE status and a recent timestamp can "
    "support current dashboard-status evidence. It does not certify "
    "station-specific inspection logs, calibration certificates or calibration "
    "status, complete monitor-grade classification, same-station OpenAQ joins, "
    "or station-radius readiness."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_dashboard_status_scan_id",
    "source_station_id",
    "source_station_name",
    "dashboard_location_key",
    "dashboard_location_found",
    "dashboard_status_raw",
    "dashboard_timestamp_raw",
    "dashboard_timestamp_iso",
    "dashboard_timestamp_age_hours",
    "dashboard_timestamp_current_within_30_days",
    "dashboard_pm25_ug_m3",
    "dashboard_category_raw",
    "dashboard_latitude",
    "dashboard_longitude",
    "dashboard_timeseries_points",
    "dashboard_positive_observation_count",
    "dashboard_zero_observation_count",
    "dashboard_last_label",
    "explicit_dashboard_online",
    "explicit_dashboard_delayed",
    "current_status_confirmed",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "dashboard_status_decision",
    "reader_use",
    "non_claim",
]

DASHBOARD_LOCATION_ALIASES = {
    "pm25_bjb2": ["BANJARBARU"],
    "pm25_btm2": ["BATAM"],
    "pm25_idp2": ["INDRAPURI"],
    "pm25_jm3": ["KOTA JAMBI"],
    "pm25_jm4": ["MUARO JAMBI"],
    "pm25_kmy3": ["KEMAYORAN"],
    "pm25_ktb2": ["KOTOTABANG", "BUKIT KOTOTABANG"],
    "pm25_mdn2": ["MEDAN"],
    "pm25_mrs": ["MAROS"],
    "pm25_msg": ["PESAWARAN"],
    "pm25_pbb": ["BENGKULU"],
    "pm25_pk2": ["PEKANBARU"],
    "pm25_pl3": ["TALANG BETUTU PALEMBANG", "PALEMBANG (TALANG BETUTU)"],
    "pm25_plb4": ["MUSI 2 PALEMBANG", "PALEMBANG (MUSI 2)"],
    "pm25_pr2": ["PALANGKARAYA", "PALANGKA RAYA"],
    "pm25_ptn2": ["MEMPAWAH"],
    "pm25_sm2": ["SAMARINDA"],
    "pm25_smg": ["SEMARANG"],
    "pm25_spd": ["KUBU RAYA"],
    "pm25_srg": ["SORONG"],
    "pm25_tj2": ["TANJUNG HARAPAN"],
    "pm25_yky": ["SLEMAN"],
}

TIMEZONE_OFFSETS = {
    "WIB": timezone(timedelta(hours=7)),
    "WITA": timezone(timedelta(hours=8)),
    "WIT": timezone(timedelta(hours=9)),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ").replace("\u200b", "")
    text = text.replace("ʻ", "'").replace("‘", "'").replace("’", "'").replace("`", "'")
    text = text.replace("µ", "u").replace("μ", "u")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def dashboard_key(value: Any) -> str:
    text = normalize(value).upper()
    text = text.replace("(", "").replace(")", "")
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


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def fetch_html(url: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "url": url,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "html": "",
        "text": "",
        "retrieval_error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
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
        html = response.text
        result["html"] = html
        result["text"] = normalize(BeautifulSoup(html, "html.parser").get_text(" ", strip=True))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def parse_dashboard_data(html: str) -> dict[str, Any]:
    marker = "const dashboardData ="
    start = html.find(marker)
    if start < 0:
        return {}
    payload = html[start + len(marker) :].lstrip()
    decoder = json.JSONDecoder()
    try:
        data, _ = decoder.raw_decode(payload)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    locations = data.get("locations", {})
    return locations if isinstance(locations, dict) else {}


def parse_dashboard_timestamp(value: str, tz_raw: str) -> str:
    if not value:
        return ""
    tz = TIMEZONE_OFFSETS.get(str(tz_raw or "").upper(), timezone.utc)
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz)
    except ValueError:
        return ""
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def age_hours(timestamp_iso: str, now: datetime) -> float | None:
    if not timestamp_iso:
        return None
    parsed = datetime.fromisoformat(timestamp_iso.replace("Z", "+00:00"))
    return round((now - parsed).total_seconds() / 3600, 2)


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(BMKG_STATUS_CSV)
    unique: dict[str, dict[str, str]] = {}
    for row in rows:
        station_id = row.get("source_station_id", "")
        if station_id:
            unique[station_id] = row
    return list(unique.values())


def match_location(station_id: str, station_name: str, locations: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    keyed_locations = {dashboard_key(key): (key, value) for key, value in locations.items()}
    aliases = DASHBOARD_LOCATION_ALIASES.get(station_id, [station_name])
    for alias in aliases:
        candidate = keyed_locations.get(dashboard_key(alias))
        if candidate:
            return candidate
    return "", None


def fetch_sources(seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for seed in seed_rows:
        fetched = fetch_html(seed["url"])
        text_for_match = f"{fetched['html']} {fetched['text']}"
        sources.append(
            {
                **seed,
                **fetched,
                "matched_expected_terms": "||".join(matched_terms(text_for_match, split_terms(seed.get("expected_terms", "")))),
            }
        )
    return sources


def build_rows(generated_at: str, sources: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    now = datetime.now(timezone.utc)
    dashboard_source = next(
        (
            source
            for source in sources
            if source["retrieved"] and source["source_role"] == "official_cews_pm25_dashboard_data"
        ),
        None,
    )
    locations = parse_dashboard_data(dashboard_source["html"]) if dashboard_source else {}
    rows: list[dict[str, Any]] = []

    for target in target_rows():
        station_id = target["source_station_id"]
        station_name = target["source_station_name"]
        location_key, location = match_location(station_id, station_name, locations)
        latest = location.get("latest", {}) if isinstance(location, dict) else {}
        timeseries = location.get("timeseries", {}) if isinstance(location, dict) else {}
        values = timeseries.get("values", []) if isinstance(timeseries, dict) else []
        labels = timeseries.get("labels", []) if isinstance(timeseries, dict) else []
        status_raw = normalize(latest.get("status", "")).upper()
        timestamp_raw = normalize(latest.get("timestamp", ""))
        timestamp_iso = parse_dashboard_timestamp(timestamp_raw, latest.get("timezone", ""))
        hours_old = age_hours(timestamp_iso, now)
        current_timestamp = hours_old is not None and -24 <= hours_old <= CURRENTNESS_WINDOW_HOURS
        explicit_online = status_raw == "ONLINE"
        explicit_delayed = status_raw == "DELAYED"
        current_status_confirmed = bool(location and explicit_online and current_timestamp)

        numeric_values = [value for value in values if isinstance(value, (int, float))]
        positive_count = sum(1 for value in numeric_values if value > 0)
        zero_count = sum(1 for value in numeric_values if value == 0)

        if current_status_confirmed:
            decision = "dashboard_online_current_but_grade_still_blocked"
            reader_use = (
                "Use as official current dashboard-status evidence: the CEWS dashboard names this target location "
                "with ONLINE status and a recent timestamp. Do not use it as calibration, certificate, complete-grade, "
                "OpenAQ join, or radius evidence."
            )
        elif location and explicit_delayed and current_timestamp:
            decision = "dashboard_delayed_current_keep_status_caution"
            reader_use = (
                "Use as official dashboard visibility with a current DELAYED status. This is a caution row, "
                "not current-online or grade evidence."
            )
        elif location:
            decision = "dashboard_location_found_but_not_current_online"
            reader_use = (
                "Use as official dashboard-location context only; the latest status/timestamp does not close "
                "current-online evidence."
            )
        else:
            decision = "dashboard_location_not_found_keep_blocked"
            reader_use = "No exact dashboard location was matched for this target row."

        row = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "bmkg_dashboard_status_scan_id": f"IDN-bmkg-dashboard-status-{station_id}",
            "source_station_id": station_id,
            "source_station_name": station_name,
            "dashboard_location_key": location_key,
            "dashboard_location_found": bool(location),
            "dashboard_status_raw": status_raw,
            "dashboard_timestamp_raw": timestamp_raw,
            "dashboard_timestamp_iso": timestamp_iso,
            "dashboard_timestamp_age_hours": hours_old if hours_old is not None else "",
            "dashboard_timestamp_current_within_30_days": current_timestamp,
            "dashboard_pm25_ug_m3": latest.get("pm25", "") if isinstance(latest, dict) else "",
            "dashboard_category_raw": normalize(latest.get("category", "")).upper(),
            "dashboard_latitude": location.get("latitude", "") if isinstance(location, dict) else "",
            "dashboard_longitude": location.get("longitude", "") if isinstance(location, dict) else "",
            "dashboard_timeseries_points": len(numeric_values),
            "dashboard_positive_observation_count": positive_count,
            "dashboard_zero_observation_count": zero_count,
            "dashboard_last_label": labels[-1] if labels else "",
            "explicit_dashboard_online": explicit_online,
            "explicit_dashboard_delayed": explicit_delayed,
            "current_status_confirmed": current_status_confirmed,
            "station_specific_inspection_log_found": False,
            "station_specific_calibration_certificate_found": False,
            "calibration_status_available": False,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
            "dashboard_status_decision": decision,
            "reader_use": reader_use,
            "non_claim": NON_CLAIM,
        }
        rows.append(row)

    source_records = [
        {
            "source_key": source["source_key"],
            "source_name": source["source_name"],
            "source_role": source["source_role"],
            "url": source["url"],
            "final_url": source["final_url"],
            "retrieved": source["retrieved"],
            "http_status": source["http_status"],
            "content_type": source["content_type"],
            "retrieval_bytes": source["retrieval_bytes"],
            "sha256": source["sha256"],
            "matched_expected_terms": source["matched_expected_terms"],
            "dashboard_location_count": len(locations) if source["source_role"] == "official_cews_pm25_dashboard_data" else "",
            "matched_target_station_rows": (
                sum(1 for row in rows if row["dashboard_location_found"])
                if source["source_role"] == "official_cews_pm25_dashboard_data"
                else 0
            ),
            "retrieval_error": source["retrieval_error"],
            "source_note": source["source_note"],
        }
        for source in sources
    ]

    return rows, source_records, locations


def evidence_gate_counts(rows: list[dict[str, Any]], sources: list[dict[str, Any]], locations: dict[str, Any]) -> list[dict[str, Any]]:
    parent_sources = sum(1 for source in sources if source["retrieved"] and source["source_role"] == "official_parent_pm25_dashboard_page")
    dashboard_sources = sum(1 for source in sources if source["retrieved"] and source["source_role"] == "official_cews_pm25_dashboard_data")
    location_rows = sum(1 for row in rows if row["dashboard_location_found"])
    recent_rows = sum(1 for row in rows if row["dashboard_timestamp_current_within_30_days"])
    online_rows = sum(1 for row in rows if row["current_status_confirmed"])
    delayed_rows = sum(1 for row in rows if row["explicit_dashboard_delayed"])
    return [
        {
            "status": "available" if parent_sources else "not_ready",
            "gate": "Official parent page retrieved",
            "rows": parent_sources,
            "reader_use": "Confirms the BMKG climate-information page that embeds the CEWS PM2.5 dashboard.",
        },
        {
            "status": "available" if dashboard_sources else "not_ready",
            "gate": "CEWS dashboard data object retrieved",
            "rows": dashboard_sources,
            "reader_use": "Confirms the public dashboardData object was fetched from the official CEWS dashboard route.",
        },
        {
            "status": "available" if locations else "not_ready",
            "gate": "Dashboard location records parsed",
            "rows": len(locations),
            "reader_use": "Counts all PM2.5 dashboard locations exposed in the source object, including non-target rows.",
        },
        {
            "status": "available" if location_rows else "not_ready",
            "gate": "Target station rows matched to dashboard locations",
            "rows": location_rows,
            "reader_use": "Counts exact target rows matched by curated dashboard aliases.",
        },
        {
            "status": "available" if recent_rows else "not_ready",
            "gate": "Target dashboard timestamps current within 30 days",
            "rows": recent_rows,
            "reader_use": "Fresh timestamps are required before any dashboard status can be treated as current.",
        },
        {
            "status": "available" if online_rows else "not_ready",
            "gate": "Current ONLINE dashboard status",
            "rows": online_rows,
            "reader_use": "Counts exact target rows with ONLINE status and a recent timestamp.",
        },
        {
            "status": "caution" if delayed_rows else "available",
            "gate": "Current DELAYED dashboard status",
            "rows": delayed_rows,
            "reader_use": "Delayed rows are visible but should not be promoted to current-online status.",
        },
        {
            "status": "not_ready",
            "gate": "Station-specific inspection log",
            "rows": 0,
            "reader_use": "The dashboard does not expose public station inspection logs.",
        },
        {
            "status": "not_ready",
            "gate": "Station-specific calibration certificate or status",
            "rows": 0,
            "reader_use": "The dashboard does not expose station calibration certificates or calibration-status records.",
        },
        {
            "status": "not_ready",
            "gate": "Complete monitor-grade and station-radius closure",
            "rows": 0,
            "reader_use": "Current dashboard status is not complete grade, same-station crosswalk, or catchment evidence.",
        },
    ]


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    sources = fetch_sources(seed_rows)
    rows, source_records, locations = build_rows(generated_at, sources)
    write_csv(OUT_CSV, rows)

    counts = {
        "target_bmkg_rows": len(rows),
        "dashboard_source_urls_seeded": len(seed_rows),
        "dashboard_source_urls_retrieved": sum(1 for source in sources if source["retrieved"]),
        "official_parent_page_sources_retrieved": sum(
            1 for source in sources if source["retrieved"] and source["source_role"] == "official_parent_pm25_dashboard_page"
        ),
        "official_dashboard_data_sources_retrieved": sum(
            1 for source in sources if source["retrieved"] and source["source_role"] == "official_cews_pm25_dashboard_data"
        ),
        "dashboard_locations_total": len(locations),
        "target_dashboard_location_rows": sum(1 for row in rows if row["dashboard_location_found"]),
        "target_dashboard_current_timestamp_rows": sum(
            1 for row in rows if row["dashboard_timestamp_current_within_30_days"]
        ),
        "target_dashboard_online_rows": sum(1 for row in rows if row["explicit_dashboard_online"]),
        "target_dashboard_delayed_rows": sum(1 for row in rows if row["explicit_dashboard_delayed"]),
        "current_status_confirmed_rows": sum(1 for row in rows if row["current_status_confirmed"]),
        "target_latest_positive_pm25_rows": sum(
            1
            for row in rows
            if isinstance(row["dashboard_pm25_ug_m3"], (int, float)) and row["dashboard_pm25_ug_m3"] > 0
        ),
        "target_timeseries_observation_rows": sum(int(row["dashboard_timeseries_points"] or 0) for row in rows),
        "station_specific_inspection_log_rows": 0,
        "station_specific_calibration_certificate_rows": 0,
        "calibration_status_available_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }

    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 BMKG dashboard current-status source scan",
        "source_scope": (
            "Official BMKG climate-information parent page and embedded CEWS PM2.5 dashboard HTML. "
            "The dashboardData object is used for exact station/location status, timestamp, PM2.5, category, and coordinates."
        ),
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "seeded BMKG parent/dashboard source routes"},
            {"path": str(BMKG_STATUS_CSV.relative_to(PROGRAM_DIR)), "role": "22 BMKG station rows from the station-specific status audit"},
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["dashboard_status_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gate_counts(rows, sources, locations),
        "station_rows": rows,
        "display_rows": rows,
        "source_records": source_records,
        "non_claim": NON_CLAIM,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
    }
    write_json(OUT_JSON, summary)


if __name__ == "__main__":
    main()
