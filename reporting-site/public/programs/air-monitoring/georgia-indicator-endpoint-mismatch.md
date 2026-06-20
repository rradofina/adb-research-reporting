---
attestation_chain: ai-first
status: computed_georgia_indicator_endpoint_mismatch
method: air_monitoring_georgia_indicator_endpoint_mismatch_v1
---

# Georgia Indicator Endpoint Mismatch

## Why this source pass was needed

The Georgia report/export ladder shows that target station codes appear in official report routes, but the live-data caution remains. The NEA station network wall adds city-level launch and network context without station-code closure. This pass tests another official source family exposed by the air.gov.ge page template: the indicator API and daily API route.

## What the scan finds

- Indicator API station objects: 136
- Exact target station-code matches: 0
- Target rows with city/address alias context in the indicator API: 14
- Daily endpoint verified-closure rows: 0
- Complete monitor-grade rows: 0

The result is a source-family falsifier. The indicator API is real and public, but it uses a different station-code namespace for nearby city stations. It does not close the exact station-code, verified-report, status, calibration, grade, or station-radius gates.

## Reproduce

```powershell
python -m py_compile air-monitoring\scripts\scan-georgia-indicator-endpoint-mismatch.py
python air-monitoring\scripts\scan-georgia-indicator-endpoint-mismatch.py
```

Outputs:

- `generated\air-monitoring-georgia-indicator-endpoint-mismatch.csv`
- `generated\air-monitoring-georgia-indicator-endpoint-mismatch-summary.json`
