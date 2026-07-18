# Social protection shock coverage

**Maturity:** PP · construct-validation checkpoint
**Attestation:** `attestation_chain: ai-first` · no individual external reviewer contacted

## Finding

The inherited “stable top five” is rejected. Only three named members survive
the panel's own descending value order. Vanuatu and Tajikistan outrank the
Philippines and Bangladesh but were omitted because each lacks one proxy leg.
A public World Bank COVID-19 response matrix records cash-transfer instruments
in all five named economies, yet supplies no comparable successful-receipt,
delivery-time, payment-failure, or shock-trigger outcome.

## Research question

Does a poverty × (one minus social-protection/account-ownership) composite
preserve its own ranking rule and align with a qualified observed-response
object strongly enough to support a shock-payment-readiness interpretation?

## Decision

No. Retire the country ranking. Publish the construct failure and the precise
delivery data needed for a future study.

## Reproduce

```powershell
python social-protection-shock-coverage/scripts/process-sp.py
python social-protection-shock-coverage/scripts/deepen-include-partial.py
python social-protection-shock-coverage/scripts/audit-social-protection-source-readiness.py
python social-protection-shock-coverage/scripts/build-covid-response-validation.py
python social-protection-shock-coverage/scripts/build-figure-dossier.py
```

Raw public responses are cached under `.cache/`; generated diagnostics and all
article figures are committed under `generated/`. The main paper is
`articles/sp-shock-readiness-cluster.md`.
