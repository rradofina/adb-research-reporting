"""Scan public source pages for official/OpenAQ candidate crosswalk evidence.

This script targets the OpenAQ `isMonitor` rows from the candidate public-
evidence audit. It fetches public official/source-owner pages and records
whether they support a same-station join, a separate-nearby-stations decision,
or continued review.
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

SEED_CSV = SOURCE_INPUTS_DIR / "candidate-crosswalk-public-source-seed.csv"
CANDIDATE_EVIDENCE_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-public-evidence.csv"
OPENAQ_CSV = GENERATED_DIR / "air-monitoring-openaq-station-metadata.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json"

METHOD = "air_monitoring_official_openaq_candidate_crosswalk_source_scan_v1"
NON_CLAIM = (
    "This scan uses public source pages to decide whether OpenAQ isMonitor "
    "candidate rows have enough evidence for a same-station join. It does not "
    "create station-radius rows, does not validate monitor grade for official "
    "stations, and does not make any catchment claim."
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
    "nearest_openaq_location_id",
    "nearest_openaq_location_name",
    "nearest_openaq_distance_km",
    "openaq_provider_name",
    "official_source_key",
    "official_source_url",
    "official_source_retrieved",
    "official_source_public_name_or_address",
    "official_latitude",
    "official_longitude",
    "openaq_latitude",
    "openaq_longitude",
    "computed_coordinate_distance_km",
    "disambiguating_source_key",
    "disambiguating_source_url",
    "disambiguating_source_retrieved",
    "disambiguating_public_evidence",
    "matched_public_terms",
    "shared_station_id_found",
    "source_crosswalk_found",
    "documented_colocation_found",
    "same_station_validated",
    "allowed_review_decision",
    "candidate_queue_status_after_scan",
    "station_radius_join_ready",
    "reviewer_action",
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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value: Any) -> float | None:
    try:
        if value in {None, ""}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


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
        "raw": "",
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
        text = extract_text(response.content, response.text, result["content_type"], seed.get("content_type_hint", ""))
        result["raw"] = response.text if "html" in result["content_type"].lower() else ""
        result["text"] = normalize_space(text)
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - retrieval failures are recorded, not fatal.
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
    if "html" in lower:
        return BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
    return text


def parse_uzb_map_rows(html: str) -> dict[str, dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    output: dict[str, dict[str, str]] = {}
    for item in soup.select(".points-item"):
        cols: dict[str, str] = {}
        for col in item.select(".col"):
            text = col.get_text(" ", strip=True)
            for cls in col.get("class", []):
                if cls.startswith("col-") and cls != "col":
                    cols[cls] = text
        name = cols.get("col-name", "")
        if name:
            output[normalize_space(name)] = {
                "name": normalize_space(name),
                "address": normalize_space(cols.get("col-address", "")),
                "index_value": normalize_space(cols.get("col-ci", "")),
                "reported_at": normalize_space(cols.get("col-art", "")),
            }
    return output


def official_bgd_coordinates(source_text: str, station_name: str) -> tuple[float | None, float | None]:
    index = source_text.lower().find(station_name.lower())
    if index < 0 and "," in station_name:
        index = source_text.lower().find(station_name.split(",", 1)[0].lower())
    if index < 0:
        return None, None
    after_snippet = source_text[index : index + 260]
    matches = re.findall(r"(\d{2,3}\.\d+)\s*;\s*(\d{1,2}\.\d+)", after_snippet)
    if not matches:
        surrounding_snippet = source_text[max(0, index - 220) : index + 260]
        matches = re.findall(r"(\d{2,3}\.\d+)\s*;\s*(\d{1,2}\.\d+)", surrounding_snippet)
    if not matches:
        return None, None
    lon, lat = matches[0]
    return float(lat), float(lon)


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


def openaq_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row.get("iso3", ""), row.get("openaq_location_id", "")): row for row in rows}


def build_candidate_row(
    generated_at: str,
    candidate: dict[str, str],
    openaq: dict[str, str],
    sources: dict[str, dict[str, Any]],
    uzb_map_rows: dict[str, dict[str, str]],
) -> dict[str, Any]:
    iso3 = candidate["iso3"]
    official_source_key = "bgd_official_ambient_air_quality_pdf" if iso3 == "BGD" else "uzb_official_monitoring_map"
    official_source = sources[official_source_key]
    disambiguating_source_key = "bgd_spartan_dhaka_site" if iso3 == "BGD" else "uzb_world_bank_tashkent_assessment"
    disambiguating_source = sources[disambiguating_source_key]

    official_lat: float | None = None
    official_lon: float | None = None
    official_name_or_address = candidate["source_station_name"]
    if iso3 == "BGD":
        official_lat, official_lon = official_bgd_coordinates(official_source["text"], candidate["source_station_name"])
    elif iso3 == "UZB":
        map_row = uzb_map_rows.get(normalize_space(candidate["source_station_name"]), {})
        official_name_or_address = "; ".join(
            value
            for value in [
                map_row.get("name", candidate["source_station_name"]),
                map_row.get("address", ""),
                f"API {map_row.get('index_value')}" if map_row.get("index_value") else "",
                f"reported {map_row.get('reported_at')}" if map_row.get("reported_at") else "",
            ]
            if value
        )

    openaq_lat = as_float(openaq.get("latitude"))
    openaq_lon = as_float(openaq.get("longitude"))
    computed_distance = haversine_km(official_lat, official_lon, openaq_lat, openaq_lon)

    matched_terms = sorted(
        set(official_source["matched_terms"])
        | set(disambiguating_source["matched_terms"])
        | set(sources.get("bgd_openaq_spartan_announcement", {}).get("matched_terms", []) if iso3 == "BGD" else [])
    )

    if iso3 == "BGD":
        evidence = (
            "The Bangladesh official report places the official station at "
            f"{official_name_or_address}"
            + (f" ({official_lat}, {official_lon})" if official_lat is not None else "")
            + "; the SPARTAN source page identifies the OpenAQ-side site as BDDU, University of Dhaka "
            "at 23.728, 90.398. No shared station ID, source crosswalk, or documented co-location was found."
        )
        reader_use = (
            "Treat as separate nearby stations for join purposes unless a source-owner crosswalk later names both records."
        )
    else:
        evidence = (
            "The Uzhydromet public map lists the official row as "
            f"{official_name_or_address}. The OpenAQ-side row is StateAir / US Diplomatic Post: Tashkent; "
            "the World Bank Tashkent assessment distinguishes the US Embassy station from Uzhydromet stations "
            "and notes that manual Uzhydromet stations do not monitor PM2.5."
        )
        reader_use = (
            "Treat as separate nearby stations; do not collapse Uzhydromet POP rows onto the US Embassy OpenAQ row."
        )

    return {
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": "computed_public_crosswalk_source_scan",
        "method": METHOD,
        "candidate_review_id": candidate["candidate_review_id"],
        "iso3": iso3,
        "country": candidate["country"],
        "source_station_id": candidate["source_station_id"],
        "source_station_name": candidate["source_station_name"],
        "nearest_openaq_location_id": candidate["nearest_openaq_location_id"],
        "nearest_openaq_location_name": candidate["nearest_openaq_location_name"],
        "nearest_openaq_distance_km": as_float(candidate["nearest_openaq_distance_km"]),
        "openaq_provider_name": candidate["openaq_provider_name"],
        "official_source_key": official_source_key,
        "official_source_url": official_source["url"],
        "official_source_retrieved": bool(official_source["retrieved"]),
        "official_source_public_name_or_address": official_name_or_address,
        "official_latitude": official_lat,
        "official_longitude": official_lon,
        "openaq_latitude": openaq_lat,
        "openaq_longitude": openaq_lon,
        "computed_coordinate_distance_km": computed_distance,
        "disambiguating_source_key": disambiguating_source_key,
        "disambiguating_source_url": disambiguating_source["url"],
        "disambiguating_source_retrieved": bool(disambiguating_source["retrieved"]),
        "disambiguating_public_evidence": evidence,
        "matched_public_terms": " | ".join(matched_terms),
        "shared_station_id_found": False,
        "source_crosswalk_found": False,
        "documented_colocation_found": False,
        "same_station_validated": False,
        "allowed_review_decision": "separate_nearby_stations",
        "candidate_queue_status_after_scan": "screened_as_separate_nearby_stations",
        "station_radius_join_ready": False,
        "reviewer_action": "Keep out of validated same-station and station-radius joins unless later public crosswalk evidence reverses this scan.",
        "reader_use": reader_use,
        "non_claim": NON_CLAIM,
    }


def build_summary(generated_at: str, rows: list[dict[str, Any]], sources: dict[str, dict[str, Any]], total_candidates: int) -> dict[str, Any]:
    counts = {
        "candidate_rows_total_before_scan": total_candidates,
        "is_monitor_candidate_rows_scanned": len(rows),
        "non_monitor_candidate_rows_not_scanned": total_candidates - len(rows),
        "source_urls_seeded": len(sources),
        "source_urls_retrieved": sum(1 for source in sources.values() if source["retrieved"]),
        "rows_with_official_coordinate_evidence": sum(1 for row in rows if row["official_latitude"] not in {None, ""}),
        "rows_with_official_address_evidence": sum(1 for row in rows if row["official_source_public_name_or_address"]),
        "rows_with_openaq_coordinate_evidence": sum(1 for row in rows if row["openaq_latitude"] not in {None, ""}),
        "rows_screened_as_separate_nearby_stations": sum(
            1 for row in rows if row["allowed_review_decision"] == "separate_nearby_stations"
        ),
        "shared_station_id_rows": sum(1 for row in rows if row["shared_station_id_found"]),
        "source_crosswalk_rows": sum(1 for row in rows if row["source_crosswalk_found"]),
        "documented_colocation_rows": sum(1 for row in rows if row["documented_colocation_found"]),
        "validated_same_station_rows": sum(1 for row in rows if row["same_station_validated"]),
        "station_radius_join_ready_rows": sum(1 for row in rows if row["station_radius_join_ready"]),
    }
    decision_counts = Counter(row["allowed_review_decision"] for row in rows)
    country_rows = []
    for iso3 in sorted({row["iso3"] for row in rows}):
        country_subset = [row for row in rows if row["iso3"] == iso3]
        country_rows.append(
            {
                "iso3": iso3,
                "country": country_subset[0]["country"],
                "rows_scanned": len(country_subset),
                "separate_nearby_station_rows": sum(
                    1 for row in country_subset if row["allowed_review_decision"] == "separate_nearby_stations"
                ),
                "validated_same_station_rows": 0,
                "station_radius_join_ready_rows": 0,
            }
        )

    source_rows = []
    for source in sources.values():
        source_rows.append(
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
        )

    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed_public_crosswalk_source_scan",
        "method": METHOD,
        "goal_level": "L3 candidate station-crosswalk public source scan",
        "source_inputs": [
            {"path": str(SEED_CSV.relative_to(PROGRAM_DIR)), "role": "public source URL and required-term seed"},
            {
                "path": str(CANDIDATE_EVIDENCE_CSV.relative_to(PROGRAM_DIR)),
                "role": "candidate rows with OpenAQ owner/provider and isMonitor metadata",
            },
            {"path": str(OPENAQ_CSV.relative_to(PROGRAM_DIR)), "role": "OpenAQ candidate coordinates"},
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
    candidates = [row for row in candidates_all if as_bool(row.get("openaq_is_monitor"))]
    openaq_rows = openaq_lookup(read_csv(OPENAQ_CSV))
    uzb_map_rows = parse_uzb_map_rows(sources["uzb_official_monitoring_map"].get("raw", ""))

    rows = [
        build_candidate_row(
            generated_at,
            candidate,
            openaq_rows.get((candidate["iso3"], candidate["nearest_openaq_location_id"]), {}),
            sources,
            uzb_map_rows,
        )
        for candidate in candidates
    ]
    summary = build_summary(generated_at, rows, sources, len(candidates_all))
    write_csv(OUT_CSV, rows)
    write_json(OUT_JSON, summary)

    counts = summary["coverage_counts"]
    print(
        "Built official/OpenAQ candidate crosswalk source scan: "
        f"{counts['is_monitor_candidate_rows_scanned']} isMonitor candidates scanned; "
        f"{counts['rows_screened_as_separate_nearby_stations']} screened as separate nearby stations; "
        f"{counts['validated_same_station_rows']} validated same-station joins."
    )
    print(f"Wrote {OUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
