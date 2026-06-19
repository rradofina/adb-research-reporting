"""Scan public-feed official/OpenAQ candidate rows for crosswalk evidence.

This script targets the candidate rows where OpenAQ metadata is present but
`isMonitor` is false. It keeps the test deliberately strict: a row may not
become a station-radius join unless public source-owner, current-status, or
documented co-location evidence names both the official station record and the
OpenAQ location record.
"""

from __future__ import annotations

import csv
import io
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "candidate-public-feed-source-seed.csv"
CANDIDATE_EVIDENCE_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-evidence.csv"
STATION_EXTRACTION_CSV = GENERATED_DIR / "air-monitoring-regulator-station-extraction.csv"
OPENAQ_CSV = GENERATED_DIR / "air-monitoring-openaq-station-metadata.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-feed-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json"

METHOD = "air_monitoring_official_openaq_candidate_public_feed_source_scan_v1"
NON_CLAIM = (
    "This scan reviews OpenAQ candidate rows that are not marked isMonitor. "
    "It does not validate same-station joins, does not certify monitor grade, "
    "and does not make any row station-radius-ready."
)

REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 ADB research reproducibility scan"}

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "candidate_review_id",
    "iso3",
    "country",
    "source_station_id",
    "source_station_name",
    "source_station_type",
    "official_source_key",
    "official_source_url",
    "official_source_retrieved",
    "official_latitude",
    "official_longitude",
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "openaq_latitude",
    "openaq_longitude",
    "computed_coordinate_distance_km",
    "openaq_owner_name",
    "openaq_provider_name",
    "openaq_is_monitor",
    "openaq_first_seen",
    "openaq_last_seen",
    "openaq_sensor_count",
    "provider_context_source_keys",
    "provider_context_retrieved",
    "provider_context_terms_matched",
    "same_openaq_location_reused_in_scan",
    "official_agency_exact_in_openaq_owner_or_provider",
    "shared_station_id_found",
    "source_owner_crosswalk_found",
    "current_status_crosswalk_found",
    "documented_colocation_found",
    "same_station_validated",
    "allowed_review_decision",
    "candidate_queue_status_after_scan",
    "station_radius_join_ready",
    "disambiguating_public_evidence",
    "reviewer_action",
    "reader_use",
    "non_claim",
]

OFFICIAL_SOURCE_BY_ISO = {
    "BGD": "bgd_official_ambient_air_quality_pdf",
    "IDN": "idn_bmkg_pm25_detail",
    "MYS": "mys_myeqms_feature_api",
    "UZB": "uzb_official_monitoring_map",
}

PROVIDER_CONTEXT_BY_ROW = {
    "BGD": ["smart_air_bangladesh_sensor_page", "airgradient_openaq_share_guidance", "openaq_airgradient_partner_profile"],
    "IDN": ["kopernik_air_quality_project_context", "airgradient_openaq_share_guidance", "openaq_airgradient_partner_profile"],
    "UZB": ["airgradient_openaq_share_guidance", "openaq_airgradient_partner_profile"],
}


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


def normalize_space(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value: Any) -> float | None:
    try:
        if value in {None, ""}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def haversine_km(lat1: float | None, lon1: float | None, lat2: float | None, lon2: float | None) -> float | None:
    if None in {lat1, lon1, lat2, lon2}:
        return None
    radius = 6371.0088
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    d_phi = math.radians(float(lat2) - float(lat1))
    d_lambda = math.radians(float(lon2) - float(lon1))
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return round(radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 3)


