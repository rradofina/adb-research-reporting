"""Coastal-informal-risk hero — top-5 coastal informal pressure.

The honest single-axis story (§6.4 demotion of composite) is the
stable top-5 set: Pakistan, Philippines, China, Bangladesh, Myanmar.
Visual: Asia-Pacific map highlighting those five, color = slum share
of urban population, marker count = population scale.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "coastal-informal-risk"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "coastal-informal-risk-adb-panel.csv"

CLUSTER = ("PAK", "PHL", "CHN", "BGD", "MMR")


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    cluster_df = df[df["iso3"].isin(CLUSTER)].copy()
    # Rank by slum-urban share (the visual axis), not by population.
    # Mixing two axes — color = slum %, headline = population — confused
    # the prior revision. The visual is now single-axis: slum %.
    cluster_df = cluster_df.sort_values("slum_pct_urban", ascending=False)

    world = tl.load_world(resolution="50m")
    world = tl.make_iso3_col(world)
    ap = world[world["REGION_UN"].isin(["Asia", "Oceania"])].copy()
    cluster_geo = ap[ap["iso3"].isin(CLUSTER)].copy()
    cluster_geo = cluster_geo.merge(
        cluster_df[["iso3", "country", "slum_pct_urban", "urban_pct", "population"]],
        on="iso3", how="left",
    )

    # Headline is now the largest slum-% in the cluster (single axis).
    headline = cluster_df.iloc[0]
    headline_slum = float(headline["slum_pct_urban"])
    print(f"Headline: {headline['country']} {headline_slum:.0f}% slum urban")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94,
             "Coastal-informal pressure concentrates in five economies",
             fontsize=26, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Stable top-5 across the screening sensitivity: Pakistan, "
             "Philippines, China, Bangladesh, Myanmar. Color = slum share "
             "of urban population (WDI EN.POP.SLUM.UR.ZS).",
             fontsize=13, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)

    fig.text(0.96, 0.94, f"{headline_slum:.0f}%",
             fontsize=72, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.83,
             f"of urban dwellers in {headline['country']}\n"
             f"live in informal settlements (WDI)",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.04, 0.10, 0.92, 0.70])
    tl.setup_map_axes(ax)
    ap.plot(ax=ax, color=tl.COLOR_LAND, edgecolor="white", linewidth=0.3, zorder=1)
    norm = mpl.colors.Normalize(
        vmin=cluster_df["slum_pct_urban"].min(),
        vmax=cluster_df["slum_pct_urban"].max(),
    )
    cluster_geo.plot(column="slum_pct_urban", ax=ax,
                     cmap="viridis_r", norm=norm,
                     edgecolor=tl.COLOR_INK, linewidth=0.6, zorder=2)
    offsets = {"PAK": (-30, 25), "PHL": (30, 10), "CHN": (-30, 30),
               "BGD": (-30, -25), "MMR": (-40, -20)}
    for _, row in cluster_geo.iterrows():
        iso = row["iso3"]
        pt = row.geometry.representative_point()
        dx, dy = offsets.get(iso, (15, 15))
        ax.annotate(
            f"{row['country']}\n{row['slum_pct_urban']:.0f}% slum · "
            f"{row['population']/1e6:.0f} M total",
            xy=(pt.x, pt.y), xytext=(dx, dy),
            textcoords="offset points",
            fontsize=10.5, fontweight="semibold", color=tl.COLOR_INK,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=tl.COLOR_INK_SOFT,
                            lw=0.7, shrinkA=4, shrinkB=4),
        )
    ax.set_xlim(60, 145)
    ax.set_ylim(0, 50)

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI EN.POP.SLUM.UR.ZS (slum population, % of urban), "
            "SP.URB.TOTL.IN.ZS (urban %), SP.POP.TOTL (population). "
            "Coastal = country has marine coastline per Natural Earth. "
            "Slum data are sparse and partly imputed."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Coastal-informal pressure concentrates in five economies",
        caption=(
            "Pakistan, Philippines, China, Bangladesh, Myanmar — stable "
            "top-5 by population-scaled informal-urban-pressure proxy."
        ),
        headline_number=f"{headline['country']} {headline_slum:.0f}% slum-share of urban population",
        source="WDI slum / urban / population shares",
        inputs=["generated/coastal-informal-risk-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="Asia-Pacific map (top-5 highlighted, color = slum-urban %)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
