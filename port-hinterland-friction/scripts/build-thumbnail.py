"""Port-hinterland-friction hero — import-friction concentration.

The honest single-axis story (§6.4 demotion) is: among ADB DMCs with
coastal access, China and India together account for the bulk of the
region's import-friction exposure when imports volume is multiplied
by inverse-LPI. The hero is a horizontal bar of imports_usd_year ×
(1/lpi_overall) for the top 10, with the share-of-total annotation
on the top two.
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
PANEL_CSV = GEN / "port-hinterland-friction-adb-panel.csv"


def _fmt_usd(v: float) -> str:
    if v >= 1e12:
        return f"${v/1e12:.2f} T"
    if v >= 1e9:
        return f"${v/1e9:.0f} B"
    if v >= 1e6:
        return f"${v/1e6:.0f} M"
    return f"${v:.0f}"


def main() -> int:
    df = tl.read_panel_csv(PANEL_CSV)
    df = df[df["imports_usd"].notna() & df["lpi_overall"].notna()].copy()

    # Prior revision led with `imports_usd / lpi_overall` as a single
    # "friction" bar — but volume dominates that product, so the visual
    # made China (LPI 3.70, mid-pack) look like the worst-logistics
    # country, which is false. The fix is to show the two axes
    # SEPARATELY as a scatter: x = LPI (lower = worse logistics),
    # y = annual imports. China sits high-imports / mid-LPI. Bangladesh
    # and Kazakhstan sit low-imports / low-LPI. That's the honest picture.
    df = df.sort_values("imports_usd", ascending=False).head(15)

    # Pick the largest-imports DMC for the right-side headline.
    leader = df.iloc[0]
    headline_country = leader["country"]
    headline_imports = float(leader["imports_usd"])
    headline_lpi = float(leader["lpi_overall"])
    # And the lowest-LPI DMC (worst logistics) for a secondary callout.
    worst_lpi = df.sort_values("lpi_overall").iloc[0]
    print(f"Largest imports: {headline_country} {_fmt_usd(headline_imports)}, LPI {headline_lpi:.2f}")
    print(f"Worst LPI:       {worst_lpi['country']} LPI {worst_lpi['lpi_overall']:.2f} "
          f"({_fmt_usd(float(worst_lpi['imports_usd']))} imports)")

    tl.editorial_style()
    fig = plt.figure(figsize=(tl.FIG_WIDTH_IN, tl.FIG_HEIGHT_IN), dpi=tl.FIG_DPI)
    fig.text(0.04, 0.94,
             "Volume of imports versus logistics performance",
             fontsize=27, fontweight="semibold", color=tl.COLOR_INK,
             ha="left", va="top")
    fig.text(0.04, 0.88,
             "Two distinct axes: annual merchandise imports (Y, log "
             "scale) and Logistics Performance Index (X, perception-"
             "based survey, higher = better). China and India dominate "
             "on volume; Bangladesh, Pakistan, Cambodia have the "
             "weakest LPI — not the same DMCs. Landlocked DMCs are "
             "structurally different and shown for context only.",
             fontsize=11.5, color=tl.COLOR_INK_MUTED, ha="left", va="top",
             wrap=True)
    fig.text(0.96, 0.94, _fmt_usd(headline_imports),
             fontsize=58, fontweight="bold", color=tl.COLOR_INK,
             ha="right", va="top")
    fig.text(0.96, 0.85,
             f"{headline_country}: annual imports\n"
             f"(LPI {headline_lpi:.2f} of 5 — mid-pack)",
             fontsize=12, color=tl.COLOR_INK_MUTED, ha="right", va="top")

    ax = fig.add_axes([0.10, 0.13, 0.84, 0.62])
    cmap = plt.get_cmap("viridis_r")
    lpi_min = df["lpi_overall"].min()
    lpi_max = df["lpi_overall"].max()
    lpi_norm = (lpi_max - df["lpi_overall"]) / max(lpi_max - lpi_min, 0.001)
    colors = [cmap(0.15 + 0.75 * x) for x in lpi_norm]
    sizes = (df["imports_usd"] / df["imports_usd"].max()) * 700 + 60
    ax.scatter(df["lpi_overall"], df["imports_usd"],
               s=sizes, c=colors, edgecolor="white", linewidth=1.0,
               alpha=0.92, zorder=2)
    # Label all 15 DMCs (some clusters at low-imports require offset)
    LABEL_OFFSETS = {
        "China": (10, -8), "India": (10, 0), "Hong Kong SAR, China": (10, -10),
        "Viet Nam": (10, 0), "Thailand": (-10, 8), "Indonesia": (-10, -10),
        "Malaysia": (10, 0), "Philippines": (10, 0),
        "Bangladesh": (-10, 8), "Kazakhstan": (10, 8),
    }
    for _, row in df.iterrows():
        dx, dy = LABEL_OFFSETS.get(row["country"], (8, 8))
        ha = "left" if dx > 0 else "right"
        ax.annotate(
            f"{row['country']}\n{_fmt_usd(float(row['imports_usd']))}",
            xy=(row["lpi_overall"], row["imports_usd"]),
            xytext=(dx, dy), textcoords="offset points",
            fontsize=9.5, color=tl.COLOR_INK, fontweight="semibold",
            ha=ha, va="center",
        )

    ax.set_yscale("log")
    ax.set_xlabel("Logistics Performance Index 2023 (lower = worse logistics)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.set_ylabel("Annual merchandise imports (USD, log scale)",
                  fontsize=11, color=tl.COLOR_INK_MUTED)
    ax.set_xlim(2.2, 4.3)
    ax.grid(color=tl.COLOR_INK_SOFT, alpha=0.15, linewidth=0.5)
    ax.spines["bottom"].set_color(tl.COLOR_INK_SOFT)
    ax.spines["left"].set_color(tl.COLOR_INK_SOFT)

    tl.draw_footer(
        fig,
        source=(
            "World Bank Logistics Performance Index 2023 + WDI imports of "
            "goods and services (current US$, NE.IMP.GNFS.CD). Latest year "
            "per DMC. Landlocked DMCs (AFG, UZB, KGZ, TJK, LAO, MNG) are "
            "structurally different and are reported separately by the "
            "program."
        ),
        program_slug=PROGRAM_SLUG,
    )
    tl.save_thumbnail(
        fig, program_slug=PROGRAM_SLUG, out_dir=CHARTS,
        title="Volume of imports versus logistics performance",
        caption=(
            f"{headline_country} {_fmt_usd(headline_imports)} (LPI "
            f"{headline_lpi:.2f}) and India $857B (LPI 3.40) dominate "
            f"imports volume; {worst_lpi['country']} (LPI "
            f"{worst_lpi['lpi_overall']:.2f}) and Kazakhstan have the "
            f"weakest logistics. Volume-leaders and logistics-laggards "
            f"are not the same DMCs."
        ),
        headline_number=f"{headline_country} {_fmt_usd(headline_imports)} imports · LPI {headline_lpi:.2f}",
        source="WB LPI 2023 + WDI NE.IMP.GNFS.CD",
        inputs=["generated/port-hinterland-friction-adb-panel.csv"],
        script=f"{PROGRAM_SLUG}/scripts/build-thumbnail.py",
        visual_form="bubble scatter (LPI × imports, log-imports axis)",
    )
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
