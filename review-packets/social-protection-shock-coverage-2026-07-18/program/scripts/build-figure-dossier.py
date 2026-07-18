"""Build the social-protection construct-validation figure dossier.

Every plotted value is read from committed generated artifacts. Figures
communicate a finding, source limitation, sensitivity result, or construct
disagreement; none is a decorative country ranking.
attestation_chain: ai-first.
"""

from __future__ import annotations

import json
import hashlib
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
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 5.9))
    fig.subplots_adjust(left=0.055, right=0.96, top=0.73, bottom=0.17, wspace=0.15)
    cards = [
        ("GATE 1 · MEMBERSHIP", "The named five is not\nthe value-ranked five", "3 of 5", RED),
        ("GATE 2 · OBSERVED RESPONSE", "Every named economy had a\ndocumented cash-transfer response", "5 of 5", BLUE),
        ("GATE 3 · DELIVERY", "Comparable receipt, speed,\nand failure outcomes are absent", "0 joined", GOLD),
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
        "A stable formula did not produce a valid shock-payment finding",
        "The screen fails its own ranking rule, and the direct source stops at instrument presence—not delivery performance.",
    )
    source(
        fig,
        "Sources: committed WDI/ASPIRE/Findex panel; World Bank COVID-19 SPJ response matrix v15. Response presence does not establish successful receipt. attestation_chain: ai-first.",
    )
    save(fig, "sp-three-gate-validity")


def membership_churn(dropped: dict, readiness: dict) -> None:
    sets = {
        "Published\nnamed five": set(dropped["headline_five"]),
        "Panel value\nrank": set(row["iso3"] for row in dropped["value_ranked_order"][:5]),
        "Mean-imputed\nmissing legs": set(dropped["imputation_variant"]["imputed_top5"]),
        "Live all-SP\nvariant": set(readiness["summary"]["all_sp_live_top5"]),
        "Safety-net\nvariant": set(readiness["summary"]["safety_net_variant_top5"]),
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
    ax.set_xticks(np.arange(-.5, len(sets), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(members), 1), minor=True)
    ax.grid(which="minor", color=RULE, linewidth=0.7)
    title(
        fig,
        "Changing the missing-data or coverage rule changes the membership",
        "The live safety-net variant shares no economy with the published set; it is also too sparse and old to replace it.",
    )
    source(
        fig,
        "Sources: committed dropped-leg and source-readiness artifacts. All sets are diagnostics; none is a policy ranking.",
    )
    save(fig, "sp-membership-churn")


def dropped_leg_rank(dropped: dict) -> None:
    rows = pd.DataFrame(dropped["value_ranked_order"][:8]).sort_values("gap")
    fig, ax = plt.subplots(figsize=(10.8, 7.3))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.77, bottom=0.15)
    colors = [BLUE if iso in dropped["headline_five"] else RED for iso in rows.iso3]
    ax.barh(rows.iso3, rows.gap, color=colors, height=0.64)
    for i, row in enumerate(rows.itertuples()):
        label = "both legs" if row.legs_present == "both" else f"{row.legs_present}; omitted"
        ax.text(row.gap + 0.25, i, label, va="center", fontsize=8.5, color=SOFT)
    ax.set_xlabel("Inherited readiness-gap value (triage composite)")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Vanuatu and Tajikistan outrank two named members but were omitted",
        "The panel scores one-legged records, then the headline silently requires both legs. Red bars expose the rule change.",
    )
    source(
        fig,
        "Source: committed WDI/ASPIRE/Findex recomputation. Composite values are triage only; missing-leg records are not comparable to complete records.",
    )
    save(fig, "sp-dropped-leg-ranking")


