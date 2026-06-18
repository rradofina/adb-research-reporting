# Pre-registration — Remittance Resilience

`attestation_chain: ai-first`

Status: **§18 AI-first frozen — 2026-04-26.**

Governed by `CONSTITUTION.md` §3.2, §7, and §18. The screening-result
computations already in `generated/` are treated as exploratory under
§3.2; this pre-registration applies to subsequent reruns under §18 ACTIVE.

---

## 1. Claim sentence

> Among the 50 ADB regional developing member economies, a small set
> of five DMCs — Kyrgyz Republic, Nepal, Tonga, Vanuatu, Samoa — are
> persistently ranked in the top five most-fragile by the
> remittance-fragility triage screen, and that set is robust to any
> ±50 percent perturbation of the screen's two arbitrary cap parameters
> and to a switch from multiplicative to additive aggregation.

The claim deliberately commits to a **set-stability** finding rather
than a country ranking (Constitution §6.4 prohibits headlines built on
composite-index country rankings; §13.3 prohibits country-deficiency
framing). The set is presented as a "high-priority screening cluster
for remittance-corridor work," not as a fragility ranking.

## 2. Falsification condition

The claim is retracted if **either** of the following triggers in the
±50% sensitivity suite:

- (a) The top-5 set composition changes by more than 1 entry in any
  single ±50% perturbation row, **or**
- (b) An aggregation switch (multiplicative → additive) changes the
  top-5 set by more than 1 entry.

A 1-entry margin allows for boundary cases (a country at rank 5 vs
rank 6 with a tied-or-near-tied score). A 2-entry shift indicates the
result is parameter-driven, not pattern-driven.

## 3. Population in scope

50 ADB regional developing member economies (the full ADB regional
DMC roster). Coverage limited to DMCs with both: (a) at least one
WDI BX.TRF.PWKR.DT.GD.ZS observation in 2015–2024, and (b) at least
one inbound RPW corridor observation in the latest period (2025-Q1).

DMCs with no RPW destination coverage (e.g., several Pacific micro-
states) are excluded from the ranking and listed explicitly in
`coverage.md`.

## 4. Time window

| Source | Start | End |
|---|---|---|
| World Bank RPW Q1 2025 dataset | 2011-Q1 | 2025-Q1 |
| WDI BX.TRF.PWKR.DT.GD.ZS | 2015 | 2024 |

Headline metrics use the latest period in each source: 2025-Q1 for RPW,
latest available year per DMC for WDI.

## 5. Primary metric

**Fragility index** for each DMC, defined as:

```
fragility = min(wdi_pct_gdp / dep_cap, 1.0) × min(mean_cost_pct / cost_cap, 1.0) × 100
```

Where `wdi_pct_gdp` is the latest available WDI personal-remittances-
received-as-percent-of-GDP value, and `mean_cost_pct` is the mean
inbound transfer cost across all RPW corridors with the DMC as
destination in the latest period. Baseline `dep_cap = 25` and
`cost_cap = 15`.

The fragility score is a triage instrument under Constitution §6.4 and
**must not** headline any output. The top-5 set membership (§1) is
the headline because set stability is a more defensible claim than
score magnitude.

## 6. Pre-specified arbitrary numerics

| Parameter | Value | Reason for value | Sensitivity range |
|---|---|---|---|
| Dependence cap (`dep_cap`) | 25% of GDP | Above the 25% threshold a DMC's economy is heavily remittance-dependent (per IMF and World Bank framing). | 12.5% to 37.5% |
| Cost cap (`cost_cap`) | 15% mean transfer cost | Above 15% the cost is exceptional (Myanmar at 28% is far above). | 7.5% to 22.5% |
| Aggregation operator | multiplicative | Multiplicative penalizes DMCs that are high on both axes; additive averages instead. | additive (mean of normalized values) |
| RPW corridor inclusion | all corridors with `cc1 total cost %` defined in latest period | The full RPW dataset for the destination DMC. | minimum 3 / minimum 10 corridor observations per DMC |

## 7. Primary sources

- `rpw` — World Bank Remittance Prices Worldwide Q1 2025 dataset,
  retrieved 2026-04-25, ~49 MB Excel, 198,000 corridor-firm-period
  observations globally.
