# Coverage — Climate-Health Workday Loss

`attestation_chain: ai-first`

Last refresh: 2026-04-26.

---

## DMCs in scope

44 ADB regional DMCs (WDI publishes for these economies on the required indicators).

## DMCs covered

| Coverage | Count | Notes |
|---|---|---|
| All 4 inputs (agri%, industry%, PM2.5, pop) | 34 | Index computable. |
| Missing PM2.5 only | ~6 | Pacific microstates not in WDI PM2.5 series. |
| Missing both employment series | ~3 | Small-island microstates with thin labor data. |

## Top 3 most-pressure-exposed (set is stable per `sensitivity.md`)

| Rank | ISO3 | DMC | agri % | industry % | PM2.5 µg/m³ | Index |
|---|---|---|---|---|---|---|
| 1 | AFG | Afghanistan | 51.5 | 19.0 | 46.1 | 55.7 |
| 2 | IND | India | (latest) | (latest) | (latest) | 53.1 |
| 3 | BGD | Bangladesh | (latest) | (latest) | (latest) | 44.6 |

## DMCs not covered

Pacific microstates (KIR, NRU, NIU, TUV, COK, PLW, MHL, FSM): WDI
PM2.5 series is sparse. The §18.5 upgrade-pass uses ACAG-V6 PM2.5
gridded raster (Earth-Engine-backed) to fill these.
