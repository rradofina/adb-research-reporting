"""Build the air-monitoring hero from the committed public-evidence ledger.

attestation_chain: ai-first
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "air-monitoring"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
LEDGER = GEN / "evidence-ledger.json"


def main() -> int:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    c = data["headline_counts"]
    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94, "Public monitor routes are visible. Claim-ready QA evidence is not.", fontsize=25, fontweight="semibold", color=tl.COLOR_INK, ha="left", va="top")
    fig.text(0.04, 0.865, f"The audit covers {c['economies_in_source_discovery']} economies, {c['official_station_rows_audited']} official station rows, and {c['identity_candidate_rows_checked']} identity candidates. It finds no validated same-station rows, complete monitor-grade rows, station-radius-ready economies, or allowed coverage claims.", fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top", wrap=True)

    ax = fig.add_axes([0.04, 0.16, 0.92, 0.58])
    ax.axis("off")
    stages = [
        ("Denominator\njoins", c["denominator_join_rows"], "#007DB8"),
        ("Identity\ncandidates", c["identity_candidate_rows_checked"], "#002569"),
        ("Validated\nidentities", c["validated_same_station_rows"], "#9B2226"),
        ("Complete\ngrade rows", c["complete_monitor_grade_rows"], "#9B2226"),
        ("Allowed coverage\nclaims", c["claim_allowed_country_rows"], "#9B2226"),
    ]
    xs = [0.10, 0.30, 0.50, 0.70, 0.90]
    for i, ((label, value, color), x) in enumerate(zip(stages, xs)):
        box = FancyBboxPatch((x - 0.075, 0.30), 0.15, 0.37, boxstyle="round,pad=0.015,rounding_size=0.02", transform=ax.transAxes, facecolor="#DCEFF7" if value else "#FBE6E7", edgecolor=color, linewidth=1.7)
        ax.add_patch(box)
        ax.text(x, 0.53, f"{value:,}", transform=ax.transAxes, ha="center", va="center", fontsize=30, fontweight="bold", color=color)
        ax.text(x, 0.37, label, transform=ax.transAxes, ha="center", va="center", fontsize=10.5, color=tl.COLOR_INK)
        if i < len(stages) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.09, 0.49), xytext=(x + 0.09, 0.49), xycoords=ax.transAxes, arrowprops={"arrowstyle": "->", "color": tl.COLOR_INK_SOFT, "lw": 1.2})
    ax.text(0.50, 0.12, "The result is a bounded public-data absence—not a monitor-coverage estimate.", transform=ax.transAxes, ha="center", fontsize=14, fontweight="bold", color="#9B2226")

    tl.draw_footer(fig, source="Committed air-monitoring public-evidence ledger; 64 source-summary rows and named retrieval routes.", program_slug=PROGRAM_SLUG)
    tl.save_thumbnail(
        fig,
        program_slug=PROGRAM_SLUG,
        out_dir=CHARTS,
        title="Public monitor routes are visible. Claim-ready QA evidence is not.",
        caption=f"Across {c['economies_in_source_discovery']} economies and {c['official_station_rows_audited']} audited official station rows, the public packet verifies 0 same-station joins, 0 complete monitor-grade rows, and 0 allowed coverage claims.",
        headline_number="0 validated joins · 0 complete grade rows · 0 allowed claims",
        source="Committed air-monitoring public-evidence ledger",
        inputs=["generated/evidence-ledger.json"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="claim-permission evidence ladder",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
