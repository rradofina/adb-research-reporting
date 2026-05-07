# Data Access Audit

Comprehensive catalog of public data sources plausibly needed across the 17
research programs in the register (CONSTITUTION.md §15). Every row records the
access model, license, registration path (with exact URL), rate limits,
reproducibility grade, and the programs that need the source.

Governed by `CONSTITUTION.md` §11. This file is a living document; the
authoritative list of pinned versions currently in use is `versions.json`
at repo root.

**Last updated:** 2026-04-29. Current-status verifications for the Google
granular-data rows were performed on 2026-04-29; broader source-catalog
verifications were last performed on 2026-04-24 to 2026-04-25 via direct
publisher pages and documentation.

---

## 1. Access model taxonomy

Every source is classified by how a researcher gains access. This affects
reproducibility directly: an A-grade source is byte-reproducible with one
HTTP call, an F-grade source cannot be reproduced by a third party at all.

| Grade | Model | Reproducibility implication |
|---|---|---|
| **A** | Open URL, no authentication, permissive license (CC-0, CC-BY, public domain, ODbL) | Byte-reproducible with one HTTP call or S3 read. |
| **B** | Free API with email-only registration | Reproducible; other researcher signs up in minutes. Cache must be committed to remove the key friction. |
| **C** | Free platform requiring full account (cloud provider, institutional) | Reproducible; other researcher creates an account. Record asset/project IDs for pinning. |
| **D** | Free but rate-limited, IP-throttled, or non-deterministic over time (OSM live, WorldPop stats API) | Reproducibility hazard. Cache must be committed. |
| **E** | Free but negotiated, per-use approval required (DHS, MICS, some IHME products) | Conditionally reproducible. Record approval terms; do not redistribute raw data. |
| **F** | Paid, institutional subscription, or restricted | Not reproducible by third parties without the same access. Do not use for headline claims. |

## 2. Reproducibility grade (separate from access model)

| Grade | Meaning |
|---|---|
| 1 | Versioned asset ID or DOI; deterministic; permissive license. |
| 2 | Stable URL; versioned by release tag or year/quarter. |
| 3 | Stable URL; values revise over time (WDI); retrieval date must be recorded. |
| 4 | Rate-limited or flaky API; cache required. |
| 5 | Continuously edited or non-deterministic (OSM live); cache mandatory, snapshot pinning recommended. |

---

## 3. Source catalog

### 3.1 Population and settlements

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| WorldPop Hub (100 m constrained and unconstrained rasters) | A via `hub.worldpop.org` direct download; also GEE asset `WorldPop/GP/100m/pop` | CC BY 4.0 | None for HTTP; FTP for bulk | Polite download cadence | 2 | 1, 4, 5, 6, 7, 8, 10, 11, 13, 15, 17 |
| WorldPop stats API (`api.worldpop.org`) | D | CC BY 4.0 | None | Flaky, area cap per request | 4 | 1 (currently in access-services pipeline; migrate to raster) |
| GHSL — Global Human Settlement Layer (built-up, pop, SMOD) | A direct download via JRC portal; also GEE `JRC/GHSL/P2023A/...` | EU open, similar to CC-BY | None | n/a | 1 | 4, 5, 6, 11, 17 |
| Meta / CIESIN HRSL — High-Resolution Settlement Layer (30 m pop grids, 140 economies) | A via HDX and AWS registry of open data; also `data.humdata.org/organization/meta` | CC BY 4.0 | None for HDX | n/a | 2 | 4, 5, 6, 17 |
| LandScan Global (Oak Ridge) | E | Non-commercial research, registration required | `landscan.ornl.gov` with institutional email | n/a | 2 | backup/validation only |
| CIESIN GPW v4 — Gridded Population of the World | A via SEDAC | CC BY 4.0 | NASA Earthdata Login | standard | 1 | validation |
| IPUMS International (census microdata) | B with full registration | Non-redistribution; citation required | `international.ipums.org` free registration | Per-project approval | 2 | 6, 11, 17 |
| DHS Program (surveys) | E | Approved-use only | `dhsprogram.com/data/new-user-registration.cfm` per-project | Per-project | 3 | 1, 2, 6, 11, 13, 17 |
| MICS (UNICEF Multiple Indicator Cluster Surveys) | E | Approved-use only | `mics.unicef.org` per-project application | Per-project | 3 | 1, 2, 13, 17 |
| LSMS-ISA (World Bank) | B with institutional-email registration | Non-redistribution | `microdata.worldbank.org` free account | standard | 2 | 1, 6, 11, 13, 14 |

### 3.2 Administrative boundaries

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| geoBoundaries `gbOpen` | A HTTP JSON API (`www.geoboundaries.org/api/current/gbOpen/...`) | CC BY 4.0 | None | polite | 1 | all |
| GADM | A direct download | Academic/personal, no commercial redistribution | None | n/a | 2 | backup |
| Natural Earth | A direct download | Public domain | None | n/a | 1 | cartography only |
| HDX country COD-AB (Common Operational Datasets — Administrative Boundaries) | A via HDX | varies by country; usually CC BY or IGO | None for HDX | n/a | 2 | disaster/humanitarian overlays |

### 3.3 Climate and weather

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| World Bank CCKP API (CMIP6) | A | World Bank open terms | None | polite | 2 | 1, 5, 11, 13, 14, 15, 17 |
| CHIRPS (UCSB CHG) daily/monthly precipitation | A direct FTP/HTTP; also GEE `UCSB-CHG/CHIRPS/...` | Public domain | None | n/a | 1 | 1, 5, 8, 9, 14, 15, 17 |
| ERA5 / ERA5-Land (Copernicus CDS) | C | Copernicus license (free, attribution) | `cds.climate.copernicus.eu` free account + `.cdsapirc` key | Queue-based | 2 | 1, 5, 8, 9, 10, 11, 14, 15 |
| NASA GPM IMERG | C | Open | NASA Earthdata Login | n/a | 1 | rainfall backup |
| MODIS LST / NDVI | C | Open | NASA Earthdata Login; or GEE | n/a | 1 | heat stress, cropland |
| TerraClimate | A via ClimateSource; also GEE `IDAHO_EPSCOR/TERRACLIMATE` | CC0 | None | n/a | 1 | 5, 9, 14 |
| NOAA GHCN daily / monthly | A via `ncei.noaa.gov` | Public domain | None | n/a | 1 | validation |

### 3.4 Air quality and pollution

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| OpenAQ v3 API | B | CC BY 4.0 | `explore.openaq.org/register` → API key via `docs.openaq.org/using-the-api/api-key` | Rate-limited; free tier published in docs | 4 | 3 |
| WHO Ambient Air Quality Database v6.1 | A direct Excel download | WHO open | None | n/a | 2 | 3 |
| Sentinel-5P TROPOMI NO2 (Copernicus) | C via Copernicus Data Space Ecosystem or GEE `COPERNICUS/S5P/...` | Copernicus open | CDSE account at `dataspace.copernicus.eu` | queue | 1 | 3 |
| ACAG (formerly Dalhousie) PM2.5 V6.GL.02.04 | A via AWS registry of open data `registry.opendata.aws/surface-pm2-5-v6gl/`; also `sites.wustl.edu/acag/datasets/surface-pm2-5/` | CC BY-NC 4.0 | None for AWS | n/a | 1 | 3, 5 |
| MERRA-2 aerosols | C | Open | NASA Earthdata Login | n/a | 1 | PM2.5 cross-check |
| CAMS (Copernicus Atmosphere Monitoring Service) | C | Copernicus open | CDSE account | queue | 2 | 3 backup |

### 3.5 Land cover, buildings, urbanization

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| Google Open Buildings (static + Temporal 2.5D) | A via `sites.research.google/open-buildings/` ZIP; also GEE `GOOGLE/Research/open-buildings/...` | CC BY 4.0 | None for ZIP; GEE requires GEE account | polite | 1 | 4, 5, 6, 11 |
| Microsoft Global ML Building Footprints | A via Azure / GitHub releases | ODbL | None | n/a | 2 | 4 backup |
| Overture Maps (buildings, places, transportation, admins, base) | A via AWS S3 (`s3://overturemaps-us-west-2/release/...`) and Azure; GeoParquet | CC BY 4.0 / ODbL combination per theme | None; `overturemaps` Python client optional | standard | 1 | 1, 4, 6, 11, 17 |
| ESA WorldCover 10 m | A via ESA; also GEE `ESA/WorldCover/v200` | CC BY 4.0 | None | n/a | 1 | 4, 11, 15, 17 |
| Dynamic World (Google × WRI) | C via GEE `GOOGLE/DYNAMICWORLD/V1` only | CC BY 4.0 | GEE account required | n/a | 1 | 4, 11 |
| AlphaEarth Foundations / Satellite Embedding V1 (Google DeepMind + Google Earth Engine) | C via GEE `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`; GCS requester-pays bucket `gs://alphaearth_foundations` | CC BY 4.0 | GEE or Google Cloud project | GCS requester-pays; Earth Engine quota | 1 | 4, 6, 7, 8, 9, 15, 17 |
| Copernicus Global Land Service | C | Copernicus open | CDSE account | queue | 1 | 11, 15 |
| MODIS Land Cover (MCD12Q1) | C | Open | NASA Earthdata Login | n/a | 1 | long-time-series backup |

### 3.6 Nighttime lights

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| NASA Black Marble VNP46A2/A3/A4 (VIIRS DNB) | C | Open | NASA Earthdata Login; or GEE `NASA/VIIRS/002/VNP46A4` | n/a | 1 | 0 |
| EOG VIIRS Nighttime Lights (annual composites) | B | CC BY 4.0 | EOG account at `eogdata.mines.edu` | n/a | 2 | 0 |
| Harmonized NTL (Li, Zhou, et al.) | A direct download via Harvard Dataverse / figshare | CC BY 4.0 | None | n/a | 1 | 0 |
| DMSP-OLS historical | A | Public domain | None | n/a | 2 | 0 long time series |

