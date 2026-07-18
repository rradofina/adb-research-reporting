# Reproduce — Water stress × crop diversification

`attestation_chain: ai-first`

Run from the repository root with Python 3.11+.

## Full pipeline

```bash
python water-stress-crop-diversification/scripts/process-water-crop.py
python water-stress-crop-diversification/scripts/deepen-denominator.py
python water-stress-crop-diversification/scripts/audit-water-source-readiness.py
python water-stress-crop-diversification/scripts/build-construct-validation.py
python water-stress-crop-diversification/scripts/build-figure-dossier.py
```

## Public inputs

- World Bank WDI API for `ER.H2O.FWTL.ZS`, `ER.H2O.FWST.ZS`,
  `ER.H2O.FWTL.K3`, `ER.H2O.INTR.K3`, and `SP.RUR.TOTL.ZS`.
- FAOSTAT Crops and Livestock Products normalized bulk ZIP, element Area
  harvested.
- The inherited WDI cache for cereal yield and land-use context.

Raw responses are cached under `.cache/` and are excluded from version control.
The generated JSON records URLs, response hashes, retrieval mode, byte sizes,
source metadata, year coverage, and filtered-row counts.

## Determinism

- Latest non-null WDI values are selected by economy.
- FAOSTAT crop year 2024 is the latest usable year in the refreshed source.
- Aggregate crop-item labels are excluded by a committed list.
- Bootstrap intervals use 5,000 resamples with fixed seeds beginning at 64202.
- The 27 diagnostic sensitivity specifications are the Cartesian product of
  0.5×, 1×, and 1.5× choices for the water ceiling and crop/rural exponents.

## Expected headline checks

```text
Roster / old rankable / crop / aligned: 43 / 30 / 41 / 30
Published set vs direct water top five: 2 of 4
Published set vs direct crop-HHI top five: 0 of 4
Crop-HHI top five with water data: 0 of 5
Old exact top-four matches: 2 of 7 runs
```

Any change requires inspecting source versions, regenerated figures, and the
claim decision before publication.
