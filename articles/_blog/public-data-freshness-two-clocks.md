---
updated_at: 2026-07-31
slug: public-data-freshness-two-clocks-blog
title: When “three years old” tells only half the story
subtitle: A better way to show data freshness without hiding age or missingness.
kind: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB developing economies]
topics: [public data, data visualization, statistical systems]
program: public-data-freshness
maturity: PP
abstract: >
  A WDI cell's calendar age combines the production cycle of its indicator
  and its distance from that indicator's frontier.
published_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---
# Two red cells can mean different things

Imagine a dashboard marks every value older than three years in red. An
environmental indicator is red in every economy because the entire series has
a 2023 frontier. A poverty indicator is red in one economy because its latest
value is 2020 while the series reaches 2025 elsewhere.

Both observations are old. Only one trails what its indicator currently makes
possible.

![Calendar age combines a shared production cycle and an economy-specific relative lag.](/programs/public-data-freshness/generated/charts/public-data-freshness-05-two-clock-construct.svg)

That difference is large enough to change the queue. In a prospectively
frozen WDI panel covering 42 ADB developing member economies and 18 indicators,
138 of 709 observed cells change three-year review status when we switch from
calendar age to lag from the indicator frontier.

# The important caveat changed the headline

Environment creates 80 of those 138 disagreements. Health creates 40. When
environment is removed, the result falls below the study's pre-declared 10%
decision line.

![The two-clock result is concentrated in selected domains.](/programs/public-data-freshness/generated/charts/public-data-freshness-06-domain-concentration.svg)

So the lesson is not “use relative age everywhere.” The lesson is to show both
clocks where production cycles differ—and to keep the original calendar year
in view.

# Missing needs its own color

Forty-seven baseline cells have no observed value through 2025. Pacific small-
island economies have 15.7% missing cells, compared with 2.4% for the rest of
the roster. A freshness score calculated only on observed cells can hide that
coverage gap.

![Coverage differs more than the observed-cell classification across the two pre-specified groups.](/programs/public-data-freshness/generated/charts/public-data-freshness-08-pacific-group-diagnostic.svg)

A useful interface should therefore show four things: latest year, source
frontier, relative lag, and missingness. It should also show the cutoff because
the result changes sharply at two, three, and five years.

That is less tidy than one red badge. It is also much closer to the question a
reader is actually trying to answer.