### 3.7 Water and floods

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| JRC Global Surface Water | A direct; also GEE `JRC/GSW1_4/...` | CC BY 4.0 | None | n/a | 1 | 1, 6, 8 |
| Global Flood Database (Cloud to Street) | A via `global-flood-database.cloudtostreet.ai` | CC BY 4.0 | None | n/a | 2 | 8 |
| Google Groundsource flood-event dataset | A via Zenodo DOI `10.5281/zenodo.18647054` | CC BY 4.0 | None | n/a | 1 | 7, 8 |
| Google Flood Forecasting API + GRRR / inundation-history datasets | B/C API approval via waitlist; historical datasets public | CC BY 4.0 for exposed data | Waitlist, API key, Google Cloud project | API access approval and quota | 3 | 7, 8 |
| Dartmouth Flood Observatory | A | Academic | None | n/a | 2 | 8 historical |
| HydroSHEDS / HydroRIVERS / HydroLAKES | A via `hydrosheds.org` | Academic; registration for larger products | optional | n/a | 2 | 8, 15 |
| AQUASTAT (FAO) | A | Open | None | n/a | 2 | 15 |

### 3.8 Economic and poverty indicators

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| World Bank WDI | A HTTP JSON API (`api.worldbank.org/v2`) | CC BY 4.0 | None | polite | 3 | all |
| OPHI Global MPI | A direct Excel/CSV | CC BY 4.0 | None | n/a | 2 | 0, 13, 16 |
| IMF WEO (World Economic Outlook) | A direct download | Open | None | n/a | 2 | 7, 9 |
| Global Data Lab SHDI (subnational HDI) | A direct CSV | CC BY 4.0 | None | n/a | 2 | 1, 13 |
| Our World in Data | A direct CSV and API | CC BY 4.0 | None | polite | 2 | cross-cutting framing |
| World Inequality Database (WID) | A | CC BY 4.0 | None | n/a | 2 | 14, 16 |
| Global Findex (World Bank) | A direct CSV | CC BY 4.0 | None | n/a | 2 | 14 |
| Poverty and Inequality Platform (PIP) | A API + R/Stata packages | World Bank open | None | polite | 2 | 13, 16 |
| OECD Data API | A SDMX API | OECD open | None | polite | 2 | 7, 9, 17 |

### 3.9 Health

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| WHO Global Health Observatory (GHO) API | A | Open | None | polite | 2 | 1, 3, 5, 15 |
| WHO Geolocated Health Facilities Data (GHFD) | A per-country | Open | None | n/a | 2 | 1, 13 |
| healthsites.io | A direct + OSM-backed API | ODbL | None | polite | 4 | 1, 13 (track OSM drift) |
| IHME GBD results (GHDx) | E per-dataset registration | Non-commercial | `ghdx.healthdata.org` registration per-dataset | per-dataset approval | 2 | 5, 15 |
| Lancet Countdown on Health and Climate Change | A direct PDFs and datasets | CC BY | None | n/a | 2 | 5 |
| PHIA (Population-based HIV Impact Assessment) | E | Registration | per-dataset | | 3 | as needed |
| SARA (Service Availability and Readiness Assessment) | A per-country PDF/Excel via WHO | Open | None | n/a | 2 | 1, 13 |

### 3.10 Infrastructure and transport

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| MAP friction surface 2019 (walking-only + motorized) | A via GEE `projects/malariaatlasproject/assets/accessibility/...`; also `data.malariaatlas.org` | CC BY 4.0 | None for direct; GEE account for GEE | n/a | 1 | 1, 8 |
| OSM roads (Overpass live) | D | ODbL | None | Overpass polite; rate limited | 5 | 1, 8, 12, 13 (migrate off live) |
| OSM roads (Geofabrik dated extract) | A | ODbL | None | n/a | 1 | recommended replacement |
| Overture transportation | A (Beta) | ODbL | None | standard | 2 | 1, 8, 12 |
| GRIP — Global Roads Inventory Project | A direct | CC BY 4.0 | None | n/a | 2 | 8, 12 backup |
| OpenFlights | A | ODbL / public domain | None | n/a | 1 | 12 |
| WRI Global Power Plant Database v1.3.0 | A direct CSV on GitHub | CC BY 4.0 | None | n/a | 2 | 10 (note: unmaintained since 2022; pin v1.3.0) |
| Natural Earth ports / airports | A | Public domain | None | n/a | 1 | 12 |
| MarineCadastre / AIS public | A | Public domain | None | varies | 2 | 12 |
| Global Fishing Watch | B API | CC BY 4.0 | free account | standard | 2 | 12 (indirect) |

### 3.11 Digital and ICT

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| Ookla Open Data — Speedtest tiles (fixed + mobile, quarterly) | A via AWS S3 `s3://ookla-open-data/` unauthenticated (`--no-sign-request`) | CC BY-NC-SA 4.0 | None | n/a | 1 | 2 |
| ITU ICT statistics | A direct | ITU open | None | n/a | 2 | 2 |
| World Bank Digital Development indicators (in WDI) | A | CC BY 4.0 | None | polite | 3 | 2 |
| M-Lab NDT measurements | A via Google BigQuery public | CC0 | Google Cloud account for BQ | standard | 1 | 2 validation |
| Cable.co.uk Worldwide Broadband Speed League | A reports | attribution | None | n/a | 2 | 2 framing |

### 3.12 Labor and employment

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| ILOSTAT bulk download + SDMX API + `Rilostat` | A | ILO open | None for bulk; SDMX open | polite | 2 | 5, 11, 14, 16 |
| World Bank WDI labor indicators | A | CC BY 4.0 | None | polite | 3 | 5, 11, 14 |
| Social Security Programs Throughout the World (ISSA/SSA) | A PDF | Public | None | n/a | 2 | 16 |

### 3.13 Disasters and conflict

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| EM-DAT (CRED) | B | Non-commercial open, attribution | `public.emdat.be` registration (free for research/NGO/gov/media) | Download cap per use | 2 | 7, 8, 11, 16 |
| GDACS (Global Disaster Alert and Coordination System) | A feed + API | Public | None | n/a | 2 | 7 near-real-time |
| ACLED (Armed Conflict Location and Event Data) | B via OAuth after registration | CC BY-SA 4.0 non-commercial | `acleddata.com` myACLED account → API credentials | standard | 2 | 11 |
| UCDP (Uppsala Conflict Data Program) | A direct CSV | CC BY 4.0 | None | n/a | 2 | 11 |
| INFORM Risk Index (JRC + IASC) | A | Open | None | n/a | 2 | 7, 8, 11, 16 |
| ThinkHazard! (GFDRR) | A + API | CC BY 4.0 | None | n/a | 2 | 6, 8 |
| GDIS (Geocoded Disasters, spatializes EM-DAT) | A via SEDAC | CC BY 4.0 | NASA Earthdata Login | n/a | 1 | 7 |

### 3.14 Remittances and finance

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| World Bank Remittance Prices Worldwide | A direct Excel at `remittanceprices.worldbank.org/data-download` | World Bank open, attribution | None | n/a | 2 | 14 |
| KNOMAD migration and remittances data | A direct | World Bank open | None | n/a | 2 | 14 (KNOMAD ended 2024; historical data archived) |
| World Bank bilateral remittance matrix | A direct Excel | CC BY 4.0 | None | n/a | 2 | 14 |
| Global Findex (World Bank) | A direct | CC BY 4.0 | None | n/a | 2 | 14 |
| BIS international banking statistics | A | BIS open | None | n/a | 2 | 14 |

### 3.15 Food, agriculture, water

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| FAOSTAT bulk + SDMX API | A | FAO open | None | polite | 2 | 9, 15 |
| FAO GAEZ (Global Agro-Ecological Zones) | A | Open | None | n/a | 2 | 15 |
| SPAM — Spatial Production Allocation Model | A via MapSPAM/IFPRI | CC BY 4.0 | None | n/a | 2 | 15 |
| AQUASTAT | A | FAO open | None | n/a | 2 | 15 |
| WFP VAM / HungerMap | A | Open | None | n/a | 2 | 9, 11 |
| FEWS NET | A reports + data | Public | None | n/a | 2 | 9 |
| IPC — Integrated Food Security Phase Classification | A via `ipcinfo.org` | IPC open | None | n/a | 2 | 9 |

### 3.16 Migration

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| UN DESA international migrant stock | A direct | UN open | None | n/a | 2 | 11, 14 |
| IOM GMDAC (Global Migration Data Analysis Centre) | A portal | Open | None | n/a | 2 | 11 |
| UNHCR refugee data finder | A + API | UNHCR open | None | n/a | 2 | 11 |
| World Bank bilateral migration matrix | A direct | CC BY 4.0 | None | n/a | 2 | 11, 14 |

### 3.17 Education

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| UNESCO UIS API | A | UIS open | None | polite | 2 | 15, 17 |
| World Bank EdStats | A | CC BY 4.0 | None | polite | 3 | 15, 17 |
| PISA / TIMSS / PIRLS public-use datasets | A | Public | None | n/a | 2 | 17 |

### 3.18 Energy and electricity

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| IEA World Energy Balances (free slice) | A partial | IEA open for free slice, paid for full | None for free slice | n/a | 2 | 10 |
| Ember Climate (electricity) | A direct + API | CC BY 4.0 | None | n/a | 2 | 10 |
| Our World in Data energy | A | CC BY 4.0 | None | polite | 2 | 10 |
| Africa Energy Portal (AfDB) | A | Open | None | n/a | 2 | 10 cross-region only |
| VIIRS nighttime lights as power-outage proxy | see §3.6 | | | | | 10 |

### 3.19 Trade, ports, logistics

| Source | Access | License | Registration | Rate limits | Repro | Programs |
|---|---|---|---|---|---|---|
| UN Comtrade API (free tier) | B | UN open | `comtradedeveloper.un.org` → free API key | 500 calls/day, 100K records per call | 2 | 12 |
| UNCTAD Stat | A direct | UNCTAD open | None | polite | 2 | 12 |
| World Bank LPI (Logistics Performance Index) | A | CC BY 4.0 | None | n/a | 2 | 12 |
| Port Liner Shipping Connectivity Index (UNCTAD) | A direct | Open | None | n/a | 2 | 12 |

### 3.20 Meta-platforms (one account unlocks many sources)

