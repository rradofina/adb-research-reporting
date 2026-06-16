"""Public Service Data Quality — deepening pass: decompose the OSM-registry
gap into a DEFINITIONAL-DENOMINATOR component and a GENUINE-MAPPING component
by reading the gap on the PRINCIPAL tier and the CLINICAL tier side by side.

Answers the keystone-adjacent contradiction in
`public-service-data-quality/deep-questions.md` §1.2 (the principal-tier
inversion) with a real recomputation over artifacts already on disk.

The headline "OSM captures only ~17.1% of facilities" is a CLINICAL-tier
ratio. The clinical tier adds Barangay Health Stations (NHFR factype 20),
which number 27,052 nationally — one-room community posts that volunteer
mappers do not record. On the PRINCIPAL tier (hospitals, main clinics, RHUs,
city/municipal/provincial health offices — the facilities a patient would
actually seek and that a regulator licenses as institutions), OSM does far
better and in some regions EXCEEDS the registry. An "OSM undercounts" story
cannot produce a ratio above 100%. This script:

  (a) lists every PHL ADM1 region where the principal-tier OSM/registry ratio
      exceeds 100% (from the committed PHL panel);
  (b) prints the clinical-tier vs principal-tier ratio per region, side by
      side, for PHL and for BGD (the parallel divisions);
  (c) re-derives — directly from the raw committed NHFR cache pages — how much
      of the national clinical denominator IS the BHS tier (factype 20), and
      recomputes the national clinical ratio with the BHS tier removed, to
      quantify how much of the 80-point gap is the BHS denominator rather than
      genuine OSM non-coverage of patient-facing facilities.

This decomposes the gap into:
  - definitional-denominator (the gap that disappears the moment the
    community-post tier — which neither enumeration convention shares — is
    excluded), and
  - genuine-mapping (the residual gap on the patient-facing principal tier,
    which is what an OSM-coverage story is actually about).

DATA POLICY. Every number traces to artifacts already in this repository:
  - `generated/public-service-data-quality-PHL.json` and `-BGD.json`, which
    are produced by the committed `scripts/process-multi-country.py` from the
    committed NHFR / DGHS caches and the access-services OSM panel;
  - the raw committed NHFR pages `.cache/nhfr_p*.json` for the factype-20
    (BHS) re-derivation in step (c).
No network. No AI-supplied figures. Per CONSTITUTION.md §6.4 these ratios are
a triage / measurement-gap diagnostic, not a country-quality ranking; per
§13.3 the framing is observability/coverage gap throughout.
attestation_chain: ai-first.
"""
import csv
import glob
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
GEN = ROOT / "generated"
os.makedirs(GEN, exist_ok=True)

# Factype 20 = Barangay Health Station, the community-post tier that is in the
# CLINICAL set but not the PRINCIPAL set. Defined identically in the committed
# process-multi-country.py (PHL_CLINICAL = PHL_PRINCIPAL | {"14","20","27","28","09"}).
BHS_FACTYPE = "20"


def load_panel(suffix):
    with open(GEN / f"public-service-data-quality-{suffix}.json", encoding="utf-8") as f:
        return json.load(f)


def derive_bhs_from_cache():
    """Re-derive the national BHS (factype 20) count straight from the raw
    committed NHFR pages, so the denominator decomposition is grounded in the
    source rows rather than read back from the processed panel."""
    files = []
    for p in glob.glob(str(CACHE / "nhfr_p*.json")):
        m = re.search(r"nhfr_p(\d+)\.json$", p)
        if m:
            files.append((int(m.group(1)), p))
    files.sort()
    ft = Counter()
    n_total = 0
    for _, p in files:
        with open(p, encoding="utf-8") as f:
            recs = json.load(f).get("v_activefacilities", [])
        for r in recs:
            n_total += 1
            ft[(r.get("factype") or "").strip()] += 1
    return n_total, ft.get(BHS_FACTYPE, 0), len(files)


def pct(x):
    return None if x is None else round(x * 100, 1)


