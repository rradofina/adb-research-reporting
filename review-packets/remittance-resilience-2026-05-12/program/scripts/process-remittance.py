"""Program 14 — Remittance Resilience.

Combines:
  - World Bank Remittance Prices Worldwide (RPW) Q1 2025 dataset
  - World Bank WDI BX.TRF.PWKR.DT.GD.ZS (personal remittances received, % GDP)

For each ADB regional DMC, computes:
  - latest WDI remittance %GDP (a measure of dependence)
  - mean / median inbound transfer cost across corridors in latest RPW period
  - "remittance fragility index" combining the two

Status: hypothesis-stage screening artifact, owner sign-off pending.
"""
import json, csv, os, statistics
from collections import defaultdict
from datetime import datetime, timezone

import openpyxl

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/remittance-resilience/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/remittance-resilience/generated"
os.makedirs(OUT, exist_ok=True)

# ADB regional DMCs (50 economies)
ADB_DMCS = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China, People's Republic of",
    "COK":"Cook Islands","FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong, China",
    "IND":"India","IDN":"Indonesia","KAZ":"Kazakhstan","KIR":"Kiribati",
    "KGZ":"Kyrgyz Republic","LAO":"Lao People's Democratic Republic",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia, Federated States of",
    "MNG":"Mongolia","MMR":"Myanmar","NRU":"Nauru","NPL":"Nepal","NIU":"Niue",
    "PAK":"Pakistan","PLW":"Palau","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam",
    "TPE":"Taipei,China",
}


def load_rpw():
    """Load RPW main dataset; return list of corridor observations."""
    print("Loading RPW xlsx (~49 MB; takes ~20 sec)...")
    wb = openpyxl.load_workbook(f"{CACHE}/rpw_dataset_2011_2025_q1.xlsx",
                                 read_only=True, data_only=True)
    ws = wb["Dataset (from Q2 2016)"]
    rows = ws.iter_rows(values_only=True)
    header = next(rows)
    cols = {h: i for i, h in enumerate(header) if h is not None}
    obs = []
    for row in rows:
        if row[cols["destination_code"]] not in ADB_DMCS:
            continue
        period = row[cols["period"]]
        cost = row[cols["cc1 total cost %"]]
        if cost is None or not isinstance(cost, (int, float)):
            continue
        obs.append({
            "period": period,
            "src": row[cols["source_code"]],
            "src_name": row[cols["source_name"]],
            "dst": row[cols["destination_code"]],
            "dst_name": row[cols["destination_name"]],
            "firm": row[cols["firm"]],
            "firm_type": row[cols["firm_type"]],
            "payment": row[cols["payment instrument"]],
            "access_point": row[cols["access point"]],
            "cost_pct": float(cost) * 100 if cost <= 1 else float(cost),  # normalize: file mixes 0.05 and 5.0
            "amount_usd": row[cols["cc1 denomination amount"]],
        })
    print(f"  {len(obs)} ADB-DMC-bound observations loaded")
    return obs


def latest_period(obs):
    periods = sorted(set(o["period"] for o in obs))
    return periods[-1] if periods else None


def load_wdi_pct_gdp():
    """Load WDI remittance % GDP per country, latest available year."""
    with open(f"{CACHE}/wdi_remittance_pct_gdp.json", encoding="utf-8") as f:
        d = json.load(f)
    if not isinstance(d, list) or len(d) < 2:
        return {}
    rows = d[1]
    latest = {}
    for row in rows:
        if not isinstance(row.get("value"), (int, float)):
            continue
        iso3 = row.get("countryiso3code")
        if not iso3 or iso3 not in ADB_DMCS:
            continue
        year = int(row.get("date"))
        val = float(row["value"])
        if iso3 not in latest or year > latest[iso3]["year"]:
            latest[iso3] = {"year": year, "value": val}
    return latest