| Platform | Model | Registration | What it unlocks |
|---|---|---|---|
| **Google Earth Engine** — noncommercial tier | C | Google account → GEE project → tier selection at `developers.google.com/earth-engine/guides/noncommercial_tiers`. As of 2026-04-29, the April 27, 2026 tier-selection deadline has passed; verify the project tier before using GEE outputs. | Friction surface (MAP), JRC GSW, Dynamic World, AlphaEarth / Satellite Embeddings, Sentinel-1/2/3/5P, MODIS, Landsat, ESA WorldCover, CHIRPS, WorldPop, GHSL, Open Buildings, VIIRS Black Marble, and more. **Single highest-leverage registration for this repo.** |
| **NASA Earthdata Login (URS)** | C | `urs.earthdata.nasa.gov/users/new` — email + name + affiliation + country | Black Marble VIIRS, MODIS LST/NDVI, GPM IMERG, MERRA-2, SEDAC datasets, GDIS, VIIRS DNB products not on GEE. |
| **Copernicus Data Space Ecosystem (CDSE)** | C | `dataspace.copernicus.eu` free account → OAuth for APIs | Sentinel-1, Sentinel-2, Sentinel-3, Sentinel-5P, CAMS, ERA5 via CDS. Replaces the retired Copernicus Open Access Hub. |
| **Copernicus Climate Data Store (CDS)** | C | `cds.climate.copernicus.eu/user/register` → API key to `.cdsapirc` | ERA5, ERA5-Land, seasonal forecasts, reanalysis products. Separate from CDSE. |
| **OpenAQ** | B | `explore.openaq.org/register` → API key | Live public air-monitor metadata and measurements. |
| **UN Comtrade Developer Portal** | B | `comtradedeveloper.un.org` → free API key | Trade flows, HS codes, bilateral. |
| **ACLED myACLED** | B | `acleddata.com` → OAuth credentials | Conflict events, 1997–present. |
| **EM-DAT public portal** | B | `public.emdat.be` → free research/NGO/gov/media access | 27,000+ historical disasters since 1900. |
| **DHS Program** | E | `dhsprogram.com/data/new-user-registration.cfm` → per-project application | DHS microdata for over 90 countries. |
| **IPUMS International** | B | `international.ipums.org` | Census microdata for 100+ countries. |
| **IHME GHDx** | E | `ghdx.healthdata.org` → per-dataset terms | GBD results, DALYs, cause-specific mortality, risk factors. |

---

## 4. Registration priority for this repository

Do these in order. Priority is based on how many programs are blocked until
the registration is complete.

### Priority 1 — do first, unlocks most programs

1. **Google Earth Engine noncommercial account.** Unlocks ~30 datasets across
   climate, air, water, buildings, land cover, and nighttime lights. Blocking
   for programs 3, 4, 5, 6, 8, 10, 11, 15, 17. Registration at
   `developers.google.com/earth-engine/guides/noncommercial_tiers`. Pick the
   Community tier unless your institutional affiliation qualifies for
   Contributor or Partner.
2. **NASA Earthdata Login.** Unlocks Black Marble (NTL, for MPI×NTL program),
   MODIS, GPM, MERRA-2, SEDAC, GDIS. Blocking for programs 0, 3, 5, 7, 8.
   `urs.earthdata.nasa.gov/users/new`.
3. **Copernicus Data Space Ecosystem.** Unlocks Sentinel-5P NO2 and full
   Sentinel archive. Blocking for program 3. `dataspace.copernicus.eu`.
4. **Copernicus Climate Data Store.** Separate account for ERA5 via
   `.cdsapirc`. Blocking for programs 5, 8, 9, 10, 11, 14, 15.
   `cds.climate.copernicus.eu/user/register`.

### Priority 2 — do when the program advances

5. **OpenAQ API key.** Already partially in pipeline via `OPENAQ_API_KEY`
   environment variable. `explore.openaq.org/register`. Program 3.
6. **UN Comtrade developer key.** `comtradedeveloper.un.org`. Program 12.
7. **ACLED myACLED credentials.** `acleddata.com`. Program 11.
8. **EM-DAT research access.** `public.emdat.be`. Programs 7, 8, 11, 16.
9. **IPUMS International account.** `international.ipums.org`. Programs 6,
   11, 17.

### Priority 3 — per-project, slower approval

10. **DHS Program data request.** `dhsprogram.com/data/new-user-registration.cfm`.
    Per-project approval; can take days to weeks. Programs 1, 2, 6, 11, 13,
    17.
11. **MICS data request.** `mics.unicef.org`. Per-project. Programs 1, 2, 13,
    17.
12. **IHME GHDx per-dataset.** Only when a specific GBD product is needed.

### Registration metadata to record

For every registered account, record in a private file (not committed):
- Registration URL
- Date registered
- Rate-limit tier / quota
- Terms of use accepted
- Attribution string required

A public file committed to repo (`registered-accounts.md`) records only which
accounts exist and their quota — not the keys themselves. Secrets belong in
`.env.local` and in environment-variable form only.

---

## 5. Per-program pre-flight registration

Each program's registration checklist. Do the registrations listed **before**
the program advances past Hypothesis.

| # | Program | Required registrations |
|---|---|---|
| 0 | MPI × nighttime lights | NASA Earthdata Login (Black Marble). Optional: EOG account for VIIRS annual composites. |
| 1 | Climate-adjusted access to services | GEE; CDS (ERA5); LSMS-ISA account for survey triangulation. |
| 2 | Measured digital development gap | No mandatory registration (Ookla S3 is `--no-sign-request`). Optional: Google Cloud for BigQuery public access to M-Lab. |
| 3 | Air pollution without air monitors | OpenAQ; GEE; CDSE (Sentinel-5P if pulled direct); NASA Earthdata (MERRA-2). |
| 4 | Invisible urbanization | GEE (Open Buildings Temporal, Dynamic World); Microsoft building footprints via Azure. |
| 5 | Climate-health workday loss | GEE; CDS (ERA5); IHME GHDx (optional). |
| 6 | Coastal informal settlement risk | GEE; optional DHS/LSMS. |
| 7 | Disaster recovery lag | EM-DAT; NASA Earthdata (GDIS); GEE (VIIRS Black Marble for recovery signal). |
| 8 | Flood-driven service isolation | GEE (JRC GSW, MAP friction); CDS (ERA5); EM-DAT. |
| 9 | Food price climate transmission | FAOSTAT (no account); WFP/IPC (no account); CDS (ERA5). |
| 10 | Grid reliability under heat | GEE (VIIRS Black Marble); CDS (ERA5); WRI GPP (no account); Ember (no account). |
| 11 | Migration and displacement signals | ACLED; EM-DAT; UNHCR (no account); GEE. |
| 12 | Port-hinterland trade friction | UN Comtrade; Overture (no account). |
| 13 | Public service data quality | None for first pass; later optional DHS/LSMS for validation. |
| 14 | Remittance resilience | No account for WB remittance data; optional IMF WEO. |
| 15 | School heat disruption | GEE; CDS (ERA5); UIS (no account). |
| 16 | Social protection shock coverage | EM-DAT; no mandatory API keys. |
| 17 | Water stress and crop concentration | GEE; FAOSTAT; CDS (ERA5). |

---

## 6. License compatibility audit

Track which sources can be redistributed versus which can only be referenced.

| License | Commercial use | Attribution | ShareAlike | Redistribution | Sources |
|---|---|---|---|---|---|
| CC0 / public domain | yes | no | no | yes | Natural Earth, NOAA GHCN, TerraClimate, M-Lab, CHIRPS |
| CC BY 4.0 | yes | yes | no | yes | WorldPop, GHSL (with caveats), geoBoundaries, Meta HRSL, Google Open Buildings, Overture-buildings, ESA WorldCover, MAP friction, JRC GSW, Dynamic World, Ember, WRI GPP, most OPHI products, OWID, most WB products, Findex, Remittance Prices, SHDI |
| CC BY-NC 4.0 | **no** | yes | no | yes (non-commercial) | ACAG PM2.5, most DHS raw files once approved |
| CC BY-NC-SA 4.0 | **no** | yes | yes | yes (NC+SA) | Ookla Open Data |
| CC BY-SA 4.0 | yes | yes | yes | yes | ACLED data |
| ODbL | yes | yes | yes (database rights) | yes | OSM, Overture roads/places, Microsoft buildings, healthsites.io, OpenFlights |
| Copernicus open | yes | yes | no | yes | Sentinel-1/2/3/5P, CAMS, ERA5 |
| NASA open | yes | attribution encouraged | no | yes | MODIS, Black Marble, MERRA-2, GPM |
| WHO / UN open (varies) | usually yes | yes | no | usually yes | WHO GHO, UIS, FAOSTAT, ILOSTAT, Comtrade, UNHCR |
| Institutional / per-project | varies | yes | varies | **no** | DHS, MICS, IPUMS, LandScan, IHME GHDx |

**Implications for this repo:**
- Ookla's NC-SA and ACAG's NC block commercial redistribution of derived
  products. Publications and policy outputs are fine; a commercial product
  would not be.
- DHS, MICS, IPUMS raw microdata cannot be redistributed in this repo. Only
  derived aggregates (with published documentation) may appear in outputs.
- OSM/Overture ODbL means any derived database we share must also be ODbL —
  this affects how we license our own generated tables if they materially
  embed OSM data.

---

## 7. Reproducibility pattern per access model

Different access models need different reproducibility treatments. This
section binds the audit to `CONSTITUTION.md` §11.

| Access model | Reproducibility action |
|---|---|
| A (open URL) | Cache response locally; commit cache; pin URL and retrieval date in `versions.json`; SHA-256 every file in `manifest.sha256`. |
| B (free API + key) | Same as A, plus: commit cache so other researchers reproduce numbers without a key. Make live refresh opt-in (e.g., `OPENAQ_REFRESH=1`). Never commit the key itself. |
| C (platform account) | For GEE: commit the export script, record the asset ID and export date in `versions.json`, commit the small derived summary (not the raster). For NASA/CDSE/CDS: identical pattern. |
| D (rate-limited / non-deterministic) | Cache committed **mandatory**; migrate away from live endpoint where possible (OSM Overpass → Geofabrik dated extract or Overture). |
| E (per-project approval) | Do not commit raw data. Commit derived aggregates only, with a line in `literature.md` stating the approval terms. |
| F (paid / restricted) | Do not use for headline claims (§2.1 public-data-only). |

---

## 8. Per-source pin records (where to put them)

Each time a source is pulled into a program, record in `versions.json`:
- Source name
- Access model
- URL or asset ID
- Version/release identifier (geoBoundaries release tag, CCKP scenario, Ookla
  year-quarter, Overture release, GEE asset version, etc.)
- Retrieval date
- Filter applied (ISO code, bounding box, admin level, year range)
- Cache path under `.cache/research/<program>/`

`manifest.sha256` records hashes of every committed cache file.
`references.bib` receives a BibTeX entry for each dataset that is directly
cited in an output (not all datasets; only those the text references).

---

## 9. Known gaps in this audit

This audit is comprehensive but not complete. Gaps identified today:

