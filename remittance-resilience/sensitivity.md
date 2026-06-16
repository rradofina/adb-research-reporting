# Sensitivity — Remittance Resilience

`attestation_chain: ai-first`

Run on 2026-06-16 by `scripts/sensitivity.py` against the repaired RPW +
WDI artifacts. Per `CONSTITUTION.md` §6.6, every arbitrary numeric in
`pre-registration.md` §6 is tested at +/-50 percent. Run artifact:
`sensitivity-runs.json`.

---

## 1. Test Matrix

Headline being tested: **top-five DMC composition in the repaired
remittance-dependence x observed-cost triage screen**.

Decision rule from `pre-registration.md` §8: positive if the top-five
composition changes by no more than one entry in any single perturbation
row. The stricter "common across every row" set is reported separately and
is not the same as the repaired baseline top five.

| Run | Top five | Entry changes vs baseline | Top-10 overlap |
|---|---|---:|---:|
| baseline | KGZ, WSM, TON, NPL, VUT | 0 | 10 |
| dep_cap_minus50 | KGZ, VUT, PAK, WSM, TON | 1 | 9 |
| dep_cap_plus50 | TON, KGZ, NPL, WSM, VUT | 0 | 10 |
| cost_cap_minus50 | KGZ, TON, NPL, WSM, VUT | 0 | 9 |
| cost_cap_plus50 | KGZ, WSM, TON, NPL, VUT | 0 | 10 |
| both_minus50 | KGZ, WSM, TON, VUT, NPL | 0 | 8 |
| both_plus50 | TON, KGZ, NPL, WSM, VUT | 0 | 10 |
| additive_aggregation | KGZ, TON, WSM, NPL, VUT | 0 | 9 |

**Common top-five set across every computed row:**

`['KGZ', 'TON', 'VUT', 'WSM']`

The repaired sensitivity result therefore narrows the reader-facing
language. The five-economy baseline should not be described as identical
across every row. Nepal is cap-sensitive in `dep_cap_minus50`, where
Pakistan enters the top five, but the maximum entry change is one.

## 2. Robustness Checks Beyond +/-50 Percent

Completed:

- **Multiplicative vs additive aggregation.** Switch to additive
  aggregation `(n_dep + n_cost) / 2 * 100` preserves the repaired
  baseline top-five membership, with rank reordering.
- **Median-cost deepening.** `scripts/deepen-median-cost.py` preserves
  the same five-economy set under both median-over-quotes and
  median-of-corridor-medians cost.
- **Corridor-flow weighting sprint.** `scripts/sprint-flow-weighted-cost.py`
  preserves the same five-economy top-five set after joining RPW Q1 2025
  corridor prices to World Bank/KNOMAD 2021 bilateral flow estimates, but
  changes the order: KGZ, NPL, VUT, WSM, TON.

Deferred to a later upgrade pass:

- **Minimum corridor sample size.** Recompute with minimum 3 / 10 RPW
  corridor observations per DMC. Several small economies have very few
  corridors; tighter thresholds may drop them from the ranking.
- **Time-window subsampling.** Recompute with the latest 2 years of RPW
  versus the latest 4 years to test whether 2025-Q1 alone drives the
  observed-cost axis.
- **Leave-one-out by DMC.** Rerun after dropping each DMC; report whether
  any one DMC's removal materially shifts the ranking.

## 3. Attestation

| Field | Value |
|---|---|
| Sensitivity suite run | yes (2026-06-16) |
| Parser repair reflected | yes |
| Critical claim correction | old all-five all-row stability wording superseded |
| Maximum entry change vs baseline | 1 |
| Common top-five across all runs | KGZ, TON, VUT, WSM |
| Reviewer chain | §18 AI-first under §18.1 |
| Upgrade-eligible | yes |
