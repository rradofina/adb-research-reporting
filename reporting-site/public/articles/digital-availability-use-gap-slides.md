---
slug: digital-availability-use-gap-slides
title: The network is present. Use still lags.
subtitle: A nine-slide evidence deck on availability and use across ADB developing member economies.
kind: slides
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [digital inclusion, connectivity monitoring]
program: digital-performance
maturity: PP
abstract: Nine-slide presentation of the exact-year ITU availability-use study.
published_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# 1 — Decision question

When reported 4G/LTE availability is high, are people actually using the
Internet at the same rate?

**Why it matters:** rollout, adoption, affordability, and quality require
different interventions.

# 2 — Main finding

In 2024, reported 4G availability exceeds internet use in **31 of 34**
exact-year ADB developing member cases.

Median difference: **14.3 percentage points**.

![Signed headline differences.](/programs/digital-performance/generated/charts/digital-performance-01-availability-use-gap-hero.svg)

# 3 — Two constructs, not one score

**Availability:** population within range of at least a 4G/LTE signal.

**Use:** individuals who used the Internet in the previous three months.

**Gap:** coverage minus use for the same economy and year.

It is not a person-level count, speed measure, or causal effect.

![Method and claim gate.](/programs/digital-performance/generated/charts/digital-performance-12-method-and-claim-gate.svg)

# 4 — Near-universal coverage can coexist with much lower use

Bangladesh, Sri Lanka, India, and the Philippines all report coverage near 100%
and use far below it.

![Coverage and use components in 2024.](/programs/digital-performance/generated/charts/digital-performance-02-components-dumbbell.svg){width=85%}

# 5 — Progress is uneven

The balanced 2018–2024 sample contains 28 economies.

- median gap change: **-5.9 points**;
- narrowed: 16 economies;
- widened: 12 economies.

![Balanced change.](/programs/digital-performance/generated/charts/digital-performance-05-balanced-gap-change.svg)

# 6 — One price basket does not explain the gap

2024 5 GB basket association: Spearman **0.16**, n=32.

Affordability remains relevant; the national basket is not household incidence
and does not measure devices, skills, trust, content, or perceived value.

![Affordability diagnostic.](/programs/digital-performance/generated/charts/digital-performance-06-affordability-association.svg){width=85%}

# 7 — The next data priority is within-economy visibility

Only ten headline cases also have same-year urban and rural use rates.

Their association with the national gap is strong (Spearman 0.93) but too small
for a regional mechanism claim.

![Urban-rural diagnostic.](/programs/digital-performance/generated/charts/digital-performance-07-urban-rural-use-gap.svg)

# 8 — Operational interpretation and reproduction

1. Put availability and use side by side.
2. Show year, source, method, and missing denominator.
3. Add quality, price, devices, and skills as separate layers.
4. Use Ookla only for performance conditional on testing.

Reproduce:

`python digital-performance/scripts/build-coverage-use-gap.py --refresh`
