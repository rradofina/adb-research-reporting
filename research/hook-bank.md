# Research hook bank

`attestation_chain: ai-first`
Date: 2026-06-19

Purpose: keep a ranked list of **data-first research hooks** before the repo
commits to another full publication ladder. This is not a claim register and
not a maturity register. It is a triage board for public data objects that may
produce a non-generic research question after a rough visual is built.

## Operating rule

Run hook triage before writing a paper frame:

1. Fetch or reuse the public data object.
2. Build the rough visual first.
3. Ask what the visual makes visible that the conventional source misses.
4. Reverse-design the research question, method, caveat, and publication plan.
5. Ditch or defer if the strongest output is only a country ranking, composite
   leaderboard, generic trend, or topic summary.

AI can scout catalogs, compare source joins, propose visuals, draft falsifiers,
and critique candidate hooks. AI cannot supply empirical values, invent missing
data, or turn a screening visual into a finding.

## New-topic rule

Separate **new-topic creation** from **existing-program repair**.

- A new-topic hook must introduce a new evidence question or source object,
  not only patch an existing article.
- Existing-program repair hooks may stay in this file, but they do not count
  as new topics unless the sprint creates a genuinely new research question.
- A new-topic sprint earns promotion only when a script produces a table or
  visual that changes the question. A plausible title is not enough.

## New-topic shortlist

These are fresh program candidates or substantial new research questions. The
ranking is a triage judgment, not empirical evidence.

