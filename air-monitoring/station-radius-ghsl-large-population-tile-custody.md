# Station-radius GHSL large population tile custody gate

`attestation_chain: ai-first`

Generated: 2026-06-20T13:30:26Z

## What this adds

This pass targets the corrected selected GHSL population tiles that were too large for the first-wave custody gate. It downloads or reuses those large ZIP files, records SHA-256 hashes, and checks opened GeoTIFF bounds against the corrected GHSL tile origin.

## Target rule

Download and inspect only corrected selected GHSL population tiles deferred by the 60 MB first-wave rule.

## Summary counts

| Measure | Count |
|---|---:|
| large corrected tile rows | 3 |
| current head ok large tiles | 3 |
| downloaded large population tile files | 3 |
| downloaded large population tile files this run | 1 |
| downloaded large population tile files from prior cache | 2 |
| sha256 checksummed large population tile files | 3 |
| downloaded large size bytes total | 521841319 |
| downloaded large size mb total | 521.841 |
| large zip files opened | 3 |
| large geotiff opened files | 3 |
| large geotiff transform matches corrected bounds | 3 |
| large geotiff transform mismatch corrected bounds | 0 |
| remaining large tile blockers | 0 |
| first wave corrected tile files in custody | 18 |
| corrected tile files in custody after large pass | 21 |
| corrected tile files required | 21 |
| station radius population rows | 0 |
| station radius pm25 exposure rows | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Deferred large corrected tile queue | 3 | available |
| Large corrected tile current URL probes | 3 | available |
| Large corrected population ZIP custody | 3 | available |
| Large corrected population SHA-256 checksums | 3 | available |
| Large corrected-bound GeoTIFF inspection | 3 | available |
| Full corrected GHSL population file custody | 21 | available |
| Station-radius population computation | 0 | not_computed |

## Large tile custody rows

| Tile | Economies | Probe | Downloaded | SHA-256 | Corrected bounds match |
|---|---|---|---:|---|---:|
| R7_C27 | BGD | head 262.283 MB | True | `c385b33300f3a2f2e4615519b79e799e9e1a130ff5a8505d7dda9216f9a55a3f` | True |
| R7_C28 | BGD | head 100.278 MB | True | `4168c669520b987b4916cd1bd65e243cb6302cd47972d87fc8a9d85de4203ba1` | True |
| R8_C26 | LKA | head 159.28 MB | True | `86478d466396a887bbb2aed0734db9d06dc9b8f8539a19a3019221a0ccf928b8` | True |

## Cache policy

Raw GHSL ZIP files are stored under air-monitoring/.cache/station-radius-ghsl-population-tiles/ and are not committed; rerun this script to rehydrate the large corrected tiles from public GHSL URLs.

## Non-claim

This large-tile GHSL custody gate downloads, hashes, and inspects only the three corrected selected population tiles deferred by the first-wave size threshold. It does not compute station-radius population, compute PM2.5 exposure, validate same-station joins, freeze radius or de-duplication rules, or promote monitor-grade rows.
