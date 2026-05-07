---
slug: per-capita-shifts-the-cluster
title: Population-weighted indices conceal Pacific vulnerability — the per-capita reanalysis
subtitle: When flood-event and coastal indices are recomputed per million population, the top-5 cluster flips from large South-Asian economies to Pacific small-island states. Same data, different scaling, different policy frame.
kind: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [MHL, KIR, FSM, FJI, SLB, TUV]
topics: [meta-analysis, per-capita, Pacific, vulnerability]
program: meta
maturity: SR
abstract: >
  The lab's headline cluster — Bangladesh, Afghanistan, India, China,
  Pakistan — is partly an absolute-scale artifact. Programs whose
  index includes log10(population) or absolute event counts surface
  large-population economies. When the same data is recomputed
  per-capita, an entirely different top-5 emerges: Pacific small-
  island states (Marshall Islands, Kiribati, FSM, Fiji, Solomon
  Islands) for flood exposure; Tuvalu enters the coastal cluster.
  This brief documents the population-weighting artifact, distinguishes
  programs that are scale-invariant by construction (remittance-
  resilience top-5 set is identical under absolute and per-capita
  rankings) from those that are not (flood, coastal, disaster). The
  policy implication is not "the cluster is wrong" — both rankings
  answer real questions — but a reader citing the lab must say which
  question. Published under §18 (AI-First).
doi:
published_at: 2026-04-27
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
references:
  - briguglio2009vulnerability
  - sen1999development
  - stiglitz2009measuring
  - mcgranahan2007rising
  - anu2023palm
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The artifact

The lab's joint-vulnerability cluster brief reports that five economies —
Bangladesh, Afghanistan, India, China, Pakistan — sit in five or more
program top-N sets each. That finding is real, but it is also
partially an artifact of how the underlying program indices treat
population scale.

Of the 16 programs at SR/PR, several have indices that include
absolute population terms — `log10(population)` for coastal-informal-
risk and flood-market-access, raw event counts for disaster-recovery-
lag. Those programs systematically rank large-population economies
higher, regardless of per-capita exposure intensity.

This brief recomputes the same data per-capita and reports the
shifted top-5.

# What changes when you re-scale

| Program | Absolute top-5 | Per-capita top-5 |
|---|---|---|
| **flood-market-access** | IND, IDN, CHN, AFG, PAK | **MHL, KIR, FSM, FJI, SLB** |
| **coastal-informal-risk** | PAK, PHL, CHN, BGD, MMR | TUV, PAK, PHL, MMR, CHN |
| **disaster-recovery-lag** (events/yr) | CHN, IDN, IND, PHL, VNM | (event-per-DMC already per-capita-adjusted in EM-DAT methodology) |
| **remittance-resilience** | KGZ, NPL, TON, VUT, WSM | identical (already population-invariant by construction) |

For flood-market-access the shift is total. The same EM-DAT 2000–2025
flood subset, reweighted from flood-events × log10(population) to
flood-events per million population, produces an entirely Pacific-
small-island top-5. Marshall Islands, Kiribati, FSM, Fiji, Solomon
Islands.

For coastal-informal-risk the shift is partial: PAK, PHL, MMR, CHN
remain in the top-5; Tuvalu enters at #1 because its entire population
sits in the LECZ [@mcgranahan2007rising].

For remittance-resilience the top-5 is invariant. The fragility-index
formulation uses GDP-share for the dependence axis and corridor-mean
cost for the cost axis — neither absolute. The set {KGZ, NPL, TON, VUT,
WSM} is the same under any plausible scaling.

# Why both are real

This brief does not say "the per-capita ranking is correct and the
absolute ranking is wrong." Both rankings answer real questions:

- **Absolute ranking** answers "where is the largest absolute
  measurement-gap burden?" — relevant for cross-DMC budget allocation
  proportional to affected population.
- **Per-capita ranking** answers "where is the highest measurement-
  gap exposure rate?" — relevant for adaptation programs designed
  per-capita.

The Stiglitz-Sen-Fitoussi commission [@stiglitz2009measuring]
explicitly argues for both alongside multidimensional measurement.
Briguglio et al. 2009 [@briguglio2009vulnerability] develops the
vulnerability-resilience framework specifically for small economies
and is cited extensively in Pacific labor-mobility work
[@anu2023palm]. The capability approach [@sen1999development] points
toward per-capita as closer to the welfare quantity.

# What the lab should do

The honest disclosure: every program's article in this issue
already reports the absolute ranking; this brief reports the
per-capita reanalysis where the indices are not scale-invariant
by construction. A future issue extends every program's
sensitivity suite to include the per-capita-vs-absolute switch as
a robustness row, alongside the +/- 50 percent parameter
perturbations.

The Pacific small-island economies' absence from the original
joint-vulnerability cluster is not evidence of low vulnerability —
it is evidence that absolute-scale indices undercount populations
under 200,000.

# What this brief does not say

- **No new index.** The brief does not propose a new composite. It
  documents that two scaling choices produce two valid rankings.
- **No claim about which scaling is right for which program.** That
  decision belongs to each program's pre-registration and the §18.5
  upgrade-pass.
- **EM-DAT thresholds still apply.** Per-capita re-scaling does not
  fix the under-counting of small recurrent events; it only
  re-allocates the events that meet thresholds.
- **Population weighting affects PR articles, not just SR.** The PR
  programs that include population terms (port-hinterland-friction,
  social-protection-shock-coverage) are subject to the same
  reanalysis if extended.

# Permanent archive

`research/per-capita-reanalysis.json` in the upstream repository.

— `attestation_chain: ai-first` · 2026-04-27
