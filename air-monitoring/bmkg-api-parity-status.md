# BMKG API telemetry/status-field check

Status: computed BMKG API parity/status-field check, Mode A AI-first.

This pass follows the public BMKG Nuxt app token flow and queries the official
PM2.5 list API plus the 22 target station-detail API routes. It is deliberately
narrow: the question is whether the official API adds station-specific
operational-status, inspection-log, calibration-status, certificate, grade, or
method fields beyond the visible station-page telemetry.

## Result

The API adds public telemetry confirmation, not certification closure. The
scan retrieves the token route, the PM2.5 list API, and all 22 target detail
API routes. It finds 21 of 22 target station files in the list API, 132 hourly
PM2.5 observations across the target detail routes, 22 detail-coordinate rows,
and 21 `KONDISI` air-quality condition labels, but it finds 0 station-status
API fields, 0 inspection fields, 0 calibration fields, 0 certificate fields, 0
grade fields, and 0 method fields for the 22 target rows.

The practical reading is that BMKG has two public telemetry surfaces for these
rows: the rendered station pages and the official API used by those pages.
Both are useful source evidence, but neither supplies the missing station
status/certificate layer needed for complete monitor-grade or station-radius
use.

## Evidence Gates

| Gate | Result |
|---|---:|
| Public app token route retrieved | 1 |
| PM2.5 list API retrieved | 1 |
| Target station files found in list API | 21 |
| Target detail API routes retrieved | 22 |
| Target rows with API hourly PM2.5 data | 22 |
| Hourly PM2.5 observations in target detail APIs | 132 |
| Target detail API coordinate rows | 22 |
| Target rows with list/detail coordinate parity | 21 |
| Target rows with `KONDISI` air-quality condition labels | 21 |
| Station-status API fields | 0 |
| Calibration/certificate API fields | 0 |
| Complete monitor-grade rows | 0 |
| Station-radius-ready rows | 0 |

## Artifacts

- Script: `air-monitoring/scripts/scan-bmkg-api-parity-status.py`
- Source seed: `air-monitoring/source-inputs/bmkg-api-parity-source-seed.csv`
- Row output: `air-monitoring/generated/air-monitoring-bmkg-api-parity-status.csv`
- Summary output: `air-monitoring/generated/air-monitoring-bmkg-api-parity-status-summary.json`

## Reader Use

Use this artifact as an API-field wall. It proves the public BMKG API route is
reachable and station-specific, but it also shows that the API payload is
telemetry-only for the evidence questions that matter here. `KONDISI` is an
air-quality condition label, not station operational status.
