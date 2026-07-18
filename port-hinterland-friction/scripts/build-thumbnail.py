"""Port-hinterland hero — the national proxy fails the port-time test.

attestation_chain: ai-first
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

PROGRAM_SLUG = "port-hinterland-friction"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
COUNTRIES = GEN / "port-cppi-country-diagnostics.csv"


def main() -> int:
    data = pd.read_csv(COUNTRIES).sort_values("inherited_friction_rank")
    inherited = data.loc[data.inherited_top5].copy()
    overlap = int((inherited.observed_disadvantage_rank <= 5).sum())

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(
        0.04,
        0.94,
        "Trade volume did not predict observed port delay",
        fontsize=28,
        fontweight="semibold",
        color=tl.COLOR_INK,
        ha="left",
        va="top",
    )
    fig.text(
        0.04,
        0.865,
        "The inherited imports × LPI screen was compared with 2025 World Bank CPPI vessel-time data. "
        "Only Indonesia remains in the top five; CPPI still stops at the port boundary and does not measure the hinterland.",
        fontsize=11.5,
        color=tl.COLOR_INK_MUTED,
        ha="left",
        va="top",
        wrap=True,
    )

    fig.text(
        0.055,
        0.64,
        f"{overlap} of 5",
        fontsize=62,
        fontweight="bold",
        color="#A63D40",
        ha="left",
        va="top",
    )
    fig.text(
        0.058,
        0.52,
        "inherited top-five members\nremain under observed\nport-time disadvantage",
        fontsize=13,
        color=tl.COLOR_INK_MUTED,
        ha="left",
        va="top",
        linespacing=1.35,
    )
    fig.text(
        0.058,
        0.33,
        "China  1 → 12\nIndia    2 → 10\nIndonesia 3 → 3",
        fontsize=14,
        color=tl.COLOR_INK,
        ha="left",
        va="top",
        linespacing=1.45,
        family="monospace",
    )

    ax = fig.add_axes([0.36, 0.15, 0.58, 0.58])
    for _, row in data.iterrows():
        color = tl.COLOR_ACCENT if row.inherited_top5 else tl.COLOR_INK_SOFT
        width = 2.5 if row.inherited_top5 else 0.9
        alpha = 0.92 if row.inherited_top5 else 0.35
        ax.plot(
            [0, 1],
            [row.inherited_friction_rank, row.observed_disadvantage_rank],
            color=color,
            linewidth=width,
            alpha=alpha,
            zorder=1,
        )
        if row.inherited_top5:
            ax.scatter(
                [0, 1],
                [row.inherited_friction_rank, row.observed_disadvantage_rank],
                s=42,
                color=color,
                edgecolor="white",
                linewidth=0.7,
                zorder=2,
            )
            ax.text(-0.035, row.inherited_friction_rank, row.iso3, ha="right", va="center", fontsize=9, color=tl.COLOR_INK)
            ax.text(1.035, row.observed_disadvantage_rank, row.iso3, ha="left", va="center", fontsize=9, color=tl.COLOR_INK)
    ax.set_xlim(-0.16, 1.16)
    ax.set_ylim(13.8, 0.2)
    ax.set_xticks([0, 1], ["Imports × LPI\nrank", "Observed CPPI\ndisadvantage rank"])
    ax.set_yticks([1, 3, 5, 7, 9, 11, 13])
    ax.grid(axis="y", color=tl.COLOR_INK_SOFT, alpha=0.20, linewidth=0.6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, colors=tl.COLOR_INK_MUTED)

    tl.draw_footer(
        fig,
        source=(
            "World Bank CPPI 2020–2025 annex; committed WDI imports × LPI panel. "
            "Main diagnostic uses 2025 median CPPI across ports with at least 48 sampled calls. "
            "Country aggregates are research diagnostics, not official World Bank rankings."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="Trade volume did not predict observed port delay",
        caption=(
            "Only Indonesia remains in the inherited top five after replacing trade scale and LPI perception "
            "with observed 2025 CPPI vessel-time performance. China moves from rank 1 to 12 and India from 2 to 10."
        ),
        headline_number=f"{overlap} of 5 retained",
        source="World Bank CPPI 2020–2025 + committed WDI imports/LPI panel",
        inputs=["generated/port-cppi-country-diagnostics.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="rank-inversion slopegraph",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
