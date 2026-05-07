"""Build minimal-viable pipelines for the 3 folder-stub programs.

Each program gets a country-level index from WDI + (where applicable)
EM-DAT subset. Honest first-pass — sub-national / Earth Engine work is
the §18.5 upgrade-pass per program.

Outputs:
- coastal-informal-risk/generated/coastal-informal-risk-adb-panel.{json,csv}
- invisible-urbanization/generated/invisible-urbanization-adb-panel.{json,csv}
- flood-market-access/generated/flood-market-access-adb-panel.{json,csv}
"""

import json
import csv
import os
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

ADB_DMCS = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China","COK":"Cook Islands",
    "FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong, China","IND":"India","IDN":"Indonesia",
    "KAZ":"Kazakhstan","KIR":"Kiribati","KGZ":"Kyrgyz Republic","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia",
    "MNG":"Mongolia","MMR":"Myanmar","NRU":"Nauru","NPL":"Nepal","NIU":"Niue",
    "PAK":"Pakistan","PLW":"Palau","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam","TWN":"Taiwan",
}

# Coastal flag: 1 if has a coastline, 0 if landlocked (per ADB DMC roster).
COASTAL = {
    "AFG":0,"ARM":0,"AZE":1,"BGD":1,"BTN":0,"BRN":1,"KHM":1,"CHN":1,"COK":1,
    "FJI":1,"GEO":1,"HKG":1,"IND":1,"IDN":1,"KAZ":0,"KIR":1,"KGZ":0,"LAO":0,
    "MYS":1,"MDV":1,"MHL":1,"FSM":1,"MNG":0,"MMR":1,"NRU":1,"NPL":0,"NIU":1,
    "PAK":1,"PLW":1,"PNG":1,"PHL":1,"WSM":1,"SLB":1,"LKA":1,"TJK":0,
    "THA":1,"TLS":1,"TON":1,"TKM":1,"TUV":1,"UZB":0,"VUT":1,"VNM":1,"TWN":1,
}


def wdi(indicator, year_window="2010:2024"):
    """Fetch WDI indicator latest-year value per DMC. Paginates through country/all results."""
    out = {}
    page = 1
    print(f"  fetching {indicator}…")
    while True:
        url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=2000&date={year_window}&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": "adb-research/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        if not isinstance(data, list) or len(data) < 2 or data[1] is None:
            break
        meta = data[0]
        for row in data[1]:
            v = row.get("value")
            if not isinstance(v, (int, float)):
                continue
            iso = row.get("countryiso3code")
            if iso not in ADB_DMCS:
                continue
            y = int(row.get("date"))
            if iso not in out or y > out[iso]["year"]:
                out[iso] = {"year": y, "value": float(v)}
        if page >= meta.get("pages", 1):
            break
        page += 1
    return out


def emdat_flood():
    """Filter EM-DAT panel to flood subset; return dict[iso3] -> {events, share}."""
    gen = ROOT / "disaster-recovery-lag" / "generated" / "disaster-recovery-lag-adb-panel.json"
    if not gen.exists():
        return {}
    d = json.loads(gen.read_text(encoding="utf-8"))
    out = {}
    for r in d.get("rows", []):
        td = r.get("type_distribution") or {}
        flood_count = td.get("Flood", 0) or 0
        total = r.get("total_events_2000_2025", 0) or 0
        out[r["iso3"]] = {
            "iso3": r["iso3"],
            "country": r.get("country", ""),
            "flood_events": flood_count,
            "total_events": total,
            "flood_share": (flood_count / total) if total else 0,
            "total_affected": r.get("total_affected", 0),
        }
    return out


def write_panel(slug, payload):
    out_dir = ROOT / slug / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{slug}-adb-panel.json"
    csv_path = out_dir / f"{slug}-adb-panel.csv"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    rows = payload.get("rows", [])
    if rows:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            keys = list(rows[0].keys())
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for row in rows:
                w.writerow(row)
    print(f"  wrote {json_path} + .csv ({len(rows)} rows)")


# =========================================================================
# 1. coastal-informal-risk
# =========================================================================

