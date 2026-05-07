export type SourceItem = {
  name: string;
  owner: string;
  years: string;
  coverage: string;
  access: string;
  use: string;
  caveat: string;
  url: string;
};

export type MetricItem = {
  name: string;
  definition: string;
  output: string;
};

export type ResearchProgram = {
  slug: string;
  number: string;
  title: string;
  shortTitle: string;
  kicker: string;
  hypothesis: string;
  oneLine: string;
  whyNow: string;
  wowFactor: string;
  adbFit: string;
  accent: string;
  status: string;
  coverage: string;
  href: string;
  questions: string[];
  literatureGap: string[];
  dataAvailability: { label: string; value: string }[];
  sourceStack: SourceItem[];
  methodSteps: string[];
  metrics: MetricItem[];
  pilotEconomies: string[];
  implementation: string[];
  caveats: string[];
};

export const researchPrograms: ResearchProgram[] = [
  {
    slug: "access-services",
    number: "01",
    title: "Climate-Adjusted Access to Services",
    shortTitle: "Access Under Climate Stress",
    kicker: "Roads, clinics, schools, markets, floods, heat",
    hypothesis:
      "A household can be near a service on paper and still be effectively cut off once travel time, monsoon flooding, heat exposure, road quality, and facility density are included.",
    oneLine:
      "Measure the population whose access to clinics, schools, markets, and city services collapses under plausible climate stress.",
    whyNow:
      "ADB operations increasingly need climate-resilient service delivery metrics, but official access measures usually count distance or facility presence, not whether people can realistically reach services during bad weather.",
    wowFactor:
      "A country map that switches from normal travel time to flood-season or heat-stress travel time, showing villages and peri-urban edges that disappear from the service network.",
    adbFit:
      "Directly relevant to transport, health, education, urban, climate adaptation, and social protection operations.",
    accent: "#22c55e",
    status: "Best flagship candidate",
    coverage:
      "Global population and climate layers; roads and POIs are broad but vary by OpenStreetMap/Overture completeness.",
    href: "/research/access-services",
    questions: [
      "How many people are within 30, 60, and 120 minutes of a clinic, school, market, or town center under normal conditions?",
      "How many lose access when flood-prone road segments or high-heat travel penalties are added?",
      "Which subnational regions have good official access indicators but poor climate-adjusted access?",
      "Do poor or low-SHDI regions experience larger access collapse than better-off regions?",
    ],
    literatureGap: [
      "Accessibility research exists, but many dashboards stop at static travel time to cities or facilities.",
      "Climate risk maps exist, but they are rarely joined to service catchments and population-weighted access loss.",
      "The useful contribution is not another road map. It is an operational measure of service failure under climate stress.",
    ],
    dataAvailability: [
      { label: "Population denominator", value: "WorldPop Global 2015-2030 plus official sources where available" },
      { label: "Current ADM1 spine", value: "geoBoundaries, PSA OpenSTAT, WorldPop stats API" },
      { label: "Baseline mobility", value: "MAP friction surface and OSM/Overture roads" },
      { label: "Climate stressors", value: "CHIRPS rainfall, ERA5-Land heat, Global Flood Database, JRC water" },
      { label: "Facilities", value: "OSM/Overture POIs plus HDX where country coverage is strong" },
    ],
    sourceStack: [
      {
        name: "geoBoundaries ADM1 boundaries",
        owner: "William & Mary geoLab",
        years: "Current API release",
        coverage: "Global administrative boundaries with country/admin metadata",
        access: "API and GeoJSON downloads",
        use: "Reproducible ADM1 reporting spine for pilot screening outputs.",
        caveat: "Boundary vintages differ by country and need review against official planning boundaries.",
        url: "https://www.geoboundaries.org/api.html",
      },
      {
        name: "PSA OpenSTAT regional population",
        owner: "Philippine Statistics Authority",
        years: "2020 Census of Population and Housing",
        coverage: "Philippines regions and provinces/HUCs",
        access: "PXWeb API",
        use: "Official Philippines ADM1 population denominator for the current screening layer.",
        caveat: "Philippines official census and WorldPop Bangladesh estimates are not a harmonized cross-country population product.",
        url: "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO/0021A6DPAG0.px",
      },
      {
        name: "WorldPop population counts",
        owner: "WorldPop, University of Southampton",
        years: "2015-2030",
        coverage: "Global, high-resolution gridded population products",
        access: "Hub downloads and API",
        use: "Population-weight all access and climate-loss metrics.",
        caveat: "Top-down gridded estimates need sensitivity checks in sparse rural areas.",
        url: "https://www.worldpop.org/datacatalog/",
      },
      {
        name: "MAP friction surface",
        owner: "Malaria Atlas Project",
        years: "2015 baseline",
        coverage: "Global land travel speed surface",
        access: "Google Earth Engine",
        use: "Create baseline least-cost travel time surfaces.",
        caveat: "Static 2015 surface; road networks and speeds need updating with OSM/Overture.",
        url: "https://developers.google.com/earth-engine/datasets/catalog/projects_malariaatlasproject_assets_accessibility_friction_surface_2015_v1_0",
      },
      {
        name: "CHIRPS precipitation",
        owner: "Climate Hazards Center, UC Santa Barbara",
        years: "1981 to near-present",
        coverage: "Quasi-global land, 60N to 60S",
        access: "GeoTIFF, NetCDF, COG, Google Earth Engine",
        use: "Estimate extreme rainfall days and monsoon disruption windows.",
        caveat: "Rainfall is not direct flood depth; combine with flood/water layers.",
        url: "https://www.chc.ucsb.edu/data/chirps3",
      },
      {
        name: "ERA5-Land",
        owner: "Copernicus Climate Data Store / ECMWF",
        years: "1950 to present",
        coverage: "Global, hourly, about 9 km land-surface fields",
        access: "CDS API, NetCDF, CSV time series",
        use: "Heat, precipitation, wind, and soil moisture stressors.",
        caveat: "Modelled reanalysis; local microclimate and urban heat islands require validation.",
        url: "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land-timeseries",
      },
      {
        name: "Global Flood Database",
        owner: "Cloud to Street / Dartmouth Flood Observatory",
        years: "2000-2018",
        coverage: "913 mapped flood events",
        access: "Google Earth Engine",
        use: "Historical flood exposure and road disruption priors.",
        caveat: "Only flood events that passed remote-sensing quality controls are mapped.",
        url: "https://developers.google.com/earth-engine/datasets/catalog/GLOBAL_FLOOD_DB_MODIS_EVENTS_V1",
      },
      {
        name: "JRC Global Surface Water",
        owner: "EC JRC / Google",
        years: "1984-2021",
        coverage: "Global surface water history",
        access: "Downloads, GEE, WMS",
        use: "Separate permanent water from flood water and identify seasonal crossings.",
        caveat: "Surface water history is not a direct road passability model.",
        url: "https://global-surface-water.appspot.com/download",
      },
      {
        name: "Overture transportation and places",
        owner: "Overture Maps Foundation",
        years: "Monthly releases",
        coverage: "Global open roads, places, buildings, admins",
        access: "Cloud-native GeoParquet on AWS/Azure",
        use: "Road graph, service POIs, and administrative joins.",
        caveat: "Licensing can vary by source; OSM-derived data may be ODbL.",
        url: "https://registry.opendata.aws/overture/",
      },
      {
        name: "Subnational Human Development Index",
        owner: "Global Data Lab",
        years: "Multi-year subnational series",
        coverage: "Subnational development indicators for many countries",
        access: "CSV/Excel after free registration",
        use: "Equity validation: do lower-SHDI regions lose more access?",
        caveat: "Not available for every ADB economy or every administrative unit.",
        url: "https://globaldatalab.org/shdi/",
      },
    ],
    methodSteps: [
      "Define ADB member economy boundaries and a common admin level for reporting.",
      "Extract population grids and service POIs for clinics, schools, markets, town centers, and transport nodes.",
      "Build a multimodal travel-time surface using MAP friction, OSM/Overture roads, slopes, waterways, and settlement barriers.",
      "Create climate-stress scenarios: flooded crossings removed, extreme rainfall speed penalties, and high-heat walking penalties.",
      "Compute population-weighted travel time under normal and stressed conditions.",
      "Rank places by access loss, not only baseline remoteness.",
    ],
    metrics: [
      {
        name: "Service Access Loss",
        definition:
          "Population share that moves from within a threshold to outside it under a climate-stress scenario.",
        output: "Percent of people losing 30/60/120 minute access.",
      },
      {
        name: "Climate-Fragile Catchment",
        definition:
          "A facility catchment where more than a chosen share of users are cut off by flood or heat penalties.",
        output: "Facility-level fragility score and affected population.",
      },
      {
        name: "Hidden Isolation",
        definition:
          "Population with acceptable straight-line distance but poor travel-time access.",
        output: "People counted as served by distance but not by realistic travel.",
      },
    ],
    pilotEconomies: [
      "Philippines",
      "Bangladesh",
      "Nepal",
      "Cambodia",
      "Lao PDR",
      "Pakistan",
      "Viet Nam",
      "Papua New Guinea",
    ],
    implementation: [
      "Use DuckDB + spatial extensions locally for vector joins and country/admin summaries.",
      "Use Earth Engine exports for raster aggregation: population, rainfall, flood history, water, heat.",
      "Store only summary tables and simplified vector tiles in Supabase or static GeoParquet; keep rasters out of the web app.",
      "Render a scenario toggle: normal access, flood-stress access, heat-stress access, and access loss.",
    ],
    caveats: [
      "Facility data quality is the largest risk; OSM/HDX completeness must be profiled by country.",
      "Road passability during floods is not directly observed everywhere; scenario rules must be explicit.",
      "Travel time is an access proxy, not a guarantee of affordability, capacity, or quality of service.",
    ],
  },
  {
    slug: "digital-performance",
    number: "02",
    title: "Measured Digital Development Gap",
    shortTitle: "Real Internet Performance",
    kicker: "Speed, latency, devices, population, official ICT indicators",
    hypothesis:
      "Official connectivity indicators often measure subscriptions or coverage. People can be counted as connected while the actual connection is too slow or unstable for school, work, telehealth, or business use.",
    oneLine:
      "Compare official internet access with measured download speed, upload speed, latency, device density, and unmeasured-population gaps.",
    whyNow:
      "AI, digital government, remote learning, telemedicine, and platform work all depend on quality, not just access. This lets ADB talk about usable connectivity.",
    wowFactor:
      "A map that shows countries with high official internet use but low measured performance outside capital regions, plus a separate map of areas where nobody is measuring speed at all.",
    adbFit:
      "Supports digital transformation, education, health, financial inclusion, e-commerce, and regional connectivity programs.",
    accent: "#38bdf8",
    status: "Cleanest data story",
    coverage:
      "Ookla has global quarterly tiles where tests exist. Official ICT indicators cover most economies, but tile measurement density varies sharply.",
    href: "/research/digital-performance",
    questions: [
      "Where do measured speeds contradict official internet-use or broadband-subscription indicators?",
      "What share of the population lives in tiles with too few tests to assess quality?",
      "Are schools, clinics, and small towns surrounded by slow or high-latency networks?",
      "Which regions have mobile performance good enough for telehealth, online learning, and cloud work?",
    ],
    literatureGap: [
      "Connectivity research often treats internet use, coverage, or subscriptions as the main outcome.",
      "Speed-test data has selection bias, but it reveals quality differences that subscriptions cannot see.",
      "The contribution is an ADB-region quality-adjusted digital access metric with explicit measurement uncertainty.",
    ],
    dataAvailability: [
      { label: "Measured performance", value: "Ookla fixed/mobile tiles, quarterly global releases" },
      { label: "Official baseline", value: "ITU ICT statistics and World Bank WDI internet indicators" },
      { label: "Population denominator", value: "WorldPop or GHSL population grids" },
      { label: "Service context", value: "Schools, clinics, markets, firms, and cities from OSM/Overture/HDX" },
    ],
    sourceStack: [
      {
        name: "Speedtest by Ookla Open Data",
        owner: "Ookla",
        years: "Quarterly releases",
        coverage: "Global tiles for fixed and mobile tests",
        access: "Public S3/GitHub documentation, shapefile and parquet downloads",
        use: "Download, upload, latency, tests, and devices by tile.",
        caveat: "Speed tests are user initiated and not a random sample of all users.",
        url: "https://github.com/teamookla/ookla-open-data",
      },
      {
        name: "ITU ICT Statistics",
        owner: "International Telecommunication Union",
        years: "2005-2025 regional series; country data through ITU DataHub",
        coverage: "Official ICT indicators for countries and regions",
        access: "DataHub and downloadable series",
        use: "Official internet use, broadband subscriptions, coverage, affordability comparison.",
        caveat: "Country-level indicators can hide subnational quality gaps.",
        url: "https://www.itu.int/en/itu-d/statistics/pages/stat/default.aspx",
      },
      {
        name: "World Bank WDI Internet Users",
        owner: "World Bank / ITU",
        years: "Long annual country series",
        coverage: "Most economies",
        access: "World Bank API and CSV",
        use: "Replicable baseline for official internet-user share.",
        caveat: "Measures use, not performance quality.",
        url: "https://data.worldbank.org/indicator/IT.NET.USER.ZS",
      },
      {
        name: "WorldPop population counts",
        owner: "WorldPop",
        years: "2015-2030",
        coverage: "Global gridded population",
        access: "Hub downloads and API",
        use: "Estimate population covered by measured-speed tiles.",
        caveat: "Population estimates have uncertainty at small-area scales.",
        url: "https://www.worldpop.org/datacatalog/",
      },
      {
        name: "Overture places and transportation",
        owner: "Overture Maps Foundation",
        years: "Monthly releases",
        coverage: "Global POIs, roads, buildings, admins",
        access: "GeoParquet on AWS/Azure",
        use: "Attach performance to schools, health facilities, firms, towns, and corridors.",
        caveat: "POI tagging completeness differs by country and urban/rural context.",
        url: "https://registry.opendata.aws/overture/",
      },
      {
        name: "ADB Data Library and Key Indicators",
        owner: "Asian Development Bank",
        years: "Varies by indicator",
        coverage: "ADB member economies",
        access: "ADB Data Library downloads/API where available",
        use: "Regional member economy metadata and ADB-relevant ICT/economic indicators.",
        caveat: "Indicator availability varies by economy and year.",
        url: "https://data.adb.org/",
      },
    ],
    methodSteps: [
      "Download fixed and mobile Ookla tiles for selected quarters and convert to GeoParquet.",
      "Intersect tiles with population grids and admin boundaries.",
      "Compute weighted median and lower-tail performance by population, not only by tile area.",
      "Create test-density and device-density layers to identify measurement deserts.",
      "Join official internet-use, broadband-subscription, and affordability indicators.",
      "Classify places into connected, low-quality, unmeasured, and high-performing categories.",
    ],
    metrics: [
      {
        name: "Usable Connectivity Share",
        definition:
          "Population in tiles meeting thresholds for download speed, upload speed, latency, and test density.",
        output: "Population share with usable mobile/fixed connectivity.",
      },
      {
        name: "Official-Performance Gap",
        definition:
          "Difference between official internet-use share and population-weighted measured usable connectivity.",
        output: "Gap score by country and subnational region.",
      },
      {
        name: "Measurement Desert",
        definition:
          "Population in tiles with too few tests or devices to support a quality estimate.",
        output: "People connected to the statistical dark zone.",
      },
    ],
    pilotEconomies: [
      "Philippines",
      "Indonesia",
      "India",
      "Bangladesh",
      "Nepal",
      "Pakistan",
      "Thailand",
      "Viet Nam",
      "Kazakhstan",
      "Georgia",
    ],
    implementation: [
      "Use quarterly parquet/shapefile tiles from Ookla and normalize fixed/mobile schemas.",
      "Use H3 or quadkey aggregation to keep client-side maps light.",
      "Store country/admin summaries plus optional vector tiles; avoid serving raw Ookla files through the app.",
      "Build a comparison panel: official internet use vs measured speed vs measurement coverage.",
    ],
    caveats: [
      "Ookla tests overrepresent people who run tests and places where the app is used.",
      "Low test density means the absence of evidence is itself a metric, not a value to impute casually.",
      "Mobile and fixed networks need separate interpretation.",
    ],
  },
  {
    slug: "air-monitoring",
    number: "03",
    title: "Air Pollution Without Air Monitors",
    shortTitle: "Pollution Data Deserts",
    kicker: "OpenAQ monitors, WHO city data, Sentinel-5P NO2, satellite PM2.5",
    hypothesis:
      "The places most exposed to pollution are not always the places with monitoring capacity. The blind spot is both environmental and statistical.",
    oneLine:
      "Map populations exposed to pollution where ground monitoring is sparse, absent, stale, or only available for large cities.",
    whyNow:
      "Clean-air policy depends on knowing where pollution is. Many ADB cities and peri-urban corridors have satellite-visible pollution but limited public monitoring.",
    wowFactor:
      "A map where pollution intensity and monitor visibility are separate layers, revealing exposed-but-unmeasured populations.",
    adbFit:
      "Highly relevant to urban health, transport, energy transition, industrial policy, livable cities, and SDG 11.6.2 monitoring.",
    accent: "#f43f5e",
    status: "Strong invisible-risk story",
    coverage:
      "Satellite layers are global or near-global; ground-monitor data is exactly the thing being measured as uneven.",
    href: "/research/air-monitoring",
    questions: [
      "Which ADB populations live in high PM2.5 or NO2 areas but far from any public ground monitor?",
      "Where are there ground monitors but no recent public data?",
      "Do official WHO city-average measurements miss peri-urban industrial and transport corridors?",
      "Can satellite pollution anomalies predict where monitoring expansion should be prioritized?",
    ],
    literatureGap: [
      "Air pollution exposure maps exist, and monitoring databases exist, but they are rarely turned into a monitor-equity index.",
      "Country or city rankings can obscure whether people have local, public, credible measurements.",
      "The contribution is a population-weighted air-quality observability metric for ADB economies.",
    ],
    dataAvailability: [
      { label: "Ground monitors", value: "OpenAQ API plus WHO Ambient Air Quality Database" },
      { label: "NO2 satellite layer", value: "Sentinel-5P TROPOMI via Earth Engine" },
      { label: "PM2.5 surface", value: "NASA SEDAC global annual PM2.5 grids" },
      { label: "Population denominator", value: "WorldPop/GHSL gridded population" },
    ],
    sourceStack: [
      {
        name: "OpenAQ API v3",
        owner: "OpenAQ",
        years: "Near-real-time and historical data where providers publish",
        coverage: "Global public ground-level air quality data",
        access: "REST API and open data on AWS",
        use: "Monitor locations, parameters, freshness, providers, and readings.",
        caveat: "OpenAQ only includes data it has discovered or received from public providers.",
        url: "https://docs.openaq.org/about/about",
      },
      {
        name: "WHO Ambient Air Quality Database",
        owner: "World Health Organization",
        years: "Updated every 2-3 years; 2024 V6.1 available",
        coverage: "7,182 settlements in more than 120 member states",
        access: "Excel and web app",
        use: "City annual PM2.5, PM10, and NO2 baseline and SDG 11.6.2 context.",
        caveat: "Not comprehensive; city averages are not station-level local exposure.",
        url: "https://www.who.int/data/gho/data/themes/air-pollution/who-air-Quality-database",
      },
      {
        name: "Sentinel-5P TROPOMI NO2",
        owner: "European Union / ESA / Copernicus",
        years: "2018 to present",
        coverage: "Near-global, near-real-time NO2",
        access: "Google Earth Engine",
        use: "Detect combustion, transport, and industrial NO2 patterns.",
        caveat: "Column NO2 is not the same as ground-level exposure; cloud screening and chemistry matter.",
        url: "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_NRTI_L3_NO2",
      },
      {
        name: "Global Annual PM2.5 Grids",
        owner: "NASA SEDAC / Dalhousie atmospheric composition group",
        years: "1998-2022",
        coverage: "Global annual PM2.5 grids",
        access: "GeoTIFF and NetCDF",
        use: "Population-weighted PM2.5 exposure at 0.01 degree.",
        caveat: "Large-scale estimates; local PM2.5 gradients are not fully resolved.",
        url: "https://data.nasa.gov/dataset/global-annual-pm2-5-grids-from-modis-misr-seawifs-and-viirs-aerosol-optical-depth-aod-1998",
      },
      {
        name: "WorldPop population counts",
        owner: "WorldPop",
        years: "2015-2030",
        coverage: "Global gridded population",
        access: "Hub downloads and API",
        use: "Estimate exposed people and monitor deserts.",
        caveat: "Small-area uncertainty must be reported.",
        url: "https://www.worldpop.org/datacatalog/",
      },
      {
        name: "Overture transportation and places",
        owner: "Overture Maps Foundation",
        years: "Monthly releases",
        coverage: "Global roads, places, admins",
        access: "GeoParquet on AWS/Azure",
        use: "Locate schools, hospitals, roads, industrial corridors, and settlement edges.",
        caveat: "Feature completeness varies by country.",
        url: "https://registry.opendata.aws/overture/",
      },
    ],
    methodSteps: [
      "Pull monitor metadata from OpenAQ and city annual observations from WHO.",
      "Create freshness and parameter coverage flags for PM2.5, PM10, NO2, O3, SO2, and CO.",
      "Aggregate satellite NO2 and annual PM2.5 to admin areas and population grids.",
      "Calculate distance from people and settlements to public monitors.",
      "Score each area by exposure, monitor distance, monitor freshness, and parameter coverage.",
      "Identify monitoring expansion candidates with high exposure and high population but weak public measurement.",
    ],
    metrics: [
      {
        name: "Exposed-Unmonitored Population",
        definition:
          "People above a pollution threshold who are beyond a defined distance from a recent public monitor.",
        output: "People and share by admin region.",
      },
      {
        name: "Monitor Freshness Score",
        definition:
          "Whether a monitor has recent observations for the pollutant of interest.",
        output: "Fresh, stale, missing, or unknown monitoring status.",
      },
      {
        name: "Pollution Observability Gap",
        definition:
          "Population-weighted pollution exposure multiplied by lack of monitor proximity and freshness.",
        output: "Priority score for monitoring investment.",
      },
    ],
    pilotEconomies: [
      "India",
      "Bangladesh",
      "Pakistan",
      "Philippines",
      "Indonesia",
      "Thailand",
      "Viet Nam",
      "Mongolia",
      "Kazakhstan",
      "Georgia",
    ],
    implementation: [
      "Use OpenAQ API for station metadata and latest observations; cache responses with timestamps.",
      "Use Earth Engine exports for monthly/annual NO2 and SEDAC PM2.5 rasters for annual exposure.",
      "Use nearest-neighbor and distance-to-monitor joins in DuckDB/PostGIS.",
      "Show two linked maps: exposure and observability, so a clean-looking area is not confused with an unmeasured area.",
    ],
    caveats: [
      "Satellite NO2 and PM2.5 estimates are exposure proxies, not direct regulatory measurements.",
      "OpenAQ coverage is not the full universe of air monitors.",
      "Monitor siting, instrument type, and operating agency affect comparability.",
    ],
  },
  {
    slug: "invisible-urbanization",
    number: "04",
    title: "Invisible Urbanization",
    shortTitle: "Building Growth Before Recognition",
    kicker: "Open Buildings, Overture, GHSL, Dynamic World, population grids",
    hypothesis:
      "Settlements often grow before official urban classifications, infrastructure budgets, and service networks catch up. Building-level change can reveal urbanization earlier than conventional indicators.",
    oneLine:
      "Use building growth, height, built-up probability, and population shifts to identify settlement expansion that is not yet visible in official urban systems.",
    whyNow:
      "New open building and land-cover datasets make it possible to track urban growth at a much finer resolution than country-level urbanization rates.",
    wowFactor:
      "A time-lapse showing buildings appearing from 2016 to 2023, then overlaying schools, clinics, roads, water, and flood risk to show where growth outruns services.",
    adbFit:
      "Relevant to urban planning, housing, water, sanitation, resilience, transport, climate risk, and informal settlement policy.",
    accent: "#a78bfa",
    status: "Most visual program",
    coverage:
      "Google temporal buildings cover South Asia and Southeast Asia well; GHSL, Dynamic World, Microsoft, and Overture provide broader global complements.",
    href: "/research/invisible-urbanization",
    questions: [
      "Where did built structures expand fastest from 2016 to 2023?",
      "Where does building growth precede official urban classification or population estimates?",
      "Are new settlements growing without roads, schools, clinics, water access, or flood-safe land?",
      "Which corridors are becoming urban before plans and budgets recognize them?",
    ],
    literatureGap: [
      "Urban growth studies often use built-up area or lights, but new building datasets allow more granular settlement morphology.",
      "Official urban classification can lag actual settlement change.",
      "The contribution is an operational early-warning system for service lag and unplanned expansion.",
    ],
    dataAvailability: [
      { label: "Temporal buildings", value: "Google Open Buildings 2.5D Temporal, 2016-2023, South/Southeast Asia" },
      { label: "Global buildings", value: "Microsoft Global ML Building Footprints and Overture Buildings" },
      { label: "Land cover", value: "Dynamic World 10m near-real-time built-up probabilities" },
      { label: "Historical settlement", value: "GHSL built-up/population/degree of urbanization series" },
    ],
    sourceStack: [
      {
        name: "Google Open Buildings 2.5D Temporal",
        owner: "Google Research",
        years: "2016-2023",
        coverage: "Africa, South Asia, South-East Asia, Latin America, Caribbean",
        access: "Google Earth Engine",
        use: "Annual building presence, fractional counts, and heights.",
        caveat: "Coverage excludes some ADB economies and is model-derived from Sentinel-2.",
        url: "https://sites.research.google/gr/open-buildings/temporal/",
      },
      {
        name: "Microsoft Global ML Building Footprints",
        owner: "Microsoft",
        years: "Current release snapshots",
        coverage: "Worldwide building footprints",
        access: "GeoJSONL downloads",
        use: "Global static footprint coverage where temporal Google coverage is missing.",
        caveat: "Quality varies by terrain, settlement type, and imagery conditions.",
        url: "https://github.com/microsoft/GlobalMLBuildingFootprints",
      },
      {
        name: "Overture buildings, places, transportation, admins",
        owner: "Overture Maps Foundation",
        years: "Monthly releases",
        coverage: "Global open map layers",
        access: "GeoParquet on AWS/Azure",
        use: "Latest open map spine for buildings, roads, POIs, and admin joins.",
        caveat: "License can vary by source; OSM-derived data may be ODbL.",
        url: "https://registry.opendata.aws/overture/",
      },
      {
        name: "Dynamic World",
        owner: "Google / World Resources Institute",
        years: "Sentinel-2 history and near-real-time updates",
        coverage: "Global, 10m land-cover probabilities",
        access: "Google Earth Engine ImageCollection",
        use: "Detect recent built-up change and confidence probabilities.",
        caveat: "Optical imagery can be affected by clouds; use composites and uncertainty.",
        url: "https://dynamicworld.app/about/",
      },
      {
        name: "Global Human Settlement Layer",
        owner: "European Commission Joint Research Centre",
        years: "1975-2030 products depending on layer",
        coverage: "Global built-up, population, and settlement model grids",
        access: "JRC downloads and Earth Engine for some products",
        use: "Long-run settlement and degree-of-urbanization baseline.",
        caveat: "Coarser than building-level datasets; use for context and validation.",
        url: "https://human-settlement.emergency.copernicus.eu/datasets.php",
      },
      {
        name: "WorldPop population counts",
        owner: "WorldPop",
        years: "2015-2030",
        coverage: "Global gridded population",
        access: "Hub downloads and API",
        use: "Estimate people in newly built-up places.",
        caveat: "Population may lag built-form change; treat mismatch as a finding and a caveat.",
        url: "https://www.worldpop.org/datacatalog/",
      },
      {
        name: "JRC Global Surface Water",
        owner: "EC JRC / Google",
        years: "1984-2021",
        coverage: "Global water history",
        access: "Downloads, GEE, WMS",
        use: "Flag settlement growth near seasonal/permanent water and flood-prone edges.",
        caveat: "Water history is not full flood risk.",
        url: "https://global-surface-water.appspot.com/download",
      },
    ],
    methodSteps: [
      "Define urban analysis units: official admin areas, GHSL urban centers, and grid cells.",
      "Measure building count, building presence, height, and built-up probability by year.",
      "Detect newly built clusters and classify morphology: infill, corridor growth, leapfrog growth, peri-urban edge, hazard-edge growth.",
      "Join population, roads, schools, clinics, water, sanitation proxies, and flood/water history.",
      "Create service-lag indicators for new built-up areas.",
      "Compare building growth against official urban population and degree-of-urbanization categories.",
    ],
    metrics: [
      {
        name: "Unrecognized Built Growth",
        definition:
          "New building growth outside existing urban classifications or planning boundaries.",
        output: "Area, building-count change, and estimated exposed population.",
      },
      {
        name: "Service-Lag Score",
        definition:
          "New built-up population with poor proximity to roads, clinics, schools, or water/sanitation proxies.",
        output: "Grid/admin score showing growth outrunning services.",
      },
      {
        name: "Hazard-Edge Growth",
        definition:
          "New settlement growth near flood-prone water histories or high-heat land-cover conditions.",
        output: "Population and building growth at climate-risk edges.",
      },
    ],
    pilotEconomies: [
      "India",
      "Bangladesh",
      "Nepal",
      "Pakistan",
      "Cambodia",
      "Lao PDR",
      "Viet Nam",
      "Thailand",
      "Philippines",
      "Indonesia",
    ],
    implementation: [
      "Use Earth Engine to export annual building and Dynamic World summaries by grid/admin area.",
      "Use Overture/Microsoft static layers for latest building footprint validation and countries outside Google temporal coverage.",
      "Use a compact vector-tile front end for time-lapse and service-lag maps.",
      "Show evidence panels with before/after metrics instead of relying only on satellite imagery.",
    ],
    caveats: [
      "Building detection can confuse nonresidential structures, shadows, and dense informal forms.",
      "Building presence does not equal occupancy.",
      "Official urban boundary comparisons require careful alignment with national definitions.",
    ],
  },
];

export function getResearchProgram(slug: string): ResearchProgram {
  const program = researchPrograms.find((item) => item.slug === slug);

  if (!program) {
    throw new Error(`Unknown research program: ${slug}`);
  }

  return program;
}

export const sharedResearchSources = Array.from(
  new Map(
    researchPrograms
      .flatMap((program) => program.sourceStack)
      .map((source) => [source.url, source])
  ).values()
).sort((a, b) => a.name.localeCompare(b.name));
