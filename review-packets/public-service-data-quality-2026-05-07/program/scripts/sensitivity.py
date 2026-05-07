"""Sensitivity suite at +/-50 percent for PSDQ.

Implements CONSTITUTION.md section 6.6 for the parameters listed in
pre-registration.md section 6. Re-computes the headline clinical-tier
OSM/registry ratio across alternative parameter values and writes the
deltas to ../sensitivity-runs.json. The accompanying sensitivity.md is
hand-edited to interpret the table.
"""

import json
import csv
import os
import re
import glob
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CACHE = ROOT / ".cache"
ACCESS_CSV = REPO_ROOT / "luminosity-gap" / "research" / "access-services" / "generated" / "access-services-computed-admin1.csv"
OUT = ROOT / "sensitivity-runs.json"

REGCODE_TO_ADM1 = {
    "01": "PH-01", "02": "PH-02", "03": "PH-03", "04": "PH-40",
    "05": "PH-05", "06": "PH-06", "07": "PH-07", "08": "PH-08",
    "09": "PH-09", "10": "PH-10", "11": "PH-11", "12": "PH-12",
    "13": "PH-00", "14": "PH-15", "16": "PH-13", "17": "PH-41",
    "19": "PH-14",
}
NIR_PROV_TO_ADM1 = {
    "18045": "PH-06", "18302": "PH-06",
    "18046": "PH-07", "18061": "PH-07",
}

# Baseline factype sets per pre-registration.md section 6.
BASELINE_PRINCIPAL = ["01","03","04","05","15","17","19","21","22","23","24","51","52","53"]
BASELINE_CLINICAL_EXTRA = ["14","20","27","28","09"]


def load_nhfr_records():
    files = []
    for p in glob.glob(str(CACHE / "nhfr_p*.json")):
        m = re.search(r"nhfr_p(\d+)\.json$", p)
        if m:
            files.append((int(m.group(1)), p))
    files.sort()
    recs = []
    for _, p in files:
        with open(p, encoding="utf-8") as f:
            recs.extend(json.load(f).get("v_activefacilities", []))
    return recs


