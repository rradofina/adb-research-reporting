"""Triage Bangladesh PSDQ registry-coordinate repair rows.

This pass reads the AI public-source review ledger and inspects only the rows
that were already marked as registry-coordinate repairs. It compares each
coordinate with public geoBoundaries ADM3/upazila polygons, checks whether the
same coordinate is reused across sampled registry rows, and measures the
nearest cached OSM health feature to the suspect coordinate.

The output is a source-repair worklist. It does not replace human validation,
does not change a source-disagreement claim, and does not infer service access.

Constitution guardrails: public data only (§2.1), auditable numbers (§2.2),
AI-first honest labeling (§18.2), and no composite headline claims (§6.4).
"""

from __future__ import annotations

import csv
import glob
import html
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any

from shapely.geometry import Point, shape
from shapely.ops import nearest_points


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
GEO_CACHE = CACHE / "geo"
OUT_DIR = ROOT / "generated"

AI_REVIEW_CSV = OUT_DIR / "psdq-bgd-facility-validation-ai-review.csv"
CODED_SCREEN_CSV = OUT_DIR / "psdq-bgd-facility-validation-coded-screen.csv"
ADM3_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM3.geojson"
OSM_CACHE_JSON = CACHE / "bgd_osm_health_features_overpass.json"

OUT_REPAIR_CSV = OUT_DIR / "psdq-bgd-facility-validation-coordinate-repair.csv"
OUT_REPAIR_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-coordinate-repair-summary.json"

REPAIR_METHOD = "ai_public_source_coordinate_repair_triage_v1"
STATUS = "ai_public_source_coordinate_repair_triage_not_human_validation"
NON_CLAIM = (
    "This is an AI-first public-source coordinate-repair triage over sampled DGHS rows. "
    "It compares registry coordinates with public geoBoundaries ADM3 polygons and cached "
    "OSM health features. It is not human validation, not ground truth, not a facility-quality "
    "assessment, and not a service-access estimate."
)

REPAIR_CODE_ORDER = [
    "missing_registry_coordinate_requires_source_retrieval",
    "coordinate_reused_by_multiple_sampled_rows",
    "coordinate_in_other_public_upazila_near_osm_health_feature",
    "coordinate_in_other_public_upazila_no_near_osm_health_feature",
    "coordinate_outside_public_adm3_boundary",
]

ALIASES = {
    "barisal": "barishal",
    "bogra": "bogura",
    "chittagong": "chattogram",
    "chittogram": "chattogram",
    "comilla": "cumilla",
    "cox s bazar": "coxs bazar",
    "cox bazar": "coxs bazar",
    "gurudashpur": "gurudaspur",
    "jessore": "jashore",
    "netrokona": "netrakona",
    "panchgarh": "panchagarh",
}


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


