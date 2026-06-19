"""Build a targeted public-map inspection pack for Bangladesh map-gap rows.

This pass starts from the 40-row row-evidence ledger. It uses the pinned
OSM/Overpass cache and public geoBoundaries ADM3 polygons to show, row by row,
which public-map features should be inspected first and what evidence would be
needed before a row could be closed or reclassified.

It does not fetch new sources, does not close rows, and does not perform human
validation. The output is a reviewer inspection packet for the next PSDQ loop.

Constitution guardrails: public data only, auditable numbers, AI-first honest
labeling, and no composite headline claims.
"""

from __future__ import annotations

import csv
import html
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from numbers import Integral
from pathlib import Path
from typing import Any

from shapely.geometry import Point, shape
from shapely.strtree import STRtree


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
GEO_CACHE = CACHE / "geo"
OUT_DIR = ROOT / "generated"

IN_ROW_EVIDENCE_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap-evidence.csv"
IN_ROW_EVIDENCE_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap-evidence-summary.json"
ADM1_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM1.geojson"
ADM2_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM2.geojson"
ADM3_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM3.geojson"
OSM_CACHE_JSON = CACHE / "bgd_osm_health_features_overpass.json"

OUT_INSPECTION_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-map-inspection.csv"
OUT_INSPECTION_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-public-map-inspection-summary.json"

METHOD = "ai_public_map_targeted_inspection_v1"
STATUS = "ai_public_map_targeted_inspection_not_human_validation"
NON_CLAIM = (
    "This is an AI-first targeted public-map inspection packet for sampled DGHS "
    "public-map-gap rows. It uses the committed row-evidence ledger, public "
    "DGHS profile links, public geoBoundaries, and the pinned OSM/Overpass "
    "health-feature cache. It is not human validation, not ground truth, not a "
    "facility-quality assessment, and not a service-access estimate."
)

TARGET_UPAZILAS = {"gazipur sadar", "narayanganj sadar", "pabna sadar"}

ROW_EVIDENCE_TIER_ORDER = [
    "source_repair_before_row_absence",
    "possible_match_or_buffer_review",
    "row_level_public_map_absence_review",
    "upazila_level_public_map_observability_review",
]

INSPECTION_LANE_ORDER = [
    "source_repair_first",
    "possible_public_map_match_or_buffer_case",
    "facility_specific_public_map_absence_candidate",
    "upazila_public_map_observability_gap",
]

ALIASES = {
    "barisal": "barishal",
    "baghai chhari": "baghaichari",
    "balia kandi": "baliakandi",
    "bagher para": "bagherpara",
    "beani bazar": "beanibazar",
    "bogra": "bogura",
    "brahamanbaria": "brahmanbaria",
    "brahman para": "brahmanpara",
    "burhanuddin": "borhanuddin",
    "char fasson": "charfession",
    "char rajibpur": "rajibpur",
    "chaugachha": "chaugacha",
    "chittagong": "chattogram",
    "chittogram": "chattogram",
    "comilla": "cumilla",
    "cox s bazar": "coxs bazar",
    "cox bazar": "coxs bazar",
    "fatikchhari": "fatikchari",
    "goalandaghat": "goalanda",
    "golabganj": "golapganj",
    "gurudashpur": "gurudaspur",
    "haim char": "haimchar",
    "jessore": "jashore",
    "jhalokati": "jhalokathi",
    "jhikargachha": "jhikargacha",
    "kala para": "kalapara",
    "khagrachhari": "khagrachari",
    "kotali para": "kotalipara",
    "kuliar char": "kuliarchar",
    "manoharganj": "monoharganj",
    "manikchhari": "manikchari",
    "manirampur": "monirampur",
    "maulvi bazar": "maulvibazar",
    "mitha pukur": "mithapukur",
    "muktagachha": "muktagacha",
    "mujib nagar": "mujibnagar",
    "naikhongchhari": "naikhongchari",
    "netrokona": "netrakona",
    "paikgachha": "paikgacha",
    "rajshani": "rajshahi",
    "rowangchhari": "rowangchari",
    "roypur": "raipur",
    "saghatta": "saghata",
    "shib char": "shibchar",
    "tungi para": "tungipara",
    "ullah para": "ullahpara",
}

