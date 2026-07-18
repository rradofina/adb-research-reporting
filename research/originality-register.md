# Originality Register

`attestation_chain: ai-first`  
Date: 2026-04-29

Purpose: answer whether the repository is doing original research, and define
what can and cannot be claimed as original under `CONSTITUTION.md` §§2.3, 3.1,
3.3, and 8.3.

## Short Answer

Yes, but not every topic is original in the same way.

The repo's strongest lane is not inventing new econometric theory. It is
original measurement work: assembling public sources that are usually analyzed
separately, moving them to a more useful geography, making the data gap itself
the object of study, and publishing a reproducible evidence packet with clear
non-claims.

The right standard is:

> Does this add a source join, geography, validation, or falsifiable
> measurement design that the existing ADB/WB/UNDP/academic literature does
> not already provide for the same DMCs and units?

The wrong standard is:

> Has nobody ever used this dataset or method before?

That second claim is usually impossible to defend and should not be used.

## Originality Levels

| Level | Meaning | Acceptable claim language |
|---|---|---|
| O0 | Restatement only | Do not publish as research. Use as background or dashboard context. |
| O1 | New application or replication | "Applies an established method to ADB DMCs / a new source stack." |
| O2 | New data integration or geography | "Combines sources at a more policy-relevant unit than standard country tables." |
| O3 | New measurement design | "Introduces a falsifiable screening measure or observability-gap design with sensitivity checks." |
| O4 | New method or theory | Use only after specialist review; not the repo's default lane. |

## First Three ADB Packages

| Package | Current originality | Why | What would strengthen it |
|---|---:|---|---|
| Public-service data quality | O3 | The Asia-Pacific DMC facility registry-versus-public-map comparison is a narrow measurement-gap design with committed PHL + BGD data, sensitivity checks, and explicit non-claims. It is not the first health-facility-list paper globally; the original part is the DMC source stack, registry comparison, and reproducible local gradient. | ADM2 geography, facility-level matching, third-source triangulation, stratified manual validation, and human-final review. |
| Small-area poverty visibility | O2 potential; O1 current | MPI, small-area poverty, and nighttime lights are established literatures. The repo has parsed MPI data but has not committed the NTL join. The original contribution becomes credible only when subnational MPI, population grids, and nighttime-light zonal statistics are joined for ADB DMCs with clear non-claims. | Commit NTL ingestion, subnational MPI coverage matrix, admin crosswalk, zonal statistics, SPID/SHDI validation, and a literature scan focused on MPI x remote sensing. |
| Road quality and poverty access | O2 potential; O1 current | ADB already has road-quality ML work. The repo should not claim novelty on road-quality prediction itself. The original contribution would be linking road-quality screening to poverty, facilities, markets, hazards, and road-segment or catchment geography. | Select one DMC or corridor, add road-quality validation/proxy source, join poverty and service layers, and report screening accuracy or validation limits. |

## Current Program Read

| Program | Current originality read | Main risk |
|---|---|---|
| `public-service-data-quality` | Strongest original empirical package now. O3 under ai-first attestation. | Needs third source and ADM2/facility matching before human-final. |
| `mpi-nighttime-lights` | Potentially strong, but not yet original in this repo beyond MPI parsing. O1 current / O2 potential. | NTL join and subnational output not committed; coauthorship status must be reconciled. |
| `access-services` | Useful O1/O2 screen. | Facility counts are not travel-time access; OSM undercount is inherited. |
| `road-quality-poverty-access` | Good O2 next-track concept. | Road-quality ML method is already ADB's line; originality must come from poverty/access integration. |
| `digital-performance` | O2: exact-year ITU availability and use are joined across the ADB-DMC roster with provenance, missingness, affordability, urban-rural, and balanced-panel diagnostics. | The aggregate difference is not a person-level usage gap; independent household microdata and service-quality data are future layers. |
| `air-monitoring` | O1 current; O2 if gridded exposure and monitor catchments replace country means. | WDI PM2.5 is too coarse and partly modeled. |
| `invisible-urbanization` | O2: GHSL Degree of Urbanisation is joined to WDI national definitions, with administrative-scale and unit-transition diagnostics. | Construct differences are measured; legal misclassification and service neglect remain outside the claim. |
| `climate-health-workdays` | O1 current; O2 if heat and occupational exposure enter at district/grid scale. | Current result is PM2.5-only despite the workday-loss framing. |
| `coastal-informal-risk` | O1 current; O2 if LECZ and settlement footprints are used. | Binary coastal exposure and sparse slum data are too blunt. |
| `disaster-recovery-lag` | O1 current; O2/O3 if event footprints and recovery curves are computed. | Current result is disaster burden, not recovery lag. |
| `flood-market-access` | O1 current; O2/O3 if flood extent, road disruption, and market/service catchments are joined. | Country-level flood-event proxy is not market isolation. |
| `food-price-climate-transmission` | O1 current; O3 only with market-month price and local climate anomaly design. | Annual macro data cannot test transmission. |
| `grid-reliability-heat` | O1 current; O2 if plant/feeder/outage and heat exposure layers are joined. | Fuel concentration is structural exposure, not reliability. |
| `migration-displacement-signals` | O1 current; O2 if corridor histories and subnational origins are added. | Stock data are not flows. |
| `port-hinterland-friction` | O1 current; O2 if port/corridor/inland-node data replace national LPI. | LPI is national and perception-based. |
| `remittance-resilience` | O1/O2 current; O3 if flow-weighted corridors and household exposure are added. | RPW average costs are unweighted. |
| `school-heat-disruption` | O1 current; O2/O3 if school geocodes and heat-learning functions are joined. | Current heat ramp is too simple. |
| `social-protection-shock-coverage` | O1 current; O2 if beneficiary, payment, and shock geographies are linked. | Coverage is not adequacy or payment success. |
| `water-stress-crop-diversification` | O1 current; O2 if basin/crop-zone data replace country water ratios. | Country averages hide basin and transboundary mechanics. |

## Research-Quality Verdict

The work is credible if presented as a portfolio with maturity labels:

- PSDQ is the real original research lead now.
- Poverty visibility and road-quality access are strong concepts, not yet
  finished findings.
- The other topics are mostly screening results until their source upgrades
  move them below country level or add stronger validation.

Researchers are unlikely to be impressed by another page of country-level
ranked indicators. They are more likely to take the work seriously if each
paper shows:

1. a literature gap,
2. a falsifiable measurement design,
3. a lower-level geography,
4. a source stack with retrieval dates,
5. sensitivity or validation,
6. clear non-claims,
7. a reproducible evidence path.

## Required Claim Language

Use:

- "This paper contributes a reproducible measurement-gap screen..."
- "This package applies an established method to ADB DMCs at a more useful
  unit of analysis..."
- "This is a screening result, not an official statistic."
- "The original contribution is the source integration and geography, not a
  new ML method."

Avoid:

- Absolute novelty claims unless an exhaustive landscape scan supports them.
- AI-as-authority claims.
- "Country X is failing."
- Proof language for descriptive screening results.

Those claims are too broad for the current evidence and will make the work
look weaker, not stronger.

## Next Originality Work

1. For PSDQ, upgrade from ADM1 to ADM2, add a third facility source, and add
   Google Open Buildings as a settlement denominator.
2. For small-area poverty, commit NTL ingestion, subnational MPI coverage,
   Google Open Buildings 2.5D Temporal, and a validation plan for AlphaEarth
   embeddings.
3. For road quality, choose one DMC or corridor and build the road-segment
   poverty/access validation layer.
