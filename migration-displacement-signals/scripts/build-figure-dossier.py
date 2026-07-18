"""Build the migration denominator-switch figure dossier.

All figures read committed generated evidence and make no network calls.
They distinguish cumulative migrant stock, population-normalized stock,
destination concentration, and the UNHCR forced-displacement component.

Outputs:
  generated/charts/migration-rank-inversion.{png,svg}
  generated/charts/migration-population-share-profile.{png,svg}
  generated/charts/migration-corridor-concentration.{png,svg}
  generated/charts/migration-forced-displacement-composition.{png,svg}
  generated/charts/migration-source-observability.{png,svg}
  generated/migration-figure-dossier-summary.json

attestation_chain: ai-first.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"
PER_POP_PATH = GEN / "migration-per-population-deepening.json"
PANEL_PATH = GEN / "migration-displacement-adb-panel.json"
FORCED_PATH = GEN / "migration-corridor-type-forced-displacement.json"
SENSITIVITY_PATH = ROOT / "sensitivity-runs.json"
SUMMARY_PATH = GEN / "migration-figure-dossier-summary.json"

ADB_BLUE = "#007DB8"
ADB_NAVY = "#002569"
ADB_GOLD = "#B07D12"
ADB_RED = "#A63D40"
ADB_GREEN = "#2C7A64"
INK = "#20262E"
INK_SOFT = "#5C6670"
RULE = "#D9DEE2"
PALE = "#EEF2F4"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_figure(fig: plt.Figure, stem: str) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    png_path = CHARTS / f"{stem}.png"
    svg_path = CHARTS / f"{stem}.svg"
    fig.savefig(png_path, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def clean_axes(ax: plt.Axes, axis: str = "x") -> None:
    ax.grid(axis=axis, color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)


def add_source(fig: plt.Figure, text: str) -> None:
    fig.text(0.06, 0.025, text, ha="left", va="bottom", fontsize=7.1, color=INK_SOFT, wrap=True)


def render_rank_inversion(per_pop: dict) -> None:
    rows = {row["iso3"]: row for row in per_pop["rows_by_share"]}
    absolute = list(per_pop["absolute_top5"])
    share = list(per_pop["share_top5"])
    union = absolute + [iso for iso in share if iso not in absolute]

    fig, ax = plt.subplots(figsize=(11.8, 7.6))
    fig.subplots_adjust(left=0.16, right=0.84, top=0.79, bottom=0.15)
    for iso in union:
        row = rows[iso]
        left = row["rank_absolute"]
        right = row["rank_share"]
        color = ADB_RED if iso in absolute else ADB_BLUE
        ax.plot([0, 1], [left, right], color=color, linewidth=2.2, alpha=0.78)
        ax.scatter([0, 1], [left, right], s=48, color=color, zorder=3, edgecolor="white", linewidth=0.7)
        ax.text(-0.035, left, f"#{left}  {row['country']}", ha="right", va="center", fontsize=9.2, color=INK)
        ax.text(1.035, right, f"{row['country']}  #{right}", ha="left", va="center", fontsize=9.2, color=INK)

    ax.set_xlim(-0.42, 1.42)
    ax.set_ylim(42, 0)
    ax.set_xticks([0, 1], ["Absolute stock rank", "Stock ÷ population rank"])
    ax.set_yticks([1, 5, 10, 20, 30, 40])
    ax.tick_params(axis="x", length=0, labelsize=10, colors=INK)
    ax.tick_params(axis="y", length=0, colors=INK_SOFT)
    ax.grid(axis="y", color=RULE, linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.suptitle(
        "The absolute and population-share top fives have zero overlap",
        x=0.06, y=0.965, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.06, 0.89,
        "Red lines start in the absolute top five; blue lines enter only after dividing stock by 2024 resident population.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed migration-per-population-deepening.json; UN DESA International Migrant Stock 2024 and World Bank WDI SP.POP.TOTL 2024. Three panel economies without a WDI denominator are withheld. Stock is cumulative, not an annual flow. attestation_chain: ai-first.",
    )
    save_figure(fig, "migration-rank-inversion")


def render_population_share(per_pop: dict) -> None:
    rows = list(reversed(per_pop["rows_by_share"][:12]))
    y = np.arange(len(rows))
    values = [row["emigrant_pct_of_population"] for row in rows]
    colors = [ADB_BLUE if row["iso3"] in per_pop["share_top5"] else PALE for row in rows]

    fig, ax = plt.subplots(figsize=(11.8, 7.0))
    fig.subplots_adjust(left=0.21, right=0.94, top=0.78, bottom=0.17)
    bars = ax.barh(y, values, height=0.62, color=colors, edgecolor=ADB_BLUE, linewidth=0.8)
    for bar, row in zip(bars, rows, strict=True):
        ax.text(
            bar.get_width() + 0.8,
            bar.get_y() + bar.get_height() / 2,
            f"{row['emigrant_pct_of_population']:.1f}%",
            va="center", fontsize=9.1, color=INK,
        )
    ax.set_yticks(y, [row["country"] for row in rows])
    ax.tick_params(axis="y", length=0, labelsize=9.4)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.set_xlabel("UN DESA emigrant stock as a share of WDI 2024 resident population", color=INK_SOFT)
    ax.set_xlim(0, 61)
    clean_axes(ax)
    fig.suptitle(
        "Samoa and Tonga exceed 50% on the population-share measure",
        x=0.06, y=0.965, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.06, 0.885,
        "The chart describes cumulative diaspora stock relative to the resident population; it does not estimate departures in 2024.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed migration-per-population-deepening.json. UN DESA migrant stock can span decades and migration purposes. WDI population is a mid-year de facto resident denominator. attestation_chain: ai-first.",
    )
    save_figure(fig, "migration-population-share-profile")


def render_corridor_concentration(sensitivity: dict) -> None:
    rows = sensitivity["corridor_concentration"]["rows"]
    labels = [row["country"] for row in rows]
    x = np.arange(len(rows))
    styles = [("top_2", "Top 2", ADB_NAVY), ("top_3", "Top 3", ADB_BLUE), ("top_5", "Top 5", ADB_GOLD)]

    fig, ax = plt.subplots(figsize=(11.8, 6.6))
    fig.subplots_adjust(left=0.10, right=0.94, top=0.77, bottom=0.19)
    for key, label, color in styles:
        values = [100 * row[key] for row in rows]
        ax.plot(x, values, marker="o", markersize=7, linewidth=2.0, label=label, color=color)
    ax.axhline(50, color=ADB_RED, linewidth=1.1, linestyle="--")
    ax.text(4.42, 51.5, "50% heuristic", ha="right", va="bottom", fontsize=8.8, color=ADB_RED)
    ax.set_xticks(x, labels)
    ax.set_ylim(25, 105)
    ax.set_ylabel("Share of emigrant stock in top destinations (%)", color=INK_SOFT)
    ax.tick_params(axis="x", length=0, labelsize=9.4)
    ax.tick_params(axis="y", colors=INK_SOFT)
    ax.legend(frameon=False, loc="lower right", ncol=3, fontsize=9)
    clean_axes(ax, "y")
    fig.suptitle(
        "Corridor concentration changes with the number of destinations counted",
        x=0.06, y=0.965, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.06, 0.885,
        "The original 50% split is a secondary descriptive result: all five clear 25%, while only Afghanistan clears 75% at top three.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed migration-displacement-adb-panel.json and sensitivity-runs.json; UN DESA 2024 bilateral stock. Corridor shares mix labor, family, student, refugee, and historical migration. attestation_chain: ai-first.",
    )
    save_figure(fig, "migration-corridor-concentration")


def render_forced_composition(per_pop: dict, forced: dict) -> None:
    by_iso = {row["iso3"]: row for row in forced["country_rows"]}
    order = ["AFG", *per_pop["share_top5"]]
    labels = [by_iso[iso]["country"] for iso in order]
    forced_pct = np.array([float(by_iso[iso]["forced_abroad_pct_of_emigrant_stock"] or 0) for iso in order])
    residual = 100 - forced_pct
    y = np.arange(len(order))

    fig, ax = plt.subplots(figsize=(11.8, 6.5))
    fig.subplots_adjust(left=0.17, right=0.94, top=0.76, bottom=0.20)
    ax.barh(y, forced_pct, color=ADB_RED, height=0.62, label="UNHCR forced-displacement stock")
    ax.barh(y, residual, left=forced_pct, color=PALE, edgecolor=RULE, height=0.62, label="Other or unclassified migrant stock")
    for pos, value in zip(y, forced_pct, strict=True):
        ax.text(min(value + 1.1, 91), pos, f"{value:.1f}%", va="center", fontsize=9.1, color=INK, weight="semibold")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of UN DESA emigrant stock (%)", color=INK_SOFT)
    ax.tick_params(axis="y", length=0, labelsize=9.4)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    clean_axes(ax)
    fig.suptitle(
        "Afghanistan is a different mobility object from the share top five",
        x=0.06, y=0.965, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.06, 0.88,
        "UNHCR forced-displacement stock is 81.7% of Afghanistan's emigrant stock; every population-share top-five economy is below 6%.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed migration-corridor-type-forced-displacement.json; UNHCR Refugee Data Finder 2024 and UN DESA 2024. The residual is not a labor-migration estimate; it includes family, student, temporary, historical, and other unclassified stock. attestation_chain: ai-first.",
    )
    save_figure(fig, "migration-forced-displacement-composition")


def render_source_observability(per_pop: dict, forced: dict) -> None:
    panel_total = int(forced["summary"]["origins_queried"])
    denominator_rows = len(per_pop["rows_by_share"])
    forced_rows = int(forced["summary"]["origins_with_forced_abroad_rows"])
    labels = ["UN DESA stock rows", "WDI denominator available", "At least one UNHCR forced-abroad row"]
    values = [panel_total, denominator_rows, forced_rows]
    colors = [ADB_NAVY, ADB_BLUE, ADB_GOLD]
    y = np.arange(3)

    fig, ax = plt.subplots(figsize=(11.8, 5.9))
    fig.subplots_adjust(left=0.31, right=0.94, top=0.73, bottom=0.23)
    bars = ax.barh(y, values, height=0.56, color=colors)
    for bar, value in zip(bars, values, strict=True):
        ax.text(value + 0.5, bar.get_y() + bar.get_height() / 2, f"{value}/{panel_total}", va="center", fontsize=10, color=INK, weight="semibold")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 48)
    ax.set_xlabel("Economies in the committed program panel", color=INK_SOFT)
    ax.tick_params(axis="y", length=0, labelsize=9.4)
    ax.tick_params(axis="x", colors=INK_SOFT)
    clean_axes(ax)
    withheld = ", ".join(row["iso3"] for row in per_pop["rows_withheld_no_population"])
    fig.suptitle(
        "The joined sources answer different parts of the migration question",
        x=0.06, y=0.965, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.06, 0.865,
        f"Population shares are withheld for {withheld}. UNHCR can identify forced displacement but cannot classify the remaining migration purposes.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed UN DESA panel, WDI denominator audit, and UNHCR corridor-type audit. A missing forced-abroad row is not proof of zero displacement; source visibility and construct coverage differ. attestation_chain: ai-first.",
    )
    save_figure(fig, "migration-source-observability")


def main() -> None:
    per_pop = load_json(PER_POP_PATH)
    panel = load_json(PANEL_PATH)
    forced = load_json(FORCED_PATH)
    sensitivity = load_json(SENSITIVITY_PATH)

    render_rank_inversion(per_pop)
    render_population_share(per_pop)
    render_corridor_concentration(sensitivity)
    render_forced_composition(per_pop, forced)
    render_source_observability(per_pop, forced)

    baseline = sensitivity["baseline_decision"]
    summary = {
        "program": "migration-displacement-signals",
        "attestation_chain": "ai-first",
        "source_inputs": [
            str(PER_POP_PATH.relative_to(ROOT)),
            str(PANEL_PATH.relative_to(ROOT)),
            str(FORCED_PATH.relative_to(ROOT)),
            str(SENSITIVITY_PATH.relative_to(ROOT)),
        ],
        "panel_rows": len(panel["rows"]),
        "population_denominator_rows": len(per_pop["rows_by_share"]),
        "withheld_denominators": per_pop["rows_withheld_no_population"],
        "absolute_top5": baseline["absolute_top5"],
        "population_share_top5": baseline["population_share_top5"],
        "top5_overlap_count": baseline["overlap_count"],
        "top5_overlap_share": baseline["overlap_share"],
        "top_n_sensitivity": sensitivity["denominator_switch"],
        "afghanistan_forced_abroad_pct_of_emigrant_stock": forced["summary"]["afghanistan_forced_abroad_pct_of_emigrant_stock"],
        "share_top5_forced_displacement_majority": forced["summary"]["share_top5_forced_displacement_majority"],
        "finding": (
            "The absolute and population-share top fives have zero overlap. "
            "Afghanistan, the near-rank exception at share rank six, is a forced-displacement-majority origin; "
            "the population-share top five is not."
        ),
        "non_claim": (
            "The dossier does not estimate current migration flows, migration propensity, labor-migration purpose, "
            "internal displacement, welfare, or causal drivers."
        ),
        "figures": [
            "migration-rank-inversion",
            "migration-population-share-profile",
            "migration-corridor-concentration",
            "migration-forced-displacement-composition",
            "migration-source-observability",
        ],
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {SUMMARY_PATH.relative_to(ROOT)} and five chart pairs")


if __name__ == "__main__":
    main()
