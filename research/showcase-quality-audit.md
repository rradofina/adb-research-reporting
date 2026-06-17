# Showcase quality audit

`attestation_chain: ai-first`
Date: 2026-06-17

Purpose: keep the 20-report ADB/ERDI showcase honest. A route with a good
visual is not automatically publication ready. This audit records the current
stage, the strongest use case, the remaining publication gap, and the next
upgrade for each report.

## Stage definitions

| Stage | Meaning | Promotion condition |
|---|---|---|
| L2 prototype | Public-source sprint or bespoke surface is visually and narratively useful, but the program package is not yet complete | Move to L3 only after a program folder records source coverage, method, sensitivity, limitations, and a reproducible evidence packet |
| L3 candidate | Strongest current reports for the next deepening loop; evidence already points to a plausible program package | Build or repair the program package, rerun scripts, write limitations and review response, then update maturity labels only if gates pass |
| Evidence audit | Useful falsification or source-audit page that explains why an existing proxy should not be overclaimed | Either add the missing source layer or demote to a methods caution note |
| Owner-gated | Public-side work is transparent, but the next required source or attestation depends on owner-controlled access or coauthor review | Pause before owner-only access or human-final/coauthor claims |

## Portfolio read

Current distribution:

- 3 L2 prototypes: reports 1-3.
- 5 L3 candidates: reports 4-8.
- 11 evidence audits: reports 9-10 and 12-20.
- 1 owner-gated report: report 11.

This is a stronger bench than a topic gallery, but it is not yet a
publication-ready 20-report package. The next loop should deepen the L3
candidates before adding new surfaces.

## Report audit table

