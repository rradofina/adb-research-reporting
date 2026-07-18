"""Build the evidence-figure spine for the digital-performance study.

Every plotted value is read from the generated panel produced by
build-coverage-use-gap.py. The figures have distinct evidence jobs; none is a
decorative restatement of the headline.

attestation_chain: ai-first
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch


PROGRAM = Path(__file__).resolve().parents[1]
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"
PANEL_PATH = OUT / "digital-performance-coverage-use-panel.csv"
SUMMARY_PATH = OUT / "digital-performance-coverage-use-summary.json"

BLUE = "#0076a1"
ORANGE = "#d96c57"
INK = "#1f2933"
MUTED = "#63717c"
GRID = "#dfe6ea"
PALE = "#eef3f5"
GREEN = "#3f7d5d"
PURPLE = "#6f4b8b"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_svg(path: Path) -> None:
    """Remove Matplotlib's line-end spaces so generated SVGs pass Git hygiene."""
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(line.rstrip() for line in text.splitlines()) + "\n",
        encoding="utf-8",
    )


def save(fig: plt.Figure, stem: str) -> dict:
    CHARTS.mkdir(parents=True, exist_ok=True)
    paths = {}
    for suffix in ("png", "svg"):
        path = CHARTS / f"digital-performance-{stem}.{suffix}"
        fig.savefig(path, dpi=190, bbox_inches="tight", facecolor="white")
        if suffix == "svg":
            clean_svg(path)
        paths[suffix] = str(path.relative_to(PROGRAM)).replace("\\", "/")
    plt.close(fig)
    return paths


def finish_axis(ax: plt.Axes, grid_axis: str = "x") -> None:
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.tick_params(axis="y", length=0)
    ax.set_axisbelow(True)


def add_source(fig: plt.Figure, text: str) -> None:
    fig.text(0.01, -0.015, text, fontsize=8.2, color=MUTED, va="top", wrap=True)


