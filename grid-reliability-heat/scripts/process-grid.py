"""Program 10 — Grid Reliability Under Heat.

Hypothesis-stage screening: combines
  - WRI Global Power Plant Database v1.3.0 (capacity, fuel, location)
  - WDI EG.ELC.ACCS.ZS (electricity access, % population)

For each ADB regional DMC, computes:
  - plant count, total installed capacity (MW), capacity per million people
  - fuel-mix concentration (Herfindahl-style) on capacity share
  - latest electricity access %

This is NOT yet a heat-stress reliability metric. The first compute target
in the program README calls for ERA5-Land tasmax × outage frequency, which
needs Earth Engine. This script produces the macro layer that the heat-
overlay will be joined to.

Per CONSTITUTION.md §3.3 / §6.4: composite indices are triage; outputs
are framed as "structural exposure" not "reliability ranking."
"""
import json, csv, os, statistics
from collections import defaultdict, Counter
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/grid-reliability-heat/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/grid-reliability-heat/generated"
os.makedirs(OUT, exist_ok=True)

ADB_DMCS = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China",
    "FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong SAR, China",
    "IND":"India","IDN":"Indonesia","KAZ":"Kazakhstan","KIR":"Kiribati",
    "KGZ":"Kyrgyzstan","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia, Fed. Sts.",
    "MNG":"Mongolia","MMR":"Myanmar","NPL":"Nepal",
    "PAK":"Pakistan","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam",
    "TWN":"Taiwan",
}


def load_wdi_indicator(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if not isinstance(d, list) or len(d) < 2:
        return {}
    out = {}
    for row in d[1]:
        if not isinstance(row.get("value"), (int, float)):
            continue
        iso3 = row.get("countryiso3code")
        if iso3 not in ADB_DMCS:
            continue
        year = int(row.get("date"))
        val = float(row["value"])
        if iso3 not in out or year > out[iso3]["year"]:
            out[iso3] = {"year": year, "value": val}
    return out


def main():
    elec_access = load_wdi_indicator(f"{CACHE}/wdi_elec_access.json")
    energy_use = load_wdi_indicator(f"{CACHE}/wdi_energy_use.json")

    # WRI GPP v1.3.0
    plants = []
    with open(f"{CACHE}/global_power_plant_database.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            iso = row.get("country", "").strip()
            if iso not in ADB_DMCS: continue
            try:
                cap = float(row.get("capacity_mw") or 0)
            except ValueError:
                cap = 0
            plants.append({
                "iso3": iso, "name": row.get("name"),
                "capacity_mw": cap,
                "primary_fuel": (row.get("primary_fuel") or "Unknown").strip(),
                "lat": row.get("latitude"), "lon": row.get("longitude"),
                "year": row.get("commissioning_year"),
            })

    # Per-DMC aggregation
    by_iso = defaultdict(list)
    for p in plants: by_iso[p["iso3"]].append(p)

    rows = []
    for iso, name in sorted(ADB_DMCS.items(), key=lambda x: x[1]):
        ps = by_iso.get(iso, [])
        total_cap = sum(p["capacity_mw"] for p in ps)
        fuel_cap = defaultdict(float)
        for p in ps: fuel_cap[p["primary_fuel"]] += p["capacity_mw"]
        # Herfindahl-style concentration on capacity share
        if total_cap > 0:
            shares = [v/total_cap for v in fuel_cap.values()]
            herfindahl = round(sum(s*s for s in shares), 4)
        else:
            herfindahl = None
        top_fuel = max(fuel_cap.items(), key=lambda x: x[1])[0] if fuel_cap else None
        top_fuel_share = round(fuel_cap[top_fuel]/total_cap, 4) if (top_fuel and total_cap) else None

        ea = elec_access.get(iso)
        eu = energy_use.get(iso)
        rows.append({
            "iso3": iso, "country": name,
            "plant_count": len(ps),
            "total_capacity_mw": round(total_cap, 1),
            "top_fuel": top_fuel,
            "top_fuel_share": top_fuel_share,
            "fuel_herfindahl": herfindahl,
            "wdi_elec_access_pct": ea["value"] if ea else None,
            "wdi_elec_access_year": ea["year"] if ea else None,
            "wdi_energy_use_kgoe_per_capita": eu["value"] if eu else None,
            "wdi_energy_use_year": eu["year"] if eu else None,
            "fuel_mix_capacity_mw": {k: round(v,1) for k,v in sorted(fuel_cap.items(), key=lambda x:-x[1])},
        })

    # Top concentration: rank by herfindahl (single-fuel risk)
    rows.sort(key=lambda r: -(r["fuel_herfindahl"] or 0))

    # Globally distinct fuel categories observed in ADB DMCs
    fuels = Counter()
    for p in plants: fuels[p["primary_fuel"]] += 1

    payload = {
        "program": "grid-reliability-heat",
        "claim_scope": (
            "Hypothesis-stage structural-exposure layer. WRI Global Power Plant "
            "Database v1.3.0 capacity + fuel-mix concentration + WDI access. "
            "NOT yet a heat-stress reliability metric — that requires ERA5-Land × "
            "outage records or generation-loss data, which need separate work."
        ),
        "framing_rule": (
            "Structural exposure metric: high single-fuel concentration + high "
            "thermal share + climate sensitivity = vulnerability to a single-"
            "shock pathway. Not a reliability ranking."
        ),
        "sources": {
            "wri_gpp": {
                "name": "WRI Global Power Plant Database v1.3.0",
                "url": "https://github.com/wri/global-power-plant-database",
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
                "version_note": "Frozen at v1.3.0; not maintained by WRI since 2022. Plant-level snapshot.",
                "rows_total": len(plants),
            },
            "wdi_elec_access": {
                "name": "EG.ELC.ACCS.ZS — Access to electricity (% population)",
                "url": "https://api.worldbank.org/v2/country/all/indicator/EG.ELC.ACCS.ZS",
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
            "wdi_energy_use": {
                "name": "EG.USE.PCAP.KG.OE — Energy use (kg oil equiv. per capita)",
                "url": "https://api.worldbank.org/v2/country/all/indicator/EG.USE.PCAP.KG.OE",
                "license": "CC BY 4.0",
                "retrieved_at": "2026-04-25",
            },
        },
        "methodology": {
            "fuel_herfindahl": (
                "Sum of squared fuel-share-of-capacity. 1.0 = single-fuel grid; "
                "low = diversified."
            ),
        },
        "global_fuel_distribution_in_adb_plants": dict(fuels.most_common()),
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/grid-reliability-heat-adb-panel.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    csv_rows = [{k: v for k, v in r.items() if k != "fuel_mix_capacity_mw"} for r in rows]
    with open(f"{OUT}/grid-reliability-heat-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        if csv_rows:
            w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            w.writeheader()
            for row in csv_rows: w.writerow(row)

    print("=== Most fuel-concentrated DMC grids (top 12) ===")
    for r in rows[:12]:
        print(f"  {r['iso3']:<4} {r['country'][:25]:<25} plants={r['plant_count']:>4}  cap={r['total_capacity_mw']:>10.1f} MW  herf={r['fuel_herfindahl']}  top={r['top_fuel']} ({(r['top_fuel_share'] or 0)*100:.1f}%)")
    print(f"\nWrote {OUT}/grid-reliability-heat-adb-panel.json + .csv")
    print(f"Total ADB-DMC plants: {len(plants)}; fuels: {dict(fuels.most_common(10))}")


if __name__ == "__main__":
    main()
