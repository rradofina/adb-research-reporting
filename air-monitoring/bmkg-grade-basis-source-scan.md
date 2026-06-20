---
attestation_chain: ai-first
status: computed_bmkg_grade_basis_source_scan
method: air_monitoring_bmkg_grade_basis_source_scan_v1
---

# BMKG Grade-Basis Source Scan

## Why this source pass was needed

The BMKG dashboard scan made the current public status surface much clearer: 21
of 22 target rows were `ONLINE` on the official dashboard and Pekanbaru was
`DELAYED`. That still did not answer the station-grade question. A station can
have visible PM2.5 telemetry and still lack public evidence of its inspection
log, calibration certificate, calibration status, or complete monitor-grade
classification.

This pass therefore searches the evidence layer behind the telemetry: official
BMKG regulations, operating standards, SOPs, service/tariff routes, PPID
reports, and annual-report context.

## Sources tested

The source seed is
`air-monitoring/source-inputs/bmkg-grade-basis-source-seed.csv`.

The script retrieved 10 of 10 seeded official/public BMKG sources:

- 3 official standard, observation-rule, or SOP sources.
- 3 official service or tariff sources.
- 4 PPID, public-information, annual-report, or public-report sources.

The retrieval output is recorded in
`air-monitoring/generated/air-monitoring-bmkg-grade-basis-source-scan-summary.json`.

## What the scan found

Across the 22 BMKG target rows, the scan found source-level context but no
station-level certificate closure:

- 8 sources with BAM or PM2.5 method-basis terms.
- 7 sources with technical or operational standard terms.
- 3 sources with daily inspection or logbook rule context.
- 2 sources with periodic calibration rule context.
- 2 sources with public BAM calibration service or tariff context.
- 2 sources with certificate-request or certificate-output context at agency or
  PPID level.
- 0 rows with a public target-station inspection log.
- 0 rows with a public target-station calibration certificate or calibration
  status record.
- 0 rows with complete monitor-grade classification.
- 0 rows ready for station-radius grade assumptions.

## How to use this result

This is useful evidence, but it is not a promotion gate. It shows that the BMKG
source wall is no longer missing basic method and operational context: the
public record contains method, inspection, logbook, calibration, and service
language. The remaining blocker is more precise. A reviewer now needs a public
row-level source that names the exact BMKG station or station code and provides
the inspection log, calibration certificate/status, or complete grade basis.

## What this does not mean

The result does not certify any of the 22 BMKG stations as complete
monitor-grade rows. It does not prove calibration is current for any station.
It does not provide an inspection log. It does not support station-radius or
catchment coverage. Source-level standards stay in the evidence ladder; they do
not become station-level claims.

## Reproduce

```powershell
python -m py_compile air-monitoring\scripts\scan-bmkg-grade-basis-sources.py
python air-monitoring\scripts\scan-bmkg-grade-basis-sources.py
```

Outputs:

- `air-monitoring/generated/air-monitoring-bmkg-grade-basis-source-scan.csv`
- `air-monitoring/generated/air-monitoring-bmkg-grade-basis-source-scan-summary.json`
