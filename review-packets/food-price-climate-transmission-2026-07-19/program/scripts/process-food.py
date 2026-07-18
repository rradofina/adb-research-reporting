"""Program 9 — Food Price Climate Transmission (first-pass macro).

Hypothesis-stage structural-exposure: per-DMC food-price sensitivity =
food inflation × agricultural import share × rural-share-adjusted
vulnerability. Does NOT yet measure climate-transmission — that needs
CHIRPS × local price series from WFP VAM or FAOSTAT FPMA at subnational
level. This is the macro layer.
"""
import json, csv, os
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/food-price-climate-transmission/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/food-price-climate-transmission/generated"
os.makedirs(OUT, exist_ok=True)

ADB_NAMES = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China","COK":"Cook Islands",
    "FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong SAR","IND":"India","IDN":"Indonesia",
    "KAZ":"Kazakhstan","KIR":"Kiribati","KGZ":"Kyrgyzstan","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia",
    "MNG":"Mongolia","MMR":"Myanmar","NRU":"Nauru","NPL":"Nepal",
    "PAK":"Pakistan","PLW":"Palau","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam","TWN":"Taiwan",
}


def load_wdi(path):
    try: d = json.load(open(path, encoding="utf-8"))
    except FileNotFoundError: return {}
    if not isinstance(d, list) or len(d) < 2: return {}
    out = {}
    for row in d[1]:
        if not isinstance(row.get("value"), (int, float)): continue
        iso = row.get("countryiso3code")
        if iso not in ADB_NAMES: continue
        y = int(row.get("date"))
        if iso not in out or y > out[iso]["year"]:
            out[iso] = {"year": y, "value": float(row["value"])}
    return out


def main():
    inflation = load_wdi(f"{CACHE}/wdi_food_inflation.json")
    ag_imports = load_wdi(f"{CACHE}/wdi_ag_imports.json")
    food_prod = load_wdi(f"{CACHE}/wdi_food_production.json")

    rows = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        inf = inflation.get(iso)
        ag = ag_imports.get(iso)
        fp = food_prod.get(iso)

        # Food-price vulnerability composite:
        # - High inflation × high ag-import share × food-production-index-slack
        # Normalize inflation at 20%, ag-imports at 25%, food prod against 100 baseline.
        if inf and ag and fp:
            inf_norm = min((inf["value"] or 0) / 20, 1.5)
            ag_norm = min((ag["value"] or 0) / 25, 1.5)
            prod_norm = max(0, (110 - (fp["value"] or 100)) / 20)  # low prod index = more pressure
            prod_norm = min(prod_norm, 1.5)
            vuln = round(inf_norm * ag_norm * prod_norm * 100, 1)
        else:
            vuln = None

        rows.append({
            "iso3": iso, "country": name,
            "cpi_inflation_pct": inf["value"] if inf else None,
            "cpi_year": inf["year"] if inf else None,
            "ag_imports_pct_merch": ag["value"] if ag else None,
            "ag_year": ag["year"] if ag else None,
            "food_production_index": fp["value"] if fp else None,
            "food_price_vulnerability": vuln,
        })

    rows.sort(key=lambda r: -(r["food_price_vulnerability"] or -1))

    print("=== Top 12 by food-price vulnerability ===")
    for r in rows[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:22]:<22} infl={r['cpi_inflation_pct']}%  ag_imp={r['ag_imports_pct_merch']}%  fp_idx={r['food_production_index']}  vuln={r['food_price_vulnerability']}")

    payload = {
        "program": "food-price-climate-transmission",
        "claim_scope": "Hypothesis-stage macro-level food-price vulnerability. WDI only; climate-transmission (CHIRPS × local prices) NOT yet included.",
        "framing_rule": "Structural exposure to food-price stress, not a country food-security ranking.",
        "sources": {
            "wdi": {
                "indicators": [
                    "FP.CPI.TOTL.ZG (CPI inflation, annual %)",
                    "TM.VAL.AGRI.ZS.UN (agricultural imports % merchandise)",
                    "AG.PRD.FOOD.XD (food production index, 2014-2016=100)",
                ],
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/food-price-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/food-price-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)
    print(f"\nWrote {OUT}/food-price-adb-panel.{{json,csv}}")


if __name__ == "__main__":
    main()
