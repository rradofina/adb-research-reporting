"""Leave-one-out ADM1 robustness for PSDQ.

For each ADM1 in PHL and BGD, drop it and recompute the country
clinical-tier ratio + the rural-urban gradient. Reports the range
across the leave-one-out reruns. Implements the OPHI-synthesized
objection in review-external.md (capability-delivery aggregation).
"""

import json, glob, re, csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CACHE = ROOT / ".cache"
ACCESS_CSV = REPO_ROOT / "luminosity-gap" / "research" / "access-services" / "generated" / "access-services-computed-admin1.csv"

# PHL setup
PHL_REGCODE_TO_ADM1 = {
    "01": "PH-01", "02": "PH-02", "03": "PH-03", "04": "PH-40",
    "05": "PH-05", "06": "PH-06", "07": "PH-07", "08": "PH-08",
    "09": "PH-09", "10": "PH-10", "11": "PH-11", "12": "PH-12",
    "13": "PH-00", "14": "PH-15", "16": "PH-13", "17": "PH-41",
    "19": "PH-14",
}
PHL_NIR_PROV_TO_ADM1 = {
    "18045": "PH-06", "18302": "PH-06",
    "18046": "PH-07", "18061": "PH-07",
}
PHL_PRINCIPAL = {"01","03","04","05","15","17","19","21","22","23","24","51","52","53"}
PHL_CLINICAL = PHL_PRINCIPAL | {"14","20","27","28","09"}


def phl_records():
    files = sorted([(int(re.search(r"nhfr_p(\d+)\.json$", p).group(1)), p)
                    for p in glob.glob(str(CACHE / "nhfr_p*.json"))])
    recs = []
    for _, p in files:
        recs.extend(json.load(open(p, encoding="utf-8")).get("v_activefacilities", []))
    return recs


def phl_clinical_per_adm1(recs):
    counts = defaultdict(int)
    for r in recs:
        rc = r.get("regcode")
        if rc == "18":
            prov = r.get("provcode") or ""
            adm1 = PHL_NIR_PROV_TO_ADM1.get(prov[:5]) or PHL_NIR_PROV_TO_ADM1.get(prov[:4])
        else:
            adm1 = PHL_REGCODE_TO_ADM1.get(rc)
        if not adm1: continue
        ft = r.get("factype") or ""
        if ft in PHL_CLINICAL:
            counts[adm1] += 1
    return dict(counts)