def main():
    rpw = load_rpw()
    wdi = load_wdi_pct_gdp()
    latest = latest_period(rpw)
    print(f"Latest RPW period in ADB-DMC subset: {latest}")
    obs_latest = [o for o in rpw if o["period"] == latest]
    print(f"  observations in latest period: {len(obs_latest)}")

    # Per-DMC inbound transfer cost (across all corridors for that DMC as destination)
    by_dst = defaultdict(list)
    for o in obs_latest:
        by_dst[o["dst"]].append(o)

    rows = []
    for iso3, name in sorted(ADB_DMCS.items(), key=lambda x: x[1]):
        rpw_obs = by_dst.get(iso3, [])
        wdi_entry = wdi.get(iso3)
        costs = [o["cost_pct"] for o in rpw_obs]
        corridors = sorted(set((o["src"], o["dst"]) for o in rpw_obs))
        firms = len(set(o["firm"] for o in rpw_obs))

        if costs:
            mean_cost = round(statistics.mean(costs), 2)
            median_cost = round(statistics.median(costs), 2)
            min_cost = round(min(costs), 2)
            max_cost = round(max(costs), 2)
        else:
            mean_cost = median_cost = min_cost = max_cost = None

        # Fragility index: high dependence × high cost
        # Normalize WDI %GDP into [0,1] using 0–25% range; cost into [0,1] using 0–15% range.
        # Cap at 1.0; combine multiplicatively × 100.
        if wdi_entry and mean_cost is not None:
            dep_norm = min((wdi_entry["value"] or 0) / 25.0, 1.0)
            cost_norm = min(mean_cost / 15.0, 1.0)
            fragility = round((dep_norm * cost_norm) * 100, 1)
        else:
            fragility = None

        rows.append({
            "iso3": iso3, "country": name,
            "wdi_remittance_pct_gdp": round(wdi_entry["value"], 2) if wdi_entry else None,
            "wdi_year": wdi_entry["year"] if wdi_entry else None,
            "rpw_period": latest if rpw_obs else None,
            "rpw_corridors_observed": len(corridors),
            "rpw_firms_observed": firms if firms > 0 else None,
            "rpw_mean_cost_pct": mean_cost,
            "rpw_median_cost_pct": median_cost,
            "rpw_min_cost_pct": min_cost,
            "rpw_max_cost_pct": max_cost,
            "fragility_index": fragility,
        })

    # Sort: highest fragility first
    rows.sort(key=lambda r: -(r["fragility_index"] or -1))

    # Top corridors by destination
    top_corridors = []
    for o in obs_latest:
        top_corridors.append({
            "src":o["src"],"src_name":o["src_name"],
            "dst":o["dst"],"dst_name":o["dst_name"],
            "firm":o["firm"],"firm_type":o["firm_type"],
            "payment":o["payment"],"cost_pct":round(o["cost_pct"],2),
            "amount_usd":o["amount_usd"],"period":o["period"],
        })
    top_corridors.sort(key=lambda x: -x["cost_pct"])

    # Aggregate by source corridor (for top "expensive" corridors)
    corridor_avg = defaultdict(list)
    for o in obs_latest:
        corridor_avg[(o["src"], o["src_name"], o["dst"], o["dst_name"])].append(o["cost_pct"])
    corridors_summary = []
    for (s, sn, d, dn), costs in corridor_avg.items():
        corridors_summary.append({
            "source_iso3": s, "source": sn,
            "dest_iso3": d, "dest": dn,
            "n_quotes": len(costs),
            "mean_cost_pct": round(statistics.mean(costs), 2),
            "median_cost_pct": round(statistics.median(costs), 2),
            "min_cost_pct": round(min(costs), 2),
            "max_cost_pct": round(max(costs), 2),
        })
    corridors_summary.sort(key=lambda x: -x["mean_cost_pct"])

    payload = {
        "program": "remittance-resilience",
        "claim_scope": (
            "Hypothesis-stage screening result combining RPW Q1 2025 transfer-"
            "cost observations and latest available WDI BX.TRF.PWKR.DT.GD.ZS "
            "(remittances % GDP). Owner sign-off pending."
        ),
        "framing_rule": (
            "Measurement-gap and dependency signal, not a country quality "
            "ranking. Per CONSTITUTION.md §13.3 §14, framing is 'corridor-cost "
            "× macro-dependence vulnerability', not 'fragile country'."
        ),
        "sources": {
            "rpw": {
                "name": "World Bank Remittance Prices Worldwide",
                "version": "Q1 2025 dataset",
                "url": "https://remittanceprices.worldbank.org/data-download",
                "file": "rpw_dataset_2011_2025_q1.xlsx",
                "license": "World Bank open; attribution: 'The World Bank, Remittance Prices Worldwide, available at remittanceprices.worldbank.org'",
                "retrieved_at": "2026-04-25",
                "rows_in_period": len(obs_latest),
                "period": latest,
            },
            "wdi": {
                "name": "World Bank WDI BX.TRF.PWKR.DT.GD.ZS — Personal remittances received (% GDP)",
                "url": "https://api.worldbank.org/v2/country/all/indicator/BX.TRF.PWKR.DT.GD.ZS",
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
                "year_window": "2015–2024",
                "countries_with_value": len(wdi),
            },
        },
        "methodology": {
            "fragility_index": (
                "Multiplicative combination of normalized dependence and "
                "normalized inbound transfer cost: "
                "min(wdi_pct_gdp / 25.0, 1.0) × min(mean_cost_pct / 15.0, 1.0) × 100. "
                "Score 0–100. Triage measure, not a final risk rating."
            ),
        },
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rows": rows,
        "expensive_corridors_top50": corridors_summary[:50],
        "totals": {
            "dmcs_with_wdi": sum(1 for r in rows if r["wdi_remittance_pct_gdp"] is not None),
            "dmcs_with_rpw": sum(1 for r in rows if r["rpw_mean_cost_pct"] is not None),
            "dmcs_with_both": sum(1 for r in rows if r["fragility_index"] is not None),
        },
    }

    with open(f"{OUT}/remittance-resilience-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/remittance-resilience-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)

    print("\n=== Top 10 most-fragile DMCs ===")
    for r in rows[:10]:
        print(f"  {r['iso3']:<4} {r['country'][:30]:<30} dep={r['wdi_remittance_pct_gdp']}% cost={r['rpw_mean_cost_pct']}% frag={r['fragility_index']}")
    print(f"\nWrote {OUT}/remittance-resilience-adb-panel.json + .csv")


if __name__ == "__main__":
    main()
