# Uzbekistan station current/method scan

## Why this scan exists

The previous method-evidence audit found 28 Uzbekistan station rows where the
exact official row carries HORIBA or automatic-station wording. That is useful,
but it still does not prove current operating status or complete monitor-grade
classification. This scan checks the next question: when those exact station
IDs are re-checked against the public Uzhydromet maps API, do they still appear,
and do their reading dates support current-status interpretation?

## Finding

The station IDs still appear, but API presence is not the same as current
station status.

The script finds:

- 28 target Uzbekistan instrument-hint station rows.
- 28 target station IDs found in the public Uzhydromet maps API.
- 28 rows with a station-level HORIBA marker.
- 5 rows with API reading dates within 30 days of retrieval.
- 1 row with an API reading date between 31 and 90 days old.
- 22 rows with API reading dates older than 365 days.
- 15 rows with positive raw PM2.5 values.
- 12 rows with negative raw PM2.5 values and 1 row with a `-9999` sentinel.
- 0 rows with explicit current-status confirmation.
- 0 rows with complete monitor-grade classification.
- 0 rows ready for station-radius grade assumptions.

The result is a stronger and more honest queue. Uzbekistan is still the first
follow-up economy because the source has station IDs, coordinates, pollutant
fields, and HORIBA markers. But the same API also carries stale reading dates
for most of the target rows. The next evidence step must therefore look for
station-owner or regulator documentation that explicitly names station status,
instrument method, calibration or certification, and applicability of the
HORIBA marker to each station row.

## Method

The script
`scripts/scan-uzbekistan-station-current-method-evidence.py` reads
`generated/air-monitoring-monitor-grade-station-method-evidence.csv`, filters to
the 28 Uzbekistan rows in the `row_level_instrument_hint` lane, and fetches the
[Uzhydromet public maps API](https://monitoring.meteo.uz/api/maps). It joins
target rows to API rows by station ID, parses the API reading date, records
HORIBA marker fields, classifies raw PM2.5 values, and writes row-level and
summary outputs.

No model memory is used. Counts are computed from committed generated CSV/JSON
artifacts and a public API retrieval record with content hash.

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Target station row found in live API | 28 | Available |
| Station-level HORIBA marker | 28 | Partly available |
| API reading date within 30 days | 5 | Partly available |
| API reading date older than 365 days | 22 | Caution |
| Positive raw PM2.5 value | 15 | Partly available |
| Negative or sentinel raw PM2.5 value | 13 | Caution |
| Current-status confirmed | 0 | Not ready |
| Complete monitor-grade classification | 0 | Not ready |
| Station-radius grade assumptions | 0 | Not ready |

## Reading-date distribution

| API reading-age lane | Rows | Reader use |
|---|---:|---|
| Within 30 days | 5 | Recent API reading, but still not an explicit station-status statement. |
| Within 90 days | 1 | Stale for current-status use; keep as API-presence evidence only. |
| Older than 365 days | 22 | Very old reading date; do not treat API presence as active status. |

## Outputs

- `generated/air-monitoring-uzbekistan-station-current-method-scan.csv`
- `generated/air-monitoring-uzbekistan-station-current-method-scan-summary.json`

## Non-claim

This scan checks public Uzhydromet API station rows for station presence, HORIBA
markers, reading-date age, and raw-value sanity. It does not certify current
operating status, reference-grade method, monitor-grade classification, or
station-radius coverage readiness.
