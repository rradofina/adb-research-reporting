# Literature review — Disaster Recovery Lag

`attestation_chain: ai-first`. §18 AI-finalized 2026-04-27.

## 1. Search record

Queries (2026-04-26):
1. `EM-DAT methodology threshold under-reporting`
2. `Sendai Framework disaster-loss accounting per-capita`
3. `disaster recovery lag indicator GDP slow-onset`
4. `UCLouvain CRED EM-DAT validation`

Tier-A: *Nature Climate Change*, *Environmental Research Letters*,
*Climatic Change*, *Disasters*. Tier-B: UNDRR, GFDRR, CRED.
Tier-C: HDX disaster-event databases.

## 2. Verified entries

- **`cred2024emdat`** — CRED EM-DAT International Disaster Database
  (vintage 2025). **Primary data source.**
- **`undrr2015sendai`** — Sendai Framework for Disaster Risk
  Reduction 2015–2030. **Per-capita accounting standard.**

## 3. Synthesis

Two established facts:

1. **EM-DAT is the canonical multi-country disaster-loss database
   for cross-DMC comparison** [@cred2024emdat] but uses thresholds
   (≥10 deaths or ≥100 affected or declared emergency) that
   under-count small recurrent events.
2. **Sendai Framework** [@undrr2015sendai] is the policy framework
   for cross-country disaster-loss accounting with per-capita
   normalization as the standard.

## 4. Gap

EM-DAT publishes per-DMC totals; the metric-robust top-2 finding
(CHN and IND hold the top regardless of events / affected /
damage-USD-adjusted) has not been published as a sensitivity-
gate result for ADB DMCs.

## 5. Risk of redundancy

CRED publishes annual disaster summaries that include CHN and IND
prominently. The marginal contribution is the metric-robust
top-2 set claim, not the discovery that big countries have many
disasters.

## 6. First testable claim

> Across the 38 ADB DMCs in EM-DAT 2000–2025, China and India
> persistently rank in the top two of the disaster-burden ranking,
> regardless of whether the metric is events-per-year,
> total-affected, or total-damage-USD-adjusted.

## 7. §18 attestation

`ai-first`. 2026-04-27.