| Rank | New-topic hook | Public dataset | First visualization | Non-generic research question | Source caveat | AI role | Kill/defer condition | Status |
|---:|---|---|---|---|---|---|---|---|
| 1 | Public data freshness blind spots | World Bank WDI API across core indicators | DMC-by-indicator heatmap of latest public reference year and relative lag | Where does a public dashboard become stale before any policy comparison begins? | Indicator update cycles differ; lag must be measured against each indicator's own latest reference year | Fetch API data, compute freshness matrix, flag missing/stale cells, draft caveat language | Ditch if the visual only says "some countries have less data" without indicator-specific update structure | L2 sprint complete; promote to program prospectus candidate |
| 2 | Shock-payment rails after disasters | World Bank ASPIRE, Global Findex/DataBank payment-use indicators, EM-DAT country profiles via HDX | Two-panel chart separating disaster-event frequency, digital-payment use, social-protection coverage, and account-minus-digital-use gaps | Where do public sources show disaster exposure, but also show that account ownership is a weak proxy for post-shock payment rails? | Electronic payment use is not shock-payment receipt; ASPIRE pools many social-protection types; Findex/GFDD vintages differ; EM-DAT affected totals are event records | Join payment-use indicators to existing disaster/social-protection panels, test vintage collision, build non-composite visual, draft non-claim language | Defer if payment-use coverage falls below a credible DMC-facing first visual or if it collapses into a readiness index | L2 sprint complete; promote to program prospectus candidate |
| 3 | Market-level climate price transmission | WFP Nepal food-price and market CSVs from HDX plus NASA POWER monthly point climate data | Aligned market-month heatmap: rice price anomaly above local seasonality versus one-month-lag precipitation anomaly | Which market price spikes line up with local climate anomalies, and which look more like broader market or macro pressure that national CPI would hide? | WFP market coverage is uneven; one commodity is not a food basket; NASA POWER is modeled point climate; no causal controls yet | Locate one DMC with public market prices, define anomaly windows, build local climate join, draft falsifiers | Ditch if only annual national CPI/import data are available or the market-month join is too sparse | L2 sprint complete; promote to program prospectus candidate |
| 4 | Public procurement concentration and delivery risk | Open Contracting data, ADB procurement notices where public, World Bank procurement datasets | Buyer-supplier network or award concentration timeline | Which sectors depend on a narrow supplier pool, and is that visible before project delays appear? | Procurement schemas and award-stage definitions differ across portals | Scout APIs, normalize identifiers, design concentration visual with caveats | Defer if award data cannot be joined to sector/project outcomes | Candidate |
| 5 | Development-project geocoding coverage gap | AidData geocoded projects, IATI, ADB project documents where public | Map of project records with and without usable location precision | Which project portfolios are geographically invisible to local planning users? | Geocoding precision and disclosure rules vary by donor | Compare geocode precision fields, draft location-uncertainty legend | Ditch if location precision is not recorded or license blocks redistribution | Candidate |
| 6 | Tourism shock exposure beyond arrivals | WDI tourism receipts, EM-DAT events, aviation/port arrivals where public | Timeline overlay of tourism receipts and disaster/event shocks for island DMCs | When tourism is a fiscal exposure channel, which shocks are visible in public macro data? | National annual data cannot identify causality or local exposure | Test event windows, source tourism dependence, design small multiples | Defer if the visual is only a tourism-dependence ranking | Candidate |
| 7 | Digital public-service friction | UN e-government/open data indices, WDI internet use, Findex digital payments, public service portals | Source-disagreement scatter: formal e-service score versus measured access/payment use | Where does digital-government supply exceed household ability to use digital services? | Cross-source concepts differ; index scores may be perception or expert-coded | Separate service supply from user access, build caveat-first visual | Ditch if it becomes another digital-readiness index | Candidate |
| 8 | Health worker pipeline visibility | WHO NHWA, WDI health workforce series, migration stock data where public | Training/workforce/migration triangle by occupation where available | Where is health workforce pressure hidden because training, stock, and migration sources do not align? | Occupation definitions and reporting years differ | Scout NHWA availability, map occupation codes, design missingness table | Defer if public data are only national aggregate doctors/nurses | Candidate |
| 9 | Debt-service pressure versus service-spending freshness | World Bank IDS, WDI health/education spending, IMF WEO where public | Debt-service versus service-spending scatter with latest-year labels | Where do fiscal-risk screens rely on fresh debt data but stale social-spending data? | Debt and spending series have different accounting concepts and update cycles | Pull macro series, compute freshness, prevent causal overclaiming | Ditch if the result is only a debt-stress country ranking | Candidate |
| 10 | Heat early-warning observability | WMO climate services status, CCKP/ERA5 heat metrics, population grids | Matrix of heat exposure versus public warning-system visibility | Which high-heat populations lack public evidence of early-warning coverage? | Warning-system data may be narrative or country-level only | Scout WMO/UNDRR sources, build exposure-observability crosswalk | Defer if warning data are not public or not comparable | Candidate |

## New-topic L2 sprint queue

1. **Public data freshness blind spots** - completed 2026-06-16 in
   `research/topic-sprints/`. Decision: promote to program prospectus
   candidate.
2. **Shock-payment rails after disasters** - completed 2026-06-16 in
   `research/topic-sprints/`. Decision: promote to program prospectus
   candidate because the visual separates shock exposure, digital-payment use,
   social-protection coverage, and account-versus-use gaps.
3. **Market-level climate price transmission** - completed 2026-06-16 in
   `research/topic-sprints/`. Decision: promote to program prospectus
   candidate because the Nepal WFP/NASA POWER heatmap creates a market-month
   source-alignment question rather than a national CPI trend.

Top-three new-topic sprint batch status: complete. Next action is to choose
one promoted prospectus for L3 program packaging or start a new L1 shortlist
batch.

## ADB/ERDI showcase queue

Goal: maintain a 20-report reader-facing bench, but only where each candidate
has a public-data evidence spine and a visual that reveals a specific
measurement problem. This is a report-quality queue, not a maturity promotion
register.

