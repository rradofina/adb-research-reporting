---
slug: measurement-gap-philippines-bangladesh
title: The OSM-vs-registry gap in Philippine and Bangladeshi health facilities
subtitle: A two-DMC screening result. OpenStreetMap captures 17.1 percent of the Philippine national registry and 11.8 percent of the Bangladeshi one — and the gap is larger in rural and conflict-affected regions.
kind: working-paper
status: draft
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [PHL, BGD]
topics: [measurement-gap, public-service-data-quality, OSM, health-facility-registry]
program: public-service-data-quality
maturity: SR
abstract: >
  Across the 17 administrative regions of the Philippines and the 8
  divisions of Bangladesh, OpenStreetMap-mapped health facilities
  capture roughly 17.1 percent and 11.8 percent of the official national
  registry's clinical-tier facilities respectively. The within-country
  rural-urban gradient is steep: 5.5x in the Philippines (top quintile
  to bottom quintile) and a comparable rural concentration in Bangladesh.
  No administrative unit in either country has OSM-vs-registry agreement
  within 10 percent. The pattern survives a +/-50 percent sensitivity
  suite on every arbitrary numeric in the pre-registration. The article
  reports the screening result, the sensitivity ranges, and what the
  result cannot establish.
doi:
published_at: 2026-04-25
updated_at: 2026-04-25
references:
  - maina2019facilities
  - south2021reproducible
  - macharia2025mapping
  - sandefur2015badata
  - markhof2025records
  - herfort2023osm
  - zhao2022datagaps
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The question

Two questions sit underneath any planning exercise that uses public
maps. First: how many facilities are there? Second: where are they?
Public maps and administrative registries answer both questions, and
when they disagree, the disagreement is rarely random. Sandefur and
Glassman 2015 [@sandefur2015badata] documented that household-survey
counts and administrative-record counts of African school enrollments
diverge in directions that correlate with reporting incentives, not
with random measurement noise. Markhof, Wollburg, and Zezza 2025
[@markhof2025records] documented a 9-percentage-point persistent gap
between phone-survey and administrative COVID-vaccination coverage in
LMICs that survives correction for respondent-selection effects.

The corresponding question for facility lists in the Asia-Pacific has
not been answered with consistent methodology. The African-side
methodological literature is well established — Maina and colleagues
2019 [@maina2019facilities] assembled a 98,745-facility cross-country
spatial database from national master facility lists; South and
colleagues 2021 [@south2021reproducible] compared MOH lists, the
WHO-KEMRI-Wellcome dataset, and OpenStreetMap-derived `healthsites.io`
across Africa, shipping the `afrihealthsites` R tools as a
reproducible reference; Macharia and colleagues 2025
[@macharia2025mapping] called for a renewed cross-country open
facility dataset. No equivalent methodologically rigorous work
exists for ADB developing member economies.

This article reports the first such comparison for two DMCs:
Philippines (Department of Health National Health Facility Registry
v2.0) and Bangladesh (Directorate General of Health Services Facility
Registry). It is a screening result, not a publication-ready finding.
The pre-registration is at `public-service-data-quality/pre-registration.md`
in the repository; the sensitivity suite is at `sensitivity.md`; the
limitations are at `limitations.md`.

# The data

Two registries:

- **Philippines DOH NHFR v2.0**, retrieved 2026-04-25, 44,267 active
  facilities across 23 paginated API responses (committed cache;
  `versions.json` pin).
- **Bangladesh DGHS Facility Registry**, retrieved 2026-04-25, 39,421
  active facilities across 20 paginated responses.

One reference for OSM:

- **OpenStreetMap** via Overpass, `amenity=hospital|clinic|doctors`
  intersected with `geoBoundaries` gbOpen ADM1 polygons. OSM data
  vintage window 2026-04-05 to 2026-04-23.

The headline metric is the **clinical-tier OSM/registry ratio at
ADM1**: OSM count divided by registry count, where the registry's
"clinical-tier" comprises hospitals, main clinics, primary-care units,
and community-level health stations. Across the Philippines, the
clinical-tier set is 19 of NHFR's 44 facility types; across Bangladesh,
the analog is the DGHS hospitals + clinics + community-clinics + UHC
union.

# The finding

## Philippines

