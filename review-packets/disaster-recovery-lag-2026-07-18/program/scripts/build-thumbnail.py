"""Build the disaster-recovery construct-validation hero.

The hero leads with the publishable finding: the burden claim fails its metric
gate and the direct recovery pilot fails its stability gate.
attestation_chain: ai-first
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
sys.path.insert(0, str(ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402


SLUG = "disaster-recovery-lag"
GEN = PROGRAM / "generated"
CHARTS = GEN / "charts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    metrics = load(GEN / "disaster-recovery-lag-metric-falsification.json")
    validation = load(GEN / "disaster-recovery-haiyan-construct-validation.json")
    killed = sum(row["kill_condition_fires"] for row in metrics["kill_condition_by_metric"].values())
    stable = len(validation["validation"]["stable_locations_all_variants"])

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI, facecolor="white")
    fig.text(0.045, 0.94, "A disaster-recovery ranking fails two validity gates", fontsize=26, fontweight="semibold", color=tl.COLOR_INK, ha="left", va="top")
    fig.text(0.045, 0.875, "Country burden is not recovery. A 108-orbit Haiyan pilot still yields no centroid with one recovery month across 54 variants.", fontsize=12.5, color=tl.COLOR_INK_MUTED, ha="left", va="top", wrap=True)

    cards = [
        (0.05, "BURDEN GATE", f"{killed} of 5", "metrics replace the claimed\nCHN–IND top two", "#A63D40"),
        (0.52, "RECOVERY GATE", f"{stable} of 7", "centroids stable across\nall recovery variants", "#002569"),
    ]
    for x, label, value, detail, color in cards:
        ax = fig.add_axes([x, 0.20, 0.42, 0.54])
        ax.set_facecolor("#EEF2F4"); ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.text(0.07, 0.82, label, transform=ax.transAxes, fontsize=10, color=color, fontweight="bold")
        ax.text(0.07, 0.48, value, transform=ax.transAxes, fontsize=48, color=color, fontweight="bold")
        ax.text(0.07, 0.20, detail, transform=ax.transAxes, fontsize=12, color=tl.COLOR_INK_MUTED, linespacing=1.35)

    tl.draw_footer(fig, source="EM-DAT country profiles; GDIS; World Bank Light Every Night VIIRS-DNB. Nighttime radiance is a proxy, not welfare.", program_slug=SLUG)
    tl.save_thumbnail(
        fig,
        program_slug=SLUG,
        out_dir=CHARTS,
        title="A disaster-recovery ranking fails two validity gates",
        caption=(
            f"{killed} of five burden metrics replace the claimed CHN–IND top two; "
            f"{stable} of seven Haiyan centroids return one recovery month across all variants."
        ),
        headline_number=f"{killed}/5 burden metrics fail; {stable}/7 recovery centroids stable",
        source="EM-DAT; GDIS; World Bank Light Every Night",
        inputs=[
            "generated/disaster-recovery-lag-metric-falsification.json",
            "generated/disaster-recovery-haiyan-construct-validation.json",
        ],
        script=f"{SLUG}/scripts/build-thumbnail.py",
        visual_form="two-stage construct-validation gate",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
