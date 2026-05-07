"""Process NHFR data and compute OSM-vs-NHFR disagreement per ADM1."""
import json, glob, re, csv, os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"
os.makedirs(OUT_DIR, exist_ok=True)

# Load NHFR pages
files = []
for p in glob.glob(f"{CACHE}/nhfr_p*.json"):
    m = re.search(r"nhfr_p(\d+)\.json$", p)
    if m:
        files.append((int(m.group(1)), p))
files.sort()
all_recs = []
for _, p in files:
    all_recs.extend(json.load(open(p)).get("v_activefacilities", []))
print(f"NHFR total active facilities: {len(all_recs)}")

# Region mapping (DOH NHFR regcode -> ADM1 ISO 3166-2:PH)
REGCODE_TO_ADM1 = {
    "01": "PH-01", "02": "PH-02", "03": "PH-03", "04": "PH-40",
    "05": "PH-05", "06": "PH-06", "07": "PH-07", "08": "PH-08",
    "09": "PH-09", "10": "PH-10", "11": "PH-11", "12": "PH-12",
    "13": "PH-00", "14": "PH-15", "16": "PH-13", "17": "PH-41",
    "19": "PH-14",
}
# regcode 18 = abolished Negros Island Region; split by provcode
NIR_PROV_TO_ADM1 = {
    "18045": "PH-06",  # Negros Occidental -> Western Visayas
    "18302": "PH-06",  # Bacolod City HUC -> Western Visayas
    "18046": "PH-07",  # Negros Oriental -> Central Visayas
    "18061": "PH-07",  # Siquijor -> Central Visayas (inferred from barangay names: Bogo, Banban, Balolang)
}

PRINCIPAL_FACTYPES = {"01","03","04","05","15","17","19","21","22","23","24","51","52","53"}
CLINICAL_FACTYPES = PRINCIPAL_FACTYPES | {"14","20","27","28","09"}

# Aggregate by ADM1
admin_counts = defaultdict(lambda: {"all": 0, "principal": 0, "clinical": 0, "by_factype": Counter()})
unmapped = Counter()
for r in all_recs:
    rc = r.get("regcode")
    if rc == "18":
        prov = r.get("provcode") or ""
        adm1 = NIR_PROV_TO_ADM1.get(prov[:5]) or NIR_PROV_TO_ADM1.get(prov[:4])
    else:
        adm1 = REGCODE_TO_ADM1.get(rc)
    if not adm1:
        unmapped[(rc, r.get("provcode"))] += 1
        continue
    ft = r.get("factype") or ""
    admin_counts[adm1]["all"] += 1
    admin_counts[adm1]["by_factype"][ft] += 1
    if ft in PRINCIPAL_FACTYPES:
        admin_counts[adm1]["principal"] += 1
    if ft in CLINICAL_FACTYPES:
        admin_counts[adm1]["clinical"] += 1

print(f"Unmapped records: {sum(unmapped.values())}")
if unmapped:
    print(f"  details: {dict(unmapped.most_common(10))}")