def run_coastal():
    print("\n=== coastal-informal-risk ===")
    urb = wdi("SP.URB.TOTL.IN.ZS")  # urban % of total
    pop = wdi("SP.POP.TOTL")         # total population
    slum = wdi("EN.POP.SLUM.UR.ZS")  # slum % of urban (sparse)

    rows = []
    for iso, name in ADB_DMCS.items():
        if not COASTAL.get(iso):
            continue
        u = urb.get(iso, {}).get("value")
        p = pop.get(iso, {}).get("value")
        s = slum.get(iso, {}).get("value")
        if u is None or p is None:
            continue
        # Index: log(pop) × urban% × slum% (where slum data exists; else conservative 10%)
        slum_proxy = s if s is not None else 10.0
        import math
        idx = round(math.log10(p) * (u / 100) * (slum_proxy / 100) * 100, 2)
        rows.append({
            "iso3": iso, "country": name,
            "coastal": 1,
            "urban_pct": round(u, 1),
            "population": int(p),
            "slum_pct_urban": round(s, 1) if s is not None else None,
            "slum_imputed": s is None,
            "coastal_informal_risk_index": idx,
        })
    rows.sort(key=lambda r: -r["coastal_informal_risk_index"])

    write_panel("coastal-informal-risk", {
        "program": "coastal-informal-risk",
        "claim_scope": "Hypothesis-stage screening result combining WDI urban share, population, and slum prevalence (where available) for ADB DMCs with a coastline. Slum data is sparse; imputed at 10% where missing (flagged per row). Sub-national LECZ analysis is the §18.5 upgrade-pass.",
        "framing_rule": "Coastal-zone informal-settlement structural-pressure proxy. Constitution §13.3 / §14: not a country-quality ranking.",
        "sources": {
            "wdi_urban_pct": "WDI SP.URB.TOTL.IN.ZS",
            "wdi_population": "WDI SP.POP.TOTL",
            "wdi_slum_pct": "WDI EN.POP.SLUM.UR.ZS (sparse — many NAs)",
            "coastal_flag": "manual ADB-DMC roster",
            "license": "WDI: CC BY 4.0",
            "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        },
        "methodology": {
            "coastal_informal_risk_index": "log10(population) × (urban_pct/100) × (slum_pct/100) × 100. Slum imputed at 10% where missing. Triage only.",
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })


# =========================================================================
# 2. invisible-urbanization
# =========================================================================

def run_urbanization():
    print("\n=== invisible-urbanization ===")
    urb_pct = wdi("SP.URB.TOTL.IN.ZS")
    urb_growth = wdi("SP.URB.GROW")
    rural_pct = wdi("SP.RUR.TOTL.ZS")
    pop = wdi("SP.POP.TOTL")

    rows = []
    for iso, name in ADB_DMCS.items():
        u = urb_pct.get(iso, {}).get("value")
        g = urb_growth.get(iso, {}).get("value")
        r = rural_pct.get(iso, {}).get("value")
        p = pop.get(iso, {}).get("value")
        if u is None or g is None or p is None:
            continue
        # Invisible-urbanization signal: still-mostly-rural countries with high urban growth.
        # Higher = more "growth-from-low-base" — likely sub-classification lag.
        rural_share = (r if r is not None else 100 - u) / 100
        invisible_signal = round(rural_share * max(g, 0) * 10, 2)
        rows.append({
            "iso3": iso, "country": name,
            "urban_pct": round(u, 1),
            "urban_pop_growth_pct": round(g, 2),
            "rural_pct": round(r, 1) if r is not None else round(100 - u, 1),
            "population": int(p),
            "invisible_urbanization_signal": invisible_signal,
        })
    rows.sort(key=lambda r: -r["invisible_urbanization_signal"])

    write_panel("invisible-urbanization", {
        "program": "invisible-urbanization",
        "claim_scope": "Hypothesis-stage screening: still-mostly-rural ADB DMCs with high urban-population growth, proxying for settlement growth that may not yet be reflected in urban classification. GHSL built-up-surface analysis is the §18.5 upgrade-pass.",
        "framing_rule": "Sub-classification-lag pressure proxy. Constitution §13.3 / §14: not a country-quality ranking.",
        "sources": {
            "wdi_urban_pct": "WDI SP.URB.TOTL.IN.ZS",
            "wdi_urban_pop_growth": "WDI SP.URB.GROW (% annual)",
            "wdi_rural_pct": "WDI SP.RUR.TOTL.ZS",
            "wdi_population": "WDI SP.POP.TOTL",
            "license": "WDI: CC BY 4.0",
            "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        },
        "methodology": {
            "invisible_urbanization_signal": "rural_share × urban_growth_rate × 10. Higher = more growth from a low-urbanization base. WDI growth-rate-only — no satellite cross-check yet. Triage only.",
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })


# =========================================================================
# 3. flood-market-access
# =========================================================================

def run_flood():
    print("\n=== flood-market-access ===")
    rural = wdi("SP.RUR.TOTL.ZS")
    pop = wdi("SP.POP.TOTL")
    floods = emdat_flood()

    rows = []
    for iso, name in ADB_DMCS.items():
        r = rural.get(iso, {}).get("value")
        p = pop.get(iso, {}).get("value")
        f = floods.get(iso)
        if r is None or p is None:
            continue
        flood_events = f.get("flood_events") if f else 0
        flood_share = f.get("flood_share") if f else 0
        # Index: rural_share × annual flood-events × log10(pop)
        import math
        rural_share = r / 100
        annual_floods = flood_events / 25  # 2000-2025 window
        idx = round(rural_share * annual_floods * math.log10(p), 2)
        rows.append({
            "iso3": iso, "country": name,
            "rural_pct": round(r, 1),
            "population": int(p),
            "flood_events_2000_2025": flood_events,
            "flood_share_of_all_disasters": round(flood_share, 3),
            "annual_flood_events": round(annual_floods, 2),
            "flood_market_access_index": idx,
        })
    rows.sort(key=lambda r: -r["flood_market_access_index"])

    write_panel("flood-market-access", {
        "program": "flood-market-access",
        "claim_scope": "Hypothesis-stage screening: rural-population × annual flood frequency × log(population). Proxies for flood-driven service-isolation pressure. EM-DAT flood subset (2000-2025) plus WDI rural and population. Sentinel-1 SAR / modeled flood layers are the §18.5 upgrade-pass.",
        "framing_rule": "Flood-driven service-isolation pressure proxy. Constitution §13.3 / §14.",
        "sources": {
            "emdat": "EM-DAT 2000-2025 flood subset (CRED, UCLouvain)",
            "wdi_rural_pct": "WDI SP.RUR.TOTL.ZS",
            "wdi_population": "WDI SP.POP.TOTL",
            "license": "WDI: CC BY 4.0; EM-DAT: non-commercial open access",
            "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        },
        "methodology": {
            "flood_market_access_index": "rural_share × annual_flood_events × log10(population). Triage only.",
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })


def main():
    run_coastal()
    run_urbanization()
    run_flood()


if __name__ == "__main__":
    main()