def load_osm_phl():
    osm = {}
    with open(ACCESS_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["iso3"] != "PHL":
                continue
            osm[row["admin1_code"]] = {
                "name": row["admin1_name"],
                "osm_health": int(row["health_facilities"]),
                "population": int(row["population"]),
            }
    return osm


def map_record(rec, nir_map):
    rc = rec.get("regcode")
    if rc == "18":
        prov = rec.get("provcode") or ""
        return nir_map.get(prov[:5]) or nir_map.get(prov[:4])
    return REGCODE_TO_ADM1.get(rc)


def compute_ratios(recs, factype_set, nir_map):
    """Return dict[admin1] = (osm, registry_count, ratio) plus aggregates."""
    osm = load_osm_phl()
    reg = defaultdict(int)
    for r in recs:
        adm1 = map_record(r, nir_map)
        if adm1 is None:
            continue
        ft = r.get("factype") or ""
        if ft in factype_set:
            reg[adm1] += 1
    rows = {}
    total_osm = 0
    total_reg = 0
    for adm1, info in osm.items():
        rcount = reg.get(adm1, 0)
        ocount = info["osm_health"]
        ratio = (ocount / rcount) if rcount > 0 else None
        rows[adm1] = {"name": info["name"], "osm": ocount, "registry": rcount, "ratio": ratio}
        total_osm += ocount
        total_reg += rcount
    country_ratio = (total_osm / total_reg) if total_reg > 0 else None
    return rows, country_ratio, total_osm, total_reg


def gradient(rows, recs, nir_map, quintile_pct=20):
    """Compute rural-urban gradient by sorting ADM1 by OSM/registry ratio.

    Since per-ADM1 rural share is not directly available in this script,
    we use the registry-clinical/registry-all population proxy as a coarse
    rural-share substitute: regions with the lowest OSM/registry ratio are
    treated as 'most rural-leaning' for this script. The pre-registered
    rural-share definition (PSA 2020 census) is enforced in the article
    rerun, not here.
    """
    valid = [(k, v["ratio"]) for k, v in rows.items() if v["ratio"] is not None]
    if not valid:
        return None
    valid.sort(key=lambda x: x[1])
    n = len(valid)
    k = max(1, round(n * (quintile_pct / 100)))
    bottom = sum(r for _, r in valid[:k]) / k
    top = sum(r for _, r in valid[-k:]) / k
    return {"bottom_quintile_mean": bottom, "top_quintile_mean": top, "ratio_top_to_bottom": (top / bottom) if bottom > 0 else None, "k": k, "n": n}


def main():
    recs = load_nhfr_records()
    print(f"NHFR records: {len(recs)}")

    runs = []

    # Baseline
    clinical_set = set(BASELINE_PRINCIPAL + BASELINE_CLINICAL_EXTRA)
    rows, country_ratio, _, _ = compute_ratios(recs, clinical_set, NIR_PROV_TO_ADM1)
    grad = gradient(rows, recs, NIR_PROV_TO_ADM1)
    runs.append({
        "label": "baseline",
        "factype_set_size": len(clinical_set),
        "country_clinical_ratio": country_ratio,
        "gradient": grad,
        "min_admin1_ratio": min(r["ratio"] for r in rows.values() if r["ratio"] is not None),
        "max_admin1_ratio": max(r["ratio"] for r in rows.values() if r["ratio"] is not None),
    })

    # +/-50 percent on CLINICAL set cardinality.
    # Half (-50 percent): take the 10 most-common factypes in CLINICAL.
    common = Counter()
    for r in recs:
        ft = r.get("factype") or ""
        if ft in clinical_set:
            common[ft] += 1
    half_set = {ft for ft, _ in common.most_common(10)}
    rows_h, ratio_h, _, _ = compute_ratios(recs, half_set, NIR_PROV_TO_ADM1)
    grad_h = gradient(rows_h, recs, NIR_PROV_TO_ADM1)
    runs.append({
        "label": "clinical_set_minus50",
        "factype_set_size": len(half_set),
        "country_clinical_ratio": ratio_h,
        "gradient": grad_h,
        "min_admin1_ratio": min(r["ratio"] for r in rows_h.values() if r["ratio"] is not None),
        "max_admin1_ratio": max(r["ratio"] for r in rows_h.values() if r["ratio"] is not None),
    })

    # +50 percent: 28 factypes (top 28 most-common across the registry).
    all_common = Counter(r.get("factype") or "" for r in recs)
    top28 = {ft for ft, _ in all_common.most_common(28)}
    rows_p, ratio_p, _, _ = compute_ratios(recs, top28, NIR_PROV_TO_ADM1)
    grad_p = gradient(rows_p, recs, NIR_PROV_TO_ADM1)
    runs.append({
        "label": "clinical_set_plus50",
        "factype_set_size": len(top28),
        "country_clinical_ratio": ratio_p,
        "gradient": grad_p,
        "min_admin1_ratio": min(r["ratio"] for r in rows_p.values() if r["ratio"] is not None),
        "max_admin1_ratio": max(r["ratio"] for r in rows_p.values() if r["ratio"] is not None),
    })

    # +/-50 percent on quintile size (10 percent and 30 percent).
    grad_q10 = gradient(rows, recs, NIR_PROV_TO_ADM1, quintile_pct=10)
    grad_q30 = gradient(rows, recs, NIR_PROV_TO_ADM1, quintile_pct=30)
    runs.append({"label": "gradient_quintile_minus50_pct10", "gradient": grad_q10, "country_clinical_ratio": country_ratio})
    runs.append({"label": "gradient_quintile_plus50_pct30", "gradient": grad_q30, "country_clinical_ratio": country_ratio})

    # +/-50 percent on falsification threshold (5 percent and 15 percent).
    # Count ADM1 units within +/-X percent of unity (registry == OSM).
    def count_within(rows, pct):
        thresh = pct / 100.0
        c = 0
        for r in rows.values():
            if r["ratio"] is None:
                continue
            if abs(r["ratio"] - 1.0) <= thresh:
                c += 1
        return c

    runs.append({
        "label": "falsification_threshold_minus50_pct5",
        "country_clinical_ratio": country_ratio,
        "admin1_within_threshold": count_within(rows, 5),
    })
    runs.append({
        "label": "falsification_threshold_baseline_pct10",
        "country_clinical_ratio": country_ratio,
        "admin1_within_threshold": count_within(rows, 10),
    })
    runs.append({
        "label": "falsification_threshold_plus50_pct15",
        "country_clinical_ratio": country_ratio,
        "admin1_within_threshold": count_within(rows, 15),
    })

    # NIR mapping sensitivity: drop the 4 manual mappings entirely.
    rows_nir, ratio_nir, _, _ = compute_ratios(recs, clinical_set, nir_map={})
    runs.append({
        "label": "nir_mapping_dropped",
        "country_clinical_ratio": ratio_nir,
    })

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "country": "PHL",
        "metric": "clinical-tier OSM/registry ratio",
        "baseline_value": runs[0]["country_clinical_ratio"],
        "runs": runs,
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f"wrote {OUT}")
    for r in runs:
        print(r["label"], r.get("country_clinical_ratio"))


if __name__ == "__main__":
    main()
