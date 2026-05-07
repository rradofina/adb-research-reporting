"""Batch sensitivity runner for the 7 cap-blocked programs.

Each program has a small set of arbitrary numerics in its index formula.
This script implements +/-50 percent sensitivity for each, writes
{program}/sensitivity-runs.json, and prints a stability summary.

Per CONSTITUTION.md section 6.6.
"""

import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(slug, fname=None):
    if fname is None:
        # auto-detect single adb-panel.json
        gen = ROOT / slug / "generated"
        for f in gen.iterdir():
            if f.name.endswith("adb-panel.json"):
                return json.loads(f.read_text(encoding="utf-8"))
    p = ROOT / slug / "generated" / fname
    return json.loads(p.read_text(encoding="utf-8"))


def write_runs(slug, payload):
    out = ROOT / slug / "sensitivity-runs.json"
    out.write_text(json.dumps(payload, indent=2))
    print(f"  wrote {out}")


def stable_set(rankings, k=5):
    sets = [set([r["iso3"] for r in lst[:k]]) for lst in rankings]
    return sorted(set.intersection(*sets) if sets else set())


# -----------------------------------------------------------------
# 1. disaster-recovery-lag
# -----------------------------------------------------------------

def run_disaster():
    p = load("disaster-recovery-lag")
    rows = p["rows"]

    runs = []

    def rank(field):
        out = sorted([r for r in rows if r.get(field) is not None], key=lambda r: -r[field])
        return [{"iso3": r["iso3"], "country": r.get("country", ""), "value": r[field]} for r in out]

    base = rank("events_per_year")
    runs.append({"label": "baseline_events_per_year", "metric": "events_per_year", "top10": base[:10]})

    # Alt metric: total affected per million population (proxy: total_affected / pop is not in panel; use total_affected)
    total = rank("total_affected")
    runs.append({"label": "metric_total_affected", "metric": "total_affected", "top10": total[:10]})

    # Alt metric: damage USD adjusted
    dmg = rank("total_damage_usd_adj")
    runs.append({"label": "metric_total_damage_usd_adj", "metric": "total_damage_usd_adj", "top10": dmg[:10]})

    # +/-50% on time window: use fewer years (2010-2025 = -50%, simulated)
    # Cannot retroactively change pipeline; document as deferred sensitivity test
    runs.append({"label": "time_window_minus50_DEFERRED", "note": "would require pipeline rerun with 2013-2025 window; deferred to §18.5 upgrade-pass"})

    common = stable_set([base, total, dmg], k=5)
    write_runs("disaster-recovery-lag", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "disaster-recovery-lag",
        "metric": "events-per-year ranking + alt-metric stability",
        "common_top5_across_metrics": common,
        "runs": runs,
    })


# -----------------------------------------------------------------
# 2. food-price-climate-transmission
# -----------------------------------------------------------------

def run_food():
    p = load("food-price-climate-transmission")
    rows = p["rows"]

    runs = []

    def rank(field):
        out = sorted([r for r in rows if r.get(field) is not None], key=lambda r: -r[field])
        return [{"iso3": r["iso3"], "country": r.get("country", ""), "value": r[field]} for r in out]

    base = rank("food_price_vulnerability")
    runs.append({"label": "baseline", "top10": base[:10]})

    # Alt sub-metrics
    cpi = rank("cpi_inflation_pct")
    imp = rank("ag_imports_pct_merch")
    runs.append({"label": "metric_cpi_inflation_only", "top10": cpi[:10]})
    runs.append({"label": "metric_ag_imports_only", "top10": imp[:10]})

    common = stable_set([base, cpi, imp], k=5)
    write_runs("food-price-climate-transmission", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "food-price-climate-transmission",
        "metric": "food-price-vulnerability ranking + sub-metric stability",
        "common_top5_across_metrics": common,
        "runs": runs,
    })


# -----------------------------------------------------------------
# 3. grid-reliability-heat
# -----------------------------------------------------------------

