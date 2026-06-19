# Sensitivity — Air Pollution Without Air Monitors

`attestation_chain: ai-first`. Run 2026-04-27.

| Variant | Top-5 |
|---|---|
| Gap-score (baseline, pre-registered) | AFG, BGD, MMR, UZB, TJK |
| Zero-monitor + above-WHO-guideline subset | (different question — see §1.3) |

The pre-registered headline metric is the gap-score, which combines
people-per-monitor with PM2.5-exposure above the 5 µg/m³ WHO 2021
guideline. The "zero-monitor-above-guideline" subset is an
informative alternative question but tests a different proposition.

The gap-score top-5 is **stable by construction** — the formula
combines the two inputs deterministically, and the 5 µg/m³ guideline
is WHO-anchored (not a tunable parameter). Sensitivity is therefore
limited to alternative *formulations*, not alternative parameter
values.

## TODO §18.5

- ACAG-V6 satellite-derived 1-km gridded PM2.5 (Dalhousie) for
  subnational exposure (currently country-mean WDI).
- Annual-update cadence; OpenAQ monitor density changes.
