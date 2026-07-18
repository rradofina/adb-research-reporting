# Reproduce — social-protection construct validation

`attestation_chain: ai-first` · PP

## Environment

- Python 3.13
- `pandas`, `numpy`, `matplotlib`, `pypdf`, `Pillow`
- public World Bank WDI API and official World Bank COVID-19 response PDF

## Commands

Run from the repository root:

```powershell
python social-protection-shock-coverage/scripts/process-sp.py
python social-protection-shock-coverage/scripts/deepen-include-partial.py
python social-protection-shock-coverage/scripts/audit-social-protection-source-readiness.py
python social-protection-shock-coverage/scripts/build-covid-response-validation.py
python social-protection-shock-coverage/scripts/build-figure-dossier.py
```

The WDI scripts refresh public JSON into ignored `.cache/` directories. The
COVID parser downloads the official 3,197-page PDF if its cache is absent,
checks the payload type, and records byte size, SHA-256, page count, retrieval
date, and parsed page range in
`generated/social-protection-covid-response-validation.json`.

## Main outputs

- `generated/social-protection-dropped-leg.json`
- `generated/social-protection-source-readiness.json`
- `generated/social-protection-covid-response-validation.json`
- `generated/social-protection-covid-response-diagnostics.csv`
- `generated/charts/sp-*.{png,svg}`

The response-matrix parser uses explicit page-specific column anchors for the
eight source-defined categories. It treats missing matrix rows as not
documented, never as no response.
