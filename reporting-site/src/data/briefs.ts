export type FinishGroup =
  | "publication-ready"
  | "construct-validation"
  | "screening-result"
  | "program-prospectus"
  | "prepared-pipeline"
  | "hypothesis";

export interface BriefDetail {
  slug: string;
  articleSlug?: string;
  domain: string;
  finish: FinishGroup;
  question: string;
  output: string;
  chartTitle: string;
  sourceNote: string;
  caveat: string;
  nextStep: string;
  flagship?: boolean;
  granularity: {
    currentUnit: string;
    targetUnit: string;
    gap: string;
    upgradeData: string;
  };
}

export const FINISH_LABELS: Record<FinishGroup, string> = {
  "publication-ready": "Publication-ready",
  "construct-validation": "Construct check",
  "screening-result": "Screening only",
  "program-prospectus": "Program prospectus",
  "prepared-pipeline": "Pipeline ready, not run",
  hypothesis: "Not finished",
};

export const ROAD_QUALITY_NEXT_TRACK = {
  title: "Road quality and poverty access",
  currentUnit: "Not in the current issue",
  targetUnit: "Road segment, village or settlement, municipality, facility and market catchment",
  gap:
    "The current register has road presence and access proxies, but not road surface quality, roughness, all-season passability, or maintenance condition.",
  upgradeData:
    "OSM/Overture/GRIP roads; Mapillary or pavedness predictions; satellite road surface/width products; smartphone or IRI validation where available; WorldPop/GHSL; MPI/PIP poverty; clinic, school, and market locations; flood and landslide layers.",
  adbMethod:
    "ADB's road-quality ML line uses satellite-image road crops plus ground road-roughness labels to classify road condition. The later guidebook frames a CNN branch, a tabular neural-network branch for geospatial covariates, optional super-resolution, and smartphone-based pavement-condition collection as complementary inputs.",
  modelStack:
    "Computer vision CNN/transfer learning for road images; tabular neural network using variables such as temperature, elevation, precipitation, and population; combined dense classification layer for good, fair, poor, and bad road classes.",
  validation:
    "The 2022 ADB working paper reports a preliminary Philippines validation with accuracy up to 75% for identifying poor-to-bad roads. Development Asia summarizes stronger binary performance, around 75%, than four-class classification, around 60%.",
  limitation:
    "This should be treated as a maintenance-screening and prioritization layer, not a replacement for conventional pavement surveys or engineering-grade IRI collection.",
  sources: [
    {
      label: "ADB EWP 675: ML satellite imagery road-quality monitoring",
      href: "https://www.adb.org/publications/machine-learning-satellite-imagery-road-quality-monitoring",
    },
    {
      label: "ADB Development Asia explainer on poverty-related mobility",
      href: "https://development.asia/explainer/innovative-solutions-address-poverty-related-transport-and-mobility-challenges",
    },
    {
      label: "ADB 2025 guidebook: ML techniques for road quality monitoring",
      href: "https://policycommons.net/artifacts/20142856/guidebook-on-machine-learning-techniques-for-road-quality-monitoring/21043381/",
    },
    {
      label: "ADB CAREC road asset management guidance",
      href: "https://www.adb.org/sites/default/files/publication/396126/best-practices-road-asset-management-carec.pdf",
    },
    {
      label: "World Bank road-quality prediction from satellite imagery",
      href: "https://documents1.worldbank.org/curated/en/099053124190527291/pdf/P17987918d4d95027181761ef0f539d6fea.pdf",
    },
    {
      label: "Mapillary global paved/unpaved road-surface dataset",
      href: "https://arxiv.org/abs/2410.19874",
    },
  ],
};

