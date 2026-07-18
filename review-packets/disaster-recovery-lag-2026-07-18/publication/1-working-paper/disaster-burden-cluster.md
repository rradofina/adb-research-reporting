---
slug: disaster-burden-cluster
title: A disaster-recovery ranking fails two validity gates
subtitle: Country burden changes with the metric, while a 108-orbit Haiyan pilot yields no centroid with one recovery month across 54 variants.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [PHL, Asia-Pacific]
topics: [disaster-recovery, nighttime-lights, measurement-validity, GDIS]
program: disaster-recovery-lag
maturity: PP
abstract: >
  This paper tests whether public disaster records and daily nighttime
  radiance support a defensible recovery-month measure. The inherited
  China–India disaster-burden top two fails under three of five metrics.
  A direct Typhoon Haiyan pilot then extracts 108 fixed VIIRS-DNB orbits for
  seven GDIS administrative centroids, evaluates 54 recovery specifications
  per centroid, and finds no centroid with one stable recovery month. Only one
  centroid has four valid pre-event baseline months. A 2,881-centroid geometry
  screen also finds three gross country mismatches. The public archive is
  accessible; the proposed recovery construct is not yet validated.
published_at: 2026-07-18
updated_at: 2026-07-18
references: [cred2024emdat, undrr2015sendai, rosvold2021gdis, roman2018blackmarble, skoufias2021viirs, worldbank2026light, noaa2013haiyan, naturalearth2025admin0]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The finding

A disaster-recovery ranking fails before it can become a ranking. The inherited
country headline changes when burden changes definition, and the more direct
nighttime-light measure does not return one stable recovery month.

![Two-stage validity gate](/programs/disaster-recovery-lag/generated/charts/disaster-two-stage-validity-gate.svg)

The first result is not subtle. China and India are the top two for total
affected and adjusted damage, but the pair becomes China–Indonesia for event
frequency, Indonesia–Myanmar for deaths, and Tuvalu–Marshall Islands for the
indicative per-million screen. Three of five metrics trigger the original kill
rule.

The second result is even more important. Across seven Typhoon Haiyan
administrative centroids and 54 reasonable recovery definitions, no centroid
has one recovery month throughout. This is not evidence that places failed to
recover. It is evidence that this measurement chain cannot yet say when they did.

# Why burden cannot answer a recovery question

Disaster databases make several legitimate quantities visible: how often an
event is recorded, how many people are reported affected, how many deaths are
reported, and how much damage is assessed. These quantities describe different
parts of disaster burden. They do not measure the time required to restore
electricity, services, livelihoods, or welfare.

![Five burden metrics produce different leading sets](/programs/disaster-recovery-lag/generated/charts/disaster-metric-rank-disagreement.svg)

The disagreement is informative. Absolute totals privilege population and
asset scale. Mortality concentrates attention on rare severe events. Frequency
is sensitive to hazard incidence and recording. Scaling cumulative events by a
single recent population denominator turns the leading set toward Pacific
small island economies.

![The per-capita screen inverts the leading set](/programs/disaster-recovery-lag/generated/charts/disaster-per-capita-inversion.svg)

That last comparison is deliberately labelled indicative: it divides 2000–2025
events by 2024 population. It demonstrates scale dependence; it is not a final
annualized exposure rate.

# What related research says

EM-DAT is a central public source for disaster occurrence and reported impacts,
but its fields are not a common severity scale [@cred2024emdat]. GDIS improves
the unit of analysis by linking 9,924 disasters to 39,953 named administrative
locations [@rosvold2021gdis]. Its authors also state the crucial limitation:
administrative polygons and centroids are approximations of impact zones.

High-frequency nighttime light is attractive because severe storms can disrupt
electricity and visible activity immediately. Black Marble processing supplies
quality, cloud, atmospheric, terrain, and lunar information needed for daily
work [@roman2018blackmarble]. The World Bank makes these public products
available in analysis-ready cloud storage [@worldbank2026light]. Yet prior
multi-event tests in Southeast Asia show that VIIRS short-run disaster signals
depend on hazard, event, and specification [@skoufias2021viirs]. The literature
therefore motivates validation, not automatic substitution for recovery.

# Data availability: a four-step ladder

