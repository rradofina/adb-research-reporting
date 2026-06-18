"""Remittance Resilience — deepening pass: fragility on a ROBUST (median)
corridor cost, not an outlier-contaminated MEAN.

Answers the keystone-adjacent question in `remittance-resilience/deep-questions.md`
§1.2 (the negative-cost question). The committed cluster ranks on a
*destination-mean* corridor cost, but RPW quote sets can contain negative
observations and high caps. A single such quote can drag an arithmetic mean
down or up, making "mean corridor cost" a poor central tendency for a thin,
skewed quote set.

This script re-reads the SAME committed public source the headline uses
(World Bank Remittance Prices Worldwide, Q1 2025 dataset, in the program
cache), reproduces the destination-cost aggregation that
`process-remittance.py` performs (same sheet, same `cc1 total cost %`
column, same corrected RPW normalization, same latest-period filter), and then
recomputes the fragility index

    fragility = min(dependence / 25, 1) * min(cost / 15, 1) * 100

substituting a robust MEDIAN cost for the mean. It re-ranks all economies
and reports:
  (a) how the headline top-5 cluster {KGZ, WSM, TON, VUT, NPL} moves under
      mean -> median;
  (b) the count of negative and sub-1% corridor quotes per cluster economy,
      straight from the cached workbook; and
  (c) the remaining negative observations after repair, without magnifying
      already-percentage negative values.

Every number below is produced here from on-disk data only. Outbound network
is not used. No figure is supplied by the model. The fragility index is a
triage measure per CONSTITUTION.md §6.4, not a final risk rating; framing is
a corridor-cost x macro-dependence measurement signal per §13.3, not a
country-quality ranking. attestation_chain: ai-first.
"""
import csv
import json
import os
import statistics
from collections import defaultdict
from datetime import datetime, timezone

import openpyxl

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/remittance-resilience"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

# Identical DMC roster + identical caps as process-remittance.py.
ADB_DMCS = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan", "BGD": "Bangladesh", "BTN": "Bhutan",
    "BRN": "Brunei Darussalam", "KHM": "Cambodia", "CHN": "China, People's Republic of",
    "COK": "Cook Islands", "FJI": "Fiji", "GEO": "Georgia", "HKG": "Hong Kong, China",
    "IND": "India", "IDN": "Indonesia", "KAZ": "Kazakhstan", "KIR": "Kiribati",
    "KGZ": "Kyrgyz Republic", "LAO": "Lao People's Democratic Republic",
    "MYS": "Malaysia", "MDV": "Maldives", "MHL": "Marshall Islands", "FSM": "Micronesia, Federated States of",
    "MNG": "Mongolia", "MMR": "Myanmar", "NRU": "Nauru", "NPL": "Nepal", "NIU": "Niue",
    "PAK": "Pakistan", "PLW": "Palau", "PNG": "Papua New Guinea", "PHL": "Philippines",
    "WSM": "Samoa", "SLB": "Solomon Islands", "LKA": "Sri Lanka", "TJK": "Tajikistan",
    "THA": "Thailand", "TLS": "Timor-Leste", "TON": "Tonga", "TKM": "Turkmenistan",
    "TUV": "Tuvalu", "UZB": "Uzbekistan", "VUT": "Vanuatu", "VNM": "Viet Nam",
    "TPE": "Taipei,China",
}
DEP_CAP = 25.0
COST_CAP = 15.0
HEADLINE_TOP5 = ["KGZ", "WSM", "TON", "VUT", "NPL"]  # committed cluster (process-remittance.py output)


def normalize_rpw_cost(raw):
    """Corrected RPW normalization: scale only nonnegative fractions."""
    value = float(raw)
    return value * 100 if 0 <= value <= 1 else value


