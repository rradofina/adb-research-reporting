"""Access to Services — deepening pass: is the access screen ranking
health access, or OpenStreetMap completeness?

Answers the keystone in `access-services/deep-questions.md` §1.1 and the
internal-contradiction question §1.2 with a real recomputation. The
"access" numerator in every cell of the screening panel is a count of
OSM-tagged amenities (amenity=hospital/clinic/doctors). The sibling
program `public-service-data-quality` (PSDQ) measured exactly that OSM
layer against each country's official national facility registry, per
ADM1 unit. This script joins the two committed panels.

Two things are done, both from data already on disk:

  (a) INTERNAL CONTRADICTION (§1.2). Show that the Philippines unit this
      program flags as worst-access (ARMM, 68,678 people per OSM facility)
      is, by PSDQ's own measurement, the worst-MAPPED unit (BARMM, 6.45%
      OSM clinical-tier capture vs NCR 63.53%). Regress this program's
      ADM1 people-per-OSM-facility on PSDQ's ADM1 OSM/registry ratio
      across all 17 PHL regions; a high R-squared means the access signal
      IS the completeness signal.

  (b) COMPLETENESS CORRECTION (§1.1). Recompute a "registry-based"
      people-per-facility for every PHL ADM1 unit two equivalent ways:
      dividing population by the registry clinical-tier count, and
      scaling the OSM count up by the PSDQ region-specific capture rate
      (national 17.12% fallback where a regional ratio is absent — for
      PHL all 17 regions have one). Show how the ADM1 access ranking
      moves once the OSM undercount is corrected.

KEY IDENTITY (why the panel's PHL numerator is exactly the PSDQ OSM count):
the access panel reports ARMM at 68,678 people/facility; PSDQ reports ARMM
population 4,944,800 and osm_health 72, and 4,944,800 / 72 = 68,678. So
the access screen's PHL "facility count" is PSDQ's osm_health column, and
the registry-corrected denominator PSDQ already carries lets us recompute
the screen with no new data.

Every number below traces to two committed public-source panels:
  - access-services/generated/access-services-adb-panel.json
      (OSM via Overpass; geoBoundaries gbOpen ADM1; PSA 2020 + WorldPop 2024)
  - public-service-data-quality/generated/public-service-data-quality-PHL.json
      (DOH National Health Facility Registry v2.0; OSM via Overpass)
  - public-service-data-quality/generated/public-service-data-quality-BGD.json
      (DGHS Facility Registry; OSM via Overpass)
No new data, no network, no AI-supplied figures. Per CONSTITUTION.md §6.4
this remains a triage screen, not an access ranking; §13.3 the framing is
a service-access measurement / observability gap, not a country judgment.
attestation_chain: ai-first.
"""
import csv
import json
import os
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research"
ACCESS = f"{BASE}/access-services"
PSDQ = f"{BASE}/public-service-data-quality"
OUT = f"{ACCESS}/generated"
os.makedirs(OUT, exist_ok=True)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pearson(xs, ys):
    """Pearson correlation; returns (r, r2) or (None, None)."""
    n = len(xs)
    if n < 3:
        return None, None
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None, None
    r = sxy / (sxx * syy) ** 0.5
    return round(r, 4), round(r * r, 4)


def spearman(xs, ys):
    """Spearman rank correlation (average-rank ties)."""
    def ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        rk = [0.0] * len(vals)
        i = 0
        while i < len(vals):
            j = i
            while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                rk[order[k]] = avg
            i = j + 1
        return rk
    r, _ = pearson(ranks(xs), ranks(ys))
    return r


