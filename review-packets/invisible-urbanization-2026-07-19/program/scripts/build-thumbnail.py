"""Build the public hero for the urban-definition measurement study.

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


SLUG = "invisible-urbanization"
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"


def main() -> int:
    gap = pd.read_csv(OUT / "invisible-urbanization-definition-gap-panel.csv")
    analysis = json.loads(
        (OUT / "invisible-urbanization-definition-gap.json").read_text(encoding="utf-8")
    )
    complete = gap[(gap.year == 2020) & gap.wdi_urban_share_pct.notna()].copy()
    median = complete.absolute_gap_pp.median()
    selected = pd.concat(
        [
            complete.nlargest(6, "ghsl_minus_wdi_pp"),
            complete.nsmallest(3, "ghsl_minus_wdi_pp"),
        ]
    ).drop_duplicates("iso3").sort_values("ghsl_minus_wdi_pp")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(
        0.045, 0.94, "One urban share can be 20 points from another",
        fontsize=28, fontweight="semibold", color=tl.COLOR_INK, ha="left", va="top",
    )
    fig.text(
        0.045, 0.87,
        "GHSL applies one global grid rule; WDI reports national definitions. "
        "Across 40 complete ADB-economy cases, the disagreement is material and runs in both directions.",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="left", va="top", wrap=True,
    )
    fig.text(
        0.955, 0.94, f"{median:.1f}", fontsize=68, fontweight="bold",
        color="#d65a3a", ha="right", va="top",
    )
    fig.text(
        0.955, 0.835, "percentage-point median\nabsolute gap · 2020",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top",
    )

    ax = fig.add_axes([0.08, 0.18, 0.61, 0.57])
    y = np.arange(len(selected))
    colors = np.where(selected.ghsl_minus_wdi_pp >= 0, "#d65a3a", "#1e5b78")
    ax.barh(y, selected.ghsl_minus_wdi_pp, color=colors, height=0.64)
    ax.axvline(0, color=tl.COLOR_INK, lw=1)
    ax.set_yticks(y, selected.iso3)
    ax.set_xlabel("GHSL minus WDI urban share (percentage points)", color=tl.COLOR_INK_MUTED)
    ax.grid(axis="x", color=tl.COLOR_INK_SOFT, alpha=0.18, linewidth=0.6)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)

    scale = pd.DataFrame(analysis["administrative_scale_2020"]["common_sample"])
    inset = fig.add_axes([0.75, 0.24, 0.20, 0.39])
    inset.bar(scale.admin_level.astype(str), scale.embedded_share_pct, color=["#1e5b78", "#5f91ae", "#8fb7c9"])
    for i, value in enumerate(scale.embedded_share_pct):
        inset.text(i, value + 0.08, f"{value:.1f}%", ha="center", fontsize=10, fontweight="bold")
    inset.set_ylim(0, 3.2)
    inset.set_title("Same 13 economies\nby admin level", fontsize=11, fontweight="semibold")
    inset.set_xlabel("GADM level", fontsize=9)
    inset.set_ylabel("Embedded share", fontsize=9)
    inset.spines[["top", "right", "left"]].set_visible(False)
    inset.grid(axis="y", color=tl.COLOR_INK_SOFT, alpha=0.18, linewidth=0.6)

    tl.draw_footer(
        fig,
        source="JRC GHS-DUC R2023A V2.0; World Bank WDI SP.URB.TOTL.IN.ZS. Different constructs; gaps are not person counts.",
        program_slug=SLUG,
    )
    tl.save_thumbnail(
        fig,
        program_slug=SLUG,
        out_dir=CHARTS,
        title="One urban share can be 20 points from another",
        caption=(
            "GHSL and WDI urban shares differ by a median absolute 20.0 percentage points "
            "across 40 complete cases in 2020; administrative scale also changes the embedded share."
        ),
        headline_number=f"{median:.1f} percentage-point median absolute gap",
        source="JRC GHS-DUC R2023A V2.0 + World Bank WDI",
        inputs=[
            "generated/invisible-urbanization-definition-gap-panel.csv",
            "generated/invisible-urbanization-definition-gap.json",
        ],
        script=f"{SLUG}/scripts/build-thumbnail.py",
        visual_form="signed definition-gap bars plus administrative-scale inset",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
