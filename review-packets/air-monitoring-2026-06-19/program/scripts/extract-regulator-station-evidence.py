"""Extract station-level evidence from official air-monitoring sources.

This pass follows the regulator-source discovery inventory. It turns official
station tables and portals into a normalized evidence layer, while keeping
count-only and plan-only sources visibly separate from coordinate evidence.
"""

from __future__ import annotations

import csv
import html
import io
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INVENTORY = GENERATED_DIR / "air-monitoring-regulator-source-inventory.csv"
OPENAQ_STATIONS = GENERATED_DIR / "air-monitoring-openaq-station-metadata.csv"
OUTPUT_CSV = GENERATED_DIR / "air-monitoring-regulator-station-extraction.csv"
OUTPUT_JSON = GENERATED_DIR / "air-monitoring-regulator-station-extraction-summary.json"

METHOD = "air_monitoring_regulator_station_extraction_v1"
USER_AGENT = "ADB-Research-Factory/1.0 regulator-station-extraction"
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This official-source extraction pass does not validate monitor grade, does "
    "not prove a monitor exists or does not exist outside OpenAQ, and does not "
    "compute station-radius population coverage."
)

TARGET_SOURCE_CLASSES = {
    "official_station_inventory",
    "official_air_quality_portal",
    "official_station_plan",
}

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "iso3",
    "iso2",
    "country",
    "subregion",
    "upgrade_queue_class",
    "source_name",
    "agency",
    "source_url",
    "retrieval_url",
    "retrieval_status",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "retrieval_note",
    "extraction_level",
    "source_evidence_type",
    "source_station_id",
    "source_station_name",
    "station_area",
    "source_station_type",
    "source_station_category",
    "latitude",
    "longitude",
    "coordinate_available",
    "pm25_signal",
    "pollutants_listed",
    "live_pm25_value",
    "source_station_count_claim",
    "source_count_basis",
    "openaq_country_rows",
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "nearest_openaq_within_5km",
    "best_openaq_name_overlap",
    "name_overlap_with_openaq",
    "non_claim",
]


@dataclass
class FetchResult:
    retrieval_url: str
    retrieval_status: str
    http_status: int | None
    content_type: str | None
    retrieval_bytes: int
    retrieval_note: str
    content: bytes


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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    text = str(value).strip().replace(",", ".")
    if not text or text.lower() in {"none", "nan", "-"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def clean_text(value: Any) -> str:
    text = "" if value is None else str(value)
    return " ".join(html.unescape(text).replace("\xa0", " ").split())


def source_targets(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row.get("source_class") in TARGET_SOURCE_CLASSES
        and row.get("official_station_inventory_or_portal", "").lower() == "true"
    ]


def fetch_url(
    url: str,
    *,
    verify: bool = True,
    fallback_urls: list[str] | None = None,
    accept: str = "*/*",
) -> FetchResult:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.8,id;q=0.7",
    }
    errors: list[str] = []
    for candidate in [url, *(fallback_urls or [])]:
        try:
            response = requests.get(
                candidate,
                headers=headers,
                timeout=TIMEOUT_SECONDS,
                allow_redirects=True,
                verify=verify,
            )
            if response.status_code >= 400:
                errors.append(f"{candidate}: HTTP {response.status_code}")
                continue
            return FetchResult(
                retrieval_url=response.url,
                retrieval_status="retrieved",
                http_status=response.status_code,
                content_type=response.headers.get("content-type"),
                retrieval_bytes=len(response.content),
                retrieval_note="; ".join(errors),
                content=response.content,
            )
        except Exception as exc:  # noqa: BLE001 - retrieval diagnostics are data.
            errors.append(f"{candidate}: {type(exc).__name__}: {exc}")
    return FetchResult(
        retrieval_url=url,
        retrieval_status="retrieval_error",
        http_status=None,
        content_type=None,
        retrieval_bytes=0,
        retrieval_note="; ".join(errors),
        content=b"",
    )


