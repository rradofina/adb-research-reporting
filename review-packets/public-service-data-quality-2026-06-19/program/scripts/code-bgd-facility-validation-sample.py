"""Code the Bangladesh PSDQ facility-validation sample with public sources.

This script reads the blank validation coding sheet, checks sampled DGHS rows
against public OpenStreetMap health features through Overpass, and emits an
automated coded screen. It is not a human validation pass. The output is a
deterministic public-source screen that identifies which rows need manual
review and why.

Constitution guardrails: public data only (§2.1), auditable numbers (§2.2),
AI-first honest labeling (§18.2), and no composite headline claims (§6.4).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from shapely.geometry import Point, shape


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
GEO_CACHE = CACHE / "geo"
OUT_DIR = ROOT / "generated"

CODING_SHEET = OUT_DIR / "psdq-bgd-facility-validation-coding-sheet.csv"
SAMPLE_JSON = OUT_DIR / "psdq-bgd-facility-validation-sample.json"
ADM3_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM3.geojson"
NATIONAL_OSM_CACHE = CACHE / "bgd_osm_health_features_overpass.json"

OUT_CODED_CSV = OUT_DIR / "psdq-bgd-facility-validation-coded-screen.csv"
OUT_CANDIDATES_CSV = OUT_DIR / "psdq-bgd-facility-validation-osm-candidates.csv"
OUT_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-coded-summary.json"

ALIASES = {
    "barisal": "barishal",
    "bogra": "bogura",
    "chittagong": "chattogram",
    "chittogram": "chattogram",
    "comilla": "cumilla",
    "cox s bazar": "coxs bazar",
    "cox bazar": "coxs bazar",
    "jessore": "jashore",
    "netrokona": "netrakona",
}

VALIDATION_CODES = [
    "confirmed_same_facility",
    "probable_duplicate_or_alias",
    "classification_mismatch",
    "registry_coordinate_issue",
    "missing_public_map_point",
    "osm_only_candidate",
    "unresolved_public_sources",
]

NAME_STOPWORDS = {
    "and",
    "bd",
    "bed",
    "center",
    "centre",
    "clinic",
    "college",
    "community",
    "district",
    "general",
    "health",
    "hospital",
    "medical",
    "sadar",
    "specialized",
    "sub",
    "union",
    "upazila",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--osm-cache",
        default=str(NATIONAL_OSM_CACHE),
        help="All-Bangladesh Overpass cache produced by build-bgd-exposure-ranked-disagreement.py.",
    )
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
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


def normalize_name(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"['`’.,:/_-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in sorted(ALIASES.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    return ALIASES.get(text, text)


def name_tokens(value: Any) -> set[str]:
    return {
        token
        for token in normalize_name(value).split()
        if len(token) > 2 and token not in NAME_STOPWORDS and not token.isdigit()
    }


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def valid_coordinate(row: dict[str, str]) -> tuple[float | None, float | None]:
    if str(row.get("has_valid_coordinate", "")).strip() != "1":
        return None, None
    lat = finite_float(row.get("latitude"))
    lon = finite_float(row.get("longitude"))
    if lat is None or lon is None:
        return None, None
    if not (20.0 <= lat <= 27.5 and 88.0 <= lon <= 92.8):
        return None, None
    return lat, lon


def load_upazila_geometries() -> dict[str, list[Any]]:
    if not ADM3_GEOJSON.exists():
        return {}
    obj = json.loads(ADM3_GEOJSON.read_text(encoding="utf-8"))
    by_name: dict[str, list[Any]] = defaultdict(list)
    for feature in obj.get("features", []):
        key = normalize_name(feature.get("properties", {}).get("shapeName", ""))
        if not key:
            continue
        by_name[key].append(shape(feature["geometry"]))
    return dict(by_name)


def coordinate_boundary_status(
    row: dict[str, str],
    lat: float,
    lon: float,
    upazila_geometries: dict[str, list[Any]],
) -> tuple[str, int | None]:
    key = normalize_name(row.get("upazila_name", ""))
    geoms = upazila_geometries.get(key, [])
    if not geoms:
        return "boundary_not_available", None
    point = Point(lon, lat)
    inside = any(geom.contains(point) or geom.touches(point) for geom in geoms)
    return ("inside_sampled_upazila" if inside else "outside_sampled_upazila"), int(inside)


def load_osm_cache(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    obj = json.loads(path.read_text(encoding="utf-8"))
    meta = obj.get("osm3s", {})
    return obj, {
        "status": "national_cache",
        "cache_file": str(path.relative_to(ROOT)),
        "retrieved_at": meta.get("timestamp_osm_base", ""),
        "overpass_url": "https://overpass-api.de/api/interpreter",
        "error": "",
    }


def element_coordinate(element: dict[str, Any]) -> tuple[float | None, float | None]:
    if "lat" in element and "lon" in element:
        return finite_float(element.get("lat")), finite_float(element.get("lon"))
    center = element.get("center") or {}
    return finite_float(center.get("lat")), finite_float(center.get("lon"))


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6_371_000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def dghs_category(row: dict[str, str]) -> str:
    text = normalize_name(
        " ".join(
            [
                row.get("facility_type_name", ""),
                row.get("facility_level_name", ""),
                row.get("facility_healthcare_level_name", ""),
            ]
        )
    )
    if "hospital" in text or "medical college" in text:
        return "hospital"
    if "clinic" in text or "health" in text or "diagnostic" in text:
        return "clinic"
    return "unknown"


def osm_category(tags: dict[str, Any]) -> str:
    amenity = normalize_name(tags.get("amenity", ""))
    if amenity == "hospital":
        return "hospital"
    if amenity in {"clinic", "doctors"}:
        return "clinic"
    return amenity or "unknown"


def name_similarity(dghs_name: str, osm_name: str) -> tuple[float, float, float]:
    d_norm = normalize_name(dghs_name)
    o_norm = normalize_name(osm_name)
    if not d_norm or not o_norm:
        return 0.0, 0.0, 0.0
    sequence = SequenceMatcher(None, d_norm, o_norm).ratio()
    d_tokens = name_tokens(d_norm)
    o_tokens = name_tokens(o_norm)
    overlap = 0.0
    if d_tokens and o_tokens:
        overlap = len(d_tokens & o_tokens) / len(d_tokens | o_tokens)
    substring = 0.0
    if len(d_norm) >= 6 and len(o_norm) >= 6 and (d_norm in o_norm or o_norm in d_norm):
        substring = min(len(d_norm), len(o_norm)) / max(len(d_norm), len(o_norm))
    return round(sequence, 4), round(overlap, 4), round(substring, 4)


def build_candidate_rows(
    row: dict[str, str],
    response: dict[str, Any] | None,
    lat: float,
    lon: float,
) -> list[dict[str, Any]]:
    if not response:
        return []
    rows: list[dict[str, Any]] = []
    d_category = dghs_category(row)
    for element in response.get("elements", []):
        tags = element.get("tags") or {}
        c_lat, c_lon = element_coordinate(element)
        if c_lat is None or c_lon is None:
            continue
        distance = haversine_m(lat, lon, c_lat, c_lon)
        if distance > 500:
            continue
        sequence, overlap, substring = name_similarity(row.get("facility_name", ""), tags.get("name", ""))
        name_score = max(sequence, overlap, substring)
        proximity_score = max(0.0, 1.0 - min(distance, 500.0) / 500.0)
        category = osm_category(tags)
        category_match = int(d_category != "unknown" and category != "unknown" and d_category == category)
        score = (0.78 * name_score) + (0.17 * proximity_score) + (0.05 * category_match)
        rows.append(
            {
                "sample_group": row.get("sample_group", ""),
                "dghs_id": row.get("dghs_id", ""),
                "facility_name": row.get("facility_name", ""),
                "dghs_category": d_category,
                "osm_id": f"{element.get('type')}/{element.get('id')}",
                "osm_type": element.get("type", ""),
                "osm_name": tags.get("name", ""),
                "osm_amenity": tags.get("amenity", ""),
                "osm_healthcare": tags.get("healthcare", ""),
                "osm_category": category,
                "candidate_latitude": round(c_lat, 7),
                "candidate_longitude": round(c_lon, 7),
                "candidate_distance_m": round(distance, 1),
                "name_sequence_score": sequence,
                "name_token_overlap": overlap,
                "name_substring_score": substring,
                "name_score": round(name_score, 4),
                "category_match": category_match,
                "candidate_score": round(score, 4),
            }
        )
    rows.sort(key=lambda item: (-float(item["candidate_score"]), float(item["candidate_distance_m"])))
    return rows


def classify_row(
    row: dict[str, str],
    candidates: list[dict[str, Any]],
    coordinate_status: str,
    coordinate_inside: int | None,
    overpass_status: dict[str, Any],
) -> tuple[str, str, dict[str, Any] | None, int]:
    if coordinate_status == "missing_or_invalid_coordinate":
        return (
            "registry_coordinate_issue",
            "DGHS row has no valid coordinate in the sampled coding sheet.",
            None,
            1,
        )
    if coordinate_inside == 0:
        return (
            "registry_coordinate_issue",
            "DGHS coordinate is outside the expected geoBoundaries ADM3/upazila polygon.",
            None,
            1,
        )
    if overpass_status["status"] in {"fetch_failed", "missing_cache"}:
        return (
            "unresolved_public_sources",
            f"Overpass public-source check did not return a usable response: {overpass_status['status']}.",
            None,
            1,
        )
    if not candidates:
        return (
            "missing_public_map_point",
            "No OSM amenity=hospital/clinic/doctors feature was found within 500 meters of the DGHS coordinate.",
            None,
            1,
        )

    best = candidates[0]
    name_score = float(best["name_score"])
    distance = float(best["candidate_distance_m"])
    d_category = best["dghs_category"]
    o_category = best["osm_category"]
    category_known = d_category != "unknown" and o_category != "unknown"
    category_mismatch = category_known and d_category != o_category

    if name_score >= 0.72 and not category_mismatch:
        return (
            "confirmed_same_facility",
            "Nearest public OSM feature has a strong name match and compatible facility class.",
            best,
            0,
        )
    if name_score >= 0.45 and category_mismatch:
        return (
            "classification_mismatch",
            "Public OSM feature has a plausible name match but a different health-facility class.",
            best,
            1,
        )
    if name_score >= 0.45:
        return (
            "probable_duplicate_or_alias",
            "Public OSM feature has a partial name match consistent with aliasing or duplicate naming.",
            best,
            1,
        )
    if distance <= 100 and category_known and not category_mismatch:
        return (
            "probable_duplicate_or_alias",
            "A compatible OSM health feature is very near the DGHS coordinate but lacks a strong name match.",
            best,
            1,
        )
    if distance <= 150 and category_mismatch:
        return (
            "classification_mismatch",
            "A nearby OSM health feature has a different health-facility class and weak name match.",
            best,
            1,
        )
    if row.get("sample_group") == "osm_ge_registry" and distance <= 500:
        return (
            "osm_only_candidate",
            "Nearby OSM health feature exists in an OSM-above-registry sample row but does not match the sampled DGHS row by name.",
            best,
            1,
        )
    return (
        "unresolved_public_sources",
        "OSM health candidates exist within 500 meters, but public evidence is insufficient for a deterministic code.",
        best,
        1,
    )


def clean_code_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counter = Counter(row["validation_code"] for row in rows)
    return [{"validation_code": code, "rows": int(counter.get(code, 0))} for code in VALIDATION_CODES]


def group_code_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[row["sample_group"]][row["validation_code"]] += 1
    output = []
    for group in sorted(grouped):
        item: dict[str, Any] = {"sample_group": group, "rows": int(sum(grouped[group].values()))}
        for code in VALIDATION_CODES:
            item[code] = int(grouped[group].get(code, 0))
        output.append(item)
    return output


def main() -> None:
    args = parse_args()
    if not CODING_SHEET.exists():
        raise FileNotFoundError(CODING_SHEET)
    sample_meta = json.loads(SAMPLE_JSON.read_text(encoding="utf-8")) if SAMPLE_JSON.exists() else {}
    osm_cache_path = Path(args.osm_cache).resolve()
    osm_obj, osm_source_status = load_osm_cache(osm_cache_path)
    rows = read_csv(CODING_SHEET)
    upazila_geometries = load_upazila_geometries()

    coded_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    retrieval_status = Counter()
    boundary_status = Counter()

    for index, row in enumerate(rows, start=1):
        lat, lon = valid_coordinate(row)
        if lat is None or lon is None:
            coordinate_status = "missing_or_invalid_coordinate"
            coordinate_inside = None
            boundary_status[coordinate_status] += 1
            overpass_status = {
                "status": "skipped_coordinate_issue",
                "cache_file": "",
                "retrieved_at": "",
                "overpass_url": "",
                "error": "",
            }
            candidates: list[dict[str, Any]] = []
        else:
            coordinate_status, coordinate_inside = coordinate_boundary_status(row, lat, lon, upazila_geometries)
            boundary_status[coordinate_status] += 1
            if coordinate_inside == 0:
                overpass_status = {
                    "status": "skipped_coordinate_issue",
                    "cache_file": "",
                    "retrieved_at": "",
                    "overpass_url": "",
                    "error": "",
                }
                candidates = []
            else:
                overpass_status = dict(osm_source_status)
                candidates = build_candidate_rows(row, osm_obj, lat, lon)
                for candidate in candidates:
                    candidate_rows.append(
                        {
                            **candidate,
                            "dghs_code": row.get("dghs_code", ""),
                            "division_name": row.get("division_name", ""),
                            "district_name": row.get("district_name", ""),
                            "upazila_name": row.get("upazila_name", ""),
                            "overpass_cache_file": overpass_status["cache_file"],
                            "overpass_retrieved_at": overpass_status["retrieved_at"],
                        }
                    )

        retrieval_status[overpass_status["status"]] += 1
        code, notes, best, manual_review = classify_row(
            row,
            candidates,
            coordinate_status,
            coordinate_inside,
            overpass_status,
        )
        if code not in VALIDATION_CODES:
            raise ValueError(f"Unexpected validation code: {code}")

        coded = {
            **row,
            "candidate_osm_id": best.get("osm_id", "") if best else "",
            "candidate_osm_name": best.get("osm_name", "") if best else "",
            "candidate_osm_amenity": best.get("osm_amenity", "") if best else "",
            "candidate_distance_m": best.get("candidate_distance_m", "") if best else "",
            "validation_code": code,
            "validation_notes": notes,
            "reviewer_initials": "ai_det_screen",
            "review_date": now_utc()[:10],
            "coordinate_boundary_status": coordinate_status,
            "coordinate_inside_sampled_upazila": "" if coordinate_inside is None else coordinate_inside,
            "osm_candidate_count_500m": len(candidates),
            "best_candidate_score": best.get("candidate_score", "") if best else "",
            "best_name_score": best.get("name_score", "") if best else "",
            "best_dghs_category": best.get("dghs_category", dghs_category(row)) if best else dghs_category(row),
            "best_osm_category": best.get("osm_category", "") if best else "",
            "manual_review_recommended": manual_review,
            "overpass_status": overpass_status["status"],
            "overpass_cache_file": overpass_status["cache_file"],
            "overpass_retrieved_at": overpass_status["retrieved_at"],
            "overpass_url": overpass_status["overpass_url"],
            "overpass_error": overpass_status["error"],
            "coding_method": "deterministic_public_source_screen_v1",
        }
        coded_rows.append(coded)
        if index % 10 == 0:
            print(f"Coded {index}/{len(rows)} sample rows...", flush=True)

    coded_fields = [
        *list(rows[0].keys()),
        "coordinate_boundary_status",
        "coordinate_inside_sampled_upazila",
        "osm_candidate_count_500m",
        "best_candidate_score",
        "best_name_score",
        "best_dghs_category",
        "best_osm_category",
        "manual_review_recommended",
        "overpass_status",
        "overpass_cache_file",
        "overpass_retrieved_at",
        "overpass_url",
        "overpass_error",
        "coding_method",
    ]
    # Keep the original candidate/code columns in their existing positions but
    # with deterministic coded values.
    write_csv(OUT_CODED_CSV, coded_rows, coded_fields)

    candidate_fields = [
        "sample_group",
        "division_name",
        "district_name",
        "upazila_name",
        "dghs_id",
        "dghs_code",
        "facility_name",
        "dghs_category",
        "osm_id",
        "osm_type",
        "osm_name",
        "osm_amenity",
        "osm_healthcare",
        "osm_category",
        "candidate_latitude",
        "candidate_longitude",
        "candidate_distance_m",
        "name_sequence_score",
        "name_token_overlap",
        "name_substring_score",
        "name_score",
        "category_match",
        "candidate_score",
        "overpass_cache_file",
        "overpass_retrieved_at",
    ]
    write_csv(OUT_CANDIDATES_CSV, candidate_rows, candidate_fields)

    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": "automated_public_source_screen_not_manual_validation",
        "goal_level": "L3 validation coding screen",
        "unit": "sampled DGHS clinical facility row",
        "source_inputs": [
            {
                "path": str(CODING_SHEET.relative_to(ROOT)),
                "role": "blank validation coding sheet from the deterministic sample design",
            },
            {
                "path": str(SAMPLE_JSON.relative_to(ROOT)),
                "role": "sample design metadata and non-claim",
            },
            {
                "path": str(osm_cache_path.relative_to(ROOT)),
                "role": "all-Bangladesh public OSM health-feature Overpass cache",
            },
            {
                "path": str(ADM3_GEOJSON.relative_to(ROOT)),
                "role": "public geoBoundaries ADM3/upazila boundary check",
            },
        ],
        "public_validation_sources": [
            {
                "source": "DGHS public facilities JSON endpoint",
                "role": "Registry row, facility name, type, coordinate, and sampled coding unit.",
                "local_artifact": str(CODING_SHEET.relative_to(ROOT)),
            },
            {
                "source": "OpenStreetMap Overpass",
                "role": "Public OSM health candidates from the cached all-Bangladesh Overpass pull, filtered within 500 meters of valid DGHS coordinates.",
                "query_template": 'area["ISO3166-1"="BD"][admin_level=2]; nwr["amenity"~"^(hospital|clinic|doctors)$"](area); out center tags;',
                "local_artifact": str(osm_cache_path.relative_to(ROOT)),
                "timestamp_osm_base": osm_source_status.get("retrieved_at", ""),
            },
            {
                "source": "geoBoundaries BGD ADM3",
                "role": "Coordinate plausibility check against expected sampled upazila geometry.",
                "local_artifact": str(ADM3_GEOJSON.relative_to(ROOT)),
            },
        ],
        "selection_context": {
            "sample_status": sample_meta.get("status", ""),
            "sampled_upazilas": sample_meta.get("sample_summary", {}).get("sampled_upazilas"),
            "sampled_facility_rows": sample_meta.get("sample_summary", {}).get("sampled_facility_rows"),
            "coordinate_ready_facility_rows": sample_meta.get("sample_summary", {}).get(
                "coordinate_ready_facility_rows"
            ),
        },
        "screen_summary": {
            "coded_rows": len(coded_rows),
            "osm_candidate_rows": len(candidate_rows),
            "manual_review_recommended_rows": sum(int(row["manual_review_recommended"]) for row in coded_rows),
            "rows_with_any_osm_candidate_500m": sum(1 for row in coded_rows if int(row["osm_candidate_count_500m"]) > 0),
            "rows_with_valid_coordinate": sum(
                1 for row in coded_rows if row["coordinate_boundary_status"] != "missing_or_invalid_coordinate"
            ),
            "rows_inside_expected_upazila": sum(
                1 for row in coded_rows if row["coordinate_inside_sampled_upazila"] == 1
            ),
        },
        "validation_code_counts": clean_code_counts(coded_rows),
        "validation_code_counts_by_group": group_code_counts(coded_rows),
        "overpass_status_counts": dict(sorted((key, int(value)) for key, value in retrieval_status.items())),
        "coordinate_boundary_status_counts": dict(sorted((key, int(value)) for key, value in boundary_status.items())),
        "non_claim": (
            "This is an automated public-source coding screen. It is not a human validation pass, "
            "not a facility-quality assessment, not a service-access estimate, and not a ground-truth "
            "facility inventory."
        ),
        "outputs": {
            "coded_screen_csv": str(OUT_CODED_CSV.relative_to(ROOT)),
            "osm_candidates_csv": str(OUT_CANDIDATES_CSV.relative_to(ROOT)),
            "summary_json": str(OUT_SUMMARY_JSON.relative_to(ROOT)),
        },
    }
    write_json(OUT_SUMMARY_JSON, summary)

    print(
        "Built BGD validation coded screen: "
        f"{len(coded_rows)} rows, {len(candidate_rows)} OSM candidates, "
        f"{summary['screen_summary']['manual_review_recommended_rows']} manual-review rows.",
        flush=True,
    )
    print(f"Wrote {OUT_CODED_CSV}", flush=True)
    print(f"Wrote {OUT_CANDIDATES_CSV}", flush=True)
    print(f"Wrote {OUT_SUMMARY_JSON}", flush=True)


if __name__ == "__main__":
    main()