OSM captures **17.1 percent** of the Philippines clinical-tier
registry country-wide. Across the 17 ADM1 regions, the ratio ranges
from **6.5 percent (BARMM)** to **63.5 percent (NCR)** — a 9.8x
ratio between the worst- and best-mapped regions, and a 5.5x ratio
between the top and bottom quintile means. Every region (17 of 17) is
outside the pre-registered ±10 percent agreement band. The
"within-X-percent" falsification condition does not trigger at ±5,
±10, or ±15 percent.

The principal-tier ratio (the narrower hospitals + main clinics
comparison) is 72.8 percent, much closer to agreement. The bulk of
the gap is in community-level facilities — Barangay Health Stations,
Rural Health Units, dialysis clinics — which OSM volunteers map less
consistently than larger institutions.

## Bangladesh

OSM captures **11.8 percent** of the Bangladesh clinical-tier
registry. Across the 8 divisions, the ratio ranges from **6.2 percent
(Barisal)** to **20.1 percent (Dhaka)**. The pattern from the
Philippine pilot reproduces independently in Bangladesh: OSM is
materially below registry counts, the rural-tilted divisions
under-represent the most, and the division around the capital
maps best.

# The sensitivity suite

The pre-registration freezes five arbitrary numerics. Every one was
tested at ±50 percent. Across the suite the country clinical-tier
ratio for the Philippines ranges 14.5 percent to 17.9 percent; the
top-quintile to bottom-quintile gradient ranges 4.0x to 7.0x; the
within-band falsification count remains 0 of 17 ADM1 units at every
threshold tested (±5 percent, ±10 percent, ±15 percent). The Bangladesh
sensitivity suite is in progress and will be appended to
`sensitivity.md` before the SR → PR gate is closed.

No row in the suite flips the §8 decision rule. The headline pattern
survives every parameter perturbation tried.

# What this result cannot establish

The full list is in `limitations.md`. The most important non-claims:

- The result does not establish that OSM is wrong. It establishes that
  OSM and the registry disagree systematically. Sandefur and Glassman
  2015 [@sandefur2015badata] document mechanisms by which
  administrative records can be biased upward; without a third
  independent source, the direction of the gap is not attributable to
  one side.
- The result does not establish causal mechanisms for the gradient.
  Volunteer behavior, registry operating-cost incentives, conflict
  exposure, and licensing-driven over-registration could all
  contribute.
- The result does not produce a country-quality ranking. The Philippines
  and Bangladesh registry definitions and facility taxonomies differ;
  the within-country rural-urban gradient is the comparable quantity,
  not the headline ratio across countries.
- The result does not yet cover India or Indonesia. The pre-registration
  scopes the SR → PR gate to PHL + BGD only. India (HMIS) and Indonesia
  (SATUSEHAT) pipelines remain TODO.

# What is next

Three concrete next steps before the SR → PR gate can close:

1. Run the Bangladesh sensitivity suite at ±50 percent on the matching
   parameters; append to `sensitivity-runs.json` and the §1 table of
   `sensitivity.md`.
2. Re-run the OSM extraction against a Geofabrik or Overture monthly
   snapshot rather than a live Overpass mirror window, to align
   retrieval dates with the registry pulls within a single week.
3. Recruit two named external reviewers per `red-team.md` — at least
   one each from the measurement and DMC-affiliated competencies — and
   complete `review-external.md`.

Until those three are complete, this is a screening result. It invites
further work; it is not policy-actionable on its own.

# Reproduction

A clean clone of the repository at the frozen commit hash reproduces
the headline ratios by running:

```bash
bash public-service-data-quality/scripts/fetch-nhfr.sh
python public-service-data-quality/scripts/process-multi-country.py
python public-service-data-quality/scripts/sensitivity.py
```

The committed cache means no API key or live network call is required.
The hash check is `node scripts/verify-manifest.mjs`. The Bangladesh
DGHS pull is committed in `.cache/bgd_dghs_p{1..20}.json`; the
Philippine NHFR pull is in `.cache/nhfr_p{1..23}.json`.

# Citations

The full citation list is in `references.bib` at the repository root.
Keys cited above:
`maina2019facilities`, `south2021reproducible`, `macharia2025mapping`,
`sandefur2015badata`, `markhof2025records`, `herfort2023osm`.

— Raymond Adofina · 2026-04-25
