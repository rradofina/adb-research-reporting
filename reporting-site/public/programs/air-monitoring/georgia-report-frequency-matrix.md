---
attestation_chain: ai-first
status: Screening Result
method: air_monitoring_georgia_report_frequency_matrix_v1
---

# Georgia report-frequency matrix

## Why this pass exists

The Georgia policy wall points readers toward reports for verified data,
while the monthly report/export ladder kept the monthly surface open.
This pass tests whether daily or annual report frequencies change that
decision for the same target station-code set.

## What the public routes show

- Report-frequency/export probes targeted: 24.
- Valid daily/monthly report or export payloads retrieved: 12.
- Annual route probes returning server-error pages: 12.
- HTML/PDF payloads retaining not-verified labels: 8.
- XLSX exports with all target station sheets: 4.
- XLSX exports with verification labels: 0.
- Verified report-closure routes found: 0.

## Reader use

Use this as a report-frequency falsifier. It shows that daily reports do
not rescue the verified-report gate, monthly comparison probes stay
consistent with the 24-month ladder, annual probes do not return a usable
public report payload for the tested formats, and XLSX station sheets are
not enough without a verification label.

## Non-claim

This scan tests official Georgia daily, monthly, and annual report routes plus XLSX/PDF exports. It does not certify any target station as verified, currently operating, station-method classified, complete monitor-grade, or station-radius ready.

## Reproduce

Run `python air-monitoring/scripts/scan-georgia-report-frequency-matrix.py`.
The source list is `air-monitoring/source-inputs/georgia-report-frequency-matrix-source-seed.csv`.
Outputs are `air-monitoring/generated/air-monitoring-georgia-report-frequency-matrix.csv`
and `air-monitoring/generated/air-monitoring-georgia-report-frequency-matrix-summary.json`.
