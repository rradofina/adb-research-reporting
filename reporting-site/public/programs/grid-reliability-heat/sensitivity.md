# Sensitivity — Grid Reliability under Heat

`attestation_chain: ai-first`. Run 2026-04-26 by `scripts/batch-sensitivity.py`.

| Variant | Top-5 |
|---|---|
| fuel-Herfindahl baseline | BRN, BTN, MNG, NPL, TJK |
| Single-fuel-share ≥ 80% | (subset of same set) |

**Common top-5: `[BRN, BTN, MNG, NPL, TJK]`.** Stable across
alternative single-fuel definitions.

## TODO §18.5 upgrade-pass

- Reliability outcome (outage frequency × heat day) instead of just
  fuel concentration. The program name implies a heat-dependence
  question; current artifact is structural exposure only.
- WRI v1.3.0 frozen since 2022 — Geofabrik or IEA/Ember updated source
  needed.

## §18 attestation closed.