def fragility(dep, cost):
    """Identical functional form to process-remittance.py / sensitivity.py."""
    if dep is None or cost is None:
        return None
    n_dep = min(dep / DEP_CAP, 1.0)
    n_cost = min(cost / COST_CAP, 1.0)  # caps at the SDG-ceiling band; negatives -> <=0
    if n_cost < 0:
        n_cost = 0.0  # a negative robust cost floors the cost axis at 0 (cannot be "fragile" on free transfers)
    return round(n_dep * n_cost * 100, 1)


def load_rpw_quotes():
    """Re-read the cached RPW workbook as process-remittance.py does.

    Returns a list of dicts: one per ADB-DMC-bound quote with its raw and
    normalized cost, so we can reproduce the headline mean and diagnose
    remaining negative observations.
    """
    print("Loading RPW xlsx from program cache (~49 MB; ~20 s)...")
    wb = openpyxl.load_workbook(
        f"{CACHE}/rpw_dataset_2011_2025_q1.xlsx", read_only=True, data_only=True
    )
    ws = wb["Dataset (from Q2 2016)"]
    rows = ws.iter_rows(values_only=True)
    header = next(rows)
    cols = {h: i for i, h in enumerate(header) if h is not None}
    obs = []
    for row in rows:
        if row[cols["destination_code"]] not in ADB_DMCS:
            continue
        cost = row[cols["cc1 total cost %"]]
        if cost is None or not isinstance(cost, (int, float)):
            continue
        raw = float(cost)
        norm = normalize_rpw_cost(raw)
        obs.append({
            "period": row[cols["period"]],
            "src": row[cols["source_code"]],
            "dst": row[cols["destination_code"]],
            "firm": row[cols["firm"]],
            "raw_cost": raw,
            "cost_pct": norm,
        })
    wb.close()
    print(f"  {len(obs)} ADB-DMC-bound quotes loaded (all periods)")
    return obs


def load_wdi():
    """Latest WDI remittance %GDP per DMC — identical loader to the headline."""
    with open(f"{CACHE}/wdi_remittance_pct_gdp.json", encoding="utf-8") as f:
        d = json.load(f)
    rows = d[1]
    latest = {}
    for row in rows:
        if not isinstance(row.get("value"), (int, float)):
            continue
        iso3 = row.get("countryiso3code")
        if not iso3 or iso3 not in ADB_DMCS:
            continue
        year = int(row.get("date"))
        if iso3 not in latest or year > latest[iso3]["year"]:
            latest[iso3] = {"year": year, "value": float(row["value"])}
    return latest


