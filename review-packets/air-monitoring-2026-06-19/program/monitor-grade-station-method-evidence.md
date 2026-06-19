# Monitor-grade station method-evidence audit

attestation_chain: ai-first

## What this adds

The station-review queue identified 66 rows where a public source group had
method, equipment, or standards context. This audit asks a narrower row-level
question: do those 66 review rows join back to exact official extraction rows,
and does the exact row itself carry method or instrument language?

The script finds:

- 66 method-context station rows reviewed.
- 66 exact official station rows found by economy, source name, and station ID.
- 66 exact rows with PM2.5 signal and coordinates.
- 28 rows where the exact row carries instrument wording.
- 38 rows where the exact row is an official PM2.5 portal or API row, but the
  exact row does not name a reference method or instrument.
- 0 rows with complete monitor-grade classification.
- 0 rows ready for station-radius grade assumptions.

## Main reading

The audit strengthens the evidence spine without changing the claim boundary.
Uzbekistan is now the strongest station-level follow-up lane because the exact
official API rows carry the `automatic HORIBA marker` station type. Indonesia
and Georgia still have exact public PM2.5 rows, but the exact rows are portal
or hourly API rows; their method language remains source-group context rather
than station-row certification.

The practical result is a sharper review order. Uzbekistan should be checked
first for station-level current-status and method documentation. Indonesia and
Georgia should be checked next for station-owner or regulator tables that
connect the source-level method language to the exact PM2.5 portal/API station
rows. None of the 66 rows should enter station-radius coverage until that
station-level evidence exists.

## Method

The script `scripts/audit-monitor-grade-station-method-evidence.py` reads:

- `generated/air-monitoring-monitor-grade-station-review-queue.csv`
- `generated/air-monitoring-regulator-station-extraction.csv`

It filters the station-review queue to
`method_context_needs_station_confirmation`, joins the official extraction rows
by `(iso3, source_name, source_station_id)`, and assigns each row to one of
three evidence lanes:

- `row_level_instrument_hint`
- `row_level_pm25_portal_or_api`
- `exact_row_not_found`

No network access is used. Counts are computed from committed generated CSVs.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Exact official row join | 66 | Available |
| Exact PM2.5 signal | 66 | Available |
| Row-level instrument hints | 28 | Partly available |
| PM2.5 portal/API rows without instrument row term | 38 | Partly available |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Country distribution

| Economy | Station rows | Exact rows | PM2.5 rows | Instrument hints | Portal/API rows | Complete grade |
|---|---:|---:|---:|---:|---:|---:|
| Uzbekistan | 28 | 28 | 28 | 28 | 0 | 0 |
| Indonesia | 22 | 22 | 22 | 0 | 22 | 0 |
| Georgia | 16 | 16 | 16 | 0 | 16 | 0 |

## Outputs

- Row audit:
  `generated/air-monitoring-monitor-grade-station-method-evidence.csv`
- Summary:
  `generated/air-monitoring-monitor-grade-station-method-evidence-summary.json`

## Non-claim

This audit confirms exact official row evidence and row-level hints only. It
does not certify station grade, does not validate same-station joins, and does
not make station-radius coverage ready.
