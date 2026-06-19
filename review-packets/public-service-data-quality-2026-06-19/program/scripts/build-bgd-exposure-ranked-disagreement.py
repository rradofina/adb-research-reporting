"""Build Bangladesh upazila exposure-ranked registry-map disagreement.

This script fetches Bangladesh OSM health features, assigns their point or
center coordinates to geoBoundaries ADM3 polygons, and joins the resulting
upazila OSM counts to DGHS registry counts plus the Google Open Buildings
nearest-facility denominator.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from numbers import Integral
from pathlib import Path
from typing import Any

from shapely.geometry import Point, shape
from shapely.strtree import STRtree


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
GEO_CACHE = CACHE / "geo"
OUT_DIR = ROOT / "generated"

FACILITY_EXTRACT = OUT_DIR / "psdq-bgd-facility-coordinate-extract.csv"
OPEN_BUILDINGS_ADMIN = OUT_DIR / "psdq-bgd-open-buildings-admin-summary.csv"

OSM_CACHE = CACHE / "bgd_osm_health_features_overpass.json"
ADM1_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM1.geojson"
ADM2_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM2.geojson"
ADM3_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM3.geojson"

OSM_UPAZILA_CSV = OUT_DIR / "psdq-bgd-osm-health-upazila.csv"
EXPOSURE_CSV = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement.csv"
EXPOSURE_JSON = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement-summary.json"

GEOB_API = "https://www.geoboundaries.org/api/current/gbOpen/BGD/{level}"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OSM_QUERY = """
[out:json][timeout:180];
area["ISO3166-1"="BD"][admin_level=2]->.a;
(
  nwr["amenity"~"^(hospital|clinic|doctors)$"](area.a);
);
out center tags;
"""


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-osm", action="store_true", help="Re-fetch Overpass even if cache exists.")
    parser.add_argument("--overpass-url", default=OVERPASS_URL)
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def request(url: str, data: bytes | None = None) -> bytes:
    req = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": "ADB-Research-PSDQ/1.0 (local reproducibility script)"},
    )
    with urllib.request.urlopen(req, timeout=240) as response:
        return response.read()


def ensure_geoboundary(level: str, path: Path) -> None:
    if path.exists():
        return
    GEO_CACHE.mkdir(parents=True, exist_ok=True)
    meta = json.loads(request(GEOB_API.format(level=level)).decode("utf-8"))
    url = meta["gjDownloadURL"]
    print(f"Downloading {level} boundary: {url}", flush=True)
    path.write_bytes(request(url))


def fetch_osm(overpass_url: str, refresh: bool) -> dict[str, Any]:
    if OSM_CACHE.exists() and not refresh:
        return json.loads(OSM_CACHE.read_text(encoding="utf-8"))
    CACHE.mkdir(parents=True, exist_ok=True)
    body = urllib.parse.urlencode({"data": OSM_QUERY}).encode("utf-8")
    print(f"Fetching OSM Bangladesh health features from {overpass_url}", flush=True)
    obj = json.loads(request(overpass_url, data=body).decode("utf-8"))
    OSM_CACHE.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return obj


def load_features(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["features"]


def normalize_name(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"['`’.-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in sorted(ALIASES.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    text = ALIASES.get(text, text)
    return text


def admin_key(district: Any, upazila: Any) -> str:
    key = f"{normalize_name(district)}|{normalize_name(upazila)}"
    return KEY_ALIASES.get(key, key)


def tree_lookup(point: Point, geoms: list[Any], tree: STRtree) -> int | None:
    hits = tree.query(point)
    for hit in hits:
        idx = int(hit) if isinstance(hit, Integral) else geoms.index(hit)
        if geoms[idx].covers(point):
            return idx
    return None


def build_admin3_units() -> list[dict[str, Any]]:
    ensure_geoboundary("ADM1", ADM1_GEOJSON)
    ensure_geoboundary("ADM2", ADM2_GEOJSON)
    ensure_geoboundary("ADM3", ADM3_GEOJSON)

    adm1_features = load_features(ADM1_GEOJSON)
    adm2_features = load_features(ADM2_GEOJSON)
    adm3_features = load_features(ADM3_GEOJSON)

    adm1_geoms = [shape(feature["geometry"]) for feature in adm1_features]
    adm2_geoms = [shape(feature["geometry"]) for feature in adm2_features]
    adm1_tree = STRtree(adm1_geoms)
    adm2_tree = STRtree(adm2_geoms)

    units = []
    for feature in adm3_features:
        geom = shape(feature["geometry"])
        point = geom.representative_point()
        adm1_idx = tree_lookup(point, adm1_geoms, adm1_tree)
        adm2_idx = tree_lookup(point, adm2_geoms, adm2_tree)
        units.append(
            {
                "division_name_geo": adm1_features[adm1_idx]["properties"]["shapeName"] if adm1_idx is not None else None,
                "district_name_geo": adm2_features[adm2_idx]["properties"]["shapeName"] if adm2_idx is not None else None,
                "upazila_name_geo": feature["properties"]["shapeName"],
                "shape_id": feature["properties"].get("shapeID"),
                "geometry": geom,
            }
        )
    return units


def osm_point(element: dict[str, Any]) -> tuple[float, float] | None:
    if "lat" in element and "lon" in element:
        return float(element["lat"]), float(element["lon"])
    center = element.get("center") or {}
    if "lat" in center and "lon" in center:
        return float(center["lat"]), float(center["lon"])
    return None


def assign_osm_to_upazilas(osm_obj: dict[str, Any], admin3_units: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    geoms = [unit["geometry"] for unit in admin3_units]
    tree = STRtree(geoms)
    assigned = defaultdict(lambda: {"osm_health": 0, "osm_hospital": 0, "osm_clinic": 0, "osm_doctors": 0})
    unassigned = 0
    missing_coordinate = 0

    for element in osm_obj.get("elements", []):
        tags = element.get("tags") or {}
        amenity = tags.get("amenity")
        coords = osm_point(element)
        if coords is None:
            missing_coordinate += 1
            continue
        lat, lon = coords
        idx = tree_lookup(Point(lon, lat), geoms, tree)
        if idx is None:
            unassigned += 1
            continue
        key = admin_key(admin3_units[idx]["district_name_geo"], admin3_units[idx]["upazila_name_geo"])
        assigned[key]["osm_health"] += 1
        if amenity == "hospital":
            assigned[key]["osm_hospital"] += 1
        elif amenity == "clinic":
            assigned[key]["osm_clinic"] += 1
        elif amenity == "doctors":
            assigned[key]["osm_doctors"] += 1

    rows = []
    for unit in admin3_units:
        key = admin_key(unit["district_name_geo"], unit["upazila_name_geo"])
        counts = assigned[key]
        rows.append(
            {
                "division_name_geo": unit["division_name_geo"],
                "district_name_geo": unit["district_name_geo"],
                "upazila_name_geo": unit["upazila_name_geo"],
                "shape_id": unit["shape_id"],
                "join_key": key,
                "osm_health": counts["osm_health"],
                "osm_hospital": counts["osm_hospital"],
                "osm_clinic": counts["osm_clinic"],
                "osm_doctors": counts["osm_doctors"],
            }
        )
    rows.sort(key=lambda r: (-r["osm_health"], r["division_name_geo"] or "", r["district_name_geo"] or "", r["upazila_name_geo"] or ""))

    meta = osm_obj.get("osm3s", {})
    stats = {
        "osm_elements": len(osm_obj.get("elements", [])),
        "assigned_features": sum(row["osm_health"] for row in rows),
        "unassigned_features": unassigned,
        "missing_coordinate_features": missing_coordinate,
        "timestamp_osm_base": meta.get("timestamp_osm_base"),
        "timestamp_areas_base": meta.get("timestamp_areas_base"),
    }
    return rows, stats


def read_registry_admin() -> dict[str, dict[str, Any]]:
    grouped = defaultdict(
        lambda: {
            "division_name": None,
            "district_name": None,
            "upazila_name": None,
            "registry_records": 0,
            "active_facilities": 0,
            "registry_clinical_facilities": 0,
            "active_clinical_facilities": 0,
            "coordinate_facilities": 0,
        }
    )
    with FACILITY_EXTRACT.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            key = admin_key(row.get("district_name"), row.get("upazila_name"))
            item = grouped[key]
            item["division_name"] = row.get("division_name")
            item["district_name"] = row.get("district_name")
            item["upazila_name"] = row.get("upazila_name")
            item["registry_records"] += 1
            is_active = int(row.get("is_active") or 0)
            is_clinical = int(row.get("is_clinical_tier") or 0)
            item["active_facilities"] += is_active
            item["registry_clinical_facilities"] += is_clinical
            item["active_clinical_facilities"] += is_active * is_clinical
            item["coordinate_facilities"] += int(row.get("has_valid_coordinate") or 0)
    return dict(grouped)


def read_open_buildings_admin() -> dict[str, dict[str, Any]]:
    out = {}
    with OPEN_BUILDINGS_ADMIN.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            out[admin_key(row.get("district_name"), row.get("upazila_name"))] = row
    return out


def int_field(row: dict[str, Any] | None, name: str) -> int:
    if not row:
        return 0
    value = row.get(name)
    return int(float(value)) if value not in (None, "") else 0


def build_exposure_rows(osm_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    registry = read_registry_admin()
    buildings = read_open_buildings_admin()
    osm_by_key = {row["join_key"]: row for row in osm_rows}

    rows = []
    matched_osm_features = 0
    for key, reg in registry.items():
        if not reg.get("upazila_name"):
            continue
        osm = osm_by_key.get(key)
        bldg = buildings.get(key)
        active_clinical = int(reg["active_clinical_facilities"])
        osm_health = int(osm["osm_health"]) if osm else 0
        gap = max(active_clinical - osm_health, 0)
        gap_share = (gap / active_clinical) if active_clinical else 0.0
        b3_p85 = int_field(bldg, "buildings_nearest_3km_p85")
        b1_p85 = int_field(bldg, "buildings_nearest_1km_p85")
        b5_p85 = int_field(bldg, "buildings_nearest_5km_p85")
        exposure_proxy = round(b3_p85 * gap_share)
        if osm:
            matched_osm_features += osm_health
        rows.append(
            {
                "division_name": reg["division_name"],
                "district_name": reg["district_name"],
                "upazila_name": reg["upazila_name"],
                "join_key": key,
                "registry_records": int(reg["registry_records"]),
                "active_facilities": int(reg["active_facilities"]),
                "active_clinical_facilities": active_clinical,
                "coordinate_facilities": int(reg["coordinate_facilities"]),
                "osm_health": osm_health,
                "osm_hospital": int(osm["osm_hospital"]) if osm else 0,
                "osm_clinic": int(osm["osm_clinic"]) if osm else 0,
                "osm_doctors": int(osm["osm_doctors"]) if osm else 0,
                "osm_to_active_clinical_ratio": round(osm_health / active_clinical, 4) if active_clinical else None,
                "registry_minus_osm_clinical": gap,
                "registry_gap_share": round(gap_share, 4),
                "buildings_nearest_1km_p85": b1_p85,
                "buildings_nearest_3km_p85": b3_p85,
                "buildings_nearest_5km_p85": b5_p85,
                "underobserved_buildings_3km_p85_proxy": exposure_proxy,
                "has_open_buildings_denominator": int(b3_p85 > 0),
                "has_osm_boundary_match": int(osm is not None),
            }
        )

    rows.sort(
        key=lambda r: (
            -int(r["underobserved_buildings_3km_p85_proxy"]),
            -int(r["buildings_nearest_3km_p85"]),
            r["division_name"] or "",
            r["district_name"] or "",
            r["upazila_name"] or "",
        )
    )
    stats = {
        "registry_admin_rows": len(rows),
        "matched_osm_features": matched_osm_features,
        "osm_admin_rows_with_features": sum(1 for row in osm_rows if row["osm_health"] > 0),
        "osm_features_not_joined_to_registry": sum(row["osm_health"] for row in osm_rows) - matched_osm_features,
        "rows_with_open_buildings_denominator": sum(1 for row in rows if row["has_open_buildings_denominator"]),
    }
    return rows, stats


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def clean_json_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return json.loads(json.dumps(rows, ensure_ascii=False, allow_nan=False))


def main() -> None:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    osm_obj = fetch_osm(args.overpass_url, args.refresh_osm)
    admin3_units = build_admin3_units()
    osm_rows, osm_stats = assign_osm_to_upazilas(osm_obj, admin3_units)
    exposure_rows, exposure_stats = build_exposure_rows(osm_rows)

    write_csv(OSM_UPAZILA_CSV, osm_rows)
    write_csv(EXPOSURE_CSV, exposure_rows)

    summary = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "unit": "division/district/upazila",
        "source": "OpenStreetMap Overpass + DGHS public facilities JSON endpoint + Google Open Buildings V3 point CSVs + geoBoundaries BGD ADM3",
        "method": (
            "OSM amenity=hospital/clinic/doctors features are assigned by node or way/relation center to "
            "geoBoundaries ADM3 polygons. Upazila OSM counts are joined to DGHS active clinical facility "
            "counts and Google Open Buildings nearest-facility p85 denominators. The exposure proxy equals "
            "3 km p85 buildings multiplied by max(active clinical registry facilities minus OSM health "
            "features, 0) divided by active clinical registry facilities."
        ),
        "osm": osm_stats,
        "exposure": {
            **exposure_stats,
            "active_clinical_facilities": sum(int(row["active_clinical_facilities"]) for row in exposure_rows),
            "osm_health_joined": sum(int(row["osm_health"]) for row in exposure_rows),
            "registry_minus_osm_clinical": sum(int(row["registry_minus_osm_clinical"]) for row in exposure_rows),
            "buildings_nearest_3km_p85": sum(int(row["buildings_nearest_3km_p85"]) for row in exposure_rows),
            "underobserved_buildings_3km_p85_proxy": sum(int(row["underobserved_buildings_3km_p85_proxy"]) for row in exposure_rows),
        },
        "top_exposure_gap_upazilas": clean_json_rows(exposure_rows[:20]),
        "outputs": {
            "osm_upazila_csv": str(OSM_UPAZILA_CSV.relative_to(ROOT)),
            "exposure_csv": str(EXPOSURE_CSV.relative_to(ROOT)),
        },
        "non_claim": (
            "The exposure proxy is a screening index. It is not population, households, poverty, service "
            "demand, a verified facility catchment, a travel-time estimate, or proof that either OSM or the "
            "official registry is the ground-truth facility list."
        ),
    }
    EXPOSURE_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(f"Wrote {OSM_UPAZILA_CSV}")
    print(f"Wrote {EXPOSURE_CSV}")
    print(f"Wrote {EXPOSURE_JSON}")


if __name__ == "__main__":
    main()
