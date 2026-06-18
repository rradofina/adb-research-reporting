# Pre-registration — Public Service Data Quality

`attestation_chain: ai-first`

Status: **§18 AI-first frozen — 2026-04-25.**

Governed by `CONSTITUTION.md` §3.2, §7, and §18. This document is
**frozen as of 2026-04-25 under §18 AI-first**. The screening-result
computations already in `generated/` are treated as exploratory under
§3.2; this pre-registration applies to subsequent pipeline runs, which
serve as the input to the SR → PR gate under §18.

---

## 1. Claim sentence

> In Philippines and Bangladesh — and, when the pipeline extends to
> them, in India and Indonesia — OpenStreetMap-mapped health-facility
> counts (`amenity=hospital`, `amenity=clinic`, `amenity=doctors`)
> systematically under-represent the count and geographic distribution
> of facilities in the official national health-facility registry, and
> the magnitude of the OSM-vs-registry gap is larger in rural and
> low-HDI ADM1 units than in capital-region or high-HDI ADM1 units.

The claim is one sentence by intent. It commits to two empirical
patterns: (a) OSM is below registry counts on average, and (b) the
shortfall is larger in rural / low-HDI ADM1 units than in capital
regions.

## 2. Falsification condition

The claim is retracted if **both** of the following are true:

- (a) OSM-vs-registry per-capita facility counts agree within **±10%**
  at ADM1 in **two or more pilot DMCs**, on the clinical-tier
  comparison (the headline measure defined in §5).
- (b) The rural-urban gradient (mean clinical-tier OSM/registry ratio
  in the bottom-quintile-by-rural-share ADM1 units **minus** the same
  ratio in the top-quintile) is not statistically distinguishable from
  zero at p < 0.05 in a Mann-Whitney rank-sum test, in **two or more**
  pilot DMCs.

Both conditions must trigger for retraction. The 10% threshold and
quintile partition are tested at ±50% in `sensitivity.md`.

## 3. Population in scope

DMCs in the pre-registration:

- PHL (Philippines) — pilot complete in `generated/public-service-data-quality-PHL.json`.
- BGD (Bangladesh) — pilot complete in `generated/public-service-data-quality-BGD.json`.
- IND (India) — pipeline TODO. HMIS via `data.gov.in`.
- IDN (Indonesia) — pipeline TODO. SATUSEHAT or PUSDATIN.

The SR → PR gate is requested for the two-DMC subset (PHL + BGD). The
extension to IND + IDN is a separate, future SR → PR gate request, with
its own pre-registration freeze.

## 4. Time window

| Source | Start | End |
|---|---|---|
| OSM Overpass (PHL + BGD admin areas) | 2026-04-05 | 2026-04-23 |
| DOH NHFR v2.0 (PHL) | 2026-04-25 | 2026-04-25 |
| DGHS Facility Registry (BGD) | 2026-04-25 | 2026-04-25 |

A publication-grade rerun aligns OSM and registry retrieval within a
single calendar week and pins OSM to a Geofabrik or Overture snapshot
per Constitution §11.

## 5. Primary metric

Headline metric: **clinical-tier OSM/registry ratio at ADM1**, defined
as OSM `amenity=hospital|clinic|doctors` count divided by the registry
clinical-tier facility count (PHL: factypes 01,03,04,05,15,17,19,21,22,23,24,51,52,53 + 14,20,27,28,09 = "clinical-tier"; BGD: equivalent clinical-tier definition derived from DGHS facility-type taxonomy).

Reported per ADM1, then aggregated to country level as a population-
weighted mean. Expressed as a percentage with one decimal.

Secondary metric: principal-tier OSM/registry ratio (PHL: factypes
01,03,04,05,15,17,19,21,22,23,24,51,52,53 only; BGD: equivalent
hospitals + main clinics only).

## 6. Pre-specified arbitrary numerics

Every numeric below is tested at ±50% in `sensitivity.md`. A change in
the headline finding inside ±50% on any numeric is a critical
sensitivity failure (per Constitution §6.6) and the claim cannot
advance until resolved.

