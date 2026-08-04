---
slug: workday-loss-pressure-cluster
title: The PM2.5 employment proxy does not recover the heat-work-loss signal
subtitle: Across 21 aligned year-and-parameter tests, the proxy shares at most one of its top three economies with the Lancet Countdown measure of heat-related potential work hours lost.
kind: working-paper
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
  An inherited regional screen multiplied national PM2.5 exposure by an
  agriculture-plus-industry employment share and presented the resulting
  order as workday-loss pressure. This paper tests whether that proxy
  recovers a direct heat-labor construct. Annual World Development
  Indicators inputs are aligned with the Lancet Countdown 2025 indicator
  1.1.3 estimate of heat-related potential work hours lost for 34 economies
  in 2018, 2019, and 2020. The baseline top threes have zero overlap in all
  three years; full-rank Spearman correlations range from 0.12 to 0.17.
  Re-estimating the proxy under ±50% changes to its industry weight, PM2.5
  floor, and PM2.5 cap produces 21 year-and-parameter tests. Sixteen have
  zero top-three overlap and five have one. None has more than one. The
  result rejects the proxy as a substitute for the heat-work-loss measure;
  it does not reject a separate PM2.5-productivity pathway. The direct 2024
  heat data cover 43 of 44 economies in the analysis roster, but remain a
  model of potential capacity loss rather than observed absence or hours
  worked. The paper therefore replaces the country-ranking story with a
  construct-validation result and leaves outcome validation open.
doi:
published_at: 2026-04-26
updated_at: 2026-07-31
references:
  - lancetcountdown2025labour
  - romanello2024lancet
  - ilo2019warmerplanet
  - ilo2024heatatwork
  - somanathan2021temperature
  - he2019pollution
  - who2021aqg
  - worldbankcckp2026
  - vandonkelaar2021monthly
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# When heat cuts working hours, does a pollution proxy find the same places?

Heat and air pollution can both affect work, but through different exposure
pathways and measurement designs. A planner who sees a stable national ranking
labeled “workday-loss pressure” needs to know whether the ranking recovers a
heat-labor construct—or only the internal behavior of an air-pollution
employment score.

The inherited analysis had found that Afghanistan, India, and Bangladesh
remained in its top three when three arbitrary parameters were varied by ±50%.
That result established internal rank stability. It did not establish validity
against heat exposure, labor capacity, or observed work outcomes.

This paper asks a deliberately narrow question: can a simple national
proxy—agriculture employment plus half of industry employment, multiplied by a
PM2.5 pressure transformation—recover the cross-economy signal in a
purpose-built heat-related potential work-hours-loss measure?

# What we found

The inherited PM2.5-employment proxy does not reproduce the ordering from a
direct heat-related labor-capacity measure. Across all 21 aligned
year-and-parameter tests, the proxy shares **at most one of its top three
economies** with the Lancet Countdown 2025 indicator 1.1.3 measure. Sixteen
tests have no overlap; five have one.

In the baseline aligned 2020 comparison, the proxy's first three economies are
India, Afghanistan, and Bangladesh. The heat measure's first three are
Cambodia, Myanmar, and Thailand. The sets do not overlap, and the full-rank
Spearman correlation across 34 comparable economies is 0.17.

![The proxy and heat-related measure produce sharply different 2020 rank positions.](/programs/climate-health-workdays/generated/charts/climate-construct-rank-disagreement.png)

*Figure 1. Rank positions in aligned 2020 data. The right side is modelled
potential heat-related work hours lost per employed person, not recorded
absence. Source: World Bank WDI and Lancet Countdown 2025 indicator 1.1.3.*

The result is a measurement correction. It does not show that particulate
pollution is harmless to workers, and it does not identify an economy with
better or worse labor policy. It shows that a national PM2.5-employment product
cannot be named or interpreted as a heat-work-loss measure.

The baseline top threes have zero overlap in 2018, 2019, and 2020. Full-rank
Spearman correlations are 0.119, 0.119, and 0.169. The proxy's top three stays
India, Afghanistan, and Bangladesh. The heat top three is Cambodia, Pakistan,
and Myanmar in 2018, then Cambodia, Myanmar, and Thailand in 2019 and 2020.

The largest rank reversals clarify what the aggregate statistic means.
Afghanistan is second on the proxy in 2020 but 28th on heat-related potential
hours lost per employed person. Cambodia is 15th on the proxy and first on the
heat measure. Neither rank is a performance grade; the contrast identifies a
construct mismatch.

## ±50% changes do not restore agreement

No one-at-a-time parameter change produces more than one shared top-three
economy. Sixteen of the 21 year-and-parameter cells have zero overlap; five
have one.

![A 3 by 7 matrix shows zero or one shared top-three economy in every test.](/programs/climate-health-workdays/generated/charts/climate-construct-sensitivity.png)

*Figure 3. Top-three overlap under the baseline and ±50% changes to each
arbitrary proxy parameter. Source: committed aligned WDI and Lancet data.*

# Why the constructs diverge