# OSM counts from access-services
ACCESS_CSV = REPO_ROOT / "luminosity-gap" / "research" / "access-services" / "generated" / "access-services-computed-admin1.csv"
osm_counts = {}
with open(ACCESS_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["iso3"] != "PHL":
            continue
        osm_counts[row["admin1_code"]] = {
            "admin1_name": row["admin1_name"],
            "osm_health": int(row["health_facilities"]),
            "population": int(row["population"]),
            "osm_timestamp": row["osm_timestamp"],
        }

# Build the comparison table
print(f"\n{'=' * 118}")
print(f"{'ADM1':<7} {'Region':<22} {'OSM':>6} {'NHFR-prin':>10} {'NHFR-clin':>10} {'NHFR-all':>10} {'OSM/clin':>10} {'OSM/prin':>10} {'OSM/all':>10}")
print(f"{'=' * 118}")

output_rows = []
total_osm = 0
total_prin = 0
total_clin = 0
total_all = 0
for adm1 in sorted(osm_counts.keys()):
    info = osm_counts[adm1]
    nhfr = admin_counts.get(adm1, {"all": 0, "principal": 0, "clinical": 0, "by_factype": Counter()})
    osm = info["osm_health"]
    p = nhfr["principal"]
    c = nhfr["clinical"]
    a = nhfr["all"]
    total_osm += osm
    total_prin += p
    total_clin += c
    total_all += a
    rcl = (osm / c * 100) if c else 0.0
    rpr = (osm / p * 100) if p else 0.0
    rall = (osm / a * 100) if a else 0.0
    print(f"{adm1:<7} {info['admin1_name'][:22]:<22} {osm:>6} {p:>10} {c:>10} {a:>10} {rcl:>9.1f}% {rpr:>9.1f}% {rall:>9.1f}%")
    output_rows.append({
        "iso3": "PHL",
        "admin1_code": adm1,
        "admin1_name": info["admin1_name"],
        "population_2020": info["population"],
        "osm_health": osm,
        "nhfr_principal": p,
        "nhfr_clinical": c,
        "nhfr_all": a,
        "delta_osm_minus_principal": osm - p,
        "delta_osm_minus_clinical": osm - c,
        "delta_osm_minus_all": osm - a,
        "ratio_osm_to_principal": round(osm / p, 4) if p else None,
        "ratio_osm_to_clinical": round(osm / c, 4) if c else None,
        "ratio_osm_to_all": round(osm / a, 4) if a else None,
        "osm_per_100k": round(osm * 100000 / info["population"], 2) if info["population"] else None,
        "nhfr_principal_per_100k": round(p * 100000 / info["population"], 2) if info["population"] else None,
        "nhfr_clinical_per_100k": round(c * 100000 / info["population"], 2) if info["population"] else None,
        "osm_timestamp": info["osm_timestamp"],
        "nhfr_retrieved_at": "2026-04-25",
        "nhfr_source_url": "https://nhfr.doh.gov.ph/api/list/v_activefacilities",
    })

print(f"{'-' * 118}")
total_rcl = (total_osm / total_clin * 100) if total_clin else 0.0
total_rpr = (total_osm / total_prin * 100) if total_prin else 0.0
total_rall = (total_osm / total_all * 100) if total_all else 0.0
print(f"{'TOTAL':<7} {'':<22} {total_osm:>6} {total_prin:>10} {total_clin:>10} {total_all:>10} {total_rcl:>9.1f}% {total_rpr:>9.1f}% {total_rall:>9.1f}%")

# Country-level summary
gen_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
country_summary = {
    "iso3": "PHL",
    "country": "Philippines",
    "totals": {
        "osm_health": total_osm,
        "nhfr_principal": total_prin,
        "nhfr_clinical": total_clin,
        "nhfr_all": total_all,
        "ratio_osm_to_principal": round(total_osm / total_prin, 4) if total_prin else None,
        "ratio_osm_to_clinical": round(total_osm / total_clin, 4) if total_clin else None,
        "ratio_osm_to_all": round(total_osm / total_all, 4) if total_all else None,
    },
    "interpretation": (
        "OSM amenity=hospital/clinic/doctors counts capture roughly "
        f"{total_rpr:.1f}% of NHFR 'principal' health facilities (hospitals, RHUs, "
        f"main clinics, city health offices), {total_rcl:.1f}% of OSM-comparable "
        "facilities including barangay health stations and dialysis centers, and "
        f"{total_rall:.1f}% of all NHFR-active facilities including labs, dental, "
        "and drug-testing centers. The clinical-tier gap (~"
        f"{100 - total_rcl:.0f}% of NHFR-clinical not in OSM) is dominated by "
        "barangay health stations (factype 20, 27,052 records nationally), "
        "which OSM volunteers under-map. The principal-tier gap is smaller "
        f"(~{100 - total_rpr:.0f}%) and likely reflects the long tail of small "
        "lying-in clinics and rural primary-care facilities."
    ),
}

print("\n=== Per-region disagreement (clinical tier) ranked ===")
ranked = sorted(output_rows, key=lambda r: (r["ratio_osm_to_clinical"] or 0))
for r in ranked:
    rcl = r["ratio_osm_to_clinical"]
    print(f"  {r['admin1_code']:<7} {r['admin1_name'][:22]:<22} ratio={rcl:.3f}" if rcl else f"  {r['admin1_code']} {r['admin1_name']} ratio=NaN")

# Write outputs
metadata = {
    "program": "public-service-data-quality",
    "iso3": "PHL",
    "claim_scope": (
        "Hypothesis-stage screening result for the Philippines (single-DMC pilot). "
        "Compares OSM-mapped health-amenity counts (from access-services pipeline cache) "
        "with the official DOH National Health Facility Registry. Owner sign-off "
        "on first testable claim and falsification condition pending per CONSTITUTION.md "
        "§6.1 and literature.md §4."
    ),
    "framing_rule": (
        "This is a measurement-gap signal, not a country quality ranking. "
        "Per CONSTITUTION.md §13.3 and §14, framing is 'OSM vs. official-registry "
        "coverage gap' rather than 'country administrative-data quality'."
    ),
    "generated_at": gen_at,
    "country_summary": country_summary,
    "sources": {
        "osm": {
            "pipeline": "access-services-pipeline",
            "output": "luminosity-gap/research/access-services/generated/access-services-computed-admin1.csv",
            "filter": "rows where iso3 == 'PHL'",
            "osm_query_mode": "osm_area_iso3166_2 (Overpass admin-area queries)",
            "license": "ODbL (OpenStreetMap)",
            "vintage_window": "2026-04-05 to 2026-04-23 per row osm_timestamp",
        },
        "nhfr": {
            "name": "DOH National Health Facility Registry v2.0",
            "url": "https://nhfr.doh.gov.ph/VActivefacilitiesList",
            "api": "/api/list/v_activefacilities (JWT issued per landing page)",
            "access_model": "A (public, JWT-issued per landing page; no login required)",
            "license": "Unstated. Public-information-disclosure framing per Philippine Republic Act 9485.",
            "fetched_at": "2026-04-25",
            "total_active_facilities": len(all_recs),
            "pages_cached": 23,
            "page_size": 2000,
        },
    },
    "methodology": {
        "regcode_to_adm1_mapping": REGCODE_TO_ADM1,
        "nir_provcode_split": NIR_PROV_TO_ADM1,
        "principal_factypes": sorted(PRINCIPAL_FACTYPES),
        "clinical_factypes": sorted(CLINICAL_FACTYPES),
        "factype_principal_definition": (
            "Hospitals, tertiary medical centers, main clinics, RHUs, MHOs, city "
            "health offices, government and private hospitals, subnational reference "
            "centers. Excludes BHS, labs, dental, drug-testing, warehouses."
        ),
        "factype_clinical_definition": (
            "Adds Barangay Health Stations (factype 20), dialysis centers, "
            "social hygiene clinics, PCR testing labs, ambulatory surgical clinics. "
            "Closer to OSM amenity=hospital/clinic/doctors universe but still "
            "imperfect — many BHSs are unmapped in OSM."
        ),
        "regcode_18_handling": (
            "Negros Island Region (NIR) was abolished in 2017 but DOH NHFR retains "
            "regcode 18. Split by provcode: 18045/18302 -> PH-06 (Western Visayas), "
            "18046 -> PH-07 (Central Visayas)."
        ),
        "unmapped_records": sum(unmapped.values()),
    },
    "first_testable_claim_status": "AI-drafted in literature.md §4; owner sign-off pending.",
    "rows": output_rows,
}

with open(f"{OUT_DIR}/public-service-data-quality-PHL.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

with open(f"{OUT_DIR}/public-service-data-quality-PHL.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
    w.writeheader()
    for row in output_rows:
        w.writerow(row)

print(f"\nWrote: {OUT_DIR}/public-service-data-quality-PHL.json")
print(f"Wrote: {OUT_DIR}/public-service-data-quality-PHL.csv")
print(f"\nDONE. Country totals: OSM={total_osm}, NHFR-principal={total_prin}, NHFR-clinical={total_clin}, NHFR-all={total_all}")
print(f"Country-level OSM/NHFR-clinical capture rate: {total_rcl:.1f}%")
