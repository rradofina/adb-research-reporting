# Methodology and claim test

`attestation_chain: ai-first`

The analysis proceeds in five steps.

1. Retrieve the official facility registries and retain active records.
2. Classify registry facility types into principal, clinical, and all-facility
   tiers using the frozen rules in `pre-registration.md`.
3. Count OpenStreetMap features tagged `amenity=hospital`,
   `amenity=clinic`, or `amenity=doctors` within the same administrative
   units.
4. Divide the OpenStreetMap count by the official-registry clinical-tier count
   for each unit, then aggregate the same numerator and denominator for the
   country result. A value of 100% would indicate equal counts, not matched
   facility identities.
5. Re-run the comparison under the pre-specified ±50% changes to facility-type
   rules, tail-group sizes, and agreement thresholds; then drop each ADM1 unit
   in turn.

The claim survives if the large registry-map disagreement remains under those
definition changes. It would weaken if reasonable facility classifications
approached the 30% planning screen or if one administrative unit drove the
national result. The completed sensitivity ranges are 14.5%–17.9% for the
Philippines and 11.6%–11.8% for Bangladesh. Leave-one-out ratios remain
9.3%–17.9% across both economies.

The method does not match individual facilities and does not treat the
official registry as verified ground truth. The separate public-source
validation chain inspected targeted Bangladesh rows but authorized zero
AI-actionable closures; unresolved identities remain unresolved.

Frozen definitions: `pre-registration.md`. Executable pipelines:
`scripts/process-multi-country.py`, `scripts/sensitivity.py`,
`scripts/sensitivity-bgd.py`, and `scripts/leave-one-out.py`.

