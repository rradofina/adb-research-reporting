---
slug: emigrant-stock-corridor-concentration
title: The top five migrant origins have zero overlap after population normalization
subtitle: Absolute emigrant stock measures diaspora scale; dividing the same stock by resident population moves Samoa and Tonga to the top and exposes Afghanistan as a forced-displacement exception.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [IND, CHN, BGD, AFG, PHL, WSM, TON, ARM, NRU, FJI]
topics: [migration, migrant-stock, population-denominator, forced-displacement]
program: migration-displacement-signals
maturity: PP
abstract: >
  Rankings of international migrant origins often lead with absolute
  emigrant stock. This paper tests whether that ordering can be interpreted
  as migration intensity in a 44-economy program panel. UN DESA
  International Migrant Stock 2024 is ranked first as an absolute count and
  then divided by World Bank WDI 2024 resident population. The absolute top
  five—India, China, Bangladesh, Afghanistan, and the Philippines—has zero
  overlap with the population-share top five—Samoa, Tonga, Armenia, Nauru,
  and Fiji. India moves from absolute rank 1 to share rank 36; China moves
  from rank 2 to 39. Samoa and Tonga exceed 50% on the stock-to-resident-
  population measure. The result survives top-N choices of 3, 5, and 8 and
  material-overlap thresholds of 25%, 50%, and 75%. A 44-origin UNHCR
  crosswalk then tests whether the share leaders are forced-displacement
  cases. None is forced-displacement-majority. Afghanistan is the near-rank
  exception at share rank 6, but UNHCR forced-displacement stock equals
  81.7% of its UN DESA emigrant stock. The paper therefore retires the
  absolute-stock intensity headline. It treats absolute scale,
  population-normalized stock, and forced displacement as distinct evidence
  objects and does not infer current flows, migration propensity, labor-
  migration purpose, welfare, or causal drivers.
doi:
published_at: 2026-04-26
updated_at: 2026-07-18
references:
  - undesa2024migrant
  - undesa2024sustainablemigration
  - worldbank2024population
  - unhcr2024methodology
  - ozden2011where
  - dehaas2021aspirations
  - clemens2011economics
  - adb2018pacificlabour
  - anu2023palm
  - idmc2024grid
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The measurement question

International migration statistics invite a simple ranking: count how many
people from each origin live abroad, then sort from largest to smallest. The
result is easy to communicate. It is also easy to overinterpret.

UN DESA origin stock measures a cumulative population abroad. Large origins
can have large diaspora counts even when that stock is small relative to the
population still resident at origin. Small economies can show the opposite
pattern. A ranking that does not name its denominator can therefore answer a
different policy question from the one readers assume.

The inherited version of this paper led with five large absolute origin
stocks: India, China, Bangladesh, Afghanistan, and the Philippines. It showed
that the set remained stable when the same stock was compared with a net-
stock ordering. That test changed the direction convention but did not test
population scale.

This paper asks a sharper question: **how much does the identity of the
leading origins change when UN DESA 2024 emigrant stock is divided by WDI
2024 resident population, and does UNHCR forced-displacement evidence change
the interpretation of the population-share leaders?**

# Why the denominator matters

UN DESA describes origin migrant stock as people from an origin who reside
abroad, sometimes referred to as a diaspora or transnational population
[@undesa2024sustainablemigration]. The measure is a stock at a reference date,
not the number who left during that year. Bilateral stock matrices combine
census, register, and other national evidence whose definitions and coverage
require harmonization [@ozden2011where].

Dividing the stock by resident population does not convert it into a flow. It
changes the comparison from **diaspora size** to **cumulative stock abroad
relative to the origin population**. That is useful, but still narrower than
migration propensity. Migration depends on the aspiration and capability to
move, policy, resources, networks, and forced circumstances
[@dehaas2021aspirations]. A high or low share is not a welfare judgment.

The distinction is operationally important in the Pacific. Small labor
markets, high skilled-emigration rates, formal labor pathways, circulation,
and older diaspora networks can all contribute to large stocks relative to
resident populations [@adb2018pacificlabour; @anu2023palm]. Those mechanisms
cannot be separated by the stock alone.

# Data and coverage

The analysis uses three public sources.

1. **UN DESA International Migrant Stock 2024.** The origin-destination matrix
   supplies the numerator and destination corridors [@undesa2024migrant].
2. **World Bank WDI `SP.POP.TOTL`.** The fixed 2024 query supplies the mid-year
   de facto resident-population denominator [@worldbank2024population].
