---
slug: water-crop-pressure-cluster
title: The “stable top four” does not survive its own water and crop measures
subtitle: The published set is the raw top four in only two of seven runs; direct water stress retains two members, direct crop concentration none, and the most crop-concentrated visible economies lack water observations.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [ADB DMCs]
topics: [water, agriculture, crop-diversification, measurement]
program: water-stress-crop-diversification
maturity: PP
abstract: >
  An inherited screen described Afghanistan, Azerbaijan, Pakistan, and
  Turkmenistan as a persistent water-crop-pressure top four. The screen
  multiplied freshwater withdrawal as a share of internal renewable water,
  inverse cereal yield, and rural population share. This paper tests the
  construction before treating it as a research result. The published set is
  the raw top four in only two of seven sensitivity runs; the baseline raw top
  four contains Uzbekistan rather than Afghanistan. Replacing the internal-
  water ratio with WDI/AQUASTAT SDG 6.4.2 available-water stress retains only
  Pakistan and Turkmenistan from the published four in its top five. Replacing
  inverse cereal yield with FAOSTAT harvested-area concentration retains none.
  Forty-one of the 43 roster economies have a 2024 crop-mix record, but only 30
  have water-stress data, and all five highest crop-HHI economies are missing
  from the water series. Among the 30 aligned economies, water stress and crop
  concentration have a Spearman correlation of -0.24 with a 95% bootstrap
  interval from -0.59 to +0.15. A source-upgraded three-term diagnostic is
  correlated +0.92 with water stress but only +0.05 with crop concentration.
  The inherited country ranking is rejected. The defensible output is a
  construct-validation result and a specification for a basin-by-crop-by-year
  exposure object.
doi:
published_at: 2026-04-26
updated_at: 2026-07-31
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# When water is scarce and crops are concentrated, where should attention go?

Water-constrained agriculture is an operational problem with several distinct
units. Water availability is organized by basin, aquifer, season, allocation,
and infrastructure. Crops occupy particular fields, growing seasons, and
irrigation systems. Exposure belongs to farms and people inside those same
hydrological and production units. A country average can summarize each
dimension, but multiplying national averages does not automatically recover a
water-crop mechanism.

An inherited screen described Afghanistan, Azerbaijan, Pakistan, and
Turkmenistan as a persistent water-crop-pressure top four. The research
question is narrower than “where is water-crop pressure highest?” It is: does
the inherited four-country set survive its stated ranking rule and direct
national measures of available-water stress and crop concentration?

# What we found

The published four-country water-crop-pressure claim does not survive direct
measurement of either construct in its title. Afghanistan, Azerbaijan,
Pakistan, and Turkmenistan were described as holding the raw top four across
seven parameter runs. They do so in only two. The baseline raw order is
Turkmenistan, Pakistan, Azerbaijan, and Uzbekistan; Afghanistan is fifth.

The mismatch grows when the proxies are replaced. Pakistan and Turkmenistan
are the only published members in the top five of the WDI/AQUASTAT
available-water-stress indicator. None of the four is in the top five of
FAOSTAT harvested-area concentration. The old ranking is therefore rejected,
not corrected.

![Three construct gates show why the inherited country claim is rejected](/programs/water-stress-crop-diversification/generated/charts/water-three-gate-validity.svg)

This result does not establish which economies face the greatest agricultural
water risk. It establishes that a stable-looking formula can preserve a country
set even when its water denominator, crop proxy, coverage rule, and stated
sensitivity interpretation do not measure the same object.

Only the two “minus 50%” water-term runs have Afghanistan, Azerbaijan,
Pakistan, and Turkmenistan as their raw top four. In the other five runs,
Uzbekistan replaces Afghanistan. Afghanistan is fifth in the baseline and in
five of seven runs.

![Membership changes when the stated rule and direct constructs are compared](/programs/water-stress-crop-diversification/generated/charts/water-membership-churn.svg)

Among 30 aligned economies, available-water stress and crop HHI have a
Spearman correlation of -0.24. The 95% bootstrap interval runs from -0.59 to
+0.15. The sample does not support a stable positive national association
between the two objects.

![Available-water stress and crop concentration show weak and uncertain association](/programs/water-stress-crop-diversification/generated/charts/water-crop-construct-scatter.svg)

The all-three diagnostic correlates +0.92 with available-water stress, +0.35
with rural share, and +0.05 with crop HHI. The crop interval spans -0.34 to
+0.41. Although crop concentration appears multiplicatively in the formula,
it contributes little to the cross-economy order.

![Correlation diagnostics show that water dominates the replacement score](/programs/water-stress-crop-diversification/generated/charts/water-diagnostic-driver-dominance.svg)

# Why the constructs pull apart

The inherited panel uses three World Development Indicators objects:

1. annual freshwater withdrawal as a percentage of internal renewable
   resources (`ER.H2O.FWTL.ZS`);
2. cereal yield in kilograms per hectare (`AG.YLD.CREL.KG`); and
3. rural population as a percentage of total population (`SP.RUR.TOTL.ZS`).

