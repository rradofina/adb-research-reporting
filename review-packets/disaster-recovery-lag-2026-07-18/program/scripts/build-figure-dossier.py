"""Build the disaster-recovery construct-validation figure dossier.

Every figure reads generated evidence. The visuals communicate two distinct
failures: the original country-burden ranking fails its own metric kill rule,
and the event-level GDIS x VIIRS pilot does not identify a stable recovery
month. No figure treats nighttime radiance as welfare or reconstruction.

attestation_chain: ai-first
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"
METRICS = GEN / "disaster-recovery-lag-metric-falsification.json"
READINESS = GEN / "disaster-recovery-lag-recovery-source-readiness.json"
VALIDATION = GEN / "disaster-recovery-haiyan-construct-validation.json"
MONTHLY = GEN / "disaster-recovery-haiyan-monthly-pilot.csv"
GEOMETRY = GEN / "disaster-recovery-gdis-geometry-audit.json"
SUMMARY = GEN / "disaster-recovery-figure-dossier-summary.json"

ADB_BLUE = "#007DB8"
ADB_NAVY = "#002569"
ADB_GOLD = "#B07D12"
ADB_RED = "#A63D40"
ADB_GREEN = "#2C7A64"
PURPLE = "#6F5A9A"
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
    svg = CHARTS / f"{stem}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def clean_axes(ax: plt.Axes, axis: str = "x") -> None:
    ax.grid(axis=axis, color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)


def add_source(fig: plt.Figure, text: str) -> None:
    fig.text(0.055, 0.025, text, ha="left", va="bottom", fontsize=7.0, color=INK_SOFT, wrap=True)


def metric_labels(metrics: dict) -> tuple[list[str], list[list[str]]]:
    labels = []
    values = []
    for key, top5 in metrics["metrics_top5"].items():
        label = key.split(" (")[0]
        labels.append(label.replace("_", " "))
        values.append(top5)
    return labels, values


def render_two_stage_gate(metrics: dict, validation: dict) -> None:
    killed = sum(1 for row in metrics["kill_condition_by_metric"].values() if row["kill_condition_fires"])
    total_metrics = len(metrics["kill_condition_by_metric"])
    main = validation["validation"]["main_specification"]
    adequate_baseline = sum(row["valid_baseline_months"] >= 4 for row in main)
    stable = len(validation["validation"]["stable_locations_all_variants"])

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.3))
    fig.subplots_adjust(left=0.06, right=0.94, top=0.73, bottom=0.18, wspace=0.18)
    cards = [
        (axes[0], "1", "Burden ranking", f"{killed} of {total_metrics}", "metrics replace the claimed CHN–IND top two", ADB_RED),
        (axes[1], "2", "Recovery construct", f"{stable} of 7", "centroids return one recovery month across all variants", ADB_NAVY),
    ]
    for ax, number, title, value, detail, color in cards:
        ax.set_facecolor(PALE)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.text(0.07, 0.86, f"GATE {number}", transform=ax.transAxes, color=color, fontsize=9, weight="bold")
        ax.text(0.07, 0.70, title, transform=ax.transAxes, color=INK, fontsize=14, weight="semibold")
        ax.text(0.07, 0.39, value, transform=ax.transAxes, color=color, fontsize=35, weight="bold")
        ax.text(0.07, 0.22, detail, transform=ax.transAxes, color=INK_SOFT, fontsize=10, wrap=True)
    axes[1].text(0.07, 0.08, f"Only {adequate_baseline} of 7 has ≥4 valid pre-event months.", transform=axes[1].transAxes, color=INK_SOFT, fontsize=9)
    fig.suptitle("The recovery ranking fails before any country can be ranked", x=0.055, y=0.96, ha="left", fontsize=19, color=INK, weight="semibold")
    fig.text(0.055, 0.84, "The original metric is not recovery, and the direct public-data pilot does not produce a stable recovery month.", ha="left", fontsize=10.5, color=INK_SOFT)
    add_source(fig, "Sources: disaster-recovery-lag-metric-falsification.json and disaster-recovery-haiyan-construct-validation.json. Nighttime radiance is a proxy, not welfare. attestation_chain: ai-first.")
    save_figure(fig, "disaster-two-stage-validity-gate")


def render_metric_disagreement(metrics: dict) -> None:
    labels, top5s = metric_labels(metrics)
    economies = sorted({iso for top5 in top5s for iso in top5})
    matrix = np.full((len(economies), len(labels)), np.nan)
    for col, top5 in enumerate(top5s):
        for rank, iso in enumerate(top5, start=1):
            matrix[economies.index(iso), col] = rank
    order = np.argsort(np.nanmean(matrix, axis=1))
    matrix = matrix[order]
    economies = [economies[i] for i in order]

    fig, ax = plt.subplots(figsize=(11.8, 7.2))
    fig.subplots_adjust(left=0.12, right=0.95, top=0.76, bottom=0.22)
    cmap = plt.matplotlib.colors.ListedColormap([ADB_NAVY, ADB_BLUE, ADB_GREEN, ADB_GOLD, ADB_RED])
    masked = np.ma.masked_invalid(matrix)
    ax.imshow(masked, cmap=cmap, vmin=1, vmax=5, aspect="auto")
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            value = matrix[row, col]
            ax.text(col, row, "—" if np.isnan(value) else f"#{int(value)}", ha="center", va="center", color=INK_SOFT if np.isnan(value) else WHITE, fontsize=9, weight="semibold")
    ax.set_xticks(range(len(labels)), labels, rotation=18, ha="right")
    ax.set_yticks(range(len(economies)), economies)
    ax.tick_params(length=0, labelsize=9)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.suptitle("Five defensible burden metrics produce five different orderings", x=0.055, y=0.96, ha="left", fontsize=18, color=INK, weight="semibold")
    fig.text(0.055, 0.855, "The pre-registered CHN–IND top-two claim survives affected population and damage, but not event frequency, deaths, or events per million.", ha="left", fontsize=10.2, color=INK_SOFT)
    add_source(fig, "Source: disaster-recovery-lag-metric-falsification.json; EM-DAT country profiles and World Bank WDI population. Cells show top-five rank only. attestation_chain: ai-first.")
    save_figure(fig, "disaster-metric-rank-disagreement")


def render_per_capita_inversion(metrics: dict) -> None:
    absolute = metrics["metrics_top5"]["events_per_year (committed)"]
    per_capita = metrics["metrics_top5"]["events_per_million_pop (DEEPENING, cross-program WDI join)"]
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.9))
    fig.subplots_adjust(left=0.07, right=0.94, top=0.72, bottom=0.18, wspace=0.24)
    for ax, title, values, color in [
        (axes[0], "Absolute event frequency", absolute, ADB_NAVY),
        (axes[1], "Events per million people", per_capita, ADB_GOLD),
    ]:
        ax.set_xlim(0, 1); ax.set_ylim(5.6, 0.4); ax.axis("off")
        ax.text(0, 0.55, title, fontsize=12, weight="semibold", color=INK)
        for rank, iso in enumerate(values, start=1):
            ax.add_patch(plt.Rectangle((0, rank + 0.05), 0.86, 0.72, color=PALE, transform=ax.transData))
            ax.text(0.04, rank + 0.42, f"{rank}", va="center", fontsize=10, color=color, weight="bold")
            ax.text(0.16, rank + 0.42, iso, va="center", fontsize=13, color=INK, weight="semibold")
    fig.suptitle("Population normalisation turns the country list upside down", x=0.055, y=0.96, ha="left", fontsize=18, color=INK, weight="semibold")
    fig.text(0.055, 0.84, "Large-country burden and small-state exposure are different questions; neither is recovery duration.", ha="left", fontsize=10.2, color=INK_SOFT)
    add_source(fig, "Source: disaster-recovery-lag-metric-falsification.json. The per-million screen uses 2024 WDI population against 2000–2025 EM-DAT event counts and is indicative, not a calibrated rate. attestation_chain: ai-first.")
    save_figure(fig, "disaster-per-capita-inversion")


def render_source_ladder(readiness: dict, validation: dict) -> None:
    summary = readiness["summary"]
    gates = [
        ("EM-DAT country profiles", "1,767 aggregate rows", "No event ID,\nday/month, or geometry", ADB_RED),
        ("GDIS event geography", f"{summary['adb_unique_ids_black_marble_window_2012_2018']:,} event IDs", f"{summary['countries_with_gdis_viirs_overlap']} economies overlap VIIRS\nin 2012–2018", ADB_GOLD),
        ("Light Every Night pilot", f"{validation['design']['scheduled_orbits']} scheduled orbits", "Public COG windows + flags\nwithout credentials", ADB_BLUE),
        ("Recovery construct", "Not validated", "0 of 7 centroids stable\nacross all variants", ADB_NAVY),
    ]
    fig, ax = plt.subplots(figsize=(11.8, 6.4))
    fig.subplots_adjust(left=0.06, right=0.95, top=0.76, bottom=0.16)
    ax.axis("off")
    for i, (title, value, detail, color) in enumerate(gates):
        x = 0.02 + i * 0.245
        ax.add_patch(plt.Rectangle((x, 0.18), 0.215, 0.60, color=PALE, transform=ax.transAxes))
        ax.add_patch(plt.Rectangle((x, 0.72), 0.215, 0.06, color=color, transform=ax.transAxes))
        ax.text(x + 0.018, 0.63, f"STEP {i + 1}", transform=ax.transAxes, fontsize=8.5, color=color, weight="bold")
        ax.text(x + 0.018, 0.53, title, transform=ax.transAxes, fontsize=11, color=INK, weight="semibold", wrap=True)
        ax.text(x + 0.018, 0.38, value, transform=ax.transAxes, fontsize=14, color=color, weight="bold", wrap=True)
        ax.text(x + 0.018, 0.22, detail, transform=ax.transAxes, fontsize=8.2, color=INK_SOFT, linespacing=1.35)
        if i < 3: ax.annotate("", xy=(x + 0.238, 0.48), xytext=(x + 0.216, 0.48), xycoords=ax.transAxes, arrowprops={"arrowstyle": "->", "color": RULE, "lw": 2})
    fig.suptitle("The data bridge is open; the measurement bridge is not", x=0.055, y=0.96, ha="left", fontsize=18, color=INK, weight="semibold")
    fig.text(0.055, 0.855, "Access was solved without credentials. Event timing, footprint meaning, clear-sky coverage, and result stability remain the binding constraints.", ha="left", fontsize=10.2, color=INK_SOFT)
    add_source(fig, "Sources: disaster-recovery-lag-recovery-source-readiness.json and disaster-recovery-haiyan-construct-validation.json; GDIS and World Bank Light Every Night. attestation_chain: ai-first.")
    save_figure(fig, "disaster-source-ladder")


def render_observation_coverage(monthly: pd.DataFrame) -> None:
    rows = monthly[(monthly["radius_km"] == 50) & (monthly["reducer"] == "mean")].copy()
    months = sorted(rows["month"].unique())
    locations = sorted(rows["location"].unique())
    matrix = np.array([[int(rows[(rows["location"] == loc) & (rows["month"] == month)]["paired_valid_nights"].iloc[0]) for month in months] for loc in locations])
    fig, ax = plt.subplots(figsize=(11.8, 6.3))
    fig.subplots_adjust(left=0.12, right=0.95, top=0.74, bottom=0.24)
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("coverage", [ADB_RED, PALE, ADB_BLUE])
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=6, aspect="auto")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            ax.text(j, i, str(value), ha="center", va="center", fontsize=7.7, color=WHITE if value in {0, 5, 6} else INK)
    ax.axvline(months.index("2013-11") - 0.5, color=ADB_RED, linewidth=2)
    ax.set_xticks(range(len(months)), [m.replace("2013-", "'13 ").replace("2014-", "'14 ") for m in months], rotation=45, ha="right")
    ax.set_yticks(range(len(locations)), locations)
    ax.tick_params(length=0, labelsize=8.5)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.suptitle("Cloud and swath gaps leave most baseline months underpowered", x=0.055, y=0.96, ha="left", fontsize=18, color=INK, weight="semibold")
    fig.text(0.055, 0.84, "Cells are paired, quality-screened nights out of six scheduled. A month needs at least two; a baseline needs four valid months.", ha="left", fontsize=10.2, color=INK_SOFT)
    add_source(fig, "Source: disaster-recovery-haiyan-monthly-pilot.csv. Main specification: 50 km square half-width, mean radiance, same-orbit Manila reference. Red line marks the November 2013 event month. attestation_chain: ai-first.")
    save_figure(fig, "disaster-haiyan-observation-coverage")


def render_main_series(monthly: pd.DataFrame, validation: dict) -> None:
    rows = monthly[(monthly["radius_km"] == 50) & (monthly["reducer"] == "mean") & monthly["month_valid"]].copy()
    baseline = {row["location"]: row["baseline_ratio"] for row in validation["validation"]["main_specification"]}
    rows["baseline_index"] = rows.apply(lambda row: 100 * row["monthly_ratio_median"] / baseline[row["location"]] if baseline[row["location"]] else np.nan, axis=1)
    locations = sorted(rows["location"].unique())
    months = sorted(monthly["month"].unique())
    colors = [ADB_BLUE, ADB_GOLD, ADB_GREEN, PURPLE, ADB_RED, ADB_NAVY, "#8B6F47"]
    fig, ax = plt.subplots(figsize=(11.8, 7.0))
    fig.subplots_adjust(left=0.09, right=0.82, top=0.76, bottom=0.20)
    for loc, color in zip(locations, colors, strict=True):
        part = rows[rows["location"] == loc]
        x = [months.index(month) for month in part["month"]]
        y = part["baseline_index"].clip(-100, 500)
        ax.plot(x, y, color=color, linewidth=1.7, marker="o", markersize=4, label=loc)
    ax.axhline(90, color=INK_SOFT, linestyle="--", linewidth=1, label="90% threshold")
    ax.axvline(months.index("2013-11"), color=ADB_RED, linewidth=1.5)
    ax.set_xticks(range(len(months)), [m.replace("2013-", "'13 ").replace("2014-", "'14 ") for m in months], rotation=45, ha="right")
    ax.set_ylim(-110, 510)
    ax.set_ylabel("Monthly radiance ratio, pre-event baseline = 100")
    clean_axes(ax, "y")
    ax.legend(frameon=False, bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8.5)
    fig.suptitle("The apparent recovery path changes by centroid and missing month", x=0.055, y=0.96, ha="left", fontsize=18, color=INK, weight="semibold")
    fig.text(0.055, 0.855, "Lines connect available months only. They are not continuous recovery curves; clipped values expose the instability of dark administrative centroids.", ha="left", fontsize=10.2, color=INK_SOFT)
    add_source(fig, "Source: disaster-recovery-haiyan-monthly-pilot.csv and construct-validation JSON. Negative raw-radiance ratios can occur after background subtraction; values are clipped to −100–500 for display only. attestation_chain: ai-first.")
    save_figure(fig, "disaster-haiyan-main-series")


def render_sensitivity(validation: dict) -> None:
    specs = validation["validation"]["specifications"]
    locations = sorted({row["location"] for row in specs})
    none_share = []
    distinct = []
    top_label = []
    for loc in locations:
        outcomes = Counter(row["recovery_month"] for row in specs if row["location"] == loc)
        none_share.append(100 * outcomes[None] / sum(outcomes.values()))
        distinct.append(len([key for key in outcomes if key is not None]))
        non_none = [(key, count) for key, count in outcomes.items() if key is not None]
        top_label.append(max(non_none, key=lambda pair: pair[1])[0] if non_none else "none")
    y = np.arange(len(locations))
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.7), gridspec_kw={"width_ratios": [1.35, 1]})
    fig.subplots_adjust(left=0.12, right=0.95, top=0.73, bottom=0.17, wspace=0.30)
    bars = axes[0].barh(y, none_share, color=ADB_RED, height=0.58)
    axes[0].set_yticks(y, locations); axes[0].invert_yaxis(); axes[0].set_xlim(0, 100)
    axes[0].set_xlabel("Specifications with no recovery month (%)")
    for bar, value in zip(bars, none_share, strict=True): axes[0].text(value + 1.5, bar.get_y() + bar.get_height()/2, f"{value:.0f}%", va="center", fontsize=9)
    clean_axes(axes[0], "x")
    bars2 = axes[1].barh(y, distinct, color=ADB_NAVY, height=0.58)
    axes[1].set_yticks(y, ["" for _ in locations]); axes[1].invert_yaxis(); axes[1].set_xlim(0, 8)
    axes[1].set_xlabel("Distinct non-missing recovery months")
    for bar, value, label in zip(bars2, distinct, top_label, strict=True): axes[1].text(value + 0.15, bar.get_y()+bar.get_height()/2, f"{value} · most often {label}", va="center", fontsize=8.3)
    clean_axes(axes[1], "x")
    fig.suptitle("No centroid returns one recovery month across the sensitivity matrix", x=0.055, y=0.96, ha="left", fontsize=18, color=INK, weight="semibold")
    fig.text(0.055, 0.84, "Each location has 54 variants: 25/50/75 km, mean/p75, 80/90/100% threshold, and one/two/three-month persistence.", ha="left", fontsize=10.2, color=INK_SOFT)
    add_source(fig, "Source: disaster-recovery-haiyan-construct-validation.json. The 25/50/75 km and one/two/three-month ranges implement the required ±50% tests. attestation_chain: ai-first.")
    save_figure(fig, "disaster-haiyan-sensitivity")


def render_geometry_audit(geometry: dict) -> None:
    mismatches = geometry["mismatches"]
    fig, ax = plt.subplots(figsize=(11.8, 5.8))
    fig.subplots_adjust(left=0.07, right=0.95, top=0.72, bottom=0.18)
    ax.axis("off")
    ax.text(0.02, 0.67, f"{geometry['rows_audited']:,}", transform=ax.transAxes, fontsize=37, color=ADB_NAVY, weight="bold")
    ax.text(0.02, 0.52, "GDIS centroids audited", transform=ax.transAxes, fontsize=11, color=INK_SOFT)
    ax.text(0.34, 0.67, f"{geometry['gross_mismatch_rows']}", transform=ax.transAxes, fontsize=37, color=ADB_RED, weight="bold")
    ax.text(0.34, 0.52, ">1,000 km from coded country", transform=ax.transAxes, fontsize=11, color=INK_SOFT)
    ax.plot([0.02, 0.95], [0.43, 0.43], transform=ax.transAxes, color=RULE, lw=1)
    for i, row in enumerate(mismatches):
        x = 0.02 + i * 0.31
        ax.text(x, 0.32, f"{row['iso3']} · {row['adm1']}", transform=ax.transAxes, fontsize=10.5, color=INK, weight="semibold")
        ax.text(x, 0.23, f"{row['distance_to_country_polygon_km']:,.0f} km", transform=ax.transAxes, fontsize=13, color=ADB_RED, weight="bold")
        ax.text(x, 0.15, f"{row['latitude']:.2f}, {row['longitude']:.2f}", transform=ax.transAxes, fontsize=8.8, color=INK_SOFT)
    fig.suptitle("Public event geography is usable—but not self-validating", x=0.055, y=0.96, ha="left", fontsize=18, color=INK, weight="semibold")
    fig.text(0.055, 0.835, "Three gross coordinate-country mismatches survive a deliberately conservative screen; every event footprint still needs a plausibility gate.", ha="left", fontsize=10.2, color=INK_SOFT)
    add_source(fig, "Source: disaster-recovery-gdis-geometry-audit.json; GDIS centroids tested against Natural Earth 1:50m polygons in EPSG:6933. The 1,000 km threshold is a gross-error screen, not full geocoding validation. attestation_chain: ai-first.")
    save_figure(fig, "disaster-gdis-geometry-audit")


def main() -> None:
    metrics = load_json(METRICS)
    readiness = load_json(READINESS)
    validation = load_json(VALIDATION)
    geometry = load_json(GEOMETRY)
    monthly = pd.read_csv(MONTHLY)
    if monthly["month_valid"].dtype != bool:
        monthly["month_valid"] = monthly["month_valid"].map(lambda value: str(value).lower() == "true")

    render_two_stage_gate(metrics, validation)
    render_metric_disagreement(metrics)
    render_per_capita_inversion(metrics)
    render_source_ladder(readiness, validation)
    render_observation_coverage(monthly)
    render_main_series(monthly, validation)
    render_sensitivity(validation)
    render_geometry_audit(geometry)

    main = validation["validation"]["main_specification"]
    payload = {
        "program": "disaster-recovery-lag",
        "logical_figures": 8,
        "finding": (
            "The original burden ranking fails its metric kill rule, while the GDIS x Light Every Night "
            "Haiyan pilot yields no centroid with one recovery month across 54 variants."
        ),
        "key_counts": {
            "burden_metrics_firing_kill_rule": sum(1 for row in metrics["kill_condition_by_metric"].values() if row["kill_condition_fires"]),
            "burden_metrics_tested": len(metrics["kill_condition_by_metric"]),
            "scheduled_orbits": validation["design"]["scheduled_orbits"],
            "affected_centroids": len(main),
            "centroids_with_four_valid_baseline_months": sum(row["valid_baseline_months"] >= 4 for row in main),
            "centroids_stable_all_variants": len(validation["validation"]["stable_locations_all_variants"]),
            "gdis_viirs_rows_audited": geometry["rows_audited"],
            "gdis_gross_geometry_mismatches": geometry["gross_mismatch_rows"],
        },
        "figures": [
            "disaster-two-stage-validity-gate", "disaster-metric-rank-disagreement",
            "disaster-per-capita-inversion", "disaster-source-ladder",
            "disaster-haiyan-observation-coverage", "disaster-haiyan-main-series",
            "disaster-haiyan-sensitivity", "disaster-gdis-geometry-audit",
        ],
        "attestation_chain": "ai-first",
    }
    SUMMARY.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built {payload['logical_figures']} disaster-recovery evidence figures")


if __name__ == "__main__":
    main()
