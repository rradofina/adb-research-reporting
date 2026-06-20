"""Scan BMKG regional/public sources for station-status closure.

The BMKG station-detail and API passes proved that telemetry is visible but did
not expose explicit station-status, inspection-log, calibration-certificate, or
grade fields. This pass tests public sources outside those central detail/API
surfaces, especially regional BMKG pages and public-information routes, for
exact station status evidence.

Only an exact target station-name match with explicit source text such as
``Status Stasiun: ONLINE`` and a recent source timestamp can close the
current-status gate. Source-level cadence, tariff, historical location, or
public-information context is recorded but cannot close grade/radius gates.
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

SEED_CSV = SOURCE_INPUTS_DIR / "bmkg-regional-status-source-seed.csv"
BMKG_STATUS_CSV = GENERATED_DIR / "air-monitoring-bmkg-station-specific-status-audit.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-bmkg-regional-status-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-bmkg-regional-status-source-scan-summary.json"

METHOD = "air_monitoring_bmkg_regional_status_source_scan_v1"
STATUS = "computed_bmkg_regional_status_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 90
NON_CLAIM = (
    "This scan records public BMKG regional, public-information, service, "
    "historical, regulator, and regional-analysis context for the 22 BMKG "
    "PM2.5 rows. Regional analysis pages can support station or official-site "
    "context, but current-status closure still requires an exact target station "
    "with explicit status text and a recent timestamp. It does not certify "
    "station-specific inspection logs, calibration certificates, complete "
    "monitor-grade status, same-station OpenAQ joins, or station-radius "
    "coverage."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "bmkg_regional_status_scan_id",
    "source_station_id",
    "source_station_name",
    "matched_source_keys",
    "matched_source_roles",
    "source_url_count",
    "exact_station_name_external_context",
    "location_level_external_context",
    "explicit_regional_status_online",
    "status_source_key",
    "status_source_url",
    "status_timestamp_raw",
    "status_timestamp_iso",
    "status_recent_within_30_days",
    "status_value_ug_m3",
    "status_category_raw",
    "source_latitude",
    "source_longitude",
    "public_information_cadence_context",
    "service_tariff_context",
    "historical_station_context",
    "regulator_station_context",
    "station_specific_inspection_log_found",
    "station_specific_calibration_certificate_found",
    "calibration_status_available",
    "current_status_confirmed",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "regional_status_decision",
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

STATUS_SOURCE_ROLES = {"official_regional_station_status"}
STATION_CONTEXT_SOURCE_ROLES = {
    "official_regional_analysis_context",
    "official_regional_station_status",
    "official_regional_upt_profile",
    "official_historical_station_context",
    "public_regulator_station_context",
}

LOCATION_ALIASES = {
    "pm25_plb4": ["palembang", "kota palembang"],
    "pm25_pl3": ["palembang", "kota palembang"],
    "pm25_idp2": ["aceh besar", "kab. aceh besar", "kab aceh besar"],
    "pm25_jm4": ["jambi", "provinsi jambi"],
}

STATION_CONTEXT_ALIASES = {
    "pm25_pbb": ["stasiun klimatologi bengkulu", "kota bengkulu"],
    "pm25_plb4": ["palembang (musi 2)", "musi 2"],
    "pm25_ptn2": ["stasiun klimatologi kalimantan barat", "mempawah"],
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


def fetch_text(url: str, hint: str) -> dict[str, Any]:
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

        lower_hint = f"{hint} {result['content_type']} {url}".lower()
        if "pdf" in lower_hint or response.content[:4] == b"%PDF":
            reader = PdfReader(io.BytesIO(response.content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(" ", strip=True)
        result["text"] = normalize(text)
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def parse_timestamp(value: str) -> tuple[str, str, bool]:
    match = re.search(
        r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4}),\s+(\d{1,2}):(\d{2})\s+(WIB|WITA)",
        value,
        flags=re.IGNORECASE,
    )
    if not match:
        return "", "", False
    day, month_raw, year, hour, minute, tz_raw = match.groups()
    month = MONTHS.get(month_raw.casefold())
    if not month:
        return match.group(0), "", False
    tz = timezone(timedelta(hours=8 if tz_raw.upper() == "WITA" else 7))
    parsed = datetime(int(year), month, int(day), int(hour), int(minute), tzinfo=tz)
    iso = parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    generated = datetime.now(timezone.utc).date()
    age_days = (generated - parsed.astimezone(timezone.utc).date()).days
    return match.group(0), iso, 0 <= age_days <= 30


def parse_regional_status_entries(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    pattern = re.compile(
        r"(?P<timestamp>\d{1,2}\s+[A-Za-z]{3}\s+\d{4},\s+\d{1,2}:\d{2}\s+WITA)\s+"
        r"(?P<value>-?\d+(?:[.,]\d+)?)\s+.{0,24}?\s+"
        r"(?P<station>[A-Z0-9 .'-]+?)\s+Latitude:\s*(?P<lat>-?\d+(?:\.\d+)?)\s+"
        r"Longitude:\s*(?P<lon>-?\d+(?:\.\d+)?)\s+Status Stasiun:\s*(?P<status>[A-Za-z]+)\s+"
        r"Kategori:\s*(?P<category>SANGAT\s+TIDAK\s+SEHAT|TIDAK\s+SEHAT|BERBAHAYA|SEDANG|BAIK)",
        flags=re.IGNORECASE,
    )
    for match in pattern.finditer(text):
        timestamp_raw, timestamp_iso, recent = parse_timestamp(match.group("timestamp"))
        entries.append(
            {
                "station": normalize(match.group("station")).title(),
                "station_key": norm_key(match.group("station")),
                "timestamp_raw": timestamp_raw,
                "timestamp_iso": timestamp_iso,
                "recent": recent,
                "value": match.group("value").replace(",", "."),
                "lat": match.group("lat"),
                "lon": match.group("lon"),
                "status": normalize(match.group("status")).upper(),
                "category": normalize(match.group("category")).upper(),
            }
        )
    return entries


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(BMKG_STATUS_CSV)
    unique: dict[str, dict[str, str]] = {}
    for row in rows:
        station_id = row.get("source_station_id", "")
        if station_id:
            unique[station_id] = row
    return list(unique.values())


def source_level_context(source_records: list[dict[str, Any]], role: str) -> bool:
    return any(record["retrieved"] and record["source_role"] == role for record in source_records)


def station_context_matches(source_role: str, station_id: str, station_key: str, text_key: str) -> bool:
    aliases = STATION_CONTEXT_ALIASES.get(station_id, [])
    if source_role == "official_regional_analysis_context":
        return any(alias in text_key for alias in aliases)
    return station_key in text_key or any(alias in text_key for alias in aliases)


def build_rows(generated_at: str, sources: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    status_entries: dict[str, dict[str, Any]] = {}
    for source in sources:
        if source["source_role"] not in STATUS_SOURCE_ROLES or not source["retrieved"]:
            continue
        for entry in parse_regional_status_entries(source["text"]):
            status_entries[entry["station_key"]] = {**entry, "source": source}

    station_rows: list[dict[str, Any]] = []
    for target in target_rows():
        station_id = target["source_station_id"]
        station_name = target["source_station_name"]
        station_key = norm_key(station_name)
        matched_sources: list[dict[str, Any]] = []
        location_sources: list[dict[str, Any]] = []

        for source in sources:
            if not source["retrieved"]:
                continue
            text_key = norm_key(source["text"])
            if source["source_role"] in STATION_CONTEXT_SOURCE_ROLES and station_context_matches(source["source_role"], station_id, station_key, text_key):
                matched_sources.append(source)
            aliases = LOCATION_ALIASES.get(station_id, [])
            if source["source_role"] == "official_historical_station_context" and any(alias in text_key for alias in aliases):
                location_sources.append(source)

        status_entry = status_entries.get(station_key)
        explicit_online = bool(status_entry and status_entry["status"] == "ONLINE")
        status_recent = bool(status_entry and status_entry["recent"])
        current_status_confirmed = bool(explicit_online and status_recent)

        matched_source_keys = [source["source_key"] for source in matched_sources]
        matched_source_roles = [source["source_role"] for source in matched_sources]
        if location_sources:
            for source in location_sources:
                if source["source_key"] not in matched_source_keys:
                    matched_source_keys.append(source["source_key"])
                    matched_source_roles.append(source["source_role"])

        historical = any(source["source_role"] == "official_historical_station_context" for source in matched_sources + location_sources)
        regulator = any(source["source_role"] == "public_regulator_station_context" for source in matched_sources)
        public_info = source_level_context(sources, "official_public_information_cadence")
        tariff = source_level_context(sources, "official_service_tariff")

        if current_status_confirmed:
            decision = "regional_online_status_current_but_grade_still_blocked"
            reader_use = (
                "Use as station-specific current-status evidence from an official regional BMKG page. "
                "Do not use it as inspection, calibration, certificate, complete-grade, or radius evidence."
            )
        elif matched_sources:
            decision = "station_named_in_public_source_but_no_current_status_closure"
            reader_use = (
                "Use as exact station-name or official site-variant public context. It does not provide current-status, "
                "inspection, calibration, certificate, complete-grade, or radius closure."
            )
        elif location_sources:
            decision = "location_context_only_no_exact_station_status"
            reader_use = (
                "Use as historical or location-level context only. It does not name the exact station "
                "row with current-status or certificate evidence."
            )
        else:
            decision = "no_regional_station_status_source_keep_blocked"
            reader_use = (
                "No seeded regional or regulator source names this exact station with status evidence."
            )

        row = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "bmkg_regional_status_scan_id": f"IDN-bmkg-regional-status-{station_id}",
            "source_station_id": station_id,
            "source_station_name": station_name,
            "matched_source_keys": "||".join(matched_source_keys),
            "matched_source_roles": "||".join(matched_source_roles),
            "source_url_count": len(matched_source_keys),
            "exact_station_name_external_context": bool(matched_sources),
            "location_level_external_context": bool(location_sources),
            "explicit_regional_status_online": explicit_online,
            "status_source_key": status_entry["source"]["source_key"] if status_entry else "",
            "status_source_url": status_entry["source"]["url"] if status_entry else "",
            "status_timestamp_raw": status_entry["timestamp_raw"] if status_entry else "",
            "status_timestamp_iso": status_entry["timestamp_iso"] if status_entry else "",
            "status_recent_within_30_days": status_recent,
            "status_value_ug_m3": status_entry["value"] if status_entry else "",
            "status_category_raw": status_entry["category"] if status_entry else "",
            "source_latitude": status_entry["lat"] if status_entry else "",
            "source_longitude": status_entry["lon"] if status_entry else "",
            "public_information_cadence_context": public_info,
            "service_tariff_context": tariff,
            "historical_station_context": historical,
            "regulator_station_context": regulator,
            "station_specific_inspection_log_found": False,
            "station_specific_calibration_certificate_found": False,
            "calibration_status_available": False,
            "current_status_confirmed": current_status_confirmed,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
            "regional_status_decision": decision,
            "reader_use": reader_use,
            "non_claim": NON_CLAIM,
        }
        station_rows.append(row)

    return station_rows, [
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
            "matched_station_status_terms": source["matched_station_status_terms"],
            "matched_calibration_terms": source["matched_calibration_terms"],
            "matched_inspection_terms": source["matched_inspection_terms"],
            "matched_grade_terms": source["matched_grade_terms"],
            "matched_target_station_rows": sum(
                1 for row in station_rows if source["source_key"] in str(row["matched_source_keys"]).split("||")
            ),
            "retrieval_error": source["retrieval_error"],
            "source_note": source["source_note"],
        }
        for source in sources
    ]


def evidence_gate_counts(rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    retrieved_sources = sum(1 for source in sources if source["retrieved"])
    status_sources = sum(1 for source in sources if source["retrieved"] and source["source_role"] == "official_regional_station_status")
    regional_analysis_sources = sum(
        1 for source in sources if source["retrieved"] and source["source_role"] == "official_regional_analysis_context"
    )
    public_info_sources = sum(
        1
        for source in sources
        if source["retrieved"]
        and source["source_role"] in {"official_public_information_cadence", "official_service_tariff"}
    )
    exact_context = sum(1 for row in rows if row["exact_station_name_external_context"])
    regional_analysis_context = sum(
        1
        for row in rows
        if "official_regional_analysis_context" in str(row["matched_source_roles"]).split("||")
    )
    current_status = sum(1 for row in rows if row["current_status_confirmed"])
    return [
        {
            "status": "available" if retrieved_sources else "not_ready",
            "gate": "Seeded regional/public sources retrieved",
            "rows": retrieved_sources,
            "reader_use": "Confirms the seeded public source routes were tested.",
        },
        {
            "status": "available" if status_sources else "not_ready",
            "gate": "Regional station-status source",
            "rows": status_sources,
            "reader_use": "A regional BMKG page can carry station-level status text outside the central detail/API surfaces.",
        },
        {
            "status": "partly_available" if regional_analysis_sources else "not_ready",
            "gate": "Regional analysis context source",
            "rows": regional_analysis_sources,
            "reader_use": "Regional analysis pages can name official monitoring sites, but they do not certify target-row status or grade.",
        },
        {
            "status": "partly_available" if exact_context else "not_ready",
            "gate": "Target station or official site named outside central detail/API",
            "rows": exact_context,
            "reader_use": "Station/site context helps target source closure, but only explicit recent status text closes current status.",
        },
        {
            "status": "partly_available" if regional_analysis_context else "not_ready",
            "gate": "Rows with regional analysis context",
            "rows": regional_analysis_context,
            "reader_use": "Counts target rows matched to official regional analysis pages without treating them as status or grade evidence.",
        },
        {
            "status": "available" if current_status else "not_ready",
            "gate": "Current-status confirmed by regional source",
            "rows": current_status,
            "reader_use": "Counts only exact target rows with explicit ONLINE status and recent source timestamp.",
        },
        {
            "status": "partly_available" if public_info_sources else "not_ready",
            "gate": "Public information and service-access context",
            "rows": public_info_sources,
            "reader_use": "Cadence and service/tariff sources explain access routes but do not certify target stations.",
        },
        {
            "status": "not_ready",
            "gate": "Station-specific inspection log",
            "rows": 0,
            "reader_use": "No seeded source exposes a public inspection log for any target row.",
        },
        {
            "status": "not_ready",
            "gate": "Station-specific calibration certificate or status",
            "rows": 0,
            "reader_use": "No seeded source exposes a calibration certificate or calibration-status record for any target row.",
        },
        {
            "status": "not_ready",
            "gate": "Complete monitor-grade and station-radius closure",
            "rows": 0,
            "reader_use": "A current-status row alone is not complete grade or station-radius readiness.",
        },
    ]


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    sources: list[dict[str, Any]] = []
    for seed in seed_rows:
        fetched = fetch_text(seed["url"], seed.get("content_type_hint", ""))
        text = fetched["text"]
        sources.append(
            {
                **seed,
                **fetched,
                "matched_expected_terms": "||".join(matched_terms(text, split_terms(seed.get("expected_terms", "")))),
                "matched_station_status_terms": "||".join(matched_terms(text, split_terms(seed.get("station_status_terms", "")))),
                "matched_calibration_terms": "||".join(matched_terms(text, split_terms(seed.get("calibration_terms", "")))),
                "matched_inspection_terms": "||".join(matched_terms(text, split_terms(seed.get("inspection_terms", "")))),
                "matched_grade_terms": "||".join(matched_terms(text, split_terms(seed.get("grade_terms", "")))),
            }
        )

    rows, source_records = build_rows(generated_at, sources)
    write_csv(OUT_CSV, rows)

    counts = {
        "target_bmkg_rows": len(rows),
        "regional_public_source_urls_seeded": len(seed_rows),
        "regional_public_source_urls_retrieved": sum(1 for source in sources if source["retrieved"]),
        "official_regional_station_status_sources_retrieved": sum(
            1 for source in sources if source["retrieved"] and source["source_role"] == "official_regional_station_status"
        ),
        "official_regional_analysis_context_sources_retrieved": sum(
            1 for source in sources if source["retrieved"] and source["source_role"] == "official_regional_analysis_context"
        ),
        "public_information_or_service_sources_retrieved": sum(
            1
            for source in sources
            if source["retrieved"]
            and source["source_role"] in {"official_public_information_cadence", "official_service_tariff"}
        ),
        "rows_with_exact_station_name_external_context": sum(1 for row in rows if row["exact_station_name_external_context"]),
        "rows_with_regional_analysis_context": sum(
            1
            for row in rows
            if "official_regional_analysis_context" in str(row["matched_source_roles"]).split("||")
        ),
        "rows_with_location_level_external_context": sum(1 for row in rows if row["location_level_external_context"]),
        "rows_with_regional_online_status": sum(1 for row in rows if row["explicit_regional_status_online"]),
        "current_status_confirmed_rows": sum(1 for row in rows if row["current_status_confirmed"]),
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
        "goal_level": "L3 BMKG regional station-status closure scan",
        "source_scope": (
            "Public regional BMKG station-status and analysis pages, BMKG public-information/service, "
            "historical BMKG, and public regulator sources outside the central BMKG station-detail and API surfaces."
        ),
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "seeded BMKG regional/public status source routes"},
            {"path": str(BMKG_STATUS_CSV.relative_to(PROGRAM_DIR)), "role": "22 BMKG station rows from the station-specific status audit"},
        ],
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["regional_status_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gate_counts(rows, sources),
        "station_rows": rows,
        "display_rows": [
            row
            for row in rows
            if row["current_status_confirmed"]
            or row["exact_station_name_external_context"]
            or row["location_level_external_context"]
        ][:10],
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
