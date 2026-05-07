# Sensitivity — Flood Market Access

`attestation_chain: ai-first`. Run 2026-04-26.

| Variant | Top-5 |
|---|---|
| Full index (baseline) | IND, IDN, CHN, AFG, PAK |
| Flood-events-only | CHN, IND, IDN, PHL, BGD |
| Rural × floods | AFG, IND, IDN, CHN, NPL |

**Common top-4: `[AFG, CHN, IDN, IND]`.** Top-5 is metric-sensitive.

Honest narrowing to top-4. Pakistan and Philippines drop in
flood-events-only; Bangladesh and Nepal drop in the multiplicative
formulations.

## TODO §18.5

- Sentinel-1 SAR-derived inundation extent for direct exposure.
- Modeled flood layers (e.g., GLOFAS) for forward-looking risk.
- Per-event timestamp + market-access (road density) integration.
