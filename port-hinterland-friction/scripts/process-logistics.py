"""Program 12 — Port-Hinterland Trade Friction.

Hypothesis-stage structural-exposure layer. Combines:
  - World Bank LPI 2023 (overall, infrastructure, customs sub-indices) via WDI
  - WDI imports value (NE.IMP.GNFS.CD) as trade-dependence proxy

Per-DMC friction-exposure: low LPI + high imports-to-GDP proxy = more
friction-exposed. Triage only per CONSTITUTION.md §6.4.
"""
import json, csv, os
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/port-hinterland-friction/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/port-hinterland-friction/generated"
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
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        return {}
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
    lpi_overall = load_wdi(f"{CACHE}/wdi_lpi_overall.json")
    lpi_infra = load_wdi(f"{CACHE}/wdi_lpi_infra.json")
    lpi_customs = load_wdi(f"{CACHE}/wdi_lpi_customs.json")
    imports_usd = load_wdi(f"{CACHE}/wdi_imports.json")

    rows = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        o = lpi_overall.get(iso)
        i = lpi_infra.get(iso)
        c = lpi_customs.get(iso)
        imp = imports_usd.get(iso)

        # Friction-exposure index: (5 - LPI_overall) × log(imports+1) normalized
        # LPI is 1-5, higher = better logistics. Lower LPI = more friction.
        # Imports in USD (trillions for big economies).
        if o and imp:
            lpi_gap = max(5.0 - o["value"], 0)  # 0 = perfect logistics; 4 = worst
            import_b = imp["value"] / 1e9  # billions USD
            import_log = 0 if import_b <= 0 else (import_b ** 0.5) / 50  # sqrt-scale, cap
            friction = round(lpi_gap * min(import_log, 2.0), 2)
        else:
            friction = None

        rows.append({
            "iso3": iso, "country": name,
            "lpi_overall": o["value"] if o else None,
            "lpi_overall_year": o["year"] if o else None,
            "lpi_infrastructure": i["value"] if i else None,
            "lpi_customs": c["value"] if c else None,
            "imports_usd": imp["value"] if imp else None,
            "imports_usd_year": imp["year"] if imp else None,
            "friction_exposure_index": friction,
        })

    rows.sort(key=lambda r: -(r["friction_exposure_index"] or -1))

    print("=== Top 12 by friction-exposure index ===")
    for r in rows[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:25]:<25} LPI={r['lpi_overall']}  imports=${(r['imports_usd'] or 0)/1e9:>9.1f}B  friction={r['friction_exposure_index']}")

    payload = {
        "program": "port-hinterland-friction",
        "claim_scope": "Hypothesis-stage structural-exposure. LPI × trade dependence combined for ADB DMCs.",
        "framing_rule": "Friction-exposure flags where logistics bottlenecks meet high trade reliance. Not a country-quality rank.",
        "sources": {
            "wdi_lpi": {
                "name": "World Bank Logistics Performance Index (via WDI)",
                "indicators": ["LP.LPI.OVRL.XQ","LP.LPI.INFR.XQ","LP.LPI.CUST.XQ"],
                "url": "https://lpi.worldbank.org/",
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
            "wdi_imports": {
                "name": "WDI NE.IMP.GNFS.CD — Imports of goods and services (current USD)",
                "url": "https://api.worldbank.org/v2/country/all/indicator/NE.IMP.GNFS.CD",
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
        },
        "methodology": {
            "friction_exposure_index": (
                "(5 - LPI_overall) × min(sqrt(imports_B)/50, 2.0). "
                "LPI gap measures logistics-performance deficit; import-proxy "
                "measures trade dependence. Triage only."
            ),
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/port-hinterland-friction-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/port-hinterland-friction-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)

    print(f"\nWrote {OUT}/port-hinterland-friction-adb-panel.{{json,csv}}")


if __name__ == "__main__":
    main()
