"""Reformulated food-price index.

The old single-composite index failed the +/-50 percent sensitivity gate
(no stable top-5 across alternative sub-metric formulations). The
reformulation: instead of averaging, use the *intersection* of two
rankings — DMCs in the top-N of both CPI inflation AND ag-imports
share. This is a joint-vulnerability qualifier, not a score.
"""
import json
import csv
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/food-price-climate-transmission")
PANEL = ROOT / "generated/food-price-adb-panel.json"


def main():
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    rows = panel["rows"]

    cpi_ranked = sorted([r for r in rows if r.get("cpi_inflation_pct") is not None],
                        key=lambda r: -r["cpi_inflation_pct"])
    imp_ranked = sorted([r for r in rows if r.get("ag_imports_pct_merch") is not None],
                        key=lambda r: -r["ag_imports_pct_merch"])

    out_rows = []
    for r in rows:
        cpi_rank = next((i + 1 for i, x in enumerate(cpi_ranked) if x["iso3"] == r["iso3"]), None)
        imp_rank = next((i + 1 for i, x in enumerate(imp_ranked) if x["iso3"] == r["iso3"]), None)
        out_rows.append({
            "iso3": r["iso3"],
            "country": r["country"],
            "cpi_inflation_pct": round(r["cpi_inflation_pct"], 2) if r.get("cpi_inflation_pct") is not None else None,
            "ag_imports_pct_merch": round(r["ag_imports_pct_merch"], 2) if r.get("ag_imports_pct_merch") is not None else None,
            "cpi_rank": cpi_rank,
            "imp_rank": imp_rank,
            "max_rank": max(cpi_rank, imp_rank) if (cpi_rank and imp_rank) else None,
            "joint_qualifier_top5": (cpi_rank is not None and cpi_rank <= 5 and imp_rank is not None and imp_rank <= 5),
            "joint_qualifier_top8": (cpi_rank is not None and cpi_rank <= 8 and imp_rank is not None and imp_rank <= 8),
        })

    out_rows.sort(key=lambda r: r["max_rank"] if r["max_rank"] is not None else 999)

    qualifying_top5 = [r for r in out_rows if r["joint_qualifier_top5"]]
    qualifying_top8 = [r for r in out_rows if r["joint_qualifier_top8"]]

    payload = {
        "program": "food-price-climate-transmission",
        "claim_scope": (
            "Reformulated food-price vulnerability: DMCs in the top-N of "
            "BOTH WDI CPI inflation AND ag-imports-share-of-merchandise. "
            "Joint qualifier, not a composite score."
        ),
        "framing_rule": "Joint food-price vulnerability qualifier. Constitution §13.3 / §14.",
        "sources": {
            "wdi_cpi": "WDI FP.CPI.TOTL.ZG (CC BY 4.0)",
            "wdi_ag_imports": "WDI TM.VAL.AGRI.ZS.UN (CC BY 4.0)",
            "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        },
        "methodology": {
            "joint_qualifier_topN": "DMC qualifies if it is in the top-N of CPI inflation AND in the top-N of ag-imports-share. Set-based, not score-based.",
        },
        "qualifying_top5": [r["iso3"] for r in qualifying_top5],
        "qualifying_top8": [r["iso3"] for r in qualifying_top8],
        "rows": out_rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    out_dir = ROOT / "generated"
    (out_dir / "food-price-reformulated-adb-panel.json").write_text(json.dumps(payload, indent=2))
    with open(out_dir / "food-price-reformulated-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        for row in out_rows: w.writerow(row)

    print(f"qualifying top-5 (intersection): {[r['iso3'] for r in qualifying_top5]}")
    print(f"qualifying top-8 (intersection): {[r['iso3'] for r in qualifying_top8]}")

    # Sensitivity: top-3 / top-5 / top-8 / top-10
    runs = []
    for n in [3, 5, 8, 10]:
        cpi_set = {r["iso3"] for r in cpi_ranked[:n]}
        imp_set = {r["iso3"] for r in imp_ranked[:n]}
        joint = sorted(cpi_set & imp_set)
        runs.append({"label": f"top_{n}_intersection", "n": n, "set": joint})

    sens_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "food-price-climate-transmission",
        "metric": "joint top-N intersection of CPI-inflation and ag-imports rankings",
        "decision_rule": "Positive if a non-empty stable set is recovered across N choices in [3, 10].",
        "runs": runs,
        "common_set_across_runs": sorted(set.intersection(*[set(r["set"]) for r in runs])) if all(r["set"] for r in runs) else [],
    }
    (ROOT / "sensitivity-runs.json").write_text(json.dumps(sens_payload, indent=2))

    print("\nIntersection across top-N choices:")
    for r in runs:
        print(f"  top-{r['n']}: {r['set']}")
    print(f"\nCommon set across all N: {sens_payload['common_set_across_runs']}")


if __name__ == "__main__":
    main()
