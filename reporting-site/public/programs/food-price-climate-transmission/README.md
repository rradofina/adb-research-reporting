# Food-price climate transmission — construct validation

**Maturity:** PP · construct-validation checkpoint

`attestation_chain: ai-first`

## Finding

The annual DMC qualifier and the old Nepal price-wave method are retired as
research findings.

- Correcting price levels to year-on-year market price change reduces flagged
  coarse-rice spike cells from **259 to 152**.
- **17 of 152** corrected spike cells follow locally dry rainfall at the main
  one-month lag; **135 do not**.
- Dry alignment remains a minority in all **81** ±50% threshold runs.
- Annual headline CPI and median market rice-price change have Spearman **+0.21**
  over five years; the objects are not interchangeable.
- Nepal sits outside the inherited annual top-10 intersection.

This is a measurement and replication-boundary result, not a climate-effect
estimate or a replacement country ranking.

## Evidence objects

- WFP coarse-rice retail prices in 12 Nepal markets, 2019–2025.
- NASA POWER monthly point rainfall at the same market coordinates, 2018–2025.
- 760 market-month observations with year-on-year price and one-month-lag rain.
- 81-run threshold factorial plus 0-, 1-, 3-, and 6-month lag checks.
- World Bank headline CPI context for 2020–2024 and the inherited DMC screen.

## Main outputs

- `generated/food-price-construct-validation.json`
- `generated/food-price-market-month-corrected.csv`
- `generated/food-price-market-year.csv`
- `generated/food-price-threshold-sensitivity.csv`
- `generated/charts/food-price-*.{png,svg}`
- `articles/food-price-joint-qualifier.md`

## Reproduce

See `REPRODUCE.md`. The claim-enabling sequence is:

```powershell
python research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py
python food-price-climate-transmission/scripts/build-construct-validation.py
python food-price-climate-transmission/scripts/build-figure-dossier.py
```

## Next qualified study

Join dated geocoded hazards, several commodities, crop and sourcing zones,
market access, fuel, exchange-rate, trade, and policy controls. Use an
event-study, fixed-effects, or local-projection design. Do not tune the annual
country screen as a substitute.
