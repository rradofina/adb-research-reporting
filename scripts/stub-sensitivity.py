"""Sensitivity at +/-50 percent for the 3 stub programs."""
import json, math
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def stable_set(rankings, k=5):
    sets = [set([r["iso3"] for r in lst[:k]]) for lst in rankings]
    return sorted(set.intersection(*sets) if sets else set())


def write_runs(slug, payload):
    (ROOT / slug / "sensitivity-runs.json").write_text(json.dumps(payload, indent=2))
    print(f"  wrote {slug}/sensitivity-runs.json")


# coastal-informal-risk: arbitrary = slum imputation value (10%)
def run_coastal():
    panel = json.loads((ROOT / "coastal-informal-risk/generated/coastal-informal-risk-adb-panel.json").read_text(encoding="utf-8"))
    rows = panel["rows"]

    def index(r, slum_impute=10.0):
        u = r["urban_pct"]
        p = r["population"]
        s = r.get("slum_pct_urban") if r.get("slum_pct_urban") is not None else slum_impute
        return round(math.log10(p) * (u / 100) * (s / 100) * 100, 2)

    def rank(impute):
        out = []
        for r in rows:
            v = index(r, slum_impute=impute)
            out.append({"iso3": r["iso3"], "country": r["country"], "value": v})
        out.sort(key=lambda x: -x["value"])
        return out

    base = rank(10.0)
    minus = rank(5.0)
    plus = rank(15.0)
    runs = [
        {"label": "baseline_slum_imputed_10pct", "top10": base[:10]},
        {"label": "slum_imputed_minus50_5pct", "top10": minus[:10]},
        {"label": "slum_imputed_plus50_15pct", "top10": plus[:10]},
    ]
    common = stable_set([base, minus, plus], k=5)
    write_runs("coastal-informal-risk", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "coastal-informal-risk",
        "metric": "coastal-informal-risk-index ranking",
        "common_top5_across_runs": common,
        "runs": runs,
    })


# invisible-urbanization: arbitrary = multiplier (10), rural-share defn
def run_urb():
    panel = json.loads((ROOT / "invisible-urbanization/generated/invisible-urbanization-adb-panel.json").read_text(encoding="utf-8"))
    rows = panel["rows"]

    def index(r, mult=10.0):
        rural = r["rural_pct"] / 100
        g = max(r["urban_pop_growth_pct"], 0)
        return round(rural * g * mult, 2)

    def rank(m):
        out = []
        for r in rows:
            v = index(r, mult=m)
            out.append({"iso3": r["iso3"], "country": r["country"], "value": v})
        out.sort(key=lambda x: -x["value"])
        return out

    base = rank(10.0)
    minus = rank(5.0)
    plus = rank(15.0)
    runs = [
        {"label": "baseline_mult_10", "top10": base[:10]},
        {"label": "mult_minus50_5", "top10": minus[:10]},
        {"label": "mult_plus50_15", "top10": plus[:10]},
    ]
    common = stable_set([base, minus, plus], k=5)
    write_runs("invisible-urbanization", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "invisible-urbanization",
        "metric": "invisible-urbanization-signal ranking",
        "note": "Multiplicative scalar does not change rank order — rank-stability is trivial under this perturbation. The honest claim is the rank order, not the score magnitude.",
        "common_top5_across_runs": common,
        "runs": runs,
    })


# flood-market-access: arbitrary = time window
def run_flood():
    panel = json.loads((ROOT / "flood-market-access/generated/flood-market-access-adb-panel.json").read_text(encoding="utf-8"))
    rows = panel["rows"]

    # Ranking by base index: deterministic from input
    base = sorted([{"iso3": r["iso3"], "country": r["country"], "value": r["flood_market_access_index"]}
                   for r in rows], key=lambda x: -x["value"])

    # Alt metric: flood-events-only (drop pop and rural multipliers)
    alt1 = sorted([{"iso3": r["iso3"], "country": r["country"], "value": r["flood_events_2000_2025"]}
                   for r in rows], key=lambda x: -x["value"])

    # Alt metric: rural-share × flood-events (drop log-pop)
    alt2 = sorted([{"iso3": r["iso3"], "country": r["country"],
                    "value": round((r["rural_pct"] / 100) * r["flood_events_2000_2025"], 2)}
                   for r in rows], key=lambda x: -x["value"])

    runs = [
        {"label": "baseline_full_index", "top10": base[:10]},
        {"label": "alt_flood_events_only", "top10": alt1[:10]},
        {"label": "alt_rural_x_floods", "top10": alt2[:10]},
    ]
    common = stable_set([base, alt1, alt2], k=5)
    write_runs("flood-market-access", {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "flood-market-access",
        "metric": "flood-market-access-index ranking + alt-metric stability",
        "common_top5_across_metrics": common,
        "runs": runs,
    })


def main():
    print("=== coastal-informal-risk ==="); run_coastal()
    print("=== invisible-urbanization ==="); run_urb()
    print("=== flood-market-access ==="); run_flood()


if __name__ == "__main__":
    main()
