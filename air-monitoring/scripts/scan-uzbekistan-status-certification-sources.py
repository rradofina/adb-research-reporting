"""Scan public Uzbekistan sources for status and certification evidence.

This pass follows the station-specific source scan. It asks a narrower
reviewer question: after official station-detail URLs close the target station
ID gate, do any public station-owner, regulator, or technical sources close
current-status, calibration/status, or complete monitor-grade classification?

The script deliberately keeps source-level context separate from exact station
closure. Source-level reference-grade or commissioning language can strengthen
the evidence ladder, but it cannot become a station-radius assumption unless
the exact station row is public and current/grade status is explicit.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "uzbekistan-status-certification-source-seed.csv"
STATION_SPECIFIC_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-station-specific-source-evidence.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-uzbekistan-status-certification-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-uzbekistan-status-certification-source-scan-summary.json"

METHOD = "air_monitoring_uzbekistan_status_certification_source_scan_v1"
STATUS = "computed_uzbekistan_status_certification_source_scan"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
TIMEOUT_SECONDS = 60
NON_CLAIM = (
    "This scan checks public source language for station-status, maintenance, "
    "calibration, and reference-grade context. It does not certify any target "
    "station as currently operating, complete monitor-grade, or station-radius-ready."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "status_certification_evidence_id",
    "source_station_id",
    "source_station_name",
    "api_alias",
    "official_region_name",
    "official_region_view_url",
    "official_detail_updated_iso",
    "official_detail_updated_age_days",
    "official_detail_recent_measurement_within_30_days",
    "official_detail_pm25_value",
    "official_detail_pm25_value_status",
    "official_region_horiba_context_found",
    "official_event_note_match_found",
    "source_level_method_context_sources",
    "source_level_current_context_sources",
    "source_level_certification_context_sources",
    "source_level_calibration_context_sources",
    "additional_exact_station_source_keys",
    "additional_context_source_keys",
    "tashkent_reference_grade_context_candidate",
    "district_commissioning_context_candidate",
    "regional_realtime_network_context_candidate",
    "stale_detail_measurement_followup",
    "sentinel_detail_measurement_followup",
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


def boolish(value: Any) -> bool:
    return norm_key(value) in {"true", "1", "yes"}


def fetch_source(seed: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_key": seed["source_key"],
        "source_name": seed["source_name"],
        "source_role": seed["source_role"],
        "url": seed["url"],
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "retrieval_error": "",
        "source_note": seed["source_note"],
    }
    try:
        response = requests.get(
            seed["url"],
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,text/plain,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        result["text"] = normalize(
            extract_text(response.content, response.text, result["content_type"], seed["content_type_hint"])
        )
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def extract_text(content: bytes, response_text: str, content_type: str, hint: str) -> str:
    lower = f"{content_type} {hint}".lower()
    if "pdf" in lower or content[:4] == b"%PDF":
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if "html" in lower:
        return BeautifulSoup(response_text, "html.parser").get_text(" ", strip=True)
    return response_text


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def build_source_rows(seed_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for seed in seed_rows:
        fetched = fetch_source(seed)
        text = fetched["text"]
        expected = split_terms(seed["expected_terms"])
        method_terms = split_terms(seed["method_terms"])
        current_terms = split_terms(seed["current_terms"])
        certification_terms = split_terms(seed["certification_terms"])
        calibration_terms = split_terms(seed["calibration_terms"])
        caution_terms = split_terms(seed["caution_terms"])
        fetched.update(
            {
                "matched_expected_terms": matched_terms(text, expected),
                "missing_expected_terms": [term for term in expected if term not in matched_terms(text, expected)],
                "matched_method_terms": matched_terms(text, method_terms),
                "matched_current_terms": matched_terms(text, current_terms),
                "matched_certification_terms": matched_terms(text, certification_terms),
                "matched_calibration_terms": matched_terms(text, calibration_terms),
                "matched_caution_terms": matched_terms(text, caution_terms),
            }
        )
        output.append(fetched)
    return output


def any_source_with(sources: list[dict[str, Any]], source_key: str, field: str) -> bool:
    return any(source["source_key"] == source_key and source["retrieved"] and source[field] for source in sources)


def retrieved_source(sources: list[dict[str, Any]], source_key: str) -> bool:
    return any(source["source_key"] == source_key and source["retrieved"] for source in sources)


def source_count(sources: list[dict[str, Any]], field: str) -> int:
    return sum(source["retrieved"] and bool(source[field]) for source in sources)


def station_additional_exact_keys(station: dict[str, str], sources: list[dict[str, Any]]) -> list[str]:
    station_id = station["source_station_id"]
    keys: list[str] = []
    if station_id in {"729", "733"} and retrieved_source(sources, "gov_uz_eco_event_en"):
        keys.append("gov_uz_eco_event_en")
    return keys


def station_additional_context_keys(station: dict[str, str], sources: list[dict[str, Any]]) -> list[str]:
    station_id = station["source_station_id"]
    keys: list[str] = []
    if station_id in {"107", "108"} and any_source_with(sources, "world_bank_tashkent_aqm_text", "matched_certification_terms"):
        keys.append("world_bank_tashkent_aqm_text")
    if station_id == "734" and retrieved_source(sources, "gov_uz_automatic_stations_tashkent_districts"):
        keys.append("gov_uz_automatic_stations_tashkent_districts")
    if station_id == "718" and retrieved_source(sources, "undp_aral_air_quality_2025"):
        keys.append("undp_aral_air_quality_2025")
    return keys


def station_decision(
    *,
    station: dict[str, str],
    exact_keys: list[str],
    context_keys: list[str],
    stale_detail: bool,
    sentinel_detail: bool,
) -> tuple[str, str]:
    if sentinel_detail:
        return (
            "sentinel_measurement_follow_up_keep_blocked",
            "The station-detail page is recent but the PM2.5 value is a negative sentinel; do not use it as current-status evidence.",
        )
    if stale_detail:
        return (
            "stale_detail_measurement_follow_up_keep_blocked",
            "The station-detail URL matches the target ID, but the latest detail timestamp is older than 30 days.",
        )
    if exact_keys:
        return (
            "exact_station_event_context_keep_open",
            "A public official source names the station in event context, but it does not certify current operating status or complete grade.",
        )
    if "world_bank_tashkent_aqm_text" in context_keys:
        return (
            "reference_grade_context_candidate_keep_open",
            "A technical report supports Tashkent Uzhydromet reference-grade context, but it does not name this public station ID.",
        )
    if "gov_uz_automatic_stations_tashkent_districts" in context_keys:
        return (
            "district_commissioning_context_candidate_keep_open",
            "A government page names district-level commissioning and maintenance context, but not the exact public station ID.",
        )
    if "undp_aral_air_quality_2025" in context_keys:
        return (
            "regional_realtime_network_context_candidate_keep_open",
            "A development-partner page supports regional 24/7 automatic network context, but not the exact target station grade.",
        )
    if boolish(station["official_detail_recent_measurement_within_30_days"]):
        return (
            "recent_detail_measurement_no_grade_keep_open",
            "The station-detail page has a recent measurement timestamp, but no complete current-status or grade statement.",
        )
    return (
        "station_id_context_no_status_or_grade_keep_open",
        "The official station-detail URL matches the target ID, but no stronger status or grade source was found.",
    )


def build_station_rows(
    generated_at: str,
    station_rows: list[dict[str, str]],
    source_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    method_count = source_count(source_rows, "matched_method_terms")
    current_count = source_count(source_rows, "matched_current_terms")
    certification_count = source_count(source_rows, "matched_certification_terms")
    calibration_count = source_count(source_rows, "matched_calibration_terms")

    output = []
    for station in station_rows:
        exact_keys = station_additional_exact_keys(station, source_rows)
        context_keys = station_additional_context_keys(station, source_rows)
        stale_detail = not boolish(station["official_detail_recent_measurement_within_30_days"])
        pm25_status = norm_key(station["official_detail_pm25_value_status"])
        sentinel_detail = pm25_status in {"negative", "sentinel_minus_9999"} or normalize(station["official_detail_pm25_value"]) == "-9999"
        decision, reader_use = station_decision(
            station=station,
            exact_keys=exact_keys,
            context_keys=context_keys,
            stale_detail=stale_detail,
            sentinel_detail=sentinel_detail,
        )
        output.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "status_certification_evidence_id": f"UZB-status-certification-{station['source_station_id']}",
                "source_station_id": station["source_station_id"],
                "source_station_name": station["source_station_name"],
                "api_alias": station["api_alias"],
                "official_region_name": station["official_region_name"],
                "official_region_view_url": station["official_region_view_url"],
                "official_detail_updated_iso": station["official_detail_updated_iso"],
                "official_detail_updated_age_days": station["official_detail_updated_age_days"],
                "official_detail_recent_measurement_within_30_days": boolish(
                    station["official_detail_recent_measurement_within_30_days"]
                ),
                "official_detail_pm25_value": station["official_detail_pm25_value"],
                "official_detail_pm25_value_status": station["official_detail_pm25_value_status"],
                "official_region_horiba_context_found": boolish(station["official_region_horiba_context_found"]),
                "official_event_note_match_found": boolish(station["official_event_note_match_found"]),
                "source_level_method_context_sources": method_count,
                "source_level_current_context_sources": current_count,
                "source_level_certification_context_sources": certification_count,
                "source_level_calibration_context_sources": calibration_count,
                "additional_exact_station_source_keys": "|".join(exact_keys),
                "additional_context_source_keys": "|".join(context_keys),
                "tashkent_reference_grade_context_candidate": "world_bank_tashkent_aqm_text" in context_keys,
                "district_commissioning_context_candidate": "gov_uz_automatic_stations_tashkent_districts" in context_keys,
                "regional_realtime_network_context_candidate": "undp_aral_air_quality_2025" in context_keys,
                "stale_detail_measurement_followup": stale_detail,
                "sentinel_detail_measurement_followup": sentinel_detail,
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


def source_record_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source_key": row["source_key"],
            "source_name": row["source_name"],
            "source_role": row["source_role"],
            "url": row["url"],
            "final_url": row["final_url"],
            "retrieved": row["retrieved"],
            "http_status": row["http_status"],
            "content_type": row["content_type"],
            "retrieval_bytes": row["retrieval_bytes"],
            "sha256": row["sha256"],
            "matched_expected_terms": row["matched_expected_terms"],
            "matched_method_terms": row["matched_method_terms"],
            "matched_current_terms": row["matched_current_terms"],
            "matched_certification_terms": row["matched_certification_terms"],
            "matched_calibration_terms": row["matched_calibration_terms"],
            "matched_caution_terms": row["matched_caution_terms"],
            "source_note": row["source_note"],
        }
        for row in source_rows
    ]


def evidence_gates(rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_failures = sum(not row["retrieved"] for row in source_rows)
    operating_context = source_count(source_rows, "matched_current_terms")
    reference_context = source_count(source_rows, "matched_certification_terms")
    calibration_context = source_count(source_rows, "matched_calibration_terms")
    exact_station_rows = sum(bool(row["additional_exact_station_source_keys"]) for row in rows)
    context_candidate_rows = sum(bool(row["additional_context_source_keys"]) for row in rows)
    stale_rows = sum(row["stale_detail_measurement_followup"] for row in rows)
    sentinel_rows = sum(row["sentinel_detail_measurement_followup"] for row in rows)
    return [
        {
            "gate": "Seeded source URLs retrieved",
            "status": "available" if source_failures == 0 else "limited",
            "rows": sum(row["retrieved"] for row in source_rows),
            "reader_use": "Retrieved public sources can be inspected for operating, grade, commissioning, and maintenance context.",
        },
        {
            "gate": "Source-level operating or online context",
            "status": "partly_available",
            "rows": operating_context,
            "reader_use": "Some public sources discuss observation, online, real-time, or commissioned automatic-station context.",
        },
        {
            "gate": "Source-level reference-grade or standards context",
            "status": "partly_available",
            "rows": reference_context,
            "reader_use": "Reference-grade or standards language is source-level unless exact station IDs are named.",
        },
        {
            "gate": "Maintenance or calibration context",
            "status": "partly_available",
            "rows": calibration_context,
            "reader_use": "Maintenance/training context helps the review queue but is not a calibration record for each station.",
        },
        {
            "gate": "Additional exact station source mention",
            "status": "partly_available",
            "rows": exact_station_rows,
            "reader_use": "Official event context names two stations but does not certify ongoing status or grade.",
        },
        {
            "gate": "Additional station-context candidate",
            "status": "partly_available",
            "rows": context_candidate_rows,
            "reader_use": "Context candidates help prioritize follow-up but do not close station-level certification.",
        },
        {
            "gate": "Stale detail measurement follow-up",
            "status": "caution",
            "rows": stale_rows,
            "reader_use": "Rows with detail timestamps older than 30 days stay out of current-status closure.",
        },
        {
            "gate": "Sentinel detail measurement follow-up",
            "status": "caution",
            "rows": sentinel_rows,
            "reader_use": "Rows with negative sentinel PM2.5 values stay out of current-status closure.",
        },
        {
            "gate": "Current-status confirmed",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No public source explicitly confirms current operation for each target station row.",
        },
        {
            "gate": "Complete monitor-grade classification",
            "status": "not_ready",
            "rows": 0,
            "reader_use": "No public source gives complete station-level monitor-grade classification for the 28 target rows.",
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
    source_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    decision_counts = Counter(row["source_scan_decision"] for row in rows)
    counts = {
        "target_uzbekistan_station_rows": len(rows),
        "source_urls_seeded": len(source_rows),
        "source_urls_retrieved": sum(row["retrieved"] for row in source_rows),
        "source_urls_failed": sum(not row["retrieved"] for row in source_rows),
        "source_level_method_context_sources": source_count(source_rows, "matched_method_terms"),
        "source_level_current_context_sources": source_count(source_rows, "matched_current_terms"),
        "source_level_certification_context_sources": source_count(source_rows, "matched_certification_terms"),
        "source_level_calibration_context_sources": source_count(source_rows, "matched_calibration_terms"),
        "additional_exact_station_source_mention_rows": sum(bool(row["additional_exact_station_source_keys"]) for row in rows),
        "tashkent_reference_grade_context_candidate_rows": sum(row["tashkent_reference_grade_context_candidate"] for row in rows),
        "district_commissioning_context_candidate_rows": sum(row["district_commissioning_context_candidate"] for row in rows),
        "regional_realtime_network_context_candidate_rows": sum(row["regional_realtime_network_context_candidate"] for row in rows),
        "official_detail_recent_measurement_rows": sum(row["official_detail_recent_measurement_within_30_days"] for row in rows),
        "stale_detail_measurement_followup_rows": sum(row["stale_detail_measurement_followup"] for row in rows),
        "sentinel_detail_measurement_followup_rows": sum(row["sentinel_detail_measurement_followup"] for row in rows),
        "current_status_confirmed_rows": 0,
        "station_method_classified_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    sample_fields = [
        "source_station_id",
        "source_station_name",
        "official_region_name",
        "official_detail_updated_iso",
        "official_detail_pm25_value",
        "additional_exact_station_source_keys",
        "additional_context_source_keys",
        "source_scan_decision",
    ]
    priority_rows = [
        row
        for row in rows
        if row["source_scan_decision"] != "recent_detail_measurement_no_grade_keep_open"
    ]
    filler_rows = [
        row
        for row in rows
        if row["source_scan_decision"] == "recent_detail_measurement_no_grade_keep_open"
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Uzbekistan status/certification source scan",
        "coverage_counts": counts,
        "source_records": source_record_rows(source_rows),
        "decision_rows": [
            {"source_scan_decision": decision, "rows": count}
            for decision, count in sorted(decision_counts.items())
        ],
        "evidence_gate_counts": evidence_gates(rows, source_rows),
        "station_sample_rows": [
            {field: row[field] for field in sample_fields}
            for row in [*priority_rows, *filler_rows][:14]
        ],
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> None:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_CSV)
    station_rows = read_csv(STATION_SPECIFIC_CSV)
    source_rows = build_source_rows(seed_rows)
    rows = build_station_rows(generated_at, station_rows, source_rows)
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary(generated_at, rows, source_rows))
    print(
        "Built Uzbekistan status/certification source scan: "
        f"{len(rows)} target rows; "
        f"{sum(row['retrieved'] for row in source_rows)}/{len(source_rows)} sources retrieved; "
        f"{sum(bool(row['additional_exact_station_source_keys']) for row in rows)} exact station mention rows; "
        f"{sum(row['stale_detail_measurement_followup'] for row in rows)} stale detail rows; "
        f"{sum(row['sentinel_detail_measurement_followup'] for row in rows)} sentinel detail rows; "
        "0 current-status confirmed rows."
    )


if __name__ == "__main__":
    main()
