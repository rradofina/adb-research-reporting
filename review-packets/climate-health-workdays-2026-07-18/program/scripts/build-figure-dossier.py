"""Build the climate-health construct-validation figure dossier.

All charts read generated evidence.  They test the old PM2.5 proxy against
the Lancet Countdown heat-work-loss construct, show the denominator repair,
and keep modelled potential loss separate from observed absence.

attestation_chain: ai-first
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from adjustText import adjust_text


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"
VALIDATION = GEN / "climate-health-construct-validation.json"
PANEL = GEN / "climate-health-heat-workloss-panel.csv"
COMPARISON = GEN / "climate-health-proxy-heat-comparison.csv"
SENSITIVITY = ROOT / "sensitivity-runs.json"
SUMMARY = GEN / "climate-health-figure-dossier-summary.json"

ADB_BLUE = "#007DB8"
ADB_NAVY = "#002569"
ADB_GOLD = "#B07D12"
ADB_RED = "#A63D40"
ADB_GREEN = "#2C7A64"
INK = "#20262E"
INK_SOFT = "#5C6670"
RULE = "#D9DEE2"
PALE = "#EEF2F4"
WHITE = "#FFFFFF"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_figure(fig: plt.Figure, stem: str) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{stem}.png", dpi=200, bbox_inches="tight", facecolor=WHITE)
    fig.savefig(CHARTS / f"{stem}.svg", bbox_inches="tight", facecolor=WHITE)
    svg_path = CHARTS / f"{stem}.svg"
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def clean_axes(ax: plt.Axes, axis: str = "x") -> None:
    ax.grid(axis=axis, color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)


def add_source(fig: plt.Figure, text: str) -> None:
    fig.text(0.055, 0.025, text, ha="left", va="bottom", fontsize=7.0, color=INK_SOFT, wrap=True)


def render_rank_disagreement(comparison: pd.DataFrame) -> None:
    rows = comparison[comparison["year"] == comparison["year"].max()].copy()
    selected = {"IND", "AFG", "BGD", "KHM", "MMR", "THA"}
    colors = {
        "IND": ADB_BLUE,
        "AFG": ADB_RED,
        "BGD": ADB_GOLD,
        "KHM": ADB_GREEN,
        "MMR": ADB_NAVY,
        "THA": "#6F5A9A",
    }

    fig, ax = plt.subplots(figsize=(11.8, 7.8))
    fig.subplots_adjust(left=0.19, right=0.81, top=0.80, bottom=0.14)
    for _, row in rows.sort_values("proxy_rank").iterrows():
        iso = row["iso3"]
        color = colors.get(iso, RULE)
        width = 2.5 if iso in selected else 0.8
        alpha = 0.95 if iso in selected else 0.55
        ax.plot([0, 1], [row["proxy_rank"], row["heat_rank"]], color=color, linewidth=width, alpha=alpha)
        ax.scatter([0, 1], [row["proxy_rank"], row["heat_rank"]], s=42 if iso in selected else 15,
                   color=color, edgecolor=WHITE, linewidth=0.6, zorder=3, alpha=alpha)
        if iso in selected:
            ax.text(-0.035, row["proxy_rank"], f"{row['country']}  #{int(row['proxy_rank'])}",
                    ha="right", va="center", fontsize=9.1, color=INK)
            ax.text(1.035, row["heat_rank"], f"#{int(row['heat_rank'])}  {row['country']}",
                    ha="left", va="center", fontsize=9.1, color=INK)

    ax.set_xlim(-0.39, 1.39)
    ax.set_ylim(35, 0)
    ax.set_xticks([0, 1], ["PM2.5 × outdoor-employment proxy", "Heat-related potential hours lost"])
    ax.set_yticks([1, 5, 10, 20, 30, 34])
    ax.tick_params(axis="x", length=0, labelsize=10, colors=INK)
    ax.tick_params(axis="y", length=0, colors=INK_SOFT)
    clean_axes(ax, "y")
    fig.suptitle(
        "The PM2.5 proxy does not recover the heat-work-loss ordering",
        x=0.055, y=0.97, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.055, 0.895,
        "Aligned 2020 data across 34 economies: the top threes have zero overlap and the full-rank Spearman correlation is 0.17.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: climate-health-proxy-heat-comparison.csv; World Bank WDI and Lancet Countdown 2025 indicator 1.1.3. The right side is modelled potential heat-related work-hours loss per employed person, not observed absence. attestation_chain: ai-first.",
    )
    save_figure(fig, "climate-construct-rank-disagreement")


def render_sensitivity_heatmap(sensitivity: dict) -> None:
    tests = pd.DataFrame(sensitivity["tests"])
    variant_order = sensitivity["variants"]
    year_order = sorted(tests["year"].unique())
    matrix = np.array([
        [int(tests[(tests["year"] == year) & (tests["variant"] == variant)]["top3_overlap_count"].iloc[0])
         for variant in variant_order]
        for year in year_order
    ])
    labels = [
        "Baseline", "Industry weight −50%", "Industry weight +50%",
        "PM2.5 floor −50%", "PM2.5 floor +50%", "PM2.5 cap −50%", "PM2.5 cap +50%",
    ]

    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    fig.subplots_adjust(left=0.11, right=0.94, top=0.73, bottom=0.25)
    cmap = plt.matplotlib.colors.ListedColormap([ADB_RED, ADB_GOLD, ADB_BLUE, ADB_GREEN])
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=3, aspect="auto")
    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            value = matrix[row_index, column_index]
            ax.text(column_index, row_index, f"{value} of 3", ha="center", va="center",
                    color=WHITE if value == 0 else INK, fontsize=10.3, weight="semibold")
    ax.set_xticks(range(len(labels)), labels, rotation=24, ha="right")
    ax.set_yticks(range(len(year_order)), [str(year) for year in year_order])
    ax.tick_params(length=0, labelsize=9.2)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.suptitle(
        "No parameter choice recovers more than one heat-loss top-three economy",
        x=0.055, y=0.97, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.055, 0.865,
        "Sixteen of 21 aligned year × parameter tests have zero overlap; the other five overlap on one economy.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: sensitivity-runs.json generated from aligned annual WDI and Lancet Countdown data. Each arbitrary proxy parameter is tested at ±50% per Constitution §6.6. attestation_chain: ai-first.",
    )
    save_figure(fig, "climate-construct-sensitivity")


def render_heat_loss_profile(panel: pd.DataFrame) -> None:
    rows = panel.dropna(subset=["potential_heat_lost_hours_per_employed_person"]).nsmallest(
        13, "heat_rank_per_worker"
    ).sort_values("potential_heat_lost_hours_per_employed_person")
    values = rows["potential_heat_lost_hours_per_employed_person"].to_numpy()
    colors = [ADB_BLUE if iso in {"KHM", "IND", "PAK"} else PALE for iso in rows["iso3"]]
    y = np.arange(len(rows))

    fig, ax = plt.subplots(figsize=(11.8, 7.0))
    fig.subplots_adjust(left=0.20, right=0.94, top=0.78, bottom=0.17)
    bars = ax.barh(y, values, color=colors, edgecolor=ADB_BLUE, linewidth=0.8, height=0.62)
    for bar, value in zip(bars, values, strict=True):
        ax.text(value + 9, bar.get_y() + bar.get_height() / 2, f"{value:.0f}",
                va="center", fontsize=9.2, color=INK)
    ax.set_yticks(y, rows["country"])
    ax.set_xlim(0, 640)
    ax.set_xlabel("Modelled potential heat-related work hours lost per employed person, 2024", color=INK_SOFT)
    ax.tick_params(axis="y", length=0, labelsize=9.3)
    ax.tick_params(axis="x", colors=INK_SOFT)
    clean_axes(ax)
    fig.suptitle(
        "Heat exposure implies large potential work-hour losses in several economies",
        x=0.055, y=0.97, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.055, 0.885,
        "The direct heat construct differs from the PM2.5 screen; Cambodia is first on the per-employed-person measure in 2024.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: Lancet Countdown 2025 indicator 1.1.3, climate-health-heat-workloss-panel.csv. Values are potential capacity loss from WBGT and sector workload, not time off work actually observed. attestation_chain: ai-first.",
    )
    save_figure(fig, "climate-heat-loss-profile-2024")


def render_rate_scale(panel: pd.DataFrame) -> None:
    rows = panel.dropna(
        subset=["potential_heat_lost_hours_per_employed_person", "potential_heat_lost_hours_millions"]
    ).copy()
    rows = rows[rows["potential_heat_lost_hours_millions"] > 0]
    worker_sizes = np.sqrt(rows["lancet_outdoor_workers_millions"].fillna(0.02)) * 58 + 20
    label_isos = {"KHM", "IND", "PAK", "CHN", "IDN", "BGD", "VNM", "THA", "MMR", "PHL"}

    fig, ax = plt.subplots(figsize=(11.8, 7.0))
    fig.subplots_adjust(left=0.10, right=0.94, top=0.78, bottom=0.17)
    ax.scatter(
        rows["potential_heat_lost_hours_per_employed_person"],
        rows["potential_heat_lost_hours_millions"],
        s=worker_sizes, color=ADB_BLUE, alpha=0.72, edgecolor=WHITE, linewidth=0.7,
    )
    labels = []
    for _, row in rows[rows["iso3"].isin(label_isos)].iterrows():
        labels.append(ax.text(
            row["potential_heat_lost_hours_per_employed_person"],
            row["potential_heat_lost_hours_millions"],
            row["country"],
            fontsize=8.7,
            color=INK,
        ))
    adjust_text(
        labels,
        ax=ax,
        x=rows["potential_heat_lost_hours_per_employed_person"].to_numpy(),
        y=rows["potential_heat_lost_hours_millions"].to_numpy(),
        expand=(1.08, 1.18),
        force_text=(0.35, 0.45),
        arrowprops={"arrowstyle": "-", "color": INK_SOFT, "lw": 0.55},
    )
    ax.set_yscale("log")
    ax.set_xlim(0, 640)
    ax.set_xlabel("Potential heat-loss hours per employed person, 2024", color=INK_SOFT)
    ax.set_ylabel("Total potential heat-loss hours, millions (log scale)", color=INK_SOFT)
    ax.tick_params(colors=INK_SOFT)
    clean_axes(ax, "both")
    fig.suptitle(
        "Heat-loss rate and aggregate burden answer different planning questions",
        x=0.055, y=0.97, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.055, 0.885,
        "India carries the largest aggregate modelled burden; Cambodia has the highest rate per employed person. Bubble area reflects outdoor workers.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: Lancet Countdown 2025 indicator 1.1.3 potential work-hours loss and outdoor-worker workbooks. National sector shares are applied within grids and informal unpaid work is excluded. attestation_chain: ai-first.",
    )
    save_figure(fig, "climate-heat-loss-rate-vs-scale")


def render_denominator_repair(panel: pd.DataFrame) -> None:
    rows = panel[panel["iso3"].isin(["AFG", "IND", "BGD"])].copy()
    rows = rows.set_index("country").loc[["Afghanistan", "India", "Bangladesh"]].reset_index()
    old_ratio = (
        rows["wdi_total_population_proxy_outdoor_workers_millions"]
        / rows["lancet_outdoor_workers_millions"]
    )
    repaired_ratio = (
        rows["wdi_repaired_outdoor_workers_millions"]
        / rows["lancet_outdoor_workers_millions"]
    )
    y = np.arange(len(rows))
    height = 0.28

    fig, ax = plt.subplots(figsize=(11.8, 5.9))
    fig.subplots_adjust(left=0.15, right=0.94, top=0.73, bottom=0.22)
    bars_old = ax.barh(y - height / 2, old_ratio, height=height, color=ADB_RED,
                       label="Old total-population calculation")
    bars_repaired = ax.barh(y + height / 2, repaired_ratio, height=height, color=ADB_BLUE,
                            label="Employed-15+ denominator repair")
    ax.axvline(1, color=INK, linewidth=1.2)
    for bars, ratios in [(bars_old, old_ratio), (bars_repaired, repaired_ratio)]:
        for bar, ratio in zip(bars, ratios, strict=True):
            ax.text(bar.get_width() + 0.07, bar.get_y() + bar.get_height() / 2,
                    f"{ratio:.2f}×", va="center", fontsize=9.3, color=INK)
    ax.set_yticks(y, rows["country"])
    ax.invert_yaxis()
    ax.set_xlim(0, 5.8)
    ax.set_xlabel("Calculated outdoor-worker count ÷ Lancet/WHO modelled count", color=INK_SOFT)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    clean_axes(ax)
    fig.suptitle(
        "The employed-adult denominator repairs most of the worker-count error",
        x=0.055, y=0.97, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.055, 0.855,
        "The old method multiplies an employment share by total population; the repair applies it to employed people aged 15+.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: climate-health-heat-workloss-panel.csv; WDI denominator audit and Lancet Countdown outdoor-worker workbook. The Lancet count is modelled, not a census benchmark. attestation_chain: ai-first.",
    )
    save_figure(fig, "climate-worker-denominator-repair")


def render_sector_composition(panel: pd.DataFrame) -> None:
    rows = panel.dropna(subset=["heat_rank_per_worker"]).nsmallest(10, "heat_rank_per_worker").copy()
    components = [
        ("service_lost_hours", "Services", ADB_NAVY),
        ("manufacturing_lost_hours", "Manufacturing", ADB_BLUE),
        ("agriculture_lost_hours", "Agriculture", ADB_GOLD),
        ("construction_lost_hours", "Construction", ADB_RED),
    ]
    totals = rows[[key for key, _, _ in components]].sum(axis=1)
    y = np.arange(len(rows))

    fig, ax = plt.subplots(figsize=(11.8, 7.0))
    fig.subplots_adjust(left=0.17, right=0.94, top=0.77, bottom=0.19)
    left = np.zeros(len(rows))
    for key, label, color in components:
        share = rows[key].to_numpy() / totals.to_numpy() * 100
        ax.barh(y, share, left=left, height=0.62, color=color, label=label)
        left += share
    for position, share in zip(y, rows["agriculture_construction_share_pct"], strict=True):
        ax.text(99, position, f"{share:.0f}% ag+constr", ha="right", va="center",
                fontsize=8.6, color=WHITE, weight="semibold")
    ax.set_yticks(y, rows["country"])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of modelled potential heat-loss hours, 2024 (%)", color=INK_SOFT)
    ax.tick_params(axis="y", length=0, labelsize=9.3)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.19), fontsize=9)
    clean_axes(ax)
    fig.suptitle(
        "Agriculture and construction dominate potential heat-loss hours",
        x=0.055, y=0.97, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.055, 0.88,
        "Sector workload and sun exposure are part of the heat construct; the old PM2.5 proxy used only agriculture plus a half-weighted industry share.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: Lancet Countdown 2025 indicator 1.1.3. Sector losses combine WBGT with assumed metabolic workload and national employment shares; they do not observe individual schedules. attestation_chain: ai-first.",
    )
    save_figure(fig, "climate-heat-loss-sector-composition")


def render_source_coverage(validation: dict) -> None:
    total = validation["roster_dmcs"]
    labels = [
        "WDI proxy rankable",
        "Lancet heat-loss estimate",
        "Lancet outdoor-worker estimate",
        "Observed absence / hours outcome joined",
    ]
    values = [34, validation["latest_heat_dmcs"], validation["latest_outdoor_worker_dmcs"], 0]
    colors = [ADB_RED, ADB_BLUE, ADB_GREEN, PALE]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    fig.subplots_adjust(left=0.28, right=0.94, top=0.72, bottom=0.23)
    bars = ax.barh(y, values, height=0.58, color=colors, edgecolor=RULE)
    for bar, value in zip(bars, values, strict=True):
        ax.text(max(value + 0.6, 1.0), bar.get_y() + bar.get_height() / 2,
                f"{value}/{total}", va="center", fontsize=10, color=INK, weight="semibold")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 47)
    ax.set_xlabel("Economies in the 44-economy analysis roster", color=INK_SOFT)
    ax.tick_params(axis="y", length=0, labelsize=9.3)
    ax.tick_params(axis="x", colors=INK_SOFT)
    clean_axes(ax)
    fig.suptitle(
        "The heat source closes the construct gap, not the outcome-validation gap",
        x=0.055, y=0.97, ha="left", fontsize=18, color=INK, weight="semibold",
    )
    fig.text(
        0.055, 0.85,
        "Potential capacity loss is available for 43 economies; this package still joins no observed absenteeism or hours-worked outcome.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: climate-health-construct-validation.json. Zero means no outcome is joined in this package, not that no economy publishes any labor outcome. Taipei,China is absent from the heat workbook; Hong Kong, China and Taipei,China are absent from the outdoor-worker workbook. attestation_chain: ai-first.",
    )
    save_figure(fig, "climate-source-coverage")


def main() -> None:
    validation = load_json(VALIDATION)
    sensitivity = load_json(SENSITIVITY)
    panel = pd.read_csv(PANEL)
    comparison = pd.read_csv(COMPARISON)

    render_rank_disagreement(comparison)
    render_sensitivity_heatmap(sensitivity)
    render_heat_loss_profile(panel)
    render_rate_scale(panel)
    render_denominator_repair(panel)
    render_sector_composition(panel)
    render_source_coverage(validation)

    summary = {
        "program": "climate-health-workdays",
        "attestation_chain": "ai-first",
        "finding": validation["claim"],
        "source_inputs": [
            str(VALIDATION.relative_to(ROOT)),
            str(PANEL.relative_to(ROOT)),
            str(COMPARISON.relative_to(ROOT)),
            str(SENSITIVITY.relative_to(ROOT)),
        ],
        "figures": [
            "climate-construct-rank-disagreement",
            "climate-construct-sensitivity",
            "climate-heat-loss-profile-2024",
            "climate-heat-loss-rate-vs-scale",
            "climate-worker-denominator-repair",
            "climate-heat-loss-sector-composition",
            "climate-source-coverage",
        ],
        "non_claim": (
            "The dossier does not interpret modelled potential work-hours loss as observed absence, "
            "does not combine PM2.5 and heat into a new index, and does not rank policy performance."
        ),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {SUMMARY.relative_to(ROOT)} and seven chart pairs")


if __name__ == "__main__":
    main()
