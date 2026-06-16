"""Remittance-resilience hero thumbnail — the five-economy cluster.

Per `research/visual-first-refactor.md`, each program produces one
1600x900 hero visual (PNG + SVG + sidecar JSON). For
remittance-resilience the repaired baseline screen highlights five small ADB
DMCs (Kyrgyz Republic, Nepal, Tonga, Vanuatu, Samoa), while the sensitivity
core is narrower after the 2026-06-16 parser repair. Tonga's 42.6 %
remittance share of GDP is the largest in the highlighted set.

The hero visual conveys this with an Asia-Pacific map: the five
cluster economies are shown in color (sequential viridis_r over
remittance/GDP share), the rest of the region is muted neutral grey,
and the one headline number ("42.6 %") sits in the top-right.

Per §6.4, the composite `fragility_index` is NOT the headline number;
the underlying single-axis quantity (remittance / GDP) is.

Inputs (read-only):
  generated/remittance-resilience-adb-panel.csv

Output:
  generated/charts/remittance-resilience-thumbnail.{png,svg,json}
"""

from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from shapely.affinity import translate

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "remittance-resilience"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "remittance-resilience-adb-panel.csv"

# Repaired baseline top-five set. The sensitivity-common set is narrower after
# the 2026-06-16 parser repair, so the thumbnail must not imply all-row
# stability for all five economies.
CLUSTER = ("KGZ", "NPL", "TON", "VUT", "WSM")


