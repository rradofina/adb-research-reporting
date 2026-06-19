"""Triage Bangladesh PSDQ public-map-gap rows after coordinate screening.

This pass reads the AI public-source review ledger and inspects only the rows
already marked as public-map gaps at valid registry coordinates. It annotates
the rows with upazila-level registry/OSM context, exact-coordinate reuse across
the sampled rows, same-upazila OSM health features outside the original 500 m
screen, and source-repair warnings from the coordinate triage.

The output is a reviewer worklist. It does not close a row, does not replace
human validation, and does not infer service access or facility quality.

Constitution guardrails: public data only, auditable numbers, AI-first honest
labeling, and no composite headline claims.
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

AI_REVIEW_CSV = OUT_DIR / "psdq-bgd-facility-validation-ai-review.csv"
CODED_SCREEN_CSV = OUT_DIR / "psdq-bgd-facility-validation-coded-screen.csv"
COORDINATE_REPAIR_CSV = OUT_DIR / "psdq-bgd-facility-validation-coordinate-repair.csv"
EXPOSURE_CSV = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement.csv"
OSM_UPAZILA_CSV = OUT_DIR / "psdq-bgd-osm-health-upazila.csv"
ADM1_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM1.geojson"
ADM2_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM2.geojson"
ADM3_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM3.geojson"
OSM_CACHE_JSON = CACHE / "bgd_osm_health_features_overpass.json"

OUT_GAP_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap.csv"
OUT_GAP_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-public-map-gap-summary.json"

TRIAGE_METHOD = "ai_public_source_public_map_gap_triage_v1"
STATUS = "ai_public_source_public_map_gap_triage_not_human_validation"
NON_CLAIM = (
    "This is an AI-first public-source triage over sampled DGHS rows already marked "
    "as public-map gaps at valid registry coordinates. It uses cached public DGHS, "
    "geoBoundaries, and OSM/Overpass artifacts only. It is not human validation, "
    "not ground truth, not a facility-quality assessment, and not a service-access estimate."
)

GAP_CODE_ORDER = [
    "valid_coordinate_reused_within_sample_public_map_gap",
    "same_upazila_specific_name_signal_far_from_registry_coordinate",
    "same_upazila_specific_name_signal_outside_500m",
    "threshold_sensitive_same_upazila_osm_500_1000m",
    "zero_osm_in_expected_public_upazila",
    "same_upazila_osm_present_but_not_at_facility",
    "no_nearby_same_upazila_osm_health_signal_within_3km",
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


def osm_url(osm_id: str) -> str:
    if "/" not in osm_id:
        return ""
    osm_type, identifier = osm_id.split("/", 1)
    return f"https://www.openstreetmap.org/{osm_type}/{identifier}"


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
                "shape_id": feature["properties"].get("shapeID") or "",
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
                "osm_name": str(tags.get("name") or ""),
                "osm_amenity": str(tags.get("amenity") or ""),
                "osm_healthcare": str(tags.get("healthcare") or ""),
                "join_key": str(unit.get("join_key") or ""),
                "division_name_geo": str(unit.get("division_name_geo") or ""),
                "district_name_geo": str(unit.get("district_name_geo") or ""),
                "upazila_name_geo": str(unit.get("upazila_name_geo") or ""),
            }
        )
    return points, obj.get("osm3s", {})


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


def duplicate_coordinate_groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = coordinate_key(row)
        if key:
            grouped[key].append(row)
    return dict(grouped)


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
    return nearest


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


def best_name_signal(row: dict[str, str], points: list[dict[str, Any]]) -> dict[str, Any]:
    best: dict[str, Any] = {}
    best_sort: tuple[float, int, float] | None = None
    lat = float_value(row.get("latitude"))
    lon = float_value(row.get("longitude"))
    if lat is None or lon is None:
        return {}
    admin_tokens = (
        name_tokens(row.get("division_name", ""))
        | name_tokens(row.get("district_name", ""))
        | name_tokens(row.get("upazila_name", ""))
    )
    for point in points:
        metrics = name_metrics(row.get("facility_name", ""), str(point.get("osm_name", "")), admin_tokens)
        distance = haversine_m(lat, lon, float(point["lat"]), float(point["lon"]))
        signal_bonus = 1 if specific_name_signal(metrics) else 0
        sort_key = (metrics["score"], signal_bonus, -distance)
        if best_sort is None or sort_key > best_sort:
            best_sort = sort_key
            best = {
                **point,
                "distance_m": round(distance, 1),
                "name_score": metrics["score"],
                "name_sequence_score": metrics["sequence"],
                "name_token_overlap": metrics["overlap"],
                "name_substring_score": metrics["substring"],
                "specific_name_signal": specific_name_signal(metrics),
            }
    return best


def classify_gap(row: dict[str, Any]) -> dict[str, str]:
    duplicate_rows = int_value(row.get("duplicate_sample_coordinate_rows"))
    same_upazila_count = int_value(row.get("same_upazila_osm_health_count"))
    nearest_same = float_value(row.get("nearest_same_upazila_osm_health_distance_m"))
    best_name_is_specific = str(row.get("best_same_upazila_name_specific_signal", "")).lower() == "true"

    if duplicate_rows >= 2:
        return {
            "public_map_gap_code": "valid_coordinate_reused_within_sample_public_map_gap",
            "public_map_gap_disposition": (
                "The row has a valid in-upazila coordinate, but the exact coordinate is reused by another sampled "
                "DGHS row, so the missing-map code is not row-specific."
            ),
            "evidence_strength": "high_for_coordinate_reuse_annotation",
            "remaining_followup_question": (
                "Is this a shared campus, a duplicated registry coordinate, or two registry rows at one mapped site?"
            ),
        }
    if best_name_is_specific:
        name_distance = float_value(row.get("best_same_upazila_name_distance_m"))
        if name_distance is not None and name_distance > 10_000:
            return {
                "public_map_gap_code": "same_upazila_specific_name_signal_far_from_registry_coordinate",
                "public_map_gap_disposition": (
                    "A same-upazila OSM health feature has specific name support, but it is more than 10 kilometers "
                    "from the registry coordinate."
                ),
                "evidence_strength": "medium_for_coordinate_or_name_source_warning",
                "remaining_followup_question": (
                    "Is the registry coordinate stale, is the OSM feature in a different locality, or do the sources use the same name for different sites?"
                ),
            }
        return {
            "public_map_gap_code": "same_upazila_specific_name_signal_outside_500m",
            "public_map_gap_disposition": (
                "A same-upazila OSM health feature outside the 500 meter screen has specific name support, "
                "so the row needs a coordinate, alias, or buffer-sensitivity check."
            ),
            "evidence_strength": "medium_for_possible_outside_buffer_match",
            "remaining_followup_question": (
                "Does the same-upazila OSM feature represent this registry row, a related campus, or a separate facility?"
            ),
        }
    if nearest_same is not None and nearest_same <= 1000:
        return {
            "public_map_gap_code": "threshold_sensitive_same_upazila_osm_500_1000m",
            "public_map_gap_disposition": (
                "The nearest same-upazila OSM health feature is outside 500 meters but within 1 kilometer."
            ),
            "evidence_strength": "medium_for_buffer_sensitivity",
            "remaining_followup_question": (
                "Would a wider matching radius or a coordinate precision rule change the row-level map-gap label?"
            ),
        }
    if same_upazila_count == 0:
        return {
            "public_map_gap_code": "zero_osm_in_expected_public_upazila",
            "public_map_gap_disposition": (
                "The expected public upazila has no joined OSM health feature in the pinned OSM cache."
            ),
            "evidence_strength": "high_for_upazila_level_public_map_absence",
            "remaining_followup_question": (
                "Can another public map tag family, official facility page, or local source identify a mapped facility?"
            ),
        }
    if nearest_same is not None and nearest_same <= 3000:
        return {
            "public_map_gap_code": "same_upazila_osm_present_but_not_at_facility",
            "public_map_gap_disposition": (
                "The upazila has OSM health features, but the nearest same-upazila feature is not within 500 meters "
                "and lacks specific name support for this row."
            ),
            "evidence_strength": "medium_for_facility_specific_public_map_gap",
            "remaining_followup_question": (
                "Is the sampled facility unmapped, mapped under a non-health tag, or recorded under a stale DGHS coordinate?"
            ),
        }
    return {
        "public_map_gap_code": "no_nearby_same_upazila_osm_health_signal_within_3km",
        "public_map_gap_disposition": (
            "The upazila has at least one OSM health feature, but none within 3 kilometers of the sampled coordinate "
            "and no specific same-upazila name signal."
        ),
        "evidence_strength": "medium_high_for_facility_specific_public_map_absence",
        "remaining_followup_question": (
            "Does manual public-map inspection find a non-health-tagged feature, or should this row remain an unmapped facility candidate?"
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
        grouped[str(row.get("sample_group", ""))][str(row.get("public_map_gap_code", ""))] += 1
    output = []
    for group in sorted(grouped):
        item: dict[str, Any] = {"sample_group": group, "rows": int(sum(grouped[group].values()))}
        for code in GAP_CODE_ORDER:
            item[code] = int(grouped[group].get(code, 0))
        output.append(item)
    return output


def upazila_queue_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("join_key", ""))].append(row)
    output: list[dict[str, Any]] = []
    for join_key, items in grouped.items():
        first = items[0]
        counter = Counter(str(item.get("public_map_gap_code", "")) for item in items)
        queue_row: dict[str, Any] = {
            "join_key": join_key,
            "division_name": first.get("division_name", ""),
            "district_name": first.get("district_name", ""),
            "upazila_name": first.get("upazila_name", ""),
            "public_map_gap_rows": len(items),
            "active_clinical_facilities": int_value(first.get("active_clinical_facilities")),
            "osm_health": int_value(first.get("osm_health")),
            "registry_minus_osm_clinical": int_value(first.get("registry_minus_osm_clinical")),
            "registry_gap_share": float_value(first.get("registry_gap_share")),
            "underobserved_buildings_3km_p85_proxy": int_value(first.get("underobserved_buildings_3km_p85_proxy")),
            "coordinate_repair_rows_same_upazila": int_value(first.get("coordinate_repair_rows_same_upazila")),
        }
        for code in GAP_CODE_ORDER:
            queue_row[code] = int(counter.get(code, 0))
        output.append(queue_row)
    output.sort(
        key=lambda row: (
            -int_value(row.get("public_map_gap_rows")),
            -int_value(row.get("underobserved_buildings_3km_p85_proxy")),
            str(row.get("join_key", "")),
        )
    )
    return output


def review_row_chart(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        rows,
        key=lambda row: (
            GAP_CODE_ORDER.index(str(row["public_map_gap_code"]))
            if row.get("public_map_gap_code") in GAP_CODE_ORDER
            else len(GAP_CODE_ORDER),
            int_value(row.get("upazila_sample_order")),
            int_value(row.get("facility_sample_order")),
        ),
    )
    return [
        {
            "review_id": row["review_id"],
            "facility_name": row["facility_name"],
            "upazila_name": row["upazila_name"],
            "join_key": row["join_key"],
            "public_map_gap_code": row["public_map_gap_code"],
            "nearest_same_upazila_osm_health_distance_m": row["nearest_same_upazila_osm_health_distance_m"],
            "same_upazila_osm_health_count": row["same_upazila_osm_health_count"],
            "best_same_upazila_name_score": row["best_same_upazila_name_score"],
        }
        for row in ordered
    ]


def order_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    code = str(row.get("public_map_gap_code", ""))
    return (
        GAP_CODE_ORDER.index(code) if code in GAP_CODE_ORDER else len(GAP_CODE_ORDER),
        int_value(row.get("upazila_sample_order")),
        int_value(row.get("facility_sample_order")),
        str(row.get("dghs_id", "")),
    )


def main() -> None:
    for path in [
        AI_REVIEW_CSV,
        CODED_SCREEN_CSV,
        COORDINATE_REPAIR_CSV,
        EXPOSURE_CSV,
        OSM_UPAZILA_CSV,
        ADM1_GEOJSON,
        ADM2_GEOJSON,
        ADM3_GEOJSON,
        OSM_CACHE_JSON,
    ]:
        if not path.exists():
            raise FileNotFoundError(path)

    ai_review_rows = read_csv(AI_REVIEW_CSV)
    public_map_rows = [
        row for row in ai_review_rows if row.get("ai_review_bucket") == "public_map_gap_at_valid_coordinate"
    ]
    coded_rows = read_csv(CODED_SCREEN_CSV)
    duplicate_groups = duplicate_coordinate_groups(coded_rows)
    coordinate_repair_rows = read_csv(COORDINATE_REPAIR_CSV)
    coordinate_repair_by_join: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in coordinate_repair_rows:
        coordinate_repair_by_join[row.get("join_key", "")].append(row)
    exposure_by_key = {row["join_key"]: row for row in read_csv(EXPOSURE_CSV)}
    osm_upazila_by_key = {row["join_key"]: row for row in read_csv(OSM_UPAZILA_CSV)}

    admin3_units = load_admin3_units()
    osm_points, osm_meta = load_osm_points(admin3_units)
    osm_by_join: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for point in osm_points:
        osm_by_join[str(point.get("join_key", ""))].append(point)
    dghs_public_rows = load_dghs_registry_rows()
    triage_date = now_utc()[:10]

    gap_rows: list[dict[str, Any]] = []
    for row in public_map_rows:
        dghs_id = row.get("dghs_id", "")
        lat = float_value(row.get("latitude"))
        lon = float_value(row.get("longitude"))
        if lat is None or lon is None:
            raise ValueError(f"Public-map-gap row without valid coordinate: {row.get('review_id')}")

        join_key = row.get("join_key", "")
        same_upazila_osm = osm_by_join.get(join_key, [])
        nearest_any = nearest_osm_feature(lat, lon, osm_points)
        nearest_same = nearest_osm_feature(lat, lon, same_upazila_osm) if same_upazila_osm else {}
        best_name = best_name_signal(row, same_upazila_osm) if same_upazila_osm else {}
        exposure = exposure_by_key.get(join_key, {})
        osm_upazila = osm_upazila_by_key.get(join_key, {})
        dghs_public = dghs_public_rows.get(dghs_id, {})
        duplicates = duplicate_groups.get(coordinate_key(row), []) if coordinate_key(row) else []
        coordinate_repairs = coordinate_repair_by_join.get(join_key, [])

        base: dict[str, Any] = {
            "attestation_chain": "ai-first",
            "public_map_gap_method": TRIAGE_METHOD,
            "public_map_gap_date": triage_date,
            **{
                key_name: row.get(key_name, "")
                for key_name in [
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
                    "is_principal_tier",
                    "is_clinical_tier",
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
                    "review_priority",
                ]
            },
            "coordinate_key": coordinate_key(row),
            "duplicate_sample_coordinate_rows": len(duplicates),
            "duplicate_sample_coordinate_facilities": "; ".join(
                f"{item.get('dghs_id', '')}:{item.get('facility_name', '')}" for item in duplicates
            ),
            "coordinate_repair_rows_same_upazila": len(coordinate_repairs),
            "coordinate_repair_codes_same_upazila": "; ".join(
                sorted({item.get("coordinate_repair_code", "") for item in coordinate_repairs if item.get("coordinate_repair_code")})
            ),
            "active_clinical_facilities": exposure.get("active_clinical_facilities", ""),
            "osm_health": exposure.get("osm_health", osm_upazila.get("osm_health", "")),
            "osm_hospital": exposure.get("osm_hospital", osm_upazila.get("osm_hospital", "")),
            "osm_clinic": exposure.get("osm_clinic", osm_upazila.get("osm_clinic", "")),
            "osm_doctors": exposure.get("osm_doctors", osm_upazila.get("osm_doctors", "")),
            "registry_minus_osm_clinical": exposure.get("registry_minus_osm_clinical", ""),
            "registry_gap_share": exposure.get("registry_gap_share", ""),
            "underobserved_buildings_3km_p85_proxy": exposure.get("underobserved_buildings_3km_p85_proxy", ""),
            "same_upazila_osm_health_count": len(same_upazila_osm),
            "nearest_any_osm_health_id": nearest_any.get("osm_id", ""),
            "nearest_any_osm_health_url": nearest_any.get("osm_url", ""),
            "nearest_any_osm_health_name": nearest_any.get("osm_name", ""),
            "nearest_any_osm_health_amenity": nearest_any.get("osm_amenity", ""),
            "nearest_any_osm_health_distance_m": nearest_any.get("distance_m", ""),
            "nearest_same_upazila_osm_health_id": nearest_same.get("osm_id", ""),
            "nearest_same_upazila_osm_health_url": nearest_same.get("osm_url", ""),
            "nearest_same_upazila_osm_health_name": nearest_same.get("osm_name", ""),
            "nearest_same_upazila_osm_health_amenity": nearest_same.get("osm_amenity", ""),
            "nearest_same_upazila_osm_health_distance_m": nearest_same.get("distance_m", ""),
            "best_same_upazila_name_osm_id": best_name.get("osm_id", ""),
            "best_same_upazila_name_osm_url": best_name.get("osm_url", ""),
            "best_same_upazila_name_osm_name": best_name.get("osm_name", ""),
            "best_same_upazila_name_osm_amenity": best_name.get("osm_amenity", ""),
            "best_same_upazila_name_distance_m": best_name.get("distance_m", ""),
            "best_same_upazila_name_score": best_name.get("name_score", ""),
            "best_same_upazila_name_sequence_score": best_name.get("name_sequence_score", ""),
            "best_same_upazila_name_token_overlap": best_name.get("name_token_overlap", ""),
            "best_same_upazila_name_substring_score": best_name.get("name_substring_score", ""),
            "best_same_upazila_name_specific_signal": bool(best_name.get("specific_name_signal", False)),
            **{
                key_name: dghs_public.get(key_name, "")
                for key_name in [
                    "dghs_public_profile_url",
                    "dghs_public_name",
                    "dghs_public_name_bn",
                    "dghs_public_agency",
                    "dghs_public_type",
                    "dghs_public_private_status",
                    "dghs_public_active_status",
                    "dghs_public_cache_file",
                ]
            },
            "source_basis": (
                "AI public-source review ledger; coded-screen sampled DGHS rows; coordinate-repair triage; "
                "Bangladesh exposure-ranked disagreement table; public geoBoundaries BGD ADM1/ADM2/ADM3; "
                "cached all-Bangladesh OSM health-feature Overpass pull; cached DGHS public DataTables rows."
            ),
            "adm1_boundary_file": str(ADM1_GEOJSON.relative_to(ROOT)),
            "adm2_boundary_file": str(ADM2_GEOJSON.relative_to(ROOT)),
            "adm3_boundary_file": str(ADM3_GEOJSON.relative_to(ROOT)),
            "osm_cache_file": str(OSM_CACHE_JSON.relative_to(ROOT)),
            "osm_cache_timestamp_osm_base": osm_meta.get("timestamp_osm_base", ""),
            "row_status_after_public_map_gap_triage": "still_open_requires_public_source_or_human_review",
            "non_claim": NON_CLAIM,
        }
        base.update(classify_gap(base))
        gap_rows.append(base)

    gap_rows.sort(key=order_key)
    for index, row in enumerate(gap_rows, start=1):
        row["public_map_gap_id"] = f"PSDQ-BGD-PMG-{index:03d}"

    fields = [
        "public_map_gap_id",
        "review_id",
        "attestation_chain",
        "public_map_gap_method",
        "public_map_gap_date",
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
        "is_principal_tier",
        "is_clinical_tier",
        "has_valid_coordinate",
        "latitude",
        "longitude",
        "coordinate_key",
        "validation_code",
        "validation_notes",
        "coordinate_boundary_status",
        "coordinate_inside_sampled_upazila",
        "review_priority",
        "duplicate_sample_coordinate_rows",
        "duplicate_sample_coordinate_facilities",
        "coordinate_repair_rows_same_upazila",
        "coordinate_repair_codes_same_upazila",
        "active_clinical_facilities",
        "osm_health",
        "osm_hospital",
        "osm_clinic",
        "osm_doctors",
        "registry_minus_osm_clinical",
        "registry_gap_share",
        "underobserved_buildings_3km_p85_proxy",
        "same_upazila_osm_health_count",
        "nearest_any_osm_health_id",
        "nearest_any_osm_health_url",
        "nearest_any_osm_health_name",
        "nearest_any_osm_health_amenity",
        "nearest_any_osm_health_distance_m",
        "nearest_same_upazila_osm_health_id",
        "nearest_same_upazila_osm_health_url",
        "nearest_same_upazila_osm_health_name",
        "nearest_same_upazila_osm_health_amenity",
        "nearest_same_upazila_osm_health_distance_m",
        "best_same_upazila_name_osm_id",
        "best_same_upazila_name_osm_url",
        "best_same_upazila_name_osm_name",
        "best_same_upazila_name_osm_amenity",
        "best_same_upazila_name_distance_m",
        "best_same_upazila_name_score",
        "best_same_upazila_name_sequence_score",
        "best_same_upazila_name_token_overlap",
        "best_same_upazila_name_substring_score",
        "best_same_upazila_name_specific_signal",
        "public_map_gap_code",
        "public_map_gap_disposition",
        "evidence_strength",
        "row_status_after_public_map_gap_triage",
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
        "adm1_boundary_file",
        "adm2_boundary_file",
        "adm3_boundary_file",
        "osm_cache_file",
        "osm_cache_timestamp_osm_base",
        "non_claim",
    ]
    write_csv(OUT_GAP_CSV, gap_rows, fields)

    nearest_any_distances = [
        float(row["nearest_any_osm_health_distance_m"])
        for row in gap_rows
        if float_value(row.get("nearest_any_osm_health_distance_m")) is not None
    ]
    nearest_same_distances = [
        float(row["nearest_same_upazila_osm_health_distance_m"])
        for row in gap_rows
        if float_value(row.get("nearest_same_upazila_osm_health_distance_m")) is not None
    ]
    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 public-map-gap triage",
        "unit": "sampled DGHS row already marked as public-map gap at a valid coordinate",
        "source_inputs": [
            {
                "path": str(AI_REVIEW_CSV.relative_to(ROOT)),
                "role": "AI public-source review ledger; public-map-gap worklist",
            },
            {
                "path": str(CODED_SCREEN_CSV.relative_to(ROOT)),
                "role": "sampled DGHS rows and exact-coordinate reuse check",
            },
            {
                "path": str(COORDINATE_REPAIR_CSV.relative_to(ROOT)),
                "role": "same-upazila coordinate-repair warning counts",
            },
            {
                "path": str(EXPOSURE_CSV.relative_to(ROOT)),
                "role": "upazila-level registry, OSM, and Open Buildings context",
            },
            {
                "path": str(OSM_UPAZILA_CSV.relative_to(ROOT)),
                "role": "upazila-level OSM health-feature counts assigned to geoBoundaries ADM3",
            },
            {
                "path": str(OSM_CACHE_JSON.relative_to(ROOT)),
                "role": "cached public OSM health-feature nearest-neighbor and same-upazila name-signal check",
                "timestamp_osm_base": osm_meta.get("timestamp_osm_base", ""),
            },
            {
                "path_pattern": str((CACHE / "bgd_dghs_p*.json").relative_to(ROOT)),
                "role": "cached DGHS public DataTables registry rows, including public profile, name, type, and active status",
            },
        ],
        "public_map_gap_scope": {
            "public_map_gap_rows_checked": len(gap_rows),
            "priority_1_high_exposure_rows": sum(
                1 for row in gap_rows if row.get("review_priority") == "priority_1_high_exposure_map_gap"
            ),
            "priority_3_spot_check_rows": sum(
                1 for row in gap_rows if row.get("review_priority") == "priority_3_public_map_gap_spot_check"
            ),
            "rows_with_valid_coordinate": sum(1 for row in gap_rows if row.get("coordinate_key")),
            "rows_inside_expected_upazila": sum(
                1 for row in gap_rows if str(row.get("coordinate_inside_sampled_upazila")) == "1"
            ),
            "rows_with_duplicate_sample_coordinate": sum(
                1 for row in gap_rows if int_value(row.get("duplicate_sample_coordinate_rows")) >= 2
            ),
            "rows_in_upazilas_with_coordinate_repair_flags": sum(
                1 for row in gap_rows if int_value(row.get("coordinate_repair_rows_same_upazila")) > 0
            ),
            "rows_in_zero_osm_expected_upazilas": sum(
                1 for row in gap_rows if int_value(row.get("same_upazila_osm_health_count")) == 0
            ),
            "rows_with_same_upazila_osm_health_features": sum(
                1 for row in gap_rows if int_value(row.get("same_upazila_osm_health_count")) > 0
            ),
            "rows_with_same_upazila_specific_name_signal_outside_500m": sum(
                1 for row in gap_rows if row.get("public_map_gap_code") == "same_upazila_specific_name_signal_outside_500m"
            ),
            "rows_with_same_upazila_specific_name_signal_far_from_registry_coordinate": sum(
                1
                for row in gap_rows
                if row.get("public_map_gap_code")
                == "same_upazila_specific_name_signal_far_from_registry_coordinate"
            ),
            "rows_threshold_sensitive_500m_to_1km": sum(
                1 for row in gap_rows if row.get("public_map_gap_code") == "threshold_sensitive_same_upazila_osm_500_1000m"
            ),
            "rows_with_nearest_any_osm_health_within_1km": sum(1 for distance in nearest_any_distances if distance <= 1000),
            "rows_with_nearest_any_osm_health_beyond_3km": sum(1 for distance in nearest_any_distances if distance > 3000),
            "rows_with_nearest_same_upazila_osm_health_beyond_3km": sum(
                1 for distance in nearest_same_distances if distance > 3000
            ),
            "rows_closed_as_resolved": 0,
            "rows_retained_open": len(gap_rows),
        },
        "public_map_gap_code_counts": count_rows(gap_rows, "public_map_gap_code", GAP_CODE_ORDER),
        "public_map_gap_counts_by_group": count_by_group(gap_rows),
        "evidence_strength_counts": count_rows(gap_rows, "evidence_strength"),
        "upazila_queue_rows": upazila_queue_rows(gap_rows),
        "review_row_chart_rows": review_row_chart(gap_rows),
        "non_claim": NON_CLAIM,
        "outputs": {
            "public_map_gap_csv": str(OUT_GAP_CSV.relative_to(ROOT)),
            "summary_json": str(OUT_GAP_SUMMARY_JSON.relative_to(ROOT)),
        },
    }
    write_json(OUT_GAP_SUMMARY_JSON, summary)

    print(
        "Built BGD public-map-gap triage: "
        f"{len(gap_rows)} rows, "
        f"{summary['public_map_gap_scope']['priority_1_high_exposure_rows']} priority-1 rows, "
        f"{summary['public_map_gap_scope']['rows_in_zero_osm_expected_upazilas']} rows in zero-OSM upazilas.",
        flush=True,
    )
    print(f"Wrote {OUT_GAP_CSV}", flush=True)
    print(f"Wrote {OUT_GAP_SUMMARY_JSON}", flush=True)


if __name__ == "__main__":
    main()
