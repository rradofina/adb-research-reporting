---
slug: food-price-joint-qualifier
title: Only one in nine corrected Nepal rice-price spikes followed locally dry rainfall
subtitle: A 12-market construct validation retires both the inherited annual DMC qualifier and an earlier price-wave method; the remaining result is a coincidence screen, not climate attribution.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [Nepal]
topics: [food-price, climate, market-prices, construct-validation]
program: food-price-climate-transmission
maturity: PP
abstract: >
  This paper tests whether an inherited annual country screen can support a
  climate-to-food-price research claim and whether a public Nepal market-month
  object offers a better-aligned alternative. The annual screen intersects
  headline CPI inflation with agricultural raw-material imports; it excludes
  Nepal from its top 10 and cannot identify a commodity, event, market, or
  mechanism. The Nepal object joins WFP coarse-rice retail prices in 12 markets
  to NASA POWER monthly point rainfall for 2019–2025. Correcting the price
  outcome from distance to a full-sample calendar-month median to year-on-year
  log change reduces flagged spike cells from 259 to 152 and broad wave months
  from 25 to 10. Under the main thresholds, 17 of 152 spike cells follow
  locally dry rainfall at a one-month lag. Dry alignment remains a minority in
  all 81 ±50% threshold combinations, but wave and cluster counts are unstable.
  Annual headline CPI and median market rice-price change have a five-year
  Spearman correlation of +0.21 (exact permutation p=0.73), too little evidence
  and too much construct mismatch for validation. The result is a measurement
  audit and replication boundary: observed hazard events, multiple commodities,
  market access, and macro controls are required before estimating transmission.
doi:
published_at: 2026-04-27
updated_at: 2026-07-19
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# The finding

Among 760 Nepal market-month coarse-rice observations with a year-on-year
comparison, 152 exceed a 20% log-change threshold. Only 17 of those spike cells
also follow locally dry rainfall at the pre-specified one-month lag. The other
135 do not.

![Only 17 of 152 corrected rice-price spike cells align with locally dry rainfall](/programs/food-price-climate-transmission/generated/charts/food-price-spike-alignment.svg)

This does not show that rainfall explains 11.2% of rice-price spikes. It says
only that 11.2% satisfy two descriptive thresholds at matching markets and
months. Rainfall can affect production before prices respond; market prices can
also move through harvest cycles, transport, fuel, trade, exchange rates,
policy, expectations, and measurement. The data do not isolate those paths.

The finding changes the program in two ways. First, it retires an annual
country ranking that could not observe climate-to-price transmission. Second,
it corrects an earlier market-month transformation that treated later high
price levels as anomalies relative to a full-sample median. What remains is a
transparent falsification screen and a precise description of the next study.

# Why this question matters

Food-price shocks can erode real incomes quickly, especially where households
spend a large share of their budget on food. Climate hazards can contribute by
changing yields, disrupting transport, or affecting regional supply. But the
policy question is not whether climate and food prices can be connected in
principle. It is when, where, through which commodity and market channel, and
with what magnitude.

Those questions require aligned units. Annual headline CPI is a national basket
covering food and non-food items. A market price is a commodity-specific local
observation. Monthly point rainfall is neither a recorded disaster nor a crop
production shock. Combining these objects without preserving their differences
would produce a larger dataset but a weaker claim.

# What prior research already establishes

Baptista, Spray, and Unsal already examine Nepal using district-level WFP food
prices and recorded climate-shock events, with product, district, and time fixed
effects and local projections [@baptista2023climateshocks]. They report a 1.9%
contemporaneous price increase after recorded shocks, rising to 3.3%, with
larger and more persistent responses in remote districts. That study sets an
important precedence boundary: this paper does not claim a novel Nepal
transmission estimate.

Shively and Thapa show why market structure matters. Their Nepal analysis links
monthly food prices with rainfall, roads, and fuel prices, finding weak spatial
integration and important transport and fuel relationships
[@shively2017nepalfoodprices]. At the global level, Kotz and coauthors estimate
temperature and precipitation effects using more than 27,000 monthly consumer
price observations, fixed effects, and trends [@kotz2024climateinflation]. These
designs go beyond temporal coincidence.