Gaps closed in amendment of 2026-04-25:
- Pacific island DMC NSOs cataloged in §10.2 (12 DMCs + 5 regional meta-sources).
- Central Asia and Caucasus NSOs cataloged in §10.3 and §10.4.
- South Asia, Southeast Asia, East Asia NSOs cataloged in §10.5, §10.6, §10.7.
- Central banks and sector ministries noted in §10.9.

Gaps closed in amendments of 2026-04-25:
- Sector-ministry and regulator portals cataloged in §11 across 58
  agencies spanning health, disaster management, energy, transport,
  education, environment, and meteorology for the major DMCs.
- Municipal and city-level open-data portals cataloged in §12, with
  national OGD platforms (11) and city / municipal portals (~16 cities)
  plus regional city aggregators (Smart Cities Mission, OpenCity,
  IUDX, C40, ASCN, CPI, CDIA).

Remaining gaps:

- **Smaller sector ministries** for Pakistan provincial governments, Lao
  PDR, Myanmar (disrupted), Cambodia, and most Pacific DMCs are less
  audited individually. Use SPC Pacific Data Hub as the Pacific entry
  point and provincial statistics bureaus for Pakistan.
- **Historical archives pre-2000** (DMSP-OLS, early WDI, pre-indepen-
  dence censuses) may need direct archival retrieval.
- **City open-data weak cohort.** Most DMC capitals outside Jakarta,
  Bangkok, Bengaluru, Delhi/Indian Smart Cities Mission, Taipei, Hong
  Kong, Singapore rely on national portals. Dhaka, Quezon City,
  Ulaanbaatar, Central Asian capitals, and all Pacific capitals have
  limited city-level open data.
- **Historical archives pre-2000** (DMSP-OLS nightlights, early WDI,
  pre-independence censuses) may need direct archival retrieval.
- **ADB internal sources** (operational data, project portfolio) are out
  of scope for public-data-only research (§2.1).
- **Commercial satellite (Planet, Maxar)** intentionally excluded under
  §2.1.
- **Social-media data** (Twitter/X, Meta) intentionally excluded as a
  class: reproducibility, ethics, and ToS are all insufficient.
- **AI-generated synthetic data** never used as a data source (§2.5).

---

## 10. National-agency sources by ADB DMC region

Tier D of `CONSTITUTION.md` §4.2 requires searching the NSO of every DMC
in scope. This section catalogs the 50 regional ADB members — grouped by
region — with portal URL, access model, and reproducibility grade.

Data licensing is heterogeneous across NSOs and often not explicitly
stated. Where absent, assume attribution required and noncommercial
redistribution unclear. When licensing is explicit (Kyrgyz Republic CC
BY-NC-SA, Kazakhstan free-use with copying permitted, etc.) record it in
`versions.json` and respect it.

Verification of portal URL and access model was performed on 2026-04-25 for
most entries. Portals change; re-verify before citing.

### 10.1 Pacific regional meta-sources (always check first)

When an individual NSO portal is thin or offline, these Pacific meta-sources
often provide a harmonized view.

| Meta-source | URL | Access | Scope | Repro |
|---|---|---|---|---|
| SPC Statistics for Development Division | `sdd.spc.int` | A | Pacific NSO coordination and outputs | 2 |
| PDH.stat — Pacific Data Hub Indicator Database (SDMX via .Stat Suite v6) | `sdd.spc.int/indicators-stat` | A | Pacific development indicators, SDGs | 1 |
| Pacific Data Hub catalogue (CKAN API) | `pacificdata.org` | A | Datasets, microdata documentation | 1 |
| Pacific Data Hub — Microdata Library | `microdata.pacificdata.org` | E | Pacific microdata per-request | 3 |
| Pacific Environment Portal (SPREP) | `pacific-data.sprep.org` | A | Environment, climate, biodiversity | 2 |

### 10.2 Pacific DMCs (12)

| ISO3 | DMC | NSO | Portal URL | Access | Notable assets | Repro |
|---|---|---|---|---|---|---|
| FJI | Fiji | Fiji Bureau of Statistics (FBOS) | `statsfiji.gov.fj` | A/B: dashboards + document library | 2017 Census dashboard, vital statistics | 2 |
| KIR | Kiribati | National Statistics Office | `nso.gov.ki` | A: reports + documents directory | 2020 Census general report and tables | 2 |
| MHL | Marshall Islands | EPPSO (Economic Policy, Planning and Statistics) | via SPC PDH | A via PDH | 2021 Census | 3 |
| FSM | Micronesia, FSM | Division of Statistics | `stats.gov.fm` | A | 2023 Census; four-state (Pohnpei, Kosrae, Chuuk, Yap) | 2 |
| NRU | Nauru | Bureau of Statistics | via SPC PDH primarily | B/E via PDH; small office | Recent census | 3 |
| PLW | Palau | Bureau of Budget and Planning | via SPC PDH | A via PDH | 2020 Census | 3 |
| PNG | Papua New Guinea | National Statistical Office | `nso.gov.pg` | A: reports; active census page | 2024 National Population Census (final figures released 2025) | 2 |
| WSM | Samoa | Samoa Bureau of Statistics (SBS) | `sbs.gov.ws` | A/B: dashboards + Excel; microdata on request | 2021 Census, MICS Plus 2022-23, MPI | 2 |
| SLB | Solomon Islands | SINSO | `statistics.gov.sb` | A: yearbooks + release archive | NEEC 2024 (Economic Establishment Census) | 2 |
| TON | Tonga | Tonga Statistics Department | `tongastats.gov.to` | A: census tables + data-request service | 2016 Census + ongoing | 2 |
| TUV | Tuvalu | Central Statistics Division | `stats.gov.tv` | A | 2022-23 Long-Form Census (combined Census + HIES) | 2 |
| VUT | Vanuatu | VBOS | `vnso.gov.vu` / `vbos.gov.vu` | A: NSDP Data Portal with CSV download | 2020 Census, 2022 Business Establishment Census | 2 |

**Pacific access patterns worth noting:**
- The SPC Pacific Data Hub is often the best single entry point when an
  individual NSO site is thin. Always consult PDH.stat before a program
  pulls Pacific-specific indicators.
- Several small-island DMCs (MHL, NRU, PLW) do not maintain independent
  high-resource portals; their data lives in aggregated form on PDH.
- TongaStats, FBOS, and VBOS have the strongest direct-download capacity.
- Multiple Pacific DMCs have fresh 2022–2025 census activity (PNG 2024,
  FSM 2023, Tuvalu 2022-23, Samoa MICS Plus 2022-23, Vanuatu 2020 + 2022,
  Solomon Islands NEEC 2024). This is a favorable moment to build
  harmonized Pacific datasets for programs 1, 4, 6, 8, 11, 13, 17.

### 10.3 Central Asia DMCs (5)

| ISO3 | DMC | NSO | Portal URL | Access | Notable assets | Repro |
|---|---|---|---|---|---|---|
| KAZ | Kazakhstan | Bureau of National Statistics (BNS) | `stat.gov.kz/en/` | A: free machine-readable, copying permitted | 2021 Census, socioeconomic, macro | 2 |
| KGZ | Kyrgyz Republic | National Statistical Committee (NSC) | `stat.gov.kg/en/` | A: open data portal; **CC BY-NC-SA** | Open data categorized by theme and region (oblast) | 2 |
| TJK | Tajikistan | Agency on Statistics under the President | `stat.tj/en/` | A+B: analytical tables, macro, regional; NADA microdata archive at `nada.stat.tj` | Macro, regional, SDG | 2 |
| TKM | Turkmenistan | State Committee on Statistics | `stat.gov.tm/en` | D: historically closed; new E-Stathasabat platform (2024+) is mostly for reporting, not public download | Very limited public data | 4 |
| UZB | Uzbekistan | National Statistics Committee / Statistics Agency | `stat.uz/en/` + `data.gov.uz` + `data.egov.uz` | A: 13,000+ datasets via Open Data Portal | Demographics, labor, national accounts, prices, trade | 2 |

Central Asia regional cross-check: **UNECE Statistical Database**
(`w3.unece.org/CountriesInFigures/en/`) provides a harmonized view of all
five Central Asia DMCs and is a useful validation layer.

### 10.4 Caucasus DMCs (3)

| ISO3 | DMC | NSO | Portal URL | Access | Notable assets | Repro |
|---|---|---|---|---|---|---|
| ARM | Armenia | Statistical Committee (ArmStat) | `armstat.am/en/` | A: ArmStatBank + ArmDevInfo; foreign-trade DB; microdata (ILCS) | ILCS microdata, agricultural census, demographic, SDG | 2 |
| AZE | Azerbaijan | State Statistical Committee (SSC) | `stat.gov.az/?lang=en` + ASIS portal at `azstat.gov.az` | A: statistical database, web map, e-publications | Demographics, labor, health, agriculture, industry, energy, trade | 2 |
| GEO | Georgia | National Statistics Office (GeoStat) | `geostat.ge/en` | A: XLS/CSV direct downloads; no formal REST API | Full macroeconomic, enterprise surveys, trade | 2 |

### 10.5 South Asia DMCs (8)

| ISO3 | DMC | NSO | Portal URL | Access | Notable assets | Repro |
|---|---|---|---|---|---|---|
| AFG | Afghanistan | National Statistics and Information Authority (NSIA) | `nsia.gov.af` | A: site content; microdata on request | IE&LFS 2020, national accounts; political situation affects cadence | 3 |
| BGD | Bangladesh | Bangladesh Bureau of Statistics (BBS) | `bbs.gov.bd` | A: publications; some Excel | 2022 Census, HIES, LFS, SVRS | 2 |
| BTN | Bhutan | National Statistics Bureau (NSB) | `nsb.gov.bt` + Bhutan Interactive Data Portal | A: 1,000+ indicators; direct downloads; dashboards; microdata on request | **Strongest South Asia portal**; dual-map views, themed dashboards | 1 |
| IND | India | MOSPI + Office of the Registrar General + `data.gov.in` | `mospi.gov.in`; `censusindia.gov.in`; `data.gov.in` | A: CSV + API | Census, PLFS (quarterly), NSS rounds, NFHS (via IIPS) | 2 |
| MDV | Maldives | Maldives Bureau of Statistics | `statisticsmaldives.gov.mv` + Data Explorer at `data.statisticsmaldives.gov.mv` + MaldivInfo | A: datasets, releases, SDG indicator portal; census request form | 2022 Census, HIES 2019, Statistical Pocketbook 2024 | 2 |
| NPL | Nepal | National Statistics Office (formerly CBS) | `nso.gov.np` | A: publications; microdata on request | 2021 Census, NLSS, NDHS | 2 |
| PAK | Pakistan | Pakistan Bureau of Statistics (PBS) | `pbs.gov.pk` | A: publications; PSLM, HIES, LFS; microdata on request | 2023 Census, PSLM | 2 |
| LKA | Sri Lanka | Department of Census and Statistics (DCS) | `statistics.gov.lk` | A: publications; microdata on request | 2012 Census (2024 round underway), HIES, LFS | 2 |