The program roster contains 43 economies. Only 30 have all three inputs needed
for the old index. Earlier program prose reported 43 of 50 as rankable. That
statement is false for the committed panel and is retired.

Turkmenistan, Pakistan, Uzbekistan, and Azerbaijan all exceed 150% on the old
internal-resource ratio. The formula therefore assigns every one the same
maximum water term of 1.5. Their ordering is determined entirely by inverse
cereal yield and rural population share.

Replacing the denominator compresses the reported ratios. Turkmenistan moves
from 1,868% of internal renewable resources to 135% on available-water stress;
Pakistan from 326% to 110%; Uzbekistan from 263% to 123%; and Azerbaijan from
161% to 58%. The revised values still indicate pressure in several economies,
but they no longer support the same order.

![Internal-resource ratios and available-water stress produce different magnitudes](/programs/water-stress-crop-diversification/generated/charts/water-denominator-rebase.svg)

A value above 100% is not direct proof of over-pumping. Depending on the
indicator, it can reflect external inflows, nonrenewable withdrawals, reuse,
desalination, environmental-flow requirements, or combinations of these. The
national series does not separate those mechanisms.

The direct FAOSTAT crop-HHI top five is Tuvalu, Kiribati, the Federated States
of Micronesia, Nauru, and Vanuatu. None appears in the published four. Coconut
accounts for 71% to 92% of reported harvested area in these records.

![Direct crop concentration does not reproduce the published set](/programs/water-stress-crop-diversification/generated/charts/water-crop-concentration-profiles.svg)

Within the published set, Afghanistan has the highest crop HHI at 0.41, with
wheat covering 64% of reported harvested area. Turkmenistan, Azerbaijan, and
Pakistan have HHIs from 0.19 to 0.28. Those values may still matter, but they do
not place the four at the top of the observed concentration distribution.

The join produces 30 national water-crop records. This apparently high overlap
hides a systematic edge case: Tuvalu, Kiribati, the Federated States of
Micronesia, Nauru, and Vanuatu have the five highest crop-concentration values,
yet none has an available-water-stress observation. The composite therefore
cannot evaluate the most concentrated crop systems visible in FAOSTAT.

![The national source stack loses the most crop-concentrated cases](/programs/water-stress-crop-diversification/generated/charts/water-source-alignment-funnel.svg)

The plot also makes the selection problem visible. The five highest crop-HHI
records cannot appear because their water values are missing. The observed
correlation describes the 30-economy aligned subset, not the entire roster and
not small-island water insecurity.

Across the required 27 ±50% specifications, Afghanistan, Sri Lanka, Pakistan,
and Turkmenistan appear in every diagnostic top five; Uzbekistan appears in
21. Azerbaijan appears in none. Internal stability is real, but it stabilizes
a different set and does not establish basin-level crop-water exposure.

![Twenty-seven diagnostic specifications show stable membership but the wrong construct](/programs/water-stress-crop-diversification/generated/charts/water-diagnostic-sensitivity-membership.svg)

# What this means for water and agriculture work

Cross-country evidence indicates that crop diversity can stabilize national
food production [@renard2019cropdiversity]. District evidence from India finds
that diversification can reduce losses from rainfall deficits and heat stress,
particularly under severe shocks [@birthal2019cropdiversification]. Those
studies evaluate production outcomes over time. They do not imply that low
cereal yield measures diversity or that a national concentration index
multiplied by water stress measures resilience.

Water research makes the spatial problem equally clear. Monthly, spatially
resolved scarcity estimates reveal conditions hidden by annual national means
[@mekonnen2016waterscarcity]. Aqueduct 4.0 separates multiple physical,
quality, and governance indicators and calculates them at hydrological,
aquifer, and national scales [@wri2023aqueduct]. Central Asia also illustrates
why country borders can conceal the mechanism: large irrigation withdrawals
from the Amu Darya and Syr Darya connect upstream allocation, downstream use,
and ecological loss [@micklin2007aralsea].

The negative result refines rather than contradicts the literature. Crop
diversity may stabilize production, and severe climate shocks may make its
benefits more visible [@renard2019cropdiversity;
@birthal2019cropdiversification]. Testing that proposition requires a dynamic
outcome: production loss, yield variance, income loss, recovery, or another
shock response measured over time. A one-year national HHI is an exposure
descriptor, not resilience. Likewise, SDG 6.4.2 is appropriate for national
monitoring but does not assign water pressure to crops [@fao2017sdg642].
Aqueduct's multi-scale design and monthly scarcity research show why basin,
season, and demand location matter [@wri2023aqueduct;
@mekonnen2016waterscarcity].

For an operations team, the useful action is to improve the data object rather
than target the current country list. The 11 crop-visible but water-missing
economies warrant source work; the aligned 30 warrant basin-level joining; and
Central Asian cases warrant explicit transboundary allocation rather than an
internal-resource denominator. This is why renaming the composite would not
solve the problem. It would still be a water ranking with a weakly associated
crop term and a rural multiplier.

