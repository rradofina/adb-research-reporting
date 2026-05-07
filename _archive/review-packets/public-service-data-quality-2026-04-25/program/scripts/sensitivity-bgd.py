"""Sensitivity suite at +/-50 percent for PSDQ Bangladesh pilot.

Mirrors scripts/sensitivity.py for the BGD DGHS Facility Registry. The
arbitrary-numerics inventory differs from PHL because BGD classification
is regex-keyword-based, not a fixed factype set. Per pre-registration.md
section 6, every arbitrary numeric is tested at +/-50 percent.

Output: appends BGD rows to ../sensitivity-runs.json under a new
top-level key 'bgd_runs'. The PHL rows under 'runs' are preserved.
"""

import json
import csv
import os
import re
import glob
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/public-service-data-quality")
CACHE = ROOT / ".cache"
ACCESS_CSV = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/luminosity-gap/research/access-services/generated/access-services-computed-admin1.csv")
OUT = ROOT / "sensitivity-runs.json"

DIV_TO_ADM1 = {
    "Barisal": "BD-A", "Barishal": "BD-A",
    "Chattogram": "BD-B", "Chittagong": "BD-B",
    "Dhaka": "BD-C",
    "Khulna": "BD-D",
    "Rajshahi": "BD-E", "Rajshani": "BD-E",
    "Rangpur": "BD-F",
    "Sylhet": "BD-G",
    "Mymensingh": "BD-H",
}

BASELINE_COMMUNITY = [
    "community clinic",
    "union health",
    "maternal & child welfare",
    "family welfare center",
    "chest disease clinic",
]
BASELINE_PRINCIPAL = ["hospital", "medical college", "clinic"]


def load_bgd():
    files = []
    for p in glob.glob(str(CACHE / "bgd_dghs_p*.json")):
        m = re.search(r"bgd_dghs_p(\d+)\.json$", p)
        if m:
            files.append((int(m.group(1)), p))
    files.sort()
    recs = []
    for _, p in files:
        with open(p, encoding="utf-8") as f:
            recs.extend(json.load(f).get("data", []))
    return recs


