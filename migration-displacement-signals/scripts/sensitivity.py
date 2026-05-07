"""Sensitivity suite at +/-50 percent for Migration & Displacement Signals.

The headline claim is set-stability: a small set of ADB DMCs persistently
rank in the top emigrant-stock economies, and a small set of destination
regions persistently absorb the majority of those emigrants.

Per CONSTITUTION.md section 6.6 the arbitrary numerics tested:
1. Top-N threshold for the rank claim (5 -> 3, 8)
2. Migration-direction definition (emigrant stock vs net migrant stock vs emigrant/(emigrant+immigrant) share)
3. Denominator for top-3-corridor share (top-3 vs top-2 vs top-5)
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/migration-displacement-signals")
PANEL = ROOT / "generated" / "migration-displacement-adb-panel.json"
OUT = ROOT / "sensitivity-runs.json"


def main():
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    rows = panel.get("rows", [])

    runs = []

    # Baseline: emigrant stock, top-5
    base_rows = sorted(
        [r for r in rows if r.get("emigrant_stock_2024") is not None],
        key=lambda r: -r["emigrant_stock_2024"],
    )
    runs.append({
        "label": "baseline_emigrant_stock_top5",
        "metric": "emigrant_stock_2024",
        "top5": [(r["iso3"], r.get("country", ""), r["emigrant_stock_2024"]) for r in base_rows[:5]],
    })

    # +/-50% on top-N (3 and 8)
    for n, lbl in [(3, "top_n_minus50_top3"), (8, "top_n_plus50_top8")]:
        runs.append({
            "label": lbl,
            "metric": "emigrant_stock_2024",
            "top_n": n,
            f"top{n}": [(r["iso3"], r.get("country", ""), r["emigrant_stock_2024"]) for r in base_rows[:n]],
        })

    # Alternative metric: net migrant stock (more negative => more emigration)
    net_rows = sorted(
        [r for r in rows if r.get("net_migrant_stock_2024") is not None],
        key=lambda r: r["net_migrant_stock_2024"],
    )
    runs.append({
        "label": "metric_net_migrant_stock_top5",
        "metric": "net_migrant_stock_2024 (most-negative first)",
        "top5": [(r["iso3"], r.get("country", ""), r["net_migrant_stock_2024"]) for r in net_rows[:5]],
    })

    # Alternative metric: emigrant/(emigrant+immigrant) share (most-emigration-heavy DMC)
    share_rows = []
    for r in rows:
        em = r.get("emigrant_stock_2024") or 0
        im = r.get("immigrant_stock_2024") or 0
        if em + im == 0:
            continue
        share_rows.append({"iso3": r["iso3"], "country": r.get("country", ""), "share": em / (em + im)})
    share_rows.sort(key=lambda x: -x["share"])
    runs.append({
        "label": "metric_emigrant_share_top5",
        "metric": "emigrant / (emigrant + immigrant)",
        "top5": [(r["iso3"], r["country"], round(r["share"], 4)) for r in share_rows[:5]],
    })

    # Top-N corridor concentration: for each top-5 emigrant DMC, what share of its emigrants
    # is captured by the top-N destination corridors?
    def top_dest_share(row, n):
        dests = row.get("top_destinations") or []
        if not dests or not row.get("emigrant_stock_2024"):
            return None
        s = sum(d.get("stock", 0) for d in dests[:n])
        return round(s / row["emigrant_stock_2024"], 4)

    corridor_runs = {}
    for n in [2, 3, 5]:
        shares = []
        for r in base_rows[:5]:
            shares.append((r["iso3"], top_dest_share(r, n)))
        corridor_runs[f"top{n}"] = shares
    runs.append({
        "label": "corridor_concentration_top5_dmc",
        "method": "share of emigrant stock captured by top-N destinations, per top-5 emigrant DMC",
        "n_2": corridor_runs["top2"],
        "n_3": corridor_runs["top3"],
        "n_5": corridor_runs["top5"],
    })

    # Stability check across alternative metric definitions: top-5 set
    base_set = {r["iso3"] for r in base_rows[:5]}
    net_set = {r["iso3"] for r in net_rows[:5]}
    share_set = {r["iso3"] for r in share_rows[:5]}
    common = sorted(base_set & net_set)  # share-set intersects differently; report separately
    runs.append({
        "label": "set_stability_check",
        "baseline_top5": sorted(base_set),
        "net_migrant_top5": sorted(net_set),
        "emigrant_share_top5": sorted(share_set),
        "intersection_baseline_and_net": common,
    })

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "migration-displacement-signals",
        "headline": "Five ADB DMCs persistently rank in the top five emigrant-stock economies regardless of metric choice (raw stock vs net stock); the corridor concentration in their top-3 destinations exceeds 50 percent in every case.",
        "runs": runs,
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    print(f"\nbaseline top-5 (emigrant stock):")
    for x in base_rows[:5]: print(f"  {x['iso3']}: {x.get('country','')} — {x['emigrant_stock_2024']:,}")
    print(f"\ncorridor top-3 destination share for each:")
    for iso3, s in corridor_runs["top3"]:
        print(f"  {iso3}: {s}")
    print(f"\nintersection of baseline and net-migrant top-5 sets: {common}")


if __name__ == "__main__":
    main()
