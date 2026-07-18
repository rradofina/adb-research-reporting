# Conclusion and next evidence upgrade — air-monitoring

`attestation_chain: ai-first`. Updated 2026-07-19.

## Conclusion

The current public packet supports one research conclusion: station visibility
is not the same as verifiable station-level QA evidence. The audit finds public
station inventories, measurements, method language, dashboard status, and
denominator geometry, but it cannot validate the identity and monitor-grade
links required for a station-radius coverage claim.

The appropriate output is therefore a documented observability gap. Publishing
that boundary is more informative than another unqualified station count and
more honest than converting 831 denominator joins into a population-coverage
estimate.

## Exact upgrade object

One row can move only when a named public source provides at least one of:

- a station-specific inspection log;
- a station-specific calibration certificate or current calibration-status
  row;
- an official station-code crosswalk linking the regulator record to the
  aggregator record; or
- a station-keyed method-grade ledger with current status.

The source must expose a stable station identifier, retrieval date or version,
and enough metadata to join the evidence to the audited station row.

## What happens next

Do not run another generic portal scan. Reopen the empirical question only for
a named source that plausibly contains one of the upgrade objects above.
Otherwise retain the SR absence finding, publish the current issue, and rotate
to the next program.

