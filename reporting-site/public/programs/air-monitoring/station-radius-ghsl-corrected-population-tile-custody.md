# Station-radius GHSL corrected population tile custody gate

`attestation_chain: ai-first`

Generated: 2026-06-20T12:59:04Z

## What this adds

This pass moves from the corrected routing queue to corrected tile custody. It probes the corrected GHSL URLs, reuses retained cached ZIP files, retries first-wave candidates, records SHA-256 hashes, and checks opened raster bounds against the corrected origin.

## First-wave rule

Probe the corrected selected GHSL tile URLs; download only rows with current public size at or below 60 MB; reuse retained cached ZIPs; keep all unresolved corrected selected rows as blockers.

## Summary counts

| Measure | Count |
|---|---:|
| corrected tile rows | 21 |
| retained corrected tile rows | 20 |
| added corrected tile rows | 1 |
| current head ok tiles | 21 |
| current range ok tiles | 0 |
| current probe size available tiles | 21 |
| corrected first wave eligible rows | 18 |
| corrected first wave download candidate rows | 0 |
| downloaded population tile files | 18 |
| downloaded population tile files this run | 0 |
| downloaded population tile files from prior cache | 18 |
| sha256 checksummed population tile files | 18 |
| sha256 matches prior rows | 3 |
| downloaded size bytes total | 464408064 |
| downloaded size mb total | 464.408 |
| zip files opened | 18 |
| geotiff opened files | 18 |
| geotiff transform matches corrected bounds | 18 |
| geotiff transform mismatch corrected bounds | 0 |
| blocked corrected selected tiles | 0 |
| deferred corrected selected tiles | 3 |
| station radius population rows | 0 |
| station radius pm25 exposure rows | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Corrected GHSL tile queue | 21 | available |
| Current public URL probes | 21 | available |
| Corrected first-wave eligible tiles | 18 | available |
| Corrected population tile ZIP custody | 18 | limited |
| Corrected population tile SHA-256 checksums | 18 | available |
| Corrected-bound GeoTIFF inspection | 18 | available |
| Deferred large corrected tiles | 3 | limited |
| Blocked corrected selected tiles | 0 | available |
| Station-radius population computation | 0 | not_computed |

## Corrected queue custody rows

