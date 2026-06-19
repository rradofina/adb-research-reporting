"""Scan official Uzbekistan station-specific pages for target-row evidence.

The previous source-policy scan found monitoring/cadence context but did not
name target station IDs. This pass tightens the evidence question: do public
official pages expose station-specific rows for the 28 Uzbekistan
instrument-hint stations, and do any official event notes independently name
the station/equipment context?

Station-specific table context remains separate from current-status and
complete monitor-grade classification. Regional map tables do not publish the
internal API station IDs, so they cannot close the station-ID gate by
themselves.
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

SEED_CSV = SOURCE_INPUTS_DIR / "uzbekistan-station-specific-source-seed.csv"
TARGET_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-current-method-scan.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-specific-source-evidence.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-station-specific-source-evidence-summary.json"

METHOD = "air_monitoring_uzbekistan_station_specific_source_evidence_v1"
STATUS = "computed_uzbekistan_station_specific_source_evidence"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This scan checks official station-specific web rows and official event "
    "text for target-row context. It does not certify a target station as "
    "currently operating, reference-grade, complete monitor-grade, or "
    "station-radius-ready."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "station_specific_evidence_id",
    "source_station_id",
    "source_station_name",
    "api_station_name",
    "api_alias",
    "api_region_id",
    "api_station_category",
    "api_reading_date_iso",
    "api_pm25_value_status",
    "official_region_table_match_found",
    "official_region_table_match_quality",
    "official_region_table_candidate_count",
    "official_region_name",
    "official_region_page_url",
    "official_region_page_sha256",
    "official_region_display_row_id",
    "official_region_row_name",
    "official_region_row_address",
    "official_region_row_auto",
    "official_region_row_updated_raw",
    "official_region_row_updated_iso",
    "official_region_row_updated_age_days",
    "official_region_horiba_context_found",
    "official_region_recent_update_within_30_days",
    "official_region_updating_data_status",
    "official_event_note_match_found",
    "official_event_note_url",
    "official_event_note_sha256",
    "official_event_note_terms",
    "station_specific_equipment_context_found",
    "station_specific_status_or_update_context_found",
    "target_station_id_named_in_non_api_source",
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


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def fetch_source(url: str, hint: str = "html") -> dict[str, Any]:
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
    except Exception as exc:  # noqa: BLE001 - retrieval failures are recorded as source evidence.
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def discover_region_links(main_source: dict[str, Any]) -> list[dict[str, str]]:
    soup = main_source.get("soup")
    if soup is None:
        return []
    links: list[dict[str, str]] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = urljoin(str(main_source["final_url"] or main_source["url"]), anchor["href"])
        if "/en/map/regions/" not in href or href in seen:
            continue
        seen.add(href)
        links.append({"region_name": normalize(anchor.get_text(" ", strip=True)), "url": href})
    return links


def col_text(item: Any, class_name: str) -> str:
    element = item.select_one(f".{class_name}")
    return normalize(element.get_text(" ", strip=True)) if element else ""


def parse_region_page(region: dict[str, str]) -> dict[str, Any]:
    fetched = fetch_source(region["url"])
    rows: list[dict[str, Any]] = []
    soup = fetched.get("soup")
    if soup is not None:
        for item in soup.select(".points-item"):
            row = {
                "region_name": region["region_name"],
                "region_page_url": region["url"],
                "region_page_sha256": fetched["sha256"],
                "display_row_id": col_text(item, "col-id"),
                "name": col_text(item, "col-name"),
                "address": col_text(item, "col-address"),
                "auto": col_text(item, "col-auto"),
                "updated_raw": col_text(item, "col-art"),
            }
            if any(row[field] for field in ("display_row_id", "name", "address", "auto", "updated_raw")):
                rows.append(row)
    return {"source": fetched, "rows": rows}


def parse_local_datetime(value: str) -> tuple[str, int | None]:
    raw = normalize(value)
    match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", raw)
    if not match:
        return "", None
    day, month, year = match.groups()
    parsed = datetime(int(year), int(month), int(day), tzinfo=timezone.utc)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return parsed.date().isoformat(), (today - parsed).days


def address_matches(target_address: str, row_address: str) -> bool:
    target = norm_key(target_address)
    row = norm_key(row_address)
    if not target:
        return not row
    return row == target or row.startswith(target) or target.startswith(row)


def pick_region_match(target: dict[str, str], candidates: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, str]:
    if not candidates:
        return None, "not_found"
    target_date = target.get("api_reading_date_iso", "")
    if target_date:
        date_matches = []
        for candidate in candidates:
            candidate_date, _ = parse_local_datetime(candidate["updated_raw"])
            if candidate_date == target_date:
                date_matches.append(candidate)
        if len(date_matches) == 1:
            return date_matches[0], "unique_by_name_address_and_update_date"
    if len(candidates) == 1:
        return candidates[0], "unique_name_address_match"
    updating = [
        candidate
        for candidate in candidates
        if "updating data" in norm_key(candidate["updated_raw"])
        or "обновление" in norm_key(candidate["updated_raw"])
        or "янгилан" in norm_key(candidate["updated_raw"])
    ]
    if len(updating) == 1:
        return updating[0], "duplicate_name_address_resolved_to_updating_status"
    return candidates[0], "duplicate_name_address_ambiguous"


def region_candidates(target: dict[str, str], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target_name = norm_key(target.get("api_station_name") or target.get("source_station_name"))
    target_address = target.get("api_station_category", "")
    exact = [
        row
        for row in rows
        if norm_key(row["name"]) == target_name and address_matches(target_address, row["address"])
    ]
    if exact:
        return exact
    if target_address:
        by_address = [row for row in rows if address_matches(target_address, row["address"])]
        if by_address:
            return by_address
    return [row for row in rows if norm_key(row["name"]) == target_name]


def event_terms_for_target(target: dict[str, str], event_text: str) -> list[str]:
    text = norm_key(event_text)
    terms = []
    alias_terms = {
        "uchtepa": ["uchtepa", "horiba", "pm2.5"],
        "jangi-uzbekistan": ["yangi o'zbekiston", "yangi o'zbekiston", "horiba", "pm2.5"],
    }
    for term in alias_terms.get(target.get("api_alias", ""), []):
        if norm_key(term) in text and term not in terms:
            terms.append(term)
    return terms


def station_decision(
    *,
    region_match: dict[str, Any] | None,
    match_quality: str,
    event_terms: list[str],
    updated_age_days: int | None,
) -> tuple[str, str]:
    if not region_match and not event_terms:
        return (
            "no_station_specific_source_match_keep_open",
            "No official station-specific table row or official event-note station mention was found.",
        )
    if match_quality == "duplicate_name_address_ambiguous":
        return (
            "station_specific_table_ambiguous_keep_open",
            "An official station-specific table row is nearby, but duplicate name/address rows prevent station-ID closure.",
        )
    if updated_age_days is not None and updated_age_days <= 30:
        return (
            "recent_station_table_row_keep_open",
            "The official table has a recent station-specific update, but no explicit current-status or complete grade statement.",
        )
    if event_terms:
        return (
            "station_specific_event_context_keep_open",
            "An official event note names station/equipment context, but it is not a current-status or complete-grade certification.",
        )
    return (
        "station_specific_table_context_keep_open",
        "The official table gives station-specific row context, but no internal station ID or complete grade statement.",
    )


def build_rows(
    generated_at: str,
    targets: list[dict[str, str]],
    region_rows: list[dict[str, Any]],
    event_source: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    event_text = event_source["text"] if event_source else ""
    event_url = event_source["final_url"] or event_source["url"] if event_source else ""
    event_sha = event_source["sha256"] if event_source else ""
    output = []
    for target in targets:
        candidates = region_candidates(target, region_rows)
        region_match, match_quality = pick_region_match(target, candidates)
        updated_iso = ""
        updated_age_days: int | None = None
        if region_match:
            updated_iso, updated_age_days = parse_local_datetime(region_match["updated_raw"])
        event_terms = event_terms_for_target(target, event_text)
        decision, reader_use = station_decision(
            region_match=region_match,
            match_quality=match_quality,
            event_terms=event_terms,
            updated_age_days=updated_age_days,
        )
        auto = region_match["auto"] if region_match else ""
        updated_raw = region_match["updated_raw"] if region_match else ""
        horiba_context = "horiba" in norm_key(auto)
        updating_status = "updating data" in norm_key(updated_raw)
        recent = updated_age_days is not None and updated_age_days <= 30
        event_match = bool(event_terms)
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "station_specific_evidence_id": f"UZB-station-specific-source-{target['source_station_id']}",
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "api_station_name": target["api_station_name"],
                "api_alias": target["api_alias"],
                "api_region_id": target["api_region_id"],
                "api_station_category": target["api_station_category"],
                "api_reading_date_iso": target["api_reading_date_iso"],
                "api_pm25_value_status": target["api_pm25_value_status"],
                "official_region_table_match_found": bool(region_match),
                "official_region_table_match_quality": match_quality,
                "official_region_table_candidate_count": len(candidates),
                "official_region_name": region_match["region_name"] if region_match else "",
                "official_region_page_url": region_match["region_page_url"] if region_match else "",
                "official_region_page_sha256": region_match["region_page_sha256"] if region_match else "",
                "official_region_display_row_id": region_match["display_row_id"] if region_match else "",
                "official_region_row_name": region_match["name"] if region_match else "",
                "official_region_row_address": region_match["address"] if region_match else "",
                "official_region_row_auto": auto,
                "official_region_row_updated_raw": updated_raw,
                "official_region_row_updated_iso": updated_iso,
                "official_region_row_updated_age_days": "" if updated_age_days is None else updated_age_days,
                "official_region_horiba_context_found": horiba_context,
                "official_region_recent_update_within_30_days": recent,
                "official_region_updating_data_status": updating_status,
                "official_event_note_match_found": event_match,
                "official_event_note_url": event_url if event_match else "",
                "official_event_note_sha256": event_sha if event_match else "",
                "official_event_note_terms": "|".join(event_terms),
                "station_specific_equipment_context_found": horiba_context or event_match,
                "station_specific_status_or_update_context_found": bool(region_match and (updated_raw or auto)) or event_match,
                "target_station_id_named_in_non_api_source": False,
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


def evidence_gates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    table_matches = sum(row["official_region_table_match_found"] for row in rows)
    unique_table = sum(
        row["official_region_table_match_found"]
        and row["official_region_table_match_quality"] != "duplicate_name_address_ambiguous"
        for row in rows
    )
    horiba_context = sum(row["station_specific_equipment_context_found"] for row in rows)
    recent_updates = sum(row["official_region_recent_update_within_30_days"] for row in rows)
    event_matches = sum(row["official_event_note_match_found"] for row in rows)
    return [
        {
            "gate": "Official regional station-table match",
            "status": "available",
            "rows": table_matches,
            "reader_use": "Target rows have official station-specific table rows on Uzhydromet regional pages.",
        },
        {
            "gate": "Unique station-table match",
            "status": "available" if unique_table == len(rows) else "partly_available",
            "rows": unique_table,
            "reader_use": "Rows matched without unresolved duplicate-name ambiguity.",
        },
        {
            "gate": "Station-specific equipment context",
            "status": "partly_available",
            "rows": horiba_context,
            "reader_use": "Official table or event text names Horiba/automatic station context, but not complete grade classification.",
        },
        {
            "gate": "Official table update within 30 days",
            "status": "partly_available",
            "rows": recent_updates,
            "reader_use": "Recent official table timestamps are follow-up priority, not explicit current-status certification.",
        },
        {
            "gate": "Official event-note station mention",
            "status": "partly_available",
            "rows": event_matches,
            "reader_use": "The official ecology note names station-specific event readings for two Tashkent stations.",
        },
        {
            "gate": "Target station ID named outside API",
            "status": "not_ready",
            "rows": sum(row["target_station_id_named_in_non_api_source"] for row in rows),
            "reader_use": "The official web tables expose display row numbers, not the internal target station IDs.",
        },
        {
            "gate": "Current-status confirmed",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No source states that each target station is currently active/current as of the scan date.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Station-specific Horiba context is not a complete reference-grade classification.",
        },
        {
            "gate": "Station-radius grade assumptions",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "Station-radius coverage remains blocked until station-grade assumptions are validated.",
        },
    ]


def summary(
    generated_at: str,
    rows: list[dict[str, Any]],
    source_records: list[dict[str, Any]],
    region_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    decision_counts = Counter(row["source_scan_decision"] for row in rows)
    match_counts = Counter(row["official_region_table_match_quality"] for row in rows)
    counts = {
        "target_uzbekistan_station_rows": len(rows),
        "sources_retrieved": sum(record["retrieved"] for record in source_records),
        "official_region_pages_retrieved": sum(
            record["retrieved"] and "/en/map/regions/" in record["url"] for record in source_records
        ),
        "official_region_station_rows_parsed": len(region_rows),
        "official_region_table_match_rows": sum(row["official_region_table_match_found"] for row in rows),
        "unique_official_region_table_match_rows": sum(
            row["official_region_table_match_found"]
            and row["official_region_table_match_quality"] != "duplicate_name_address_ambiguous"
            for row in rows
        ),
        "official_region_horiba_context_rows": sum(row["official_region_horiba_context_found"] for row in rows),
        "official_region_recent_update_within_30_days_rows": sum(
            row["official_region_recent_update_within_30_days"] for row in rows
        ),
        "official_region_updating_data_status_rows": sum(row["official_region_updating_data_status"] for row in rows),
        "official_event_note_match_rows": sum(row["official_event_note_match_found"] for row in rows),
        "station_specific_equipment_context_rows": sum(row["station_specific_equipment_context_found"] for row in rows),
        "target_station_id_named_in_non_api_source_rows": sum(
            row["target_station_id_named_in_non_api_source"] for row in rows
        ),
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    sample_fields = [
        "source_station_id",
        "api_alias",
        "official_region_name",
        "official_region_display_row_id",
        "official_region_row_name",
        "official_region_row_address",
        "official_region_row_auto",
        "official_region_row_updated_raw",
        "official_event_note_terms",
        "source_scan_decision",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Uzbekistan station-specific source scan",
        "coverage_counts": counts,
        "source_records": [
            {
                "source_key": record.get("source_key", ""),
                "source_role": record.get("source_role", ""),
                "url": record["url"],
                "final_url": record["final_url"],
                "retrieved": record["retrieved"],
                "http_status": record["http_status"],
                "content_type": record["content_type"],
                "retrieval_bytes": record["retrieval_bytes"],
                "sha256": record["sha256"],
            }
            for record in source_records
        ],
        "match_quality_rows": [
            {"official_region_table_match_quality": key, "rows": value}
            for key, value in sorted(match_counts.items())
        ],
        "decision_rows": [
            {"source_scan_decision": key, "rows": value}
            for key, value in sorted(decision_counts.items())
        ],
        "evidence_gate_counts": evidence_gates(rows),
        "station_sample_rows": [{field: row[field] for field in sample_fields} for row in rows[:12]],
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    targets = read_csv(TARGET_CSV)
    seed_by_key = {row["source_key"]: row for row in seed_rows}

    main_seed = seed_by_key["uzhydromet_main_map"]
    main_source = fetch_source(main_seed["url"], main_seed["content_type_hint"])
    main_source.update({"source_key": main_seed["source_key"], "source_role": main_seed["source_role"]})
    region_links = discover_region_links(main_source)

    source_records = [main_source]
    region_rows: list[dict[str, Any]] = []
    for region in region_links:
        parsed = parse_region_page(region)
        parsed["source"].update({"source_key": f"uzhydromet_region_{region['region_name']}", "source_role": "official_regional_station_table"})
        source_records.append(parsed["source"])
        region_rows.extend(parsed["rows"])

    event_seed = seed_by_key["gov_uz_eco_tashkent_pm25_event"]
    event_source = fetch_source(event_seed["url"], event_seed["content_type_hint"])
    event_source.update({"source_key": event_seed["source_key"], "source_role": event_seed["source_role"]})
    source_records.append(event_source)

    rows = build_rows(generated_at, targets, region_rows, event_source if event_source["retrieved"] else None)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary(generated_at, rows, source_records, region_rows))
    print(
        "Built Uzbekistan station-specific source evidence: "
        f"{len(rows)} target rows; "
        f"{sum(row['official_region_table_match_found'] for row in rows)} official regional table matches; "
        f"{sum(row['official_region_horiba_context_found'] for row in rows)} Horiba table rows; "
        f"{sum(row['official_event_note_match_found'] for row in rows)} official event-note matches; "
        "0 current-status confirmed rows."
    )


if __name__ == "__main__":
    main()
