# Air-monitoring station-method classification audit

`attestation_chain: ai-first`

## Why this audit exists

The station-grade decision ledger reduced the question to 66 exact public
station rows across Indonesia, Georgia, and Uzbekistan. The next decision
question is narrower: which rows have enough public evidence to classify the
PM2.5 measurement method without also claiming complete monitor-grade status?

This audit is a method-classification layer, not a station-grade layer.

## Data sources and coverage

The script
`air-monitoring/scripts/build-station-method-classification-audit.py` reads:

- `generated/air-monitoring-station-grade-decision-ledger.csv`
- `generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv`
- `generated/air-monitoring-station-code-status-method-source-scan.csv`
- `source-inputs/station-method-classification-source-seed.csv`

It retrieves 4 public method or catalog sources and writes:

- `generated/air-monitoring-station-method-classification-audit.csv`
- `generated/air-monitoring-station-method-classification-audit-summary.json`

The source records in the JSON keep the final URL, HTTP status, byte count,
SHA-256 hash, matched method/current/calibration/caution terms, and retrieval
error where applicable.

## Result

The audit covers 66 exact rows: 22 Indonesia rows, 16 Georgia rows, and 28
Uzbekistan rows.

It finds:

- 22 Indonesia rows where exact BMKG station-detail pages and the official
  BMKG air-quality observation regulation support a PM2.5 method class of
  Beta Attenuation Monitoring.
- 22 Indonesia rows with recent exact station-detail pages.
- 16 Georgia rows with source-level instrument catalog context, but 0
  station-level method classifications because the catalog is not a station-code
  method table.
- 16 Georgia rows with a live-data verification caution because the public
  portal says automatic-station live data are not the verified data product.
- 28 Uzbekistan rows with instrument-hint context carried forward, but 0
  method classifications because status, blocker, and certification gaps remain.
- 37 rows with recent public measurement visibility.
- 16 rows with raw-value or blocker caution.

The audit keeps these gates at 0:

- current-status confirmed rows
- calibration/status available rows
- complete monitor-grade classification rows
- station-radius grade-assumption-ready rows

## What changed

The Indonesia lane is now stronger. For those 22 exact BMKG rows, the evidence
supports method classification as Beta Attenuation Monitoring. That is useful
for review because the row-level method gap is no longer generic.

The Georgia lane did not close. Georgia now has better source-level instrument
context and an explicit verification caution, but not a station-level method
table.

The Uzbekistan lane did not close. Exact station IDs and instrument hints remain
visible, but unresolved stale/sentinel/status blockers prevent method or grade
promotion.

## What this does not mean

This audit does not certify any station as currently operating, reference-grade,
regulatory-grade, OpenAQ-joinable, calibration-current, or radius-ready.

A method class is only one gate. Grade use still requires row-level public
current-status evidence, calibration/status evidence where applicable, complete
grade basis, and catchment denominators.

## Reproduce

```powershell
python air-monitoring\scripts\build-station-method-classification-audit.py
python -m py_compile air-monitoring\scripts\build-station-method-classification-audit.py
```

## Next statistical upgrade

Use this audit as the next targeting wall:

- For Indonesia, search for station-level calibration/status or official grade
  basis for the 22 BMKG rows now method-classified.
- For Georgia, search for a station-code method table or verified report table
  that maps station codes to instrument/method and verified status.
- For Uzbekistan, resolve the exact blocker rows and find station-owner or
  regulator status/certification evidence before treating any instrument hint as
  grade evidence.
