# Station-radius GHSL population tile-selection gate

`attestation_chain: ai-first`

Generated: 2026-06-20T11:15:46Z

## What this adds

This pass turns committed station coordinates into a bounded GHSL population tile download queue. It probes the selected public tile URLs for header metadata, but it does not download population ZIP bodies or compute catchment population.

## Summary counts

| Measure | Count |
|---|---:|
| coordinate ready economies | 11 |
| coordinate rows used | 277 |
| openaq coordinate rows used | 101 |
| official pm25 coordinate rows used | 176 |
| unique coordinate points | 275 |
| draft radius buffer km | 50 |
| ghsl population tile urls selected | 23 |
| ghsl tile head probes | 23 |
| ghsl tile head ok | 7 |
| ghsl tile head failed | 16 |
| selected tile content length bytes total | 189405916 |
| selected tile content length mb total | 189.406 |
| population denominator files downloaded | 0 |
| population denominator files sha256 checksummed | 0 |
| station radius population rows | 0 |
| station radius pm25 exposure rows | 0 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| station radius ready economies | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Coordinate-driven population tile queue | 23 | available |
| Selected tile HEAD metadata | 7 | limited |
| Population tile ZIP downloads | 0 | not_ready |
| Population tile SHA-256 checksums | 0 | not_ready |
| GeoTIFF transform inspection | 0 | not_ready |
| Station-radius population computation | 0 | not_computed |

## Country queue

| Economy | Coordinate rows | GHSL tiles | Tile IDs |
|---|---:|---:|---|
| Afghanistan (AFG) | 2 | 1 | `R6_C25` |
| Bangladesh (BGD) | 53 | 2 | `R7_C27||R7_C28` |
| Myanmar (MMR) | 3 | 1 | `R8_C28` |
| Uzbekistan (UZB) | 44 | 5 | `R5_C24||R5_C25||R5_C26||R6_C25||R6_C26` |
| Tajikistan (TJK) | 7 | 4 | `R5_C25||R5_C26||R6_C25||R6_C26` |
| Azerbaijan (AZE) | 2 | 4 | `R5_C23||R5_C24||R6_C23||R6_C24` |
| Georgia (GEO) | 18 | 1 | `R5_C23` |
| Indonesia (IDN) | 58 | 8 | `R9_C28||R9_C29||R9_C30||R10_C28||R10_C29||R10_C30||R10_C31||R10_C32` |
| Sri Lanka (LKA) | 3 | 4 | `R8_C26||R8_C27||R9_C26||R9_C27` |
| Malaysia (MYS) | 85 | 3 | `R9_C28||R9_C29||R9_C30` |
| Turkmenistan (TKM) | 2 | 1 | `R6_C24` |

## Selected tile URLs

| Tile | Economies | Size MB | HEAD |
|---|---|---:|---|
| `R5_C23` | AZE||GEO |  | not ok |
| `R5_C24` | AZE||UZB |  | not ok |
| `R5_C25` | TJK||UZB | 33.350 | 200 |
| `R5_C26` | TJK||UZB | 32.990 | 200 |
| `R6_C23` | AZE |  | not ok |
| `R6_C24` | AZE||TKM |  | not ok |
| `R6_C25` | AFG||TJK||UZB |  | not ok |
| `R6_C26` | TJK||UZB |  | not ok |
| `R7_C27` | BGD |  | not ok |
| `R7_C28` | BGD |  | not ok |
| `R8_C26` | LKA |  | not ok |
| `R8_C27` | LKA | 20.948 | 200 |
| `R8_C28` | MMR | 34.371 | 200 |
| `R9_C26` | LKA |  | not ok |
| `R9_C27` | LKA |  | not ok |
| `R9_C28` | IDN||MYS |  | not ok |
| `R9_C29` | IDN||MYS |  | not ok |
| `R9_C30` | IDN||MYS | 16.003 | 200 |
| `R10_C28` | IDN | 1.696 | 200 |
| `R10_C29` | IDN |  | not ok |
| `R10_C30` | IDN | 50.049 | 200 |
| `R10_C31` | IDN |  | not ok |
| `R10_C32` | IDN |  | not ok |

## Non-claim

This GHSL population tile-selection gate constructs and probes the public 2020 GHSL 4326 3 arc-second tile URLs needed by committed station coordinates using a conservative 50 km draft-radius buffer. It does not download GHSL ZIP bodies, compute SHA-256 checksums, inspect GeoTIFF transforms, compute station-radius population, compute PM2.5 exposure, validate same-station joins, freeze radius or de-duplication rules, or promote monitor-grade rows.
