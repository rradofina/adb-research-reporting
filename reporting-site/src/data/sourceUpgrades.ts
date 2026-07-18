export type UpgradePriority = "P1" | "P2" | "P3" | "Watch";

export interface SourceLink {
  label: string;
  href: string;
}

export interface SourceUpgrade {
  slug: string;
  betterSource: string;
  betterUnit: string;
  priority: UpgradePriority;
  rationale: string;
  sourceLinks: SourceLink[];
}

export const PRIORITY_META: Record<
  UpgradePriority,
  { label: string; short: string; tone: "crimson" | "ochre" | "sage" | "default"; weight: number }
> = {
  P1: {
    label: "P1 - claim-changing",
    short: "Must add before strong subnational claim",
    tone: "crimson",
    weight: 1,
  },
  P2: {
    label: "P2 - high-value",
    short: "Major improvement, not always gating",
    tone: "ochre",
    weight: 2,
  },
  P3: {
    label: "P3 - validation",
    short: "Useful triangulation or robustness layer",
    tone: "sage",
    weight: 3,
  },
  Watch: {
    label: "Watch",
    short: "Track for later releases",
    tone: "default",
    weight: 4,
  },
};

export const SOURCE_UPGRADES: SourceUpgrade[] = [
  {
    slug: "mpi-nighttime-lights",
    betterSource:
      "OPHI/UNDP 2025 Global MPI subnational tables; World Bank SPID; Global Data Lab SHDI; NASA Black Marble or VIIRS DNB; Google Open Buildings 2.5D Temporal; AlphaEarth Satellite Embeddings.",
    betterUnit:
      "Subnational poverty region joined to 500 m or 1 km nighttime-light, building-growth, population-grid, and 10 m embedding-change layers.",
    priority: "P1",
    rationale:
      "This is the poverty anchor. It should not stay at national MPI plus planned NTL; the research value is within-country deprivation versus economic-light exposure.",
    sourceLinks: [
      { label: "UNDP 2025 MPI", href: "https://hdr.undp.org/content/2025-global-multidimensional-poverty-index-mpi" },
      { label: "World Bank SPID", href: "https://datacatalog.worldbank.org/search/dataset/0064796/subnational-poverty-and-inequality-database-spid" },
      { label: "Global Data Lab SHDI", href: "https://globaldatalab.org/shdi/archive/" },
      { label: "Google Open Buildings 2.5D Temporal", href: "https://sites.research.google/gr/open-buildings/temporal/" },
      { label: "AlphaEarth / Satellite Embedding V1", href: "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL" },
    ],
  },
  {
    slug: "access-services",
    betterSource:
      "MAP friction surface; Geofabrik/Overture roads; Google Open Buildings settlement denominators; health, school, and market facility registries; WorldPop 100 m population.",
    betterUnit:
      "Settlement-to-facility travel time, facility catchment, municipality, and road-access corridor.",
    priority: "P1",
    rationale:
      "Facility counts are a useful screen, but travel-time access is the policy-grade measure ADB readers will expect.",
    sourceLinks: [
      { label: "WorldPop", href: "https://www.worldpop.org/datacatalog/" },
      { label: "Overture transportation", href: "https://overturemaps.org/announcements/2024/overture-general-availability-of-transportation-dataset/" },
      { label: "Google Open Buildings V3", href: "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons" },
    ],
  },
  {
    slug: "digital-performance",
    betterSource:
      "Ookla fixed/mobile parquet; M-Lab NDT; ITU ICT indicators; WorldPop and GHSL denominators.",
    betterUnit:
      "Ookla tile, mobile/fixed access cell, city, municipality, school or clinic catchment.",
    priority: "P2",
    rationale:
      "The code path exists but the parquet aggregation has not run. Once run, this becomes a strong granular infrastructure-performance story.",
    sourceLinks: [
      { label: "Ookla Open Data", href: "https://registry.opendata.aws/speedtest-global-performance/" },
      { label: "M-Lab", href: "https://www.measurementlab.net/data/" },
    ],
  },
  {
    slug: "air-monitoring",
    betterSource:
      "ACAG satellite-derived PM2.5; OpenAQ station histories; Sentinel-5P NO2; WHO AAQ; WorldPop exposure denominators.",
    betterUnit:
      "1 km population exposure grid, city, industrial corridor, and monitor catchment.",
    priority: "P1",
    rationale:
      "A country-level PM2.5 mean cannot show who is exposed or whether monitors cover the exposed population.",
    sourceLinks: [
      { label: "ACAG PM2.5 archive", href: "https://sites.wustl.edu/acag/satellites/surface-pm2-5-archive/" },
      { label: "OpenAQ", href: "https://docs.openaq.org/" },
    ],
  },
  {
    slug: "invisible-urbanization",
    betterSource:
      "GHSL 2023 built-up and settlement layers; Google Open Buildings 2.5D Temporal; Dynamic World land cover; AlphaEarth Satellite Embeddings.",
    betterUnit:
      "Settlement grid, city edge, municipality, built-up expansion cluster, and building-footprint time slice.",
    priority: "P1",
    rationale:
      "The current WDI proxy is interesting but not enough; the claim becomes serious when built-up expansion is measured directly.",
    sourceLinks: [
      { label: "GHSL Data Package 2023", href: "https://human-settlement.emergency.copernicus.eu/documents/GHSL_Data_Package_2023.pdf" },
      { label: "Google Open Buildings", href: "https://sites.research.google/open-buildings/" },
      { label: "Open Buildings 2.5D Temporal", href: "https://sites.research.google/gr/open-buildings/temporal/" },
      { label: "AlphaEarth / Satellite Embedding V1", href: "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL" },
    ],
  },
  {
    slug: "climate-health-workdays",
    betterSource:
      "ERA5-Land or CMIP6 heat; ACAG PM2.5; ILOSTAT or labor-force microdata; WorldPop working-age denominators.",
    betterUnit:
      "Grid cell, district, occupational group, outdoor worksite, and heat-exposure zone.",
    priority: "P1",
    rationale:
      "The current screen measures PM2.5 pressure, but the title promises heat-workday loss; heat has to enter before the stronger claim.",
    sourceLinks: [
      { label: "ERA5-Land", href: "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land" },
      { label: "ILOSTAT", href: "https://ilostat.ilo.org/data/" },
    ],
  },
  {
    slug: "coastal-informal-risk",
    betterSource:
      "Low-elevation coastal-zone population; GHSL and WorldPop; Google Open Buildings 2.5D Temporal; AlphaEarth/Dynamic World built-up change; national slum or informal-settlement layers; flood and coastal hazard surfaces.",
    betterUnit:
      "Low-elevation coastal-zone grid, settlement footprint, barangay, municipality, and flood-prone neighborhood.",
    priority: "P2",
    rationale:
      "The current coastal flag and sparse slum data are too blunt; settlement footprints would make the exposure spatially legible.",
    sourceLinks: [
      { label: "GHSL", href: "https://ghsl.jrc.ec.europa.eu/" },
      { label: "WorldPop", href: "https://www.worldpop.org/datacatalog/" },
      { label: "Google Open Buildings 2.5D Temporal", href: "https://sites.research.google/gr/open-buildings/temporal/" },
    ],
  },
  {
    slug: "disaster-recovery-lag",
    betterSource:
      "GDIS geocoded disasters; EM-DAT event metadata; Google Groundsource flood events for urban flash floods; VIIRS or Black Marble nightlights; Google Open Buildings 2.5D Temporal; GDACS; service restoration and economic time series.",
    betterUnit:
      "Event footprint, affected municipality, nighttime-light grid, and restoration catchment.",
    priority: "P1",
    rationale:
      "The current result is disaster burden, not recovery lag. Event footprints plus post-event trajectories are needed for the actual claim.",
    sourceLinks: [
      { label: "GDIS", href: "https://sedac.ciesin.columbia.edu/data/set/pend-gdis-1960-2018" },
      { label: "GDACS", href: "https://www.gdacs.org/" },
      { label: "Google Groundsource flood events", href: "https://doi.org/10.5281/zenodo.18647054" },
    ],
  },
  {
    slug: "flood-market-access",
    betterSource:
      "Google Groundsource flood events; Google Flood Forecasting API/GRRR where approved; Global Flood Database or JRC Global Surface Water; Overture/Geofabrik roads; markets and service POIs; WorldPop and Google Open Buildings settlement grids.",
    betterUnit:
      "Flooded road segment, settlement, market catchment, municipality, and facility catchment.",
    priority: "P1",
    rationale:
      "The current flood-rural proxy is country-level. The real ADB-relevant story is which road segments and markets become unreachable.",
    sourceLinks: [
      { label: "Global Flood Database", href: "https://global-flood-database.cloudtostreet.ai/" },
      { label: "JRC Global Surface Water", href: "https://global-surface-water.appspot.com/" },
      { label: "Google Groundsource flood events", href: "https://doi.org/10.5281/zenodo.18647054" },
      { label: "Google Flood Forecasting API", href: "https://developers.google.com/flood-forecasting" },
    ],
  },
  {
    slug: "food-price-climate-transmission",
    betterSource:
      "FAO FPMA; WFP VAM market prices; FEWS NET Data Center; CHIRPS rainfall; ERA5 heat; commodity calendars.",
    betterUnit:
      "Market, commodity, month, livelihood zone, and local climate anomaly.",
    priority: "P1",
    rationale:
      "Climate-to-price transmission cannot be tested with annual macro indicators. Market-month price series are the minimum serious unit.",
    sourceLinks: [
      { label: "FAO FPMA", href: "https://www.fao.org/giews/food-prices/price-tool/en/" },
      { label: "FEWS NET Data Center", href: "https://fews.net/data" },
      { label: "WFP market analysis", href: "https://www.wfp.org/market-analysis" },
    ],
  },
  {
    slug: "grid-reliability-heat",
    betterSource:
      "Global Energy Monitor power trackers; WRI plant data as baseline; GridFinder/OpenInfraMap; ERA5 heat; public outage or load-shedding records.",
    betterUnit:
      "Plant, substation, feeder or service area, city, and heat-stressed demand zone.",
    priority: "P2",
    rationale:
      "Fuel concentration is defensible, but reliability under heat requires current assets and observed outage or load stress.",
    sourceLinks: [
      { label: "Global Energy Monitor", href: "https://globalenergymonitor.org/projects/global-integrated-power-tracker/download-data/" },
      { label: "WRI power plants", href: "https://github.com/wri/global-power-plant-database" },
    ],
  },
  {
    slug: "migration-displacement-signals",
    betterSource:
      "UN DESA bilateral stock; IDMC GIDD and IDU APIs; IOM DTM; IPUMS, DHS, or census origin fields where available.",
    betterUnit:
      "Origin province, bilateral corridor, displacement event/location, destination cluster, and household origin group.",
    priority: "P2",
    rationale:
      "The emigrant-stock result is credible, but displacement and origin granularity would make it much more policy-relevant.",
    sourceLinks: [
      { label: "IDMC API", href: "https://www.internal-displacement.org/database/api-documentation/" },
      { label: "IOM DTM", href: "https://dtm.iom.int/" },
    ],
  },
  {
    slug: "port-hinterland-friction",
    betterSource:
      "UNCTAD port liner shipping connectivity index; AIS or PortWatch-style port calls; Overture roads and rail; customs and corridor-time data.",
    betterUnit:
      "Port, inland node, corridor, road/rail segment, province, and chokepoint exposure route.",
    priority: "P2",
    rationale:
      "LPI is perception-based and national. Port- and corridor-level data would turn this from a macro friction screen into a logistics measurement paper.",
    sourceLinks: [
      { label: "UNCTAD maritime data", href: "https://unctadstat.unctad.org/insights/theme/45" },
      { label: "Overture transportation", href: "https://overturemaps.org/announcements/2024/overture-general-availability-of-transportation-dataset/" },
    ],
  },
  {
    slug: "public-service-data-quality",
    betterSource:
      "Geocoded national registries; WHO GHFD; healthsites.io and dated OSM extracts; fuzzy name/address matching; ADM2 boundaries.",
    betterUnit:
      "Facility record, duplicate cluster, ADM2/province/district, and facility catchment.",
    priority: "P1",
    rationale:
      "This is already a flagship. Facility-level matching and ADM2 geography would make it difficult to dismiss as a count comparison.",
    sourceLinks: [
      { label: "WHO GHFD", href: "https://www.who.int/data/gho/data/themes/topics/geo-located-health-facilities-data" },
      { label: "healthsites.io", href: "https://healthsites.io/" },
    ],
  },
  {
    slug: "remittance-resilience",
    betterSource:
      "World Bank bilateral remittance matrix; RPW microdata; central-bank corridor flows; LSMS, DHS, or national household surveys.",
    betterUnit:
      "Bilateral corridor, remittance-receiving household group, origin/destination region, and service provider route.",
    priority: "P2",
    rationale:
      "The current result is strong as a screen. Flow-weighted corridors and household concentration would make it a much stronger resilience paper.",
    sourceLinks: [
      { label: "RPW", href: "https://remittanceprices.worldbank.org/data-download" },
      { label: "World Bank microdata", href: "https://microdata.worldbank.org/" },
    ],
  },
  {
    slug: "school-heat-disruption",
    betterSource:
      "National EMIS school geocodes; UIS/UNICEF education data; ERA5 or CMIP6 heat; Dynamic World land cover; Google Open Buildings built-up context; classroom or learning heat-response functions.",
    betterUnit:
      "School, district, municipality, classroom heat-exposure zone, and affected student group.",
    priority: "P2",
    rationale:
      "The current screen is honest but too simple. School geocodes and a real heat-learning function are needed for policy-grade disruption estimates.",
    sourceLinks: [
      { label: "UNESCO UIS", href: "https://uis.unesco.org/" },
      { label: "UNICEF MICS", href: "https://mics.unicef.org/" },
      { label: "Dynamic World", href: "https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1" },
    ],
  },
  {
    slug: "social-protection-shock-coverage",
    betterSource:
      "ASPIRE disaggregations; World Bank G2Px; administrative beneficiary coverage; payment-agent or mobile-money locations; disaster shock footprints.",
    betterUnit:
      "Province/district, beneficiary group, payment-point catchment, shock-affected municipality, and delivery-time window.",
    priority: "P2",
    rationale:
      "The current country-level readiness gap is useful. Delivery speed, adequacy, and payment geography are what make it shock-responsive.",
    sourceLinks: [
      { label: "ASPIRE", href: "https://www.worldbank.org/en/data/datatopics/aspire" },
      { label: "G2Px", href: "https://www.worldbank.org/en/programs/g2px" },
    ],
  },
  {
    slug: "water-stress-crop-diversification",
    betterSource:
      "HydroBASINS/HydroSHEDS; AQUASTAT basin data; SPAM crop allocation; GAEZ; crop calendars; irrigation command maps.",
    betterUnit:
      "River basin, irrigation command, crop zone, district, and transboundary dependency corridor.",
    priority: "P2",
    rationale:
      "The current country screen is useful but hides basin mechanics. Basin and crop-zone data would make the Turkmenistan/Pakistan mechanism clearer.",
    sourceLinks: [
      { label: "HydroSHEDS", href: "https://www.hydrosheds.org/" },
      { label: "MapSPAM", href: "https://www.mapspam.info/" },
      { label: "FAO AQUASTAT", href: "https://www.fao.org/aquastat/" },
    ],
  },
];

