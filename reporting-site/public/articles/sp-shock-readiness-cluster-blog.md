---
updated_at: 2026-07-31
slug: sp-shock-readiness-cluster-blog
title: A stable social-protection score can still rank the wrong records
subtitle: The published top five changes when the panel's own missing-data rule is applied consistently.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [social-protection, payments, measurement]
program: social-protection-shock-coverage
maturity: PP
abstract: >
  The inherited screen looked stable under weight changes, but omitted two
  higher-valued one-legged records and had no direct delivery outcome.
references: [worldbank2026aspire, wb2022findex, gentilini2021covidresponses, worldbank2026g2px]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---
# The reassuring result was answering the wrong question

The first version of this research combined three national indicators: poverty,
coverage by any social-protection or labor program, and ownership of a financial
or mobile-money account. Bangladesh, Lao PDR, Myanmar, Pakistan, and the
Philippines were presented as a stable top-five “shock-payment-readiness gap.”

Changing the weight on the two readiness proxies by ±50 percent preserved that
set. It looked robust.

But the exercise asked only whether the same formula kept naming the same
complete records. It did not ask whether the named five were the five largest
values produced by the panel, or whether the formula measured delivery.

# Two missing legs change the membership

The script computes a gap when only one readiness leg is available. Vanuatu has
social-protection coverage but no inherited Findex value; Tajikistan has Findex
but no inherited all-SP value. Both still receive composite scores.

When all scored records are sorted, the top five are Pakistan, Vanuatu,
Myanmar, Lao PDR, and Tajikistan. Vanuatu and Tajikistan outrank the Philippines
and Bangladesh, yet disappear when the headline imposes a both-legs rule.

![The omitted one-legged records sit above the published tail](/programs/social-protection-shock-coverage/generated/charts/sp-dropped-leg-ranking.svg)

Filling each missing leg with the complete-record mean does not restore the
published membership. This is not an argument for mean imputation. It is proof
that the missing-data decision is doing substantive work.

# A narrower proxy changes the set again

ASPIRE's all-SP indicator covers social assistance, social insurance, and labor
programs [@worldbank2026aspire]. That is broader than emergency cash support.
Replacing it with the narrower safety-net series produces a completely
different five-economy set.

![The membership changes under value, imputation, and coverage rules](/programs/social-protection-shock-coverage/generated/charts/sp-membership-churn.svg)

That alternative is also not ready for publication as a ranking. Its leading
rows combine old and asynchronous poverty, coverage, and account observations.
The test exposes construct and vintage sensitivity; it does not solve them.

# A direct response source still stops short of delivery

The World Bank's May 2021 COVID-19 response database records which response
instruments countries documented [@gentilini2021covidresponses]. All five
members of the published set have a cash-based transfer checkmark.

![The source records instruments rather than successful receipt](/programs/social-protection-shock-coverage/generated/charts/sp-covid-response-matrix.svg)

That checkmark does not show that intended recipients received the payment. It
has no common receipt denominator, delivery time, failure rate, or grievance
resolution measure. The World Bank's G2Px work treats payment architecture and
recipient experience as separate issues for exactly this reason
[@worldbank2026g2px]. Findex account ownership is useful context, but it cannot
stand in for a successful government payment [@wb2022findex].

# The better result is knowing where the evidence stops

The country ranking is retired. The stronger research output is the measurement
correction:

1. internal weight sensitivity did not test the missing-data rule;
2. all-SP coverage did not isolate shock-responsive delivery;
3. account ownership did not observe payment use; and
4. the direct response database observed instruments, not last-mile outcomes.

The next study should start from a public event-level table: eligible and actual
recipients, successful and failed transactions, timestamps, benefit amount,
channel, geography, shock, and program identifier. That is slower than inventing
another index, but it is the shortest path to a result that means what its label
says.

— `attestation_chain: ai-first`; maturity PP; no individual external reviewer was contacted.
