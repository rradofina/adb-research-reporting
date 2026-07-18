"""Build the CPPI construct-validation figure spine.

attestation_chain: ai-first
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
CHARTS = GEN / "charts"
VALIDATION = GEN / "port-cppi-construct-validation.json"
COUNTRIES = GEN / "port-cppi-country-diagnostics.csv"
PORTS = GEN / "port-cppi-ports.csv"
SENSITIVITY = GEN / "port-cppi-sensitivity.csv"

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


def save(fig, stem: str) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHARTS / f"{stem}.png", dpi=200, bbox_inches="tight", facecolor=WHITE)
    fig.savefig(CHARTS / f"{stem}.svg", bbox_inches="tight", facecolor=WHITE)
    svg = CHARTS / f"{stem}.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def title(fig, main: str, sub: str) -> None:
    fig.suptitle(main, x=0.055, y=0.97, ha="left", fontsize=19, color=INK, weight="semibold")
    fig.text(0.055, 0.885, sub, fontsize=10.2, color=SOFT, ha="left")


def source(fig, text: str) -> None:
    fig.text(0.055, 0.025, text, fontsize=7, color=SOFT, ha="left")


def two_gate(summary: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.1))
    fig.subplots_adjust(left=0.055, right=0.95, top=0.74, bottom=0.17, wspace=0.18)
    cards = [
        (
            "GATE 1 · PORT TIME",
            "The inherited rank fails",
            "1 of 5",
            "main-specification overlap between\nthe trade/LPI screen and observed\nCPPI disadvantage",
            RED,
        ),
        (
            "GATE 2 · HINTERLAND",
            "The next object is not joined",
            "0 joined routes",
            "no port-to-inland origin-destination\ntime, cost, reliability, or network\nimpedance is estimated",
            GOLD,
        ),
    ]
    for ax, (kicker, heading, value, note, color) in zip(axes, cards):
        ax.set_facecolor(PALE)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.text(0.07, 0.86, kicker, transform=ax.transAxes, color=color, fontsize=9, weight="bold")
        ax.text(0.07, 0.69, heading, transform=ax.transAxes, color=INK, fontsize=14, weight="semibold")
        ax.text(0.07, 0.39, value, transform=ax.transAxes, color=color, fontsize=35, weight="bold")
        ax.text(0.07, 0.18, note, transform=ax.transAxes, color=SOFT, fontsize=10, wrap=True)
    title(
        fig,
        "A national trade screen is neither a port measure nor a hinterland measure",
        "Observed vessel time falsifies the first bridge; this package does not yet cross the second.",
    )
    source(
        fig,
        "Sources: World Bank CPPI 2020–2025 annex; committed imports × LPI panel. Country aggregates are diagnostics, not official rankings. attestation_chain: ai-first.",
    )
    save(fig, "port-two-gate-validation")


def rank_inversion(countries: pd.DataFrame) -> None:
    data = countries.sort_values("inherited_friction_rank")
    fig, ax = plt.subplots(figsize=(10.8, 8.2))
    fig.subplots_adjust(left=0.16, right=0.86, top=0.78, bottom=0.12)
    for _, row in data.iterrows():
        color = BLUE if row.inherited_top5 else RULE
        width = 2.4 if row.inherited_top5 else 1.2
        ax.plot(
            [0, 1],
            [row.inherited_friction_rank, row.observed_disadvantage_rank],
            color=color,
            lw=width,
            alpha=0.9,
            zorder=1,
        )
        ax.scatter([0, 1], [row.inherited_friction_rank, row.observed_disadvantage_rank], color=color, s=34, zorder=2)
        ax.text(-0.035, row.inherited_friction_rank, row.iso3, ha="right", va="center", fontsize=8.5, color=INK)
        ax.text(1.035, row.observed_disadvantage_rank, row.iso3, ha="left", va="center", fontsize=8.5, color=INK)
    ax.set_xlim(-0.20, 1.20)
    ax.set_ylim(13.8, 0.2)
    ax.set_xticks([0, 1], ["Inherited imports × LPI rank", "Observed CPPI disadvantage rank"])
    ax.set_yticks(range(1, 14))
    ax.grid(axis="y", color=RULE, lw=0.7)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "China falls from first to twelfth; India from second to tenth",
        "Only Indonesia remains in the top five when the construct changes from trade scale and perception to observed vessel time.",
    )
    source(
        fig,
        "Main diagnostic: 2025 median CPPI across ports with at least 48 sampled calls; lower CPPI means greater observed port-time disadvantage. N=13 matched DMCs.",
    )
    save(fig, "port-rank-inversion")


def proxy_scatter(countries: pd.DataFrame, validation: dict) -> None:
    data = countries.dropna(subset=["friction_exposure_index", "call_weighted_cppi"]).copy()
    fig, ax = plt.subplots(figsize=(10.8, 7.2))
    fig.subplots_adjust(left=0.11, right=0.95, top=0.78, bottom=0.17)
    colors = np.where(data.inherited_top5, BLUE, SOFT)
    sizes = np.clip(np.sqrt(data.calls_2025) * 5, 45, 230)
    ax.scatter(
        data.friction_exposure_index,
        data.call_weighted_cppi,
        s=sizes,
        c=colors,
        alpha=0.86,
        edgecolor=WHITE,
        linewidth=0.8,
    )
    fit = np.polyfit(data.friction_exposure_index, data.call_weighted_cppi, 1)
    xs = np.linspace(data.friction_exposure_index.min(), data.friction_exposure_index.max(), 100)
    ax.plot(xs, fit[0] * xs + fit[1], color=RED, lw=1.6, ls="--")
    for _, row in data.iterrows():
        dx, dy = 0.015, 2.2
        if row.iso3 == "CHN":
            dx, dy = -0.08, 4
        if row.iso3 == "HKG":
            dx, dy = 0.015, -7
        if row.iso3 == "BGD":
            dx, dy = 0.015, -7
        ax.text(row.friction_exposure_index + dx, row.call_weighted_cppi + dy, row.iso3, fontsize=8, color=INK)
    ax.axhline(0, color=RULE, lw=1)
    ax.grid(color=RULE, lw=0.7)
    ax.set_xlabel("Inherited friction-exposure index (higher was labeled worse)")
    ax.set_ylabel("2025 call-weighted CPPI (higher observed performance)")
    for spine in ax.spines.values():
        spine.set_visible(False)
    corr = next(
        row
        for row in validation["summary"]["correlations"]
        if row["direct_metric"] == "call_weighted_cppi"
    )
    ax.text(
        0.02,
        0.96,
        f"Spearman with observed disadvantage = {corr['spearman_with_observed_disadvantage']:+.2f}\n95% bootstrap interval {corr['bootstrap_ci95'][0]:+.2f} to {corr['bootstrap_ci95'][1]:+.2f}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color=RED,
        bbox=dict(boxstyle="round,pad=.5", facecolor=WHITE, edgecolor=RULE),
    )
    title(
        fig,
        "The proxy rises as observed port performance improves",
        "Bubble area reflects sampled 2025 port calls. The statistically clearest association points opposite the inherited interpretation.",
    )
    source(
        fig,
        "Source: World Bank CPPI 2025 and committed imports × LPI panel. Call-weighted country values are diagnostics constructed here; CPPI remains port-level.",
    )
    save(fig, "port-proxy-vs-cppi")


def distributions(ports: pd.DataFrame, countries: pd.DataFrame) -> None:
    eligible = ports.loc[
        ports.iso3.isin(countries.iso3)
        & ports.cppi_2025.notna()
        & (ports.calls_2025 >= 48)
    ].copy()
    order = countries.sort_values("median_cppi").iso3.tolist()
    fig, ax = plt.subplots(figsize=(11.2, 8.0))
    fig.subplots_adjust(left=0.11, right=0.95, top=0.78, bottom=0.14)
    rng = np.random.default_rng(20260718)
    for y, iso3 in enumerate(order):
        values = eligible.loc[eligible.iso3 == iso3, "cppi_2025"].to_numpy()
        ax.hlines(y, values.min(), values.max(), color=RULE, lw=3, zorder=1)
        ax.scatter(values, np.full(len(values), y) + rng.normal(0, 0.055, len(values)), color=BLUE, s=30, alpha=0.82, zorder=2)
        median = float(np.median(values))
        ax.scatter(median, y, marker="|", s=210, color=RED, linewidth=2.2, zorder=3)
    ax.axvline(0, color=INK, lw=1)
    ax.set_yticks(range(len(order)), order)
    ax.set_xlabel("2025 CPPI score (positive = above the 2024 reference distribution)")
    ax.grid(axis="x", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "A country label hides large differences among its ports",
        "Each dot is a port; red ticks are country medians. China spans both the best and one of the weakest observed scores.",
    )
    source(
        fig,
        "Source: World Bank CPPI 2025. Ports shown have at least 48 sampled calls. CPPI measures vessel time inside the port boundary, not hinterland performance.",
    )
    save(fig, "port-cppi-distributions")


def sensitivity_matrix(sensitivity: pd.DataFrame) -> None:
    columns = [(year, calls) for year in (2024, 2025) for calls in (0, 24, 48, 72)]
    rows = ["median_cppi", "q25_cppi", "call_weighted_cppi"]
    matrix = np.full((len(rows), len(columns)), np.nan)
    for i, aggregation in enumerate(rows):
        for j, (year, calls) in enumerate(columns):
            found = sensitivity.loc[
                (sensitivity.year == year)
                & (sensitivity.min_calls == calls)
                & (sensitivity.aggregation == aggregation)
            ]
            if not found.empty:
                matrix[i, j] = found.iloc[0].overlap_with_inherited_top5
    fig, ax = plt.subplots(figsize=(11.3, 5.8))
    fig.subplots_adjust(left=0.18, right=0.91, top=0.72, bottom=0.22)
    masked = np.ma.masked_invalid(matrix)
    image = ax.imshow(masked, vmin=0, vmax=5, cmap="Blues", aspect="auto")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if np.isnan(matrix[i, j]):
                ax.text(j, i, "—", ha="center", va="center", color=SOFT)
            else:
                ax.text(j, i, f"{int(matrix[i, j])}/5", ha="center", va="center", color=INK, weight="semibold")
    labels = [f"{year}\n{'all' if calls == 0 else f'≥{calls} calls'}" for year, calls in columns]
    ax.set_xticks(range(len(columns)), labels)
    ax.set_yticks(range(len(rows)), ["Country median", "Lower quartile", "Call-weighted mean"])
    ax.tick_params(length=0)
    cbar = fig.colorbar(image, ax=ax, shrink=0.72)
    cbar.set_label("Members retained from inherited top five")
    title(
        fig,
        "No defensible specification recovers more than two of five",
        "The old cluster is not restored by changing vintage, the ±50% call threshold, or the country aggregation rule.",
    )
    source(
        fig,
        "Source: port-cppi-sensitivity.csv. The numeric threshold is centered at 48 sampled calls and tested at 24 and 72 (±50%); 'all' retains every scored CPPI port.",
    )
    save(fig, "port-cppi-sensitivity")


def source_funnel(summary: dict) -> None:
    labels = [
        "Global ports\nin annex",
        "ADB DMC ports\nwith 2025 score",
        "Main-spec ports\n≥48 calls",
        "ADB DMCs\nrepresented",
        "Matched DMCs\nwith old screen",
        "Hinterland OD\nmetrics",
    ]
    values = [
        summary["source_port_rows"],
        summary["adb_dmc_port_rows_with_2025_score"],
        summary["common_ports_main_spec"],
        summary["adb_dmcs_with_2025_score"],
        summary["common_rankable_dmcs_main_spec"],
        0,
    ]
    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    fig.subplots_adjust(left=0.06, right=0.96, top=0.74, bottom=0.20)
    x = np.arange(len(values))
    colors = [NAVY, BLUE, BLUE, GREEN, GREEN, RED]
    ax.bar(x, values, color=colors, width=0.65)
    for i, value in enumerate(values):
        ax.text(i, value + max(values) * 0.025, str(value), ha="center", va="bottom", fontsize=12, weight="bold", color=INK)
    ax.set_xticks(x, labels)
    ax.set_yscale("symlog", linthresh=1)
    ax.set_ylim(0, 800)
    ax.grid(axis="y", color=RULE, lw=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    title(
        fig,
        "Port data are now visible; the hinterland remains unobserved",
        "The source upgrade replaces perception with 65 observed ports in the main test, then stops honestly at the port boundary.",
    )
    source(
        fig,
        "Source: World Bank CPPI 2020–2025 annex and committed ADB DMC screen. Log-like vertical scale used only to display counts of different orders of magnitude.",
    )
    save(fig, "port-source-alignment-funnel")


def time_series(ports: pd.DataFrame) -> None:
    selected = ["CHN", "IND", "IDN", "VNM", "THA", "BGD", "GEO", "PHL"]
    years = range(2020, 2026)
    rows = []
    for iso3 in selected:
        group = ports.loc[ports.iso3 == iso3]
        for year in years:
            values = group[f"cppi_{year}"].dropna()
            if len(values):
                rows.append({"iso3": iso3, "year": year, "median": float(values.median())})
    data = pd.DataFrame(rows)
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.6), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.95, top=0.72, bottom=0.16, wspace=0.14)
    groups = [(["CHN", "IND", "IDN", "VNM", "THA"], "Inherited top five"), (["BGD", "GEO", "PHL"], "Direct-signal contrasts")]
    palette = [BLUE, NAVY, GREEN, GOLD, RED, RED, GOLD, SOFT]
    color_map = dict(zip(selected, palette))
    for ax, (members, heading) in zip(axes, groups):
        for iso3 in members:
            group = data.loc[data.iso3 == iso3].sort_values("year")
            ax.plot(group.year, group["median"], marker="o", lw=1.8, color=color_map[iso3], label=iso3)
        ax.axhline(0, color=RULE, lw=1)
        ax.set_title(heading, loc="left", color=INK, fontsize=12, weight="semibold")
        ax.set_xticks(list(years))
        ax.grid(color=RULE, lw=0.7)
        ax.legend(frameon=False, ncol=2, fontsize=8, loc="best")
        for spine in ax.spines.values():
            spine.set_visible(False)
    axes[0].set_ylabel("Median standardized CPPI across observed ports")
    title(
        fig,
        "The disagreement is not a one-year snapshot",
        "The standardized CPPI time series shows persistent separation between the trade-scale cluster and economies with weaker observed port-time scores.",
    )
    source(
        fig,
        "Source: World Bank standardized CPPI 2020–2025 series, rebased to the 2024 reference distribution. Country medians are diagnostics constructed here.",
    )
    save(fig, "port-cppi-time-series")


def main() -> None:
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    countries = pd.read_csv(COUNTRIES)
    ports = pd.read_csv(PORTS)
    sensitivity = pd.read_csv(SENSITIVITY)
    two_gate(validation["summary"])
    rank_inversion(countries)
    proxy_scatter(countries, validation)
    distributions(ports, countries)
    sensitivity_matrix(sensitivity)
    source_funnel(validation["summary"])
    time_series(ports)
    figures = [
        "port-two-gate-validation",
        "port-rank-inversion",
        "port-proxy-vs-cppi",
        "port-cppi-distributions",
        "port-cppi-sensitivity",
        "port-source-alignment-funnel",
        "port-cppi-time-series",
    ]
    (GEN / "port-figure-dossier-summary.json").write_text(
        json.dumps(
            {
                "program": "port-hinterland-friction",
                "attestation_chain": "ai-first",
                "figure_count": len(figures),
                "figures": figures,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