export const ROAD_QUALITY_UPGRADE: SourceUpgrade = {
  slug: "road-quality-poverty-access",
  betterSource:
    "ADB road-quality ML workflow; Mapillary paved/unpaved surface predictions; Overture/Geofabrik roads; Google Open Buildings settlement growth; Google Groundsource flood-event history; IRI or smartphone roughness validation; WorldPop/GHSL; poverty and facility layers.",
  betterUnit:
    "Road segment, settlement, municipality, clinic/school/market catchment, and poverty-exposed corridor.",
  priority: "P2",
  rationale:
    "Road quality is not part of the current issue count, but it is a strong next-track candidate because it connects AI road-condition monitoring with poverty access.",
  sourceLinks: [
    { label: "ADB road-quality ML paper", href: "https://www.adb.org/publications/machine-learning-satellite-imagery-road-quality-monitoring" },
    { label: "ADB 2025 guidebook", href: "https://policycommons.net/artifacts/20142856/guidebook-on-machine-learning-techniques-for-road-quality-monitoring/21043381/" },
    { label: "Mapillary road surface dataset", href: "https://arxiv.org/abs/2410.19874" },
    { label: "Google Open Buildings 2.5D Temporal", href: "https://sites.research.google/gr/open-buildings/temporal/" },
    { label: "Google Groundsource flood events", href: "https://doi.org/10.5281/zenodo.18647054" },
  ],
};
