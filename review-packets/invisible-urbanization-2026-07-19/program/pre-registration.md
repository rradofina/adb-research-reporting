# Retrospective design freeze

`attestation_chain: ai-first` · Retrospective pre-analysis record · 2026-07-19

This design was frozen after the public GHS-DUC schema was inspected and before
the full narrative was written. It is retrospective and must not be described
as a prospective pre-registration.

## Primary estimands

1. **Definition gap:** GHSL level-0 urban share minus WDI
   `SP.URB.TOTL.IN.ZS`, in percentage points, at matching five-year epochs.
2. **Embedded urban population:** `UCentre_Pop + UCluster_Pop` inside a GHS-DUC
   administrative unit where `DEGURBA_L1 = 1`.
3. **Embedded share:** embedded urban population divided by all GHSL
   urban-centre-plus-urban-cluster population in the covered economy sample.

## Primary population and period

- Repository's established 44-economy ADB developing-member roster.
- 2020 cross-section for the headline definition gap.
- 1975–2020 five-year epochs for persistence.
- GADM 4.1 level 2 for the transition analysis.
- 2000–2020 as the descriptive transition window.

## Decision rules

- Do not impute missing WDI observations or missing GADM levels.
- Aggregate multiple GADM level-0 fragments to `GID_0GHSL` before joining WDI.
- Compare administrative levels only on the intersection of economies present
  at levels 1, 2, and 3.
- Treat the definition-gap sign as descriptive; no direction is assumed.
- Do not convert a cross-source percentage-point gap to people.
- Do not label a GHS-DUC transition a national legal reclassification.

## Sensitivity plan

- Administrative scale: levels 1, 2, and 3 on the same economy sample.
- Time-window choice: vary the 20-year window by ±50%, using 10 and 30 years.
- Report both signed and absolute definition gaps.
- Report full coverage at each analytical layer.

## Falsification and stopping rules

- If the GHSL–WDI median absolute gap is trivial, retire the definition-gap
  story.
- If administrative-level results reverse or disappear on a common sample,
  do not claim scale sensitivity.
- If the transition decomposition does not close arithmetically, stop and fix
  the panel.
- The analysis cannot pass a legal-misclassification or policy-neglect claim
  without country-specific administrative and service evidence.
