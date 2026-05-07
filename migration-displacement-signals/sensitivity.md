# Sensitivity — Migration & Displacement Signals

`attestation_chain: ai-first`

Run on 2026-04-26 by `scripts/sensitivity.py`. Run artifact:
`sensitivity-runs.json`. Per Constitution §6.6.

---

## 1. Test matrix

| Parameter | Pre-registered | Variant | Top-5 set change | Decision-rule preserved? |
|---|---|---|---|---|
| Top-N for set claim | 5 | 3 (top-3) | 0 entries (subset) | yes |
| Top-N for set claim | 5 | 8 (top-8) | superset; top-5 unchanged | yes |
| Migration metric | emigrant stock | net migrant stock | 0 entries change (same 5 economies) | yes |
| Migration metric | emigrant stock | emigrant share of total | substantial shift (small DMCs with high share) | n/a — different question |
| Top-N for corridor concentration | 3 | 2 | concentration figures lower; pattern preserved | yes |
| Top-N for corridor concentration | 3 | 5 | concentration figures higher; pattern preserved | yes |
| Concentration threshold | 50% | 25%, 75% | 25%: all 5 above; 75%: only AFG above | partial |

## 2. Replication ranges

| Metric | Baseline | Across suite |
|---|---|---|
| Top-5 emigrant-stock set | IND, CHN, BGD, AFG, PHL | identical across emigrant-stock and net-migrant rankings |
| Top-3 corridor concentration | BGD 65%, AFG 80%, PHL 55%, IND 45%, CHN 49% | range 45%–80%; ordering stable |

## 3. Robustness checks beyond ±50%

Completed:
- **Direction-of-definition switch** (emigrant stock ↔ net migrant
  stock): top-5 set identical (5/5 overlap).

TODO (deferred to §18.5 upgrade-pass):
- **Vintage stability**: re-rank using UN DESA 2020 and 2015 vintages;
  confirm whether the top-5 set is stable across releases.
- **Sub-national exposure**: ADB DMC migrant stock disaggregated by
  ADM1 to test whether the pattern is country-level or
  region-concentrated.

## 4. Owner attestation

| Field | Value |
|---|---|
| Sensitivity suite run | yes (2026-04-26) |
| Critical failures resolved | yes (no failures) |
| Reviewer chain | §18 AI-first |
| Upgrade-eligible | yes |
