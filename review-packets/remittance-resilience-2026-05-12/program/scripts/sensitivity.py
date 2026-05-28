"""Sensitivity suite at +/-50 percent for Remittance Resilience.

Implements CONSTITUTION.md section 6.6 for the parameters listed in
pre-registration.md. Re-computes the fragility-ranking headline across
alternative parameter values and writes deltas to ../sensitivity-runs.json.
"""

import json
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/remittance-resilience")
PANEL = ROOT / "generated" / "remittance-resilience-adb-panel.json"
OUT = ROOT / "sensitivity-runs.json"


def load_panel():
    return json.loads(PANEL.read_text(encoding="utf-8"))


def fragility(dep, cost, dep_cap, cost_cap):
    if dep is None or cost is None:
        return None
    n_dep = min(dep / dep_cap, 1.0) if dep_cap > 0 else 0
    n_cost = min(cost / cost_cap, 1.0) if cost_cap > 0 else 0
    return round(n_dep * n_cost * 100, 2)


def rank(rows, dep_cap, cost_cap):
    out = []
    for r in rows:
        f = fragility(r.get("wdi_remittance_pct_gdp"), r.get("rpw_mean_cost_pct"), dep_cap, cost_cap)
        if f is None:
            continue
        out.append({"iso3": r["iso3"], "country": r["country"], "fragility": f})
    out.sort(key=lambda x: -x["fragility"])
    return out


def top10_overlap(a, b):
    a_iso = {r["iso3"] for r in a[:10]}
    b_iso = {r["iso3"] for r in b[:10]}
    return len(a_iso & b_iso)


def main():
    panel = load_panel()
    rows = panel["rows"]

    runs = []

    # Baseline
    base = rank(rows, dep_cap=25.0, cost_cap=15.0)
    runs.append({
        "label": "baseline",
        "dep_cap": 25.0,
        "cost_cap": 15.0,
        "n_ranked": len(base),
        "top10": base[:10],
        "top10_overlap_with_baseline": 10,
    })

    # +/-50 percent on dependence cap
    for cap, lbl in [(12.5, "dep_cap_minus50"), (37.5, "dep_cap_plus50")]:
        r = rank(rows, dep_cap=cap, cost_cap=15.0)
        runs.append({
            "label": lbl,
            "dep_cap": cap,
            "cost_cap": 15.0,
            "n_ranked": len(r),
            "top10": r[:10],
            "top10_overlap_with_baseline": top10_overlap(base, r),
        })

    # +/-50 percent on cost cap
    for cap, lbl in [(7.5, "cost_cap_minus50"), (22.5, "cost_cap_plus50")]:
        r = rank(rows, dep_cap=25.0, cost_cap=cap)
        runs.append({
            "label": lbl,
            "dep_cap": 25.0,
            "cost_cap": cap,
            "n_ranked": len(r),
            "top10": r[:10],
            "top10_overlap_with_baseline": top10_overlap(base, r),
        })

    # Both caps simultaneously perturbed (cross-effect)
    for d, c, lbl in [
        (12.5, 7.5, "both_minus50"),
        (37.5, 22.5, "both_plus50"),
    ]:
        r = rank(rows, dep_cap=d, cost_cap=c)
        runs.append({
            "label": lbl,
            "dep_cap": d,
            "cost_cap": c,
            "n_ranked": len(r),
            "top10": r[:10],
            "top10_overlap_with_baseline": top10_overlap(base, r),
        })

    # Decision-rule check: which DMCs are in the top-5 across every suite row?
    sets = [{x["iso3"] for x in run["top10"][:5]} for run in runs]
    common_top5 = set.intersection(*sets) if sets else set()

    # Mean cost cap edge: what if we additively combine instead of multiplicatively?
    additive = []
    for r in rows:
        dep = r.get("wdi_remittance_pct_gdp")
        cost = r.get("rpw_mean_cost_pct")
        if dep is None or cost is None:
            continue
        n_dep = min(dep / 25.0, 1.0)
        n_cost = min(cost / 15.0, 1.0)
        additive.append({"iso3": r["iso3"], "country": r["country"], "fragility": round((n_dep + n_cost) / 2 * 100, 2)})
    additive.sort(key=lambda x: -x["fragility"])
    runs.append({
        "label": "additive_aggregation",
        "dep_cap": 25.0,
        "cost_cap": 15.0,
        "aggregation": "additive (mean of normalized values)",
        "top10": additive[:10],
        "top10_overlap_with_baseline": top10_overlap(base, additive),
    })

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "remittance-resilience",
        "metric": "fragility-index ranking, top-10 ADB DMC composition",
        "decision_rule": "Pre-registered §8: positive if the top-5 set is stable across all ±50% suite rows.",
        "common_top5_across_runs": sorted(common_top5),
        "runs": runs,
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    for r in runs:
        print(f"{r['label']:<30} top10_overlap={r['top10_overlap_with_baseline']}")
    print(f"\ncommon top-5 across all runs: {sorted(common_top5)}")


if __name__ == "__main__":
    main()
