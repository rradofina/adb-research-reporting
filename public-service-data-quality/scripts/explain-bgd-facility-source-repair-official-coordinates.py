"""Fetch official DGHS coordinate evidence for PSDQ BGD source-repair rows.

This live public-source pass reads the four source-repair evidence rows,
retrieves each public DGHS profile page, parses the embedded official map
coordinate, and compares it with the pinned OSM candidate coordinate. It does
not close, reclassify, or validate any row.
"""

from __future__ import annotations

import csv
import html
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"
CACHE_DIR = ROOT / ".cache"

IN_SOURCE_REPAIR_EVIDENCE_CSV = (
    OUT_DIR / "psdq-bgd-facility-validation-source-repair-public-evidence.csv"
)
IN_INSPECTION_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-map-inspection.csv"
IN_OSM_OVERPASS_CACHE = CACHE_DIR / "bgd_osm_health_features_overpass.json"

OUT_OFFICIAL_COORDINATE_EVIDENCE_CSV = (
    OUT_DIR / "psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv"
)
OUT_OFFICIAL_COORDINATE_EVIDENCE_SUMMARY_JSON = (
    OUT_DIR / "psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json"
)

METHOD = "ai_public_source_repair_official_coordinate_evidence_v1"
STATUS = "ai_public_source_repair_official_coordinate_evidence_not_human_validation"
USER_AGENT = "ADB-AI-Research-PSDQ-source-repair-official-coordinate-evidence/1.0"
NON_CLAIM = (
    "This is an AI-first public-source coordinate evidence pass for PSDQ "
    "source-repair rows. It parses official DGHS public profile map "
    "coordinates and compares them with pinned public OSM candidate "
    "coordinates. It is not human validation, not ground truth, not a row "
    "closure, not a same-facility reclassification, not a facility-quality "
    "assessment, and not a service-access estimate."
)

