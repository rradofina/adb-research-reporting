# Food-price climate-transmission cache notes

`scripts/audit-food-import-source-readiness.py` regenerates the public-source
cache under `.cache/food-import-source-readiness/`.

The script fetches:

- World Bank WDI `FP.CPI.TOTL.ZG`
- World Bank WDI `TM.VAL.AGRI.ZS.UN`
- World Bank WDI `TM.VAL.FOOD.ZS.UN`
- HDX package metadata for `wfp-food-prices`
- a small byte-range header sample from the WFP food-prices CSV

Cache contents are reproducible from public sources and are not committed.
Generated audit outputs are committed under `generated/`.