def main():
    quotes = load_rpw_quotes()
    wdi = load_wdi()

    # Same latest-period filter as the headline.
    periods = sorted(set(o["period"] for o in quotes))
    latest = periods[-1] if periods else None
    obs = [o for o in quotes if o["period"] == latest]
    print(f"Latest RPW period in ADB-DMC subset: {latest}  ({len(obs)} quotes)\n")

    # Group destination-bound quotes (the headline's unit of aggregation).
    by_dst = defaultdict(list)
    for o in obs:
        by_dst[o["dst"]].append(o)

    rows = []
    for iso3, name in ADB_DMCS.items():
        oq = by_dst.get(iso3, [])
        costs = [o["cost_pct"] for o in oq]
        wdi_e = wdi.get(iso3)
        dep = wdi_e["value"] if wdi_e else None
        if not costs:
            continue
        corridors = sorted(set(o["src"] for o in oq))
        # Per-corridor median of normalized quotes, then median across corridors
        # (equal-weight corridors, robust within corridor).
        corr_meds = []
        for s in corridors:
            cc = [o["cost_pct"] for o in oq if o["src"] == s]
            corr_meds.append(statistics.median(cc))
        mean_cost = round(statistics.mean(costs), 2)                 # headline measure (reproduced)
        median_quote = round(statistics.median(costs), 2)           # robust: median over all dest quotes
        median_corr = round(statistics.median(corr_meds), 2)        # robust: median of per-corridor medians
        n_neg = sum(1 for c in costs if c < 0)
        n_sub1 = sum(1 for c in costs if 0 <= c < 1)
        rows.append({
            "iso3": iso3, "country": name,
            "dep_pct_gdp": round(dep, 2) if dep is not None else None,
            "wdi_year": wdi_e["year"] if wdi_e else None,
            "n_corridors": len(corridors),
            "n_quotes": len(costs),
            "n_neg_quotes": n_neg,
            "n_sub1_quotes": n_sub1,
            "min_quote": round(min(costs), 2),
            "max_quote": round(max(costs), 2),
            "mean_cost": mean_cost,
            "median_quote": median_quote,
            "median_corr": median_corr,
            "frag_mean": fragility(dep, mean_cost),
            "frag_median_quote": fragility(dep, median_quote),
            "frag_median_corr": fragility(dep, median_corr),
        })

    # Three rankings: headline (mean) vs robust (two median variants).
    ranked_mean = sorted([r for r in rows if r["frag_mean"] is not None],
                         key=lambda r: -r["frag_mean"])
    ranked_mq = sorted([r for r in rows if r["frag_median_quote"] is not None],
                       key=lambda r: -r["frag_median_quote"])
    ranked_mc = sorted([r for r in rows if r["frag_median_corr"] is not None],
                       key=lambda r: -r["frag_median_corr"])

    top5_mean = [r["iso3"] for r in ranked_mean[:5]]
    top5_mq = [r["iso3"] for r in ranked_mq[:5]]
    top5_mc = [r["iso3"] for r in ranked_mc[:5]]

    def rankpos(ranked, iso):
        for i, r in enumerate(ranked, 1):
            if r["iso3"] == iso:
                return i
        return None

    # ----- console report -----
    print("=== Headline top-5 (MEAN corridor cost), reproduced from cache:")
    print("   ", top5_mean)
    print("=== Robust top-5 (MEDIAN over destination quotes):")
    print("   ", top5_mq)
    print("=== Robust top-5 (MEDIAN of per-corridor medians):")
    print("   ", top5_mc)
    dropped_mq = [i for i in top5_mean if i not in top5_mq]
    entered_mq = [i for i in top5_mq if i not in top5_mean]
    dropped_mc = [i for i in top5_mean if i not in top5_mc]
    entered_mc = [i for i in top5_mc if i not in top5_mean]
    print(f"\nmean->median(quote): dropped {dropped_mq}  entered {entered_mq}")
    print(f"mean->median(corr) : dropped {dropped_mc}  entered {entered_mc}")

    print("\n--- Headline cluster members: cost + rank under each measure ---")
    print(f"{'iso':<4} {'dep%':>6} {'meanC':>7} {'medQ':>6} {'medC':>6} "
          f"{'fMean':>6} {'fMedQ':>6} {'fMedC':>6} {'rMean':>5} {'rMedQ':>5} {'rMedC':>5}")
    for iso in HEADLINE_TOP5:
        r = next((x for x in rows if x["iso3"] == iso), None)
        if not r:
            print(f"{iso:<4}  (no RPW quotes in latest period)")
            continue
        print(f"{r['iso3']:<4} {r['dep_pct_gdp']:>6} {r['mean_cost']:>7} "
              f"{r['median_quote']:>6} {r['median_corr']:>6} "
              f"{str(r['frag_mean']):>6} {str(r['frag_median_quote']):>6} "
              f"{str(r['frag_median_corr']):>6} "
              f"{str(rankpos(ranked_mean, iso)):>5} {str(rankpos(ranked_mq, iso)):>5} "
              f"{str(rankpos(ranked_mc, iso)):>5}")

    print("\n--- Negative / sub-1% quote counts per cluster economy (from cache) ---")
    print(f"{'iso':<4} {'n_quotes':>9} {'n_neg':>6} {'n_sub1':>7} {'min_quote':>10} {'max_quote':>10}")
    for iso in HEADLINE_TOP5:
        r = next((x for x in rows if x["iso3"] == iso), None)
        if not r:
            continue
        print(f"{r['iso3']:<4} {r['n_quotes']:>9} {r['n_neg_quotes']:>6} {r['n_sub1_quotes']:>7} "
              f"{r['min_quote']:>10} {r['max_quote']:>10}")

    # Same panel-wide negative tally for context (all DMCs with quotes).
    tot_neg = sum(r["n_neg_quotes"] for r in rows)
    tot_q = sum(r["n_quotes"] for r in rows)
    print(f"\nPanel-wide: {tot_neg} negative quotes out of {tot_q} "
          f"({100*tot_neg/tot_q:.2f}%) across {len(rows)} DMCs with RPW coverage.")

    # ----- corrected-normalization diagnostic -----
    print("\n--- Negative observations after corrected RPW normalization ---")
    extreme = sorted([o for o in obs if o["cost_pct"] < 0],
                     key=lambda o: o["cost_pct"])
    print(f"{len(extreme)} latest-period quotes remain negative. Most extreme 8:")
    print(f"{'dst':<4} {'src':<4} {'raw_cc1':>10} {'normalized':>11}  multiplied_by_100?")
    for o in extreme[:8]:
        mult = "yes" if 0 <= o["raw_cost"] <= 1 else "no"
        print(f"{o['dst']:<4} {str(o['src']):<4} {o['raw_cost']:>10} "
              f"{o['cost_pct']:>11}  {mult}")

    # ----- write artifact -----
    payload = {
        "program": "remittance-resilience",
        "analysis": "fragility on robust (median) corridor cost vs outlier-contaminated mean",
        "claim_scope": (
            "Deepening of the mean-cost fragility screen. Recomputes the identical "
            "fragility index on a robust median corridor cost instead of the "
            "arithmetic mean, re-ranks all DMCs, and tallies negative / sub-1% "
            "quotes per cluster economy. Triage measure (CONSTITUTION.md §6.4), not "
            "a risk rating; measurement-gap framing per §13.3."
        ),
        "source": {
            "name": "World Bank Remittance Prices Worldwide, Q1 2025 dataset",
            "file": "rpw_dataset_2011_2025_q1.xlsx (program cache)",
            "sheet": "Dataset (from Q2 2016)",
            "cost_field": "cc1 total cost %",
            "normalization": "raw*100 if 0 <= raw <= 1 else raw (identical to repaired process-remittance.py)",
            "wdi": "WDI BX.TRF.PWKR.DT.GD.ZS, latest available year per DMC (program cache)",
            "license": "World Bank open / CC BY 4.0",
            "retrieved_at": "2026-04-25 (program cache)",
            "latest_period": latest,
        },
        "caps": {"dep_cap": DEP_CAP, "cost_cap": COST_CAP},
        "headline_top5_mean": top5_mean,
        "robust_top5_median_quote": top5_mq,
        "robust_top5_median_corridor": top5_mc,
        "dropped_on_median_quote": dropped_mq,
        "entered_on_median_quote": entered_mq,
        "dropped_on_median_corridor": dropped_mc,
        "entered_on_median_corridor": entered_mc,
        "panel_negative_quotes": tot_neg,
        "panel_total_quotes": tot_q,
        "rows_by_frag_mean": ranked_mean,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/remittance-median-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    flat_fields = ["iso3", "country", "dep_pct_gdp", "wdi_year", "n_corridors",
                   "n_quotes", "n_neg_quotes", "n_sub1_quotes", "min_quote",
                   "max_quote", "mean_cost", "median_quote", "median_corr",
                   "frag_mean", "frag_median_quote", "frag_median_corr"]
    with open(f"{OUT}/remittance-median-deepening.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flat_fields)
        w.writeheader()
        for r in ranked_mean:
            w.writerow({k: r[k] for k in flat_fields})

    print(f"\nWrote {OUT}/remittance-median-deepening.json + .csv")


if __name__ == "__main__":
    main()
