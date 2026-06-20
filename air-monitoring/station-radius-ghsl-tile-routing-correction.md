# Station-radius GHSL tile-routing correction gate

`attestation_chain: ai-first`

Generated: 2026-06-20T12:18:54Z

## What this adds

This pass uses the four opened GHSL GeoTIFF bounds from the checksum gate to derive the actual R/C tile-routing origin. It then reruns the existing 50 km coordinate buffer against that origin and records how the selected population tile queue changes.

## Routing rule

Use the mean origin derived from opened GHSL GeoTIFF bounds: north_origin=89.09958351, west_origin=-180.00791704, then assign R/C with floor((north_origin - latitude)/10)+1 and floor((longitude - west_origin)/10)+1 before applying the same 50 km draft buffer.

## Summary counts

| Measure | Count |
|---|---:|
| coordinate ready economies | 11 |
| coordinate rows used | 277 |
| openaq coordinate rows used | 101 |
| official pm25 coordinate rows used | 176 |
| origin observation rows | 4 |
| observed north origin | 89.09958351 |
| observed west origin | -180.00791704 |
| north origin range degrees | 8e-08 |
| west origin range degrees | 8e-08 |
| previous tile urls selected | 23 |
| corrected tile urls selected | 21 |
| retained previous tile urls | 20 |
| added corrected tile urls | 1 |
| removed previous tile urls | 3 |
| corrected tile prior head ok | 6 |
| corrected tile prior head not ok | 14 |
| corrected tile prior head unknown | 1 |
| downloaded population tiles retained by corrected routing | 3 |
| downloaded population tiles removed by corrected routing | 1 |
| station radius population rows | 0 |
| station radius pm25 exposure rows | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Observed GHSL raster origin | 4 | available |
| Origin consistency check | 4 | available |
| Corrected GHSL tile queue | 21 | available |
| Retained selected tile URLs | 20 | available |
| New corrected tile URLs needing custody | 1 | limited |
| Removed previous tile URLs | 3 | limited |
| Station-radius population computation | 0 | not_computed |

## Queue changes

- Retained previous tile IDs: `R10_C29||R10_C30||R10_C31||R10_C32||R5_C23||R5_C24||R5_C25||R5_C26||R6_C24||R6_C25||R7_C27||R7_C28||R8_C26||R8_C27||R8_C28||R9_C26||R9_C27||R9_C28||R9_C29||R9_C30`
- Added corrected tile IDs: `R9_C32`
- Removed previous tile IDs: `R10_C28||R6_C23||R6_C26`

## Origin evidence

| Tile | Raster bounds | Derived north origin | Derived west origin |
|---|---|---:|---:|
| R8_C28 | `89.992083,9.0995835,99.99208296,19.09958346` | 89.09958346 | -180.007917 |
| R9_C30 | `109.99208292,-0.90041646,119.99208288,9.0995835` | 89.0995835 | -180.00791708 |
| R10_C28 | `89.992083,-10.90041642,99.99208296,-0.90041646` | 89.09958354 | -180.007917 |
| R10_C30 | `109.99208292,-10.90041642,119.99208288,-0.90041646` | 89.09958354 | -180.00791708 |

## Corrected tile queue

| Tile | Status | Corrected economies | Corrected coordinate rows | Prior HEAD | Prior downloaded |
|---|---|---|---:|---:|---:|
| R5_C23 | retained_by_corrected_origin | AZE||GEO | 20 | False | False |
| R5_C24 | retained_by_corrected_origin | AZE||UZB | 3 | False | False |
| R5_C25 | retained_by_corrected_origin | TJK||UZB | 42 | True | False |
| R5_C26 | retained_by_corrected_origin | TJK||UZB | 16 | True | False |
| R6_C23 | removed_by_corrected_origin | AZE | 0 | False | False |
| R6_C24 | retained_by_corrected_origin | TKM | 2 | False | False |
| R6_C25 | retained_by_corrected_origin | AFG||TJK||UZB | 9 | False | False |
| R6_C26 | removed_by_corrected_origin | TJK||UZB | 0 | False | False |
| R7_C27 | retained_by_corrected_origin | BGD | 40 | False | False |
| R7_C28 | retained_by_corrected_origin | BGD | 48 | False | False |
| R8_C26 | retained_by_corrected_origin | LKA | 1 | False | False |
| R8_C27 | retained_by_corrected_origin | LKA | 1 | True | False |
| R8_C28 | retained_by_corrected_origin | MMR | 3 | True | True |
| R9_C26 | retained_by_corrected_origin | LKA | 2 | False | False |
| R9_C27 | retained_by_corrected_origin | LKA | 2 | False | False |
| R9_C28 | retained_by_corrected_origin | IDN||MYS | 13 | False | False |
| R9_C29 | retained_by_corrected_origin | IDN||MYS | 71 | False | False |
| R9_C30 | retained_by_corrected_origin | IDN||MYS | 23 | True | True |
| R9_C32 | added_by_corrected_origin | IDN | 1 |  |  |
| R10_C28 | removed_by_corrected_origin | IDN | 0 | True | True |
| R10_C29 | retained_by_corrected_origin | IDN | 39 | False | False |
| R10_C30 | retained_by_corrected_origin | IDN | 13 | True | True |
| R10_C31 | retained_by_corrected_origin | IDN | 1 | False | False |
| R10_C32 | retained_by_corrected_origin | IDN | 1 | False | False |

## Non-claim

This GHSL tile-routing correction gate derives an observed R/C grid origin from already downloaded GHSL GeoTIFF bounds, recomputes the station-coordinate tile queue with the same 50 km draft buffer, and records which selected tile IDs are retained, added, or removed. It does not download newly added tiles, retry HEAD probes, compute station-radius population, compute PM2.5 exposure, validate same-station joins, freeze radius or de-duplication rules, or promote monitor-grade rows.
