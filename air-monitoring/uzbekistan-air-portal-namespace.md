---
attestation_chain: ai-first
status: Screening Result
method: air_monitoring_uzbekistan_air_portal_namespace_v1
---

# Uzbekistan Air Uzbekistan portal namespace wall

## Why this measurement problem matters

The three Uzbekistan blocker rows are no longer a vague source problem.
They are exact station rows with stale or sentinel measurements on
`monitoring.meteo.uz`. This pass tests whether the newer public
Air Uzbekistan / DigitalMeteo surface supplies a row-level correction
or whether it simply exposes the same stations in a second namespace.

## What the source upgrade adds

- Public source URLs seeded: 4.
- Seeded source URLs retrieved: 4.
- Air Uzbekistan Horiba station objects: 28.
- Alternate station-name matches for the three blockers: 3.
- Original blocker IDs accepted by the Air Uzbekistan detail endpoint: 0.
- Alternate details that mirror the official blocker detail row: 3.
- Public portal blocker-resolution rows: 0.

## Interpretation

Air Uzbekistan improves source observability but does not close the
blocker. The portal station list maps the same station names to
alternate Horiba IDs, and all three alternate detail probes reproduce
the same timestamp and PM2.5 value found on the official detail pages.
The original blocker IDs 107, 728, and 737 are not accepted by that
portal detail endpoint.

## What this does not mean

This scan checks whether a second public Uzbekistan air-quality portal resolves three exact blocker rows. Alternate station IDs, portal active flags, or mirrored pollutant values do not confirm current operating status, station-method classification, calibration status, complete monitor-grade classification, or station-radius readiness unless a public source names the exact blocker row and gives explicit status, correction, or grade language.

## Reproduce

Run `python air-monitoring/scripts/scan-uzbekistan-air-portal-namespace.py`.
The source seed is `air-monitoring/source-inputs/uzbekistan-air-portal-namespace-source-seed.csv`.
Outputs are `air-monitoring/generated/air-monitoring-uzbekistan-air-portal-namespace.csv`
and `air-monitoring/generated/air-monitoring-uzbekistan-air-portal-namespace-summary.json`.
