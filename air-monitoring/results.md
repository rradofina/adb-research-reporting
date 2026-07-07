# Results -- Air-monitoring public QA observability

`attestation_chain: ai-first`. L3 candidate evidence package. Generated from
`air-monitoring/scripts/build-evidence-ledger.py` and
`air-monitoring/generated/air-monitoring-evidence-ledger.json`.

## Finding

The current air-monitoring evidence packet supports a documented-absence
finding, not a station-radius coverage finding. Public sources provide station
lists, method language, dashboard status, denominator geometry, and source
routes, but the public station-level QA evidence needed to validate a coverage
claim remains absent in the audited packet.

## What the generated ledger sees

The ledger script reads 64 committed summary JSON files and indexes 214
supporting files. Its headline counts are:

| Gate | Public evidence found |
|---|---:|
| Economies in source discovery | 24 |
| Economies with an official station source or portal | 9 |
| Official station rows audited for monitor-grade evidence | 239 |
| Official/OpenAQ identity candidate rows checked | 44 |
| Validated same-station rows | 0 |
| BMKG PM2.5 target rows with method/display/status context | 22 |
| BMKG station-specific inspection-log rows | 0 |
| BMKG station-specific calibration-certificate rows | 0 |
| BMKG calibration-status rows | 0 |
| Complete monitor-grade rows in the coverage gate | 0 |
| Station-radius-ready economies | 0 |
| Denominator join rows computed | 831 |
| Coverage-claim rows allowed | 0 |

## Interpretation

The result is a public observability gap. The audit can say that several
official and regulator-facing source routes are visible, and that some rows
carry method or dashboard context. It cannot say that monitors are
station-level calibration traceable, inspection traceable, or ready for
station-radius population or exposure coverage claims.

The useful contribution is therefore negative but substantive: for this audit
queue, public evidence is not enough to validate station-level monitor quality
or same-station joins. The absence is documented by named source routes,
retrieval states, row scopes, and zero-valued claim gates rather than by model
memory or a general web-search impression.

## What this cannot say

This packet does not prove that calibration certificates or inspection logs do
not exist. It says they were not public in the audited routes. A future public
release of station-level certificates, inspection logs, calibration-status
rows, or official/OpenAQ crosswalks would change the claim.

This packet also does not estimate population coverage, PM2.5 exposure, monitor
performance, or regulatory performance. The denominator dry runs stay as
geometry and custody evidence until station identity and monitor-grade gates
close.

## Reproduce

Run:

```powershell
python air-monitoring\scripts\build-evidence-ledger.py
```

Primary outputs:

- `air-monitoring/generated/air-monitoring-evidence-ledger.json`
- `air-monitoring/generated/air-monitoring-evidence-ledger.csv`
