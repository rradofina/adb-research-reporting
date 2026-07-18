"""Build the migration denominator-switch research hero.

Input: committed migration-per-population-deepening.json and
migration-corridor-type-forced-displacement.json. No network access.
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

PROGRAM_SLUG = "migration-displacement-signals"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PER_POP_PATH = GEN / "migration-per-population-deepening.json"
FORCED_PATH = GEN / "migration-corridor-type-forced-displacement.json"


def main() -> int:
    per_pop = json.loads(PER_POP_PATH.read_text(encoding="utf-8"))
    forced = json.loads(FORCED_PATH.read_text(encoding="utf-8"))
    rows = {row["iso3"]: row for row in per_pop["rows_by_share"]}
    panel_rows = {
        row["iso3"]: row
        for row in json.loads((GEN / "migration-displacement-adb-panel.json").read_text(encoding="utf-8"))["rows"]
    }
    absolute = per_pop["absolute_top5"]
    share = per_pop["share_top5"]
    overlap = len(set(absolute) & set(share))
    afghanistan_pct = forced["summary"]["afghanistan_forced_abroad_pct_of_emigrant_stock"]

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(
        0.04, 0.945,
        "The leading origins change when population enters the denominator",
        fontsize=26, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.865,
        "UN DESA 2024 emigrant stock and the same stock divided by WDI 2024 resident "
        "population produce disjoint top fives. The first measures diaspora size; the "
        "second measures cumulative stock relative to the origin population.",
        fontsize=11.8, color=tl.COLOR_INK_MUTED, ha="left", va="top", wrap=True,
    )
    fig.text(0.955, 0.945, f"{overlap}/5", fontsize=66, fontweight="bold", color=tl.COLOR_INK, ha="right", va="top")
    fig.text(0.955, 0.845, "economies appear in both top fives", fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    left = fig.add_axes([0.04, 0.22, 0.39, 0.49])
    right = fig.add_axes([0.57, 0.22, 0.39, 0.49])
    for ax, title in [(left, "Absolute emigrant stock"), (right, "Stock ÷ resident population")]:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 6)
        ax.axis("off")
        ax.text(0, 5.72, title, fontsize=14, color=tl.COLOR_INK, fontweight="semibold", va="bottom")
        ax.plot([0, 1], [5.52, 5.52], color=tl.COLOR_INK_SOFT, alpha=0.35, linewidth=1)

    for idx, iso in enumerate(absolute, 1):
        row = panel_rows[iso]
        y = 5.05 - (idx - 1) * 0.93
        left.text(0.00, y, f"{idx}", fontsize=13, color="#A63D40", fontweight="bold", va="center")
        left.text(0.10, y, row["country"], fontsize=13, color=tl.COLOR_INK, va="center")
        left.text(0.98, y, f"{row['emigrant_stock_2024']/1e6:.1f}M", fontsize=12.5, color=tl.COLOR_INK, ha="right", va="center")

    for idx, iso in enumerate(share, 1):
        row = rows[iso]
        y = 5.05 - (idx - 1) * 0.93
        right.text(0.00, y, f"{idx}", fontsize=13, color=tl.COLOR_HIGHLIGHT, fontweight="bold", va="center")
        right.text(0.10, y, row["country"], fontsize=13, color=tl.COLOR_INK, va="center")
        right.text(0.98, y, f"{row['emigrant_pct_of_population']:.1f}%", fontsize=12.5, color=tl.COLOR_INK, ha="right", va="center")

    fig.text(0.50, 0.49, "÷", fontsize=48, color=tl.COLOR_INK_SOFT, ha="center", va="center")
    fig.text(0.50, 0.43, "2024 population", fontsize=9.5, color=tl.COLOR_INK_MUTED, ha="center", va="center")

    fig.text(
        0.04, 0.145,
        f"Near-rank exception: Afghanistan moves from absolute rank 4 to share rank 6, "
        f"but UNHCR forced-displacement stock equals {afghanistan_pct:.1f}% of its UN DESA emigrant stock.",
        fontsize=10.6, color=tl.COLOR_INK, ha="left", va="top",
    )

    tl.draw_footer(
        fig,
        source=(
            "UN DESA International Migrant Stock 2024; World Bank WDI SP.POP.TOTL 2024; "
            "UNHCR Refugee Data Finder 2024. Cumulative stock, not current flow. Population "
            "shares withheld for TWN, COK, and NIU because WDI does not report a denominator."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="The leading origins change when population enters the denominator",
        caption=(
            "The absolute and population-share top fives have zero overlap. Afghanistan "
            "is the near-rank exception, but its stock is forced-displacement-majority."
        ),
        headline_number="0 of 5 economies appear in both top fives",
        source="UN DESA 2024 + WDI 2024 + UNHCR 2024",
        inputs=[
            "generated/migration-per-population-deepening.json",
            "generated/migration-corridor-type-forced-displacement.json",
        ],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="paired ranked lists (absolute stock versus stock divided by population)",
    )
    svg_path = CHARTS / f"{PROGRAM_SLUG}-thumbnail.svg"
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
