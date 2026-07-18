# Sensitivity and robustness — air-monitoring public QA observability

`attestation_chain: ai-first`. Updated 2026-07-19.

## Numeric sensitivity

The downstream station-radius diagnostic uses 4 km as the main geometry, 0.5
km as the −87.5% narrow lane, and 50 km as a deliberately wide stress lane. The
active claim stops before coverage is allowed, so the required ±50% question is
answered conservatively: moving the radius by at least ±50% cannot create a
same-station crosswalk, calibration record, inspection log, or complete
monitor-grade row. Allowed claims remain zero in every radius lane.

![The absence result is invariant to radius choice](generated/charts/air-monitoring-sensitivity-boundary.svg)

## Denominator-route robustness

The ledger records 831 GHSL/ACAG denominator joins. Replacing the population or
PM2.5 surface could alter future denominator values but cannot close the public
identity and station-grade gates. Denominator choice is therefore downstream
of the active finding.

## Source-discovery sensitivity

The result is sensitive to false negatives in public source discovery. A new
pass is justified only when it names a previously unchecked source and explains
why that source plausibly contains one of the following:

- a station-specific calibration certificate or inspection log;
- a current station-level calibration-status record;
- an official station-code crosswalk; or
- a public method-grade ledger keyed to station identifiers.

One valid row narrows the finding for that station or economy. A generic search
that produces the same source classes does not count as robustness evidence.

## Claim robustness

The result survives the strongest noncausal interpretation test: removing the
denominator calculations entirely leaves the public-evidence conclusion
unchanged. Conversely, the finding is deliberately easy to falsify with a
specific public QA object. This asymmetry is appropriate for a bounded absence
claim.
