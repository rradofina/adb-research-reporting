# Air Monitoring Station-Radius Method Prefreeze

attestation_chain: ai-first

## Status

This is a method prefreeze, not a coverage result. The package now has corrected GHSL population file custody for 21 of 21 selected tiles and 2 ACAG coarse PM2.5 files in custody, but a station-radius map remains blocked until radius, join, and grade assumptions are closed.

## Evidence Gates

| Gate | Status | Rows | Reader use |
|---|---:|---:|---|
| Coordinate input universe | prefrozen | 277 | Committed OpenAQ and official PM2.5 coordinate rows define the dry-run universe. |
| Unique coordinate points | prefrozen | 275 | Exact duplicate coordinate points are visible before any buffer union. |
| Corrected GHSL population tile custody | available | 21 | All selected corrected population tiles are downloaded or reused, hashed, and bounds-checked. |
| ACAG coarse PM2.5 custody | available_for_pilot | 2 | Coarse 2023 PM2.5 files are inspectable, but final exposure resolution is not frozen. |
| Primary radius and sensitivity rule | not_ready | 0 | The 50 km tile envelope is not yet a reporting radius. |
| Validated official/OpenAQ same-station joins | not_ready | 0 | No candidate proximity/name row is promoted to a station identity join. |
| Complete monitor-grade classification | not_ready | 0 | No station row can be used as complete regulatory-grade coverage evidence yet. |
| Station-radius population/exposure computation | not_computed | 0 | No catchment population, PM2.5 exposure, or map exists in this gate. |

## Method Rules

| Rule | Status | Frozen for next compute | Decision |
|---|---:|---:|---|
| Coordinate input universe | prefrozen | True | Future dry runs may use only committed OpenAQ coordinate rows accepted by the station-metadata gate and official PM2.5 coordinate rows accepted by the regulator extraction gate. |
| GHSL population file custody | available | True | Use the corrected GHSL R2023A 2020 4326 3ss tile set already downloaded, hashed, and bounds-checked; do not substitute older or unverified population files. |
| ACAG coarse PM2.5 file custody | available_for_pilot | False | Keep the two checked ACAG V6.GL.03 2023 coarse files as a pilot exposure denominator only; final exposure claims need an explicit resolution decision and join method. |
| Radius reporting rule | not_frozen | False | The 50 km value used so far is only the maximum tile-selection envelope. A primary reporting radius and sensitivity bands must be sourced and frozen before any population count is shown. |
| Catchment de-duplication rule | prefrozen | True | Future catchment population must union overlapping buffers by economy before summing population; exact duplicate coordinate points must not duplicate people. |
| Official/OpenAQ station-identity join rule | blocked | False | Do not merge OpenAQ and official station rows by proximity or name alone. Candidate rows stay source-family separated unless a public station ID, source-owner crosswalk, or other explicit validation is added. |
| Monitor-grade use rule | blocked | False | Do not label rows as regulatory-grade monitor coverage until exact station method, current status, and grade/calibration evidence are closed. |
| Public headline rule | blocked | False | No public headline may state population covered, exposed, or monitored until radius, de-duplication, join, grade, and sensitivity gates are computed from committed artifacts. |

## Country Prefreeze Rows

| Economy | Coordinate rows | Unique points | Corrected GHSL tiles | Tile custody | Next blocker |
|---|---:|---:|---:|---:|---|
| AFG | 2 | 2 | 1 | 1/1 | radius_join_grade_rules_not_closed |
| AZE | 2 | 2 | 2 | 2/2 | radius_join_grade_rules_not_closed |
| BGD | 53 | 52 | 2 | 2/2 | radius_join_grade_rules_not_closed |
| GEO | 18 | 18 | 1 | 1/1 | radius_join_grade_rules_not_closed |
| IDN | 58 | 58 | 8 | 8/8 | radius_join_grade_rules_not_closed |
| LKA | 3 | 3 | 4 | 4/4 | radius_join_grade_rules_not_closed |
| MMR | 3 | 3 | 1 | 1/1 | radius_join_grade_rules_not_closed |
| MYS | 85 | 84 | 3 | 3/3 | radius_join_grade_rules_not_closed |
| TJK | 7 | 7 | 3 | 3/3 | radius_join_grade_rules_not_closed |
| TKM | 2 | 2 | 1 | 1/1 | radius_join_grade_rules_not_closed |
| UZB | 44 | 44 | 4 | 4/4 | radius_join_grade_rules_not_closed |

## What This Does Not Mean

This method prefreeze ledger records which station-radius inputs and rules are ready for a future dry run and which gates still block a reader-facing coverage claim. It does not compute station-radius population, PM2.5 exposure, monitor coverage, same-station joins, or complete monitor-grade classification.

## Reproduce

```powershell
python air-monitoring\scripts\build-station-radius-method-prefreeze.py
```