def response_heatmap(diagnostics: pd.DataFrame) -> None:
    focus = ["BGD", "LAO", "MMR", "PAK", "PHL", "VUT", "TJK", "PNG", "SLB", "TLS"]
    columns = [
        "cash_based_transfers", "public_works", "in_kind_or_school_feeding",
        "utility_and_financial_support", "paid_leave_or_unemployment",
        "health_insurance_support", "pensions_and_disability_benefits",
        "social_security_contributions",
    ]
    labels = ["Cash", "Public\nworks", "In-kind", "Utility /\nfinance", "Leave /\nunemp.", "Health", "Pension /\ndisability", "Contributions"]
    data = diagnostics.set_index("iso3").loc[focus, columns].astype(float)
    fig, ax = plt.subplots(figsize=(12.1, 7.4))
    fig.subplots_adjust(left=0.12, right=0.94, top=0.76, bottom=0.17)
    ax.imshow(data.values, cmap=ListedColormap([WHITE, BLUE]), vmin=0, vmax=1, aspect="auto")
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, "✓" if data.iloc[i, j] else "", ha="center", va="center",
                    color=WHITE, fontsize=12, weight="bold")
    ax.set_xticks(range(len(labels)), labels)
    ax.set_yticks(range(len(focus)), focus)
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(-.5, len(labels), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(focus), 1), minor=True)
    ax.grid(which="minor", color=RULE, linewidth=0.7)
    title(
        fig,
        "The direct source observes response instruments, not whether payments arrived",
        "All five published members have a documented cash-transfer response; checkmarks carry no receipt or speed denominator.",
    )
    source(
        fig,
        "Source: World Bank Global Database on Social Protection and Jobs Responses to COVID-19, v15, matrix pp. 5–10. Preliminary instrument presence only.",
    )
    save(fig, "sp-covid-response-matrix")


def proxy_vs_response(diagnostics: pd.DataFrame, validation: dict) -> None:
    data = diagnostics.dropna(subset=["shock_payment_readiness_gap", "social_protection_breadth"]).copy()
    fig, ax = plt.subplots(figsize=(10.8, 7.3))
    fig.subplots_adjust(left=0.11, right=0.95, top=0.77, bottom=0.16)
    colors = np.where(data.headline_top5, BLUE, SOFT)
    ax.scatter(data.shock_payment_readiness_gap, data.social_protection_breadth,
               c=colors, s=68, alpha=0.88, edgecolor=WHITE, linewidth=0.8)
    for row in data.itertuples():
        if row.headline_top5 or row.iso3 in {"VUT", "TJK", "IND", "NPL", "UZB"}:
            ax.text(row.shock_payment_readiness_gap + 0.18, row.social_protection_breadth + 0.08,
                    row.iso3, fontsize=8.2, color=INK)
    corr = validation["summary"]["correlations"][0]
    ax.text(0.98, 0.94,
            f"Spearman {corr['spearman']:+.2f}\n95% bootstrap interval {corr['bootstrap_ci95'][0]:+.2f} to {corr['bootstrap_ci95'][1]:+.2f}",
            transform=ax.transAxes, ha="right", va="top", fontsize=9, color=RED,
            bbox=dict(boxstyle="round,pad=.5", facecolor=WHITE, edgecolor=RULE))
    ax.set_xlabel("Inherited readiness-gap value")
    ax.set_ylabel("Documented social-protection response categories (0–8)")
    ax.set_yticks(range(0, 9))
    ax.grid(color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The inherited gap has no visible association with response breadth",
        "Near-zero association and a wide interval do not validate either need or delivery capacity.",
    )
    source(
        fig,
        "N=24 economies with a computed inherited gap and a documented response row. Breadth is a database diagnostic, not an outcome or readiness score.",
    )
    save(fig, "sp-proxy-vs-response-breadth")


