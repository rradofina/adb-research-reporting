"""MPI x Nighttime Lights — deepening pass: which MPI dimensions a luminosity
signal could even see.

Co-authored program (Program 0, with Arturo Martinez Jr; owner-led). This
script does NOT advance the program, freeze a claim, or supersede the
co-authored work. It scopes the *eventual* NTL x MPI study by answering the
keystone in `deep-questions.md` §1.2 / §1.1 with committed data already on
disk: of each ADB economy's Multidimensional Poverty Index, what share comes
from dimensions a nighttime-radiance signal is structurally blind to?

The mechanism the deep questions name: nighttime radiance tracks, at best,
part of MPI's LIVING-STANDARDS dimension (electricity, assets, housing
density). It carries no signature for the HEALTH dimension (nutrition, child
mortality) or the EDUCATION dimension (years of schooling, school
attendance) — a district can electrify without one child staying in school
longer or one stunting case resolving. So before any NTL ingestion is built,
the answerable question is: how much of the deprivation MPI measures sits in
the two dimensions light cannot observe?

Two readings are computed, both from the OPHI Alkire-Foster decomposition:

  A. DIMENSION reading (coarse, the headline). NTL-blind share =
     health_contribution_pct + education_contribution_pct. This treats the
     entire living-standards dimension as potentially NTL-visible — the most
     GENEROUS possible case for a luminosity proxy.

  B. INDICATOR reading (fine, the lower bound on blindness). Even within
     living standards, radiance plausibly speaks only to electricity,
     housing, and assets — not to cooking fuel, sanitation, or drinking
     water, which have no luminance signature. So the NTL-PLAUSIBLE share is
     contrib_electricity + contrib_housing + contrib_assets, and everything
     else (health + education + cooking fuel + sanitation + water) is the
     NTL-blind share under the indicator reading. This is the more honest
     ceiling on what a luminosity signal could decompose.

Every number traces to the committed OPHI Global MPI 2024 national table
(Alkire, Kanagaratnam & Suppa 2024; CC BY 4.0), parsed into
`luminosity-gap/public/data/mpi-national-adb.json`. No new data, no network,
no AI-supplied figures. Per CONSTITUTION.md §13.3 this is a measurement /
observability framing, not a country ranking; per §6.4 any composite is
triage only. attestation_chain: ai-first.
"""
import json, os
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/mpi-nighttime-lights"
DATA = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/luminosity-gap/public/data/mpi-national-adb.json"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

# OPHI Alkire-Foster dimension -> indicator map (Global MPI 2024 structure).
HEALTH_INDS = ["nutrition", "child_mortality"]
EDUCATION_INDS = ["years_schooling", "school_attendance"]
LIVING_INDS = ["cooking_fuel", "sanitation", "drinking_water",
               "electricity", "housing", "assets"]

# Within living standards, the indicators a nighttime-radiance signal could
# PLAUSIBLY carry information about (electrified dwellings, dwelling
# materials/density, electric assets). Cooking fuel, sanitation and drinking
# water have no luminance signature and are therefore NTL-blind even though
# they sit inside the living-standards dimension.
NTL_PLAUSIBLE_LIVING = ["electricity", "housing", "assets"]
NTL_BLIND_LIVING = ["cooking_fuel", "sanitation", "drinking_water"]


def f(row, key):
    """Indicator contribution %, treating OPHI nulls (indicator not in that
    survey) as 0 so the per-economy reading is conservative and additive."""
    v = row.get(f"contrib_{key}_pct")
    return float(v) if v is not None else 0.0


