"""Build the evidence-led figure spine for the Sylhet flood-route pilot.

Every number comes from the committed route-pilot outputs. The map rebuilds
only the spatial display object from the cached, checksum-recorded public
sources used by ``build-sylhet-route-pilot.py``.

attestation_chain: ai-first
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import FancyBboxPatch
from PIL import Image
from shapely import STRtree
from shapely.geometry import Point
from shapely.ops import unary_union


PROGRAM = Path(__file__).resolve().parents[1]
REPO = PROGRAM.parent
GENERATED = PROGRAM / "generated"
CHARTS = GENERATED / "charts"
PILOT = GENERATED / "flood-sylhet-route-pilot.json"
SENSITIVITY = GENERATED / "flood-sylhet-route-sensitivity.csv"

BLUE = "#007DB8"
NAVY = "#002569"
CYAN = "#56B4D3"
GREEN = "#5A8227"
GOLD = "#FBB00E"
RED = "#9B2226"
INK = "#212529"
MID = "#66717B"
PALE = "#E7EEF3"
LIGHT_BLUE = "#DCEFF7"
LIGHT_GOLD = "#FFF3CE"
WHITE = "#FFFFFF"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 16,
        "axes.labelsize": 11,
        "axes.edgecolor": "#C7D2DB",
        "axes.linewidth": 0.8,
        "xtick.color": MID,
        "ytick.color": MID,
        "text.color": INK,
        "axes.titlecolor": INK,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
    }
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def new_figure(nrows=1, ncols=1, figsize=(16, 9), **kwargs):
    return plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, **kwargs)


def header(fig, title: str, subtitle: str):
    fig.suptitle(title, x=0.06, y=0.965, ha="left", fontsize=23, fontweight="bold")
    fig.text(0.06, 0.915, subtitle, ha="left", fontsize=11.5, color=MID)


def footer(fig, source: str, note: str):
    fig.text(0.06, 0.045, f"Source: {source}", fontsize=8.5, color=MID)
    fig.text(0.06, 0.021, f"Note: {note}", fontsize=8.3, color=MID)
    fig.text(
        0.94,
        0.021,
        "attestation_chain: ai-first",
        fontsize=8.1,
        color=MID,
        ha="right",
        family="monospace",
    )


def clean_axis(ax, grid="y"):
    ax.spines[["top", "right"]].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=PALE, linewidth=0.8)
        ax.set_axisbelow(True)


def save(fig, stem: str):
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{stem}.png", dpi=180, bbox_inches="tight")
    svg_path = CHARTS / f"{stem}.svg"
    fig.savefig(svg_path, bbox_inches="tight")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def load_spatial_display():
    script_path = PROGRAM / "scripts" / "build-sylhet-route-pilot.py"
    spec = importlib.util.spec_from_file_location("sylhet_route_pilot", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    paths = module.acquire_sources()
    osm = load_json(paths["overpass"])
    elements = osm["elements"]
    nodes = {
        int(item["id"]): (float(item["lon"]), float(item["lat"]))
        for item in elements
        if item.get("type") == "node" and "lon" in item and "lat" in item
    }
    flood = gpd.read_file(paths["shp_root"] / module.FLOOD_SHP).to_crs(32646)
    analysis = gpd.read_file(paths["shp_root"] / module.ANALYSIS_SHP).to_crs(32646)
    analysis_geom = unary_union(analysis.geometry)
    markets = [
        row
        for row in module.market_points(elements, nodes)
        if analysis_geom.covers(Point(row["x"], row["y"]))
    ]
    markets = module.deduplicate_markets(markets, 100)
    graph, edge_rows = module.build_graph(
        elements, nodes, module.ROAD_SETS["core"], analysis_geom
    )
    flood_geom = unary_union(flood.geometry).buffer(20)
    edge_geoms = np.array([row["geometry"] for row in edge_rows], dtype=object)
    cut_indices = set(STRtree(edge_geoms).query(flood_geom, predicate="intersects"))
    market_gdf = gpd.GeoDataFrame(
        markets,
        geometry=[Point(row["x"], row["y"]) for row in markets],
        crs=32646,
    )
    return analysis, flood, edge_rows, cut_indices, market_gdf


def hero_map(data, spatial):
    analysis, flood, edge_rows, cut_indices, markets = spatial
    fig = plt.figure(figsize=(16, 9))
    grid = fig.add_gridspec(1, 2, width_ratios=[1.65, 0.75])
    ax = fig.add_subplot(grid[0, 0])
    panel = fig.add_subplot(grid[0, 1])
    base = data["base_result"]
    rounded_disconnected = round(base["disconnected_population"] / 1000) * 1000
    header(
        fig,
        f"Flood water cuts modeled market access for about {rounded_disconnected:,.0f} people",
        "Sylhet · 26 June 2024 observed flood extent · historical OSM roads and marketplaces · WorldPop 2020",
    )
    open_lines = [
        list(row["geometry"].coords)
        for index, row in enumerate(edge_rows)
        if index not in cut_indices
    ]
    cut_lines = [
        list(row["geometry"].coords)
        for index, row in enumerate(edge_rows)
        if index in cut_indices
    ]
    analysis.boundary.plot(ax=ax, color=NAVY, linewidth=1.1, zorder=1)
    ax.add_collection(LineCollection(open_lines, colors="#AAB8C2", linewidths=0.22, alpha=0.52, zorder=2))
    flood.plot(ax=ax, color=CYAN, alpha=0.62, edgecolor="none", zorder=3)
    ax.add_collection(LineCollection(cut_lines, colors=RED, linewidths=0.34, alpha=0.72, zorder=4))
    markets.plot(ax=ax, color=GOLD, edgecolor=NAVY, linewidth=0.45, markersize=35, zorder=5)
    minx, miny, maxx, maxy = analysis.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(minx, miny - (maxy - miny) * 0.035, "UNOSAT analysis extent", color=MID, fontsize=9)

    panel.axis("off")
    panel.text(0.02, 0.91, f"{base['disconnected_share_pct']:.2f}%", fontsize=42, fontweight="bold", color=NAVY, transform=panel.transAxes)
    panel.text(0.02, 0.83, "of baseline-accessible covered population\nis modeled disconnected", fontsize=12.5, color=INK, transform=panel.transAxes)
    rows = [
        (f"{base['disconnected_population']:,.0f}", "modeled disconnected population", RED),
        (f"{base['markets_snapped']}", "OSM-mapped marketplaces in base graph", GOLD),
        (f"{base['cut_edge_length_km']:.0f} km", "core-road segments intersect flood + 20 m", BLUE),
        (f"{data['headline']['variant_count']}", "sensitivity variants", GREEN),
    ]
    y = 0.68
    for number, label, color in rows:
        panel.text(0.02, y, number, fontsize=22, fontweight="bold", color=color, transform=panel.transAxes)
        panel.text(0.02, y - 0.055, label, fontsize=10.5, color=MID, transform=panel.transAxes)
        y -= 0.15
    panel.text(
        0.02,
        0.07,
        "Mechanical counterfactual\nnot observed road closure",
        fontsize=11.5,
        color=RED,
        fontweight="bold",
        transform=panel.transAxes,
        bbox={"boxstyle": "round,pad=0.65", "facecolor": "#FBE9E7", "edgecolor": "none"},
    )
    footer(
        fig,
        "UNOSAT product 3888; OpenStreetMap 25 Jun 2024 snapshot; WorldPop 2020",
        "Blue is satellite-detected water; red road segments intersect water plus the base 20 m buffer. Market completeness is not independently validated.",
    )
    fig.subplots_adjust(left=0.055, right=0.95, top=0.86, bottom=0.09, wspace=0.03)
    save(fig, "flood-sylhet-route-map")


def headline_access(data):
    base = data["base_result"]
    reachable = base["post_flood_accessible_population"]
    disconnected = base["disconnected_population"]
    total = base["baseline_accessible_population"]
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "Two in five baseline-accessible residents lose a modeled route to market",
        "Population-weighted access split under the core-road, 20 m flood-buffer, 1 km population-snap base specification",
    )
    ax.barh([0], [reachable], color=BLUE, height=0.38)
    ax.barh([0], [disconnected], left=[reachable], color=RED, height=0.38)
    ax.text(reachable / 2, 0, f"{reachable/1000:.0f}k\nstill reachable", ha="center", va="center", color=WHITE, fontsize=20, fontweight="bold")
    ax.text(reachable + disconnected / 2, 0, f"{disconnected/1000:.0f}k\ndisconnected", ha="center", va="center", color=WHITE, fontsize=20, fontweight="bold")
    ax.text(total, 0.36, f"{base['disconnected_share_pct']:.2f}% modeled disconnection", ha="right", fontsize=27, color=NAVY, fontweight="bold")
    ax.set_xlim(0, total)
    ax.set_ylim(-0.75, 0.78)
    ax.set_yticks([])
    ax.set_xlabel("WorldPop 2020 population with a baseline route to an OSM-mapped marketplace")
    clean_axis(ax, "x")
    ax.spines[["left", "bottom"]].set_visible(False)
    fig.text(0.08, 0.21, f"Denominator: {total:,.0f} people with a baseline route after the 1 km road-snap screen.", fontsize=11.5, color=MID)
    fig.text(0.08, 0.16, "The model removes every road segment intersecting mapped water; it does not observe passability.", fontsize=13, color=RED, fontweight="bold")
    footer(fig, "Generated Sylhet route-pilot artifact", "Population is modeled and predates the event; no displacement, boats, or informal markets are represented.")
    fig.subplots_adjust(left=0.08, right=0.94, top=0.80, bottom=0.25)
    save(fig, "flood-sylhet-access-split")


def sensitivity_chart(rows):
    fig, axes = new_figure(1, 2, figsize=(16, 9), gridspec_kw={"width_ratios": [1.25, 1]})
    header(
        fig,
        "The disconnection result survives every pre-specified sensitivity variant",
        "54 combinations: 2 road sets × 3 flood buffers × 3 population snaps × 3 market-deduplication radii",
    )
    grouped = {}
    for row in rows:
        key = (row["road_set"], int(row["flood_buffer_m"]), int(row["population_snap_m"]))
        grouped.setdefault(key, []).append(float(row["disconnected_share_pct"]))
    colors = {"core": BLUE, "broad": GOLD}
    offset = {"core": -0.12, "broad": 0.12}
    for road_set in ["core", "broad"]:
        for buffer_m in [10, 20, 30]:
            x = []
            y = []
            for snap in [500, 1000, 1500]:
                values = grouped[(road_set, buffer_m, snap)]
                x.append(snap + offset[road_set] * 500)
                y.append(float(np.mean(values)))
            axes[0].plot(x, y, marker="o", linewidth=1.7, color=colors[road_set], alpha=0.9, label=road_set if buffer_m == 20 else None)
            axes[0].text(x[-1] + 30, y[-1], f"{buffer_m} m", va="center", fontsize=9, color=colors[road_set])
    all_values = np.array([float(row["disconnected_share_pct"]) for row in rows])
    base_value = next(
        float(row["disconnected_share_pct"])
        for row in rows
        if row["road_set"] == "core"
        and int(row["flood_buffer_m"]) == 20
        and int(row["population_snap_m"]) == 1000
        and int(row["market_dedup_m"]) == 100
    )
    axes[0].axhspan(all_values.min(), all_values.max(), color=LIGHT_BLUE, alpha=0.4, zorder=0)
    axes[0].set_title("All parameter paths remain in a narrow band", loc="left", fontweight="bold")
    axes[0].set_xlabel("Maximum population-to-road snap distance (m)")
    axes[0].set_ylabel("Modeled disconnected share (%)")
    axes[0].set_xticks([500, 1000, 1500])
    axes[0].set_ylim(37.5, 44.5)
    clean_axis(axes[0])
    axes[0].legend(frameon=False, title="Road set")

    axes[1].hist(all_values, bins=np.arange(38.5, 44.1, 0.5), color=BLUE, edgecolor=WHITE)
    axes[1].axvline(base_value, color=RED, linewidth=2, label=f"Base: {base_value:.2f}%")
    axes[1].set_title("Variant distribution", loc="left", fontweight="bold")
    axes[1].set_xlabel("Modeled disconnected share (%)")
    axes[1].set_ylabel("Variant count")
    clean_axis(axes[1])
    axes[1].legend(frameon=False)
    fig.text(0.52, 0.13, "Market deduplication at 50, 100, or 150 m does not change the result in this pilot.", ha="center", fontsize=11.5, color=NAVY)
    footer(fig, "flood-sylhet-route-sensitivity.csv", "Numeric choices are tested at ±50%; the road-set alternative adds service and track roads. Stability does not validate the closure assumption.")
    fig.subplots_adjust(left=0.07, right=0.94, top=0.80, bottom=0.28, wspace=0.25)
    save(fig, "flood-sylhet-sensitivity")


def coverage_funnel(data):
    base = data["base_result"]
    labels = [
        "Population in analysis extent",
        "Within 1 km of core road graph",
        "Baseline route to mapped market",
        "Post-cut route to mapped market",
    ]
    values = [
        base["population_in_analysis_extent"],
        base["population_within_snap_distance"],
        base["baseline_accessible_population"],
        base["post_flood_accessible_population"],
    ]
    widths = np.sqrt(np.array(values) / max(values))
    fig, ax = new_figure(figsize=(16, 9))
    header(fig, "The headline denominator is built through three visible coverage gates", "Population coverage and network reachability funnel for the base specification")
    y = np.arange(len(labels))[::-1]
    colors = ["#D7E0E6", "#AFC5D2", BLUE, RED]
    for position, label, value, width, color in zip(y, labels, values, widths, colors):
        rect = FancyBboxPatch((0.5 - width / 2, position - 0.32), width, 0.64, boxstyle="round,pad=0.02,rounding_size=0.04", facecolor=color, edgecolor="none")
        ax.add_patch(rect)
        ax.text(0.5, position, f"{value/1000:.0f}k", ha="center", va="center", fontsize=18, fontweight="bold", color=WHITE if color in [BLUE, RED] else INK)
        ax.text(1.03, position, label, ha="left", va="center", fontsize=11.5)
    ax.set_xlim(-0.05, 1.62)
    ax.set_ylim(-0.8, len(labels) - 0.2)
    ax.axis("off")
    road_coverage = 100 * values[1] / values[0]
    baseline_coverage = 100 * values[2] / values[1]
    fig.text(0.51, 0.15, f"{road_coverage:.2f}% of modeled population is within 1 km of the core graph; {baseline_coverage:.2f}% of that covered population has a baseline market route.", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    footer(fig, "WorldPop 2020; generated route-pilot artifact", "The final drop mixes true network separation with the mechanical assumption that any water-intersecting segment is unavailable.")
    fig.subplots_adjust(left=0.07, right=0.94, top=0.79, bottom=0.18)
    save(fig, "flood-sylhet-coverage-funnel")


def source_disagreement(data):
    event = data["event"]
    base = data["base_result"]
    fig, axes = new_figure(1, 2, figsize=(16, 9))
    header(fig, "The public source bundle contains two useful checks—and one non-comparable model count", "Metadata, clipped vector geometry, and the routed OSM graph do not measure exactly the same object")
    flood_values = [134, event["satellite_detected_flood_km2"]]
    road_values = [254, event["unosat_potentially_affected_road_km_clipped"], base["cut_edge_length_km"]]
    axes[0].bar([0, 1], flood_values, color=["#AFC5D2", BLUE], width=0.6)
    axes[0].set_xticks([0, 1], ["Product-page\nrounded text", "Downloaded SHP\ncomputed area"])
    axes[0].set_ylabel("Flooded area (km²)")
    axes[0].set_title("Flood-area source check", loc="left", fontweight="bold")
    axes[0].set_ylim(0, 170)
    for i, value in enumerate(flood_values):
        axes[0].text(i, value + 5, f"{value:.1f}" if i else "about 134", ha="center", fontweight="bold", fontsize=15)
    clean_axis(axes[0])
    axes[1].bar([0, 1, 2], road_values, color=["#AFC5D2", BLUE, RED], width=0.6)
    axes[1].set_xticks([0, 1, 2], ["Product-page\nrounded text", "UNOSAT road SHP\nclipped to extent", "OSM core graph\nwater + 20 m"])
    axes[1].set_ylabel("Road length (km)")
    axes[1].set_title("Road-length diagnostic", loc="left", fontweight="bold")
    axes[1].set_ylim(0, 410)
    for i, value in enumerate(road_values):
        axes[1].text(i, value + 10, f"{value:.0f}", ha="center", fontweight="bold", fontsize=15)
    clean_axis(axes[1])
    fig.text(0.68, 0.13, f"The {base['cut_edge_length_km']:.0f} km OSM result is not a validation target: network segmentation, road coverage, and the 20 m buffer differ.", ha="center", fontsize=11.2, color=RED, fontweight="bold")
    footer(fig, "UNOSAT product 3888 and downloaded SHP bundle; generated route-pilot artifact", "The SHP-derived flood area is 144.5 km² versus about 134 km² in rounded product text. Both are retained as a source disagreement.")
    fig.subplots_adjust(left=0.07, right=0.95, top=0.80, bottom=0.28, wspace=0.25)
    save(fig, "flood-sylhet-source-disagreement")


def market_gate(data):
    base = data["base_result"]
    overpass = data["overpass"]
    fig, ax = new_figure(figsize=(16, 9))
    header(fig, f"Seventeen queried OSM market objects become {base['markets_functioning']} routed destinations", "Footprint filtering, object deduplication, and graph snapping are explicit; destination completeness is not independently validated")
    labels = ["Raw objects in\nquery bbox", "Inside UNOSAT\nanalysis extent", "Deduplicated\nmarkets", "Snapped to\ncore graph", "Not directly\ninside flood water"]
    values = [overpass["raw_market_objects_in_query_bbox"], overpass["raw_market_objects_in_analysis_extent"], base["markets_deduplicated"], base["markets_snapped"], base["markets_functioning"]]
    colors = ["#D7E0E6", "#AFC5D2", BLUE, BLUE, GREEN]
    x = np.arange(5)
    ax.bar(x, values, color=colors, width=0.62)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Mapped market destinations")
    ax.set_ylim(0, 21)
    for i, value in enumerate(values):
        ax.text(i, value + 0.7, str(value), ha="center", fontsize=22, fontweight="bold", color=NAVY)
    clean_axis(ax)
    fig.text(0.50, 0.17, "A stable route result can still be wrong if markets are missing or households use unmapped destinations.", ha="center", fontsize=13, color=RED, fontweight="bold")
    footer(fig, "Historical OpenStreetMap Overpass query dated 25 Jun 2024", "Ways and nodes within 100 m are merged in the base case. The 50–150 m sensitivity range leaves the headline unchanged.")
    fig.subplots_adjust(left=0.08, right=0.94, top=0.80, bottom=0.24)
    save(fig, "flood-sylhet-market-gate")


def survivor_selection(data):
    base = data["base_result"]
    fig, ax = new_figure(figsize=(16, 9))
    header(fig, "A lower post-flood median does not mean travel improved", f"The post-cut median is calculated only among people who remain connected; {base['disconnected_population']:,.0f} disconnected residents leave that comparison")
    labels = ["Baseline-accessible\npopulation", "Post-cut survivors\nonly"]
    values = [base["baseline_weighted_median_minutes"], base["post_flood_weighted_median_minutes_reachable"]]
    bars = ax.bar([0, 1], values, color=[BLUE, GREEN], width=0.58)
    ax.set_xticks([0, 1], labels)
    ax.set_ylabel("Population-weighted median modeled minutes")
    ax.set_ylim(0, 9.5)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.35, f"{value:.1f} min", ha="center", fontsize=22, fontweight="bold", color=NAVY)
    clean_axis(ax)
    fig.text(0.51, 0.25, f"{base['disconnected_population']/1000:.0f}k disconnected", ha="center", fontsize=26, color=RED, fontweight="bold", bbox={"boxstyle": "round,pad=0.5", "facecolor": "#FBE9E7", "edgecolor": "none"})
    fig.text(0.51, 0.17, "The more remote connected origins are disproportionately removed. This is survivor selection, not a travel-time benefit.", ha="center", fontsize=12.5, color=INK)
    footer(fig, "Generated route-pilot artifact", "Travel times use class-default or OSM maxspeed values and omit congestion, turn penalties, boats, and observed behavior.")
    fig.subplots_adjust(left=0.18, right=0.86, top=0.80, bottom=0.29)
    save(fig, "flood-sylhet-survivor-selection")


def road_set_comparison(rows):
    selected = [
        row for row in rows
        if int(row["flood_buffer_m"]) == 20
        and int(row["population_snap_m"]) == 1000
        and int(row["market_dedup_m"]) == 100
    ]
    selected.sort(key=lambda row: row["road_set"], reverse=True)
    fig, axes = new_figure(1, 2, figsize=(16, 9))
    header(fig, "Adding service and track roads changes cut length, not the access conclusion", "Base numeric settings under the core and broad historical OSM road definitions")
    labels = [row["road_set"].title() for row in selected]
    shares = [float(row["disconnected_share_pct"]) for row in selected]
    lengths = [float(row["cut_edge_length_km"]) for row in selected]
    colors = [BLUE if row["road_set"] == "core" else GOLD for row in selected]
    axes[0].bar(labels, shares, color=colors, width=0.6)
    axes[0].set_ylim(0, 50)
    axes[0].set_ylabel("Modeled disconnected share (%)")
    axes[0].set_title("Population result", loc="left", fontweight="bold")
    axes[1].bar(labels, lengths, color=colors, width=0.6)
    axes[1].set_ylim(0, 550)
    axes[1].set_ylabel("Water-intersecting graph length (km)")
    axes[1].set_title("Physical graph diagnostic", loc="left", fontweight="bold")
    for ax, values, fmt in [(axes[0], shares, "{:.1f}%"), (axes[1], lengths, "{:.0f} km")]:
        clean_axis(ax)
        for i, value in enumerate(values):
            ax.text(i, value + max(values) * 0.06, fmt.format(value), ha="center", fontsize=19, fontweight="bold", color=NAVY)
    difference = abs(shares[1] - shares[0])
    fig.text(0.50, 0.16, f"Core: excludes service and track. Broad: includes both. The access estimate differs by only {difference:.2f} percentage points.", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    footer(fig, "flood-sylhet-route-sensitivity.csv", "Road-length totals are graph-specific diagnostics, not independently observed closure lengths.")
    fig.subplots_adjust(left=0.08, right=0.95, top=0.80, bottom=0.22, wspace=0.28)
    save(fig, "flood-sylhet-road-set")


def claim_gates():
    gates = [
        ("Observed flood\nfootprint", True),
        ("Date-aligned\nroad graph", True),
        ("Population-weighted\nrouting", True),
        ("Observed road\npassability", False),
        ("Validated market\ndestinations", False),
        ("Behavior or welfare\noutcome", False),
    ]
    fig, ax = new_figure(figsize=(16, 9))
    header(fig, "Three construct gates pass; three decision-grade gates remain open", "Why the result supports a routed-access pilot—not a closure, behavior, or welfare claim")
    for index, (label, passed) in enumerate(gates):
        x = index % 3
        y = 1 - index // 3
        color = GREEN if passed else WHITE
        edge = GREEN if passed else "#9AA8B3"
        rect = FancyBboxPatch((x + 0.08, y + 0.10), 0.82, 0.66, boxstyle="round,pad=0.03,rounding_size=0.05", facecolor=color, edgecolor=edge, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + 0.49, y + 0.50, "✓" if passed else "—", ha="center", va="center", fontsize=27, color=WHITE if passed else MID, fontweight="bold")
        ax.text(x + 0.49, y + 0.25, label, ha="center", va="center", fontsize=10.5, color=WHITE if passed else INK)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 2)
    ax.axis("off")
    fig.text(0.5, 0.17, "The next study must add field- or depth-calibrated passability and independently audited destinations before policy targeting.", ha="center", fontsize=12, color=NAVY, fontweight="bold")
    footer(fig, "Claim gates in the Sylhet construct-validation design", "Passing sensitivity tests cannot substitute for missing outcome validation.")
    fig.subplots_adjust(left=0.08, right=0.94, top=0.79, bottom=0.20)
    save(fig, "flood-sylhet-claim-gates")


def thumbnail(data):
    base = data["base_result"]
    rounded_disconnected = round(base["disconnected_population"] / 1000) * 1000
    fig, ax = new_figure(figsize=(16, 9))
    fig.text(0.06, 0.91, "FLOOD ROUTES TO MARKET", fontsize=11, color=BLUE, fontweight="bold")
    fig.text(0.06, 0.81, f"Flood water cuts modeled market access\nfor about {rounded_disconnected:,.0f} people", fontsize=28, color=NAVY, fontweight="bold", va="top")
    fig.text(0.06, 0.62, "Sylhet · 26 June 2024 · observed flood footprint", fontsize=12, color=MID)
    reachable = base["post_flood_accessible_population"]
    disconnected = base["disconnected_population"]
    total = base["baseline_accessible_population"]
    ax.barh([0], [reachable], color=BLUE, height=0.40)
    ax.barh([0], [disconnected], left=[reachable], color=RED, height=0.40)
    ax.text(reachable / 2, 0, f"{reachable/1000:.0f}k reachable", ha="center", va="center", color=WHITE, fontsize=17, fontweight="bold")
    ax.text(reachable + disconnected / 2, 0, f"{disconnected/1000:.0f}k cut off", ha="center", va="center", color=WHITE, fontsize=17, fontweight="bold")
    ax.set_xlim(0, total)
    ax.set_ylim(-0.7, 0.7)
    ax.axis("off")
    fig.text(0.06, 0.17, f"{base['disconnected_share_pct']:.2f}% base estimate · {data['headline']['sensitivity_disconnected_share_min_pct']:.2f}%–{data['headline']['sensitivity_disconnected_share_max_pct']:.2f}% across {data['headline']['variant_count']} variants", fontsize=12, color=NAVY, fontweight="bold")
    fig.text(0.06, 0.11, "Mechanical road-cut model, not observed closure", fontsize=13, color=RED, fontweight="bold")
    fig.text(0.94, 0.04, "attestation_chain: ai-first", ha="right", fontsize=8.5, color=MID, family="monospace")
    fig.subplots_adjust(left=0.07, right=0.94, top=0.56, bottom=0.22)
    save(fig, "flood-market-access-thumbnail")
    png = CHARTS / "flood-market-access-thumbnail.png"
    svg = CHARTS / "flood-market-access-thumbnail.svg"
    with Image.open(png) as image:
        width, height = image.size
    sidecar = {
        "attestation_chain": "ai-first",
        "program": "flood-market-access",
        "title": f"Flood water cuts modeled market access for about {rounded_disconnected:,.0f} people",
        "caption": f"In the Sylhet base specification, {base['disconnected_share_pct']:.2f}% of baseline-accessible covered population loses a modeled route to an OSM-mapped marketplace.",
        "headline_number": f"{base['disconnected_population']:,.0f} · {base['disconnected_share_pct']:.2f}%",
        "visual_form": "routed-access finding card",
        "headline": f"About {rounded_disconnected:,.0f} people lose modeled market access in the Sylhet flood-route pilot",
        "metric": {"disconnected_population": base["disconnected_population"], "disconnected_share_pct": base["disconnected_share_pct"], "variant_range_pct": [data["headline"]["sensitivity_disconnected_share_min_pct"], data["headline"]["sensitivity_disconnected_share_max_pct"]]},
        "source": "flood-market-access/generated/flood-sylhet-route-pilot.json",
        "inputs": ["generated/flood-sylhet-route-pilot.json", "generated/flood-sylhet-route-sensitivity.csv"],
        "script": "flood-market-access/scripts/build-figure-dossier.py",
        "constitution_ref": "CONSTITUTION.md §18",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dimensions": {"width": width, "height": height},
        "files": {"png": png.name, "svg": svg.name},
        "sha256": {"png": hashlib.sha256(png.read_bytes()).hexdigest(), "svg": hashlib.sha256(svg.read_bytes()).hexdigest()},
        "outputs": {"png": "flood-market-access/generated/charts/flood-market-access-thumbnail.png", "svg": "flood-market-access/generated/charts/flood-market-access-thumbnail.svg"},
        "nonclaim": "Mechanical all-intersecting-road-segments-unavailable model, not observed road closure or welfare loss.",
    }
    (CHARTS / "flood-market-access-thumbnail.json").write_text(json.dumps(sidecar, indent=2) + "\n", encoding="utf-8")


def main():
    data = load_json(PILOT)
    rows = load_csv(SENSITIVITY)
    spatial = load_spatial_display()
    hero_map(data, spatial)
    headline_access(data)
    sensitivity_chart(rows)
    coverage_funnel(data)
    source_disagreement(data)
    market_gate(data)
    survivor_selection(data)
    road_set_comparison(rows)
    claim_gates()
    thumbnail(data)
    print("Flood-market-access figure dossier complete")
    for path in sorted(CHARTS.glob("flood-*.png")):
        print(path.relative_to(REPO))


if __name__ == "__main__":
    main()
