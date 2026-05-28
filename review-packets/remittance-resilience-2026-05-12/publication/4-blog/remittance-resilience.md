---
slug: remittance-resilience-blog
title: Five economies sit in the upper-right of the remittance-corridor map — and they stay there
subtitle: A set-not-rank result for ADB developing member economies whose dependence on remittance flows runs into the highest published transfer costs.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [KGZ, NPL, TON, VUT, WSM]
topics: [remittances, corridor-cost, fragility-screen]
program: remittance-resilience
maturity: PP
abstract: >
  Five ADB developing member economies — Kyrgyz Republic, Nepal, Tonga,
  Vanuatu, and Samoa — sit in the top five of a joint dependence × cost
  ranking for remittances, and stay there across the full ±50 percent
  sensitivity suite. The result is reported as a stable set, not a rank,
  because the rank inside the set is not robust to the same perturbations
  that leave set-membership stable. The screen is a triage instrument for
  where corridor-cost work deserves attention first; it is not a household
  exposure measure and not a country-quality ranking.
references:
  - wb2024rpw
  - ratha2024migration
  - yang2011migrant
  - un2015sdg10c1
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# Two indicators that point in similar directions

A development planner thinking about remittance-corridor work has two
public indicators to consult. The first is macroeconomic: what share of a
country's GDP arrives as personal remittances? KNOMAD tracks this
yearly in the Migration and Development Brief [@ratha2024migration], and
the World Bank publishes the underlying series in WDI. The second is
operational: what does it actually cost to send money into the
destination country? The World Bank's Remittance Prices Worldwide
(RPW) dataset publishes corridor-firm prices quarterly [@wb2024rpw].

The two indicators are usually read separately. A small Pacific
economy where remittances are 40 percent of GDP gets attention because
of the macro share. A country where corridor costs sit far above the
SDG 10.c.1 target [@un2015sdg10c1] gets attention because of the cost
figure. But a planner deciding where corridor-cost interventions
should go first wants to know where the two stack up *together* — and
that requires a joint view.

# The numbers, as a set

When you build a joint screen across the 21 ADB developing member
economies with both axes observed, five economies persistently sit in
the top five:

- **Kyrgyz Republic** — 26.6% of GDP from remittances, 10.5% mean
  corridor cost.
- **Samoa** — 24.0% of GDP, 8.0% cost.
- **Tonga** — 42.6% of GDP, 7.5% cost.
- **Vanuatu** — 18.8% of GDP, 9.5% cost.
- **Nepal** — 26.2% of GDP, 6.7% cost.

The result is reported as a set, not a rank. The five economies remain
the top five when the dependence cap moves from 12.5% to 37.5%, when
the cost cap moves from 7.5% to 22.5%, when both caps move together,
and when the index aggregation switches from multiplicative to
additive. Top-10 overlap with baseline ranges from 9 of 10 to 10 of 10
across every row of the suite. The rank-order inside the set is not
robust to the same perturbations, so the artifact a reader should cite
is the set, not the table order.

![Dot-plot of 20 rankable ADB developing member economies in dependence × cost space. The horizontal axis is personal remittances received as a share of GDP from the World Bank WDI series; the vertical axis is mean inbound transfer cost as a percent from the World Bank Remittance Prices Worldwide Q1 2025 dataset. Five red bubbles in the upper-right region — Kyrgyz Republic, Nepal, Tonga, Vanuatu, and Samoa — mark the stable top-five set. Bubble size scales with the number of RPW corridors observed: Tonga, Vanuatu, and Samoa appear as small bubbles (two corridors each), Kyrgyz Republic as the smallest (one corridor), Nepal is the only top-five entry with eight corridors. Dashed reference lines show the pre-registered dependence cap (25 percent of GDP) and cost cap (15 percent); the dotted reference line shows SDG target 10.c.1 (3 percent cost).](/programs/remittance-resilience/generated/charts/remittance-fragility-scatter.svg)

# Why this is not a country ranking

Three things make the set defensible while making the *rank* inside the
set unreliable.

First, the cost figures rest on RPW corridor samples that vary by an
order of magnitude across the set. Tonga, Vanuatu, and Samoa are each
observed at two corridors. The Kyrgyz Republic is observed at one.
Nepal — at eight — is the only top-five member whose mean is not
dominated by a small-N average. A reader who wants to be conservative
about the small-sample members can simply look at the chart: the
bubbles for KGZ, TON, VUT, and WSM are small.

Second, the headline cost is a destination-level mean across all
observed corridors. Some of those corridors carry most of the actual
flow; some carry almost none. For the Kyrgyz Republic, the
Russia–Kyrgyz corridor is anomalously low (~2–3 percent) because of
MTO competition and EAEU banking integration; the non-Russia corridors
that drag the destination mean up account for a small share of actual
inbound flow. Volume-weighted cost would be the more appropriate
measure; the data to compute it (central-bank corridor flows, IMF
DOTS) is not in RPW.

Third, informal corridors — hawala/hundi/undocumented MTO use — are
common in GCC → South Asia and Russia → Central Asia routes
[@yang2011migrant]. RPW measures publicly-quoted formal corridors, so
the published cost is an upper bound on what households actually pay
if they substitute into informal channels.

# What the set is and is not for

This is a **triage instrument**, not a final risk rating. It tells a
project pipeline which economies deserve a deeper corridor audit and
household-exposure measurement first. It does not tell a planner what
the household-level cost incidence is, whether informal corridors
substitute for the formal ones RPW observes, or whether
volume-weighted cost would re-order the set.

It also does not measure resilience proper. The program name is a
legacy; the screen measures *exposure* to corridor-cost stress
combined with macro dependence. Resilience — counter-cyclicality of
the flow, diversification of sources, household ability to absorb a
shock — requires a different program and different data (LSMS, DHS,
central-bank flow series).

# What's next

The full working paper documents the method, the sensitivity suite,
the limitations, and the upgrade path to a human-final attestation at
`articles/remittance-corridors-vulnerability-cluster.md`. The
reproducibility runbook and committed scripts live in
`remittance-resilience/`. This blog post carries an `ai-first`
attestation chain under `CONSTITUTION.md` §18; the path to a
human-final upgrade (volume-weighted cost, household receipt
concentration, real external reviewer contact, owner-signed
attestation) is open and explicit.
