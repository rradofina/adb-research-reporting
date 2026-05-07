# Sensitivity — Disaster Recovery Lag

`attestation_chain: ai-first`

Run 2026-04-26 by `scripts/batch-sensitivity.py`. Per `CONSTITUTION.md` §6.6.

## 1. Test matrix

| Metric | Top-2 |
|---|---|
| Events-per-year | CHN, IND |
| Total affected | CHN, IND |
| Total damage USD-adjusted | CHN, IND |

**Common top-2 across all three metrics: `[CHN, IND]`.** Honest
narrowing: the top-5 set is metric-sensitive; only the top-2 is
metric-robust.

## 2. Replication ranges

Top-2 set: identical across all three alternative metrics.

## 3. TODO (§18.5 upgrade-pass)

- Per-event recovery-curve analysis (the program's named question)
  requires post-event indicator-recovery data joined to EM-DAT
  timestamps. Not implemented.
- Time-window subsampling (2010–2025 vs 2000–2025).

## 4. §18 attestation

Sensitivity run complete. Critical failures resolved (top-5 narrowed
to top-2). Reviewer chain: §18 AI-first.
