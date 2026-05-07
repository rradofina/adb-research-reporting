---
attestation_chain: ai-first
package_status: next_track_concept_package
topic_status: not_in_current_issue
program: road-quality-poverty-access
created: 2026-04-29
---

# Road Quality and Poverty Access

## 1. Problem Statement

Road access indicators often measure whether roads exist, but project teams
also need to know whether roads are passable, maintained, and connected to
schools, clinics, markets, and poor settlements. This package frames a road-
quality and poverty-access brief that would combine road networks, poverty and
population layers, facility locations, hazard layers, and road-quality
screening data to identify corridors where poor road condition may weaken
access. The output is a maintenance and access-prioritization screen, not a
replacement for engineering-grade International Roughness Index surveys.

## Marginal Contribution

The original contribution should not be framed as a new road-quality ML method.
ADB already has that line of work. The contribution is the spatial integration:
road-quality screening joined to poverty, settlement, facility, market, hazard,
and catchment geography at road-segment or municipality scale. The research
question is where road condition may matter most for poverty access and
service reach, and where field validation should be prioritized.

## 2. Key Messages

- This is a next-track candidate, not a finished result in the current issue.
  The existing access-services pilot has an 8-DMC facility-count access-stress
  result; it does not yet measure travel time, road condition, or passability.
- ADB already has a credible road-quality ML line: a 2022 Economics Working
  Paper, a 2025 guidebook, and a 2026 Scientific Reports paper involving
  Arturo Martinez Jr. and ADB coauthors.
- The current 2026 lesson is methodological humility: satellite-image
  super-resolution improved visual quality but did not improve road-roughness
  classification; combining native imagery with contextual covariates
  performed better.
- The repository's angle should not be "we have a better AI model." The
  stronger angle is "connect road-quality screening to poverty, facility,
  market, hazard, and settlement granularity for project prioritization."

## 3. Evidence Spine

- Current unit in repo: access-services has an 8-DMC, 104-ADM1 pilot using
  facility-count access stress; Bangladesh, Cambodia, Lao PDR, and Pakistan
  form the stable top-4 access-stress set under the current aggregation test.
- Target unit: road segment, village or settlement, municipality, clinic,
  school or market catchment, and poverty-exposed corridor.
- Source stack: OSM/Overture/GRIP road networks, ADB road-quality ML workflow,
  Mapillary or other road-surface predictions, Google Open Buildings 2.5D
  Temporal for settlement growth, Google Groundsource for urban flash-flood
  history, IRI or smartphone validation where available, WorldPop/GHSL, OPHI
  MPI or World Bank poverty data, service facility locations, flood and
  landslide layers.
- Repository evidence: `access-services/results.md`,
  `access-services/limitations.md`, `reporting-site/src/data/briefs.ts`,
  and `reporting-site/src/data/sourceUpgrades.ts`.
- Claim status: concept package only. It can become a paper package after a
  road-quality validation source and at least one spatial overlay are
  committed.

## 4. Proposed Section Outline

1. Why road presence is not enough for poverty access
2. Existing ADB road-quality ML work and what it establishes
3. Data design for segment-level road quality, poverty, hazards, and services
4. Validation hierarchy: IRI, smartphone roughness, surface type, and proxy
   confidence
5. Prioritization screen for road segments and catchments
6. Limitations: screening versus engineering inspection
7. Policy use for maintenance planning and project preparation

## 5. Figure and Table Plan

1. Road-quality and poverty-access corridor map.
   - Chart type: map with road segments, poor-road screen, population/MPI
     exposure, and clinic/school/market catchments.
   - Source note: Author calculations using road-network data, road-quality
     proxy or validation source, population and poverty layers, facility or
     market locations, and hazard surfaces. Unit = road segment or catchment.
     Values are screening indicators, not engineering-grade pavement surveys.
2. Model-validation panel.
   - Chart type: confusion matrix or predicted-versus-observed road-quality
     class where IRI or smartphone labels exist.
   - Caveat line: Adjacent road-quality categories are expected to be the
     hardest to distinguish; validation must report binary and multi-class
     performance separately.
3. Prioritization quadrant.
   - Axes: poor road-quality screen and poverty/service-access exposure.
   - Use: identify segments for field validation, maintenance screening, or
     project-preparation diagnostics.

## 6. Caveat / Non-Claim Box

This package does not claim to replace IRI, pavement-condition surveys, or
engineering inspection. It does not claim that AI can infer road quality
everywhere from imagery alone. It does not establish causal effects of road
quality on poverty. It is a screening and prioritization layer whose value
depends on validation data, transparent caveats, and integration with poverty,
service, and hazard geography.

## 7. Policy-Use Paragraph

ADB transport, rural development, social sector, and climate-resilience teams
can use this package to prioritize where road-condition validation or
maintenance screening would most improve access for poor or underserved
communities. Transport ministries and road agencies can use it to triage field
surveys, identify corridors where deterioration may undermine service access,
and connect maintenance planning with poverty and facility-catchment evidence.
The operational unit should be the road segment or catchment, not the country.

## 8. References and Source Notes to Add

- Thegeya, Aaron, Thomas Mitterling, Clifford Njoroge, Arturo Martinez Jr.,
  Yohan Iddawela, Joseph Albert Nino Bulan, Ron Lester Durante, Oshean Lee
  Garonita, and Jayzon Mag-atas. 2026. "Evaluating the effectiveness of
  satellite image super-resolution for road quality monitoring." Scientific
  Reports. https://www.nature.com/articles/s41598-026-47749-3
- Thegeya, Aaron, Thomas Mitterling, Arturo Martinez Jr., Joseph Bulan, Ron
  Lester Durante, and Jayzon Mag-atas. 2022. Application of Machine Learning
  Algorithms on Satellite Imagery for Road Quality Monitoring: An Alternative
  Approach to Road Quality Surveys. ADB Economics Working Paper Series No.
  675. https://www.adb.org/sites/default/files/publication/849926/ewp-675-machinelearning-satellite-image-road-quality.pdf
- Asian Development Bank. 2025. Guidebook on Machine Learning Techniques for
  Road Quality Monitoring. https://www.adb.org/publications/guidebook-machine-learning-techniques-road-quality
- Asian Development Bank. 2023. Key Indicators for Asia and the Pacific 2023.
  https://www.adb.org/sites/default/files/publication/900716/ki2023.pdf
- Repository source: `access-services/results.md` and
  `reporting-site/src/data/briefs.ts`.
- Google Open Buildings 2.5D Temporal. https://sites.research.google/gr/open-buildings/temporal/
- Groundsource flood-event dataset. https://doi.org/10.5281/zenodo.18647054
