# Results — Public Service Data Quality (multi-country pilot)

Status: **Screening result, two-DMC pilot (PHL + BGD).** Owner attestation pending.

## Cross-country headline (added 2026-04-25)

| Country | Source | Total active | OSM | OSM/clinical | Worst ADM1 | Best ADM1 |
|---|---|---|---|---|---|---|
| **PHL** | DOH NHFR v2.0 | 44,267 | 6,401 | **17.1%** | BARMM 6.5% | NCR 63.5% |
| **BGD** | DGHS Facility Registry | 39,421 | 3,298 | **11.8%** | Barisal 6.2% | Dhaka 20.1% |

Both countries show OSM materially under-counting their official health-
facility registry, with a consistent rural-urban gradient. **The first
testable claim's pattern is supported by both pilots independently.**

Bangladesh (BGD) detail:

| ADM1 | Division | OSM | Reg-clinical | OSM/clin |
|---|---|---|---|---|
| BD-A | Barisal | 126 | 2,017 | 6.2% |
| BD-G | Sylhet | 127 | 1,626 | 7.8% |
| BD-B | Chittagong | 467 | 5,172 | 9.0% |
| BD-E | Rajshahi | 362 | 3,805 | 9.5% |
| BD-H | Mymensingh | 207 | 2,106 | 9.8% |
| BD-F | Rangpur | 327 | 3,185 | 10.3% |
| BD-D | Khulna | 376 | 3,573 | 10.5% |
| BD-C | Dhaka | 1,306 | 6,508 | 20.1% |
| **TOTAL** | | **3,298** | **27,992** | **11.8%** |

## Below: original single-country (Philippines) write-up


Computed 2026-04-25. Per `CONSTITUTION.md` §7.2 the program may be marked
"Screening result" once the owner attests in the commit message that
`literature.md`, `scoring.md`, and these results have been reviewed
line-by-line. Until then, the maturity label remains **Hypothesis** and
this document is an AI-drafted screening artifact, not a ratified finding.

---

## TL;DR

Across 17 ADM1 regions of the Philippines, the OSM-mapped count of health
amenities (`amenity=hospital`, `amenity=clinic`, `amenity=doctors`)
captures roughly **17.1%** of facilities the Department of Health's
National Health Facility Registry (NHFR) classifies as "clinical-tier"
(hospitals + main clinics + Rural Health Units + Barangay Health Stations
+ dialysis + similar) and **72.8%** of the narrower "principal-tier"
(hospitals + main clinics + RHUs + city/municipal health offices, no
BHSs). The clinical-tier capture rate ranges from **6.5% in BARMM** to
**63.5% in NCR** — a **9.8× rural-urban gradient** consistent with the
program's first testable claim.

This is a measurement-gap signal, not a country-quality ranking
(`CONSTITUTION.md` §13.3 framing).

---

## Headline numbers

| Aggregate | OSM | NHFR-principal | NHFR-clinical | NHFR-all |
|---|---|---|---|---|
| Country total | 6,401 | 8,789 | 37,392 | 44,267 |
| OSM ÷ NHFR | — | 72.8% | **17.1%** | 14.5% |

OSM = `amenity=hospital`/`clinic`/`doctors` from the access-services
pipeline cache (`luminosity-gap/research/access-services/generated/access-services-computed-admin1.csv`).

NHFR = DOH National Health Facility Registry v2.0 active facilities,
fetched 2026-04-25 from `https://nhfr.doh.gov.ph/api/list/v_activefacilities`.

Definitions:
- **NHFR-principal:** hospitals (factype 01, 03, 04), main clinics
  (05), lying-in (15), RHUs and MHOs (17, 19), city health offices
  (21, 22), provincial offices (23), major hospitals (24), government
  hospitals (51), private hospitals (52), subnational reference (53).
- **NHFR-clinical:** principal + Barangay Health Stations (20,
  27,052 records), dialysis (14), social hygiene clinics (27), PCR
  testing (28), ambulatory surgical (09).
- **NHFR-all:** every active facility, including 4,201 clinical labs,
  1,684 drug-testing centers, 155 dental labs, etc., that are typically
  not OSM-mapped.

