# Station-radius GHSL population tile checksum gate

`attestation_chain: ai-first`

Generated: 2026-06-20T11:52:14Z

## What this adds

This pass downloads and hashes the first wave of selected GHSL population tile ZIP files, then inspects the GeoTIFF transform inside each downloaded ZIP. Selected tiles whose HEAD probes did not close remain explicit blockers.

## First-wave rule

Download only selected GHSL tile rows with successful HEAD metadata and recorded size at or below 60 MB; keep all other selected tile rows as blockers.

## Summary counts

| Measure | Count |
|---|---:|
| selected tile rows | 23 |
| first wave download candidate rows | 7 |
| downloaded population tile files | 4 |
| downloaded population tile files this run | 1 |
| sha256 checksummed population tile files | 4 |
| downloaded size bytes total | 102118404 |
| downloaded size mb total | 102.118 |
| zip files opened | 4 |
| geotiff members found | 4 |
| geotiff transform inspected files | 4 |
| geotiff transform matches 10 degree tile bounds | 0 |
| geotiff transform mismatch files | 4 |
| selected head not ok blocked tiles | 16 |
| station radius population rows | 0 |
| station radius pm25 exposure rows | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Selected GHSL tile queue | 23 | available |
| First-wave downloadable tiles | 7 | available |
| Population tile ZIP downloads | 4 | limited |
| Population tile SHA-256 checksums | 4 | available |
| GeoTIFF transform inspection | 4 | available |
| 10-degree routing assumption check | 0 | limited |
| Selected HEAD-failed tile blockers | 16 | limited |
| Station-radius population computation | 0 | not_computed |

## Tile custody rows

| Tile | Economies | Decision | Downloaded | SHA-256 | GeoTIFF opened | Bounds match |
|---|---|---|---:|---|---:|---:|
| R5_C23 | AZE||GEO | blocked_selected_tile_head_not_ok | False |  |  |  |
| R5_C24 | AZE||UZB | blocked_selected_tile_head_not_ok | False |  |  |  |
| R5_C25 | TJK||UZB | selected_first_wave_download_candidate | False |  |  |  |
| R5_C26 | TJK||UZB | selected_first_wave_download_candidate | False |  |  |  |
| R6_C23 | AZE | blocked_selected_tile_head_not_ok | False |  |  |  |
| R6_C24 | AZE||TKM | blocked_selected_tile_head_not_ok | False |  |  |  |
| R6_C25 | AFG||TJK||UZB | blocked_selected_tile_head_not_ok | False |  |  |  |
| R6_C26 | TJK||UZB | blocked_selected_tile_head_not_ok | False |  |  |  |
| R7_C27 | BGD | blocked_selected_tile_head_not_ok | False |  |  |  |
| R7_C28 | BGD | blocked_selected_tile_head_not_ok | False |  |  |  |
| R8_C26 | LKA | blocked_selected_tile_head_not_ok | False |  |  |  |
| R8_C27 | LKA | selected_first_wave_download_candidate | False |  |  |  |
| R8_C28 | MMR | selected_first_wave_download_candidate | True | `91502e9dbb6d24be9cadd707469a17b2ad837974e63ffd8a137aa32f9a273fb0` | True | False |
| R9_C26 | LKA | blocked_selected_tile_head_not_ok | False |  |  |  |
| R9_C27 | LKA | blocked_selected_tile_head_not_ok | False |  |  |  |
| R9_C28 | IDN||MYS | blocked_selected_tile_head_not_ok | False |  |  |  |
| R9_C29 | IDN||MYS | blocked_selected_tile_head_not_ok | False |  |  |  |
| R9_C30 | IDN||MYS | selected_first_wave_download_candidate | True | `7d916fdda72322f4ec018b2931b3e6d9f6d1b6a8e397af4d9118684db3c9c335` | True | False |
| R10_C28 | IDN | selected_first_wave_download_candidate | True | `f41af3262aa9528a27c7440183f717f89081990626d0abb7816c33634fc4959b` | True | False |
| R10_C29 | IDN | blocked_selected_tile_head_not_ok | False |  |  |  |
| R10_C30 | IDN | selected_first_wave_download_candidate | True | `e6e30b1030807596ebd1da9caa4e8b660162b23eba28a87d4b2e41733882a327` | True | False |
| R10_C31 | IDN | blocked_selected_tile_head_not_ok | False |  |  |  |
| R10_C32 | IDN | blocked_selected_tile_head_not_ok | False |  |  |  |

## Cache policy

Raw GHSL ZIP files are stored under air-monitoring/.cache/station-radius-ghsl-population-tiles/ and are not committed; rerun this script to rehydrate them from public GHSL tile URLs.

## Non-claim

This GHSL population tile checksum gate downloads, hashes, and inspects only selected GHSL tile ZIP files whose HEAD metadata already closed and whose recorded size is within the first-wave custody threshold. It does not download selected HEAD-failed tiles, compute station-radius population, compute PM2.5 exposure, validate same-station joins, freeze radius or de-duplication rules, or promote monitor-grade rows.