def source_funnel(readiness: dict, validation: dict) -> None:
    summary = readiness["summary"]
    stages = [
        ("ADB DMC roster", summary["roster_n"]),
        ("Current poverty value", summary["poverty_latest_rows"]),
        ("All-SP coverage", summary["all_sp_latest_rows"]),
        ("Account ownership", summary["account_latest_rows"]),
        ("COVID response matrix", validation["summary"]["documented_dmc"]),
        ("Comparable delivery outcome", 0),
    ]
    labels, values = zip(*stages)
    colors = [NAVY, BLUE, BLUE, BLUE, GREEN, RED]
    fig, ax = plt.subplots(figsize=(11.2, 7.3))
    fig.subplots_adjust(left=0.25, right=0.94, top=0.77, bottom=0.15)
    y = np.arange(len(stages))
    ax.barh(y, values, color=colors, height=0.6)
    for i, value in enumerate(values):
        ax.text(value + 0.7, i, str(value), va="center", fontsize=10, weight="semibold", color=INK)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 47)
    ax.set_xlabel("Economies / joined country records")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "More source rows do not close the delivery-outcome gap",
        "The response database expands observability of instruments; the comparable last-mile outcome remains zero.",
    )
    source(
        fig,
        "Sources: current WDI API audit and World Bank COVID-19 SPJ matrix. Counts describe source availability, not quality-adjusted evidence.",
    )
    save(fig, "sp-source-alignment-funnel")


def vintage_profile(readiness: dict) -> None:
    rows = pd.DataFrame(readiness["rerank_rows"])
    specs = [
        ("poverty_year", "Poverty", RED),
        ("all_sp_year", "All SP", BLUE),
        ("safety_net_year", "Safety net", GREEN),
        ("findex_year", "Account", GOLD),
    ]
    fig, ax = plt.subplots(figsize=(11.4, 7.2))
    fig.subplots_adjust(left=0.12, right=0.95, top=0.77, bottom=0.17)
    rng = np.random.default_rng(20260718)
    for idx, (column, label, color) in enumerate(specs):
        values = pd.to_numeric(rows.get(column), errors="coerce").dropna().to_numpy()
        jitter = rng.normal(0, 0.055, len(values))
        ax.scatter(values, np.full(len(values), idx) + jitter, s=32, color=color, alpha=0.72)
        if len(values):
            ax.scatter(np.median(values), idx, marker="|", s=260, color=INK, linewidth=2.2)
    ax.set_yticks(range(len(specs)), [item[1] for item in specs])
    ax.set_xlabel("Latest available year used per economy")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The composite combines different years and different policy eras",
        "Dots are economy-specific vintages; black ticks are medians. Safety-net observations reach back to 2000.",
    )
    source(
        fig,
        "Source: committed World Bank WDI source-readiness audit. Latest-year selection is per indicator and economy, not a balanced panel.",
    )
    save(fig, "sp-vintage-profile")


def poverty_dominance(diagnostics: pd.DataFrame) -> None:
    data = diagnostics.dropna(subset=["poverty_pct", "shock_payment_readiness_gap"]).copy()
    rho = data.poverty_pct.corr(data.shock_payment_readiness_gap, method="spearman")
    fig, ax = plt.subplots(figsize=(10.8, 7.2))
    fig.subplots_adjust(left=0.11, right=0.95, top=0.77, bottom=0.16)
    colors = np.where(data.legs_present == "both", BLUE, RED)
    ax.scatter(data.poverty_pct, data.shock_payment_readiness_gap, c=colors, s=64,
               alpha=0.84, edgecolor=WHITE, linewidth=0.8)
    for row in data.itertuples():
        if row.shock_payment_readiness_gap >= 2.5:
            ax.text(row.poverty_pct + 0.3, row.shock_payment_readiness_gap + 0.18,
                    row.iso3, fontsize=8.2, color=INK)
    ax.plot([0, max(data.poverty_pct) + 3], [0, max(data.poverty_pct) + 3], color=RULE, ls="--")
    ax.text(0.98, 0.08, f"Spearman poverty vs gap = {rho:+.2f}", transform=ax.transAxes,
            ha="right", fontsize=9, color=RED,
            bbox=dict(boxstyle="round,pad=.45", facecolor=WHITE, edgecolor=RULE))
    ax.set_xlabel("Poverty headcount at $3.00/day (2021 PPP), latest value (%)")
    ax.set_ylabel("Inherited readiness-gap value")
    ax.grid(color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "The index is largely a poverty transformation",
        "Red points have only one readiness leg; their apparent comparability is another artifact of the formula.",
    )
    source(
        fig,
        "Source: committed WDI/ASPIRE/Findex panel. The diagonal is equality, not a fitted model. Composite values are triage only.",
    )
    save(fig, "sp-poverty-dominance")


