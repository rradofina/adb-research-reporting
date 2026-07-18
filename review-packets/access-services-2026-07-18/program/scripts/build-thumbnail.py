"""Build the access-services research hero from committed registry evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt


PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "access-services"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
SOURCE = GEN / "access-osm-completeness-deepening.json"


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    correction = source["phl_correction"]
    rows = source["phl_rows"]
    largest = sorted(rows, key=lambda row: abs(row["rank_shift"]), reverse=True)[:8]
    largest = sorted(largest, key=lambda row: row["rank_shift"])

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(
        0.04, 0.94,
        "The facility map changes the regional rank",
        fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
        ha="left", va="top",
    )
    fig.text(
        0.04, 0.865,
        "Replacing OSM health-point counts with the Philippine official clinical registry "
        "reorders nearly every regional people-per-facility rank. The inherited eight-economy "
        "screen is a map-observability triage, not a service-access ranking.",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="left", va="top", wrap=True,
    )
    fig.text(
        0.955, 0.94,
        f"{correction['n_adm1_rank_changed']}/{correction['n_adm1_total']}",
        fontsize=66, fontweight="bold", color=tl.COLOR_INK,
        ha="right", va="top",
    )
    fig.text(
        0.955, 0.84,
        "Philippine regional ranks change",
        fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top",
    )

    ax = fig.add_axes([0.24, 0.15, 0.69, 0.57])
    labels = [row["admin1_name"] for row in largest]
    shifts = [row["rank_shift"] for row in largest]
    colors = ["#A63D40" if shift < 0 else tl.COLOR_HIGHLIGHT for shift in shifts]
    bars = ax.barh(labels, shifts, color=colors, height=0.62, alpha=0.92)
    ax.axvline(0, color=tl.COLOR_INK, linewidth=1.1)
    for bar, row in zip(bars, largest, strict=True):
        shift = row["rank_shift"]
        ax.annotate(
            f"{row['rank_osm']} → {row['rank_registry']}",
            xy=(shift, bar.get_y() + bar.get_height() / 2),
            xytext=(6 if shift >= 0 else -6, 0),
            textcoords="offset points",
            ha="left" if shift >= 0 else "right",
            va="center",
            fontsize=10.5,
            color=tl.COLOR_INK,
            fontweight="semibold",
        )
    ax.set_xlim(-11, 16)
    ax.set_xlabel("Rank movement after registry substitution", color=tl.COLOR_INK_MUTED)
    ax.tick_params(axis="y", length=0, labelsize=10.5)
    ax.tick_params(axis="x", colors=tl.COLOR_INK_MUTED)
    ax.grid(axis="x", color=tl.COLOR_INK_SOFT, alpha=0.22, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)

    tl.draw_footer(
        fig,
        source=(
            "Philippine PSA 2020 population; DOH NHFR v2.0 official clinical registry; "
            "OpenStreetMap health points. Counts retrieved in 2026. Rank movement is a "
            "denominator test, not travel-time, capacity, quality, utilization, or welfare."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="The facility map changes the regional rank",
        caption=(
            "Official clinical registry counts reorder 16 of 17 Philippine regional "
            "people-per-facility ranks. The eight-economy OSM screen is retained only "
            "as a map-observability and source-validation queue."
        ),
        headline_number="16 of 17 Philippine regional ranks change",
        source="PSA 2020 + DOH NHFR v2.0 + OSM",
        inputs=["generated/access-osm-completeness-deepening.json"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="diverging bars (largest Philippine rank shifts after registry substitution)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
