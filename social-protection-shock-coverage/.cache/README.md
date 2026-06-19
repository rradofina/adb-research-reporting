# Social-protection shock-coverage cache notes

`scripts/audit-social-protection-source-readiness.py` regenerates the public
source cache under `.cache/source-readiness/`.

The script fetches World Bank WDI data and metadata for:

- `per_allsp.cov_pop_tot`
- `per_sa_allsa.cov_pop_tot`
- `FX.OWN.TOTL.ZS`
- `SI.POV.DDAY`
- `SI.POV.GAPS`

Cache contents are reproducible from public sources and are not committed.
Generated audit outputs are committed under `generated/`.