The Lancet Countdown labor-capacity indicator uses wet-bulb globe temperature,
which combines temperature, humidity, solar radiation, and wind, with sector-
specific metabolic workload and employment. It estimates potential work hours
lost under heat exposure [@lancetcountdown2025labour]. The ILO likewise treats
heat stress as a physiological and occupational-safety constraint, especially
for physically demanding work and poorly cooled settings
[@ilo2019warmerplanet; @ilo2024heatatwork].

Microeconomic evidence supports the heat-productivity mechanism while also
showing why a modelled capacity estimate is not the same as an observed
outcome. Evidence from selected Indian manufacturing settings links hotter
days to lower output and greater absenteeism, with climate control moderating
some losses [@somanathan2021temperature]. Such firm-level effects depend on
work organization, technology, wages, and adaptation; they cannot be read
directly from a national exposure rank.

PM2.5 has its own labor-productivity evidence. Work in Chinese industrial towns
finds productivity effects from severe air pollution [@he2019pollution]. WHO's
air-quality guideline and satellite-derived PM2.5 surfaces remain important
for air-pollution research [@who2021aqg; @vandonkelaar2021monthly]. But this
literature does not make PM2.5 a substitute for WBGT, sector workload, or heat-
related capacity loss. Combining the pathways without an identified model
would obscure rather than clarify them.

## The direct 2024 heat profile answers two different scale questions

The 2024 per-employed-person measure is highest for Cambodia at 573 potential
hours, followed by India at 419, Pakistan at 413, Lao PDR at 410, Thailand and
Myanmar at about 408, and Bangladesh at 391. These values are annual modelled
potential hours, not days absent from work.

![Ranked bars show 2024 potential heat-related hours lost per employed person.](/programs/climate-health-workdays/generated/charts/climate-heat-loss-profile-2024.png)

*Figure 4. The direct heat-loss rate for the leading 13 covered economies in
2024. Values combine WBGT and sector workload assumptions.*

Aggregate burden produces a different ordering because workforce size enters.
India has the largest modelled total at about 247.4 billion potential hours;
China follows at about 71.6 billion and Indonesia at 35.3 billion. Cambodia's
rate is highest, while its total is about 5.6 billion. Rate and total should
not be collapsed into one priority score.

![A bubble plot separates heat-loss rate from aggregate potential hours.](/programs/climate-health-workdays/generated/charts/climate-heat-loss-rate-vs-scale.png)

*Figure 5. Potential hours per employed person versus total potential hours,
2024. Bubble area represents the Lancet modelled outdoor-worker count. The
vertical axis is logarithmic.*

Agriculture and construction account for 76%–96% of modelled potential heat-
loss hours among the ten highest per-worker rows. The Lancet method distinguishes
sector workload and sun exposure. The inherited proxy instead combines all
agriculture with a half-weighted industry share and then scales by PM2.5.

![Stacked bars show the sector composition of potential heat-loss hours.](/programs/climate-health-workdays/generated/charts/climate-heat-loss-sector-composition.png)

*Figure 6. Sector shares of 2024 modelled potential hours for the ten highest
per-employed-person rows. National sector shares are applied within grids.*

The inherited screen multiplied a labor-sector share by total population when
producing an exposed-worker count. Relative to the Lancet modelled outdoor-
worker count, this makes the Afghanistan count 5.09 times as large, India's
2.72 times, and Bangladesh's 2.61 times. Replacing total population with WDI
employed people aged 15+ brings the three ratios to 0.94, 1.09, and 1.06.

![Bars compare the old and repaired worker denominators with the Lancet modelled count.](/programs/climate-health-workdays/generated/charts/climate-worker-denominator-repair.png)

*Figure 7. Calculated outdoor-worker count divided by the Lancet modelled
count. The comparison source is itself modelled, not a census benchmark.*

# What this means for climate-labor work

Three lessons follow.

First, internal sensitivity is necessary but not sufficient. A stable ranking
shows that a result is not driven by small changes to selected parameters. It
does not show that the metric represents the intended concept. The negative
result is stronger than the inherited internal-stability result: the proxy can
keep naming the same economies and still fail to recover the external construct
it was implicitly asked to represent.

Second, heat and PM2.5 should remain separate evidence objects. A heat-capacity
model should be used for potential heat-related labor loss. A PM2.5 analysis
should state its air-pollution pathway and use exposure and outcome data suited
to that question. Adding the two into a new composite would not repair the
identification problem.

Third, rate and scale support different planning uses. Per-worker estimates can
identify where heat exposure is intense relative to the employed population;
total potential hours can indicate the aggregate scale of modelled capacity at
risk. Neither alone identifies adaptation effectiveness, welfare loss, or the
value of a specific intervention.

The old top-three pressure-cluster headline is retired. Its stability described
the behavior of a PM2.5-employment score, not agreement with heat-related labor
capacity. Once the score is tested against a documented direct construct, the
leading sets separate and the full-rank associations remain weak.

# What this does not say

