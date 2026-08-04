---
slug: sp-shock-readiness-cluster-brief
title: The shock-payment “top five” fails its own ranking rule
subtitle: The named shock-payment-readiness set fails its own value order and the COVID-19 response source has no comparable delivery outcome—so publish a construct-validation failure, not a prioritization list.
kind: brief
tier: brief
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [social-protection, payments, measurement]
program: social-protection-shock-coverage
maturity: PP
updated_at: 2026-07-31
abstract: >
  The named shock-payment-readiness top five is rejected. Only three members
  survive the panel's own value order, and the external response source does
  not contain a comparable delivery outcome.
references: [worldbank2026aspire, wb2022findex, gentilini2021covidresponses, worldbank2026g2px]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# What we found

Do not use the inherited country ranking for prioritization. Publish it as a construct-validation failure and begin the next study from event-level delivery data.

![The inherited claim fails three validity gates](/programs/social-protection-shock-coverage/generated/charts/sp-three-gate-validity.svg)

The composite multiplies poverty by one minus the average of all-social-protection coverage and account ownership. It computes values even when one proxy leg is missing, then the headline silently requires both legs.

The result is material. The named set `{BGD, LAO, MMR, PAK, PHL}` overlaps the actual value-ranked set `{PAK, VUT, MMR, LAO, TJK}` in only three places. Vanuatu and Tajikistan outrank the Philippines and Bangladesh. Mean imputation keeps the same substitution.

A narrower ASPIRE safety-net variant shares no member with the named set. That does not create a new ranking: its leading observations mix vintages from 1998 to 2017 and are often incomplete.

The World Bank COVID-19 response matrix records cash-transfer instruments in all five named economies [@gentilini2021covidresponses]. Across 24 comparable economies, the inherited gap has near-zero association with eight-category response breadth (Spearman −0.07; 95% bootstrap interval −0.47 to 0.36).

More important, the matrix does not provide a harmonized successful-receipt rate, delivery time, payment-failure rate, or shock-trigger latency. Account ownership and program coverage remain enabling proxies, not transaction-level delivery evidence [@worldbank2026aspire; @wb2022findex; @worldbank2026g2px].

# What this means

Build an event-level table with affected or eligible people, planned and actual recipients, successful and failed payments, initiation and receipt timestamps, benefit amount, channel, geography, shock, and program identifier. Until those objects align, no replacement readiness ranking is warranted.

# What this does not say

The brief does not measure household receipt, payment failure, or shock-trigger latency. It does not rank social-protection system quality. A construct-validation failure is not a claim that the named economies lack programs.

# Where the evidence lives

Program evidence: `/program/social-protection-shock-coverage/evidence`. Working paper: `articles/sp-shock-readiness-cluster.md`.

— `attestation_chain: ai-first`; maturity PP.