| Tile | Correction | Economies | Probe | Decision | Downloaded | SHA-256 | Corrected bounds match |
|---|---|---|---|---|---:|---|---:|
| R5_C23 | retained_by_corrected_origin | AZE||GEO | head 49.399 MB | retained_corrected_queue_cached_zip | True | `c1ed4e4c7b285b9c90c1d6a177e2e0bda5dc5b02f966e2d8c8bf28fd540e6360` | True |
| R5_C24 | retained_by_corrected_origin | AZE||UZB | head 10.359 MB | retained_corrected_queue_cached_zip | True | `33774a300fe3c9d91113b136b861d3e9cd4a84ab6d6740ce9b4da7ff3e042669` | True |
| R5_C25 | retained_by_corrected_origin | TJK||UZB | head 33.35 MB | retained_corrected_queue_cached_zip | True | `dada5ad3d739fc79fbda3c27b0f2e848b7165db5a371b2a9b8aa0419bd1bf5c0` | True |
| R5_C26 | retained_by_corrected_origin | TJK||UZB | head 32.99 MB | retained_corrected_queue_cached_zip | True | `335a745dda9aae8dc944928afc57045f90f7a3613621ed66f8a51ff576db7ceb` | True |
| R6_C24 | retained_by_corrected_origin | TKM | head 29.701 MB | retained_corrected_queue_cached_zip | True | `9a4b608a64a02aebc3205d264717bd090f07ebb5f93f213cfa42c89c59c249c8` | True |
| R6_C25 | retained_by_corrected_origin | AFG||TJK||UZB | head 35.542 MB | retained_corrected_queue_cached_zip | True | `f5f11f0568e85fd1ca28d08c69d9737b43d067a7a773efd64b717bee1f2f9850` | True |
| R7_C27 | retained_by_corrected_origin | BGD | head 262.283 MB | deferred_corrected_tile_over_first_wave_size_threshold | False |  |  |
| R7_C28 | retained_by_corrected_origin | BGD | head 100.278 MB | deferred_corrected_tile_over_first_wave_size_threshold | False |  |  |
| R8_C26 | retained_by_corrected_origin | LKA | head 159.28 MB | deferred_corrected_tile_over_first_wave_size_threshold | False |  |  |
| R8_C27 | retained_by_corrected_origin | LKA | head 20.948 MB | retained_corrected_queue_cached_zip | True | `4ce3a1e60339b3f64869b16c7e23c32f3ae7f07dba2416fc5e3f830ee112d82a` | True |
| R8_C28 | retained_by_corrected_origin | MMR | head 34.371 MB | retained_corrected_queue_cached_zip | True | `91502e9dbb6d24be9cadd707469a17b2ad837974e63ffd8a137aa32f9a273fb0` | True |
| R9_C26 | retained_by_corrected_origin | LKA | head 9.358 MB | retained_corrected_queue_cached_zip | True | `d1064a04cfa2405533d17296217f4c1a95cd71ac0656dae87538388da0df8981` | True |
| R9_C27 | retained_by_corrected_origin | LKA | head 18.479 MB | retained_corrected_queue_cached_zip | True | `c70a2c731bb4503d10189d6aedd303f6c89d714a89377ee51d4ef156fdd345d6` | True |
| R9_C28 | retained_by_corrected_origin | IDN||MYS | head 20.613 MB | retained_corrected_queue_cached_zip | True | `8841958ed8e260c72081ccaa146333889800425ffb7fa9a9cf4fbe3f27d7362e` | True |
| R9_C29 | retained_by_corrected_origin | IDN||MYS | head 37.524 MB | retained_corrected_queue_cached_zip | True | `21b11a50f7bdc5fee19417d2049cb36e743fb99d46c9da6667d019b4c4cd6428` | True |
| R9_C30 | retained_by_corrected_origin | IDN||MYS | head 16.003 MB | retained_corrected_queue_cached_zip | True | `7d916fdda72322f4ec018b2931b3e6d9f6d1b6a8e397af4d9118684db3c9c335` | True |
| R9_C32 | added_by_corrected_origin | IDN | head 1.941 MB | retained_corrected_queue_cached_zip | True | `626964eb26014a3a5ccd1dc3a0354d1db86b81be06b5a310c674197af4513905` | True |
| R10_C29 | retained_by_corrected_origin | IDN | head 43.067 MB | retained_corrected_queue_cached_zip | True | `845f0ab2190e32c862c8ee6695e99d9dcd5d17547c389c89ad221cd6f11727f5` | True |
| R10_C30 | retained_by_corrected_origin | IDN | head 50.049 MB | retained_corrected_queue_cached_zip | True | `e6e30b1030807596ebd1da9caa4e8b660162b23eba28a87d4b2e41733882a327` | True |
| R10_C31 | retained_by_corrected_origin | IDN | head 16.285 MB | retained_corrected_queue_cached_zip | True | `b67ce516f5a4bfa999f7401521a4a1cb3add9002d8d43833da7bc24bc264e97b` | True |
| R10_C32 | retained_by_corrected_origin | IDN | head 4.431 MB | retained_corrected_queue_cached_zip | True | `9f8c090b098ab0434f9e7ba5c73d91532e70c88d2e0b923f896a3711196204db` | True |

## Cache policy

Raw GHSL ZIP files are stored under air-monitoring/.cache/station-radius-ghsl-population-tiles/ and are not committed; rerun this script to rehydrate them from public GHSL tile URLs.

## Non-claim

This corrected-queue GHSL population tile custody gate probes the corrected tile URLs, reuses or downloads ZIP files, records SHA-256 hashes, and checks opened GeoTIFF bounds against the corrected GHSL tile origin. It does not compute station-radius population, compute PM2.5 exposure, validate same-station joins, freeze radius or de-duplication rules, or promote monitor-grade rows.
