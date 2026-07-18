"""Build the non-map figures in the PSDQ research figure spine.

The script reads only committed JSON outputs. It does not fetch data, repair
records, or create a new substantive metric. The sensitivity range is computed
from completed pre-registered runs. The validation-path figure reports the
committed evidence-ledger counts and makes the zero-closure wall visible.

Outputs:
  generated/charts/psdq-sensitivity-range.{png,svg}
  generated/charts/psdq-validation-wall.{png,svg}
  generated/psdq-figure-dossier-summary.json
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
CHARTS = ROOT / "generated" / "charts"
SENSITIVITY_PATH = ROOT / "sensitivity-runs.json"
LEDGER_PATH = ROOT / "generated" / "evidence-ledger.json"
SUMMARY_PATH = ROOT / "generated" / "psdq-figure-dossier-summary.json"

ADB_BLUE = "#007DB8"
ADB_NAVY = "#002569"
ADB_GREEN = "#5A8227"
ADB_GOLD = "#B07D12"
INK = "#212529"
INK_SOFT = "#59636D"
RULE = "#D9DEE2"
PAPER_DEEP = "#F4F5F6"
PLANNING_SCREEN = 0.30

SENSITIVITY_FOOTER = (
    "Source: committed sensitivity-runs.json. Ratios compare OSM clinical-tier features with public registry counts; "
    "neither source is ground truth. The offline polygon-dilation test remains incomplete. attestation_chain: ai-first."
)

VALIDATION_FOOTER = (
    "Source: committed generated/evidence-ledger.json. Public-source review is not human validation and does not authorize "
    "row closure, same-facility reclassification, or coordinate correction. attestation_chain: ai-first."
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_figure(fig: plt.Figure, stem: str) -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    png_path = CHARTS / f"{stem}.png"
    svg_path = CHARTS / f"{stem}.svg"
    fig.savefig(png_path, dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    # Matplotlib emits trailing spaces in multiline SVG path definitions.
    # Normalize them so generated vector artifacts pass repository hygiene and
    # remain stable across syncs.
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


def completed_ratios(runs: list[dict]) -> list[float]:
    values = [
        float(run["country_clinical_ratio"])
        for run in runs
        if run.get("country_clinical_ratio") is not None
    ]
    if not values:
        raise ValueError("No completed country_clinical_ratio values found")
    return values


def render_sensitivity(sensitivity: dict) -> dict:
    phl_values = completed_ratios(sensitivity["runs"])
    bgd_values = completed_ratios(sensitivity["bgd_runs"])
    rows = [
        {
            "country": "Philippines",
            "baseline": float(sensitivity["baseline_value"]),
            "minimum": min(phl_values),
            "maximum": max(phl_values),
            "completed_runs": len(phl_values),
        },
        {
            "country": "Bangladesh",
            "baseline": float(sensitivity["bgd_baseline_value"]),
            "minimum": min(bgd_values),
            "maximum": max(bgd_values),
            "completed_runs": len(bgd_values),
        },
    ]

    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    fig.subplots_adjust(left=0.18, right=0.96, top=0.74, bottom=0.25)
    ax.set_xlim(0, 0.34)
    ax.set_ylim(-0.65, 1.65)
    ax.axvline(PLANNING_SCREEN, color=ADB_GOLD, linewidth=2, linestyle=(0, (5, 4)))
    ax.text(
        PLANNING_SCREEN,
        1.48,
        "30% fit-for-planning screen",
        ha="center",
        va="bottom",
        fontsize=10,
        color=ADB_GOLD,
        weight="semibold",
    )

    colors = [ADB_BLUE, ADB_GREEN]
    for y, row, color in zip([1, 0], rows, colors, strict=True):
        ax.hlines(y, row["minimum"], row["maximum"], color=color, linewidth=12, alpha=0.3)
        ax.scatter(row["baseline"], y, s=120, color=color, edgecolor="white", linewidth=1.5, zorder=3)
        ax.text(
            row["maximum"] + 0.006,
            y,
            f"{row['minimum']:.1%}–{row['maximum']:.1%}",
            ha="left",
            va="center",
            fontsize=11,
            color=INK,
            weight="semibold",
        )
        ax.text(
            row["baseline"],
            y - 0.25,
            f"baseline {row['baseline']:.1%}",
            ha="center",
            va="top",
            fontsize=9,
            color=INK_SOFT,
        )

    ax.set_yticks([1, 0], [row["country"] for row in rows])
    ax.set_xticks([0, 0.1, 0.2, 0.3], ["0%", "10%", "20%", "30%"])
    ax.tick_params(axis="y", length=0, labelsize=11)
    ax.tick_params(axis="x", colors=INK_SOFT)
    ax.grid(axis="x", color=RULE, linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle(
        "Both pilots remain below the planning screen across tested definitions",
        x=0.06,
        y=0.94,
        ha="left",
        fontsize=17,
        color=INK,
        weight="semibold",
    )
    fig.text(
        0.06,
        0.84,
        "Country clinical-tier OSM-to-registry ratio; bars span every completed sensitivity run and dots mark the baseline.",
        ha="left",
        fontsize=10.5,
        color=INK_SOFT,
    )
    fig.text(0.06, 0.05, SENSITIVITY_FOOTER, ha="left", va="bottom", fontsize=7.2, color=INK_SOFT, wrap=True)
    save_figure(fig, "psdq-sensitivity-range")
    return {"planning_screen": PLANNING_SCREEN, "countries": rows}


def render_validation_wall(ledger: dict) -> dict:
    counts = ledger["headline_counts"]
    stages = [
        {
            "value": int(counts["targeted_public_source_rows"]),
            "label": "Targeted public-\nsource rows",
            "note": "Evidence gathered and organized",
            "color": ADB_BLUE,
        },
        {
            "value": int(counts["human_or_source_owner_wall_rows"]),
            "label": "Human/source-\nowner wall",
            "note": "Identity or location still unresolved",
            "color": ADB_GOLD,
        },
        {
            "value": int(counts["ai_actionable_without_human_or_source_owner_rows"]),
            "label": "AI-actionable\nclosures",
            "note": "No row may be closed or reclassified",
            "color": ADB_NAVY,
        },
    ]

    fig, ax = plt.subplots(figsize=(11.5, 5.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    positions = [0.04, 0.365, 0.69]
    box_width = 0.27
    for index, (x, stage) in enumerate(zip(positions, stages, strict=True)):
        box = FancyBboxPatch(
            (x, 0.27),
            box_width,
            0.42,
            boxstyle="round,pad=0.012,rounding_size=0.012",
            linewidth=1.2,
            edgecolor=stage["color"],
            facecolor=PAPER_DEEP,
        )
        ax.add_patch(box)
        ax.text(x + 0.025, 0.58, f"{stage['value']:,}", fontsize=30, weight="bold", color=stage["color"])
        ax.text(x + 0.025, 0.49, stage["label"], fontsize=11, weight="semibold", color=INK, va="top")
        ax.text(x + 0.025, 0.34, stage["note"], fontsize=9.2, color=INK_SOFT, wrap=True)
        if index < len(stages) - 1:
            ax.add_patch(
                FancyArrowPatch(
                    (x + box_width + 0.012, 0.48),
                    (positions[index + 1] - 0.012, 0.48),
                    arrowstyle="-|>",
                    mutation_scale=14,
                    linewidth=1.2,
                    color=INK_SOFT,
                )
            )

    fig.suptitle(
        "Public-source review reaches a validation wall, not row closure",
        x=0.055,
        y=0.95,
        ha="left",
        fontsize=17,
        color=INK,
        weight="semibold",
    )
    fig.text(
        0.055,
        0.84,
        "Bangladesh facility-validation queue. The evidence becomes better organized while closure permission remains at zero.",
        ha="left",
        fontsize=10.5,
        color=INK_SOFT,
    )
    fig.text(0.055, 0.07, VALIDATION_FOOTER, ha="left", va="bottom", fontsize=7.2, color=INK_SOFT, wrap=True)
    save_figure(fig, "psdq-validation-wall")
    return {"stages": stages}


def main() -> None:
    sensitivity = load_json(SENSITIVITY_PATH)
    ledger = load_json(LEDGER_PATH)
    summary = {
        "program": "public-service-data-quality",
        "attestation_chain": "ai-first",
        "source_inputs": [
            str(SENSITIVITY_PATH.relative_to(ROOT)),
            str(LEDGER_PATH.relative_to(ROOT)),
        ],
        "sensitivity_figure": render_sensitivity(sensitivity),
        "validation_wall_figure": render_validation_wall(ledger),
        "non_claim": (
            "The ratios are source-disagreement diagnostics, not facility quality, service access, or proof that either source is ground truth. "
            "The validation path is not human review and does not authorize row closure."
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
