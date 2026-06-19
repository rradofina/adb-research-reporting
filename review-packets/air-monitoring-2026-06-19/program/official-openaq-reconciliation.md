# Official-to-OpenAQ reconciliation audit

`attestation_chain: ai-first`

This audit asks whether official station-coordinate rows can be reconciled to
OpenAQ PM2.5 station rows using the signals already produced by the official
station-source extraction. It does not introduce a new fuzzy matching threshold.
It cross-tabulates two screening signals: whether the nearest OpenAQ row is
within 5 kilometers, and whether the extraction found a name-overlap signal.

## Why this measurement problem matters

The station-source extraction showed that official sources expose 230 station
coordinate rows across 5 economies, while OpenAQ exposes 82 coordinate rows in
those same official-coordinate economies. A catchment or station-radius map
would implicitly ask the reader to merge these station universes. That merge is
not justified until the official and OpenAQ rows are reconciled.

## Source added

The script `scripts/reconcile-official-openaq-stations.py` reads:

- `generated/air-monitoring-regulator-station-extraction.csv`
- `generated/air-monitoring-openaq-station-metadata.csv`

It writes:

- `generated/air-monitoring-official-openaq-reconciliation.csv`
- `generated/air-monitoring-official-openaq-reconciliation-summary.json`

The audit uses the extraction pass's nearest-OpenAQ distance and name-overlap
fields. Rows remain candidates unless a station ID, documented crosswalk, or
source-owner/current-status evidence validates the join.

## What the audit found

Generated at `2026-06-19T07:47:02Z`, the audit covers 230 official coordinate
rows and 82 OpenAQ coordinate rows in the same five economies.

| Reconciliation lane | Rows |
|---|---:|
| Official coordinate rows audited | 230 |
| OpenAQ coordinate rows in the same official-coordinate economies | 82 |
| Near plus name-overlap candidate rows | 13 |
| Near-only candidate rows | 9 |
| Name-overlap but not near candidate rows | 22 |
| Official coordinate rows without either candidate signal | 186 |
| Unique near OpenAQ candidate rows | 13 |
| OpenAQ rows not used as a near candidate | 69 |
| Validated same-station joins | 0 |

The most plausible lane is still only a candidate lane: 13 official rows have
both a within-5-kilometer nearest OpenAQ row and a name-overlap signal. Another
9 rows have proximity without name overlap, and 22 rows have a name signal
without the 5-kilometer proximity signal. The largest group remains 186
official coordinate rows with neither signal.

## Country-level evidence

| ISO | Official coordinate rows | OpenAQ coordinate rows | Near + name | Near only | Name only | No candidate | Validated joins |
|---|---:|---:|---:|---:|---:|---:|---:|
| BGD | 31 | 22 | 4 | 1 | 2 | 24 | 0 |
| GEO | 16 | 2 | 0 | 0 | 0 | 16 | 0 |
| IDN | 22 | 36 | 1 | 1 | 1 | 19 | 0 |
| MYS | 68 | 18 | 3 | 2 | 11 | 52 | 0 |
| UZB | 93 | 4 | 5 | 5 | 8 | 75 | 0 |

## Interpretation

This narrows the next review queue. Bangladesh and Uzbekistan supply the
largest number of near-plus-name candidate rows, but the audit does not turn
those rows into a station crosswalk. Malaysia has many name-only candidate
rows, which are useful for source review but weak for same-station language
because the nearest OpenAQ row is not within the 5-kilometer diagnostic
threshold.

For the public article and map, the implication is simple: official station
coordinates and OpenAQ station coordinates should remain separate layers until
the candidate rows are validated. The next evidence step is a station ID or
source-owner/current-status crosswalk, not a population catchment.

## What this does not mean

- It does not validate any official-to-OpenAQ same-station join.
- It does not prove that official rows absent from OpenAQ are active monitors.
- It does not prove that OpenAQ rows absent from the official extraction are
  non-regulatory or low quality.
- It does not classify monitor grade.
- It does not compute station-radius population coverage.

## Reproduce

```bash
python air-monitoring/scripts/extract-regulator-station-evidence.py
python air-monitoring/scripts/reconcile-official-openaq-stations.py
```

The next upgrade is to validate the 13 near-plus-name candidates first, then
review near-only and name-only rows with station IDs, source-owner documentation,
or current-status pages where public sources exist.
