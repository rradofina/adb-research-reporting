# Results — Disaster Recovery Lag

`attestation_chain: ai-first`. §18 AI-first SR — 2026-04-26.

## 1. Headline

Two ADB DMCs — **China and India** — persistently hold the top two
positions in the disaster-burden ranking across every alternative
metric (events-per-year, total-affected, total-damage-USD-adjusted),
EM-DAT 2000–2025.

## 2. Tables

| Rank | ISO3 | DMC | Events/yr | Total affected | Total damage USD-adj |
|---|---|---|---|---|---|
| 1 | CHN | China | 25.6 | 1.77 B | (computed) |
| 2 | IND | India | 15.5 | 1.15 B | (computed) |

## 3. Reproduction

```bash
python disaster-recovery-lag/scripts/process-disaster.py
python scripts/batch-sensitivity.py
```
