# Pre-registration record — Water stress × crop diversification

`attestation_chain: ai-first`

## Historical frozen screen

The 2026-04-26 frozen screen claimed that Afghanistan, Azerbaijan, Pakistan,
and Turkmenistan persistently occupied the top four of an inherited composite
under ±50% perturbations. Its metric was:

`min(water/100, 1.5) × min(3000/max(yield,100), 1.0) × rural/100 × 100`.

The saved computation actually defines the set as the intersection of seven
**top-five** lists. This historical record remains part of the audit trail; the
claim is not retained.

## Construct-validation protocol

The current validation is a post-registered audit, not a retroactive
pre-registration. It was opened because the inherited water denominator and
crop proxy did not match the research question.

### Population

The fixed 43-economy program roster used by the inherited scripts. Coverage is
reported separately for every source object; missing economies are never
silently removed from the denominator.

### Direct replacements

1. Replace withdrawal divided by internal renewable resources with
   WDI/AQUASTAT SDG 6.4.2 available-water stress.
2. Replace inverse cereal yield with HHI and Shannon equitability calculated
   from FAOSTAT item-level Area harvested shares.
3. Retain rural population only as context and as a diagnostic component, not
   as evidence of water or crop exposure.

### Tests

1. Count exact matches between the published set and each saved run's raw top
   four.
2. Compare published membership with the direct water top five and direct crop
   HHI top five.
3. Report water, crop, and aligned coverage, including whether crop-HHI leaders
   are selected out by missing water data.
4. Calculate Spearman rank associations with deterministic 5,000-resample
   bootstrap intervals.
5. Apply ±50% sensitivity to the diagnostic water ceiling and crop/rural
   exponents, producing 27 specifications.
6. Ablate water, crop, and rural components to identify driver dominance.

### Decision rule

Reject the inherited country claim if any of the following occurs:

- it is not the raw top four in all seven inherited runs;
- fewer than three published members appear in either direct-construct top
  five; or
- the source-upgraded diagnostic is much more strongly associated with one
  component than the other named construct.

All three rejection conditions occur. No replacement country ranking is
promoted.

## Non-claims

The validation does not estimate basin scarcity, groundwater depletion,
irrigation demand, crop water requirements, climate resilience, or policy
priority. A basin × crop × irrigation × year join remains required.
