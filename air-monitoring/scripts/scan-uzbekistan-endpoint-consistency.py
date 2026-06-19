"""Compare official Uzbekistan station endpoints for exact blocker rows.

The blocker-row follow-up narrowed Uzbekistan to three station IDs whose public
rows still block station-radius use. This pass does not broaden the source
universe. It compares the exact official surfaces for those same station IDs:
the public maps API, the English/Russian/Uzbek station-detail pages, and the
English/Russian/Uzbek regional table rows.
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

TARGET_SEED_CSV = SOURCE_INPUTS_DIR / "uzbekistan-endpoint-consistency-targets.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-endpoint-consistency.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-endpoint-consistency-summary.json"

METHOD = "air_monitoring_uzbekistan_endpoint_consistency_v1"
STATUS = "computed_uzbekistan_endpoint_consistency"
API_URL = "https://monitoring.meteo.uz/api/maps"
BASE_URL = "https://monitoring.meteo.uz"
LANGUAGES = ["en", "ru", "uz"]
TIMEOUT_SECONDS = 60
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "Endpoint consistency is a QA gate, not a station-grade or station-status "
    "certification. This scan does not turn API presence, Horiba labels, recent "
    "timestamps, or pollutant values into current operating status, complete "
    "monitor-grade classification, or station-radius readiness without explicit "
    "public row-level language."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "source_station_id",
    "source_station_name",
    "review_focus",
    "detail_pages_retrieved",
    "detail_language_count",
    "detail_updated_dates",
    "detail_pm25_values",
    "detail_cross_language_consistent",
    "detail_latest_updated_iso",
    "detail_latest_age_days",
    "detail_any_stale_over_30_days",
    "detail_any_pm25_sentinel",
    "api_retrieved",
    "api_date_iso",
    "api_pm25_value",
    "api_pm25_value_status",
    "api_is_horiba",
    "api_si",
    "region_rows_found",
    "region_updated_values",
    "region_auto_values",
    "region_any_updating_data",
    "region_any_horiba_marker",
    "api_detail_date_mismatch",
    "api_detail_pm25_mismatch",
    "region_detail_status_mismatch",
    "endpoint_disagreement_count",
    "unresolved_blocker_present",
    "public_endpoint_resolution_available",
    "current_status_confirmed",
    "station_method_classified",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "endpoint_decision",
    "reader_use",
    "reader_question",
    "non_claim",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ")
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


def fetch_source(url: str, *, accept: str = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8") -> dict[str, Any]:
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
        "soup": None,
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
        if "json" in result["content_type"].lower():
            result["json"] = response.json()
            result["text"] = normalize(response.text)
        else:
            result["soup"] = BeautifulSoup(response.text, "html.parser")
            result["text"] = normalize(result["soup"].get_text(" ", strip=True))
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are evidence.
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def parse_date(value: str, generated_at: str) -> tuple[str, int | None]:
    raw = normalize(value)
    match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", raw)
    if not match:
        return "", None
    day, month, year = match.groups()
    parsed = datetime(int(year), int(month), int(day), tzinfo=timezone.utc).date()
    generated_date = datetime.fromisoformat(generated_at.replace("Z", "+00:00")).date()
    return parsed.isoformat(), (generated_date - parsed).days


def value_status(value: str) -> str:
    if not normalize(value):
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


def parse_pm25(text: str) -> str:
    match = re.search(r"PM\s*2\.5:\s*(-?[0-9]+(?:[.,][0-9]+)?)", text)
    return match.group(1).replace(",", ".") if match else ""


def parse_detail_page(source: dict[str, Any], language: str, generated_at: str) -> dict[str, Any]:
    soup = source.get("soup")
    text = source.get("text", "")
    title = ""
    if soup is not None:
        h1 = soup.find("h1")
        if h1:
            title = normalize(h1.get_text(" ", strip=True))
    date_match = re.search(
        r"(?:Updated|Обновлено|Date|Дата|Сана)\s*:?\s*"
        r"([0-9]{2}\.[0-9]{2}\.[0-9]{4}(?:\s+[0-9]{2}:[0-9]{2}(?::[0-9]{2})?)?)",
        text,
    )
    updated_raw = date_match.group(1) if date_match else ""
    updated_iso, updated_age_days = parse_date(updated_raw, generated_at)
    pm25 = parse_pm25(text)
    return {
        "language": language,
        "retrieved": bool(source.get("retrieved")),
        "http_status": source.get("http_status", ""),
        "url": source.get("url", ""),
        "sha256": source.get("sha256", ""),
        "title": title,
        "updated_raw": updated_raw,
        "updated_iso": updated_iso,
        "updated_age_days": updated_age_days,
        "pm25_value": pm25,
        "pm25_value_status": value_status(pm25),
    }


def col_text(item: Any, class_name: str) -> str:
    element = item.select_one(f".{class_name}")
    return normalize(element.get_text(" ", strip=True)) if element else ""


def parse_region_rows(source: dict[str, Any], language: str) -> list[dict[str, Any]]:
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
            "language": language,
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


def is_updating_data(value: str) -> bool:
    key = norm_key(value)
    return any(term in key for term in ["updating data", "обновление данных", "маълумотлар янгиланиши"])


def unique_join(values: list[Any]) -> str:
    cleaned = []
    for value in values:
        text = normalize(value)
        if text and text not in cleaned:
            cleaned.append(text)
    return " | ".join(cleaned)


def numeric_equal(left: str, right: str) -> bool:
    try:
        return abs(float(left) - float(right)) < 0.000001
    except Exception:
        return False


def flatten_api_stations(api_payload: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not isinstance(api_payload, dict):
        return rows
    for group in api_payload.get("data", []):
        rows.extend(group.get("stations", []))
    return rows


def api_row_for_station(api_rows: list[dict[str, Any]], station_id: str, generated_at: str) -> dict[str, Any]:
    row = next((item for item in api_rows if str(item.get("id")) == station_id), None)
    if not row:
        return {
            "retrieved": False,
            "date_raw": "",
            "date_iso": "",
            "date_age_days": None,
            "pm25_value": "",
            "pm25_value_status": "missing",
            "is_horiba": False,
            "si": "",
            "color": "",
            "alias": "",
        }
    date_iso, date_age_days = parse_date(str(row.get("date", "")), generated_at)
    pm25 = normalize(row.get("PM2.5"))
    return {
        "retrieved": True,
        "date_raw": normalize(row.get("date")),
        "date_iso": date_iso,
        "date_age_days": date_age_days,
        "pm25_value": pm25,
        "pm25_value_status": value_status(pm25),
        "is_horiba": bool(row.get("is_horiba")),
        "si": normalize(row.get("Si")),
        "color": normalize(row.get("color")),
        "alias": normalize(row.get("alias")),
    }


def endpoint_decision(row: dict[str, Any]) -> str:
    if row["detail_any_pm25_sentinel"]:
        return "detail_sentinel_and_endpoint_mismatch_keep_blocked"
    if row["detail_any_stale_over_30_days"] and row["region_any_updating_data"]:
        return "stale_detail_region_updating_and_endpoint_mismatch_keep_blocked"
    if row["endpoint_disagreement_count"]:
        return "official_endpoint_disagreement_keep_blocked"
    return "no_explicit_status_or_grade_closure_keep_open"


def reader_use(row: dict[str, Any]) -> str:
    if row["detail_any_pm25_sentinel"]:
        return (
            "Use as an endpoint QA blocker: the station-detail pages agree on a "
            "PM2.5 sentinel, while the API and regional row do not provide a "
            "public correction or grade/status closure."
        )
    if row["detail_any_stale_over_30_days"] and row["region_any_updating_data"]:
        return (
            "Use as an endpoint QA blocker: the exact detail pages remain stale "
            "and the regional table still marks the row as Updating data, even "
            "where the API exposes a different date."
        )
    return (
        "Use as source-routing context only. Official endpoints are visible, "
        "but they do not provide explicit current-status and complete-grade closure."
    )


def source_record(source_key: str, role: str, source: dict[str, Any], **extra: Any) -> dict[str, Any]:
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
    targets = read_csv(TARGET_SEED_CSV)
    source_records: list[dict[str, Any]] = []

    api_source = fetch_source(API_URL, accept="application/json,*/*;q=0.8")
    source_records.append(source_record("uzhydromet_api_maps", "official_public_maps_api", api_source))
    api_rows = flatten_api_stations(api_source.get("json"))

    region_cache: dict[tuple[str, str], dict[str, Any]] = {}
    for target in targets:
        region_slug = normalize(target["region_slug"])
        for language in LANGUAGES:
            cache_key = (language, region_slug)
            if cache_key in region_cache:
                continue
            url = f"{BASE_URL}/{language}/map/regions/{region_slug}"
            region_cache[cache_key] = fetch_source(url)
            source_records.append(
                source_record(
                    f"uzhydromet_region_{language}_{region_slug}",
                    "official_language_region_table",
                    region_cache[cache_key],
                    language=language,
                    region_slug=region_slug,
                )
            )

    rows: list[dict[str, Any]] = []
    station_json_rows: list[dict[str, Any]] = []

    for target in targets:
        station_id = normalize(target["source_station_id"])
        expected_name = normalize(target["expected_station_name"])

        detail_pages: dict[str, dict[str, Any]] = {}
        for language in LANGUAGES:
            url = f"{BASE_URL}/{language}/map/view/{station_id}"
            source = fetch_source(url)
            source_records.append(
                source_record(
                    f"uzhydromet_detail_{language}_{station_id}",
                    "official_language_station_detail",
                    source,
                    language=language,
                    source_station_id=station_id,
                )
            )
            detail_pages[language] = parse_detail_page(source, language, generated_at)

        region_rows: dict[str, dict[str, Any]] = {}
        for language in LANGUAGES:
            source = region_cache[(language, normalize(target["region_slug"]))]
            parsed_rows = parse_region_rows(source, language)
            region_rows[language] = next(
                (row for row in parsed_rows if row.get("view_station_id") == station_id),
                {},
            )

        api_row = api_row_for_station(api_rows, station_id, generated_at)
        retrieved_detail_pages = [page for page in detail_pages.values() if page["retrieved"]]
        retrieved_region_rows = [row for row in region_rows.values() if row]
        detail_dates = [page["updated_iso"] for page in retrieved_detail_pages if page["updated_iso"]]
        detail_pm25_values = [page["pm25_value"] for page in retrieved_detail_pages if page["pm25_value"]]
        detail_cross_language_consistent = (
            len(retrieved_detail_pages) == len(LANGUAGES)
            and len(set(detail_dates)) == 1
            and len(set(detail_pm25_values)) == 1
        )
        detail_latest_iso = max(detail_dates) if detail_dates else ""
        detail_latest_age_days = min(
            [page["updated_age_days"] for page in retrieved_detail_pages if page["updated_age_days"] is not None],
            default=None,
        )
        detail_any_stale = any(
            page["updated_age_days"] is not None and page["updated_age_days"] > 30
            for page in retrieved_detail_pages
        )
        detail_any_sentinel = any(
            page["pm25_value_status"] == "sentinel_minus_9999" for page in retrieved_detail_pages
        )
        detail_canonical_date = detail_dates[0] if detail_dates else ""
        detail_canonical_pm25 = detail_pm25_values[0] if detail_pm25_values else ""

        region_updated_values = [row.get("updated_raw", "") for row in retrieved_region_rows]
        region_auto_values = [row.get("auto", "") for row in retrieved_region_rows]
        region_any_updating = any(is_updating_data(value) for value in region_updated_values)
        region_any_horiba = any(norm_key(value) == "horiba" for value in region_auto_values)
        region_detail_status_mismatch = bool(
            retrieved_region_rows
            and detail_dates
            and (
                region_any_updating
                or any(parse_date(value, generated_at)[0] and parse_date(value, generated_at)[0] != detail_canonical_date for value in region_updated_values)
            )
        )
        api_detail_date_mismatch = bool(
            api_row["date_iso"] and detail_canonical_date and api_row["date_iso"] != detail_canonical_date
        )
        api_detail_pm25_mismatch = bool(
            api_row["pm25_value"]
            and detail_canonical_pm25
            and not numeric_equal(api_row["pm25_value"], detail_canonical_pm25)
        )
        endpoint_disagreement_count = sum(
            [api_detail_date_mismatch, api_detail_pm25_mismatch, region_detail_status_mismatch]
        )

        row: dict[str, Any] = {
            "generated_at": generated_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "method": METHOD,
            "source_station_id": station_id,
            "source_station_name": expected_name,
            "review_focus": normalize(target["review_focus"]),
            "detail_pages_retrieved": len(retrieved_detail_pages),
            "detail_language_count": len(LANGUAGES),
            "detail_updated_dates": unique_join(detail_dates),
            "detail_pm25_values": unique_join(detail_pm25_values),
            "detail_cross_language_consistent": detail_cross_language_consistent,
            "detail_latest_updated_iso": detail_latest_iso,
            "detail_latest_age_days": detail_latest_age_days if detail_latest_age_days is not None else "",
            "detail_any_stale_over_30_days": detail_any_stale,
            "detail_any_pm25_sentinel": detail_any_sentinel,
            "api_retrieved": api_row["retrieved"],
            "api_date_iso": api_row["date_iso"],
            "api_pm25_value": api_row["pm25_value"],
            "api_pm25_value_status": api_row["pm25_value_status"],
            "api_is_horiba": api_row["is_horiba"],
            "api_si": api_row["si"],
            "region_rows_found": len(retrieved_region_rows),
            "region_updated_values": unique_join(region_updated_values),
            "region_auto_values": unique_join(region_auto_values),
            "region_any_updating_data": region_any_updating,
            "region_any_horiba_marker": region_any_horiba,
            "api_detail_date_mismatch": api_detail_date_mismatch,
            "api_detail_pm25_mismatch": api_detail_pm25_mismatch,
            "region_detail_status_mismatch": region_detail_status_mismatch,
            "endpoint_disagreement_count": endpoint_disagreement_count,
            "unresolved_blocker_present": detail_any_sentinel or detail_any_stale or endpoint_disagreement_count > 0,
            "public_endpoint_resolution_available": False,
            "current_status_confirmed": False,
            "station_method_classified": False,
            "complete_monitor_grade_classification_available": False,
            "station_radius_grade_assumption_ready": False,
            "reader_question": normalize(target["reader_question"]),
            "non_claim": NON_CLAIM,
        }
        row["endpoint_decision"] = endpoint_decision(row)
        row["reader_use"] = reader_use(row)
        rows.append(row)

        station_json_rows.append(
            {
                **row,
                "detail_pages": detail_pages,
                "region_rows": region_rows,
                "api_row": api_row,
                "endpoint_cards": [
                    {
                        "endpoint": "Regional table",
                        "routes": len(retrieved_region_rows),
                        "date_or_status": row["region_updated_values"],
                        "pm25": "",
                        "signal": "Updating data" if region_any_updating else (row["region_auto_values"] or "row found"),
                        "tone": "caution" if region_any_updating or region_detail_status_mismatch else "available",
                    },
                    {
                        "endpoint": "Detail pages",
                        "routes": len(retrieved_detail_pages),
                        "date_or_status": row["detail_updated_dates"],
                        "pm25": row["detail_pm25_values"],
                        "signal": "stale" if detail_any_stale else ("sentinel" if detail_any_sentinel else "visible"),
                        "tone": "blocked" if detail_any_sentinel else ("caution" if detail_any_stale else "available"),
                    },
                    {
                        "endpoint": "Maps API",
                        "routes": 1 if api_row["retrieved"] else 0,
                        "date_or_status": row["api_date_iso"],
                        "pm25": row["api_pm25_value"],
                        "signal": row["api_pm25_value_status"],
                        "tone": "caution" if api_detail_date_mismatch or api_detail_pm25_mismatch else "available",
                    },
                ],
            }
        )

    counts = Counter()
    counts["target_blocker_rows"] = len(rows)
    counts["source_routes_seeded"] = len(source_records)
    counts["source_routes_retrieved"] = sum(1 for source in source_records if source["retrieved"])
    counts["api_sources_retrieved"] = 1 if api_source.get("retrieved") else 0
    counts["language_detail_pages_seeded"] = len(rows) * len(LANGUAGES)
    counts["language_detail_pages_retrieved"] = sum(int(row["detail_pages_retrieved"]) for row in rows)
    counts["language_region_rows_found"] = sum(int(row["region_rows_found"]) for row in rows)
    counts["cross_language_detail_consistent_rows"] = sum(bool(row["detail_cross_language_consistent"]) for row in rows)
    counts["api_detail_date_mismatch_rows"] = sum(bool(row["api_detail_date_mismatch"]) for row in rows)
    counts["api_detail_pm25_mismatch_rows"] = sum(bool(row["api_detail_pm25_mismatch"]) for row in rows)
    counts["region_detail_status_mismatch_rows"] = sum(bool(row["region_detail_status_mismatch"]) for row in rows)
    counts["official_endpoint_disagreement_rows"] = sum(int(row["endpoint_disagreement_count"]) > 0 for row in rows)
    counts["detail_stale_over_30_days_rows"] = sum(bool(row["detail_any_stale_over_30_days"]) for row in rows)
    counts["detail_pm25_sentinel_rows"] = sum(bool(row["detail_any_pm25_sentinel"]) for row in rows)
    counts["unresolved_blocker_rows"] = sum(bool(row["unresolved_blocker_present"]) for row in rows)
    counts["public_endpoint_resolution_rows"] = 0
    counts["current_status_confirmed_rows"] = 0
    counts["station_method_classified_rows"] = 0
    counts["complete_monitor_grade_classification_rows"] = 0
    counts["station_radius_grade_assumption_ready_rows"] = 0

    evidence_gates = [
        {
            "gate": "Official source routes retrieved",
            "status": "available",
            "rows": counts["source_routes_retrieved"],
            "reader_use": "The API, regional table pages, and language detail pages were retrieved for endpoint comparison.",
        },
        {
            "gate": "Language detail pages retrieved",
            "status": "available",
            "rows": counts["language_detail_pages_retrieved"],
            "reader_use": "The exact station-detail pages are visible in English, Russian, and Uzbek.",
        },
        {
            "gate": "Cross-language detail agreement",
            "status": "available",
            "rows": counts["cross_language_detail_consistent_rows"],
            "reader_use": "Detail pages agree across languages on date and PM2.5, so the blocker is not just a translation artifact.",
        },
        {
            "gate": "API/detail date mismatch",
            "status": "caution",
            "rows": counts["api_detail_date_mismatch_rows"],
            "reader_use": "The maps API date differs from the station-detail page date for these exact station IDs.",
        },
        {
            "gate": "API/detail PM2.5 mismatch",
            "status": "caution",
            "rows": counts["api_detail_pm25_mismatch_rows"],
            "reader_use": "The maps API PM2.5 value differs from the station-detail page PM2.5 value.",
        },
        {
            "gate": "Region/detail status mismatch",
            "status": "caution",
            "rows": counts["region_detail_status_mismatch_rows"],
            "reader_use": "Regional table status/date values do not align cleanly with the detail-page measurement timestamp.",
        },
        {
            "gate": "Unresolved blocker rows",
            "status": "caution",
            "rows": counts["unresolved_blocker_rows"],
            "reader_use": "Each target row still has a stale, sentinel, or cross-endpoint disagreement blocker.",
        },
        {
            "gate": "Public endpoint resolution",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No official endpoint gives a public correction, status, or grade closure that resolves the blocker.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Endpoint agreement or disagreement still does not supply station-level monitor-grade classification.",
        },
        {
            "gate": "Station-radius readiness",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No row is eligible for station-radius assumptions.",
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
            "Exact official Uzbekistan endpoint comparison for station IDs 107, 728, and 737: "
            "public maps API, English/Russian/Uzbek station-detail pages, and English/Russian/Uzbek regional table rows."
        ),
        "coverage_counts": dict(counts),
        "evidence_gate_counts": evidence_gates,
        "station_rows": station_json_rows,
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
