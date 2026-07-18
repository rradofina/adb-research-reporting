"""Validate the inherited water-crop ranking against its promised constructs.

The inherited screen combines annual freshwater withdrawal as a share of
INTERNAL renewable resources, inverse cereal yield, and rural population. It
then describes the intersection of seven top-five lists as a persistent top
four. This script tests that claim against two public objects already fetched
by ``audit-water-source-readiness.py``:

* WDI/AQUASTAT SDG 6.4.2 water stress, which uses available renewable water
  after environmental-flow requirements; and
* FAOSTAT harvested-area crop shares, summarized by HHI and Shannon
  equitability.

Every reported number is generated here from committed artifacts. The
diagnostic composite remains triage only. Public data only.
attestation_chain: ai-first.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generated"
READINESS_PATH = GEN / "water-stress-source-readiness.json"
DENOMINATOR_PATH = GEN / "water-stress-denominator-deepening.json"
SENSITIVITY_PATH = ROOT / "sensitivity-runs.json"

OUT_JSON = GEN / "water-construct-validation.json"
OUT_DIAGNOSTICS = GEN / "water-construct-diagnostics.csv"
OUT_SENSITIVITY = GEN / "water-construct-sensitivity.csv"

PUBLISHED_SET = {"AFG", "AZE", "PAK", "TKM"}
BOOTSTRAP_REPS = 5000
BOOTSTRAP_SEED = 64202


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rankdata(values: list[float]) -> list[float]:
    """Average ranks with deterministic tie handling."""
    order = sorted(range(len(values)), key=lambda idx: values[idx])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start
        while end + 1 < len(order) and values[order[end + 1]] == values[order[start]]:
            end += 1
        average_rank = (start + end + 2) / 2.0
        for position in range(start, end + 1):
            ranks[order[position]] = average_rank
        start = end + 1
    return ranks


def pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) < 3 or len(left) != len(right):
        return None
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    left_ss = sum((x - left_mean) ** 2 for x in left)
    right_ss = sum((y - right_mean) ** 2 for y in right)
    if left_ss <= 0 or right_ss <= 0:
        return None
    return numerator / math.sqrt(left_ss * right_ss)


def spearman(left: list[float], right: list[float]) -> float | None:
    return pearson(rankdata(left), rankdata(right))


def percentile(values: list[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def bootstrap_spearman(left: list[float], right: list[float], seed_offset: int) -> list[float | None]:
    rng = random.Random(BOOTSTRAP_SEED + seed_offset)
    estimates: list[float] = []
    for _ in range(BOOTSTRAP_REPS):
        indices = [rng.randrange(len(left)) for _ in left]
        estimate = spearman([left[i] for i in indices], [right[i] for i in indices])
        if estimate is not None and math.isfinite(estimate):
            estimates.append(estimate)
    return [percentile(estimates, 0.025), percentile(estimates, 0.975)]


def add_descending_rank(rows: list[dict], value_field: str, rank_field: str) -> None:
    usable = [row for row in rows if row.get(value_field) is not None]
    usable.sort(key=lambda row: (-float(row[value_field]), row["iso3"]))
    for rank, row in enumerate(usable, 1):
        row[rank_field] = rank


def top_isos(rows: list[dict], value_field: str, limit: int = 5) -> list[str]:
    usable = [row for row in rows if row.get(value_field) is not None]
    usable.sort(key=lambda row: (-float(row[value_field]), row["iso3"]))
    return [row["iso3"] for row in usable[:limit]]


def overlap(left: list[str] | set[str], right: list[str] | set[str]) -> dict:
    left_set = set(left)
    right_set = set(right)
    intersection = sorted(left_set & right_set)
    union = left_set | right_set
    return {
        "count": len(intersection),
        "members": intersection,
        "jaccard": round(len(intersection) / len(union), 4) if union else None,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def correlation_record(rows: list[dict], left_field: str, right_field: str,
                       label: str, seed_offset: int) -> dict:
    aligned = [
        row for row in rows
        if row.get(left_field) is not None and row.get(right_field) is not None
    ]
    left = [float(row[left_field]) for row in aligned]
    right = [float(row[right_field]) for row in aligned]
    estimate = spearman(left, right)
    interval = bootstrap_spearman(left, right, seed_offset)
    return {
        "label": label,
        "left_field": left_field,
        "right_field": right_field,
        "n": len(aligned),
        "spearman": round(estimate, 4) if estimate is not None else None,
        "bootstrap_ci95": [round(value, 4) if value is not None else None for value in interval],
        "bootstrap_reps": BOOTSTRAP_REPS,
        "bootstrap_seed": BOOTSTRAP_SEED + seed_offset,
    }


def sensitivity_specs(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Apply the required +/-50% checks to the diagnostic composite.

    The baseline diagnostic implicitly gives unit exponents to crop HHI and
    rural share and caps the water term at 1.5. All three arbitrary choices
    are tested at 0.5x, 1.0x, and 1.5x their baseline value.
    """
    rankable = [
        row for row in rows
        if row.get("available_water_stress_pct") is not None
        and row.get("crop_hhi") is not None
        and row.get("rural_pct") is not None
    ]
    baseline_top5: list[str] = []
    specs: list[dict] = []
    frequency: Counter[str] = Counter()
    for water_ceiling in (0.75, 1.5, 2.25):
        for crop_exponent in (0.5, 1.0, 1.5):
            for rural_exponent in (0.5, 1.0, 1.5):
                scored = []
                for row in rankable:
                    water_term = min(float(row["available_water_stress_pct"]) / 100.0, water_ceiling)
                    crop_term = float(row["crop_hhi"]) ** crop_exponent
                    rural_term = (float(row["rural_pct"]) / 100.0) ** rural_exponent
                    scored.append((row["iso3"], water_term * crop_term * rural_term * 100.0))
                scored.sort(key=lambda item: (-item[1], item[0]))
                top5 = [iso for iso, _ in scored[:5]]
                if (water_ceiling, crop_exponent, rural_exponent) == (1.5, 1.0, 1.0):
                    baseline_top5 = top5
                specs.append({
                    "water_ceiling": water_ceiling,
                    "crop_hhi_exponent": crop_exponent,
                    "rural_exponent": rural_exponent,
                    "top5": top5,
                    "top5_text": "|".join(top5),
                })
                frequency.update(top5)

    for spec in specs:
        comparison = overlap(spec["top5"], baseline_top5)
        spec["overlap_baseline_count"] = comparison["count"]
        spec["overlap_baseline_jaccard"] = comparison["jaccard"]
        spec["overlap_published_count"] = overlap(spec["top5"], PUBLISHED_SET)["count"]

    membership = []
    for iso, count in sorted(frequency.items(), key=lambda item: (-item[1], item[0])):
        membership.append({
            "iso3": iso,
            "top5_appearances": count,
            "specifications": len(specs),
            "appearance_share": round(count / len(specs), 4),
            "published_member": iso in PUBLISHED_SET,
        })
    return specs, membership