def load_osm_bgd():
    osm = {}
    with open(ACCESS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["iso3"] != "BGD":
                continue
            osm[row["admin1_code"]] = {
                "name": row["admin1_name"],
                "osm_health": int(row["health_facilities"]),
                "population": int(row["population"]),
            }
    return osm


def categorize(name, principal_keywords, community_keywords):
    n = (name or "").lower()
    if not n:
        return False, False
    # Standard exclusions (admin / education / pure-lab)
    if any(w in n for w in ["office", "municipality", "city corporation zone",
                            "nursing college", "nursing institute",
                            "ngo for government", "warehouse", "store",
                            "training centre", "training center"]):
        return False, False
    if n == "consultancy & diagnostic center" or "diagnostic centre" in n:
        return False, False
    if "blood bank" in n:
        return False, True
    is_community = any(w in n for w in community_keywords)
    is_principal = any(w in n for w in principal_keywords)
    if is_community:
        is_principal = False
    return is_principal, is_principal or is_community


def compute(recs, principal_keywords, community_keywords):
    osm = load_osm_bgd()
    reg = defaultdict(int)
    for r in recs:
        div = r.get("division_name") or ""
        adm1 = DIV_TO_ADM1.get(div)
        if not adm1:
            continue
        is_p, is_c = categorize(r.get("facility_type_name") or "",
                                 principal_keywords, community_keywords)
        if is_c:
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
    return rows, country_ratio


def gradient(rows, quintile_pct=20):
    valid = [(k, v["ratio"]) for k, v in rows.items() if v["ratio"] is not None]
    if not valid:
        return None
    valid.sort(key=lambda x: x[1])
    n = len(valid)
    k = max(1, round(n * (quintile_pct / 100)))
    bottom = sum(r for _, r in valid[:k]) / k
    top = sum(r for _, r in valid[-k:]) / k
    return {"bottom_quintile_mean": bottom, "top_quintile_mean": top,
            "ratio_top_to_bottom": (top / bottom) if bottom > 0 else None,
            "k": k, "n": n}


def count_within(rows, pct):
    thresh = pct / 100.0
    return sum(1 for r in rows.values() if r["ratio"] is not None and abs(r["ratio"] - 1.0) <= thresh)


def main():
    recs = load_bgd()
    print(f"BGD records: {len(recs)}")

    runs = []

    # Baseline
    rows, ratio = compute(recs, BASELINE_PRINCIPAL, BASELINE_COMMUNITY)
    grad = gradient(rows)
    runs.append({
        "label": "bgd_baseline",
        "principal_keyword_count": len(BASELINE_PRINCIPAL),
        "community_keyword_count": len(BASELINE_COMMUNITY),
        "country_clinical_ratio": ratio,
        "gradient": grad,
        "min_admin1_ratio": min(r["ratio"] for r in rows.values() if r["ratio"] is not None),
        "max_admin1_ratio": max(r["ratio"] for r in rows.values() if r["ratio"] is not None),
        "admin1_within_pct10": count_within(rows, 10),
    })

    # -50 percent on community keywords (5 -> 2)
    minus_community = BASELINE_COMMUNITY[:2]  # community clinic, union health
    rows_mc, ratio_mc = compute(recs, BASELINE_PRINCIPAL, minus_community)
    runs.append({
        "label": "bgd_community_keywords_minus50",
        "community_keyword_count": len(minus_community),
        "country_clinical_ratio": ratio_mc,
        "gradient": gradient(rows_mc),
        "admin1_within_pct10": count_within(rows_mc, 10),
    })

    # +50 percent on community keywords (5 -> 8): add MCH center, sub-district health, USC
    plus_community = BASELINE_COMMUNITY + [
        "mch", "sub-district", "upazila health complex",
    ]
    rows_pc, ratio_pc = compute(recs, BASELINE_PRINCIPAL, plus_community)
    runs.append({
        "label": "bgd_community_keywords_plus50",
        "community_keyword_count": len(plus_community),
        "country_clinical_ratio": ratio_pc,
        "gradient": gradient(rows_pc),
        "admin1_within_pct10": count_within(rows_pc, 10),
    })

    # -50 percent on principal keywords (3 -> 1)
    minus_principal = ["hospital"]
    rows_mp, ratio_mp = compute(recs, minus_principal, BASELINE_COMMUNITY)
    runs.append({
        "label": "bgd_principal_keywords_minus50",
        "principal_keyword_count": len(minus_principal),
        "country_clinical_ratio": ratio_mp,
        "gradient": gradient(rows_mp),
        "admin1_within_pct10": count_within(rows_mp, 10),
    })

    # +50 percent on principal keywords (3 -> 5): add center and unit
    plus_principal = BASELINE_PRINCIPAL + ["health center", "health unit"]
    rows_pp, ratio_pp = compute(recs, plus_principal, BASELINE_COMMUNITY)
    runs.append({
        "label": "bgd_principal_keywords_plus50",
        "principal_keyword_count": len(plus_principal),
        "country_clinical_ratio": ratio_pp,
        "gradient": gradient(rows_pp),
        "admin1_within_pct10": count_within(rows_pp, 10),
    })

    # +/-50 percent on quintile size (10 percent and 30 percent)
    runs.append({"label": "bgd_quintile_minus50_pct10", "gradient": gradient(rows, 10), "country_clinical_ratio": ratio})
    runs.append({"label": "bgd_quintile_plus50_pct30", "gradient": gradient(rows, 30), "country_clinical_ratio": ratio})

    # +/-50 percent on falsification threshold
    runs.append({"label": "bgd_falsification_threshold_pct5", "country_clinical_ratio": ratio, "admin1_within_threshold": count_within(rows, 5)})
    runs.append({"label": "bgd_falsification_threshold_pct10", "country_clinical_ratio": ratio, "admin1_within_threshold": count_within(rows, 10)})
    runs.append({"label": "bgd_falsification_threshold_pct15", "country_clinical_ratio": ratio, "admin1_within_threshold": count_within(rows, 15)})

    # Append to existing PHL runs file
    existing = json.loads(OUT.read_text()) if OUT.exists() else {}
    existing["bgd_generated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    existing["bgd_baseline_value"] = runs[0]["country_clinical_ratio"]
    existing["bgd_runs"] = runs
    OUT.write_text(json.dumps(existing, indent=2))
    print(f"appended BGD rows to {OUT}")
    for r in runs:
        print(r["label"], r.get("country_clinical_ratio"))


if __name__ == "__main__":
    main()
