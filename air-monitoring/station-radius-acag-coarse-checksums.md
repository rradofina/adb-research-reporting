# Station-radius ACAG coarse checksum gate

`attestation_chain: ai-first`

Generated: 2026-06-20T10:59:31Z

## What this adds

This pass downloads the two approved 2023 ACAG V6.GL.03 coarse NetCDF objects into the ignored local cache, computes SHA-256 hashes, and records NetCDF dimensions and variables before any exposure or catchment computation.

## Summary counts

| Measure | Count |
|---|---:|
| approved coarse candidate files | 2 |
| downloaded files | 2 |
| downloaded this run | 0 |
| sha256 checksummed files | 2 |
| size matches expected files | 2 |
| netcdf files opened | 2 |
| files with pm25 variable candidates | 2 |
| files with lat lon coordinate variables | 2 |
| population denominator files selected | 0 |
| population denominator files downloaded | 0 |
| station radius pm25 exposure rows | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Approved coarse ACAG files downloaded | 2 | available |
| SHA-256 checksum ledger | 2 | available |
| NetCDF variable metadata | 2 | available |
| Population denominator selection | 0 | not_ready |
| Station-radius exposure computation | 0 | not_ready |
| Station joins and monitor-grade closure | 0 | not_ready |

## Checksum rows

| Record | Size bytes | SHA-256 | Dimensions | PM2.5 variable candidates | Decision |
|---|---:|---|---|---|---|
| v6gl03_as_coarse_annual | 1098264 | `d2be821db5eb03c2babbc671fd21914ffa9fa5608fcdf400fd6fc9526022f8b0` | lat:700||lon:800 | PM25 | metadata_ready_for_method_freeze |
| v6gl03_gl_coarse_annual | 5201631 | `89ae44c70d939a5ae5ed298264e026fc3ce50e3af76ba3de53ba51c11d34a8e3` | lat:1300||lon:3600 | PM25 | metadata_ready_for_method_freeze |

## Cache policy

Raw NetCDF files are stored under air-monitoring/.cache/station-radius-acag-coarse-checksums/ and are not committed; rerun the script to rehydrate them from public S3 object URLs.

## Non-claim

This ACAG coarse checksum pass downloads and hashes only the two approved 2023 V6.GL.03 coarse PM2.5 pilot objects and inspects NetCDF metadata. It does not download fine-resolution PM2.5 files; does not select or download a population denominator; does not compute PM2.5 exposure, station catchments, or station-radius population; does not validate same-station joins; and does not promote monitor-grade rows.
