"""Climate-health-workdays hero — outdoor labor × PM2.5 exposure.

The honest single-axis story (§6.4 demotion) is that India is the
single largest population exposed: ~800 million outdoor workers
breathing PM2.5 above the WHO 5 µg/m³ guideline. Afghanistan and
Bangladesh sit on the same Pareto frontier (high PM2.5 × high
outdoor-labor share) but with smaller populations.

Visual: scatter of `outdoor_labor_share_pct` (Y) × `pm25_exposure_ugm3`
(X), point area proportional to `exposed_outdoor_millions`. The four
named DMCs are labeled.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "climate-health-workdays"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "climate-health-workdays-adb-panel.csv"

LABEL_ISO = ["IND", "CHN", "BGD", "AFG", "PAK", "IDN", "PHL", "VNM", "MMR", "NPL"]
# DMCs whose national PM2.5 is monitor-interpolated / imputed (per limitations.md §2).
PM25_IMPUTED = {"AFG", "MMR", "KHM", "LAO", "TLS"}
# DMCs with dramatic within-country PM2.5 variance hidden by national mean.
PM25_LARGE_AREA = {"IND", "CHN", "IDN"}


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    df = df[
        df["outdoor_labor_share_pct"].notna()
        & df["pm25_exposure_ugm3"].notna()
        & df["exposed_outdoor_millions"].notna()
    ].copy()

    headline = df.sort_values("exposed_outdoor_millions", ascending=False).iloc[0]
    print(f"Headline: {headline['country']} {headline['exposed_outdoor_millions']:.0f}M exposed")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94,
             "Outdoor-labor share × annual PM2.5 exposure",
             fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Each circle is an ADB DMC. Bubble area = total population "
             "× outdoor-labor share (agri + industry employment). NOT a "
             "working-age labor-force count. PM2.5 is the WDI national "
             "mean (large within-country variance for IND/CHN/IDN); "
             "AFG, MMR, KHM, LAO, TLS values are monitor-interpolated.",
             fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)
    fig.text(0.96, 0.94, f"{headline['outdoor_labor_share_pct']:.0f}%",
             fontsize=70, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.84,
             f"of {headline['country']}'s employment is outdoor\n"
             f"in air at {headline['pm25_exposure_ugm3']:.0f} µg/m³ "
             f"({headline['pm25_exposure_ugm3']/5:.1f}× the WHO guideline)",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.07, 0.13, 0.86, 0.62])
    # Marker size: area-proportional to exposed_outdoor_millions
    sizes = np.sqrt(df["exposed_outdoor_millions"]) * 65 + 25
    # Color: viridis_r by pm25 exposure
    cmap = plt.get_cmap("viridis_r")
    norm = plt.Normalize(vmin=5.0, vmax=80.0)
    ax.scatter(
        df["pm25_exposure_ugm3"], df["outdoor_labor_share_pct"],
        s=sizes, c=df["pm25_exposure_ugm3"], cmap=cmap, norm=norm,
        edgecolor="white", linewidth=0.8, alpha=0.88, zorder=2,
    )
    # WHO guideline line
    ax.axvline(5.0, color=tl.COLOR_INK_SOFT, linestyle="--", linewidth=1, zorder=1)
    ax.text(5.5, 2, "WHO 5 µg/m³\nannual guideline",
            fontsize=9, color=tl.COLOR_INK_SOFT, ha="left", va="bottom")

    # Label named DMCs; mark imputed PM2.5 with †
    for iso in LABEL_ISO:
        row = df[df["iso3"] == iso]
        if row.empty:
            continue
        r = row.iloc[0]
        marker = "†" if iso in PM25_IMPUTED else ("‡" if iso in PM25_LARGE_AREA else "")
        ax.annotate(
            f"{r['country']}{marker}\n{r['exposed_outdoor_millions']:.0f} M",
            xy=(r["pm25_exposure_ugm3"], r["outdoor_labor_share_pct"]),
            xytext=(8, 8), textcoords="offset points",
            fontsize=9.5, fontweight="semibold",
            color=tl.COLOR_INK,
        )
    # Legend for the marker glyphs
    ax.text(0.02, 0.04, "† PM2.5 imputed (sparse monitors)   "
                       "‡ national mean hides within-country variance",
            transform=ax.transAxes, fontsize=8.5, color=tl.COLOR_INK_SOFT,
            ha="left", va="bottom", fontstyle="italic")

    ax.set_xlim(0, 90)
    ax.set_ylim(0, 95)
    ax.set_xlabel("Annual PM2.5 exposure (µg/m³, latest WDI year)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.set_ylabel("Outdoor-labor share of employment (%, agri + industry)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.grid(color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI EN.ATM.PM25.MC.M3 (PM2.5 annual mean), "
            "SL.AGR.EMPL.ZS + SL.IND.EMPL.ZS (outdoor-labor share), "
            "SP.POP.TOTL (population). Latest available year per indicator."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Outdoor-labor share × annual PM2.5 exposure",
        caption=(
            f"{headline['country']} 55% of employment in agri + industry, "
            f"country-mean PM2.5 at 48 µg/m³ — nearly 10× the WHO "
            f"5 µg/m³ guideline. Bubble area = population × outdoor-"
            f"labor share, NOT a working-age labor-force count."
        ),
        headline_number=f"{headline['country']} {headline['outdoor_labor_share_pct']:.0f}% outdoor employment",
        source="WDI PM2.5 + employment + population",
        inputs=["generated/climate-health-workdays-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="bubble scatter (PM2.5 × outdoor share, area = pop × outdoor share)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
