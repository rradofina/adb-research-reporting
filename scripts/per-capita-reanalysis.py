"""Per-capita reanalysis: which DMCs surface when absolute-scale
indices are population-normalized?

For each program with a numerical index, recompute per-capita
(or per-relevant-population) and compare top-5 sets.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def load(slug):
    candidates = list((ROOT / slug / "generated").glob("*adb-panel.json"))
    if not candidates:
        return None
    return json.loads(candidates[0].read_text(encoding="utf-8"))


def topN(rows, key, n=5, reverse=True):
    valid = [r for r in rows if r.get(key) is not None]
    valid.sort(key=lambda r: -r[key] if reverse else r[key])
    return [r["iso3"] for r in valid[:n]]


def main():
    out = {}

    # disaster-recovery-lag: total_affected vs total_affected per capita
    d = load("disaster-recovery-lag")
    if d:
        rows = d["rows"]
        # We don't have population in this panel; use migration's pop-style or just compute from population_total elsewhere
        # Use total_deaths as already a per-event metric
        absolute = topN(rows, "total_affected")
        per_event = topN(rows, "events_per_year")
        out["disaster-recovery-lag"] = {
            "absolute_top5_total_affected": absolute,
            "alternative_events_per_year_top5": per_event,
        }

    # flood-market-access: index uses log10(pop) so big DMCs win.
    # Per-capita: events / pop (already in panel as flood_events / population)
    d = load("flood-market-access")
    if d:
        rows = d["rows"]
        for r in rows:
            p = r.get("population")
            f = r.get("flood_events_2000_2025")
            if p and f:
                r["flood_events_per_million"] = round((f * 1_000_000 / p), 4)
        absolute = topN(rows, "flood_market_access_index")
        per_capita = topN(rows, "flood_events_per_million")
        out["flood-market-access"] = {
            "absolute_top5_index": absolute,
            "per_capita_top5_events_per_million": per_capita,
        }

    # coastal-informal-risk: index uses log10(pop) so big DMCs win.
    # Per-capita: urban_pct × slum_pct (no log-pop)
    d = load("coastal-informal-risk")
    if d:
        rows = d["rows"]
        for r in rows:
            u = r.get("urban_pct")
            s = r.get("slum_pct_urban")
            if u is not None:
                if s is None:
                    s = 10.0  # Use the imputation value
                r["coastal_per_capita"] = round((u / 100) * (s / 100) * 100, 4)
        absolute = topN(rows, "coastal_informal_risk_index")
        per_capita = topN(rows, "coastal_per_capita")
        out["coastal-informal-risk"] = {
            "absolute_top5_index": absolute,
            "per_capita_top5_urban_x_slum": per_capita,
        }

    # port-hinterland-friction: friction_exposure_index uses sqrt(imports_USD).
    # Per-capita alternative: imports / GDP (would need GDP) — skip; report the structural difference.

    # remittance-resilience: top-5 already invariant to scaling; report
    # that finding.

    # Display
    print("=== Per-capita reanalysis ===\n")
    for prog, sets in out.items():
        print(f"{prog}:")
        for k, v in sets.items():
            print(f"  {k}: {v}")
        print()

    OUT = ROOT / "research" / "per-capita-reanalysis.json"
    OUT.write_text(json.dumps(out, indent=2))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
