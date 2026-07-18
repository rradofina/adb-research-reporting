"""Build the climate-health construct-validation research hero.

Inputs are committed generated evidence. No network access.
attestation_chain: ai-first.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt


PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "climate-health-workdays"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
VALIDATION_PATH = GEN / "climate-health-construct-validation.json"

NAMES = {
    "IND": "India",
    "AFG": "Afghanistan",
    "BGD": "Bangladesh",
    "KHM": "Cambodia",
    "MMR": "Myanmar",
    "THA": "Thailand",
}


def main() -> int:
    evidence = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))
    latest = max(evidence["baseline_year_summaries"], key=lambda row: row["year"])
    proxy_top3 = latest["proxy_top3"]
    heat_top3 = latest["heat_top3"]
    overlap = latest["top3_overlap_count"]

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(
        0.04, 0.945,
        "The PM2.5 proxy does not recover the heat-work-loss signal",
        fontsize=26, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.865,
        "In aligned 2020 data for 34 economies, the proxy and the Lancet Countdown heat-related\n"
        "potential work-hours-loss measure produce disjoint top threes. They measure different constructs.",
        fontsize=11.8, color=tl.COLOR_INK_MUTED, ha="left", va="top", wrap=True,
    )
    fig.text(
        0.955, 0.945, f"{overlap}/3", fontsize=66, fontweight="bold",
        color=tl.COLOR_INK, ha="right", va="top",
    )
    fig.text(
        0.955, 0.845, "economies appear in both top threes",
        fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="right", va="top",
    )

    left = fig.add_axes([0.05, 0.23, 0.38, 0.47])
    right = fig.add_axes([0.57, 0.23, 0.38, 0.47])
    for ax, title, color in [
        (left, "PM2.5 × employment proxy", "#A63D40"),
        (right, "Heat-related potential hours lost", tl.COLOR_HIGHLIGHT),
    ]:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 4)
        ax.axis("off")
        ax.text(0, 3.64, title, fontsize=14, color=tl.COLOR_INK, fontweight="semibold", va="bottom")
        ax.plot([0, 1], [3.48, 3.48], color=tl.COLOR_INK_SOFT, alpha=0.35, linewidth=1)
        ax.plot([0.02, 0.02], [0.38, 3.22], color=color, linewidth=4, solid_capstyle="round")

    for idx, iso in enumerate(proxy_top3, 1):
        y = 2.94 - (idx - 1) * 0.93
        left.text(0.10, y, str(idx), fontsize=13, color="#A63D40", fontweight="bold", va="center")
        left.text(0.22, y, NAMES[iso], fontsize=14, color=tl.COLOR_INK, va="center")

    for idx, iso in enumerate(heat_top3, 1):
        y = 2.94 - (idx - 1) * 0.93
        right.text(0.10, y, str(idx), fontsize=13, color=tl.COLOR_HIGHLIGHT, fontweight="bold", va="center")
        right.text(0.22, y, NAMES[iso], fontsize=14, color=tl.COLOR_INK, va="center")

    fig.text(0.50, 0.48, "≠", fontsize=54, color=tl.COLOR_INK_SOFT, ha="center", va="center")
    fig.text(
        0.50, 0.39, f"Spearman ρ = {latest['spearman_proxy_vs_heat']:.2f}",
        fontsize=10, color=tl.COLOR_INK_MUTED, ha="center", va="center",
    )
    fig.text(
        0.04, 0.145,
        "The disagreement survives all 21 aligned year × ±50% parameter tests: "
        "16 have zero top-three overlap and five have one.",
        fontsize=10.8, color=tl.COLOR_INK, ha="left", va="top",
    )

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI employment and PM2.5; Lancet Countdown 2025 indicator 1.1.3. "
            "The heat measure is modelled potential capacity loss, not observed absence."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="The PM2.5 proxy does not recover the heat-work-loss signal",
        caption=(
            "The two aligned 2020 top threes have zero overlap. Across all 21 aligned "
            "year-and-parameter tests, overlap never exceeds one economy."
        ),
        headline_number="0 of 3 economies overlap in 2020",
        source="WDI + Lancet Countdown 2025 indicator 1.1.3",
        inputs=["generated/climate-health-construct-validation.json"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="paired ranked lists (PM2.5 proxy versus heat-related potential work-hours loss)",
    )
    svg_path = CHARTS / f"{PROGRAM_SLUG}-thumbnail.svg"
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
