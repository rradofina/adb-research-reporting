# Reproduce — Food-price climate transmission

`attestation_chain: ai-first`

Run from the repository root with Python 3.11+.

## Claim-enabling pipeline

```powershell
python research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py
python food-price-climate-transmission/scripts/build-construct-validation.py
python food-price-climate-transmission/scripts/build-figure-dossier.py
```

The upstream sprint may use its committed public-source cache. The construct
validation and figure scripts are deterministic and use only Python's standard
library.

## Public inputs

- WFP *Nepal - Food Prices* and market-location CSVs via HDX.
- NASA POWER monthly point API, corrected precipitation at 12 market points.
- World Bank Indicators API headline CPI inflation.
- The inherited annual DMC screen committed in this program.

Source URLs, timestamps, resource modification dates, and cache paths are
carried in the upstream JSON and `versions.json`.

## Expected checks

```text
Market-month cells with year-on-year price: 760
Corrected price-spike cells: 152
Dry-aligned cells at one month: 17
Dry share: 0.1118
Full threshold runs: 81
Annual overlap years: 5
Annual Spearman: 0.2052
Exact permutation p-value: 0.7333
```

Any upstream source change requires regenerating the evidence, reviewing the
threshold stability, and reconsidering the claim decision before publication.
