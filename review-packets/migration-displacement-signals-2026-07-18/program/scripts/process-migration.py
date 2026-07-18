"""Program 11 — Migration and Displacement Signals.

Hypothesis-stage screening: per-DMC international migrant stock (both
directions) from UN DESA International Migrant Stock 2024, latest year
(2024). Plus top 5 origin and destination corridors per DMC.

Per CONSTITUTION.md §13.3/§14: this is a structural-signal layer, not a
country-fragility ranking.
"""
import json, csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import openpyxl

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache"
OUT = BASE / "generated"
OUT.mkdir(parents=True, exist_ok=True)

# UN M49 -> ISO3 for ADB regional DMCs
UN_TO_ISO3 = {
    4:"AFG", 51:"ARM", 31:"AZE", 50:"BGD", 64:"BTN", 96:"BRN",
    116:"KHM", 156:"CHN", 184:"COK", 242:"FJI", 268:"GEO",
    344:"HKG", 356:"IND", 360:"IDN", 398:"KAZ", 296:"KIR",
    417:"KGZ", 418:"LAO", 458:"MYS", 462:"MDV", 584:"MHL",
    583:"FSM", 496:"MNG", 104:"MMR", 520:"NRU", 524:"NPL",
    570:"NIU", 586:"PAK", 585:"PLW", 598:"PNG", 608:"PHL",
    882:"WSM", 90:"SLB", 144:"LKA", 762:"TJK", 764:"THA",
    626:"TLS", 776:"TON", 795:"TKM", 798:"TUV", 860:"UZB",
    548:"VUT", 704:"VNM", 158:"TWN",
}
ADB_NAMES = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China","COK":"Cook Islands",
    "FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong SAR","IND":"India","IDN":"Indonesia",
    "KAZ":"Kazakhstan","KIR":"Kiribati","KGZ":"Kyrgyzstan","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia",
    "MNG":"Mongolia","MMR":"Myanmar","NRU":"Nauru","NPL":"Nepal","NIU":"Niue",
    "PAK":"Pakistan","PLW":"Palau","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam","TWN":"Taiwan",
}


def main():
    wb = openpyxl.load_workbook(CACHE / "undesa_migrant_stock_2024_destination.xlsx", data_only=True)
    ws = wb["Table 1"]

    # Identify year columns. Header row is row 10 (1-indexed); col offsets:
    # 0=Index, 1=dest-name, 2=Coverage, 3=Data type, 4=dest-code, 5=origin-name, 6=origin-code
    # 7+ = year columns (1990, 1995, 2000, ..., 2024)
    rows = list(ws.iter_rows(values_only=True))
    header = rows[10]
    # Find year columns
    year_cols = []
    for i, h in enumerate(header):
        if isinstance(h, int) and 1990 <= h <= 2030:
            year_cols.append((i, h))
    print(f"Year columns: {year_cols}")
    latest_year_col = max(year_cols, key=lambda x: x[1])
    print(f"Using {latest_year_col[1]} from col {latest_year_col[0]}")

    # Aggregate
    # inward[dest] += stock where origin != dest, origin is a country (not region/world)
    # outward[origin] += stock where dest != origin
    inward = defaultdict(int)
    outward = defaultdict(int)
    corridors_inward = defaultdict(list)  # dest -> [(origin, stock)]
    corridors_outward = defaultdict(list)  # origin -> [(dest, stock)]

    for row in rows[11:]:
        if not row or len(row) < latest_year_col[0] + 1: continue
        dest_code = row[4]
        origin_code = row[6]
        stock = row[latest_year_col[0]]
        if not isinstance(dest_code, int) or not isinstance(origin_code, int): continue
        if not isinstance(stock, (int, float)): continue
        if stock <= 0: continue
        if dest_code == origin_code: continue  # same-country flow
        if dest_code == 900 or origin_code == 900: continue  # World totals

        dest_iso = UN_TO_ISO3.get(dest_code)
        origin_iso = UN_TO_ISO3.get(origin_code)
        stock = int(stock)

        # Accumulate for ADB DMCs as dest (inward to DMC)
        if dest_iso in ADB_NAMES and origin_code != dest_code:
            # Only count rows where origin is a country (not a region aggregate) — heuristic: origin_code not in region-level codes
            if origin_code >= 900: continue  # exclude World (900) and regional aggregates (18xx/19xx)
            inward[dest_iso] += stock
            corridors_inward[dest_iso].append({
                "origin_code": origin_code,
                "origin_iso3": origin_iso,
                "origin_name": row[5],
                "stock": stock,
            })
        if origin_iso in ADB_NAMES and origin_code != dest_code:
            if dest_code >= 900: continue  # exclude World and regional aggregates
            outward[origin_iso] += stock
            corridors_outward[origin_iso].append({
                "dest_code": dest_code,
                "dest_iso3": dest_iso,
                "dest_name": row[1],
                "stock": stock,
            })

    # Compose per-DMC rows
    rows_out = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        inw = inward.get(iso, 0)
        outw = outward.get(iso, 0)
        top_in = sorted(corridors_inward.get(iso, []), key=lambda c: -c["stock"])[:5]
        top_out = sorted(corridors_outward.get(iso, []), key=lambda c: -c["stock"])[:5]
        rows_out.append({
            "iso3": iso, "country": name,
            "immigrant_stock_2024": inw,
            "emigrant_stock_2024": outw,
            "net_migrant_stock_2024": inw - outw,
            "top_origins": top_in,
            "top_destinations": top_out,
        })

    rows_out.sort(key=lambda r: -r["emigrant_stock_2024"])

    print("=== Top 12 DMCs by emigrant stock ===")
    for r in rows_out[:12]:
        top_dst = ", ".join(f"{c['dest_name']} ({c['stock']:,})" for c in r["top_destinations"][:2])
        print(f"  {r['iso3']:<4} {r['country'][:22]:<22} emigrants={r['emigrant_stock_2024']:>12,}  top: {top_dst}")

    payload = {
        "program": "migration-displacement-signals",
        "claim_scope": "Hypothesis-stage: structural migrant stock signal. UN DESA 2024 snapshot.",
        "framing_rule": "Signal of mobility pressure, not country fragility.",
        "sources": {
            "undesa": {
                "name": "UN DESA International Migrant Stock 2024",
                "url": "https://www.un.org/development/desa/pd/content/international-migrant-stock",
                "license": "CC BY 3.0 IGO",
                "retrieved_at": "2026-04-25",
                "year_used": latest_year_col[1],
            },
        },
        "rows": rows_out,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with (OUT / "migration-displacement-adb-panel.json").open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    csv_rows = [{"iso3":r["iso3"], "country":r["country"],
                 "immigrant_stock_2024":r["immigrant_stock_2024"],
                 "emigrant_stock_2024":r["emigrant_stock_2024"],
                 "net_migrant_stock_2024":r["net_migrant_stock_2024"]} for r in rows_out]
    with (OUT / "migration-displacement-adb-panel.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        for row in csv_rows: w.writerow(row)

    print(f"\nWrote {OUT}/migration-displacement-adb-panel.{{json,csv}}")


if __name__ == "__main__":
    main()
