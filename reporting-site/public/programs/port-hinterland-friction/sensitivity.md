# Sensitivity — Port-Hinterland Friction

`attestation_chain: ai-first`. Updated 2026-07-19.

The inherited imports × LPI formula is internally stable when its arbitrary
normalizer and cap are changed by ±50%: all variants retain the same inherited
top five. That is formula stability, not construct validity.

The direct CPPI test varies the observed-data choices that can change the
substantive comparison.

| Dimension | Variants |
|---|---|
| CPPI year | 2024, 2025 |
| Minimum sampled calls | unrestricted, 24, 48, 72 |
| Economy diagnostic | median, lower quartile, call-weighted mean |

The 24- and 72-call thresholds implement the required ±50% test around the
main 48-call threshold. Across 20 specifications, inherited top-five overlap
ranges from zero to two; four specifications have zero overlap and the main
specification has one.

For the 2025 common sample, Spearman associations between the inherited score
and observed CPPI disadvantage are:

| Diagnostic | Association | 95% bootstrap interval |
|---|---:|---:|
| Median | −0.36 | −0.79 to 0.21 |
| Lower quartile | −0.26 | −0.76 to 0.29 |
| Call-weighted mean | −0.57 | −0.83 to −0.11 |

Intervals use 2,000 deterministic bootstrap draws. The median and lower-
quartile intervals cross zero; the call-weighted interval excludes zero and
points opposite the inherited label.

Landlocked economies require a separate transit-country and border-delay
model and are not evidence for a domestic-port ranking. CPPI does not observe
the inland leg, so subnational route time remains outside the current claim
until the named shipment-level source is available.

Evidence: `generated/port-cppi-construct-validation.json` and
`generated/port-cppi-sensitivity.csv`.
