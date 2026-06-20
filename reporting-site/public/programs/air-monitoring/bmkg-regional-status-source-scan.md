---
program: air-monitoring
attestation_chain: ai-first
artifact_type: evidence_note
generated_by: air-monitoring/scripts/scan-bmkg-regional-status-sources.py
generated_at: 2026-06-20
status: L3 candidate
---

# BMKG regional station-status source scan

## Why This Pass Was Needed

The BMKG station-detail and API checks showed that the 22 Indonesia PM2.5 rows
are publicly visible and carry BAM method context, but those central telemetry
surfaces did not expose station-status, inspection-log, calibration-certificate,
or grade fields. This pass tests a narrower question: do regional BMKG pages or
public regulator/public-information sources outside the central detail/API
surfaces close any station-specific status gate?

## What Changed

The scan retrieves 6 of 6 seeded public sources: a Kalimantan Selatan regional
PM2.5 status page, a Kalimantan Selatan UPT profile, a BMKG PPID public
information list, a BMKG PTSP service/tariff page, a BMKG PPID 2024 report,
and a Jakarta environment-agency air-quality report that names BMKG Kemayoran.

The generated artifact records 22 target BMKG rows, 2 rows with exact
station-name external context, and 1 row with regional online status. Banjarbaru
(`pm25_bjb2`) is the only row that closes the current-status gate: the official
Kalimantan Selatan BMKG page names Banjarbaru with latitude -3.475, longitude
114.856, `Status Stasiun: ONLINE`, category `SEDANG`, value 32.9 ug/m3, and
timestamp `20 Jun 2026, 08:00 WITA`.

Kemayoran (`pm25_kmy3`) is named in a public regulator report, but the source
does not provide a station-status, inspection-log, calibration-certificate, or
grade closure. The other 20 target rows do not receive regional station-status
evidence from this seeded pass.

## What Remains Blocked

The current-status gate moves from 0 to 1 row for BMKG, but complete
monitor-grade classification remains blocked. The scan records 0
station-specific inspection-log rows, 0 station-specific calibration-certificate
rows, 0 calibration-status rows, 0 complete monitor-grade rows, and 0
station-radius-ready rows. A public `ONLINE` status on a regional page is useful
status evidence, not a calibration certificate or station-radius denominator.

## Reproduce the Scan

```powershell
python -m py_compile air-monitoring\scripts\scan-bmkg-regional-status-sources.py
python air-monitoring\scripts\scan-bmkg-regional-status-sources.py
```

Generated outputs:

- `air-monitoring/generated/air-monitoring-bmkg-regional-status-source-scan.csv`
- `air-monitoring/generated/air-monitoring-bmkg-regional-status-source-scan-summary.json`
- `air-monitoring/source-inputs/bmkg-regional-status-source-seed.csv`

## Next Statistical Upgrade

The next useful BMKG source is not another central station-detail page or PM2.5
API scrape. It is station-specific inspection logs, calibration certificates,
calibration-status records, or official grade-basis evidence for the remaining
BMKG rows, starting with rows that already have exact regional or regulator
context.
