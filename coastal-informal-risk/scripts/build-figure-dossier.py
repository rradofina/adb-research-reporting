"""Build the evidence-bearing figure dossier for the coastal LECZ study.

Every plotted value comes from the committed GHS-UCDB processing object.
The figures describe low-elevation urban-centre exposure; they do not identify
flood hazard, informality, protection, or loss. attestation_chain: ai-first.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.ticker import FuncFormatter


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
OUT = PROGRAM / "generated"
CHARTS = OUT / "charts"
PANEL = OUT / "coastal-lecz-urban-centre-panel.csv"
DIAGNOSTICS = OUT / "coastal-lecz-growth-diagnostics.json"
SENSITIVITY = OUT / "coastal-lecz-sensitivity-runs.json"

INK = "#17202A"
MUTED = "#60707C"
GRID = "#E5E9EC"
BLUE = "#1177AA"
BLUE_LIGHT = "#DCEAF0"
ORANGE = "#D95F02"
ORANGE_LIGHT = "#F7E5DE"
GREEN = "#238B73"
RED = "#B44B4B"
GOLD = "#C99A2E"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def clean_axis(ax, grid_axis="x") -> None:
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)


def frame_title(fig, kicker: str, title: str, subtitle: str) -> None:
    fig.text(0.07, 0.94, kicker.upper(), color=ORANGE, fontsize=9, fontweight="bold")
    fig.text(0.07, 0.885, title, color=INK, fontsize=20, fontweight="bold")
    fig.text(0.07, 0.835, subtitle, color=MUTED, fontsize=10.5)


def footnote(fig, text: str) -> None:
    fig.text(0.07, 0.035, text, color=MUTED, fontsize=8.2)


def save(fig, slug: str) -> dict:
    paths = {}
    for suffix in ("png", "svg"):
        path = CHARTS / f"{slug}.{suffix}"
        fig.savefig(path, dpi=190, bbox_inches="tight")
        paths[suffix] = str(path.relative_to(ROOT)).replace("\\", "/")
    plt.close(fig)
    return paths


def panel_with_changes(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy()
    out["pop_change_10m"] = out.lecz10_population_2020 - out.lecz10_population_2000
    out["pop_change_5m"] = out.lecz5_population_2020 - out.lecz5_population_2000
    out["built_change_10m"] = out.lecz10_built_m2_2020 - out.lecz10_built_m2_2000
    out["share_change_pp"] = out.lecz10_share_pct_2020 - out.lecz10_share_pct_2000
    return out


def figure_hero(panel: pd.DataFrame, diagnostics: dict) -> dict:
    plot = panel.dropna(subset=["pop_change_10m"]).nlargest(15, "pop_change_10m").sort_values("pop_change_10m")
    fig, ax = plt.subplots(figsize=(11.8, 7.8))
    fig.subplots_adjust(left=0.23, right=0.95, top=0.76, bottom=0.14)
    y = np.arange(len(plot))
    bars = ax.barh(y, plot.pop_change_10m / 1e6, color=ORANGE, height=0.66)
    ax.set_yticks(y, [f"{r.urban_centre} · {r.iso3}" for r in plot.itertuples()])
    ax.set_xlabel("Additional population recorded below 10 m, 2000–2020 (millions)")
    clean_axis(ax)
    for bar, value in zip(bars, plot.pop_change_10m / 1e6):
        ax.text(value + 0.12, bar.get_y() + bar.get_height() / 2, f"+{value:.2f}m", va="center", fontsize=8.5)
    total = diagnostics["base_result"]["total_population_change"] / 1e6
    frame_title(fig, "Finding · reported LECZ centres", f"The recorded low-elevation population grew by {total:.1f} million", "Shanghai, Bangkok and Dhaka lead the centre-level change; fixed 2025 footprints")
    footnote(fig, "1,334 reporting centres in 24 ADB developing economies. This is exposure growth, not flood loss or informality. Source: GHS-UCDB R2024A V1.2.")
    return save(fig, "coastal-informal-risk-01-growth-hero")


def figure_dumbbell(panel: pd.DataFrame) -> dict:
    plot = panel.dropna(subset=["pop_change_10m"]).nlargest(18, "pop_change_10m").sort_values("pop_change_10m")
    fig, ax = plt.subplots(figsize=(11.8, 8.5))
    fig.subplots_adjust(left=0.24, right=0.95, top=0.76, bottom=0.14)
    y = np.arange(len(plot))
    for idx, row in enumerate(plot.itertuples()):
        ax.plot([row.lecz10_population_2000 / 1e6, row.lecz10_population_2020 / 1e6], [idx, idx], color=GRID, lw=5)
    ax.scatter(plot.lecz10_population_2000 / 1e6, y, color=MUTED, s=40, label="2000", zorder=3)
    ax.scatter(plot.lecz10_population_2020 / 1e6, y, color=ORANGE, s=58, label="2020", zorder=3)
    ax.set_yticks(y, [f"{r.urban_centre} · {r.iso3}" for r in plot.itertuples()])
    ax.set_xlabel("Population recorded below 10 m (millions)")
    ax.legend(frameon=False, ncol=2, loc="lower right")
    clean_axis(ax)
    frame_title(fig, "Scale · centre trajectories", "The increase is concentrated in named urban centres", "Largest absolute changes, 2000–2020")
    footnote(fig, "Both endpoints are zonal statistics inside each centre's fixed 2025 footprint; boundary growth is not being compared.")
    return save(fig, "coastal-informal-risk-02-centre-dumbbell")


def figure_proxy(diagnostics: dict) -> dict:
    old = diagnostics["proxy_falsification"]["inherited_top5_economies"]
    new = diagnostics["proxy_falsification"]["observed_top5_economies_by_aggregated_centre_change"]
    labels = list(dict.fromkeys(old + new))
    fig, ax = plt.subplots(figsize=(10.6, 6.6))
    fig.subplots_adjust(left=0.08, right=0.92, top=0.76, bottom=0.13)
    for y, iso in enumerate(labels[::-1]):
        a = old.index(iso) + 1 if iso in old else None
        b = new.index(iso) + 1 if iso in new else None
        if a and b:
            ax.plot([0, 1], [y, y], color="#BFD2DD", lw=3)
        ax.scatter(0, y, s=105, color=BLUE if a else GRID, edgecolor="white")
        ax.scatter(1, y, s=105, color=ORANGE if b else GRID, edgecolor="white")
        ax.text(-0.08, y, f"{a}. {iso}" if a else iso, ha="right", va="center", fontsize=11)
        ax.text(1.08, y, f"{b}. {iso}" if b else iso, ha="left", va="center", fontsize=11)
    ax.text(0, len(labels) + 0.1, "Inherited national proxy", ha="center", fontweight="bold")
    ax.text(1, len(labels) + 0.1, "Observed centre aggregation", ha="center", fontweight="bold")
    ax.set_xlim(-0.7, 1.7); ax.set_ylim(-0.8, len(labels) + 0.8); ax.axis("off")
    frame_title(fig, "Falsification · construct", "Only two of the old top five remain", "The proxy and the spatial object answer different questions")
    footnote(fig, "Observed side ranks economy totals of centre-level population change below 10 m. Neither side is a coastal-risk ranking.")
    return save(fig, "coastal-informal-risk-03-proxy-falsification")


def figure_economies(diagnostics: dict) -> dict:
    plot = pd.DataFrame(diagnostics["base_result"]["top10_economies_population_change"]).sort_values("change")
    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    fig.subplots_adjust(left=0.20, right=0.95, top=0.76, bottom=0.15)
    y = np.arange(len(plot))
    ax.barh(y, plot.change / 1e6, color=BLUE, height=0.66)
    ax.set_yticks(y, [f"{r.economy} · {r.iso3}" for r in plot.itertuples()])
    ax.set_xlabel("Aggregated centre-level population change below 10 m (millions)")
    clean_axis(ax)
    frame_title(fig, "Aggregation · economy context", "China accounts for the largest recorded increase", "Top ten economy sums across reporting urban centres, 2000–2020")
    footnote(fig, "Economy totals are context, not performance scores. Coverage is defined by reported UCDB LECZ fields.")
    return save(fig, "coastal-informal-risk-04-economy-aggregation")


def figure_threshold(sensitivity: list[dict]) -> dict:
    plot = pd.DataFrame(sensitivity)
    plot = plot[plot.window_years == 20].sort_values("threshold_m")
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.74, bottom=0.17)
    bars = ax.bar(["Below 5 m", "Below 10 m"], plot.total_population_change / 1e6, color=[BLUE, ORANGE], width=0.58)
    for bar, value in zip(bars, plot.total_population_change / 1e6):
        ax.text(bar.get_x() + bar.get_width()/2, value + 2, f"+{value:.1f}m", ha="center", fontweight="bold")
    ax.set_ylabel("Population change, 2000–2020 (millions)")
    clean_axis(ax, "y")
    frame_title(fig, "Sensitivity · elevation", "The magnitude changes; the direction does not", "Direct 5-metre and 10-metre definitions")
    footnote(fig, "The 5 m result is the stricter spatial definition. Both use the same fixed urban-centre footprints.")
    return save(fig, "coastal-informal-risk-05-elevation-sensitivity")


def figure_windows(sensitivity: list[dict]) -> dict:
    plot = pd.DataFrame(sensitivity)
    fig, ax = plt.subplots(figsize=(9.8, 6.2))
    fig.subplots_adjust(left=0.12, right=0.95, top=0.76, bottom=0.16)
    for threshold, color, label in [(5, BLUE, "Below 5 m"), (10, ORANGE, "Below 10 m")]:
        part = plot[plot.threshold_m == threshold].sort_values("window_years")
        ax.plot(part.window_years, part.total_population_change / 1e6, marker="o", lw=2.8, color=color, label=label)
        for row in part.itertuples():
            ax.text(row.window_years, row.total_population_change / 1e6 + 4, f"{row.total_population_change/1e6:.1f}", ha="center", fontsize=8.5)
    ax.set_xticks([10, 20, 30], ["10 years", "20 years", "30 years"])
    ax.set_ylabel("Recorded population change (millions)")
    ax.legend(frameon=False)
    clean_axis(ax, "y")
    frame_title(fig, "Sensitivity · time window", "The conclusion survives ±50% window choices", "2010–2020, 2000–2020 and 1990–2020")
    footnote(fig, "Absolute magnitudes accumulate over longer windows; positive growth appears in all six pre-registered runs.")
    return save(fig, "coastal-informal-risk-06-window-sensitivity")


def figure_pop_built(panel: pd.DataFrame, diagnostics: dict) -> dict:
    plot = panel.dropna(subset=["pop_change_10m", "built_change_10m"])
    fig, ax = plt.subplots(figsize=(9.8, 6.6))
    fig.subplots_adjust(left=0.13, right=0.94, top=0.76, bottom=0.16)
    ax.scatter(plot.built_change_10m / 1e6, plot.pop_change_10m / 1e6, s=18, alpha=0.38, color=BLUE)
    focus = plot.nlargest(6, "pop_change_10m")
    for row in focus.itertuples():
        ax.annotate(row.urban_centre, (row.built_change_10m/1e6, row.pop_change_10m/1e6), xytext=(4,4), textcoords="offset points", fontsize=8)
    ax.axhline(0, color=GRID); ax.axvline(0, color=GRID)
    ax.set_xlabel("Built-up surface change below 10 m (million m²)")
    ax.set_ylabel("Population change below 10 m (millions)")
    clean_axis(ax, None)
    r = diagnostics["base_result"]["population_built_change_pearson_r"]
    frame_title(fig, "Corroboration · two quantities", "Population and built-up growth move together", f"Centre-level Pearson r = {r:.2f}, 2000–2020")
    footnote(fig, "Correlation is descriptive and size-sensitive. It does not identify causation, housing quality, or adaptation.")
    return save(fig, "coastal-informal-risk-07-population-built-corroboration")


def figure_share(panel: pd.DataFrame, diagnostics: dict) -> dict:
    plot = panel.dropna(subset=["pop_change_10m", "share_change_pp"])
    fig, ax = plt.subplots(figsize=(10.2, 6.8))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.76, bottom=0.16)
    colors = np.where((plot.pop_change_10m > 0) & (plot.share_change_pp < 0), ORANGE, BLUE)
    ax.scatter(plot.share_change_pp, plot.pop_change_10m / 1e6, s=19, alpha=0.42, c=colors)
    ax.axhline(0, color=GRID); ax.axvline(0, color=GRID)
    ax.set_xlabel("Change in below-10-metre share of centre population (percentage points)")
    ax.set_ylabel("Below-10-metre population change (millions)")
    clean_axis(ax, None)
    count = diagnostics["base_result"]["centres_more_people_but_smaller_share"]
    frame_title(fig, "Denominator · composition", f"{count} centres gained people while the low-elevation share fell", "Absolute exposure and proportional exposure can move in opposite directions")
    footnote(fig, "Orange marks more people but a smaller centre share. The population denominator also changes inside the fixed footprint.")
    return save(fig, "coastal-informal-risk-08-absolute-versus-share")


def figure_direction(diagnostics: dict) -> dict:
    base = diagnostics["base_result"]
    labels = ["Increased", "Decreased"]
    values = [base["centres_increasing"], base["centres_decreasing"]]
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.74, bottom=0.17)
    bars = ax.bar(labels, values, color=[ORANGE, BLUE], width=0.58)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x()+bar.get_width()/2, value+15, f"{value}", ha="center", fontweight="bold")
    ax.set_ylabel("Positive-endpoint urban centres")
    clean_axis(ax, "y")
    frame_title(fig, "Distribution · direction", "Growth is widespread, not universal", "775 centres increased and 149 decreased, 2000–2020")
    footnote(fig, "924 centres had positive population below 10 m in at least one endpoint. Changes may reflect redistribution within fixed footprints.")
    return save(fig, "coastal-informal-risk-09-change-direction")


def figure_concentration(panel: pd.DataFrame, diagnostics: dict) -> dict:
    change = panel.pop_change_10m.dropna()
    change = change[change > 0].sort_values(ascending=False).reset_index(drop=True)
    cumulative = 100 * change.cumsum() / change.sum()
    x = 100 * (np.arange(len(change)) + 1) / len(change)
    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    fig.subplots_adjust(left=0.12, right=0.95, top=0.76, bottom=0.16)
    ax.plot(x, cumulative, color=ORANGE, lw=3)
    ax.plot([0,100], [0,100], color=GRID, ls="--")
    ax.set_xlim(0,100); ax.set_ylim(0,102)
    ax.set_xlabel("Cumulative share of increasing centres, ranked largest first (%)")
    ax.set_ylabel("Cumulative share of positive population change (%)")
    clean_axis(ax)
    top10 = diagnostics["base_result"]["top10_centres_share_of_positive_change_pct"]
    frame_title(fig, "Concentration · positive change", f"The top ten centres contribute {top10:.1f}% of positive growth", "A small set of large centres shapes the aggregate")
    footnote(fig, "The curve excludes decreasing and zero-change centres so it describes the concentration of positive change only.")
    return save(fig, "coastal-informal-risk-10-growth-concentration")


def figure_coverage(diagnostics: dict) -> dict:
    coverage = diagnostics["coverage"]
    values = [coverage["source_urban_centres"], coverage["matched_dmc_urban_centres"], coverage["complete_2000_2020_below10_centres"], coverage["positive_below10_endpoint_centres"]]
    labels = ["All GHS-UCDB centres", "Matched coastal-DMC centres", "Reported 2000–2020 LECZ block", "Positive below 10 m at either endpoint"]
    fig, ax = plt.subplots(figsize=(10.2, 6.0))
    fig.subplots_adjust(left=0.31, right=0.95, top=0.74, bottom=0.16)
    y = np.arange(len(values))[::-1]
    ax.barh(y, values, color=[INK, BLUE, GOLD, ORANGE], height=0.62)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Urban centres")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value/1000:.0f}k" if value >= 1000 else f"{value:.0f}"))
    for yi, value in zip(y, values):
        ax.text(value + 170, yi, f"{value:,}", va="center", fontweight="bold")
    clean_axis(ax)
    frame_title(fig, "Coverage · honest denominator", "Blank LECZ blocks are not converted to zeros", "The result is a reporting-subset total, not an all-DMC estimate")
    footnote(fig, "4,013 matched centres have an undefined blank LECZ block; 410 reporting centres are zero at both endpoints.")
    return save(fig, "coastal-informal-risk-11-coverage-funnel")


def figure_claim_gate() -> dict:
    fig, ax = plt.subplots(figsize=(11.5, 6.3))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.75, bottom=0.12)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    boxes = [
        (0.03, .34, .22, .33, BLUE_LIGHT, "GHS-UCDB object", "Fixed 2025 city footprints\nPopulation + built-up surface\n5 m and 10 m LECZ fields"),
        (.39, .55, .24, .27, ORANGE_LIGHT, "Supported findings", "Change, concentration,\neconomy aggregation,\ndefinition sensitivity"),
        (.39, .15, .24, .27, "#F0F2F3", "Required safeguards", "Reported-field denominator\nNo blank-to-zero imputation\nFixed-footprint interpretation"),
        (.76, .34, .21, .33, "#F3E6E6", "Not identified", "Flood probability or loss\nInformality or deprivation\nProtection or policy quality"),
    ]
    for x,y,w,h,color,title,body in boxes:
        patch = FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.012,rounding_size=.02",facecolor=color,edgecolor="white")
        ax.add_patch(patch)
        ax.text(x+.02,y+h-.07,title,fontweight="bold",fontsize=11,color=INK)
        ax.text(x+.02,y+h-.15,body,fontsize=9.2,color=MUTED,va="top",linespacing=1.45)
    for start,end in [((.26,.50),(.38,.68)),((.26,.50),(.38,.28)),((.64,.68),(.75,.50)),((.64,.28),(.75,.50))]:
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle="-|>",mutation_scale=14,color=MUTED,lw=1.4))
    frame_title(fig, "Research architecture · claim gate", "A low-elevation settlement measure is not a risk index", "The object strengthens spatial evidence while narrowing the language")
    footnote(fig, "All empirical values trace to a committed script, cached public packages, checksums, and generated panels.")
    return save(fig, "coastal-informal-risk-12-method-and-claim-gate")


def main() -> None:
    setup_style(); CHARTS.mkdir(parents=True, exist_ok=True)
    panel = panel_with_changes(pd.read_csv(PANEL))
    diagnostics = json.loads(DIAGNOSTICS.read_text(encoding="utf-8"))
    sensitivity = json.loads(SENSITIVITY.read_text(encoding="utf-8"))["runs"]
    figures = [
        ("growth hero", figure_hero(panel, diagnostics)),
        ("centre dumbbell", figure_dumbbell(panel)),
        ("proxy falsification", figure_proxy(diagnostics)),
        ("economy aggregation", figure_economies(diagnostics)),
        ("elevation sensitivity", figure_threshold(sensitivity)),
        ("window sensitivity", figure_windows(sensitivity)),
        ("population-built corroboration", figure_pop_built(panel, diagnostics)),
        ("absolute versus share", figure_share(panel, diagnostics)),
        ("change direction", figure_direction(diagnostics)),
        ("growth concentration", figure_concentration(panel, diagnostics)),
        ("coverage funnel", figure_coverage(diagnostics)),
        ("method and claim gate", figure_claim_gate()),
    ]
    payload = {"program":"coastal-informal-risk","analysis":"evidence-bearing figure dossier","attestation_chain":"ai-first","figure_count":len(figures),"figures":[{"order":i,"name":name,"paths":paths} for i,(name,paths) in enumerate(figures,1)]}
    (OUT / "coastal-informal-risk-figure-dossier.json").write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(f"Built {len(figures)} evidence-bearing figures")


if __name__ == "__main__":
    main()
