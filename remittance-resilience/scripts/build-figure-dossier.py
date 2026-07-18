"""Build the remittance-resilience coverage figure from committed L3 output.

This script does not fetch or recompute corridor prices or bilateral flows. It
reads the formal flow-weighting module output and makes the headline top-five
coverage caveat visible.

Outputs:
  generated/charts/remittance-flow-coverage-top5.{png,svg}
  generated/remittance-figure-dossier-summary.json
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "generated" / "remittance-flow-weighting-sprint.json"
CHARTS = ROOT / "generated" / "charts"
SUMMARY_PATH = ROOT / "generated" / "remittance-figure-dossier-summary.json"

ADB_BLUE = "#007DB8"
ADB_NAVY = "#002569"
ADB_GOLD = "#B07D12"
INK = "#212529"
INK_SOFT = "#59636D"
RULE = "#D9DEE2"
LOW_COVERAGE_THRESHOLD = 0.25


def load_source() -> dict:
    with SOURCE_PATH.open("r", encoding="utf-8") as handle:
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


def top_five_coverage(source: dict) -> list[dict]:
    baseline = source["ranking_test"]["repaired_program_baseline_top5"]
    ledger = {
        row["iso3"]: row
        for row in source["evidence_confidence"]["confidence_ledger"]
    }
    missing = [iso3 for iso3 in baseline if iso3 not in ledger]
    if missing:
        raise ValueError(f"Missing baseline top-five rows in confidence ledger: {missing}")
    rows = []
    for iso3 in baseline:
        row = ledger[iso3]
        rows.append(
            {
                "iso3": iso3,
                "country": row["country"],
                "flow_coverage_share": float(row["flow_coverage_share"]),
                "matched_rpw_corridors": int(row["matched_rpw_corridors"]),
                "rpw_corridors_observed": int(row["rpw_corridors_observed"]),
                "low_coverage_flag": bool(row["low_matched_flow_coverage_flag"]),
                "evidence_confidence_label": row["evidence_confidence_label"],
            }
        )
    return sorted(rows, key=lambda item: item["flow_coverage_share"])


def render_coverage(rows: list[dict]) -> None:
    countries = [row["country"] for row in rows]
    shares = [row["flow_coverage_share"] for row in rows]
    colors = [ADB_GOLD if row["low_coverage_flag"] else ADB_BLUE for row in rows]

    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    fig.subplots_adjust(left=0.25, right=0.95, top=0.75, bottom=0.22)
    y_positions = range(len(rows))
    ax.barh(y_positions, shares, color=colors, height=0.55, alpha=0.9)
    ax.axvline(
        LOW_COVERAGE_THRESHOLD,
        color=ADB_GOLD,
        linewidth=1.8,
        linestyle=(0, (5, 4)),
    )
    ax.text(
        LOW_COVERAGE_THRESHOLD,
        len(rows) - 0.25,
        "25% low-coverage warning",
        color=ADB_GOLD,
        fontsize=9.5,
        weight="semibold",
        ha="left",
        va="bottom",
    )

    for y, row in zip(y_positions, rows, strict=True):
        share = row["flow_coverage_share"]
        ax.text(
            min(share + 0.018, 0.94),
            y,
            f"{share:.1%}  ·  {row['matched_rpw_corridors']} of {row['rpw_corridors_observed']} priced corridors matched",
            va="center",
            ha="left",
            fontsize=10,
            color=INK,
            weight="semibold" if row["low_coverage_flag"] else "normal",
        )

    ax.set_xlim(0, 1)
    ax.set_yticks(list(y_positions), countries)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
    ax.tick_params(axis="y", length=0, labelsize=10.5)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.grid(axis="x", color=RULE, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle(
        "Kyrgyz Republic's priced corridor covers only 13.8% of estimated inbound flow",
        x=0.06,
        y=0.95,
        ha="left",
        fontsize=17,
        color=INK,
        weight="semibold",
    )
    fig.text(
        0.06,
        0.85,
        "Matched RPW Q1 2025 corridors as a share of KNOMAD 2021 inbound-flow estimates, repaired baseline top five.",
        ha="left",
        fontsize=10.5,
        color=INK_SOFT,
    )
    fig.text(
        0.06,
        0.055,
        "Source: committed generated/remittance-flow-weighting-sprint.json. The flow matrix predates the price data by four years and is not household transaction microdata. attestation_chain: ai-first.",
        ha="left",
        va="bottom",
        fontsize=7.2,
        color=INK_SOFT,
        wrap=True,
    )
    save_figure(fig, "remittance-flow-coverage-top5")


def main() -> None:
    source = load_source()
    rows = top_five_coverage(source)
    render_coverage(rows)
    summary = {
        "program": "remittance-resilience",
        "attestation_chain": "ai-first",
        "source_input": str(SOURCE_PATH.relative_to(ROOT)),
        "low_coverage_threshold": LOW_COVERAGE_THRESHOLD,
        "baseline_top_five_coverage": rows,
        "finding": (
            "Four repaired baseline top-five economies clear the module's 25 percent warning threshold; "
            "Kyrgyz Republic does not, with one matched corridor covering 13.75 percent of estimated inbound flow."
        ),
        "non_claim": (
            "Matched-flow coverage is a source-support diagnostic. It is not household exposure, transaction coverage, "
            "corridor validation, or a country-performance measure."
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