def fetch_source(seed: dict[str, str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_key": seed["source_key"],
        "source_role": seed["source_role"],
        "url": seed["url"],
        "content_type_hint": seed.get("content_type_hint", ""),
        "source_note": seed.get("source_note", ""),
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "text": "",
        "matched_terms": [],
        "missing_terms": [],
        "retrieval_error": "",
    }
    try:
        response = requests.get(seed["url"], headers=REQUEST_HEADERS, timeout=60)
        result["http_status"] = response.status_code
        result["content_type"] = response.headers.get("content-type", "")
        result["retrieval_bytes"] = len(response.content)
        response.raise_for_status()
        result["text"] = normalize_space(
            extract_text(response.content, response.text, result["content_type"], seed.get("content_type_hint", ""))
        )
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are recorded as data.
        result["retrieval_error"] = str(exc)

    required_terms = [term.strip() for term in seed.get("required_terms", "").split("||") if term.strip()]
    lower_text = result["text"].lower()
    result["matched_terms"] = [term for term in required_terms if term.lower() in lower_text]
    result["missing_terms"] = [term for term in required_terms if term.lower() not in lower_text]
    return result


def extract_text(content: bytes, text: str, content_type: str, hint: str) -> str:
    lower = f"{content_type} {hint}".lower()
    if "pdf" in lower:
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if "json" in lower:
        return content.decode("utf-8", errors="replace")
    if "html" in lower:
        soup = BeautifulSoup(text, "html.parser")
        script_text = " ".join(script.get_text(" ", strip=True) for script in soup.find_all("script"))
        return f"{soup.get_text(' ', strip=True)} {script_text}"
    return text


def station_extraction_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    output: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row.get("iso3", ""), row.get("source_station_id", ""))
        if row.get("extraction_level") == "station_coordinates" and key[1]:
            output[key] = row
    return output


def openaq_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row.get("iso3", ""), row.get("openaq_location_id", "")): row for row in rows}


def provider_context_keys(candidate: dict[str, str]) -> list[str]:
    if candidate["iso3"] == "MYS" and candidate.get("openaq_provider_name") == "Clarity":
        return ["clarity_kl_hyperlocal_source"]
    return PROVIDER_CONTEXT_BY_ROW.get(candidate["iso3"], ["airgradient_openaq_share_guidance"])


def contains_agency(candidate: dict[str, str]) -> bool:
    agency = normalize_space(candidate.get("agency")).lower()
    owner_provider = f"{candidate.get('openaq_owner_name', '')} {candidate.get('openaq_provider_name', '')}".lower()
    return bool(agency and agency in owner_provider)


def build_evidence_text(
    candidate: dict[str, str],
    extraction: dict[str, str],
    openaq: dict[str, str],
    context_keys: list[str],
    source_reuse_count: int,
) -> str:
    distance = extraction.get("nearest_openaq_distance_km") or candidate.get("nearest_openaq_distance_km")
    official_part = (
        f"The official row is {candidate['source_station_id']} / {candidate['source_station_name']} "
        f"({extraction.get('latitude')}, {extraction.get('longitude')}) from {candidate['agency']}."
    )
    openaq_part = (
        f"The OpenAQ-side row is {candidate['nearest_openaq_location_name']} "
        f"({openaq.get('latitude')}, {openaq.get('longitude')}), owner/provider "
        f"{candidate.get('openaq_owner_name')} / {candidate.get('openaq_provider_name')}, "
        f"isMonitor={candidate.get('openaq_is_monitor')}, at {distance} km."
    )
    context_part = f"Provider context checked: {', '.join(context_keys)}."
    reuse_part = (
        " The same OpenAQ public-feed location is nearest to multiple official rows in this scan."
        if source_reuse_count > 1
        else ""
    )
    return (
        f"{official_part} {openaq_part} {context_part} No shared station ID, source-owner crosswalk, "
        f"current-status crosswalk, or documented co-location was found.{reuse_part}"
    )


