"""Access-services hero — 8-DMC ADM1 climate-adjusted access.

The honest single-axis story (§6.4 demotion of composite) is that
the panel covers 104 ADM1 units across 8 ADB DMCs (PHL, BGD, PAK,
NPL, LKA, KHM, LAO, TLS). The pilot ranks DMC-level worst-ADM1
exposure — Lao PDR has a single ADM1 (Phongsali) where ~76,000
people share each health facility. Visual: horizontal bar of
worst_adm1_people_per_health_facility per DMC.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "access-services"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "access-services-adb-panel.csv"


def _fmt(v: float) -> str:
    if v >= 1e6:
        return f"{v/1e6:.1f} M"
    if v >= 1e3:
        return f"{v/1e3:.0f} k"
    return f"{v:.0f}"


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    df = df[df["worst_adm1_people_per_health_facility"].notna()].copy()
    df = df.sort_values("worst_adm1_people_per_health_facility", ascending=True)
    total_units = int(df["n_adm1_units"].sum())
    total_pop = float(df["total_population"].sum())
    print(f"Panel: {len(df)} DMCs, {total_units} ADM1 units, {total_pop/1e6:.0f}M total pop")

    headline_row = df.iloc[-1]
    headline_country = headline_row["country"]
    headline_value = float(headline_row["worst_adm1_people_per_health_facility"])
    headline_unit = headline_row["worst_adm1_name"]
    print(f"Headline: {headline_country} ({headline_unit}) {headline_value:,.0f} people / health facility")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94,
             "Worst-ADM1 OSM-tagged-facility coverage, eight DMC pilot",
             fontsize=25, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             f"For each pilot DMC, the population per OSM-tagged health "
             f"amenity in its worst-served ADM1 region. "
             f"{total_units} ADM1 units, {total_pop/1e6:.0f} M people in panel. "
             f"OSM tag coverage under-counts the official health "
             f"registry by 5–10× per the PSDQ program — read these as "
             f"OSM-coverage gaps, not facility counts.",
             fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)
    fig.text(0.96, 0.94, _fmt(headline_value),
             fontsize=64, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.85,
             f"people per OSM-tagged health amenity\n"
             f"in {headline_unit}, {headline_country}",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.20, 0.13, 0.74, 0.62])
    cmap = plt.get_cmap("viridis_r")
    vmax = float(df["worst_adm1_people_per_health_facility"].max())
    colors = [cmap(0.15 + 0.75 * v / vmax)
              for v in df["worst_adm1_people_per_health_facility"]]
    bars = ax.barh(df["country"], df["worst_adm1_people_per_health_facility"],
                   color=colors, edgecolor="white", linewidth=0.8, height=0.72)
    for bar, val, name in zip(bars, df["worst_adm1_people_per_health_facility"],
                              df["worst_adm1_name"]):
        ax.annotate(
            f"{_fmt(val)} · {name}",
            xy=(val, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0), textcoords="offset points",
            ha="left", va="center",
            fontsize=10, color=tl.COLOR_INK, fontweight="semibold",
        )
    ax.set_xlim(0, vmax * 1.45)
    ax.set_xticks([])
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df["country"], fontsize=10, color=tl.COLOR_INK)
    ax.tick_params(left=False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color(tl.COLOR_INK_SOFT)

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI, geoBoundaries ADM1, WorldPop population, "
            "OpenStreetMap Overpass health-amenities; PSA OpenSTAT, CCKP. "
            "Eight-DMC pilot — pending travel-time-isochrone integration "
            "(§18.5 owner-gated)."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Worst-ADM1 OSM-tagged-facility coverage, eight DMC pilot",
        caption=(
            f"{total_units} ADM1 units across 8 DMCs · ranked by "
            f"population per OSM-tagged health amenity in each DMC's "
            f"worst-served region. Numbers are OSM-coverage gaps, not "
            f"actual facility counts — OSM under-counts the official "
            f"registry by 5–10× per PSDQ."
        ),
        headline_number=f"{headline_unit}, {headline_country} {_fmt(headline_value)} people / OSM-tagged amenity",
        source="WDI + geoBoundaries + WorldPop + OSM Overpass",
        inputs=["generated/access-services-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="horizontal bar (worst-ADM1 OSM-tagged coverage per DMC)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
