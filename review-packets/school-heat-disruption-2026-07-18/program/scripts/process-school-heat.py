"""Program 15 — School Heat Disruption.

Hypothesis-stage screening combining:
  - WDI SE.PRM.ENRL.TC.ZS — primary pupil-teacher ratio
  - WDI SP.POP.0014.TO.ZS — population ages 0-14 %
  - WDI SP.POP.TOTL — total pop
  - CCKP CMIP6 historical (1995-2014) tasmax climatology per country

Per-DMC school-heat-pressure composite. Children in school-age × heat
exposure. Triage only.
"""
import json, csv, os
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/school-heat-disruption/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/school-heat-disruption/generated"
os.makedirs(OUT, exist_ok=True)

ADB_NAMES = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China",
    "FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong SAR","IND":"India","IDN":"Indonesia",
    "KAZ":"Kazakhstan","KGZ":"Kyrgyzstan","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MNG":"Mongolia","MMR":"Myanmar",
    "NPL":"Nepal","PAK":"Pakistan","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TKM":"Turkmenistan","UZB":"Uzbekistan","VNM":"Viet Nam",
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


def load_cckp_tasmax(iso):
    path = f"{CACHE}/cckp_tasmax_{iso}.json"
    try: d = json.load(open(path, encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError): return None
    data = d.get("data", {}).get(iso, {})
    if not data: return None
    # Values are keyed by period; take the first/only numeric value
    for v in data.values():
        if isinstance(v, (int, float)):
            return float(v)
    return None


def main():
    ptr = load_wdi(f"{CACHE}/wdi_ptr.json")
    pop014 = load_wdi(f"{CACHE}/wdi_pop_0_14.json")
    pop_total = load_wdi(f"{CACHE}/wdi_pop.json")

    rows = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        ptr_v = ptr.get(iso)
        p014 = pop014.get(iso)
        ptot = pop_total.get(iso)
        tasmax = load_cckp_tasmax(iso)

        child_count = None
        if p014 and ptot:
            child_count = (p014["value"] or 0) / 100 * (ptot["value"] or 0)

        # Heat pressure: tasmax > 30°C = warming; > 35°C = significant.
        # Score = max(tasmax - 25, 0) / 15 (0 at 25°C, 1.0 at 40°C), capped.
        heat_score = None
        if tasmax is not None:
            heat_score = min(max(tasmax - 25, 0) / 15, 1.0)

        # School-heat pressure index = child-age-share × heat_score × PTR proxy
        # Higher PTR = overcrowded classrooms; add 0.5× scaled. Normalize PTR at 40.
        if child_count and heat_score is not None:
            ptr_norm = min((ptr_v["value"] or 20) / 40, 1.5) if ptr_v else 1.0
            pressure = round(heat_score * (p014["value"] / 100) * ptr_norm * 100, 1)
        else:
            pressure = None

        rows.append({
            "iso3": iso, "country": name,
            "primary_pupil_teacher_ratio": ptr_v["value"] if ptr_v else None,
            "ptr_year": ptr_v["year"] if ptr_v else None,
            "pop_0_14_pct": p014["value"] if p014 else None,
            "pop_total": ptot["value"] if ptot else None,
            "children_0_14_millions": round(child_count / 1e6, 2) if child_count else None,
            "annual_tasmax_1995_2014_celsius": round(tasmax, 2) if tasmax is not None else None,
            "school_heat_pressure_index": pressure,
        })

    rows.sort(key=lambda r: -(r["school_heat_pressure_index"] or -1))

    print("=== Top 12 by school-heat pressure index ===")
    for r in rows[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:22]:<22} children={r['children_0_14_millions']}M  tasmax={r['annual_tasmax_1995_2014_celsius']}°C  PTR={r['primary_pupil_teacher_ratio']}  idx={r['school_heat_pressure_index']}")

    payload = {
        "program": "school-heat-disruption",
        "claim_scope": "Hypothesis-stage school-heat pressure composite. Historical tasmax × child share × PTR. Triage only.",
        "framing_rule": "Signals where many school-age children experience high heat with overcrowded classrooms; not a country quality metric.",
        "sources": {
            "wdi": {
                "indicators": [
                    "SE.PRM.ENRL.TC.ZS (primary pupil-teacher ratio)",
                    "SP.POP.0014.TO.ZS (population ages 0-14, %)",
                    "SP.POP.TOTL (total population)",
                ],
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
            "cckp": {
                "name": "World Bank Climate Change Knowledge Portal CMIP6 tasmax climatology 1995–2014 historical",
                "url_pattern": "https://cckpapi.worldbank.org/cckp/v1/cmip6-x0.25_climatology_tasmax_climatology_annual_1995-2014_median_historical_ensemble_all_mean/{iso3}",
                "license": "World Bank open",
                "retrieved_at": "2026-04-25",
            },
        },
        "methodology": {
            "school_heat_pressure_index": (
                "min(max(tasmax-25,0)/15, 1) × (pop_0_14_pct/100) × "
                "min(PTR/40, 1.5) × 100. Triage."
            ),
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/school-heat-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/school-heat-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)
    print(f"\nWrote {OUT}/school-heat-adb-panel.{{json,csv}}")


if __name__ == "__main__":
    main()
