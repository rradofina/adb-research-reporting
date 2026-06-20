# Station-radius denominator readiness wall

`attestation_chain: ai-first`

Generated: 2026-06-20T08:02:55Z

## What this adds

This pass shows why the next map is still blocked. The project now has station-coordinate inputs, but the committed package still lacks gridded denominator files, validated same-station joins, complete monitor-grade rows, and a declared radius/deduplication method.

## Summary counts

| Measure | Count |
|---|---:|
| upgrade queue economies | 24 |
| economies with any coordinate input | 11 |
| economies with openaq coordinate rows | 11 |
| economies with official coordinate rows | 5 |
| openaq coordinate rows | 101 |
| official coordinate rows | 230 |
| official pm25 coordinate rows | 176 |
| near plus name candidate rows | 13 |
| near only candidate rows | 9 |
| name overlap not near candidate rows | 22 |
| validated same station join rows | 0 |
| complete monitor grade rows | 0 |
| boundary reference files available | 2 |
| gridded population denominator files | 0 |
| gridded pm25 denominator files | 0 |
| station radius ready economies | 0 |

## Readiness lanes

| Lane | Economies |
|---|---:|
| blocked_no_station_coordinates_or_denominators | 13 |
| blocked_denominator_missing_after_coordinates | 11 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| OpenAQ station-coordinate inputs | 101 | available |
| Official station-coordinate inputs | 230 | available |
| Candidate official/OpenAQ proximity signals | 22 | limited |
| Validated same-station joins | 0 | not_ready |
| Boundary reference files | 2 | available |
| Gridded population denominator | 0 | not_ready |
| Gridded PM2.5 denominator | 0 | not_ready |
| Complete monitor-grade rows | 0 | not_ready |
| Declared radius and deduplication method | 0 | not_ready |
| Station-radius analysis | 0 | not_computed |

## Non-claim

This readiness wall inventories coordinate, boundary, denominator, crosswalk, and grade inputs for possible future station-radius analysis. It does not compute catchment population, PM2.5 exposure inside a radius, monitor coverage, same-station OpenAQ joins, or complete monitor-grade classification.