KEY_ALIASES = {
    "jashore|kotwali": "jashore|jashore sadar",
    "nawabganj|gomastapur": "chapainawabganj|gomastapur",
    "nawabganj|bholahat": "chapainawabganj|bholahat",
    "nawabganj|nachole": "chapainawabganj|nachole",
    "nawabganj|nawabganj sadar": "chapainawabganj|chapainawabganj sadar",
    "nawabganj|shibganj": "chapainawabganj|shibganj",
    "sunamganj|dakshin sunamganj": "sunamganj|shantiganj",
}

NAME_STOPWORDS = {
    "and",
    "bank",
    "bd",
    "bed",
    "blood",
    "care",
    "center",
    "centre",
    "clinic",
    "college",
    "community",
    "complex",
    "diagnostic",
    "district",
    "foundation",
    "general",
    "health",
    "hospital",
    "limited",
    "ltd",
    "medical",
    "mission",
    "nursing",
    "private",
    "pvt",
    "sadar",
    "specialized",
    "sub",
    "union",
    "upazila",
}

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
    "website",
    "phone",
]


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
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"['`’.,:/_-]", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
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


def admin_key(district: Any, upazila: Any) -> str:
    key = f"{normalize_name(district)}|{normalize_name(upazila)}"
    return KEY_ALIASES.get(key, key)


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6_371_000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def osm_url(osm_id: str) -> str:
    if "/" not in osm_id:
        return ""
    osm_type, identifier = osm_id.split("/", 1)
    return f"https://www.openstreetmap.org/{osm_type}/{identifier}"


def compact_tags(tags: dict[str, Any]) -> str:
    pairs = []
    for key in TAG_KEYS_FOR_REVIEW:
        value = tags.get(key)
        if value not in (None, ""):
            pairs.append(f"{key}={value}")
    return "; ".join(pairs)


def tree_lookup(point: Point, geoms: list[Any], tree: STRtree) -> int | None:
    hits = tree.query(point)
    for hit in hits:
        idx = int(hit) if isinstance(hit, Integral) else geoms.index(hit)
        if geoms[idx].covers(point):
            return idx
    return None


