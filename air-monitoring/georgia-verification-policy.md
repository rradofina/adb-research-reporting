---
attestation_chain: ai-first
status: Screening Result
method: air_monitoring_georgia_verification_policy_v1
---

# Georgia verification-policy wall

## Why this pass exists

The Georgia report/export ladder found exact station-code PM2.5 rows, but
the official monthly HTML and PDF export surfaces retained a not-verified
label. This pass checks the official policy pages that explain where
verification is supposed to live, then joins that policy signal back to the
report/export ladder.

## What the public sources show

- Official source routes retrieved: 5 of 5.
- Live-data-not-verified policy sources: 1.
- Sources saying verified data are available in reports: 1.
- Report-generator source routes available: 1.
- Network or instrument-model context source rows: 2.
- Management-plan validation/capture-rate context rows: 1.
- Monthly HTML report months still carrying not-verified labels: 24 of 24.
- PDF export probes retaining the not-verified footer: 3 of 3.
- Verified report-closure months found: 0.

## Reader use

Use this as a verification-surface map. It supports the stronger caveat that
Georgia has official monitoring, report, network, and policy context, but the
public surfaces retrieved by the pipeline still do not provide station-code
verified-report closure, station current status, calibration status, complete
method class, or station-radius readiness.

## Non-claim

This scan records official Georgia verification-policy, report-generator, network, and management-plan source language. It does not certify any target station as verified, currently operating, station-method classified, complete monitor-grade, or station-radius ready.

## Reproduce

Run `python air-monitoring/scripts/scan-georgia-verification-policy.py`.
The source list is `air-monitoring/source-inputs/georgia-verification-policy-source-seed.csv`.
Outputs are `air-monitoring/generated/air-monitoring-georgia-verification-policy.csv`
and `air-monitoring/generated/air-monitoring-georgia-verification-policy-summary.json`.
