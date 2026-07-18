"""Hero for the grid heat/reliability construct-validation story.

attestation_chain: ai-first
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

SLUG = "grid-reliability-heat"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"


def main() -> int:
    result = json.loads((GEN / "grid-heat-reliability-construct-validation.json").read_text(encoding="utf-8"))
    positive = result["signs"]["positive"]
    negative = result["signs"]["negative"]
    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(.04,.94,"One grid result survives. The heat direction does not.",fontsize=28,fontweight="semibold",color=tl.COLOR_INK,ha="left",va="top")
    fig.text(.04,.865,"Capacity and generation retain the same five most-concentrated economies. Across exact-year public heat and reliability definitions, the sign splits almost evenly.",fontsize=12,color=tl.COLOR_INK_MUTED,ha="left",va="top",wrap=True)
    cards=[(.04,"GATE 1","CAPACITY → GENERATION","5 of 5","top economies remain","#2C7A64"),(.52,"GATE 2","HEAT → RELIABILITY",f"{positive} vs {negative}","positive vs negative correlations","#A63D40")]
    for x,kicker,heading,value,note,color in cards:
        ax=fig.add_axes([x,.22,.44,.50]); ax.set_facecolor("#EEF2F4"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
        ax.text(.07,.84,kicker,transform=ax.transAxes,fontsize=9,fontweight="bold",color=color)
        ax.text(.07,.68,heading,transform=ax.transAxes,fontsize=12,fontweight="semibold",color=tl.COLOR_INK)
        ax.text(.07,.38,value,transform=ax.transAxes,fontsize=35,fontweight="bold",color=color)
        ax.text(.07,.19,note,transform=ax.transAxes,fontsize=10,color=tl.COLOR_INK_MUTED)
    tl.draw_footer(fig,source="WRI GPPD v1.3.0; World Bank CCKP ERA5; World Bank public reliability indicators. Descriptive construct validation.",program_slug=SLUG)
    tl.save_thumbnail(fig,program_slug=SLUG,out_dir=CHARTS,title="One grid result survives. The heat direction does not.",caption=f"The generation-mix top five is stable; heat–reliability correlations split {positive} positive to {negative} negative.",headline_number=f"{positive} vs {negative}",source="WRI GPPD; World Bank CCKP and indicators",inputs=["generated/grid-generation-deepening.json","generated/grid-heat-reliability-construct-validation.json"],script=f"{SLUG}/scripts/build-thumbnail.py",visual_form="two-gate construct-validation cards")
    plt.close(fig)
    return 0


if __name__ == "__main__": sys.exit(main())
