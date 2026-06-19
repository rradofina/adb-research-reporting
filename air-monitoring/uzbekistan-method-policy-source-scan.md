# Uzbekistan method-policy source scan

## Why this scan exists

The Uzbekistan station current/method scan showed a sharp gap: the 28 target
station IDs still appear in the public Uzhydromet API and carry HORIBA markers,
but most reading dates are stale. The next question is whether public
source-policy pages explain the observation cadence, station status, method
basis, or applicability of those HORIBA markers to the exact station rows.

## Finding

The scan finds source-level context, but not station-level closure.

The script scans 5 public sources and retrieves 4. The retrieved sources include
official Uzhydromet pages, a World Bank technical report, and a UNDP Uzbekistan
press release. It finds:

- 4 retrieved public source rows.
- 4 rows with source-level method, equipment, or monitoring context.
- 4 rows with source-level reading cadence, status, or continuous-monitoring
  context.
- 0 rows that name a target station ID from the 28-row Uzbekistan queue.
- 0 rows that confirm current status for any target station.
- 0 rows that classify any target station as complete monitor-grade.
- 0 rows ready for station-radius grade assumptions.

This matters because source-level language can improve review priority without
closing the evidence gate. Uzhydromet pages describe monitoring basis,
observation points, automatic stations, and observation cadence; the World Bank
report distinguishes manual stations from automatic PM2.5 stations in Tashkent;
UNDP describes 24/7 automatic measurement in a newer regional network. None of
those sources, as retrieved here, names the exact 28 target station IDs and
connects station status, method classification, and reading-date policy to each
row.

## Method

The script `scripts/scan-uzbekistan-method-policy-sources.py` reads the seeded
public source list in `source-inputs/uzbekistan-method-policy-source-seed.csv`
and the target station queue in
`generated/air-monitoring-uzbekistan-station-current-method-scan.csv`. It
retrieves HTML or PDF content, extracts text, matches method and cadence terms,
and checks for explicit target station-ID mentions. Name-like text matches are
retained as review hints but are not treated as station-level evidence because
city names and generic station labels can be ambiguous.

Counts are written to committed CSV/JSON artifacts. Retrieval hashes are stored
in the row-level CSV.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Public source retrieved | 4 | Available |
| Method or equipment context | 4 | Partly available |
| Reading cadence or status context | 4 | Partly available |
| Target station ID named | 0 | Not ready |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Source lanes

| Source-policy lane | Rows |
|---|---:|
| Source-level method and cadence context | 4 |
| Retrieval failed | 1 |

## Outputs

- `generated/air-monitoring-uzbekistan-method-policy-source-scan.csv`
- `generated/air-monitoring-uzbekistan-method-policy-source-scan-summary.json`

## Non-claim

This source-policy scan checks public pages for method, station-status, and
reading-cadence context. It does not certify any target station row as current,
reference-grade, complete monitor-grade, or station-radius-ready.