def base_row(
    generated_at: str,
    source: dict[str, str],
    fetch: FetchResult,
    *,
    extraction_level: str,
    evidence_type: str,
) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": "computed" if fetch.retrieval_status == "retrieved" else "source_retrieval_error",
        "method": METHOD,
        "iso3": source["iso3"],
        "iso2": source["iso2"],
        "country": source["country"],
        "subregion": source["subregion"],
        "upgrade_queue_class": source["upgrade_queue_class"],
        "source_name": source["source_name"],
        "agency": source["agency"],
        "source_url": source["url"],
        "retrieval_url": fetch.retrieval_url,
        "retrieval_status": fetch.retrieval_status,
        "http_status": fetch.http_status,
        "content_type": fetch.content_type,
        "retrieval_bytes": fetch.retrieval_bytes,
        "retrieval_note": fetch.retrieval_note,
        "extraction_level": extraction_level,
        "source_evidence_type": evidence_type,
        "source_station_id": "",
        "source_station_name": "",
        "station_area": "",
        "source_station_type": "",
        "source_station_category": "",
        "latitude": None,
        "longitude": None,
        "coordinate_available": False,
        "pm25_signal": False,
        "pollutants_listed": "",
        "live_pm25_value": None,
        "source_station_count_claim": source["official_station_count_claim"],
        "source_count_basis": "",
        "openaq_country_rows": 0,
        "nearest_openaq_location_id": "",
        "nearest_openaq_location_name": "",
        "nearest_openaq_distance_km": None,
        "nearest_openaq_within_5km": False,
        "best_openaq_name_overlap": 0,
        "name_overlap_with_openaq": False,
        "non_claim": NON_CLAIM,
    }


def error_row(generated_at: str, source: dict[str, str], fetch: FetchResult, note: str) -> dict[str, Any]:
    row = base_row(
        generated_at,
        source,
        fetch,
        extraction_level="unresolved",
        evidence_type="source_retrieval_or_parse_error",
    )
    row["retrieval_note"] = clean_text(f"{row['retrieval_note']} {note}")
    return row


def normalize_station_id(raw: str) -> str:
    value = re.sub(r"\s+", "", raw.upper())
    value = value.replace("C-CAMS-", "C-CAMS-").replace("CAMS-", "CAMS-")
    return value


