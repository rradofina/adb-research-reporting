# Air Monitoring Station-Radius Radius-Rule Source Scan

attestation_chain: ai-first

## Status

This gate freezes a source-based diagnostic radius rule before any catchment population is computed. The primary dry-run band is 4.0 km, with 0.5 km and 50.0 km sensitivity bands.

## Evidence Counts

| Check | Count |
|---|---:|
| Seed sources | 2 |
| Retrieved sources | 2 |
| Spatial-scale evidence rows | 4 |
| Rule-selected evidence rows | 4 |
| Catchment population rows | 0 |

## Frozen Rule

| Rule element | Value |
|---|---|
| Primary radius | 4.0 km |
| Primary label | PM2.5 neighborhood-scale upper-bound diagnostic |
| Sensitivity radii | 0.5 km / 50.0 km |
| Tile envelope | 50.0 km |
| Claim guardrail | Report these as diagnostic spatial-scale bands only. They are not service areas, legal station representativeness determinations, or monitor-grade coverage claims. |

## Public Sources Retrieved

| Source | Family | Status | HTTP | Cached bytes |
|---|---|---:|---:|---:|
| [40 CFR Part 58 Appendix D network design criteria](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-58/appendix-Appendix%20D%20to%20Part%2058) | official_regulatory_text | retrieved | 200 | 202615 |
| [EPA ambient air monitoring network assessment guidance](https://www.epa.gov/sites/default/files/2020-01/documents/network-assessment-guidance.pdf) | official_guidance_pdf | retrieved | 200 | 2305122 |

## Selected Source Evidence

| Evidence row | Role | Extracted scale | Radius | Reader use |
|---|---|---|---:|---|
| ecfr_neighborhood_scale_range | primary_radius_source | neighborhood | 4.0 km | Select 4 km as the primary PM2.5 neighborhood-scale upper-bound diagnostic radius. |
| ecfr_urban_scale_range | upper_sensitivity_source | urban | 50.0 km | Keep 50 km as the upper sensitivity radius and as the already-used tile-selection envelope. |
| ecfr_pm25_neighborhood_priority | pm25_scale_priority | PM2.5 neighborhood priority |  | Treat neighborhood-scale PM2.5 as the primary interpretation, not the 50 km tile envelope. |
| ecfr_middle_scale_boundary | lower_sensitivity_source | middle-to-neighborhood boundary | 0.5 km | Use 0.5 km as the lower sensitivity boundary between middle and neighborhood scale. |

## Gate Ledger

| Gate | Status | Rows | Reader use |
|---|---|---:|---|
| Public source retrieval | available | 2 | Confirms the current public source pages are reachable before freezing a radius rule. |
| Neighborhood-scale PM2.5 source | available | 1 | Supports 4 km as the primary diagnostic upper-bound band. |
| Urban-scale sensitivity source | available | 1 | Supports 50 km as the upper sensitivity band and existing tile envelope. |
| Lower sensitivity boundary | available | 1 | Supports 0.5 km as the lower middle/neighborhood boundary sensitivity check. |
| Catchment computation | not_computed | 0 | No population, exposure, join, grade, or map is computed in this source gate. |

## What This Does Not Mean

This radius-rule source scan uses public spatial-scale guidance to freeze diagnostic station-radius bands for a future dry run. It does not compute station buffers, catchment population, PM2.5 exposure, monitor coverage, same-station joins, or complete monitor-grade classification.

## Reproduce

```powershell
python air-monitoring\scripts\scan-station-radius-radius-rule-sources.py
```
