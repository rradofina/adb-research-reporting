"""Invisible-urbanization hero — urban growth from rural base.

The honest single-axis story (§6.4 demotion) is: five DMCs sit in the
top of the urban-growth-from-rural-base screen — Papua New Guinea,
Solomon Islands, Afghanistan, Lao PDR, Bangladesh. Visual: slope
chart showing urban % start vs urban % growth, with the five
highlighted.
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

PROGRAM_SLUG = "invisible-urbanization"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "invisible-urbanization-adb-panel.csv"

CLUSTER = ("PNG", "SLB", "AFG", "LAO", "BGD")


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    df = df[df["urban_pct"].notna() & df["urban_pop_growth_pct"].notna()].copy()
    print(f"Panel: {len(df)} DMCs")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94, "Urban growth from a rural base",
             fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Five DMCs sit where urban share is still low (<40 %) and "
             "urban-population growth is fast (>2.5 %/yr) — the cities "
             "GHSL satellite analysis would expect to be expanding "
             "fastest. Signal is co-produced by REAL growth AND "
             "delayed statistical reclassification of rural settlements "
             "as urban; the two are not separable here. GHSL BUILT-S "
             "validation deferred.",
             fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)

    cluster_df = df[df["iso3"].isin(CLUSTER)].copy()
    headline = cluster_df.sort_values("urban_pop_growth_pct", ascending=False).iloc[0]
    print(f"Headline: {headline['country']} urban {headline['urban_pct']:.0f}% growing "
          f"{headline['urban_pop_growth_pct']:.1f}%/yr")
    fig.text(0.96, 0.94, f"{headline['urban_pop_growth_pct']:.1f}%",
             fontsize=68, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.84,
             f"annual urban growth in {headline['country']}\n"
             f"urban share still only {headline['urban_pct']:.0f}%",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.07, 0.13, 0.87, 0.62])
    # Background scatter
    others = df[~df["iso3"].isin(CLUSTER)]
    ax.scatter(others["urban_pct"], others["urban_pop_growth_pct"],
               s=60, color=tl.COLOR_INK_SOFT, alpha=0.5,
               edgecolor="white", linewidth=0.5, zorder=2)
    high = df[df["iso3"].isin(CLUSTER)]
    ax.scatter(high["urban_pct"], high["urban_pop_growth_pct"],
               s=200, color="#3a5a4c",
               edgecolor="white", linewidth=1.2, zorder=3)
    for _, r in high.iterrows():
        ax.annotate(
            f"{r['country']}\n{r['urban_pct']:.0f}% urban · "
            f"{r['urban_pop_growth_pct']:.1f}%/yr",
            xy=(r["urban_pct"], r["urban_pop_growth_pct"]),
            xytext=(10, 10), textcoords="offset points",
            fontsize=10, color=tl.COLOR_INK, fontweight="semibold",
        )
    ax.axhline(2.5, color=tl.COLOR_INK_SOFT, linestyle="--", linewidth=1, zorder=1)
    ax.text(95, 2.55, "2.5 %/yr threshold",
            fontsize=9, color=tl.COLOR_INK_SOFT, ha="right", va="bottom")
    ax.axvline(40, color=tl.COLOR_INK_SOFT, linestyle="--", linewidth=1, zorder=1)
    ax.set_xlim(0, 100)
    ax.set_ylim(min(-1, df["urban_pop_growth_pct"].min() - 0.5),
                df["urban_pop_growth_pct"].max() * 1.18)
    ax.set_xlabel("Urban share of population (%)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.set_ylabel("Annual urban population growth (%)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.grid(color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI SP.URB.TOTL.IN.ZS (urban share) and "
            "SP.URB.GROW (urban population growth, %). Latest available "
            "year. Pending: GHSL built-up-surface validation."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Urban growth from a rural base",
        caption=(
            "Papua New Guinea, Solomon Islands, Afghanistan, Lao PDR, "
            "Bangladesh — low urban share + fast urban growth, the cities "
            "satellite imagery would expect to see expanding fastest."
        ),
        headline_number=f"{headline['country']} {headline['urban_pop_growth_pct']:.1f}%/yr urban growth",
        source="WDI urban share + urban growth",
        inputs=["generated/invisible-urbanization-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="two-axis scatter (urban % × urban growth %)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
