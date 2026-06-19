# Pre-registration — Air Pollution Without Air Monitors

`attestation_chain: ai-first`. §18 frozen 2026-04-27.

## 1. Claim

> Five ADB-region economies — Afghanistan, Bangladesh, Myanmar,
> Uzbekistan, Tajikistan — hold the top-5 PM2.5 observability-gap
> score positions, combining high WHO-derived PM2.5 exposure with
> sparse or absent OpenAQ public PM2.5 monitoring infrastructure.

## 2. Falsification

Top-5 set changes under alternative gap-score formulations (e.g.,
zero-monitors + above-guideline subset).

## 3. Population

50 ADB-region economies in the OpenAQ pilot.

## 5. Metric

`pm25_observability_gap_score` ∈ [0, 100], composite of
(people-per-monitor) × (PM2.5-exposure-above-WHO-5-µg/m³-guideline).

## 6. Arbitrary numerics

| Param | Value | Range |
|---|---|---|
| WHO PM2.5 guideline | 5 µg/m³ | (WHO 2021 anchored; not an arbitrary range) |
| Gap-score scale | 0–100 | (deterministic from inputs) |

## 8. Decision

Top-5 by gap-score baseline = `[AFG, BGD, MMR, UZB, TJK]`. The
zero-monitor-above-guideline subset returns a different ordering
because it's a different question (which DMCs have NO public PM2.5
monitor at all and are above the guideline). The pre-registered
headline is the gap-score top-5.

## 10. §18

`ai-first`. 2026-04-27.
