"""School-heat-disruption hero — Cambodia stands alone (top-1 narrowing).

The honest single-axis story is per program §STATUS: top-5 fails the
±50 % sensitivity gate; only Cambodia survives as a stable top-1 pressure
case (5.3M children, PTR 41.7, historical-period tasmax 31.9 °C). The
hero is therefore a single-country card, not a multi-country
comparison — making the narrowing visually unmistakable.
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

PROGRAM_SLUG = "school-heat-disruption"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "school-heat-adb-panel.csv"


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    khm = df[df["iso3"] == "KHM"].iloc[0]
    children_m = float(khm["children_0_14_millions"])
    ptr = float(khm["primary_pupil_teacher_ratio"])
    tasmax = float(khm["annual_tasmax_1995_2014_celsius"])
    print(f"KHM: {children_m:.1f}M children, PTR {ptr:.1f}, tasmax {tasmax:.1f}°C")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94, "Cambodia: one DMC clears the school-heat gate",
             fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "The top-5 ranking failed ±50 % sensitivity. Only Cambodia "
             "remains as a stable single-economy pressure case under the "
             "screen's three indicators.",
             fontsize=13, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)

    # Three "cards" laid out horizontally — each one metric
    ax_left = fig.add_axes([0.04, 0.10, 0.30, 0.62])
    ax_mid = fig.add_axes([0.36, 0.10, 0.30, 0.62])
    ax_right = fig.add_axes([0.68, 0.10, 0.30, 0.62])
    for ax in (ax_left, ax_mid, ax_right):
        ax.set_facecolor("#F8FAFC")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    def card(ax, big: str, big_unit: str, small: str, footnote: str, color: str):
        ax.text(0.5, 0.70, big, fontsize=72, fontweight="bold",
                color=color, ha="center", va="center",
                transform=ax.transAxes)
        ax.text(0.5, 0.50, big_unit, fontsize=14, color=tl.COLOR_INK_MUTED,
                ha="center", va="center", transform=ax.transAxes)
        ax.text(0.5, 0.32, small, fontsize=13, color=tl.COLOR_INK,
                ha="center", va="center", transform=ax.transAxes,
                fontweight="semibold")
        ax.text(0.5, 0.16, footnote, fontsize=10, color=tl.COLOR_INK_SOFT,
                ha="center", va="center", transform=ax.transAxes,
                style="italic")

    card(ax_left, f"{children_m:.1f}", "million children 0–14",
         f"{children_m:.1f} M",
         "from World Bank WDI population shares",
         "#3a5a4c")
    card(ax_mid, f"{ptr:.1f}", "pupils per primary teacher",
         "PTR (WDI SE.PRM.ENRL.TC.ZS)",
         "highest in the screened ADB DMCs",
         "#7a1c20")
    card(ax_right, f"{tasmax:.1f}", "° C historical-period tasmax",
         "CCKP 1995–2014 baseline",
         "future-period SSP2-4.5 would amplify",
         "#c8893d")

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI (population 0–14 share, SP.POP.0014.TO; primary "
            "pupil-teacher ratio, SE.PRM.ENRL.TC.ZS), CCKP historical tasmax "
            "1995–2014 mean. Sensitivity: top-5 fails ±50 %; KHM is the "
            "single stable case."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Cambodia: one DMC clears the school-heat gate",
        caption=(
            f"Cambodia: {children_m:.1f}M children 0–14, primary PTR "
            f"{ptr:.1f}, historical-period tasmax {tasmax:.1f}°C. Top-5 "
            f"ranking fails ±50 % sensitivity; only Cambodia is stable."
        ),
        headline_number=f"Cambodia {children_m:.1f}M children · PTR {ptr:.1f} · tasmax {tasmax:.1f}°C",
        source="WDI + CCKP historical tasmax",
        inputs=["generated/school-heat-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="single-country triple-card (children, PTR, tasmax)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
