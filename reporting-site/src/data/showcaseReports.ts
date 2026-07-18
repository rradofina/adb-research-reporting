export type ShowcaseReportStatus = "verified" | "active";

export type ShowcaseAuditKind =
  | "rank-shift"
  | "stacked-blindness"
  | "coverage-funnel"
  | "sensitivity-lanes"
  | "parameter-audit"
  | "tautology-audit"
  | "component-audit";

export interface ShowcaseAudit {
  kind: ShowcaseAuditKind;
  programSlug: string;
  dataUrl: string;
  csvUrl?: string;
  question: string;
  finding: string;
  method: string;
  readerPayoff: string;
  nonClaim: string;
  downloadLabel: string;
}

export interface ShowcaseReport {
  id: number;
  title: string;
  shortTitle: string;
  href: string;
  status: ShowcaseReportStatus;
  statusLabel: string;
  deck: string;
  evidencePath: string;
  visual: string;
  sourceNote: string;
  audit?: ShowcaseAudit;
}

export interface ShowcaseReportDepth {
  operationalUse: string;
  falsifier: string;
  limitation: string;
}

export type ShowcaseReadiness =
  | "prototype"
  | "l3-candidate"
  | "evidence-audit"
  | "portfolio-proof"
  | "owner-gated";

export interface ShowcaseReportQuality {
  readiness: ShowcaseReadiness;
  readinessLabel: string;
  qaSummary: string;
  publicationGap: string;
  nextUpgrade: string;
}