- `wdi` — World Bank WDI BX.TRF.PWKR.DT.GD.ZS, latest available year
  per DMC.

Both pinned in `versions.json`. License: World Bank open / CC BY 4.0.

## 8. Decision rule

- **Positive** (claim survives): The top-5 set is identical across
  baseline and every ±50% perturbation, including the additive-vs-
  multiplicative switch. Set membership shifts by ≤ 1 entry are
  permitted.
- **Negative** (claim retracts): Set composition changes by more than
  1 entry in any single perturbation row.

## 9. Stopping rule

The pipeline stops when every DMC has either: (a) at least one RPW
corridor observation in the latest period and at least one WDI
observation in 2015–2024, or (b) is documented in `coverage.md` as
out-of-coverage with the reason.

## 10. Attestation (§18 AI-first)

| Field | Value |
|---|---|
| Frozen by | §18 AI-first under `CONSTITUTION.md` §18.1 (owner: Raymond Adofina, who toggled §18 ACTIVE on 2026-04-25) |
| Date frozen | 2026-04-26 |
| Commit hash | (recorded at the freeze commit) |
| Pipeline run started after this commit | yes (existing artifacts treated as exploratory under §3.2; subsequent reruns begin after the freeze) |
| Attestation chain | `ai-first` |
| §18.5 upgrade-eligible | yes |

## 11. AI assistance disclosure (§12 + §18.2)

This pre-registration is AI-drafted and AI-frozen under §18.1. Every
artifact in this program carries `attestation_chain: ai-first`. A
subsequent owner-attestation upgrade-pass under §18.5 converts the
chain to `mixed` or `human-final`.

## 12. 2026-06-17 L3 flow-weighting addendum

This addendum does not rewrite the frozen 2026-04-26 claim. It records the
post-repair decision rule for using public bilateral-flow estimates as an L3
sensitivity module after the RPW cost-normalization defect was repaired.

### 12.1 Public sources

| Source | Unit | Period used | Local artifact |
|---|---|---:|---|
| World Bank Remittance Prices Worldwide | Source-destination corridor price quotes | 2025 Q1 | `.cache/rpw_dataset_2011_2025_q1.xlsx` |
| World Bank/KNOMAD bilateral remittance matrix, `WB.KNOMAD.BRE` | Bilateral flow estimates, US$ million | 2021 | `.cache/WB-KNOMAD-bilateral-remittance-matrix-2021.xlsx` |
| WDI `BX.TRF.PWKR.DT.GD.ZS` | Personal remittances received, percent of GDP | latest available year by economy | `.cache/wdi_remittance_pct_gdp.json` |

The unit of analysis is the receiving ADB DMC, aggregating observed RPW
source-to-destination corridors.

### 12.2 Coverage gate

The flow-weighting module is treated as L3 sensitivity evidence only if at
least 90 percent of latest-period ADB-DMC-bound RPW corridors match to public
KNOMAD bilateral-flow estimates. Destination rows with matched-flow coverage
below 25 percent must be flagged wherever the result is interpreted.

The current run passes the corridor-match gate: 140 of 142 RPW corridors match
to KNOMAD flow estimates. Low matched-flow coverage is still flagged for KGZ,
TJK, ARM, and AFG in `generated/remittance-flow-weighting-sprint.json`.

### 12.3 Interpretation rule

- If the flow-weighted top-five set differs from the repaired equal-weighted
  baseline by more than one entry, retract or reframe the equal-weighted
  baseline.
- If the same set survives but order or observed costs change, keep
  set-membership language but show the order/cost movement and coverage
  caveats.
- No result from this module may be described as household transaction cost,
  informal-channel incidence, country performance, or a maturity promotion.

### 12.4 Current decision

The repaired equal-weighted baseline top five are `KGZ`, `WSM`, `TON`, `NPL`,
and `VUT`. Inside the matched-corridor flow module, the equal-weighted quote
order is `KGZ`, `WSM`, `TON`, `VUT`, `NPL`; the flow-weighted top five are
`KGZ`, `NPL`, `VUT`, `WSM`, and `TON`. The same set survives, but the order
changes. Reader-facing copy must therefore report the repaired five-economy
set, the four-economy full-suite sensitivity core, Nepal's cap sensitivity,
and the flow-weighted order change together.
