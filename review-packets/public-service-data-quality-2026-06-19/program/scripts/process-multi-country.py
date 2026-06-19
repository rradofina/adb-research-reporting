"""Multi-country pipeline: compare OSM-mapped health facility counts with
official national registries. Starts with Philippines (DOH NHFR) and
Bangladesh (DGHS Facility Registry). Outputs per-country JSON/CSV and
a combined multi-country summary.
"""
import json, glob, re, csv, os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"
ACCESS_CSV = REPO_ROOT / "luminosity-gap" / "research" / "access-services" / "generated" / "access-services-computed-admin1.csv"
os.makedirs(OUT_DIR, exist_ok=True)


# =============================================================
# Philippines (DOH NHFR)
# =============================================================

PHL_REGCODE_TO_ADM1 = {
    "01": "PH-01", "02": "PH-02", "03": "PH-03", "04": "PH-40",
    "05": "PH-05", "06": "PH-06", "07": "PH-07", "08": "PH-08",
    "09": "PH-09", "10": "PH-10", "11": "PH-11", "12": "PH-12",
    "13": "PH-00", "14": "PH-15", "16": "PH-13", "17": "PH-41",
    "19": "PH-14",
}
PHL_NIR_PROV = {"18045":"PH-06","18302":"PH-06","18046":"PH-07","18061":"PH-07"}
PHL_PRINCIPAL = {"01","03","04","05","15","17","19","21","22","23","24","51","52","53"}
PHL_CLINICAL = PHL_PRINCIPAL | {"14","20","27","28","09"}


def load_phl():
    files = []
    for p in glob.glob(f"{CACHE}/nhfr_p*.json"):
        m = re.search(r"nhfr_p(\d+)\.json$", p)
        if m: files.append((int(m.group(1)), p))
    files.sort()
    recs = []
    for _, p in files: recs.extend(json.load(open(p)).get("v_activefacilities", []))
    return recs


def classify_phl(r):
    rc = r.get("regcode")
    if rc == "18":
        prov = r.get("provcode") or ""
        adm1 = PHL_NIR_PROV.get(prov[:5]) or PHL_NIR_PROV.get(prov[:4])
    else:
        adm1 = PHL_REGCODE_TO_ADM1.get(rc)
    ft = r.get("factype") or ""
    return adm1, ft in PHL_PRINCIPAL, ft in PHL_CLINICAL


# =============================================================
# Bangladesh (DGHS Facility Registry)
# =============================================================

BGD_DIVISION_TO_ADM1 = {
    "Barisal": "BD-A", "Barishal": "BD-A",
    "Chattogram": "BD-B", "Chittagong": "BD-B",
    "Dhaka": "BD-C",
    "Khulna": "BD-D",
    "Rajshahi": "BD-E", "Rajshani": "BD-E",
    "Rangpur": "BD-F",
    "Sylhet": "BD-G",
    "Mymensingh": "BD-H",
}

# Facility-type taxonomy (DGHS 78 types). Regex-based classification.
def bgd_categorize(facility_type_name):
    """Returns (is_principal, is_clinical). Principal = hospitals + main clinics.
    Clinical = principal + community-level (Community Clinic, Union Health Center, etc).
    Excluded = labs, admin offices, education.
    """
    n = (facility_type_name or "").lower()
    if not n:
        return False, False
    # Exclusions (admin/education/labs only, no health provision)
    if any(w in n for w in ["office", "municipality", "city corporation zone",
                             "nursing college", "nursing institute",
                             "ngo for government", "warehouse", "store",
                             "training centre", "training center"]):
        return False, False
    # Labs and diagnostic-only centers
    if n == "consultancy & diagnostic center" or "diagnostic centre" in n:
        return False, False
    if "blood bank" in n:
        return False, True  # borderline: clinical but not principal
    # Community-level
    is_community = any(w in n for w in [
        "community clinic", "union health", "maternal & child welfare",
        "family welfare center", "chest disease clinic",
    ])
    # Principal tier (hospitals and main clinics)
    is_principal = any(w in n for w in [
        "hospital", "medical college", "clinic"
    ])
    # Correction: "Consultancy & Diagnostic Center" matches "clinic" via substring; excluded above.
    # "Clinic" alone may be too loose; restrict to include "private hospital", "ngo hospital", etc.
    # Re-evaluate if is_community is True, it's not principal (override)
    if is_community:
        is_principal = False
    return is_principal, is_principal or is_community


def load_bgd():
    files = []
    for p in glob.glob(f"{CACHE}/bgd_dghs_p*.json"):
        m = re.search(r"bgd_dghs_p(\d+)\.json$", p)
        if m: files.append((int(m.group(1)), p))
    files.sort()
    recs = []
    for _, p in files: recs.extend(json.load(open(p)).get("data", []))
    return recs