The Lancet Countdown measure is a model, not an observed labor outcome. It
uses gridded weather and population, national employment shares applied across
grid cells, sector-specific workload assumptions, and a potential-capacity
relationship. It omits informal unpaid work and does not observe individual
work schedules, rest breaks, cooling, acclimatization, wages, output, or days
actually absent.

The construct comparison is limited to 2018–2020 because those are the annual
WDI years common to all proxy inputs and the heat series. It evaluates rank
agreement, not level agreement or causal prediction. National averages conceal
subnational exposure differences. The World Bank Climate Change Knowledge
Portal offers more granular heat variables [@worldbankcckp2026], but a valid
subnational study would also need aligned employment, workload, adaptation, and
outcome data.

The ±50% tests vary one proxy parameter at a time. They do not exhaust all
possible functional forms. That is acceptable for the present decision: even
the inherited function's plausible perturbations fail to recover the direct
heat construct.

In 2024, the heat-loss workbook covers 43 of 44 economies in the analysis
roster; Taipei,China is absent. The outdoor-worker workbook covers 42;
Hong Kong, China and Taipei,China are absent. The roster is an analysis panel,
not an authoritative current list of all ADB developing members. The values
remain a model of potential capacity loss rather than observed absence or hours
worked.

![Coverage expands with the heat source, while observed outcome validation remains open.](/programs/climate-health-workdays/generated/charts/climate-source-coverage.png)

*Figure 2. Source coverage in the 44-economy analysis roster. Zero observed
outcomes means none is joined in this package; it does not mean no economy
publishes labor outcomes.*

Finally, the Lancet workbooks are distributed under CC BY-NC-SA 4.0. This
repository records the retrieval date, source URLs, file hashes, and license;
reuse must preserve the source terms.

# What would change this finding

The next evidence step is not another proxy refinement. It is a pre-specified
join to observed absenteeism, hours worked, output, or labor-supply data for a
small set of economies with compatible subnational heat exposure and workplace
information. Until that object exists, the proxy should not be renamed or
interpreted as heat-related work-hour loss.

# How we measured this

The inherited screen uses annual World Development Indicators: agriculture
employment as a share of total employment, industry employment as a share of
total employment, and national annual mean PM2.5 exposure. For aligned annual
testing, the three series must be present for the same economy and year.
Thirty-four economies meet that condition in each of 2018, 2019, and 2020.

The Lancet Countdown 2025 country workbook provides annual estimates from
1990 through 2024. This paper uses four sector components—services,
manufacturing, agriculture in sun, and construction in sun—and the published
total potential work-hours-loss rate per employed person. The companion
workbook provides modelled outdoor-worker counts from 2000 through 2024
[@lancetcountdown2025labour]. The workbook stores sector totals in thousands of
hours; the pipeline converts them to hours before aggregation.

## 1. Reconstruct the inherited proxy

For economy *i* in year *t*:

`outdoor employment share = agriculture share + w × industry share`

`PM2.5 pressure = clamp((PM2.5 − floor) ÷ cap, 0, 1)`

`proxy = outdoor employment share × PM2.5 pressure`

The baseline uses an industry weight of 0.5, PM2.5 floor of 5 µg/m³,
and PM2.5 cap of 45 µg/m³. The resulting number is a triage score only.

## 2. Align years and economies

The construct test retains only economy-year rows observed in all three WDI
inputs and the Lancet heat series. The common window is 2018–2020, with 34
economies in every year.

## 3. Compare ranks and leading sets

Within each year, both measures are ranked from highest to lowest. The primary
comparison is overlap between their top-three sets. A secondary diagnostic is
the Spearman rank correlation across all 34 rows.

The decision rule is intentionally demanding: if any aligned test produces
top-three overlap above one economy, the headline must be weakened. If the
baseline top threes are usually disjoint and no sensitivity run exceeds one,
the proxy is rejected as a substitute for the heat construct.

## 4. Test the arbitrary proxy choices

Each of the proxy's three numeric choices is varied independently by ±50%:

| Choice | Baseline | −50% | +50% |
|---|---:|---:|---:|
| Industry weight | 0.50 | 0.25 | 0.75 |
| PM2.5 floor, µg/m³ | 5.0 | 2.5 | 7.5 |
| PM2.5 cap, µg/m³ | 45.0 | 22.5 | 67.5 |

Together with the baseline, seven specifications are applied to each of three
years, producing 21 tests.

```powershell
python climate-health-workdays/scripts/process-climate-health.py
python climate-health-workdays/scripts/deepen-cap-and-laborforce.py
python climate-health-workdays/scripts/build-heat-workloss-evidence.py
python climate-health-workdays/scripts/build-figure-dossier.py
python climate-health-workdays/scripts/build-thumbnail.py
```

The final three commands rebuild the construct-validation evidence and figure
dossier from the recorded public sources. Full cache, unit, and expected-output
instructions are in `climate-health-workdays/REPRODUCE.md`.

Permanent evidence route:
[/program/climate-health-workdays/evidence](/program/climate-health-workdays/evidence).

— Raymond Adofina · 2026-07-18 · `attestation_chain: ai-first`
