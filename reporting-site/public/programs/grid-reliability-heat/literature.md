# Literature review — Grid Reliability under Heat

`attestation_chain: ai-first`. §18 AI-finalized 2026-04-27.

## 1. Search record

Queries (2026-04-26):
1. `WRI Global Power Plant Database fuel concentration LMIC`
2. `IEA Electricity 2024 capacity additions Asia`
3. `Herfindahl fuel-mix grid fragility`
4. `single-fuel grid hydro drought reliability`

Tier-A: *Energy Policy*, *Nature Energy*, *Joule*. Tier-B: IEA, IRENA,
WRI Energy. Tier-C: ADB Energy Sector Group reports.

## 2. Verified entries

- **`wri2022plants`** — WRI Global Power Plant Database v1.3.0
  (frozen 2022). **Primary data source. Cited with the explicit
  vintage caveat.**
- **`iea2024electricity`** — IEA Electricity 2024 report.
  **The §18.5 upgrade-pass source for current-capacity additions
  not in WRI v1.3.0.**

## 3. Synthesis

Two established facts:

1. **Single-fuel grids are exposed to fuel-specific shocks.**
   Hydro to drought, gas to global price swings, coal to carbon-
   transition risk. The Herfindahl is a defensible single-number
   summary [@wri2022plants].
2. **The 2022–2025 solar buildout is unevenly distributed across
   ADB DMCs.** IEA 2024 [@iea2024electricity] documents capacity
   additions that are missing from WRI v1.3.0.

## 4. Gap

No cross-DMC sensitivity-tested top-N concentration cluster has
been published for the ADB regional roster. WRI publishes the
plant database; the top-5 set-stability claim across the alternative
single-fuel-share definition is a derivative finding.

## 5. Risk of redundancy

IEA capacity reports rank installed capacity. The marginal
contribution here is the set-stability claim across the
fuel-Herfindahl and single-fuel-share-≥-80% definitions.

## 6. First testable claim

> Five ADB DMCs — Brunei, Bhutan, Mongolia, Nepal, Tajikistan —
> persistently rank in the top five most-fuel-concentrated grids
> across both fuel-Herfindahl and single-fuel-share ≥ 80%
> definitions.

## 7. §18 attestation

`ai-first`. 2026-04-27.