export const showcaseReports: ShowcaseReport[] = [
  {
    id: 1,
    title: "When Food Prices Spike, Is the Weather Local?",
    shortTitle: "Market-level climate price transmission",
    href: "/showcase",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "Nepal market-month rice prices joined to point climate data, now with a generated ledger that counts broad price-wave months against dry local-rainfall alignment.",
    evidencePath: "research/topic-sprints/nepal-market-climate-prices-sprint.md",
    visual: "Animated market-month heatmaps, price-wave signal strip, broad-wave ledger, and commodity source audit",
    sourceNote: "WFP food-price rows, commodity inventory, and NASA POWER point climate API",
  },
  {
    id: 2,
    title: "When Public Data Arrive Late",
    shortTitle: "Public data freshness blind spots",
    href: "/showcase/data-freshness",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "A 42-economy by 9-indicator WDI vintage matrix now separates latest, watch, protocol-review, stale-alert, and missing public cells before any dashboard comparison.",
    evidencePath: "research/topic-sprints/wdi-data-freshness-sprint.md",
    visual: "Interactive economy-indicator freshness matrix with source-context protocol status",
    sourceNote: "World Bank WDI API retrieval and source-vintage fields",
  },
  {
    id: 3,
    title: "When Account Ownership Is Not a Payment Rail",
    shortTitle: "Shock-payment rails after disasters",
    href: "/showcase/shock-payment-rails",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "Disaster exposure is compared with observable account, payment-use, social-protection, and 2024 Findex candidate-source rails before any readiness claim.",
    evidencePath: "research/topic-sprints/shock-payment-rails-sprint.md",
    visual: "Disaster-frequency scatter, payment-rail gap bars, and evidence-leg observability ledger",
    sourceNote: "EM-DAT, Global Findex API/2025 country CSV inventory, ASPIRE, and WDI public indicators",
  },
  {
    id: 4,
    title: "When the Registry and the Map Disagree",
    shortTitle: "Public service data quality source disagreement",
    href: "/showcase/psdq-source-disagreement",
    status: "verified",
    statusLabel: "L3 evidence module",
    deck: "Bangladesh joins 572 DGHS upazila rows with 28,166 active clinical facilities to 3,212 OSM health features; the facility-validation chain ends with 39 human/source-owner wall rows and 0 AI-actionable closures.",
    evidencePath: "public-service-data-quality/source-disagreement-l3-module.md",
    visual: "Generated evidence-gate matrix plus a 28-row source-disagreement evidence ledger",
    sourceNote: "DOH NHFR, DGHS registry, OSM, Open Buildings, and PSA context",
  },
  {
    id: 5,
    title: "When Corridor Averages Hide Flow Exposure",
    shortTitle: "Remittance corridors after flow weighting",
    href: "/showcase/remittance-flow-weighting",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "RPW remittance prices are rechecked with public bilateral-flow weights so corridor-cost exposure is not counted equally by default.",
    evidencePath: "remittance-resilience/flow-weighting-l3-module.md",
    visual: "Equal-weighted versus flow-weighted corridor-cost scatter",
    sourceNote: "World Bank RPW, KNOMAD bilateral flows, and WDI remittance dependence",
  },
  {
    id: 6,
    title: "When Public Monitor QA Evidence Is Not Verifiable",
    shortTitle: "Air-monitoring observability",
    href: "/showcase/air-monitoring-observability",
    status: "verified",
    statusLabel: "L3 candidate evidence package",
    deck: "A generated evidence ledger collapses 64 public-source summary rows and 214 supporting files into a documented absence finding: the audit sees station lists, method context, dashboards, and denominator geometry, but 0 validated same-station rows, 0 station-specific BMKG calibration certificates or inspection logs, 0 complete monitor-grade rows, 0 station-radius-ready economies, and 0 allowed coverage-claim rows.",
    evidencePath: "air-monitoring/results.md",
    visual: "Finding-first QA gate matrix, grouped evidence ledger, source-route protocol, economy strip, and reproducibility links",
    sourceNote: "OpenAQ v3, official regulator and station portals, BMKG public station/API/PPID/PTSP routes, Georgia report/export/API routes, Uzbekistan station-detail and endpoint routes, GHSL/ACAG denominator custody, and generated air-monitoring evidence ledger",
  },
  {
    id: 7,
    title: "When Access Maps Measure Mapping Completeness",
    shortTitle: "Access map-completeness audit",
    href: "/showcase/access-map-completeness",
    status: "verified",
    statusLabel: "PP evidence package",
    deck: "Official registries reorder 16 of 17 Philippine regional ranks and 6 of 8 Bangladesh division ranks built from OSM points. The Cambodia source audit exposes a separate vintage and provider-scope disagreement.",
    evidencePath: "access-services/deepened-results.md",
    visual: "Rank-flip chart, completeness scatter, correction wall, and Cambodia source-scope ledger",
    sourceNote: "OSM, official clinical registries, WorldPop, sibling PSDQ artifacts, and HDX Cambodia Health Facilities",
  },
  {
    id: 8,
    title: "When the Disaster Top-Two Breaks",
    shortTitle: "Disaster metric falsification",
    href: "/showcase/disaster-metric-falsification",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "A pre-registered disaster-burden pair is tested against alternate EM-DAT metrics, then checked against a public GDIS x Black Marble source-readiness queue before any recovery-lag narrative is reused.",
    evidencePath: "disaster-recovery-lag/deepened-results.md",
    visual: "Metric-switch bars, recovery source gates, and GDIS x Black Marble overlap bars",
    sourceNote: "EM-DAT country profiles, WDI population denominators, GDIS geocoded disaster locations, and NASA Black Marble VNP46A3 CMR metadata",
  },
  {
    id: 9,
    title: "When Single-Fuel Grids Meet Patchy Outage Evidence",
    shortTitle: "Grid reliability proxy source wall",
    href: "/showcase/grid-generation-mismatch",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "WRI generation fuel concentration is joined to World Bank firm-outage, Doing Business, and B-READY utility-service indicators to show what public reliability evidence can and cannot support.",
    evidencePath: "grid-reliability-heat/generated/grid-generation-reliability-source-audit.json",
    visual: "Capacity-generation bridge plus public reliability-proxy source wall",
    sourceNote: "WRI Global Power Plant Database, 2017 generation fields, World Bank firm-outage indicators, Doing Business electricity indicators, and B-READY utility-service scores",
    audit: {
      kind: "rank-shift",
      programSlug: "grid-reliability-heat",
      dataUrl: "/programs/grid-reliability-heat/generated/grid-generation-reliability-source-audit.json",
      csvUrl: "/programs/grid-reliability-heat/generated/grid-public-reliability-proxy-readiness-country.csv",
      question: "Can a single-fuel generation screen be crosswalked to public outage and electricity-service proxies without becoming a grid-reliability claim?",
      finding: "Public proxies exist for 38 DMCs and overlap 22 generation-ranked rows, but the page stops at source readiness because proxy years and methods differ.",
      method: "Recompute fuel concentration on generation, query 15 World Bank reliability-proxy indicators, take each DMC's latest non-null public value, and show which rows have both layers.",
      readerPayoff: "The report becomes a source wall: it shows where direct reliability research could start and where public proxies are still too indirect.",
      nonClaim: "This is not a power-reliability ranking and does not observe outage events, reserve margins, seasonal dispatch, or heat-stress curtailment.",
      downloadLabel: "Download source-audit JSON",
    },
  },
  {
    id: 10,
    title: "When Population Changes the Migration Leaders",
    shortTitle: "Emigration denominator switch",
    href: "/showcase/migration-denominator-switch",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The absolute and population-share top fives have zero overlap. A UNHCR crosswalk then shows why Afghanistan's near-rank exception is not comparable with the population-share leaders.",
    evidencePath: "migration-displacement-signals/generated/migration-denominator-corridor-type-audit.json",
    visual: "Absolute-vs-share rank bridge plus UNHCR forced-displacement exception cards",
    sourceNote: "UN DESA International Migrant Stock 2024, WDI 2024 population denominators, and UNHCR Refugee Data Finder 2024 origin-asylum population rows",
    audit: {
      kind: "rank-shift",
      programSlug: "migration-displacement-signals",
      dataUrl: "/programs/migration-displacement-signals/generated/migration-denominator-corridor-type-audit.json",
      csvUrl: "/programs/migration-displacement-signals/generated/migration-corridor-type-forced-displacement-country.csv",
      question: "What changes when emigrant stock is read by population share, and which rows are really forced-displacement stock?",
      finding: "Zero of five economies appear in both leading sets. The population-share top five is not forced-displacement-majority, but Afghanistan is: UNHCR forced-displacement stock equals 81.7% of its UN DESA emigrant stock.",
      method: "Join UN DESA emigrant stock to WDI population, then query UNHCR 2024 origin-asylum rows and compare refugees, asylum-seekers, and other international-protection stock to each origin's emigrant stock.",
      readerPayoff: "The denominator switch becomes sharper: small-island diaspora exposure and Afghanistan displacement exposure are both large, but they are different policy objects.",
      nonClaim: "This does not classify labor, family, student, or temporary-work migration, and it is not a welfare or fragility ranking.",
      downloadLabel: "Download corridor-type audit JSON",
    },
  },
  {
    id: 11,
    title: "When Night Lights Cannot See the Poverty Dimension",
    shortTitle: "MPI night-light blind spot",
    href: "/showcase/mpi-nightlight-blindspot",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "MPI deprivation shares are decomposed before any VIIRS join, then NASA CMR metadata is checked so the source wall is explicit.",
    evidencePath: "mpi-nighttime-lights/generated/mpi-nightlight-blindspot-source-audit.json",
    visual: "Blind-versus-visible MPI dimension bars plus Black Marble source-readiness cards",
    sourceNote: "OPHI Global MPI 2024 national table and NASA CMR Black Marble VNP46A3/VNP46A4 metadata",
    audit: {
      kind: "stacked-blindness",
      programSlug: "mpi-nighttime-lights",
      dataUrl: "/programs/mpi-nighttime-lights/generated/mpi-nightlight-blindspot-source-audit.json",
      csvUrl: "/programs/mpi-nighttime-lights/generated/mpi-nightlight-source-readiness-collections.csv",
      question: "Before joining night lights, how much of MPI is structurally outside radiance, and is the NTL source path public?",
      finding: "Most ADB economies have majority NTL-blind MPI weight; CMR confirms Black Marble metadata and sample links, but no analysis-ready raster join exists here.",
      method: "Decompose each economy's MPI dimensions, then query NASA CMR for VNP46A3 and VNP46A4 collection and sample-granule metadata.",
      readerPayoff: "The chart turns a flashy satellite idea into a humility test for the poverty construct.",
      nonClaim: "This does not download radiance rasters, compute zonal statistics, estimate a night-lights poverty model, or replace the owner-led co-authored MPI track.",
      downloadLabel: "Download MPI + NTL source audit JSON",
    },
  },
  {
    id: 12,
    title: "When Population Size Drives the Coastal Slum Screen",
    shortTitle: "Coastal denominator audit",
    href: "/showcase/coastal-population-denominator",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "An informal coastal-risk proxy drops log population, then checks whether public settlement, elevation, and coastal-hazard sources are ready for the true spatial exposure object.",
    evidencePath: "coastal-informal-risk/generated/coastal-denominator-spatial-source-audit.json",
    visual: "Headline rank bridge plus GHSL/NASADEM/Aqueduct source-readiness wall",
    sourceNote: "WDI coastal panel, GHSL/JRC download page, NASA CMR NASADEM_HGT metadata, and WRI Aqueduct Floods v2 index",
    audit: {
      kind: "rank-shift",
      programSlug: "coastal-informal-risk",
      dataUrl: "/programs/coastal-informal-risk/generated/coastal-denominator-spatial-source-audit.json",
      csvUrl: "/programs/coastal-informal-risk/generated/coastal-spatial-source-readiness-sources.csv",
      question: "Who remains high once the coastal-informal proxy stops rewarding country population size?",
      finding: "Tuvalu enters the no-population top five, Bangladesh drops out, and the source wall still records zero analysis-ready spatial overlays.",
      method: "Recompute the committed index, remove the log-population term, then query public GHSL, NASADEM, and Aqueduct coastal-hazard metadata before any exposure claim.",
      readerPayoff: "The page separates the useful small-island warning from the unfinished settlement-in-surge-zone measurement task.",
      nonClaim: "This is not a storm-surge exposure result and does not map informal settlements, low-elevation cells, or exposed population inside inundation zones.",
      downloadLabel: "Download coastal source-audit JSON",
    },
  },
  {
    id: 13,
    title: "When a Flood Access Index Measures Event Counts",
    shortTitle: "Flood access decomposition",
    href: "/showcase/flood-component-decomposition",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The flood-market-access proxy is decomposed, then checked against the road, market, population, and observed-flood source layers needed before any routed access claim.",
    evidencePath: "flood-market-access/generated/flood-decomposition-access-source-audit.json",
    visual: "Per-capita rank bridge plus four-layer access source wall",
    sourceNote: "Committed EM-DAT/WDI flood panel plus Geofabrik, HDX/WFP, WorldPop, Global Flood Database, and NASA flood-product metadata",
    audit: {
      kind: "rank-shift",
      programSlug: "flood-market-access",
      dataUrl: "/programs/flood-market-access/generated/flood-decomposition-access-source-audit.json",
      csvUrl: "/programs/flood-market-access/generated/flood-access-source-readiness-sources.csv",
      question: "Can a flood-access proxy claim market access before roads, markets, population, and observed flood footprints are joined?",
      finding: "The per-capita version replaces the committed top four, while every routed-access join flag remains false.",
      method: "Reproduce the index, compute the per-capita rerank, then query public Geofabrik, HDX/WFP, WorldPop, Global Flood Database, NASA NRT, and CMR metadata before any access-loss claim.",
      readerPayoff: "The page lets the route object stay visibly missing instead of hiding behind a confident country list.",
      nonClaim: "This contains no road graph, market geocoding, population raster weighting, flood-footprint raster, routed travel time, or access-loss estimate.",
      downloadLabel: "Download flood access source-audit JSON",
    },
  },
  {
    id: 14,
    title: "When a Stable Proxy Measures the Wrong Construct",
    shortTitle: "Climate-health construct test",
    href: "/showcase/climate-health-measurement-repair",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "Aligned annual WDI and Lancet Countdown data show that the inherited PM2.5 × employment proxy does not recover the direct heat-related potential work-hours-loss ordering.",
    evidencePath: "climate-health-workdays/generated/climate-health-construct-validation.json",
    visual: "Rank disagreement, 21-test sensitivity matrix, direct heat profile, and outcome-source wall",
    sourceNote: "World Bank WDI and Lancet Countdown 2025 indicator 1.1.3 potential-hours and outdoor-worker workbooks",
    audit: {
      kind: "sensitivity-lanes",
      programSlug: "climate-health-workdays",
      dataUrl: "/programs/climate-health-workdays/generated/climate-health-construct-validation.json",
      csvUrl: "/programs/climate-health-workdays/generated/climate-health-proxy-heat-comparison.csv",
      question: "Does an internally stable PM2.5 × employment proxy recover the direct heat-work-loss construct?",
      finding: "Across 21 aligned tests, top-three overlap never exceeds one economy; 16 tests have zero overlap and five have one.",
      method: "Align annual WDI proxy inputs with Lancet heat-loss rates for 34 economies in 2018–2020, compare ranks, and vary every arbitrary proxy choice by ±50%.",
      readerPayoff: "The page distinguishes internal stability from external construct validity and replaces a country list with a measurement decision.",
      nonClaim: "Potential work hours lost are modelled capacity losses, not observed absence, output, or a policy-performance rank; PM2.5 remains a separate pathway.",
      downloadLabel: "Download construct-validation JSON",
    },
  },
  {
    id: 15,
    title: "When Vulnerability Is a Coverage Intersection",
    shortTitle: "Food price coverage trap",
    href: "/showcase/food-price-coverage-trap",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The CPI and agricultural-imports screen is repaired with a true food-import leg, exposing that the old stable pair was a source-label artifact.",
    evidencePath: "food-price-climate-transmission/generated/food-price-coverage-food-import-audit.json",
    visual: "Coverage funnel plus raw-ag versus food-import source wall",
    sourceNote: "World Bank WDI CPI, agricultural raw-materials imports, WDI food imports, and HDX/WFP market-price metadata",
    audit: {
      kind: "coverage-funnel",
      programSlug: "food-price-climate-transmission",
      dataUrl: "/programs/food-price-climate-transmission/generated/food-price-coverage-food-import-audit.json",
      csvUrl: "/programs/food-price-climate-transmission/generated/food-price-food-import-rerank.csv",
      question: "Was the food-price screen identifying food-import exposure, or a raw-materials source mismatch?",
      finding: "Replacing raw-ag imports with true WDI food imports expands the CPI x import universe from 34 to 36 rows, but the LAO+PAK stable set becomes empty.",
      method: "Reproduce the old CPI x raw-ag intersection, fetch WDI food imports and CPI metadata, rerank the joint sets, and inspect HDX/WFP market-price source readiness.",
      readerPayoff: "The visual turns a tempting top list into a source wall: the repair improves the macro label but still stops before local market-price exposure.",
      nonClaim: "This is not a food-security ranking, a household welfare measure, or a climate-to-food-price transmission estimate.",
      downloadLabel: "Download food-price source audit JSON",
    },
  },
  {
    id: 16,
    title: "When Missing a Data Leg Removes the Runner-Up",
    shortTitle: "Social-protection dropped leg",
    href: "/showcase/social-protection-dropped-leg",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "Shock-payment readiness is re-ranked before excluding one-legged observations, then stress-tested against the source object behind the coverage leg.",
    evidencePath: "social-protection-shock-coverage/generated/social-protection-dropped-leg-source-audit.json",
    visual: "Value-rank ledger plus ASPIRE/Findex/poverty source wall",
    sourceNote: "WDI ASPIRE all-SP coverage, ASPIRE social safety-net coverage, Findex account ownership, and WDI poverty metadata",
    audit: {
      kind: "rank-shift",
      programSlug: "social-protection-shock-coverage",
      dataUrl: "/programs/social-protection-shock-coverage/generated/social-protection-dropped-leg-source-audit.json",
      csvUrl: "/programs/social-protection-shock-coverage/generated/social-protection-social-safety-net-rerank.csv",
      question: "Is the shock-payment screen observing delivery capacity, or only a convenient WDI source stack?",
      finding: "Two one-legged rows still outrank the headline tail, and a narrower ASPIRE safety-net leg leaves zero overlap with the named headline five.",
      method: "Reproduce the dropped-leg ledger, fetch WDI metadata for all-SP, safety-net, Findex, and poverty legs, rerun a safety-net variant, and record the missing delivery object.",
      readerPayoff: "The page turns a readiness ranking into a source audit: the current data stack can screen observability gaps but cannot certify emergency payment delivery.",
      nonClaim: "This does not certify shock-payment readiness, beneficiary reach, delivery speed, payment-rail use, or adaptive social-protection capacity.",
      downloadLabel: "Download social-protection source audit JSON",
    },
  },
  {
    id: 17,
    title: "When Water Stress Exceeds 100 Percent",
    shortTitle: "Water denominator artifact",
    href: "/showcase/water-stress-denominator",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The water-crop pressure screen tests the internal-water denominator, then joins WDI/AQUASTAT available-water stress and FAOSTAT harvested-area crop mix before any crop-water claim is widened.",
    evidencePath: "water-stress-crop-diversification/generated/water-stress-denominator-source-audit.json",
    visual: "Internal-vs-available denominator bridge plus FAOSTAT crop-mix wall",
    sourceNote: "WDI internal withdrawal, WDI/AQUASTAT available-water stress, WDI rural population, and FAOSTAT Area harvested crop rows",
    audit: {
      kind: "component-audit",
      programSlug: "water-stress-crop-diversification",
      dataUrl: "/programs/water-stress-crop-diversification/generated/water-stress-denominator-source-audit.json",
      csvUrl: "/programs/water-stress-crop-diversification/generated/water-stress-source-variant-rerank.csv",
      question: "Does the water-crop screen survive when internal-water stress is replaced by available-water stress and cereal yield is replaced by crop-mix evidence?",
      finding: "The available-water-stress top five are TKM, UZB, PAK, LKA, and TJK; FAOSTAT crop-HHI concentration points to TUV, KIR, FSM, NRU, and VUT; the source-upgraded national variant keeps only three of the old raw top-four rows.",
      method: "Reproduce the denominator audit, fetch WDI/AQUASTAT water-stress metadata, parse FAOSTAT 2024 Area harvested rows, build a crop-mix HHI ledger, and keep basin-level crop-water exposure out of scope.",
      readerPayoff: "An internal-denominator result becomes a source-repair workbench: the page shows which part is denominator, which part is crop mix, and which basin/crop overlay is still missing.",
      nonClaim: "This is not a basin allocation, irrigation-demand, crop-water-use, GRACE depletion, or subnational exposure analysis.",
      downloadLabel: "Download water source audit JSON",
    },
  },
  {
    id: 18,
    title: "When Robustness Is Just Multiplication",
    shortTitle: "Invisible urbanization tautology",
    href: "/showcase/invisible-urban-tautology",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The claimed sensitivity sweep is tested as a scalar multiplier, then public GHSL, SMOD, WDI, and boundary metadata are checked before any built-up claim is widened.",
    evidencePath: "invisible-urbanization/generated/invisible-urbanization-source-audit.json",
    visual: "Rank-preserving multiplier sweep plus GHSL/SMOD boundary source wall",
    sourceNote: "WDI urban-definition metadata, GHSL built-up and SMOD metadata pages, and geoBoundaries ADM2 metadata",
    audit: {
      kind: "tautology-audit",
      programSlug: "invisible-urbanization",
      dataUrl: "/programs/invisible-urbanization/generated/invisible-urbanization-source-audit.json",
      csvUrl: "/programs/invisible-urbanization/generated/invisible-urbanization-source-readiness-sources.csv",
      question: "Does the sensitivity sweep test robustness, and is the public built-up/boundary source object ready for a real replacement?",
      finding: "The 5/10/15 sweep preserves ranks exactly; GHSL and boundary metadata are visible; the built-up/boundary overlay, classification-history ledger, and zonal statistic remain unbuilt.",
      method: "Reproduce the committed proxy, test the scalar sweep, check WDI urban-definition metadata, inspect GHSL built-up and SMOD metadata pages, and query geoBoundaries ADM2 metadata for the top-five economies.",
      readerPayoff: "The page separates an empty robustness test from the public source stack needed to replace the WDI-only proxy.",
      nonClaim: "This does not download GHSL rasters, intersect administrative boundaries, build a classification-history ledger, or detect invisible urbanization on the ground.",
      downloadLabel: "Download urban source audit JSON",
    },
  },
  {
    id: 19,
    title: "When a Sensitivity Knob Never Touches the Model",
    shortTitle: "Port hinterland inert parameter",
    href: "/showcase/port-inert-parameter",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The import-cap parameter is audited, then public WDI logistics, port-throughput, and freight-proxy sources are checked before any hinterland friction claim is widened.",
    evidencePath: "port-hinterland-friction/generated/port-hinterland-source-audit.json",
    visual: "Cap binding lanes plus public port/freight source wall",
    sourceNote: "WDI LPI components, imports, container port traffic, and road/rail/air freight metadata",
    audit: {
      kind: "parameter-audit",
      programSlug: "port-hinterland-friction",
      dataUrl: "/programs/port-hinterland-friction/generated/port-hinterland-source-audit.json",
      csvUrl: "/programs/port-hinterland-friction/generated/port-hinterland-source-readiness-sources.csv",
      question: "Can a perturbed import cap prove robustness, and are direct port/hinterland sources ready to replace the proxy?",
      finding: "At the baseline cap, zero DMCs bind; public WDI logistics and freight layers are visible, but direct port-performance and hinterland travel-time joins remain false.",
      method: "Compare observed import proxy values with the cap, rerun the cap lanes, then query WDI LPI, imports, container port traffic, and road/rail/air freight indicators for coverage.",
      readerPayoff: "The page shows both problems at once: a knob detached from the data and a missing travel-time evidence object.",
      nonClaim: "This is not a port-performance ranking and does not measure actual port dwell time, corridor impedance, or hinterland travel time.",
      downloadLabel: "Download port source audit JSON",
    },
  },
  {
    id: 20,
    title: "When School Heat Is Not Yet a School-Day Object",
    shortTitle: "School heat source wall",
    href: "/showcase/school-heat-sensitivity",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The Cambodia top-one sensitivity audit now sits beside public WDI, CCKP, OSM school-count, and UNICEF disruption-source checks while the school-calendar, school-day heat, school-location, and outcome joins stay false.",
    evidencePath: "school-heat-disruption/generated/school-heat-source-audit.json",
    visual: "Sensitivity run ledger plus public school-heat source-readiness wall",
    sourceNote: "Committed school-heat sensitivity runs, WDI education and population indicators, CCKP tasmax, OSM Overpass school counts, and UNICEF climate-related school-disruption source pointer",
    audit: {
      kind: "sensitivity-lanes",
      programSlug: "school-heat-disruption",
      dataUrl: "/programs/school-heat-disruption/generated/school-heat-source-audit.json",
      csvUrl: "/programs/school-heat-disruption/generated/school-heat-source-readiness-sources.csv",
      question: "Can the Cambodia top-one screen become a school-disruption claim before calendars, school locations, daily heat, and outcomes are joined?",
      finding: "Cambodia is top one in 5 of 6 discriminating runs and WDI/CCKP/OSM source rows are visible, but every analysis-ready school-day and outcome join remains false.",
      method: "Reread every sensitivity run, then query public WDI metadata and values, CCKP tasmax rows for Cambodia and Pakistan, OSM Overpass school counts, and a UNICEF disruption source pointer.",
      readerPayoff: "The page turns a catchy top-one result into a clear evidence wall: what is visible, what is still missing, and why the school-day object has not been measured.",
      nonClaim: "This is not a classroom heat-exposure, school-calendar, school-location, closure, attendance, learning, or causal disruption measurement.",
      downloadLabel: "Download school-heat source audit JSON",
    },
  },
];