def ablation_specs(rows: list[dict]) -> list[dict]:
    rankable = [
        row for row in rows
        if row.get("available_water_stress_pct") is not None
        and row.get("crop_hhi") is not None
        and row.get("rural_pct") is not None
    ]
    definitions = {
        "water only": (True, False, False),
        "crop HHI only": (False, True, False),
        "rural share only": (False, False, True),
        "water x crop HHI": (True, True, False),
        "water x rural share": (True, False, True),
        "crop HHI x rural share": (False, True, True),
        "all three": (True, True, True),
    }
    out = []
    for label, (use_water, use_crop, use_rural) in definitions.items():
        scored = []
        for row in rankable:
            score = 1.0
            if use_water:
                score *= min(float(row["available_water_stress_pct"]) / 100.0, 1.5)
            if use_crop:
                score *= float(row["crop_hhi"])
            if use_rural:
                score *= float(row["rural_pct"]) / 100.0
            scored.append((row["iso3"], score))
        scored.sort(key=lambda item: (-item[1], item[0]))
        top5 = [iso for iso, _ in scored[:5]]
        out.append({
            "specification": label,
            "top5": top5,
            "overlap_published_count": overlap(top5, PUBLISHED_SET)["count"],
        })
    return out


def main() -> None:
    readiness = json.loads(READINESS_PATH.read_text(encoding="utf-8"))
    denominator = json.loads(DENOMINATOR_PATH.read_text(encoding="utf-8"))
    sensitivity = json.loads(SENSITIVITY_PATH.read_text(encoding="utf-8"))

    rows = [dict(row) for row in readiness["source_variant_rows"]]
    add_descending_rank(rows, "old_raw_index", "old_index_rank")
    add_descending_rank(rows, "available_water_stress_pct", "available_water_rank")
    add_descending_rank(rows, "crop_hhi", "crop_hhi_rank")
    add_descending_rank(rows, "rural_pct", "rural_rank")
    add_descending_rank(rows, "source_variant_score", "source_variant_rank_rebuilt")
    for row in rows:
        row["published_member"] = row["iso3"] in PUBLISHED_SET
        row["has_available_water"] = row.get("available_water_stress_pct") is not None
        row["has_crop_mix"] = row.get("crop_hhi") is not None
        row["aligned_water_crop"] = row["has_available_water"] and row["has_crop_mix"]

    raw_top4 = top_isos(rows, "old_raw_index", 4)
    available_top5 = top_isos(rows, "available_water_stress_pct", 5)
    crop_top5 = top_isos(rows, "crop_hhi", 5)
    variant_top5 = top_isos(rows, "source_variant_score", 5)
    crop_top5_with_water = [
        row["iso3"] for row in rows
        if row["iso3"] in crop_top5 and row["has_available_water"]
    ]

    run_checks = []
    exact_top4_matches = 0
    published_member_top4_counts: Counter[str] = Counter()
    for run in sensitivity["runs"]:
        order = [item["iso3"] if isinstance(item, dict) else item for item in run["top10"]]
        run_top4 = order[:4]
        if set(run_top4) == PUBLISHED_SET:
            exact_top4_matches += 1
        for iso in PUBLISHED_SET:
            if iso in run_top4:
                published_member_top4_counts[iso] += 1
        run_checks.append({
            "label": run["label"],
            "top4": run_top4,
            "top5": order[:5],
            "published_overlap_top4": overlap(run_top4, PUBLISHED_SET)["count"],
            "published_exact_top4": set(run_top4) == PUBLISHED_SET,
        })

    correlations = [
        correlation_record(rows, "old_raw_index", "available_water_stress_pct",
                           "Old composite vs available-water stress", 1),
        correlation_record(rows, "old_raw_index", "crop_hhi",
                           "Old composite vs crop concentration", 2),
        correlation_record(rows, "available_water_stress_pct", "crop_hhi",
                           "Available-water stress vs crop concentration", 3),
        correlation_record(rows, "source_variant_score", "available_water_stress_pct",
                           "Diagnostic variant vs available-water stress", 4),
        correlation_record(rows, "source_variant_score", "crop_hhi",
                           "Diagnostic variant vs crop concentration", 5),
        correlation_record(rows, "source_variant_score", "rural_pct",
                           "Diagnostic variant vs rural share", 6),
    ]

    specs, membership = sensitivity_specs(rows)
    ablations = ablation_specs(rows)
    summary = {
        "program_roster_n": readiness["summary"]["roster_n"],
        "old_rankable_n": sum(row.get("old_raw_index") is not None for row in rows),
        "available_water_n": sum(row["has_available_water"] for row in rows),
        "crop_mix_n": sum(row["has_crop_mix"] for row in rows),
        "aligned_water_crop_n": sum(row["aligned_water_crop"] for row in rows),
        "published_set": sorted(PUBLISHED_SET),
        "old_raw_top4": raw_top4,
        "published_vs_old_raw_top4": overlap(PUBLISHED_SET, raw_top4),
        "available_water_top5": available_top5,
        "published_vs_available_water_top5": overlap(PUBLISHED_SET, available_top5),
        "crop_hhi_top5": crop_top5,
        "published_vs_crop_hhi_top5": overlap(PUBLISHED_SET, crop_top5),
        "crop_hhi_top5_with_available_water_n": len(crop_top5_with_water),
        "crop_hhi_top5_with_available_water": crop_top5_with_water,
        "diagnostic_variant_top5": variant_top5,
        "published_vs_diagnostic_variant_top5": overlap(PUBLISHED_SET, variant_top5),
        "old_sensitivity_run_count": len(run_checks),
        "old_sensitivity_exact_published_top4_runs": exact_top4_matches,
        "published_member_top4_run_counts": dict(sorted(published_member_top4_counts.items())),
        "old_top4_water_term_saturated_n": len(
            set(raw_top4)
            & {
                row["iso3"]
                for row in denominator["over_100pct_internal_denominator"]
                if row.get("water_term_saturated")
            }
        ),
        "diagnostic_sensitivity_specifications": len(specs),
        "diagnostic_sensitivity_min_baseline_overlap": min(
            spec["overlap_baseline_count"] for spec in specs
        ),
        "diagnostic_sensitivity_max_baseline_overlap": max(
            spec["overlap_baseline_count"] for spec in specs
        ),
        "analysis_ready_basin_crop_overlay": False,
        "claim_decision": "reject inherited country ranking",
        "next_data_object": (
            "basin x crop harvested area x irrigation status/water requirement, with "
            "withdrawal or depletion and exposure aligned to a common year"
        ),
    }

    payload = {
        "program": "water-stress-crop-diversification",
        "analysis": "construct validation of inherited water-crop country ranking",
        "claim_scope": (
            "Tests the inherited country set against direct national water-stress and "
            "crop-concentration objects. Results establish construct disagreement and "
            "coverage limits; they do not estimate basin-level scarcity, crop water "
            "demand, irrigation exposure, depletion, resilience, or policy priority."
        ),
        "summary": summary,
        "correlations": correlations,
        "old_sensitivity_runs": run_checks,
        "diagnostic_sensitivity_specs": specs,
        "diagnostic_membership_frequency": membership,
        "component_ablations": ablations,
        "diagnostic_rows": rows,
        "sources": readiness["sources"],
        "attestation_chain": "ai-first",
        "generated_at": utc_stamp(),
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(OUT_DIAGNOSTICS, rows)
    write_csv(OUT_SENSITIVITY, specs)

    print("=== Water-crop construct validation ===")
    print(f"Roster / old rankable / crop / aligned: {summary['program_roster_n']} / "
          f"{summary['old_rankable_n']} / {summary['crop_mix_n']} / {summary['aligned_water_crop_n']}")
    print(f"Published set vs direct water top five: {summary['published_vs_available_water_top5']['count']} of 4")
    print(f"Published set vs direct crop-HHI top five: {summary['published_vs_crop_hhi_top5']['count']} of 4")
    print(f"Crop-HHI top five with water data: {summary['crop_hhi_top5_with_available_water_n']} of 5")
    for record in correlations:
        print(f"{record['label']}: rho={record['spearman']:+.3f}, n={record['n']}, "
              f"CI={record['bootstrap_ci95']}")
    print(f"Old exact top-four matches: {exact_top4_matches} of {len(run_checks)} runs")
    print(f"Diagnostic 27-spec baseline overlap range: "
          f"{summary['diagnostic_sensitivity_min_baseline_overlap']}-"
          f"{summary['diagnostic_sensitivity_max_baseline_overlap']} of 5")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_DIAGNOSTICS}")
    print(f"Wrote {OUT_SENSITIVITY}")


if __name__ == "__main__":
    main()
