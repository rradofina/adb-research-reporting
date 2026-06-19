# BMKG station-specific status and calibration audit

Status: computed source audit.
Program: `air-monitoring`.
Attestation: `ai-first`.
Generated artifacts:
`generated/air-monitoring-bmkg-station-specific-status-audit.csv` and
`generated/air-monitoring-bmkg-station-specific-status-audit-summary.json`.

## Question

The BMKG operation and maintenance scan showed that the 22 Indonesia/BMKG PM2.5
rows have useful source-level support: exact station pages, BAM method text,
daily-inspection SOP context, maintenance/check context, and calibration
procedure or service/tariff context. The remaining reviewer question is stricter:
does the public source package contain station-specific operational status,
inspection-log, calibration-certificate, or calibration-status evidence for the
exact target rows?

## What the audit did

`scripts/audit-bmkg-station-specific-status.py` reads
`generated/air-monitoring-bmkg-operation-maintenance-source-scan.csv`,
re-fetches the 22 exact BMKG station-detail pages, caches the raw HTML under
`.cache/bmkg-station-specific-status/`, and records a page-level source trail
with URL, cache path, SHA-256 hash, retrieval status, parsed timestamp, parsed
PM2.5 display value, category, method text, and station-specific closure gates.

The parsed public display snapshot is retained because it is useful evidence
that the public station page is active as a display object. It is not used as
station-status certification.

## Result

The audit records:

- 22 target BMKG rows.
- 22 exact BMKG station-detail pages retrieved.
- 22 pages with parsed public display timestamp, PM2.5 value, and category.
- 22 pages with station name matches and station code in the URL.
- 22 pages with BMKG PM2.5 / BAM method text.
- 22 rows inheriting source-level daily-inspection, maintenance, and
  calibration context from the previous BMKG source wall.

It also records:

- 0 station-detail pages with station-specific operational-status
  certification.
- 0 station-specific inspection-log rows.
- 0 station-specific calibration-certificate rows.
- 0 calibration-status rows.
- 0 status or certificate links from the station pages.
- 0 current-status confirmed rows.
- 0 complete monitor-grade rows.
- 0 station-radius-ready rows.

## Interpretation

The new evidence makes the BMKG lane clearer, not stronger than the source
allows. The station pages provide exact public display snapshots and method
language. They do not provide the missing certification layer that would let the
pipeline promote these rows to complete monitor-grade or use them as a
station-radius denominator.

For reviewers, the useful distinction is now visible: public telemetry and
method text are available for all 22 rows, while station-specific logs,
calibration certificates, calibration status, and operational-status
certification remain absent from the public station pages.

## Non-claim

This audit records exact BMKG station-detail public display snapshots and
station-page evidence gates for the 22 BMKG BAM rows. It does not certify
station current status, station-specific inspection logs, station-specific
calibration certificates, complete monitor-grade status, same-station OpenAQ
joins, or station-radius coverage.

## Reproduce

```bash
python air-monitoring/scripts/audit-bmkg-station-specific-status.py
```

The committed CSV/JSON outputs are the reproducible evidence packet. The raw
BMKG HTML cache is local and ignored by git; delete
`air-monitoring/.cache/bmkg-station-specific-status/` before rerunning if a
fresh live retrieval is required.