export const verifiedShowcaseReports = showcaseReports.filter(
  (report) => report.status === "verified",
);

export const showcaseAuditReports = showcaseReports.filter(
  (report): report is ShowcaseReport & { audit: ShowcaseAudit } => Boolean(report.audit),
);

export const showcaseReportDepth: Record<number, ShowcaseReportDepth> = {
  1: {
    operationalUse: "Screen market-months where broad price waves need non-climate controls before local-weather interpretation.",
    falsifier: "If commodity expansion, import, exchange-rate, fuel, and market-access checks explain the broad-wave months, the local-weather hook narrows to the dry-aligned subset.",
    limitation: "The lead chart still uses one rice series, uneven WFP market coverage, and modeled NASA POWER point climate; it cannot establish causality.",
  },
  2: {
    operationalUse: "Help statisticians and operations teams see which dashboard indicators are too stale for current comparison.",
    falsifier: "If lag patterns disappear after indicator-specific update schedules are applied, the freshness concern is overstated.",
    limitation: "Freshness is not statistical-agency performance; indicators have different revision calendars and reporting duties.",
  },
  3: {
    operationalUse: "Separate account ownership from active digital-payment and social-protection rails before shock-transfer planning.",
    falsifier: "If verified shock-payment channel data show high delivery through the same populations, the proxy gap narrows.",
    limitation: "Findex and ASPIRE are public proxies with vintage mismatch; they do not observe emergency transfers arriving.",
  },
  4: {
    operationalUse: "Target registry, map, and building-footprint validation where service-access analysis depends on facility visibility.",
    falsifier: "If facility-level audits show registry and OSM differences are mostly duplicate naming or harmless classification, the gap weakens.",
    limitation: "Source disagreement is not a service-quality or travel-time result and does not prove facilities are absent.",
  },
  5: {
    operationalUse: "Help remittance teams decide when equal-weighted corridor prices hide exposure in high-flow corridors.",
    falsifier: "If corridor flow weights are too sparse, stale, or inconsistent with observed transactions, the flow-weighted comparison cannot lead.",
    limitation: "Bilateral flows are estimates and do not observe household remittance transactions or informal channels.",
  },
  6: {
    operationalUse: "Use the ledger to decide whether a public monitor source is context only or claim-enabling QA evidence.",
    falsifier: "A public station-level calibration certificate, inspection log, current calibration-status row, official/OpenAQ crosswalk, or method-grade ledger would narrow or overturn the absence finding.",
    limitation: "The packet documents absence in audited public routes only. It does not prove records do not exist elsewhere and does not estimate monitor coverage, PM2.5 exposure, population served, monitor performance, or regulatory performance.",
  },
  7: {
    operationalUse: "Flag geographies where OSM health amenities are too incomplete to support access or catchment planning.",
    falsifier: "If official registry joins do not change local facility-load ranks, the map-completeness concern is weaker.",
    limitation: "OSM completeness is not actual service availability, capacity, quality, or travel-time access; the Cambodia HDX layer is a 2010 public-facility inventory, not a complete current all-provider registry.",
  },
  8: {
    operationalUse: "Prevent recovery-lag narratives from reusing a disaster burden pair that fails under alternate metrics, while showing the event-geography queue needed for a real recovery pilot.",
    falsifier: "If an event-level EM-DAT/date join plus Black Marble extraction restores the same priority pair, the metric-falsification warning narrows.",
    limitation: "EM-DAT burden screens and the GDIS overlap queue do not measure recovery speed, reconstruction, household loss, or service restoration.",
  },
  9: {
    operationalUse: "Help energy teams see which single-fuel generation screens have public outage or electricity-service proxy context before requesting operations data.",
    falsifier: "If direct outage, reserve-margin, seasonal dispatch, or heat-stress curtailment records contradict the proxy crosswalk, the proxy layer remains source triage only.",
    limitation: "World Bank firm-outage, Doing Business, and B-READY indicators are mixed-vintage proxies, not direct operating reliability records.",
  },
  10: {
    operationalUse: "Help migration analysts separate small-economy diaspora exposure from origins where the same stock metric is dominated by forced displacement.",
    falsifier: "If visa, deployment, or corridor-purpose data show the share-top-five rows are not mainly diaspora stock, the interpretation needs another split.",
    limitation: "UNHCR observes forced displacement only; the page still cannot identify labor, family, student, or temporary-work migration from public stock data.",
  },
  11: {
    operationalUse: "Keep night-light poverty work from overclaiming before the blind MPI dimensions and the Black Marble source wall are both visible.",
    falsifier: "If an owner-led VIIRS join predicts health and education deprivation independently after raster access, population weighting, and flare masking, the blind-spot warning can be narrowed.",
    limitation: "The page computes MPI-side decomposition and public CMR metadata only; it does not run a night-light model.",
  },
  12: {
    operationalUse: "Distinguish small-economy coastal informal-settlement questions from country-size-driven proxy rankings before any hazard-exposure language is used.",
    falsifier: "If a GHSL/NASADEM/Aqueduct overlay does not confirm no-population entrants, the proxy should remain a denominator caution rather than an exposure screen.",
    limitation: "The screen verifies public metadata only; it does not locate informal settlements inside coastal hazard zones or estimate exposed population.",
  },
  13: {
    operationalUse: "Stop flood-market-access language until a road-market-flood route object exists; use the source wall to scope a one-DMC pilot.",
    falsifier: "If a routed road-market-flood pilot preserves the same priority set after population weighting, the access framing gains support.",
    limitation: "The current artifact confirms source visibility only; it contains no road graph, geocoded market join, raster overlay, route, or access-loss estimate.",
  },
  14: {
    operationalUse: "Help health and labor teams distinguish a stable screen from a valid heat-labor construct before using ranks for planning.",
    falsifier: "If an observed exposure-outcome panel shows the proxy predicts labor outcomes as well as the heat construct under a frozen design, the rejection must be reconsidered.",
    limitation: "The direct heat measure remains modelled potential capacity loss, and this package joins no observed absence, hours, output, or labor-supply outcome.",
  },
  15: {
    operationalUse: "Show food-price analysts whether the vulnerability screen is driven by countries with both public indicators.",
    falsifier: "If household or market price data keep the same high-risk group after missing-data repair, the coverage warning narrows.",
    limitation: "The joint CPI/imports screen is not a food-security or household-exposure ranking.",
  },
  16: {
    operationalUse: "Make missing social-protection or payment legs visible before excluding economies from shock-readiness screens.",
    falsifier: "If payment-channel and beneficiary data validate the headline five after one-leg repair, the missingness concern weakens.",
    limitation: "The public legs do not certify emergency payment delivery, identity readiness, or beneficiary reach.",
  },
  17: {
    operationalUse: "Help water and agriculture teams separate internal-denominator artifacts from national available-water stress and observed crop-mix concentration before scoping a basin pilot.",
    falsifier: "If a basin-level crop-water overlay preserves the same priority set after water allocation, crop water requirements, irrigation command areas, and subnational rural exposure are joined, the warning narrows.",
    limitation: "The upgraded artifact is still national: it adds WDI/AQUASTAT available-water stress and FAOSTAT crop mix, but not basin allocation, irrigation demand, GRACE depletion, or crop-water exposure.",
  },
  18: {
    operationalUse: "Help urban teams distinguish a WDI-only low-urban-base screen from the GHSL, SMOD, boundary, and classification-history objects needed for a real built-up test.",
    falsifier: "If a GHSL built-up or SMOD x boundary overlay plus classification-history ledger confirms the same top set, the topic can be rebuilt as a spatial measurement package.",
    limitation: "The upgraded artifact is still source readiness: it checks public metadata but does not download rasters, intersect boundaries, or compute built-up population outside urban classifications.",
  },
  19: {
    operationalUse: "Show transport teams when the cap sensitivity is inert and which public logistics, throughput, and freight proxy layers are visible before corridor evidence is claimed.",
    falsifier: "If port-level dwell, turnaround, berth-productivity, or port-to-inland OD travel-time data confirm the same top set, the report can graduate.",
    limitation: "The upgraded artifact is still source readiness: WDI throughput and freight proxies are visible, but no port-performance table, OD network, or hinterland travel-time statistic is joined.",
  },
  20: {
    operationalUse: "Help education and climate teams separate a national heat-pressure proxy from the school-day evidence object needed for planning closures, calendars, or cooling investments.",
    falsifier: "If school calendars, daily school-day heat, school geocodes, enrollment denominators, or observed closure and learning records change the Cambodia/Pakistan comparison, the national proxy should be replaced.",
    limitation: "The upgraded artifact is source readiness: it checks WDI, CCKP, OSM, and UNICEF source visibility but does not build a school calendar, school-day heat series, school-location overlay, enrollment-weighted exposure, or outcome join.",
  },
};

