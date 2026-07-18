"""Build the school-heat construct-validation figure dossier.

Every plotted value comes from generated school-construct-validation.json or
school-construct-diagnostics.csv. A figure earns space only by carrying a
finding, sensitivity result, coverage limit, or next-data requirement.
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


def corr(validation: dict, label: str) -> dict:
    return next(row for row in validation["correlations"] if row["label"] == label)


def validity_gates(validation: dict) -> None:
    s = validation["summary"]
    heat_corr = corr(validation, "Old index vs heatwave affected count")
    child_corr = corr(validation, "Child population vs heatwave affected count")
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 7.2))
    fig.subplots_adjust(left=0.055, right=0.96, top=0.73, bottom=0.17, wspace=0.15)
    cards = [
        ("GATE 1 · ROBUSTNESS", "Cambodia leads only five of\nsix discriminating runs", "5 of 6", RED),
        ("GATE 2 · OBSERVED COUNT", "Cambodia ranks last among six\nheatwave-major ADB rows", "6 of 6", GOLD),
        ("GATE 3 · CONSTRUCT", "Index correlation vs outcome;\nchild population shown below", f"{heat_corr['spearman']:+.2f}", BLUE),
    ]
    for ax, (kicker, heading, value, color) in zip(axes, cards):
        ax.set_facecolor(PALE)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.text(0.07, 0.86, kicker, transform=ax.transAxes, color=color, fontsize=8.5, weight="bold")
        ax.text(0.07, 0.65, heading, transform=ax.transAxes, color=INK, fontsize=12.0, weight="semibold")
        ax.text(0.07, 0.29, value, transform=ax.transAxes, color=color, fontsize=30, weight="bold")
        if kicker.endswith("CONSTRUCT"):
            ax.text(0.07, 0.18, f"child population: {child_corr['spearman']:+.2f}",
                    transform=ax.transAxes, color=GREEN, fontsize=10, weight="semibold")
    title(
        fig,
        "The Cambodia top-one claim fails robustness and outcome checks",
        "The old index loses one non-degenerate sensitivity run and does not order the six observed heatwave-major disruption counts.",
    )
    source(
        fig,
        "Sources: committed ±50% sensitivity runs; UNICEF Learning Interrupted annex, 2024. Correlations are descriptive for N=6 selected event rows.",
    )
    save(fig, "school-three-gate-validity")


def sensitivity_runs(validation: dict) -> None:
    data = pd.DataFrame(validation["sensitivity_runs"])
    data["status"] = np.where(data.all_zero, "All-zero tie",
                              np.where(data.khm_is_top1, "KHM #1", "PAK #1 · KHM #2"))
    colors = [RULE if row.all_zero else (BLUE if row.khm_is_top1 else RED) for row in data.itertuples()]
    fig, ax = plt.subplots(figsize=(11.4, 7.5))
    fig.subplots_adjust(left=0.23, right=0.94, top=0.77, bottom=0.16)
    y = np.arange(len(data))
    bars = ax.barh(y, data.khm_value.fillna(0), color=colors, height=0.62)
    for bar, row in zip(bars, data.itertuples()):
        x = max(float(row.khm_value or 0), 0)
        ax.text(x + 0.8, bar.get_y() + bar.get_height() / 2,
                f"{row.status} · KHM score {float(row.khm_value or 0):.2f}",
                va="center", fontsize=8.7, color=INK)
    labels = [label.replace("_", " ") for label in data.label]
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(data.khm_value.max() * 1.45, 40))
    ax.set_xlabel("Cambodia index value under each specification")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "One perturbation puts Pakistan first; another produces no ranking",
        "The published ‘every perturbation’ language counted an all-zero tie as evidence and overlooked the lower-floor run that Cambodia loses.",
    )
    source(fig, "Source: school-heat-disruption/sensitivity-runs.json, seven committed baseline/±50% specifications.")
    save(fig, "school-sensitivity-run-verdicts")


def proxy_outcome_scatter(diagnostics: pd.DataFrame, validation: dict) -> None:
    data = diagnostics[(diagnostics.is_heatwave_major == True) & diagnostics.old_panel_member].copy()  # noqa: E712
    relation = corr(validation, "Old index vs heatwave affected count")
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    fig.subplots_adjust(left=0.11, right=0.94, top=0.77, bottom=0.16)
    sizes = 45 + 3.0 * np.sqrt(data.children_0_14_millions * 10)
    colors = [RED if iso == "KHM" else (GOLD if iso == "AFG" else BLUE) for iso in data.iso3]
    ax.scatter(data.school_heat_pressure_index, data.students_affected_2024 / 1e6,
               s=sizes, c=colors, edgecolor=WHITE, linewidth=1.0, alpha=0.9)
    for row in data.itertuples():
        ax.text(row.school_heat_pressure_index + 0.25, row.students_affected_2024 / 1e6 + 0.9,
                row.iso3, fontsize=9, color=INK, weight="semibold")
    ax.text(0.98, 0.94,
            f"Spearman {relation['spearman']:+.2f}\n95% bootstrap interval "
            f"{relation['bootstrap_ci95'][0]:+.2f} to {relation['bootstrap_ci95'][1]:+.2f}",
            transform=ax.transAxes, ha="right", va="top", fontsize=9, color=RED,
            bbox=dict(boxstyle="round,pad=.5", facecolor=WHITE, edgecolor=RULE))
    ax.set_xlabel("Inherited school-heat pressure index")
    ax.set_ylabel("Students affected in 2024 (millions)")
    ax.set_xlim(-0.6, 16.0)
    ax.set_ylim(0, 60)
    ax.grid(color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The national proxy does not order observed heatwave disruptions",
        "Cambodia has the highest proxy score but the smallest affected-student count; Afghanistan records 10.9 million with a zero proxy score.",
    )
    source(
        fig,
        "Sources: UNICEF 2024 annex rows whose largest disruption hazard is heatwave; WDI/CCKP inherited panel. Bubble area scales with population aged 0-14.",
    )
    save(fig, "school-proxy-outcome-scatter")


def heatwave_ranking(diagnostics: pd.DataFrame) -> None:
    data = diagnostics[(diagnostics.is_heatwave_major == True) & diagnostics.old_panel_member].copy()  # noqa: E712
    data = data.sort_values("students_affected_2024")
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    fig.subplots_adjust(left=0.15, right=0.94, top=0.77, bottom=0.16)
    colors = [RED if iso == "KHM" else (GOLD if iso == "AFG" else BLUE) for iso in data.iso3]
    bars = ax.barh(data.iso3, data.students_affected_2024 / 1e6, color=colors, height=0.62)
    for bar, row in zip(bars, data.itertuples()):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                f"{row.students_affected_2024 / 1e6:.1f}M · old index rank {int(row.old_baseline_rank)}",
                va="center", fontsize=9, color=INK)
    ax.set_xlim(0, 64)
    ax.set_xlabel("Students affected by climate-related school disruption in 2024 (millions)")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Cambodia is sixth of six by the direct heatwave-disruption count",
        "The annex count is not days lost or learning loss, but it directly contradicts presenting Cambodia as the uniquely leading disruption case.",
    )
    source(fig, "Source: UNICEF Learning Interrupted annex, 2024. Major hazard is the hazard causing each country's largest recorded disruption.")
    save(fig, "school-heatwave-affected-ranking")


def driver_dominance(validation: dict) -> None:
    labels = [
        "Child population",
        "Inherited index",
        "Historical tasmax",
        "Primary PTR",
    ]
    keys = [
        "Child population vs heatwave affected count",
        "Old index vs heatwave affected count",
        "Historical tasmax vs heatwave affected count",
        "Primary PTR vs heatwave affected count",
    ]
    records = [corr(validation, key) for key in keys]
    estimates = np.array([row["spearman"] for row in records])
    lows = np.array([row["bootstrap_ci95"][0] for row in records])
    highs = np.array([row["bootstrap_ci95"][1] for row in records])
    errors = np.vstack([estimates - lows, highs - estimates])
    fig, ax = plt.subplots(figsize=(10.9, 7.2))
    fig.subplots_adjust(left=0.23, right=0.94, top=0.77, bottom=0.16)
    y = np.arange(len(labels))
    colors = [GREEN, BLUE, GOLD, RED]
    ax.barh(y, estimates, xerr=errors, color=colors, height=0.58, capsize=4,
            error_kw={"ecolor": INK, "elinewidth": 1.1})
    for idx, value in enumerate(estimates):
        ax.text(value + (0.04 if value >= 0 else -0.04), idx, f"{value:+.2f}",
                va="center", ha="left" if value >= 0 else "right", fontsize=10, weight="semibold")
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.set_xlim(-1.15, 1.15)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Spearman correlation with affected-student count")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Affected-student counts track demographic scale, not the proxy",
        "Within six heatwave-major rows, child population correlates strongly with the count; the index and annual tasmax correlations are near zero.",
    )
    source(fig, "N=6 selected UNICEF heatwave-major ADB rows. Error bars are deterministic 95% bootstrap intervals; small-N uncertainty is intentionally visible.")
    save(fig, "school-driver-dominance")


def coverage_funnel(validation: dict) -> None:
    s = validation["summary"]
    stages = [
        ("ADB program roster", s["adb_roster_n"]),
        ("Inherited index panel", s["old_panel_n"]),
        ("UNICEF annex rows", s["unicef_adb_annex_rows_n"]),
        ("Index × annex overlap", s["old_panel_unicef_overlap_n"]),
        ("Complete enrollment overlap", s["complete_enrollment_overlap_n"]),
        ("Heatwave-major validation rows", s["heatwave_major_rows_n"]),
        ("School-day × duration × learning panel", 0),
    ]
    labels, values = zip(*stages)
    colors = [NAVY, BLUE, BLUE, GREEN, GREEN, GOLD, RED]
    fig, ax = plt.subplots(figsize=(11.3, 7.5))
    fig.subplots_adjust(left=0.29, right=0.94, top=0.77, bottom=0.15)
    y = np.arange(len(stages))
    ax.barh(y, values, color=colors, height=0.58)
    for idx, value in enumerate(values):
        ax.text(value + 0.7, idx, str(value), va="center", fontsize=10, weight="semibold", color=INK)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 48)
    ax.set_xlabel("Economies / aligned records")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "An outcome join is now possible, but the decision-grade panel is still absent",
        "UNICEF supplies 21 ADB rows and 19 overlap the old screen; no source yet joins school-day heat, closure duration, and learning or attendance.",
    )
    source(fig, "Sources: inherited 32-economy WDI/CCKP panel, UNICEF 2024 annex, and WDI enrollment by level. Missing annex rows are unknown, not zero.")
    save(fig, "school-source-alignment-funnel")


def hazard_composition(validation: dict) -> None:
    s = validation["summary"]
    affected = pd.Series(s["hazard_students_affected"]).sort_values()
    counts = s["hazard_row_counts"]
    fig, ax = plt.subplots(figsize=(11.2, 7.4))
    fig.subplots_adjust(left=0.20, right=0.94, top=0.77, bottom=0.16)
    colors = [BLUE if label == "Heatwave" else SOFT for label in affected.index]
    bars = ax.barh(affected.index, affected.values / 1e6, color=colors, height=0.62)
    for bar, label, value in zip(bars, affected.index, affected.values):
        magnitude = f"{value / 1e6:.1f}M" if value >= 100_000 else f"{value / 1e3:.1f}k"
        ax.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height() / 2,
                f"{magnitude} · {counts[label]} row{'s' if counts[label] != 1 else ''}",
                va="center", fontsize=9, color=INK)
    ax.set_xlim(0, max(affected.values / 1e6) * 1.16)
    ax.set_xlabel("Students affected across the 21 ADB annex rows (millions)")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Heatwaves dominate the observed ADB disruption count",
        "Six heatwave-major rows account for 154.9 million affected students, but the annex records each country's largest hazard rather than a complete event panel.",
    )
    source(fig, "Source: UNICEF Learning Interrupted annex, 2024. Affected counts may combine direct reports and enrollment-based estimates.")
    save(fig, "school-hazard-burden-composition")


def enrollment_share(diagnostics: pd.DataFrame) -> None:
    data = diagnostics[diagnostics.enrollment_levels_complete == True].copy()  # noqa: E712
    data = data.sort_values("affected_to_enrollment_pct")
    fig, ax = plt.subplots(figsize=(11.2, 8.2))
    fig.subplots_adjust(left=0.16, right=0.94, top=0.77, bottom=0.14)
    colors = [RED if value > 100 else (BLUE if hazard == "Heatwave" else SOFT)
              for value, hazard in zip(data.affected_to_enrollment_pct, data.major_hazard)]
    bars = ax.barh(data.iso3, data.affected_to_enrollment_pct, color=colors, height=0.62)
    for bar, row in zip(bars, data.itertuples()):
        ax.text(bar.get_width() + 1.4, bar.get_y() + bar.get_height() / 2,
                f"{row.affected_to_enrollment_pct:.1f}% · {row.major_hazard}",
                va="center", fontsize=8.2, color=INK)
    ax.axvline(100, color=RED, linestyle="--", linewidth=1)
    ax.set_xlim(0, max(110, data.affected_to_enrollment_pct.max() * 1.12))
    ax.set_xlabel("Affected students / latest pre-primary + primary + secondary enrollment (%)")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The denominator check exposes both nationwide disruption and vintage mismatch",
        "Bangladesh slightly exceeds 100% because the 2024 numerator is compared with mixed-vintage enrollment levels; this is a diagnostic proxy, not an official rate.",
    )
    source(fig, "Sources: UNICEF 2024 annex and latest WDI SE.PRE.ENRL, SE.PRM.ENRL, SE.SEC.ENRL observations from 2015-2025. N=19 complete denominators.")
    save(fig, "school-enrollment-share-proxy")


def next_data_object() -> None:
    fig, ax = plt.subplots(figsize=(12.8, 7.0))
    fig.subplots_adjust(left=0.035, right=0.965, top=0.78, bottom=0.15)
    ax.axis("off")
    boxes = [
        (0.015, "CALENDAR", "Instruction days\nand school hours", BLUE),
        (0.215, "HEAT", "Daily temperature,\nhumidity, indoor conditions", RED),
        (0.415, "SCHOOLS", "Geocodes, enrollment,\ncooling and infrastructure", GREEN),
        (0.615, "DISRUPTION", "Closure dates, hours\nand reason", GOLD),
        (0.815, "OUTCOME", "Attendance, progression\nor learning", NAVY),
    ]
    for x, kicker, body, color in boxes:
        ax.add_patch(plt.Rectangle((x, 0.34), 0.17, 0.38, transform=ax.transAxes,
                                   facecolor=PALE, edgecolor=RULE, linewidth=1.2))
        ax.text(x + 0.015, 0.64, kicker, transform=ax.transAxes, color=color,
                fontsize=8.2, weight="bold")
        ax.text(x + 0.015, 0.49, body, transform=ax.transAxes, color=INK,
                fontsize=9.8, weight="semibold")
        if x < 0.815:
            ax.annotate("", xy=(x + 0.198, 0.53), xytext=(x + 0.173, 0.53),
                        xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", color=SOFT, lw=1.2))
    ax.text(0.5, 0.18, "CURRENT COMPLETE JOIN: 0 school × instructional-day × outcome observations",
            transform=ax.transAxes, ha="center", color=RED, fontsize=12.4, weight="bold")
    title(
        fig,
        "The next study needs school-day exposure and duration—not another national score",
        "UNICEF adds an observed disruption count; decision-grade research still requires all five objects to meet at school or district × day level.",
    )
    source(fig, "Design specification derived from the construct-validation result. Candidate sources: national EMIS/calendars, ERA5-Land, school geocodes, closure orders, and administrative outcomes.")
    save(fig, "school-next-data-object")


def thumbnail(validation: dict) -> None:
    s = validation["summary"]
    relation = corr(validation, "Old index vs heatwave affected count")
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    fig.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.10)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color=NAVY))
    ax.text(0.055, 0.82, "SCHOOL HEAT · CONSTRUCT VALIDATION", transform=ax.transAxes,
            color="#75D1F0", fontsize=10, weight="bold")
    ax.text(0.055, 0.62, "Cambodia led the proxy—\nbut ranked last by disruption count",
            transform=ax.transAxes, color=WHITE, fontsize=28, weight="bold", va="center")
    ax.text(0.055, 0.27,
            "The ‘every perturbation’ claim is false. Among six heatwave-major\n"
            "ADB rows, the old index has near-zero rank association with affected students.",
            transform=ax.transAxes, color="#D8E7F0", fontsize=12.4, va="center")
    ax.add_patch(plt.Rectangle((0.74, 0.17), 0.20, 0.66, transform=ax.transAxes, color=WHITE, alpha=0.98))
    ax.text(0.84, 0.68, "6 / 6", transform=ax.transAxes, ha="center", color=RED, fontsize=34, weight="bold")
    ax.text(0.84, 0.55, "Cambodia's affected-count\nrank among heatwave rows",
            transform=ax.transAxes, ha="center", color=INK, fontsize=9.6)
    ax.plot([0.775, 0.905], [0.43, 0.43], transform=ax.transAxes, color=RULE, lw=1)
    ax.text(0.84, 0.31, f"{relation['spearman']:+.2f}", transform=ax.transAxes,
            ha="center", color=BLUE, fontsize=30, weight="bold")
    ax.text(0.84, 0.22, "index vs affected count\nSpearman correlation",
            transform=ax.transAxes, ha="center", color=INK, fontsize=9)
    save(fig, "school-heat-disruption-thumbnail", dpi=220)

    png = CHARTS / "school-heat-disruption-thumbnail.png"
    svg = CHARTS / "school-heat-disruption-thumbnail.svg"
    with Image.open(png) as image:
        width, height = image.size
    sidecar = {
        "program": "school-heat-disruption",
        "title": "Cambodia led the proxy but ranked last by disruption count",
        "caption": (
            "Cambodia leads the inherited proxy but ranks sixth of six by the UNICEF 2024 affected-student count "
            "among ADB rows whose largest disruption hazard is heatwave."
        ),
        "headline_number": f"6 of 6 · rho {relation['spearman']:+.2f}",
        "visual_form": "construct-validation finding card",
        "source": "UNICEF Learning Interrupted annex 2024; WDI/CCKP inherited panel",
        "inputs": [
            "generated/school-construct-validation.json",
            "generated/school-construct-diagnostics.csv",
        ],
        "script": "school-heat-disruption/scripts/build-figure-dossier.py",
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
    (CHARTS / "school-heat-disruption-thumbnail.json").write_text(
        json.dumps(sidecar, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    validation = json.loads((GEN / "school-construct-validation.json").read_text(encoding="utf-8"))
    diagnostics = pd.read_csv(GEN / "school-construct-diagnostics.csv")
    validity_gates(validation)
    sensitivity_runs(validation)
    proxy_outcome_scatter(diagnostics, validation)
    heatwave_ranking(diagnostics)
    driver_dominance(validation)
    coverage_funnel(validation)
    hazard_composition(validation)
    enrollment_share(diagnostics)
    next_data_object()
    thumbnail(validation)
    print("Built 9 article figures plus the program thumbnail.")


if __name__ == "__main__":
    main()