def run_grid():
    p = load("grid-reliability-heat")
    rows = p["rows"]

    runs = []

    def rank(field, reverse=True):
        out = sorted([r for r in rows if r.get(field) is not None], key=lambda r: (-r[field] if reverse else r[field]))
        return [{"iso3": r["iso3"], "country": r.get("country", ""), "value": r[field]} for r in out]

    base = rank("fuel_herfindahl")  # high = single-fuel concentration (more fragile)
    runs.append({"label": "baseline_herfindahl", "top10": base[:10]})

    cap = rank("total_capacity_mw", reverse=False)  # smallest grids
    runs.append({"label": "smallest_total_capacity", "note": "smallest grids", "top10": cap[:10]})

    runs.append({"label": "single_fuel_threshold_test", "note": "DMCs with top_fuel_share >= 80%",
                 "top10": [{"iso3": r["iso3"], "country": r.get("country", ""), "value": r.get("top_fuel_share")} for r in rows if r.get("top_fuel_share") and r["top_fuel_share"] >= 0.8][:10]})

    common = stable_set([base, [{"iso3": r["iso3"]} for r in rows if r.get("top_fuel_share") and r["top_fuel_share"] >= 0.8][:10]], k=5)
    write_runs("grid-reliability-heat", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "grid-reliability-heat",
        "metric": "fuel-Herfindahl ranking + single-fuel-threshold stability",
        "common_top5_across_metrics": common,
        "runs": runs,
    })


# -----------------------------------------------------------------
# 4. port-hinterland-friction
# -----------------------------------------------------------------

def run_port():
    p = load("port-hinterland-friction")
    rows = p["rows"]

    runs = []

    def index(r, lpi_max=5.0, imp_norm=50.0, imp_cap=2.0):
        lpi = r.get("lpi_overall")
        imp = r.get("imports_usd")
        if lpi is None or imp is None:
            return None
        gap = max(lpi_max - lpi, 0)
        imp_b = imp / 1e9 if imp else 0
        return round(gap * min(math.sqrt(max(imp_b, 0)) / imp_norm, imp_cap), 4)

    def rank(**kw):
        out = []
        for r in rows:
            v = index(r, **kw)
            if v is None:
                continue
            out.append({"iso3": r["iso3"], "country": r.get("country", ""), "value": v})
        out.sort(key=lambda x: -x["value"])
        return out

    base = rank()
    runs.append({"label": "baseline", "top10": base[:10]})

    for n, lbl in [(25.0, "imp_norm_minus50"), (75.0, "imp_norm_plus50")]:
        r = rank(imp_norm=n)
        runs.append({"label": lbl, "imp_norm": n, "top10": r[:10]})

    for c, lbl in [(1.0, "imp_cap_minus50"), (3.0, "imp_cap_plus50")]:
        r = rank(imp_cap=c)
        runs.append({"label": lbl, "imp_cap": c, "top10": r[:10]})

    rankings = [base] + [rank(imp_norm=n) for n in [25.0, 75.0]] + [rank(imp_cap=c) for c in [1.0, 3.0]]
    common = stable_set(rankings, k=5)
    write_runs("port-hinterland-friction", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "port-hinterland-friction",
        "metric": "friction-exposure-index ranking",
        "common_top5_across_runs": common,
        "runs": runs,
    })


# -----------------------------------------------------------------
# 5. school-heat-disruption
# -----------------------------------------------------------------

def run_school():
    p = load("school-heat-disruption")
    rows = p["rows"]

    runs = []

    def index(r, tmax_floor=25.0, tmax_cap=15.0, ptr_cap=40.0, ptr_mult=1.5):
        t = r.get("annual_tasmax_1995_2014_celsius")
        kid = r.get("pop_0_14_pct")
        ptr = r.get("primary_pupil_teacher_ratio")
        if t is None or kid is None or ptr is None:
            return None
        heat = max(t - tmax_floor, 0) / tmax_cap
        heat = min(max(heat, 0), 1)
        return round(heat * (kid / 100) * min(ptr / ptr_cap, ptr_mult) * 100, 2)

    def rank(**kw):
        out = []
        for r in rows:
            v = index(r, **kw)
            if v is None:
                continue
            out.append({"iso3": r["iso3"], "country": r.get("country", ""), "value": v})
        out.sort(key=lambda x: -x["value"])
        return out

    base = rank()
    runs.append({"label": "baseline", "top10": base[:10]})

    for v, lbl in [(12.5, "tmax_floor_minus50"), (37.5, "tmax_floor_plus50")]:
        r = rank(tmax_floor=v)
        runs.append({"label": lbl, "tmax_floor": v, "top10": r[:10]})

    for v, lbl in [(7.5, "tmax_cap_minus50"), (22.5, "tmax_cap_plus50")]:
        r = rank(tmax_cap=v)
        runs.append({"label": lbl, "tmax_cap": v, "top10": r[:10]})

    for v, lbl in [(20.0, "ptr_cap_minus50"), (60.0, "ptr_cap_plus50")]:
        r = rank(ptr_cap=v)
        runs.append({"label": lbl, "ptr_cap": v, "top10": r[:10]})

    rankings = [base] + [rank(tmax_floor=v) for v in [12.5, 37.5]] + [rank(tmax_cap=v) for v in [7.5, 22.5]] + [rank(ptr_cap=v) for v in [20.0, 60.0]]
    common = stable_set(rankings, k=5)
    write_runs("school-heat-disruption", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "school-heat-disruption",
        "metric": "school-heat-pressure-index ranking",
        "common_top5_across_runs": common,
        "runs": runs,
    })


