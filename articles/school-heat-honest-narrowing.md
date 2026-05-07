---
slug: school-heat-honest-narrowing
title: A negative result on the school-heat top-5 — only Cambodia survives
subtitle: The top-5 set fails the +/- 50 percent sensitivity gate. Honest narrowing to top-1. The index needs a different functional form.
kind: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [KHM]
topics: [climate-health, schools, methodology]
program: school-heat-disruption
maturity: SR
abstract: >
  The school-heat-pressure index — heat × children-share × pupil-
  teacher-ratio — produces a top-5 ranking across 32 ADB DMCs that
  fails the +/- 50 percent sensitivity gate on its tmax-floor and
  tmax-cap parameters. Only the top-1 (Cambodia) is parameter-
  robust. The article reports the negative result on the top-5
  claim and the honest narrowing to the top-1. The high parameter-
  sensitivity is itself the finding: the index's linear tmax ramp is
  not the right functional form. The Lancet Countdown labor-capacity-
  loss curve and Park et al. 2020 PNAS empirical thresholds are
  the §18.5 upgrade-pass. Published under §18 (AI-First).
doi:
published_at: 2026-04-26
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# Why this is a brief, not a working paper

A claim that fails the sensitivity gate is itself a finding, when
reported honestly. This brief documents that the top-5 of the
school-heat-pressure ranking is **not parameter-robust** under the
pre-registration's +/- 50 percent gate; only the top-1 (Cambodia)
survives every row of the suite.

This is the §18 decision rule working as designed: AI-attested
findings are narrowed to what the data supports, not promoted past
their evidence.

# The diagnosis

The index multiplies four terms:
1. Heat ramp `clamp((tasmax - 25) / 15, 0, 1)`
2. Children share `pop_0_14_pct / 100`
3. PTR factor `min(PTR / 40, 1.5)`
4. Constant 100 for readability

The sensitivity suite shows that perturbations to the heat ramp's
floor (25 → 12.5 / 37.5) and cap (15 → 7.5 / 22.5) shift the top-5
set by 2 or more entries. Only Cambodia stays at #1 across every
row.

# What this means for the program

1. The current index design produces unstable rankings beyond top-1.
2. The Lancet Countdown indicator 1.1.5 (children exposed to
   heatwaves) uses age-specific exposure curves — empirically
   grounded — rather than a linear tmax ramp.
3. Park et al. 2020 (PNAS) document learning-loss thresholds at
   27–32°C; the 25°C floor in this index is empirically too low.

The §18.5 upgrade-pass: replace the linear ramp with a Lancet
Countdown-style heat-stress function and re-run the sensitivity suite.

# What the article still claims

Cambodia holds the top-1 position across every parameter perturbation
and every alternative formulation tested. That single finding is
defensible; the broader top-5 cluster is not.

# Attestation chain

§18 AI-first. AI synthesis from Lancet Countdown, UNICEF EAPRO,
Park et al. 2020 / academic climate-schools network, World Bank CCKP.
**No individual reviewer was contacted.**

Permanent archive: [/program/school-heat-disruption/evidence](/program/school-heat-disruption/evidence).
