---
attestation_chain: ai-first
package_status: methods_concept_package
topic_status: hypothesis_for_ntl_join_in_this_repo
program: mpi-nighttime-lights
created: 2026-04-29
---

# Small-Area Poverty Visibility

## 1. Problem Statement

Poverty programs are designed for places and households, but comparable
poverty indicators are often published at national or broad subnational
levels. This package frames a small-area poverty-visibility paper that would
combine multidimensional poverty, population grids, administrative boundaries,
and nighttime-light data to identify where deprivation remains poorly observed
at project-relevant geography. The output is a targeting and validation screen,
not an official poverty estimate and not a substitute for household surveys.

## Marginal Contribution

This is not yet an original empirical result in this repository. MPI,
small-area poverty, and nighttime-light poverty proxies are established
literatures. The contribution becomes original only if the repo commits a
transparent ADB-DMC source integration: subnational MPI, population grids,
administrative boundaries, and nighttime-light zonal statistics, with explicit
coverage and validation checks. The claim should be about where the measures
disagree and what that means for targeting, not about replacing poverty
statistics with satellite data.

## 2. Key Messages

- This is the strongest strategic poverty package, but it is not yet a
  computed repo result. The repository contains OPHI Global MPI 2024 parsing
  and ADB-member outputs; the nighttime-lights join is not committed here.
- The central research contribution is granularity: preserve MPI's
  multidimensional structure while moving analysis toward subnational MPI
  units, ADM1/ADM2, population grids, and nighttime-light pixels.
- Nighttime lights should be treated as an economic-activity and
  electrification proxy, not as a poverty measure. The paper should ask where
  the proxy and MPI disagree, not replace one with the other.
- Before drafting, update the source stack against the 2025 Global MPI release,
  which reports MPI data for 109 countries and subnational estimates covering
  1,359 regions across 101 countries.

## 3. Evidence Spine

- Current unit in repo: national MPI values and dimension decomposition for
  ADB members from OPHI Global MPI 2024.
- Target unit: subnational MPI region, ADM1/ADM2, 500 m or 1 km nighttime-
  light and population grid, Google Open Buildings 2.5D Temporal grid, 10 m
  AlphaEarth embedding-change layer, and harmonized ADB DMC boundary.
- Source stack: OPHI/UNDP Global MPI, NASA Black Marble VNP46A4 or EOG VIIRS
  DNB composites, Google Open Buildings 2.5D Temporal, AlphaEarth Satellite
  Embeddings, geoBoundaries, WorldPop or GHSL, World Bank SPID, Global Data
  Lab SHDI, and national poverty estimates where available.
- Repository evidence: `mpi-nighttime-lights/README.md`,
  `mpi-nighttime-lights/NEGATIVE-RESULT.md`, `data-access-audit.md`, and
  `luminosity-gap/public/data/mpi-national-adb.json`.
- Claim status: hypothesis for MPI x nighttime-lights decomposition in this
  repo. The package should stay a methods/data-integration concept until the
  NTL ingestion and zonal statistics are committed.

## 4. Proposed Section Outline

1. Why poverty targeting needs subnational and multidimensional evidence
2. What MPI measures and what nighttime lights can and cannot proxy
3. Data architecture for small-area poverty visibility
4. Coverage: which ADB DMCs have subnational MPI and usable boundary joins
5. Prototype charts: MPI deprivation profiles versus nighttime-light exposure
6. Validation plan against SPID, SHDI, national poverty statistics, or survey
   microdata
7. Policy use for targeting, survey design, and project preparation

## 5. Figure and Table Plan

1. MPI coverage and granularity matrix for ADB DMCs.
   - Chart type: heatmap table.
   - Source note: Author compilation using OPHI/UNDP Global MPI, repo MPI
     parser outputs, and boundary metadata. Unit = economy and subnational
     MPI region. Values are coverage indicators, not poverty estimates.
2. MPI deprivation profile versus nighttime-light intensity.
   - Chart type: scatter plot or small multiples by subnational unit.
   - Source note: Author calculations using OPHI/UNDP MPI, NASA Black Marble
     or VIIRS DNB, WorldPop/GHSL population, and geoBoundaries; access dates
     and raster processing version must be stated. Values are screening
     correlations and do not establish welfare, income, or causal change.
3. Bivariate map of deprivation and luminosity.
   - Chart type: two-color bivariate choropleth or gridded map.
   - Caveat line: Nighttime lights are affected by electrification, urban
     form, gas flares, sensor saturation, cloud filtering, and settlement
     density.

## 6. Caveat / Non-Claim Box

This package does not produce an official poverty estimate. It does not claim
that brighter places are less poor, that dark places are poorer, or that
satellite data can replace household surveys. It is a data-integration screen
for finding mismatch between observed economic light and multidimensional
deprivation. Co-authorship with Arturo Martinez Jr. on the legacy external
track must be preserved before any repository-side advancement.

## 7. Policy-Use Paragraph

ADB poverty, social protection, urban, education, and infrastructure teams can
use this package to identify places where national poverty averages hide
within-country deprivation patterns. National statistics offices can use the
same workflow to prioritize survey sample design, small-area estimation,
administrative-data validation, and local poverty diagnostics. The value is
highest when the unit moves below the country level: subnational MPI region,
ADM2, settlement grid, or project catchment.

## 8. References and Source Notes to Add

- UNDP. 2025. 2025 Global Multidimensional Poverty Index (MPI): Overlapping
  Hardships: Poverty and Climate Hazards. New York.
  https://hdr.undp.org/content/2025-global-multidimensional-poverty-index-mpi
- Alkire, Sabina, Usha Kanagaratnam, and Nicolai Suppa. 2024. The global
  Multidimensional Poverty Index (MPI) 2024: Poverty amid conflict. OPHI,
  University of Oxford. https://ophi.org.uk/global-mpi/2024
- NASA. n.d. Black Marble. https://blackmarble.gsfc.nasa.gov/
- Elvidge, Christopher D., et al. 2017. "VIIRS night-time lights."
  International Journal of Remote Sensing 38(21):5860-5879.
  https://doi.org/10.1080/01431161.2017.1342050
- Asian Development Bank. 2020. Mapping Poverty through Data Integration and
  Artificial Intelligence. https://www.adb.org/sites/default/files/publication/630406/mapping-poverty-ki2020-supplement.pdf
- Google Open Buildings 2.5D Temporal. https://sites.research.google/gr/open-buildings/temporal/
- AlphaEarth / Satellite Embedding V1. https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL
