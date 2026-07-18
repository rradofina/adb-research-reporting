# School heat disruption — construct validation

**Maturity:** PP · construct-validation checkpoint

`attestation_chain: ai-first`

## Finding

The inherited national ranking is rejected as a measure of school disruption.

- “Cambodia is first in every perturbation” is false: it leads **5 of 6**
  discriminating runs; Pakistan leads one; a seventh is an all-zero tie.
- UNICEF's 2024 annex contains **21** ADB-economy rows, including **6** whose
  major disruption hazard is heatwave.
- Cambodia ranks **6 of 6** by affected-student count in that subset.
- The old index has Spearman **+0.03** with affected counts; child population
  alone has **+0.94**.
- The subset is small and selected. This is a construct-validation result, not
  a replacement risk, safety, or resilience ranking.

## Evidence objects

- Inherited 32-economy WDI/CCKP proxy panel and seven sensitivity runs.
- UNICEF *Learning Interrupted* Annex 1, transcribed and programmatically
  checked against the public PDF: 21 ADB rows.
- World Bank Indicators API enrollment denominator diagnostic: 19 complete
  three-level denominators, including 17 rows overlapping the old panel.
- School × day × exposure × outcome join: **0 observations**.

## Main outputs

- `generated/school-heat-sensitivity-audit.json`
- `generated/school-construct-validation.json`
- `generated/school-construct-diagnostics.csv`
- `generated/school-construct-correlations.csv`
- `generated/charts/school-*.{png,svg}`
- `articles/school-heat-honest-narrowing.md`

## Reproduce

See `REPRODUCE.md`. The claim-enabling sequence is:

```powershell
python school-heat-disruption/scripts/deepen-sensitivity-audit.py
python school-heat-disruption/scripts/build-construct-validation.py
python school-heat-disruption/scripts/build-figure-dossier.py
```

## Next qualified study

Join daily local heat, school calendars, enrolled students and school
conditions, and an observed closure, attendance, assessment, or learning
outcome. Do not retune the national index as a substitute for that shared unit.
