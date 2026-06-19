---
slug: public-service-data-quality-brief
title: When the public map disagrees with the official registry
subtitle: A one-page brief on the measurement gap between OpenStreetMap health facilities and the Philippine and Bangladeshi national registries.
kind: brief
tier: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [PHL, BGD]
topics: [measurement-gap, public-service-data-quality, OSM, health-facility-registry]
program: public-service-data-quality
maturity: PR
abstract: >
  OpenStreetMap captures 17.1 percent of Philippine and 11.8 percent of
  Bangladeshi clinical-tier health facilities recorded by the official
  national registries. The gap is systematically larger in rural and
  low-density admin units. Project preparation that reads facility
  availability from OSM alone will misread service supply by a factor
  that depends on which region of the country is being read.
references:
  - macharia2025mapping
  - sandefur2015badata
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The issue

Public maps and official administrative registries answer the same two
questions — *how many facilities are there* and *where are they* — and they
disagree, especially where it matters most. In two ADB developing member
economies (Philippines and Bangladesh), OpenStreetMap captures only
**17.1%** and **11.8%** respectively of the clinical-tier facilities listed
by each country's national health-facility registry [@macharia2025mapping].
A planner reading the public map alone will see a different country than a
planner reading the registry alone. The disagreement is not random
[@sandefur2015badata] — it is systematically larger in rural, low-density,
and conflict-affected admin units.

# What we found

- **Philippines (DOH NHFR, 44,267 active facilities, 2026-04-25).** The OSM
  share of clinical-tier registry entries ranges from **6.5% in BARMM** to
  **63.5% in NCR** — a 9.8× rural-urban gradient across 17 ADM1 regions.
  Every region disagrees with OSM by more than ±10%.
- **Bangladesh (DGHS Facility Registry, 39,421 active facilities, 2026-04-25).**
  The OSM share ranges from **6.2% in Barisal** to **20.1% in Dhaka** — the
  same direction of gradient, narrower because the country is smaller and
  more urbanised.
- **Both countries**, every parameter in a ±50% sensitivity sweep
  (factype set, gradient quintile size, falsification threshold)
  preserves the direction and order of the finding.
- **Granular layer (Philippines).** At city/municipality level (1,642 ADM3
  units), the registry-map gap can be read alongside official 2023 PSA
  poverty incidence for 1,632 of those units. Ten units remain explicitly
  source-missing rather than imputed.

![Philippines — OSM ÷ NHFR clinical-tier ratio per ADM1 region. Best: NCR
63.5%. Worst: BARMM 6.5%.](/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm1.svg)

# Why it matters for project preparation

Health-system project pipelines that assume OSM coverage is a fair stand-in
for the registry will under-estimate facility density most severely exactly
where additional access matters most — rural and conflict-affected admin
units. The same logic applies to schools, markets, and other public-service
amenities. The remedy is straightforward: any OSM-derived denominator used
for planning purposes should be cross-checked against the relevant national
registry, and the disagreement reported alongside the denominator. The
methodological precedent for this exists in the African health-facility-list
literature; what has been missing is the parallel evidence for ADB DMCs.

# What this brief does NOT claim

- It does **not** claim OSM is wrong. It claims OSM and the registry
  *disagree*, and the direction is systematic.
- It does **not** rank countries. The ratios are not directly comparable
  between PHL and BGD because registry definitions differ; the
  *within-country* gradient is the comparable finding.
- It does **not** establish causal mechanisms. Volunteer behaviour,
  registry incentives, and conflict exposure all plausibly contribute.
- It is **not** human-final. Under `CONSTITUTION.md` §18, this brief
  carries an `ai-first` attestation chain. Owner attestation, line-by-line
  paper reading, and external reviewer contact are pre-conditions for a
  human-final upgrade.

# Source and reproduction

Working paper: `articles/measurement-gap-philippines-bangladesh.md`.
Evidence packet: `/program/public-service-data-quality/evidence`.
Pipeline: `public-service-data-quality/scripts/`. Sensitivity:
`public-service-data-quality/sensitivity.md`. Limitations:
`public-service-data-quality/limitations.md`. Chart code:
`public-service-data-quality/scripts/build-choropleth.py` reading
`generated/public-service-data-quality-PHL.csv`.
