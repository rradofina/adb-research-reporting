# Georgia report verification source scan

Status: computed source audit.
Program: `air-monitoring`.
Attestation: `ai-first`.
Generated artifacts:
`generated/air-monitoring-georgia-report-verification-source-scan.csv` and
`generated/air-monitoring-georgia-report-verification-source-scan-summary.json`.

## Question

The station-method classification audit kept Georgia at source-level catalog
context because the live `air.gov.ge` station data are not verified. The
`air.gov.ge` AQI method note says verified data are available in reports. This
scan asks whether the official report route closes verified station-code PM2.5
evidence for the 16 Georgia target rows.

## What the scan did

`scripts/scan-georgia-report-verification-sources.py` reads the 16 Georgia rows
from `generated/air-monitoring-station-method-classification-audit.csv` and the
seed file `source-inputs/georgia-report-verification-source-seed.csv`.

It retrieves:

- The official `air.gov.ge` monthly report route for all 16 target station
  codes in May 2026.
- The official `air.gov.ge` AQI method note.
- The official `air.gov.ge` monitoring-network catalog.

## Result

The scan retrieved all 3 source records.

It records:

- 16 Georgia target rows.
- 16 station-code rows appearing in the official monthly report page.
- 16 PM2.5 report-table rows.
- 16 rows where the report page carries a `Not Verified Data` label.
- 16 rows where the AQI note states live automatic-station data are not
  verified and verified data are available in reports.
- 16 rows with source-level monitoring-network instrument context.

It also records:

- 0 verified-report closure rows.
- 0 station-method classified rows.
- 0 current-status confirmed rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

## Interpretation

The report route is useful because it proves the 16 target station codes can be
called through an official report page and that PM2.5 appears in the report
tables. But it does not close the verification gate: the fetched monthly report
page labels the data as not verified. The Georgia lane therefore remains
source-level evidence plus caution, not verified station-grade evidence.

The next useful source target is an official verified report export, station
metadata table, or regulator document that names the target station code and
gives method, current-status, and grade-basis evidence without the not-verified
label.

## Non-claim

This scan checks whether official `air.gov.ge` report pages provide verified
station-code PM2.5 evidence for the 16 Georgia target rows. It does not certify
station method, current status, complete monitor-grade status, same-station
OpenAQ joins, or station-radius coverage.