def main():
    phl = load_panel("PHL")
    bgd = load_panel("BGD")

    # ---- step (c) groundwork: re-derive BHS straight from the raw NHFR cache.
    nhfr_total, bhs_n, pages = derive_bhs_from_cache()

    pt = phl["totals"]
    osm_phl = pt["osm_health"]
    clin_phl = pt["registry_clinical"]
    prin_phl = pt["registry_principal"]
    # Clinical tier with the BHS community-post tier removed. The remaining
    # community-level factypes (14/27/28/09) are tiny relative to the 27,052
    # BHSs; removing factype 20 isolates the single denominator term that the
    # deep-questions keystone names as the driver.
    clin_ex_bhs = clin_phl - bhs_n
    ratio_clin = osm_phl / clin_phl
    ratio_clin_ex_bhs = osm_phl / clin_ex_bhs if clin_ex_bhs else None
    ratio_prin = osm_phl / prin_phl
    bhs_share_of_clin = bhs_n / clin_phl if clin_phl else None
    # Share of the absolute clinical-tier "missing" count that is the BHS tier.
    clin_missing = clin_phl - osm_phl
    bhs_share_of_missing = bhs_n / clin_missing if clin_missing else None

    # ---- per-region tier table, PHL. Numbers come from the committed panel.
    def region_rows(panel, ratio_floor=1.0):
        rows = []
        over = []
        for r in panel["rows"]:
            rp = r.get("ratio_osm_to_principal")
            rc = r.get("ratio_osm_to_clinical")
            rows.append({
                "code": r["admin1_code"],
                "name": r["admin1_name"],
                "osm": r["osm_health"],
                "reg_prin": r["registry_principal"],
                "reg_clin": r["registry_clinical"],
                "ratio_prin": rp,
                "ratio_clin": rc,
                "prin_over_100": (rp is not None and rp > ratio_floor),
            })
            if rp is not None and rp > ratio_floor:
                over.append((r["admin1_name"], rp, r["osm_health"], r["registry_principal"]))
        # sort by principal-tier ratio descending (where the inversion lives)
        rows.sort(key=lambda x: (x["ratio_prin"] is None, -(x["ratio_prin"] or 0)))
        over.sort(key=lambda x: -x[1])
        return rows, over

    phl_rows, phl_over = region_rows(phl)
    bgd_rows, bgd_over = region_rows(bgd)

    # ---- amplification factor: principal-tier ratio ÷ clinical-tier ratio per
    # region. This is exactly the "definitional-denominator multiplier" — how
    # much the headline number shrinks purely by swapping the denominator for
    # one that includes the community-post tier.
    for rows in (phl_rows, bgd_rows):
        for r in rows:
            if r["ratio_prin"] and r["ratio_clin"]:
                r["prin_over_clin"] = round(r["ratio_prin"] / r["ratio_clin"], 2)
            else:
                r["prin_over_clin"] = None

    # ---- gradient on each tier (best/worst), PHL.
    def gradient(rows, key):
        vals = [(r["name"], r[key]) for r in rows if r[key] is not None]
        lo = min(vals, key=lambda x: x[1])
        hi = max(vals, key=lambda x: x[1])
        return lo, hi, (hi[1] / lo[1] if lo[1] else None)

    phl_clin_lo, phl_clin_hi, phl_clin_grad = gradient(phl_rows, "ratio_clin")
    phl_prin_lo, phl_prin_hi, phl_prin_grad = gradient(phl_rows, "ratio_prin")

    # =====================================================================
    # PRINT — real stdout
    # =====================================================================
    print("=" * 88)
    print("PSDQ deepening — tier decomposition: principal vs clinical OSM/registry ratio")
    print("All figures from committed artifacts on disk; no network; no AI-supplied numbers.")
    print("=" * 88)

    print(f"\n[c] BHS denominator, re-derived from raw NHFR cache "
          f"({pages} pages, {nhfr_total} active rows):")
    print(f"    Barangay Health Stations (factype {BHS_FACTYPE}): {bhs_n:,}")
    print(f"    National clinical-tier denominator               : {clin_phl:,}")
    print(f"    BHS share of clinical denominator                : {pct(bhs_share_of_clin)}%")
    print(f"    BHS share of the clinical 'missing-from-OSM' count: {pct(bhs_share_of_missing)}%  "
          f"({bhs_n:,} of {clin_missing:,})")

    print(f"\n    National OSM/clinical ratio (headline)           : {pct(ratio_clin)}%  "
          f"({osm_phl:,} / {clin_phl:,})")
    print(f"    National OSM/clinical with BHS tier removed      : {pct(ratio_clin_ex_bhs)}%  "
          f"({osm_phl:,} / {clin_ex_bhs:,})")
    print(f"    National OSM/principal ratio                     : {pct(ratio_prin)}%  "
          f"({osm_phl:,} / {prin_phl:,})")
    print(f"    => Removing one definitional tier (the {bhs_n:,} community posts) moves the")
    print(f"       national capture rate from {pct(ratio_clin)}% to {pct(ratio_clin_ex_bhs)}%; on the")
    print(f"       patient-facing principal tier it is {pct(ratio_prin)}%.")

    print("\n[a] PHL ADM1 regions where the PRINCIPAL-tier OSM/registry ratio EXCEEDS 100%")
    print("    (an OSM-undercount story cannot produce these):")
    if phl_over:
        for name, rp, o, p in phl_over:
            print(f"    {name:<18} {pct(rp):>6}%   OSM {o:>5}  vs  principal-registry {p:>5}")
    else:
        print("    (none)")
    print(f"    BGD divisions with principal-tier ratio > 100%: "
          f"{[n for n, *_ in bgd_over] if bgd_over else 'none'}")

    print("\n[b] PHL — clinical-tier vs principal-tier ratio, side by side")
    print("    (sorted by principal-tier ratio; '>' flags principal-tier > 100%)")
    print(f"    {'ADM1':<6} {'Region':<20} {'OSM':>5} {'prin':>5} {'clin':>5} "
          f"{'OSM/prin':>9} {'OSM/clin':>9} {'prin÷clin':>9}")
    for r in phl_rows:
        flag = ">" if r["prin_over_100"] else " "
        print(f"  {flag} {r['code']:<6} {r['name'][:20]:<20} {r['osm']:>5} {r['reg_prin']:>5} "
              f"{r['reg_clin']:>5} {str(pct(r['ratio_prin']))+'%':>9} "
              f"{str(pct(r['ratio_clin']))+'%':>9} {str(r['prin_over_clin'])+'x':>9}")

    print("\n[b] BGD — clinical-tier vs principal-tier ratio, side by side")
    print(f"    {'ADM1':<6} {'Division':<20} {'OSM':>5} {'prin':>5} {'clin':>5} "
          f"{'OSM/prin':>9} {'OSM/clin':>9} {'prin÷clin':>9}")
    for r in bgd_rows:
        flag = ">" if r["prin_over_100"] else " "
        print(f"  {flag} {r['code']:<6} {r['name'][:20]:<20} {r['osm']:>5} {r['reg_prin']:>5} "
              f"{r['reg_clin']:>5} {str(pct(r['ratio_prin']))+'%':>9} "
              f"{str(pct(r['ratio_clin']))+'%':>9} {str(r['prin_over_clin'])+'x':>9}")

    print("\n[gradient] PHL best/worst on each tier:")
    print(f"    clinical : {phl_clin_lo[0]} {pct(phl_clin_lo[1])}%  ->  "
          f"{phl_clin_hi[0]} {pct(phl_clin_hi[1])}%   gradient {round(phl_clin_grad,1)}x")
    print(f"    principal: {phl_prin_lo[0]} {pct(phl_prin_lo[1])}%  ->  "
          f"{phl_prin_hi[0]} {pct(phl_prin_hi[1])}%   gradient {round(phl_prin_grad,1)}x")
    print(f"    => the {round(phl_clin_grad,1)}x clinical-tier gradient collapses to "
          f"{round(phl_prin_grad,1)}x on the principal tier.")

    # =====================================================================
    # WRITE artifact
    # =====================================================================
    payload = {
        "program": "public-service-data-quality",
        "analysis": "tier decomposition — principal vs clinical OSM/registry ratio",
        "claim_scope": (
            "Deepening of the clinical-tier headline (OSM ~17.1% of NHFR-clinical). "
            "Reads the gap on the principal tier and the clinical tier side by side "
            "from the committed PHL/BGD panels, and re-derives the Barangay Health "
            "Station (factype 20) share of the clinical denominator straight from "
            "the raw committed NHFR cache. Decomposes the gap into a "
            "definitional-denominator component (the community-post tier neither "
            "enumeration convention shares) and a genuine-mapping component (the "
            "residual gap on the patient-facing principal tier). Triage / "
            "measurement-gap diagnostic per CONSTITUTION.md §6.4 and §13.3, not a "
            "country-quality ranking."
        ),
        "sources": {
            "phl_panel": "generated/public-service-data-quality-PHL.json (process-multi-country.py)",
            "bgd_panel": "generated/public-service-data-quality-BGD.json (process-multi-country.py)",
            "bhs_rederivation": f".cache/nhfr_p*.json ({pages} pages, {nhfr_total} active rows)",
            "osm": "access-services panel, Overpass amenity=hospital|clinic|doctors, ODbL",
            "license_nhfr": "DOH NHFR v2.0; public-information disclosure framing under RA 9485",
        },
        "phl_national": {
            "osm_health": osm_phl,
            "registry_principal": prin_phl,
            "registry_clinical": clin_phl,
            "bhs_factype20_count": bhs_n,
            "registry_clinical_excluding_bhs": clin_ex_bhs,
            "bhs_share_of_clinical_pct": pct(bhs_share_of_clin),
            "bhs_share_of_clinical_missing_pct": pct(bhs_share_of_missing),
            "ratio_osm_to_clinical_pct": pct(ratio_clin),
            "ratio_osm_to_clinical_excl_bhs_pct": pct(ratio_clin_ex_bhs),
            "ratio_osm_to_principal_pct": pct(ratio_prin),
        },
        "phl_principal_tier_over_100pct": [
            {"region": n, "ratio_pct": pct(rp), "osm": o, "registry_principal": p}
            for n, rp, o, p in phl_over
        ],
        "bgd_principal_tier_over_100pct": [
            {"region": n, "ratio_pct": pct(rp), "osm": o, "registry_principal": p}
            for n, rp, o, p in bgd_over
        ],
        "phl_gradient": {
            "clinical": {"worst": phl_clin_lo[0], "worst_pct": pct(phl_clin_lo[1]),
                         "best": phl_clin_hi[0], "best_pct": pct(phl_clin_hi[1]),
                         "ratio": round(phl_clin_grad, 1)},
            "principal": {"worst": phl_prin_lo[0], "worst_pct": pct(phl_prin_lo[1]),
                          "best": phl_prin_hi[0], "best_pct": pct(phl_prin_hi[1]),
                          "ratio": round(phl_prin_grad, 1)},
        },
        "phl_rows": phl_rows,
        "bgd_rows": bgd_rows,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(GEN / "psdq-tier-decomposition.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # flat CSV: one row per ADM1, both tiers
    flat_fields = ["iso3", "code", "name", "osm", "reg_prin", "reg_clin",
                   "ratio_prin", "ratio_clin", "prin_over_clin", "prin_over_100"]
    with open(GEN / "psdq-tier-decomposition.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flat_fields)
        w.writeheader()
        for iso, rows in (("PHL", phl_rows), ("BGD", bgd_rows)):
            for r in rows:
                w.writerow({"iso3": iso, **{k: r.get(k) for k in flat_fields if k != "iso3"}})

    print(f"\nWrote {GEN / 'psdq-tier-decomposition.json'} + .csv")


if __name__ == "__main__":
    main()
