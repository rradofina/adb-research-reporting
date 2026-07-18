"""Build the access-services figure dossier from committed generated evidence.

The figures test whether OSM facility-count ratios can support an access
ranking. They do not fetch data and they do not estimate travel time, service
capacity, utilization, or welfare.

Outputs:
  generated/charts/access-phl-rank-shift.{png,svg}
  generated/charts/access-phl-completeness-signal.{png,svg}
  generated/charts/access-cross-economy-registry-readiness.{png,svg}
  generated/charts/access-cambodia-source-disagreement.{png,svg}
  generated/access-figure-dossier-summary.json
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEEPENING_PATH = ROOT / "generated" / "access-osm-completeness-deepening.json"
CAMBODIA_PATH = ROOT / "generated" / "access-cambodia-health-facility-source-audit.json"
CHARTS = ROOT / "generated" / "charts"
SUMMARY_PATH = ROOT / "generated" / "access-figure-dossier-summary.json"

ADB_BLUE = "#007DB8"
ADB_NAVY = "#002569"
ADB_GOLD = "#B07D12"
ADB_RED = "#A63D40"
INK = "#212529"
INK_SOFT = "#59636D"
RULE = "#D9DEE2"
PALE = "#EEF2F4"
RESHAPE_THRESHOLDS = [0.25, 0.50, 0.75]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_figure(fig: plt.Figure, stem: str) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    png_path = CHARTS / f"{stem}.png"
    svg_path = CHARTS / f"{stem}.svg"
    fig.savefig(png_path, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def clean_axes(ax: plt.Axes, axis: str = "x") -> None:
    ax.grid(axis=axis, color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)


def add_source(fig: plt.Figure, text: str) -> None:
    fig.text(0.06, 0.025, text, ha="left", va="bottom", fontsize=7.1, color=INK_SOFT, wrap=True)


def render_phl_rank_shift(rows: list[dict]) -> None:
    ordered = sorted(rows, key=lambda row: row["rank_shift"])
    labels = [row["admin1_name"] for row in ordered]
    shifts = [row["rank_shift"] for row in ordered]
    colors = [ADB_RED if shift < 0 else ADB_BLUE if shift > 0 else INK_SOFT for shift in shifts]
    y = np.arange(len(ordered))

    fig, ax = plt.subplots(figsize=(12.0, 8.2))
    fig.subplots_adjust(left=0.25, right=0.92, top=0.79, bottom=0.13)
    ax.barh(y, shifts, color=colors, height=0.58, alpha=0.9)
    ax.axvline(0, color=INK, linewidth=1.0)
    for pos, row in zip(y, ordered, strict=True):
        shift = row["rank_shift"]
        x = shift + (0.35 if shift >= 0 else -0.35)
        ax.text(
            x,
            pos,
            f"{row['rank_osm']} → {row['rank_registry']}",
            va="center",
            ha="left" if shift >= 0 else "right",
            fontsize=8.6,
            color=INK,
        )

    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", length=0, labelsize=9.4)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.set_xlabel("Rank movement after replacing OSM counts with the official clinical registry", color=INK_SOFT)
    ax.set_xlim(-11, 16)
    clean_axes(ax)
    fig.suptitle(
        "Official registry counts reorder 16 of 17 Philippine regional ranks",
        x=0.06, y=0.965, ha="left", fontsize=17, color=INK, weight="semibold",
    )
    fig.text(
        0.06,
        0.895,
        "Labels show OSM-based rank → registry-based rank. Positive bars move toward a worse registry load rank; negative bars move away.",
        ha="left", fontsize=10.2, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed access-osm-completeness-deepening.json; PSA 2020 population and DOH NHFR v2.0/OSM facility counts retrieved in 2026. Ranks describe people per mapped or registered clinical point, not travel-time access. attestation_chain: ai-first.",
    )
    save_figure(fig, "access-phl-rank-shift")


def render_phl_completeness_signal(rows: list[dict], stats: dict) -> None:
    x = np.array([float(row["capture_ratio"]) for row in rows])
    y = np.array([float(row["osm_people_per_facility"]) for row in rows])
    sizes = np.array([max(float(row["population_2020"]), 1) for row in rows])
    sizes = 45 + 230 * np.sqrt(sizes / sizes.max())

    fig, ax = plt.subplots(figsize=(11.5, 6.6))
    fig.subplots_adjust(left=0.12, right=0.94, top=0.78, bottom=0.18)
    ax.scatter(x, y, s=sizes, color=ADB_BLUE, alpha=0.72, edgecolor="white", linewidth=0.8)
    for row in rows:
        if row["admin1_name"] in {"ARMM", "NCR", "Central Luzon", "Calabarzon", "Cagayan Valley"}:
            ax.annotate(
                row["admin1_name"],
                (row["capture_ratio"], row["osm_people_per_facility"]),
                xytext=(5, 6), textcoords="offset points", fontsize=8.7, color=INK,
            )

    ax.set_yscale("log")
    ax.set_xlim(0, 0.69)
    ax.set_xlabel("OSM clinical points as a share of official registry points", color=INK_SOFT)
    ax.set_ylabel("People per OSM-tagged health point (log scale)", color=INK_SOFT)
    ax.tick_params(colors=INK_SOFT)
    clean_axes(ax, "both")
    fig.suptitle(
        "Sparse OSM capture is associated with worse apparent facility load",
        x=0.06, y=0.965, ha="left", fontsize=17, color=INK, weight="semibold",
    )
    fig.text(
        0.06,
        0.89,
        f"Across 17 Philippine regions, Spearman ρ = {stats['spearman_rho']:.2f}; the log–log relationship explains {stats['pearson_r2_loglog']:.0%} of variation.",
        ha="left", fontsize=10.3, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed access-osm-completeness-deepening.json. Bubble area scales with 2020 population. The association diagnoses denominator sensitivity; it is not causal evidence and does not measure facility quality, capacity, utilization, or travel time. attestation_chain: ai-first.",
    )
    save_figure(fig, "access-phl-completeness-signal")


def render_cross_economy_readiness(rows: list[dict]) -> None:
    ordered = sorted(rows, key=lambda row: row["osm_worst_people_per_facility"])
    y = np.arange(len(ordered))
    osm = [row["osm_worst_people_per_facility"] for row in ordered]
    corrected = [row["corrected_people_per_facility"] or 0 for row in ordered]

    fig, ax = plt.subplots(figsize=(11.8, 6.5))
    fig.subplots_adjust(left=0.24, right=0.94, top=0.76, bottom=0.19)
    ax.barh(y, osm, color=PALE, edgecolor=ADB_BLUE, linewidth=1.2, height=0.62, label="OSM-based worst ADM1 load")
    ax.barh(y, corrected, color=ADB_GOLD, height=0.36, label="Registry-adjusted load available")
    for pos, row in zip(y, ordered, strict=True):
        if row["corrected_people_per_facility"] is None:
            ax.text(row["osm_worst_people_per_facility"] + 6500, pos, "no registry join", va="center", fontsize=8.8, color=INK_SOFT)
        else:
            ax.text(
                row["corrected_people_per_facility"] + 3500,
                pos,
                f"{row['corrected_people_per_facility']:,}",
                va="center", fontsize=8.7, color=INK,
            )

    ax.set_yticks(y, [row["country"] for row in ordered])
    ax.tick_params(axis="y", length=0, labelsize=9.5)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.set_xlabel("People per facility in the economy's worst OSM-screened ADM1", color=INK_SOFT)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    clean_axes(ax)
    fig.suptitle(
        "Only 2 of 8 pilot economies have a comparable registry correction",
        x=0.06, y=0.965, ha="left", fontsize=17, color=INK, weight="semibold",
    )
    fig.text(
        0.06,
        0.885,
        "The OSM screen can identify where source validation is urgent; it cannot support a common eight-economy access ranking.",
        ha="left", fontsize=10.3, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed access-osm-completeness-deepening.json. Philippine and Bangladesh corrections use national clinical capture rates only for this cross-economy diagnostic; the ADM1 analysis uses regional registry counts. Missing bars mean no comparable registry join, not zero facilities. attestation_chain: ai-first.",
    )
    save_figure(fig, "access-cross-economy-registry-readiness")


def render_cambodia_disagreement(summary: dict) -> None:
    rows = list(reversed(summary["largest_osm_load_ratios"]))
    y = np.arange(len(rows))
    osm = [row["osm_people_per_health_facility"] for row in rows]
    government = [row["government_people_per_facility_2010"] for row in rows]

    fig, ax = plt.subplots(figsize=(11.8, 6.8))
    fig.subplots_adjust(left=0.23, right=0.94, top=0.76, bottom=0.20)
    height = 0.32
    ax.barh(y + height / 2, osm, height=height, color=ADB_BLUE, label="2026 OSM screen")
    ax.barh(y - height / 2, government, height=height, color=ADB_GOLD, label="2010 public-facility inventory")
    for pos, row in zip(y, rows, strict=True):
        ax.text(
            row["osm_people_per_health_facility"] * 1.04,
            pos + height / 2,
            f"{row['osm_load_to_government_load_ratio']:.1f}×",
            va="center", fontsize=8.8, color=INK, weight="semibold",
        )

    ax.set_xscale("log")
    ax.set_yticks(y, [row["admin1_name"] for row in rows])
    ax.tick_params(axis="y", length=0, labelsize=9.3)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.set_xlabel("People per counted health-facility point (log scale)", color=INK_SOFT)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    clean_axes(ax)
    fig.suptitle(
        "Cambodia's two public sources imply 5–20× different provincial loads",
        x=0.06, y=0.965, ha="left", fontsize=17, color=INK, weight="semibold",
    )
    fig.text(
        0.06,
        0.885,
        "Eight largest ratios among 24 joined provinces. The mismatch is evidence of source disagreement, not a current completeness rate.",
        ha="left", fontsize=10.3, color=INK_SOFT,
    )
    add_source(
        fig,
        "Source: committed access-cambodia-health-facility-source-audit.json. HDX/MoH/OCHA public facilities are from 2010; OSM is from 2026 and can include different provider types. Phnom Penh reverses the count relationship, reinforcing the scope/vintage warning. attestation_chain: ai-first.",
    )
    save_figure(fig, "access-cambodia-source-disagreement")


def main() -> None:
    deepening = load_json(DEEPENING_PATH)
    cambodia = load_json(CAMBODIA_PATH)

    render_phl_rank_shift(deepening["phl_rows"])
    render_phl_completeness_signal(deepening["phl_rows"], deepening["phl_internal_contradiction"])
    render_cross_economy_readiness(deepening["cluster_worst_adm1_corrected"])
    render_cambodia_disagreement(cambodia["summary"])

    changed = {
        "PHL": {
            "changed": int(deepening["phl_correction"]["n_adm1_rank_changed"]),
            "total": int(deepening["phl_correction"]["n_adm1_total"]),
        },
        "BGD": {
            "changed": sum(row["rank_osm"] != row["rank_registry"] for row in deepening["bgd_rows"]),
            "total": len(deepening["bgd_rows"]),
        },
        "KHM": {
            "changed": int(cambodia["summary"]["rank_changed_after_2010_inventory"]),
            "total": int(cambodia["summary"]["rank_joined_total"]),
        },
    }
    for values in changed.values():
        values["share"] = round(values["changed"] / values["total"], 4)
        values["threshold_results"] = {
            f"{threshold:.2f}": values["changed"] / values["total"] >= threshold
            for threshold in RESHAPE_THRESHOLDS
        }

    summary = {
        "program": "access-services",
        "attestation_chain": "ai-first",
        "source_inputs": [
            str(DEEPENING_PATH.relative_to(ROOT)),
            str(CAMBODIA_PATH.relative_to(ROOT)),
        ],
        "claim_reshape_thresholds": RESHAPE_THRESHOLDS,
        "rank_change_sensitivity": changed,
        "identity_check": deepening["identity_check"],
        "phl_completeness_relationship": deepening["phl_internal_contradiction"],
        "registry_join_readiness": {
            "pilot_economies": len(deepening["cluster_worst_adm1_corrected"]),
            "comparable_registry_corrections": sum(
                row["corrected_people_per_facility"] is not None
                for row in deepening["cluster_worst_adm1_corrected"]
            ),
        },
        "finding": (
            "Official clinical registry counts reorder 16 of 17 Philippine regional load ranks. "
            "The OSM denominator is therefore suitable for map-observability triage, not a service-access ranking."
        ),
        "supporting_source_disagreement": (
            "Bangladesh registry counts reorder 6 of 8 divisions. Cambodia's 2010 public-facility inventory "
            "reorders 21 of 24 joined provinces, but its source-vintage and provider-scope mismatch prevents "
            "interpretation as current completeness or access validation."
        ),
        "non_claim": (
            "The dossier does not measure travel time, service capacity, utilization, quality, affordability, "
            "household access, or welfare."
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {SUMMARY_PATH.relative_to(ROOT)} and four chart pairs")


if __name__ == "__main__":
    main()
