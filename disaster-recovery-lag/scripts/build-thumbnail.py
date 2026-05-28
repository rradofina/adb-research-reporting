"""Disaster-recovery-lag hero — the affected-population burden.

The honest single-axis story (§6.4 demotion) is that the EM-DAT
people-affected total over 2000–2025 concentrates heavily in two
countries: China (~1.77 B) and India (~1.15 B). The hero conveys the
order-of-magnitude gap to other DMCs with a horizontal ranked bar of
the top 10 by `total_affected`.

NOTE: this is BURDEN exposure, not recovery lag — per program §STATUS
the recovery-lag metric requires event-timestamped indicator-recovery
curves which the program has not yet committed. The thumbnail title
makes this explicit.
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

PROGRAM_SLUG = "disaster-recovery-lag"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "disaster-recovery-lag-adb-panel.csv"
TOP_N = 10


def _fmt(v: float) -> str:
    if v >= 1e9:
        return f"{v/1e9:.2f} B"
    if v >= 1e6:
        return f"{v/1e6:.0f} M"
    if v >= 1e3:
        return f"{v/1e3:.0f} k"
    return f"{v:.0f}"


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    # Prior revision led with "total_affected" — but EM-DAT counts the
    # same person across multiple events, so CHN's 1.77 B was greater
    # than CHN's population (~1.4 B), which is impossible as a unique-
    # person count. Switch the primary axis to events_per_year (a
    # straight rate of EM-DAT-recorded disasters, no double-counting),
    # and surface the person-events number only as a secondary label
    # with an explicit "may double-count" disclosure.
    sub = df[df["events_per_year"].notna()].copy()
    sub = sub.sort_values("events_per_year", ascending=False).head(TOP_N).iloc[::-1]

    headline_country = sub.iloc[-1]["country"]
    headline_events = float(sub.iloc[-1]["events_per_year"])
    headline_affected = float(sub.iloc[-1]["total_affected"])
    print(f"Headline: {headline_country} {headline_events:.1f} events/yr "
          f"({_fmt(headline_affected)} person-event exposures, may double-count)")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94, "Recorded disasters per year, 2000–2025",
             fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Annual rate of EM-DAT-recorded disasters, top 10 ADB DMCs. "
             "Bar length is a clean disaster-count rate; person-events "
             "(below each bar) are summed across events and may double-"
             "count people who lived through more than one. Burden "
             "exposure — not yet a recovery-lag metric.",
             fontsize=12.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)
    fig.text(0.96, 0.94, f"{headline_events:.1f}/yr",
             fontsize=68, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.84,
             f"recorded disasters per year\n"
             f"in {headline_country} (EM-DAT, 2000–2025)",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.20, 0.13, 0.74, 0.62])
    cmap = plt.get_cmap("viridis_r")
    vmax_rate = float(sub["events_per_year"].max())
    colors = [cmap(0.15 + 0.75 * v / vmax_rate) for v in sub["events_per_year"]]
    bars = ax.barh(sub["country"], sub["events_per_year"],
                   color=colors, edgecolor="white", linewidth=0.8, height=0.72)
    for bar, rate, affected in zip(bars, sub["events_per_year"], sub["total_affected"]):
        ax.annotate(
            f"{rate:.1f}/yr   ·   {_fmt(affected)} person-events",
            xy=(rate, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0), textcoords="offset points",
            ha="left", va="center",
            fontsize=10, color=tl.COLOR_INK, fontweight="semibold",
        )
    ax.set_xlim(0, vmax_rate * 1.55)
    ax.tick_params(left=False)
    ax.set_yticks(range(len(sub)))
    ax.set_yticklabels(sub["country"], fontsize=10, color=tl.COLOR_INK)
    ax.set_xlabel("Recorded disasters per year (2000–2025)",
                  fontsize=10, color=tl.COLOR_INK_MUTED)
    ax.grid(axis="x", color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)

    tl.draw_footer(
        fig,
        source=(
            "EM-DAT (CRED) International Disaster Database, events recorded "
            "2000–2025. People affected = injured + made homeless + needing "
            "assistance, summed across events."
        ),
        program_slug=PROGRAM_SLUG,
    )

    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Recorded disasters per year, 2000–2025",
        caption=(
            f"{headline_country} {headline_events:.1f} EM-DAT-recorded "
            f"disasters per year, {_fmt(headline_affected)} person-event "
            f"exposures (may double-count people across events). India, "
            f"Philippines, Bangladesh follow."
        ),
        headline_number=f"{headline_country} {headline_events:.1f} recorded disasters per year",
        source="EM-DAT (CRED) 2000–2025",
        inputs=["generated/disaster-recovery-lag-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="horizontal ranked bar (events per year, person-events as secondary)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
