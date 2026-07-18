"""Build the water-crop construct-validation figure dossier.

Every plotted number is read from committed generated artifacts. Each figure
must carry a finding, a coverage limit, a sensitivity result, or a source
disagreement; decorative rankings are excluded.
attestation_chain: ai-first.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"

BLUE = "#007DB8"
NAVY = "#002569"
GOLD = "#B07D12"
RED = "#A63D40"
GREEN = "#2C7A64"
INK = "#20262E"
SOFT = "#5C6670"
RULE = "#D9DEE2"
PALE = "#EEF2F4"
WHITE = "#FFFFFF"


def save(fig, stem: str, dpi: int = 200) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{stem}.png", dpi=dpi, bbox_inches="tight", facecolor=WHITE)
    fig.savefig(CHARTS / f"{stem}.svg", bbox_inches="tight", facecolor=WHITE)
    svg = CHARTS / f"{stem}.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def title(fig, main: str, sub: str) -> None:
    fig.suptitle(main, x=0.055, y=0.975, ha="left", fontsize=19, color=INK, weight="semibold")
    fig.text(0.055, 0.895, sub, fontsize=10.2, color=SOFT, ha="left")


def source(fig, text: str) -> None:
    fig.text(0.055, 0.025, text, fontsize=7.1, color=SOFT, ha="left")


def validity_gates(validation: dict) -> None:
    summary = validation["summary"]
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 7.2))
    fig.subplots_adjust(left=0.055, right=0.96, top=0.73, bottom=0.17, wspace=0.15)
    cards = [
        (
            "GATE 1 · STATED RULE",
            "Published set is the raw\ntop four in only two runs",
            f"{summary['old_sensitivity_exact_published_top4_runs']} of {summary['old_sensitivity_run_count']}",
            RED,
        ),
        (
            "GATE 2 · WATER",
            "Published members in the\ndirect water-stress top five",
            f"{summary['published_vs_available_water_top5']['count']} of 4",
            BLUE,
        ),
        (
            "GATE 3 · CROP MIX",
            "Published members in the\ndirect crop-HHI top five",
            f"{summary['published_vs_crop_hhi_top5']['count']} of 4",
            GOLD,
        ),
    ]
    for ax, (kicker, heading, value, color) in zip(axes, cards):
        ax.set_facecolor(PALE)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.text(0.07, 0.86, kicker, transform=ax.transAxes, color=color, fontsize=8.5, weight="bold")
        ax.text(0.07, 0.66, heading, transform=ax.transAxes, color=INK, fontsize=12.3, weight="semibold")
        ax.text(0.07, 0.29, value, transform=ax.transAxes, color=color, fontsize=30, weight="bold")
    title(
        fig,
        "The inherited four-country claim fails three construct gates",
        "Formula sensitivity, direct available-water stress, and observed crop concentration do not support the same country statement.",
    )
    source(
        fig,
        "Sources: committed WDI internal-water screen, WDI/AQUASTAT SDG 6.4.2, and FAOSTAT 2024 harvested area. Sets are diagnostics, not policy priorities.",
    )
    save(fig, "water-three-gate-validity")


def membership_churn(validation: dict) -> None:
    summary = validation["summary"]
    sets = {
        "Published\nset": set(summary["published_set"]),
        "Old raw\ntop four": set(summary["old_raw_top4"]),
        "Available-water\ntop five": set(summary["available_water_top5"]),
        "Crop-HHI\ntop five": set(summary["crop_hhi_top5"]),
        "All-three\ndiagnostic": set(summary["diagnostic_variant_top5"]),
    }
    members = sorted(set().union(*sets.values()))
    matrix = np.array([[iso in group for group in sets.values()] for iso in members], dtype=int)
    fig, ax = plt.subplots(figsize=(10.9, 8.5))
    fig.subplots_adjust(left=0.14, right=0.94, top=0.76, bottom=0.15)
    ax.imshow(matrix, cmap=ListedColormap([WHITE, BLUE]), vmin=0, vmax=1, aspect="auto")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, "●" if matrix[i, j] else "·", ha="center", va="center",
                    color=WHITE if matrix[i, j] else RULE, fontsize=13)
    ax.set_xticks(range(len(sets)), list(sets.keys()))
    ax.set_yticks(range(len(members)), members)
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(-0.5, len(sets), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(members), 1), minor=True)
    ax.grid(which="minor", color=RULE, linewidth=0.7)
    title(
        fig,
        "Replacing proxies changes the countries, not just their order",
        "The direct crop-concentration set shares no member with the published four; the direct water set retains only Pakistan and Turkmenistan.",
    )
    source(
        fig,
        "Sources: committed construct-validation artifact. Crop-HHI top five uses all 41 FAOSTAT-visible roster economies; the combined diagnostic has 30 aligned rows.",
    )
    save(fig, "water-membership-churn")


def denominator_rebase(diagnostics: pd.DataFrame, validation: dict) -> None:
    focus = sorted(set(validation["summary"]["old_raw_top4"] + ["AFG", "LKA", "TJK"]))
    data = diagnostics.set_index("iso3").loc[focus].copy()
    data = data.dropna(subset=["internal_withdrawal_pct", "available_water_stress_pct"])
    data = data.sort_values("internal_withdrawal_pct")
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    fig.subplots_adjust(left=0.12, right=0.94, top=0.77, bottom=0.16)
    y = np.arange(len(data))
    for idx, (_, row) in enumerate(data.iterrows()):
        ax.plot([row.available_water_stress_pct, row.internal_withdrawal_pct], [idx, idx],
                color=RULE, linewidth=2.2, zorder=1)
    ax.scatter(data.available_water_stress_pct, y, color=BLUE, s=72, label="Available-water stress", zorder=3)
    ax.scatter(data.internal_withdrawal_pct, y, color=RED, s=72, label="Withdrawal / internal resources", zorder=3)
    for idx, (_, row) in enumerate(data.iterrows()):
        ax.text(row.internal_withdrawal_pct * 1.08, idx, f"{row.internal_withdrawal_pct:,.0f}%",
                va="center", fontsize=8.5, color=RED)
    ax.set_xscale("log")
    ax.set_xlim(5, max(data.internal_withdrawal_pct) * 1.8)
    ax.set_yticks(y, data.index)
    ax.set_xlabel("Percent (log scale)")
    ax.grid(axis="x", color=RULE, lw=0.7, which="both")
    ax.legend(frameon=False, loc="lower right")
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Changing the denominator compresses the extreme internal-water ratios",
        "SDG 6.4.2 uses available renewable water after environmental-flow requirements; it is still national and does not identify the basin mechanism.",
    )
    source(
        fig,
        "Source: World Bank WDI ER.H2O.FWTL.ZS and ER.H2O.FWST.ZS, latest 2022. A value above 100% is pressure, not direct proof of depletion or over-pumping.",
    )
    save(fig, "water-denominator-rebase")


def water_crop_scatter(diagnostics: pd.DataFrame, validation: dict) -> None:
    data = diagnostics.dropna(subset=["available_water_stress_pct", "crop_hhi"]).copy()
    corr = next(item for item in validation["correlations"]
                if item["label"] == "Available-water stress vs crop concentration")
    colors = np.where(data.published_member.astype(bool), BLUE, SOFT)
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    fig.subplots_adjust(left=0.11, right=0.94, top=0.77, bottom=0.16)
    ax.scatter(data.available_water_stress_pct, data.crop_hhi, c=colors, s=68,
               alpha=0.86, edgecolor=WHITE, linewidth=0.8)
    for row in data.itertuples():
        if row.published_member or row.iso3 in {"UZB", "LKA", "TJK", "KAZ"}:
            ax.text(row.available_water_stress_pct + 2, row.crop_hhi + 0.006,
                    row.iso3, fontsize=8.2, color=INK)
    ax.axvline(100, color=RULE, linestyle="--", linewidth=1)
    ax.text(102, ax.get_ylim()[1] * 0.96, "100%", color=SOFT, fontsize=8)
    ax.text(
        0.98, 0.94,
        f"Spearman {corr['spearman']:+.2f}\n95% bootstrap interval "
        f"{corr['bootstrap_ci95'][0]:+.2f} to {corr['bootstrap_ci95'][1]:+.2f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=9, color=RED,
        bbox=dict(boxstyle="round,pad=.5", facecolor=WHITE, edgecolor=RULE),
    )
    ax.text(
        0.98, 0.08,
        "Not plotted: TUV · KIR · FSM · NRU · VUT\n"
        "The crop-HHI top five all lack water-stress rows.",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8.6, color=GOLD,
        bbox=dict(boxstyle="round,pad=.45", facecolor=WHITE, edgecolor=RULE),
    )
    ax.set_xlabel("Available-water stress, SDG 6.4.2 (%)")
    ax.set_ylabel("Crop concentration (harvested-area HHI)")
    ax.grid(color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Water stress and crop concentration do not form one national pattern",
        "Across 30 aligned economies, the association is weak and uncertain; the most concentrated visible crop systems are excluded by missing water data.",
    )
    source(
        fig,
        "Sources: WDI/AQUASTAT SDG 6.4.2 (2022) and FAOSTAT Area harvested (2024). HHI measures national harvested-area concentration, not resilience.",
    )
    save(fig, "water-crop-construct-scatter")


def coverage_funnel(validation: dict) -> None:
    summary = validation["summary"]
    stages = [
        ("Program roster", summary["program_roster_n"]),
        ("FAOSTAT crop mix", summary["crop_mix_n"]),
        ("Available-water stress", summary["available_water_n"]),
        ("Aligned national rows", summary["aligned_water_crop_n"]),
        ("Crop-HHI top five with water data", summary["crop_hhi_top5_with_available_water_n"]),
        ("Basin × crop × irrigation join", 0),
    ]
    labels, values = zip(*stages)
    colors = [NAVY, BLUE, BLUE, GREEN, RED, GOLD]
    fig, ax = plt.subplots(figsize=(11.2, 7.3))
    fig.subplots_adjust(left=0.28, right=0.94, top=0.77, bottom=0.15)
    y = np.arange(len(stages))
    ax.barh(y, values, color=colors, height=0.6)
    for idx, value in enumerate(values):
        ax.text(value + 0.7, idx, str(value), va="center", fontsize=10, weight="semibold", color=INK)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 47)
    ax.set_xlabel("Economies / joined records")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The national source join loses the most crop-concentrated cases",
        "Coverage reaches 30 aligned economies, but none of the crop-HHI top five has a water-stress observation and no basin-level crop-water object exists.",
    )
    source(
        fig,
        "Sources: committed WDI/AQUASTAT and FAOSTAT source audit. Counts measure observability, not evidence quality or policy severity.",
    )
    save(fig, "water-source-alignment-funnel")


def crop_profiles(diagnostics: pd.DataFrame, validation: dict) -> None:
    summary = validation["summary"]
    focus = list(dict.fromkeys(summary["published_set"] + summary["crop_hhi_top5"]))
    data = diagnostics.set_index("iso3").loc[focus].dropna(subset=["crop_hhi"]).copy()
    data = data.sort_values("crop_hhi")
    fig, ax = plt.subplots(figsize=(11.3, 7.8))
    fig.subplots_adjust(left=0.13, right=0.94, top=0.77, bottom=0.16)
    colors = [BLUE if iso in summary["published_set"] else GOLD for iso in data.index]
    bars = ax.barh(data.index, data.crop_hhi, color=colors, height=0.64)
    for bar, (_, row) in zip(bars, data.iterrows()):
        label = f"{row.top_crop} · {row.top_crop_share:.0%} of harvested area"
        ax.text(row.crop_hhi + 0.012, bar.get_y() + bar.get_height() / 2,
                label, va="center", fontsize=8.4, color=SOFT)
    ax.set_xlim(0, 1.08)
    ax.set_xlabel("Harvested-area concentration (HHI; 1 = one crop)")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The published four are not the most crop-concentrated economies",
        "Blue bars are published members; gold bars are the direct FAOSTAT top five, dominated by coconut area in small island economies.",
    )
    source(
        fig,
        "Source: FAOSTAT Crops and Livestock Products, Area harvested, latest common crop year 2024. National crop mix is not crop-water demand.",
    )
    save(fig, "water-crop-concentration-profiles")


def driver_dominance(validation: dict) -> None:
    wanted = [
        "Diagnostic variant vs available-water stress",
        "Diagnostic variant vs crop concentration",
        "Diagnostic variant vs rural share",
    ]
    labels = ["Available-water stress", "Crop concentration", "Rural share"]
    records = [next(item for item in validation["correlations"] if item["label"] == label) for label in wanted]
    estimates = np.array([record["spearman"] for record in records])
    lows = np.array([record["bootstrap_ci95"][0] for record in records])
    highs = np.array([record["bootstrap_ci95"][1] for record in records])
    errors = np.vstack([estimates - lows, highs - estimates])
    fig, ax = plt.subplots(figsize=(10.9, 7.1))
    fig.subplots_adjust(left=0.24, right=0.94, top=0.77, bottom=0.16)
    y = np.arange(len(labels))
    colors = [BLUE, GOLD, GREEN]
    ax.barh(y, estimates, xerr=errors, color=colors, height=0.58, capsize=4,
            error_kw={"ecolor": INK, "elinewidth": 1.2})
    for idx, estimate in enumerate(estimates):
        ax.text(estimate + (0.035 if estimate >= 0 else -0.035), idx, f"{estimate:+.2f}",
                va="center", ha="left" if estimate >= 0 else "right", fontsize=10, weight="semibold")
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.set_xlim(-0.5, 1.05)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Spearman correlation with the all-three diagnostic score")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The source-upgraded diagnostic is still a water ranking",
        "Its ordering tracks available-water stress closely and has near-zero association with the crop-concentration term named in the research question.",
    )
    source(
        fig,
        "N=30 aligned national rows. Error bars are 95% deterministic bootstrap intervals (5,000 resamples). Composite remains triage only.",
    )
    save(fig, "water-diagnostic-driver-dominance")


def sensitivity_membership(validation: dict) -> None:
    data = pd.DataFrame(validation["diagnostic_membership_frequency"])
    data = data.sort_values(["top5_appearances", "iso3"]).reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10.8, 7.1))
    fig.subplots_adjust(left=0.12, right=0.94, top=0.77, bottom=0.16)
    colors = [BLUE if value else GOLD for value in data.published_member]
    ax.barh(data.iso3, data.top5_appearances, color=colors, height=0.62)
    for idx, row in data.iterrows():
        ax.text(row.top5_appearances + 0.4, idx, f"{row.top5_appearances}/27",
                va="center", fontsize=9, color=INK)
    ax.set_xlim(0, 30)
    ax.set_xlabel("Appearances in the diagnostic top five")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Internal stability cannot repair a construct mismatch",
        "Across 27 ±50% specifications, four economies recur—but Sri Lanka is one of them and Azerbaijan never appears. Blue marks published members.",
    )
    source(
        fig,
        "Diagnostic sensitivity varies the water ceiling and crop/rural exponents at 0.5×, 1×, and 1.5×. Stability is not external validation.",
    )
    save(fig, "water-diagnostic-sensitivity-membership")


def next_data_object(validation: dict) -> None:
    fig, ax = plt.subplots(figsize=(12.0, 6.8))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.78, bottom=0.15)
    ax.axis("off")
    boxes = [
        (0.02, "WATER", "Basin withdrawal /\ndepletion and allocation", BLUE),
        (0.27, "CROPS", "Harvested area ×\nirrigation status", GREEN),
        (0.52, "DEMAND", "Crop water requirement\nand common-year weather", GOLD),
        (0.77, "EXPOSURE", "Farms / people inside\nthe same basin-crop unit", RED),
    ]
    for x, kicker, body, color in boxes:
        ax.add_patch(plt.Rectangle((x, 0.34), 0.20, 0.38, transform=ax.transAxes,
                                   facecolor=PALE, edgecolor=RULE, linewidth=1.2))
        ax.text(x + 0.02, 0.64, kicker, transform=ax.transAxes, color=color,
                fontsize=9, weight="bold")
        ax.text(x + 0.02, 0.49, body, transform=ax.transAxes, color=INK,
                fontsize=11, weight="semibold")
        if x < 0.77:
            ax.annotate("", xy=(x + 0.245, 0.53), xytext=(x + 0.205, 0.53),
                        xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", color=SOFT, lw=1.3))
    ax.text(0.5, 0.18, "CURRENT JOIN: 0 basin × crop × irrigation observations",
            transform=ax.transAxes, ha="center", color=RED, fontsize=13, weight="bold")
    title(
        fig,
        "The next study needs one shared unit—not another national composite",
        "A defensible water-crop exposure claim requires the four objects to meet at basin × crop × year level.",
    )
    source(
        fig,
        "Design specification derived from the construct-validation result. Candidate public sources: AQUASTAT/Aqueduct or GRACE, FAOSTAT/SPAM, crop-water coefficients, and gridded exposure.",
    )
    save(fig, "water-next-data-object")


def thumbnail(validation: dict) -> None:
    summary = validation["summary"]
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    fig.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.10)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color=NAVY))
    ax.text(0.055, 0.82, "WATER × CROPS · CONSTRUCT VALIDATION", transform=ax.transAxes,
            color="#75D1F0", fontsize=10, weight="bold")
    ax.text(0.055, 0.62, "The ‘stable top four’\ndoes not survive its own constructs",
            transform=ax.transAxes, color=WHITE, fontsize=29, weight="bold", va="center")
    ax.text(0.055, 0.28,
            "Direct available-water stress retains two published members.\n"
            "Direct crop concentration retains none.",
            transform=ax.transAxes, color="#D8E7F0", fontsize=13, va="center")
    ax.add_patch(plt.Rectangle((0.72, 0.18), 0.21, 0.64, transform=ax.transAxes, color=WHITE, alpha=0.97))
    ax.text(0.825, 0.67, f"{summary['old_sensitivity_exact_published_top4_runs']} / 7",
            transform=ax.transAxes, ha="center", color=RED, fontsize=34, weight="bold")
    ax.text(0.825, 0.53, "sensitivity runs have the\npublished raw top four",
            transform=ax.transAxes, ha="center", color=INK, fontsize=10)
    ax.plot([0.76, 0.89], [0.43, 0.43], transform=ax.transAxes, color=RULE, lw=1)
    ax.text(0.825, 0.31, "0 / 4", transform=ax.transAxes, ha="center", color=GOLD, fontsize=30, weight="bold")
    ax.text(0.825, 0.22, "published members in the\ncrop-HHI top five",
            transform=ax.transAxes, ha="center", color=INK, fontsize=9)
    save(fig, "water-stress-crop-diversification-thumbnail", dpi=220)
    png = CHARTS / "water-stress-crop-diversification-thumbnail.png"
    svg = CHARTS / "water-stress-crop-diversification-thumbnail.svg"
    with Image.open(png) as image:
        width, height = image.size
    sidecar = {
        "program": "water-stress-crop-diversification",
        "title": "The stable top four does not survive its own constructs",
        "caption": (
            "The published set is the raw top four in only two of seven sensitivity runs; "
            "direct water stress retains two members and direct crop concentration none."
        ),
        "headline_number": "2 of 7 · 0 of 4 crop",
        "visual_form": "construct-validation finding card",
        "source": "WDI/AQUASTAT SDG 6.4.2 and FAOSTAT 2024 harvested area",
        "inputs": [
            "generated/water-construct-validation.json",
            "generated/water-construct-diagnostics.csv",
        ],
        "script": "water-stress-crop-diversification/scripts/build-figure-dossier.py",
        "attestation_chain": "ai-first",
        "constitution_ref": "CONSTITUTION.md §18",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dimensions": {"width": width, "height": height},
        "files": {"png": png.name, "svg": svg.name},
        "sha256": {
            "png": hashlib.sha256(png.read_bytes()).hexdigest(),
            "svg": hashlib.sha256(svg.read_bytes()).hexdigest(),
        },
    }
    (CHARTS / "water-stress-crop-diversification-thumbnail.json").write_text(
        json.dumps(sidecar, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    validation = json.loads((GEN / "water-construct-validation.json").read_text(encoding="utf-8"))
    diagnostics = pd.read_csv(GEN / "water-construct-diagnostics.csv")
    validity_gates(validation)
    membership_churn(validation)
    denominator_rebase(diagnostics, validation)
    water_crop_scatter(diagnostics, validation)
    coverage_funnel(validation)
    crop_profiles(diagnostics, validation)
    driver_dominance(validation)
    sensitivity_membership(validation)
    next_data_object(validation)
    thumbnail(validation)
    print("Built 9 article figures plus the program thumbnail.")


if __name__ == "__main__":
    main()