3. **UNHCR Refugee Data Finder 2024.** Origin-asylum rows identify refugees,
   asylum-seekers, and other people in need of international protection
   abroad [@unhcr2024methodology].

The committed program panel contains 44 economies. UN DESA stock is present
for all 44. WDI provides a 2024 denominator for 41. Taipei,China, Cook Islands,
and Niue are withheld from the population-share ranking because no value is
reported in the fixed WDI query. The UNHCR pipeline queries all 44 origins and
finds at least one positive forced-abroad row for 41.

These counts describe an analysis roster, not an authoritative current list
of every ADB developing member. They also describe different source functions:
a missing positive UNHCR row is not equivalent to a missing WDI denominator.

# Method

The method has four sequential steps.

## 1. Rank absolute origin stock

For each program economy, sum UN DESA 2024 destination rows by origin. Sort
the resulting emigrant stock from largest to smallest.

## 2. Add the resident-population denominator

Join the origin code to WDI `SP.POP.TOTL` for 2024 and calculate:

`emigrant stock ÷ resident population × 100`.

Rows without a denominator are withheld. The analysis then ranks the 41
valid rows by this percentage.

## 3. Compare the leading sets

At the baseline top-N of five, calculate the intersection count and divide by
five. Reshape the absolute-stock headline when overlap is at most 50%. Test
top-N at 3, 5, and 8 and the material-overlap threshold at 25%, 50%, and 75%.

## 4. Test the forced-displacement component

For each origin, sum UNHCR refugees, asylum-seekers, and other people in need
of international protection located outside the origin. Divide that sum by
UN DESA emigrant stock. IDPs are excluded because they remain inside the
origin economy. The forced-displacement-majority rule is 50%, tested at 25%
and 75%.

The residual is labeled other or unclassified migrant stock. It is not
labeled labor migration.

# Result 1: the top five is replaced completely

The absolute top five is India, China, Bangladesh, Afghanistan, and the
Philippines. The population-share top five is Samoa, Tonga, Armenia, Nauru,
and Fiji. The intersection is empty.

![Rank inversion between absolute stock and stock divided by population](/programs/migration-displacement-signals/generated/charts/migration-rank-inversion.png)

*Figure 1. Rank positions for the union of the absolute and population-share
top fives. Source: UN DESA International Migrant Stock 2024 and World Bank
WDI 2024 population. Three rows without a WDI denominator are withheld.
Stock is cumulative, not an annual flow.*

India's 18.5 million origin stock is 1.28% of resident population and moves
from absolute rank 1 to share rank 36. China's 11.7 million is 0.83% and moves
from rank 2 to 39. Bangladesh moves from 3 to 25, and the Philippines from 5
to 23. Afghanistan moves from 4 to 6 and becomes the near-rank exception.

This does not mean the absolute counts are wrong. They answer a scale
question. It means they cannot carry an intensity interpretation without a
denominator.

# Result 2: the population-share leaders are small and medium economies

Samoa's 119,313 people in the origin stock equal 54.73% of its resident
population. Tonga's 53,237 equal 51.10%. Armenia, Nauru, and Fiji follow at
21.02%, 20.79%, and 19.49%.

![Top twelve migrant-stock shares of resident population](/programs/migration-displacement-signals/generated/charts/migration-population-share-profile.png)

*Figure 2. UN DESA origin stock divided by WDI mid-year population, 2024. The
bars describe cumulative stock relative to the population at origin; they do
not estimate departures in 2024.*

The Pacific rows require careful interpretation. The numerator can include
older diaspora waves, family mobility, labor schemes, study, and other
movements. The stock cannot reveal which mechanism dominates or whether the
corridor is currently growing.

# Result 3: corridor concentration is descriptive, not decisive

The original paper also compared the share of each large absolute origin's
stock in its top destinations. At top three, India records 45.2%, China 49.5%,
Bangladesh 65.3%, Afghanistan 80.2%, and the Philippines 55.2%.

![Corridor concentration across top two, three, and five destinations](/programs/migration-displacement-signals/generated/charts/migration-corridor-concentration.png)

*Figure 3. Share of UN DESA origin stock in the top two, three, or five
destinations. The 50% line is heuristic; the corridors combine migration
purposes and historical periods.*

Every origin clears a 25% threshold, three clear 50%, and only Afghanistan
clears 75%. The count also rises materially when five rather than three
destinations are included. Corridor concentration remains useful context, but
its classification is too choice-sensitive to carry the paper.

# Result 4: Afghanistan is a different mobility object

