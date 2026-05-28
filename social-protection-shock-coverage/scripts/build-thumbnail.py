"""Social-protection-shock-coverage hero — readiness gap.

The honest single-axis story (§6.4 demotion) is that Pakistan has the
widest gap between poverty (23 %) and the two transfer-rail
prerequisites — social-protection coverage (22 %) and account
ownership (21 %) — meaning a shock payment cannot reach the bulk of
the at-risk population through either rail.

Visual: triple-bar (poverty / SP coverage / account ownership) for
the top 8 DMCs by readiness gap. Pakistan annotated.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROGRAM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROGRAM_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import thumbnail_lib as tl  # noqa: E402

PROGRAM_SLUG = "social-protection-shock-coverage"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "social-protection-adb-panel.csv"


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    df = df[
        df["poverty_headcount_215_pct"].notna()
        & df["sp_coverage_pct"].notna()
        & df["findex_account_pct"].notna()
    ].copy()
    # Rank by the program's already-computed readiness gap (this is the
    # composite — we use it for ORDERING, not as the headline number).
    df = df.sort_values("shock_payment_readiness_gap", ascending=False).head(8)
    df = df.iloc[::-1]
    print(f"Top: {df.iloc[-1]['country']} poverty={df.iloc[-1]['poverty_headcount_215_pct']:.0f}%, "
          f"SP={df.iloc[-1]['sp_coverage_pct']:.0f}%, accounts={df.iloc[-1]['findex_account_pct']:.0f}%")

    headline_country = df.iloc[-1]["country"]
    headline_poverty = float(df.iloc[-1]["poverty_headcount_215_pct"])
    headline_sp = float(df.iloc[-1]["sp_coverage_pct"])
    headline_acc = float(df.iloc[-1]["findex_account_pct"])

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94, "Where a shock-response payment cannot reach",
             fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Three bars per DMC: share in extreme poverty ($2.15/day), "
             "share covered by any social-protection programme (ASPIRE "
             "pools all SP types), share with a financial account "
             "(Findex 2021, conducted during pandemic — account figures "
             "elevated). A shock payment must travel one of the last two "
             "rails. Ownership ≠ active use.",
             fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)
    fig.text(0.96, 0.94,
             f"{headline_poverty:.0f}% · {headline_sp:.0f}% · {headline_acc:.0f}%",
             fontsize=36, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.86,
             f"{headline_country}: poverty · SP · accounts.\n"
             f"The widest gap in the panel.",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.18, 0.10, 0.76, 0.65])
    y = np.arange(len(df))
    h = 0.25
    colors = {"poverty": "#7a1c20", "sp": "#3a5a4c", "accounts": "#c8893d"}
    ax.barh(y + h, df["poverty_headcount_215_pct"], height=h,
            color=colors["poverty"], label="Poverty $2.15/day",
            edgecolor="white", linewidth=0.5)
    ax.barh(y, df["sp_coverage_pct"], height=h,
            color=colors["sp"], label="Social-protection coverage",
            edgecolor="white", linewidth=0.5)
    ax.barh(y - h, df["findex_account_pct"], height=h,
            color=colors["accounts"], label="Findex account ownership",
            edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(df["country"], fontsize=10, color=tl.COLOR_INK)
    ax.set_xlim(0, 105)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0 %", "25 %", "50 %", "75 %", "100 %"])
    ax.legend(loc="lower right", fontsize=10, frameon=False,
              ncol=1, labelcolor=tl.COLOR_INK_MUTED)
    ax.tick_params(left=False)
    ax.grid(axis="x", color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)

    tl.draw_footer(
        fig,
        source=(
            "World Bank: WDI poverty headcount ($2.15/day 2017 PPP, SI.POV.DDAY), "
            "ASPIRE social-protection coverage, Findex account ownership. "
            "Latest available year per indicator."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Where a shock-response payment cannot reach",
        caption=(
            f"{headline_country}: {headline_poverty:.0f}% in poverty, "
            f"{headline_sp:.0f}% covered by social protection, "
            f"{headline_acc:.0f}% holding a financial account. A shock "
            f"payment must travel one of the last two rails."
        ),
        headline_number=(
            f"{headline_country} {headline_poverty:.0f}% · {headline_sp:.0f}% · {headline_acc:.0f}%"
        ),
        source="WDI poverty + ASPIRE SP + Findex accounts",
        inputs=["generated/social-protection-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="triple horizontal bar (poverty / SP / accounts, top-8 readiness gap)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