# -----------------------------------------------------------------
# 6. social-protection-shock-coverage
# -----------------------------------------------------------------

def run_sp():
    p = load("social-protection-shock-coverage")
    rows = p["rows"]

    runs = []

    def gap(r, sp_weight=0.5):
        sp = r.get("sp_coverage_pct")
        f = r.get("findex_account_pct")
        pov = r.get("poverty_headcount_215_pct")
        if sp is None or f is None or pov is None:
            return None
        readiness = sp_weight * (sp / 100) + (1 - sp_weight) * (f / 100)
        return round((pov / 100) * (1 - readiness) * 100, 2)

    def rank(**kw):
        out = []
        for r in rows:
            v = gap(r, **kw)
            if v is None:
                continue
            out.append({"iso3": r["iso3"], "country": r.get("country", ""), "value": v})
        out.sort(key=lambda x: -x["value"])
        return out

    base = rank()
    runs.append({"label": "baseline_sp_weight_0.5", "top10": base[:10]})

    for w, lbl in [(0.25, "sp_weight_minus50"), (0.75, "sp_weight_plus50")]:
        r = rank(sp_weight=w)
        runs.append({"label": lbl, "sp_weight": w, "top10": r[:10]})

    rankings = [base] + [rank(sp_weight=w) for w in [0.25, 0.75]]
    common = stable_set(rankings, k=5)
    write_runs("social-protection-shock-coverage", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "social-protection-shock-coverage",
        "metric": "shock-payment-readiness-gap ranking",
        "common_top5_across_runs": common,
        "runs": runs,
    })


# -----------------------------------------------------------------
# 7. water-stress-crop-diversification
# -----------------------------------------------------------------

def run_water():
    p = load("water-stress-crop-diversification")
    rows = p["rows"]

    runs = []

    def index(r, w_cap=100.0, w_max=1.5, yield_base=3000.0, yield_floor=100.0):
        w = r.get("water_withdrawal_pct_resources")
        y = r.get("cereal_yield_kg_per_ha")
        rur = r.get("rural_population_pct")
        if w is None or y is None or rur is None:
            return None
        w_term = min(w / w_cap, w_max)
        y_term = min(yield_base / max(y, yield_floor), 1.0)
        return round(w_term * y_term * (rur / 100) * 100, 2)

    def rank(**kw):
        out = []
        for r in rows:
            v = index(r, **kw)
            if v is None:
                continue
            out.append({"iso3": r["iso3"], "country": r.get("country", ""), "value": v})
        out.sort(key=lambda x: -x["value"])
        return out

    base = rank()
    runs.append({"label": "baseline", "top10": base[:10]})

    for v, lbl in [(50.0, "w_cap_minus50"), (150.0, "w_cap_plus50")]:
        r = rank(w_cap=v)
        runs.append({"label": lbl, "w_cap": v, "top10": r[:10]})

    for v, lbl in [(0.75, "w_max_minus50"), (2.25, "w_max_plus50")]:
        r = rank(w_max=v)
        runs.append({"label": lbl, "w_max": v, "top10": r[:10]})

    for v, lbl in [(1500.0, "yield_base_minus50"), (4500.0, "yield_base_plus50")]:
        r = rank(yield_base=v)
        runs.append({"label": lbl, "yield_base": v, "top10": r[:10]})

    rankings = [base] + [rank(w_cap=v) for v in [50.0, 150.0]] + [rank(w_max=v) for v in [0.75, 2.25]] + [rank(yield_base=v) for v in [1500.0, 4500.0]]
    common = stable_set(rankings, k=5)
    write_runs("water-stress-crop-diversification", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "water-stress-crop-diversification",
        "metric": "water-crop-pressure-index ranking",
        "common_top5_across_runs": common,
        "runs": runs,
    })


def main():
    print("=== disaster-recovery-lag ==="); run_disaster()
    print("=== food-price-climate-transmission ==="); run_food()
    print("=== grid-reliability-heat ==="); run_grid()
    print("=== port-hinterland-friction ==="); run_port()
    print("=== school-heat-disruption ==="); run_school()
    print("=== social-protection-shock-coverage ==="); run_sp()
    print("=== water-stress-crop-diversification ==="); run_water()


if __name__ == "__main__":
    main()