FAO's Food Price Monitoring and Analysis system provides a practical precedent
for monitoring price changes and anomalies while separating alerting from
causal explanation [@fao2022fpma]. The World Bank's 2025 Nepal Development
Update also discusses food and vegetable inflation alongside import and
cross-border linkages, reinforcing that local rainfall is only one possible
driver [@worldbank2025nepaldevelopmentupdate].

The contribution here is therefore narrower but useful: test whether the
factory's inherited objects deserve their labels, identify which conclusion is
stable, and stop before the data are asked to establish more.

# Research questions

The analysis asks four falsifiable questions:

1. Does the inherited annual CPI–imports qualifier select the country in which
   the available market-month evidence can actually be studied?
2. Does the earlier calendar-month-median price transformation measure price
   change, or mainly identify later price levels?
3. After correcting the outcome, what share of rice-price spike cells follows
   locally dry rainfall under the main definition and plausible lags?
4. Which conclusions survive ±50% changes to every arbitrary threshold?

# Data

## Nepal market-month object

The market panel comes from the WFP *Nepal - Food Prices* dataset distributed
through the Humanitarian Data Exchange [@wfp2026nepalprices]. The upstream
sprint selects coarse-rice retail prices, reported in Nepalese rupees per
kilogram, for 12 markets. Price observations span 2019–2025.

For the same market coordinates, the sprint retrieves NASA POWER monthly
corrected precipitation from 2018–2025 [@nasa2026powermonthly]. Rainfall is a
point estimate in millimeters per day. It is standardized within each market
and calendar month so that “dry” means unusually dry for that market and season,
not simply a low-rainfall month in Nepal's dry season.

The original selection contains 1,008 possible market-month cells and 937 cells
with a price. Requiring a same-market price 12 months earlier leaves 760
analysis cells across 2020–2025. All 760 also join to rainfall at the main
one-month lag.

![The usable evidence narrows from a public market panel to 760 aligned change observations](/programs/food-price-climate-transmission/generated/charts/food-price-source-alignment-funnel.svg)

## Annual macro object

The inherited screen uses each ADB economy's latest World Development
Indicators headline CPI inflation and agricultural raw-material imports as a
share of merchandise imports [@worldbank2026indicatorsapi]. It identifies the
intersection of the top-N lists rather than estimating a relationship.

That imports indicator includes agricultural raw materials, not a household
food basket. The object is retained only to test whether it aligns with the
market research question. It is not used as a climate-exposure variable.

# Methods

## Correcting the price outcome

The earlier sprint defined a price anomaly as the log difference between a
market-month price and that market's 2019–2025 median for the same calendar
month. Because the median uses the full sample, a sustained upward shift in the
price level makes later years look anomalous even if the month-to-month pattern
is smooth.

The corrected outcome is 100 times the natural log of the current coarse-rice
price divided by the same market's price 12 months earlier. A spike is a value
of at least 20%. This is a year-on-year market price change—not CPI inflation
and not a welfare measure.

![Changing the price construct removes mechanically late high-price cells](/programs/food-price-climate-transmission/generated/charts/food-price-method-correction.svg)

The correction reduces price-spike cells from 259 to 152 and broad wave months
from 25 to 10. The count of dry-aligned cluster months remains two, but the
membership and meaning are evaluated under the corrected outcome.

## Rainfall alignment

The main dry threshold is a precipitation z-score at or below -1 in the prior
month. A dry-aligned price spike satisfies both that rainfall threshold and the
20% price-change threshold. The denominator is all price spikes with joined
rainfall.

The analysis also tests rainfall in the same month and at 3- and 6-month lags.
These are timing diagnostics, not distributed-lag estimates. No lag was chosen
after looking for the largest result.

## Wave classifications