def thumbnail() -> None:
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    fig.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.10)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color=NAVY))
    ax.text(0.055, 0.82, "SOCIAL PROTECTION · CONSTRUCT VALIDATION", transform=ax.transAxes,
            color="#75D1F0", fontsize=10, weight="bold")
    ax.text(0.055, 0.62, "The ‘stable top five’\nwas fixed by a missing-data rule", transform=ax.transAxes,
            color=WHITE, fontsize=29, weight="bold", va="center")
    ax.text(0.055, 0.28, "Vanuatu and Tajikistan outrank two named members—\nbut disappear when the headline requires both proxy legs.",
            transform=ax.transAxes, color="#D8E7F0", fontsize=13, va="center")
    ax.add_patch(plt.Rectangle((0.72, 0.18), 0.21, 0.64, transform=ax.transAxes, color=WHITE, alpha=0.97))
    ax.text(0.825, 0.67, "3 / 5", transform=ax.transAxes, ha="center", color=RED, fontsize=34, weight="bold")
    ax.text(0.825, 0.53, "named members survive\nthe panel's own value rank", transform=ax.transAxes,
            ha="center", color=INK, fontsize=10)
    ax.plot([0.76, 0.89], [0.43, 0.43], transform=ax.transAxes, color=RULE, lw=1)
    ax.text(0.825, 0.31, "0", transform=ax.transAxes, ha="center", color=GOLD, fontsize=30, weight="bold")
    ax.text(0.825, 0.22, "comparable delivery\noutcomes joined", transform=ax.transAxes,
            ha="center", color=INK, fontsize=9)
    save(fig, "social-protection-shock-coverage-thumbnail", dpi=220)
    png = CHARTS / "social-protection-shock-coverage-thumbnail.png"
    svg = CHARTS / "social-protection-shock-coverage-thumbnail.svg"
    with Image.open(png) as image:
        width, height = image.size
    sidecar = {
        "program": "social-protection-shock-coverage",
        "title": "The stable top five was fixed by a missing-data rule",
        "caption": (
            "Only three named members survive the panel's own value order, and "
            "no comparable successful-receipt or delivery-time outcome is joined."
        ),
        "headline_number": "3 of 5 · 0 delivery outcomes",
        "visual_form": "construct-validation finding card",
        "source": "WDI/ASPIRE/Findex panel and World Bank COVID-19 SPJ response matrix v15",
        "inputs": [
            "generated/social-protection-dropped-leg.json",
            "generated/social-protection-covid-response-validation.json",
        ],
        "script": "social-protection-shock-coverage/scripts/build-figure-dossier.py",
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
    (CHARTS / "social-protection-shock-coverage-thumbnail.json").write_text(
        json.dumps(sidecar, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    validation = json.loads((GEN / "social-protection-covid-response-validation.json").read_text(encoding="utf-8"))
    dropped = json.loads((GEN / "social-protection-dropped-leg.json").read_text(encoding="utf-8"))
    readiness = json.loads((GEN / "social-protection-source-readiness.json").read_text(encoding="utf-8"))
    diagnostics = pd.read_csv(GEN / "social-protection-covid-response-diagnostics.csv")

    validity_gates(validation)
    membership_churn(dropped, readiness)
    dropped_leg_rank(dropped)
    response_heatmap(diagnostics)
    proxy_vs_response(diagnostics, validation)
    source_funnel(readiness, validation)
    vintage_profile(readiness)
    poverty_dominance(diagnostics)
    thumbnail()
    print("Built 8 article figures plus the program thumbnail.")


if __name__ == "__main__":
    main()