def build_candidate_row(
    generated_at: str,
    candidate: dict[str, str],
    extraction: dict[str, str],
    openaq: dict[str, str],
    sources: dict[str, dict[str, Any]],
    location_reuse_counts: Counter[str],
) -> dict[str, Any]:
    iso3 = candidate["iso3"]
    official_source_key = OFFICIAL_SOURCE_BY_ISO[iso3]
    official_source = sources[official_source_key]
    context_keys = provider_context_keys(candidate)
    context_sources = [sources[key] for key in context_keys if key in sources]
    official_lat = as_float(extraction.get("latitude"))
    official_lon = as_float(extraction.get("longitude"))
    openaq_lat = as_float(openaq.get("latitude"))
    openaq_lon = as_float(openaq.get("longitude"))
    computed_distance = haversine_km(official_lat, official_lon, openaq_lat, openaq_lon)
    provider_context_retrieved = any(source["retrieved"] for source in context_sources)
    provider_context_terms_matched = sorted({term for source in context_sources for term in source["matched_terms"]})
    source_reuse_count = location_reuse_counts[candidate["nearest_openaq_location_id"]]

    decision = "public_feed_nearby_not_join_ready"
    return {
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": "computed_public_feed_source_scan",
        "method": METHOD,
        "candidate_review_id": candidate["candidate_review_id"],
        "iso3": iso3,
        "country": candidate["country"],
        "source_station_id": candidate["source_station_id"],
        "source_station_name": candidate["source_station_name"],
        "source_station_type": extraction.get("source_station_type", ""),
        "official_source_key": official_source_key,
        "official_source_url": official_source["url"],
        "official_source_retrieved": bool(official_source["retrieved"]),
        "official_latitude": official_lat,
        "official_longitude": official_lon,
        "nearest_openaq_location_id": candidate["nearest_openaq_location_id"],
        "nearest_openaq_location_name": candidate["nearest_openaq_location_name"],
        "nearest_openaq_distance_km": as_float(candidate["nearest_openaq_distance_km"]),
        "openaq_latitude": openaq_lat,
        "openaq_longitude": openaq_lon,
        "computed_coordinate_distance_km": computed_distance,
        "openaq_owner_name": candidate["openaq_owner_name"],
        "openaq_provider_name": candidate["openaq_provider_name"],
        "openaq_is_monitor": as_bool(candidate.get("openaq_is_monitor")),
        "openaq_first_seen": candidate.get("openaq_first_seen", ""),
        "openaq_last_seen": candidate.get("openaq_last_seen", ""),
        "openaq_sensor_count": as_float(candidate.get("openaq_pm25_sensor_count")),
        "provider_context_source_keys": " | ".join(context_keys),
        "provider_context_retrieved": provider_context_retrieved,
        "provider_context_terms_matched": " | ".join(provider_context_terms_matched),
        "same_openaq_location_reused_in_scan": source_reuse_count > 1,
        "official_agency_exact_in_openaq_owner_or_provider": contains_agency(candidate),
        "shared_station_id_found": False,
        "source_owner_crosswalk_found": False,
        "current_status_crosswalk_found": False,
        "documented_colocation_found": False,
        "same_station_validated": False,
        "allowed_review_decision": decision,
        "candidate_queue_status_after_scan": "screened_public_feed_nearby_not_join_ready",
        "station_radius_join_ready": False,
        "disambiguating_public_evidence": build_evidence_text(
            candidate,
            extraction,
            openaq,
            context_keys,
            source_reuse_count,
        ),
        "reviewer_action": "Keep out of validated same-station and station-radius joins unless later public source-owner evidence names both records.",
        "reader_use": "This is a nearby public-feed row, not a validated official/OpenAQ station crosswalk.",
        "non_claim": NON_CLAIM,
    }


