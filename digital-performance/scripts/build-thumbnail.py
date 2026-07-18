"""Build the public hero for the availability–use measurement study.

attestation_chain: ai-first.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
sys.path.insert(0, str(ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402


SLUG = "digital-performance"
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"


def main() -> int:
    panel = pd.read_csv(OUT / "digital-performance-coverage-use-panel.csv")
    summary = json.loads(
        (OUT / "digital-performance-coverage-use-summary.json").read_text(
            encoding="utf-8"
        )
    )
    year = summary["headline_year"]
    headline = panel[panel.year == year].copy()
    median = summary["headline"]["median_gap_pp"]
    selected = headline.nlargest(7, "availability_use_gap_pp").sort_values(
        "availability_use_gap_pp"
    )

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(
        0.045, 0.94, "The network is present. Use still lags.",
        fontsize=29, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.045, 0.865,
        "Reported 4G/LTE availability and recent Internet use are different monitoring objects. "
        "In 2024, the difference is positive in 31 of 34 observed ADB developing member cases.",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="left", va="top", wrap=True,
    )
    fig.text(
        0.955, 0.94, f"{median:.1f}", fontsize=68, fontweight="bold",
        color="#d96c57", ha="right", va="top",
    )
    fig.text(
        0.955, 0.835, "percentage-point\nmedian difference · 2024",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top",
    )

    ax = fig.add_axes([0.10, 0.19, 0.55, 0.53])
    y = np.arange(len(selected))
    ax.barh(y, selected.availability_use_gap_pp, color="#d96c57", height=0.62)
    ax.set_yticks(y, selected.iso3)
    ax.set_xlabel("4G/LTE coverage minus Internet use (percentage points)", color=tl.COLOR_INK_MUTED)
    ax.grid(axis="x", color=tl.COLOR_INK_SOFT, alpha=0.18, linewidth=0.6)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for ypos, value in zip(y, selected.availability_use_gap_pp):
        ax.text(value + 0.8, ypos, f"{value:.1f}", va="center", fontsize=9)

    inset = fig.add_axes([0.73, 0.23, 0.22, 0.38])
    inset.bar(
        ["4G/LTE\ncoverage", "Internet\nuse"],
        [summary["headline"]["median_4g_coverage_pct"], summary["headline"]["median_internet_use_pct"]],
        color=["#d96c57", "#0076a1"], width=0.62,
    )
    inset.set_ylim(0, 105)
    inset.set_title("Observed-sample medians", fontsize=11, fontweight="semibold")
    inset.set_ylabel("Percent", fontsize=9)
    inset.spines[["top", "right", "left"]].set_visible(False)
    inset.grid(axis="y", color=tl.COLOR_INK_SOFT, alpha=0.18, linewidth=0.6)
    for i, value in enumerate([
        summary["headline"]["median_4g_coverage_pct"],
        summary["headline"]["median_internet_use_pct"],
    ]):
        inset.text(i, value + 2, f"{value:.1f}%", ha="center", fontsize=10, fontweight="bold")

    tl.draw_footer(
        fig,
        source="ITU DataHub i271GA + i99H. Exact-year aggregate indicators; the difference is not a person count, speed result, or causal effect.",
        program_slug=SLUG,
    )
    tl.save_thumbnail(
        fig,
        program_slug=SLUG,
        out_dir=CHARTS,
        title="The network is present. Use still lags.",
        caption=(
            "Reported 4G/LTE coverage exceeds Internet use by a median 14.3 percentage "
            "points across 34 exact-year observed cases in 2024."
        ),
        headline_number=f"{median:.1f} percentage-point median difference",
        source="ITU DataHub i271GA + i99H",
        inputs=[
            "generated/digital-performance-coverage-use-panel.csv",
            "generated/digital-performance-coverage-use-summary.json",
        ],
        script=f"{SLUG}/scripts/build-thumbnail.py",
        visual_form="top signed gaps plus median component inset",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
