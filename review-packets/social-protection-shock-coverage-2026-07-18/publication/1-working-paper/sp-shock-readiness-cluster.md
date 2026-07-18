---
slug: sp-shock-readiness-cluster
title: The “stable top five” was fixed by a missing-data rule
subtitle: Two omitted economies outrank the published tail, every named economy had a documented COVID-19 cash-transfer response, and no comparable delivery outcome is joined.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [social-protection, financial-inclusion, shock-response, measurement]
program: social-protection-shock-coverage
maturity: PP
abstract: >
  An inherited country screen multiplied the World Bank poverty headcount by
  one minus the average of ASPIRE social-protection coverage and Global Findex
  account ownership, then named Bangladesh, Lao PDR, Myanmar, Pakistan, and the
  Philippines as a stable shock-payment-readiness-gap top five. This paper
  audits the construction before adding more polish. The named set is not the
  panel's descending value order: Vanuatu and Tajikistan outrank the
  Philippines and Bangladesh but were omitted because each lacks one proxy
  leg. Mean imputation preserves that substitution. Replacing all-social-
  protection coverage with the narrower safety-net series produces zero
  overlap, but with old and incomplete observations that cannot support a
  replacement ranking. A new parse of the World Bank COVID-19 response matrix
  documents cash-transfer instruments in all five named economies, yet the
  source does not supply comparable successful-receipt, delivery-time,
  payment-failure, or trigger-latency outcomes. The country ranking is
  rejected. The defensible contribution is a construct-validation result and
  a precise specification of the next data object.
doi:
published_at: 2026-04-26
updated_at: 2026-07-18
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The finding

The published “stable top five” was not the panel's value-ranked top five.
Pakistan, Vanuatu, Myanmar, Lao PDR, and Tajikistan have the five highest
computed values. The article instead named Bangladesh, Lao PDR, Myanmar,
Pakistan, and the Philippines. Only three members overlap.

![Three validity gates show where the inherited claim fails](/programs/social-protection-shock-coverage/generated/charts/sp-three-gate-validity.svg)

This is not a corrected readiness ranking. It is evidence that the ranking
should be retired. The composite changes its missing-data rule between the
calculation and the headline; its coverage leg is broader than shock-responsive
social assistance; its account leg measures ownership rather than payment use;
and no joined outcome says whether a transfer arrived, how long it took, or who
failed to receive it.

# Research problem and background

Shock-responsive social protection is a delivery problem as well as a coverage
problem. A system must identify people affected by a shock, enroll or verify
them, authorize support, move funds or assistance through an operating channel,
and resolve failures. Each step has a denominator and a time dimension.

The inherited screen had none of those event-level objects. It combined three
national indicators:

1. poverty headcount at $3.00 a day in 2021 purchasing-power-parity terms;
2. coverage of all social-protection and labor programs; and
3. ownership of an account at a financial institution or mobile-money provider.

ASPIRE is a valuable compilation of social assistance, social insurance, and
labor-market indicators, but the World Bank explicitly notes cross-country
comparability caveats [@worldbank2026aspire]. Global Findex measures access and
use at the adult level; an account can be inactive, inaccessible during a
shock, controlled by another household member, or disconnected from a specific
government program [@wb2022findex]. The G2Px evidence agenda therefore treats
payment architecture and recipient experience as separate objects rather than
assuming that account ownership equals successful receipt [@worldbank2026g2px].

The research question is consequently not “which economies are least ready?”
It is narrower and falsifiable: **does the inherited construction preserve its
own stated ranking rule, and does a qualified direct response source validate
the interpretation attached to that ranking?**

# Data

The inherited panel covers the 43-economy ADB developing member roster. It uses
the latest World Development Indicators observation available for each economy
and indicator, rather than a common year. Thirty-six economies have a current
poverty observation in the source audit, 35 have an all-social-protection
coverage observation, and 27 have an account-ownership observation. Only 24
economies have a computed gap and a documented row in the external response
matrix used for the correlation diagnostic.

The current World Bank metadata labels `SI.POV.DDAY` as poverty at $3.00 a day
(2021 PPP). Earlier program prose called the same code $2.15 a day (2017 PPP).
The values were retrieved again under the current metadata; this paper uses the
current label and records the mismatch rather than silently retaining the old
definition.