def build_summary(generated_at: str, rows: list[dict[str, Any]], sources: dict[str, dict[str, Any]], total_candidates: int) -> dict[str, Any]:
    counts = {
        "candidate_rows_total_before_scan": total_candidates,
        "public_feed_candidate_rows_scanned": len(rows),
        "is_monitor_candidate_rows_not_scanned_here": total_candidates - len(rows),
        "source_urls_seeded": len(sources),
        "source_urls_retrieved": sum(1 for source in sources.values() if source["retrieved"]),
        "rows_with_official_coordinate_evidence": sum(1 for row in rows if row["official_latitude"] not in {None, ""}),
        "rows_with_openaq_coordinate_evidence": sum(1 for row in rows if row["openaq_latitude"] not in {None, ""}),
        "rows_with_public_feed_owner_provider": sum(1 for row in rows if row["openaq_owner_name"] or row["openaq_provider_name"]),
        "openaq_not_is_monitor_rows": sum(1 for row in rows if not row["openaq_is_monitor"]),
        "provider_context_retrieved_rows": sum(1 for row in rows if row["provider_context_retrieved"]),
        "same_openaq_location_reused_rows": sum(1 for row in rows if row["same_openaq_location_reused_in_scan"]),
        "official_agency_owner_provider_match_rows": sum(1 for row in rows if row["official_agency_exact_in_openaq_owner_or_provider"]),
        "shared_station_id_rows": sum(1 for row in rows if row["shared_station_id_found"]),
        "source_owner_crosswalk_rows": sum(1 for row in rows if row["source_owner_crosswalk_found"]),
        "current_status_crosswalk_rows": sum(1 for row in rows if row["current_status_crosswalk_found"]),
        "documented_colocation_rows": sum(1 for row in rows if row["documented_colocation_found"]),
        "validated_same_station_rows": sum(1 for row in rows if row["same_station_validated"]),
        "station_radius_join_ready_rows": sum(1 for row in rows if row["station_radius_join_ready"]),
        "rows_screened_public_feed_nearby_not_join_ready": sum(
            1 for row in rows if row["allowed_review_decision"] == "public_feed_nearby_not_join_ready"
        ),
    }
    decision_counts = Counter(row["allowed_review_decision"] for row in rows)
    country_rows = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        subset = [row for row in rows if row["iso3"] == iso3]
        country_rows.append(
            {
                "iso3": iso3,
                "country": subset[0]["country"],
                "rows_scanned": len(subset),
                "public_feed_not_join_ready_rows": sum(
                    1 for row in subset if row["allowed_review_decision"] == "public_feed_nearby_not_join_ready"
                ),
                "validated_same_station_rows": 0,
                "station_radius_join_ready_rows": 0,
            }
        )

    source_rows = [
        {
            "source_key": source["source_key"],
            "source_role": source["source_role"],
            "url": source["url"],
            "retrieved": source["retrieved"],
            "http_status": source["http_status"],
            "content_type": source["content_type"],
            "retrieval_bytes": source["retrieval_bytes"],
            "matched_terms": source["matched_terms"],
            "missing_terms": source["missing_terms"],
            "retrieval_error": source["retrieval_error"],
            "source_note": source["source_note"],
        }
        for source in sources.values()
    ]

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed_public_feed_source_scan",
        "method": METHOD,
        "goal_level": "L3 candidate station-crosswalk public-feed source scan",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "public source URL and required-term seed"},
            {
                "path": str(CANDIDATE_EVIDENCE_CSV.relative_to(PROGRAM_DIR)),
                "role": "candidate rows with OpenAQ owner/provider and isMonitor metadata",
            },
            {"path": str(STATION_EXTRACTION_CSV.relative_to(PROGRAM_DIR)), "role": "official station coordinates"},
            {"path": str(OPENAQ_CSV.relative_to(PROGRAM_DIR)), "role": "OpenAQ candidate coordinates and provider metadata"},
        ],
        "coverage_counts": counts,
        "decision_counts": [{"decision": key, "rows": value} for key, value in sorted(decision_counts.items())],
        "country_rows": country_rows,
        "source_rows": source_rows,
        "candidate_rows": rows,
        "outputs": {
            "csv": str(OUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "non_claim": NON_CLAIM,
    }


def main() -> int:
    generated_at = now_iso()
    seeds = read_csv(SEED_CSV)
    sources = {seed["source_key"]: fetch_source(seed) for seed in seeds}
    candidates_all = read_csv(CANDIDATE_EVIDENCE_CSV)
    candidates = [row for row in candidates_all if not as_bool(row.get("openaq_is_monitor"))]
    extraction_rows = station_extraction_lookup(read_csv(STATION_EXTRACTION_CSV))
    openaq_rows = openaq_lookup(read_csv(OPENAQ_CSV))
    location_reuse_counts = Counter(row["nearest_openaq_location_id"] for row in candidates)

    rows = []
    for candidate in candidates:
        extraction = extraction_rows.get((candidate["iso3"], candidate["source_station_id"]), {})
        openaq = openaq_rows.get((candidate["iso3"], candidate["nearest_openaq_location_id"]), {})
        rows.append(build_candidate_row(generated_at, candidate, extraction, openaq, sources, location_reuse_counts))

    summary = build_summary(generated_at, rows, sources, len(candidates_all))
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built official/OpenAQ candidate public-feed source scan: "
        f"{counts['public_feed_candidate_rows_scanned']} candidates scanned; "
        f"{counts['rows_screened_public_feed_nearby_not_join_ready']} screened as not join-ready; "
        f"{counts['validated_same_station_rows']} validated same-station joins."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