| # | Report | Current stage | Why it counts now | Publication gap | Next upgrade |
|---:|---|---|---|---|---|
| 1 | Market-level climate price transmission | L2 prototype | Public WFP/NASA POWER sprint, interactive market-month heatmap, and clear non-causal caveat | Needs commodity expansion, alternative rainfall source, and non-climate price falsifiers | Convert the Nepal sprint into an L3 market-price package |
| 2 | Public data freshness blind spots | L2 prototype | Public WDI API matrix makes stale and missing indicator vintages visible | Needs indicator-specific refresh expectations and non-applicability rules | Add source-specific refresh cadence labels |
| 3 | Shock-payment rails after disasters | L2 prototype | Public disaster, payment-use, and social-protection proxies are concept-separated | Needs payment-channel metadata and emergency-transfer validation | Add payment-channel source scan and vintage checks |
| 4 | PSDQ source disagreement | L3 candidate | Mature PSDQ program spine plus source-disagreement visual and public artifacts | Needs facility-level matching sample and independent validation layer | Package BGD source-disagreement with matching strata and validation notes |
| 5 | Remittance corridors after flow weighting | L3 candidate | Flow-weighting sprint directly repairs a current flagship claim | Needs parser coverage notes and formal review-loop response | Move sprint into remittance L3 package |
| 6 | Air-monitoring observability | L3 candidate | Deepening artifacts and bespoke visuals make the monitoring observability gap legible | Needs station-radius sensitivity and regulatory-inventory comparison | Build air-monitor catchment package |
| 7 | Access map-completeness audit | L3 candidate | Registry comparison artifacts and source-audit visuals show when OSM access maps are incomplete | Needs more registry joins and travel-time/catchment denominator | Extend official registry joins and add public friction validation |
| 8 | Disaster metric falsification | L3 candidate | Alternate EM-DAT burden metrics visibly break the original pair | Needs event-level recovery curves and exposure denominator | Build recovery-lag source plan before reusing the hook |
| 9 | Power-fuel concentration audit | Evidence audit | Capacity-versus-generation bridge keeps generation coverage visible | Needs outage, reserve-margin, dispatch, or heat-stress evidence | Search for public reliability proxies |
| 10 | Emigration denominator switch | Evidence audit | Absolute-stock versus population-share ranks reveal denominator dependence | Needs corridor composition and migration-purpose split | Build corridor-type falsifier |
| 11 | MPI night-light blind spot | Owner-gated | MPI-side decomposition shows what night lights cannot directly see | Needs owner-led VIIRS/Earth Engine access and coauthor attestation | Keep as methods note until owner-gated access clears |
| 12 | Coastal population-denominator audit | Evidence audit | No-population rank bridge prevents a size-driven coastal proxy from overclaiming | Needs settlement footprints, elevation, and surge-zone overlay | Choose one-coast pilot and join settlement/hazard layers |
| 13 | Flood component decomposition | Evidence audit | Per-capita rerank shows the flood proxy is mostly event counts and population size | Needs roads, markets/services, flood footprint, and travel-time logic | Build one-DMC flooded-network pilot or demote to methods caution |
| 14 | Climate-health measurement repair | Evidence audit | PM2.5 cap lanes reveal drift toward labor-share ranking | Needs labor-force denominator and heat exposure evidence | Repair denominator and lead with cap sensitivity |
| 15 | Food-price coverage trap | Evidence audit | Coverage funnel foregrounds missing CPI/import indicator legs | Needs household or market price exposure evidence | Join a market-price or household-expenditure source |
| 16 | Social-protection dropped leg | Evidence audit | Missing-leg ledger shows why some economies disappear from the headline | Needs payment-channel or beneficiary delivery data | Rebuild as coverage-versus-payment-rail observability |
| 17 | Water denominator artifact | Evidence audit | Internal-water denominator cards expose above-100-percent artifacts | Needs total-renewable-water, basin, and crop-area data | Rebuild with AQUASTAT/FAOSTAT or demote to denominator caution |
| 18 | Invisible urbanization tautology | Evidence audit | Rank-preserving scalar sweep is visibly not a robustness test | Needs satellite/built-up layer and classification history | Select one pilot and replace the WDI-only proxy |
| 19 | Port inert-parameter audit | Evidence audit | Cap-binding wall shows an inert sensitivity knob | Needs actual hinterland travel-time, logistics, or port-performance source | Search for public port/hinterland travel-time proxies |
| 20 | School heat top-one audit | Evidence audit | Sensitivity ledger names discriminating, degenerate, and rank-losing runs | Needs school geocodes, calendars, enrollment, and local heat exposure | Pick a public school-location pilot or keep as sensitivity caution |

## Current QA evidence

- The reporting site builds with `npm run build`.
- The deterministic gates pass: citations, composite headlines, WIP, DMC
  framing, banned words, and source-version checks.
- Screenshot QA exists under `reporting-site/qa/` for the 20-report batch and
  the later depth-standard pass.
- The current site surfaces operational use, falsifiers, evidence paths, source
  stacks, limitations, and next upgrades. That is evidence of a stronger
  showcase bench, not evidence of publication readiness.
- Static showcase pages 1-8 now use the same shared QA/readiness panel as the
  portfolio ladder: current stage, operational use, falsifier, publication gap,
  next upgrade, evidence path, and source stack. Dynamic audit pages 9-20
  already render equivalent QA readouts from the same registry.
- Focused browser QA on the remittance-flow static report confirmed the shared
  QA panel, next-upgrade text, and zero mobile horizontal overflow. Build and
  source audit confirm the shared component is wired into all static reports
  1-8. Screenshot:
  `reporting-site/qa/showcase-remittance-readiness-panel-mobile.png`. The full
  multi-route browser batch should be rerun later if the browser CLI stops
  timing out on long loops.

## Next deepening order

1. Remittance flow weighting, because it repairs the active flagship.
2. PSDQ source disagreement, because the program spine is already mature.
3. Air-monitoring observability, because the visual hook is strong and the
   next source upgrade is concrete.
4. Access map-completeness, because official registry joins can turn a source
   audit into a defensible planning note.
5. Disaster metric falsification, only after a true recovery-lag source object
   exists.
