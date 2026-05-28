"""Water-stress hero thumbnail — withdrawal beyond renewability.

The honest single-axis story (§6.4 demotion of the composite index) is
that a handful of ADB DMCs withdraw more freshwater per year than
their internal renewable resources, with Turkmenistan at 1,868 %
(18.7× its internal resources, transboundary-reliant) — by far the
largest outlier in the panel.

Visual: horizontal ranked bar of top 10 by `water_withdrawal_pct_resources`,
with a vertical dashed line at 100 % (renewable cap). Color =
viridis_r sequential.
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

PROGRAM_SLUG = "water-stress-crop-diversification"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "water-stress-crop-adb-panel.csv"

TOP_N = 10


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    sub = df[df["water_withdrawal_pct_resources"].notna()].copy()
    sub = sub.sort_values("water_withdrawal_pct_resources", ascending=False).head(TOP_N)
    sub = sub.iloc[::-1]  # so largest is at top of horizontal bar

    headline_iso = sub.iloc[-1]["iso3"]
    headline_country = sub.iloc[-1]["country"]
    headline_pct = float(sub.iloc[-1]["water_withdrawal_pct_resources"])
    multiple = headline_pct / 100.0
    print(
        f"Headline: {headline_country} ({headline_iso}) {headline_pct:.0f}% of "
        f"internal renewable water resources ({multiple:.1f}×)"
    )

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)

    fig.text(
        0.04, 0.94,
        "Withdrawals beyond the renewable line",
        fontsize=28, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.88,
        "Annual freshwater withdrawal as % of INTERNAL renewable water "
        "resources. Values above 100 % are not over-pumping per se — "
        "the denominator excludes transboundary river inflows. "
        "Turkmenistan's 1,868 % is driven by Amu Darya inflows; "
        "Pakistan/Uzbekistan/Azerbaijan similarly transboundary-reliant.",
        fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
        wrap=True,
    )

    fig.text(
        0.96, 0.94, f"{multiple:.1f}×",
        fontsize=72, fontweight="bold", color=tl.COLOR_INK,
        ha="right", va="top",
    )
    fig.text(
        0.96, 0.83,
        f"{headline_country} withdraws this many times\n"
        f"its internal renewable water resources",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top",
    )

    ax = fig.add_axes([0.16, 0.13, 0.78, 0.62])
    cmap = plt.get_cmap("viridis_r")
    vmax = float(sub["water_withdrawal_pct_resources"].max())
    colors = [cmap(0.15 + 0.75 * v / vmax)
              for v in sub["water_withdrawal_pct_resources"]]

    bars = ax.barh(
        sub["country"], sub["water_withdrawal_pct_resources"],
        color=colors, edgecolor="white", linewidth=0.8, height=0.72,
    )
    # Value labels at end of each bar
    for bar, value in zip(bars, sub["water_withdrawal_pct_resources"]):
        ax.annotate(
            f"{value:,.0f}%",
            xy=(value, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0), textcoords="offset points",
            ha="left", va="center",
            fontsize=10, color=tl.COLOR_INK,
            fontweight="semibold",
        )

    # 100 % renewable-cap line
    ax.axvline(100, color=tl.COLOR_INK_SOFT, linestyle="--", linewidth=1, zorder=0)
    ax.text(
        100, len(sub) - 0.4, "100 % renewability line",
        fontsize=9, color=tl.COLOR_INK_SOFT, ha="left", va="bottom",
        rotation=0,
    )

    ax.set_xlim(0, vmax * 1.18)
    ax.set_xticks([0, 100, 500, 1000, 1500, 2000])
    ax.set_xticklabels(["0", "100 %", "500 %", "1 000 %", "1 500 %", "2 000 %"])
    ax.tick_params(left=False)
    ax.set_yticklabels(sub["country"], fontsize=10, color=tl.COLOR_INK)
    ax.spines["bottom"].set_color(tl.COLOR_INK_SOFT)
    ax.spines["left"].set_color(tl.COLOR_INK_SOFT)
    ax.grid(axis="x", color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI ER.H2O.FWTL.ZS (annual freshwater withdrawal as % "
            "of internal renewable resources). Latest year per country."
        ),
        program_slug=PROGRAM_SLUG,
    )

    sidecar = tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="Withdrawals beyond the renewable line",
        caption=(
            f"{headline_country} {headline_pct:,.0f}% — Pakistan, "
            f"Uzbekistan, Azerbaijan, Iran each draw beyond 100 % of "
            f"internal renewable water, relying on transboundary rivers."
        ),
        headline_number=f"{headline_country} {multiple:.1f}× internal renewable water resources",
        source="World Bank WDI ER.H2O.FWTL.ZS",
        inputs=["generated/water-stress-crop-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="horizontal ranked bar (top 10 ADB DMCs)",
    )
    plt.close(fig)
    print(f"Wrote {CHARTS / sidecar['files']['png']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