The program works backward from the outcome. A country burden table is only the
first step. Measuring recovery requires dated events, plausible affected
geography, repeated observations, and an interpretable outcome.

![Source ladder from country burden to recovery outcome](/programs/disaster-recovery-lag/generated/charts/disaster-source-ladder.svg)

The source intersection is real. During the 2012–2018 GDIS–VIIRS overlap, 609
unique GDIS IDs, 565 disaster numbers, and 2,881 locations fall in ADB
developing member economies. The World Bank archive is readable without a user
account. Access, however, is only one validity gate.

# Method: a frozen Haiyan pilot

Typhoon Haiyan is linked through GDIS disaster number `2013-0433`, with the
event date set to 8 November 2013. Seven named first-order administrative
centroids are retained: Aklan, Capiz, Cebu, Iloilo, Leyte, Palawan, and Samar.

The script samples six fixed dates per month from May 2013 through October 2014,
for 108 scheduled satellite orbits. It filters for valid, clear, nighttime,
non-stray-light, non-lightning observations and pairs each affected window with
a same-orbit Manila reference. Missing pairs remain missing.

The main rule uses mean radiance within a 50 km square half-width, a pre-event
baseline, recovery at 90% of baseline, and two-month persistence. A month needs
two paired nights and at least 25 valid pixels per window. The construct passes
only if at least three centroids have four valid baseline months, a main result,
and the same recovery month under all variants.

![Valid paired nights by centroid and month](/programs/disaster-recovery-lag/generated/charts/disaster-haiyan-observation-coverage.svg)

Only Samar has four valid baseline months. Missingness arises from orbit swath,
quality flags, valid-pixel minimums, and the paired reference—not zero light.

# Main results

The main specification detects March 2014 for Aklan, September 2014 for
Palawan, and June 2014 for Samar. It detects no qualifying month for Capiz,
Cebu, Iloilo, or Leyte within the window.

![Main-specification monthly radiance index](/programs/disaster-recovery-lag/generated/charts/disaster-haiyan-main-series.svg)

Those dates are not the headline. Raw background-subtracted radiance can be
negative, dark baselines produce volatile ratios, and the plotted series is
clipped only to remain readable. The main result is a candidate output whose
stability must be tested.

# Sensitivity: 54 ways to define return

The full matrix crosses radius 25/50/75 km, mean/p75 radiance, threshold
80/90/100%, and persistence one/two/three months. Radius and persistence span
the required ±50% choices around the main values.

![Recovery outcome across 54 specifications](/programs/disaster-recovery-lag/generated/charts/disaster-haiyan-sensitivity.svg)

Every centroid changes outcome. Aklan and Samar have no detected recovery in
12 of 54 variants; Cebu has none in 44. The centroids produce between three and
seven distinct outcomes. Zero of seven therefore meet the stable-month rule.

# Geometry audit

Before expanding, the pipeline tests all 2,881 candidate centroids against
Natural Earth country polygons in an equal-area projection. Three lie more than
1,000 km from their associated country: Fiji Eastern, Fiji Northern, and a
Philippine Cordillera row.

![Gross GDIS centroid mismatch screen](/programs/disaster-recovery-lag/generated/charts/disaster-gdis-geometry-audit.svg)

The 1,000 km cutoff is intentionally a gross-error screen. Passing it does not
prove that an administrative centroid represents the affected footprint.

# What the result means

The pipeline succeeds as research because it separates technical scalability
from inferential validity. Public object storage can serve the rasters; scripts
can extract and quality-filter them; a database can later index events,
geometries, observations, specifications, and results. None of those engineering
achievements licenses the word “recovery.”

For a defensible recovery study, the next evidence object should combine
verified hazard or damage footprints, a longer local baseline, settlement-aware
aggregation, comparison areas, and an independent outcome such as electricity
restoration, facility operation, school reopening, firm activity, or household
recovery.

# Conclusion

Country burden is not recovery, and access to daily nighttime lights is not
validation of a recovery measure. The burden headline fails under three of five
metrics. The Haiyan pilot fails the frozen construct rule at all seven
centroids. The responsible result is therefore not a new ranking but a clear
measurement boundary—and a precise specification of what the next study must add.

**Attestation.** AI-first synthesis and computation under Constitution §18.
No individual external reviewer was contacted. Human-final review remains
owner-led.
