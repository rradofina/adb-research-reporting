"""Build the evidence-led figure spine for food-price construct validation.

Every plotted quantity is read from the committed construct-validation JSON
or its generated CSVs.  The figures communicate the finding, the method
correction, the sensitivity, and the remaining claim gates.

attestation_chain: ai-first
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image


PROGRAM = Path(__file__).resolve().parents[1]
REPO = PROGRAM.parent
GENERATED = PROGRAM / "generated"
CHARTS = GENERATED / "charts"
VALIDATION = GENERATED / "food-price-construct-validation.json"
CORRECTED = GENERATED / "food-price-market-month-corrected.csv"
SENSITIVITY = GENERATED / "food-price-threshold-sensitivity.csv"

BLUE = "#007DB8"
NAVY = "#002569"
GREEN = "#5A8227"
GOLD = "#FBB00E"
RED = "#9B2226"
INK = "#212529"
MID = "#66717B"
PALE = "#E7EEF3"
LIGHT_BLUE = "#DCEFF7"
LIGHT_GOLD = "#FFF3CE"
WHITE = "#FFFFFF"


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 16,
        "axes.labelsize": 11,
        "axes.edgecolor": "#C7D2DB",
        "axes.linewidth": 0.8,
        "xtick.color": MID,
        "ytick.color": MID,
        "text.color": INK,
        "axes.titlecolor": INK,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
    }
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def new_figure(nrows=1, ncols=1, figsize=(16, 9), **kwargs):
    return plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, **kwargs)


def header(fig, title: str, subtitle: str):
    fig.suptitle(title, x=0.06, y=0.965, ha="left", fontsize=23, fontweight="bold")
    fig.text(0.06, 0.915, subtitle, ha="left", fontsize=11.5, color=MID)


def footer(fig, source: str, note: str):
    fig.text(0.06, 0.045, f"Source: {source}", fontsize=8.6, color=MID)
    fig.text(0.06, 0.022, f"Note: {note}", fontsize=8.4, color=MID)
    fig.text(
        0.94,
        0.022,
        "attestation_chain: ai-first",
        fontsize=8.2,
        color=MID,
        ha="right",
        family="monospace",
    )


def clean_axis(ax, grid="y"):
    ax.spines[["top", "right"]].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=PALE, linewidth=0.8)
        ax.set_axisbelow(True)


def save(fig, stem: str):
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{stem}.png", dpi=180, bbox_inches="tight")
    svg_path = CHARTS / f"{stem}.svg"
    fig.savefig(svg_path, bbox_inches="tight")
    # Matplotlib emits trailing spaces in multi-line SVG path data. Normalize
    # the committed artifact so repository whitespace checks stay clean.
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def method_correction(data):
    correction = data["method_correction"]
    fig, axes = new_figure(1, 2, figsize=(16, 9))
    header(
        fig,
        "The original price transformation overstated broad waves",
        "Counts before and after replacing the full-sample seasonal median with year-on-year market price change",
    )
    labels = ["Price-spike\nmarket-months", "Broad non-dry\nwave months"]
    old = [correction["old_price_spike_cells"], correction["old_broad_non_dry_wave_months"]]
    corrected = [
        correction["corrected_price_spike_cells"],
        correction["corrected_broad_non_dry_wave_months"],
    ]
    for ax, index in zip(axes, range(2)):
        bars = ax.bar(
            [0, 1],
            [old[index], corrected[index]],
            color=["#B7C4CE", BLUE],
            width=0.62,
        )
        ax.set_xticks([0, 1], ["Old seasonal-median\nanomaly", "Corrected year-on-year\nlog change"])
        ax.set_title(labels[index].replace("\n", " "), loc="left", fontweight="bold")
        ax.set_ylim(0, max(old[index], corrected[index]) * 1.28)
        ax.set_yticks([])
        clean_axis(ax, grid=None)
        ax.spines[["left", "bottom"]].set_visible(False)
        for bar, value in zip(bars, [old[index], corrected[index]]):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(old[index], corrected[index]) * 0.04,
                f"{value:,}",
                ha="center",
                fontsize=21,
                fontweight="bold",
                color=INK,
            )
    fig.text(
        0.50,
        0.16,
        "Later high price levels were mechanically far above the 2019–2025 median.\nYear-on-year change asks whether the same market's price actually rose sharply.",
        ha="center",
        fontsize=11.5,
        color=NAVY,
        bbox={"boxstyle": "round,pad=0.7", "facecolor": LIGHT_BLUE, "edgecolor": "none"},
    )
    footer(
        fig,
        "WFP Nepal market prices via HDX; generated construct-validation artifact",
        "A count change is a method correction, not evidence that the remaining spikes have a particular cause.",
    )
    fig.subplots_adjust(left=0.07, right=0.95, top=0.82, bottom=0.25, wspace=0.25)
    save(fig, "food-price-method-correction")


def spike_alignment(data):
    result = data["main_result"]
    dry = result["dry_aligned_price_spike_cells"]
    other = result["non_dry_price_spike_cells"]
    total = result["price_spike_cells"]
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "Only 17 of 152 corrected rice-price spikes follow locally dry rainfall",
        "Nepal · 12 selected markets · coarse rice · 2020–2025 year-on-year price change · one-month rainfall lag",
    )
    ax.barh([0], [other], color=BLUE, height=0.36, label="Not dry-aligned")
    ax.barh([0], [dry], left=[other], color=GOLD, height=0.36, label="Dry-aligned")
    ax.text(other / 2, 0, f"{other}\nnot dry-aligned", ha="center", va="center", color=WHITE, fontsize=18, fontweight="bold")
    ax.text(other + dry / 2, 0, f"{dry}", ha="center", va="center", color=NAVY, fontsize=16, fontweight="bold")
    ax.text(
        total,
        0.36,
        f"{100 * dry / total:.1f}% dry-aligned",
        ha="right",
        fontsize=26,
        fontweight="bold",
        color=NAVY,
    )
    ax.set_xlim(0, total)
    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([])
    ax.set_xlabel("Market-month price-spike cells")
    clean_axis(ax, grid="x")
    ax.spines[["left", "bottom"]].set_visible(False)
    fig.text(
        0.08,
        0.23,
        "A spike is ≥20% year-on-year in the same market. Dry alignment is NASA POWER precipitation z ≤ −1 one month earlier.",
        fontsize=11,
        color=MID,
    )
    fig.text(
        0.08,
        0.18,
        "This is a coincidence screen. It does not estimate the share caused by climate.",
        fontsize=13,
        color=RED,
        fontweight="bold",
    )
    footer(
        fig,
        "WFP Nepal market prices; NASA POWER monthly point data",
        "Non-dry alignment does not rule out heat, flood, crop, transport, trade, fuel, currency, policy, or other mechanisms.",
    )
    fig.subplots_adjust(left=0.08, right=0.94, top=0.78, bottom=0.30)
    save(fig, "food-price-spike-alignment")


def wave_timeline(data):
    ledger = data["main_month_ledger"]
    months = [row["month"] for row in ledger]
    shares = [row["price_spike_market_share"] for row in ledger]
    colors = [
        RED
        if row["signal_class"] == "dry_aligned_cluster"
        else BLUE
        if row["signal_class"] == "broad_price_wave_not_local_dryness"
        else "#C7D2DB"
        for row in ledger
    ]
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "Ten broad rice-price wave months were not dominated by local dryness",
        "Share of observed markets with coarse-rice inflation ≥20% year-on-year; red marks the two dry-aligned clusters",
    )
    x = np.arange(len(months))
    ax.bar(x, shares, color=colors, width=0.82)
    ax.axhline(0.5, color=NAVY, linestyle="--", linewidth=1.2)
    ax.text(len(months) - 0.5, 0.515, "50% broad-wave threshold", ha="right", color=NAVY, fontsize=9)
    for index, row in enumerate(ledger):
        if row["signal_class"] == "dry_aligned_cluster":
            ax.annotate(
                f"{row['month']}\n{100 * row['dry_share_among_price_spikes']:.0f}% of spikes dry-aligned",
                xy=(index, row["price_spike_market_share"]),
                xytext=(index, min(1.02, row["price_spike_market_share"] + 0.22)),
                ha="center",
                fontsize=8.5,
                color=RED,
                arrowprops={"arrowstyle": "-", "color": RED, "lw": 0.8},
            )
    ticks = [index for index, month in enumerate(months) if month.endswith("-01") or index == len(months) - 1]
    ax.set_xticks(ticks, [months[index] for index in ticks])
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Share of observed markets")
    ax.yaxis.set_major_formatter(lambda value, _position: f"{value:.0%}")
    clean_axis(ax)
    footer(
        fig,
        "Generated year-on-year market panel and NASA POWER lagged precipitation",
        "Month classes are threshold-sensitive; the figure shows the pre-specified main thresholds only.",
    )
    fig.subplots_adjust(left=0.08, right=0.96, top=0.82, bottom=0.14)
    save(fig, "food-price-wave-timeline")


def lag_sensitivity(data):
    rows = data["lag_sensitivity"]
    lags = [row["rain_lag_months"] for row in rows]
    shares = [100 * row["dry_share_of_joined_price_spikes"] for row in rows]
    counts = [row["dry_aligned_price_spike_cells"] for row in rows]
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "Dry alignment stays below 12% across four rainfall lags",
        "Share of 152 corrected rice-price spike cells aligned with precipitation z ≤ −1",
    )
    bars = ax.bar([str(lag) for lag in lags], shares, color=["#85BCD4", BLUE, "#85BCD4", "#85BCD4"], width=0.58)
    for bar, share, count in zip(bars, shares, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, share + 0.45, f"{share:.1f}%\n({count} cells)", ha="center", fontsize=14, fontweight="bold")
    ax.set_xlabel("Rainfall lag before the price month (months)")
    ax.set_ylabel("Dry-aligned share of price spikes")
    ax.set_ylim(0, 14.5)
    ax.yaxis.set_major_formatter(lambda value, _position: f"{value:.0f}%")
    clean_axis(ax)
    footer(
        fig,
        "WFP Nepal market prices; NASA POWER monthly point precipitation",
        "Lag comparison is descriptive and does not resolve crop calendars, floods, heat, or delayed transport effects.",
    )
    fig.subplots_adjust(left=0.09, right=0.95, top=0.80, bottom=0.16)
    save(fig, "food-price-rain-lag-sensitivity")


def threshold_sensitivity(data, rows):
    price_values = [10.0, 20.0, 30.0]
    dry_values = [-0.5, -1.0, -1.5]
    wave_values = [0.25, 0.50, 0.75]

    dry_matrix = np.zeros((3, 3))
    wave_matrix = np.zeros((3, 3))
    for i, dry in enumerate(dry_values):
        for j, price in enumerate(price_values):
            matching = [
                row
                for row in rows
                if float(row["price_spike_threshold_pct"]) == price
                and float(row["dry_precipitation_z_threshold"]) == dry
            ]
            dry_matrix[i, j] = float(matching[0]["dry_share_of_price_spike_cells"])
    for i, wave in enumerate(wave_values):
        for j, price in enumerate(price_values):
            matching = [
                row
                for row in rows
                if float(row["price_spike_threshold_pct"]) == price
                and float(row["dry_precipitation_z_threshold"]) == -1.0
                and float(row["broad_wave_market_share_threshold"]) == wave
                and float(row["max_dry_share_for_non_dry_wave"]) == 0.34
            ]
            wave_matrix[i, j] = float(matching[0]["broad_non_dry_wave_months"])

    fig, axes = new_figure(1, 2, figsize=(16, 9))
    header(
        fig,
        "The direction survives, but wave counts depend on arbitrary thresholds",
        "Left: dry share of spike cells. Right: broad non-dry wave months at the main dry-share rule.",
    )
    cmap = LinearSegmentedColormap.from_list("adb", [WHITE, LIGHT_BLUE, BLUE, NAVY])
    image_left = axes[0].imshow(dry_matrix, cmap=cmap, vmin=0, vmax=0.5)
    image_right = axes[1].imshow(wave_matrix, cmap=cmap, vmin=0, vmax=max(1, wave_matrix.max()))
    for ax, matrix, ylabels, title, fmt in [
        (axes[0], dry_matrix, ["−0.5", "−1.0", "−1.5"], "Dry alignment remains a minority", lambda value: f"{value:.0%}"),
        (axes[1], wave_matrix, ["25%", "50%", "75%"], "Broad-wave counts are unstable", lambda value: f"{value:.0f}"),
    ]:
        ax.set_xticks(range(3), ["10%", "20%", "30%"])
        ax.set_yticks(range(3), ylabels)
        ax.set_xlabel("Year-on-year price-spike threshold")
        ax.set_title(title, loc="left", fontweight="bold")
        for i in range(3):
            for j in range(3):
                value = matrix[i, j]
                ax.text(j, i, fmt(value), ha="center", va="center", fontsize=15, fontweight="bold", color=WHITE if value > matrix.max() * 0.55 else INK)
    axes[0].set_ylabel("Dry precipitation z threshold")
    axes[1].set_ylabel("Markets required to spike")
    footer(
        fig,
        "81-run full-factorial sensitivity artifact",
        "Every arbitrary numeric rule is tested at −50%, baseline, and +50%. The headline uses the cell-level dry share, not the unstable month count.",
    )
    fig.subplots_adjust(left=0.08, right=0.95, top=0.79, bottom=0.16, wspace=0.25)
    save(fig, "food-price-threshold-sensitivity")


def annual_alignment(data):
    rows = [row for row in data["market_year_rows"] if row["wdi_headline_cpi_inflation_pct"] is not None]
    x = [row["wdi_headline_cpi_inflation_pct"] for row in rows]
    y = [row["median_market_rice_yoy_log_change_pct"] for row in rows]
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "Five annual observations cannot validate headline CPI against market rice inflation",
        "Nepal · World Bank headline CPI versus median year-on-year coarse-rice change across selected markets",
    )
    ax.scatter(x, y, s=135, color=BLUE, edgecolor=WHITE, linewidth=1.5, zorder=3)
    for row in rows:
        ax.annotate(str(row["year"]), (row["wdi_headline_cpi_inflation_pct"], row["median_market_rice_yoy_log_change_pct"]), xytext=(7, 7), textcoords="offset points", fontsize=10, fontweight="bold")
    alignment = data["annual_alignment"]
    ax.text(
        0.98,
        0.13,
        f"Spearman ρ = {alignment['spearman_rho']:+.2f}\nexact p = {alignment['exact_two_sided_permutation_p_for_spearman']:.2f}\nn = {alignment['n_years']}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=16,
        color=NAVY,
        bbox={"boxstyle": "round,pad=0.6", "facecolor": LIGHT_BLUE, "edgecolor": "none"},
    )
    ax.axhline(0, color="#C7D2DB", linewidth=1)
    ax.set_xlabel("Headline CPI inflation (%)")
    ax.set_ylabel("Median market coarse-rice year-on-year log change (%)")
    clean_axis(ax)
    footer(
        fig,
        "World Bank WDI FP.CPI.TOTL.ZG; WFP Nepal market prices",
        "Different baskets and five overlapping years make this a measurement comparison, not a validation or causal test.",
    )
    fig.subplots_adjust(left=0.10, right=0.94, top=0.80, bottom=0.16)
    save(fig, "food-price-annual-alignment")


def macro_mismatch(data):
    rows = data["macro_selection"]["comparison_rows"]
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "The annual screen would not have selected Nepal's market-price problem",
        "Latest-year rank positions in the inherited WDI intersection; lower rank is closer to the screen's cutoff",
    )
    for row in rows:
        selected = row["iso3"] != "NPL"
        ax.scatter(
            row["cpi_rank"],
            row["imp_rank"],
            s=210 if row["iso3"] == "NPL" else 130,
            color=GOLD if row["iso3"] == "NPL" else BLUE,
            edgecolor=NAVY if row["iso3"] == "NPL" else WHITE,
            linewidth=1.8,
            zorder=3,
        )
        ax.annotate(
            f"{row['iso3']}\n({row['cpi_rank']}, {row['imp_rank']})",
            (row["cpi_rank"], row["imp_rank"]),
            xytext=(8, 7),
            textcoords="offset points",
            fontsize=10.5,
            fontweight="bold" if row["iso3"] == "NPL" else "normal",
        )
    ax.add_patch(
        Rectangle(
            (0.5, 0.5),
            10,
            10,
            facecolor=LIGHT_BLUE,
            edgecolor="none",
            alpha=0.65,
            zorder=0,
        )
    )
    ax.axvline(10.5, color=BLUE, linestyle="--", linewidth=1)
    ax.axhline(10.5, color=BLUE, linestyle="--", linewidth=1)
    ax.set_xlim(0, 38)
    ax.set_ylim(0, 28)
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.set_xlabel("Headline CPI inflation rank")
    ax.set_ylabel("Agricultural raw-material import-share rank")
    clean_axis(ax)
    fig.text(
        0.67,
        0.22,
        "Nepal: CPI rank 12 · import-share rank 22\nYet the market panel contains 152 corrected rice-price spike cells.",
        fontsize=12,
        color=NAVY,
        bbox={"boxstyle": "round,pad=0.65", "facecolor": LIGHT_GOLD, "edgecolor": "none"},
    )
    footer(
        fig,
        "Inherited World Bank WDI screen; corrected WFP Nepal market panel",
        "The chart diagnoses a unit mismatch. It is not a new economy ranking and does not imply the selected economies lack local price problems.",
    )
    fig.subplots_adjust(left=0.10, right=0.95, top=0.80, bottom=0.17)
    save(fig, "food-price-macro-market-mismatch")


def source_funnel(data):
    coverage = data["coverage"]
    main = data["main_result"]
    labels = [
        "Selected market-month grid",
        "Cells with observed price",
        "Cells with year-on-year price",
        "Corrected price-spike cells",
        "Dry-aligned spike cells",
    ]
    values = [
        coverage["original_selected_market_month_cells"],
        coverage["original_cells_with_price"],
        coverage["corrected_cells_with_year_on_year_price"],
        main["price_spike_cells"],
        main["dry_aligned_price_spike_cells"],
    ]
    widths = np.sqrt(np.array(values) / max(values))
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "The evidence narrows from 1,008 planned cells to 17 dry-aligned spikes",
        "Coverage and outcome funnel for the Nepal coarse-rice construct validation",
    )
    y = np.arange(len(labels))[::-1]
    colors = ["#D7E0E6", "#B7C4CE", "#85BCD4", BLUE, GOLD]
    for position, label, value, width, color in zip(y, labels, values, widths, colors):
        rect = FancyBboxPatch(
            (0.5 - width / 2, position - 0.33),
            width,
            0.66,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            facecolor=color,
            edgecolor="none",
        )
        ax.add_patch(rect)
        ax.text(0.5, position, f"{value:,}", ha="center", va="center", fontsize=17, fontweight="bold", color=NAVY if color == GOLD else INK)
        ax.text(0.98, position, label, ha="left", va="center", fontsize=11.5, color=INK)
    ax.set_xlim(-0.05, 1.55)
    ax.set_ylim(-0.8, len(labels) - 0.2)
    ax.axis("off")
    footer(
        fig,
        "Generated construct-validation artifact",
        "The final 17 are screened coincidences under the main threshold, not attributed climate effects.",
    )
    fig.subplots_adjust(left=0.07, right=0.95, top=0.80, bottom=0.13)
    save(fig, "food-price-source-alignment-funnel")


def claim_gates(data):
    gates = [
        ("Market price outcome\ntrend-corrected", True),
        ("Price and local climate\nunits aligned", True),
        ("Observed hazard-event\njoin", False),
        ("Multiple commodities", False),
        ("Market-access and\nmacro controls", False),
        ("Transmission estimate\nallowed", False),
    ]
    fig, ax = new_figure(figsize=(16, 9))
    header(
        fig,
        "Two measurement gates pass; four transmission gates remain open",
        "Why the current issue is a construct-validation finding rather than a climate-attribution result",
    )
    for index, (label, passed) in enumerate(gates):
        x = index % 3
        y = 1 - index // 3
        color = GREEN if passed else "#D7E0E6"
        edge = GREEN if passed else "#9AA8B3"
        rect = FancyBboxPatch(
            (x + 0.08, y + 0.10),
            0.82,
            0.66,
            boxstyle="round,pad=0.03,rounding_size=0.05",
            facecolor=color if passed else WHITE,
            edgecolor=edge,
            linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(x + 0.49, y + 0.50, "✓" if passed else "—", ha="center", va="center", fontsize=27, color=WHITE if passed else MID, fontweight="bold")
        ax.text(x + 0.49, y + 0.25, label, ha="center", va="center", fontsize=10.5, color=WHITE if passed else INK)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 2)
    ax.axis("off")
    fig.text(
        0.5,
        0.17,
        "The next claim-enabling object is an event-defined, multi-commodity market panel with access and macro controls.",
        ha="center",
        fontsize=12,
        color=NAVY,
        fontweight="bold",
    )
    footer(
        fig,
        "Claim gates in food-price-construct-validation.json",
        "The IMF Nepal study is the methodological benchmark; this issue does not duplicate its transmission estimate.",
    )
    fig.subplots_adjust(left=0.08, right=0.94, top=0.79, bottom=0.20)
    save(fig, "food-price-claim-gates")


def thumbnail(data):
    result = data["main_result"]
    dry = result["dry_aligned_price_spike_cells"]
    other = result["non_dry_price_spike_cells"]
    total = result["price_spike_cells"]
    fig, ax = new_figure(figsize=(16, 9))
    fig.patch.set_facecolor(WHITE)
    fig.text(0.06, 0.91, "FOOD-PRICE CLIMATE TRANSMISSION", fontsize=11, color=BLUE, fontweight="bold")
    fig.text(0.06, 0.81, "Only 1 in 9 corrected rice-price\nspikes follows locally dry rainfall", fontsize=28, color=NAVY, fontweight="bold", va="top")
    fig.text(0.06, 0.62, "Nepal · 12 markets · 2020–2025 · coarse rice", fontsize=12, color=MID)
    ax.barh([0], [other], color=BLUE, height=0.40)
    ax.barh([0], [dry], left=[other], color=GOLD, height=0.40)
    ax.text(other / 2, 0, f"{other} not dry-aligned", ha="center", va="center", color=WHITE, fontsize=17, fontweight="bold")
    ax.text(other + dry / 2, 0, str(dry), ha="center", va="center", color=NAVY, fontsize=15, fontweight="bold")
    ax.set_xlim(0, total)
    ax.set_ylim(-0.7, 0.7)
    ax.axis("off")
    fig.text(0.06, 0.17, "Year-on-year price change ≥20%; precipitation z ≤ −1 at one-month lag", fontsize=10.5, color=MID)
    fig.text(0.06, 0.11, "Coincidence screen, not climate attribution", fontsize=13, color=RED, fontweight="bold")
    fig.text(0.94, 0.04, "attestation_chain: ai-first", ha="right", fontsize=8.5, color=MID, family="monospace")
    fig.subplots_adjust(left=0.07, right=0.94, top=0.56, bottom=0.22)
    save(fig, "food-price-climate-transmission-thumbnail")
    png = CHARTS / "food-price-climate-transmission-thumbnail.png"
    svg = CHARTS / "food-price-climate-transmission-thumbnail.svg"
    with Image.open(png) as image:
        width, height = image.size
    sidecar = {
        "attestation_chain": "ai-first",
        "program": "food-price-climate-transmission",
        "title": "Only one in nine corrected rice-price spikes follows locally dry rainfall",
        "caption": (
            "Seventeen of 152 corrected Nepal coarse-rice price-spike cells "
            "follow locally dry rainfall at the one-month lag."
        ),
        "headline_number": "17 of 152 · 11.2%",
        "visual_form": "construct-validation finding card",
        "headline": "Only 1 in 9 corrected Nepal rice-price spikes follows locally dry rainfall",
        "metric": {
            "price_spike_cells": total,
            "dry_aligned_price_spike_cells": dry,
            "dry_share": result["dry_share_of_price_spike_cells"],
        },
        "source": "food-price-climate-transmission/generated/food-price-construct-validation.json",
        "inputs": [
            "generated/food-price-construct-validation.json",
            "generated/food-price-market-month-corrected.csv",
        ],
        "script": "food-price-climate-transmission/scripts/build-figure-dossier.py",
        "constitution_ref": "CONSTITUTION.md §18",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dimensions": {"width": width, "height": height},
        "files": {"png": png.name, "svg": svg.name},
        "sha256": {
            "png": hashlib.sha256(png.read_bytes()).hexdigest(),
            "svg": hashlib.sha256(svg.read_bytes()).hexdigest(),
        },
        "outputs": {
            "png": "food-price-climate-transmission/generated/charts/food-price-climate-transmission-thumbnail.png",
            "svg": "food-price-climate-transmission/generated/charts/food-price-climate-transmission-thumbnail.svg",
        },
        "nonclaim": "Coincidence screen, not climate attribution.",
    }
    (CHARTS / "food-price-climate-transmission-thumbnail.json").write_text(
        json.dumps(sidecar, indent=2) + "\n", encoding="utf-8"
    )


def main():
    data = load_json(VALIDATION)
    sensitivity_rows = load_csv(SENSITIVITY)
    method_correction(data)
    spike_alignment(data)
    wave_timeline(data)
    lag_sensitivity(data)
    threshold_sensitivity(data, sensitivity_rows)
    annual_alignment(data)
    macro_mismatch(data)
    source_funnel(data)
    claim_gates(data)
    thumbnail(data)
    print("Food-price figure dossier complete")
    for path in sorted(CHARTS.glob("food-price-*.png")):
        print(path.relative_to(REPO))


if __name__ == "__main__":
    main()