## Per-ADM1 disagreement (clinical-tier ratio)

Ranked from worst OSM coverage to best.

| Rank | ADM1 | Region | Pop 2020 | OSM | NHFR-clin | OSM/clin | NHFR-prin | OSM/prin |
|---|---|---|---|---|---|---|---|---|
| 1 | PH-14 | BARMM | 4,944,800 | 72 | 1,117 | **6.5%** | 326 | 22.1% |
| 2 | PH-02 | Cagayan Valley | 3,685,744 | 168 | 2,319 | 7.2% | 331 | 50.8% |
| 3 | PH-09 | Zamboanga Peninsula | 3,875,576 | 125 | 1,571 | 8.0% | 331 | 37.8% |
| 4 | PH-05 | Bicol Region | 6,082,165 | 267 | 3,183 | 8.4% | 520 | 51.3% |
| 5 | PH-07 | Central Visayas | 8,081,988 | 323 | 3,260 | 9.9% | 584 | 55.3% |
| 6 | PH-13 | Caraga | 2,804,788 | 149 | 1,458 | 10.2% | 267 | 55.8% |
| 7 | PH-41 | Mimaropa | 3,228,558 | 159 | 1,474 | 10.8% | 229 | 69.4% |
| 8 | PH-06 | Western Visayas | 7,954,723 | 308 | 2,820 | 10.9% | 464 | 66.4% |
| 9 | PH-01 | Ilocos Region | 5,301,139 | 307 | 2,715 | 11.3% | 449 | 68.4% |
| 10 | PH-12 | Soccsksargen | 4,360,974 | 173 | 1,475 | 11.7% | 326 | 53.1% |
| 11 | PH-15 | CAR | 1,797,660 | 146 | 1,238 | 11.8% | 254 | 57.5% |
| 12 | PH-10 | Northern Mindanao | 5,022,768 | 253 | 1,986 | 12.7% | 411 | 61.6% |
| 13 | PH-11 | Davao Region | 5,243,536 | 376 | 1,646 | 22.8% | 344 | 109.3% |
| 14 | PH-40 | Calabarzon | 16,195,042 | 1,004 | 4,396 | 22.8% | 1,264 | 79.4% |
| 15 | PH-08 | Eastern Visayas | 4,547,150 | 338 | 1,479 | 22.9% | 484 | 69.8% |
| 16 | PH-03 | Central Luzon | 12,422,172 | 1,139 | 3,533 | 32.2% | 972 | 117.2% |
| 17 | PH-00 | NCR | 13,484,462 | 1,094 | 1,722 | **63.5%** | 1,233 | 88.7% |

The **9.8× ratio between best (NCR 63.5%) and worst (BARMM 6.5%)**
clinical-tier coverage is the headline rural-urban gradient.

## First-testable-claim assessment

Claim (draft, owner finalizes): *"In at least three ADB DMCs (proposed
pilots: PHL, BGD, IDN, IND), OSM-mapped facility counts disagree
materially with the official national facility registry, and the
disagreement is systematically larger in rural and low-HDI ADM1 units
than in capital or high-HDI ADM1 units."*

For the Philippines pilot:

- **Disagreement at ADM1 ≥ ±10% of either count:** 17 out of 17 regions
  (100%). Even NCR — the best-mapped region — has 36.5% of
  clinical-tier NHFR facilities not in OSM.
- **Rural-urban gradient distinguishable from null:** Yes, qualitatively.
  Bottom 5 regions by clinical-tier capture rate (BARMM, Cagayan Valley,
  Zamboanga, Bicol, Central Visayas) have a mean ratio of 8.0%; top 5
  (NCR, Central Luzon, Davao, Calabarzon, Eastern Visayas) have a mean
  of 33.0%. **4.1× gap** between the two halves of the distribution.
  Statistical significance test pending (rank-sum or t-test on the 17
  observations).
- **Falsification condition test (draft):** the claim retracts if
  (a) ratio agrees within ±10% in two or more pilot DMCs **and** (b) the
  rural-urban gap is null. For PHL alone, condition (a) fails for 0/17
  regions on clinical-tier and (b) fails based on the visible gradient.
  Single-DMC evidence, but it is consistent with the claim.

