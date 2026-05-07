"""Program 16 — Social Protection Shock Coverage.

Hypothesis-stage screening: per-DMC social-protection coverage + payment-
system readiness (Findex account ownership) + poverty baseline.

Per CONSTITUTION.md §13.3/§14: flags where shock payments are mechanically
hard to reach low-income households. Not a country quality ranking.
"""
import json, csv, os
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/social-protection-shock-coverage/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/social-protection-shock-coverage/generated"
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
    sp = load_wdi(f"{CACHE}/wdi_sp_coverage.json")
    acc = load_wdi(f"{CACHE}/wdi_findex_account.json")
    pov = load_wdi(f"{CACHE}/wdi_poverty_215.json")
    gap = load_wdi(f"{CACHE}/wdi_poverty_gap.json")

    rows = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        s = sp.get(iso); a = acc.get(iso); p = pov.get(iso); g = gap.get(iso)
        # Readiness gap: poverty × (1 - coverage) × (1 - account ownership)
        # High readiness-gap = poverty high AND coverage low AND accounts low
        if p is not None and (s or a):
            sp_v = (s["value"] or 0) / 100 if s else 0.0
            acc_v = (a["value"] or 0) / 100 if a else 0.0
            # Gap = poverty × (1 - average of coverage and accounts)
            mean_readiness = (sp_v + acc_v) / 2 if (s and a) else (sp_v if s else acc_v)
            readiness_gap = round(((p["value"] or 0) / 100) * (1 - mean_readiness) * 100, 1)
        else:
            readiness_gap = None

        rows.append({
            "iso3": iso, "country": name,
            "sp_coverage_pct": s["value"] if s else None,
            "sp_coverage_year": s["year"] if s else None,
            "findex_account_pct": a["value"] if a else None,
            "findex_year": a["year"] if a else None,
            "poverty_headcount_215_pct": p["value"] if p else None,
            "poverty_year": p["year"] if p else None,
            "poverty_gap_pct": g["value"] if g else None,
            "shock_payment_readiness_gap": readiness_gap,
        })

    rows.sort(key=lambda r: -(r["shock_payment_readiness_gap"] or -1))

    print("=== Top 12 by shock-payment readiness gap ===")
    for r in rows[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:22]:<22} pov={r['poverty_headcount_215_pct']}  sp={r['sp_coverage_pct']}  acct={r['findex_account_pct']}  gap={r['shock_payment_readiness_gap']}")

    payload = {
        "program": "social-protection-shock-coverage",
        "claim_scope": "Hypothesis-stage readiness-gap composite. WDI social-protection coverage × Findex account × poverty baseline.",
        "framing_rule": "Structural shock-payment readiness gap, not a country quality score.",
        "sources": {
            "wdi": {
                "indicators": [
                    "per_allsp.cov_pop_tot — ASPIRE total social protection coverage (% pop)",
                    "FX.OWN.TOTL.ZS — Findex account ownership (% age 15+)",
                    "SI.POV.DDAY — Poverty headcount at $2.15/day 2017 PPP",
                    "SI.POV.GAPS — Poverty gap at $2.15/day",
                ],
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
        },
        "methodology": {
            "shock_payment_readiness_gap": (
                "(poverty/100) × (1 - avg(sp_coverage, account_ownership)) × 100. "
                "Triage only."
            ),
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/social-protection-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/social-protection-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)
    print(f"\nWrote {OUT}/social-protection-adb-panel.{{json,csv}}")

if __name__ == "__main__":
    main()
