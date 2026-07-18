"""Food-price-climate-transmission hero — Lao PDR and Pakistan.

The honest single-axis story (per program §STATUS) is that the
composite index failed sensitivity and was dropped. What survives is
a usable two-axis screen: Lao PDR and Pakistan jointly sit high on
both CPI inflation and agriculture-import exposure for every N from
3 to 10. The hero is a two-axis scatter with those two DMCs labeled.
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

PROGRAM_SLUG = "food-price-climate-transmission"
GEN = PROGRAM_ROOT / "generated"
CHARTS = GEN / "charts"
PANEL_CSV = GEN / "food-price-adb-panel.csv"

# The program's stable claim (results.md): LAO and PAK clear both
# axes for every N from 3 to 10. Bangladesh joins from N=5; including
# it as a primary highlight contradicts the "only DMCs that clear
# both" subtitle, so BGD is downgraded to a secondary marker.
LABELED = {"LAO", "PAK"}
SECONDARY = {"BGD"}


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    df = df[
        df["cpi_inflation_pct"].notna()
        & df["ag_imports_pct_merch"].notna()
    ].copy()

    lao = df[df["iso3"] == "LAO"].iloc[0]
    pak = df[df["iso3"] == "PAK"].iloc[0]
    print(f"LAO CPI={lao['cpi_inflation_pct']:.1f}%, ag-imports={lao['ag_imports_pct_merch']:.1f}%")
    print(f"PAK CPI={pak['cpi_inflation_pct']:.1f}%, ag-imports={pak['ag_imports_pct_merch']:.1f}%")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94,
             "Joint exposure on CPI inflation AND ag-import share",
             fontsize=26, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "The composite index failed ±50 % sensitivity and was "
             "dropped. The two-axis screen survives: Lao PDR and Pakistan "
             "clear both axes for every N from 3 to 10. "
             "General CPI (not food-CPI). Pakistan's 2023 CPI was "
             "exchange-rate-driven (per WB Food Crisis Observatory) — "
             "the joint exposure here is not a climate-transmission claim.",
             fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)

    ax = fig.add_axes([0.08, 0.13, 0.86, 0.65])
    # Background scatter
    backdrop_mask = ~df["iso3"].isin(LABELED | SECONDARY)
    others = df[backdrop_mask]
    ax.scatter(others["ag_imports_pct_merch"], others["cpi_inflation_pct"],
               s=60, color=tl.COLOR_INK_SOFT, alpha=0.55,
               edgecolor="white", linewidth=0.5, zorder=2)
    # Secondary (joins from N=5)
    sec = df[df["iso3"].isin(SECONDARY)]
    ax.scatter(sec["ag_imports_pct_merch"], sec["cpi_inflation_pct"],
               s=140, facecolor="white",
               edgecolor="#7a1c20", linewidth=2.0, zorder=2.5)
    for _, r in sec.iterrows():
        ax.annotate(
            f"{r['country']} (joins from N=5)\n"
            f"CPI {r['cpi_inflation_pct']:.1f} % · "
            f"ag-imports {r['ag_imports_pct_merch']:.1f} %",
            xy=(r["ag_imports_pct_merch"], r["cpi_inflation_pct"]),
            xytext=(10, -10), textcoords="offset points",
            fontsize=9.5, color=tl.COLOR_INK_MUTED, fontweight="semibold",
            fontstyle="italic",
        )
    # Primary highlight (stable across N=3..10)
    high = df[df["iso3"].isin(LABELED)]
    ax.scatter(high["ag_imports_pct_merch"], high["cpi_inflation_pct"],
               s=200, color="#7a1c20",
               edgecolor="white", linewidth=1.2, zorder=3)
    for _, r in high.iterrows():
        ax.annotate(
            f"{r['country']}\nCPI {r['cpi_inflation_pct']:.1f} % · "
            f"ag-imports {r['ag_imports_pct_merch']:.1f} %",
            xy=(r["ag_imports_pct_merch"], r["cpi_inflation_pct"]),
            xytext=(10, 10), textcoords="offset points",
            fontsize=10, color=tl.COLOR_INK, fontweight="semibold",
        )

    ax.set_xlabel("Agriculture share of total merchandise imports (%)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.set_ylabel("CPI inflation (%, year-on-year)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.grid(color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)
    ax.spines["bottom"].set_color(tl.COLOR_INK_SOFT)
    ax.spines["left"].set_color(tl.COLOR_INK_SOFT)
    ax.set_xlim(0, max(df["ag_imports_pct_merch"].max() * 1.1, 25))
    ax.set_ylim(min(0, df["cpi_inflation_pct"].min()) - 3,
                df["cpi_inflation_pct"].max() * 1.18)

    tl.draw_footer(
        fig,
        source=(
            "World Bank WDI FP.CPI.TOTL.ZG (CPI inflation), TM.VAL.AGRI.ZS.UN "
            "(ag share of merchandise imports). Latest available year per "
            "DMC. Sensitivity: pairing stable for every N=3..10."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Two economies with high CPI inflation AND ag-import exposure",
        caption=(
            f"Lao PDR (CPI {lao['cpi_inflation_pct']:.1f} %, ag-imports "
            f"{lao['ag_imports_pct_merch']:.1f} % of merchandise) and Pakistan "
            f"({pak['cpi_inflation_pct']:.1f} % / "
            f"{pak['ag_imports_pct_merch']:.1f} %) are the only DMCs that "
            f"clear both axes — stable across every N from 3 to 10."
        ),
        headline_number=f"LAO {lao['cpi_inflation_pct']:.1f}% CPI · {lao['ag_imports_pct_merch']:.1f}% ag-imports",
        source="WDI CPI inflation + agricultural-import share",
        inputs=["generated/food-price-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="two-axis scatter (CPI × ag-import share)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
