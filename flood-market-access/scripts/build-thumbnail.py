"""Flood-market-access hero — top-4 stable map.

The honest single-axis story (§6.4 demotion of composite) is the
stable top-4 set across ±50 % sensitivity: India, China, Indonesia,
Afghanistan. Visual: Asia-Pacific map highlighting those four, color
= annual flood events 2000–2025.
"""
from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "flood-market-access"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "flood-market-access-adb-panel.csv"

CLUSTER = ("IND", "CHN", "IDN", "AFG")


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    cluster_df = df[df["iso3"].isin(CLUSTER)].copy()
    cluster_df = cluster_df.sort_values("annual_flood_events", ascending=False)

    world = tl.load_world(resolution="50m")
    world = tl.make_iso3_col(world)
    ap = world[world["REGION_UN"].isin(["Asia", "Oceania"])].copy()
    cluster_geo = ap[ap["iso3"].isin(CLUSTER)].copy()
    cluster_geo = cluster_geo.merge(
        cluster_df[["iso3", "country", "annual_flood_events",
                    "flood_events_2000_2025", "rural_pct"]],
        on="iso3", how="left",
    )

    headline = cluster_df.iloc[0]
    print(f"Headline: {headline['country']} {headline['annual_flood_events']:.1f} flood events/yr")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94, "Four economies absorb the flood-event burden",
             fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Top-4 stable across ±50 % sensitivity: India, China, "
             "Indonesia, Afghanistan. Color = annual flood events 2000–2025 "
             "(EM-DAT). Rural population shares range from 33 % to 74 %.",
             fontsize=13, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)

    fig.text(0.96, 0.94, f"{headline['annual_flood_events']:.1f}/yr",
             fontsize=64, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.85,
             f"flood events per year in {headline['country']}\n"
             f"EM-DAT recorded 2000–2025",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.04, 0.10, 0.92, 0.70])
    tl.setup_map_axes(ax)
    ap.plot(ax=ax, color=tl.COLOR_LAND, edgecolor="white", linewidth=0.3, zorder=1)
    norm = mpl.colors.Normalize(vmin=cluster_df["annual_flood_events"].min(),
                                vmax=cluster_df["annual_flood_events"].max())
    cluster_geo.plot(column="annual_flood_events", ax=ax,
                     cmap="viridis_r", norm=norm,
                     edgecolor=tl.COLOR_INK, linewidth=0.6, zorder=2)

    offsets = {"IND": (-30, -30), "CHN": (-30, 30), "IDN": (30, -20), "AFG": (-30, 20)}
    for _, row in cluster_geo.iterrows():
        iso = row["iso3"]
        pt = row.geometry.representative_point()
        dx, dy = offsets.get(iso, (15, 15))
        ax.annotate(
            f"{row['country']}\n{row['annual_flood_events']:.1f} events/yr "
            f"· {row['rural_pct']:.0f}% rural",
            xy=(pt.x, pt.y), xytext=(dx, dy),
            textcoords="offset points",
            fontsize=10.5, fontweight="semibold", color=tl.COLOR_INK,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=tl.COLOR_INK_SOFT,
                            lw=0.7, shrinkA=4, shrinkB=4),
        )
    ax.set_xlim(40, 160)
    ax.set_ylim(-15, 55)

    tl.draw_footer(
        fig,
        source=(
            "EM-DAT (CRED) flood events 2000–2025; World Bank WDI rural "
            "population share. Natural Earth 1:50m, public domain."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Four economies absorb the flood-event burden",
        caption=(
            f"India {cluster_df.iloc[0]['annual_flood_events']:.1f}/yr · "
            f"China {cluster_df.iloc[1]['annual_flood_events']:.1f}/yr · "
            f"Indonesia {cluster_df.iloc[2]['annual_flood_events']:.1f}/yr · "
            f"Afghanistan {cluster_df.iloc[3]['annual_flood_events']:.1f}/yr "
            f"— stable top-4 across ±50 % sensitivity."
        ),
        headline_number=f"{headline['country']} {headline['annual_flood_events']:.1f} flood events/yr",
        source="EM-DAT 2000–2025 + WDI rural share",
        inputs=["generated/flood-market-access-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="Asia-Pacific map (top-4 highlighted, color = events/yr)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