def rank_average(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[order[end]] == values[order[start]]:
            end += 1
        ranks[order[start:end]] = (start + end - 1) / 2 + 1
        start = end
    return ranks


def correlation(x: pd.Series, y: pd.Series) -> dict:
    pair = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(pair) < 3:
        return {"n": len(pair), "pearson_r": None, "spearman_rho": None}
    xv = pair["x"].to_numpy(float)
    yv = pair["y"].to_numpy(float)
    return {
        "n": len(pair),
        "pearson_r": float(np.corrcoef(xv, yv)[0, 1]),
        "spearman_rho": float(
            np.corrcoef(rank_average(xv), rank_average(yv))[0, 1]
        ),
    }


def figure_01_hero(headline: pd.DataFrame, year: int) -> dict:
    d = headline.sort_values("availability_use_gap_pp", ascending=True)
    fig, ax = plt.subplots(figsize=(11.5, max(8, len(d) * 0.30)))
    y = np.arange(len(d))
    colors = np.where(d["availability_use_gap_pp"] >= 0, ORANGE, PURPLE)
    ax.barh(y, d["availability_use_gap_pp"], color=colors, height=0.62)
    ax.axvline(0, color=INK, linewidth=0.9)
    ax.set_yticks(y, d["country"])
    ax.set_xlabel("4G/LTE coverage minus internet use (percentage points)")
    ax.set_title(
        f"Reported 4G availability exceeded internet use in 31 of 34 economies in {year}",
        loc="left", fontsize=16, weight="bold", pad=18,
    )
    ax.text(
        0, 1.012,
        "Exact-year ITU observations; negative values are retained as source-disagreement diagnostics",
        transform=ax.transAxes, color=MUTED, fontsize=10,
    )
    for ypos, value in zip(y, d["availability_use_gap_pp"]):
        ax.text(
            value + (0.8 if value >= 0 else -0.8), ypos, f"{value:.1f}",
            va="center", ha="left" if value >= 0 else "right", fontsize=8.5,
        )
    finish_axis(ax)
    add_source(
        fig,
        "Source: ITU DataHub i271GA and i99H. The difference compares availability with use; it does not measure speed, quality, affordability, or causal impact.",
    )
    fig.tight_layout()
    return save(fig, "01-availability-use-gap-hero")


def figure_02_components(headline: pd.DataFrame, year: int) -> dict:
    d = headline.sort_values("availability_use_gap_pp", ascending=False)
    fig, ax = plt.subplots(figsize=(11.5, max(8, len(d) * 0.30)))
    y = np.arange(len(d))
    ax.hlines(y, d["internet_use_pct"], d["coverage_4g_pct"], color="#b9c7ce", lw=2.4)
    ax.scatter(d["internet_use_pct"], y, color=BLUE, s=34, label="Internet use", zorder=3)
    ax.scatter(d["coverage_4g_pct"], y, color=ORANGE, s=34, label="4G/LTE coverage", zorder=3)
    ax.set_yticks(y, d["country"])
    ax.invert_yaxis()
    ax.set_xlim(0, 103)
    ax.set_xlabel("Percent")
    ax.set_title(
        f"The largest gaps often combine high coverage with much lower use ({year})",
        loc="left", fontsize=16, weight="bold", pad=18,
    )
    ax.text(
        0, 1.012,
        "Dumbbells show both source components so the difference is never mistaken for a direct observation",
        transform=ax.transAxes, color=MUTED, fontsize=10,
    )
    ax.legend(frameon=False, loc="lower right")
    finish_axis(ax)
    add_source(fig, "Source: ITU DataHub i271GA and i99H; exact economy-year pairs only.")
    fig.tight_layout()
    return save(fig, "02-components-dumbbell")


def figure_03_scatter(headline: pd.DataFrame, year: int) -> dict:
    fig, ax = plt.subplots(figsize=(9.4, 8.2))
    ax.scatter(
        headline["coverage_4g_pct"], headline["internet_use_pct"],
        s=55, color=BLUE, alpha=0.9, edgecolor="white", linewidth=0.5,
    )
    ax.plot([0, 100], [0, 100], color=INK, linestyle="--", linewidth=1, label="equal coverage and use")
    label_set = set(
        pd.concat([
            headline.nlargest(4, "availability_use_gap_pp"),
            headline.nsmallest(3, "availability_use_gap_pp"),
        ])["iso3"]
    )
    for row in headline.itertuples():
        if row.iso3 in label_set:
            ax.annotate(
                row.country,
                (row.coverage_4g_pct, row.internet_use_pct),
                xytext=(5, 5), textcoords="offset points", fontsize=8.5,
            )
    ax.set(xlim=(0, 103), ylim=(0, 103), xlabel="4G/LTE population coverage (%)", ylabel="Individuals using the Internet (%)")
    ax.set_title(
        f"Near-universal network availability does not guarantee near-universal use ({year})",
        loc="left", fontsize=15, weight="bold", pad=18,
    )
    ax.text(0, 1.01, "Points below the diagonal have a positive availability–use gap", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right")
    add_source(fig, "Source: ITU DataHub i271GA and i99H. Labels identify the four largest positive and three negative differences.")
    fig.tight_layout()
    return save(fig, "03-coverage-use-scatter")


def figure_04_time(panel: pd.DataFrame) -> dict:
    g = panel.groupby("year", as_index=False).agg(
        coverage=("coverage_4g_pct", "median"),
        use=("internet_use_pct", "median"),
        gap=("availability_use_gap_pp", "median"),
        n=("iso3", "nunique"),
    )
    fig, (ax, axn) = plt.subplots(
        2, 1, figsize=(11, 7.4), sharex=True,
        gridspec_kw={"height_ratios": [4, 1], "hspace": 0.08},
    )
    ax.plot(g["year"], g["coverage"], color=ORANGE, marker="o", label="median 4G/LTE coverage")
    ax.plot(g["year"], g["use"], color=BLUE, marker="o", label="median internet use")
    ax.fill_between(g["year"], g["use"], g["coverage"], color="#e8c7bb", alpha=0.35)
    ax.set_ylabel("Cross-sectional median (%)")
    ax.set_title(
        "Availability rose faster than use, but the annual comparison sample also changed",
        loc="left", fontsize=15, weight="bold", pad=18,
    )
    ax.text(0, 1.01, "Medians use exact-year pairs only; the lower panel shows the changing denominator", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.legend(frameon=False, ncol=2, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=GRID)
    axn.bar(g["year"], g["n"], color="#9fb2bc", width=0.72)
    axn.set_ylabel("n")
    axn.set_xlabel("Year")
    axn.spines[["top", "right", "left"]].set_visible(False)
    axn.tick_params(axis="y", length=0)
    for row in g.itertuples():
        axn.text(row.year, row.n + 0.5, str(row.n), ha="center", fontsize=8)
    add_source(fig, "Source: ITU DataHub i271GA and i99H. No missing value is carried across years.")
    fig.tight_layout()
    return save(fig, "04-components-over-time")


def figure_05_balanced_change(panel: pd.DataFrame, start: int, end: int) -> tuple[dict, dict]:
    a = panel[panel["year"] == start].set_index("iso3")
    b = panel[panel["year"] == end].set_index("iso3")
    common = sorted(set(a.index) & set(b.index))
    change = pd.DataFrame({
        "country": b.loc[common, "country"],
        "gap_start": a.loc[common, "availability_use_gap_pp"],
        "gap_end": b.loc[common, "availability_use_gap_pp"],
    })
    change["change_pp"] = change["gap_end"] - change["gap_start"]
    change = change.sort_values("change_pp")
    fig, ax = plt.subplots(figsize=(10.8, max(6.5, len(change) * 0.36)))
    y = np.arange(len(change))
    ax.hlines(y, change["gap_start"], change["gap_end"], color="#b7c3ca", lw=2.2)
    ax.scatter(change["gap_start"], y, color="#7b8790", s=35, label=str(start), zorder=3)
    ax.scatter(change["gap_end"], y, color=BLUE, s=35, label=str(end), zorder=3)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(y, change["country"])
    ax.set_xlabel("Availability–use gap (percentage points)")
    ax.set_title(
        f"The gap changed unevenly in the {len(common)}-economy {start}–{end} balanced sample",
        loc="left", fontsize=15, weight="bold", pad=18,
    )
    ax.text(0, 1.01, "A falling gap can reflect faster use growth, slower coverage growth, or revised source values", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.legend(frameon=False, loc="lower right")
    finish_axis(ax)
    add_source(fig, "Source: ITU DataHub i271GA and i99H. Only economies observed in both anchor years are shown.")
    fig.tight_layout()
    metrics = {
        "start_year": start,
        "end_year": end,
        "economies": len(common),
        "median_change_pp": float(change["change_pp"].median()) if len(change) else None,
        "gap_narrowed": int((change["change_pp"] < 0).sum()),
        "gap_widened": int((change["change_pp"] > 0).sum()),
    }
    return save(fig, "05-balanced-gap-change"), metrics


def figure_06_affordability(headline: pd.DataFrame, year: int) -> tuple[dict, dict]:
    d = headline.dropna(subset=["mobile_5gb_pct_gni"]).copy()
    stats = correlation(d["mobile_5gb_pct_gni"], d["availability_use_gap_pp"])
    fig, ax = plt.subplots(figsize=(9.5, 7.8))
    ax.scatter(d["mobile_5gb_pct_gni"], d["availability_use_gap_pp"], color=BLUE, s=55, alpha=0.9)
    for row in d.itertuples():
        if row.mobile_5gb_pct_gni >= 5 or abs(row.availability_use_gap_pp) >= 40:
            ax.annotate(row.country, (row.mobile_5gb_pct_gni, row.availability_use_gap_pp), xytext=(5, 5), textcoords="offset points", fontsize=8.5)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(2, color=ORANGE, ls="--", lw=1.1, label="Broadband Commission 2% reference")
    ax.set_xscale("log")
    ax.set_xlabel("5 GB mobile-data basket (% of GNI per capita, log scale)")
    ax.set_ylabel("Availability–use gap (percentage points)")
    ax.set_title(
        f"The 5 GB basket alone does not explain the availability–use gap ({year})",
        loc="left", fontsize=15, weight="bold", pad=18,
    )
    ax.text(0, 1.01, f"Exact-year matches: n={stats['n']}; Spearman ρ={stats['spearman_rho']:.2f}", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=GRID, lw=0.8)
    ax.legend(frameon=False, loc="lower right")
    add_source(fig, "Source: ITU DataHub i271GA, i99H, and i271mb_5GB_GNI. Association is descriptive; the basket is not a household-incidence measure.")
    fig.tight_layout()
    return save(fig, "06-affordability-association"), stats


def figure_07_rural(headline: pd.DataFrame, year: int) -> tuple[dict, dict]:
    d = headline.dropna(subset=["urban_rural_use_gap_pp"]).copy()
    stats = correlation(d["urban_rural_use_gap_pp"], d["availability_use_gap_pp"])
    fig, ax = plt.subplots(figsize=(9.3, 7.6))
    ax.scatter(d["urban_rural_use_gap_pp"], d["availability_use_gap_pp"], s=60, color=PURPLE)
    for row in d.itertuples():
        ax.annotate(row.country, (row.urban_rural_use_gap_pp, row.availability_use_gap_pp), xytext=(5, 5), textcoords="offset points", fontsize=8.4)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlabel("Urban minus rural internet-use rate (percentage points)")
    ax.set_ylabel("Availability–use gap (percentage points)")
    ax.set_title(
        f"The national gap can coexist with a second divide inside economies ({year})",
        loc="left", fontsize=15, weight="bold", pad=18,
    )
    ax.text(0, 1.01, f"Exact-year matches: n={stats['n']}; Spearman ρ={stats['spearman_rho']:.2f}; small-sample diagnostic only", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=GRID, lw=0.8)
    add_source(fig, "Source: ITU DataHub national i99H and rural/urban disaggregations. The small matched sample does not support generalization to all DMCs.")
    fig.tight_layout()
    return save(fig, "07-urban-rural-use-gap"), stats


def figure_08_source_mix(headline: pd.DataFrame, year: int) -> tuple[dict, dict]:
    d = headline.copy()
    d["source_group"] = np.where(
        d["coverage_source"].str.lower().str.contains("itu estimate")
        & d["internet_use_source"].str.lower().str.contains("itu estimate"),
        "Both ITU estimates", "At least one national/other source",
    )
    groups = [
        d.loc[d["source_group"] == label, "availability_use_gap_pp"].to_numpy()
        for label in ("Both ITU estimates", "At least one national/other source")
    ]
    fig, ax = plt.subplots(figsize=(9.4, 6.8))
    bp = ax.boxplot(groups, tick_labels=[f"Both ITU estimates\n(n={len(groups[0])})", f"At least one national/other source\n(n={len(groups[1])})"], patch_artist=True, widths=0.5)
    for patch, color in zip(bp["boxes"], [BLUE, ORANGE]):
        patch.set_facecolor(color); patch.set_alpha(0.75)
    for median_line in bp["medians"]:
        median_line.set_color(INK); median_line.set_linewidth(1.5)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_ylabel("Availability–use gap (percentage points)")
    ax.set_title(
        f"Source provenance changes the uncertainty story, not the sign of the median ({year})",
        loc="left", fontsize=15, weight="bold", pad=18,
    )
    ax.text(0, 1.01, "Groups are defined from the source strings returned with each ITU observation", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=GRID)
    metrics = {
        "both_itu_estimates_n": int(len(groups[0])),
        "both_itu_estimates_median_gap_pp": float(np.median(groups[0])) if len(groups[0]) else None,
        "other_or_mixed_n": int(len(groups[1])),
        "other_or_mixed_median_gap_pp": float(np.median(groups[1])) if len(groups[1]) else None,
    }
    add_source(fig, "Source: ITU DataHub source strings accompanying i271GA and i99H. This is a provenance diagnostic, not an accuracy ranking.")
    fig.tight_layout()
    return save(fig, "08-source-provenance"), metrics


def figure_09_sensitivity(summary: dict) -> dict:
    labels = ["25% floor", "50% floor", "75% floor"]
    keys = ["minus_50pct", "baseline", "plus_50pct"]
    values = [summary["sensitivity"][key]["median_gap_pp"] for key in keys]
    years = [summary["sensitivity"][key]["headline_year"] for key in keys]
    ns = [summary["sensitivity"][key]["paired_economies"] for key in keys]
    fig, ax = plt.subplots(figsize=(9.6, 6.3))
    bars = ax.bar(labels, values, color=["#9fbcc8", BLUE, "#315f73"], width=0.58)
    ax.set_ylim(0, max(values) * 1.20)
    for bar, value, year, n in zip(bars, values, years, ns):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.22, f"{value:.1f} pp\n{year}; n={n}", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Median availability–use gap (percentage points)")
    ax.set_title("The headline year and median survive the ±50% sample-floor check", loc="left", fontsize=15, weight="bold", pad=18)
    ax.text(0, 1.01, "The baseline requires half of the 44-economy roster; sensitivity uses one-quarter and three-quarters", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", color=GRID)
    ax.tick_params(axis="y", length=0)
    add_source(fig, "Source: committed selection rule applied to ITU exact-year pairs. No value is carried across years.")
    fig.tight_layout()
    return save(fig, "09-sample-floor-sensitivity")


def figure_10_heatmap(panel: pd.DataFrame, roster: list[dict]) -> dict:
    years = list(range(2012, 2025))
    countries = [item["country"] for item in roster]
    iso_order = [item["iso3"] for item in roster]
    observed = {(row.iso3, int(row.year)) for row in panel.itertuples()}
    matrix = np.array([[1 if (iso, year) in observed else 0 for year in years] for iso in iso_order])
    fig, ax = plt.subplots(figsize=(11.2, 12.5))
    ax.imshow(matrix, aspect="auto", cmap=plt.matplotlib.colors.ListedColormap(["#f1f3f4", BLUE]), vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(years)), years, rotation=45, ha="right")
    ax.set_yticks(np.arange(len(countries)), countries)
    ax.set_title("Exact-year comparability improved, but five roster economies never form a pair", loc="left", fontsize=15, weight="bold", pad=18)
    ax.text(0, 1.01, "Blue cells contain both 4G/LTE coverage and internet-use observations", transform=ax.transAxes, color=MUTED, fontsize=10)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    add_source(fig, "Source: ITU DataHub i271GA and i99H. Grey means no exact-year pair, not zero connectivity.")
    fig.tight_layout()
    return save(fig, "10-pair-availability-heatmap")


def figure_11_funnel(summary: dict) -> dict:
    steps = [
        ("Repository DMC roster", summary["roster_n"]),
        ("Any exact-year pair, 2012–2024", summary["panel_economies"]),
        (f"Headline pair in {summary['headline_year']}", summary["headline"]["paired_economies"]),
        (f"Headline + 5 GB price", summary["secondary_exact_match_counts"]["headline_mobile_5gb_pct_gni"]),
        (f"Headline + rural/urban use", summary["secondary_exact_match_counts"]["headline_urban_rural_use_gap"]),
    ]
    fig, ax = plt.subplots(figsize=(10.8, 6.6))
    labels, values = zip(*steps)
    y = np.arange(len(steps))
    bars = ax.barh(y, values, color=["#355d6d", "#527f91", BLUE, "#4f8f78", PURPLE], height=0.62)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(values) * 1.16)
    for bar, value in zip(bars, values):
        ax.text(value + 0.7, bar.get_y() + bar.get_height()/2, str(value), va="center", weight="bold")
    ax.set_xlabel("Economies")
    ax.set_title("Every additional question reduces the defensible comparison sample", loc="left", fontsize=15, weight="bold", pad=18)
    ax.text(0, 1.01, "The study reports each denominator instead of treating the 44-economy roster as observed", transform=ax.transAxes, color=MUTED, fontsize=10)
    finish_axis(ax)
    add_source(fig, "Source: committed DMC roster and exact-year ITU joins. No missing values are imputed.")
    fig.tight_layout()
    return save(fig, "11-coverage-funnel")


def figure_12_claim_gate() -> dict:
    fig, ax = plt.subplots(figsize=(12, 7.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7.2); ax.axis("off")
    ax.text(0.2, 6.75, "What the measurement supports—and where inference must stop", fontsize=17, weight="bold", color=INK)
    ax.text(0.2, 6.35, "A visual claim gate for the availability–use study", fontsize=10.5, color=MUTED)
    boxes = [
        (0.35, 4.2, 3.1, 1.45, "Availability", "ITU 4G/LTE population coverage\nwithin signal range", ORANGE),
        (4.45, 4.2, 3.1, 1.45, "Use", "ITU individuals using the Internet\nin the previous three months", BLUE),
        (8.55, 4.2, 3.1, 1.45, "Supported result", "Exact-year percentage-point\navailability–use difference", GREEN),
    ]
    for x, y, w, h, title, body, color in boxes:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08", facecolor="white", edgecolor=color, linewidth=2)
        ax.add_patch(patch); ax.text(x+0.18, y+h-0.38, title, weight="bold", fontsize=11.5, color=color); ax.text(x+0.18, y+0.33, body, fontsize=9.3, color=INK, va="bottom")
    ax.annotate("", xy=(4.2, 4.92), xytext=(3.55, 4.92), arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1.8})
    ax.annotate("", xy=(8.3, 4.92), xytext=(7.65, 4.92), arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1.8})
    ax.text(0.4, 2.95, "Secondary diagnostics", fontsize=12, weight="bold", color=INK)
    ax.text(0.4, 2.5, "5 GB basket affordability  •  urban–rural use difference  •  source provenance  •  sample sensitivity", fontsize=10.2, color=GREEN)
    ax.plot([0.4, 11.6], [2.05, 2.05], color=GRID, lw=1.2)
    ax.text(0.4, 1.55, "Not identified by this design", fontsize=12, weight="bold", color=ORANGE)
    ax.text(0.4, 0.92, "Speed  •  latency  •  reliability  •  household affordability  •  digital skills  •  welfare  •  causal policy effects", fontsize=10.3, color=INK)
    ax.text(0.4, 0.42, "Ookla can later add performance conditional on testing; it cannot validate adoption or explain why people remain offline.", fontsize=9.3, color=MUTED)
    fig.tight_layout()
    return save(fig, "12-method-and-claim-gate")


def main() -> int:
    panel = pd.read_csv(PANEL_PATH)
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    year = int(summary["headline_year"])
    headline = panel[panel["year"] == year].copy()
    for column in ["mobile_5gb_pct_gni", "urban_rural_use_gap_pp"]:
        headline[column] = pd.to_numeric(headline[column], errors="coerce")

    figure_records = []
    def record(number: int, title: str, job: str, guard: str, paths: dict) -> None:
        figure_records.append({"number": number, "title": title, "evidence_job": job, "claim_guard": guard, "files": paths})

    record(1, "Availability–use gap hero", "Show every signed headline gap", "Difference, not unobserved users", figure_01_hero(headline, year))
    record(2, "Coverage and use components", "Expose both inputs behind each gap", "No direct gap observation", figure_02_components(headline, year))
    record(3, "Coverage–use scatter", "Test whether high availability implies high use", "No causal quadrant labels", figure_03_scatter(headline, year))
    record(4, "Components over time", "Show cross-sectional evolution and denominator", "Changing sample is visible", figure_04_time(panel))
    paths, balanced = figure_05_balanced_change(panel, 2018, year)
    record(5, "Balanced change", "Separate time pattern from changing membership", "Descriptive anchor years", paths)
    paths, affordability = figure_06_affordability(headline, year)
    record(6, "Affordability association", "Test one plausible correlate", "Association is not explanation", paths)
    paths, rural = figure_07_rural(headline, year)
    record(7, "Urban–rural use gap", "Expose a within-economy divide", "Small matched sample", paths)
    paths, source_mix = figure_08_source_mix(headline, year)
    record(8, "Source provenance", "Show estimate/reporting mix", "Not an accuracy ranking", paths)
    record(9, "Sample-floor sensitivity", "Apply ±50% rule to headline-year selection", "Sample rule only", figure_09_sensitivity(summary))
    roster = sorted(
        summary["excluded_headline_economies"] + [
            {"iso3": row.iso3, "country": row.country}
            for row in headline[["iso3", "country"]].drop_duplicates().itertuples()
        ], key=lambda item: item["country"],
    )
    record(10, "Pair-availability heatmap", "Show every missing exact-year pair", "Grey is missing, not zero", figure_10_heatmap(panel, roster))
    record(11, "Coverage funnel", "Expose denominators for each question", "No 44-economy generalization", figure_11_funnel(summary))
    record(12, "Method and claim gate", "Separate supported and unsupported inference", "Infographic carries nonclaims", figure_12_claim_gate())

    metrics = {
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
        "program": "digital-performance",
        "headline_year": year,
        "headline": summary["headline"],
        "affordability_association": affordability,
        "urban_rural_association": rural,
        "source_provenance": source_mix,
        "balanced_change": balanced,
        "figures": figure_records,
    }
    (OUT / "digital-performance-figure-dossier.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (PROGRAM / "sensitivity-runs.json").write_text(
        json.dumps({
            "program": "digital-performance",
            "attestation_chain": "ai-first",
            "generated_at": now_iso(),
            "sample_floor_sensitivity": summary["sensitivity"],
            "balanced_change": balanced,
            "affordability_association": affordability,
            "urban_rural_association": rural,
            "source_provenance": source_mix,
        }, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "figures": len(figure_records),
        "headline": summary["headline"],
        "affordability": affordability,
        "urban_rural": rural,
        "balanced_change": balanced,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
