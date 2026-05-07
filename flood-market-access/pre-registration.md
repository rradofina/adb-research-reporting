# Pre-registration — Flood Market Access

`attestation_chain: ai-first`. §18 frozen 2026-04-26. **Honest top-4
narrowing.**

## 1. Claim

> Four ADB DMCs — India, China, Indonesia, Afghanistan — persistently
> hold the top-4 flood-market-access pressure index positions across
> alternative metric formulations (full index, flood-events-only,
> rural × floods).

## 2. Falsification

Top-4 set composition changes by ≥ 1 entry under any alternative
metric.

## 3. Population

41 ADB DMCs with WDI rural + population + EM-DAT flood data.

## 5. Metric

`index = (rural_pct / 100) × annual_flood_events × log10(population)`
where annual_flood_events = EM-DAT flood subset 2000-2025 / 25.
Triage only.

## 6. Arbitrary

| Param | Value | Range |
|---|---|---|
| Time window | 2000-2025 (25 years) | (deferred §18.5) |
| Combine operator | multiplicative | tested vs flood-events-only and rural × floods |

## 8. Decision rule

Common top-4 across all 3 metric formulations: `[AFG, CHN, IDN, IND]`.
**Positive (top-4 narrowing).** Top-5 is metric-sensitive.

## 10. §18

`ai-first`. 2026-04-26.