![The source stack narrows without ever reaching a comparable delivery outcome](/programs/social-protection-shock-coverage/generated/charts/sp-source-alignment-funnel.svg)

For the external construct check, the pipeline parses pages 5–10 of the World
Bank *Global Database on Social Protection and Jobs Responses to COVID-19*,
version 15 dated 14 May 2021 [@gentilini2021covidresponses]. The matrix records
whether eight social-assistance and social-insurance response categories were
documented. It covers 41 of the 43-economy roster; Marshall Islands and Nauru do
not appear in the parsed matrix.

The database is a real observed-response object, but it has a hard analytical
limit. A checkmark records instrument presence. It is not a comparable rate of
successful receipt, delivery speed, payment failure, inclusion error, benefit
adequacy, or shock-trigger latency. The source itself describes the records as
preliminary and requiring caution.

# Methodology

## The inherited construction

For poverty share (P_i), social-protection coverage (S_i), and account
ownership (A_i), the inherited screen computes:

\[
G_i = 100 \times P_i \left(1 - \frac{S_i + A_i}{2}\right),
\]

where percentage inputs are first expressed as proportions. When only one of
(S_i) or (A_i) exists, the committed script substitutes the available leg
for the two-leg mean and still computes (G_i).

That is a consequential design choice. A one-legged record is scored, but the
published headline later selects only records with both legs. The analysis
therefore reproduces the exact value for every economy with poverty data,
ranks those values before filtering, and labels each record as both-legs,
social-protection-only, or account-only.

## Missing-data and construct tests

Four tests follow.

1. **Value-order test.** Compare the named five with the five largest computed
   values, without adding a new completeness filter.
2. **Mean-imputation test.** Fill a missing proxy leg with the mean among
   complete records. This is a diagnostic, not a preferred estimator.
3. **Coverage-construct test.** Replace all-social-protection coverage with the
   narrower ASPIRE safety-net series and rerank. The result is interpreted only
   as sensitivity because the top rows have old and incomplete inputs.
4. **Observed-response test.** Compare the inherited gap with the count of
   response categories documented in the World Bank COVID-19 matrix. Spearman
   correlation is bootstrapped with 2,000 deterministic resamples. Response
   breadth is not relabeled readiness.

The inherited component weights were already varied by ±50 percent. That
exercise tests internal formula sensitivity. It cannot establish that the
formula measures the intended construct.

# Results

## The headline applies an unannounced completeness filter

Vanuatu's computed gap is 13.6, second in the panel, but it lacks the Findex
leg. Tajikistan's gap is 3.7, fifth in the panel, but it lacks the inherited
all-social-protection leg. Both values exceed the Philippines at 2.8 and
Bangladesh at 2.7.

