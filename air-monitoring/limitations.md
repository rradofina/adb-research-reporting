# Limitations -- Air-monitoring public QA observability

`attestation_chain: ai-first`. Updated 2026-07-07.

## Scope

The active claim is a public-evidence absence finding. It says the audited
public routes do not expose enough station-level QA evidence to support
station-radius monitor coverage claims.

It does not say that calibration certificates, inspection logs, or
station-code crosswalks do not exist outside the audited public routes.

## Main limits

1. **Public-route limit.** The result is bounded by the public sources named
   in the generated ledger and its source-input summaries.
2. **No private or credentialed evidence.** The project uses public data only.
   Nonpublic regulator files, internal QA ledgers, or restricted portals are
   outside scope.
3. **No monitor certification.** Method or dashboard context is not treated as
   station-level calibration, inspection, or complete monitor-grade evidence.
4. **No same-station assumption.** Official and OpenAQ rows are not joined
   unless public evidence supports the same-station identity.
5. **No coverage estimate.** GHSL/ACAG denominator rows and station-radius dry
   runs are geometry/custody evidence only until identity and grade gates close.
6. **No performance claim.** The packet does not rank regulators, agencies, or
   monitor networks by performance.

## What would overturn or narrow the finding

A public source can change the result if it contains at least one of:

- station-level calibration certificates;
- station-level inspection logs;
- station-level current calibration-status rows;
- official station-code crosswalks that validate official/OpenAQ identity;
- a public method-grade ledger with station identifiers.

Generic source expansion is not enough. A new search pass must name the source
route and why it plausibly contains one of those records.

## Reproduce

Run:

```powershell
python air-monitoring\scripts\build-evidence-ledger.py
```

Then inspect:

- `air-monitoring/generated/air-monitoring-evidence-ledger.json`
- `air-monitoring/generated/air-monitoring-evidence-ledger.csv`
