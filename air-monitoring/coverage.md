# Coverage -- Air-monitoring public QA audit scope

`attestation_chain: ai-first`. Updated 2026-07-07.

This coverage note describes the scope of the public QA evidence audit. It does
not describe monitor population coverage.

Generated source: `air-monitoring/generated/air-monitoring-evidence-ledger.json`.

| Scope item | Count |
|---|---:|
| Ledger rows generated from committed summaries | 64 |
| Supporting files indexed | 214 |
| Economies in source discovery | 24 |
| Economies with an official station source or portal | 9 |
| Official station rows audited for monitor-grade evidence | 239 |
| Official/OpenAQ identity candidate rows checked | 44 |
| BMKG PM2.5 target rows with method/display/status context | 22 |
| Denominator join rows computed as non-claim geometry | 831 |

## Claim-enabling coverage

The audit does not yet cover station-radius population or exposure claims,
because the claim-enabling gates remain closed:

| Gate | Count |
|---|---:|
| Validated same-station rows | 0 |
| BMKG station-specific inspection-log rows | 0 |
| BMKG station-specific calibration-certificate rows | 0 |
| BMKG calibration-status rows | 0 |
| Complete monitor-grade rows in the coverage gate | 0 |
| Station-radius-ready economies | 0 |
| Coverage-claim rows allowed | 0 |

## Use

Use this file to understand what public evidence was indexed. Use
`results.md` for the finding and `sensitivity.md` for false-negative and source
expansion rules.
