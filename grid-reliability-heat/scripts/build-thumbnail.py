"""Grid-reliability-heat hero — single-fuel grids.

The honest single-axis story (§6.4 demotion) is that six ADB DMC
grids are functionally single-fuel — Bhutan and Brunei are 100 % on
one source, Mongolia and Kazakhstan ~85–89 % on coal, Nepal 95 %
hydro, Tajikistan 88 % hydro — concentrating supply-side weather and
fuel-market shock exposure. The hero is a horizontal bar of
top-fuel-share for the 10 most-concentrated DMCs, colored by fuel
type.

NOTE: not yet a heat-stress reliability metric (program §STATUS:
requires ERA5 × outage data not yet committed).
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

PROGRAM_SLUG = "grid-reliability-heat"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "grid-reliability-heat-adb-panel.csv"
TOP_N = 10

FUEL_COLOR = {
    "Hydro": "#2563EB",
    "Gas": "#F59E0B",
    "Coal": "#475569",
    "Oil": "#7C2D12",
    "Nuclear": "#9333EA",
    "Solar": "#FACC15",
    "Wind": "#06B6D4",
    "Biomass": "#65A30D",
    "Geothermal": "#DC2626",
    "Other": "#6B7280",
}


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    sub = df[df["top_fuel_share"].notna()].copy()
    sub = sub.sort_values("top_fuel_share", ascending=False).head(TOP_N).iloc[::-1]

    sub["top_fuel"] = sub["top_fuel"].fillna("Other")
    sub["top_fuel_share_pct"] = sub["top_fuel_share"].astype(float) * 100.0

    headline_country = sub.iloc[-1]["country"]
    headline_fuel = sub.iloc[-1]["top_fuel"]
    headline_pct = float(sub.iloc[-1]["top_fuel_share_pct"])
    print(f"Headline: {headline_country} {headline_pct:.0f}% {headline_fuel}")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94, "Six grids: single-fuel capacity concentration",
             fontsize=28, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Installed capacity share (WRI Global Power Plant DB v1.3.0) "
             "of each DMC's largest-fuel fleet. Capacity ≠ generation; "
             "2022–2025 solar buildouts not in this vintage. Structural "
             "single-fuel exposure — not a heat-stressed reliability "
             "measure.",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)
    fig.text(0.96, 0.94, f"{headline_pct:.0f}%",
             fontsize=70, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.85,
             f"of {headline_country}'s grid capacity\n"
             f"is {headline_fuel.lower()}",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.16, 0.13, 0.78, 0.62])
    colors = [FUEL_COLOR.get(f, "#6B7280") for f in sub["top_fuel"]]
    bars = ax.barh(sub["country"], sub["top_fuel_share_pct"],
                   color=colors, edgecolor="white", linewidth=0.8, height=0.72)
    for bar, value, fuel in zip(bars, sub["top_fuel_share_pct"], sub["top_fuel"]):
        ax.annotate(
            f"{value:.0f}% {fuel}",
            xy=(value, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0), textcoords="offset points",
            ha="left", va="center",
            fontsize=10, color=tl.COLOR_INK, fontweight="semibold",
        )
    ax.axvline(85, color=tl.COLOR_INK_SOFT, linestyle="--", linewidth=1, zorder=0)
    ax.text(85, len(sub) - 0.4, "85 % single-fuel threshold",
            fontsize=9, color=tl.COLOR_INK_SOFT, ha="left", va="bottom")
    ax.set_xlim(0, 130)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0 %", "25 %", "50 %", "75 %", "100 %"])
    ax.set_yticks(range(len(sub)))
    ax.set_yticklabels(sub["country"], fontsize=10, color=tl.COLOR_INK)
    ax.tick_params(left=False)
    ax.grid(axis="x", color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)

    tl.draw_footer(
        fig,
        source=(
            "WRI Global Power Plant Database v1.3.0 (capacity, fuel type). "
            "Top-fuel share = largest single fuel's installed-capacity share "
            "of the DMC's plant fleet."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Six grids: single-fuel capacity concentration",
        caption=(
            f"{sub.iloc[-1]['country']} 100 % {sub.iloc[-1]['top_fuel'].lower()} · "
            f"{sub.iloc[-2]['country']} 100 % {sub.iloc[-2]['top_fuel'].lower()} · "
            f"six DMCs above 85 % single-fuel."
        ),
        headline_number=f"{headline_country} {headline_pct:.0f}% {headline_fuel.lower()}",
        source="WRI Global Power Plant DB v1.3.0",
        inputs=["generated/grid-reliability-heat-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="horizontal ranked bar (top 10 by single-fuel share)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