| Batch | Report candidate | Evidence base | Showcase visual concept | Current report status | Next loop |
|---:|---|---|---|---|---|
| 1 | Market-level climate price transmission | `research/topic-sprints/nepal-market-climate-prices-sprint.md` and generated WFP/NASA POWER market-month JSON | Interactive market-month heatmap with price anomaly and lagged precipitation anomaly | Prototype surface at `/showcase`; desktop/mobile screenshot QA complete | L3 program package: commodity expansion, rainfall-source comparison, non-climate falsifiers |
| 1 | Public data freshness blind spots | `research/topic-sprints/wdi-data-freshness-sprint.md` and WDI freshness matrix | Interactive DMC-by-indicator freshness matrix with source-vintage explanation and focus control | Prototype surface at `/showcase/data-freshness`; desktop/mobile screenshot QA complete | L3 program package: indicator inclusion rules, source-specific refresh expectations, non-applicability checks |
| 1 | Shock-payment rails after disasters | `research/topic-sprints/shock-payment-rails-sprint.md` and joined disaster/payment-use table | Interactive disaster-frequency/payment-use scatter plus account-vs-use and program-vs-government-payment gap bars | Prototype surface at `/showcase/shock-payment-rails`; desktop/mobile screenshot QA complete | L3 program package: payment-channel metadata, ID/source-vintage falsifiers, event case check |
| 1 | Remittance corridors after flow weighting | `remittance-resilience/l2-flow-weighting-sprint.md` and generated flow-weighting artifacts | Corridor flow-weighting visual that shows how corridor weighting changes the cost story | Prototype surface at `/showcase/remittance-flow-weighting`; desktop/mobile screenshot QA complete | Formalize flow weighting as L3 evidence, rebuild review packet, then re-close remittance or continue next showcase batch |
| 1 | PSDQ source disagreement | `public-service-data-quality/source-disagreement-l3-module.md`, `public-service-data-quality/facility-validation-sample.md`, `public-service-data-quality/facility-validation-coded-screen.md`, `public-service-data-quality/facility-validation-ai-review.md`, `public-service-data-quality/facility-validation-candidate-resolution.md`, `public-service-data-quality/facility-validation-candidate-public-source-check.md`, `public-service-data-quality/facility-validation-coordinate-repair.md`, `public-service-data-quality/facility-validation-public-map-gap.md`, `public-service-data-quality/facility-validation-public-map-gap-evidence.md`, `public-service-data-quality/facility-validation-public-map-inspection.md`, `public-service-data-quality/facility-validation-public-source-confirmation.md`, `public-service-data-quality/facility-validation-public-source-confirmation-targeted-rows.md`, `public-service-data-quality/facility-validation-public-source-decision-ledger.md`, `public-service-data-quality/facility-validation-possible-same-facility-review.md`, `public-service-data-quality/facility-validation-priority-name-conflict-review.md`, `public-service-data-quality/facility-validation-lower-priority-name-conflict-review.md`, `public-service-data-quality/facility-validation-zero-osm-upazila-observability-review.md`, `public-service-data-quality/facility-validation-evidence-ladder.md`, `public-service-data-quality/facility-validation-human-gated-handoff.md`, `public-service-data-quality/facility-validation-human-validation-worksheet.md`, `public-service-data-quality/facility-validation-ai-closure-audit.md`, `public-service-data-quality/facility-validation-source-repair-public-evidence.md`, `public-service-data-quality/facility-validation-source-repair-official-coordinate-evidence.md`, `public-service-data-quality/facility-validation-source-repair-public-explanation-evidence.md`, `public-service-data-quality/facility-validation-source-repair-correction-record-followup.md`, `public-service-data-quality/facility-validation-source-repair-clarification-packet.md`, `public-service-data-quality/facility-validation-source-repair-registry-vintage-review.md`, generated L3 strata/sample/coded-screen/AI-review/candidate-resolution/public-source-check/coordinate-repair/public-map-gap/row-evidence/inspection/confirmation/decision-ledger/possible-same-facility/priority-name-conflict/lower-priority-name-conflict/zero-OSM-observability/evidence-ladder/human-gated-handoff/human-validation-worksheet/AI-closure-audit/source-repair-evidence/official-coordinate/public-explanation/correction-record/clarification-packet/registry-vintage artifacts, and PSDQ national summary | Interactive registry-vs-OSM disagreement workbench plus ratio-strata validation ledger, validation-sample panel, grouped coded-screen chart, AI public-source review workstream chart, candidate-resolution lane chart, public-source tag-support lane chart, coordinate-repair distance ledger, public-map-gap upazila queue, row-evidence reviewer queue, targeted public-map inspection cards, first-row public-source confirmation scores, 40-row upazila confirmation lanes, 16-row public-source decision-ledger tracks, 3-row possible same-facility evidence gates, 9-row priority name-conflict queue cards, 6-row lower-priority repeated-candidate spot-check cards, 115-upazila zero-OSM observability bars, 10-stage evidence ladder, 39-row human-gated handoff wall, 39-row blank worksheet downloads, 39-row AI closure-audit wall, 4-row source-repair evidence cards, 4-row official-coordinate gap cards, 4-row public-explanation cards, 3-row correction-record follow-up cards, 3-row clarification-question cards, and 3-row registry-vintage gate cards | L3 evidence module at `/showcase/psdq-source-disagreement`; validation sample, automated coded screen, AI row-review ledger, 8-row candidate-resolution pass, richer public-source tag scan, 23-row coordinate-repair triage, 40-row public-map-gap triage, 40-row row-evidence ledger, 40-row targeted public-map inspection packet, 12-row first-source pass, 40-row public-source confirmation pass, 16-row public-source decision ledger, 3-row possible same-facility review, 9-row priority name-conflict review, 6-row lower-priority name-conflict spot check, 115-upazila zero-OSM observability review, 10-stage evidence ladder, 39-row human-gated handoff matrix, 39-row blank human-validation worksheet, 39-row AI closure audit, 4-row source-repair public-evidence attachment, 4-row official-coordinate evidence, 4-row public-explanation search, 3-row correction-record follow-up, 3-row no-contact clarification packet, and 3-row registry-vintage review generated; same-facility, priority-name-conflict, lower-priority name-conflict, zero-OSM, evidence-ladder, handoff, worksheet, and closure-audit desktop/mobile screenshot QA complete; no rows closed or reclassified | Owner-only source-owner contact or human location validation remains the substantive source-repair, same-facility, priority/lower-priority name-conflict, and facility-level zero-OSM wall |
| 2 | Air-monitoring observability | `air-monitoring/deepened-results.md`, `air-monitoring/metadata-readiness-audit.md`, `air-monitoring/station-metadata-source-access.md`, `air-monitoring/generated/air-monitoring-concentration-deepening.json`, `air-monitoring/generated/air-monitoring-adb-panel.json`, `air-monitoring/generated/air-monitoring-metadata-readiness-audit-summary.json`, and `air-monitoring/generated/air-monitoring-openaq-station-metadata-summary.json` | Zero-monitor population concentration stack plus GDP-adjusted monitor-density residual scatter, exposure/monitor-count panel, station-metadata readiness wall, and OpenAQ station-coordinate map | Prototype surface at `/showcase/air-monitoring-observability`; station-metadata source pass generated 101 OpenAQ PM2.5 station rows and 101 coordinate rows for 11 of 24 upgrade-queue economies, excluded 2 coordinate-QC rows, with 13 economies still at OpenAQ-visible zero and 0 monitor-grade/regulatory-inventory/station-radius rows; station map desktop/mobile screenshot QA complete | L3 source-validation package: collect regulator inventories, validate monitor grade where public, and add gridded population/PM2.5 denominators before station-radius claims |
| 2 | Access map-completeness audit | `access-services/deepened-results.md`, `access-services/generated/access-osm-completeness-deepening.json`, and `access-services/generated/access-services-adb-panel.json` | Rank-flip chart showing OSM people-per-facility versus registry people-per-facility, plus correction wall for uncorrected cluster rows | Prototype surface at `/showcase/access-map-completeness`; desktop/mobile screenshot QA complete | L3 validation package: official registry joins for PAK/KHM/LAO/NPL/LKA/TLS, public travel-time/friction denominator, map-completeness falsifier |
| 2 | Disaster metric falsification | `disaster-recovery-lag/deepened-results.md` and `disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.{json,csv}` | Metric-switch report showing where the original CHN+IND top-two holds and where deaths, events/year, and per-capita burden break it | Prototype surface at `/showcase/disaster-metric-falsification`; desktop/mobile screenshot QA complete with mobile-native ranked bars | L3 recovery-lag package: event-timestamped recovery curves, exposure denominator, and source-reporting falsifiers before any recovery-speed claim |
| 3 | Power-fuel concentration audit | `grid-reliability-heat/generated/grid-generation-deepening.{json,csv}` | Capacity-versus-generation rank bridge with generation-coverage gate | Evidence-audit surface at `/showcase/grid-generation-mismatch`; desktop/mobile CDP screenshot QA complete | L3 reliability package: outage/reserve-margin or heat-stress evidence before reliability language |
| 3 | Emigration denominator switch | `migration-displacement-signals/generated/migration-per-population-deepening.{json,csv}` | Absolute emigrant-stock rank versus population-share rank bridge | Evidence-audit surface at `/showcase/migration-denominator-switch`; desktop/mobile CDP screenshot QA complete | L3 migration package: corridor composition, remittance/refugee split, and denominator source caveats |
| 3 | MPI night-light blind spot | `mpi-nighttime-lights/generated/mpi-dimension-decomposition.{json,csv}` | NTL-blind versus plausibly visible MPI dimension stack | Evidence-audit surface at `/showcase/mpi-nightlight-blindspot`; desktop/mobile CDP screenshot QA complete | Owner-led L3 path only: VIIRS/GEE join, admin crosswalk, and coauthor attestation |
| 3 | Coastal population-denominator audit | `coastal-informal-risk/generated/coastal-drop-population-deepening.{json,csv}` | Headline rank versus no-population rank bridge | Evidence-audit surface at `/showcase/coastal-population-denominator`; desktop/mobile CDP screenshot QA complete | L3 coastal package: GHSL/DEM/surge footprint before exposure language |
| 3 | Flood component decomposition | `flood-market-access/generated/flood-decompose-deepening.{json,csv}` | Committed flood proxy versus per-capita/event-count decomposition bridge | Evidence-audit surface at `/showcase/flood-component-decomposition`; desktop/mobile CDP screenshot QA complete | L3 access package: roads, market/service points, flood footprint, and travel-time falsifier |
| 3 | Climate-health measurement repair | `climate-health-workdays/generated/climate-health-workdays-deepening.json` | PM2.5-cap sensitivity lanes against outdoor-labor-share rank | Evidence-audit surface at `/showcase/climate-health-measurement-repair`; desktop/mobile CDP screenshot QA complete | L3 health package: labor-force denominator, heat exposure, and causal non-claim repair |
| 3 | Food-price coverage trap | `food-price-climate-transmission/generated/food-price-coverage-deepening.{json,csv}` | CPI/import indicator coverage funnel plus common-vintage top sets | Evidence-audit surface at `/showcase/food-price-coverage-trap`; desktop/mobile CDP screenshot QA complete | L3 food-price package: household/market price exposure and missing-data sensitivity before vulnerability language |
| 3 | Social-protection dropped leg | `social-protection-shock-coverage/generated/social-protection-dropped-leg.{json,csv}` | Value-rank ledger with missing-leg flags | Evidence-audit surface at `/showcase/social-protection-dropped-leg`; desktop/mobile CDP screenshot QA complete | L3 shock-coverage package: payment-channel metadata and beneficiary-reach validation |
| 3 | Water denominator artifact | `water-stress-crop-diversification/generated/water-stress-denominator-deepening.{json,csv}` | Saturated internal-water denominator cards plus rural counterfactual | Evidence-audit surface at `/showcase/water-stress-denominator`; desktop/mobile CDP screenshot QA complete | L3 water/crop package: total-renewable-water and crop-area denominators before crop-diversity language |
| 3 | Invisible urbanization tautology | `invisible-urbanization/generated/invisible-urbanization-tautology.{json,csv}` | Rank-preserving multiplier lanes plus input-perturbation boundary card | Evidence-audit surface at `/showcase/invisible-urban-tautology`; desktop/mobile CDP screenshot QA complete | L3 urban package: satellite/built-up layer and classification-history evidence |
| 3 | Port inert-parameter audit | `port-hinterland-friction/generated/port-hinterland-inert-parameter.json` | Import-cap binding wall and top-five invariance lanes | Evidence-audit surface at `/showcase/port-inert-parameter`; desktop/mobile CDP screenshot QA complete | L3 port package: actual hinterland friction, travel time, or logistics-performance source |
| 3 | School heat top-one audit | `school-heat-disruption/generated/school-heat-sensitivity-audit.json` | Sensitivity-run ledger separating discriminating, degenerate, and rank-losing runs | Evidence-audit surface at `/showcase/school-heat-sensitivity`; desktop/mobile CDP screenshot QA complete | L3 school package: school geocodes, school calendars, enrollment denominators, and indoor/heat-exposure caveats |