def float_value(value: Any) -> float | None:
    try:
        number = float(str(value or "").strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def int_value(value: Any) -> int:
    try:
        return int(float(str(value or "").strip()))
    except (TypeError, ValueError):
        return 0


def normalize_name(value: Any) -> str:
    text = html.unescape(str(value or "")).strip().lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"['`’.,:/_-]", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in sorted(ALIASES.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    return ALIASES.get(text, text)


def coordinate_key(row: dict[str, str]) -> str:
    lat = float_value(row.get("latitude"))
    lon = float_value(row.get("longitude"))
    if lat is None or lon is None:
        return ""
    return f"{lat:.7f},{lon:.7f}"


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6_371_000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def clean_anchor_text(value: Any) -> str:
    text = html.unescape(str(value or ""))
    match = re.search(r">([^<]+)<", text)
    if match:
        return match.group(1).strip()
    return re.sub(r"<[^>]+>", "", text).strip()


def clean_anchor_href(value: Any) -> str:
    text = html.unescape(str(value or ""))
    match = re.search(r"href=([^ >]+)", text)
    return match.group(1).strip("\"'") if match else ""


def load_dghs_registry_rows() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for filename in glob.glob(str(CACHE / "bgd_dghs_p*.json")):
        obj = json.loads(Path(filename).read_text(encoding="utf-8"))
        for row in obj.get("data", []):
            row_id_match = re.search(r">(\d+)<", str(row.get("id", "")))
            row_id = row_id_match.group(1) if row_id_match else str(row.get("id", "")).strip()
            if not row_id:
                continue
            rows[row_id] = {
                "dghs_public_profile_url": clean_anchor_href(row.get("id")),
                "dghs_public_name": clean_anchor_text(row.get("name")),
                "dghs_public_name_bn": str(row.get("name_bn") or "").strip(),
                "dghs_public_agency": str(row.get("facility_agency_name") or "").strip(),
                "dghs_public_type": str(row.get("facility_type_name") or "").strip(),
                "dghs_public_private_status": str(row.get("is_private") or "").strip(),
                "dghs_public_active_status": str(row.get("is_active") or "").strip(),
                "dghs_public_cache_file": str(Path(filename).relative_to(ROOT)),
            }
    return rows


def load_adm3_features() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    obj = json.loads(ADM3_GEOJSON.read_text(encoding="utf-8"))
    features: list[dict[str, Any]] = []
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feature in obj.get("features", []):
        props = feature.get("properties") or {}
        name = str(props.get("shapeName") or "").strip()
        if not name:
            continue
        item = {
            "name": name,
            "name_norm": normalize_name(name),
            "shape_id": str(props.get("shapeID") or ""),
            "geometry": shape(feature["geometry"]),
        }
        features.append(item)
        by_name[item["name_norm"]].append(item)
    return features, dict(by_name)


def load_osm_points() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    obj = json.loads(OSM_CACHE_JSON.read_text(encoding="utf-8"))
    points: list[dict[str, Any]] = []
    for element in obj.get("elements", []):
        lat = float_value(element.get("lat") or (element.get("center") or {}).get("lat"))
        lon = float_value(element.get("lon") or (element.get("center") or {}).get("lon"))
        if lat is None or lon is None:
            continue
        tags = element.get("tags") or {}
        points.append(
            {
                "lat": lat,
                "lon": lon,
                "osm_id": f"{element.get('type')}/{element.get('id')}",
                "osm_type": str(element.get("type") or ""),
                "osm_name": str(tags.get("name") or ""),
                "osm_amenity": str(tags.get("amenity") or ""),
                "osm_healthcare": str(tags.get("healthcare") or ""),
            }
        )
    return points, obj.get("osm3s", {})


def osm_url(osm_id: str) -> str:
    if "/" not in osm_id:
        return ""
    osm_type, identifier = osm_id.split("/", 1)
    return f"https://www.openstreetmap.org/{osm_type}/{identifier}"


def containing_adm3_names(lat: float, lon: float, features: list[dict[str, Any]]) -> list[str]:
    point = Point(lon, lat)
    names = [
        feature["name"]
        for feature in features
        if feature["geometry"].contains(point) or feature["geometry"].touches(point)
    ]
    return sorted(set(names))


def distance_to_expected_upazila_m(
    lat: float,
    lon: float,
    expected_name: str,
    adm3_by_name: dict[str, list[dict[str, Any]]],
) -> float | None:
    expected = adm3_by_name.get(normalize_name(expected_name), [])
    if not expected:
        return None
    point = Point(lon, lat)
    distances: list[float] = []
    for feature in expected:
        point_on_input, point_on_geom = nearest_points(point, feature["geometry"])
        distances.append(haversine_m(point_on_input.y, point_on_input.x, point_on_geom.y, point_on_geom.x))
    return min(distances) if distances else None


def nearest_osm_feature(lat: float, lon: float, osm_points: list[dict[str, Any]]) -> dict[str, Any]:
    nearest: dict[str, Any] = {}
    nearest_distance: float | None = None
    for point in osm_points:
        distance = haversine_m(lat, lon, float(point["lat"]), float(point["lon"]))
        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest = dict(point)
    if nearest_distance is None:
        return {}
    nearest["distance_m"] = round(nearest_distance, 1)
    nearest["osm_url"] = osm_url(str(nearest.get("osm_id", "")))
    return nearest


def duplicate_coordinate_groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = coordinate_key(row)
        if key:
            grouped[key].append(row)
    return dict(grouped)


def classify_repair(row: dict[str, Any]) -> dict[str, str]:
    if not row["coordinate_key"]:
        return {
            "coordinate_repair_code": "missing_registry_coordinate_requires_source_retrieval",
            "coordinate_repair_disposition": (
                "The sampled DGHS row has no usable latitude/longitude, so map matching cannot start."
            ),
            "evidence_strength": "high_for_missing_coordinate_only",
            "remaining_followup_question": (
                "Can a public DGHS profile, registry export, or official facility page provide a coordinate?"
            ),
        }
    if int_value(row["duplicate_sample_coordinate_rows"]) >= 2:
        return {
            "coordinate_repair_code": "coordinate_reused_by_multiple_sampled_rows",
            "coordinate_repair_disposition": (
                "The exact sampled coordinate is reused by more than one DGHS facility row."
            ),
            "evidence_strength": "high_for_registry_coordinate_reuse",
            "remaining_followup_question": (
                "Is this a shared campus coordinate, a district placeholder, or a duplicated coordinate copied across rows?"
            ),
        }
    if not row["observed_public_adm3_names"]:
        return {
            "coordinate_repair_code": "coordinate_outside_public_adm3_boundary",
            "coordinate_repair_disposition": (
                "The coordinate does not fall inside a public Bangladesh ADM3 polygon in the geoBoundaries file."
            ),
            "evidence_strength": "high_for_boundary_mismatch",
            "remaining_followup_question": (
                "Is the coordinate outside Bangladesh, on a boundary gap, or attached to a stale/non-registry location?"
            ),
        }
    if float_value(row["nearest_osm_health_distance_m"]) is not None and float(row["nearest_osm_health_distance_m"]) <= 500:
        return {
            "coordinate_repair_code": "coordinate_in_other_public_upazila_near_osm_health_feature",
            "coordinate_repair_disposition": (
                "The registry coordinate falls in a different public ADM3/upazila and is near a cached OSM health feature."
            ),
            "evidence_strength": "medium_high_for_wrong_admin_coordinate",
            "remaining_followup_question": (
                "Does the coordinate point to a different facility, a nearby campus, or a stale registry coordinate?"
            ),
        }
    return {
        "coordinate_repair_code": "coordinate_in_other_public_upazila_no_near_osm_health_feature",
        "coordinate_repair_disposition": (
            "The registry coordinate falls in a different public ADM3/upazila and is not near a cached OSM health feature."
        ),
        "evidence_strength": "medium_for_wrong_admin_coordinate",
        "remaining_followup_question": (
            "Can another public source repair the coordinate, or should the row stay outside the map-matching denominator?"
        ),
    }


def count_rows(rows: list[dict[str, Any]], key: str, order: list[str] | None = None) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(key, "")) for row in rows)
    keys = order or sorted(counter)
    output = [{"name": item, "rows": int(counter.get(item, 0))} for item in keys if counter.get(item, 0)]
    for item in sorted(counter):
        if order and item not in order:
            output.append({"name": item, "rows": int(counter[item])})
    return output


