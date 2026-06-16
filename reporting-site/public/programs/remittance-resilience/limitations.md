# Limitations — Remittance Resilience

`attestation_chain: ai-first`

Status: §18 AI-finalized 2026-04-26. Updated to incorporate the
unresolved synthesized objections from `review-external.md` §5.

---

## 1. What this result cannot establish

- The fragility index does not measure resilience. It measures
  exposure to corridor-cost stress combined with macro dependence.
  Counter-cyclicality (the proper resilience question) requires a
  different program.
- The fragility ranking does not measure household exposure. WDI
  remittance-as-percent-of-GDP is a country-level macro figure;
  within-country remittance receipt is highly concentrated.
- The result does not produce a country-quality ranking. Per
  Constitution §6.4, the headline is the **set** stability of the
  top-5, not the score magnitudes. Any reading that compares top-5
  DMCs against each other on the score is outside scope.
- The result does not establish causal mechanisms. High cost may
  reduce flow (cost and dependence partly substitutes); high
  dependence may keep cost high (low elasticity); the screen is
  agnostic.

## 2. Source-side limitations

- **RPW measures publicly-quoted corridors.** Informal corridors
  (hawala / hundi / undocumented MTO use) are common in GCC → South
  Asia and Russia → Central Asia. The fragility figure is an upper
  bound on what households actually pay if they use informal
  channels.
- **Small-sample uncertainty in most top-five entries.** KGZ has 1
  observed RPW corridor; TON, VUT, and WSM have 2 each. Nepal is the
  only repaired baseline top-five entry with 8 corridors. The mean
  cost has wide sampling uncertainty, and the §18.5 upgrade-pass
  restricts the top-five to DMCs with >= 10 corridor observations.
- **Myanmar exceptional cost.** MMR's 28.16% mean transfer cost
  reflects post-2021 sanctions / FX friction and is not comparable
  to ordinary corridor pricing. Excluded from the headline cluster.
- **Volume-weighting unavailable.** RPW publishes corridor cost but
  not corridor flow volume. The mean cost is equal-weighted across
  corridors; a volume-weighted estimate (more appropriate for
  policy use) requires IMF-DOTS or central-bank corridor flow data
  not in scope here.

## 3. Method-side limitations

- **Multiplicative aggregation.** The fragility index multiplies
  normalized dependence × normalized cost. The sensitivity suite
  shows the top-5 set is stable under additive aggregation as well,
  but other operators (geometric mean, max-of-two) are not tested.
- **National-level WDI.** The dependence axis uses country-level
  WDI BX.TRF.PWKR.DT.GD.ZS. A subnational household-level analog
  requires LSMS or DHS microdata.
- **Cap binding.** Both `dep_cap` and `cost_cap` cap normalized
  values at 1.0. The uncapped-scaling robustness check shifts the
  top-5 by 1 entry (TJK drops out, MMR enters); within the
  decision-rule margin.

## 4. DMC-coverage limitations

- 6 of 50 DMCs are not rankable: 4 lack RPW destination corridors,
  1 lacks WDI in window, 1 lacks both. See `coverage.md` §3.
- The 44 rankable DMCs cover the great majority of remittance flow
  in the ADB region but miss several Pacific micro-states for which
  RPW does not publish destination corridors.

## 5. Synthesized reviewer objections quoted verbatim

Per `review-external.md` §5 under §18.4. **No individual reviewer
was contacted.** Upgrade-eligible.

### 5.1 From C-2 (World Bank Payment Systems), synthesized

> The destination-aggregated mean loses information about which
> sending corridors are most expensive. For policy use, the per-
> source-corridor breakdown is more actionable.

### 5.2 From C-4 (Pacific Community), synthesized

> Pacific micro-states have very few RPW corridors. The mean cost
> across so few corridors has wide sampling uncertainty. The article
> should report a confidence interval or restrict the top-5 to DMCs
> with at least 10 corridor observations.

### 5.3 From C-6 (OSCE Academy, Bishkek), synthesized

> Russia-Kyrgyz corridor cost is anomalously low due to MTO
> competition and EAEU banking integration. The 10.5% mean cost
> for KGZ is dragged up by non-Russia corridors that account for a
> small share of actual flow. Volume-weighted cost is the more
> appropriate measure.

### 5.4 From C-3 (IZA), synthesized

> Within-country distribution of remittance receipt is highly
> concentrated. The country-level fragility index does not measure
> household exposure.

## 6. Banned framings — explicit non-claims

Per `CONSTITUTION.md` §13.3 and §14:

- This result does **not** rank DMCs as fragile countries.
- This result does **not** describe DMCs as deficient.
- This result does **not** support causal inference from the
  screening signal.
- The headline is set-stability, not score magnitude.
