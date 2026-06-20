---
attestation_chain: ai-first
status: computed_bmkg_installation_audit_source_scan
method: air_monitoring_bmkg_installation_audit_source_scan_v1
---

# BMKG Installation and Audit Source Scan

## Why this source pass was needed

The BMKG station public-context scan found station studies, station-unit
publications, regulator context, and deployment context, but it did not find
station-specific inspection logs, calibration certificates, calibration status,
or complete monitor-grade closure.

This pass tests a narrower official source family: BMKG installation,
audit/calibration, public-information, and operational-monitoring routes.

## Sources tested

The source seed is
`air-monitoring/source-inputs/bmkg-installation-audit-source-seed.csv`.

The scan tests an official BMKG GAW Bukit Kototabang article with WMO audit and
calibration language, the BMKG 2020 annual report PM2.5 installation section,
a BMKG routine-calibration article, a BMKG Network Operations Center article,
the BMKG PPID public-information list, and the BMKG AWS Center landing page.

## What the scan records

The generated output records, for each of the 22 BMKG target rows:

- whether an official source names the exact station with audit/calibration
  context;
- whether an official source links the row to PM2.5 installation or deployment
  wording;
- whether source-level operational or calibration routes exist; and
- whether any row has station-specific inspection-log, calibration-certificate,
  calibration-status, complete-grade, or station-radius closure.

The closure gates remain zero unless the public source provides a target-station
record.

## How to use this result

Use this scan as a stronger official-source context layer. It adds one exact
station audit/calibration context row for Kototabang and official PM2.5
installation/deployment context for seven rows. It still cannot promote any row
to complete monitor-grade because installation, audit, NOC, PPID, and source
program context are not station-specific calibration certificates or inspection
logs.

## What this does not mean

This scan does not certify current calibration for any target BMKG PM2.5 row. It
does not provide a station-specific inspection log. It does not resolve
calibration status. It does not support station-radius or catchment coverage.

## Reproduce

```powershell
python -m py_compile air-monitoring\scripts\scan-bmkg-installation-audit-sources.py
python air-monitoring\scripts\scan-bmkg-installation-audit-sources.py
```

Outputs:

- `air-monitoring/generated/air-monitoring-bmkg-installation-audit-source-scan.csv`
- `air-monitoring/generated/air-monitoring-bmkg-installation-audit-source-scan-summary.json`