def load_features(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["features"]


def load_admin3_units() -> list[dict[str, Any]]:
    adm1_features = load_features(ADM1_GEOJSON)
    adm2_features = load_features(ADM2_GEOJSON)
    adm3_features = load_features(ADM3_GEOJSON)

    adm1_geoms = [shape(feature["geometry"]) for feature in adm1_features]
    adm2_geoms = [shape(feature["geometry"]) for feature in adm2_features]
    adm1_tree = STRtree(adm1_geoms)
    adm2_tree = STRtree(adm2_geoms)

    units: list[dict[str, Any]] = []
    for feature in adm3_features:
        geom = shape(feature["geometry"])
        point = geom.representative_point()
        adm1_idx = tree_lookup(point, adm1_geoms, adm1_tree)
        adm2_idx = tree_lookup(point, adm2_geoms, adm2_tree)
        district = adm2_features[adm2_idx]["properties"]["shapeName"] if adm2_idx is not None else ""
        upazila = feature["properties"]["shapeName"]
        units.append(
            {
                "division_name_geo": adm1_features[adm1_idx]["properties"]["shapeName"] if adm1_idx is not None else "",
                "district_name_geo": district,
                "upazila_name_geo": upazila,
                "join_key": admin_key(district, upazila),
                "geometry": geom,
            }
        )
    return units


def osm_point(element: dict[str, Any]) -> tuple[float, float] | None:
    lat = float_value(element.get("lat") or (element.get("center") or {}).get("lat"))
    lon = float_value(element.get("lon") or (element.get("center") or {}).get("lon"))
    if lat is None or lon is None:
        return None
    return lat, lon


def load_osm_points(admin3_units: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    obj = json.loads(OSM_CACHE_JSON.read_text(encoding="utf-8"))
    geoms = [unit["geometry"] for unit in admin3_units]
    tree = STRtree(geoms)
    points: list[dict[str, Any]] = []
    for element in obj.get("elements", []):
        coords = osm_point(element)
        if coords is None:
            continue
        lat, lon = coords
        idx = tree_lookup(Point(lon, lat), geoms, tree)
        unit = admin3_units[idx] if idx is not None else {}
        tags = element.get("tags") or {}
        osm_id = f"{element.get('type')}/{element.get('id')}"
        points.append(
            {
                "lat": lat,
                "lon": lon,
                "osm_id": osm_id,
                "osm_url": osm_url(osm_id),
                "osm_name": str(tags.get("name") or tags.get("name:en") or tags.get("name:bn") or ""),
                "osm_amenity": str(tags.get("amenity") or ""),
                "osm_healthcare": str(tags.get("healthcare") or ""),
                "osm_tags_compact": compact_tags(tags),
                "join_key": str(unit.get("join_key") or ""),
                "division_name_geo": str(unit.get("division_name_geo") or ""),
                "district_name_geo": str(unit.get("district_name_geo") or ""),
                "upazila_name_geo": str(unit.get("upazila_name_geo") or ""),
            }
        )
    return points, obj.get("osm3s", {})


def name_metrics(left: str, right: str, admin_tokens: set[str] | None = None) -> dict[str, float]:
    left_norm = normalize_name(left)
    right_norm = normalize_name(right)
    if not left_norm or not right_norm:
        return {"sequence": 0.0, "overlap": 0.0, "substring": 0.0, "score": 0.0}
    sequence = SequenceMatcher(None, left_norm, right_norm).ratio()
    admin_tokens = admin_tokens or set()
    left_tokens = name_tokens(left_norm) - admin_tokens
    right_tokens = name_tokens(right_norm) - admin_tokens
    overlap = 0.0
    if left_tokens and right_tokens:
        overlap = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
    substring = 0.0
    if len(left_norm) >= 6 and len(right_norm) >= 6 and (left_norm in right_norm or right_norm in left_norm):
        substring = min(len(left_norm), len(right_norm)) / max(len(left_norm), len(right_norm))
    return {
        "sequence": round(sequence, 4),
        "overlap": round(overlap, 4),
        "substring": round(substring, 4),
        "score": round(max(sequence, overlap, substring), 4),
    }


def specific_name_signal(metrics: dict[str, float]) -> bool:
    return (
        metrics["score"] >= 0.55
        and (metrics["overlap"] > 0 or metrics["substring"] >= 0.50 or metrics["sequence"] >= 0.75)
    )


def feature_records(row: dict[str, str], points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lat = float_value(row.get("latitude"))
    lon = float_value(row.get("longitude"))
    if lat is None or lon is None:
        return []
    admin_tokens = (
        name_tokens(row.get("division_name", ""))
        | name_tokens(row.get("district_name", ""))
        | name_tokens(row.get("upazila_name", ""))
    )
    records = []
    for point in points:
        distance = haversine_m(lat, lon, float(point["lat"]), float(point["lon"]))
        metrics = name_metrics(row.get("facility_name", ""), str(point.get("osm_name", "")), admin_tokens)
        records.append(
            {
                **point,
                "distance_m": round(distance, 1),
                "name_score": metrics["score"],
                "name_sequence_score": metrics["sequence"],
                "name_token_overlap": metrics["overlap"],
                "name_substring_score": metrics["substring"],
                "specific_name_signal": specific_name_signal(metrics),
            }
        )
    return records


def sort_candidate_features(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda item: (
            -int(bool(item.get("specific_name_signal"))),
            -float(item.get("name_score") or 0),
            float(item.get("distance_m") or 9_999_999),
            str(item.get("osm_id") or ""),
        ),
    )


def nearest_features(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda item: (float(item.get("distance_m") or 9_999_999), -float(item.get("name_score") or 0)),
    )


def nearest_national_records(row: dict[str, str], points: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    lat = float_value(row.get("latitude"))
    lon = float_value(row.get("longitude"))
    if lat is None or lon is None:
        return []
    nearest = []
    for point in points:
        nearest.append(
            {
                **point,
                "distance_m": round(haversine_m(lat, lon, float(point["lat"]), float(point["lon"])), 1),
            }
        )
    nearest = sorted(nearest, key=lambda item: (float(item.get("distance_m") or 9_999_999), str(item.get("osm_id") or "")))[
        :limit
    ]
    admin_tokens = (
        name_tokens(row.get("division_name", ""))
        | name_tokens(row.get("district_name", ""))
        | name_tokens(row.get("upazila_name", ""))
    )
    for item in nearest:
        metrics = name_metrics(row.get("facility_name", ""), str(item.get("osm_name", "")), admin_tokens)
        item["name_score"] = metrics["score"]
        item["name_sequence_score"] = metrics["sequence"]
        item["name_token_overlap"] = metrics["overlap"]
        item["name_substring_score"] = metrics["substring"]
        item["specific_name_signal"] = specific_name_signal(metrics)
    return nearest


def focus_class(row: dict[str, str]) -> str:
    upazila_norm = normalize_name(row.get("upazila_name", ""))
    if upazila_norm in TARGET_UPAZILAS:
        return "start_here_named_upazila"
    if row.get("row_evidence_tier") == "upazila_level_public_map_observability_review":
        return "start_here_zero_osm_upazila_queue"
    if row.get("priority_scope") == "priority_1_high_exposure":
        return "priority_1_follow_on"
    return "priority_3_spot_check_backstop"


def focus_sort_value(row: dict[str, str]) -> int:
    order = {
        "start_here_named_upazila": 0,
        "start_here_zero_osm_upazila_queue": 1,
        "priority_1_follow_on": 2,
        "priority_3_spot_check_backstop": 3,
    }
    return order.get(focus_class(row), 9)


def inspection_lane(row: dict[str, str]) -> str:
    tier = row.get("row_evidence_tier", "")
    if tier == "source_repair_before_row_absence":
        return "source_repair_first"
    if tier == "possible_match_or_buffer_review":
        return "possible_public_map_match_or_buffer_case"
    if tier == "row_level_public_map_absence_review":
        return "facility_specific_public_map_absence_candidate"
    if tier == "upazila_level_public_map_observability_review":
        return "upazila_public_map_observability_gap"
    return "unclassified_public_map_inspection"


def decision_text(row: dict[str, str], candidates: list[dict[str, Any]]) -> tuple[str, str, str, str]:
    lane = inspection_lane(row)
    best = candidates[0] if candidates else {}
    best_name = str(best.get("osm_name") or "").strip()
    best_distance = float_value(best.get("distance_m"))
    best_score = float_value(best.get("name_score")) or 0.0

    if lane == "source_repair_first":
        return (
            "keep_open_source_repair_first",
            "not_eligible_for_ai_closure",
            "coordinate_or_duplicate_source_repair",
            "A public DGHS coordinate correction, shared-campus explanation, or public OSM feature confirming the duplicated/far-name site would be needed before row-level map absence language is used.",
        )
    if lane == "possible_public_map_match_or_buffer_case":
        if best_name and best_distance is not None:
            evidence = f"Best same-upazila public-map candidate is {best_name} at {best_distance:,.0f} m with name score {best_score:.4f}."
        else:
            evidence = "No same-upazila OSM candidate is available in the pinned health-feature cache."
        return (
            "keep_open_possible_match_or_buffer_review",
            "not_eligible_for_ai_closure",
            "possible_same_facility_after_public_map_or_alias_review",
            evidence + " A row could be reclassified only if public map tags or an official source show the feature represents the DGHS row.",
        )
    if lane == "facility_specific_public_map_absence_candidate":
        if best_name and best_distance is not None:
            evidence = f"Nearest prioritized same-upazila candidate is {best_name} at {best_distance:,.0f} m; this supports inspection, not closure."
        else:
            evidence = "The pinned cache provides no same-upazila candidate for this row."
        return (
            "keep_open_facility_specific_absence_candidate",
            "not_eligible_for_ai_closure",
            "candidate_public_map_absence_requires_manual_public_map_check",
            evidence + " Closure would require public coordinate inspection and a documented search for mapped non-health tags or official public locator evidence.",
        )
    if lane == "upazila_public_map_observability_gap":
        return (
            "keep_open_upazila_observability_gap",
            "not_eligible_for_ai_closure",
            "upazila_level_observability_not_row_absence",
            "The expected upazila has zero joined OSM health features in the pinned cache. A row-level label would require another public tag family, official locator, or human public-map confirmation.",
        )
    return (
        "keep_open_unclassified_public_map_review",
        "not_eligible_for_ai_closure",
        "unclassified_review_required",
        "The row needs public-source review before any label change.",
    )


def public_cache_finding(row: dict[str, str], candidates: list[dict[str, Any]], nearest_any: list[dict[str, Any]]) -> str:
    lane = inspection_lane(row)
    same_count = int_value(row.get("same_upazila_osm_health_count"))
    if lane == "upazila_public_map_observability_gap":
        nearest = nearest_any[0] if nearest_any else {}
        if nearest:
            return (
                f"Expected upazila has 0 joined OSM health features; nearest health feature in the national cache is "
                f"{nearest.get('osm_name') or 'unnamed feature'} at {float(nearest.get('distance_m') or 0):,.0f} m "
                f"outside the expected upazila join."
            )
        return "Expected upazila has 0 joined OSM health features in the pinned national cache."
    if candidates:
        best = candidates[0]
        return (
            f"Expected upazila has {same_count} joined OSM health features. Prioritized candidate: "
            f"{best.get('osm_name') or 'unnamed feature'} at {float(best.get('distance_m') or 0):,.0f} m; "
            f"name score {float(best.get('name_score') or 0):.4f}; tags: {best.get('osm_tags_compact') or 'no review tags'}."
        )
    return f"Expected upazila has {same_count} joined OSM health features, but no candidate record was available for this row."


def add_candidate_fields(output: dict[str, Any], candidates: list[dict[str, Any]], prefix: str, limit: int = 3) -> None:
    for idx in range(limit):
        item = candidates[idx] if idx < len(candidates) else {}
        number = idx + 1
        output[f"{prefix}_{number}_url"] = item.get("osm_url", "")
        output[f"{prefix}_{number}_name"] = item.get("osm_name", "")
        output[f"{prefix}_{number}_amenity"] = item.get("osm_amenity", "")
        output[f"{prefix}_{number}_healthcare"] = item.get("osm_healthcare", "")
        output[f"{prefix}_{number}_distance_m"] = item.get("distance_m", "")
        output[f"{prefix}_{number}_name_score"] = item.get("name_score", "")
        output[f"{prefix}_{number}_specific_name_signal"] = bool(item.get("specific_name_signal", False)) if item else ""
        output[f"{prefix}_{number}_tags_compact"] = item.get("osm_tags_compact", "")


def count_rows(rows: list[dict[str, Any]], key: str, order: list[str] | None = None) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(key, "")) for row in rows)
    keys = order or sorted(counter)
    output = [{"name": item, "rows": int(counter.get(item, 0))} for item in keys if counter.get(item, 0)]
    for item in sorted(counter):
        if order and item not in order:
            output.append({"name": item, "rows": int(counter[item])})
    return output


def upazila_inspection_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("join_key", ""))].append(row)
    output = []
    for join_key, items in grouped.items():
        first = items[0]
        lane_counter = Counter(str(item.get("inspection_lane", "")) for item in items)
        focus_counter = Counter(str(item.get("focus_class", "")) for item in items)
        output.append(
            {
                "join_key": join_key,
                "division_name": first.get("division_name", ""),
                "district_name": first.get("district_name", ""),
                "upazila_name": first.get("upazila_name", ""),
                "inspection_rows": len(items),
                "priority_1_rows": sum(1 for item in items if item.get("priority_scope") == "priority_1_high_exposure"),
                "source_repair_first": int(lane_counter.get("source_repair_first", 0)),
                "possible_public_map_match_or_buffer_case": int(lane_counter.get("possible_public_map_match_or_buffer_case", 0)),
                "facility_specific_public_map_absence_candidate": int(
                    lane_counter.get("facility_specific_public_map_absence_candidate", 0)
                ),
                "upazila_public_map_observability_gap": int(lane_counter.get("upazila_public_map_observability_gap", 0)),
                "start_here_rows": int(
                    focus_counter.get("start_here_named_upazila", 0)
                    + focus_counter.get("start_here_zero_osm_upazila_queue", 0)
                ),
                "active_clinical_facilities": int_value(first.get("active_clinical_facilities")),
                "osm_health": int_value(first.get("osm_health")),
                "underobserved_buildings_3km_p85_proxy": int_value(first.get("underobserved_buildings_3km_p85_proxy")),
            }
        )
    output.sort(
        key=lambda row: (
            -int_value(row.get("start_here_rows")),
            -int_value(row.get("inspection_rows")),
            -int_value(row.get("underobserved_buildings_3km_p85_proxy")),
            str(row.get("join_key", "")),
        )
    )
    return output


