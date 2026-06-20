# Air Monitoring Station-Radius PM2.5 Resolution Decision

attestation_chain: ai-first

## Status

This gate freezes the PM2.5 grid-resolution lane before any station-radius denominator dry run. The selected first dry-run surface is V6.GL.03 2023 0.10 degree coarse annual PM2.5.

## Evidence Counts

| Check | Count |
|---|---:|
| Check-summed coarse PM2.5 files | 2 |
| Files with PM25(lat,lon) metadata | 2 |
| Selected primary dry-run PM2.5 surface | 1 |
| Consistency-lane PM2.5 surfaces | 1 |
| PM2.5 exposure rows | 0 |

## Frozen Resolution Decision

| Element | Value |
|---|---|
| Selected version | V6.GL.03 |
| Selected vintage | 2023 |
| Selected resolution | 0.10 degree coarse annual |
| Primary dry-run file | v6gl03_gl_coarse_annual |
| Consistency lane | v6gl03_as_coarse_annual |
| Deferred lanes | fine-resolution ACAG objects and visible 2024 V6.GL.03 annual objects |
| Claim guardrail | Use the grid only as a coarse annual contextual PM2.5 denominator for a dry run. Do not report station catchment exposure, monitor coverage, or neighborhood-scale measured concentration from this gate. |

## Decision Rows

| Decision | Role | Status | Grid | File | Reader use |
|---|---|---|---|---|---|
| v6gl03_gl_coarse_annual_pm25_resolution | primary_dry_run_pm25_surface | frozen_for_dry_run | global_coarse | v6gl03_gl_coarse_annual | Use the check-summed 2023 V6.GL.03 global coarse PM2.5 grid as the first dry-run pollutant surface. |
| v6gl03_as_coarse_annual_pm25_resolution | regional_consistency_pm25_surface | frozen_consistency_lane | asia_coarse | v6gl03_as_coarse_annual | Retain the check-summed 2023 V6.GL.03 Asia coarse grid as a consistency lane. |

## Gate Ledger

| Gate | Status | Rows | Reader use |
|---|---|---:|---|
| ACAG current-version decision | available | 9 | Confirms V6.GL.03 2023 coarse PM2.5 objects are the pinned first-wave lane. |
| ACAG coarse checksum custody | available | 2 | Confirms the two coarse NetCDF files are downloaded, check-summed, and metadata-opened. |
| Radius rule | available | 4 | Confirms the 4 km primary and 0.5/50 km sensitivity bands are source-frozen. |
| PM2.5 denominator join | not_computed | 0 | No station-radius PM2.5 exposure rows are computed in this decision gate. |

## What This Does Not Mean

This PM2.5 resolution decision freezes the coarse annual ACAG grid lane for a future denominator dry run. It does not compute PM2.5 exposure, station buffers, catchment population, monitor coverage, validated same-station joins, or complete monitor-grade classification.

## Reproduce

```powershell
python air-monitoring\scripts\build-station-radius-pm25-resolution-decision.py
```