The 20-report bench intentionally mixes bespoke L2 surfaces and artifact-driven
audit pages. The first eight reports are prototype surfaces around market
climate alignment, data freshness, payment rails, PSDQ source disagreement,
remittance flow weighting, air-monitoring observability, access map
completeness, and disaster metric falsification. Reports 9-20 are evidence
audits that make a measurement problem visible before a program claim is
widened. The common non-claim is explicit: these surfaces do not promote a
maturity label, do not replace the underlying scripts, and do not turn
screening proxies into performance rankings.

## L1 ranking snapshot

Scoring is subjective hook triage, not empirical evidence. Columns: visual
distinctiveness (V), public-data feasibility (F), DMC relevance (D), and
non-generic question strength (Q), each 1-5.

| Rank | Candidate hook | V | F | D | Q | Total | L2 status |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | Remittance corridors after flow weighting | 5 | 5 | 5 | 5 | 20 | Sprint complete; promote to L3 repair pass |
| 2 | PSDQ district/catchment validation | 5 | 4 | 5 | 5 | 19 | Next sprint candidate |
| 3 | Road quality as access constraint | 5 | 4 | 5 | 5 | 19 | Next sprint candidate |
| 4 | Air-monitor catchment gap | 5 | 5 | 5 | 4 | 19 | Prototype report complete; catchment L3 still next |
| 5 | Market-price climate transmission | 5 | 4 | 5 | 5 | 19 | Strong backup sprint |
| 6 | Flood isolation of markets/services | 5 | 3 | 5 | 5 | 18 | Needs one-DMC data narrowing |
| 7 | Coastal informal settlement exposure | 5 | 3 | 5 | 5 | 18 | Needs one-coast pilot |
| 8 | Urban reclassification lag | 4 | 4 | 5 | 5 | 18 | Needs admin-boundary history |
| 9 | School heat with actual schools | 5 | 3 | 5 | 4 | 17 | Needs school geocodes |
| 10 | Digital performance gap | 4 | 4 | 5 | 4 | 17 | Needs large data pull decision |
| 11 | Migration corridor concentration | 4 | 4 | 5 | 4 | 17 | Needs non-stock outcome hook |
| 12 | Social-protection payment rails | 4 | 3 | 5 | 4 | 16 | Needs payment-channel source |
| 13 | Grid heat/water reliability exposure | 4 | 3 | 5 | 4 | 16 | Needs plant stress join |
| 14 | Water stress and crop mix | 4 | 3 | 5 | 4 | 16 | Needs basin-level move |
| 15 | Small-area poverty visibility | 5 | 3 | 5 | 5 | 18 | Owner-led path; do not advance silently |

