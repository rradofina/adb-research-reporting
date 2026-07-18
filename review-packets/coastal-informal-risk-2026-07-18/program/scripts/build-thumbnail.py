"""Build the public thumbnail for the low-elevation urban-growth study."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
sys.path.insert(0, str(ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"


def main() -> int:
    panel = pd.read_csv(OUT / "coastal-lecz-urban-centre-panel.csv")
    panel["change"] = panel.lecz10_population_2020 - panel.lecz10_population_2000
    plot = panel.dropna(subset=["change"]).nlargest(9, "change").sort_values("change")
    total = panel.change.sum() / 1e6

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.05, 0.93, f"{total:.1f} million more people recorded below 10 metres", fontsize=27, fontweight="semibold", color=tl.COLOR_INK, ha="left", va="top")
    fig.text(0.05, 0.855, "Largest urban-centre increases across the reporting ADB developing-economy panel, 2000–2020", fontsize=13, color=tl.COLOR_INK_MUTED, ha="left", va="top")

    ax = fig.add_axes([0.23, 0.17, 0.72, 0.60])
    bars = ax.barh(range(len(plot)), plot.change / 1e6, color="#D95F02", height=0.66)
    ax.set_yticks(range(len(plot)), [f"{r.urban_centre} · {r.iso3}" for r in plot.itertuples()])
    ax.set_xlabel("Additional population below 10 m (millions)")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color="#E5E9EC", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    for bar, value in zip(bars, plot.change / 1e6):
        ax.text(value + 0.1, bar.get_y() + bar.get_height()/2, f"+{value:.1f}m", va="center", fontsize=9)

    tl.draw_footer(fig, source="GHS-UCDB R2024A V1.2; 1,334 centres with reported LECZ fields. Exposure growth, not flood loss or informality.", program_slug="coastal-informal-risk")
    tl.save_thumbnail(
        fig,
        program_slug="coastal-informal-risk",
        out_dir=CHARTS,
        title=f"{total:.1f} million more people recorded below 10 metres",
        caption="Shanghai, Bangkok, and Dhaka lead the centre-level change, 2000–2020.",
        headline_number=f"+{total:.1f} million",
        source="GHS-UCDB R2024A V1.2",
        inputs=["generated/coastal-lecz-urban-centre-panel.csv"],
        script="coastal-informal-risk/scripts/build-thumbnail.py",
        visual_form="ranked horizontal bar chart",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
