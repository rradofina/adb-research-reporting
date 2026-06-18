"""Build Bangladesh upazila road-surface context for PSDQ exposure gaps.

The road input is HeiGIT's Bangladesh road-surface GeoPackage derived from
OSM, Mapillary imagery, and deep-learning predictions. Road segments are
assigned to geoBoundaries ADM3 polygons by a representative point on each
line. This is a triage/context layer, not a length-split road inventory.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
import pyogrio


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
GEO_CACHE = CACHE / "geo"
ROAD_CACHE = CACHE / "roads"
OUT_DIR = ROOT / "generated"

ROAD_GPKG = ROAD_CACHE / "heigit_bgd_roadsurface_lines.gpkg"
ADM1_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM1.geojson"
ADM2_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM2.geojson"
ADM3_GEOJSON = GEO_CACHE / "geoBoundaries-BGD-ADM3.geojson"
EXPOSURE_CSV = OUT_DIR / "psdq-bgd-exposure-ranked-disagreement.csv"

ROAD_UPAZILA_CSV = OUT_DIR / "psdq-bgd-road-surface-upazila.csv"
ROAD_SUMMARY_JSON = OUT_DIR / "psdq-bgd-road-surface-summary.json"
EXPOSURE_ROAD_CSV = OUT_DIR / "psdq-bgd-exposure-road-context.csv"
EXPOSURE_ROAD_JSON = OUT_DIR / "psdq-bgd-exposure-road-context-summary.json"

ROAD_URL = "https://downloads.ohsome.org/hdx/mapillary_road_surface/heigit_bgd_roadsurface_lines.gpkg"
GEOB_API = "https://www.geoboundaries.org/api/current/gbOpen/BGD/{level}"

ROAD_COLUMNS = [
    "highway",
    "surface",
    "smoothness",
    "osm_surface_class",
    "pred_class",
    "pred_label",
    "combined_surface_osm_priority",
    "combined_surface_DL_priority",
    "osm_length",
    "predicted_length",
    "n_of_predictions_used",
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
    parser.add_argument("--refresh-road", action="store_true", help="Re-download the road GeoPackage.")
    parser.add_argument("--skip-download", action="store_true", help="Fail if the road GeoPackage is missing.")
    parser.add_argument(
        "--min-classified-km",
        type=float,
        default=50.0,
        help="Minimum classified road-surface length for an upazila to receive the road-context score.",
    )
    parser.add_argument(
        "--min-classified-share",
        type=float,
        default=0.10,
        help="Minimum classified share of mapped road length for an upazila to receive the road-context score.",
    )
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def request(url: str) -> bytes:
    req = urllib.request.Request(
        url,
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


def download_road_gpkg(refresh: bool, skip_download: bool) -> None:
    if ROAD_GPKG.exists() and not refresh:
        return
    if skip_download:
        raise FileNotFoundError(f"Missing road GeoPackage: {ROAD_GPKG}")
    ROAD_CACHE.mkdir(parents=True, exist_ok=True)
    tmp = ROAD_GPKG.with_suffix(".gpkg.tmp")
    print(f"Downloading road-surface GeoPackage: {ROAD_URL}", flush=True)
    req = urllib.request.Request(
        ROAD_URL,
        headers={"User-Agent": "ADB-Research-PSDQ/1.0 (local reproducibility script)"},
    )
    with urllib.request.urlopen(req, timeout=900) as response, tmp.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    tmp.replace(ROAD_GPKG)


def normalize_name(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    text = str(value or "").strip().lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"['`.-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in sorted(ALIASES.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    return ALIASES.get(text, text)


def admin_key(district: Any, upazila: Any) -> str:
    key = f"{normalize_name(district)}|{normalize_name(upazila)}"
    return KEY_ALIASES.get(key, key)


def pct(numerator: float, denominator: float, digits: int = 4) -> float | None:
    if not denominator:
        return None
    return round(numerator / denominator, digits)


def finite(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(number):
        return 0.0
    return number


def round_km(value_m: float) -> float:
    return round(value_m / 1000.0, 3)


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


def load_admin3() -> gpd.GeoDataFrame:
    ensure_geoboundary("ADM1", ADM1_GEOJSON)
    ensure_geoboundary("ADM2", ADM2_GEOJSON)
    ensure_geoboundary("ADM3", ADM3_GEOJSON)

    adm1 = gpd.read_file(ADM1_GEOJSON, engine="pyogrio")[["shapeName", "geometry"]].rename(
        columns={"shapeName": "division_name"}
    )
    adm2 = gpd.read_file(ADM2_GEOJSON, engine="pyogrio")[["shapeName", "geometry"]].rename(
        columns={"shapeName": "district_name"}
    )
    adm3 = gpd.read_file(ADM3_GEOJSON, engine="pyogrio")[["shapeName", "shapeID", "geometry"]].rename(
        columns={"shapeName": "upazila_name", "shapeID": "shape_id"}
    )

    adm3_points = adm3[["upazila_name", "shape_id", "geometry"]].copy()
    adm3_points["geometry"] = adm3_points.geometry.representative_point()
    adm3_points = gpd.sjoin(adm3_points, adm2, how="left", predicate="within").drop(columns=["index_right"])
    adm3_points = gpd.sjoin(adm3_points, adm1, how="left", predicate="within").drop(columns=["index_right"])

    attrs = pd.DataFrame(adm3_points.drop(columns="geometry"))
    admin = adm3.merge(attrs, on=["upazila_name", "shape_id"], how="left")
    admin[["division_name", "district_name", "upazila_name", "shape_id"]] = admin[
        ["division_name", "district_name", "upazila_name", "shape_id"]
    ].fillna("")
    admin["join_key"] = admin.apply(lambda row: admin_key(row["district_name"], row["upazila_name"]), axis=1)
    return admin[["division_name", "district_name", "upazila_name", "shape_id", "join_key", "geometry"]]


def load_roads() -> gpd.GeoDataFrame:
    print(f"Reading road GeoPackage: {ROAD_GPKG}", flush=True)
    roads = pyogrio.read_dataframe(ROAD_GPKG, columns=ROAD_COLUMNS)
    roads = gpd.GeoDataFrame(roads, geometry="geometry", crs="EPSG:4326")
    roads["length_m"] = pd.to_numeric(roads["osm_length"], errors="coerce").fillna(0.0)
    roads.loc[roads["length_m"] < 0, "length_m"] = 0.0
    roads["surface_class"] = roads["combined_surface_DL_priority"].fillna(roads["combined_surface_osm_priority"])
    roads["surface_class"] = roads["surface_class"].where(roads["surface_class"].isin(["paved", "unpaved"]))
    roads["has_osm_surface_class"] = roads["osm_surface_class"].isin(["paved", "unpaved"])
    roads["has_ml_surface_class"] = roads["pred_class"].isin(["paved", "unpaved"])
    return roads


def assign_roads_to_admin(roads: gpd.GeoDataFrame, admin: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    print("Assigning road-segment representative points to ADM3 polygons", flush=True)
    road_points = roads.copy()
    road_points["geometry"] = road_points.geometry.representative_point()
    joined = gpd.sjoin(
        road_points,
        admin[["division_name", "district_name", "upazila_name", "shape_id", "join_key", "geometry"]],
        how="left",
        predicate="within",
    )
    if "index_right" in joined:
        joined = joined.drop(columns=["index_right"])
    return joined


def aggregate_roads(joined: gpd.GeoDataFrame, admin: gpd.GeoDataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    assigned = joined[joined["join_key"].notna()].copy()
    assigned["classified_length_m"] = assigned["length_m"].where(assigned["surface_class"].notna(), 0.0)
    assigned["paved_length_m"] = assigned["length_m"].where(assigned["surface_class"].eq("paved"), 0.0)
    assigned["unpaved_length_m"] = assigned["length_m"].where(assigned["surface_class"].eq("unpaved"), 0.0)
    assigned["osm_surface_length_m"] = assigned["length_m"].where(assigned["has_osm_surface_class"], 0.0)
    assigned["ml_surface_length_m"] = assigned["length_m"].where(assigned["has_ml_surface_class"], 0.0)
    assigned["length_present"] = assigned["length_m"] > 0
    assigned["surface_present"] = assigned["surface_class"].notna()

    group_cols = ["division_name", "district_name", "upazila_name", "shape_id", "join_key"]
    grouped = (
        assigned.groupby(group_cols, dropna=False)
        .agg(
            road_segments=("length_m", "size"),
            road_segments_with_length=("length_present", "sum"),
            road_segments_with_surface=("surface_present", "sum"),
            total_road_m=("length_m", "sum"),
            classified_surface_m=("classified_length_m", "sum"),
            paved_m=("paved_length_m", "sum"),
            unpaved_m=("unpaved_length_m", "sum"),
            osm_surface_m=("osm_surface_length_m", "sum"),
            ml_surface_m=("ml_surface_length_m", "sum"),
        )
        .reset_index()
    )

    rows_by_key = {row["join_key"]: row for row in grouped.to_dict(orient="records")}
    output_rows: list[dict[str, Any]] = []
    for admin_row in admin.drop(columns="geometry").to_dict(orient="records"):
        row = rows_by_key.get(admin_row["join_key"], {})
        total_m = finite(row.get("total_road_m"))
        classified_m = finite(row.get("classified_surface_m"))
        paved_m = finite(row.get("paved_m"))
        unpaved_m = finite(row.get("unpaved_m"))
        out = {
            **admin_row,
            "road_segments": int(row.get("road_segments") or 0),
            "road_segments_with_length": int(row.get("road_segments_with_length") or 0),
            "road_segments_with_surface": int(row.get("road_segments_with_surface") or 0),
            "total_road_km": round_km(total_m),
            "classified_surface_km": round_km(classified_m),
            "paved_km": round_km(paved_m),
            "unpaved_km": round_km(unpaved_m),
            "unknown_surface_km": round_km(max(total_m - classified_m, 0.0)),
            "osm_surface_km": round_km(finite(row.get("osm_surface_m"))),
            "ml_surface_km": round_km(finite(row.get("ml_surface_m"))),
            "classified_surface_share": pct(classified_m, total_m),
            "classified_paved_share": pct(paved_m, classified_m),
            "classified_unpaved_share": pct(unpaved_m, classified_m),
        }
        output_rows.append(out)

    total_m = float(assigned["length_m"].sum())
    classified_m = float(assigned["classified_length_m"].sum())
    paved_m = float(assigned["paved_length_m"].sum())
    unpaved_m = float(assigned["unpaved_length_m"].sum())
    stats = {
        "road_features": int(len(joined)),
        "assigned_features": int(joined["join_key"].notna().sum()),
        "unassigned_features": int(joined["join_key"].isna().sum()),
        "features_with_osm_length": int((joined["length_m"] > 0).sum()),
        "features_missing_osm_length": int((joined["length_m"] <= 0).sum()),
        "surface_classified_features": int(joined["surface_class"].notna().sum()),
        "total_road_km": round_km(total_m),
        "classified_surface_km": round_km(classified_m),
        "paved_km": round_km(paved_m),
        "unpaved_km": round_km(unpaved_m),
        "unknown_surface_km": round_km(max(total_m - classified_m, 0.0)),
        "classified_surface_share": pct(classified_m, total_m),
        "classified_paved_share": pct(paved_m, classified_m),
        "classified_unpaved_share": pct(unpaved_m, classified_m),
    }
    return output_rows, stats


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_exposure_rows() -> list[dict[str, Any]]:
    if not EXPOSURE_CSV.exists():
        return []
    with EXPOSURE_CSV.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def join_exposure_context(
    exposure_rows: list[dict[str, Any]],
    road_rows: list[dict[str, Any]],
    min_classified_km: float,
    min_classified_share: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    roads_by_key = {row["join_key"]: row for row in road_rows}
    joined: list[dict[str, Any]] = []
    for row in exposure_rows:
        road = roads_by_key.get(row.get("join_key", ""))
        out = dict(row)
        if road:
            for key in [
                "total_road_km",
                "classified_surface_km",
                "paved_km",
                "unpaved_km",
                "unknown_surface_km",
                "classified_surface_share",
                "classified_paved_share",
                "classified_unpaved_share",
            ]:
                out[key] = road.get(key)
            unpaved_share = finite(road.get("classified_unpaved_share"))
            classified_share = finite(road.get("classified_surface_share"))
            classified_km = finite(road.get("classified_surface_km"))
            proxy = finite(row.get("underobserved_buildings_3km_p85_proxy"))
            eligible = classified_km >= min_classified_km and classified_share >= min_classified_share
            out["has_road_context"] = 1
            out["has_surface_context"] = 1 if eligible else 0
            out["road_context_score"] = round(proxy * (1.0 + unpaved_share)) if eligible else ""
        else:
            for key in [
                "total_road_km",
                "classified_surface_km",
                "paved_km",
                "unpaved_km",
                "unknown_surface_km",
                "classified_surface_share",
                "classified_paved_share",
                "classified_unpaved_share",
            ]:
                out[key] = ""
            out["has_road_context"] = 0
            out["has_surface_context"] = 0
            out["road_context_score"] = ""
        joined.append(out)

    scored = [row for row in joined if str(row.get("road_context_score", "")).strip()]
    scored.sort(key=lambda row: finite(row.get("road_context_score")), reverse=True)

    stats = {
        "exposure_rows": len(exposure_rows),
        "rows_with_road_context": sum(1 for row in joined if int(row.get("has_road_context") or 0)),
        "rows_with_surface_context": sum(1 for row in joined if int(row.get("has_surface_context") or 0)),
        "min_classified_surface_km_for_score": min_classified_km,
        "min_classified_surface_share_for_score": min_classified_share,
        "top_exposure_road_context_upazilas": scored[:15],
    }
    return joined, stats


def compact_top(rows: list[dict[str, Any]], sort_key: str, limit: int = 15) -> list[dict[str, Any]]:
    keep = [
        "division_name",
        "district_name",
        "upazila_name",
        "join_key",
        "total_road_km",
        "classified_surface_km",
        "paved_km",
        "unpaved_km",
        "classified_surface_share",
        "classified_unpaved_share",
    ]
    ranked = sorted(rows, key=lambda row: finite(row.get(sort_key)), reverse=True)[:limit]
    return [{key: row.get(key) for key in keep} for row in ranked]


def write_outputs(
    road_rows: list[dict[str, Any]],
    road_stats: dict[str, Any],
    exposure_rows: list[dict[str, Any]],
    exposure_stats: dict[str, Any],
) -> None:
    write_csv(ROAD_UPAZILA_CSV, road_rows)
    ROAD_SUMMARY_JSON.write_text(
        json.dumps(
            json_ready(
            {
                "generated_at": now_utc(),
                "program": "public-service-data-quality",
                "country": "Bangladesh",
                "unit": "division/district/upazila",
                "source": "HeiGIT Bangladesh Road Surface Data from HDX, derived from OSM road geometries, Mapillary imagery, and deep-learning road-surface classification; geoBoundaries BGD ADM3.",
                "road_source_url": ROAD_URL,
                "method": "Road segments are assigned to geoBoundaries ADM3 polygons using a representative point on each line. Length totals use the dataset osm_length field when present. Surface mix uses combined_surface_DL_priority, which gives a paved/unpaved class when OSM or deep-learning evidence is available. Boundary-crossing segments are not split by polygon, and unclassified road length is kept separate.",
                "stats": road_stats,
                "top_unpaved_km_upazilas": compact_top(road_rows, "unpaved_km"),
                "top_unpaved_share_upazilas": compact_top(
                    [row for row in road_rows if finite(row.get("classified_surface_km")) >= 10],
                    "classified_unpaved_share",
                ),
                "top_total_road_km_upazilas": compact_top(road_rows, "total_road_km"),
                "non_claim": "This layer is a granular road-surface context screen. It does not estimate travel time, road roughness, poverty, or health-care access outcomes without additional validation.",
            }
            ),
            indent=2,
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    if exposure_rows:
        write_csv(EXPOSURE_ROAD_CSV, exposure_rows)
        EXPOSURE_ROAD_JSON.write_text(
            json.dumps(
                json_ready(
                {
                    "generated_at": now_utc(),
                    "program": "public-service-data-quality",
                    "country": "Bangladesh",
                    "unit": "division/district/upazila",
                    "source": "DGHS public facilities + OpenStreetMap health features + Google Open Buildings V3 + HeiGIT/HDX Bangladesh road-surface data + geoBoundaries BGD ADM3.",
                    "method": "The existing PSDQ exposure proxy is joined to upazila road-surface context by normalized district/upazila name. road_context_score equals underobserved 3 km p85 building proxy multiplied by one plus classified unpaved share, only for upazilas with at least the configured classified-surface road length and classified-surface coverage share. It is a prioritization screen, not a causal model.",
                    "stats": {k: v for k, v in exposure_stats.items() if k != "top_exposure_road_context_upazilas"},
                    "top_exposure_road_context_upazilas": exposure_stats["top_exposure_road_context_upazilas"],
                    "non_claim": "The road-context score is for research triage and field-prioritization discussion. It should not be reported as an access, poverty, or service-delivery effect estimate.",
                }
                ),
                indent=2,
                allow_nan=False,
            ),
            encoding="utf-8",
        )


def main() -> None:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    download_road_gpkg(refresh=args.refresh_road, skip_download=args.skip_download)
    admin = load_admin3()
    roads = load_roads()
    joined = assign_roads_to_admin(roads, admin)
    road_rows, road_stats = aggregate_roads(joined, admin)
    exposure_input = read_exposure_rows()
    exposure_rows, exposure_stats = join_exposure_context(
        exposure_input,
        road_rows,
        args.min_classified_km,
        args.min_classified_share,
    )
    write_outputs(road_rows, road_stats, exposure_rows, exposure_stats)
    print(f"Wrote {ROAD_UPAZILA_CSV}", flush=True)
    print(f"Wrote {ROAD_SUMMARY_JSON}", flush=True)
    if exposure_input:
        print(f"Wrote {EXPOSURE_ROAD_CSV}", flush=True)
        print(f"Wrote {EXPOSURE_ROAD_JSON}", flush=True)


if __name__ == "__main__":
    main()
