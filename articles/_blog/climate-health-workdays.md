---
updated_at: 2026-07-31
slug: climate-health-workdays-blog
title: A stable climate-health proxy can still measure the wrong thing
subtitle: Direct heat-labor data overturn the inherited PM2.5 workday-loss ranking.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [KHM, IND, PAK, MMR, THA, AFG, BGD]
topics: [climate-health, labor-capacity, heat, PM2.5, measurement]
program: climate-health-workdays
maturity: PP
abstract: >
  A PM2.5 × employment proxy kept the same leading economies under parameter
  changes, but failed an external test against the Lancet Countdown heat-
  related potential work-hours-loss measure. The episode shows why internal
  sensitivity cannot substitute for construct validation.
references: [lancetcountdown2025labour, ilo2019warmerplanet, ilo2024heatatwork, somanathan2021temperature, he2019pollution]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---
# Stability is not validity

The first version of this research looked reassuring. A simple score combined
national PM2.5 exposure with agriculture and industry employment. Afghanistan,
India, and Bangladesh stayed near the top when the score's arbitrary parameters
were changed by ±50%.

That was a valid internal check. It answered: *does this formula keep producing
the same leading set when its settings move?* It did not answer: *does the
formula measure heat-related work loss?*

The distinction matters because the score had no temperature, humidity, solar
radiation, workload, observed hours, or absence. Its label had outrun its data.

# A direct data object changes the story

The Lancet Countdown 2025 indicator 1.1.3 estimates potential work hours lost
from heat using wet-bulb globe temperature, employment, population, sun
exposure, and sector workload [@lancetcountdown2025labour]. It is not a perfect
outcome measure—it is a model of potential capacity—but it is a direct heat-
labor construct.

The research aligned that measure with the annual WDI inputs used by the proxy.
Thirty-four economies are comparable in 2018, 2019, and 2020.

![Rank lines show the proxy and heat measure placing the same economies in very different positions.](/programs/climate-health-workdays/generated/charts/climate-construct-rank-disagreement.svg)

In 2020, India, Afghanistan, and Bangladesh form the proxy's top three.
Cambodia, Myanmar, and Thailand form the heat measure's top three. The sets
have zero overlap. Afghanistan moves from second to 28th; Cambodia moves from
15th to first. The full-rank correlation is only 0.17.

The same baseline pattern appears in 2018 and 2019.

# Tuning the proxy does not repair it

The industry weight, PM2.5 floor, and PM2.5 cap were each varied by ±50%.
Together with the baseline, that creates seven specifications in each of three
years—21 tests.

![The sensitivity matrix contains only zero- and one-overlap cells.](/programs/climate-health-workdays/generated/charts/climate-construct-sensitivity.svg)

Sixteen tests share none of the heat top three. Five share one. No setting
recovers two or three.

The lesson is not that sensitivity analysis failed. It did its job. It showed
that the formula was internally stable. The external test then showed that the
stable formula represented a different construct.

# Heat and pollution should stay separate

Heat and PM2.5 can both affect workers. Evidence from selected Indian
manufacturing settings links hotter days to lower productivity and higher
absence [@somanathan2021temperature]. Research in Chinese industrial towns
supports a separate air-pollution-productivity pathway [@he2019pollution].

Those findings do not justify folding the exposures into one score. A direct
heat question should use a heat measure. A pollution question should use
pollution exposure and an appropriate outcome. A joint question needs a design
that identifies both pathways.

# The direct heat profile still requires restraint

The 2024 Lancet workbook covers 43 of the 44 economies in the analysis roster.
Cambodia has the highest estimate per employed person, at about 573 potential
hours. India has the largest aggregate estimate, about 247.4 billion potential
hours.

![The rate profile shows high potential hours per employed person in several economies.](/programs/climate-health-workdays/generated/charts/climate-heat-loss-profile-2024.svg)

![The rate-versus-scale chart separates Cambodia's high rate from India's aggregate burden.](/programs/climate-health-workdays/generated/charts/climate-heat-loss-rate-vs-scale.svg)

These are not recorded days off work. The model applies national sector shares
within grids and does not observe individual schedules, cooling, shade, rest,
or informal unpaid work. The ILO literature makes those workplace conditions
central to heat risk and response [@ilo2019warmerplanet; @ilo2024heatatwork].

# Better research begins by retiring the wrong headline

The old pressure-cluster ranking is no longer the output. The stronger result
is the measurement correction:

1. internal stability does not establish construct validity;
2. heat and PM2.5 are separate pathways;
3. an employment share must not be multiplied by total population and called
   workers; and
4. potential capacity loss must not be reported as observed absence.

The next study needs a new data object: observed absenteeism, hours, output, or
labor supply joined to compatible heat exposure at the same place and time.
Until then, the honest research contribution is knowing what the current data
can—and cannot—carry.

— `attestation_chain: ai-first`; maturity PP; no named external reviewer was contacted.