def row_card_rows(rows: list[dict[str, Any]], limit: int = 12) -> list[dict[str, Any]]:
    cards = []
    for row in rows[:limit]:
        cards.append(
            {
                "inspection_id": row["inspection_id"],
                "inspection_rank": int_value(row["inspection_rank"]),
                "focus_class": row["focus_class"],
                "facility_name": row["facility_name"],
                "facility_type_name": row["facility_type_name"],
                "district_name": row["district_name"],
                "upazila_name": row["upazila_name"],
                "priority_scope": row["priority_scope"],
                "inspection_lane": row["inspection_lane"],
                "inspection_decision": row["inspection_decision"],
                "closure_eligibility": row["closure_eligibility"],
                "public_cache_finding": row["public_cache_finding"],
                "evidence_needed_to_close_or_reclassify": row["evidence_needed_to_close_or_reclassify"],
                "dghs_public_profile_url": row["dghs_public_profile_url"],
                "registry_coordinate_osm_inspection_url": row["registry_coordinate_osm_inspection_url"],
                "candidate_feature_1_url": row["candidate_feature_1_url"],
                "candidate_feature_1_name": row["candidate_feature_1_name"],
                "candidate_feature_1_distance_m": row["candidate_feature_1_distance_m"],
                "candidate_feature_1_name_score": row["candidate_feature_1_name_score"],
                "candidate_feature_1_tags_compact": row["candidate_feature_1_tags_compact"],
            }
        )
    return cards


