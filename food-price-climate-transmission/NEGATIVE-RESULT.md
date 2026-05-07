# Sensitivity-suite negative result — Food Price Climate Transmission

`attestation_chain: ai-first`. 2026-04-26.

## Status

The sensitivity-run for this program produced **no stable top-5 set**
across the alternative metric formulations (full vulnerability index,
CPI-inflation only, ag-imports-share only). Decision rule per a
hypothetical pre-registration would fail.

**This program does NOT advance to SR under §18.** It remains at PP
until the index design is reformulated.

## What this means

The current `food_price_vulnerability` index over-weights one of its
sub-components depending on parameter choice. Different sub-components
produce wildly different top-5 sets. There is no defensible single
top-5 to commit to.

## What's needed for SR-readiness

1. **Reformulate the metric** so a stable cluster emerges. Candidates:
   - Joint inflation × ag-import-dependence threshold (DMCs above
     both thresholds), removing the sub-metric averaging.
   - Restrict to climate-transmission proxy (ag-CPI minus core CPI),
     which is the program's named claim.
2. **Test the new formulation** with a fresh ±50% sensitivity suite.
3. **Re-attempt SR promotion.**

## §18.5 upgrade-pass scope

Re-design the metric. Current pipeline output retained at
`generated/food-price-adb-panel.{json,csv}` for reference.
