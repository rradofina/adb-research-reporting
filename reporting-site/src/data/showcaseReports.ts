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
    title: "When a Recovery Measure Fails Two Validity Gates",
    shortTitle: "Disaster construct validation",
    href: "/disaster-recovery-lag",
    status: "verified",
    statusLabel: "Construct-validation report",
    deck: "A pre-registered burden pair fails three of five metric tests. A direct 108-orbit Haiyan pilot then finds no GDIS centroid with one recovery month across 54 variants.",
    evidencePath: "disaster-recovery-lag/results.md",
    visual: "Eight-figure story spanning metric disagreement, source availability, observation coverage, recovery sensitivity, and geometry",
    sourceNote: "EM-DAT, WDI population, GDIS, World Bank Light Every Night VIIRS-DNB, NOAA, and Natural Earth",
  },
  {
    id: 9,
    title: "When the Heat–Reliability Direction Changes with the Measure",
    shortTitle: "Grid construct validation",
    href: "/grid-reliability-heat",
    status: "verified",
    statusLabel: "Construct-validation report",
    deck: "The capacity-to-generation top five survives, but 15 exact-year heat–reliability correlations split 8 positive to 7 negative and reject a directional regional claim.",
    evidencePath: "grid-reliability-heat/generated/grid-heat-reliability-construct-validation.json",
    visual: "Seven-figure story spanning denominator validity, source alignment, proxy vintages, correlation disagreement, and weighting sensitivity",
    sourceNote: "WRI GPPD v1.3.0, World Bank CCKP ERA5, Enterprise Survey and Doing Business electricity indicators",
    audit: {
      kind: "rank-shift",
      programSlug: "grid-reliability-heat",
      dataUrl: "/programs/grid-reliability-heat/generated/grid-heat-reliability-construct-validation.json",
      csvUrl: "/programs/grid-reliability-heat/generated/grid-heat-reliability-diagnostics.csv",
      question: "Does a directional heat–reliability relationship survive reasonable public definitions?",
      finding: "No: 8 of 15 exact-year correlations are positive, 7 negative, and 10 intervals include zero.",
      method: "Join three CCKP ERA5 heat anomalies to five public reliability proxies in the same country and year, then test sign, uncertainty, country weighting, and outcome-tail sensitivity.",
      readerPayoff: "The report separates a supported structural-exposure result from an unsupported regional heat-vulnerability ranking.",
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
    title: "When the Coastal Data Became Spatial",
    shortTitle: "Low-elevation city growth",
    href: "/showcase/coastal-population-denominator",
    status: "verified",
    statusLabel: "Measurement study",
    deck: "GHS-UCDB replaces an inherited national proxy with centre-level population and built-up change below 5 and 10 metres, plus an explicit coverage funnel.",
    evidencePath: "coastal-informal-risk/generated/coastal-lecz-growth-diagnostics.json",
    visual: "Ranked centre changes, proxy falsification, sensitivity, concentration, and coverage",
    sourceNote: "GHS-UCDB R2024A V1.2 Exposure and General Characteristics themes",
    audit: {
      kind: "rank-shift",
      programSlug: "coastal-informal-risk",
      dataUrl: "/programs/coastal-informal-risk/generated/coastal-lecz-growth-diagnostics.json",
      csvUrl: "/programs/coastal-informal-risk/generated/coastal-lecz-urban-centre-panel.csv",
      question: "Which reporting urban centres added the most population below 10 metres from 2000 to 2020?",
      finding: "The reporting subset added 90.9 million people; Shanghai, Bangkok, and Dhaka lead, and only two of the inherited proxy's top five economies remain.",
      method: "Sum the GHS-UCDB below-5-metre and 5-to-10-metre fields inside fixed 2025 centre footprints, compare 2000 with 2020, and repeat at 5 metres and across 10-, 20-, and 30-year windows.",
      readerPayoff: "The page turns a national proxy into a named-city research queue while keeping the blank-field denominator visible.",
      nonClaim: "This is recorded low-elevation exposure growth, not flood probability, loss, informality, deprivation, protection, or policy performance.",
      downloadLabel: "Download LECZ growth diagnostics",
    },
  },
  {
    id: 13,
    title: "When Flood Water Cuts the Route to Market",
    shortTitle: "Sylhet routed-access pilot",
    href: "/showcase/flood-component-decomposition",
    status: "verified",
    statusLabel: "Construct validation",
    deck: "An observed UNOSAT flood footprint is joined to historical OSM roads and marketplaces plus WorldPop, then flood-intersecting road edges are mechanically removed across 54 sensitivity variants.",
    evidencePath: "flood-market-access/generated/flood-sylhet-route-pilot.json",
    visual: "Route map, access split, sensitivity grid, denominator funnel, and claim gates",
    sourceNote: "UNOSAT product 3888, historical OSM Overpass snapshot, and WorldPop Bangladesh 2020",
    audit: {
      kind: "rank-shift",
      programSlug: "flood-market-access",
      dataUrl: "/programs/flood-market-access/generated/flood-sylhet-route-pilot.json",
      csvUrl: "/programs/flood-market-access/generated/flood-sylhet-route-sensitivity.csv",
      question: "How much baseline market access disappears when every road edge intersecting observed flood water is treated as unavailable?",
      finding: "About 345,718 people, or 41.24% of the baseline-accessible covered population, lose a modeled route to eight mapped marketplaces; all 54 variants remain between 38.92% and 43.45%.",
      method: "Clip historical roads, mapped marketplaces, and WorldPop cells to the UNOSAT analysis footprint; remove every flood-intersecting road edge; reroute population; vary all arbitrary numeric choices by ±50% and test a broader road set.",
      readerPayoff: "The page shows both the stable route result and the exact validation gates that prevent it from becoming a road-investment claim.",
      nonClaim: "This is not observed road closure or passability, actual market choice, welfare loss, food insecurity, or a Bangladesh-wide estimate.",
      downloadLabel: "Download Sylhet route-pilot JSON",
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
    title: "When the Rice-Price Wave Is Not Locally Dry",
    shortTitle: "Food-price construct validation",
    href: "/showcase/food-price-coverage-trap",
    status: "verified",
    statusLabel: "Construct validation",
    deck: "A corrected 12-market Nepal panel turns an inherited climate-price ranking into a measurement result: 17 of 152 rice-price spikes follow locally dry rainfall, and the direction survives 81 threshold runs.",
    evidencePath: "food-price-climate-transmission/generated/food-price-construct-validation.json",
    visual: "Alignment split, lag lanes, source funnel, threshold stability, annual mismatch, and claim gates",
    sourceNote: "WFP Nepal market prices, NASA POWER monthly point rainfall, and World Bank headline CPI context",
    audit: {
      kind: "sensitivity-lanes",
      programSlug: "food-price-climate-transmission",
      dataUrl: "/programs/food-price-climate-transmission/generated/food-price-construct-validation.json",
      csvUrl: "/programs/food-price-climate-transmission/generated/food-price-market-month-corrected.csv",
      question: "After correcting the price outcome, is local dry rainfall the common near-term signature of Nepal rice-price spikes?",
      finding: "No. At one month, 17 of 152 corrected spike cells are dry-aligned; the dry share remains below half in every one of 81 threshold runs.",
      method: "Replace the full-sample calendar-month median with same-market year-on-year log price change, align point rainfall by market and lag, then vary every arbitrary threshold by ±50%.",
      readerPayoff: "The page explains why the old wave count changed, which direction survives sensitivity, why annual CPI cannot validate the market result, and which attribution gates remain closed.",
      nonClaim: "The 11.2% is a coincidence share, not a causal contribution, food-security ranking, household-welfare estimate, or all-food-price result.",
      downloadLabel: "Download construct-validation JSON",
    },
  },
  {
    id: 16,
    title: "When Missing a Data Leg Removes the Runner-Up",
    shortTitle: "Social-protection dropped leg",
    href: "/showcase/social-protection-dropped-leg",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The inherited screen is re-ranked before excluding one-legged observations, stress-tested against a narrower coverage object, and checked against documented COVID-19 response instruments.",
    evidencePath: "social-protection-shock-coverage/generated/social-protection-covid-response-validation.json",
    visual: "Three-gate validity audit plus observed-response matrix",
    sourceNote: "WDI poverty, ASPIRE all-SP and safety-net coverage, Findex account ownership, and World Bank COVID-19 response matrix",
    audit: {
      kind: "rank-shift",
      programSlug: "social-protection-shock-coverage",
      dataUrl: "/programs/social-protection-shock-coverage/generated/social-protection-covid-response-validation.json",
      csvUrl: "/programs/social-protection-shock-coverage/generated/social-protection-covid-response-diagnostics.csv",
      question: "Is the shock-payment screen observing delivery capacity, or only a convenient WDI source stack?",
      finding: "Only three named members survive the panel's own value order; every named economy has a documented cash-transfer response; no comparable delivery outcome is joined.",
      method: "Reproduce the dropped-leg ledger, rerun the coverage variants, parse the World Bank COVID-19 response matrix, and bootstrap the gap-versus-response-breadth association.",
      readerPayoff: "The page turns a readiness ranking into a three-gate construct audit and specifies the event-level delivery table the next study requires.",
      nonClaim: "This does not certify shock-payment readiness, beneficiary reach, delivery speed, payment-rail use, or adaptive social-protection capacity.",
      downloadLabel: "Download social-protection construct-validation JSON",
    },
  },
  {
    id: 17,
    title: "When a Stable Water-Crop Ranking Fails Its Own Constructs",
    shortTitle: "Water-crop construct failure",
    href: "/showcase/water-stress-denominator",
    status: "verified",
    statusLabel: "Construct validation",
    deck: "The published set is the raw top four in only two of seven runs; direct available-water stress retains two members, direct crop concentration none, and the source join loses every crop-HHI leader.",
    evidencePath: "water-stress-crop-diversification/generated/water-construct-validation.json",
    visual: "Three-gate finding, membership matrix, denominator bridge, crop-water scatter, coverage funnel, driver diagnostics, and next-object design",
    sourceNote: "Inherited WDI screen, WDI/AQUASTAT SDG 6.4.2, FAOSTAT 2024 Area harvested, and deterministic bootstrap/sensitivity outputs",
    audit: {
      kind: "component-audit",
      programSlug: "water-stress-crop-diversification",
      dataUrl: "/programs/water-stress-crop-diversification/generated/water-construct-validation.json",
      csvUrl: "/programs/water-stress-crop-diversification/generated/water-construct-diagnostics.csv",
      question: "Does the inherited four-country screen survive its saved ranking rule and direct national water and crop measures?",
      finding: "No. The set is the raw top four in 2 of 7 runs; direct water retains 2 of 4 members, direct crop HHI 0 of 4, and all five crop-HHI leaders lack water rows.",
      method: "Reconstruct seven saved runs, replace the internal-water ratio with SDG 6.4.2, replace inverse cereal yield with FAOSTAT crop HHI, audit coverage, bootstrap rank associations, and test 27 ±50% diagnostic specifications.",
      readerPayoff: "The page makes the claim decision visible first, then shows denominator effects, crop disagreement, coverage selection, driver dominance, and the exact basin-crop object required next.",
      nonClaim: "This is not a basin allocation, irrigation-demand, crop-water-use, GRACE depletion, or subnational exposure analysis.",
      downloadLabel: "Download water construct-validation JSON",
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
    title: "When a School-Heat Proxy Meets an Observed Outcome",
    shortTitle: "School-heat construct check",
    href: "/showcase/school-heat-sensitivity",
    status: "verified",
    statusLabel: "Construct validation",
    deck: "Cambodia led the inherited proxy but ranks sixth of six by affected-student count in UNICEF's heatwave-major ADB subset; demographic scale, not the composite, carries the observed count order.",
    evidencePath: "school-heat-disruption/generated/school-construct-validation.json",
    visual: "Sensitivity correction, observed-outcome rank reversal, driver comparison, coverage funnel, and next-data-object specification",
    sourceNote: "UNICEF Learning Interrupted Annex 1, World Bank Indicators API enrollment, and the inherited WDI/CCKP proxy panel",
    audit: {
      kind: "rank-shift",
      programSlug: "school-heat-disruption",
      dataUrl: "/programs/school-heat-disruption/generated/school-construct-validation.json",
      csvUrl: "/programs/school-heat-disruption/generated/school-construct-diagnostics.csv",
      question: "Does the inherited proxy preserve its claimed sensitivity result and order UNICEF's observed 2024 heatwave-major affected-student counts?",
      finding: "No. Cambodia wins 5 of 6 discriminating runs but ranks 6 of 6 by observed count; the old index has Spearman +0.03, compared with +0.94 for child population.",
      method: "Reread the seven committed sensitivity runs, validate 21 transcribed ADB rows against UNICEF's PDF annex, isolate six heatwave-major rows, and bootstrap rank correlations with fixed seeds.",
      readerPayoff: "The page shows exactly where internal formula stability stops and outcome validation begins, then specifies the school-day object needed next.",
      nonClaim: "This is not a causal heat effect, complete event census, harmonized disruption rate, days-lost estimate, learning-loss estimate, or replacement country ranking.",
      downloadLabel: "Download school-heat construct-validation JSON",
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
    operationalUse: "Prioritize named urban centres for local hazard, subsidence, protection, and service-data deepening while retiring the inherited country proxy.",
    falsifier: "If the direction disappears under the 5-metre definition or ±50% time windows, the regional growth claim should be withdrawn.",
    limitation: "The 1,334-centre reporting subset measures low-elevation exposure growth, not flood probability, loss, informality, deprivation, protection, or policy performance.",
  },
  13: {
    operationalUse: "Use the stable disconnection band to prioritize passability and destination validation in the Sylhet footprint, not to select investments yet.",
    falsifier: "Observed passability, official market validation, or household destination evidence could reconnect the modeled population or materially change which routes matter.",
    limitation: "Flood intersection is treated as complete unavailability; mapped marketplaces proxy destinations; WorldPop 2020 predates the 2024 event; boats, traffic, bridge condition, elevation, and flood depth are omitted.",
  },
  14: {
    operationalUse: "Help health and labor teams distinguish a stable screen from a valid heat-labor construct before using ranks for planning.",
    falsifier: "If an observed exposure-outcome panel shows the proxy predicts labor outcomes as well as the heat construct under a frozen design, the rejection must be reconsidered.",
    limitation: "The direct heat measure remains modelled potential capacity loss, and this package joins no observed absence, hours, output, or labor-supply outcome.",
  },
  15: {
    operationalUse: "Stop annual macro rankings from being narrated as climate-to-food-price transmission and focus the next study on the visible 2023–2024 Nepal market wave.",
    falsifier: "A recorded-event, multi-commodity panel with access and common-driver controls could show a stronger or delayed climate relationship than the market-point dryness screen captures.",
    limitation: "The panel covers coarse rice in 12 selected markets and monthly point rainfall; it has no observed hazard event, crop-zone exposure, or causal design.",
  },
  16: {
    operationalUse: "Make missing social-protection or payment legs visible before excluding economies from shock-readiness screens.",
    falsifier: "If payment-channel and beneficiary data validate the headline five after one-leg repair, the missingness concern weakens.",
    limitation: "The public legs do not certify emergency payment delivery, identity readiness, or beneficiary reach.",
  },
  17: {
    operationalUse: "Prevent a national proxy ranking from being used for targeting and focus source work on basin, crop, irrigation, and outcome alignment.",
    falsifier: "If a basin-level crop-water outcome study preserves the same set after allocation, crop demand, irrigation status, weather, and exposure are aligned, the construct-failure conclusion narrows.",
    limitation: "The validation is national and cross-sectional; it contains no basin allocation, irrigation demand, depletion, crop-water exposure, or resilience outcome.",
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
    falsifier: "A harmonized school-day panel could show that the UNICEF count comparison is driven by reporting selection, event duration, calendars, or adaptation rather than the inherited proxy's construct failure.",
    limitation: "The heatwave-major validation set has six selected country rows. Counts can be reported or enrollment-estimated, identify only the largest disruption hazard, and do not measure duration, attendance, or learning.",
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
    readiness: "portfolio-proof",
    readinessLabel: "Measurement study",
    qaSummary: "The route reads the direct GHS-UCDB centre panel, shows 90.9 million net growth, the old/new construct break, all six sensitivity runs, and the 5,347-to-1,334 coverage funnel.",
    publicationGap: "Needs local storm surge, relative sea level, subsidence, protection, and validated social conditions before advancing from exposure growth to risk or policy targeting.",
    nextUpgrade: "Select a small number of leading centres and qualify local hazard, protection, planning-boundary, and housing or service layers before any risk study.",
  },
  13: {
    readiness: "portfolio-proof",
    readinessLabel: "Construct validation",
    qaSummary: "The full package joins an observed flood vector, a historical road graph, mapped marketplaces, and a population raster; it reports a 41.24% modeled disconnection share and a 38.92%-43.45% range across 54 variants.",
    publicationGap: "Needs observed road and bridge passability, an official or audited market destination inventory, and observed travel or market outcomes before operational targeting or welfare claims.",
    nextUpgrade: "Validate road passability and market destinations inside the same Sylhet footprint, then compare modeled routes with observed travel or market outcomes.",
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
    readinessLabel: "Construct validation",
    qaSummary: "Full paper and ten-figure evidence spine correct the Nepal outcome, align 760 market-month cells, expose 81-run threshold stability, and retire the annual qualifier.",
    publicationGap: "Needs recorded geocoded hazards, multiple commodities, crop and sourcing zones, connectivity, common-driver controls, and an event-study or local-projection design before transmission language.",
    nextUpgrade: "Update the existing Nepal event-based literature with newer events and commodities; test connectivity heterogeneity rather than create another country score.",
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
    readinessLabel: "Construct validation",
    qaSummary: "Full paper and nine-figure evidence spine reject the inherited country ranking using saved-run fidelity, direct water and crop objects, coverage selection, bootstrap associations, and ±50% sensitivity.",
    publicationGap: "Needs one basin × crop × irrigation × year pilot with an observed depletion, production, income, or recovery outcome before any exposure or resilience claim.",
    nextUpgrade: "Build the shared-unit pilot; do not create another national composite.",
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
    readinessLabel: "Construct validation",
    qaSummary: "The artifact verifies the seven sensitivity runs, checks 21 transcribed ADB rows against UNICEF's PDF annex, isolates six heatwave-major rows, and reports fixed-seed bootstrap diagnostics.",
    publicationGap: "Needs a school-day or district-day join of local heat, calendars, enrollment, school conditions, adaptation, and closure, attendance, assessment, or learning outcomes.",
    nextUpgrade: "Build one public school-day exposure-outcome pilot; do not retune the national composite as a substitute for the shared unit.",
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
