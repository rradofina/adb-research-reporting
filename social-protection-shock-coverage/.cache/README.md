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

`scripts/build-covid-response-validation.py` also uses the official World Bank
*Global Database on Social Protection and Jobs Responses to COVID-19*, version
15 (14 May 2021). The 3,197-page public PDF is cached under
`.cache/covid-response-validation/`, verified by SHA-256 in the generated
validation JSON, and is not committed. The parser reads the source's instrument-
presence matrix on PDF pages 5–10; it does not infer delivery success from a
checkmark.