def count_by_group(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[str(row.get("sample_group", ""))][str(row.get("coordinate_repair_code", ""))] += 1
    output = []
    for group in sorted(grouped):
        item: dict[str, Any] = {"sample_group": group, "rows": int(sum(grouped[group].values()))}
        for code in REPAIR_CODE_ORDER:
            item[code] = int(grouped[group].get(code, 0))
        output.append(item)
    return output


def order_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    code = str(row.get("coordinate_repair_code", ""))
    return (
        REPAIR_CODE_ORDER.index(code) if code in REPAIR_CODE_ORDER else len(REPAIR_CODE_ORDER),
        int_value(row.get("upazila_sample_order")),
        int_value(row.get("facility_sample_order")),
        str(row.get("dghs_id", "")),
    )


def distance_chart_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_rows = [row for row in rows if float_value(row.get("distance_to_expected_upazila_km")) is not None]
    valid_rows.sort(key=lambda row: float(row["distance_to_expected_upazila_km"]), reverse=True)
    output = []
    for row in valid_rows:
        output.append(
            {
                "review_id": row["review_id"],
                "facility_name": row["facility_name"],
                "expected_upazila": row["upazila_name"],
                "observed_public_adm3_names": row["observed_public_adm3_names"],
                "distance_to_expected_upazila_km": row["distance_to_expected_upazila_km"],
                "coordinate_repair_code": row["coordinate_repair_code"],
                "nearest_osm_health_distance_m": row["nearest_osm_health_distance_m"],
            }
        )
    return output


def main() -> None:
    for path in [AI_REVIEW_CSV, CODED_SCREEN_CSV, ADM3_GEOJSON, OSM_CACHE_JSON]:
        if not path.exists():
            raise FileNotFoundError(path)

    ai_review_rows = read_csv(AI_REVIEW_CSV)
    coded_rows = read_csv(CODED_SCREEN_CSV)
    coordinate_rows = [
        row for row in ai_review_rows if row.get("ai_review_bucket") == "registry_coordinate_repair"
    ]
    duplicate_groups = duplicate_coordinate_groups(coded_rows)
    adm3_features, adm3_by_name = load_adm3_features()
    osm_points, osm_meta = load_osm_points()
    dghs_public_rows = load_dghs_registry_rows()
    triage_date = now_utc()[:10]

    repair_rows: list[dict[str, Any]] = []
    for row in coordinate_rows:
        dghs_id = row.get("dghs_id", "")
        lat = float_value(row.get("latitude"))
        lon = float_value(row.get("longitude"))
        key = coordinate_key(row)
        duplicates = duplicate_groups.get(key, []) if key else []
        observed_names: list[str] = []
        distance_to_expected_m: float | None = None
        nearest_osm: dict[str, Any] = {}
        if lat is not None and lon is not None:
            observed_names = containing_adm3_names(lat, lon, adm3_features)
            distance_to_expected_m = distance_to_expected_upazila_m(lat, lon, row.get("upazila_name", ""), adm3_by_name)
            nearest_osm = nearest_osm_feature(lat, lon, osm_points)

        dghs_public = dghs_public_rows.get(dghs_id, {})
        base: dict[str, Any] = {
            "attestation_chain": "ai-first",
            "coordinate_repair_method": REPAIR_METHOD,
            "coordinate_repair_date": triage_date,
            **{key_name: row.get(key_name, "") for key_name in [
                "review_id",
                "sample_group",
                "upazila_sample_order",
                "facility_sample_order",
                "division_name",
                "district_name",
                "upazila_name",
                "join_key",
                "dghs_id",
                "dghs_code",
                "facility_name",
                "facility_type_name",
                "facility_level_name",
                "facility_healthcare_level_name",
                "is_private",
                "has_valid_coordinate",
                "latitude",
                "longitude",
                "validation_code",
                "validation_notes",
                "coordinate_boundary_status",
                "coordinate_inside_sampled_upazila",
                "ai_review_disposition",
                "ai_review_notes",
                "human_followup_question",
            ]},
            "coordinate_key": key,
            "observed_public_adm3_names": "; ".join(observed_names),
            "distance_to_expected_upazila_km": (
                "" if distance_to_expected_m is None else round(distance_to_expected_m / 1000, 1)
            ),
            "nearest_osm_health_id": nearest_osm.get("osm_id", ""),
            "nearest_osm_health_url": nearest_osm.get("osm_url", ""),
            "nearest_osm_health_name": nearest_osm.get("osm_name", ""),
            "nearest_osm_health_amenity": nearest_osm.get("osm_amenity", ""),
            "nearest_osm_health_distance_m": nearest_osm.get("distance_m", ""),
            "duplicate_sample_coordinate_rows": len(duplicates),
            "duplicate_sample_coordinate_facilities": "; ".join(
                f"{item.get('dghs_id', '')}:{item.get('facility_name', '')}" for item in duplicates
            ),
            **{key_name: dghs_public.get(key_name, "") for key_name in [
                "dghs_public_profile_url",
                "dghs_public_name",
                "dghs_public_name_bn",
                "dghs_public_agency",
                "dghs_public_type",
                "dghs_public_private_status",
                "dghs_public_active_status",
                "dghs_public_cache_file",
            ]},
            "source_basis": (
                "AI public-source review ledger; coded-screen sampled DGHS rows; public geoBoundaries BGD ADM3; "
                "cached all-Bangladesh OSM health-feature Overpass pull; cached DGHS public DataTables rows."
            ),
            "adm3_boundary_file": str(ADM3_GEOJSON.relative_to(ROOT)),
            "osm_cache_file": str(OSM_CACHE_JSON.relative_to(ROOT)),
            "osm_cache_timestamp_osm_base": osm_meta.get("timestamp_osm_base", ""),
            "row_status_after_coordinate_repair_triage": "still_open_requires_public_coordinate_source_or_human_review",
            "non_claim": NON_CLAIM,
        }
        base.update(classify_repair(base))
        repair_rows.append(base)

    repair_rows.sort(key=order_key)
    for index, row in enumerate(repair_rows, start=1):
        row["coordinate_repair_id"] = f"PSDQ-BGD-CR-{index:03d}"

    fields = [
        "coordinate_repair_id",
        "review_id",
        "attestation_chain",
        "coordinate_repair_method",
        "coordinate_repair_date",
        "sample_group",
        "upazila_sample_order",
        "facility_sample_order",
        "division_name",
        "district_name",
        "upazila_name",
        "join_key",
        "dghs_id",
        "dghs_code",
        "facility_name",
        "facility_type_name",
        "facility_level_name",
        "facility_healthcare_level_name",
        "is_private",
        "has_valid_coordinate",
        "latitude",
        "longitude",
        "coordinate_key",
        "validation_code",
        "validation_notes",
        "coordinate_boundary_status",
        "coordinate_inside_sampled_upazila",
        "observed_public_adm3_names",
        "distance_to_expected_upazila_km",
        "nearest_osm_health_id",
        "nearest_osm_health_url",
        "nearest_osm_health_name",
        "nearest_osm_health_amenity",
        "nearest_osm_health_distance_m",
        "duplicate_sample_coordinate_rows",
        "duplicate_sample_coordinate_facilities",
        "coordinate_repair_code",
        "coordinate_repair_disposition",
        "evidence_strength",
        "row_status_after_coordinate_repair_triage",
        "remaining_followup_question",
        "dghs_public_profile_url",
        "dghs_public_name",
        "dghs_public_name_bn",
        "dghs_public_agency",
        "dghs_public_type",
        "dghs_public_private_status",
        "dghs_public_active_status",
        "dghs_public_cache_file",
        "ai_review_disposition",
        "ai_review_notes",
        "human_followup_question",
        "source_basis",
        "adm3_boundary_file",
        "osm_cache_file",
        "osm_cache_timestamp_osm_base",
        "non_claim",
    ]
    write_csv(OUT_REPAIR_CSV, repair_rows, fields)

    valid_distances = [
        float(row["distance_to_expected_upazila_km"])
        for row in repair_rows
        if float_value(row.get("distance_to_expected_upazila_km")) is not None
    ]
    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 coordinate-source repair triage",
        "unit": "sampled DGHS row already queued for registry-coordinate repair",
        "source_inputs": [
            {
                "path": str(AI_REVIEW_CSV.relative_to(ROOT)),
                "role": "AI public-source review ledger; coordinate-repair worklist",
            },
            {
                "path": str(CODED_SCREEN_CSV.relative_to(ROOT)),
                "role": "sampled DGHS rows and exact-coordinate reuse check",
            },
            {
                "path": str(ADM3_GEOJSON.relative_to(ROOT)),
                "role": "public ADM3/upazila boundary check",
            },
            {
                "path": str(OSM_CACHE_JSON.relative_to(ROOT)),
                "role": "cached public OSM health-feature nearest-neighbor check",
                "timestamp_osm_base": osm_meta.get("timestamp_osm_base", ""),
            },
            {
                "path_pattern": str((CACHE / "bgd_dghs_p*.json").relative_to(ROOT)),
                "role": "cached DGHS public DataTables registry rows, including public profile, name, type, and active status",
            },
        ],
        "repair_scope": {
            "coordinate_repair_rows_checked": len(repair_rows),
            "missing_registry_coordinate_rows": sum(
                1 for row in repair_rows if row["coordinate_repair_code"] == "missing_registry_coordinate_requires_source_retrieval"
            ),
            "valid_coordinate_rows": sum(1 for row in repair_rows if row["coordinate_key"]),
            "valid_coordinates_outside_expected_upazila": sum(1 for row in repair_rows if row["coordinate_key"]),
            "rows_inside_other_public_adm3": sum(1 for row in repair_rows if row["observed_public_adm3_names"]),
            "rows_outside_public_adm3_boundary": sum(
                1 for row in repair_rows if row["coordinate_repair_code"] == "coordinate_outside_public_adm3_boundary"
            ),
            "rows_with_nearest_osm_health_feature_within_500m": sum(
                1
                for row in repair_rows
                if float_value(row.get("nearest_osm_health_distance_m")) is not None
                and float(row["nearest_osm_health_distance_m"]) <= 500
            ),
            "rows_with_duplicate_sample_coordinate": sum(
                1 for row in repair_rows if int_value(row.get("duplicate_sample_coordinate_rows")) >= 2
            ),
            "rows_at_least_50km_from_expected_upazila": sum(1 for distance in valid_distances if distance >= 50),
            "max_distance_to_expected_upazila_km": max(valid_distances) if valid_distances else None,
            "median_distance_to_expected_upazila_km": median(valid_distances) if valid_distances else None,
            "rows_closed_as_coordinate_repaired": 0,
            "rows_retained_open": len(repair_rows),
        },
        "coordinate_repair_code_counts": count_rows(repair_rows, "coordinate_repair_code", REPAIR_CODE_ORDER),
        "coordinate_repair_counts_by_group": count_by_group(repair_rows),
        "evidence_strength_counts": count_rows(repair_rows, "evidence_strength"),
        "distance_chart_rows": distance_chart_rows(repair_rows),
        "non_claim": NON_CLAIM,
        "outputs": {
            "coordinate_repair_csv": str(OUT_REPAIR_CSV.relative_to(ROOT)),
            "summary_json": str(OUT_REPAIR_SUMMARY_JSON.relative_to(ROOT)),
        },
    }
    write_json(OUT_REPAIR_SUMMARY_JSON, summary)

    print(
        "Built BGD coordinate-repair triage: "
        f"{len(repair_rows)} rows, "
        f"{summary['repair_scope']['missing_registry_coordinate_rows']} missing coordinates, "
        f"{summary['repair_scope']['valid_coordinate_rows']} outside expected upazila.",
        flush=True,
    )
    print(f"Wrote {OUT_REPAIR_CSV}", flush=True)
    print(f"Wrote {OUT_REPAIR_SUMMARY_JSON}", flush=True)


if __name__ == "__main__":
    main()