### 10.6 Southeast Asia DMCs (10)

| ISO3 | DMC | NSO | Portal URL | Access | Notable assets | Repro |
|---|---|---|---|---|---|---|
| BRN | Brunei Darussalam | Department of Economic Planning and Statistics (DEPS) | `deps.mofe.gov.bn` | A: publications | 2021 Census | 2 |
| KHM | Cambodia | National Institute of Statistics (NIS) | `nis.gov.kh` | A: publications; microdata on request | 2019 Census; CSES; CDHS | 2 |
| IDN | Indonesia | Badan Pusat Statistik (BPS) | `bps.go.id` | A: extensive open data; Web API; strong programmatic access | SUSENAS, SAKERNAS, Podes, 2020 Census + long-form 2022 | 1 |
| LAO | Lao PDR | Lao Statistics Bureau (LSB) | `lsb.gov.la` | A: publications | 2015 Census; LECS | 2 |
| MYS | Malaysia | Department of Statistics Malaysia (DOSM) | `dosm.gov.my` + `data.gov.my` (OpenDOSM) | A: excellent open data + API; **best-in-region programmatic access** | 2020 Census, HIS, LFS | 1 |
| MMR | Myanmar | Central Statistical Organization (CSO) | `mmsis.gov.mm` | D: disrupted since 2021 coup; caution required | 2014 Census; sparse updates since | 4 |
| PHL | Philippines | Philippine Statistics Authority (PSA) | `psa.gov.ph` + `openstat.psa.gov.ph` | A: OpenSTAT (PX-Web API); CSV bulk | 2020 Census (already used in repo); FIES, APIS, monthly LFS | 2 |
| THA | Thailand | National Statistical Office (NSO) | `nso.go.th` | A: publications | 2010 Census (2020 new round); SES, LFS | 2 |
| TLS | Timor-Leste | Direção-Geral de Estatística (DGE) | `statistics.gov.tl` | A: publications | 2022 Census (preliminary 1,340,434 population) | 2 |
| VNM | Viet Nam | General Statistics Office (GSO) | `gso.gov.vn` | A: publications + CSV | 2019 Census; VHLSS; LFS | 2 |

### 10.7 East Asia DMCs (4)

| ISO3 | DMC | NSO | Portal URL | Access | Notable assets | Repro |
|---|---|---|---|---|---|---|
| CHN | China, PRC | National Bureau of Statistics (NBS) | `stats.gov.cn` (English portal) | A: national monthly/annual; English partial | Extensive national accounts; 2020 Census | 2 |
| HKG | Hong Kong, China | Census and Statistics Department | `censtatd.gov.hk` | A: free open data + API | Thematic census, quarterly series | 1 |
| MNG | Mongolia | National Statistics Office | `1212.mn/en/` + SDG portal at `sdg.1212.mn/EN/` | A: Open Data initiative; indicators database; microdata archive at `web.nso.mn/nada` | 2020 Census; macro; SDG | 2 |
| TAP | Taipei,China | DGBAS (Directorate General of Budget, Accounting and Statistics) | `stat.gov.tw` (English) | A: publications + CSV | Census, LFS, national accounts | 2 |

### 10.8 ADB non-DMC regional members (for comparative analysis only)

Non-DMC regional members have mature open-data portals. Listed here because
cross-regional comparison in some programs (e.g., program 2 measured digital
gap) requires a developed-economy reference point.

| ISO3 | Member | NSO | URL | Access |
|---|---|---|---|---|
| AUS | Australia | Australian Bureau of Statistics | `abs.gov.au` | A (REST API) |
| NZL | New Zealand | Stats NZ | `stats.govt.nz` | A (API) |
| JPN | Japan | Statistics Bureau | `e-stat.go.jp` | A (API) |
| KOR | Korea, Republic of | Statistics Korea (KOSTAT) | `kostat.go.kr` | A (API) |
| SGP | Singapore | Department of Statistics | `singstat.gov.sg` | A (API) |

### 10.9 Central banks and sectoral ministries

For programs 2, 10, 14, 16 (digital, grid, remittance, social protection),
central bank and sector-ministry data is often timelier than NSO data.

| DMC | Central bank / portal | Relevance |
|---|---|---|
| PHL | BSP (`bsp.gov.ph`) | Financial inclusion, remittances (OF cash remittances) |
| BGD | Bangladesh Bank (`bb.org.bd`) | Remittances, financial inclusion |
| IND | RBI (`rbi.org.in`) + DBIE | Financial stats, remittances |
| PAK | SBP (`sbp.org.pk`) | Macro, remittances |
| IDN | Bank Indonesia (`bi.go.id`) | Macro, finance |
| VNM | SBV (`sbv.gov.vn`) | Macro, finance |
| KAZ | NBK (`nationalbank.kz`) | Macro |
| FJI | RBF (`rbf.gov.fj`) | Pacific macro, finance |
| NPL | NRB (`nrb.org.np`) | Remittances |
| LKA | CBSL (`cbsl.gov.lk`) | Macro, remittances |

National planning agencies (NEDA Philippines, Planning Commission Bangladesh,
Bappenas Indonesia, MPI Viet Nam, etc.) and national SDG reporting platforms
are the default next stop when NSO and central-bank data are insufficient.

### 10.10 Access-pattern heuristics for NSO data

1. **Language.** Most NSOs publish in a national language plus partial
   English. Plan for bilingual column-header parsing or build PDF-table
   extraction.
2. **Format.** Expect Excel, PDF, and occasionally CSV. Clean REST APIs are
   rare; SDMX is more common in OECD-adjacent agencies and regional
   aggregators (PDH.stat, UNECE). Best-in-region programmatic access:
   Bhutan (NSB Interactive Data Portal), Malaysia (OpenDOSM), Indonesia
   (BPS Web API), Hong Kong (CSD), PSA OpenSTAT (Philippines).
3. **Licensing.** Frequently unstated; default assumption is attribution
   required, noncommercial redistribution unclear. When licensing is
   explicit, record it in `versions.json` and respect it.
4. **Microdata.** Usually per-project approval; timeline 4–12 weeks. Do
   not assume instant access. Treat as access-model E.
5. **Timeliness.** Census cadence is usually decadal; household surveys
   2–5 years; monthly/quarterly series come from labor-force and CPI
   programs. Plan around the cadence of the series you need, not the
   calendar you want.
6. **Change cadence.** NSO portals are redesigned every 2–5 years and
   URLs break. Commit cached files to repo; do not assume URL stability.
7. **Reproducibility.** Treat NSO data as reproducibility grade 2 or 3
   (re-derivable from committed cache) at best. Live retrieval is not
   deterministic across time.
8. **Recent-census triage.** Several DMCs have fresh (2022–2025) census
   releases: PNG 2024, FSM 2023, Tuvalu 2022-23, Vanuatu 2022 business,
   Solomon Islands NEEC 2024, Samoa MICS+ 2022-23, Timor-Leste 2022,
   Pakistan 2023, Bangladesh 2022, Maldives 2022, Nepal 2021,
   Indonesia long-form 2022. Programs should use these as anchor years
   where appropriate.

---

## 11. Sector-ministry and regulator portals

NSO data is often thinner, slower, and less granular than what sector
ministries and regulators actually hold. For programs that need
operational facility data (health, education), near-real-time metered
series (electricity, air quality), or disaster incidents, the sector
ministry or regulator is the primary source — not the NSO. This section
catalogs the main sector portals for the largest DMCs, plus access
patterns and regional meta-sources.

Verification performed 2026-04-25. Portals change; re-verify before citing.

### 11.1 Regional meta-source (ASEAN)

| Source | URL | Access | Scope |
|---|---|---|---|
| ASEAN Statistical Yearbook + ASEANstats portal | `aseanstats.org` + `asean.org` | A | Population, education, health, employment, macro, trade in goods and services, FDI, tourism, transport, agriculture, manufacturing — harmonized across 10 ASEAN members |

ASEANstats is the harmonization layer managed by the ASEAN Secretariat's
Statistics Division under the ASEAN Community Statistical System (ACSS).
Cross-check regional SEA DMC series here before citing country-specific
numbers.

### 11.2 Health facility registries and HMIS (relevant to programs 1, 5, 13)

Facility registries and routine health-management-information systems
(HMIS) live under health ministries, not NSOs. For program 13 (public
service data quality), the comparison of OSM-mapped facilities against
these admin registries is the core data test.

| DMC | Ministry / agency | Portal URL | Access | Notable |
|---|---|---|---|---|
| PHL | DOH — National Health Facility Registry (NHFR v2.0) | `nhfr.doh.gov.ph/VActivefacilitiesList` | A: master facility list, searchable | Validated annually each March; unique NHFR code per facility; **the primary complement to OSM counts** |
| BGD | DGHS — Facility Registry (Central HRIS) | `hrm.dghs.gov.bd/public/facility-registry` + `facilityregistry.dghs.gov.bd` | A: searchable; dashboard at `dashboard.dghs.gov.bd` | DHIS2 network covers ~75% of public facilities, 14,000+ community clinics |
| IDN | Kemenkes — SATUSEHAT | `satusehat.kemkes.go.id/data` | A: dashboards + downloads | National EMR integration across hospitals, puskesmas, posyandu, labs, pharmacies |
| IND | MoHFW — HMIS | `hmis.mohfw.gov.in` + `hmis.nhp.gov.in` + `data.gov.in` (HMIS keyword) | A: public reports; G2G at the facility level | 200,000+ facilities, 600+ indicators; links NFHS, DLHS, RGI |
| PAK | MoNHSR&C | `nhsrc.gov.pk` | B/E: DHIS2 for vertical programs (Malaria, TB, HIV); facility-list access less centralized | Provincial DoHS (Punjab, Sindh, KP, Balochistan) hold more complete provincial data |
| NPL | DoHS — HMIS (IHIMS Roadmap 2022-2030) | `hmis.gov.np` + `dohs.gov.np` | A: annual reports (latest 2080/81 ≈ 2023/24) | DHIS2 expansion to 33 local level governments (LLGs) |
| LKA | Ministry of Health | `health.gov.lk` | A: publications | HHIMS/DHIS2 deployments |
| VNM | MoH (Bộ Y tế) | `moh.gov.vn` | A: Health Statistics Yearbook via GHDx | DHIS2 adoption via HISP Vietnam; facility-level microdata less open |
| KHM | Ministry of Health | `moh.gov.kh` | A: publications | HMIS through DHIS2 |
| LAO | Ministry of Health | `moh.gov.la` | A: publications | DHIS2 adoption |
| MNG | Ministry of Health | `moh.gov.mn` | A: publications | — |
| BTN | Ministry of Health | `moh.gov.bt` | A: publications | Small system, high coverage |
| Pacific | SPC + country MoH | via PDH | A via PDH | SPC coordinates Pacific health data harmonization |

