"""Program 7 — Disaster Recovery Lag.

Hypothesis-stage screening artifact using EM-DAT country profiles
(Centre for Research on the Epidemiology of Disasters) via the HDX mirror.

Per-DMC aggregates:
  - Total events 2000-2025 by disaster type
  - Total people affected, deaths, damage USD (CPI-adjusted)
  - Annual event frequency
  - Damage burden as % of latest GDP (proxy for "recovery lag" pressure)

This is NOT yet a recovery-lag metric (which would compare event timing to
indicator-recovery curves). It is a structural-burden layer that the lag
analysis will sit on top of.
"""
import json, csv, os
from collections import defaultdict
from datetime import datetime, timezone

import openpyxl

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/disaster-recovery-lag/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/disaster-recovery-lag/generated"
os.makedirs(OUT, exist_ok=True)

ADB_DMCS = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China",
    "FJI":"Fiji","GEO":"Georgia",
    "IND":"India","IDN":"Indonesia","KAZ":"Kazakhstan","KIR":"Kiribati",
    "KGZ":"Kyrgyzstan","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia, Fed. Sts.",
    "MNG":"Mongolia","MMR":"Myanmar","NPL":"Nepal",
    "PAK":"Pakistan","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam",
}

def main():
    wb = openpyxl.load_workbook(f"{CACHE}/emdat_country_profiles.xlsx", data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    cols = {h: i for i, h in enumerate(header)}
    # Skip header (row 0) and the HXL/structure marker (row 1, "#date +occurred")
    data_rows = rows[2:]
    # Filter to ADB DMCs and years 2000-2025
    filt = []
    for row in data_rows:
        if row is None or len(row) < len(header): continue
        iso = row[cols["ISO"]]
        if iso not in ADB_DMCS: continue
        try:
            year = int(row[cols["Year"]])
        except (TypeError, ValueError):
            continue
        if year < 2000 or year > 2025: continue
        filt.append(row)
    print(f"Filtered rows (ADB DMCs, 2000-2025): {len(filt)}")

    # Per-DMC aggregation
    by_dmc = defaultdict(lambda: {
        "events": 0, "affected": 0, "deaths": 0, "damage_adj_usd": 0.0,
        "by_type": defaultdict(int),
        "years_covered": set(),
        "biggest_event": None,
    })

    for row in filt:
        iso = row[cols["ISO"]]
        d = by_dmc[iso]
        try: d["events"] += int(row[cols["Total Events"]] or 0)
        except: pass
        try: d["affected"] += int(row[cols["Total Affected"]] or 0)
        except: pass
        try: d["deaths"] += int(row[cols["Total Deaths"]] or 0)
        except: pass
        try:
            damage = row[cols["Total Damage (USD, adjusted)"]]
            if isinstance(damage, (int, float)) and damage > 0:
                d["damage_adj_usd"] += float(damage)
        except: pass
        d["by_type"][row[cols["Disaster Type"]]] += int(row[cols["Total Events"]] or 0)
        d["years_covered"].add(int(row[cols["Year"]]))
        # Track biggest single record by deaths
        try:
            deaths_this = int(row[cols["Total Deaths"]] or 0)
            if d["biggest_event"] is None or deaths_this > d["biggest_event"]["deaths"]:
                d["biggest_event"] = {
                    "year": int(row[cols["Year"]]),
                    "type": row[cols["Disaster Type"]],
                    "subtype": row[cols["Disaster Subtype"]],
                    "deaths": deaths_this,
                    "affected": int(row[cols["Total Affected"]] or 0),
                }
        except: pass

    # Build output
    rows_out = []
    for iso, name in sorted(ADB_DMCS.items(), key=lambda x: x[1]):
        d = by_dmc.get(iso)
        if not d:
            rows_out.append({
                "iso3": iso, "country": name,
                "total_events_2000_2025": 0, "total_affected": 0, "total_deaths": 0,
                "total_damage_usd_adj": 0.0,
                "events_per_year": 0.0,
                "type_distribution": {},
                "biggest_event": None,
                "years_covered": 0,
            })
            continue
        years = sorted(d["years_covered"])
        per_year = d["events"] / max(len(years), 1)
        rows_out.append({
            "iso3": iso, "country": name,
            "total_events_2000_2025": d["events"],
            "total_affected": d["affected"],
            "total_deaths": d["deaths"],
            "total_damage_usd_adj": round(d["damage_adj_usd"], 0),
            "events_per_year": round(per_year, 2),
            "type_distribution": dict(d["by_type"]),
            "biggest_event": d["biggest_event"],
            "years_covered": len(years),
        })

    rows_out.sort(key=lambda r: -r["events_per_year"])

    # Country-level top 10
    print("=== Top 12 by event frequency (events/year) ===")
    for r in rows_out[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:25]:<25} events/yr={r['events_per_year']:>5.2f}  affected={r['total_affected']:>13,}  deaths={r['total_deaths']:>7,}")

    payload = {
        "program": "disaster-recovery-lag",
        "claim_scope": (
            "Hypothesis-stage structural-burden layer for 2000–2025. "
            "Per-DMC counts and impacts from EM-DAT (CRED) via the HDX "
            "mirror. NOT yet a recovery-lag metric — that requires "
            "indicator-recovery-curve analysis around event timestamps."
        ),
        "framing_rule": "Burden frequency, not country fragility ranking.",
        "sources": {
            "emdat": {
                "name": "EM-DAT — The International Disaster Database (CRED, UCLouvain)",
                "url": "https://data.humdata.org/dataset/emdat-country-profiles",
                "license": "EM-DAT terms; non-commercial open access",
                "vintage": "2026-04-24",
                "retrieved_at": "2026-04-25",
                "rows_total": len(rows),
                "rows_in_filter": len(filt),
            },
        },
        "rows": rows_out,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/disaster-recovery-lag-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    csv_rows = [{k: v for k, v in r.items() if k not in ("type_distribution", "biggest_event")} for r in rows_out]
    with open(f"{OUT}/disaster-recovery-lag-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        if csv_rows:
            w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            w.writeheader()
            for row in csv_rows: w.writerow(row)

    print(f"\nWrote {OUT}/disaster-recovery-lag-adb-panel.{{json,csv}}")


if __name__ == "__main__":
    main()