TAG_KEYS_FOR_REVIEW = [
    "amenity",
    "healthcare",
    "name",
    "name:en",
    "name:bn",
    "official_name",
    "alt_name",
    "operator",
    "addr:city",
    "addr:street",
    "phone",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def clean_html(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = text.replace("\u0165", ">")
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_label(value: str) -> str:
    label = clean_html(value).lower()
    label = re.sub(r"[^a-z0-9]+", "_", label)
    return label.strip("_")


def fetch_url(url: str, timeout: int = 30) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "final_url": response.url,
                "content_type": response.headers.get("content-type", ""),
                "body": body,
                "error": "",
            }
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        return {
            "ok": False,
            "status": exc.code,
            "final_url": url,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "body": body,
            "error": f"http_error_{exc.code}",
        }
    except URLError as exc:
        return {
            "ok": False,
            "status": "",
            "final_url": url,
            "content_type": "",
            "body": "",
            "error": f"url_error:{exc.reason}",
        }
    except TimeoutError:
        return {
            "ok": False,
            "status": "",
            "final_url": url,
            "content_type": "",
            "body": "",
            "error": "timeout",
        }


def parse_profile_page(body: str) -> dict[str, Any]:
    map_match = re.search(
        r"maps\.google\.com/maps\?q=([-0-9.]+),([-0-9.]+)",
        body,
        flags=re.IGNORECASE,
    )
    header_values = [
        clean_html(value)
        for value in re.findall(r"<h3[^>]*>(.*?)</h3>", body, flags=re.IGNORECASE | re.DOTALL)
    ]
    facility_header = next(
        (value for value in header_values if re.search(r"#\d+\.", value)),
        header_values[0] if header_values else "",
    )
    td_values = re.findall(r"<td[^>]*>(.*?)</td>", body, flags=re.IGNORECASE | re.DOTALL)

    fields: dict[str, str] = {}
    cleaned = [clean_html(value) for value in td_values]
    for index in range(0, len(cleaned) - 1, 2):
        label = normalize_label(cleaned[index])
        value = cleaned[index + 1]
        if label and value and label not in fields:
            fields[label] = value

    return {
        "dghs_profile_map_lat": map_match.group(1) if map_match else "",
        "dghs_profile_map_lon": map_match.group(2) if map_match else "",
        "dghs_profile_map_iframe_url": (
            f"https://maps.google.com/maps?q={map_match.group(1)},{map_match.group(2)}&hl=es;z=14&output=embed"
            if map_match
            else ""
        ),
        "dghs_profile_header": facility_header,
        "dghs_profile_organization_name": fields.get("organization_name", ""),
        "dghs_profile_division_name": fields.get("division_name", ""),
        "dghs_profile_district_name": fields.get("district_name", ""),
        "dghs_profile_upazilla_name": fields.get("upazilla_name", ""),
        "dghs_profile_city_corporation_name": fields.get("city_corporation_name", ""),
        "dghs_profile_facility_email": fields.get("facility_email_address", ""),
        "dghs_profile_fields_found": len(fields),
    }


def coordinate_source_explanation_found(body: str) -> bool:
    profile_text = clean_html(body).lower()
    patterns = [
        "coordinate source",
        "coordinate correction",
        "coordinate corrected",
        "gps source",
        "gps coordinate",
        "geocode source",
        "map coordinate source",
        "latitude source",
        "longitude source",
        "location source",
    ]
    return any(pattern in profile_text for pattern in patterns)


def feature_key(feature_url: str) -> tuple[str, int] | None:
    match = re.search(r"openstreetmap\.org/(node|way|relation)/(\d+)", str(feature_url or ""))
    if not match:
        return None
    osm_type, osm_id = match.groups()
    return osm_type, int(osm_id)


def compact_tags(tags: dict[str, Any]) -> str:
    pairs = []
    for key in TAG_KEYS_FOR_REVIEW:
        value = tags.get(key)
        if value not in (None, ""):
            pairs.append(f"{key}={value}")
    return "; ".join(pairs)


def read_osm_cache(path: Path) -> tuple[dict[tuple[str, int], dict[str, Any]], dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    index: dict[tuple[str, int], dict[str, Any]] = {}
    for element in payload.get("elements", []):
        center = element.get("center") or {}
        key = (str(element.get("type") or ""), int(element.get("id")))
        index[key] = {
            "osm_type": str(element.get("type") or ""),
            "osm_id": str(element.get("id") or ""),
            "osm_lat": element.get("lat") or center.get("lat") or "",
            "osm_lon": element.get("lon") or center.get("lon") or "",
            "osm_name": (element.get("tags") or {}).get("name", ""),
            "osm_tags_compact": compact_tags(element.get("tags") or {}),
        }
    return index, {
        "version": payload.get("version", ""),
        "generator": payload.get("generator", ""),
        "osm3s": payload.get("osm3s", {}),
    }


def haversine_m(lat1: Any, lon1: Any, lat2: Any, lon2: Any) -> float:
    phi1 = math.radians(to_float(lat1))
    phi2 = math.radians(to_float(lat2))
    delta_phi = math.radians(to_float(lat2) - to_float(lat1))
    delta_lambda = math.radians(to_float(lon2) - to_float(lon1))
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return 6_371_000 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def evidence_class(row: dict[str, Any], shared_profile_coordinate_rows: int) -> str:
    distance = to_float(row.get("dghs_profile_to_osm_candidate_distance_m"))
    if shared_profile_coordinate_rows > 1:
        return "official_profile_coordinate_shared_by_multiple_dghs_rows"
    if distance >= 50_000:
        return "official_profile_coordinate_extreme_distance_from_named_osm_candidate"
    if distance >= 10_000:
        return "official_profile_coordinate_long_distance_from_named_osm_candidate"
    return "official_profile_coordinate_near_named_osm_candidate"


def reviewer_action(row: dict[str, Any], shared_profile_coordinate_rows: int) -> str:
    if shared_profile_coordinate_rows > 1:
        return (
            "Treat the shared DGHS profile coordinate as a coordinate-collision "
            "question; do not close either row without an official source "
            "explaining whether the records intentionally share a site."
        )
    if to_float(row.get("dghs_profile_to_osm_candidate_distance_m")) >= 10_000:
        return (
            "Treat the DGHS profile coordinate as the official public coordinate "
            "currently exposed, but keep the row open until an official source "
            "explains the coordinate or source correction."
        )
    return "Keep the row open; the official coordinate is exposed but does not by itself validate the mapped candidate."


def main() -> None:
    for path in [IN_SOURCE_REPAIR_EVIDENCE_CSV, IN_INSPECTION_CSV, IN_OSM_OVERPASS_CACHE]:
        if not path.exists():
            raise FileNotFoundError(path)

    source_rows = read_csv(IN_SOURCE_REPAIR_EVIDENCE_CSV)
    inspection_rows = read_csv(IN_INSPECTION_CSV)
    inspection_by_id = {row["inspection_id"]: row for row in inspection_rows}
    osm_index, osm_metadata = read_osm_cache(IN_OSM_OVERPASS_CACHE)
    retrieved_at = now_utc()

    output_rows: list[dict[str, Any]] = []
    profile_coordinate_keys: list[str] = []

    for index, row in enumerate(source_rows, start=1):
        inspection = inspection_by_id.get(str(row.get("inspection_id") or ""))
        if inspection is None:
            raise KeyError(f"Missing inspection row for {row.get('inspection_id')}")

        dghs_fetch = fetch_url(str(row.get("dghs_public_profile_url") or ""))
        profile = parse_profile_page(dghs_fetch.get("body", ""))
        source_explanation_found = coordinate_source_explanation_found(dghs_fetch.get("body", ""))

        key = feature_key(str(row.get("candidate_feature_url") or ""))
        osm_feature = osm_index.get(key or ("", -1), {})
        if not osm_feature:
            raise KeyError(f"Missing OSM cache feature for {row.get('candidate_feature_url')}")

        profile_lat = profile["dghs_profile_map_lat"]
        profile_lon = profile["dghs_profile_map_lon"]
        profile_to_registry_m = round(
            haversine_m(profile_lat, profile_lon, inspection.get("latitude"), inspection.get("longitude")),
            1,
        )
        profile_to_osm_m = round(
            haversine_m(profile_lat, profile_lon, osm_feature.get("osm_lat"), osm_feature.get("osm_lon")),
            1,
        )
        coordinate_key = f"{round(to_float(profile_lat), 6)}|{round(to_float(profile_lon), 6)}"
        profile_coordinate_keys.append(coordinate_key)

        output_rows.append(
            {
                "official_coordinate_evidence_id": f"PSDQ-BGD-SROC-{index:03d}",
                "evidence_rank": index,
                "evidence_method": METHOD,
                "retrieved_at": retrieved_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "source_repair_evidence_id": row.get("evidence_id", ""),
                "decision_id": row.get("decision_id", ""),
                "inspection_id": row.get("inspection_id", ""),
                "facility_name": row.get("facility_name", ""),
                "facility_type_name": row.get("facility_type_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "dghs_public_profile_url": row.get("dghs_public_profile_url", ""),
                "dghs_profile_http_status": dghs_fetch.get("status", ""),
                "dghs_profile_retrieved": bool(dghs_fetch.get("ok")),
                "dghs_profile_final_url": dghs_fetch.get("final_url", ""),
                "dghs_profile_error": dghs_fetch.get("error", ""),
                **profile,
                "profile_coordinate_key": coordinate_key,
                "inspection_registry_lat": inspection.get("latitude", ""),
                "inspection_registry_lon": inspection.get("longitude", ""),
                "dghs_profile_matches_inspection_registry_coordinate": profile_to_registry_m <= 5,
                "dghs_profile_to_inspection_registry_distance_m": profile_to_registry_m,
                "candidate_feature_url": row.get("candidate_feature_url", ""),
                "candidate_osm_type": osm_feature.get("osm_type", ""),
                "candidate_osm_id": osm_feature.get("osm_id", ""),
                "candidate_osm_name": osm_feature.get("osm_name", ""),
                "candidate_osm_lat": osm_feature.get("osm_lat", ""),
                "candidate_osm_lon": osm_feature.get("osm_lon", ""),
                "candidate_osm_tags_compact": osm_feature.get("osm_tags_compact", ""),
                "dghs_profile_to_osm_candidate_distance_m": profile_to_osm_m,
                "candidate_distance_m_from_inspection": row.get("candidate_distance_m_from_inspection", ""),
                "candidate_name_score_from_live_tags": row.get("candidate_name_score_from_live_tags", ""),
                "explicit_coordinate_source_explanation_found": source_explanation_found,
                "source_explanation_status": (
                    "official_coordinate_exposed_without_coordinate_source_explanation"
                    if profile_lat and profile_lon
                    else "official_coordinate_not_exposed_in_profile"
                ),
                "rows_closed_as_resolved": 0,
                "rows_reclassified_as_same_facility": 0,
                "source_basis": (
                    "Live public DGHS profile HTML map iframe plus pinned all-Bangladesh "
                    "OSM/Overpass health-feature cache."
                ),
                "non_claim": NON_CLAIM,
            }
        )

    shared_counter = Counter(profile_coordinate_keys)
    for row in output_rows:
        shared_rows = int(shared_counter[row["profile_coordinate_key"]])
        row["shared_official_profile_coordinate_rows"] = shared_rows
        row["official_coordinate_evidence_class"] = evidence_class(row, shared_rows)
        row["source_repair_reviewer_action"] = reviewer_action(row, shared_rows)

    class_counter = Counter(row["official_coordinate_evidence_class"] for row in output_rows)
    profile_to_osm_distances = [
        to_float(row["dghs_profile_to_osm_candidate_distance_m"]) for row in output_rows
    ]
    summary = {
        "generated_at": retrieved_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 source-repair official-coordinate evidence",
        "unit": "source-repair-first row selected from the PSDQ source-repair evidence attachment",
        "source_inputs": [
            {
                "path": str(IN_SOURCE_REPAIR_EVIDENCE_CSV.relative_to(ROOT)),
                "role": "4-row source-repair public-evidence attachment",
            },
            {
                "path": str(IN_INSPECTION_CSV.relative_to(ROOT)),
                "role": "40-row targeted public-map inspection CSV",
            },
            {
                "path": str(IN_OSM_OVERPASS_CACHE.relative_to(ROOT)),
                "role": "pinned all-Bangladesh OSM/Overpass health-feature cache",
                "osm3s_timestamp_osm_base": osm_metadata.get("osm3s", {}).get("timestamp_osm_base", ""),
                "generator": osm_metadata.get("generator", ""),
            },
        ],
        "selection_rule": "Include only rows in the 4-row source-repair public-evidence attachment.",
        "official_coordinate_scope": {
            "source_repair_rows": len(output_rows),
            "dghs_profiles_retrieved": sum(1 for row in output_rows if row["dghs_profile_retrieved"]),
            "official_profile_coordinates_exposed": sum(
                1 for row in output_rows if row["dghs_profile_map_lat"] and row["dghs_profile_map_lon"]
            ),
            "profile_coordinates_match_inspection_registry_coordinates": sum(
                1 for row in output_rows if row["dghs_profile_matches_inspection_registry_coordinate"]
            ),
            "rows_with_shared_official_profile_coordinate": sum(
                1 for row in output_rows if int(row["shared_official_profile_coordinate_rows"]) > 1
            ),
            "rows_with_official_coordinate_distance_10km_or_more_from_osm_candidate": sum(
                1 for value in profile_to_osm_distances if value >= 10_000
            ),
            "rows_with_official_coordinate_distance_50km_or_more_from_osm_candidate": sum(
                1 for value in profile_to_osm_distances if value >= 50_000
            ),
            "max_official_coordinate_to_osm_candidate_distance_m": round(
                max(profile_to_osm_distances) if profile_to_osm_distances else 0.0,
                1,
            ),
            "explicit_coordinate_source_explanations_found": sum(
                1 for row in output_rows if row["explicit_coordinate_source_explanation_found"]
            ),
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
        },
        "official_coordinate_evidence_class_counts": [
            {"name": name, "rows": int(class_counter[name])} for name in sorted(class_counter)
        ],
        "evidence_rows": output_rows,
        "evidence_notes": [
            "The public DGHS profile pages expose map coordinates through an embedded Google Maps iframe.",
            "All parsed DGHS profile coordinates match the coordinates already carried in the inspection CSV.",
            "The profiles expose coordinates, but this pass found no explicit public coordinate-source explanation field.",
            "Rows remain open pending an official explanation, correction record, or human validation.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "official_coordinate_evidence_id",
        "evidence_rank",
        "evidence_method",
        "retrieved_at",
        "attestation_chain",
        "status",
        "source_repair_evidence_id",
        "decision_id",
        "inspection_id",
        "facility_name",
        "facility_type_name",
        "district_name",
        "upazila_name",
        "dghs_public_profile_url",
        "dghs_profile_http_status",
        "dghs_profile_retrieved",
        "dghs_profile_final_url",
        "dghs_profile_error",
        "dghs_profile_map_lat",
        "dghs_profile_map_lon",
        "dghs_profile_map_iframe_url",
        "dghs_profile_header",
        "dghs_profile_organization_name",
        "dghs_profile_division_name",
        "dghs_profile_district_name",
        "dghs_profile_upazilla_name",
        "dghs_profile_city_corporation_name",
        "dghs_profile_facility_email",
        "dghs_profile_fields_found",
        "profile_coordinate_key",
        "inspection_registry_lat",
        "inspection_registry_lon",
        "dghs_profile_matches_inspection_registry_coordinate",
        "dghs_profile_to_inspection_registry_distance_m",
        "candidate_feature_url",
        "candidate_osm_type",
        "candidate_osm_id",
        "candidate_osm_name",
        "candidate_osm_lat",
        "candidate_osm_lon",
        "candidate_osm_tags_compact",
        "dghs_profile_to_osm_candidate_distance_m",
        "candidate_distance_m_from_inspection",
        "candidate_name_score_from_live_tags",
        "shared_official_profile_coordinate_rows",
        "official_coordinate_evidence_class",
        "source_repair_reviewer_action",
        "explicit_coordinate_source_explanation_found",
        "source_explanation_status",
        "rows_closed_as_resolved",
        "rows_reclassified_as_same_facility",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_OFFICIAL_COORDINATE_EVIDENCE_CSV, output_rows, fields)
    write_json(OUT_OFFICIAL_COORDINATE_EVIDENCE_SUMMARY_JSON, summary)

    scope = summary["official_coordinate_scope"]
    print(
        "Built BGD source-repair official-coordinate evidence: "
        f"{scope['source_repair_rows']} rows; "
        f"{scope['official_profile_coordinates_exposed']} official profile coordinates exposed; "
        f"{scope['explicit_coordinate_source_explanations_found']} explicit coordinate-source explanations; "
        f"{scope['rows_closed_as_resolved']} closed."
    )
    print(f"Wrote {OUT_OFFICIAL_COORDINATE_EVIDENCE_CSV}")
    print(f"Wrote {OUT_OFFICIAL_COORDINATE_EVIDENCE_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