def main() -> None:
    for path in [
        IN_ROW_EVIDENCE_CSV,
        IN_ROW_EVIDENCE_SUMMARY_JSON,
        ADM1_GEOJSON,
        ADM2_GEOJSON,
        ADM3_GEOJSON,
        OSM_CACHE_JSON,
    ]:
        if not path.exists():
            raise FileNotFoundError(path)

    row_evidence = read_csv(IN_ROW_EVIDENCE_CSV)
    row_summary = json.loads(IN_ROW_EVIDENCE_SUMMARY_JSON.read_text(encoding="utf-8"))
    admin3_units = load_admin3_units()
    osm_points, osm_meta = load_osm_points(admin3_units)
    osm_by_join: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for point in osm_points:
        osm_by_join[str(point.get("join_key", ""))].append(point)

    inspection_date = now_utc()[:10]
    ordered_evidence = sorted(
        row_evidence,
        key=lambda row: (
            focus_sort_value(row),
            int_value(row.get("evidence_rank")),
            str(row.get("dghs_id", "")),
        ),
    )

    inspection_rows: list[dict[str, Any]] = []
    for index, row in enumerate(ordered_evidence, start=1):
        join_key = row.get("join_key", "")
        same_upazila_records = feature_records(row, osm_by_join.get(join_key, []))
        candidate_features = sort_candidate_features(same_upazila_records)[:3]
        nearest_same = nearest_features(same_upazila_records)[:3]
        nearest_any = nearest_national_records(row, osm_points)
        if not candidate_features:
            candidate_features = nearest_any[:3]

        decision, closure, reclassification, evidence_needed = decision_text(row, candidate_features)
        lane = inspection_lane(row)
        focus = focus_class(row)
        output: dict[str, Any] = {
            "inspection_id": f"PSDQ-BGD-PMI-{index:03d}",
            "inspection_rank": index,
            "inspection_method": METHOD,
            "inspection_date": inspection_date,
            "attestation_chain": "ai-first",
            "focus_class": focus,
            "row_evidence_id": row.get("row_evidence_id", ""),
            "evidence_rank": row.get("evidence_rank", ""),
            "priority_scope": row.get("priority_scope", ""),
            "public_map_gap_id": row.get("public_map_gap_id", ""),
            "review_id": row.get("review_id", ""),
            "division_name": row.get("division_name", ""),
            "district_name": row.get("district_name", ""),
            "upazila_name": row.get("upazila_name", ""),
            "join_key": join_key,
            "dghs_id": row.get("dghs_id", ""),
            "dghs_code": row.get("dghs_code", ""),
            "facility_name": row.get("facility_name", ""),
            "facility_type_name": row.get("facility_type_name", ""),
            "dghs_public_name": row.get("dghs_public_name", ""),
            "dghs_public_name_bn": row.get("dghs_public_name_bn", ""),
            "dghs_public_type": row.get("dghs_public_type", ""),
            "dghs_public_private_status": row.get("dghs_public_private_status", ""),
            "dghs_public_active_status": row.get("dghs_public_active_status", ""),
            "dghs_public_profile_url": row.get("dghs_public_profile_url", ""),
            "latitude": row.get("latitude", ""),
            "longitude": row.get("longitude", ""),
            "registry_coordinate_osm_inspection_url": row.get("registry_coordinate_osm_inspection_url", ""),
            "active_clinical_facilities": row.get("active_clinical_facilities", ""),
            "osm_health": row.get("osm_health", ""),
            "registry_minus_osm_clinical": row.get("registry_minus_osm_clinical", ""),
            "registry_gap_share": row.get("registry_gap_share", ""),
            "underobserved_buildings_3km_p85_proxy": row.get("underobserved_buildings_3km_p85_proxy", ""),
            "same_upazila_osm_health_count": row.get("same_upazila_osm_health_count", ""),
            "duplicate_sample_coordinate_rows": row.get("duplicate_sample_coordinate_rows", ""),
            "coordinate_repair_rows_same_upazila": row.get("coordinate_repair_rows_same_upazila", ""),
            "public_map_gap_code": row.get("public_map_gap_code", ""),
            "public_map_gap_lane_label": row.get("public_map_gap_lane_label", ""),
            "row_evidence_tier": row.get("row_evidence_tier", ""),
            "row_evidence_decision": row.get("row_evidence_decision", ""),
            "inspection_lane": lane,
            "inspection_decision": decision,
            "closure_eligibility": closure,
            "reclassification_candidate": reclassification,
            "inspection_status_after_pass": "still_open_requires_public_source_or_human_review",
            "public_cache_finding": public_cache_finding(row, candidate_features, nearest_any),
            "evidence_needed_to_close_or_reclassify": evidence_needed,
            "source_basis": (
                "Row-evidence CSV; public DGHS profile URL; public geoBoundaries ADM3 cache; "
                "pinned all-Bangladesh OSM/Overpass health-feature cache; public OSM coordinate and feature URLs."
            ),
            "non_claim": NON_CLAIM,
        }
        add_candidate_fields(output, candidate_features, "candidate_feature")
        add_candidate_fields(output, nearest_same, "nearest_same_upazila_feature")
        add_candidate_fields(output, nearest_any, "nearest_national_feature")
        inspection_rows.append(output)

    fields = [
        "inspection_id",
        "inspection_rank",
        "inspection_method",
        "inspection_date",
        "attestation_chain",
        "focus_class",
        "row_evidence_id",
        "evidence_rank",
        "priority_scope",
        "public_map_gap_id",
        "review_id",
        "division_name",
        "district_name",
        "upazila_name",
        "join_key",
        "dghs_id",
        "dghs_code",
        "facility_name",
        "facility_type_name",
        "dghs_public_name",
        "dghs_public_name_bn",
        "dghs_public_type",
        "dghs_public_private_status",
        "dghs_public_active_status",
        "dghs_public_profile_url",
        "latitude",
        "longitude",
        "registry_coordinate_osm_inspection_url",
        "active_clinical_facilities",
        "osm_health",
        "registry_minus_osm_clinical",
        "registry_gap_share",
        "underobserved_buildings_3km_p85_proxy",
        "same_upazila_osm_health_count",
        "duplicate_sample_coordinate_rows",
        "coordinate_repair_rows_same_upazila",
        "public_map_gap_code",
        "public_map_gap_lane_label",
        "row_evidence_tier",
        "row_evidence_decision",
        "inspection_lane",
        "inspection_decision",
        "closure_eligibility",
        "reclassification_candidate",
        "inspection_status_after_pass",
        "public_cache_finding",
        "evidence_needed_to_close_or_reclassify",
    ]
    for prefix in ["candidate_feature", "nearest_same_upazila_feature", "nearest_national_feature"]:
        for number in range(1, 4):
            fields.extend(
                [
                    f"{prefix}_{number}_url",
                    f"{prefix}_{number}_name",
                    f"{prefix}_{number}_amenity",
                    f"{prefix}_{number}_healthcare",
                    f"{prefix}_{number}_distance_m",
                    f"{prefix}_{number}_name_score",
                    f"{prefix}_{number}_specific_name_signal",
                    f"{prefix}_{number}_tags_compact",
                ]
            )
    fields.extend(["source_basis", "non_claim"])

    write_csv(OUT_INSPECTION_CSV, inspection_rows, fields)

    lane_counts = count_rows(inspection_rows, "inspection_lane", INSPECTION_LANE_ORDER)
    focus_counts = count_rows(
        inspection_rows,
        "focus_class",
        [
            "start_here_named_upazila",
            "start_here_zero_osm_upazila_queue",
            "priority_1_follow_on",
            "priority_3_spot_check_backstop",
        ],
    )
    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 targeted public-map inspection packet",
        "unit": "sampled DGHS public-map-gap row",
        "source_inputs": [
            {
                "path": str(IN_ROW_EVIDENCE_CSV.relative_to(ROOT)),
                "role": "row-level public-source evidence ledger",
            },
            {
                "path": str(IN_ROW_EVIDENCE_SUMMARY_JSON.relative_to(ROOT)),
                "role": "row-level evidence summary",
            },
            {
                "path": str(OSM_CACHE_JSON.relative_to(ROOT)),
                "role": "pinned all-Bangladesh OSM/Overpass health-feature cache",
            },
            {
                "path": str(ADM3_GEOJSON.relative_to(ROOT)),
                "role": "public ADM3 boundary cache for same-upazila assignment",
            },
        ],
        "upstream_row_evidence_scope": row_summary.get("row_evidence_scope", {}),
        "inspection_scope": {
            "rows_inspected": len(inspection_rows),
            "priority_1_rows_inspected": sum(
                1 for row in inspection_rows if row.get("priority_scope") == "priority_1_high_exposure"
            ),
            "start_here_named_upazila_rows": sum(
                1 for row in inspection_rows if row.get("focus_class") == "start_here_named_upazila"
            ),
            "start_here_zero_osm_upazila_rows": sum(
                1 for row in inspection_rows if row.get("focus_class") == "start_here_zero_osm_upazila_queue"
            ),
            "rows_with_candidate_public_map_feature": sum(
                1 for row in inspection_rows if row.get("candidate_feature_1_url")
            ),
            "rows_with_same_upazila_candidate_public_map_feature": sum(
                1
                for row in inspection_rows
                if row.get("candidate_feature_1_url") and int_value(row.get("same_upazila_osm_health_count")) > 0
            ),
            "rows_with_specific_name_signal_in_candidate_features": sum(
                1 for row in inspection_rows if row.get("candidate_feature_1_specific_name_signal") is True
            ),
            "rows_kept_open": sum(
                1
                for row in inspection_rows
                if row.get("inspection_status_after_pass") == "still_open_requires_public_source_or_human_review"
            ),
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
        },
        "inspection_lane_counts": lane_counts,
        "focus_class_counts": focus_counts,
        "closure_eligibility_counts": count_rows(inspection_rows, "closure_eligibility"),
        "reclassification_candidate_counts": count_rows(inspection_rows, "reclassification_candidate"),
        "upazila_inspection_rows": upazila_inspection_rows(inspection_rows),
        "row_card_rows": row_card_rows(inspection_rows),
        "public_map_cache": {
            "osm_health_features_loaded": len(osm_points),
            "overpass_timestamp_osm_base": osm_meta.get("timestamp_osm_base", ""),
            "overpass_copyright": osm_meta.get("copyright", ""),
        },
        "inspection_notes": [
            "This pass intentionally keeps every row open because the public cache does not by itself prove ground truth.",
            "Source-repair-first rows should not be used as facility-specific map absence evidence until coordinate or duplicate-row questions are resolved.",
            "Zero-OSM upazila rows are interpreted as upazila-level public-map observability gaps, not row-level absence findings.",
            "Rows with possible outside-buffer or same-name signals need public-map or official-source confirmation before reclassification.",
        ],
        "non_claim": NON_CLAIM,
    }
    write_json(OUT_INSPECTION_SUMMARY_JSON, summary)
    print(
        "Built BGD targeted public-map inspection: "
        f"{len(inspection_rows)} rows, "
        f"{summary['inspection_scope']['start_here_named_upazila_rows']} named-upazila start rows, "
        f"{summary['inspection_scope']['start_here_zero_osm_upazila_rows']} zero-OSM queue rows, "
        "0 closed."
    )
    print(f"Wrote {OUT_INSPECTION_CSV}")
    print(f"Wrote {OUT_INSPECTION_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
