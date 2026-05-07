---
slug: food-price-joint-qualifier
title: Two DMCs sit at the top of both food-price-stress rankings — Lao PDR and Pakistan
subtitle: Joint top-N intersection of CPI inflation and ag-imports share. Set-based reformulation after the original composite failed the sensitivity gate.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [LAO, PAK, BGD]
topics: [food-price, joint-vulnerability, methodology]
program: food-price-climate-transmission
maturity: SR
abstract: >
  The original food-price composite-index formulation failed the
  +/-50 percent sensitivity gate (alternative sub-metric weights
  produced no stable top-5). This article reports the reformulated
  set-based joint qualifier across 43 ADB DMCs: two economies — Lao
  PDR and Pakistan — sit in the top-N of BOTH WDI CPI inflation AND
  ag-imports-share-of-merchandise for every N from 3 to 10. A third,
  Bangladesh, joins from N=5. The reformulation is invariant to
  weight choice by construction. The article does NOT claim
  climate-CPI transmission; the named program question requires sub-
  annual + commodity-level analysis, deferred to §18.5 upgrade-pass.
  Pakistan's 2023 CPI was exchange-rate-driven, flagged separately
  from climate vulnerability. Published under §18 (AI-First).
doi:
published_at: 2026-04-27
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# What changed

The first attempt at this program failed the sensitivity gate. The
original composite-index formula combined CPI inflation, ag-imports
share, and food-production index with weights — and different weight
choices produced different top-5 sets with no overlap. Per
Constitution §6.6 and the program's own pre-registration §8 decision
rule, that's a fail.

The reformulation is set-based, not score-based. A DMC qualifies if
it is in the top-N of both individual rankings — CPI and ag-imports —
simultaneously. The "intersection" set is the headline. Weight choice
disappears from the formulation.

# The finding

| ISO3 | DMC | CPI inflation % | Ag imports % merch | Joint top-N? |
|---|---|---|---|---|
| LAO | Lao PDR | 23.1 | 4.6 | yes (every N from 3 to 10) |
| PAK | Pakistan | 12.6 | 4.3 | yes (every N from 3 to 10) |
| BGD | Bangladesh | 10.5 | 6.0 | yes (N ≥ 5) |

The set `{LAO, PAK}` is stable across every N tested. `{BGD}` joins
from N=5 onward.

# What it cannot say

- The article does **not** claim climate transmission. The named
  program question requires sub-annual + commodity-level CPI
  analysis linked to climate-anomaly timestamps. Annual country-
  mean CPI cannot detect transmission events.
- Pakistan's 2023 CPI was exchange-rate-driven (per WB Food Crisis
  Observatory). The joint qualifier doesn't separate drivers.
- WDI ag-imports includes non-food (cotton, rubber). Food-specific
  subset is the upgrade-pass.
- WFP/IPC food-insecurity classification is the actionable layer for
  food crisis; this artifact is structural-vulnerability only.

# Permanent archive

[/program/food-price-climate-transmission/evidence](/program/food-price-climate-transmission/evidence)

— `attestation_chain: ai-first`