## Top three L2 sprints

1. **Remittance corridors after flow weighting** — completed on 2026-06-16.
   The rough visual and generated JSON are in
   `remittance-resilience/generated/`; decision is to promote the hook into a
   full L3 repair pass, not to publish it as a claim.
2. **PSDQ district/catchment validation** — next best sprint because the repo
   already has a strong program spine and the first visual can be a
   source-disagreement map below the national level.
3. **Road quality as access constraint** — high-value but narrower: pick one
   DMC corridor or province first so it does not collapse into a road-density
   leaderboard.

## Expanded hook cards

| Rank | Candidate hook | Public data object | First visual | Non-generic question | AI assist | Kill/defer condition |
|---:|---|---|---|---|---|---|
| 1 | Remittance corridors after flow weighting | RPW Q1 2025 quote data + World Bank/KNOMAD bilateral remittance matrix + WDI remittance-dependence series | Dependence-vs-cost scatter comparing equal-weighted and flow-weighted corridor costs, with matched-flow bubble size | Does the high-cost remittance group survive once observed corridors are weighted by estimated bilateral flow rather than counted equally? | Search source vintage and metadata, build parser checks, compare mean/median/flow-weighted costs, flag coverage caveats | Completed L2 sprint; move to L3 only after parser repair and coverage panel |
| 2 | PSDQ district/catchment validation | Official facility registries + OSM health features + building or settlement denominators + optional DHS/MICS/service-use outcome | District/catchment disagreement map: official registry, public map, settlement denominator, high-gap service areas | Are public map gaps concentrated where service planning needs the most complete facility visibility? | Plan source joins, matching rules, validation strata, and figure sequence; critique whether the gap predicts an independent outcome | Defer if the third source only repeats the registry/map disagreement and no independent denominator or outcome is available |
| 3 | Road quality as access constraint | OSM road surface/smoothness tags, public road inventories where available, service/market points, settlement grids | Road-link map showing poor-quality or unknown-quality segments that separate settlements from services or markets | Which specific links, not which countries, create the access bottleneck for high-poverty settlements? | Identify one tractable pilot area, design road-quality validation, build network-distance comparison, prevent novelty overclaiming | Ditch if it becomes a national road-density ranking or if road quality cannot be validated beyond sparse OSM tags |
| 4 | Air-monitor catchment gap | OpenAQ station metadata + gridded PM2.5 + WorldPop or GHS population grid | Catchment map of high-population/high-PM2.5 areas outside a monitor radius | Which polluted population centers are least observed by ground monitors, not just most polluted? | Test station metadata, catchment radii, population denominators, and HDI/income confounding | Ditch if the result only reproduces income or population size without an independent observability story |
| 5 | Market-price climate transmission | WFP or national market-month prices + CHIRPS/ERA5 local rainfall/heat anomalies + crop/import context | Market small multiples: local price anomaly against rainfall or heat anomaly by commodity | Are price spikes spatially and temporally aligned with local climate anomalies, or was the macro screen mostly import/CPI noise? | Locate public market-price source by DMC, define anomalies, draft falsification tests, guard against causal language | Defer if only annual national CPI/import data are available |
| 6 | Flood isolation of markets/services | Flood extent or modeled hazard + road network + markets/facilities + settlement grid | Baseline and flooded-network catchment map for one pilot geography | Which settlements lose practical market or service access when specific flood-prone links fail? | Plan network analysis, source hazard layers, and pick a one-DMC pilot with public data | Defer if only national EM-DAT event counts are available |
| 7 | Coastal informal settlement exposure | GHSL/WorldPop or settlement grids + elevation/storm-surge layer + public slum/informal settlement proxies | Coastal strip map of exposed settlement density with proxy-quality flags | Which coastal settlement clusters are both exposed and least visible in official/informal-settlement data? | Search open elevation/surge layers, design proxy flags, separate exposure from settlement legality | Ditch if the only result is total coastal population by country |
| 8 | Urban reclassification lag | GHSL built-up/settlement layers + official urban/rural classifications or admin-boundary histories | Map of built-up growth outside units still classified as rural or non-urban | Where does the physical city expand faster than the statistical classification used for planning? | Find boundary/history sources, test classification vintages, build small multiples by period | Defer if no public classification history exists for the pilot geography |
| 9 | School heat with actual schools | Public school geocodes + ERA5/CCKP heat metrics + enrollment or pupil-teacher ratios where public | School-point heat-days map with crowding/coverage flags | Which school clusters face repeated high-heat days, and where does this intersect with crowding or sparse public data? | Find school-location sources, design heat thresholds, draft uncertainty notes for modeled climate data | Ditch if the only available unit is national school-age population |
| 10 | Digital performance gap | Ookla Open Data tiles + admin or urban polygons + official coverage claims where public | Tile-to-admin distribution map and fixed/mobile speed comparison | Where does measured user performance diverge from nominal connectivity coverage? | Plan DuckDB aggregation, licensing caveats, tile-to-admin joins, and privacy-preserving bins | Defer if the pull or redistribution constraints prevent a reproducible evidence packet |
| 11 | Migration corridor concentration | UN DESA bilateral migrant stock + remittance corridors + displacement/refugee indicators where public | Corridor chord/map separating labor, family, and displacement-heavy corridors where source allows | Which migration corridors should not be read as labor-migration or remittance-market signals? | Build corridor typology, test stock vs share denominators, draft non-claim language | Ditch if it remains only a migrant-stock leaderboard |
| 12 | Social-protection payment rails | ASPIRE coverage + Findex account/mobile money variables + ID4D or payment-channel indicators where public | Readiness matrix separating coverage from payment access and identity rails | Where does program coverage exist on paper but payment rails limit shock delivery? | Search payment-channel sources, test vintage issues, separate account ownership from active use | Defer if no public payment-channel or identity proxy can be joined |
| 13 | Grid heat/water reliability exposure | WRI power plant database + generation/capacity sources + ERA5 heat or water-stress layers | Plant-level map of exposed assets by fuel and role in the grid | Which assets create heat/water reliability exposure that a national fuel-mix table hides? | Search generation/reliability proxies, separate capacity from generation, design plant-level encoding | Defer if no heat, water, generation, or reliability variable can be joined |
| 14 | Water stress and crop mix | AQUASTAT/FAOSTAT where public + HydroBASINS + crop maps or national crop areas | Basin/crop exposure panel rather than national water-withdrawal table | Which crop systems face water-stress exposure after transboundary-water denominator problems are made visible? | Search basin and crop sources, design denominator checks, avoid overreading national withdrawal ratios | Defer if the result remains a national withdrawal ranking |
| 15 | Small-area poverty visibility | Subnational MPI/poverty + VIIRS/Black Marble or comparable nightlights + population/building grids | Poverty-component map against nighttime-light intensity | Where do health and education poverty components remain invisible to nightlight proxies? | Plan crosswalks, zonal statistics, and component caveats; keep owner/coauthor path explicit | Owner-led path; defer if coauthor/attestation or Earth Engine/NTL access is not cleared |

## Selection rule

Pick the next hook by expected **visual distinctiveness per unit of data work**:

1. Can the first visual be built from public data in one session?
2. Does it show a unit below the national average, a corridor, a network, a
   catchment, or a source disagreement?
3. Does it create a question that would survive as a paper title without
   sounding like a dashboard category?
4. Does it have a clear falsifier or kill condition?
5. Can it produce a reader-facing artifact with receipts, not just a map?

After the 20-report bench, the next strongest loop is critique and L3
strengthening, not adding another surface by default. The best candidates are
PSDQ, remittance, air-monitoring, access-services, disaster recovery-lag, or one
of the artifact audits whose visual exposes a fixable measurement flaw. A new
road-quality/access pilot remains a strong new visual object, but it should
start only if the owner chooses a new-topic loop over strengthening the current
bench.
