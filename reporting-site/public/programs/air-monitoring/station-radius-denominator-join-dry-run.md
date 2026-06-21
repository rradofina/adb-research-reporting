# Air Monitoring Station-Radius Denominator Join Dry Run

attestation_chain: ai-first

## Status

This dry run physically joins the frozen candidate coordinate universe to cached GHSL population cells and the selected ACAG V6.GL.03 2023 coarse annual PM2.5 grid. It is a denominator diagnostic, not a monitor-coverage result.

## Evidence Counts

| Check | Count |
|---|---:|
| Candidate coordinate rows | 277 |
| Unique coordinate points | 275 |
| Radius bands computed | 3 |
| Candidate coordinate-radius rows | 831 |
| GHSL population rows computed | 831 |
| ACAG PM2.5 rows computed | 831 |
| Country radius summaries | 33 |
| Validated same-station joins | 0 |
| Complete monitor-grade rows | 0 |

## Primary 4 km Diagnostic Rows

These rows show the largest non-unioned exact-coordinate-deduplicated candidate population sums at the source-frozen 4 km band. They are not people covered by monitors.

| Economy | Coordinate rows | Unique points | Candidate population, exact-coordinate dedup | Mean nearest PM2.5 | GHSL tiles |
|---|---:|---:|---:|---:|---:|
| BGD | 53 | 52 | 79371463.157 | 78.451 | 2 |
| IDN | 58 | 58 | 27402298.671 | 27.478 | 7 |
| MYS | 85 | 84 | 9407324.841 | 17.413 | 3 |
| UZB | 44 | 44 | 7965633.979 | 35.74 | 4 |
| GEO | 18 | 18 | 2609473.9 | 18.802 | 1 |
| AFG | 2 | 2 | 2375372.397 | 45.465 | 1 |
| MMR | 3 | 3 | 1602881.76 | 31.845 | 1 |
| TJK | 7 | 7 | 1584518.836 | 36.557 | 2 |

## Gate Ledger

| Gate | Status | Rows | Reader use |
|---|---|---:|---|
| Coordinate input universe | computed | 277 | Frozen OpenAQ and official PM2.5 coordinate rows were physically joined to denominators. |
| Radius bands | computed | 3 | The source-frozen 0.5 km, 4 km, and 50 km bands are evaluated at row level. |
| GHSL population denominator join | computed_dry_run | 831 | GHSL cells are summed inside candidate-row buffers, not unioned into country coverage. |
| ACAG PM2.5 denominator join | computed_dry_run | 831 | The selected coarse annual ACAG grid is sampled as contextual PM2.5, not station measurement. |
| Validated same-station joins | not_ready | 0 | No candidate official/OpenAQ proximity row is promoted to station identity. |
| Complete monitor-grade rows | not_ready | 0 | No coordinate row can yet be used as complete regulatory-grade evidence. |
| Unioned country catchment coverage | not_computed | 0 | Overlapping buffers are not unioned; the public surface must not report people covered. |

## What This Does Not Mean

This denominator join dry run attaches the frozen candidate coordinate universe to cached GHSL population cells and the selected ACAG coarse annual PM2.5 grid. It reports candidate-row denominator diagnostics only. It does not validate same-station joins, does not classify complete monitor grade, does not compute unioned monitor catchment coverage, and does not support a population-served, exposure, or official monitor coverage claim.

## Reproduce

```powershell
python air-monitoring\scripts\build-station-radius-denominator-join-dry-run.py
```