A broad price wave requires at least six observed markets, price spikes in at
least half of observed markets, and dry alignment in no more than 34% of spike
markets. A dry-aligned cluster uses the same breadth requirement but exceeds
the 34% dry-share threshold. These labels help organize the timeline; because
their counts change substantially under alternative thresholds, they are not
headline estimands.

## Sensitivity and annual alignment

Every arbitrary threshold is varied by ±50%: price change at 10%, 20%, and 30%;
dryness at z≤-0.5, z≤-1, and z≤-1.5; broad-wave market share at 25%, 50%, and
75%; and the maximum dry share at 17%, 34%, and 51%. The full factorial contains
81 runs.

For context only, annual median market rice-price change is compared with
Nepal's headline CPI inflation over the five overlapping complete years,
2020–2024. Spearman and Pearson correlations are reported with an exact
two-sided permutation p-value for Spearman. Five observations cannot validate
either series as a proxy for the other.

# Results

## Most corrected spike cells do not follow local dryness

Seventeen of 152 corrected spike cells are dry-aligned at a one-month lag;
135 are not. The same-month share is 11.8%, the three-month share 5.9%, and the
six-month share 8.6%. No tested lag makes dry alignment the dominant pattern.

![Dry alignment remains a small share at every tested rainfall lag](/programs/food-price-climate-transmission/generated/charts/food-price-rain-lag-sensitivity.svg)

This is evidence against a simple story in which an unusually dry month near
each market is the common precursor to large rice-price increases. It is not
evidence against climate effects more broadly. Drought may operate over longer
growing periods or different production locations; floods, heat, and
region-wide shocks are not measured by this dryness flag.

## The visible wave is broad, but usually not locally dry

The corrected timeline identifies ten broad non-dry wave months, concentrated
between July 2023 and June 2024. In September 2023, 10 of 12 markets exceed the
20% threshold, yet none is dry-aligned. Two months meet the main dry-cluster
definition: October 2023 and May 2024.

![The 2023–2024 rice-price wave is broad across markets but rarely aligned with local dryness](/programs/food-price-climate-transmission/generated/charts/food-price-wave-timeline.svg)

This temporal clustering points toward a common or connected price process
that a stronger study should explain. It does not identify that process. The
pattern could reflect production, trade, transport, fuel, exchange-rate,
policy, or other shared conditions.

## The direction survives sensitivity; the event counts do not

Across all 81 threshold combinations, dry alignment ranges from 0% to 48.8% of
corrected spike cells. It remains a minority in every run. That directional
result is stable.

![All 81 threshold runs keep dry alignment below half of price-spike cells](/programs/food-price-climate-transmission/generated/charts/food-price-threshold-sensitivity.svg)

By contrast, broad non-dry wave counts range from 0 to 44 months and dry-cluster
counts from 0 to 27. Those classifications depend too heavily on the chosen
cutoffs to support a headline such as “ten waves” or “two climate clusters.”
They remain descriptive annotations under the main specification.

## Annual CPI and market rice prices are not interchangeable

Across 2020–2024, headline CPI inflation and the median of available market
coarse-rice year-on-year changes have Spearman correlation +0.21 and Pearson
correlation +0.20. The exact two-sided permutation p-value for Spearman is 0.73.

![Five annual observations do not validate headline CPI as a market-rice outcome](/programs/food-price-climate-transmission/generated/charts/food-price-annual-alignment.svg)

The point is not that the true association is zero. With five years, it is not
estimable with useful precision. More importantly, the series measure different
baskets and aggregation levels. Their weak visible co-movement reinforces the
decision not to carry annual CPI language into the market result.

## The inherited country screen misses the available mechanism object

The annual intersection names Lao PDR and Pakistan across every top-N threshold
from 3 to 10. Nepal ranks 12th on headline CPI inflation and 22nd on
agricultural raw-material import share, so it does not enter the top-10
intersection.

![The annual qualifier would not select Nepal despite its usable market-month evidence](/programs/food-price-climate-transmission/generated/charts/food-price-macro-market-mismatch.svg)

