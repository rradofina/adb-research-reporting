# Air Monitoring Station-Radius Country-Unioned Catchment Dry Run

attestation_chain: ai-first

## Status

This pass turns the row-level denominator join into a country-unioned candidate catchment diagnostic. It removes overlap among candidate buffers within each economy/radius band, but it remains outside any coverage or exposure claim.

## Evidence Counts

| Check | Count |
|---|---:|
| Country-radius union rows | 33 |
| Coordinate rows represented | 277 |
| Unique coordinate points represented | 275 |
| Radius bands computed | 3 |
| GHSL tiles opened | 21 |
| ACAG PM2.5 union rows computed | 22 |
| Validated same-station joins | 0 |
| Complete monitor-grade rows | 0 |
| Coverage claim allowed | False |

## Primary 4 km Unioned Diagnostic Rows

These rows compare the prior row-level buffer sum with the new unioned GHSL-cell denominator. The difference is duplicate candidate-buffer mass, not people newly covered or uncovered by monitors.

| Economy | Coordinates | Unioned population | Row buffer sum | Row/union multiplier | Mean ACAG PM2.5 |
|---|---:|---:|---:|---:|---:|
| BGD | 53 | 24712113.168 | 80227280.523 | 3.246 | 73.929 |
| IDN | 58 | 15154232.146 | 27402298.671 | 1.808 | 22.024 |
| MYS | 85 | 7627671.214 | 9745622.205 | 1.278 | 17.011 |
| UZB | 44 | 5050716.278 | 7965633.979 | 1.577 | 34.542 |
| AFG | 2 | 1571500.293 | 2375372.397 | 1.512 |  |
| MMR | 3 | 1384417.179 | 1602881.76 | 1.158 | 32.917 |
| GEO | 18 | 1332609.962 | 2609473.9 | 1.958 | 18.495 |
| TJK | 7 | 1219474.147 | 1584518.836 | 1.299 | 43.452 |

## Gate Ledger

| Gate | Status | Rows | Reader use |
|---|---|---:|---|
| Country-unioned GHSL catchment denominator | computed_dry_run | 33 | Each GHSL population cell is counted at most once within an economy/radius band. |
| Row-level denominator comparison | computed | 33 | The dry run preserves the prior buffer-sum and exact-coordinate-dedup diagnostics for comparison. |
| ACAG PM2.5 union-cell context | computed_dry_run | 22 | PM2.5 is averaged across coarse ACAG cells inside candidate buffers; it is contextual, not exposure. |
| Validated same-station joins | not_ready | 0 | No official/OpenAQ proximity row is promoted to a same-station identity. |
| Complete monitor-grade rows | not_ready | 0 | No coordinate row is promoted to complete regulatory-grade evidence. |
| Coverage claim | blocked | 0 | The public surface may show denominator geometry, not people served or protected by monitors. |

## What This Does Not Mean

This country-unioned catchment dry run counts each GHSL population cell at most once within an economy and radius band. It is still a candidate denominator diagnostic. It does not validate same-station joins, does not classify complete monitor grade, does not prove regulatory monitor coverage, and does not support a population-served or exposure claim.

## Reproduce

```powershell
python air-monitoring\scripts\build-station-radius-country-unioned-catchment-dry-run.py
```
