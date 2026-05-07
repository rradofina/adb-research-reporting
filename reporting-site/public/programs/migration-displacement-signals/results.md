# Results — Migration & Displacement Signals

`attestation_chain: ai-first`

Status: **§18 AI-first Screening Result — 2026-04-26.**

---

## 1. Headline

Five ADB DMCs — **India, China, Bangladesh, Afghanistan, Philippines** —
persistently rank in the top five emigrant-stock economies in UN DESA
2024, regardless of whether ranked by raw emigrant stock or by net
migrant stock. Three of the five (BGD, AFG, PHL) concentrate over
50 percent of their emigration in their top-3 destination corridors;
IND and CHN have more diversified destination profiles.

## 2. Headline-supporting tables

| Rank | ISO3 | DMC | Emigrant stock 2024 | Top-3 destination share |
|---|---|---|---|---|
| 1 | IND | India | 18,533,845 | 45% |
| 2 | CHN | China | 11,701,619 | 49% |
| 3 | BGD | Bangladesh | 8,706,947 | 65% |
| 4 | AFG | Afghanistan | 7,528,994 | 80% (refugee-driven) |
| 5 | PHL | Philippines | 6,988,383 | 55% |

## 3. Sensitivity

Top-5 set: identical across emigrant-stock and net-migrant rankings.
Top-3 corridor concentration: 45%–80% range; ordering stable.

## 4. Reproduction

```bash
python migration-displacement-signals/scripts/process-migration.py
python migration-displacement-signals/scripts/sensitivity.py
```