def phl_osm_per_adm1():
    out = {}
    with open(ACCESS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["iso3"] != "PHL": continue
            out[row["admin1_code"]] = int(row["health_facilities"])
    return out


# BGD setup
BGD_DIVISION_TO_ADM1 = {
    "Barisal": "BD-A", "Barishal": "BD-A",
    "Chattogram": "BD-B", "Chittagong": "BD-B",
    "Dhaka": "BD-C", "Khulna": "BD-D",
    "Rajshahi": "BD-E", "Rajshani": "BD-E",
    "Rangpur": "BD-F", "Sylhet": "BD-G",
    "Mymensingh": "BD-H",
}


def bgd_categorize(name):
    n = (name or "").lower()
    if not n: return False
    if any(w in n for w in ["office", "municipality", "city corporation zone",
                             "nursing college", "nursing institute",
                             "ngo for government", "warehouse", "store",
                             "training centre", "training center"]):
        return False
    if n == "consultancy & diagnostic center" or "diagnostic centre" in n:
        return False
    if "blood bank" in n: return True
    if any(w in n for w in ["community clinic", "union health",
                             "maternal & child welfare",
                             "family welfare center", "chest disease clinic"]):
        return True
    if any(w in n for w in ["hospital", "medical college", "clinic"]):
        return True
    return False


def bgd_records():
    files = sorted([(int(re.search(r"bgd_dghs_p(\d+)\.json$", p).group(1)), p)
                    for p in glob.glob(str(CACHE / "bgd_dghs_p*.json"))])
    recs = []
    for _, p in files:
        recs.extend(json.load(open(p, encoding="utf-8")).get("data", []))
    return recs


def bgd_clinical_per_adm1(recs):
    counts = defaultdict(int)
    for r in recs:
        adm1 = BGD_DIVISION_TO_ADM1.get(r.get("division_name") or "")
        if not adm1: continue
        if bgd_categorize(r.get("facility_type_name")):
            counts[adm1] += 1
    return dict(counts)


def bgd_osm_per_adm1():
    out = {}
    with open(ACCESS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["iso3"] != "BGD": continue
            out[row["admin1_code"]] = int(row["health_facilities"])
    return out


def country_ratio(osm, reg, drop=None):
    o = sum(v for k, v in osm.items() if k != drop)
    r = sum(v for k, v in reg.items() if k != drop)
    return (o / r) if r else None


def main():
    out = {"generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}

    # PHL
    phl_recs = phl_records()
    phl_reg = phl_clinical_per_adm1(phl_recs)
    phl_osm = phl_osm_per_adm1()
    phl_adm1s = sorted(set(phl_osm.keys()) | set(phl_reg.keys()))
    phl_baseline = country_ratio(phl_osm, phl_reg)
    phl_loo = []
    for a in phl_adm1s:
        r = country_ratio(phl_osm, phl_reg, drop=a)
        delta = (r - phl_baseline) if r is not None else None
        phl_loo.append({"dropped_adm1": a, "country_ratio": round(r, 4) if r else None,
                         "delta_vs_baseline": round(delta, 4) if delta is not None else None})
    phl_loo.sort(key=lambda x: -abs(x["delta_vs_baseline"] or 0))

    out["phl"] = {
        "baseline_country_ratio": round(phl_baseline, 4),
        "n_adm1": len(phl_adm1s),
        "leave_one_out": phl_loo,
        "max_delta_abs": max((abs(x["delta_vs_baseline"]) for x in phl_loo if x["delta_vs_baseline"] is not None), default=0),
        "max_impact_adm1": phl_loo[0]["dropped_adm1"] if phl_loo else None,
    }

    # BGD
    bgd_recs = bgd_records()
    bgd_reg = bgd_clinical_per_adm1(bgd_recs)
    bgd_osm = bgd_osm_per_adm1()
    bgd_adm1s = sorted(set(bgd_osm.keys()) | set(bgd_reg.keys()))
    bgd_baseline = country_ratio(bgd_osm, bgd_reg)
    bgd_loo = []
    for a in bgd_adm1s:
        r = country_ratio(bgd_osm, bgd_reg, drop=a)
        delta = (r - bgd_baseline) if r is not None else None
        bgd_loo.append({"dropped_adm1": a, "country_ratio": round(r, 4) if r else None,
                         "delta_vs_baseline": round(delta, 4) if delta is not None else None})
    bgd_loo.sort(key=lambda x: -abs(x["delta_vs_baseline"] or 0))

    out["bgd"] = {
        "baseline_country_ratio": round(bgd_baseline, 4),
        "n_adm1": len(bgd_adm1s),
        "leave_one_out": bgd_loo,
        "max_delta_abs": max((abs(x["delta_vs_baseline"]) for x in bgd_loo if x["delta_vs_baseline"] is not None), default=0),
        "max_impact_adm1": bgd_loo[0]["dropped_adm1"] if bgd_loo else None,
    }

    out_path = ROOT / "leave-one-out-runs.json"
    out_path.write_text(json.dumps(out, indent=2))

    print(f"PHL baseline = {phl_baseline:.4f}  (17 ADM1)")
    print(f"  max LOO delta = {out['phl']['max_delta_abs']:.4f} when {out['phl']['max_impact_adm1']} dropped")
    print(f"\nBGD baseline = {bgd_baseline:.4f}  (8 divisions)")
    print(f"  max LOO delta = {out['bgd']['max_delta_abs']:.4f} when {out['bgd']['max_impact_adm1']} dropped")
    print(f"\nLeave-one-out range PHL: {min(x['country_ratio'] for x in phl_loo if x['country_ratio']):.4f} to {max(x['country_ratio'] for x in phl_loo if x['country_ratio']):.4f}")
    print(f"Leave-one-out range BGD: {min(x['country_ratio'] for x in bgd_loo if x['country_ratio']):.4f} to {max(x['country_ratio'] for x in bgd_loo if x['country_ratio']):.4f}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
