---
attestation_chain: ai-first
status: Screening Result
method: air_monitoring_uzbekistan_blocker_external_context_v1
---

# Uzbekistan blocker external-context wall

## Why this pass exists

The Uzbekistan endpoint wall leaves three exact station rows blocked:
IDs 107 and 737 have stale detail pages whose regional rows say
`Updating data`, while ID 728 has a recent Sergili detail page with a
`-9999` PM2.5 sentinel. This pass asks whether public official or
technical context outside those telemetry pages resolves the exact
blockers.

## What the public sources add

- External source URLs seeded: 4.
- External source URLs retrieved: 4.
- Rows with any external context: 2.
- Rows with launch context only: 1.
- Rows with source-level reference context only: 1.
- Rows with exact station-ID external context: 0.
- Public blocker-resolution rows: 0.
- Complete monitor-grade rows: 0.

## Reader use

Use this as the distinction between context and closure. The government
launch note makes Sergili/Sergeli visible as an official automatic
station launch, and the technical source keeps source-level Tashkent
reference-grade context visible. Neither source names the exact blocker
station ID with a public correction/status/calibration record that
clears the stale, sentinel, or endpoint-disagreement blocker.

## Non-claim

This scan checks public official or technical context outside the exact Uzbekistan telemetry pages. Launch, platform-integration, or reference-grade context does not resolve a stale detail page, a -9999 PM2.5 sentinel, endpoint disagreement, current operating status, complete monitor-grade classification, or station-radius readiness unless a public source names the exact station row and gives explicit correction/status or grade language.

## Reproduce

Run `python air-monitoring/scripts/scan-uzbekistan-blocker-external-context.py`.
The source list is `air-monitoring/source-inputs/uzbekistan-blocker-external-context-source-seed.csv`.
Outputs are `air-monitoring/generated/air-monitoring-uzbekistan-blocker-external-context.csv`
and `air-monitoring/generated/air-monitoring-uzbekistan-blocker-external-context-summary.json`.