**Cross-DMC pattern.** DHIS2 is the dominant HMIS software across most
South and Southeast Asia DMCs. The DHIS2 data model is standardized
(`dataElement`, `categoryOptionCombo`, `orgUnit`, `period`) so a single
integration pattern scales across DMCs once facility-level access is
negotiated. Public portals typically expose aggregated dashboards; raw
facility-level detail usually requires DGHS/DoH approval.

### 11.3 Disaster management agencies (programs 7, 8, 11, 16)

DRM agencies hold the near-real-time incident data that EM-DAT aggregates
with lag. For program 7 (disaster recovery lag) and program 8 (flood
market access), DRM-agency data is the primary source and EM-DAT is the
harmonized cross-check.

| DMC | Agency | Portal URL | Access | Notable |
|---|---|---|---|---|
| PHL | NDRRMC + DSWD DROMIC | `ndrrmc.gov.ph`, monitoring dashboard at `monitoring-dashboard.ndrrmc.gov.ph`, DROMIC at `dromic.dswd.gov.ph` | A: situation reports (PDF + archive) | Situation Reports per event; NDRRMP 2020-2030 committed |
| IDN | BNPB — DIBI (Data Informasi Bencana Indonesia) | `dibi.bnpb.go.id` + `data.bnpb.go.id` + `gis.bnpb.go.id` | A: historical disaster events since 400 AD; Excel downloads 2008-2019; GIS layer | Uses DesInventar + DesconsultaR methodology (UN-SPIDER standard) |
| IND | NDMA (policy) + NDEM (operations) | `ndma.gov.in` + `ndem.nrsc.gov.in` | A: policies + guidelines + resources; NDEM has geospatial emergency data | Apex body under PM; State DMAs hold operational data |
| BGD | DDM (Department of Disaster Management, under Ministry of Disaster Management and Relief) | `ddm.gov.bd` + `ddm.portal.gov.bd` | A: policies, Post Disaster Needs Assessments (PDNAs) | Disaster Management Act 2012; cyclone and flood focus |
| PAK | NDMA + Provincial DMAs | `nationaldisastermanagementauthority.pk` | A: publications | — |
| NPL | NDRRMA (National Disaster Risk Reduction and Management Authority) | `bipad.gov.np` (BIPAD portal) | A: incident dashboard | Near-real-time incident reporting |
| VNM | DMHCC (Disaster Management Center) | — | A: publications | Via Vietnam Disaster Management Authority |
| Pacific | Pacific Risk Information System (PRIS) | via SPC | A via SPC | Regional coordination |

**Cross-DMC pattern.** DesInventar is the dominant methodology for
historical disaster event cataloging; BNPB's DIBI is the flagship
implementation. Excel exports are common; API access is rarer. EM-DAT
(§3.13) aggregates many of these into a single cross-country frame but
with lag.

### 11.4 Energy and electricity regulators (program 10)

Grid-reliability, generation, consumption, and capacity data are held by
electricity regulators and state utilities, not NSOs. Cadence is often
daily or hourly — much faster than any NSO release.

| DMC | Regulator / utility | Portal URL | Access | Cadence |
|---|---|---|---|---|
| IND | Central Electricity Authority + National Power Portal | `cea.nic.in/dashboard` + `npp.gov.in` | A: national + regional + state; GIS-enabled; API via `data.gov.in` | Daily; annual "All India Electricity Statistics (General Review)" |
| IDN | Kementerian ESDM (MEMR) + ESDM One Map Indonesia | `esdm.go.id/en` + ESDM One Map Indonesia | A: web-GIS with oil/gas/mineral/renewable/electricity/geology | Annual; project-level layers |
| PHL | DOE — Electric Power Industry Management Bureau | `doe.gov.ph/energy-statistics` | A: 2003-2024 power statistics per grid (Luzon/Visayas/Mindanao), per-technology, per-sector | Monthly + annual |
| BGD | Bangladesh Power Development Board (BPDB) | `bpdb.gov.bd` | A: daily reports (researcher-scraped dataset 2019-2024 with 1867 daily reports published via ScienceDirect) | Daily |
| PAK | NEPRA + NTDC | `nepra.org.pk` + `ntdc.gov.pk` | A: publications | Monthly + annual |
| VNM | MOIT + EVN (Electricity Vietnam) | `evn.com.vn` | A: publications | Monthly + annual |
| LKA | CEB (Ceylon Electricity Board) + PUCSL | `ceb.lk` + `pucsl.gov.lk` | A: annual statistics | Annual |
| NPL | NEA (Nepal Electricity Authority) + ERC | `nea.org.np` | A: annual report | Annual |
| MNG | Ministry of Energy + MOEE | `energy.gov.mn` | A: publications | Annual |
| Pacific | Per utility (EPC Samoa, UNELCO Vanuatu, EPC PNG, etc.) | Per utility website | B: often publications only | Annual |

**Cross-DMC pattern.** National Power Portals (India NPP, Philippines
EPIMB, BPDB daily reports) are structurally similar: they expose
generation, installed capacity, demand, and consumption by grid, source,
and sector. A single scraping pattern works across several DMCs. For
programs needing continuous-time electricity reliability, **BPDB's daily
reports are the best single resource in South Asia** because of their
cadence, explicit load-shedding fields, and recently compiled
machine-readable archive.

### 11.5 Transport and public-works ministries (programs 1, 8, 12)

Road networks and transport infrastructure data sit with PWD/MoRTH/DPWH
equivalents. Many expose GIS portals; bulk shapefile access often needs
a formal request.

| DMC | Ministry / agency | Portal URL | Access | Notable |
|---|---|---|---|---|
| IND | MoRTH + PM GatiShakti National Master Plan | `morth.gov.in` + `pmgatishakti.gov.in` | C: 550+ layers of multi-modal infrastructure; GIS-enabled; login required | NMP integrates 16 ministries; excellent if login is obtainable |
| PHL | DPWH — Road and Bridge Inventory | `dpwh.gov.ph/dpwh/gis/rbi` + RTI + DBI | A when feature server is public (accessible via QGIS); E via FOI for shapefiles | ArcGIS Map/Feature Server backend |
| BGD | Roads and Highways Department (RHD) + LGED | `rhd.gov.bd` + `lged.gov.bd` | A: publications; LGED is strong on rural roads | — |
| IDN | Kementerian PUPR + Ina-Geoportal | `pu.go.id` + `tanahair.indonesia.go.id` | A: national spatial data infrastructure | Ina-Geoportal is the one-stop GIS |
| PAK | NHA (National Highway Authority) | `nha.gov.pk` | A: publications | — |
| NPL | DoR (Department of Roads) | `dor.gov.np` | A: publications | — |
| VNM | Ministry of Transport | `mt.gov.vn` | A: publications | — |

**Cross-DMC pattern.** Access tiers: A for network maps on the website,
C for API/GIS feature-server access (India NMP needs login), E for bulk
shapefile downloads (often require formal FOI/letter requests). OSM /
Overture is usually more complete and more accessible than the ministry
data for program 8 (flood market access) at ADM2 and below; use ministry
data for the backbone network only.

### 11.6 Education ministries (program 17)

School data lives with education ministries, not NSOs. Program 17 (school
heat disruption) should source school locations and enrollment from these
ministries.

| DMC | Ministry / agency | Portal URL | Access | Notable |
|---|---|---|---|---|
| PHL | DepEd — BEIS / LIS / EBEIS | `ebeis.deped.gov.ph` + `beis.deped.gov.ph` + `depedph.com/beis-basic-education-information-system` | A: master list of schools; BEIS annual data collection | School + teacher + facility + curriculum; validated BOSY/EOSY; Australian Aid–supported |
| IDN | Kementerian Pendidikan Dasar dan Menengah — Dapodik + Portal Satu Data | `data.kemendikdasmen.go.id` + `dapo.kemdikbud.go.id` | A: dashboards and datasets; Dapodik itself is administrative (not pure open data) | Version 2026.b released 2026-01-13; semester cadence |
| IND | MoE — UDISE+ (Unified District Information System for Education) | `udiseplus.gov.in` | A: annual reports; school- and district-level dashboards | 1.5M schools, 250M students; annual data |
| BGD | BANBEIS (Bangladesh Bureau of Educational Information and Statistics) | `banbeis.gov.bd` | A: annual publications | — |
| PAK | NEAS + Provincial school-census systems | `neas.gov.pk` | A: publications | School census per province |
| VNM | MOET (Ministry of Education and Training) | `moet.gov.vn` | A: publications | — |
| NPL | MoEST + CEHRD | `moest.gov.np` | A: publications | Flash reports |

**Cross-DMC pattern.** School master lists are usually accessible at DMC
level (DepEd, Dapodik, UDISE+, BANBEIS); programmatic access is weaker
than for health. For cross-country comparability, UNESCO UIS (§3.17) is
the harmonized layer.

### 11.7 Environment ministries and air-quality regulators (program 3)

EMB-equivalent bureaus hold official air-quality monitoring data; they
are the ground-truth analog to OpenAQ for program 3.

| DMC | Agency | Portal URL | Access | Notable |
|---|---|---|---|---|
| PHL | DENR — EMB Air Quality | `air.emb.gov.ph` + `ambientair.emb.gov.ph` | A: real-time monitoring dashboard; Philippines AQI App | 75 stations, 34 with real-time continuous online monitoring; 16 regions |
| IND | CPCB — Central Pollution Control Board + SAFAR | `cpcb.nic.in` + `safar.tropmet.res.in` | A: national AQI + station data; API partial | 400+ CAAQMS stations |
| IDN | KLHK (Kementerian Lingkungan Hidup dan Kehutanan) + BMKG | `menlhk.go.id` + `bmkg.go.id` | A: dashboards; ISPU air quality index | — |
| BGD | DoE (Department of Environment) + CASE | `doe.gov.bd` | A: CAMS 11-city network | — |
| PAK | Pakistan EPA + provincial EPAs | `environment.gov.pk` | A: limited | Punjab EPA more data-rich than others |
| VNM | VEA (Vietnam Environment Administration) | `vea.gov.vn` | A: publications | — |

