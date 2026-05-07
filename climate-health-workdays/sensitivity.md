# Sensitivity — Climate-Health Workday Loss

`attestation_chain: ai-first`

Run on 2026-04-26 by `scripts/sensitivity.py`. Run artifact:
`sensitivity-runs.json`. Per Constitution §6.6.

---

## 1. Test matrix

Headline metric: **top-N set composition of the workday-loss pressure
index ranking across 34 rankable ADB DMCs**.

| Parameter | Pre-registered | -50% test | +50% test | Top-5 overlap with baseline | Decision-rule preserved? |
|---|---|---|---|---|---|
| Industry-share weight | 0.5 | 0.25 | 0.75 | 5/5 (-50%) · 4/5 (+50%) | yes (top-5: ≤ 1 entry change) |
| PM2.5 floor | 5 µg/m³ | 2.5 | 7.5 | 5/5 (-50%) · 5/5 (+50%) | yes |
| PM2.5 cap (ramp range) | 45 µg/m³ | 22.5 | 67.5 | **3/5** (-50%) · 5/5 (+50%) | **no** (top-5: 2-entry change at -50%) |

Headline narrows accordingly:

- **Top-3 (AFG, IND, BGD): stable across every perturbation row.**
  This is the claim.
- Top-5 (AFG, IND, BGD, PAK, TJK): not fully stable. PM2.5-cap-minus50
  shifts 2 of the bottom 2 entries. The pre-registration's decision
  rule (§8: positive only if ≤ 1 entry change) requires the headline
  to commit only to the stable top-3.

**Common top-3 across every row**: `['AFG', 'IND', 'BGD']` — confirmed
by `sensitivity-runs.json` `common_top5_across_runs` field (returns
the 3-element intersection).

## 2. Replication ranges (for the article)

| Metric | Baseline | Across suite |
|---|---|---|
| Top-3 set composition | AFG, IND, BGD | identical (0 entries change) |
| Top-5 set composition | AFG, IND, BGD, PAK, TJK | 4th + 5th positions shift; top-3 stable |

## 3. Robustness checks beyond ±50%

TODO (deferred to §18.5 upgrade-pass):
- **Subnational PM2.5** via Earth Engine (currently country-mean only;
  India and China especially have very large within-country variance
  in PM2.5 exposure).
- **Heat exposure** via CCKP tasmax (currently the index uses PM2.5
  alone; the program README anticipates heat as a future dimension).
- **Leave-one-out by DMC**: currently not run; would test whether the
  top-3 set is driven by any single DMC's data anomaly.

## 4. Owner attestation

| Field | Value |
|---|---|
| Sensitivity suite run | yes (2026-04-26) |
| Critical failures resolved | yes — claim narrowed from top-5 to top-3 |
| Reviewer chain | §18 AI-first under §18.1 |
| Upgrade-eligible | yes |