def extract_bangladesh(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    fetch = fetch_url(source["url"], accept="application/pdf,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "Bangladesh PDF could not be retrieved.")]

    reader = PdfReader(io.BytesIO(fetch.content))
    table_text = "\n".join((reader.pages[i].extract_text() or "") for i in range(17, 19))
    start = table_text.find("City  ID  Location")
    end = table_text.find("UB=Urban", start)
    if start < 0 or end < 0:
        return [error_row(generated_at, source, fetch, "Bangladesh station table markers were not found.")]

    table = table_text[start:end]
    id_matches = list(re.finditer(r"(C\s*-\s*CAMS\s*-\s*\d+|CAMS\s*-\s*\d+)", table, flags=re.I))
    coord_re = re.compile(r"(\d{2,3}\.\s*\d+(?:\s+\d{2,6})?)\s*;\s*(\d{1,2}\.\s*\d+(?:\s+\d{2,6})?)")
    rows: list[dict[str, Any]] = []
    for idx, match in enumerate(id_matches):
        segment = table[match.end() : id_matches[idx + 1].start() if idx + 1 < len(id_matches) else len(table)]
        coord_match = coord_re.search(segment)
        if not coord_match:
            continue
        station_id = normalize_station_id(match.group(1))
        station_name = clean_text(segment[: coord_match.start()])
        longitude = as_float(re.sub(r"\s+", "", coord_match.group(1)))
        latitude = as_float(re.sub(r"\s+", "", coord_match.group(2)))
        row = base_row(
            generated_at,
            source,
            fetch,
            extraction_level="station_coordinates",
            evidence_type="official_pdf_station_table",
        )
        row.update(
            {
                "source_station_id": station_id,
                "source_station_name": station_name,
                "source_station_type": "C-CAMS" if station_id.startswith("C-CAMS") else "CAMS",
                "latitude": latitude,
                "longitude": longitude,
                "coordinate_available": latitude is not None and longitude is not None,
                "pm25_signal": True,
                "pollutants_listed": "PM10; PM2.5; SO2; CO; O3; NOx; meteorological parameters",
                "source_station_count_claim": "31 monitoring sites; 16 CAMS; 15 C-CAMS",
                "source_count_basis": "PDF text states 16 CAMS and 15 C-CAMS; station table lists 31 IDs.",
            }
        )
        rows.append(row)

    if len(rows) != 31:
        return [
            error_row(
                generated_at,
                source,
                fetch,
                f"Bangladesh station table yielded {len(rows)} rows; expected 31 from the source count claim.",
            )
        ]
    return rows


def resolve_nuxt_object(data: list[Any], index: int) -> dict[str, Any]:
    spec = data[index]
    if not isinstance(spec, dict):
        return {}
    return {key: data[value_index] for key, value_index in spec.items() if isinstance(value_index, int)}


def extract_indonesia(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    main = fetch_url(source["url"], accept="text/html,*/*")
    if main.retrieval_status != "retrieved":
        return [error_row(generated_at, source, main, "BMKG PM2.5 portal could not be retrieved.")]

    soup = BeautifulSoup(main.content, "html.parser")
    detail_link = ""
    for link in soup.find_all("a", href=True):
        href = str(link["href"])
        if "/kualitas-udara/pm25/" in href and "pm25_" in href:
            detail_link = f"https://www.bmkg.go.id{href}" if href.startswith("/") else href
            break
    if not detail_link:
        detail_link = "https://www.bmkg.go.id/kualitas-udara/pm25/pm25_kmy3"

    detail = fetch_url(detail_link, accept="text/html,*/*")
    if detail.retrieval_status != "retrieved":
        return [error_row(generated_at, source, detail, "BMKG PM2.5 detail page could not be retrieved.")]

    detail_soup = BeautifulSoup(detail.content, "html.parser")
    script = detail_soup.find("script", id="__NUXT_DATA__")
    if not script or not script.string:
        return [error_row(generated_at, source, detail, "BMKG Nuxt payload was not found.")]

    data = json.loads(script.string)
    list_index = data[5]["listPm25"]
    rows: list[dict[str, Any]] = []
    for item_index in data[list_index]:
        item = resolve_nuxt_object(data, item_index)
        latitude = as_float(item.get("LAT"))
        longitude = as_float(item.get("LON"))
        row = base_row(
            generated_at,
            source,
            detail,
            extraction_level="station_coordinates",
            evidence_type="official_pm25_portal_nuxt_payload",
        )
        station_id = str(item.get("nama_file", "")).replace(".xml", "")
        row.update(
            {
                "source_station_id": station_id,
                "source_station_name": clean_text(item.get("LOKASI")),
                "source_station_type": "BMKG PM2.5 portal location",
                "source_station_category": clean_text(item.get("KONDISI")),
                "latitude": latitude,
                "longitude": longitude,
                "coordinate_available": latitude is not None and longitude is not None,
                "pm25_signal": True,
                "pollutants_listed": "PM2.5",
                "live_pm25_value": as_float(item.get("PM25")),
                "source_count_basis": "BMKG Nuxt listPm25 payload parsed from the official PM2.5 portal.",
            }
        )
        rows.append(row)
    return rows


def extract_malaysia(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    api_url = (
        "https://eqms.doe.gov.my/api3/publicmapproxy/PUBLIC_DISPLAY/"
        "CAQM_MCAQM_Current_Reading/MapServer/0/query?where=1%3D1&outFields=%2A&returnGeometry=true&f=json"
    )
    fetch = fetch_url(api_url, accept="application/json,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "Malaysia public map proxy API could not be retrieved.")]

    payload = json.loads(fetch.content.decode("utf-8"))
    rows: list[dict[str, Any]] = []
    for feature in payload.get("features") or []:
        attr = feature.get("attributes") or {}
        latitude = as_float(attr.get("LATITUDE"))
        longitude = as_float(attr.get("LONGITUDE"))
        row = base_row(
            generated_at,
            source,
            fetch,
            extraction_level="station_coordinates",
            evidence_type="official_arcgis_station_feature_api",
        )
        row.update(
            {
                "source_station_id": clean_text(attr.get("STATION_ID")),
                "source_station_name": clean_text(attr.get("STATION_LOCATION")),
                "station_area": clean_text(attr.get("PLACE")),
                "source_station_type": "APIMS/MyEQMS current-reading station",
                "source_station_category": clean_text(attr.get("STATION_CATEGORY")),
                "latitude": latitude,
                "longitude": longitude,
                "coordinate_available": latitude is not None and longitude is not None,
                "pm25_signal": "PM2.5" in clean_text(attr.get("PARAM_SELECTED")),
                "pollutants_listed": clean_text(attr.get("PARAM_SELECTED")),
                "live_pm25_value": as_float(attr.get("PM25_CONC")),
                "source_count_basis": "Public MyEQMS ArcGIS feature layer current-reading station rows.",
            }
        )
        rows.append(row)
    return rows


def php_serialized_title(raw: Any) -> str:
    text = str(raw or "")
    for key in ("en", "ru", "uz", "oz"):
        match = re.search(rf's:2:"{key}";s:\d+:"([^"]*)"', text)
        if match:
            return clean_text(match.group(1))
    return clean_text(text)


def pollutant_keys(record: dict[str, Any]) -> str:
    keys = []
    for key in ("PM2.5", "PM10", "SO2", "CO", "NO2", "NO", "NOX", "O3"):
        value = record.get(key)
        if value not in (None, "", "-", " "):
            keys.append(key)
    return "; ".join(keys)


def extract_uzbekistan(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    fetch = fetch_url("https://monitoring.meteo.uz/api/maps", accept="application/json,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "Uzhydromet maps API could not be retrieved.")]

    payload = json.loads(fetch.content.decode("utf-8"))
    rows: list[dict[str, Any]] = []
    for group in payload.get("data") or []:
        for station in group.get("stations") or []:
            latitude = as_float(station.get("lat"))
            longitude = as_float(station.get("lon"))
            is_horiba = as_bool(station.get("is_horiba"))
            pm25_value = as_float(station.get("PM2.5"))
            row = base_row(
                generated_at,
                source,
                fetch,
                extraction_level="station_coordinates",
                evidence_type="official_air_quality_map_api",
            )
            row.update(
                {
                    "source_station_id": clean_text(station.get("id")),
                    "source_station_name": php_serialized_title(station.get("title")),
                    "source_station_type": "automatic HORIBA marker" if is_horiba else "station marker",
                    "source_station_category": clean_text(station.get("Si")),
                    "latitude": latitude,
                    "longitude": longitude,
                    "coordinate_available": latitude is not None and longitude is not None,
                    "pm25_signal": station.get("PM2.5") not in (None, "", "-", " "),
                    "pollutants_listed": pollutant_keys(station),
                    "live_pm25_value": pm25_value,
                    "source_station_count_claim": source["official_station_count_claim"],
                    "source_count_basis": "Uzhydromet public maps API station marker rows; source page count claim still needs reconciliation.",
                }
            )
            rows.append(row)
    return rows


def extract_georgia(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(hours=48)
    api_url = (
        "https://air.gov.ge/api/get_data_1hour/"
        f"?from_date_time={start:%Y-%m-%dT%H:%M:%S}"
        f"&to_date_time={end:%Y-%m-%dT%H:%M:%S}"
        "&station_code=all&municipality_id=all&substance=all&format=json"
    )
    fetch = fetch_url(api_url, accept="application/json,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "air.gov.ge hourly station API could not be retrieved.")]

    payload = json.loads(fetch.content.decode("utf-8"))
    rows: list[dict[str, Any]] = []
    for station in payload:
        equipment = station.get("stationequipment_set") or []
        pollutants = []
        for item in equipment:
            substance = item.get("substance") or {}
            name = substance.get("name")
            if name:
                pollutants.append(str(name))
        latitude = as_float(station.get("lat"))
        longitude = as_float(station.get("long"))
        row = base_row(
            generated_at,
            source,
            fetch,
            extraction_level="station_coordinates",
            evidence_type="official_hourly_station_api",
        )
        station_name = clean_text(station.get("address_en")) or clean_text(station.get("settlement_en"))
        row.update(
            {
                "source_station_id": clean_text(station.get("code") or station.get("id")),
                "source_station_name": station_name,
                "station_area": clean_text(station.get("settlement_en")),
                "source_station_type": "air.gov.ge hourly station",
                "source_station_category": clean_text(station.get("station_type")),
                "latitude": latitude,
                "longitude": longitude,
                "coordinate_available": latitude is not None and longitude is not None,
                "pm25_signal": any(pollutant.upper() == "PM2.5" for pollutant in pollutants),
                "pollutants_listed": "; ".join(sorted(set(pollutants))),
                "source_station_count_claim": source["official_station_count_claim"],
                "source_count_basis": "air.gov.ge hourly API station list; NEA source count claim says 18 stations including automatic and mobile units.",
            }
        )
        rows.append(row)
    return rows


def html_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    return clean_text(soup.get_text(" "))


def extract_sri_lanka(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    fetch = fetch_url(source["url"], accept="text/html,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "CEA air-quality page could not be retrieved.")]
    text = html_text(fetch.content)
    required = ["Battaramulla", "Kandy", "Jaffna", "Kurunegala", "Anuradhapura", "PM2.5"]
    missing = [term for term in required if term.lower() not in text.lower()]
    if missing:
        return [error_row(generated_at, source, fetch, f"CEA page did not contain expected terms: {missing}")]

    site_rows = [
        ("LKA_AUTOMATED_1", "Battaramulla", "automated ambient station"),
        ("LKA_AUTOMATED_2", "Kandy city", "automated ambient station"),
        ("LKA_SENSOR_TEST_1", "Jaffna", "sensor-based unit under test"),
        ("LKA_SENSOR_TEST_2", "Kurunegala", "sensor-based unit under test"),
        ("LKA_SENSOR_TEST_3", "Anuradhapura", "sensor-based unit under test"),
    ]
    rows: list[dict[str, Any]] = []
    for station_id, name, station_type in site_rows:
        row = base_row(
            generated_at,
            source,
            fetch,
            extraction_level="station_names_only",
            evidence_type="official_web_statement",
        )
        row.update(
            {
                "source_station_id": station_id,
                "source_station_name": name,
                "source_station_type": station_type,
                "pm25_signal": True,
                "pollutants_listed": "PM2.5; PM10; SO2; NO2; O3; CO",
                "source_station_count_claim": "2 automated ambient stations; 3 sensor-based units under test",
                "source_count_basis": "CEA page names Battaramulla and Kandy automated stations and Jaffna, Kurunegala, and Anuradhapura sensor units under test.",
            }
        )
        rows.append(row)
    return rows


def extract_tajikistan(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    fetch = fetch_url(source["url"], accept="text/html,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "Hydrometeorology Agency page could not be retrieved.")]
    text = html_text(fetch.content)
    if "dushanbe" not in text.lower() or "pm2.5" not in text.lower():
        return [error_row(generated_at, source, fetch, "Expected Dushanbe PM2.5 station text was not found.")]
    row = base_row(
        generated_at,
        source,
        fetch,
        extraction_level="station_names_only",
        evidence_type="official_web_statement",
    )
    row.update(
        {
            "source_station_id": "TJK_DUSHANBE_AUTOMATIC",
            "source_station_name": "Dushanbe automatic station",
            "station_area": "Dushanbe",
            "source_station_type": "automatic air-quality monitoring station",
            "pm25_signal": True,
            "pollutants_listed": "PM10; PM2.5; PM1; gases; meteorological parameters",
            "source_station_count_claim": "1 automatic station in Dushanbe referenced",
            "source_count_basis": "Hydrometeorology Agency page states that a Dushanbe automatic station measures PM10, PM2.5, PM1, gases, and meteorological parameters.",
        }
    )
    return [row]


def extract_brunei(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    fallback = "http://www.env.gov.bn/SitePages/Air%20Quality%20Management%20in%20Brunei%20Darussalam.aspx"
    fetch = fetch_url(source["url"], fallback_urls=[fallback], accept="text/html,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "JASTRe air-quality page could not be retrieved.")]
    text = html_text(fetch.content)
    if "6 monitoring stations" not in text.lower() and "six monitoring stations" not in text.lower():
        return [error_row(generated_at, source, fetch, "Expected six-station statement was not found.")]
    row = base_row(
        generated_at,
        source,
        fetch,
        extraction_level="count_only",
        evidence_type="official_web_statement",
    )
    row.update(
        {
            "source_station_id": "BRN_COUNT_STATEMENT",
            "source_station_type": "automatic real-time monitoring network count",
            "pm25_signal": True,
            "pollutants_listed": "PM10; PM2.5",
            "source_station_count_claim": "6 monitoring stations",
            "source_count_basis": "JASTRe page states that six monitoring stations are operated and linked to the central monitoring centre.",
        }
    )
    return [row]


def decode_js_escapes(text: str) -> str:
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)


def extract_myanmar(generated_at: str, source: dict[str, str]) -> list[dict[str, Any]]:
    fetch = fetch_url(source["url"], verify=False, accept="text/html,*/*")
    if fetch.retrieval_status != "retrieved":
        return [error_row(generated_at, source, fetch, "Project Bank page could not be retrieved.")]
    text = decode_js_escapes(html.unescape(fetch.content.decode("utf-8", errors="replace")))
    fixed = "seven fixed-type air quality monitoring stations"
    mobile = "five mobile-type air quality monitoring stations"
    if fixed not in text or mobile not in text:
        return [error_row(generated_at, source, fetch, "Expected fixed/mobile project-plan station text was not found.")]

    groups = [
        (
            "MMR_FIXED_PLAN",
            "Fixed-type planned station group",
            "7 fixed-type air quality monitoring stations",
            "Project plan says one in Naypyitaw, three in Yangon Region, and three in Mandalay Region.",
        ),
        (
            "MMR_MOBILE_PLAN",
            "Mobile-type planned station group",
            "5 mobile-type air quality monitoring stations",
            "Project plan says one each in Naypyitaw, Yangon Region, Mandalay Region, Shan State, and Sagaing Region.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for station_id, name, claim, basis in groups:
        row = base_row(
            generated_at,
            source,
            fetch,
            extraction_level="plan_count_only",
            evidence_type="official_project_plan",
        )
        row.update(
            {
                "source_station_id": station_id,
                "source_station_name": name,
                "source_station_type": "planned air-quality monitoring station group",
                "pm25_signal": False,
                "pollutants_listed": "",
                "source_station_count_claim": claim,
                "source_count_basis": basis,
            }
        )
        rows.append(row)
    return rows


EXTRACTORS = {
    "BGD": extract_bangladesh,
    "IDN": extract_indonesia,
    "MYS": extract_malaysia,
    "UZB": extract_uzbekistan,
    "GEO": extract_georgia,
    "LKA": extract_sri_lanka,
    "TJK": extract_tajikistan,
    "BRN": extract_brunei,
    "MMR": extract_myanmar,
}


def load_openaq_rows() -> dict[str, list[dict[str, Any]]]:
    rows = read_csv(OPENAQ_STATIONS)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if not row.get("openaq_location_id"):
            continue
        lat = as_float(row.get("latitude"))
        lon = as_float(row.get("longitude"))
        if lat is None or lon is None:
            continue
        item = {
            "openaq_location_id": row.get("openaq_location_id", ""),
            "openaq_location_name": row.get("openaq_location_name", ""),
            "latitude": lat,
            "longitude": lon,
        }
        grouped.setdefault(row["iso3"], []).append(item)
    return grouped


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def name_tokens(value: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", clean_text(value).lower())
    stop = {"the", "of", "and", "doe", "office", "station", "city", "sadar"}
    return {token for token in tokens if len(token) >= 3 and token not in stop}


def best_name_overlap(source_name: str, openaq_rows: list[dict[str, Any]]) -> int:
    source_tokens = name_tokens(source_name)
    if not source_tokens:
        return 0
    best = 0
    for openaq in openaq_rows:
        overlap = len(source_tokens & name_tokens(openaq.get("openaq_location_name", "")))
        best = max(best, overlap)
    return best


def annotate_openaq(rows: list[dict[str, Any]], openaq_by_iso: dict[str, list[dict[str, Any]]]) -> None:
    for row in rows:
        openaq_rows = openaq_by_iso.get(row["iso3"], [])
        row["openaq_country_rows"] = len(openaq_rows)
        overlap = best_name_overlap(row.get("source_station_name", ""), openaq_rows)
        row["best_openaq_name_overlap"] = overlap
        row["name_overlap_with_openaq"] = overlap > 0
        lat = as_float(row.get("latitude"))
        lon = as_float(row.get("longitude"))
        if lat is None or lon is None or not openaq_rows:
            continue
        nearest = min(
            openaq_rows,
            key=lambda item: haversine_km(lat, lon, item["latitude"], item["longitude"]),
        )
        distance = haversine_km(lat, lon, nearest["latitude"], nearest["longitude"])
        row["nearest_openaq_location_id"] = nearest["openaq_location_id"]
        row["nearest_openaq_location_name"] = nearest["openaq_location_name"]
        row["nearest_openaq_distance_km"] = round(distance, 3)
        row["nearest_openaq_within_5km"] = distance <= 5.0


def country_level(rows: list[dict[str, Any]]) -> str:
    levels = {row["extraction_level"] for row in rows}
    for level in ("station_coordinates", "station_names_only", "count_only", "plan_count_only", "unresolved"):
        if level in levels:
            return level
    return "unresolved"


def build_summary(generated_at: str, targets: list[dict[str, str]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_iso: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_iso.setdefault(row["iso3"], []).append(row)

    coordinate_rows = [row for row in rows if row["coordinate_available"]]
    name_only_rows = [row for row in rows if row["extraction_level"] == "station_names_only"]
    count_only_rows = [row for row in rows if row["extraction_level"] == "count_only"]
    plan_only_rows = [row for row in rows if row["extraction_level"] == "plan_count_only"]
    unresolved_rows = [row for row in rows if row["extraction_level"] == "unresolved"]
    near_openaq = [row for row in coordinate_rows if row["nearest_openaq_within_5km"]]

    country_rows = []
    for target in targets:
        country = by_iso.get(target["iso3"], [])
        country_coordinate_rows = [row for row in country if row["coordinate_available"]]
        country_rows.append(
            {
                "iso3": target["iso3"],
                "iso2": target["iso2"],
                "country": target["country"],
                "subregion": target["subregion"],
                "source_name": target["source_name"],
                "source_class": target["source_class"],
                "source_extraction_level": country_level(country),
                "retrieval_status": country[0]["retrieval_status"] if country else "not_attempted",
                "official_rows_extracted": len([row for row in country if row["extraction_level"] != "unresolved"]),
                "coordinate_rows": len(country_coordinate_rows),
                "station_name_only_rows": len([row for row in country if row["extraction_level"] == "station_names_only"]),
                "count_only_rows": len([row for row in country if row["extraction_level"] == "count_only"]),
                "plan_count_only_rows": len([row for row in country if row["extraction_level"] == "plan_count_only"]),
                "pm25_signal_rows": sum(1 for row in country if row["pm25_signal"]),
                "openaq_country_rows": country[0]["openaq_country_rows"] if country else 0,
                "nearest_openaq_within_5km_rows": sum(1 for row in country if row["nearest_openaq_within_5km"]),
                "name_overlap_rows": sum(1 for row in country if row["name_overlap_with_openaq"]),
                "source_station_count_claim": target["official_station_count_claim"],
                "retrieval_note": country[0]["retrieval_note"] if country else "",
            }
        )

    counts = {
        "official_sources_targeted": len(targets),
        "official_sources_retrieved_or_extracted": sum(
            1 for rows_for_country in by_iso.values() if rows_for_country[0]["retrieval_status"] == "retrieved"
        ),
        "countries_with_station_coordinates": len({row["iso3"] for row in coordinate_rows}),
        "official_station_coordinate_rows": len(coordinate_rows),
        "official_station_name_only_rows": len(name_only_rows),
        "official_count_only_rows": len(count_only_rows),
        "official_plan_count_only_rows": len(plan_only_rows),
        "countries_with_unresolved_extraction": len({row["iso3"] for row in unresolved_rows}),
        "official_rows_with_pm25_signal": sum(1 for row in rows if row["pm25_signal"]),
        "official_coordinate_rows_near_openaq_within_5km": len(near_openaq),
        "official_coordinate_rows_not_near_openaq_within_5km": len(coordinate_rows) - len(near_openaq),
        "official_rows_with_name_overlap_to_openaq": sum(1 for row in rows if row["name_overlap_with_openaq"]),
        "monitor_grade_rows": 0,
        "station_radius_analysis_ready": False,
    }

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed" if not unresolved_rows else "partial_unresolved_sources",
        "method": METHOD,
        "goal_level": "L3 official station-source extraction",
        "source_inputs": [
            {"path": str(SOURCE_INVENTORY.relative_to(PROGRAM_DIR)), "role": "regulator-source candidate inventory"},
            {"path": str(OPENAQ_STATIONS.relative_to(PROGRAM_DIR)), "role": "OpenAQ station metadata for reconciliation diagnostics"},
        ],
        "coverage_counts": counts,
        "evidence_gate_counts": [
            {
                "gate": "Official station-coordinate extraction",
                "status": "available" if coordinate_rows else "blocked_or_absent",
                "rows": len(coordinate_rows),
                "reader_use": "Shows where official tables or portals expose station coordinates.",
            },
            {
                "gate": "Official-to-OpenAQ proximity candidates",
                "status": "partly_available" if near_openaq else "not_ready",
                "rows": len(near_openaq),
                "reader_use": "Nearest-distance diagnostic only; not a validated station match.",
            },
            {
                "gate": "Name/count-only official evidence",
                "status": "limited",
                "rows": len(name_only_rows) + len(count_only_rows),
                "reader_use": "Useful for source audit, insufficient for catchment or station-radius work.",
            },
            {
                "gate": "Plan-only official evidence",
                "status": "limited",
                "rows": len(plan_only_rows),
                "reader_use": "Project plans cannot be treated as active station validation.",
            },
            {
                "gate": "Monitor-grade classification",
                "status": "not_ready",
                "rows": 0,
                "reader_use": "No complete source classifies these rows as reference-grade or regulatory-grade monitors.",
            },
            {
                "gate": "Station-radius population coverage",
                "status": "not_computed",
                "rows": 0,
                "reader_use": "Still requires a declared catchment method and gridded denominators.",
            },
        ],
        "country_rows": country_rows,
        "top_coordinate_rows": coordinate_rows[:30],
        "outputs": {
            "csv": str(OUTPUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUTPUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "review_notes": [
            "Coordinate rows identify official-source station locations, not monitor grade.",
            "Nearest OpenAQ distance is a screening diagnostic, not a validated same-station join.",
            "Name-only, count-only, and plan-only sources remain visible because they should not support station-radius claims.",
            "The script intentionally excludes public API contact fields and keeps only station evidence needed for the research claim.",
        ],
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = now_iso()
    inventory_rows = read_csv(SOURCE_INVENTORY)
    targets = source_targets(inventory_rows)
    openaq_by_iso = load_openaq_rows()

    rows: list[dict[str, Any]] = []
    for target in targets:
        extractor = EXTRACTORS.get(target["iso3"])
        if extractor is None:
            fake_fetch = FetchResult(target["url"], "not_implemented", None, None, 0, "", b"")
            rows.append(error_row(generated_at, target, fake_fetch, "No extractor is implemented for this source."))
            continue
        rows.extend(extractor(generated_at, target))

    annotate_openaq(rows, openaq_by_iso)
    summary = build_summary(generated_at, targets, rows)

    write_csv(OUTPUT_CSV, rows)
    write_json(OUTPUT_JSON, summary)
    counts = summary["coverage_counts"]
    print(
        "Built regulator station extraction: "
        f"{counts['official_sources_targeted']} sources; "
        f"{counts['official_station_coordinate_rows']} coordinate rows; "
        f"{counts['official_station_name_only_rows']} name-only rows; "
        f"{counts['official_count_only_rows']} count-only rows; "
        f"{counts['official_plan_count_only_rows']} plan-only rows."
    )
    print(f"Wrote {OUTPUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    try:
        requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]
    except Exception:
        pass
    sys.exit(main())
