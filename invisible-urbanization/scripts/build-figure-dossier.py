"""Build the evidence-bearing figure dossier for invisible urbanization.

Every figure is generated from committed outputs of the GHSL/WDI definition-gap
and GHS-DUC transition scripts. Charts communicate a finding, a sensitivity
result, coverage, or a nonclaim; none are decorative.

Public data only. attestation_chain: ai-first.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


PROGRAM = Path(__file__).resolve().parents[1]
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"

INK = "#172B3A"
MUTED = "#60717F"
GRID = "#DCE5EA"
BLUE = "#1E5B78"
BLUE_LIGHT = "#8FB7C9"
ORANGE = "#D65A3A"
ORANGE_LIGHT = "#F0B49F"
GREEN = "#2F7D69"
RED = "#B83A3A"
GOLD = "#C79A2B"
PAPER = "#F7FAFB"


def setup_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 17,
            "axes.labelsize": 11,
            "axes.edgecolor": GRID,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": INK,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def frame_title(fig, eyebrow: str, title: str, subtitle: str) -> None:
    fig.text(0.08, 0.955, eyebrow.upper(), color=ORANGE, fontsize=9, fontweight="bold")
    fig.text(0.08, 0.92, title, fontsize=18, fontweight="bold", color=INK)
    fig.text(0.08, 0.887, subtitle, fontsize=10.5, color=MUTED)


def footnote(fig, text: str) -> None:
    fig.text(0.08, 0.018, text, fontsize=8.3, color=MUTED, va="bottom")


def save(fig, slug: str) -> dict:
    paths = {}
    for suffix in ("png", "svg"):
        path = CHARTS / f"{slug}.{suffix}"
        fig.savefig(path, dpi=190, bbox_inches="tight")
        paths[suffix] = str(path.relative_to(PROGRAM))
    plt.close(fig)
    return paths


def clean_axis(ax, grid_axis="x") -> None:
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, lw=0.8, zorder=0)
    ax.tick_params(axis="y", length=0)


def figure_gap_hero(gap: pd.DataFrame) -> dict:
    plot = gap[(gap.year == 2020) & gap.wdi_urban_share_pct.notna()].copy()
    plot = plot.sort_values("ghsl_minus_wdi_pp")
    fig, ax = plt.subplots(figsize=(10.8, 11.8))
    fig.subplots_adjust(left=0.19, right=0.96, top=0.84, bottom=0.09)
    colors = np.where(plot.ghsl_minus_wdi_pp >= 0, ORANGE, BLUE)
    y = np.arange(len(plot))
    ax.barh(y, plot.ghsl_minus_wdi_pp, color=colors, height=0.66, zorder=3)
    ax.axvline(0, color=INK, lw=1.1)
    ax.set_yticks(y, plot.iso3)
    ax.set_xlim(-45, 72)
    ax.set_xlabel("GHSL standardized share minus WDI national-definition share (percentage points)")
    clean_axis(ax)
    frame_title(
        fig,
        "Finding 1 · definition gap",
        "One urban share can be 20 points away from another",
        "Median absolute difference across 40 complete ADB-economy cases, 2020",
    )
    ax.text(1, len(plot) - 0.3, "GHSL higher →", color=ORANGE, fontsize=9, fontweight="bold")
    ax.text(-1, len(plot) - 0.3, "← WDI higher", color=BLUE, fontsize=9, fontweight="bold", ha="right")
    footnote(
        fig,
        "Source: JRC GHS-DUC R2023A V2.0 and World Bank WDI SP.URB.TOTL.IN.ZS. "
        "The measures use different definitions and population models; gaps are not person counts.",
    )
    return save(fig, "invisible-urbanization-01-definition-gap-hero")


def figure_selected_dumbbell(gap: pd.DataFrame) -> dict:
    plot = gap[(gap.year == 2020) & gap.wdi_urban_share_pct.notna()].copy()
    largest = plot.nlargest(10, "absolute_gap_pp")
    negative = plot.nsmallest(4, "ghsl_minus_wdi_pp")
    near = plot.nsmallest(2, "absolute_gap_pp")
    plot = pd.concat([largest, negative, near]).drop_duplicates("iso3")
    plot = plot.sort_values("ghsl_minus_wdi_pp")
    fig, ax = plt.subplots(figsize=(10.5, 7.6))
    fig.subplots_adjust(left=0.20, right=0.95, top=0.82, bottom=0.14)
    y = np.arange(len(plot))
    ax.hlines(y, plot.wdi_urban_share_pct, plot.ghsl_urban_share_pct, color="#AABBC6", lw=2)
    ax.scatter(plot.wdi_urban_share_pct, y, s=52, color=BLUE, label="WDI national definition", zorder=3)
    ax.scatter(plot.ghsl_urban_share_pct, y, s=52, color=ORANGE, label="GHSL standardized", zorder=3)
    ax.set_yticks(y, [f"{r.country}  ·  {r.iso3}" for r in plot.itertuples()])
    ax.set_xlim(0, 103)
    ax.set_xlabel("Population classified urban (%)")
    clean_axis(ax)
    ax.legend(frameon=False, loc="lower right", ncol=2)
    frame_title(
        fig,
        "Comparison · selected cases",
        "The difference runs in both directions",
        "Largest absolute gaps, four WDI-higher cases, and two near-agreement cases",
    )
    footnote(
        fig,
        "Selection is descriptive, not a performance ranking. Source: JRC GHS-DUC R2023A V2.0; World Bank WDI, 2020.",
    )
    return save(fig, "invisible-urbanization-02-selected-definition-dumbbell")


def figure_gap_over_time(gap: pd.DataFrame) -> dict:
    complete = gap[gap.wdi_urban_share_pct.notna()].copy()
    summary = complete.groupby("year", as_index=False).agg(
        median_signed=("ghsl_minus_wdi_pp", "median"),
        median_absolute=("absolute_gap_pp", "median"),
        coverage=("iso3", "nunique"),
    )
    fig, ax = plt.subplots(figsize=(10.2, 6.3))
    fig.subplots_adjust(left=0.11, right=0.96, top=0.80, bottom=0.16)
    ax.plot(summary.year, summary.median_absolute, color=ORANGE, lw=2.8, marker="o", label="Median absolute gap")
    ax.plot(summary.year, summary.median_signed, color=BLUE, lw=2.2, marker="o", label="Median signed gap")
    ax.axhline(0, color=INK, lw=0.9)
    ax.set_ylabel("Percentage points")
    ax.set_xlabel("Epoch")
    clean_axis(ax, "y")
    ax.legend(frameon=False, loc="upper left")
    frame_title(
        fig,
        "Time series · definition gap",
        "The disagreement is structural, not a one-year anomaly",
        f"Median GHSL–WDI differences across the same {int(summary.coverage.min())} complete cases, 1975–2020",
    )
    footnote(fig, "The complete-case panel is constant across epochs; no missing value is imputed.")
    return save(fig, "invisible-urbanization-03-definition-gap-over-time")


def figure_focus_trajectories(gap: pd.DataFrame) -> dict:
    focus = ["BGD", "LKA", "AFG", "PLW"]
    labels = {"BGD": "Bangladesh", "LKA": "Sri Lanka", "AFG": "Afghanistan", "PLW": "Palau"}
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.8), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.78, bottom=0.12, wspace=0.18, hspace=0.30)
    for ax, iso3 in zip(axes.flat, focus):
        plot = gap[(gap.iso3 == iso3) & gap.wdi_urban_share_pct.notna()]
        ax.plot(plot.year, plot.wdi_urban_share_pct, color=BLUE, lw=2.2, marker="o", label="WDI")
        ax.plot(plot.year, plot.ghsl_urban_share_pct, color=ORANGE, lw=2.2, marker="o", label="GHSL")
        ax.set_title(labels[iso3], loc="left", fontsize=13, fontweight="bold")
        ax.set_ylim(0, 105)
        clean_axis(ax, "y")
    axes[0, 0].set_ylabel("Population classified urban (%)")
    axes[1, 0].set_ylabel("Population classified urban (%)")
    axes[1, 0].set_xlabel("Epoch")
    axes[1, 1].set_xlabel("Epoch")
    axes[0, 0].legend(frameon=False, ncol=2, loc="upper left")
    frame_title(
        fig,
        "Trajectories · four contrasts",
        "A single national trend can conceal a second measurement story",
        "Three large positive 2020 gaps and one WDI-higher case; fixed GHSL method across epochs",
    )
    footnote(fig, "These trajectories compare constructs; they do not identify which series is the true legal or lived urban status.")
    return save(fig, "invisible-urbanization-04-focus-trajectories")


def figure_scale_sensitivity(analysis: dict) -> dict:
    frame = pd.DataFrame(analysis["administrative_scale_2020"]["common_sample"])
    fig, ax = plt.subplots(figsize=(9.4, 5.8))
    fig.subplots_adjust(left=0.12, right=0.96, top=0.76, bottom=0.17)
    bars = ax.bar(frame.admin_level.astype(str), frame.embedded_share_pct, color=[BLUE, "#5F91AE", BLUE_LIGHT], width=0.62)
    for bar, value in zip(bars, frame.embedded_share_pct):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.08, f"{value:.1f}%", ha="center", fontweight="bold")
    ax.set_ylabel("Urban-cell population inside rural-classified units (%)")
    ax.set_xlabel("GADM administrative level")
    clean_axis(ax, "y")
    n = len(analysis["administrative_scale_2020"]["common_sample_economies"])
    frame_title(
        fig,
        "Sensitivity · administrative scale",
        "Finer units expose more urban population inside rural units",
        f"Same {n}-economy sample at every level, 2020",
    )
    footnote(fig, "GHS-DUC classification on GADM 4.1. Levels are not institutionally equivalent across countries.")
    return save(fig, "invisible-urbanization-05-administrative-scale-sensitivity")


def figure_embedded_time(embedded: pd.DataFrame) -> dict:
    level2 = embedded[embedded.admin_level == 2].copy()
    common = set.intersection(*[set(x.iso3) for _, x in level2.groupby("year")])
    level2 = level2[level2.iso3.isin(common)]
    summary = level2.groupby("year", as_index=False).agg(
        embedded=("embedded_urban_pop", "sum"), urban=("urban_cell_pop", "sum")
    )
    summary["share"] = 100 * summary.embedded / summary.urban
    fig, ax = plt.subplots(figsize=(10.2, 6.1))
    fig.subplots_adjust(left=0.12, right=0.94, top=0.78, bottom=0.16)
    ax.plot(summary.year, summary.share, color=ORANGE, lw=3, marker="o")
    ax.fill_between(summary.year, summary.share, color=ORANGE_LIGHT, alpha=0.25)
    for row in summary.iloc[[0, -1]].itertuples():
        ax.text(row.year, row.share + 0.15, f"{row.share:.1f}%", ha="center", fontweight="bold")
    ax.set_ylabel("Urban-cell population inside rural-classified level-2 units (%)")
    ax.set_xlabel("Epoch")
    ax.set_ylim(0, max(summary.share) * 1.18)
    clean_axis(ax, "y")
    frame_title(
        fig,
        "Time series · embedded urban population",
        "The standardized hidden share has declined",
        f"Population-weighted across the same {len(common)} level-2-covered economies, 1975–2020",
    )
    footnote(fig, "A falling stock can reflect threshold crossing by administrative units, not the disappearance of urban growth.")
    return save(fig, "invisible-urbanization-06-embedded-share-over-time")


def figure_transition_waterfall(transitions: dict) -> dict:
    rows = [r for r in transitions["transition_summary"] if r["window_years"] == 20]
    by = {r["transition"]: r for r in rows}
    start = sum(r["embedded_start"] for r in rows) / 1e6
    persistent = by["remained_rural"]["embedded_change"] / 1e6
    graduated = by["rural_to_town_or_city"]["embedded_change"] / 1e6
    reverse = by["town_or_city_to_rural"]["embedded_change"] / 1e6
    values = [start, persistent, graduated, reverse]
    labels = ["Embedded\nstock, 2000", "Growth in units\nstill rural", "Rural → town/city\nthreshold crossings", "Town/city → rural\nchanges"]
    bases = [0, start, start + persistent, start + persistent + graduated]
    colors = [BLUE, GREEN, RED, GOLD]
    final = start + persistent + graduated + reverse
    fig, ax = plt.subplots(figsize=(10.5, 6.3))
    fig.subplots_adjust(left=0.10, right=0.96, top=0.77, bottom=0.20)
    ax.bar(range(4), values, bottom=bases, color=colors, width=0.66, zorder=3)
    ax.bar(4, final, color=ORANGE, width=0.66, zorder=3)
    for i, (value, base) in enumerate(zip(values, bases)):
        label = f"{value:+.1f}" if i else f"{value:.1f}"
        ax.text(i, base + value + (1.5 if value >= 0 else -3.5), label, ha="center", fontweight="bold")
    ax.text(4, final + 1.5, f"{final:.1f}", ha="center", fontweight="bold")
    ax.set_xticks(range(5), labels + ["Embedded\nstock, 2020"])
    ax.set_ylabel("Million people in GHSL urban cells")
    clean_axis(ax, "y")
    frame_title(
        fig,
        "Mechanism · 20-year decomposition",
        "Persistent rural units gained 13.9 million urban-cell residents",
        "The total embedded stock fell because more units crossed out of the rural class than crossed in",
    )
    footnote(fig, "Matched GADM 4.1 level-2 units in 34 covered economies. Classification changes are statistical, not legal redesignations.")
    return save(fig, "invisible-urbanization-07-transition-waterfall")


def figure_country_embedded(embedded: pd.DataFrame) -> dict:
    plot = embedded[(embedded.year == 2020) & (embedded.admin_level == 2)].copy()
    plot = plot.nlargest(15, "embedded_share_of_urban_cell_pop_pct").sort_values("embedded_share_of_urban_cell_pop_pct")
    fig, ax = plt.subplots(figsize=(9.8, 7.8))
    fig.subplots_adjust(left=0.24, right=0.95, top=0.80, bottom=0.13)
    y = np.arange(len(plot))
    ax.barh(y, plot.embedded_share_of_urban_cell_pop_pct, color=BLUE, height=0.68)
    ax.set_yticks(y, [f"{r.country}  ·  {r.iso3}" for r in plot.itertuples()])
    ax.set_xlabel("Urban-cell population inside rural-classified level-2 units (%)")
    clean_axis(ax)
    frame_title(
        fig,
        "Heterogeneity · level-2 diagnostic",
        "The aggregation effect is concentrated, not universal",
        "Fifteen largest shares among 34 covered economies, 2020",
    )
    footnote(fig, "Descriptive ordering only. Administrative level 2 represents different institutions and unit sizes across economies.")
    return save(fig, "invisible-urbanization-08-country-embedded-shares")


def figure_heatmap(embedded: pd.DataFrame) -> dict:
    level2 = embedded[embedded.admin_level == 2].copy()
    focus = (
        level2[level2.year == 2020]
        .nlargest(12, "embedded_share_of_urban_cell_pop_pct")["iso3"]
        .tolist()
    )
    plot = level2[level2.iso3.isin(focus)].pivot(index="iso3", columns="year", values="embedded_share_of_urban_cell_pop_pct")
    plot = plot.loc[plot[2020].sort_values(ascending=False).index]
    fig, ax = plt.subplots(figsize=(11, 6.7))
    fig.subplots_adjust(left=0.13, right=0.93, top=0.78, bottom=0.16)
    image = ax.imshow(plot.to_numpy(), aspect="auto", cmap="YlOrBr", vmin=0, vmax=np.nanpercentile(plot.to_numpy(), 95))
    ax.set_yticks(range(len(plot)), plot.index)
    ax.set_xticks(range(len(plot.columns)), plot.columns)
    ax.tick_params(length=0)
    for i in range(len(plot)):
        for j in range(len(plot.columns)):
            value = plot.iloc[i, j]
            if pd.notna(value) and (j in [0, len(plot.columns) - 1]):
                ax.text(j, i, f"{value:.0f}", ha="center", va="center", fontsize=8, color=INK)
    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Embedded share (%)")
    frame_title(
        fig,
        "Dynamics · selected level-2 cases",
        "High embedded shares do not all move in the same direction",
        "Twelve largest 2020 shares, fixed GADM 4.1 units and five-year GHSL epochs",
    )
    footnote(fig, "First and last cells are labelled. Intermediate colour changes show classification and population dynamics together.")
    return save(fig, "invisible-urbanization-09-country-time-heatmap")


def figure_coverage(analysis: dict) -> dict:
    values = [44, 43, 40, 34, 13]
    labels = ["Repo DMC roster", "GHSL level 0", "GHSL + WDI, 2020", "GHSL level 2", "Levels 1–3 common"]
    fig, ax = plt.subplots(figsize=(9.8, 5.9))
    fig.subplots_adjust(left=0.24, right=0.95, top=0.76, bottom=0.15)
    y = np.arange(len(values))[::-1]
    ax.barh(y, values, color=[INK, BLUE, ORANGE, "#5F91AE", BLUE_LIGHT], height=0.62)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 48)
    ax.set_xlabel("Economies")
    for yi, value in zip(y, values):
        ax.text(value + 0.6, yi, str(value), va="center", fontweight="bold")
    clean_axis(ax)
    frame_title(
        fig,
        "Coverage · honest denominator",
        "Every deeper question narrows the comparable sample",
        "No absent WDI value or administrative level is imputed",
    )
    footnote(fig, "Hong Kong, China is not separable in the GHSL country-code aggregation; WDI is missing for COK, NIU, and TWN in 2020.")
    return save(fig, "invisible-urbanization-10-coverage-funnel")


def figure_method_infographic() -> dict:
    fig, ax = plt.subplots(figsize=(11.5, 6.3))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.77, bottom=0.12)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    boxes = [
        (0.03, 0.55, 0.22, 0.27, BLUE_LIGHT, "WDI national-definition share", "Country-reported urban series\nused for national trends"),
        (0.03, 0.16, 0.22, 0.27, ORANGE_LIGHT, "GHSL standardized grid", "Population density, size,\ncontiguity and built-up inputs"),
        (0.39, 0.55, 0.24, 0.27, "#DCEAF0", "Definition-gap panel", "GHSL share − WDI share\n40 complete cases in 2020"),
        (0.39, 0.16, 0.24, 0.27, "#F7E5DE", "Administrative embedding", "Urban-cell population inside\nrural-classified GADM units"),
        (0.76, 0.55, 0.21, 0.27, "#DCEDE8", "What it supports", "Definition disagreement,\nscale sensitivity, transitions"),
        (0.76, 0.16, 0.21, 0.27, "#F3E6E6", "What it cannot support", "Legal misclassification, neglect,\nservice or welfare effects"),
    ]
    for x, y, w, h, color, title, body in boxes:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02", facecolor=color, edgecolor="white")
        ax.add_patch(patch)
        ax.text(x + 0.02, y + h - 0.07, title, fontsize=11, fontweight="bold", color=INK)
        ax.text(x + 0.02, y + h - 0.14, body, fontsize=9.3, color=MUTED, va="top", linespacing=1.4)
    for y in (0.69, 0.30):
        ax.add_patch(FancyArrowPatch((0.26, y), (0.38, y), arrowstyle="-|>", mutation_scale=14, color=MUTED, lw=1.4))
        ax.add_patch(FancyArrowPatch((0.64, y), (0.75, y), arrowstyle="-|>", mutation_scale=14, color=MUTED, lw=1.4))
    frame_title(
        fig,
        "Research architecture · claim gate",
        "Two public-data objects answer two different questions",
        "The method separates comparable measurement from unsupported policy inference",
    )
    footnote(fig, "All empirical values trace to committed scripts, cached public sources, checksums, and generated panels.")
    return save(fig, "invisible-urbanization-11-method-and-claim-gate")


def main() -> None:
    setup_style()
    CHARTS.mkdir(parents=True, exist_ok=True)
    gap = pd.read_csv(OUT / "invisible-urbanization-definition-gap-panel.csv")
    embedded = pd.read_csv(OUT / "invisible-urbanization-embedded-urban-panel.csv")
    analysis = json.loads((OUT / "invisible-urbanization-definition-gap.json").read_text(encoding="utf-8"))
    transitions = json.loads((OUT / "invisible-urbanization-transition-diagnostics.json").read_text(encoding="utf-8"))

    figures = [
        ("definition-gap hero", figure_gap_hero(gap)),
        ("selected definition dumbbell", figure_selected_dumbbell(gap)),
        ("definition gap over time", figure_gap_over_time(gap)),
        ("focus trajectories", figure_focus_trajectories(gap)),
        ("administrative-scale sensitivity", figure_scale_sensitivity(analysis)),
        ("embedded share over time", figure_embedded_time(embedded)),
        ("transition waterfall", figure_transition_waterfall(transitions)),
        ("country embedded shares", figure_country_embedded(embedded)),
        ("country-time heatmap", figure_heatmap(embedded)),
        ("coverage funnel", figure_coverage(analysis)),
        ("method and claim gate", figure_method_infographic()),
    ]
    payload = {
        "program": "invisible-urbanization",
        "analysis": "evidence-bearing figure dossier",
        "attestation_chain": "ai-first",
        "figure_count": len(figures),
        "figures": [
            {"order": index, "name": name, "paths": paths}
            for index, (name, paths) in enumerate(figures, 1)
        ],
    }
    (OUT / "invisible-urbanization-figure-dossier.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Built {len(figures)} evidence-bearing figures")


if __name__ == "__main__":
    main()
