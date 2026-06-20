---
program: air-monitoring
attestation_chain: ai-first
artifact_type: evidence_note
generated_by: air-monitoring/scripts/scan-bmkg-dashboard-status-sources.py
generated_at: 2026-06-20
status: L3 candidate
---

# BMKG dashboard current-status source scan

## Why This Pass Was Needed

The earlier BMKG station-detail and API checks proved that the 22 Indonesia
PM2.5 rows are visible public telemetry objects and carry BAM method context.
They did not expose an explicit station-status field. The regional status scan
then found one public regional `ONLINE` row for Banjarbaru, but left the other
BMKG rows without current-status closure. This pass tests the official BMKG
climate-information page and its embedded CEWS PM2.5 dashboard because that
dashboard is the public route readers actually see when BMKG presents national
near-real-time PM2.5 monitoring.

## What Changed

The scan retrieves 2 of 2 seeded public sources: the BMKG climate-information
parent page and the embedded CEWS PM2.5 dashboard HTML. The CEWS dashboard
contains a public `dashboardData` object with 26 PM2.5 dashboard locations,
coordinates, latest timestamp, PM2.5 value, category, status, and time-series
values.

The generated artifact matches all 22 target BMKG rows to exact dashboard
locations through curated aliases. It records 22 current dashboard timestamps,
21 rows with explicit `ONLINE` status, 1 row with explicit `DELAYED` status,
21 rows with positive latest PM2.5 values, and 2,640 target-row time-series
observations. The only delayed target row in this run is Pekanbaru
(`pm25_pk2`), which the dashboard reports as `DELAYED`, category
`NOT AVAILABLE`, PM2.5 value 0.0, and timestamp `2026-06-20 07:00:00`.

This is the first BMKG source wall in the package that closes current dashboard
status for most target rows. It does not change the method or grade wall:
current dashboard status is not an inspection log, calibration certificate,
complete monitor-grade classification, same-station OpenAQ crosswalk, or
station-radius denominator.

## What Remains Blocked

The scan records 0 station-specific inspection-log rows, 0 station-specific
calibration-certificate rows, 0 calibration-status rows, 0 complete
monitor-grade rows, and 0 station-radius-ready rows. The dashboard is strong
current-status evidence because it names target locations with explicit status
and current timestamps, but it is still operational telemetry. Complete
monitor-grade promotion still needs station-specific calibration/status or
grade-basis documentation.

## Reproduce the Scan

```powershell
python -m py_compile air-monitoring\scripts\scan-bmkg-dashboard-status-sources.py
python air-monitoring\scripts\scan-bmkg-dashboard-status-sources.py
```

Generated outputs:

- `air-monitoring/generated/air-monitoring-bmkg-dashboard-status-source-scan.csv`
- `air-monitoring/generated/air-monitoring-bmkg-dashboard-status-source-scan-summary.json`
- `air-monitoring/source-inputs/bmkg-dashboard-status-source-seed.csv`

## Next Statistical Upgrade

The next useful BMKG source is not another station-detail page, API scrape, or
dashboard refresh. It is station-specific inspection logs, calibration
certificates, calibration-status records, or official grade-basis evidence for
the 21 rows now carrying current `ONLINE` dashboard status and for Pekanbaru,
which remains a current `DELAYED` status caution row.
