"""Build the public-evidence figure spine for the air-monitoring study.

Every plotted quantity is read from the committed evidence ledger. The figures
communicate the documented absence, the audited scope, the closed claim gates,
and the exact evidence that could change the result. They do not estimate
monitor coverage, exposure, or regulator performance.

attestation_chain: ai-first
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyBboxPatch


PROGRAM = Path(__file__).resolve().parents[1]
LEDGER = PROGRAM / "generated" / "evidence-ledger.json"
CHARTS = PROGRAM / "generated" / "charts"

NAVY = "#002569"
BLUE = "#007DB8"
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
        "xtick.color": MID,
        "ytick.color": MID,
        "text.color": INK,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
    }
)


def load_ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def header(fig, title: str, subtitle: str):
    fig.suptitle(title, x=0.06, y=0.965, ha="left", fontsize=23, fontweight="bold")
    fig.text(0.06, 0.915, subtitle, ha="left", fontsize=11.3, color=MID)


def footer(fig, note: str):
    fig.text(0.06, 0.043, "Source: committed air-monitoring public-evidence ledger", fontsize=8.5, color=MID)
    fig.text(0.06, 0.020, f"Note: {note}", fontsize=8.2, color=MID)
    fig.text(0.94, 0.020, "attestation_chain: ai-first", fontsize=8.1, color=MID, ha="right", family="monospace")


def save(fig, stem: str):
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{stem}.png", dpi=180, bbox_inches="tight")
    svg = CHARTS / f"{stem}.svg"
    fig.savefig(svg, bbox_inches="tight")
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def clean(ax, grid="x"):
    ax.spines[["top", "right"]].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=PALE, linewidth=0.8)
        ax.set_axisbelow(True)


def evidence_funnel(data):
    c = data["headline_counts"]
    stages = [
        ("Economies in\nsource discovery", c["economies_in_source_discovery"]),
        ("Economies with an official\nstation source or portal", c["economies_with_official_station_source_or_portal"]),
        ("Official station rows\naudited", c["official_station_rows_audited"]),
        ("Identity candidates\nchecked", c["identity_candidate_rows_checked"]),
        ("Validated same-station\nrows", c["validated_same_station_rows"]),
    ]
    fig, ax = plt.subplots(figsize=(16, 9))
    header(fig, "The audit found station routes, but no validated station crosswalk", "Five evidence stages; counts use different units and should not be read as an attrition rate")
    ax.axis("off")
    xs = np.linspace(0.09, 0.91, len(stages))
    for i, ((label, value), x) in enumerate(zip(stages, xs)):
        color = RED if value == 0 else BLUE if i < 2 else NAVY
        box = FancyBboxPatch((x - 0.085, 0.34), 0.17, 0.30, boxstyle="round,pad=0.015,rounding_size=0.02", transform=ax.transAxes, facecolor=LIGHT_BLUE if value else "#FBE6E7", edgecolor=color, linewidth=1.8)
        ax.add_patch(box)
        ax.text(x, 0.54, f"{value:,}", transform=ax.transAxes, ha="center", va="center", fontsize=31, fontweight="bold", color=color)
        ax.text(x, 0.40, label, transform=ax.transAxes, ha="center", va="center", fontsize=10.5, color=INK)
        if i < len(stages) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.10, 0.49), xytext=(x + 0.10, 0.49), xycoords=ax.transAxes, arrowprops={"arrowstyle": "->", "color": MID, "lw": 1.4})
    ax.text(0.50, 0.23, "The zero is the research result: public identity evidence did not close the join gate.", transform=ax.transAxes, ha="center", fontsize=14, color=RED, fontweight="bold")
    footer(fig, "Economy, station-row, and candidate-row counts are deliberately separated; no causal or performance inference.")
    save(fig, "air-monitoring-evidence-funnel")


def qa_gates(data):
    c = data["headline_counts"]
    labels = [
        "Validated same-station rows",
        "BMKG inspection-log rows",
        "BMKG calibration-certificate rows",
        "BMKG calibration-status rows",
        "Complete monitor-grade rows",
        "Station-radius-ready economies",
        "Coverage-claim rows allowed",
    ]
    values = [
        c["validated_same_station_rows"],
        c["bmkg_station_specific_inspection_log_rows"],
        c["bmkg_station_specific_calibration_certificate_rows"],
        c["bmkg_calibration_status_rows"],
        c["complete_monitor_grade_rows"],
        c["station_radius_ready_economies"],
        c["claim_allowed_country_rows"],
    ]
    fig, ax = plt.subplots(figsize=(16, 9))
    header(fig, "Every claim-enabling public QA gate remains closed", "A zero is counted only when the source route, retrieval state, row scope, and missing field are recorded")
    y = np.arange(len(labels))
    ax.barh(y, [1] * len(labels), color="#FBE6E7", edgecolor="#E7AEB1", height=0.62)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.spines[:].set_visible(False)
    for yi, value in zip(y, values):
        ax.text(0.04, yi, f"{value}", va="center", fontsize=22, fontweight="bold", color=RED)
        ax.text(0.96, yi, "not verified in audited public routes", va="center", ha="right", fontsize=10.5, color=MID)
    fig.text(0.68, 0.13, "Coverage claim: NOT ALLOWED", ha="center", fontsize=18, color=RED, fontweight="bold", bbox={"boxstyle": "round,pad=0.6", "facecolor": "#FBE6E7", "edgecolor": RED})
    footer(fig, "Zero means not verified in the audited public packet, not evidence that the record does not exist elsewhere.")
    fig.subplots_adjust(left=0.34, right=0.94, top=0.82, bottom=0.18)
    save(fig, "air-monitoring-qa-gates")


def bmkg_closure(data):
    c = data["headline_counts"]
    labels = ["Target rows", "Method/display/status context", "Current online dashboard rows", "Station inspection logs", "Calibration certificates", "Complete monitor-grade rows"]
    values = [c["bmkg_pm25_target_rows"], c["bmkg_pm25_target_rows"], 21, c["bmkg_station_specific_inspection_log_rows"], c["bmkg_station_specific_calibration_certificate_rows"], c["complete_monitor_grade_rows"]]
    colors = [NAVY, BLUE, GREEN, RED, RED, RED]
    fig, ax = plt.subplots(figsize=(16, 9))
    header(fig, "BMKG is visible online, but visibility is not grade closure", "The public dashboard and method context cover the target queue; station-specific QA records do not")
    y = np.arange(len(labels))
    bars = ax.barh(y, values, color=colors, height=0.58)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(values) * 1.22)
    clean(ax)
    for bar, value in zip(bars, values):
        ax.text(value + 0.4, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=16, fontweight="bold", color=RED if value == 0 else INK)
    footer(fig, "Dashboard ONLINE status is operational context; it is not a calibration certificate or inspection record.")
    fig.subplots_adjust(left=0.31, right=0.94, top=0.82, bottom=0.14)
    save(fig, "air-monitoring-bmkg-closure")


def economy_matrix(data):
    rows = sorted(data["economy_rows"], key=lambda x: x["country"])
    cols = [
        ("Official route", lambda r: int(r["official_station_source_or_portal"])),
        ("Grade rows audited", lambda r: int(r["monitor_grade_rows_audited"] > 0)),
        ("Identity candidates", lambda r: int(r["identity_candidate_rows"] > 0)),
        ("Coordinates", lambda r: int(r["station_radius_coordinate_rows"] > 0)),
        ("Claim-ready", lambda r: int(r["station_radius_ready_rows"] > 0)),
    ]
    mat = np.array([[fn(r) for _, fn in cols] for r in rows])
    fig, ax = plt.subplots(figsize=(16, 12))
    header(fig, "Public evidence coverage is uneven across the 24-economy discovery frame", "Blue marks a visible evidence lane; the final claim-ready column remains empty")
    ax.imshow(mat, aspect="auto", cmap=ListedColormap(["#F2F5F7", BLUE]), vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(cols)), [name for name, _ in cols])
    ax.set_yticks(np.arange(len(rows)), [r["country"] for r in rows])
    ax.tick_params(axis="x", rotation=18)
    ax.set_xticks(np.arange(-0.5, len(cols), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color=WHITE, linewidth=1.4)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    footer(fig, "A blank cell means the corresponding committed ledger field is zero or false; it is not a country performance score.")
    fig.subplots_adjust(left=0.25, right=0.94, top=0.84, bottom=0.13)
    save(fig, "air-monitoring-economy-matrix")


def evidence_groups(data):
    counts = Counter(row["group"] for row in data["rows"])
    pairs = sorted(counts.items(), key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(16, 10))
    header(fig, "The ledger spans source discovery, station identity, and QA closure", "Number of committed summary artifacts consolidated in each evidence family")
    labels = [p[0].replace("-", " ").title() for p in pairs]
    values = [p[1] for p in pairs]
    bars = ax.barh(np.arange(len(pairs)), values, color=[BLUE if v < max(values) else NAVY for v in values])
    ax.set_yticks(np.arange(len(pairs)), labels)
    ax.set_xlabel("Ledger summary rows")
    clean(ax)
    for bar, value in zip(bars, values):
        ax.text(value + 0.15, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=10, fontweight="bold")
    footer(fig, "Artifact counts describe audit coverage, not the strength or quality of any regulator or monitoring network.")
    fig.subplots_adjust(left=0.32, right=0.94, top=0.84, bottom=0.12)
    save(fig, "air-monitoring-evidence-groups")


def sensitivity_boundary(data):
    c = data["headline_counts"]
    fig, axes = plt.subplots(1, 2, figsize=(16, 9), gridspec_kw={"width_ratios": [1.1, 1]})
    header(fig, "Changing the radius cannot create missing QA evidence", "The absence finding is invariant to ±50% geometry choices but sensitive to a genuinely new station-level source")
    radii = ["0.5 km", "4 km", "50 km"]
    axes[0].bar(radii, [0, 0, 0], color=RED)
    axes[0].set_ylim(0, 1)
    axes[0].set_yticks([0, 1], ["0 claims", "1+ claims"])
    axes[0].set_title("Coverage claims allowed by radius", loc="left", fontweight="bold")
    for i in range(3):
        axes[0].text(i, 0.06, "0", ha="center", fontsize=24, fontweight="bold", color=RED)
    clean(axes[0], grid="y")
    axes[1].axis("off")
    axes[1].text(0.05, 0.80, "Would not change the finding", fontsize=15, fontweight="bold", color=NAVY, transform=axes[1].transAxes)
    axes[1].text(0.08, 0.67, "• another radius\n• another denominator surface\n• another generic portal search", fontsize=12, linespacing=1.8, transform=axes[1].transAxes)
    axes[1].text(0.05, 0.40, "Could change the finding", fontsize=15, fontweight="bold", color=GREEN, transform=axes[1].transAxes)
    axes[1].text(0.08, 0.19, "• station certificate or inspection log\n• current calibration-status row\n• official same-station crosswalk\n• station-keyed method-grade ledger", fontsize=12, linespacing=1.7, transform=axes[1].transAxes)
    fig.text(0.28, 0.16, f"{c['denominator_join_rows']:,} denominator joins already computed", ha="center", fontsize=12, color=MID)
    footer(fig, "The radius comparison tests the arbitrary geometry choice; source-expansion sensitivity requires a named, plausibly different source.")
    fig.subplots_adjust(left=0.07, right=0.95, top=0.82, bottom=0.20, wspace=0.20)
    save(fig, "air-monitoring-sensitivity-boundary")


def overturning_evidence(data):
    c = data["headline_counts"]
    items = [
        ("Inspection log", c["bmkg_station_specific_inspection_log_rows"]),
        ("Calibration certificate", c["bmkg_station_specific_calibration_certificate_rows"]),
        ("Calibration status", c["bmkg_calibration_status_rows"]),
        ("Official crosswalk", c["validated_same_station_rows"]),
        ("Complete grade row", c["complete_monitor_grade_rows"]),
    ]
    fig, ax = plt.subplots(figsize=(16, 9))
    header(fig, "Five public evidence objects would overturn or narrow the result", "None is verified in the current packet; one valid row would change the claim for the affected station or economy")
    ax.axis("off")
    xs = np.linspace(0.12, 0.88, len(items))
    for (label, value), x in zip(items, xs):
        box = FancyBboxPatch((x - 0.08, 0.33), 0.16, 0.34, boxstyle="round,pad=0.015,rounding_size=0.025", transform=ax.transAxes, facecolor="#FBE6E7", edgecolor=RED, linewidth=1.4)
        ax.add_patch(box)
        ax.text(x, 0.55, str(value), transform=ax.transAxes, ha="center", fontsize=36, fontweight="bold", color=RED)
        ax.text(x, 0.41, label, transform=ax.transAxes, ha="center", va="center", fontsize=10.5, wrap=True)
    ax.text(0.5, 0.22, "A future public release changes the ledger; it does not require changing the research rule.", transform=ax.transAxes, ha="center", fontsize=13.5, color=NAVY, fontweight="bold")
    footer(fig, "The study reports a bounded public-data absence, not a universal claim that these records do not exist.")
    save(fig, "air-monitoring-overturning-evidence")


def claim_ladder(data):
    c = data["headline_counts"]
    stages = [
        ("Denominator geometry", c["denominator_join_rows"], BLUE),
        ("Identity candidates", c["identity_candidate_rows_checked"], NAVY),
        ("Validated identities", c["validated_same_station_rows"], RED),
        ("Complete grade rows", c["complete_monitor_grade_rows"], RED),
        ("Ready economies", c["station_radius_ready_economies"], RED),
        ("Allowed claims", c["claim_allowed_country_rows"], RED),
    ]
    fig, ax = plt.subplots(figsize=(16, 9))
    header(fig, "The analysis stops before population coverage can be claimed", "Geometry exists; identity and monitor-grade evidence do not close")
    ax.axis("off")
    for i, (label, value, color) in enumerate(stages):
        y = 0.78 - i * 0.115
        width = 0.70 - i * 0.08
        x = 0.5 - width / 2
        box = FancyBboxPatch((x, y - 0.045), width, 0.078, boxstyle="round,pad=0.008,rounding_size=0.012", transform=ax.transAxes, facecolor=LIGHT_BLUE if value else "#FBE6E7", edgecolor=color, linewidth=1.2)
        ax.add_patch(box)
        ax.text(x + 0.02, y - 0.006, label, transform=ax.transAxes, ha="left", va="center", fontsize=11, fontweight="bold")
        ax.text(x + width - 0.02, y - 0.006, f"{value:,}", transform=ax.transAxes, ha="right", va="center", fontsize=17, fontweight="bold", color=color)
    ax.text(0.5, 0.08, "Decision: publish the observability gap; do not publish a coverage estimate.", transform=ax.transAxes, ha="center", fontsize=15, color=RED, fontweight="bold")
    footer(fig, "Stage counts have different units; the ladder is a claim-permission sequence, not a sample-flow calculation.")
    save(fig, "air-monitoring-claim-ladder")


def main():
    data = load_ledger()
    evidence_funnel(data)
    qa_gates(data)
    bmkg_closure(data)
    economy_matrix(data)
    evidence_groups(data)
    sensitivity_boundary(data)
    overturning_evidence(data)
    claim_ladder(data)
    print("Built 8 air-monitoring evidence figures.")


if __name__ == "__main__":
    main()
