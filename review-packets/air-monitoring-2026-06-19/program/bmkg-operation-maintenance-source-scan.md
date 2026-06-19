# BMKG operation and maintenance source scan

Status: computed source audit.
Program: `air-monitoring`.
Attestation: `ai-first`.
Generated artifacts:
`generated/air-monitoring-bmkg-operation-maintenance-source-scan.csv` and
`generated/air-monitoring-bmkg-operation-maintenance-source-scan-summary.json`.

## Question

The station-method classification audit upgraded 22 Indonesia/BMKG rows to a
publicly supported `Beta Attenuation Monitoring (BAM)` method class. The next
question is narrower: do public BMKG operation, daily-inspection,
calibration-procedure, or service-tariff sources close station-level current
status, station-specific inspection logs, station-specific calibration
certificates, complete monitor-grade status, or station-radius readiness?

## What the scan did

`scripts/scan-bmkg-operation-maintenance-sources.py` reads the 22 BMKG rows in
`generated/air-monitoring-station-method-classification-audit.csv` and the
seed file `source-inputs/bmkg-operation-maintenance-source-seed.csv`. It
retrieves 4 public BMKG context sources and re-fetches 22 exact BMKG PM2.5
station-detail pages.

The context sources are:

- BMKG SOP No. 014/KB/IV/2023 for daily BAM-1020 inspection.
- BMKG Regulation No. 11/2019 on air-quality observation and data management.
- BMKG Central Java service and PNBP tariff page.
- BMKG South Sumatra PM2.5 / BAM-1020 instrument note.

## Result

The scan retrieved all 26 source records: 4 context sources and 22 exact
station-detail pages.

It records:

- 22 BMKG target rows.
- 22 exact station-detail pages retrieved.
- 22 exact station-detail pages with a recent public measurement display.
- 22 rows with source-level daily inspection SOP context.
- 22 rows with source-level daily inspection procedure context.
- 22 rows with source-level maintenance/check context.
- 22 rows with source-level calibration procedure context.
- 22 rows with source-level BAM calibration service/tariff context.
- 22 rows with source-level regional BAM-1020 model context.

It also records:

- 0 station-specific inspection log rows.
- 0 station-specific calibration certificate rows.
- 0 current-status confirmed rows.
- 0 calibration-status available rows.
- 0 complete monitor-grade classification rows.
- 0 station-radius-ready rows.

## Interpretation

This is a useful upgrade for the evidence ladder, but it is not a grade
promotion. Public BMKG materials now show that the BAM-1020 lane has official
daily-inspection, maintenance/check, calibration-procedure, and calibration
service/tariff context. The evidence still does not show the target station's
own inspection log, calibration certificate, calibration status, or public
current-status certification.

The next useful source target is therefore not another source-level BMKG method
document. It is a public station-owner record that names one of the 22 exact
station IDs or station names and gives station-specific inspection,
calibration, status, or certification evidence.

## Non-claim

This scan records public BMKG operation, maintenance, calibration-procedure,
and service-tariff context for the 22 BMKG BAM method-classified rows. It does
not certify station current status, station-specific inspection logs,
station-specific calibration certificates, complete monitor-grade status,
same-station OpenAQ joins, or station-radius coverage.