![The panel's value order exposes two omitted one-legged records](/programs/social-protection-shock-coverage/generated/charts/sp-dropped-leg-ranking.svg)

Mean imputation does not restore the published membership. Vanuatu's value
falls from 13.6 to 10.4 and Tajikistan's from 3.7 to 3.3, yet both remain above
the Philippines and Bangladesh. This does not make the imputed ranking valid;
it shows that the omission cannot be defended as a harmless presentation
shortcut.

## Changing the coverage object changes the set

The current all-social-protection and narrower safety-net variants name Papua
New Guinea, Solomon Islands, Timor-Leste, the Federated States of Micronesia,
and Turkmenistan. They share no economy with the published five.

![Membership changes across value, missing-data, and coverage rules](/programs/social-protection-shock-coverage/generated/charts/sp-membership-churn.svg)

That zero overlap is a falsification of robustness, not a new result to
publish. Papua New Guinea combines 2009 poverty with 2009 safety-net coverage;
Solomon Islands combines 2012 poverty with 2005 coverage; Timor-Leste combines
2014 poverty with 2011 coverage; Micronesia uses a 2000 safety-net observation;
and Turkmenistan combines 1998 poverty with 2017 account ownership. The variant
reveals the measurement problem precisely because it is too temporally uneven
to replace the original ranking.

![The source stack combines observations from different years and policy eras](/programs/social-protection-shock-coverage/generated/charts/sp-vintage-profile.svg)

## The direct response source does not validate delivery claims

Every member of the published five has a documented cash-based transfer
response in the World Bank COVID-19 matrix. Their broader response patterns
differ, but the matrix contains no comparable receipt or timeliness outcome.

![The direct source records instrument presence rather than delivery performance](/programs/social-protection-shock-coverage/generated/charts/sp-covid-response-matrix.svg)

Across the 24 economies with both a computed gap and a documented matrix row,
the Spearman correlation between the inherited gap and eight-category response
breadth is −0.07. The 95 percent bootstrap interval runs from −0.47 to 0.36.
The named five average 4.8 documented categories; the other rankable economies
average 4.79. These values provide no empirical validation for interpreting the
gap as response breadth, and response breadth would still not be delivery
readiness if the association were strong.

![The inherited gap has no visible association with documented response breadth](/programs/social-protection-shock-coverage/generated/charts/sp-proxy-vs-response-breadth.svg)

## The composite mostly transforms the poverty input

The gap is mechanically bounded by poverty and increases with it. The readiness
legs attenuate the poverty share; they do not add a shock event or delivery
outcome. The resulting cross-section is therefore largely a transformed
poverty profile, with incomparable one-legged values mixed into the same order.

![The inherited gap closely follows the poverty component](/programs/social-protection-shock-coverage/generated/charts/sp-poverty-dominance.svg)

# Related literature and contribution

The social-protection literature provides strong reasons to study coverage,
adequacy, targeting, payment systems, and adaptive expansion. ASPIRE organizes
cross-country indicators for program scope and performance
[@worldbank2026aspire]. Findex documents financial access and the pandemic-era
expansion of digital payments [@wb2022findex]. G2Px centers responsible
digitization, payment architecture, and recipient experience
[@worldbank2026g2px]. The COVID-19 response database documents a wide expansion
of program measures across countries [@gentilini2021covidresponses].

This paper does not compete with those outcome and systems agendas by proposing
another national index. Its contribution is diagnostic: it shows how a
plausible composite can appear stable while changing its eligibility rule,
mixing vintages, and lacking the outcome necessary for its label. That is a
replicable warning for data-led policy screens: formula sensitivity is not
construct validity.

# Limitations

The COVID-19 matrix is a May 2021 snapshot. Documentation intensity differs
across economies, response categories are broad, and a checkmark says nothing
about population coverage or implementation quality. The breadth correlation
therefore tests only a weak external implication of the inherited label.

The WDI panel uses latest available observations rather than a balanced year.
ASPIRE coverage may be based on household surveys or administrative sources,
and “all social protection” pools instruments with different objectives and
adaptability. Findex is adult-level account ownership, while poverty is a
whole-population measure. Their denominators are not harmonized.

Mean imputation is intentionally simple and should not be read as a model-based
solution. The safety-net rerank is a source sensitivity test whose old vintages
make it unsuitable for current prioritization. No beneficiary microdata,
subnational shock footprint, program eligibility file, payment transaction,
agent-network availability, grievance record, or delivery timestamp is joined.

No causal claim is made. No economy's social-protection system is graded. The
result concerns the validity of this data construction.

# Conclusion and next evidence upgrade

The original country ranking is rejected. Only three of its five members
survive the panel's own value order. A reasonable missing-leg imputation keeps
the two omitted economies above the published tail. A narrower coverage proxy
changes the set completely, while its vintage pattern prevents a replacement
ranking. A direct COVID-19 response source confirms that all five named
economies deployed cash-transfer instruments but cannot say whether payments
reached intended recipients quickly or reliably.

The next study should begin from an event-level public data object, not from a
topic label. The minimum defensible table has a shock and reference date, an
eligible or affected population denominator, planned and actual recipients,
payment initiation and successful-receipt timestamps, failed or reversed
transactions, benefit amount, delivery channel, geography, and program
identifier. Only after coverage, timeliness, and failure are aligned at the
same unit should country or subnational comparisons be considered.

The construct check is reproduced by
`social-protection-shock-coverage/scripts/build-covid-response-validation.py`;
the figure dossier by `social-protection-shock-coverage/scripts/build-figure-dossier.py`.
No individual external reviewer was contacted. Computation, synthesis, and
critique are AI-first under Constitution §18; human-final review remains
outstanding.
