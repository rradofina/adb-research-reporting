# Visual research roadmap

`attestation_chain: ai-first`

## Finding

The current site has a visual-distribution problem, not merely a styling
problem. The deterministic audit at `research/generated/figure-audit.json`
counts logical figures after collapsing PNG/SVG duplicates. At the 2026-07-18
snapshot, 13 programs have only a hero thumbnail, three have multiple figures,
and two have no generated visual. PSDQ, remittance, and access-services now
have multi-figure research stories.

The next work is therefore program-specific figure building from committed data
objects. The table names the highest-value visual sequence; it does not authorize
new claims or imply that every planned chart is currently supportable.

| Program | Current logical figures | Highest-value next visual sequence |
|---|---:|---|
| `public-service-data-quality` | 6 | Current-issue figure spine complete: hero, two ADM1 disagreement maps, non-causal poverty context, sensitivity range, and validation-wall infographic. Add another view only if a new public source changes the claim. |
| `remittance-resilience` | 4 | Current-issue figure spine complete: hero, dependence-cost scatter, quote-mean versus flow-weighted cost comparison, and top-five matched-flow coverage. Add another view only if a distinct corridor distribution or new source changes the claim. |
| `access-services` | 5 | Current-issue figure spine complete: hero, Philippine registry rank shifts, map-completeness scatter, eight-economy registry-readiness wall, and Cambodia source/vintage disagreement. Add another view only for a current crosswalk, travel-time, facility-capability, or utilization result. |
| `migration-displacement-signals` | 1 | Origin-destination network; absolute-to-population-normalized rank shifts; forced-displacement share scatter; destination concentration; denominator sensitivity. |
| `climate-health-workdays` | 1 | PM2.5 against observed exposed workers; published-to-observed denominator correction; heat-change small multiples; source coverage; cap sensitivity. |
| `disaster-recovery-lag` | 1 | Metric-rank stability matrix; event-frequency distribution; affected/deaths/damage comparison; recovery-source coverage; population-normalized falsification. |
| `grid-reliability-heat` | 1 | Generation concentration against outage proxies; capacity-to-generation concentration shifts; fuel-mix small multiples; proxy coverage matrix; low-generation-coverage sensitivity. |
| `port-hinterland-friction` | 1 | LPI against observed freight proxies; baseline-to-proxy rank shifts; source-vintage matrix; coverage by transport mode; sensitivity to trade-volume weighting. |
| `water-stress-crop-diversification` | 1 | Internal-to-available-water denominator shifts; stress against crop diversity; crop-concentration decomposition; rank sensitivity; source coverage. |
| `social-protection-shock-coverage` | 1 | Coverage against account ownership; three-leg gap decomposition; all-program to safety-net rank shifts; missing-leg matrix; source-vintage sensitivity. |
| `school-heat-disruption` | 1 | Heat against pupil-teacher ratio with child population support; rank sensitivity; KHM/PAK source-readiness matrix; observed-outcome absence; denominator robustness. |
| `food-price-climate-transmission` | 1 | Inflation against food-import share; original-to-food-specific rank shifts; top-set overlap matrix; source-vintage coverage; reformulation sensitivity. |
| `coastal-informal-risk` | 1 | Population-weighted to unweighted rank shifts; urban share against slum share; imputation influence; source coverage; spatial figure only after an eligible coastal object is retrieved. |
| `flood-market-access` | 1 | Composite decomposition; rural share against flood frequency; raw-to-per-capita rank shifts; source-readiness matrix; spatial extent only after the modeled layer is admitted. |
| `invisible-urbanization` | 1 | Urban share against growth; tautology sensitivity and rank inversions; boundary-vintage matrix; coverage by spatial unit; spatial mismatch only after the boundary join exists. |
| `air-monitoring` | 1 | Station-evidence coverage matrix; calibration/status absence matrix; concentration against monitor observability; source-vintage timeline; unresolved evidence by station. |
| `digital-performance` | 0 | Stop at hook triage: name a public data object and rough falsifiable visual before creating a program figure. |
| `mpi-nighttime-lights` | 0 | MPI dimension decomposition; night-light-blind share against MPI; indicator-observability matrix; source-readiness figure; spatial validation only after an eligible raster join. |

## Build order

1. Finish the active flagship's figure dossier without reopening its owner-only
   source-repair wall.
2. Convert existing deepening and falsification tables into figures before
   fetching new data.
3. Move program by program through the current queue; do not generate 18 sets of
   superficial country rankings in parallel.
4. Add each accepted figure inline to the canonical working paper, then expose
   it through the topic page's research narrative.
5. Re-run the figure audit, governance gates, production build, and desktop/mobile
   chart QA after each program package.
