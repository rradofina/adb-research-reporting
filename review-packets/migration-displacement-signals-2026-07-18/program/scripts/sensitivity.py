"""Sensitivity suite for the migration denominator-switch claim.

The primary test compares an absolute UN DESA emigrant-stock ranking with
the same numerator divided by WDI origin population. The arbitrary top-N
choice is tested at 3, 5, and 8 (approximately -50%/+50% around five). The
material-change threshold is tested at 25%, 50%, and 75% overlap.

The UNHCR forced-displacement classification uses a 50% majority threshold
and tests 25% and 75%. Corridor concentration remains a descriptive
secondary result and is shown at top-2/top-3/top-5 destinations and at
25%/50%/75% thresholds.

All inputs are committed generated objects. No network access.
attestation_chain: ai-first.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = ROOT / "generated" / "migration-displacement-adb-panel.json"
PER_POP_PATH = ROOT / "generated" / "migration-per-population-deepening.json"
FORCED_PATH = ROOT / "generated" / "migration-corridor-type-forced-displacement.json"
OUT_PATH = ROOT / "sensitivity-runs.json"

TOP_N_VARIANTS = [3, 5, 8]
OVERLAP_THRESHOLDS = [0.25, 0.50, 0.75]
FORCED_THRESHOLDS = [0.25, 0.50, 0.75]
CORRIDOR_N_VARIANTS = [2, 3, 5]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def top_destination_share(row: dict, n: int) -> float:
    destinations = row.get("top_destinations") or []
    denominator = row.get("emigrant_stock_2024") or 0
    if not denominator:
        return 0.0
    return sum(int(item.get("stock") or 0) for item in destinations[:n]) / denominator


def main() -> None:
    panel = load_json(PANEL_PATH)
    per_pop = load_json(PER_POP_PATH)
    forced = load_json(FORCED_PATH)

    panel_rows = [row for row in panel["rows"] if row.get("emigrant_stock_2024") is not None]
    absolute_order = sorted(panel_rows, key=lambda row: -int(row["emigrant_stock_2024"]))
    share_order = list(per_pop["rows_by_share"])

    overlap_runs = []
    for n in TOP_N_VARIANTS:
        absolute_set = {row["iso3"] for row in absolute_order[:n]}
        share_set = {row["iso3"] for row in share_order[:n]}
        overlap = sorted(absolute_set & share_set)
        overlap_share = len(overlap) / n
        overlap_runs.append({
            "top_n": n,
            "absolute": [row["iso3"] for row in absolute_order[:n]],
            "population_share": [row["iso3"] for row in share_order[:n]],
            "overlap": overlap,
            "overlap_count": len(overlap),
            "overlap_share": round(overlap_share, 4),
            "material_change_at_threshold": {
                f"{threshold:.2f}": overlap_share <= threshold
                for threshold in OVERLAP_THRESHOLDS
            },
        })

    forced_by_iso = {row["iso3"]: row for row in forced["country_rows"]}
    share_top5 = [row["iso3"] for row in share_order[:5]]
    afghanistan_share = float(
        forced_by_iso["AFG"]["forced_abroad_share_of_emigrant_stock"]
    )
    share_top5_forced = {
        iso: float(forced_by_iso[iso]["forced_abroad_share_of_emigrant_stock"] or 0)
        for iso in share_top5
    }
    forced_runs = []
    for threshold in FORCED_THRESHOLDS:
        forced_runs.append({
            "threshold": threshold,
            "afghanistan_at_or_above": afghanistan_share >= threshold,
            "share_top5_at_or_above": [
                iso for iso, value in share_top5_forced.items() if value >= threshold
            ],
        })

    absolute_top5_rows = absolute_order[:5]
    corridor_rows = []
    for row in absolute_top5_rows:
        shares = {
            f"top_{n}": round(top_destination_share(row, n), 4)
            for n in CORRIDOR_N_VARIANTS
        }
        corridor_rows.append({"iso3": row["iso3"], "country": row["country"], **shares})

    corridor_thresholds = []
    for threshold in FORCED_THRESHOLDS:
        corridor_thresholds.append({
            "threshold": threshold,
            "origins_at_or_above_top3_share": [
                row["iso3"] for row in corridor_rows if row["top_3"] >= threshold
            ],
        })

    baseline = next(run for run in overlap_runs if run["top_n"] == 5)
    suite = {
        "program": "migration-displacement-signals",
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_inputs": [
            str(PANEL_PATH.relative_to(ROOT)),
            str(PER_POP_PATH.relative_to(ROOT)),
            str(FORCED_PATH.relative_to(ROOT)),
        ],
        "primary_question": (
            "How much does the leading-origin set change when UN DESA 2024 emigrant "
            "stock is divided by WDI 2024 origin population?"
        ),
        "decision_rule": (
            "Reshape the absolute-stock headline if the absolute and population-share "
            "top-five sets overlap by at most 50 percent."
        ),
        "top_n_variants": TOP_N_VARIANTS,
        "overlap_thresholds": OVERLAP_THRESHOLDS,
        "denominator_switch": overlap_runs,
        "baseline_decision": {
            "absolute_top5": baseline["absolute"],
            "population_share_top5": baseline["population_share"],
            "overlap_count": baseline["overlap_count"],
            "overlap_share": baseline["overlap_share"],
            "reshape": baseline["overlap_share"] <= 0.50,
        },
        "forced_displacement_thresholds": FORCED_THRESHOLDS,
        "forced_displacement_sensitivity": {
            "afghanistan_share": round(afghanistan_share, 4),
            "population_share_top5": share_top5_forced,
            "threshold_runs": forced_runs,
        },
        "corridor_concentration": {
            "top_n_variants": CORRIDOR_N_VARIANTS,
            "rows": corridor_rows,
            "threshold_runs": corridor_thresholds,
            "interpretation": (
                "The top-three corridor split is descriptive and threshold-sensitive; "
                "it is not the primary denominator-switch finding."
            ),
        },
        "finding": (
            "The absolute and population-share top fives have zero overlap. The overlap "
            "remains zero at top three and rises only to one of eight at top eight. "
            "Afghanistan remains a forced-displacement-majority origin even at the 75 "
            "percent threshold; no population-share top-five economy reaches 25 percent."
        ),
        "non_claim": (
            "The suite does not measure current migration flows, migration propensity, "
            "welfare, labor-migration purpose, internal displacement, or causal drivers."
        ),
    }
    OUT_PATH.write_text(json.dumps(suite, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(ROOT)}")
    print(
        "Top-five overlap: "
        f"{baseline['overlap_count']}/5; reshape={suite['baseline_decision']['reshape']}"
    )


if __name__ == "__main__":
    main()
