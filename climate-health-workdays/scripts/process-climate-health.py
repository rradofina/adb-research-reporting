"""Program 5 — Climate-Health Workday Loss.

Hypothesis-stage screening: outdoor-labor × pollution exposure composite.
Heat exposure (CCKP tasmax per country) is a future pipeline step; this
version uses PM2.5 exposure only, with rural-agriculture share as the
outdoor-labor proxy.
"""
import json, csv, os
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/climate-health-workdays/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/climate-health-workdays/generated"
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
    agri = load_wdi(f"{CACHE}/wdi_emp_agri.json")
    industry = load_wdi(f"{CACHE}/wdi_emp_industry.json")
    pm25 = load_wdi(f"{CACHE}/wdi_pm25.json")
    urban = load_wdi(f"{CACHE}/wdi_urban.json")
    pop = load_wdi(f"{CACHE}/wdi_pop.json")

    rows = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        a = agri.get(iso); ind = industry.get(iso)
        p = pm25.get(iso); u = urban.get(iso); pp = pop.get(iso)

        # Outdoor-labor share = agri employment + (0.5 × industry — assumed ~half outdoor)
        if a is not None and ind is not None:
            outdoor = (a["value"] or 0) + 0.5 * (ind["value"] or 0)
        else:
            outdoor = None

        # Workday-loss pressure index:
        #   outdoor-labor × PM2.5-exposure-pressure
        #   PM2.5 pressure = max((PM2.5 - WHO_5), 0) / 45  (0–1 roughly)
        if outdoor is not None and p is not None:
            pm_pressure = max((p["value"] or 0) - 5, 0) / 45.0
            pm_pressure = min(pm_pressure, 1.0)
            workday_idx = round((outdoor / 100.0) * pm_pressure * 100.0, 1)
        else:
            workday_idx = None

        # Exposed-population proxy (millions): outdoor share × total pop
        exposed_m = None
        if outdoor is not None and pp is not None:
            exposed_m = round((outdoor / 100.0) * pp["value"] / 1e6, 1)

        rows.append({
            "iso3": iso, "country": name,
            "emp_agri_pct": a["value"] if a else None,
            "emp_industry_pct": ind["value"] if ind else None,
            "outdoor_labor_share_pct": round(outdoor, 1) if outdoor is not None else None,
            "pm25_exposure_ugm3": p["value"] if p else None,
            "pm25_year": p["year"] if p else None,
            "urban_pop_pct": u["value"] if u else None,
            "population_total": pp["value"] if pp else None,
            "exposed_outdoor_millions": exposed_m,
            "workday_loss_pressure_index": workday_idx,
        })

    rows.sort(key=lambda r: -(r["workday_loss_pressure_index"] or -1))

    print("=== Top 12 by workday-loss pressure index ===")
    for r in rows[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:22]:<22} outdoor={r['outdoor_labor_share_pct']}%  PM25={r['pm25_exposure_ugm3']}  exposed={r['exposed_outdoor_millions']}M  idx={r['workday_loss_pressure_index']}")

    payload = {
        "program": "climate-health-workdays",
        "claim_scope": (
            "Hypothesis-stage outdoor-labor × pollution-exposure composite "
            "for ADB DMCs. Heat (tasmax × vulnerable-days) is a planned "
            "pipeline step and NOT included in this version."
        ),
        "framing_rule": (
            "Structural pressure signal for hidden labor-productivity loss; "
            "not a country productivity ranking."
        ),
        "sources": {
            "wdi": {
                "indicators": [
                    "SL.AGR.EMPL.ZS (employment in agriculture, %)",
                    "SL.IND.EMPL.ZS (employment in industry, %)",
                    "EN.ATM.PM25.MC.M3 (annual mean PM2.5 exposure µg/m³)",
                    "SP.URB.TOTL.IN.ZS (urban pop %)",
                    "SP.POP.TOTL (total population)",
                ],
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
        },
        "methodology": {
            "workday_loss_pressure_index": (
                "(outdoor_labor_share / 100) × PM2.5_pressure × 100, "
                "where outdoor = agri% + 0.5 × industry%, and "
                "PM2.5_pressure = min(max(PM2.5 - 5, 0)/45, 1). Triage only."
            ),
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/climate-health-workdays-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/climate-health-workdays-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)
    print(f"\nWrote {OUT}/climate-health-workdays-adb-panel.{{json,csv}}")


if __name__ == "__main__":
    main()
