---
slug: digital-availability-use-gap-brief
title: Network availability is not internet use
subtitle: Reported mobile broadband coverage routinely exceeds internet use in exact-year ADB developing member cases, so coverage alone is not an adoption measure for connectivity monitoring.
kind: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [digital inclusion, connectivity monitoring]
program: digital-performance
maturity: PP
updated_at: 2026-07-31
abstract: >
  In 2024, reported 4G/LTE population coverage exceeds internet use by a median
  14.3 percentage points across 34 exact-year ADB developing member cases. The
  difference is positive in 31. It is a measurement difference, not a count of
  covered non-users.
published_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# What we found

Do not use national 4G coverage as a proxy for internet adoption. In the 34 ADB developing member economies with exact-year ITU observations in 2024, reported coverage exceeds use by a median **14.3 percentage points**; 31 differences are positive.

![Signed 2024 differences between 4G/LTE coverage and internet use.](/programs/digital-performance/generated/charts/digital-performance-01-availability-use-gap-hero.svg)

- 4G/LTE coverage: people within signal range, irrespective of use.
- Internet use: use from any location in the previous three months.
- Difference: coverage minus use, same economy and year.

The difference is not a person-level count and does not measure speed, reliability, household affordability, skills, or impact.

- In a 28-economy balanced panel, the median gap narrows by 5.9 points from 2018 to 2024, but widens in 12 economies.
- The national 5 GB price basket has a weak association with the 2024 gap (Spearman 0.16; n=32), so one price measure does not explain the pattern.
- The urban–rural use difference has a strong association in the ten matched cases (0.93), but the sample is too small for a regional mechanism claim.
- The headline is unchanged when the roster-coverage floor varies from 25% to 75%.

# What this means

1. Display availability and use together.
2. Carry year, source, method, and missing denominator.
3. Add household affordability, device, skill, and location data before assigning a barrier.
4. Reserve speed-test data for a separate quality layer conditional on testing.

# What this does not say

The gap is a measurement difference, not a count of covered non-users. Speed, reliability, affordability, skills, and impact are not measured by the headline difference. The urban–rural association is too thin for a regional mechanism claim. The result does not rate economies on digital performance.

# Where the evidence lives

Program evidence: `/program/digital-performance/evidence`. Working paper: `articles/digital-availability-use-gap.md`.

`python digital-performance/scripts/build-coverage-use-gap.py --refresh`