| Parameter | Value | Reason for value | Sensitivity range |
|---|---|---|---|
| Falsification threshold (within-±X% match required for retraction) | 10% | Convention: 10% is the WHO-standard "material agreement" cut-off in admin-survey comparisons (cf. `markhof2025records`). | 5% to 15% |
| Rural-urban gradient quintile size | 20% (top + bottom 20% of ADM1 by rural share) | A quintile is the standard tail-tail comparison for small-N geographic analyses. | 10% to 30% |
| PRINCIPAL_FACTYPES set cardinality (PHL) | 14 of 44 NHFR factypes | Hospitals, main clinics, RHUs, MHOs, city/provincial health offices, government and private hospital codes. | 7 to 21 factypes |
| CLINICAL_FACTYPES set cardinality (PHL) | 19 of 44 NHFR factypes | Adds Barangay Health Stations, dialysis, social hygiene clinics, PCR testing, ambulatory surgical to PRINCIPAL. | 10 to 28 factypes |
| Region-18 NIR provcode-split assumption | 4 provcodes manually mapped (18045, 18302 → PH-06; 18046, 18061 → PH-07) | NIR was abolished in 2017; DOH still uses regcode 18. Manual mapping preserves 1,790 facilities (4.0% of total). | Reassign per alternative geographic schemes; test impact on ADM1 totals. |
| OSM-Overpass query window | ADM1 polygon dilate-zero | Strict admin-boundary clip from geoBoundaries gbOpen. | 0–5 km buffer; tests effect of cross-boundary OSM features being misattributed. |

## 7. Primary sources

Cited in `references.bib` by BibTeX key. Pinned in `versions.json`.

- `maina2019facilities` — methodological precedent for facility-list assembly
- `south2021reproducible` — direct method template for the comparison
- `macharia2025mapping` — minimum-completeness criteria
- `sandefur2015badata` — theoretical anchor for systematic admin-vs-alternative-source divergence
- `markhof2025records` — recent quantification of admin-record gap in LMICs
- `herfort2023osm` — global OSM-completeness inequalities baseline

Source pins (from `versions.json`):

- `doh_nhfr_phl` — DOH NHFR v2.0, retrieved 2026-04-25, 44,267 active records, 23 pages
- `geoboundaries` — gbOpen ADM1 polygons for PHL and BGD
- `osm_overpass` — Overpass per-ADM1 amenity queries 2026-04-05 to 2026-04-23

## 8. Decision rule

Given the metric and the sensitivity suite:

- **Positive result** (claim survives): The clinical-tier OSM/registry
  ratio is below 50% in all 17 PHL ADM1 regions and all 8 BGD divisions
  in the baseline run **and** in every ±50% sensitivity-suite run **and**
  the rural-urban gradient is positive in both DMCs in every run.
- **Mixed result** (claim refines, does not retract): The headline
  pattern survives in baseline but flips for one or more parameters in
  the sensitivity suite. The article reports the parameter range over
  which the claim survives.
- **Negative result** (claim retracts): Either (a) the within-±10%
  falsification condition triggers in two or more pilot DMCs in the
  baseline run, or (b) the rural-urban gradient is statistically
  indistinguishable from zero in two or more pilot DMCs in the baseline
  run.

## 9. Stopping rule

Pipeline runs stop when:

- The 17 PHL ADM1 regions and 8 BGD divisions are each represented by
  at least one observation in the OSM cache and at least one observation
  in the registry pull, **OR**
- The OSM-Overpass mirror has been retried 3 times with exponential
  backoff and a partial result is committed with the missing ADM1 noted
  in `coverage.md` §3.

The stopping rule explicitly rejects retrying until coverage is
complete; some ADM1 units in conflict-affected regions or during
Overpass outages may not be recoverable in any one retrieval.

## 10. Attestation (§18 AI-first)

| Field | Value |
|---|---|
| Frozen by | §18 AI-first under `CONSTITUTION.md` §18.1 (owner: Raymond Adofina, repository owner who toggled §18 ACTIVE on 2026-04-25) |
| Date frozen | 2026-04-25 |
| Commit hash | (recorded at the freeze commit) |
| Pipeline run started after this commit | yes (the existing PHL + BGD generated artifacts are exploratory under §3.2; subsequent reruns under this pre-registration begin after the freeze commit) |
| Attestation chain | `ai-first` |

Under §18 ACTIVE, this freeze is binding. Any change to §1–§9 after a
subsequent pipeline run is a retraction of the prior result, not an
edit. The new pre-registration replaces this one and the prior result
moves to `retracted/`.

## 11. AI assistance disclosure (§12 + §18.2)

- This document is AI-drafted and AI-frozen under `CONSTITUTION.md`
  §18.1. The freeze is honest under §18.2: the file's
  `attestation_chain` field is `ai-first`, and any reader sees that
  the freeze was an AI act, not an owner act.
- A subsequent owner-attestation upgrade-pass is allowed (and
  encouraged) under §18.5. If the owner later reads each cited paper
  line-by-line and re-freezes by editing this section's `Frozen by`
  line and re-committing, the artifact's `attestation_chain` upgrades
  from `ai-first` to `mixed` (or `human-final` if every other §18
  attestation is also upgraded). The article is then re-deposited on
  Zenodo with a new DOI version.