# What this does not say

- It does not show that the published four have low agricultural water risk.
- It does not show that the five coconut-concentrated small island economies
  have the greatest crop vulnerability. Their high HHI may partly reflect
  small reported crop portfolios and does not measure import dependence,
  nutrition, farm income, or freshwater access.
- It does not measure groundwater depletion, return flows, desalination,
  water reuse, irrigation efficiency, or treaty-secured inflows.
- It does not estimate crop water requirements or distinguish irrigated from
  rain-fed harvested area.
- It does not establish that crop diversification causes resilience. The
  cross-sectional correlations are descriptive and the sample is 30 aligned
  economies.
- It does not place farms or rural residents inside stressed basins. Rural
  population share remains a national contextual variable.

AQUASTAT cautions that renewable-water totals are not equivalent to water that
is economically or physically exploitable [@fao2024aquastat]. The measure
improves the denominator but remains national and does not identify depletion,
seasonal scarcity, or transboundary allocation. The sources are also not a
balanced panel. Water stress is latest 2022, crop mix is 2024, and the rural
share reaches 2025. The analysis treats this as a source-alignment diagnostic,
not a common-year exposure estimate.

# What would change this finding

The next qualified object has four linked layers: basin withdrawal or
depletion and allocation; crop harvested area with irrigation status; crop
water requirements and common-year weather; and farms or people inside the
same basin-crop unit. Candidate public inputs include AQUASTAT or Aqueduct/GRACE,
FAOSTAT or SPAM crop maps, crop-water coefficients, and gridded exposure. Until
that join exists, national composite membership should not be presented as a
water-crop finding.

![The next data object must align water, crops, demand, and exposure](/programs/water-stress-crop-diversification/generated/charts/water-next-data-object.svg)

The country ranking is retired. What remains is a clear research design: join
water, crops, demand, and exposure at a common basin-by-crop-by-year unit, then
test an observed shock or depletion outcome.

# How we measured this

For withdrawal divided by internal renewable resources \(W_i\), cereal yield
\(Y_i\), and rural population share \(R_i\), the inherited index is

\[
I_i = 100 \times \min(W_i/100, 1.5)
      \times \min(3000/\max(Y_i,100),1)
      \times (R_i/100).
\]

All three numeric choices—the 100% normalization, 1.5 ceiling, and 3,000
kilogram yield reference—are arbitrary screening parameters. The published set
is not the baseline raw top four. It is the four economies appearing in the
top five of every one of seven parameter runs. The validation reconstructs
each run and compares that intersection with each run's actual top four.

The water replacement is SDG 6.4.2. Unlike the old internal-resource ratio, it
uses total renewable freshwater resources after environmental-flow
requirements. The crop replacement uses each crop item's share of total
positive harvested area. Concentration is summarized as a
Herfindahl-Hirschman index \(HHI_i = \sum_c s_{ic}^2\), where \(s_{ic}\) is
crop \(c\)'s harvested-area share in economy \(i\). The pipeline parses FAOSTAT Crops and Livestock Products Area harvested rows
for crop year 2024 [@fao2026faostatqcl]. The pipeline also calculates Shannon
equitability and the top-one and top-three shares, but HHI is used for the
direct rank comparison. Confidence intervals use 5,000 deterministic bootstrap
resamples. Five tests are committed:

1. **Rule fidelity.** Count how many of the seven inherited sensitivity runs
   have the published set as their actual raw top four.
2. **Construct overlap.** Compare the published four with the top five of
   direct available-water stress and direct crop HHI.
3. **Coverage selection.** Identify which high-concentration crop systems are
   lost because the water series is missing.
4. **Association.** Calculate Spearman correlations among the old index,
   direct water stress, crop HHI, rural share, and a source-upgraded diagnostic.
5. **Sensitivity and ablation.** Vary the diagnostic water ceiling and the
   crop and rural exponents by ±50%, producing 27 specifications.

The source-upgraded diagnostic multiplies capped available-water stress, crop
HHI, and rural share; it is retained only as a diagnostic. The validation adds
WDI/AQUASTAT SDG 6.4.2 with a latest 2022 observation for 30 roster economies.
After excluding aggregate item labels, the FAOSTAT pipeline calculates crop
shares for 41 economies.

```bash
python water-stress-crop-diversification/scripts/process-water-crop.py
python water-stress-crop-diversification/scripts/deepen-denominator.py
python water-stress-crop-diversification/scripts/audit-water-source-readiness.py
python water-stress-crop-diversification/scripts/build-construct-validation.py
python water-stress-crop-diversification/scripts/build-figure-dossier.py
```

The raw WDI responses and FAOSTAT bulk ZIP are regenerated from public sources
and remain outside version control. The scripts commit the filtered rows,
diagnostics, sensitivity specifications, figures, source hashes, and retrieval
records needed to audit every empirical statement. Inspect the full evidence
object at
[/program/water-stress-crop-diversification/evidence](/program/water-stress-crop-diversification/evidence).

`attestation_chain: ai-first`
