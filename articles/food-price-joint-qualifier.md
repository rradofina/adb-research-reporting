---
slug: food-price-joint-qualifier
title: Only one in nine Nepal rice-price spikes followed locally dry rainfall
subtitle: In 12 Nepali markets over 2020–2025, only 17 of 152 large coarse-rice price jumps followed an unusually dry month. Whatever drove the 2023–24 price wave, local dryness was not the common trigger — and this dataset cannot yet say what was.
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
updated_at: 2026-07-31
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# When rice prices jump, was it the weather?

A food-price spike erodes real incomes fastest where households spend
the largest share of their budget on food. Climate hazards are an
intuitive suspect — dry months can cut yields, disrupt transport, and
tighten regional supply. But the question that matters for policy is
not whether climate and food prices *can* be connected in principle.
It is when, where, through which commodity and market, and by how
much.

Answering that requires objects that line up. Annual headline CPI is a
national basket of food and non-food items. A market price is one
commodity in one town. Monthly point rainfall is neither a recorded
disaster nor a crop shock. This paper checks, for Nepal's coarse-rice
markets, whether the simplest climate story — a locally dry month
precedes a price spike — actually shows up in the public data.

# What we found

Mostly, it does not. Among 760 Nepal market-month coarse-rice
observations with a year-on-year comparison, 152 exceed a 20 percent
price-jump threshold. Only **17 of those 152** — about one in nine —
also follow unusually dry local rainfall in the previous month. The
other 135 do not.

![Only 17 of 152 corrected rice-price spike cells align with locally dry rainfall](/programs/food-price-climate-transmission/generated/charts/food-price-spike-alignment.svg)

Timing choices do not rescue the story. The same-month dry share is
11.8 percent, the three-month share 5.9 percent, and the six-month
share 8.6 percent — at no tested lag does dryness become the dominant
precursor.

![Dry alignment remains a small share at every tested rainfall lag](/programs/food-price-climate-transmission/generated/charts/food-price-rain-lag-sensitivity.svg)

Read this carefully: it does not show that rainfall "explains 11.2
percent" of rice-price spikes. It says only that 11.2 percent of
spikes satisfy two descriptive thresholds at matching markets and
months. Prices also move through harvest cycles, transport, fuel,
trade, exchange rates, policy, and expectations — and drought can act
over longer growing periods or in production areas far from the
market. The data do not isolate any of those paths. What the result
rules out is one specific, simple story: that a locally dry month is
the common near-term signature of a Nepali rice-price spike.

# What earlier studies already show

This is deliberately not a new transmission estimate, because a better
one exists. Baptista, Spray, and Unsal [@baptista2023climateshocks]
study Nepal with district-level WFP prices, *recorded* climate-shock
events, and fixed-effects local projections, finding a 1.9 percent
contemporaneous price increase after shocks, rising to 3.3 percent,
larger and more persistent in remote districts. Shively and Thapa
[@shively2017nepalfoodprices] show why market structure matters,
linking Nepali food prices to rainfall, roads, and fuel with weak
spatial integration. Globally, Kotz and coauthors
[@kotz2024climateinflation] estimate climate effects on consumer
prices from more than 27,000 monthly observations.

FAO's price-monitoring system [@fao2022fpma] sets the practical
precedent this paper follows: separate *alerting* on price anomalies
from *explaining* them. The World Bank's 2025 Nepal Development Update
[@worldbank2025nepaldevelopmentupdate] likewise reads food inflation
alongside import and cross-border linkages — local rainfall is one
candidate driver among many. The contribution here is narrower: test
whether the factory's inherited measurement objects deserve their
labels, report what is stable, and stop before the data are asked to
establish more.

# What we measured

The market panel is the WFP *Nepal - Food Prices* dataset
[@wfp2026nepalprices]: coarse-rice retail prices, rupees per kilogram,
in 12 markets, 2019–2025. For each market's coordinates, NASA POWER
monthly precipitation [@nasa2026powermonthly] is standardized within
market and calendar month, so "dry" means unusually dry *for that
market and season* — not just any dry-season month.

The panel offers 1,008 possible market-month cells, 937 with a price;
requiring a same-market price 12 months earlier leaves 760 analysis
cells across 2020–2025, all of which join to rainfall.

![The usable evidence narrows from a public market panel to 760 aligned change observations](/programs/food-price-climate-transmission/generated/charts/food-price-source-alignment-funnel.svg)

One measurement correction changed everything downstream. The earlier
sprint had defined a price anomaly as distance from the market's
full-sample calendar-month median — which mechanically flags later
years as anomalous whenever the price *level* has shifted up, even if
month-to-month changes are smooth. The corrected outcome is the
year-on-year log change, with a spike at 20 percent or more. That one
fix cuts flagged spike cells from 259 to 152 and broad wave months
from 25 to 10.

![Changing the price construct removes mechanically late high-price cells](/programs/food-price-climate-transmission/generated/charts/food-price-method-correction.svg)

# The 2023–24 wave was broad — but rarely dry