def _shift_to_pacific(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Shift Pacific-side geometries (longitude < 0) by +360°.

    The Asia-Pacific map crosses the antimeridian; Samoa, Tonga sit at
    longitudes near -172° and would otherwise render outside the
    extent. Translating their geometries by +360° puts them on the
    Pacific side of the same projection plane.
    """
    gdf = gdf.copy()

    def shift(geom):
        if geom is None:
            return geom
        x_centroid = geom.representative_point().x
        if x_centroid < -30:
            return translate(geom, xoff=360.0)
        return geom

    gdf["geometry"] = gdf.geometry.apply(shift)
    return gdf


def main() -> int:
    if not PANEL_CSV.exists():
        print(f"FATAL: missing {PANEL_CSV}", file=sys.stderr)
        return 1

    df = pd.read_csv(PANEL_CSV)
    cluster_df = df[df["iso3"].isin(CLUSTER)].copy()
    if len(cluster_df) != len(CLUSTER):
        missing = set(CLUSTER) - set(cluster_df["iso3"])
        print(f"FATAL: cluster ISO3 missing from panel: {missing}", file=sys.stderr)
        return 2

    # Rank within cluster, by dependence (not by composite)
    cluster_df = cluster_df.sort_values("wdi_remittance_pct_gdp", ascending=False)
    headline_iso = cluster_df.iloc[0]["iso3"]
    headline_country = cluster_df.iloc[0]["country"]
    headline_pct = float(cluster_df.iloc[0]["wdi_remittance_pct_gdp"])
    print(f"Headline: {headline_country} ({headline_iso}) {headline_pct:.1f}% of GDP")

    # Tajikistan has the largest remittance/GDP share in the entire
    # panel (~48%) but is excluded from the cluster because its RPW
    # corridor-cost coverage is too sparse (1 corridor, 1 firm
    # observed). Surfacing TJK on the map with an "excluded" treatment
    # is more honest than dropping it silently.
    tjk_row = df[df["iso3"] == "TJK"]
    tjk_pct = float(tjk_row["wdi_remittance_pct_gdp"].iloc[0]) if len(tjk_row) else None
    tjk_corridors = int(tjk_row["rpw_corridors_observed"].iloc[0]) if len(tjk_row) else None
    tjk_firms_raw = tjk_row["rpw_firms_observed"].iloc[0] if len(tjk_row) else None
    tjk_firms = int(tjk_firms_raw) if pd.notna(tjk_firms_raw) else 0
    if tjk_pct is not None:
        print(f"TJK excluded: {tjk_pct:.1f}% remittance/GDP, "
              f"only {tjk_corridors} RPW corridor / {tjk_firms} firm(s) observed")

    # Load and prepare basemap
    world = tl.load_world(resolution="50m")
    world = tl.make_iso3_col(world)
    ap = world[world["REGION_UN"].isin(["Asia", "Oceania"])].copy()
    ap = _shift_to_pacific(ap)
    cluster_geo = ap[ap["iso3"].isin(CLUSTER)].copy()
    cluster_geo = cluster_geo.merge(
        cluster_df[["iso3", "wdi_remittance_pct_gdp", "country"]],
        on="iso3", how="left",
    )
    tjk_geo = ap[ap["iso3"] == "TJK"].copy() if tjk_pct is not None else None

    # Figure
    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)

    # Title block
    fig.text(
        0.04, 0.94,
        "Five economies where remittances are the economy",
        fontsize=28, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.875,
        "Repaired baseline top-five; four remain common across the +/-50% suite.\n"
        f"Tajikistan ({tjk_pct:.0f}% of GDP) is largest in the panel but excluded: "
        f"{tjk_corridors} RPW corridor / {tjk_firms} firm. "
        "KGZ has one priced corridor; TON, VUT, and WSM have two each.",
        fontsize=10.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
        linespacing=1.25,
    )

    # Headline number (top-right) — Tonga 42.6 %
    fig.text(
        0.96, 0.94, f"{headline_pct:.1f}%",
        fontsize=72, fontweight="bold", color=tl.COLOR_INK,
        ha="right", va="top",
    )
    fig.text(
        0.96, 0.825, f"of {headline_country}'s GDP\ncomes from remittances",
        fontsize=12, color=tl.COLOR_INK_MUTED,
        ha="right", va="top",
    )

    # Main map axes
    ax = fig.add_axes([0.04, 0.10, 0.92, 0.70])
    tl.setup_map_axes(ax)

    # Asia-Pacific neutral background
    ap.plot(ax=ax, color=tl.COLOR_LAND, edgecolor="white", linewidth=0.3, zorder=1)

    # TJK: high remittance share but excluded — show with hatched fill
    # so the reader sees it on the map, not silently dropped.
    if tjk_geo is not None and not tjk_geo.empty:
        tjk_geo.plot(
            ax=ax,
            facecolor="#FDE68A",
            edgecolor=tl.COLOR_INK_SOFT,
            linewidth=0.6,
            hatch="///",
            zorder=2,
        )

    # Cluster highlight (color = remittance share)
    norm = mpl.colors.Normalize(
        vmin=min(15.0, cluster_df["wdi_remittance_pct_gdp"].min()),
        vmax=max(45.0, cluster_df["wdi_remittance_pct_gdp"].max()),
    )
    cluster_geo.plot(
        column="wdi_remittance_pct_gdp",
        ax=ax, cmap="viridis_r", norm=norm,
        edgecolor=tl.COLOR_INK, linewidth=0.6, zorder=2,
    )

    # Annotate TJK as excluded
    if tjk_geo is not None and not tjk_geo.empty:
        pt = tjk_geo.geometry.representative_point().iloc[0]
        ax.annotate(
            f"Tajikistan\n{tjk_pct:.0f}% — excluded\n"
            f"(only {tjk_corridors} corridor / {tjk_firms} firm in RPW)",
            xy=(pt.x, pt.y), xytext=(-70, -30),
            textcoords="offset points",
            fontsize=9, color=tl.COLOR_INK_MUTED,
            ha="right", va="top", fontstyle="italic",
            arrowprops=dict(arrowstyle="-", color=tl.COLOR_INK_SOFT,
                            lw=0.7, shrinkA=4, shrinkB=4),
        )

    # Country annotations (callouts inside the figure, not legend)
    # Place at the cluster member's representative point. Where the country
    # is tiny (TON/WSM/VUT) the marker is small; we add a leader text.
    annotations = {
        "KGZ": (-30, 30),   # offset in points relative to centroid
        "NPL": (-30, -25),
        "TON": (30, 0),
        "VUT": (40, 30),
        "WSM": (40, -10),
    }
    for _, row in cluster_geo.iterrows():
        iso = row["iso3"]
        country = row["country"]
        share = row["wdi_remittance_pct_gdp"]
        pt = row.geometry.representative_point()
        dx, dy = annotations.get(iso, (20, 20))
        ax.annotate(
            f"{country}\n{share:.1f}%",
            xy=(pt.x, pt.y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=11,
            fontweight="semibold",
            color=tl.COLOR_INK,
            ha="left",
            va="center",
            arrowprops=dict(
                arrowstyle="-", color=tl.COLOR_INK_SOFT, lw=0.7, shrinkA=4, shrinkB=4,
            ),
        )

    # Set extent to cover Asia-Pacific including the shifted Pacific
    ax.set_xlim(50, 200)
    ax.set_ylim(-30, 55)

    # Colorbar (small, inside the figure)
    cax = fig.add_axes([0.06, 0.13, 0.18, 0.012])
    cbar = mpl.colorbar.ColorbarBase(
        cax, cmap=plt.get_cmap("viridis_r"), norm=norm, orientation="horizontal",
    )
    cbar.set_label(
        "Remittance share of GDP (%, WDI latest)",
        fontsize=9, color=tl.COLOR_INK_MUTED,
    )
    cbar.ax.tick_params(labelsize=8, colors=tl.COLOR_INK_MUTED)
    cbar.outline.set_edgecolor(tl.COLOR_INK_SOFT)

    # Footer
    tl.draw_footer(
        fig,
        source=(
            "WDI BX.TRF.PWKR.DT.GD.ZS (remittance share of GDP), World Bank "
            "Remittance Prices Worldwide Q1 2025. Natural Earth 1:50m, public domain."
        ),
        program_slug=PROGRAM_SLUG,
    )

    sidecar = tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="Five economies where remittances are the economy",
        caption=(
            f"{headline_country} {headline_pct:.1f}%, Kyrgyz Republic 26.6%, "
            f"Nepal 26.2%, Samoa 24.0%, Vanuatu 18.8% — all carry remittance "
            f"cost above the SDG 10.c.1 3% reference line in the repaired baseline."
        ),
        headline_number=f"{headline_country} {headline_pct:.1f}% of GDP",
        source="World Bank WDI + Remittance Prices Worldwide Q1 2025",
        inputs=["generated/remittance-resilience-adb-panel.csv"],
        script="remittance-resilience/scripts/build-thumbnail.py",
        visual_form="Asia-Pacific map with five cluster economies highlighted",
    )
    plt.close(fig)

    print("Wrote:")
    for k, v in sidecar["files"].items():
        print(f"  {k}: {CHARTS / v}")
    print(f"  json: {CHARTS / (PROGRAM_SLUG + '-thumbnail.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
