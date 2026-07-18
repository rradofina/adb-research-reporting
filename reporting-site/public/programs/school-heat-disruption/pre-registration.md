# Pre-registration and post-registered validation protocol

`attestation_chain: ai-first`

## Historical specification — frozen

The inherited screen multiplied child population, capped primary
pupil-teacher ratio, and a capped linear transform of 1995–2014 national annual
maximum temperature. It varied the temperature floor, temperature cap, and
pupil-teacher cap by ±50%. The historical public hypothesis was that Cambodia
remained first in every perturbation.

That hypothesis is retained here as an audit target, not rewritten after the
fact. The saved run file falsifies it.

## Post-registered construct-validation question — 2026-07-18

Among ADB-economy rows in UNICEF's 2024 climate-related school-disruption annex
whose major hazard is heatwave, does the inherited index preserve the rank
order of affected-student counts?

## Locked rules

- Data object: UNICEF Annex 1 country, affected-student count, and major hazard.
- Roster: 43 ADB economies used by the research factory.
- Construct-relevant subset: `major_hazard == Heatwave`.
- Missing annex rows: unknown, never zero.
- Primary statistic: Spearman rank correlation between old index and affected
  count.
- Comparators: child population, historical annual tasmax, and primary
  pupil-teacher ratio.
- Uncertainty: 5,000 deterministic bootstrap resamples per correlation.
- Denominator diagnostic: sum the latest non-null WDI pre-primary, primary,
  and secondary enrollment observations from 2015–2025 only when all three
  levels are present.
- Sensitivity: retain and reread the original ±50% run ledger; do not create a
  new tuning grid to improve alignment.

## Decision rule

Retire the country ranking if either the public robustness statement is false
or the observed outcome check does not preserve its ordering. No alternative
country ranking will be published from this sample.

## Scope

The validation is descriptive. It does not estimate causal heat effects,
closure duration, attendance loss, learning loss, or education-system quality.