The corrected timeline shows ten broad wave months, concentrated
between July 2023 and June 2024. In September 2023, 10 of 12 markets
exceed the 20 percent threshold — and not one of them follows a dry
month. Only two months in the whole panel meet the dry-cluster
definition: October 2023 and May 2024.

![The 2023–2024 rice-price wave is broad across markets but rarely aligned with local dryness](/programs/food-price-climate-transmission/generated/charts/food-price-wave-timeline.svg)

A wave that hits ten of twelve markets at once points to a common or
connected price process — production, trade, transport, fuel,
exchange-rate, or policy conditions shared across markets. This
dataset can see that the wave happened; it cannot say what caused it.
That is the question the next study should be built to answer.

# What survives scrutiny — and what doesn't

Every arbitrary threshold was varied by ±50 percent: the price-spike
cutoff (10/20/30 percent), the dryness cutoff (z ≤ −0.5/−1/−1.5), and
both wave-definition shares — 81 runs in all. Dry alignment ranges
from 0 to 48.8 percent of spike cells and **stays a minority in every
single run**. That directional conclusion is stable.

![All 81 threshold runs keep dry alignment below half of price-spike cells](/programs/food-price-climate-transmission/generated/charts/food-price-threshold-sensitivity.svg)

The event counts are not. Broad-wave counts range from 0 to 44 months
and dry-cluster counts from 0 to 27 depending on cutoffs — far too
unstable to support a headline like "ten waves" or "two climate
clusters." They stay descriptive annotations, nothing more.

# Two inherited shortcuts, retired

The audit also killed two measurement conveniences the program had
inherited.

**Annual CPI is not a stand-in for market rice prices.** Over the five
overlapping years 2020–2024, headline CPI inflation and the median
market rice-price change correlate at just +0.21 (Spearman; exact
permutation p = 0.73). Five annual observations cannot estimate the
true association with any precision — but the two series measure
different baskets at different aggregation levels, and their weak
co-movement confirms the decision to keep CPI language out of the
market result.

![Five annual observations do not validate headline CPI as a market-rice outcome](/programs/food-price-climate-transmission/generated/charts/food-price-annual-alignment.svg)

**The annual country screen misses the evidence it should find.** The
inherited qualifier — intersecting headline CPI inflation with
agricultural raw-material imports [@worldbank2026indicatorsapi] —
names Lao PDR and Pakistan at every top-N threshold and never selects
Nepal, which ranks 12th on inflation and 22nd on import share. Yet
Nepal is where the usable market-month evidence actually exists. That
is not a contradiction between countries; it is a mismatch between
research objects, and the screen is retired as the program's research
finding.

![The annual qualifier would not select Nepal despite its usable market-month evidence](/programs/food-price-climate-transmission/generated/charts/food-price-macro-market-mismatch.svg)

# What this does not say

The data pass the alignment and trend-correction gates; they do not
pass any attribution gate.

![The data pass alignment and trend-correction gates but not attribution gates](/programs/food-price-climate-transmission/generated/charts/food-price-claim-gates.svg)

Seven limits shape the reading. The WFP panel covers selected markets
and one rice category, not a national basket. Missing prices cut the
sample from 937 cells to 760. NASA POWER rainfall is a point estimate
at the market, not rainfall over the crop's production area. A dryness
z-score is not a recorded drought, flood, or heat event. The lag
screen is descriptive, not a distributed-lag model. There are no road,
fuel, trade, production, exchange-rate, or policy controls. And the
annual comparison rests on five mismatched years.

These limits block attribution and generalization. They do not
overturn the method correction, and they do not soften the stable
finding that local dryness is a minority alignment under every
threshold tried.

# What would change this finding — and what to build next

The next study should start from an event-defined, multi-commodity
market panel rather than another country score: WFP or official
prices for several staples; geocoded, dated drought, flood, heat, or
production-shock events; crop calendars and sourcing zones; road
access, fuel, exchange-rate, trade, and policy controls; a
pre-specified fixed-effects, event-study, or local-projection design;
and explicit heterogeneity tests by connectivity and commodity.

That object would extend the literature rather than reproduce a weaker
version of an existing Nepal study — updating the
Baptista–Spray–Unsal period, testing newer events and commodities,
and checking whether the remoteness gradient persists.

# How we measured this

```powershell
python research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py
python food-price-climate-transmission/scripts/build-construct-validation.py
python food-price-climate-transmission/scripts/build-figure-dossier.py
```

The first script builds the committed WFP–NASA market object. The
second writes the corrected market-month panel, annual comparison,
81-run sensitivity ledger, and claim gates. The third regenerates
every figure. Source URLs, retrieval and version records, and method
definitions are stored in the evidence JSON and `versions.json`.

# References

Baptista, Spray, and Unsal [@baptista2023climateshocks]; Kotz et al.
[@kotz2024climateinflation]; Shively and Thapa
[@shively2017nepalfoodprices]; FAO [@fao2022fpma]; NASA POWER
[@nasa2026powermonthly]; World Food Programme [@wfp2026nepalprices]; World
Bank [@worldbank2025nepaldevelopmentupdate; @worldbank2026indicatorsapi].