export const BRIEF_DETAILS: Record<string, BriefDetail> = {
  "mpi-nighttime-lights": {
    slug: "mpi-nighttime-lights",
    domain: "Poverty",
    finish: "hypothesis",
    question:
      "Can MPI deprivation patterns be read alongside nighttime-light intensity without losing the multidimensional structure of poverty?",
    output:
      "Repository contains OPHI MPI 2024 parsing and seed data; the nighttime-lights join is not committed here.",
    chartTitle: "Chart pending: MPI x nighttime lights decomposition",
    sourceNote: "OPHI Global MPI 2024 is parsed; VIIRS or Black Marble data are planned for the light layer.",
    caveat:
      "This is a co-authored external track with Arturo Martinez Jr.; repo status stays hypothesis until the external work is reconciled.",
    nextStep:
      "Decide whether to import the external NTL code/data path or retire this repo track with a pointer to the external paper.",
    granularity: {
      currentUnit: "National MPI tables parsed; subnational MPI raw file present",
      targetUnit: "Subnational MPI unit, ADM1/ADM2 where available, VIIRS or Black Marble grid cell",
      gap:
        "Nighttime-lights ingestion and zonal statistics are not committed here; the co-authored external track still needs reconciliation.",
      upgradeData:
        "OPHI subnational MPI, NASA Black Marble or VIIRS DNB, geoBoundaries, WorldPop/GHSL population, and a harmonized admin crosswalk.",
    },
  },
  "access-services": {
    slug: "access-services",
    articleSlug: "access-stress-pilot-cluster",
    domain: "Access",
    finish: "prepared-pipeline",
    question:
      "Which pilot DMCs show the strongest mismatch between mapped amenities and population-weighted service load?",
    output:
      "An 8-DMC ADM1 pilot finds a stable top-4 access-stress set: Bangladesh, Cambodia, Lao PDR, and Pakistan.",
    chartTitle: "Access-stress index, pilot economies",
    sourceNote: "OSM/Overpass, geoBoundaries, WorldPop, and national census population where available.",
    caveat:
      "Facility-count stress is not travel-time access; road-network isochrones remain the policy-grade measure.",
    nextStep:
      "Run travel-time surfaces and separate health, education, and market access instead of pooling services.",
    granularity: {
      currentUnit: "ADM1 pilot across 104 units in 8 DMCs",
      targetUnit: "Road segment, settlement grid, facility catchment, municipality",
      gap:
        "Current result is facility-count/service-load stress, not travel-time access or climate-disrupted passability.",
      upgradeData:
        "MAP friction surface, OSM/Overture roads, clinic/school/market POIs, WorldPop, and flood and heat rasters.",
    },
  },
  "digital-performance": {
    slug: "digital-performance",
    articleSlug: "digital-availability-use-gap",
    domain: "Connectivity",
    finish: "prepared-pipeline",
    question:
      "Do reported 4G/LTE population coverage and recent internet use tell the same connectivity story?",
    output:
      "In 2024, coverage exceeds use by a median 14.3 percentage points across 34 exact-year ADB developing member cases; 31 differences are positive.",
    chartTitle: "4G/LTE availability minus internet use, 2024",
    sourceNote: "ITU DataHub i271GA and i99H; exact economy-year pairs with no temporal imputation.",
    caveat:
      "The difference is between aggregate official indicators, not a person-level count; it does not measure speed, quality, household affordability, or causal effects.",
    nextStep:
      "Expand comparable urban/rural and demographic use data, then add Ookla only as a separate performance-conditional-on-testing layer.",
    granularity: {
      currentUnit: "Economy-year exact matches across 39 observed roster economies, 2012–2024",
      targetUnit: "Household/person, rural/urban stratum, municipality, and tested performance tile as separate layers",
      gap:
        "National aggregates cannot identify the covered-but-offline population or explain barriers; only ten 2024 cases have exact-year rural/urban use rates.",
      upgradeData:
        "Household ICT surveys, device ownership, digital skills, stated non-use barriers, distribution-sensitive affordability, and Ookla/MLab as conditional quality layers.",
    },
  },
  "air-monitoring": {
    slug: "air-monitoring",
    articleSlug: "pm25-observability-gap-cluster",
    domain: "Environment",
    finish: "screening-result",
    question:
      "Can public sources verify station-level monitor QA well enough for coverage claims?",
    output:
      "The generated ledger indexes 64 summary rows and 214 supporting files, but the claim-enabling QA counters remain zero for validated same-station rows, BMKG station-level certificates/logs/status rows, complete monitor-grade rows, station-radius-ready economies, and allowed coverage-claim rows.",
    chartTitle: "Public monitor-QA evidence gate ledger",
    sourceNote: "OpenAQ v3, public regulator/station portals, BMKG routes, Georgia routes, Uzbekistan routes, GHSL/ACAG custody, and generated evidence ledger.",
    caveat:
      "The result is absence in audited public routes, not proof the records do not exist.",
    nextStep:
      "Add a newly named source only if it plausibly contains station-level calibration, inspection, crosswalk, or grade evidence.",
    granularity: {
      currentUnit: "Public source route, station row, and claim-enabling QA gate",
      targetUnit: "Validated same-station monitor with station-level calibration, inspection, and grade evidence",
      gap:
        "Public station/source context exists, but station-level QA records and same-station crosswalks do not close the coverage gate.",
      upgradeData:
        "Official station-level QA ledgers, calibration certificates, inspection logs, current calibration-status rows, and official/OpenAQ station crosswalks.",
    },
  },
  "invisible-urbanization": {
    slug: "invisible-urbanization",
    articleSlug: "invisible-urbanization-cluster",
    domain: "Built form",
    finish: "screening-result",
    question:
      "Which rural-majority economies have rapid urban growth that may outrun official urban classification?",
    output:
      "Papua New Guinea, Solomon Islands, Afghanistan, Lao PDR, and Bangladesh hold the top urban-growth-from-rural-base signal.",
    chartTitle: "Invisible urbanization signal",
    sourceNote: "WDI urban share, urban population growth, rural share, and population.",
    caveat:
      "The signal is a proxy; official urban definitions differ across economies.",
    nextStep:
      "Run GHSL built-up-surface change and compare it with national urban-classification changes.",
    granularity: {
      currentUnit: "Country-level WDI urban-growth-from-rural-base proxy",
      targetUnit: "Settlement grid, city edge, municipality, building footprint cluster",
      gap:
        "No GHSL, Dynamic World, or building-time-series layer has been joined yet.",
      upgradeData:
        "GHSL built-up/population grids, Google Open Buildings temporal data, Dynamic World, Overture buildings, and WorldPop.",
    },
  },
  "climate-health-workdays": {
    slug: "climate-health-workdays",
    articleSlug: "workday-loss-pressure-cluster",
    domain: "Health",
    finish: "program-prospectus",
    question:
      "Does the inherited PM2.5 × employment proxy recover a direct heat-related labor-capacity signal?",
    output:
      "No. Across 21 aligned tests, top-three overlap is never greater than one economy; 16 tests have zero overlap.",
    chartTitle: "Proxy versus heat-work-loss construct agreement",
    sourceNote: "Aligned World Bank WDI inputs and Lancet Countdown 2025 indicator 1.1.3 country workbooks.",
    caveat:
      "Potential work hours lost are modelled capacity losses, not recorded absence, output, or a causal estimate from this study.",
    nextStep:
      "Join observed absenteeism, hours, output, or labor-supply data to compatible workplace or subnational heat exposure.",
    granularity: {
      currentUnit: "Aligned country-year rank comparison, 34 economies in 2018–2020",
      targetUnit: "Workplace or subnational exposure-outcome panel by sector and time",
      gap:
        "The direct heat measure is modelled and no observed labor outcome is joined.",
      upgradeData:
        "Observed absence, hours, output, or labor supply; workplace adaptation; WBGT or heat-index exposure; aligned employment and sector data.",
    },
  },
  "coastal-informal-risk": {
    slug: "coastal-informal-risk",
    articleSlug: "coastal-informal-cluster",
    domain: "Built form",
    finish: "publication-ready",
    question:
      "Which urban centres recorded the largest population and built-up growth below 5 and 10 metres from 2000 to 2020?",
    output:
      "The reporting subset added 90.9 million people below 10 metres; Shanghai, Bangkok, and Dhaka lead, and ten centres account for 52.1% of positive change.",
    chartTitle: "Low-elevation urban-centre growth",
    sourceNote: "GHS-UCDB R2024A V1.2 Exposure and General Characteristics themes.",
    caveat:
      "Only 1,334 of 5,347 matched centres report the required LECZ block; the result is exposure growth, not flood loss or informality.",
    nextStep:
      "Join local storm surge, relative sea level, subsidence, protection, and validated housing or service data for a small set of leading centres.",
    granularity: {
      currentUnit: "Fixed-2025 GHS-UCDB urban centre with 5 m and 10 m LECZ attributes",
      targetUnit: "Hazard-resolved neighbourhood, barangay, or municipality inside selected centres",
      gap:
        "The centre object observes elevation-zone exposure but not surge, subsidence, protection, tenure, services, or loss.",
      upgradeData:
        "Local coastal-hazard surfaces, relative sea level, subsidence, protection and drainage, dated boundaries, and validated deprivation or service layers.",
    },
  },
  "disaster-recovery-lag": {
    slug: "disaster-recovery-lag",
    articleSlug: "disaster-burden-cluster",
    domain: "Disaster",
    finish: "construct-validation",
    question:
      "Can public disaster records and daily nighttime radiance support a stable recovery-month measure?",
    output:
      "No. Three of five burden metrics replace the inherited top two, while zero of seven Haiyan centroids retain one recovery month across 54 variants.",
    chartTitle: "Two-stage recovery construct validation",
    sourceNote: "EM-DAT, GDIS, World Bank Light Every Night VIIRS-DNB, NOAA, and Natural Earth.",
    caveat:
      "GDIS centroids are administrative approximations; nighttime radiance is not welfare, reconstruction, or a causal recovery outcome.",
    nextStep:
      "Join verified event footprints, longer baselines, comparison areas, and independent service or household recovery outcomes.",
    granularity: {
      currentUnit: "Country-level burden plus seven GDIS administrative centroids for one Haiyan pilot",
      targetUnit: "Event footprint, affected municipality, nightlight grid, service-restoration area",
      gap:
        "Administrative centroids do not represent impact footprints, and the daily series has thin valid baselines.",
      upgradeData:
        "Verified hazard or damage footprints, longer VIIRS baselines, settlement masks, electricity or facility restoration, and household outcomes.",
    },
  },
  "flood-market-access": {
    slug: "flood-market-access",
    articleSlug: "flood-market-access-cluster",
    domain: "Access",
    finish: "construct-validation",
    question:
      "Within the observed 26 June 2024 Sylhet flood footprint, how much modeled population loses a road route to a mapped marketplace under a transparent road-cut rule?",
    output:
      "The base model disconnects 345,718 people, or 41.24% of the baseline-accessible covered population; all 54 variants remain between 38.92% and 43.45%.",
    chartTitle: "Sylhet modeled market-route disconnection",
    sourceNote: "UNOSAT product 3888, historical OpenStreetMap roads and marketplaces, and WorldPop 2020.",
    caveat:
      "Every water-intersecting segment is modeled unavailable; road closure, market operation, destination choice, and welfare are not observed.",
    nextStep:
      "Validate road and bridge passability, audit formal and informal markets, add multiple event times, and join observed travel or market outcomes.",
    granularity: {
      currentUnit: "WorldPop cell × historical road graph × mapped marketplace inside one UNOSAT event footprint",
      targetUnit: "Validated road/bridge state × operating market × origin × event time",
      gap:
        "Passability and destination completeness are unvalidated, and the population surface predates the event.",
      upgradeData:
        "Road depth or field closure observations, bridge elevations, official and informal market registries, travel modes, market operation, prices, and household or trader outcomes.",
    },
  },
  "food-price-climate-transmission": {
    slug: "food-price-climate-transmission",
    articleSlug: "food-price-joint-qualifier",
    domain: "Food",
    finish: "publication-ready",
    question:
      "After correcting the price outcome, how often do large Nepal rice-price increases follow locally dry rainfall?",
    output:
      "Only 17 of 152 corrected market-month spike cells align with locally dry rainfall at one month; the minority direction survives all 81 threshold runs.",
    chartTitle: "Corrected Nepal rice-price alignment",
    sourceNote: "WFP Nepal coarse-rice market prices, NASA POWER monthly point rainfall, and WDI CPI context.",
    caveat:
      "The 11.2% is a threshold coincidence share, not the fraction of price change caused by climate.",
    nextStep:
      "Build an event-defined multi-commodity panel with crop zones, connectivity, common-driver controls, and a pre-specified panel design.",
    granularity: {
      currentUnit: "Nepal market × month × coarse-rice price × point rainfall",
      targetUnit: "Market × commodity × dated hazard event × production/sourcing zone",
      gap:
        "No recorded hazard event, multi-commodity outcome, market-access controls, or causal design is joined.",
      upgradeData:
        "WFP or official multi-commodity prices, geocoded hazard events, crop calendars, production zones, roads, fuel, exchange rates, trade, and policy data.",
    },
  },
  "grid-reliability-heat": {
    slug: "grid-reliability-heat",
    articleSlug: "single-fuel-grid-cluster",
    domain: "Energy",
    finish: "publication-ready",
    question:
      "Does a directional regional heat–reliability relationship survive reasonable public definitions?",
    output:
      "No. The 15 exact-year correlations split 8 positive to 7 negative; the separate capacity-to-generation concentration top five remains stable.",
    chartTitle: "Two-gate construct validation",
    sourceNote: "WRI GPPD v1.3.0; World Bank CCKP ERA5; World Bank public reliability indicators.",
    caveat:
      "Annual country heat and sporadic reliability proxies do not identify event-level heat effects or current grid reliability.",
    nextStep:
      "Obtain service-territory interruption timing joined to daily/hourly heat, demand, available generation, imports, and network conditions.",
    granularity: {
      currentUnit: "Country-level power-plant fuel-mix concentration",
      targetUnit: "Plant, substation, feeder/service area, city or district",
      gap:
        "Fuel concentration is structural exposure; outage and heat-reliability layers are missing.",
      upgradeData:
        "Plant coordinates, grid/substation layers, public outage records where available, ERA5 heat, and demand/load data.",
    },
  },
  "migration-displacement-signals": {
    slug: "migration-displacement-signals",
    articleSlug: "emigrant-stock-corridor-concentration",
    domain: "Migration",
    finish: "publication-ready",
    question:
      "How much does the leading-origin set change when the same emigrant stock is divided by resident population?",
    output:
      "The absolute and population-share top fives have zero overlap; Afghanistan is the separate forced-displacement-majority exception at population-share rank six.",
    chartTitle: "Absolute versus population-normalized emigrant-stock rank",
    sourceNote:
      "UN DESA International Migrant Stock 2024, WDI 2024 population, and UNHCR Refugee Data Finder 2024.",
    caveat:
      "The ratio compares cumulative stock with a resident-population snapshot; it is not a current flow, migration propensity, labor-purpose, welfare, or causal estimate.",
    nextStep:
      "Build a purpose-specific annual-flow panel from documented deployment or visa data and test whether its ordering separates from the stock ordering.",
    granularity: {
      currentUnit:
        "Country-level absolute stock, stock relative to resident population, and UNHCR protection-category crosswalk",
      targetUnit:
        "Annual purpose-specific bilateral flow, subnational origin, and destination corridor",
      gap:
        "Stock data do not identify current departures, labor purpose, repeat movers, or subnational origin.",
      upgradeData:
        "Public deployment, visa-class, return, census-transition, or disclosure-reviewed household migration data.",
    },
  },
  "port-hinterland-friction": {
    slug: "port-hinterland-friction",
    articleSlug: "port-friction-trade-volume-cluster",
    domain: "Trade",
    finish: "screening-result",
    question:
      "Does a national imports × LPI screen agree with observed port-time disadvantage?",
    output:
      "No. Only Indonesia overlaps between the inherited and observed-port top fives in the main test.",
    chartTitle: "National proxy versus observed port time",
    sourceNote: "World Bank CPPI 2020–2025 annex, WDI imports, and LPI.",
    caveat:
      "CPPI measures vessel time inside the port boundary, not the port-to-inland journey.",
    nextStep:
      "Join the official LPI 2.0 shipment file before making any hinterland claim.",
    granularity: {
      currentUnit: "Port-level CPPI with diagnostic country summaries",
      targetUnit: "Port-to-inland shipment corridor and destination",
      gap:
        "CPPI stops at the port boundary; the official shipment-corridor file is not yet joined.",
      upgradeData:
        "World Bank LPI 2.0 shipment indicators, including port turnaround and port-exit-to-destination corridor lead time.",
    },
  },
  "public-service-data-quality": {
    slug: "public-service-data-quality",
    articleSlug: "measurement-gap-philippines-bangladesh",
    domain: "Measurement",
    finish: "publication-ready",
    flagship: true,
    question:
      "How far do public maps diverge from official health-facility registries?",
    output:
      "OSM captures 17.1% of the Philippines clinical-tier registry and 11.8% of the Bangladesh registry.",
    chartTitle: "Clinical registry gap",
    sourceNote: "OpenStreetMap, Philippines DOH NHFR, and Bangladesh DGHS Facility Registry.",
    caveat:
      "The comparison is a registry-observability gap, not a claim about actual service availability.",
    nextStep:
      "Extend to India and Indonesia and add facility-type harmonization checks.",
    granularity: {
      currentUnit: "ADM1 counts for Philippines and Bangladesh",
      targetUnit: "Facility record, ADM2/province/district, facility catchment",
      gap:
        "Current result compares counts by harmonized tier; facility-level matching and ADM2 geography are not complete.",
      upgradeData:
        "Geocoded registry records, healthsites.io/OSM extracts, fuzzy name/address matching, ADM2 boundaries, and facility-type harmonization.",
    },
  },
  "remittance-resilience": {
    slug: "remittance-resilience",
    articleSlug: "remittance-corridors-vulnerability-cluster",
    domain: "Finance",
    finish: "publication-ready",
    flagship: true,
    question:
      "Which DMCs combine high remittance dependence with costly inbound corridors?",
    output:
      "The repaired baseline top five are Kyrgyz Republic, Samoa, Tonga, Nepal, and Vanuatu; four remain common across the +/-50% sensitivity suite after parser repair, while the same five remain in the flow-weighted top five.",
    chartTitle: "Remittance corridor stress screen",
    sourceNote: "World Bank WDI remittance share, Remittance Prices Worldwide Q1 2025, and World Bank/KNOMAD 2021 bilateral flows.",
    caveat:
      "This is corridor-cost exposure, not household-level resilience.",
    nextStep:
      "Use the rebuilt L3 packet as sensitivity evidence, then add household microdata or central-bank validation before any stronger remittance-price claim.",
    granularity: {
      currentUnit: "Country destination mean cost and remittance dependence",
      targetUnit: "Bilateral corridor, household survey region, remittance-receiving household group",
      gap:
        "RPW destination means are source-sensitive, KNOMAD flows are 2021 estimates, and household exposure is not observed.",
      upgradeData:
        "Central-bank corridor flow data, RPW microdata, LSMS/DHS/national household surveys, and migrant corridor histories.",
    },
  },
  "school-heat-disruption": {
    slug: "school-heat-disruption",
    articleSlug: "school-heat-honest-narrowing",
    domain: "Education",
    finish: "construct-validation",
    question:
      "Does the inherited school-heat proxy survive its own sensitivity language and align with an observed disruption outcome?",
    output:
      "No. Cambodia leads 5 of 6 discriminating runs but ranks 6 of 6 by affected-student count in UNICEF's heatwave-major ADB subset.",
    chartTitle: "Three validity gates",
    sourceNote: "UNICEF 2024 climate-related school-disruption annex, WDI enrollment, and the inherited WDI/CCKP proxy panel.",
    caveat:
      "The heatwave subset has six selected rows; affected counts mix observations and enrollment-based estimates and do not measure days or learning loss.",
    nextStep:
      "Build a school-day or district-day panel joining local heat, calendars, enrollment, school conditions, and closure, attendance, assessment, or learning.",
    granularity: {
      currentUnit: "Six heatwave-major country rows with national proxy inputs and 2024 affected-student counts",
      targetUnit: "School-day or district-day heat exposure and educational outcome",
      gap:
        "Country counts do not align event timing, calendars, local or indoor heat, adaptation, duration, attendance, or learning.",
      upgradeData:
        "School geocodes, daily humid heat, calendars, enrollment, cooling/building conditions, closures, attendance, and assessments.",
    },
  },
  "social-protection-shock-coverage": {
    slug: "social-protection-shock-coverage",
    articleSlug: "sp-shock-readiness-cluster",
    domain: "Social protection",
    finish: "publication-ready",
    question:
      "Does the inherited shock-payment screen preserve its own ranking rule and align with an observed response object?",
    output:
      "No. Only three named members survive the panel's own value order, while zero comparable delivery outcomes are joined.",
    chartTitle: "Three-gate construct validation",
    sourceNote: "WDI poverty, ASPIRE coverage, Findex account ownership, and the World Bank COVID-19 response matrix.",
    caveat:
      "Response-category presence is not successful receipt, delivery speed, payment failure, or shock-trigger latency.",
    nextStep:
      "Start from event-level eligibility, actual receipt, failed payments, timestamps, channel, geography, and shock trigger.",
    granularity: {
      currentUnit: "Country-level poverty, ASPIRE social-protection coverage, and Findex account ownership",
      targetUnit: "Province/district, payment point catchment, beneficiary group, shock-affected municipality",
      gap:
        "The national proxy stack changes membership under missing-data and coverage rules; delivery outcomes are absent.",
      upgradeData:
        "Shock-program registries, eligibility denominators, payment transactions and failures, timestamps, grievance records, delivery channels, and shock footprints.",
    },
  },
  "water-stress-crop-diversification": {
    slug: "water-stress-crop-diversification",
    articleSlug: "water-crop-pressure-cluster",
    domain: "Environment",
    finish: "construct-validation",
    question:
      "Does the inherited four-country screen survive direct measures of available-water stress and harvested-area crop concentration?",
    output:
      "No. The published set is the raw top four in 2 of 7 runs; direct water retains 2 of 4 members and direct crop concentration 0 of 4.",
    chartTitle: "Three construct gates",
    sourceNote: "WDI/AQUASTAT SDG 6.4.2 and FAOSTAT 2024 Area harvested, with the inherited WDI screen retained for audit.",
    caveat:
      "The 30-row national join excludes all five crop-HHI leaders and contains no basin, irrigation, crop-water-demand, or outcome layer.",
    nextStep:
      "Build one basin × crop × irrigation × year pilot with an observed depletion or production outcome.",
    granularity: {
      currentUnit: "Thirty aligned national water-stress, crop-HHI, and rural-share rows",
      targetUnit: "Basin × crop × irrigation × year, linked to farms or people",
      gap:
        "Country averages cannot align transboundary allocation, seasonal water demand, crop location, irrigation status, and exposure.",
      upgradeData:
        "Basin withdrawal/depletion and allocation, SPAM or equivalent crop areas, irrigation masks, crop-water coefficients, weather, and gridded exposure.",
    },
  },
};
