"""Build the remittance-resilience visualization — single source of truth.

Principle. The visualization rule in `research/factory.md` requires that each
program has 1–2 visualizations its argument actually needs, defined once, used
across every publication tier. Remittance-resilience's argument is that five
DMCs (KGZ, NPL, TON, VUT, WSM) sit in the top five of a joint dependence × cost
ranking and stay there across the ±50 percent sensitivity suite. The single
visualization that conveys this across attention budgets is a dependence × cost
scatter with the top-five set highlighted and the pre-registered caps drawn as
reference lines.

Outputs (PNG raster + SVG vector):
  generated/charts/remittance-fragility-scatter.{png,svg}

Input (read-only; deterministic):
  generated/remittance-resilience-adb-panel.csv

What this does NOT do:
  - Generate any number not in the input CSV (no imputation).
  - Recompute the fragility index (that comes from process-remittance.py).
  - Produce a country-quality ranking. Per `CONSTITUTION.md` §13.3, the
    framing is corridor-cost-stress observability, not a policy quality
    judgment. The chart visualizes a set-stability claim, not a rank.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)
PANEL_CSV = GEN / "remittance-resilience-adb-panel.csv"

# Pre-registered top-5 set (stable across the full ±50% sensitivity suite,
# including a multiplicative→additive aggregation switch).
TOP5 = {"KGZ", "NPL", "TON", "VUT", "WSM"}

# Pre-registered caps used in the fragility-index calibration. Both were
# perturbed at ±50%; the top-5 set did not change in any row of the suite.
DEP_CAP = 25.0  # % GDP
COST_CAP = 15.0  # %

# SDG target 10.c.1 reference value (countries should reduce remittance costs
# toward 3%; this paper does not evaluate progress against the SDG target —
# it is shown as a policy reference line only).
SDG_TARGET = 3.0  # %

# DMCs to label inline with the iso3. Top-5 always labeled; others labeled
# when the point would otherwise be unidentifiable in the cluster.
NOTABLE = {
    "KGZ", "NPL", "TON", "VUT", "WSM",
    "TJK", "PAK", "BGD", "PHL", "IND", "CHN", "MMR", "KHM", "LKA", "IDN", "LAO",
}

SOURCE_FOOTER = (
    "Source: World Bank Remittance Prices Worldwide Q1 2025 (corridor-firm prices); "
    "World Bank WDI BX.TRF.PWKR.DT.GD.ZS (personal remittances % GDP, latest year per DMC). "
    "See remittance-resilience/{REPRODUCE.md, results.md, sensitivity.md}. "
    "attestation_chain: ai-first under CONSTITUTION.md §18."
)


def load_panel() -> list[dict]:
    rows: list[dict] = []
    with PANEL_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            wdi_raw = r.get("wdi_remittance_pct_gdp")
            cost_raw = r.get("rpw_mean_cost_pct")
            corridors_raw = r.get("rpw_corridors_observed") or "0"
            firms_raw = r.get("rpw_firms_observed") or "0"
            if not wdi_raw or not cost_raw:
                continue
            try:
                wdi = float(wdi_raw)
                cost = float(cost_raw)
                corridors = int(corridors_raw) if corridors_raw else 0
                firms = int(firms_raw) if firms_raw else 0
            except ValueError:
                continue
            if cost <= 0:
                # Drop outlier-driven negative means (Fiji at -1.28% across a
                # -134.0 to 21.02 range). Documented in limitations.md as a
                # publicly-quoted-price-floor artifact.
                continue
            rows.append({
                "iso3": r["iso3"],
                "country": r["country"],
                "wdi": wdi,
                "cost": cost,
                "corridors": corridors,
                "firms": firms,
            })
    return rows


def build_scatter(rows: list[dict]) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11.0, 7.5))

    # Reference lines first so points sit on top.
    ax.axhline(SDG_TARGET, color="#7f8c8d", linestyle=":", linewidth=0.9, alpha=0.85, zorder=1)
    ax.axhline(COST_CAP, color="#bdc3c7", linestyle="--", linewidth=0.8, alpha=0.7, zorder=1)
    ax.axvline(DEP_CAP, color="#bdc3c7", linestyle="--", linewidth=0.8, alpha=0.7, zorder=1)

    # Reference-line labels.
    ax.text(0.6, SDG_TARGET + 0.4, f"SDG 10.c.1 reference: {int(SDG_TARGET)}% cost",
            fontsize=8, color="#7f8c8d", ha="left", va="bottom", zorder=2)
    ax.text(0.6, COST_CAP + 0.4, f"Pre-registered cost cap: {int(COST_CAP)}%",
            fontsize=8, color="#95a5a6", ha="left", va="bottom", zorder=2)
    ax.text(DEP_CAP + 0.5, 0.6, f"Pre-registered dependence cap: {int(DEP_CAP)}% GDP",
            fontsize=8, color="#95a5a6", ha="left", va="bottom", rotation=90, zorder=2)

    # Bubble size scales with RPW corridors observed (the small-sample caveat
    # made visually loud — Pacific entries and KGZ appear as small bubbles).
    def size_for(c: int) -> float:
        return max(40.0, min(420.0, 30.0 + 30.0 * c))

    top5_rows = [r for r in rows if r["iso3"] in TOP5]
    other_rows = [r for r in rows if r["iso3"] not in TOP5]

    ax.scatter(
        [r["wdi"] for r in other_rows],
        [r["cost"] for r in other_rows],
        s=[size_for(r["corridors"]) for r in other_rows],
        c="#bbcedd", edgecolor="#5e7c95", linewidth=0.6, alpha=0.85, zorder=3,
    )

    ax.scatter(
        [r["wdi"] for r in top5_rows],
        [r["cost"] for r in top5_rows],
        s=[size_for(r["corridors"]) for r in top5_rows],
        c="#c0392b", edgecolor="#5a1a12", linewidth=1.0, alpha=0.95, zorder=5,
    )

    # Inline labels.
    for r in rows:
        if r["iso3"] not in NOTABLE:
            continue
        in_top5 = r["iso3"] in TOP5
        ax.annotate(
            r["iso3"],
            xy=(r["wdi"], r["cost"]),
            xytext=(8 if in_top5 else 6, 4 if in_top5 else 3),
            textcoords="offset points",
            fontsize=9.5 if in_top5 else 8,
            color="#5a1a12" if in_top5 else "#33445a",
            fontweight="semibold" if in_top5 else "normal",
            zorder=6,
        )

    # Axes.
    ax.set_xlabel("Personal remittances received, % GDP (WDI, latest year)", fontsize=10)
    ax.set_ylabel("Mean inbound transfer cost, % (RPW, Q1 2025)", fontsize=10)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, color="#ecf0f1", linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)

    # Title and subtitle.
    fig.suptitle(
        "Where remittance dependence and corridor cost both run high",
        fontsize=14, fontweight="semibold", x=0.125, ha="left", y=0.965,
    )
    fig.text(
        0.125, 0.925,
        "Five DMCs — Kyrgyz Republic, Nepal, Tonga, Vanuatu, Samoa — sit in the top five of the joint exposure "
        "screen and stay there across the ±50% sensitivity suite. Bubble size = RPW corridors observed; small "
        "bubbles (Pacific entries and KGZ) carry a small-sample caveat.",
        fontsize=9, color="#444", ha="left", va="top", wrap=True,
    )

    # Legend.
    top5_patch = mpatches.Patch(color="#c0392b", label="Stable top-5 set (set is the headline; rank inside is not)")
    other_patch = mpatches.Patch(color="#bbcedd", label="Other rankable ADB DMCs")
    ax.legend(handles=[top5_patch, other_patch], loc="upper right", fontsize=9, framealpha=0.95)

    # Source footer (single-line wrap).
    fig.text(0.125, 0.015, SOURCE_FOOTER, fontsize=7, color="#7f8c8d", ha="left", va="bottom", wrap=True)

    fig.tight_layout(rect=(0.0, 0.045, 1.0, 0.88))
    return fig


def main() -> None:
    rows = load_panel()
    if not rows:
        raise SystemExit("No rankable rows in the panel CSV. Run process-remittance.py first.")
    fig = build_scatter(rows)
    png_path = CHARTS / "remittance-fragility-scatter.png"
    svg_path = CHARTS / "remittance-fragility-scatter.svg"
    fig.savefig(png_path, dpi=180, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {png_path} ({len(rows)} rankable DMCs)")
    print(f"Wrote {svg_path} ({len(rows)} rankable DMCs)")


if __name__ == "__main__":
    main()