def main():
    access = load(f"{ACCESS}/generated/access-services-adb-panel.json")
    phl = load(f"{PSDQ}/generated/public-service-data-quality-PHL.json")
    bgd = load(f"{PSDQ}/generated/public-service-data-quality-BGD.json")

    nat_ratio_phl = phl["totals"]["ratio_osm_to_clinical"]   # 0.1712
    nat_ratio_bgd = bgd["totals"]["ratio_osm_to_clinical"]   # 0.1178

    print("=" * 78)
    print("ACCESS-SERVICES DEEPENING — does the access screen rank OSM completeness?")
    print("=" * 78)

    # ----- (0) Confirm the identity: access panel PHL worst-ADM1 == PSDQ OSM count.
    acc_phl = next(r for r in access["rows"] if r["iso3"] == "PHL")
    armm = next(r for r in phl["rows"] if r["admin1_name"] == "ARMM")
    armm_osm_ppf = armm["population_2020"] / armm["osm_health"]
    print("\n[0] IDENTITY CHECK — the access numerator IS the PSDQ OSM count")
    print(f"    access panel: PHL worst-ADM1 ({acc_phl['worst_adm1_name']}) = "
          f"{acc_phl['worst_adm1_people_per_health_facility']:,} people / OSM facility")
    print(f"    PSDQ ARMM:    pop {armm['population_2020']:,} / osm_health "
          f"{armm['osm_health']} = {armm_osm_ppf:,.0f} people / OSM facility")
    print(f"    match: {round(armm_osm_ppf) == acc_phl['worst_adm1_people_per_health_facility']}")

    # ----- (1) Per-ADM1 recomputation for PHL (all 17 regions).
    # OSM people-per-facility   = population / osm_health         (the screen)
    # Registry people-per-facility = population / registry_clinical (corrected)
    # Scaled people-per-facility = OSM ppf * region capture ratio  (== registry ppf)
    # Capture ratio = osm_health / registry_clinical = ratio_osm_to_clinical.
    phl_rows = []
    for r in phl["rows"]:
        pop = r["population_2020"]
        osm = r["osm_health"]
        reg = r["registry_clinical"]
        ratio = r["ratio_osm_to_clinical"]          # region-specific capture
        osm_ppf = pop / osm if osm else None
        reg_ppf = pop / reg if reg else None
        scaled_ppf = osm_ppf * ratio if osm_ppf is not None else None  # = reg_ppf
        phl_rows.append({
            "admin1_name": r["admin1_name"],
            "population_2020": pop,
            "osm_health": osm,
            "registry_clinical": reg,
            "capture_ratio": round(ratio, 4),
            "osm_people_per_facility": round(osm_ppf) if osm_ppf else None,
            "registry_people_per_facility": round(reg_ppf) if reg_ppf else None,
            "scaled_people_per_facility": round(scaled_ppf) if scaled_ppf else None,
        })

    # Rankings (1 = worst access = highest people per facility).
    by_osm = sorted(phl_rows, key=lambda x: -x["osm_people_per_facility"])
    by_reg = sorted(phl_rows, key=lambda x: -x["registry_people_per_facility"])
    osm_rank = {r["admin1_name"]: i + 1 for i, r in enumerate(by_osm)}
    reg_rank = {r["admin1_name"]: i + 1 for i, r in enumerate(by_reg)}
    for r in phl_rows:
        r["rank_osm"] = osm_rank[r["admin1_name"]]
        r["rank_registry"] = reg_rank[r["admin1_name"]]
        r["rank_shift"] = r["rank_osm"] - r["rank_registry"]

    print("\n[1] PHL per-ADM1: OSM-screen vs registry-corrected people-per-facility")
    print("    (rank 1 = worst access in that column)")
    print(f"    {'region':<20} {'capture':>8} {'OSM ppf':>10} {'reg ppf':>10} "
          f"{'rkOSM':>6} {'rkREG':>6} {'shift':>6}")
    for r in sorted(phl_rows, key=lambda x: x["rank_osm"]):
        print(f"    {r['admin1_name']:<20} {r['capture_ratio']*100:>7.2f}% "
              f"{r['osm_people_per_facility']:>10,} "
              f"{r['registry_people_per_facility']:>10,} "
              f"{r['rank_osm']:>6} {r['rank_registry']:>6} {r['rank_shift']:>+6}")

    # ----- (2) The internal contradiction (§1.2): regress OSM ppf on capture.
    osm_ppf_vec = [r["osm_people_per_facility"] for r in phl_rows]
    capture_vec = [r["capture_ratio"] for r in phl_rows]
    r_lin, r2_lin = pearson(capture_vec, osm_ppf_vec)
    rho = spearman(capture_vec, osm_ppf_vec)
    # log-linear too, since ppf = pop/(ratio*registry) is ~ inverse in ratio.
    import math
    log_osm = [math.log(v) for v in osm_ppf_vec]
    log_cap = [math.log(v) for v in capture_vec]
    r_log, r2_log = pearson(log_cap, log_osm)

    print("\n[2] INTERNAL CONTRADICTION (§1.2): is access rank the inverse of mapping?")
    print(f"    PHL regions n={len(phl_rows)}")
    print(f"    Pearson r (capture vs OSM ppf, level):  r={r_lin}  R^2={r2_lin}")
    print(f"    Pearson r (log capture vs log OSM ppf): r={r_log}  R^2={r2_log}")
    print(f"    Spearman rank rho (capture vs OSM ppf): {rho}")
    best = max(phl_rows, key=lambda x: x["capture_ratio"])
    worst = min(phl_rows, key=lambda x: x["capture_ratio"])
    print(f"    capture gradient: best {best['admin1_name']} "
          f"{best['capture_ratio']*100:.2f}%  ->  worst {worst['admin1_name']} "
          f"{worst['capture_ratio']*100:.2f}%  "
          f"({best['capture_ratio']/worst['capture_ratio']:.1f}x)")

    # ----- (3) Does correcting the undercount move the worst-access unit?
    worst_osm = by_osm[0]
    worst_reg = by_reg[0]
    print("\n[3] COMPLETENESS CORRECTION (§1.1): worst-access PHL unit, before/after")
    print(f"    worst on OSM screen:        {worst_osm['admin1_name']} "
          f"= {worst_osm['osm_people_per_facility']:,} people/facility")
    print(f"    same unit, registry-based:  {worst_osm['admin1_name']} "
          f"= {worst_osm['registry_people_per_facility']:,} people/facility "
          f"({worst_osm['osm_people_per_facility']/worst_osm['registry_people_per_facility']:.1f}x lower)")
    print(f"    worst on registry-corrected: {worst_reg['admin1_name']} "
          f"= {worst_reg['registry_people_per_facility']:,} people/facility")
    n_moved = sum(1 for r in phl_rows if r["rank_shift"] != 0)
    print(f"    ADM1 units whose rank changed after correction: {n_moved} of {len(phl_rows)}")

    # ----- (4) National-fallback illustration for the cluster headline.
    # The four cluster members' worst-ADM1 OSM values, corrected by the only
    # capture rates available on disk: PHL/BGD national clinical ratios.
    # PAK/KHM/LAO/NPL/LKA/TLS have NO registry join in PSDQ -> uncorrectable.
    print("\n[4] CLUSTER worst-ADM1, corrected only where a registry ratio exists")
    print("    (national clinical-tier capture: PHL 17.12%, BGD 11.78%;")
    print("     PAK/KHM/LAO/NPL/LKA/TLS have NO PSDQ registry join -> UNCORRECTABLE)")
    cluster_corr = []
    for row in access["rows"]:
        iso = row["iso3"]
        osm_worst = row["worst_adm1_people_per_health_facility"]
        if iso == "PHL":
            ratio, src = nat_ratio_phl, "PHL national clinical (PSDQ)"
        elif iso == "BGD":
            ratio, src = nat_ratio_bgd, "BGD national clinical (PSDQ)"
        else:
            ratio, src = None, "no registry join in PSDQ"
        corrected = round(osm_worst * ratio) if ratio else None
        cluster_corr.append({
            "iso3": iso, "country": row["country"],
            "worst_adm1_name": row["worst_adm1_name"],
            "osm_worst_people_per_facility": osm_worst,
            "capture_ratio_applied": round(ratio, 4) if ratio else None,
            "corrected_people_per_facility": corrected,
            "correction_source": src,
        })
    print(f"    {'iso':<4} {'worst ADM1':<18} {'OSM ppf':>10} {'capture':>9} {'corrected':>11}  source")
    for c in cluster_corr:
        cap = f"{c['capture_ratio_applied']*100:.2f}%" if c["capture_ratio_applied"] else "    n/a"
        cor = f"{c['corrected_people_per_facility']:,}" if c["corrected_people_per_facility"] else "UNCORRECTABLE"
        print(f"    {c['iso3']:<4} {c['worst_adm1_name']:<18} "
              f"{c['osm_worst_people_per_facility']:>10,} {cap:>9} {cor:>11}  {c['correction_source']}")

    # ----- (5) BGD per-ADM1 corrected ranking (the other registry-join DMC).
    bgd_rows = []
    for r in bgd["rows"]:
        pop, osm, reg = r["population_2020"], r["osm_health"], r["registry_clinical"]
        bgd_rows.append({
            "admin1_name": r["admin1_name"],
            "capture_ratio": round(r["ratio_osm_to_clinical"], 4),
            "osm_people_per_facility": round(pop / osm) if osm else None,
            "registry_people_per_facility": round(pop / reg) if reg else None,
        })
    b_by_osm = sorted(bgd_rows, key=lambda x: -x["osm_people_per_facility"])
    b_by_reg = sorted(bgd_rows, key=lambda x: -x["registry_people_per_facility"])
    b_osm_rank = {r["admin1_name"]: i + 1 for i, r in enumerate(b_by_osm)}
    b_reg_rank = {r["admin1_name"]: i + 1 for i, r in enumerate(b_by_reg)}
    for r in bgd_rows:
        r["rank_osm"] = b_osm_rank[r["admin1_name"]]
        r["rank_registry"] = b_reg_rank[r["admin1_name"]]
        r["rank_shift"] = r["rank_osm"] - r["rank_registry"]
    b_cap = [r["capture_ratio"] for r in bgd_rows]
    b_osm = [r["osm_people_per_facility"] for r in bgd_rows]
    b_r, b_r2 = pearson(b_cap, b_osm)
    print("\n[5] BGD per-ADM1 (8 divisions): OSM-screen vs registry-corrected")
    print(f"    {'division':<14} {'capture':>8} {'OSM ppf':>9} {'reg ppf':>8} "
          f"{'rkOSM':>6} {'rkREG':>6} {'shift':>6}")
    for r in sorted(bgd_rows, key=lambda x: x["rank_osm"]):
        print(f"    {r['admin1_name']:<14} {r['capture_ratio']*100:>7.2f}% "
              f"{r['osm_people_per_facility']:>9,} {r['registry_people_per_facility']:>8,} "
              f"{r['rank_osm']:>6} {r['rank_registry']:>6} {r['rank_shift']:>+6}")
    print(f"    Pearson r (capture vs OSM ppf): r={b_r}  R^2={b_r2}")

    # ----- Persist artifact.
    payload = {
        "program": "access-services",
        "analysis": "OSM-completeness correction of the access screen (deepening of §1.1, §1.2)",
        "claim_scope": (
            "Deepening of the OSM-amenity access screen. Joins the access panel's "
            "OSM facility numerator to PSDQ's official-registry capture rates per "
            "ADM1 for the two DMCs with a registry join (PHL, BGD), and recomputes "
            "people-per-facility on the registry denominator. Triage screen "
            "(CONSTITUTION.md §6.4), not an access ranking; service-access "
            "measurement/observability-gap framing (§13.3)."
        ),
        "sources": {
            "access_panel": "access-services/generated/access-services-adb-panel.json (OSM Overpass; geoBoundaries gbOpen ADM1; PSA 2020 + WorldPop 2024; retrieved 2026-04-23)",
            "psdq_phl": "public-service-data-quality/generated/public-service-data-quality-PHL.json (DOH NHFR v2.0; OSM Overpass; retrieved 2026-04-25)",
            "psdq_bgd": "public-service-data-quality/generated/public-service-data-quality-BGD.json (DGHS Facility Registry; OSM Overpass; retrieved 2026-04-25)",
            "license": "OSM ODbL; geoBoundaries CC BY 4.0; registries public-disclosure",
        },
        "identity_check": {
            "access_phl_worst_adm1": acc_phl["worst_adm1_name"],
            "access_phl_worst_ppf": acc_phl["worst_adm1_people_per_health_facility"],
            "psdq_armm_pop_over_osm": round(armm_osm_ppf),
            "match": round(armm_osm_ppf) == acc_phl["worst_adm1_people_per_health_facility"],
        },
        "phl_national_clinical_capture": round(nat_ratio_phl, 4),
        "bgd_national_clinical_capture": round(nat_ratio_bgd, 4),
        "phl_internal_contradiction": {
            "n_regions": len(phl_rows),
            "pearson_r_level": r_lin, "pearson_r2_level": r2_lin,
            "pearson_r_loglog": r_log, "pearson_r2_loglog": r2_log,
            "spearman_rho": rho,
            "capture_best": {"region": best["admin1_name"], "ratio": round(best["capture_ratio"], 4)},
            "capture_worst": {"region": worst["admin1_name"], "ratio": round(worst["capture_ratio"], 4)},
        },
        "phl_correction": {
            "worst_on_osm": {"region": worst_osm["admin1_name"], "ppf": worst_osm["osm_people_per_facility"]},
            "worst_on_osm_registry_corrected_ppf": worst_osm["registry_people_per_facility"],
            "worst_on_registry": {"region": worst_reg["admin1_name"], "ppf": worst_reg["registry_people_per_facility"]},
            "n_adm1_rank_changed": n_moved,
            "n_adm1_total": len(phl_rows),
        },
        "phl_rows": phl_rows,
        "bgd_rows": bgd_rows,
        "bgd_internal_contradiction": {"pearson_r_level": b_r, "pearson_r2_level": b_r2},
        "cluster_worst_adm1_corrected": cluster_corr,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/access-osm-completeness-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/access-osm-completeness-deepening-phl.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(phl_rows[0].keys()))
        w.writeheader()
        for r in phl_rows:
            w.writerow(r)

    print(f"\nWrote {OUT}/access-osm-completeness-deepening.json")
    print(f"Wrote {OUT}/access-osm-completeness-deepening-phl.csv")


if __name__ == "__main__":
    main()
