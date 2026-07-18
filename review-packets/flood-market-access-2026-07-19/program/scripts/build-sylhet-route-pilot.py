"""Build a routed flood-to-market access pilot for Sylhet, Bangladesh.

Constitution references: sections 2.1, 2.2, 6.1, 6.3, 6.6, 7.2,
11, 13.3, 14, 15, and 18. attestation_chain: ai-first.

The script replaces the program's national proxy with the smallest public
object that actually contains roads, markets, population, and observed flood
water. It combines:

* UNOSAT product 3888, SAOCOM-1A flood extent for 26 June 2024;
* an OpenStreetMap historical Overpass snapshot for 25 June 2024;
* WorldPop 2020 unconstrained population at approximately 100 metres.

Raw files are cached under ``.cache/flood-market-access-sylhet-2024`` and are
not committed. Derived tables and a source/checksum record are committed under
``flood-market-access/generated``.

This is a construct-validation pilot. It estimates routes to OSM-mapped
marketplaces under the mechanical counterfactual that every road segment
intersecting satellite-detected flood water is unavailable. It does not claim
observed road closure, actual market choice, vehicle speeds, welfare effects,
or population displacement.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import time
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from scipy.spatial import cKDTree
from shapely import STRtree
from shapely.geometry import LineString, Point, mapping
from shapely.ops import transform, unary_union
from pyproj import Transformer


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
OUT = PROGRAM / "generated"
CACHE = ROOT / ".cache" / "flood-market-access-sylhet-2024"

UNOSAT_PRODUCT = "https://unosat.org/our_products/3888"
UNOSAT_ZIP = "https://unosat.org/static/unosat_filesystem/3888/TC20240502BGD_SHP.zip"
WORLDPOP_URL = (
    "https://data.worldpop.org/GIS/Population/Global_2000_2020/2020/BGD/"
    "bgd_ppp_2020.tif"
)
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_DATE = "2024-06-25T00:00:00Z"

# Bounds come from the UNOSAT analysis-extent polygon, not a hand-drawn box.
SOUTH, WEST, NORTH, EAST = (
    24.846298886,
    91.661870200,
    25.022810757,
    91.898510143,
)

OVERPASS_QUERY = f"""[out:json][timeout:240][date:\"{OVERPASS_DATE}\"];
(
  way[\"highway\"]({SOUTH},{WEST},{NORTH},{EAST});
  nwr[\"amenity\"=\"marketplace\"]({SOUTH},{WEST},{NORTH},{EAST});
);
(._;>;);
out body;
"""

UNOSAT_FOLDER = "TC20240502BGD_SHP"
ANALYSIS_SHP = "SAOCOM_20240626_AnalysisExtent_Sylhet_1.shp"
FLOOD_SHP = "SAOCOM_20240626_FloodExtent_Sylhet.shp"
UNOSAT_ROAD_SHP = "SAOCOM_20240626_PotentiallyAffectedRoad_Sylhet.shp"

CORE_HIGHWAYS = {
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "unclassified",
    "residential",
    "living_street",
}
BROAD_HIGHWAYS = CORE_HIGHWAYS | {"service", "track"}
ROAD_SETS = {"core": CORE_HIGHWAYS, "broad": BROAD_HIGHWAYS}

DEFAULT_SPEED_KPH = {
    "motorway": 80,
    "trunk": 60,
    "primary": 50,
    "secondary": 40,
    "tertiary": 30,
    "unclassified": 25,
    "residential": 20,
    "living_street": 10,
    "service": 15,
    "track": 10,
}

FLOOD_BUFFERS_M = [10, 20, 30]  # Base 20 m, ±50%.
POP_SNAP_M = [500, 1000, 1500]  # Base 1 km, ±50%.
MARKET_DEDUP_M = [50, 100, 150]  # Base 100 m, ±50%.
TIME_THRESHOLDS_MIN = [15, 30, 45]  # Base 30 minutes, ±50%.

BASE_PARAMS = {
    "road_set": "core",
    "flood_buffer_m": 20,
    "population_snap_m": 1000,
    "market_dedup_m": 100,
}

USER_AGENT = "ADB-Research-Flood-Market-Access/1.0 (public-data research)"
TO_UTM = Transformer.from_crs(4326, 32646, always_xy=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def retrieve(url: str, path: Path, data: bytes | None = None) -> None:
    if path.exists() and path.stat().st_size:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, application/zip, image/tiff, */*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=360) as response, path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def acquire_sources() -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)

    product_path = CACHE / "unosat-product-3888.json"
    zip_path = CACHE / "TC20240502BGD_SHP.zip"
    worldpop_path = CACHE / "bgd_ppp_2020.tif"
    overpass_path = CACHE / "overpass-sylhet-2024-06-25.json"

    retrieve(UNOSAT_PRODUCT, product_path)
    retrieve(UNOSAT_ZIP, zip_path)
    retrieve(WORLDPOP_URL, worldpop_path)
    retrieve(
        OVERPASS_URL,
        overpass_path,
        urllib.parse.urlencode({"data": OVERPASS_QUERY}).encode("utf-8"),
    )

    extract_dir = CACHE / "shp"
    required = extract_dir / UNOSAT_FOLDER / FLOOD_SHP
    if not required.exists():
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_dir)

    return {
        "product": product_path,
        "unosat_zip": zip_path,
        "worldpop": worldpop_path,
        "overpass": overpass_path,
        "shp_root": extract_dir / UNOSAT_FOLDER,
    }


def parse_maxspeed(value: object, fallback: float) -> float:
    if not value:
        return fallback
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", str(value))
    if not match:
        return fallback
    speed = float(match.group(1))
    if "mph" in str(value).lower():
        speed *= 1.609344
    return min(max(speed, 5.0), 100.0)


def projected_xy(lon: float, lat: float) -> tuple[float, float]:
    return TO_UTM.transform(lon, lat)


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float | None:
    finite = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not finite.any():
        return None
    vals = values[finite]
    wts = weights[finite]
    order = np.argsort(vals)
    vals, wts = vals[order], wts[order]
    cutoff = q * wts.sum()
    return float(vals[np.searchsorted(np.cumsum(wts), cutoff, side="left")])


def market_points(elements: list[dict], node_lookup: dict[int, tuple[float, float]]) -> list[dict]:
    markets = []
    for element in elements:
        tags = element.get("tags") or {}
        if tags.get("amenity") != "marketplace":
            continue
        if element["type"] == "node":
            lon, lat = float(element["lon"]), float(element["lat"])
        elif element["type"] == "way":
            coords = [node_lookup.get(node_id) for node_id in element.get("nodes", [])]
            coords = [coord for coord in coords if coord is not None]
            if len(coords) < 2:
                continue
            geom = LineString(coords)
            centroid = geom.centroid
            lon, lat = centroid.x, centroid.y
        else:
            continue
        x, y = projected_xy(lon, lat)
        markets.append(
            {
                "osm_type": element["type"],
                "osm_id": int(element["id"]),
                "name": tags.get("name") or tags.get("name:en") or "Unnamed marketplace",
                "lon": lon,
                "lat": lat,
                "x": x,
                "y": y,
            }
        )
    return markets


def deduplicate_markets(markets: list[dict], radius_m: float) -> list[dict]:
    if not markets:
        return []
    coords = np.array([[row["x"], row["y"]] for row in markets])
    pairs = cKDTree(coords).query_pairs(radius_m)
    parent = list(range(len(markets)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in pairs:
        union(a, b)

    groups: dict[int, list[dict]] = {}
    for index, market in enumerate(markets):
        groups.setdefault(find(index), []).append(market)

    rows = []
    for group in groups.values():
        rows.append(
            {
                "name": sorted({row["name"] for row in group})[0],
                "names": sorted({row["name"] for row in group}),
                "member_count": len(group),
                "x": float(np.mean([row["x"] for row in group])),
                "y": float(np.mean([row["y"] for row in group])),
                "lon": float(np.mean([row["lon"] for row in group])),
                "lat": float(np.mean([row["lat"] for row in group])),
                "osm_ids": sorted(f"{row['osm_type']}/{row['osm_id']}" for row in group),
            }
        )
    return sorted(rows, key=lambda row: (row["name"], row["lon"], row["lat"]))


def build_graph(
    elements: list[dict],
    node_lookup: dict[int, tuple[float, float]],
    allowed: set[str],
    analysis_geom=None,
) -> tuple[nx.Graph, list[dict]]:
    graph = nx.Graph()
    edge_rows: list[dict] = []
    for way in elements:
        tags = way.get("tags") or {}
        highway = tags.get("highway")
        if way.get("type") != "way" or highway not in allowed:
            continue
        speed_kph = parse_maxspeed(tags.get("maxspeed"), DEFAULT_SPEED_KPH[highway])
        nodes = [node_id for node_id in way.get("nodes", []) if node_id in node_lookup]
        for u, v in zip(nodes[:-1], nodes[1:]):
            if u == v:
                continue
            lon1, lat1 = node_lookup[u]
            lon2, lat2 = node_lookup[v]
            x1, y1 = projected_xy(lon1, lat1)
            x2, y2 = projected_xy(lon2, lat2)
            geometry = LineString([(x1, y1), (x2, y2)])
            if analysis_geom is not None and not analysis_geom.covers(geometry):
                continue
            length_m = math.hypot(x2 - x1, y2 - y1)
            if length_m <= 0:
                continue
            minutes = length_m / (speed_kph * 1000 / 60)
            row = {
                "u": u,
                "v": v,
                "way_id": int(way["id"]),
                "highway": highway,
                "length_m": length_m,
                "minutes": minutes,
                "geometry": geometry,
            }
            edge_rows.append(row)
            graph.add_node(u, lon=lon1, lat=lat1, x=x1, y=y1)
            graph.add_node(v, lon=lon2, lat=lat2, x=x2, y=y2)
            current = graph.get_edge_data(u, v)
            if current is None or minutes < current["minutes"]:
                graph.add_edge(
                    u,
                    v,
                    minutes=minutes,
                    length_m=length_m,
                    highway=highway,
                    way_id=int(way["id"]),
                )
    return graph, edge_rows


def snap_markets(graph: nx.Graph, markets: list[dict], max_distance_m: float = 1000) -> list[dict]:
    node_ids = np.array(list(graph.nodes), dtype=np.int64)
    coords = np.array([[graph.nodes[node]["x"], graph.nodes[node]["y"]] for node in node_ids])
    tree = cKDTree(coords)
    snapped = []
    for market in markets:
        distance, index = tree.query([market["x"], market["y"]])
        if distance <= max_distance_m:
            snapped.append({**market, "node": int(node_ids[index]), "snap_distance_m": float(distance)})
    return snapped


def population_cells(worldpop_path: Path, analysis_geom) -> pd.DataFrame:
    with rasterio.open(worldpop_path) as src:
        clipped, transform_affine = mask(
            src,
            [mapping(analysis_geom)],
            crop=True,
            filled=False,
        )
        data = clipped[0]
        rows, cols = np.where((~data.mask) & np.isfinite(data.data) & (data.data > 0))
        xs, ys = rasterio.transform.xy(transform_affine, rows, cols, offset="center")
        population = data.data[rows, cols].astype(float)
    x, y = TO_UTM.transform(np.asarray(xs), np.asarray(ys))
    return pd.DataFrame(
        {
            "lon": np.asarray(xs),
            "lat": np.asarray(ys),
            "x": np.asarray(x),
            "y": np.asarray(y),
            "population": population,
        }
    )


def snap_population(graph: nx.Graph, cells: pd.DataFrame) -> pd.DataFrame:
    node_ids = np.array(list(graph.nodes), dtype=np.int64)
    coords = np.array([[graph.nodes[node]["x"], graph.nodes[node]["y"]] for node in node_ids])
    distances, indices = cKDTree(coords).query(cells[["x", "y"]].to_numpy())
    result = cells.copy()
    result["node"] = node_ids[indices]
    result["snap_distance_m"] = distances
    return result


def flooded_graph(graph: nx.Graph, edge_rows: list[dict], flood_geom, buffer_m: float):
    flood_zone = flood_geom.buffer(buffer_m)
    edge_geoms = np.array([row["geometry"] for row in edge_rows], dtype=object)
    cut_indices = STRtree(edge_geoms).query(flood_zone, predicate="intersects")
    cut_pairs = {(edge_rows[index]["u"], edge_rows[index]["v"]) for index in cut_indices}
    after = graph.copy()
    after.remove_edges_from(cut_pairs)
    unique_pairs = {tuple(sorted(pair)) for pair in cut_pairs}
    cut_length_m = sum(
        graph.get_edge_data(u, v)["length_m"]
        for u, v in unique_pairs
        if graph.has_edge(u, v)
    )
    return after, flood_zone, unique_pairs, cut_length_m


def multi_source_minutes(graph: nx.Graph, sources: list[int]) -> dict[int, float]:
    unique = sorted(set(sources))
    if not unique:
        return {}
    return nx.multi_source_dijkstra_path_length(graph, unique, weight="minutes")


def prepare_route_state(
    graph: nx.Graph,
    markets: list[dict],
    flood_state: dict,
    market_dedup_m: int,
) -> dict:
    """Compute the expensive network state once per road/buffer/market scenario."""
    deduped = deduplicate_markets(markets, market_dedup_m)
    snapped_markets = snap_markets(graph, deduped)
    for market in snapped_markets:
        market["flooded"] = bool(
            flood_state["flood_zone"].covers(Point(market["x"], market["y"]))
        )
    baseline_sources = [row["node"] for row in snapped_markets]
    functioning_sources = [row["node"] for row in snapped_markets if not row["flooded"]]
    return {
        "deduped": deduped,
        "snapped_markets": snapped_markets,
        "cut_pairs": flood_state["cut_pairs"],
        "cut_length_m": flood_state["cut_length_m"],
        "baseline_minutes": multi_source_minutes(graph, baseline_sources),
        "after_minutes": multi_source_minutes(flood_state["after"], functioning_sources),
        "functioning_sources": functioning_sources,
    }


def run_variant(
    graph: nx.Graph,
    markets: list[dict],
    population: pd.DataFrame,
    route_state: dict,
    road_set: str,
    flood_buffer_m: int,
    population_snap_m: int,
    market_dedup_m: int,
) -> tuple[dict, list[dict]]:
    deduped = route_state["deduped"]
    snapped_markets = route_state["snapped_markets"]
    functioning_sources = route_state["functioning_sources"]
    baseline_minutes = route_state["baseline_minutes"]
    after_minutes = route_state["after_minutes"]

    eligible = population[population["snap_distance_m"] <= population_snap_m].copy()
    eligible["baseline_min"] = eligible["node"].map(baseline_minutes)
    eligible["after_min"] = eligible["node"].map(after_minutes)
    baseline_ok = eligible["baseline_min"].notna()
    after_ok = eligible["after_min"].notna()
    comparable = baseline_ok & after_ok
    disconnected = baseline_ok & ~after_ok

    weights = eligible["population"].to_numpy(float)
    base_values = eligible["baseline_min"].to_numpy(float)
    after_values = eligible["after_min"].to_numpy(float)
    change_values = after_values - base_values
    baseline_population = float(eligible.loc[baseline_ok, "population"].sum())
    disconnected_population = float(eligible.loc[disconnected, "population"].sum())
    comparable_population = float(eligible.loc[comparable, "population"].sum())

    result = {
        "road_set": road_set,
        "flood_buffer_m": flood_buffer_m,
        "population_snap_m": population_snap_m,
        "market_dedup_m": market_dedup_m,
        "graph_nodes": graph.number_of_nodes(),
        "graph_edges": graph.number_of_edges(),
        "cut_edges": len(route_state["cut_pairs"]),
        "cut_edge_length_km": round(route_state["cut_length_m"] / 1000, 3),
        "markets_raw": len(markets),
        "markets_deduplicated": len(deduped),
        "markets_snapped": len(snapped_markets),
        "markets_flooded": sum(row["flooded"] for row in snapped_markets),
        "markets_functioning": len(functioning_sources),
        "population_in_analysis_extent": round(float(population["population"].sum()), 3),
        "population_within_snap_distance": round(float(eligible["population"].sum()), 3),
        "baseline_accessible_population": round(baseline_population, 3),
        "post_flood_accessible_population": round(float(eligible.loc[after_ok, "population"].sum()), 3),
        "disconnected_population": round(disconnected_population, 3),
        "disconnected_share_pct": round(
            100 * disconnected_population / baseline_population if baseline_population else 0,
            3,
        ),
        "comparable_population": round(comparable_population, 3),
        "baseline_weighted_median_minutes": None,
        "post_flood_weighted_median_minutes_reachable": None,
        "weighted_median_increase_minutes_reachable": None,
        "weighted_mean_increase_minutes_reachable": None,
    }

    if baseline_ok.any():
        result["baseline_weighted_median_minutes"] = round(
            weighted_quantile(base_values[baseline_ok], weights[baseline_ok], 0.5), 3
        )
    if after_ok.any():
        result["post_flood_weighted_median_minutes_reachable"] = round(
            weighted_quantile(after_values[after_ok], weights[after_ok], 0.5), 3
        )
    if comparable.any():
        median_change = weighted_quantile(change_values[comparable], weights[comparable], 0.5)
        result["weighted_median_increase_minutes_reachable"] = round(median_change, 3)
        result["weighted_mean_increase_minutes_reachable"] = round(
            float(np.average(change_values[comparable], weights=weights[comparable])), 3
        )
        for threshold in TIME_THRESHOLDS_MIN:
            population_over = float(
                eligible.loc[comparable & (eligible["after_min"] - eligible["baseline_min"] >= threshold), "population"].sum()
            )
            result[f"population_with_increase_ge_{threshold}m"] = round(population_over, 3)
            result[f"share_comparable_with_increase_ge_{threshold}m_pct"] = round(
                100 * population_over / comparable_population if comparable_population else 0,
                3,
            )

    market_rows = [
        {
            "road_set": road_set,
            "flood_buffer_m": flood_buffer_m,
            "market_dedup_m": market_dedup_m,
            **market,
        }
        for market in snapped_markets
    ]
    return result, market_rows


def main() -> None:
    started = time.perf_counter()
    CACHE.mkdir(parents=True, exist_ok=True)
    progress_log = CACHE / "route-pilot-progress.log"
    progress_log.write_text("", encoding="utf-8")

    def progress(message: str) -> None:
        line = f"[{time.perf_counter() - started:7.1f}s] {message}"
        print(line, flush=True)
        with progress_log.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    OUT.mkdir(parents=True, exist_ok=True)
    progress("acquiring cached public sources")
    paths = acquire_sources()

    product = json.loads(paths["product"].read_text(encoding="utf-8"))["map_event"]
    osm = json.loads(paths["overpass"].read_text(encoding="utf-8"))
    elements = osm["elements"]
    nodes = {
        int(element["id"]): (float(element["lon"]), float(element["lat"]))
        for element in elements
        if element.get("type") == "node" and "lon" in element and "lat" in element
    }
    markets = market_points(elements, nodes)
    progress(f"parsed OSM: {len(nodes):,} nodes; {len(markets)} raw markets")

    shp_root = paths["shp_root"]
    analysis = gpd.read_file(shp_root / ANALYSIS_SHP).to_crs(4326)
    flood = gpd.read_file(shp_root / FLOOD_SHP).to_crs(32646)
    unosat_roads = gpd.read_file(shp_root / UNOSAT_ROAD_SHP).to_crs(32646)
    analysis_geom = unary_union(analysis.geometry)
    flood_geom = unary_union(flood.geometry)
    analysis_utm = transform(TO_UTM.transform, analysis_geom)
    markets_in_query_bbox = len(markets)
    markets = [
        market
        for market in markets
        if analysis_utm.covers(Point(market["x"], market["y"]))
    ]
    progress(
        f"retained {len(markets)} of {markets_in_query_bbox} raw markets inside analysis extent"
    )
    progress("loaded and projected UNOSAT geometries")
    clipped_unosat_roads = gpd.clip(unosat_roads, gpd.GeoSeries([analysis_utm], crs=32646))
    progress("clipped UNOSAT affected-road layer")

    cells = population_cells(paths["worldpop"], analysis_geom)
    progress(f"extracted {len(cells):,} positive WorldPop cells")
    graphs: dict[str, tuple[nx.Graph, list[dict], pd.DataFrame]] = {}
    for road_set, allowed in ROAD_SETS.items():
        progress(f"building {road_set} road graph")
        graph, edge_rows = build_graph(elements, nodes, allowed, analysis_utm)
        snapped_population = snap_population(graph, cells)
        graphs[road_set] = (graph, edge_rows, snapped_population)
        progress(
            f"built {road_set}: {graph.number_of_nodes():,} nodes; "
            f"{graph.number_of_edges():,} edges"
        )

    variants = []
    market_rows = []
    for road_set, (graph, edge_rows, snapped_population) in graphs.items():
        for flood_buffer_m in FLOOD_BUFFERS_M:
            progress(f"cutting {road_set} graph at flood buffer {flood_buffer_m}m")
            after, flood_zone, cut_pairs, cut_length_m = flooded_graph(
                graph, edge_rows, flood_geom, flood_buffer_m
            )
            flood_state = {
                "after": after,
                "flood_zone": flood_zone,
                "cut_pairs": cut_pairs,
                "cut_length_m": cut_length_m,
            }
            for market_dedup_m in MARKET_DEDUP_M:
                progress(
                    f"routing {road_set}; flood buffer {flood_buffer_m}m; "
                    f"market dedup {market_dedup_m}m"
                )
                route_state = prepare_route_state(
                    graph,
                    markets,
                    flood_state,
                    market_dedup_m,
                )
                for population_snap_m in POP_SNAP_M:
                    result, snapped = run_variant(
                        graph,
                        markets,
                        snapped_population,
                        route_state,
                        road_set,
                        flood_buffer_m,
                        population_snap_m,
                        market_dedup_m,
                    )
                    variants.append(result)
                    market_rows.extend(snapped)
    progress(f"completed {len(variants)} sensitivity variants")

    base = next(
        row
        for row in variants
        if all(row[key] == value for key, value in BASE_PARAMS.items())
    )
    disconnected_shares = [row["disconnected_share_pct"] for row in variants]
    cut_lengths = [row["cut_edge_length_km"] for row in variants]
    headline = {
        "base_disconnected_population": base["disconnected_population"],
        "base_disconnected_share_pct": base["disconnected_share_pct"],
        "base_cut_edge_length_km": base["cut_edge_length_km"],
        "base_markets_functioning": base["markets_functioning"],
        "base_markets_snapped": base["markets_snapped"],
        "base_population_coverage_pct": round(
            100
            * base["population_within_snap_distance"]
            / base["population_in_analysis_extent"],
            3,
        ),
        "sensitivity_disconnected_share_min_pct": min(disconnected_shares),
        "sensitivity_disconnected_share_max_pct": max(disconnected_shares),
        "sensitivity_cut_edge_length_min_km": min(cut_lengths),
        "sensitivity_cut_edge_length_max_km": max(cut_lengths),
        "all_variants_positive_disconnection": all(value > 0 for value in disconnected_shares),
        "variant_count": len(variants),
    }

    source_records = []
    for role, url, path in [
        ("unosat_product_metadata", UNOSAT_PRODUCT, paths["product"]),
        ("observed_flood_vector_bundle", UNOSAT_ZIP, paths["unosat_zip"]),
        ("historical_osm_query", OVERPASS_URL, paths["overpass"]),
        ("population_raster", WORLDPOP_URL, paths["worldpop"]),
    ]:
        source_records.append(
            {
                "role": role,
                "url": url,
                "local_cache_name": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "retrieved_on": "2026-07-19",
            }
        )

    payload = {
        "program": "flood-market-access",
        "analysis": "Sylhet 2024 observed-flood routed-market-access construct validation",
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "claim_scope": (
            "Population-weighted model of access to OSM-mapped marketplaces within the UNOSAT "
            "analysis extent under a mechanical all-intersecting-road-segments-unavailable counterfactual. "
            "Not observed closure, actual market choice, welfare loss, or a Bangladesh-wide estimate."
        ),
        "event": {
            "unosat_product_id": product["id"],
            "title": product["title"],
            "event_code": product["glide"],
            "image_date": "2024-06-26T11:45:00Z",
            "analysis_extent_km2": round(float(analysis.to_crs(32646).area.sum() / 1e6), 3),
            "satellite_detected_flood_km2": round(float(flood.area.sum() / 1e6), 3),
            "unosat_potentially_affected_road_km_clipped": round(
                float(clipped_unosat_roads.length.sum() / 1000), 3
            ),
            "field_validation": "not yet field validated",
        },
        "sources": source_records,
        "overpass": {
            "endpoint": OVERPASS_URL,
            "snapshot_date": OVERPASS_DATE,
            "query": OVERPASS_QUERY,
            "osm_base_reported_by_endpoint": osm.get("osm3s", {}).get("timestamp_osm_base"),
            "element_count": len(elements),
            "element_types": dict(Counter(element["type"] for element in elements)),
            "raw_market_objects_in_query_bbox": markets_in_query_bbox,
            "raw_market_objects_in_analysis_extent": len(markets),
        },
        "method": {
            "road_sets": {key: sorted(value) for key, value in ROAD_SETS.items()},
            "speeds_kph": DEFAULT_SPEED_KPH,
            "baseline": BASE_PARAMS,
            "sensitivity": {
                "flood_buffer_m": FLOOD_BUFFERS_M,
                "population_snap_m": POP_SNAP_M,
                "market_dedup_m": MARKET_DEDUP_M,
                "road_set": list(ROAD_SETS),
                "variant_count": len(variants),
                "numeric_parameters_tested_at_plus_minus_50_pct": True,
            },
            "non_claims": [
                "All road segments intersecting flood water are modeled unavailable; closure is not observed.",
                "OSM marketplaces proxy destinations; actual household or trader market choice is unknown.",
                "Road speeds are class defaults or parsed OSM maxspeed values; no traffic or boat travel is modeled.",
                "WorldPop 2020 predates the 2024 event and is an unconstrained modeled population surface.",
                "One-way rules, turn penalties, bridge passability, elevation, road surface, and flood depth are omitted.",
            ],
        },
        "headline": headline,
        "base_result": base,
        "variants": variants,
    }

    sensitivity_payload = {
        "program": "flood-market-access",
        "analysis": "Sylhet 2024 routed-market-access sensitivity grid",
        "metric": "share of baseline-accessible covered population disconnected by the mechanical flood-edge cut",
        "attestation_chain": "ai-first",
        "generated_at": payload["generated_at"],
        "baseline": BASE_PARAMS,
        "parameter_grid": payload["method"]["sensitivity"],
        "headline": headline,
        "claim_scope": payload["claim_scope"],
        "runs": variants,
    }

    json_path = OUT / "flood-sylhet-route-pilot.json"
    variants_path = OUT / "flood-sylhet-route-sensitivity.csv"
    markets_path = OUT / "flood-sylhet-markets.csv"
    sensitivity_runs_path = ROOT / "flood-market-access" / "sensitivity-runs.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sensitivity_runs_path.write_text(
        json.dumps(sensitivity_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    pd.DataFrame(variants).to_csv(variants_path, index=False, quoting=csv.QUOTE_MINIMAL)
    market_df = pd.DataFrame(market_rows).drop_duplicates(
        subset=["road_set", "flood_buffer_m", "market_dedup_m", "node"]
    )
    market_df.to_csv(markets_path, index=False, quoting=csv.QUOTE_MINIMAL)

    print("=== Sylhet 2024 routed market-access pilot ===")
    print(f"Analysis extent: {payload['event']['analysis_extent_km2']:.1f} km2")
    print(f"Satellite-detected flood: {payload['event']['satellite_detected_flood_km2']:.1f} km2")
    print(
        "Base disconnected population: "
        f"{base['disconnected_population']:,.0f} "
        f"({base['disconnected_share_pct']:.2f}% of baseline-accessible covered population)"
    )
    print(
        "Sensitivity range: "
        f"{headline['sensitivity_disconnected_share_min_pct']:.2f}% to "
        f"{headline['sensitivity_disconnected_share_max_pct']:.2f}% across {len(variants)} variants"
    )
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {variants_path.relative_to(ROOT)}")
    print(f"Wrote {markets_path.relative_to(ROOT)}")
    print(f"Wrote {sensitivity_runs_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
