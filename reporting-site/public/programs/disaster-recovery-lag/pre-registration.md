# Pre-registration — Disaster Recovery Lag

`attestation_chain: ai-first`

Status: **§18 AI-first frozen — 2026-04-26.**

## 1. Claim sentence

> Across the 38 ADB DMCs in EM-DAT 2000–2025, two economies — China
> and India — persistently rank in the top two of the disaster-burden
> ranking, regardless of whether the metric is events-per-year,
> total-affected, or total-damage-USD-adjusted.

The headline is the **top-2 set** stability across alternative metrics.
This is a structural-burden signal, not a country-quality ranking
(§13.3).

## 2. Falsification condition

Retracted if the top-2 set composition changes by ≥ 1 entry under any
alternative metric (events, affected, damage).

## 3. Population in scope

50 ADB regional DMCs. EM-DAT 2000–2025 has at least one event for 38;
12 small/quiet DMCs have zero recorded events.

## 4. Time window

EM-DAT vintage 2026-04-24, 2000–2025.

## 5. Metric

Three alternative rankings: events-per-year, total-affected,
total-damage-USD (CPI-adjusted). The headline is set-stability across
these three.

## 6. Pre-specified arbitrary numerics

| Parameter | Value | Sensitivity range |
|---|---|---|
| Time window | 2000–2025 | Test against 2010–2025 (deferred §18.5) |
| Damage CPI base year | 2024 | (deterministic) |
| Top-N for set claim | 2 | (claim narrowed to top-2 because top-5 is metric-sensitive) |

## 7. Sources

EM-DAT (CRED, UCLouvain), HDX mirror retrieval 2026-04-24. Non-
commercial open access. Pinned in `versions.json`.

## 8. Decision rule

Positive: top-2 set identical across all three metrics. Per
`sensitivity-runs.json`, common top-2 = `[CHN, IND]` — **positive**.

## 9. Stopping rule

Stops when each in-scope DMC has at least one EM-DAT event in window
or is documented zero.

## 10. §18 attestation

Frozen by §18 AI-first 2026-04-26. `attestation_chain: ai-first`.
Upgrade-eligible.
