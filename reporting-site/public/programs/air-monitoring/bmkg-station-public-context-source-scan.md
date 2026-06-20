---
attestation_chain: ai-first
status: computed_bmkg_station_public_context_source_scan
method: air_monitoring_bmkg_station_public_context_source_scan_v1
---

# BMKG Station Public-Context Source Scan

## Why this source pass was needed

The BMKG grade-basis scan established that public BMKG standards, SOPs, service
pages, PPID reports, and annual reports contain method, inspection, logbook,
calibration, service-route, and certificate-request context. The unresolved
question is narrower: whether public station-unit publications, local BMKG
PM2.5 report pages, local bulletins, regulator reports, or station studies name
exact BMKG PM2.5 station units and provide station-level support.

This pass tests that source family without treating station context as
certification.

## Sources tested

The source seed is
`air-monitoring/source-inputs/bmkg-station-public-context-source-seed.csv`.

The scan tests station-unit publications from GAW Bukit Kototabang, official
local PM2.5 pages and bulletins from Kalbar, Bengkulu, Sumsel, and Kemayoran,
public station studies for Jambi, Sorong, and West Kalimantan, a Jakarta
regulator report naming BMKG Kemayoran, and a BMKG performance report that
lists PM2.5 deployment areas.

## What the scan records

The generated output records, for each of the 22 BMKG target rows:

- whether a public source names the exact station or station unit;
- whether a public source only names a city or deployment area;
- whether the matched source contains BAM/PM2.5 method terms;
- whether it contains calibration, inspection, operation, status, or certificate
  language; and
- whether any row has station-specific inspection-log, calibration-certificate,
  calibration-status, complete-grade, or station-radius closure.

The last set of closure gates remains zero unless the source provides an actual
row-level station record.

## How to use this result

Use the scan as a station-context layer. It can strengthen the evidence trail
for rows where public station/unit material confirms the station, reporting
activity, and BAM-1020 method context. It still cannot promote any station to
complete monitor-grade because a local PM2.5 report, station study, city
deployment note, or historical unit publication is not a current calibration
certificate or inspection log.

## What this does not mean

This scan does not certify that any BMKG station is currently calibrated. It
does not provide a station-specific inspection log. It does not resolve
calibration status. It does not support station-radius or catchment coverage.

## Reproduce

```powershell
python -m py_compile air-monitoring\scripts\scan-bmkg-station-public-context-sources.py
python air-monitoring\scripts\scan-bmkg-station-public-context-sources.py
```

Outputs:

- `air-monitoring/generated/air-monitoring-bmkg-station-public-context-source-scan.csv`
- `air-monitoring/generated/air-monitoring-bmkg-station-public-context-source-scan-summary.json`
