"""Scan Indonesia and Georgia exact PM2.5 rows for method/source closure.

The station method-evidence audit left 38 exact PM2.5 portal/API rows open:
22 BMKG Indonesia rows and 16 air.gov.ge Georgia rows. This pass retrieves
public station-owner or regulator sources that may connect source-level method
language to those exact rows, while keeping current-status and complete
monitor-grade gates closed unless the public evidence is station-level and
explicit.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "indonesia-georgia-row-method-source-seed.csv"
METHOD_EVIDENCE_CSV = GENERATED_DIR / "air-monitoring-monitor-grade-station-method-evidence.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-indonesia-georgia-row-method-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-indonesia-georgia-row-method-source-scan-summary.json"

METHOD = "air_monitoring_indonesia_georgia_row_method_source_scan_v1"
STATUS = "computed_indonesia_georgia_row_method_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This scan checks public Indonesia and Georgia source language for exact-row "
    "method, operating, and station-context evidence. It does not certify any "
    "station as currently operating, complete monitor-grade, or station-radius-ready."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "row_method_source_scan_id",
    "method_evidence_id",
    "iso3",
    "country",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "exact_source_evidence_type",
    "exact_source_station_category",
    "exact_pm25_signal",
    "exact_live_pm25_value_raw",
    "exact_live_pm25_value_status",
    "public_current_row_observed_from_prior_audit",
    "source_urls_retrieved_for_country",
    "source_level_method_context_sources",
    "source_level_current_context_sources",
    "source_level_standard_context_sources",
    "exact_station_detail_source_retrieved",
    "exact_station_detail_url",
    "exact_station_detail_timestamp_raw",
    "exact_station_detail_timestamp_iso",
    "exact_station_detail_recent_within_30_days",
    "exact_station_detail_value_raw",
    "exact_station_detail_method_terms",
    "exact_station_id_source_keys",
    "exact_station_name_source_keys",
    "station_alias_context_source_keys",
    "same_page_method_context_candidate",
    "same_page_current_context_candidate",
    "source_level_method_context_candidate",
    "source_level_current_context_candidate",
    "station_context_candidate",
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
        "soup": None,
        "retrieval_error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,text/plain,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        text, soup = extract_text(response.content, response.text, result["content_type"], content_type_hint)
        result["text"] = normalize(text)
        result["soup"] = soup
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def extract_text(content: bytes, response_text: str, content_type: str, hint: str) -> tuple[str, BeautifulSoup | None]:
    lower = f"{content_type} {hint}".lower()
    if "pdf" in lower or content[:4] == b"%PDF":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages), None
    soup = BeautifulSoup(response_text, "html.parser")
    return soup.get_text(" ", strip=True), soup


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(METHOD_EVIDENCE_CSV)
    output = [
        row
        for row in rows
        if row["iso3"] in {"IDN", "GEO"} and row["row_evidence_lane"] == "row_level_pm25_portal_or_api"
    ]
    output.sort(key=lambda row: (row["iso3"], row["source_station_id"]))
    return output


def expanded_seed_rows(seed_rows: list[dict[str, str]], targets: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for seed in seed_rows:
        if "{source_station_id}" not in seed["url"]:
            output.append({**seed, "expanded_for_station_id": "", "expanded_for_station_name": ""})
            continue
        for row in targets:
            if row["iso3"] != seed["iso3"]:
                continue
            output.append(
                {
                    **seed,
                    "url": seed["url"].replace("{source_station_id}", row["source_station_id"]),
                    "source_key": f"{seed['source_key']}_{row['source_station_id']}",
                    "expanded_for_station_id": row["source_station_id"],
                    "expanded_for_station_name": row["source_station_name"],
                }
            )
    return output


def build_source_rows(seed_rows: list[dict[str, str]], targets: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for seed in expanded_seed_rows(seed_rows, targets):
        fetched = fetch_url(seed["url"], seed["content_type_hint"])
        text = fetched["text"]
        expected = split_terms(seed["expected_terms"])
        method_terms = split_terms(seed["method_terms"])
        current_terms = split_terms(seed["current_terms"])
        standard_terms = split_terms(seed["standard_terms"])
        caution_terms = split_terms(seed["caution_terms"])
        output.append(
            {
                "source_key": seed["source_key"],
                "source_name": seed["source_name"],
                "source_role": seed["source_role"],
                "iso3": seed["iso3"],
                "country": seed["country"],
                "url": seed["url"],
                "final_url": fetched["final_url"],
                "retrieved": fetched["retrieved"],
                "http_status": fetched["http_status"],
                "content_type": fetched["content_type"],
                "retrieval_bytes": fetched["retrieval_bytes"],
                "sha256": fetched["sha256"],
                "retrieval_error": fetched["retrieval_error"],
                "text": text,
                "soup": fetched["soup"],
                "expanded_for_station_id": seed.get("expanded_for_station_id", ""),
                "expanded_for_station_name": seed.get("expanded_for_station_name", ""),
                "matched_expected_terms": matched_terms(text, expected),
                "missing_expected_terms": [term for term in expected if term not in matched_terms(text, expected)],
                "matched_method_terms": matched_terms(text, method_terms),
                "matched_current_terms": matched_terms(text, current_terms),
                "matched_standard_terms": matched_terms(text, standard_terms),
                "matched_caution_terms": matched_terms(text, caution_terms),
                "source_note": seed["source_note"],
            }
        )
    return output


def source_record_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source_key": row["source_key"],
            "source_name": row["source_name"],
            "source_role": row["source_role"],
            "iso3": row["iso3"],
            "url": row["url"],
            "final_url": row["final_url"],
            "retrieved": row["retrieved"],
            "http_status": row["http_status"],
            "content_type": row["content_type"],
            "retrieval_bytes": row["retrieval_bytes"],
            "sha256": row["sha256"],
            "expanded_for_station_id": row["expanded_for_station_id"],
            "matched_expected_terms": row["matched_expected_terms"],
            "matched_method_terms": row["matched_method_terms"],
            "matched_current_terms": row["matched_current_terms"],
            "matched_standard_terms": row["matched_standard_terms"],
            "matched_caution_terms": row["matched_caution_terms"],
            "retrieval_error": row["retrieval_error"],
            "source_note": row["source_note"],
        }
        for row in source_rows
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


def parse_bmkg_timestamp(text: str) -> tuple[str, str]:
    match = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4}),\s+(\d{1,2})\.(\d{2})\s+WIB", text)
    if not match:
        return "", ""
    day, month_raw, year, hour, minute = match.groups()
    month = MONTHS.get(month_raw.casefold())
    if not month:
        return match.group(0), ""
    parsed = datetime(int(year), month, int(day), int(hour), int(minute), tzinfo=timezone.utc)
    return match.group(0), parsed.isoformat().replace("+00:00", "Z")


def parse_bmkg_value(text: str, station_name: str) -> str:
    station = re.escape(normalize(station_name))
    pattern = rf"(\d+(?:[,.]\d+)?)\s*(?:ug/m\^3|µg/m\^3|ug/m3|µg/m3)\s+di\s+{station}"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return match.group(1).replace(",", ".")
    generic = re.search(r"(\d+(?:[,.]\d+)?)\s*(?:ug/m\^3|µg/m\^3|ug/m3|µg/m3)", text, flags=re.IGNORECASE)
    return generic.group(1).replace(",", ".") if generic else ""


def iso_date_recent_within_30_days(value: str, generated_at: str) -> bool:
    if not value:
        return False
    try:
        observed = datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        generated = datetime.fromisoformat(generated_at.replace("Z", "+00:00")).date()
    except ValueError:
        return False
    age = (generated - observed).days
    return 0 <= age <= 30


def station_alias_terms(row: dict[str, str]) -> list[str]:
    name = normalize(row["source_station_name"])
    if row["iso3"] == "IDN":
        return [name]
    preferred = {
        "01005": ["Tazakendi"],
        "AGMS": ["Agmashenebeli"],
        "BTUM": ["Abuseridze"],
        "KUTS": ["Asatiani"],
        "KZBG": ["Kazbegi"],
        "ORN01": ["Gelovani"],
        "ORN02": ["Friendship"],
        "ORN04": ["Ninoshvili"],
        "ORN05": ["Zugdidi"],
        "ORN06": ["Mestia"],
        "ORN07": ["Telavi"],
        "ORN08": ["Akhaltsikhe"],
        "TSRT": ["Tsereteli"],
        "VRKT": ["Varketili"],
    }
    return preferred.get(row["source_station_id"], [])


def source_keys_with_text(source_rows: list[dict[str, Any]], term: str) -> list[str]:
    if not term:
        return []
    key = norm_key(term)
    return [row["source_key"] for row in source_rows if row["retrieved"] and key in norm_key(row["text"])]


def detail_source_for(row: dict[str, str], source_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    for source in source_rows:
        if source["expanded_for_station_id"] == row["source_station_id"]:
            return source
    return None


def country_source_rows(row: dict[str, str], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        source
        for source in source_rows
        if source["iso3"] == row["iso3"]
        and (not source["expanded_for_station_id"] or source["expanded_for_station_id"] == row["source_station_id"])
    ]


def station_decision(
    *,
    row: dict[str, str],
    detail_source: dict[str, Any] | None,
    exact_id_keys: list[str],
    exact_name_keys: list[str],
    alias_keys: list[str],
    source_level_method: bool,
    source_level_current: bool,
) -> tuple[str, str]:
    if row["iso3"] == "IDN" and detail_source and detail_source["retrieved"] and detail_source["matched_method_terms"]:
        return (
            "exact_bmkg_detail_method_context_keep_not_grade_ready",
            "BMKG station-detail pages connect the exact station page to Beta Attenuation Monitoring language, but they do not provide complete station-grade/current-status certification.",
        )
    if row["iso3"] == "GEO" and alias_keys:
        return (
            "georgia_station_alias_context_keep_not_grade_ready",
            "Georgia sources provide station or place context for a target row, but not a station-code method table or complete grade/current-status certification.",
        )
    if exact_id_keys or exact_name_keys:
        return (
            "exact_row_source_context_keep_open",
            "A public source names the row or station, but source language is not complete station-grade certification.",
        )
    if source_level_method or source_level_current:
        return (
            "source_level_context_only_keep_open",
            "Country source context exists, but it is not connected to the exact station row strongly enough for grade assumptions.",
        )
    return (
        "no_new_station_method_closure_keep_open",
        "The scan found no public source that closes exact station method, current-status, or grade classification.",
    )


def build_station_rows(generated_at: str, targets: list[dict[str, str]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in targets:
        relevant_sources = country_source_rows(row, source_rows)
        source_level_method = [source for source in relevant_sources if source["retrieved"] and source["matched_method_terms"]]
        source_level_current = [source for source in relevant_sources if source["retrieved"] and source["matched_current_terms"]]
        source_level_standard = [source for source in relevant_sources if source["retrieved"] and source["matched_standard_terms"]]

        detail_source = detail_source_for(row, source_rows)
        detail_text = detail_source["text"] if detail_source and detail_source["retrieved"] else ""
        detail_timestamp_raw, detail_timestamp_iso = parse_bmkg_timestamp(detail_text)
        detail_value_raw = parse_bmkg_value(detail_text, row["source_station_name"]) if detail_text else ""
        detail_recent = iso_date_recent_within_30_days(detail_timestamp_iso, generated_at)

        exact_id_keys = source_keys_with_text(relevant_sources, row["source_station_id"])
        exact_name_keys = source_keys_with_text(relevant_sources, row["source_station_name"])
        alias_keys = []
        for term in station_alias_terms(row):
            alias_keys.extend(source_keys_with_text(relevant_sources, term))
        alias_keys = sorted(set(alias_keys) - set(exact_name_keys))

        same_page_method = bool(detail_source and detail_source["retrieved"] and detail_source["matched_method_terms"])
        same_page_current = bool(detail_source and detail_source["retrieved"] and detail_source["matched_current_terms"])
        station_context = bool(exact_id_keys or exact_name_keys or alias_keys)
        decision, reader_use = station_decision(
            row=row,
            detail_source=detail_source,
            exact_id_keys=exact_id_keys,
            exact_name_keys=exact_name_keys,
            alias_keys=alias_keys,
            source_level_method=bool(source_level_method),
            source_level_current=bool(source_level_current),
        )
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "row_method_source_scan_id": f"{row['iso3']}-row-method-source-{row['source_station_id']}",
                "method_evidence_id": row["method_evidence_id"],
                "iso3": row["iso3"],
                "country": row["country"],
                "source_station_id": row["source_station_id"],
                "source_station_name": row["source_station_name"],
                "source_station_type": row["source_station_type"],
                "exact_source_evidence_type": row["exact_source_evidence_type"],
                "exact_source_station_category": row["exact_source_station_category"],
                "exact_pm25_signal": boolish(row["exact_pm25_signal"]),
                "exact_live_pm25_value_raw": row["exact_live_pm25_value_raw"],
                "exact_live_pm25_value_status": row["exact_live_pm25_value_status"],
                "public_current_row_observed_from_prior_audit": boolish(row["public_current_row_observed"]),
                "source_urls_retrieved_for_country": sum(source["retrieved"] for source in relevant_sources),
                "source_level_method_context_sources": len(source_level_method),
                "source_level_current_context_sources": len(source_level_current),
                "source_level_standard_context_sources": len(source_level_standard),
                "exact_station_detail_source_retrieved": bool(detail_source and detail_source["retrieved"]),
                "exact_station_detail_url": detail_source["url"] if detail_source else "",
                "exact_station_detail_timestamp_raw": detail_timestamp_raw,
                "exact_station_detail_timestamp_iso": detail_timestamp_iso,
                "exact_station_detail_recent_within_30_days": detail_recent,
                "exact_station_detail_value_raw": detail_value_raw,
                "exact_station_detail_method_terms": "|".join(detail_source["matched_method_terms"]) if detail_source else "",
                "exact_station_id_source_keys": "|".join(sorted(set(exact_id_keys))),
                "exact_station_name_source_keys": "|".join(sorted(set(exact_name_keys))),
                "station_alias_context_source_keys": "|".join(sorted(set(alias_keys))),
                "same_page_method_context_candidate": same_page_method,
                "same_page_current_context_candidate": same_page_current,
                "source_level_method_context_candidate": bool(source_level_method),
                "source_level_current_context_candidate": bool(source_level_current),
                "station_context_candidate": station_context,
                "current_status_confirmed": False,
                "station_method_classified": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "source_scan_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return output


def country_rows(rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country_station_rows = [row for row in rows if row["iso3"] == iso3]
        country_sources = [source for source in source_rows if source["iso3"] == iso3]
        output.append(
            {
                "iso3": iso3,
                "country": country_station_rows[0]["country"],
                "target_rows": len(country_station_rows),
                "source_urls_retrieved": sum(source["retrieved"] for source in country_sources),
                "source_urls_seeded_or_expanded": len(country_sources),
                "prior_exact_pm25_rows": sum(row["exact_pm25_signal"] for row in country_station_rows),
                "positive_prior_raw_value_rows": sum(row["exact_live_pm25_value_status"] == "positive_raw_value" for row in country_station_rows),
                "missing_prior_raw_value_rows": sum(row["exact_live_pm25_value_status"] == "missing_raw_value" for row in country_station_rows),
                "same_page_method_context_candidate_rows": sum(row["same_page_method_context_candidate"] for row in country_station_rows),
                "same_page_current_context_candidate_rows": sum(row["same_page_current_context_candidate"] for row in country_station_rows),
                "station_context_candidate_rows": sum(row["station_context_candidate"] for row in country_station_rows),
                "current_status_confirmed_rows": 0,
                "station_method_classified_rows": 0,
                "complete_monitor_grade_classification_rows": 0,
                "station_radius_grade_assumption_ready_rows": 0,
            }
        )
    return output


def gate(status: str, gate_name: str, rows: int, reader_use_text: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use_text}


def evidence_gates(rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_failures = sum(not row["retrieved"] for row in source_rows)
    return [
        gate(
            "available" if source_failures == 0 else "limited",
            "Seeded and expanded source URLs retrieved",
            sum(row["retrieved"] for row in source_rows),
            "Retrieved source text can be inspected for station rows, method terms, current-display terms, and standards context.",
        ),
        gate(
            "available",
            "Prior exact PM2.5 portal/API rows",
            sum(row["exact_pm25_signal"] for row in rows),
            "The previous exact-row audit already confirms PM2.5 row presence for these Indonesia and Georgia targets.",
        ),
        gate(
            "partly_available",
            "Exact station-detail method context candidates",
            sum(row["same_page_method_context_candidate"] for row in rows),
            "BMKG station-detail pages place station names, current PM2.5 display, and Beta Attenuation Monitoring text on the same public page.",
        ),
        gate(
            "partly_available",
            "Station or alias context candidates",
            sum(row["station_context_candidate"] for row in rows),
            "Some sources name exact station rows or recognizable station/place aliases; this is context, not grade closure.",
        ),
        gate(
            "partly_available",
            "Source-level method or standard context",
            sum(row["source_level_method_context_candidate"] or row["source_level_standard_context_sources"] > 0 for row in rows),
            "Country-level method and standards language is useful for the evidence ladder but remains insufficient for station-radius assumptions.",
        ),
        gate(
            "not_ready",
            "Current-status confirmed",
            0,
            "A current PM2.5 display is not the same as a public station-status certification.",
        ),
        gate(
            "not_ready",
            "Station method classified",
            0,
            "No public source gives a complete station-level method table for all 38 exact rows.",
        ),
        gate(
            "not_ready",
            "Complete monitor-grade classification",
            0,
            "No public source classifies the 38 exact rows as complete monitor-grade records.",
        ),
        gate(
            "not_ready",
            "Station-radius grade assumptions",
            0,
            "Station-radius coverage remains blocked until current status, method class, and complete grade are public and row-level.",
        ),
    ]


def summary_payload(generated_at: str, rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_indonesia_georgia_rows": len(rows),
        "target_indonesia_rows": sum(row["iso3"] == "IDN" for row in rows),
        "target_georgia_rows": sum(row["iso3"] == "GEO" for row in rows),
        "source_urls_seeded_or_expanded": len(source_rows),
        "source_urls_retrieved": sum(row["retrieved"] for row in source_rows),
        "source_urls_failed": sum(not row["retrieved"] for row in source_rows),
        "prior_exact_pm25_rows": sum(row["exact_pm25_signal"] for row in rows),
        "positive_prior_raw_value_rows": sum(row["exact_live_pm25_value_status"] == "positive_raw_value" for row in rows),
        "missing_prior_raw_value_rows": sum(row["exact_live_pm25_value_status"] == "missing_raw_value" for row in rows),
        "exact_station_detail_retrieved_rows": sum(row["exact_station_detail_source_retrieved"] for row in rows),
        "exact_station_detail_recent_within_30_days_rows": sum(row["exact_station_detail_recent_within_30_days"] for row in rows),
        "same_page_method_context_candidate_rows": sum(row["same_page_method_context_candidate"] for row in rows),
        "same_page_current_context_candidate_rows": sum(row["same_page_current_context_candidate"] for row in rows),
        "station_context_candidate_rows": sum(row["station_context_candidate"] for row in rows),
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    sample_fields = [
        "iso3",
        "source_station_id",
        "source_station_name",
        "exact_live_pm25_value_status",
        "exact_station_detail_timestamp_raw",
        "same_page_method_context_candidate",
        "station_alias_context_source_keys",
        "source_scan_decision",
    ]
    prioritized = sorted(
        rows,
        key=lambda row: (
            row["iso3"] != "IDN",
            not row["same_page_method_context_candidate"],
            not row["station_context_candidate"],
            row["source_station_id"],
        ),
    )
    idn_samples = [row for row in prioritized if row["iso3"] == "IDN"][:8]
    geo_context_samples = [row for row in rows if row["iso3"] == "GEO" and row["station_context_candidate"]][:6]
    geo_open_samples = [row for row in rows if row["iso3"] == "GEO" and not row["station_context_candidate"]][:2]
    sample_rows = [*idn_samples, *geo_context_samples, *geo_open_samples]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Indonesia/Georgia row-method source scan",
        "source_inputs": [
            {
                "path": str(SEED_CSV.relative_to(PROGRAM_DIR)),
                "role": "seeded Indonesia and Georgia public source URLs, including BMKG station-detail URL template",
            },
            {
                "path": str(METHOD_EVIDENCE_CSV.relative_to(PROGRAM_DIR)),
                "role": "exact station method-evidence audit; source of the 38 target rows",
            },
        ],
        "coverage_counts": counts,
        "country_rows": country_rows(rows, source_rows),
        "decision_counts": [
            {"decision": key, "rows": value}
            for key, value in sorted(Counter(row["source_scan_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": evidence_gates(rows, source_rows),
        "source_records": source_record_rows(source_rows),
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
    seed_rows = read_csv(SEED_CSV)
    source_rows = build_source_rows(seed_rows, targets)
    rows = build_station_rows(generated_at, targets, source_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary_payload(generated_at, rows, source_rows))
    counts = Counter(row["source_scan_decision"] for row in rows)
    print(
        "Built Indonesia/Georgia row-method source scan: "
        f"{len(rows)} target rows; "
        f"{sum(row['retrieved'] for row in source_rows)}/{len(source_rows)} sources retrieved; "
        f"{sum(row['same_page_method_context_candidate'] for row in rows)} same-page method context candidates; "
        "0 complete grade rows; "
        f"decisions={dict(counts)}."
    )


if __name__ == "__main__":
    main()