**Cross-DMC pattern.** Air-quality ground-truth networks are sparser
than OpenAQ (OpenAQ includes both public and private sources). EMB-type
bureaus are the authoritative national source but coverage is uneven
between capitals and rural areas. Program 3 should triangulate OpenAQ ×
ground-truth EMB × satellite (Sentinel-5P, ACAG).

### 11.8 Meteorological agencies (programs 5, 8, 9, 15, 17)

National met agencies hold the observational ground-truth for climate
series. Public access varies, but most provide at least historical
monthly summaries.

| DMC | Agency | Portal URL | Access | Notable |
|---|---|---|---|---|
| PHL | PAGASA | `pagasa.dost.gov.ph` | A: public bulletins; climatology and monthly stats | TC tracks; climate outlook |
| IND | IMD (India Meteorological Department) | `imd.gov.in` + `mausam.imd.gov.in` | A: long-period archives | Gridded rainfall products |
| IDN | BMKG | `bmkg.go.id` | A: stations and dashboards | — |
| BGD | BMD (Bangladesh Meteorological Department) | `bmd.gov.bd` | A: publications | — |
| PAK | PMD + CDPC (Climate Data Processing Centre) | `pmd.gov.pk` + `cdpc.pmd.gov.pk` + `weather.gov.pk` | A: climatology; historical climate records at CDPC Karachi | 60-80 year statistical models; AR5 climate-change scenarios at `pmd.gov.pk/rnd/rndweb/rnd_new/climchange_ar5.php` |
| VNM | NCHMF (Viet Nam National Centre for Hydro-Meteorological Forecasting) | `nchmf.gov.vn` | A: forecasts and climatology | — |
| NPL | DHM (Department of Hydrology and Meteorology) | `dhm.gov.np` | A: station data; glacier and hydrology | — |
| LKA | Department of Meteorology | `meteo.gov.lk` | A: publications | — |
| Pacific | SPREP + national met services | via SPREP and SPC | A via SPREP Pacific Climate Change Portal | Regional coordination strong |

### 11.9 Central banks (programs 2, 10, 14, 16)

Already summarized in §10.9. Repeated here in the sector-ministry frame
for completeness: central banks are the primary source for remittances,
financial inclusion, credit, exchange rates, reserves, and balance of
payments — faster than WDI and more granular than IMF WEO.

### 11.10 Access patterns and integration recommendations

1. **NSO vs. sector ministry.** Use NSO for harmonized macro, census, and
   survey. Use sector ministry for facility registries, incidents, daily
   operational data, sectoral indicators. These are not substitutes;
   they are complements.

2. **DHIS2 is the dominant HMIS.** Bangladesh, Nepal, Pakistan,
   Sri Lanka, Cambodia, Lao PDR, Viet Nam, Mongolia, Bhutan, and most
   Pacific DMCs run DHIS2. A single DHIS2 integration pattern scales
   across all of them once a program negotiates facility-level access.

3. **DesInventar is the dominant disaster-data standard.** BNPB's DIBI is
   the reference implementation; many other Asia-Pacific DRM agencies
   use the same methodology. EM-DAT is the harmonized global layer but
   lags country data.

4. **Access tier downgrades are common.** Public dashboards are often
   A-grade; bulk exports, shapefiles, and microdata are often C (request
   with credentials) or E (per-project FOI). Plan for the slower path
   when programs need bulk data.

5. **Language.** National-language primary, English coverage partial.
   Expect to build bilingual parsing for facility-list CSVs, PDF tables
   from annual reports, and dashboard scrapers.

6. **Cadence matters per program.**
   - Census: decadal.
   - Facility registry: monthly to annual update.
   - HMIS aggregated: monthly.
   - Electricity: daily to near-real-time.
   - Air quality: hourly at best, sparse geographically.
   - Disaster incidents: per-event, near-real-time.
   - Meteorological: daily to monthly, long archives.

7. **Program-to-source map (direct recommendations):**
   - **Program 1 (access-services):** PHL DOH NHFR + BGD DGHS Facility
     Registry + IDN SATUSEHAT + IND HMIS as master facility registries
     to complement OSM counts. DPWH RBI + MoRTH Gati Shakti + BGD RHD
     for road network backbone.
   - **Program 3 (air-monitoring):** PHL DENR EMB + IDN KLHK + IND CPCB
     as ground-truth for OpenAQ triangulation.
   - **Program 5 (climate-health-workdays):** IMD + PAGASA + PMD + BMD +
     BMKG for daily temperature archives; HMIS for heat-related morbidity
     (limited).
   - **Program 7 (disaster-recovery-lag):** BNPB DIBI + NDRRMC DROMIC +
     IND NDEM + NPL BIPAD; use EM-DAT as cross-country harmonization.
   - **Program 8 (flood-market-access):** DRM agencies for incidents;
     DPWH / MoRTH / RHD for roads; DMH/BMD for rainfall.
   - **Program 10 (grid-reliability-heat):** CEA + NPP + DOE + BPDB +
     MEMR ESDM One Map. BPDB daily reports are the best cadence in
     South Asia.
   - **Program 13 (public-service-data-quality):** **The comparison of
     OSM facility counts against DOH NHFR / DGHS Facility Registry /
     SATUSEHAT / HMIS facility lists is literally the core data test of
     this program.**
   - **Program 17 (school-heat-disruption):** DepEd BEIS + Dapodik +
     UDISE+ + BANBEIS for school locations and enrollment; met agencies
     for heat exposure.

---

## 12. Municipal and city-level open-data portals (and national OGDs)

Two adjacent resource families distinct from NSO and sector ministries:

1. **National Open Government Data (OGD) platforms** aggregate datasets
   from many ministries into one portal. Distinct from NSO (produces
   official statistics) and from sector ministries (own operations).
2. **Municipal / city open-data portals** give sub-ADM1 resolution —
   relevant to programs 1, 4, 6, 8, 11, 13 where intra-city patterns
   (informal settlements, municipal services, flood zones) matter more
   than national averages.

Verification performed 2026-04-25. Portals shift frequently; re-verify
before citing.

### 12.1 National Open Government Data platforms

| DMC / member | Portal | URL | Scale | Notable |
|---|---|---|---|---|
| PHL | Open Data Philippines | `data.gov.ph` | Central hub | Managed by Open Data PH Task Force |
| IND | Open Government Data (OGD) India | `data.gov.in` | Very large, multi-ministry | API; state+sectoral; UDISE+, HMIS, etc. integrated |
| IDN | Portal Satu Data Indonesia | `data.go.id` + `katalog.satudata.go.id` | Large | Under Bappenas / Indonesian One Data Secretariat |
| THA | Open Government Data Thailand | `data.go.th` | 11,000+ datasets (2013→) | DGA-managed; EGA Open Government License; API |
| MYS | data.gov.my | `data.gov.my` | Large; OpenDOSM integration | Best-in-region programmatic access |
| SGP | data.gov.sg | `data.gov.sg` | 4,000+ datasets from 69 agencies | 350K monthly visitors, 13M API calls/month, real-time + historical |
| HKG | DATA.GOV.HK | `data.gov.hk/en/` | 6,000+ datasets, 18 categories | Coordinated by Digital Policy Office; open to commercial + non-commercial reuse |
| TAP | data.gov.tw | `data.gov.tw/en` | Large national aggregator | — |
| NPL | Nepal Open Data | `opendata.gov.np` | Growing | National catalog |
| PAK | data.gov.pk | `data.gov.pk` | Limited | Weaker than regional neighbors |
| BGD | data.gov.bd | `data.gov.bd` | Growing | Multi-ministry |

Meta-aggregators:
- **Pan-Asia Open Data Portal** (`dataportal.asia`) — cross-DMC meta-catalog
- **HDX** (`data.humdata.org`) — humanitarian-focused aggregator, many
  government datasets mirrored

### 12.2 City / municipal open-data portals

Graded by access and data depth.

| City | DMC | Portal URL | Access | Notable |
|---|---|---|---|---|
| Jakarta | IDN | `satudata.jakarta.go.id` + `jakartasatu.jakarta.go.id` (geoportal) | A: official open-data portal since 2022 under Governor Regulation 37/2022 | Tourism, disaster mgmt, urban planning, health, public works, transport, agriculture, energy; BPS integration |
| Bandung | IDN | via `data.go.id` provincial; smart-city layer at city level | A | Pioneer Indonesian open-data city (Smart City Award 2015) |
| Semarang | IDN | SEMAR SATATA (Semarang Satu Data) | A: OGP commitment IDSMG0001 | Collaborative with BPS, OPDs, community; real-time integrated |
| Surabaya | IDN | via national Satu Data + smart-city operational | B: partial | — |
| Bangkok | THA | `data.bangkok.go.th` | A: ~430 datasets | Flood Risk Management Platform co-built with Open Contracting Partnership; transport, urban planning, waste, environment |
| Taipei | TAP | `data.taipei` + Data.Taipei 2.0 Beta | A: 22 categories since 2011, upgraded 2019 | **First Asian city to implement open-data policy (2011)**; Taipei City Dashboard open-source on GitHub |
| Ho Chi Minh City | VNM | `opendata.hcmgis.vn` + `portal.hcmgis.vn` + digital-transformation portal `chuyendoiso.hochiminhcity.gov.vn` | A: GIS layers operational | Smart City by 2030 target; common database integrating DoH, DPI, DOT, DoNRE |
| Hong Kong | HKG | `data.gov.hk/en/` (same as national) | A: 6,000+ datasets | City-state effectively; see §12.1 |
| Singapore | SGP | `data.gov.sg` (same as national) | A: 4,000+ datasets | City-state; see §12.1 |
| Delhi NCR | IND | `delhi.data.gov.in` + `des.delhi.gov.in` + OGD Delhi state listing | A: multiple portals; "Statistics of Delhi at a glance" | Open Transit Data at `otd.delhi.gov.in/data/realtime/`; DISE/UDISE+ by district |
| Bengaluru | IND | `opendata.benscl.com` (Bengaluru Smart City Ltd) | A: runs India Urban Data Exchange (IUDX) | IUDX is an open-source data-exchange platform; Liveable Bengaluru vision |
| Mumbai, Chennai, Hyderabad, Pune, Ahmedabad (and 100 total Indian cities) | IND | `smartcities.data.gov.in` | A: Smart Cities Mission Data Portal | **100 Indian cities, 2,600+ datasets, 25 sectors, 75 templates**, APIs |
| Dhaka (North + South City Corporations) | BGD | No official city open-data portal; community GitHub + city-corp websites | D: community-maintained | Official city-corp data limited |
| Kuala Lumpur | MYS | DBKL Portal (`dbkl.gov.my/en/data-statistik/data-terbuka`) + City Planning System (`cps.dbkl.gov.my`) | A: partial for planning; national `data.gov.my` covers most | DBKL CPS has development-control info with geospatial map |
| Quezon City, Manila, Davao, Cebu | PHL | Partial city websites + national `data.gov.ph` | B: city-level open-data not well developed | QCitizen mobile app; national portal is usually the entry point |
| Ulaanbaatar | MNG | Limited; via national `1212.mn` | B/D | Capital data is in national NSO |
| Bishkek, Almaty, Tashkent, Baku, Tbilisi, Yerevan | Central Asia + Caucasus | No dedicated city portals; via national NSOs | B/D | Use national NSO and central bank |
| Port Moresby, Suva, Apia, Honiara, Nuku'alofa | Pacific | None; via national + SPC Pacific Data Hub | D | Pacific DMCs rarely have dedicated city portals |

