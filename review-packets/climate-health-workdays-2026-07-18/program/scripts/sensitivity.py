"""Sensitivity suite at +/-50 percent for Climate-Health Workday Loss.

Per CONSTITUTION.md section 6.6 every arbitrary numeric in
pre-registration.md is tested at +/-50 percent. Arbitrary numerics:
1. Industry weight (0.5) in outdoor_labor_share = agri + 0.5 * industry
2. PM2.5 floor (5)
3. PM2.5 cap (45 ramp range)
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/climate-health-workdays")
PANEL = ROOT / "generated" / "climate-health-workdays-adb-panel.json"
OUT = ROOT / "sensitivity-runs.json"


def index_for(row, industry_weight=0.5, pm25_floor=5.0, pm25_cap=45.0):
    a = row.get("emp_agri_pct")
    i = row.get("emp_industry_pct")
    p = row.get("pm25_exposure_ugm3")
    if a is None or i is None or p is None:
        return None
    outdoor = (a + industry_weight * i) / 100.0
    pressure = max(p - pm25_floor, 0.0) / pm25_cap
    pressure = min(max(pressure, 0.0), 1.0)
    return round(outdoor * pressure * 100, 2)


def rank(rows, **kw):
    out = []
    for r in rows:
        idx = index_for(r, **kw)
        if idx is None:
            continue
        out.append({"iso3": r["iso3"], "country": r.get("country", ""), "index": idx})
    out.sort(key=lambda x: -x["index"])
    return out


def overlap(a, b, k=5):
    return len({x["iso3"] for x in a[:k]} & {x["iso3"] for x in b[:k]})


def main():
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    rows = panel.get("rows", [])

    runs = []
    base = rank(rows)
    runs.append({"label": "baseline", "industry_weight": 0.5, "pm25_floor": 5.0, "pm25_cap": 45.0, "top10": base[:10], "top5_overlap_with_baseline": 5})

    for w, lbl in [(0.25, "industry_weight_minus50"), (0.75, "industry_weight_plus50")]:
        r = rank(rows, industry_weight=w)
        runs.append({"label": lbl, "industry_weight": w, "top10": r[:10], "top5_overlap_with_baseline": overlap(base, r)})

    for f, lbl in [(2.5, "pm25_floor_minus50"), (7.5, "pm25_floor_plus50")]:
        r = rank(rows, pm25_floor=f)
        runs.append({"label": lbl, "pm25_floor": f, "top10": r[:10], "top5_overlap_with_baseline": overlap(base, r)})

    for c, lbl in [(22.5, "pm25_cap_minus50"), (67.5, "pm25_cap_plus50")]:
        r = rank(rows, pm25_cap=c)
        runs.append({"label": lbl, "pm25_cap": c, "top10": r[:10], "top5_overlap_with_baseline": overlap(base, r)})

    # Common top-5 across all runs
    sets = [{x["iso3"] for x in run["top10"][:5]} for run in runs]
    common = sorted(set.intersection(*sets) if sets else set())

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "climate-health-workdays",
        "metric": "workday-loss-pressure-index ranking, top-5 ADB DMC composition",
        "decision_rule": "Pre-registered: positive if the top-5 set composition changes by <= 1 entry in any single +/-50% perturbation.",
        "common_top5_across_runs": common,
        "runs": runs,
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    for r in runs:
        print(f"{r['label']:<32} top5_overlap={r['top5_overlap_with_baseline']}")
    print(f"\ncommon top-5 across all runs: {common}")


if __name__ == "__main__":
    main()