export const showcaseReportQuality: Record<number, ShowcaseReportQuality> = {
  1: {
    readiness: "prototype",
    readinessLabel: "L2 prototype",
    qaSummary: "Public sprint artifact now includes interactive heatmaps, a generated broad-wave falsifier ledger, commodity inventory, caveats, screenshots, and build/gates.",
    publicationGap: "Needs full commodity expansion, alternative rainfall source, and external price controls before a program claim.",
    nextUpgrade: "Convert the Nepal sprint into an L3 market-price package by expanding the 21 candidate commodity series and adding import, fuel, exchange-rate, market-access, and rainfall-source checks.",
  },
  2: {
    readiness: "prototype",
    readinessLabel: "L2 prototype",
    qaSummary: "WDI freshness matrix has a public API artifact, interactive matrix, caveats, screenshots, build/gates, and a generated protocol layer that labels latest, watch, protocol-review, stale-alert, and missing public cells.",
    publicationGap: "Needs full indicator documentation, source-specific non-applicability evidence, and a pre-registered inclusion protocol before a statistical-capacity brief.",
    nextUpgrade: "Promote the protocol into an L3 package by attaching indicator documentation, non-applicability rules, and sensitivity checks for the review thresholds.",
  },
  3: {
    readiness: "prototype",
    readinessLabel: "L2 prototype",
    qaSummary: "Shock-payment rails joins public disaster, payment-use, social-protection, and Findex 2025 candidate-source inventory fields with a checked source-observability ledger.",
    publicationGap: "Needs Findex 2025 variable-glossary mapping, payment-channel validation, ID/source checks, and event-case validation before readiness language.",
    nextUpgrade: "Map the Findex 2025 payment/G2P variables into the generator, then rerun the sprint with event-transfer non-claim checks and one high-exposure case timeline.",
  },
  4: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "BGD source-disagreement route now reads generated psdq-evidence-ledger.json: 28 evidence rows, 572 DGHS upazila rows, 28,166 active clinical facilities, 3,212 joined OSM health features, 39 human/source-owner wall rows, and 0 AI-actionable closures.",
    publicationGap: "Needs owner-only source-owner contact or human validation for possible same-facility candidates, priority and lower-priority name-conflict candidates, zero-OSM facility-row absence decisions, the Durgapur same-name cross-district coordinate conflict, and shared-coordinate Narayanganj records before stronger access-map use.",
    nextUpgrade: "Advance the next decision-ledger class only through public evidence, or stop at owner-only source-owner contact and human location validation when identity/location evidence is required.",
  },
  5: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "Flow-weighting L3 module and remittance program artifacts make this one of the strongest repair-to-publication candidates.",
    publicationGap: "Needs owner-led human-final validation and non-public transaction or central-bank validation before stronger public use.",
    nextUpgrade: "Validate corridor rows against central-bank or transaction sources where available; keep the L3 module as a sensitivity result until then.",
  },
  6: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "The air-monitoring package now publishes a generated evidence ledger: 64 committed summary rows, 214 supporting files, 239 station rows audited, 44 identity candidates, 831 denominator rows, and zero rows at the station-level QA gates needed for coverage claims.",
    publicationGap: "The result is publication-ready only as a public-evidence absence finding. Station-radius coverage and people-served language remain blocked.",
    nextUpgrade: "Add a named §6.7-qualified source only if it plausibly contains station-level calibration, inspection, current status, same-station crosswalk, or method-grade records.",
  },
  7: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "Access map-completeness has registry comparison artifacts, a Cambodia public-facility source audit, and a strong source-audit visual surface.",
    publicationGap: "Needs comparable official/current registry joins for Pakistan and Lao, Cambodia boundary-year and national-hospital source checks, and a travel-time or catchment denominator before access language.",
    nextUpgrade: "Extend registry joins for Pakistan and Lao, finish the Cambodia source-scope checks, and add a public friction/travel-time validation plan.",
  },
  8: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "Disaster metric-falsification now has a bespoke route, clear kill-condition evidence across alternate burden metrics, and a generated GDIS x Black Marble source-readiness object.",
    publicationGap: "Needs an event-level EM-DAT/date join and Black Marble extraction over GDIS footprints or an accepted affected-area proxy before any recovery-lag claim.",
    nextUpgrade: "Build the event-date join and one pilot radiance extraction; keep the current report as source readiness until an actual recovery curve exists.",
  },
  9: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route now joins generation fuel concentration to 15 public World Bank proxy indicators, with 38 DMCs carrying at least one proxy.",
    publicationGap: "Needs direct outage records, reserve-margin/dispatch data, or heat-stress curtailment evidence before reliability framing.",
    nextUpgrade: "Pick 1-2 high-concentration rows and search for regulator outage records, seasonal dispatch, or reserve-margin evidence beyond the World Bank proxy wall.",
  },
  10: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route shows the denominator switch and adds a UNHCR forced-displacement crosswalk for 44 origins; Afghanistan is the only forced-displacement-majority row.",
    publicationGap: "Needs labor, family, student, temporary-work, and visa/deployment corridor data before a migration-purpose report.",
    nextUpgrade: "Add national deployment or visa-class evidence for selected Pacific, Caucasus, and Afghanistan corridors beyond the UNHCR forced-displacement layer.",
  },
  11: {
    readiness: "owner-gated",
    readinessLabel: "Owner-gated",
    qaSummary: "MPI-side decomposition is public and checked, and a CMR source-readiness layer now verifies Black Marble VNP46A3/VNP46A4 metadata and sample links.",
    publicationGap: "Needs owner-led Earthdata/Earth Engine raster access, population-weighted zonal statistics, flare masking, subnational MPI crosswalks, and coauthor attestation before advancing beyond source readiness.",
    nextUpgrade: "Keep as a transparent methods note until owner-led NTL ingestion, zonal statistics, and coauthored review are cleared.",
  },
  12: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route exposes how dropping population changes the proxy and adds a public GHSL/NASADEM/Aqueduct source-readiness wall.",
    publicationGap: "Needs raster download, return-period choice, low-elevation derivation, settlement-footprint overlay, and exposed-population denominator before coastal exposure language.",
    nextUpgrade: "Choose a one-coast pilot, pull the named raster layers, and join settlement, elevation, population, informality, and coastal-hazard cells.",
  },
  13: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route decomposes the flood-market-access proxy and adds a public Geofabrik/WFP/WorldPop/GFD/NASA source wall with all routed-access join flags still false.",
    publicationGap: "Needs a downloaded and routed road graph, geocoded markets or services, population raster weights, observed flood footprints, cut road edges, and travel-time recomputation before access framing.",
    nextUpgrade: "Build a one-DMC flooded-network pilot from the visible source stack, or demote the proxy to a source-method caution note.",
  },
  14: {
    readiness: "portfolio-proof",
    readinessLabel: "Portfolio proof",
    qaSummary: "The route exposes the 34-economy aligned rank comparison, all 21 parameter tests, 2024 direct heat profile, worker-denominator repair, and the unjoined outcome gap.",
    publicationGap: "Needs an observed absenteeism, hours, output, or labor-supply object before advancing from potential capacity to realized labor effects.",
    nextUpgrade: "Freeze a one- or two-economy workplace or subnational exposure-outcome design; do not reopen the national proxy ranking.",
  },
  15: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route foregrounds indicator coverage and common-vintage instability in the food-price screen.",
    publicationGap: "Needs household or market price exposure evidence before vulnerability language.",
    nextUpgrade: "Join a market-price or household-expenditure source for one DMC and keep WDI coverage as the source audit.",
  },
  16: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route makes missing social-protection/payment legs visible before exclusion.",
    publicationGap: "Needs payment-channel or beneficiary delivery data before shock-readiness interpretation.",
    nextUpgrade: "Search public payment-channel metadata and rebuild the screen as coverage-versus-payment-rail observability.",
  },
  17: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route now joins WDI/AQUASTAT available-water stress and FAOSTAT 2024 Area harvested crop mix, while preserving the old internal-denominator artifact.",
    publicationGap: "Needs basin allocation, crop-specific water requirements, irrigation command areas, GRACE depletion, and subnational rural exposure before water-crop diversification framing.",
    nextUpgrade: "Build one basin/crop pilot from the source wall, or keep the current national variant as a denominator and crop-mix caution note.",
  },
  18: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route now preserves the scalar-sweep falsifier and adds GHSL built-up, SMOD, WDI urban-definition, and top-five ADM2 boundary source readiness.",
    publicationGap: "Needs GHSL raster download or Earth Engine export, boundary intersection, classification-history ledger, and population-weighted zonal statistic before invisible-urbanization framing.",
    nextUpgrade: "Select one pilot geography and build the GHSL/SMOD x boundary overlay, or keep the current route as a source-readiness caution note.",
  },
  19: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route preserves the inert-cap audit and adds public WDI LPI, imports, container port traffic, and road/rail/air freight source readiness.",
    publicationGap: "Needs port-level dwell/turnaround/productivity data, port-to-inland OD network, corridor travel-time surface, customs release time, trucking cost, or inland terminal performance evidence.",
    nextUpgrade: "Build one corridor-level port-to-hinterland pilot, or keep the current route as a proxy/source-readiness caution note.",
  },
  20: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route preserves the sensitivity narrowing and adds WDI, CCKP, OSM school-count, and UNICEF source readiness while keeping school-day and outcome joins false.",
    publicationGap: "Needs national school calendars, daily school-day heat or WBGT, cleaned school geocodes, enrollment-weighted exposure, and observed closure, attendance, or learning outcomes before school-disruption language.",
    nextUpgrade: "Build a one-country school calendar x daily heat x school-location pilot, then test whether the Cambodia top-one narrowing survives on in-session exposure rather than annual national heat.",
  },
};

export function getShowcaseReportDepth(report: ShowcaseReport) {
  return showcaseReportDepth[report.id];
}

export function getShowcaseReportQuality(report: ShowcaseReport) {
  return showcaseReportQuality[report.id];
}

export function findShowcaseReportBySlug(slug: string) {
  return showcaseReports.find((report) => report.href === `/showcase/${slug}`);
}