### 12.3 Regional and program-specific city aggregators

| Platform | URL | Scope | Program relevance |
|---|---|---|---|
| India Smart Cities Mission Data Portal | `smartcities.data.gov.in` | 100 Indian cities, 2,600+ datasets, 25 sectors | Programs 4, 6, 11, 13 |
| OpenCity — Urban Data Portal (non-government, India) | `opencity.in` + `data.opencity.in` | Indian cities; often better download ergonomics than government portals | Program 4, 13 |
| India Urban Data Exchange (IUDX) | `opendata.benscl.com` + `iudx.org.in` | Open-source cross-city data exchange | Program 4 |
| Pacific Data Hub — city-level series | via SPC | Pacific small islands | Programs 4, 6 |
| C40 Cities Open Data | `c40.org` | 96 global member cities including Dhaka, Jakarta, Delhi, Mumbai | Programs 5, 6, 10 (climate-adjacent) |
| ASEAN Smart Cities Network (ASCN) | `aseansmartcities.asean.org` | 26 ASEAN pilot cities | Programs 2, 4 |
| UN-Habitat City Prosperity Initiative (CPI) | `unhabitat.org/cpi` | Global urban index | Program 4 cross-comparison |
| ADB Cities Development Initiative for Asia (CDIA) | `cdia.asia` | ADB-regional city projects | Program 4 |

### 12.4 Cross-DMC patterns

1. **City open data is extremely uneven.** Strong: Jakarta, Taipei, Hong
   Kong, Singapore (city-state), Bangkok, Bengaluru, and the 100 Indian
   Smart Cities Mission cities. Weak: most other DMC capitals rely on
   national OGD or NSO.
2. **Smart-city branding ≠ open data.** A city can be marketed as a
   "smart city" without publishing open data. Look for explicit
   open-data policy documents (e.g., Jakarta Governor Regulation
   37/2022) rather than smart-city marketing.
3. **Indonesia has the most coherent stack.** Jakarta, Bandung, Semarang,
   and the national Satu Data policy create a national → province →
   city open-data hierarchy unusual for the region.
4. **India's Smart Cities Mission Data Portal is the single biggest
   open-data resource at city level in Asia** — 100 cities, one portal,
   standardized templates.
5. **Taipei was first to institutionalize city open data** (2011); the
   Taipei City Dashboard is open-source and worth studying as a
   reference implementation.
6. **Pacific DMCs have essentially no city-level open data.** Use
   national NSO and SPC PDH instead.
7. **License treatment is rarely explicit.** Default assumption:
   attribution required, noncommercial redistribution unclear, unless
   the portal publishes a license.
8. **Geoportal vs. data portal.** Jakarta, HCMC, and several others have
   separate geoportals (`jakartasatu.jakarta.go.id`,
   `portal.hcmgis.vn`) for GIS layers alongside tabular-data portals.
   For programs with spatial needs, check both.

### 12.5 Relevance per program

- **Program 1 (access-services).** Jakarta Satu, Bangkok BMA, Bengaluru
  IUDX, Delhi OGD, HCMGIS give sub-ADM1 resolution for clinic/school/
  market locations where city-level planning data is more complete
  than national.
- **Program 3 (air-monitoring).** City air-quality data (Jakarta, Delhi,
  Bangkok, Bengaluru) is a useful triangulation against national EMBs.
- **Program 4 (invisible urbanization).** **Highest-leverage program
  for city portals.** Building-permit, land-use, and settlement-pressure
  data in Jakarta Satu, Bengaluru IUDX, Bangkok BMA, Delhi, and Indian
  Smart Cities Mission portals is directly relevant.
- **Program 6 (coastal informal risk).** Bangkok BMA flood risk
  platform, Jakarta coastal data, Indian coastal Smart Cities Mission
  cities (Chennai, Mumbai, Kochi, Visakhapatnam).
- **Program 8 (flood market access).** Bangkok BMA is the reference
  implementation; Jakarta, Chennai, Mumbai have equivalents.
- **Program 11 (migration and displacement).** City-level registration,
  housing-assistance, and social-services data where published.
- **Program 13 (public service data quality).** **City-published
  facility lists are the third independent source** after OSM and
  national health registries. Triangulation is materially stronger for
  cities that publish their own facility inventories (Jakarta,
  Bengaluru, Bangkok, Taipei).
- **Program 17 (school-heat disruption).** DepEd / Dapodik / UDISE+
  already give school locations; city portals rarely add more unless
  they publish school-level operational data (rare).

---

## 13. Amendment log

- **2026-04-24** — Initial version. Twenty source categories cataloged,
  registration priorities set, license compatibility table added,
  reproducibility-pattern-per-access-model rules committed. Current-status
  verifications performed same date for OpenAQ v3, Google Earth Engine
  noncommercial tiers, Copernicus Data Space Ecosystem, NASA Earthdata
  Login, EM-DAT access, ACLED API, UN Comtrade, ILOSTAT, Meta HRSL, ACAG
  PM2.5 V6, MAP friction surface, WorldPop, Ookla Open Data, Overture Maps,
  KNOMAD remittance prices, and WRI Global Power Plant Database.
- **2026-04-25** — Added §10 "National-agency sources by ADB DMC region"
  covering all 50 ADB regional members: Pacific regional meta-sources
  (SPC SDD, PDH.stat, Pacific Data Hub, PDH Microdata Library, Pacific
  Environment Portal); 12 Pacific DMCs; 5 Central Asia DMCs; 3 Caucasus
  DMCs; 8 South Asia DMCs; 10 Southeast Asia DMCs; 4 East Asia DMCs; 5
  non-DMC regional members for comparative analysis; 10 DMC central
  banks; and access-pattern heuristics (§10.10). Verification performed
  2026-04-25 for 16 NSO portals. Known-gaps section (§9) updated to
  close Pacific and Central Asia/Caucasus entries and surface new gaps
  (sector-ministry portals, municipal open data, pre-2000 archives).
- **2026-04-25** — Added §11 "Sector-ministry and regulator portals":
  ASEAN meta-source (ASEANstats); 13 DMC health-ministry facility
  registries and HMIS (PHL NHFR, BGD DGHS Facility Registry, IDN
  SATUSEHAT, IND HMIS, PAK MoNHSR, NPL DoHS HMIS, LKA MoH, VNM MoH,
  KHM MoH, LAO MoH, MNG MoH, BTN MoH, Pacific via SPC); 7 DMC disaster
  management agencies (PHL NDRRMC/DROMIC, IDN BNPB DIBI, IND NDMA/NDEM,
  BGD DDM, PAK NDMA, NPL NDRRMA/BIPAD, Pacific PRIS); 10 DMC electricity
  regulators/utilities (IND CEA/NPP, IDN MEMR/ESDM, PHL DOE, BGD BPDB,
  PAK NEPRA/NTDC, VNM MOIT/EVN, LKA CEB/PUCSL, NPL NEA, MNG MOE, Pacific
  utilities); 6 DMC transport/PWD agencies (IND MoRTH/Gati Shakti, PHL
  DPWH, BGD RHD/LGED, IDN PUPR/Ina-Geoportal, PAK NHA, NPL DoR, VNM
  MoT); 7 DMC education ministries (PHL DepEd BEIS, IDN Dapodik, IND
  UDISE+, BGD BANBEIS, PAK NEAS, VNM MOET, NPL CEHRD); 6 DMC environment
  agencies (PHL DENR-EMB, IND CPCB/SAFAR, IDN KLHK, BGD DoE, PAK EPA,
  VNM VEA); 9 DMC meteorological agencies (PAGASA, IMD, BMKG, BMD, PMD
  with CDPC, NCHMF, DHM, Met Lk, Pacific via SPREP). Program-to-source
  direct recommendations for programs 1, 3, 5, 7, 8, 10, 13, 17.
  Verification run same date across 14 ministry portals.
- **2026-04-25** — Added §12 "Municipal and city-level open-data portals
  and national OGD platforms": 11 national OGD platforms (PHL, IND, IDN,
  THA, MYS, SGP, HKG, TAP, NPL, PAK, BGD); Pan-Asia Open Data Portal and
  HDX meta-aggregators; ~16 city portals (Jakarta, Bandung, Semarang,
  Surabaya, Bangkok, Taipei, HCMC, Hong Kong, Singapore, Delhi NCR,
  Bengaluru, Indian Smart Cities Mission cities [100], Dhaka city
  corporations, Kuala Lumpur, Philippine LGUs, Ulaanbaatar, Central
  Asian and Caucasus capitals, Pacific capitals); 8 regional city
  aggregators (Smart Cities Mission Data Portal, OpenCity India, IUDX,
  Pacific Data Hub city series, C40, ASEAN Smart Cities Network,
  UN-Habitat CPI, ADB CDIA). Program-to-source mapping for programs 1,
  3, 4, 6, 8, 11, 13, 17. Verification run same date across 14 city
  portals.
- **2026-04-29** — Added Google granular-data update: AlphaEarth Foundations /
  Satellite Embedding V1, Google Groundsource flood-event dataset, and Google
  Flood Forecasting API. Added `research/google-granular-data-upgrades.md` to
  keep Google Places / Maps Platform content out of persistent research
  databases and prioritize open Google Research / Earth Engine datasets.