def main():
    blob = json.load(open(DATA, encoding="utf-8"))
    src = blob["metadata"]
    rows = []
    null_indicator_notes = []

    for r in blob["data"]:
        if not r.get("is_adb_member"):
            continue
        iso, name = r["iso3"], r["country"]

        # --- Reading A: dimension-level (generous to NTL) ---
        health = float(r["health_contribution_pct"])
        education = float(r["education_contribution_pct"])
        living = float(r["living_std_contribution_pct"])
        ntl_blind_dim = health + education            # health + education
        ntl_visible_dim = living                      # whole living-standards

        # --- Reading B: indicator-level (honest ceiling on NTL) ---
        ntl_plausible_ind = sum(f(r, k) for k in NTL_PLAUSIBLE_LIVING)
        living_blind_ind = sum(f(r, k) for k in NTL_BLIND_LIVING)
        ind_health = sum(f(r, k) for k in HEALTH_INDS)
        ind_education = sum(f(r, k) for k in EDUCATION_INDS)
        ntl_blind_ind = ind_health + ind_education + living_blind_ind

        # Note any indicator whose contribution is null (survey did not carry
        # it) so the reader knows the indicator reading is a lower bound on
        # NTL-blindness for that economy.
        nulls = [k for k in (HEALTH_INDS + EDUCATION_INDS + LIVING_INDS)
                 if r.get(f"contrib_{k}_pct") is None]
        if nulls:
            null_indicator_notes.append({"iso3": iso, "null_indicators": nulls})

        rows.append({
            "iso3": iso, "country": name,
            "world_region": r["world_region"],
            "survey": r["survey"], "survey_year": r["survey_year"],
            "mpi_value": round(float(r["mpi_value"]), 6),
            "headcount_ratio_pct": round(float(r["headcount_ratio"]), 3),
            # dimension reading
            "health_pct": round(health, 2),
            "education_pct": round(education, 2),
            "living_std_pct": round(living, 2),
            "ntl_blind_dim_pct": round(ntl_blind_dim, 2),
            "ntl_visible_dim_pct": round(ntl_visible_dim, 2),
            # indicator reading
            "ntl_plausible_ind_pct": round(ntl_plausible_ind, 2),
            "ntl_blind_ind_pct": round(ntl_blind_ind, 2),
            "living_blind_ind_pct": round(living_blind_ind, 2),
            "has_null_indicator": bool(nulls),
        })

    # Rank by NTL-blind share under the dimension reading (the keystone):
    # most "NTL-invisible" deprivation at the top.
    by_blind_dim = sorted(rows, key=lambda x: -x["ntl_blind_dim_pct"])

    # Cross-check: dimension health+ed+living should sum to ~100 (OPHI
    # rounding). Report the largest residual so the decomposition is auditable.
    residuals = [(r["iso3"], round(r["health_pct"] + r["education_pct"]
                 + r["living_std_pct"] - 100.0, 3)) for r in rows]
    max_resid = max(residuals, key=lambda x: abs(x[1]))

    n = len(rows)
    mean_blind_dim = round(sum(r["ntl_blind_dim_pct"] for r in rows) / n, 2)
    median_blind_dim = round(
        sorted(r["ntl_blind_dim_pct"] for r in rows)[n // 2], 2)
    mean_blind_ind = round(sum(r["ntl_blind_ind_pct"] for r in rows) / n, 2)
    # Economies where the NON-NTL share exceeds half the MPI under BOTH
    # readings — the deprivation a luminosity join would mostly miss.
    majority_blind_both = [r["iso3"] for r in rows
                           if r["ntl_blind_dim_pct"] > 50.0
                           and r["ntl_blind_ind_pct"] > 50.0]

    payload = {
        "program": "mpi-nighttime-lights",
        "analysis": (
            "Dimensional scope of an eventual NTL x MPI join: share of each "
            "ADB economy's MPI arising in dimensions a nighttime-radiance "
            "signal is structurally blind to (health + education), under a "
            "generous dimension reading and an honest indicator reading."
        ),
        "co_authorship": (
            "Program 0, co-authored with Arturo Martinez Jr (ADB), owner-led. "
            "This scopes the joint study; it does not advance the program, "
            "freeze a claim under CONSTITUTION.md §6.1, or supersede the "
            "co-authored track. The NTL side is not computed here (see wall)."
        ),
        "ntl_data_wall": (
            "The NTL x MPI join itself is owner-gated and NOT runnable here: "
            "NASA Black Marble VNP46A4 / VIIRS DNB ingestion via Google Earth "
            "Engine requires OAuth on the owner's Earth Engine + Google Cloud "
            "credentials (a §2 hard wall: account on the owner's identity), "
            "plus geoBoundaries ADM1/ADM2 and a WorldPop/GHSL population "
            "denominator. Network is blocked in this session. Only the MPI "
            "side — already on disk — is computed."
        ),
        "source": {
            "name": src["source"],
            "table": "Table 1 National Results (1.1 / 1.2 / 1.3)",
            "citation": src["citation"],
            "license": src["license"],
            "parsed_at": src["parsed_at"],
            "file": "luminosity-gap/public/data/mpi-national-adb.json",
            "bibtex_key": "alkire2024mpi",
        },
        "dimension_map": {
            "health": HEALTH_INDS, "education": EDUCATION_INDS,
            "living_standards": LIVING_INDS,
            "ntl_plausible_within_living": NTL_PLAUSIBLE_LIVING,
            "ntl_blind_within_living": NTL_BLIND_LIVING,
        },
        "n_adb_economies": n,
        "mean_ntl_blind_dim_pct": mean_blind_dim,
        "median_ntl_blind_dim_pct": median_blind_dim,
        "mean_ntl_blind_ind_pct": mean_blind_ind,
        "majority_ntl_blind_both_readings": majority_blind_both,
        "decomposition_residual_check": {
            "rule": "health+education+living should sum to 100 (OPHI rounding)",
            "max_abs_residual_iso3": max_resid[0],
            "max_abs_residual_pp": max_resid[1],
        },
        "null_indicator_notes": null_indicator_notes,
        "rows_by_ntl_blind_dimension": by_blind_dim,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/mpi-dimension-decomposition.json", "w",
              encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    # Flat CSV for the evidence table.
    import csv
    cols = ["iso3", "country", "world_region", "survey", "survey_year",
            "mpi_value", "headcount_ratio_pct", "health_pct", "education_pct",
            "living_std_pct", "ntl_blind_dim_pct", "ntl_visible_dim_pct",
            "ntl_plausible_ind_pct", "ntl_blind_ind_pct",
            "living_blind_ind_pct", "has_null_indicator"]
    with open(f"{OUT}/mpi-dimension-decomposition.csv", "w",
              encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in by_blind_dim:
            w.writerow({k: r[k] for k in cols})

    # ---- stdout ----
    print("=== MPI x NTL dimensional scope (ADB members, OPHI Global MPI 2024) ===")
    print(f"economies: {n}   source: {src['source']} ({src['license']})")
    print(f"mean NTL-blind share (dimension reading, health+education): {mean_blind_dim}%")
    print(f"median NTL-blind share (dimension reading): {median_blind_dim}%")
    print(f"mean NTL-blind share (indicator reading, +cooking/sanitation/water): {mean_blind_ind}%")
    print(f"decomposition residual check: max |health+ed+living-100| = "
          f"{max_resid[1]}pp ({max_resid[0]})")
    print(f"majority NTL-blind under BOTH readings: {majority_blind_both}")
    print()
    hdr = (f"{'ISO':<4}{'economy':<18}{'MPI':>8}{'health':>8}{'educ':>7}"
           f"{'living':>8}{'BLIND(dim)':>11}{'BLIND(ind)':>11}")
    print(hdr)
    print("-" * len(hdr))
    for r in by_blind_dim:
        star = "*" if r["has_null_indicator"] else " "
        print(f"{r['iso3']:<4}{r['country'][:17]:<18}{r['mpi_value']:>8.4f}"
              f"{r['health_pct']:>8.1f}{r['education_pct']:>7.1f}"
              f"{r['living_std_pct']:>8.1f}{r['ntl_blind_dim_pct']:>11.1f}"
              f"{r['ntl_blind_ind_pct']:>10.1f}{star}")
    print("-" * len(hdr))
    print("* indicator reading is a lower bound: this economy has >=1 OPHI "
          "indicator the survey did not carry (treated as 0).")
    print(f"\nWrote {OUT}/mpi-dimension-decomposition.json + .csv")


if __name__ == "__main__":
    main()
