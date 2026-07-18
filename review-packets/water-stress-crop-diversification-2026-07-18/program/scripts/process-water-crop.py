"""Program 17 — Water Stress and Crop Concentration.

Hypothesis-stage screening: combines WDI indicators for
  - Freshwater withdrawal (% internal resources)  [ER.H2O.FWTL.ZS]
  - Agricultural land (% of land area)           [AG.LND.AGRI.ZS]
  - Arable land (% of land area)                 [AG.LND.ARBL.ZS]
  - Cereal yield (kg/ha)                          [AG.YLD.CREL.KG]
  - Rural population (% of total)                 [SP.RUR.TOTL.ZS]

Per-DMC water-crop pressure composite. Triage only.
"""
import json, csv, os
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/water-stress-crop-diversification/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/water-stress-crop-diversification/generated"
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
    water = load_wdi(f"{CACHE}/wdi_freshwater_withdrawal.json")
    agri = load_wdi(f"{CACHE}/wdi_agri_land_pct.json")
    arable = load_wdi(f"{CACHE}/wdi_ag_land_arable.json")
    yld = load_wdi(f"{CACHE}/wdi_cereal_yield.json")
    rural = load_wdi(f"{CACHE}/wdi_rural_pct.json")

    rows = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        w = water.get(iso); a = agri.get(iso); ar = arable.get(iso)
        y = yld.get(iso); r = rural.get(iso)

        # Water-crop-pressure composite:
        # - High freshwater withdrawal (close to or over 100% = stressed)
        # - Low cereal yield (indicates less diversified / less efficient ag)
        # - High rural share (more people reliant on agriculture)
        # Normalize: water-withdrawal / 100; yield inverse (1000/yield capped); rural/100.
        if w and y and r:
            water_norm = min((w["value"] or 0) / 100.0, 1.5)  # can exceed 100%
            yld_inv = min(3000 / max(y["value"], 100), 1.0)  # higher when yield low
            rural_norm = (r["value"] or 0) / 100.0
            stress = round((water_norm * yld_inv * rural_norm) * 100, 1)
        else:
            stress = None

        rows.append({
            "iso3": iso, "country": name,
            "water_withdrawal_pct_resources": w["value"] if w else None,
            "water_withdrawal_year": w["year"] if w else None,
            "agri_land_pct": a["value"] if a else None,
            "arable_land_pct": ar["value"] if ar else None,
            "cereal_yield_kg_per_ha": y["value"] if y else None,
            "rural_population_pct": r["value"] if r else None,
            "water_crop_pressure_index": stress,
        })

    rows.sort(key=lambda r: -(r["water_crop_pressure_index"] or -1))

    print("=== Top 12 by water-crop pressure index ===")
    for r in rows[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:22]:<22} water={r['water_withdrawal_pct_resources']}  yield={r['cereal_yield_kg_per_ha']}  rural={r['rural_population_pct']}%  idx={r['water_crop_pressure_index']}")

    payload = {
        "program": "water-stress-crop-diversification",
        "claim_scope": "Hypothesis-stage water-crop pressure composite. WDI indicators. Triage only.",
        "framing_rule": "Water × crop × rural-share pressure signal, not a country ranking.",
        "sources": {
            "wdi": {
                "indicators": [
                    "ER.H2O.FWTL.ZS (freshwater withdrawal % internal resources)",
                    "AG.LND.AGRI.ZS (agricultural land % area)",
                    "AG.LND.ARBL.ZS (arable land % area)",
                    "AG.YLD.CREL.KG (cereal yield kg/ha)",
                    "SP.RUR.TOTL.ZS (rural population %)",
                ],
                "url": "https://api.worldbank.org/v2/country/all/indicator/...",
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
        },
        "methodology": {
            "water_crop_pressure_index": (
                "min(water_withdrawal/100, 1.5) × min(3000/max(yield,100), 1.0) × rural_pct/100, × 100. "
                "Higher = more water/yield/rural stress combined. Triage only."
            ),
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/water-stress-crop-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/water-stress-crop-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)
    print(f"\nWrote {OUT}/water-stress-crop-adb-panel.{{json,csv}}")


if __name__ == "__main__":
    main()