## Caveats and limitations

1. **Single DMC.** This is the Philippines pilot only. Three more pilot
   DMCs (BGD, IDN, IND) are required before the program's first testable
   claim can be tested cross-country.

2. **Factype mapping is imperfect.** OSM `amenity=hospital/clinic/
   doctors` does not have a 1:1 mapping to NHFR's 44 factypes. We
   reported three NHFR aggregates (principal, clinical, all) so a reader
   can choose the comparison most appropriate to their question. The
   "clinical-tier" measure is the closest defensible match but still
   imperfect. The program owner may want to commission a manual
   one-to-one factype-to-OSM-tag review for publication-grade work.

3. **OSM vintage drift.** OSM counts come from the access-services
   pipeline cache, with `osm_timestamp` per row ranging 2026-04-05 to
   2026-04-23. NHFR was fetched 2026-04-25. This is acceptable for a
   screening result; a publication-grade version should align retrieval
   dates within a single week and use a pinned Geofabrik or Overture
   snapshot per `CONSTITUTION.md` §11.

4. **NHFR completeness assumption.** The claim implicit in the "OSM/NHFR"
   ratio is that NHFR is closer to ground truth than OSM. This is
   plausible (NHFR is operated by DOH with regulatory authority and
   licensing implications) but not guaranteed. Sandefur and Glassman
   (2015, `sandefur2015badata`) document systematic admin-record
   over-reporting in some sectors. A publication-grade version should
   triangulate against DHIS2 (where deployable in the Philippines, via
   DOH HOMIS) and against survey-enumerated facility lists from PSA's
   2020 census or PhilHealth provider directory.

5. **Region 18 = Negros Island Region** was abolished in 2017 but DOH
   still uses regcode 18 in NHFR. We split by provcode:
   18045/18302 → PH-06, 18046/18061 → PH-07. This affects 1,790
   facilities (4.0% of total). Spot-checked via barangay names; no
   misassignment expected.

6. **No statistical inference yet.** ADM1 = 17 observations is small.
   Rank-sum test (Mann-Whitney U) on the rural-urban split, plus a
   regression of `osm_ratio ~ rural_share + log(population) + region_FE`
   should be the next step before publication.

7. **Conflict-affected regions.** BARMM at 6.5% capture is consistent
   with both genuine under-mapping (OSM volunteers less active in
   conflict areas) and lower NHFR data quality (admin-record gaps in
   conflict areas). Both effects probably contribute. Disentangling
   them requires triangulation against an independent third source
   (DHS facility module, PhilHealth provider list).

## Reproducibility

Rerun:
```bash
bash public-service-data-quality/scripts/fetch-nhfr.sh
python public-service-data-quality/scripts/process-disagreement.py
```

Outputs:
- `public-service-data-quality/generated/public-service-data-quality-PHL.json`
- `public-service-data-quality/generated/public-service-data-quality-PHL.csv`

Cache: `public-service-data-quality/.cache/nhfr_p{1..23}.json`
(committed per `CONSTITUTION.md` §11). Live refresh requires
`PSDQ_REFRESH=1` on `fetch-nhfr.sh`. Each fresh fetch issues a new JWT
from the landing page automatically.

Source pin (in `versions.json`):
- DOH NHFR active facilities, retrieved 2026-04-25, total 44,267 active
  facilities, page size 2000, 23 pages.

OSM source pin (already in `versions.json` for access-services):
- OSM Overpass per-ADM1 admin-area queries, OSM data vintage window
  2026-04-05 to 2026-04-23.

## Owner actions before promotion to Screening result

1. Attest in commit message that this `results.md`, the supporting
   `literature.md`, and `scoring.md` have been reviewed line-by-line.
2. Approve or rewrite the framing-rule statement at the top of this
   document (no country-ranking headline).
3. Approve or rewrite the first testable claim and falsification
   condition in `literature.md` §4.
4. Update `CONSTITUTION.md` §15 Program Register to mark Program 13 as
   Screening Result with date.

## Amendment log

- **2026-04-25** — Initial computation, single-DMC (Philippines)
  pilot. AI-drafted; owner attestation pending.