This is not a contradiction between countries. It is a mismatch between
research objects. The annual screen ranks macro indicators; the Nepal panel
observes one commodity in selected markets. Neither can validate the other.
The screen is therefore retired as the program's research finding.

# Interpretation and claim gates

The corrected evidence supports one positive conclusion: unusually dry local
rainfall is not the common near-term signature of large coarse-rice price
increases in this 12-market panel. It also supports a research-design decision:
the 2023–2024 broad wave deserves investigation with variables that can
distinguish common drivers.

![The data pass alignment and trend-correction gates but not attribution gates](/programs/food-price-climate-transmission/generated/charts/food-price-claim-gates.svg)

The market and rainfall units are aligned, and the price outcome is corrected
for the earlier level-trend problem. But no observed hazard-event join,
multi-commodity result, market-access controls, or causal design exists. A
climate-to-price effect estimate is therefore not permitted by the evidence.

# Limitations

Seven limits determine how the result should be read.

First, the WFP panel covers selected markets and one rice category; it is not a
national consumer basket. Second, missing prices reduce the year-on-year sample
from 937 price cells to 760 comparable cells. Third, NASA POWER rainfall is a
monthly point estimate at the market, not rainfall over the commodity's
production and sourcing area. Fourth, a z-score captures relative local
dryness but not recorded drought, flood, heat, or crop damage. Fifth, the lag
screen is descriptive and does not model growing seasons or distributed
responses. Sixth, the analysis lacks road access, fuel, trade, production,
exchange-rate, policy, and market-integration controls. Seventh, the annual
comparison has only five overlapping years and mismatched baskets.

These limits block attribution and generalization. They do not overturn the
method correction or the finding that local dryness is a minority alignment
under every threshold run.

# The next research object

The next study should start with an event-defined, multi-commodity
market-month panel rather than another country score. At minimum it needs:

1. WFP or official prices for several staples and market locations;
2. geocoded, dated drought, flood, heat, or production-shock events;
3. crop calendars and production or sourcing zones;
4. road access, remoteness, fuel, exchange-rate, trade, and policy controls;
5. a pre-specified fixed-effects, event-study, or local-projection design; and
6. explicit tests of heterogeneity by connectivity and commodity.

That object would directly extend the literature rather than reproduce a
weaker version of an existing Nepal study. A useful replication could update
the Baptista–Spray–Unsal period, test newer events and commodities, and examine
whether the remoteness gradient persists.

# Conclusion

The program began with a stable-looking annual intersection and an apparently
rich market-price wave count. Neither survived a construct check unchanged.
The annual object could not observe the proposed mechanism, and the earlier
price transformation confused high later levels with large changes.

After correction, the defensible story is smaller and more informative: 17 of
152 coarse-rice price-spike cells follow locally dry rainfall at one month, and
dry alignment remains a minority across all 81 threshold combinations. The
2023–2024 wave is real in the selected market series, but this dataset cannot
say what caused it. That boundary is the result—and the starting point for a
proper transmission study.

# Reproduce

```powershell
python research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py
python food-price-climate-transmission/scripts/build-construct-validation.py
python food-price-climate-transmission/scripts/build-figure-dossier.py
```

The first script builds the committed WFP–NASA market object. The second writes
the corrected market-month panel, annual comparison, 81-run sensitivity ledger,
and claim gates. The third regenerates every figure. Source URLs, retrieval and
version records, and method definitions are stored in the evidence JSON and
`versions.json`.

# References

Baptista, Spray, and Unsal [@baptista2023climateshocks]; Kotz et al.
[@kotz2024climateinflation]; Shively and Thapa
[@shively2017nepalfoodprices]; FAO [@fao2022fpma]; NASA POWER
[@nasa2026powermonthly]; World Food Programme [@wfp2026nepalprices]; World
Bank [@worldbank2025nepaldevelopmentupdate; @worldbank2026indicatorsapi].
