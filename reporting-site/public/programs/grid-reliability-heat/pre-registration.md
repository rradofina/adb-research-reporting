# Methodology and claim test

`attestation_chain: ai-first`

The original 26 April 2026 pre-registration tested whether five economies remained in the capacity-based top five under an alternative single-fuel-share rule. That rule was positive. It did not pre-register a heat–outage model.

The present analysis is explicitly a **retrospective construct-validation addendum**, frozen in code rather than represented as a prospective experiment. It asks whether a directional regional claim survives reasonable definitions on both sides of the proposed bridge.

## Units and transformations

- Unit: country-year-outcome observation.
- Heat: annual country values for average maximum temperature (`tasmax`), maximum daily maximum temperature (`txx`), and tropical nights (`tr`). Each is expressed as an anomaly from that economy's 1991–2020 mean.
- Reliability: five separate outcomes; none is combined into a composite.
- Association: Spearman rank correlation. This is descriptive and unadjusted.
- Structural exposure: fuel-Herfindahl on 2017 generation, shown separately and withheld below 80% generation coverage.

## Decision rule

Reject a directional heat–reliability claim if the correlation changes sign across defensible outcomes or heat measures, or if most 95% bootstrap intervals include zero. The rule fires: eight correlations are positive, seven negative, and 10 of 15 intervals include zero.

## Sensitivity

The ±50% requirement applies to the 80% generation-coverage floor (40%–100%) and any display threshold. The headline does not depend on a high/low cutoff. Correlations are also recomputed on one latest observation per economy and after 5th/95th percentile winsorization of outcomes.

## Interpretation boundary

No coefficient estimates a causal heat effect. The design omits demand, reserve margin, generation availability, imports, network topology, adaptation, price, and weather-event timing. Country-year rank association cannot substitute for service-territory outage records.