The UNHCR crosswalk shows why Afghanistan cannot be read like the population-
share leaders. Its selected international forced-displacement stock is
6,151,318, equal to 81.7% of the UN DESA emigrant stock. Iran and Pakistan
are the two largest forced-displacement destinations in the public crosswalk.

None of the population-share top five is forced-displacement-majority. Their
UNHCR components range from 0.4% for Samoa to 5.7% for Armenia.

![Forced-displacement composition for Afghanistan and the population-share top five](/programs/migration-displacement-signals/generated/charts/migration-forced-displacement-composition.png)

*Figure 4. UNHCR refugees, asylum-seekers, and other people in need of
international protection abroad as a share of UN DESA origin stock. The
residual is other or unclassified stock, not a labor-migration estimate.*

Afghanistan remains above the majority rule at 25%, 50%, and 75%. Every
population-share top-five economy remains below 25%. The construct exception
therefore survives the required threshold sensitivity.

# Source observability

The result is only as strong as the joined source layers. UN DESA supplies
the common stock object. WDI supplies the denominator for 41 rows. UNHCR
identifies one part of migration purpose but cannot classify the residual.

![Coverage of the three joined migration evidence layers](/programs/migration-displacement-signals/generated/charts/migration-source-observability.png)

*Figure 5. Source observability across the 44-economy program panel. Missing
population denominators and the limits of forced-displacement classification
remain visible.*

The chart is not a generic data inventory. It explains why the paper can make
a denominator and forced-displacement claim but cannot make a flow or labor-
migration claim.

# Robustness

The denominator result is stable across the required arbitrary choices:

| Top-N | Shared members | Overlap |
|---:|---:|---:|
| 3 | 0 | 0.0% |
| 5 | 0 | 0.0% |
| 8 | 1 | 12.5% |

Every run satisfies the material-change decision at 25%, 50%, and 75%.
Afghanistan remains above every forced-displacement threshold, while no
population-share top-five economy reaches even 25%.

The analysis does not test vintage stability. Repeating the comparison for
UN DESA 2015 and 2020 would answer a separate temporal question and should be
pre-specified before the next issue.

# What the finding means

The evidence supports three different operational readings.

- Use **absolute stock** when the decision concerns the scale of diaspora
  systems or the number of people connected to bilateral origin-destination
  relationships.
- Use **stock relative to resident population** when the decision concerns
  how large cumulative mobility is relative to the origin economy's current
  population.
- Add **migration-purpose evidence** before describing a row as labor,
  family, student, temporary, or forced movement.

These readings can guide source selection, country diagnostics, and the design
of a future flow study. They do not establish which economy has too much or
too little migration.

# What the finding does not mean

The paper does not estimate current migration flow, an individual's migration
probability, welfare effects, brain drain, remittance benefits, climate-
related migration, internal displacement, or causal drivers. High stock
shares can coexist with very different policies and development outcomes.
Migration can also create substantial gains for migrants and origin and
destination economies [@clemens2011economics].

The population-share ranking is incomplete because three program economies
lack WDI denominators. Cook Islands and Niue could plausibly enter the upper
tail if authoritative denominators were added. That uncertainty does not
restore the absolute top five, but it prevents treating the observed share
ordering as a complete regional league table.

# Conclusion

The inherited absolute-stock intensity story is falsified. The same public
stock object produces a disjoint leading set when population enters the
denominator. The strongest interpretation is not that one ranking is right
and the other wrong, but that they answer different questions and should not
share a headline.

The UNHCR crosswalk adds the second necessary distinction. Afghanistan is
close to the population-share leaders, but its stock is predominantly a
forced-displacement object. Samoa, Tonga, Armenia, Nauru, and Fiji are not.
Even then, the remaining stock cannot be called labor migration.

This issue therefore stops at a defensible measurement correction: name the
denominator, separate forced displacement where the source permits, expose
missing rows, and reserve current-flow or migration-purpose claims for a new
public data object.

# Reproduce the analysis

```powershell
python migration-displacement-signals/scripts/deepen-per-population.py
python migration-displacement-signals/scripts/audit-corridor-type-forced-displacement.py
python migration-displacement-signals/scripts/sensitivity.py
python migration-displacement-signals/scripts/build-figure-dossier.py
python migration-displacement-signals/scripts/build-thumbnail.py
```

The figure-only rebuild uses committed JSON and requires no network call.
Full source and cache instructions are in
`migration-displacement-signals/REPRODUCE.md`.

Permanent evidence route:
[/program/migration-displacement-signals/evidence](/program/migration-displacement-signals/evidence).

— Raymond Adofina · 2026-07-18 · `attestation_chain: ai-first`