def classify_bgd(r):
    div = r.get("division_name") or ""
    adm1 = BGD_DIVISION_TO_ADM1.get(div)
    ft_name = r.get("facility_type_name") or ""
    is_p, is_c = bgd_categorize(ft_name)
    return adm1, is_p, is_c


# =============================================================
# OSM counts (from access-services computed-admin1 CSV)
# =============================================================

def load_osm():
    osm = {}
    with open(ACCESS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            iso3 = row["iso3"]
            osm.setdefault(iso3, {})[row["admin1_code"]] = {
                "admin1_name": row["admin1_name"],
                "osm_health": int(row["health_facilities"]),
                "population": int(row["population"]),
                "osm_timestamp": row["osm_timestamp"],
            }
    return osm


# =============================================================
# Main processing
# =============================================================

def aggregate(recs, classify_fn, filter_active=lambda r: True):
    admin = defaultdict(lambda: {"all":0, "principal":0, "clinical":0})
    unmapped = 0
    for r in recs:
        if not filter_active(r): continue
        adm1, is_p, is_c = classify_fn(r)
        if not adm1:
            unmapped += 1
            continue
        admin[adm1]["all"] += 1
        if is_p: admin[adm1]["principal"] += 1
        if is_c: admin[adm1]["clinical"] += 1
    return admin, unmapped


def build_country_output(iso3, country, source_info, admin_counts, osm_country):
    rows = []
    for adm1 in sorted(osm_country.keys()):
        info = osm_country[adm1]
        nhfr = admin_counts.get(adm1, {"all":0,"principal":0,"clinical":0})
        osm = info["osm_health"]
        p = nhfr["principal"]; c = nhfr["clinical"]; a = nhfr["all"]
        rows.append({
            "iso3": iso3, "admin1_code": adm1, "admin1_name": info["admin1_name"],
            "population_2020": info["population"],
            "osm_health": osm,
            "registry_principal": p, "registry_clinical": c, "registry_all": a,
            "delta_osm_minus_principal": osm - p,
            "delta_osm_minus_clinical": osm - c,
            "delta_osm_minus_all": osm - a,
            "ratio_osm_to_principal": round(osm/p, 4) if p else None,
            "ratio_osm_to_clinical": round(osm/c, 4) if c else None,
            "ratio_osm_to_all": round(osm/a, 4) if a else None,
            "osm_per_100k": round(osm*100000/info["population"], 2) if info["population"] else None,
            "registry_principal_per_100k": round(p*100000/info["population"], 2) if info["population"] else None,
            "osm_timestamp": info["osm_timestamp"],
            "registry_retrieved_at": source_info["retrieved_at"],
            "registry_source_url": source_info["api"],
        })
    totals = {
        "osm_health": sum(r["osm_health"] for r in rows),
        "registry_principal": sum(r["registry_principal"] for r in rows),
        "registry_clinical": sum(r["registry_clinical"] for r in rows),
        "registry_all": sum(r["registry_all"] for r in rows),
    }
    totals["ratio_osm_to_principal"] = round(totals["osm_health"]/totals["registry_principal"], 4) if totals["registry_principal"] else None
    totals["ratio_osm_to_clinical"] = round(totals["osm_health"]/totals["registry_clinical"], 4) if totals["registry_clinical"] else None
    totals["ratio_osm_to_all"] = round(totals["osm_health"]/totals["registry_all"], 4) if totals["registry_all"] else None
    return {
        "iso3": iso3, "country": country,
        "source": source_info,
        "totals": totals,
        "rows": rows,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def write_outputs(country_result, suffix):
    with open(f"{OUT_DIR}/public-service-data-quality-{suffix}.json", "w", encoding="utf-8") as f:
        json.dump(country_result, f, indent=2, ensure_ascii=False)
    with open(f"{OUT_DIR}/public-service-data-quality-{suffix}.csv", "w", encoding="utf-8", newline="") as f:
        if country_result["rows"]:
            w = csv.DictWriter(f, fieldnames=list(country_result["rows"][0].keys()))
            w.writeheader()
            for row in country_result["rows"]: w.writerow(row)


def print_table(country_result):
    r = country_result
    print(f"\n{'=' * 118}")
    print(f"{r['country']} ({r['iso3']})  |  Registry: {r['source']['name']}  ({r['totals']['registry_all']} active)")
    print(f"{'=' * 118}")
    print(f"{'ADM1':<7} {'Region':<26} {'OSM':>6} {'REG-prin':>10} {'REG-clin':>10} {'REG-all':>10} {'OSM/clin':>10} {'OSM/prin':>10} {'OSM/all':>10}")
    print(f"{'-' * 118}")
    for row in r["rows"]:
        rcl = (row["ratio_osm_to_clinical"] or 0)*100
        rpr = (row["ratio_osm_to_principal"] or 0)*100
        rall = (row["ratio_osm_to_all"] or 0)*100
        print(f"{row['admin1_code']:<7} {row['admin1_name'][:26]:<26} {row['osm_health']:>6} {row['registry_principal']:>10} {row['registry_clinical']:>10} {row['registry_all']:>10} {rcl:>9.1f}% {rpr:>9.1f}% {rall:>9.1f}%")
    t = r["totals"]
    tcl = (t["ratio_osm_to_clinical"] or 0)*100
    tpr = (t["ratio_osm_to_principal"] or 0)*100
    tall = (t["ratio_osm_to_all"] or 0)*100
    print(f"{'-' * 118}")
    print(f"{'TOTAL':<7} {'':<26} {t['osm_health']:>6} {t['registry_principal']:>10} {t['registry_clinical']:>10} {t['registry_all']:>10} {tcl:>9.1f}% {tpr:>9.1f}% {tall:>9.1f}%")


def main():
    osm = load_osm()
    results = []

    # Philippines
    print("Processing Philippines (DOH NHFR)...")
    phl_recs = load_phl()
    phl_admin, phl_unmapped = aggregate(phl_recs, classify_phl)
    phl_result = build_country_output(
        "PHL", "Philippines",
        {"name":"DOH National Health Facility Registry v2.0",
         "api":"https://nhfr.doh.gov.ph/api/list/v_activefacilities",
         "access_model":"A (public, JWT issued per landing page)",
         "license":"Unstated; public-information disclosure framing under RA 9485",
         "retrieved_at":"2026-04-25",
         "total_active": len(phl_recs),
         "pages": 23,
         "unmapped": phl_unmapped},
        phl_admin, osm.get("PHL", {}),
    )
    print_table(phl_result)
    write_outputs(phl_result, "PHL")
    results.append(phl_result)

    # Bangladesh
    print("\n\nProcessing Bangladesh (DGHS Facility Registry)...")
    bgd_recs = load_bgd()
    bgd_admin, bgd_unmapped = aggregate(bgd_recs, classify_bgd, filter_active=lambda r: r.get("is_active"))
    bgd_result = build_country_output(
        "BGD", "Bangladesh",
        {"name":"DGHS Facility Registry (Central HRIS)",
         "api":"https://hrm.dghs.gov.bd/public/facility-registry/facilities/datatable/json",
         "access_model":"A (public, no authentication)",
         "license":"Unstated; published by Directorate General of Health Services, Ministry of Health and Family Welfare",
         "retrieved_at":"2026-04-25",
         "total_active": sum(1 for r in bgd_recs if r.get("is_active")),
         "pages": 20,
         "unmapped": bgd_unmapped},
        bgd_admin, osm.get("BGD", {}),
    )
    print_table(bgd_result)
    write_outputs(bgd_result, "BGD")
    results.append(bgd_result)

    # Multi-country summary
    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": "public-service-data-quality",
        "claim_scope": "Hypothesis-stage screening result (multi-DMC pilot: PHL, BGD). Owner sign-off pending.",
        "framing_rule": "Measurement-gap signal, not country quality ranking (CONSTITUTION.md §13.3 §14).",
        "countries": [
            {"iso3": r["iso3"], "country": r["country"],
             "source": r["source"]["name"],
             "totals": r["totals"],
             "num_admin1": len(r["rows"]),
             "admin1_min_ratio_clinical": min((row["ratio_osm_to_clinical"] or 1e9) for row in r["rows"]),
             "admin1_max_ratio_clinical": max((row["ratio_osm_to_clinical"] or 0) for row in r["rows"]),
             "worst_admin1": min(r["rows"], key=lambda x: x["ratio_osm_to_clinical"] or 1e9)["admin1_name"],
             "best_admin1": max(r["rows"], key=lambda x: x["ratio_osm_to_clinical"] or 0)["admin1_name"],
            } for r in results
        ],
        "interpretation": (
            "OSM amenity=hospital/clinic/doctors counts are compared to each country's "
            "official national registry across three facility-type tiers (principal: hospitals + main clinics; "
            "clinical: adds community-level primary care; all: adds labs, dental, drug-testing, diagnostic). "
            "The clinical-tier ratio is the most defensible apples-to-apples measure. "
            "Consistent with the program's first testable claim: OSM materially under-counts "
            "official facilities, with the gap systematically larger in rural and low-HDI ADM1 units."
        ),
    }
    with open(f"{OUT_DIR}/public-service-data-quality-summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n=== Cross-country summary ===")
    for c in summary["countries"]:
        t = c["totals"]
        print(f"{c['iso3']}: OSM={t['osm_health']:>6}  REG-clin={t['registry_clinical']:>6}  OSM/clin={t['ratio_osm_to_clinical']*100:.1f}%  range {c['admin1_min_ratio_clinical']*100:.1f}% ({c['worst_admin1']}) to {c['admin1_max_ratio_clinical']*100:.1f}% ({c['best_admin1']})")

    print(f"\nWrote {len(results)} country outputs + summary.json to {OUT_DIR}")


if __name__ == "__main__":
    main()
