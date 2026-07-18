export type FinishGroup =
  | "publication-ready"
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
    finish: "screening-result",
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
    domain: "Connectivity",
    finish: "prepared-pipeline",
    question:
      "Do measured fixed and mobile speeds reveal a digital-performance gap that headline subscription indicators miss?",
    output:
      "Ookla Q1 2026 manifest and DuckDB SQL are committed for Philippines and Bangladesh pilots; no parquet aggregation has been run.",
    chartTitle: "Chart pending: Ookla parquet aggregation",
    sourceNote: "Ookla Open Data manifest; SQL prepared for large parquet files.",
    caveat:
      "No speed, latency, or coverage claim should appear until the parquet files are downloaded and aggregated.",
    nextStep:
      "Fetch the mobile and fixed parquet files, run DuckDB aggregation, and publish fixed/mobile median-speed charts.",
    granularity: {
      currentUnit: "Prepared PHL/BGD Ookla manifest; no aggregated tile result yet",
      targetUnit: "Ookla fixed/mobile tile, city, municipality, school/clinic catchment",
      gap:
        "Parquet aggregation has not run, so no speed, latency, or measurement-density surface exists.",
      upgradeData:
        "Ookla fixed/mobile parquet, ITU/WDI ICT indicators, WorldPop/GHSL, admin boundaries, and service POIs.",
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
      "Which DMCs combine high outdoor-labor exposure with above-guideline PM2.5 pressure?",
    output:
      "Afghanistan, India, and Bangladesh are stable across the pressure-index sensitivity suite.",
    chartTitle: "Workday-loss pressure index",
    sourceNote: "WDI employment structure and PM2.5 exposure; WHO guideline used for excess exposure framing.",
    caveat:
      "This version is PM2.5-only; heat exposure is not yet integrated into the headline.",
    nextStep:
      "Add heat-work-hour loss using climate grids and occupational heat-stress functions.",
    granularity: {
      currentUnit: "Country-level WDI outdoor labor share and PM2.5 exposure",
      targetUnit: "District/grid cell, occupational group, heat-exposure zone",
      gap:
        "PM2.5 is currently a country mean; heat-work-hour loss and subnational labor exposure are not integrated.",
      upgradeData:
        "PM2.5 grids, ERA5/CMIP heat, labor-force shares, WorldPop, and occupation/sector data.",
    },
  },
  "coastal-informal-risk": {
    slug: "coastal-informal-risk",
    articleSlug: "coastal-informal-cluster",
    domain: "Built form",
    finish: "screening-result",
    question:
      "Which coastal DMCs combine large urban populations with measured or imputed informal-settlement pressure?",
    output:
      "Pakistan, Philippines, China, Bangladesh, and Myanmar hold the top urban-informal-pressure positions.",
    chartTitle: "Coastal informal-pressure index",
    sourceNote: "WDI urban share, population, and slum prevalence where available.",
    caveat:
      "WDI slum data are sparse, and coastal exposure is binary rather than low-elevation coastal-zone exposure.",
    nextStep:
      "Replace the binary coastal flag with LECZ population and settlement-footprint layers.",
    granularity: {
      currentUnit: "Country-level coastal flag with urban population and sparse slum prevalence",
      targetUnit: "Low-elevation coastal-zone grid, settlement footprint, barangay/municipality",
      gap:
        "Coastal exposure is binary and WDI slum data are sparse or imputed.",
      upgradeData:
        "LECZ population, GHSL/WorldPop, building footprints, national slum or informal-settlement layers, and flood/coastal hazard surfaces.",
    },
  },
  "disaster-recovery-lag": {
    slug: "disaster-recovery-lag",
    articleSlug: "disaster-burden-cluster",
    domain: "Disaster",
    finish: "publication-ready",
    question:
      "Which economies remain at the top of disaster burden across alternative burden metrics?",
    output:
      "China and India remain the top two across events per year, total affected, and damage-adjusted views.",
    chartTitle: "Disaster events per year",
    sourceNote: "EM-DAT country profiles, 2000-2025 burden layer.",
    caveat:
      "This is disaster burden, not recovery lag; recovery curves require event-timestamped indicator data.",
    nextStep:
      "Estimate post-event recovery curves using night lights, economic indicators, or service restoration data.",
    granularity: {
      currentUnit: "Country-level EM-DAT burden, 2000-2025",
      targetUnit: "Event footprint, affected municipality, nightlight grid, service-restoration area",
      gap:
        "Current result is disaster burden, not recovery lag; event geographies and recovery trajectories are missing.",
      upgradeData:
        "GDIS/geocoded EM-DAT, VIIRS/Black Marble nightlights, admin boundaries, and service/economic time series.",
    },
  },
  "flood-market-access": {
    slug: "flood-market-access",
    articleSlug: "flood-market-access-cluster",
    domain: "Access",
    finish: "screening-result",
    question:
      "Which rural populations are most exposed to recurrent flood events in the current public-data proxy?",
    output:
      "India, China, Indonesia, and Afghanistan hold the stable top-4 flood-rural-exposure set.",
    chartTitle: "Flood-rural exposure index",
    sourceNote: "EM-DAT flood subset, WDI rural share, and WDI population.",
    caveat:
      "The current measure is not road-network disruption or market isolation.",
    nextStep:
      "Join modeled flood extent to road networks, market locations, and service catchments.",
    granularity: {
      currentUnit: "Country-level flood events by rural population proxy",
      targetUnit: "Flooded road segment, market catchment, settlement/village, municipality",
      gap:
        "No road-network disruption, market isolation, or flood-extent join exists yet.",
      upgradeData:
        "Global Flood Database or JRC water/flood layers, OSM/Overture/GRIP roads, market/service POIs, and WorldPop.",
    },
  },
  "food-price-climate-transmission": {
    slug: "food-price-climate-transmission",
    articleSlug: "food-price-joint-qualifier",
    domain: "Food",
    finish: "screening-result",
    question:
      "Which economies sit jointly high on CPI inflation and agriculture-import exposure after dropping the unstable composite?",
    output:
      "Lao PDR and Pakistan sit in the top-N of both rankings for every N from 3 to 10; Bangladesh joins from N=5.",
    chartTitle: "Food-price vulnerability screen",
    sourceNote: "WDI CPI inflation, agriculture imports share, and food production index.",
    caveat:
      "This does not establish climate-to-price transmission; the annual macro data are too coarse.",
    nextStep:
      "Use sub-annual commodity prices and local climate anomalies to test transmission directly.",
    granularity: {
      currentUnit: "Country-year macro screen",
      targetUnit: "Market, commodity, month, local climate anomaly",
      gap:
        "Annual macro data cannot establish climate-to-price transmission.",
      upgradeData:
        "WFP/VAM or national market price series, FAO FPMA, CHIRPS rainfall, ERA5 heat, and commodity calendars.",
    },
  },
  "grid-reliability-heat": {
    slug: "grid-reliability-heat",
    articleSlug: "single-fuel-grid-cluster",
    domain: "Energy",
    finish: "publication-ready",
    question:
      "Which power systems show strong single-fuel concentration before adding the heat-reliability layer?",
    output:
      "Brunei, Bhutan, Mongolia, Nepal, and Tajikistan exceed 80% dependence on a single fuel category.",
    chartTitle: "Fuel-mix Herfindahl concentration",
    sourceNote: "WRI Global Power Plant Database and WDI electricity access.",
    caveat:
      "Fuel concentration is structural exposure, not heat-related outage risk.",
    nextStep:
      "Add ERA5 heat anomalies and outage or reliability data where public records exist.",
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
      "Which DMCs combine large emigrant stocks with concentrated destination corridors?",
    output:
      "India, China, Bangladesh, Afghanistan, and the Philippines remain the top emigrant-stock group.",
    chartTitle: "Emigrant stock, 2024",
    sourceNote: "UN DESA International Migrant Stock 2024.",
    caveat:
      "Migrant stock is not a flow, and Afghanistan is a refugee-driven case that needs separate treatment.",
    nextStep:
      "Add corridor-level change over time and displacement-specific series from UNHCR or IDMC.",
    granularity: {
      currentUnit: "Country-level emigrant stock and destination concentration",
      targetUnit: "Origin province, bilateral corridor, displacement location, destination cluster",
      gap:
        "Stock data are not flows and do not identify subnational origin or displacement mechanism.",
      upgradeData:
        "UN DESA bilateral stock, UNHCR/IDMC/IOM displacement series, census or microdata origin fields, and corridor histories.",
    },
  },
  "port-hinterland-friction": {
    slug: "port-hinterland-friction",
    articleSlug: "port-friction-trade-volume-cluster",
    domain: "Trade",
    finish: "publication-ready",
    question:
      "Which economies combine large import exposure with logistics-performance friction?",
    output:
      "China, India, Indonesia, Thailand, and Viet Nam hold the top friction-exposure set.",
    chartTitle: "Port-hinterland friction exposure",
    sourceNote: "World Bank Logistics Performance Index and WDI import values.",
    caveat:
      "LPI is perception-based, and landlocked economies have a different mechanism.",
    nextStep:
      "Split coastal and landlocked mechanisms and add port, road, and inland-node data.",
    granularity: {
      currentUnit: "Country-level imports and LPI friction",
      targetUnit: "Port, inland node, corridor, road/rail segment, province",
      gap:
        "LPI is national and perception-based; inland logistics paths are not represented.",
      upgradeData:
        "Port locations/calls, AIS or port statistics, OSM/Overture roads and rail, customs/corridor time data, and inland city nodes.",
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
    finish: "screening-result",
    question:
      "Which education systems show the strongest simple pressure signal from children, pupil-teacher ratio, and heat?",
    output:
      "Only Cambodia is parameter-stable at the top; the top-5 changes under sensitivity testing.",
    chartTitle: "School-heat pressure index",
    sourceNote: "WDI school-age share, primary pupil-teacher ratio, and CCKP historical tasmax.",
    caveat:
      "The linear heat ramp is too simple for a policy-grade learning-loss estimate.",
    nextStep:
      "Use classroom-temperature or heat-learning functions and future-period climate scenarios.",
    granularity: {
      currentUnit: "Country-level children, pupil-teacher ratio, and historical tasmax",
      targetUnit: "School, district, municipality, classroom heat-exposure zone",
      gap:
        "Linear heat ramp is too simple and school locations/enrollment are not joined.",
      upgradeData:
        "School geocodes, district enrollment, ERA5/CMIP heat, classroom/learning heat-response functions, and UNICEF/UIS data.",
    },
  },
  "social-protection-shock-coverage": {
    slug: "social-protection-shock-coverage",
    articleSlug: "sp-shock-readiness-cluster",
    domain: "Social protection",
    finish: "publication-ready",
    question:
      "Which DMCs combine poverty exposure, low social-protection coverage, and weak digital-payment reach?",
    output:
      "Bangladesh, Lao PDR, Myanmar, Pakistan, and the Philippines hold the stable readiness-gap set.",
    chartTitle: "Shock-payment readiness gap",
    sourceNote: "WDI poverty, ASPIRE social-protection coverage, and Global Findex account ownership.",
    caveat:
      "Coverage is not adequacy, and account ownership is not payment success.",
    nextStep:
      "Add benefit adequacy, delivery speed, and post-shock administrative coverage where public data exist.",
    granularity: {
      currentUnit: "Country-level poverty, ASPIRE social-protection coverage, and Findex account ownership",
      targetUnit: "Province/district, payment point catchment, beneficiary group, shock-affected municipality",
      gap:
        "Coverage is national and not shock-specific; delivery speed and adequacy are missing.",
      upgradeData:
        "Administrative social-protection coverage by area, payment-agent/mobile-money locations, LSMS/DHS/MICS, disaster shock footprints, and benefit adequacy data.",
    },
  },
  "water-stress-crop-diversification": {
    slug: "water-stress-crop-diversification",
    articleSlug: "water-crop-pressure-cluster",
    domain: "Environment",
    finish: "screening-result",
    question:
      "Which rural economies combine high freshwater withdrawal pressure with crop-system exposure?",
    output:
      "Afghanistan, Azerbaijan, Pakistan, and Turkmenistan form a stable top-4 narrowing; top-5 is sensitive.",
    chartTitle: "Water-crop pressure index",
    sourceNote: "WDI freshwater withdrawal, cereal yield, and rural share.",
    caveat:
      "Turkmenistan's withdrawal ratio reflects transboundary-water dependence; it is not comparable to purely internal-resource stress.",
    nextStep:
      "Add AQUASTAT basin data, crop calendars, and commodity-specific diversification measures.",
    granularity: {
      currentUnit: "Country-level water withdrawal, cereal yield, and rural share",
      targetUnit: "River basin, irrigation command, crop zone, district",
      gap:
        "Country water-withdrawal ratios hide basin/transboundary mechanisms and crop calendars.",
      upgradeData:
        "AQUASTAT/basin water data, HydroBASINS/HydroRIVERS, crop calendars, irrigation maps, and commodity-specific yield data.",
    },
  },
};
