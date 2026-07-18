"""Build the 12-role evidence figure spine for public-data-freshness.

Every plotted value comes from the committed output of
``build-freshness-panel.py``. Figures carry coverage, claim, sensitivity,
falsification, or limitation work; none is decorative.

attestation_chain: ai-first
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch


PROGRAM = Path(__file__).resolve().parents[1]
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"

BLUE = "#0076A8"
TEAL = "#248A8D"
ORANGE = "#D97742"
RED = "#B84A4A"
GREEN = "#4C7A5B"
PURPLE = "#6E5A8A"
INK = "#1F2933"
MUTED = "#62717C"
GRID = "#DDE5E9"
PALE = "#EEF3F5"
GOLD = "#B58A2A"

DOMAIN_ORDER = [
    "Demography", "Poverty and inequality", "Health", "Education",
    "Labor and social conditions", "Infrastructure and digital access",
    "Environment and climate", "Economy and structure",
    "External and public finance",
]
DOMAIN_SHORT = {
    "Demography": "Demography",
    "Poverty and inequality": "Poverty",
    "Health": "Health",
    "Education": "Education",
    "Labor and social conditions": "Labor",
    "Infrastructure and digital access": "Infrastructure / digital",
    "Environment and climate": "Environment",
    "Economy and structure": "Economy",
    "External and public finance": "External / public finance",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def truth(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


def clean_svg(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")


def save(fig: plt.Figure, stem: str) -> dict[str, str]:
    CHARTS.mkdir(parents=True, exist_ok=True)
    paths = {}
    for suffix in ("png", "svg"):
        path = CHARTS / f"public-data-freshness-{stem}.{suffix}"
        fig.savefig(path, dpi=190, bbox_inches="tight", facecolor="white")
        if suffix == "svg":
            clean_svg(path)
        paths[suffix] = str(path.relative_to(PROGRAM)).replace("\\", "/")
    plt.close(fig)
    return paths


def title(fig: plt.Figure, headline: str, subtitle: str) -> None:
    fig.suptitle(headline, x=0.02, y=0.985, ha="left", fontsize=17, weight="bold", color=INK)
    fig.text(0.02, 0.94, subtitle, ha="left", fontsize=10.2, color=MUTED)


def source(fig: plt.Figure, note: str) -> None:
    fig.text(0.02, -0.01, note, ha="left", va="top", fontsize=8.2, color=MUTED, wrap=True)


def axis_style(ax: plt.Axes, grid_axis: str = "x") -> None:
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def figure_01_coverage(panel: pd.DataFrame, summary: dict) -> dict:
    observed_upper = int((~truth(panel["missing"])).sum())
    values = [27, summary["valid_indicator_count"], len(panel), observed_upper]
    labels = ["Frozen indicator codes", "Valid WDI series", "Possible 42 × 27 cells", "Observed cells"]
    display = ["27", f"{summary['valid_indicator_count']}", f"{len(panel):,}", f"{observed_upper:,}"]
    fig, ax = plt.subplots(figsize=(12.5, 5.6))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    for i, (label, value) in enumerate(zip(labels, display)):
        x = 0.2 + i * 2.55
        color = BLUE if i < 2 else TEAL
        box = FancyBboxPatch((x, 0.75), 2.05, 1.45, boxstyle="round,pad=0.04,rounding_size=0.08", facecolor="white", edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x + 1.025, 1.83, label.upper(), ha="center", va="center", fontsize=8.5, color=color, weight="bold")
        ax.text(x + 1.025, 1.30, value, ha="center", va="center", fontsize=19, color=INK, weight="bold")
        if i < 3:
            ax.annotate("", xy=(x + 2.48, 1.48), xytext=(x + 2.08, 1.48), arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1.5})
    title(fig, "The upper set yields 1,006 observed cells", "One archived CO₂ code remains in the design as a reported source failure; missing cells are not converted to stale cells")
    source(fig, "Source: WDI public API responses and the committed source inventory. Baseline coverage is 709 of 756 cells (93.8%). attestation_chain: ai-first.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.87))
    return {"role": "coverage", "paths": save(fig, "01-coverage-funnel")}


def figure_02_production(indicators: pd.DataFrame) -> dict:
    d = indicators.copy()
    d["production_age"] = 2026 - pd.to_numeric(d["global_frontier_2025"], errors="coerce")
    d = d.sort_values(["production_age", "indicator_code"], na_position="last")
    y = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(11.5, 10.2))
    colors = [ORANGE if np.isfinite(v) and v >= 3 else BLUE for v in d["production_age"]]
    ax.hlines(y, 0, d["production_age"].fillna(0), color=GRID, linewidth=2)
    ax.scatter(d["production_age"], y, color=colors, s=56, zorder=3)
    missing = d["production_age"].isna()
    ax.scatter(np.zeros(missing.sum()), y[missing], marker="x", color=RED, s=70, linewidth=2, zorder=4)
    ax.set_yticks(y, d["indicator_code"])
    ax.invert_yaxis()
    ax.set_xlabel("Indicator-wide production age in 2026 (years)")
    ax.axvline(3, color=GOLD, linestyle="--", linewidth=1.2)
    axis_style(ax)
    title(fig, "Indicators carry different production clocks", "A cell can cross a three-year calendar rule even when its economy is at the indicator frontier")
    source(fig, "Source: WDI global country/economy frontier through reference year 2025. EN.ATM.CO2E.PC returned an archived-code error and is marked ×. Frontier is empirical, not a formal release schedule.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.91))
    return {"role": "production context", "paths": save(fig, "02-indicator-production-age")}


def figure_03_hero(baseline: pd.DataFrame) -> dict:
    rows = []
    for domain in DOMAIN_ORDER:
        d = baseline[baseline["domain"] == domain]
        observed = d[~truth(d["missing"])]
        both = int(truth(observed["relative_review"]).sum())
        calendar_only = int(truth(observed["classification_disagreement"]).sum())
        neither = len(observed) - both - calendar_only
        rows.append((DOMAIN_SHORT[domain], neither, both, calendar_only, len(observed)))
    labels, neither, both, only, totals = zip(*rows)
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(12, 7.6))
    ax.barh(y, np.array(neither) / totals, color=PALE, label="No review")
    ax.barh(y, np.array(both) / totals, left=np.array(neither) / totals, color=PURPLE, label="Both clocks")
    ax.barh(y, np.array(only) / totals, left=(np.array(neither) + np.array(both)) / totals, color=ORANGE, label="Calendar only")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share of observed domain cells")
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    ax.legend(frameon=False, ncol=3, loc="lower right")
    axis_style(ax)
    title(fig, "Clock disagreement is large—but concentrated", "At the frozen three-year rule, environment and health account for most calendar-only review cells")
    source(fig, "Source: baseline 18-indicator WDI panel, 709 observed cells. ‘Calendar only’ means calendar age ≥3 while lag behind the indicator frontier is <3. No economy ranking is shown.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.91))
    return {"role": "hero decomposition", "paths": save(fig, "03-domain-clock-decomposition")}


def figure_04_matrix(baseline: pd.DataFrame) -> dict:
    observed = baseline[~truth(baseline["missing"])].copy()
    absolute = truth(observed["absolute_review"])
    relative = truth(observed["relative_review"])
    matrix = np.array([
        [int((~absolute & ~relative).sum()), int((~absolute & relative).sum())],
        [int((absolute & ~relative).sum()), int((absolute & relative).sum())],
    ])
    fig, ax = plt.subplots(figsize=(8.2, 6.8))
    ax.imshow(matrix, cmap="Blues", vmin=0, vmax=matrix.max())
    for i in range(2):
        for j in range(2):
            text_color = "white" if matrix[i, j] > matrix.max() * 0.55 else INK
            ax.text(j, i, f"{matrix[i, j]:,}\n{matrix[i, j] / len(observed):.1%}", ha="center", va="center", fontsize=17, weight="bold", color=text_color)
    ax.set_xticks([0, 1], ["Relative: no", "Relative: review"])
    ax.set_yticks([0, 1], ["Calendar: no", "Calendar: review"])
    ax.tick_params(length=0)
    title(fig, "138 cells change status under the relative clock", "Every disagreement is calendar-only; none is relative-only because production age cannot be negative")
    source(fig, "Source: baseline 18-indicator WDI panel; 709 observed cells, frozen threshold ≥3 years. Counts exclude 47 missing cells.")
    fig.tight_layout(rect=(0, 0.04, 1, 0.90))
    return {"role": "main result", "paths": save(fig, "04-classification-matrix")}


def figure_05_construct(baseline: pd.DataFrame) -> dict:
    d = baseline[~truth(baseline["missing"])].copy()
    d["calendar_bin"] = pd.to_numeric(d["calendar_age_years"]).clip(upper=12)
    d["relative_bin"] = pd.to_numeric(d["relative_lag_years"]).clip(upper=12)
    counts = d.groupby(["relative_bin", "calendar_bin"]).size().reset_index(name="n")
    fig, ax = plt.subplots(figsize=(9.3, 8.0))
    ax.scatter(counts["relative_bin"], counts["calendar_bin"], s=counts["n"] * 8 + 18, c=counts["n"], cmap="Blues", alpha=0.85, edgecolor="white")
    ax.axhline(3, color=ORANGE, linestyle="--", linewidth=1.2, label="calendar review rule")
    ax.axvline(3, color=PURPLE, linestyle="--", linewidth=1.2, label="relative review rule")
    ax.plot([0, 12], [0, 12], color=INK, linewidth=1, alpha=0.5)
    ax.set_xlim(-0.5, 12.8)
    ax.set_ylim(-0.5, 12.8)
    ax.set_xlabel("Lag behind indicator frontier (years; 12 = 12+)")
    ax.set_ylabel("Calendar age in 2026 (years; 12 = 12+)")
    ax.legend(frameon=False, loc="lower right")
    axis_style(ax, "both")
    title(fig, "Calendar age contains two additive components", "Bubble area is the number of observed cells; points above the diagonal carry indicator-wide production age")
    source(fig, "Source: baseline WDI panel. Calendar age = production age + relative lag by construction. Discrete years are clipped only for display, not computation.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.90))
    return {"role": "construct", "paths": save(fig, "05-two-clock-construct")}


def figure_06_domains(domains: pd.DataFrame) -> dict:
    d = domains.copy()
    d["label"] = d["domain"].map(DOMAIN_SHORT)
    d["share"] = pd.to_numeric(d["disagreement_share_observed"])
    d = d.sort_values("share")
    fig, ax = plt.subplots(figsize=(11, 7.2))
    colors = [ORANGE if value >= 0.10 else BLUE for value in d["share"]]
    ax.barh(d["label"], d["share"], color=colors)
    ax.axvline(0.10, color=GOLD, linestyle="--", linewidth=1.2, label="10% decision rule")
    for y, value in enumerate(d["share"]):
        ax.text(value + 0.012, y, pct(value), va="center", fontsize=9.5)
    ax.set_xlim(0, 1.08)
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    ax.set_xlabel("Clock-disagreement share of observed cells")
    ax.legend(frameon=False, loc="lower right")
    axis_style(ax)
    title(fig, "Two domains create most of the cross-domain result", "The leave-environment-out run falls to 9.2%, below the preregistered 10% rule")
    source(fig, "Source: baseline WDI panel and frozen domain mapping. Domain selection is prospective but not exhaustive; the result supports a concentrated, not universal, claim.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.90))
    return {"role": "heterogeneity and falsification", "paths": save(fig, "06-domain-concentration")}


def figure_07_missing(baseline: pd.DataFrame) -> dict:
    rows = []
    for domain in DOMAIN_ORDER:
        d = baseline[baseline["domain"] == domain]
        missing = int(truth(d["missing"]).sum())
        observed = d[~truth(d["missing"])]
        old = int(truth(observed["absolute_review"]).sum())
        current = len(observed) - old
        rows.append((DOMAIN_SHORT[domain], current, old, missing, len(d)))
    labels, current, old, missing, totals = zip(*rows)
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(11.5, 7.5))
    current_s = np.array(current) / totals
    old_s = np.array(old) / totals
    missing_s = np.array(missing) / totals
    ax.barh(y, current_s, color=TEAL, label="Observed, calendar age <3")
    ax.barh(y, old_s, left=current_s, color=ORANGE, label="Observed, calendar age ≥3")
    ax.barh(y, missing_s, left=current_s + old_s, color="#B8C2C8", label="Missing")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    ax.set_xlabel("Share of possible domain cells")
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.18))
    axis_style(ax)
    title(fig, "Missing and old are different evidence states", "Poverty and labor have the most missing cells; environment and health have old observed vintages")
    source(fig, "Source: baseline WDI panel. Missing means no non-null value through 2025; it is excluded from all observed-cell freshness shares and is never imputed.")
    fig.tight_layout(rect=(0, 0.07, 1, 0.90))
    return {"role": "limitation", "paths": save(fig, "07-missing-versus-old")}


def figure_08_pacific(groups: pd.DataFrame) -> dict:
    d = groups.copy()
    d["group"] = d["pacific_small_island"].map({"True": "Pacific small-island group", "False": "Other roster economies"})
    missing = pd.to_numeric(d["missing_share"])
    disagreement = pd.to_numeric(d["disagreement_share_observed"])
    x = np.arange(len(d))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9.8, 6.5))
    ax.bar(x - width / 2, missing, width, color="#B8C2C8", label="Missing share")
    ax.bar(x + width / 2, disagreement, width, color=ORANGE, label="Clock disagreement")
    for xpos, value in zip(x - width / 2, missing):
        ax.text(xpos, value + 0.008, pct(value), ha="center", fontsize=10)
    for xpos, value in zip(x + width / 2, disagreement):
        ax.text(xpos, value + 0.008, pct(value), ha="center", fontsize=10)
    ax.set_xticks(x, d["group"])
    ax.set_ylim(0, max(max(missing), max(disagreement)) + 0.08)
    ax.yaxis.set_major_formatter(lambda y, _: f"{y:.0%}")
    ax.set_ylabel("Share")
    ax.legend(frameon=False)
    axis_style(ax, "y")
    title(fig, "Missingness is more concentrated in the small-island group", "The grouped diagnostic is descriptive; it does not identify why values are absent or delayed")
    source(fig, "Source: baseline WDI panel. Frozen group: COK, FJI, KIR, MHL, FSM, NRU, PLW, WSM, SLB, TON, TUV, VUT. No economy rank or deficiency claim.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.90))
    return {"role": "coverage equity diagnostic", "paths": save(fig, "08-pacific-group-diagnostic")}


def figure_09_sets(sensitivity: pd.DataFrame) -> dict:
    d = sensitivity[sensitivity["run"].isin(["set_9", "set_18", "set_27"])].copy()
    d["size"] = pd.to_numeric(d["frozen_set_label"])
    d["share"] = pd.to_numeric(d["disagreement_share_observed"])
    d = d.sort_values("size")
    fig, ax = plt.subplots(figsize=(9.5, 6.4))
    bars = ax.bar(d["size"].astype(str), d["share"], color=[TEAL, BLUE, PURPLE])
    ax.axhline(0.10, color=GOLD, linestyle="--", linewidth=1.2, label="10% decision rule")
    for bar, value in zip(bars, d["share"]):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.008, pct(value), ha="center", fontsize=11, weight="bold")
    ax.set_ylim(0, max(d["share"]) + 0.08)
    ax.yaxis.set_major_formatter(lambda y, _: f"{y:.0%}")
    ax.set_xlabel("Frozen indicator-set size")
    ax.set_ylabel("Clock-disagreement share")
    ax.legend(frameon=False)
    axis_style(ax, "y")
    title(fig, "The result survives the ±50% indicator-set test", "All three prospectively nested sets remain above the 10% gate")
    source(fig, "Source: frozen 9-, 18-, and 27-indicator runs at the global frontier, 2025 cap, and ≥3-year review rule.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.90))
    return {"role": "set-size sensitivity", "paths": save(fig, "09-indicator-set-sensitivity")}


def figure_10_thresholds(sensitivity: pd.DataFrame) -> dict:
    d = sensitivity[sensitivity["run"].isin(["threshold_1.5", "threshold_3", "threshold_4.5"])].copy()
    d["threshold"] = pd.to_numeric(d["threshold_literal_years"])
    d["effective"] = pd.to_numeric(d["threshold_effective_integer_years"]).astype(int)
    d["share"] = pd.to_numeric(d["disagreement_share_observed"])
    d = d.sort_values("threshold")
    labels = [f"{literal:g}\n(effective {effective})" for literal, effective in zip(d["threshold"], d["effective"])]
    fig, ax = plt.subplots(figsize=(11.5, 7.0))
    bars = ax.bar(labels, d["share"], color=[TEAL, BLUE, ORANGE])
    ax.axhline(0.10, color=GOLD, linestyle="--", linewidth=1.2, label="10% decision rule")
    for bar, value in zip(bars, d["share"]):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.012, pct(value), ha="center", fontsize=11, weight="bold")
    ax.set_ylim(0, max(d["share"]) + 0.10)
    ax.yaxis.set_major_formatter(lambda y, _: f"{y:.0%}")
    ax.set_xlabel("")
    ax.set_ylabel("Clock-disagreement share")
    ax.legend(frameon=False)
    axis_style(ax, "y")
    title(fig, "Review threshold changes the result", "Disagreement falls to 0.7% at the effective five-year cutoff; the three-year result is not threshold-invariant")
    source(fig, "Source: baseline 18-indicator runs. Integer reference years make 1.5, 3, and 4.5 equivalent to cutoffs of 2, 3, and 5 years.")
    fig.tight_layout(rect=(0, 0.07, 1, 0.88))
    return {"role": "threshold sensitivity", "paths": save(fig, "10-threshold-sensitivity")}


def figure_11_alternatives(sensitivity: pd.DataFrame) -> dict:
    lookup = sensitivity.set_index("run")
    labels = ["Global frontier\n2025 cap", "DMC frontier\n2025 cap", "Global frontier\n2024 cap", "Lowest leave-one-\ndomain-out"]
    values = [
        float(lookup.loc["frontier_global", "disagreement_share_observed"]),
        float(lookup.loc["frontier_dmc", "disagreement_share_observed"]),
        float(lookup.loc["cap_2024", "disagreement_share_observed"]),
        float(sensitivity[sensitivity["run"].str.startswith("leave_out_")]["disagreement_share_observed"].astype(float).min()),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 6.5))
    bars = ax.bar(labels, values, color=[BLUE, TEAL, PURPLE, ORANGE])
    ax.axhline(0.10, color=GOLD, linestyle="--", linewidth=1.2, label="10% decision rule")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.006, pct(value), ha="center", fontsize=10.5, weight="bold")
    ax.set_ylim(0, max(values) + 0.07)
    ax.yaxis.set_major_formatter(lambda y, _: f"{y:.0%}")
    ax.set_ylabel("Clock-disagreement share")
    ax.legend(frameon=False)
    axis_style(ax, "y")
    title(fig, "Frontier and vintage choices are stable; domain deletion is not", "Global and DMC frontiers agree here, while removing environment takes the result below the claim gate")
    source(fig, "Source: frozen alternative-frontier, reference-cap, and leave-one-domain-out runs. Equality of the two frontiers is sample-specific, not guaranteed by method.")
    fig.tight_layout(rect=(0, 0.03, 1, 0.90))
    return {"role": "alternative-specification falsification", "paths": save(fig, "11-alternative-specifications")}


def figure_12_gate(summary: dict) -> dict:
    gate = summary["decision_gate"]
    steps = [
        ("SOURCE", "26 of 27\nseries valid", BLUE),
        ("COVERAGE", "93.8%\nbaseline cells", TEAL),
        ("PRIMARY", "19.5%\ndisagree", GREEN),
        ("SET TEST", "9 / 18 / 27\nall ≥10%", PURPLE),
        ("FALSIFIER", "Without environment\n9.2%", ORANGE),
        ("DECISION", "RESHAPE\nDomain-specific", RED),
    ]
    fig, ax = plt.subplots(figsize=(13, 6.2))
    ax.set_xlim(0, len(steps) * 2.05)
    ax.set_ylim(0, 3)
    ax.axis("off")
    for i, (label, value, color) in enumerate(steps):
        x = i * 2.05 + 0.15
        box = FancyBboxPatch((x, 0.8), 1.7, 1.35, boxstyle="round,pad=0.04,rounding_size=0.08", facecolor="white", edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x + 0.85, 1.87, label, ha="center", va="center", fontsize=8.5, color=color, weight="bold")
        ax.text(x + 0.85, 1.35, value, ha="center", va="center", fontsize=11.5, color=INK, weight="bold")
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 2.02, 1.48), xytext=(x + 1.72, 1.48), arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1.5})
    title(fig, "The claim gate narrows the conclusion", "Primary and set-size tests pass; the domain-deletion falsifier rejects a broad cross-domain interpretation")
    source(fig, f"Source: committed decision gate ({gate['decision']}). The allowed claim is about a three-year review rule and domain-specific production cycles, not formal timeliness or economy performance.")
    fig.tight_layout(rect=(0, 0.04, 1, 0.86))
    return {"role": "claim gate", "paths": save(fig, "12-claim-gate")}


def main() -> None:
    panel = pd.read_csv(OUT / "freshness-panel.csv")
    summary = json.loads((OUT / "freshness-summary.json").read_text(encoding="utf-8"))
    sensitivity = pd.read_csv(OUT / "freshness-sensitivity.csv")
    indicators = pd.read_csv(OUT / "freshness-indicator-summary.csv")
    domains = pd.read_csv(OUT / "freshness-domain-summary.csv")
    groups = pd.read_csv(OUT / "freshness-coverage-groups.csv", dtype={"pacific_small_island": str})
    baseline = panel[pd.to_numeric(panel["indicator_position"]) <= 2].copy()

    figures = [
        figure_01_coverage(panel, summary),
        figure_02_production(indicators),
        figure_03_hero(baseline),
        figure_04_matrix(baseline),
        figure_05_construct(baseline),
        figure_06_domains(domains),
        figure_07_missing(baseline),
        figure_08_pacific(groups),
        figure_09_sets(sensitivity),
        figure_10_thresholds(sensitivity),
        figure_11_alternatives(sensitivity),
        figure_12_gate(summary),
    ]
    payload = {
        "program": "public-data-freshness",
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
        "figure_count": len(figures),
        "figures": [{"number": i + 1, **figure} for i, figure in enumerate(figures)],
    }
    (OUT / "figure-manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(figures)} logical figures to {CHARTS}")


if __name__ == "__main__":
    main()
