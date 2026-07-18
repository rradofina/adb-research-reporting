---
slug: school-heat-honest-narrowing-blog
title: A heat proxy is not a school-disruption result
subtitle: Cambodia led the formula, but the first direct outcome check reverses the story.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [education, heat, school-disruption, construct-validation]
program: school-heat-disruption
maturity: PP
abstract: >
  The inherited formula looked robust until its saved sensitivity runs and an
  observed school-disruption source were read together.
references: [unicef2025learninginterrupted, worldbank2024choosingfuture, park2020heat, wargocki2019classroom]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# The headline was stronger than the evidence

An inherited school-heat index ranked Cambodia first by combining the number
of children, primary pupil-teacher ratio, and historical annual maximum
temperature. The public story said Cambodia stayed first under every ±50%
parameter change.

The saved files say otherwise. Cambodia leads five of six discriminating runs.
Pakistan leads when the temperature floor is cut in half. A seventh run gives
every economy a zero and therefore cannot distinguish a leader.

![One sensitivity run changes the leader and one cannot rank anything](/programs/school-heat-disruption/generated/charts/school-sensitivity-run-verdicts.svg)

That correction matters, but it is still only an internal formula test. The
harder question is whether the index orders anything observed in schools.

# A direct source changes the story

UNICEF's 2024 climate-related school-disruption annex lists affected students
and the hazard associated with each country's largest reported disruption
[@unicef2025learninginterrupted]. Twenty-one rows match the ADB roster. Six name
heatwave as the major hazard: Afghanistan, Bangladesh, Cambodia, India,
Pakistan, and the Philippines.

India has the largest affected-student count in that subset. Cambodia has the
smallest. The country that ranked first in the proxy ranks sixth by the direct
count.

![The observed count order does not reproduce the proxy order](/programs/school-heat-disruption/generated/charts/school-heatwave-affected-ranking.svg)

The rank correlation between the proxy and affected counts is +0.03. Child
population alone correlates +0.94. With only six selected observations, neither
number should be treated as a general law. But the comparison gives no support
for narrating the composite as school disruption.

# Thresholds hid an obvious failure case

Afghanistan's historical annual maximum temperature is below the index's 25°C
floor, so its baseline heat score is zero. UNICEF reports 10.914 million
affected students and identifies heatwave as the major 2024 disruption hazard.
Historical national climatology is not school-day exposure.

Research on heat and learning points toward local, time-aligned exposure and
educational outcomes [@park2020heat; @wargocki2019classroom]. It does not
validate the inherited threshold or its linear response.

# The direct count has limits too

UNICEF's annex is selected by public reporting. Missing countries are unknown,
not zero. Counts can be observed or enrollment-estimated. The listed hazard is
the largest disruption, not every event. Counts do not tell us how many school
days were lost or whether learning declined.

Those limits prevent a new country ranking. They do not justify retaining the
old one.

# Build the school-day object next

The successor study needs four aligned layers: daily local heat; the school
calendar; enrolled students and school conditions; and an observed closure,
attendance, assessment, or learning outcome. Until that object exists, the
country score is best treated as a transparent sampling frame—not a finding
about educational disruption.

— `attestation_chain: ai-first`; maturity PP; no individual external reviewer was contacted.
