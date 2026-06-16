# Research hook bank

`attestation_chain: ai-first`
Date: 2026-06-16

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

Goal: build 10-20 reader-facing reports, but only after each candidate has a
public-data evidence spine and a visual that reveals a specific measurement
problem. This is a report-quality queue, not a maturity promotion register.

| Batch | Report candidate | Evidence base | Showcase visual concept | Current report status | Next loop |
|---:|---|---|---|---|---|
| 1 | Market-level climate price transmission | `research/topic-sprints/nepal-market-climate-prices-sprint.md` and generated WFP/NASA POWER market-month JSON | Interactive market-month heatmap with price anomaly and lagged precipitation anomaly | Prototype surface at `/showcase`; desktop/mobile screenshot QA complete | L3 program package: commodity expansion, rainfall-source comparison, non-climate falsifiers |
| 1 | Public data freshness blind spots | `research/topic-sprints/wdi-data-freshness-sprint.md` and WDI freshness matrix | Interactive DMC-by-indicator freshness matrix with source-vintage explanation and focus control | Prototype surface at `/showcase/data-freshness`; desktop/mobile screenshot QA complete | L3 program package: indicator inclusion rules, source-specific refresh expectations, non-applicability checks |
| 1 | Shock-payment rails after disasters | `research/topic-sprints/shock-payment-rails-sprint.md` and joined disaster/payment-use table | Interactive disaster-frequency/payment-use scatter plus account-vs-use and program-vs-government-payment gap bars | Prototype surface at `/showcase/shock-payment-rails`; desktop/mobile screenshot QA complete | L3 program package: payment-channel metadata, ID/source-vintage falsifiers, event case check |
| 1 | Remittance corridors after flow weighting | `remittance-resilience/l2-flow-weighting-sprint.md` and generated flow-weighting artifacts | Corridor flow-weighting visual that shows how corridor weighting changes the cost story | Prototype surface at `/showcase/remittance-flow-weighting`; desktop/mobile screenshot QA complete | Formalize flow weighting as L3 evidence, rebuild review packet, then re-close remittance or continue next showcase batch |
| 1 | PSDQ source disagreement | `public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement.{csv,json}` plus PSDQ national summary | Interactive registry-vs-OSM disagreement workbench with Open Buildings exposure proxy | Prototype surface at `/showcase/psdq-source-disagreement`; desktop/mobile screenshot QA complete | L3 validation package: facility-level matching sample, registry-vintage notes, source-ground-truth falsifier |
| 2 | Air-monitoring observability | `air-monitoring/deepened-results.md`, `air-monitoring/generated/air-monitoring-concentration-deepening.json`, and `air-monitoring/generated/air-monitoring-adb-panel.json` | Zero-monitor population concentration stack plus GDP-adjusted monitor-density residual scatter and exposure/monitor-count panel | Prototype surface at `/showcase/air-monitoring-observability`; desktop/mobile screenshot QA complete | L3 catchment package: station-radius sensitivity, gridded population/PM2.5 denominators, OpenAQ-vs-regulatory inventory validation |
| 2 | Access map-completeness audit | `access-services/deepened-results.md`, `access-services/generated/access-osm-completeness-deepening.json`, and `access-services/generated/access-services-adb-panel.json` | Rank-flip chart showing OSM people-per-facility versus registry people-per-facility, plus correction wall for uncorrected cluster rows | Prototype surface at `/showcase/access-map-completeness`; desktop/mobile screenshot QA complete | L3 validation package: official registry joins for PAK/KHM/LAO/NPL/LKA/TLS, public travel-time/friction denominator, map-completeness falsifier |

The first seven prototypes intentionally start with the Nepal market-climate,
WDI data-freshness, shock-payment rails, PSDQ source-disagreement, and
remittance flow-weighting, air-monitoring observability, and access
map-completeness evidence because each has an immediate visual object and a
clear non-claim: local climate alignment is observable but not yet causal, WDI
freshness is a public-source observability screen rather than a score of
statistical agency performance, payment-use rails are visible only as
concept-separated public proxies rather than evidence that emergency transfers
arrived, registry-map disagreement is a source-QA screen rather than a
facility-access or service-quality result, flow-weighted remittance costs are a
corridor-weighting sensitivity rather than household transaction incidence,
air-monitor visibility is a public-source observability screen rather than a
pollution ranking or regulatory audit, and access map-completeness is a
source-audit result rather than travel-time access or service-quality evidence.

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

After the first seven prototype reports, the next strongest loop is either a
road-quality/access pilot as the next new visual object, or an L3 upgrade of
PSDQ, remittance, air-monitoring, or access-services where the existing prototype needs
validation rather than another surface. The shared originality lane is still
public-source joins at a more useful geography.
