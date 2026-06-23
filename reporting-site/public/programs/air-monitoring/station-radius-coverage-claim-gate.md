# Station-radius coverage-claim gate

`attestation_chain: ai-first`

Generated: 2026-06-23T08:58:18Z

## What this adds

This derivative gate reads the committed denominator, country-union, station-identity, and monitor-grade artifacts and decides whether the public surface may use station-radius coverage language.

It currently blocks the claim. The denominator geometry is computed, but the identity and grade prerequisites remain at zero.

## Mechanical rule

A station-radius coverage claim is allowed only when denominator geometry is computed, validated same-station identity rows exist, complete monitor-grade rows exist, station-radius readiness is true, and the coverage-claim flag is true for the row/economy.

## Summary counts

| Measure | Count |
|---|---:|
| primary radius country rows checked | 11 |
| coordinate economies | 11 |
| country union rows computed | 33 |
| country union population rows computed | 33 |
| country union pm25 rows computed | 22 |
| denominator join rows | 831 |
| ghsl population rows computed | 831 |
| acag pm25 rows computed | 831 |
| validated same station join rows | 0 |
| candidate review rows | 13 |
| candidate crosswalk source scan rows | 6 |
| complete monitor grade rows | 0 |
| station method classified rows | 22 |
| current status confirmed rows | 0 |
| calibration status available rows | 0 |
| station radius ready economies | 0 |
| station radius ready rows | 0 |
| claim allowed country rows | 0 |
| coverage claim allowed | False |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Country-unioned denominator geometry | 33 | computed |
| ACAG PM2.5 context | 22 | computed |
| Validated same-station identity | 0 | blocked |
| Station-method classification | 22 | partly_available |
| Current status confirmed | 0 | blocked |
| Calibration/status record | 0 | blocked |
| Complete monitor-grade rows | 0 | blocked |
| Station-radius readiness | 0 | blocked |
| Coverage claim permission | 0 | blocked |

## Largest blocked denominator rows

| Economy | Unioned denominator | Decision | Missing gates |
|---|---:|---|---|
| Bangladesh (`BGD`) | 24712113.168 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |
| Indonesia (`IDN`) | 15154232.146 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |
| Malaysia (`MYS`) | 7627671.214 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |
| Uzbekistan (`UZB`) | 5050716.278 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |
| Afghanistan (`AFG`) | 1571500.293 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |
| Myanmar (`MMR`) | 1384417.179 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |
| Georgia (`GEO`) | 1332609.962 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |
| Tajikistan (`TJK`) | 1219474.147 | block_coverage_claim | validated same-station identity, complete monitor-grade evidence, station-radius readiness, coverage-claim permission |

## Non-claim

This gate decides whether the current station-radius denominator evidence may be described as monitor coverage. It does not validate same-station joins, does not certify complete monitor grade, does not estimate people served by monitors, and does not create an exposure or regulatory-coverage claim.
