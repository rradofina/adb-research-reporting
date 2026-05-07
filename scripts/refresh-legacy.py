"""Refresh legacy luminosity-gap programs into §18-format SR evidence.

Reads existing CSV outputs and produces standard {slug}/generated/{slug}-adb-panel.json
for access-services and air-monitoring. Also runs simple sensitivity.
"""
import json, csv
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def stable_set(rankings, k=5):
    sets = [set([r["iso3"] for r in lst[:k]]) for lst in rankings]
    return sorted(set.intersection(*sets) if sets else set())


# =========================================================================
# access-services
# =========================================================================

def run_access():
    src = ROOT / "luminosity-gap/research/access-services/generated/access-services-computed-admin1.csv"
    rows_raw = []
    with open(src, encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            rows_raw.append(r)

    # Aggregate to country level — average across ADM1, weighted by population
    by_country = {}
    for r in rows_raw:
        iso = r["iso3"]
        pop = float(r["population"]) if r["population"] else 0
        stress = float(r["access_stress_index"]) if r["access_stress_index"] else 0
        people_per_hf = float(r["people_per_health_facility"]) if r["people_per_health_facility"] else 0
        d = by_country.setdefault(iso, {"iso3": iso, "country": r["country_name"], "n_adm1": 0, "total_pop": 0, "weighted_stress_sum": 0, "max_people_per_hf": 0, "max_adm1": ""})
        d["n_adm1"] += 1
        d["total_pop"] += pop
        d["weighted_stress_sum"] += stress * pop
        if people_per_hf > d["max_people_per_hf"]:
            d["max_people_per_hf"] = people_per_hf
            d["max_adm1"] = r["admin1_name"]

    rows = []
    for iso, d in by_country.items():
        wstress = (d["weighted_stress_sum"] / d["total_pop"]) if d["total_pop"] else 0
        rows.append({
            "iso3": iso,
            "country": d["country"],
            "n_adm1_units": d["n_adm1"],
            "total_population": int(d["total_pop"]),
            "population_weighted_access_stress": round(wstress, 2),
            "worst_adm1_people_per_health_facility": int(d["max_people_per_hf"]),
            "worst_adm1_name": d["max_adm1"],
        })
    rows.sort(key=lambda r: -r["population_weighted_access_stress"])

    out = {
        "program": "access-services",
        "claim_scope": "Hypothesis-stage screening: country-level pop-weighted access-stress index from ADM1 OSM amenity counts × WorldPop / national-census population, across 8 ADB DMC pilots (PHL, BGD, PAK, NPL, LKA, KHM, LAO, TLS).",
        "framing_rule": "Service-access measurement-gap signal. Constitution §13.3 / §14.",
        "sources": {
            "osm_amenity_counts": "luminosity-gap/research/access-services pipeline; OSM via Overpass; geoBoundaries gbOpen ADM1",
            "population": "PSA 2020 Census + WorldPop 2024",
            "license": "OSM ODbL; geoBoundaries CC BY 4.0",
            "retrieved_at": "2026-04-23",
        },
        "methodology": {
            "access_stress_index": "Composite of {service_load_score, osm_completeness_risk_score} per ADM1 (legacy formulation), aggregated to country with population-weighted mean.",
        },
        "rows": rows,
        "n_adm1_total": len(rows_raw),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    out_dir = ROOT / "access-services/generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "access-services-adb-panel.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    with open(out_dir / "access-services-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)
    print(f"  access-services: {len(rows)} country rows from {len(rows_raw)} ADM1 rows; top-5 stress = {[r['iso3'] for r in rows[:5]]}")

    # Sensitivity: alternative country aggregation (mean vs population-weighted vs max-ADM1)
    mean_rank = sorted(rows, key=lambda r: -r["population_weighted_access_stress"])
    max_rank = sorted(rows, key=lambda r: -r["worst_adm1_people_per_health_facility"])
    runs = [
        {"label": "baseline_pop_weighted_stress", "top5": [{"iso3": r["iso3"], "country": r["country"], "value": r["population_weighted_access_stress"]} for r in mean_rank[:5]]},
        {"label": "alt_max_people_per_health_facility", "top5": [{"iso3": r["iso3"], "country": r["country"], "value": r["worst_adm1_people_per_health_facility"]} for r in max_rank[:5]]},
    ]
    common = stable_set([mean_rank, max_rank], k=5)
    sens_out = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "access-services",
        "metric": "country-level access-stress ranking + alt-aggregation stability",
        "common_top5_across_metrics": common,
        "runs": runs,
        "note": "Pilot covers 8 DMCs only (PHL, BGD, PAK, NPL, LKA, KHM, LAO, TLS). Sensitivity scope is limited; the §18.5 upgrade-pass extends to all 50 ADB DMCs.",
    }
    (ROOT / "access-services/sensitivity-runs.json").write_text(json.dumps(sens_out, indent=2))


# =========================================================================
# air-monitoring
# =========================================================================

def run_air():
    src = ROOT / "luminosity-gap/research/air-monitoring/generated/openaq-adb-regional-economies.csv"
    rows = []
    with open(src, encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            iso = r["iso3"]
            try: gap = float(r["pm25_observability_gap_score"]) if r["pm25_observability_gap_score"] else 0
            except: gap = 0
            try: pm25 = float(r["pm25_exposure_ugm3"]) if r["pm25_exposure_ugm3"] else 0
            except: pm25 = 0
            try: pop = int(float(r["population"])) if r["population"] else 0
            except: pop = 0
            try: locs = int(r["pm25_locations"]) if r["pm25_locations"] else 0
            except: locs = 0
            rows.append({
                "iso3": iso,
                "country": r.get("name", ""),
                "subregion": r.get("subregion", ""),
                "population": pop,
                "pm25_locations": locs,
                "pm25_exposure_ugm3": round(pm25, 2),
                "pm25_above_who_guideline_5_ugm3": r.get("pm25_above_who_guideline_5_ugm3") == "true",
                "pm25_observability_gap_score": round(gap, 1),
                "pm25_observability_status": r.get("pm25_observability_status", ""),
            })

    rows.sort(key=lambda r: -r["pm25_observability_gap_score"])

    out = {
        "program": "air-monitoring",
        "claim_scope": "Country-level PM2.5 observability-gap signal. Combines OpenAQ public PM2.5 monitor density (per-million-population) with WHO ambient PM2.5 exposure (above the 5 µg/m³ guideline). Higher gap = high pollution + thin public monitoring.",
        "framing_rule": "Observability-gap signal. Constitution §13.3 / §14.",
        "sources": {
            "openaq_v3": "OpenAQ API v3 — public PM2.5 monitor metadata (License CC BY 4.0)",
            "wdi_pm25": "WDI EN.ATM.PM25.MC.M3 (CC BY 4.0)",
            "who_aaq": "WHO Ambient AQ Database v6.1 (WHO open)",
            "retrieved_at": "2026-04-23",
        },
        "methodology": {
            "pm25_observability_gap_score": "Composite of (people-per-monitor) × (PM2.5-exposure-above-WHO-guideline). 0 = no gap (low pollution or dense monitoring), 100 = high pollution + sparse/no monitoring.",
        },
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    out_dir = ROOT / "air-monitoring/generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "air-monitoring-adb-panel.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    with open(out_dir / "air-monitoring-adb-panel.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows: w.writerow(row)
    print(f"  air-monitoring: {len(rows)} country rows; top-5 gap = {[r['iso3'] for r in rows[:5]]}")

    # Sensitivity: alternative ranking by raw monitor density vs gap-score
    by_gap = sorted(rows, key=lambda r: -r["pm25_observability_gap_score"])
    by_density = sorted([r for r in rows if r["pm25_locations"] > 0],
                        key=lambda r: -((r["population"] or 0) / r["pm25_locations"]) if r["pm25_locations"] else 0)
    by_density_no_monitor = sorted([r for r in rows if r["pm25_locations"] == 0 and r["pm25_above_who_guideline_5_ugm3"]],
                                    key=lambda r: -(r["population"] or 0))
    runs = [
        {"label": "baseline_gap_score", "top5": [{"iso3": r["iso3"], "country": r["country"], "value": r["pm25_observability_gap_score"]} for r in by_gap[:5]]},
        {"label": "alt_zero_monitors_above_guideline", "top5": [{"iso3": r["iso3"], "country": r["country"], "population": r["population"]} for r in by_density_no_monitor[:5]]},
    ]
    common = stable_set([by_gap, by_density_no_monitor], k=5)
    sens_out = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "program": "air-monitoring",
        "metric": "PM2.5 observability-gap ranking",
        "common_top5_across_metrics": common,
        "runs": runs,
    }
    (ROOT / "air-monitoring/sensitivity-runs.json").write_text(json.dumps(sens_out, indent=2))


def main():
    print("=== access-services ==="); run_access()
    print("=== air-monitoring ==="); run_air()


if __name__ == "__main__":
    main()
