-- ============================================================
-- THE LUMINOSITY GAP
-- Database Schema for Nighttime Lights vs MPI Analysis
--
-- All data sourced from public APIs:
--   - OPHI Global MPI (ophi.org.uk) — CC BY 4.0
--   - VIIRS Nighttime Lights (eogdata.mines.edu) — CC BY 4.0
--   - World Bank PIP API (pip.worldbank.org)
--   - ADB Key Indicators (kidb.adb.org/api)
--   - UN SDG Database (unstats.un.org/sdgs)
-- ============================================================

-- Enable PostGIS for geospatial queries
create extension if not exists postgis;

-- ============================================================
-- COUNTRIES
-- Core reference table for ADB developing member countries
-- ============================================================
create table countries (
  id serial primary key,
  iso3 char(3) unique not null,        -- ISO 3166-1 alpha-3
  iso2 char(2) unique,                 -- ISO 3166-1 alpha-2
  name text not null,
  adb_region text,                     -- e.g., 'Central and West Asia', 'Southeast Asia'
  is_adb_member boolean default false,
  centroid geography(Point, 4326),     -- country centroid for map display
  bbox jsonb,                          -- bounding box [west, south, east, north]
  created_at timestamptz default now()
);

create index idx_countries_iso3 on countries(iso3);
create index idx_countries_adb_region on countries(adb_region);

-- ============================================================
-- SUBNATIONAL REGIONS
-- Subnational admin units (provinces, states, etc.)
-- Matches OPHI MPI subnational disaggregation
-- ============================================================
create table subnational_regions (
  id serial primary key,
  country_id integer references countries(id) on delete cascade,
  name text not null,
  admin_level integer default 1,       -- 1 = province/state, 2 = district
  ophi_region_code text,               -- OPHI's subnational identifier
  centroid geography(Point, 4326),
  created_at timestamptz default now(),
  unique(country_id, name, admin_level)
);

create index idx_subnational_country on subnational_regions(country_id);

-- ============================================================
-- NIGHTTIME LIGHTS
-- Aggregated VIIRS radiance data by country and year
-- Source: Earth Observation Group (eogdata.mines.edu)
-- ============================================================
create table nighttime_lights (
  id serial primary key,
  country_id integer references countries(id) on delete cascade,
  subnational_id integer references subnational_regions(id) on delete set null,
  year integer not null check (year >= 2012 and year <= 2030),

  -- Radiance metrics (nanoWatts/cm²/sr)
  mean_radiance double precision,      -- average radiance across area
  median_radiance double precision,
  sum_radiance double precision,       -- total radiance (proxy for total economic activity)
  lit_area_km2 double precision,       -- area with detectable light
  total_area_km2 double precision,     -- total land area
  lit_area_pct double precision,       -- % of area that is lit

  -- Growth metrics (computed)
  yoy_radiance_change double precision, -- year-over-year % change in mean radiance

  source_url text,                     -- direct link to source data file
  created_at timestamptz default now(),
  unique(country_id, subnational_id, year)
);

create index idx_ntl_country_year on nighttime_lights(country_id, year);
create index idx_ntl_subnational on nighttime_lights(subnational_id, year);

-- ============================================================
-- MPI DATA
-- Global Multidimensional Poverty Index by dimension
-- Source: OPHI / UNDP (ophi.org.uk)
-- ============================================================
create table mpi_data (
  id serial primary key,
  country_id integer references countries(id) on delete cascade,
  subnational_id integer references subnational_regions(id) on delete set null,
  survey_year integer not null,         -- year of household survey

  -- Headline MPI
  mpi_value double precision,           -- MPI value (0-1)
  headcount_ratio double precision,     -- % of population that is MPI-poor (H)
  intensity double precision,           -- average deprivation intensity among poor (A)

  -- DIMENSION: Health (weight: 1/3)
  health_contribution double precision, -- % contribution to overall MPI
  d_nutrition double precision,         -- deprivation rate: nutrition
  d_child_mortality double precision,   -- deprivation rate: child mortality

  -- DIMENSION: Education (weight: 1/3)
  education_contribution double precision,
  d_years_schooling double precision,   -- deprivation rate: years of schooling
  d_school_attendance double precision, -- deprivation rate: school attendance

  -- DIMENSION: Living Standards (weight: 1/3)
  living_std_contribution double precision,
  d_cooking_fuel double precision,      -- deprivation rate: cooking fuel
  d_sanitation double precision,        -- deprivation rate: sanitation
  d_drinking_water double precision,    -- deprivation rate: drinking water
  d_electricity double precision,       -- deprivation rate: electricity
  d_housing double precision,           -- deprivation rate: housing
  d_assets double precision,            -- deprivation rate: assets

  source_url text,
  created_at timestamptz default now(),
  unique(country_id, subnational_id, survey_year)
);

create index idx_mpi_country_year on mpi_data(country_id, survey_year);
create index idx_mpi_subnational on mpi_data(subnational_id);

-- ============================================================
-- INCOME POVERTY (for comparison with MPI)
-- Source: World Bank PIP API
-- ============================================================
create table income_poverty (
  id serial primary key,
  country_id integer references countries(id) on delete cascade,
  year integer not null,

  -- International poverty lines
  headcount_190 double precision,       -- % below $1.90/day (2011 PPP)
  headcount_320 double precision,       -- % below $3.20/day
  headcount_550 double precision,       -- % below $5.50/day
  headcount_685 double precision,       -- % below $6.85/day (2017 PPP)
  headcount_365 double precision,       -- % below $3.65/day (2017 PPP)

  gini_index double precision,          -- Gini coefficient

  -- National poverty line
  national_headcount double precision,  -- % below national poverty line

  source_url text,
  created_at timestamptz default now(),
  unique(country_id, year)
);

create index idx_income_country_year on income_poverty(country_id, year);

-- ============================================================
-- DEVELOPMENT INDICATORS
-- Additional socioeconomic indicators from ADB/World Bank/UN
-- ============================================================
create table development_indicators (
  id serial primary key,
  country_id integer references countries(id) on delete cascade,
  year integer not null,
  indicator_code text not null,         -- e.g., 'GDP_PC_PPP', 'HDI', 'LIFE_EXP'
  indicator_name text not null,
  value double precision,
  unit text,                            -- e.g., 'constant 2017 USD', 'years', 'index'
  source text,                          -- 'ADB', 'World Bank', 'UNDP', 'UN'
  source_url text,
  created_at timestamptz default now(),
  unique(country_id, year, indicator_code)
);

create index idx_dev_country_year on development_indicators(country_id, year);
create index idx_dev_indicator on development_indicators(indicator_code);

-- ============================================================
-- LUMINOSITY GAP ANALYSIS (pre-computed)
-- The core research output: correlation between NTL and each MPI dimension
-- ============================================================
create table luminosity_gap (
  id serial primary key,
  country_id integer references countries(id) on delete cascade,
  analysis_level text not null check (analysis_level in ('national', 'subnational', 'regional')),

  -- Time alignment
  ntl_year integer not null,
  mpi_survey_year integer not null,

  -- Overall correlation
  corr_ntl_mpi double precision,        -- Pearson r: NTL vs overall MPI

  -- Per-dimension correlations (THE GAP)
  corr_ntl_health double precision,     -- NTL vs health dimension
  corr_ntl_education double precision,  -- NTL vs education dimension
  corr_ntl_living_std double precision, -- NTL vs living standards dimension

  -- Per-indicator correlations
  corr_ntl_nutrition double precision,
  corr_ntl_child_mortality double precision,
  corr_ntl_schooling double precision,
  corr_ntl_attendance double precision,
  corr_ntl_electricity double precision,
  corr_ntl_sanitation double precision,
  corr_ntl_water double precision,
  corr_ntl_cooking_fuel double precision,
  corr_ntl_housing double precision,
  corr_ntl_assets double precision,

  -- The "gap" metric: difference between best-predicted and worst-predicted dimension
  max_dimension_gap double precision,   -- living_std_corr - health_corr (typically)
  gap_description text,                 -- human-readable summary

  -- Statistical metadata
  n_observations integer,
  r_squared_overall double precision,
  methodology_notes text,

  created_at timestamptz default now(),
  unique(country_id, analysis_level, ntl_year, mpi_survey_year)
);

create index idx_gap_country on luminosity_gap(country_id);

-- ============================================================
-- RESEARCH LOG
-- Every AI prompt, data fetch, and analysis step documented
-- For full reproducibility
-- ============================================================
create table research_log (
  id serial primary key,
  step_number integer not null,
  category text not null check (category in ('prompt', 'data_fetch', 'analysis', 'visualization', 'decision')),
  title text not null,
  description text,
  prompt_text text,                     -- the actual AI prompt used (if applicable)
  ai_response_summary text,            -- summary of AI response
  data_source text,                    -- API/URL used
  code_snippet text,                   -- code executed
  output_summary text,                 -- what was produced
  timestamp timestamptz default now()
);

create index idx_log_step on research_log(step_number);
create index idx_log_category on research_log(category);

-- ============================================================
-- VIEWS for common queries
-- ============================================================

-- Country-level summary: NTL + MPI + income poverty aligned
create or replace view country_summary as
select
  c.iso3,
  c.name as country_name,
  c.adb_region,
  ntl.year,
  ntl.mean_radiance,
  ntl.lit_area_pct,
  m.mpi_value,
  m.headcount_ratio as mpi_headcount,
  m.health_contribution,
  m.education_contribution,
  m.living_std_contribution,
  ip.headcount_685 as income_poverty_685,
  ip.gini_index,
  lg.corr_ntl_health,
  lg.corr_ntl_education,
  lg.corr_ntl_living_std,
  lg.max_dimension_gap
from countries c
left join nighttime_lights ntl on c.id = ntl.country_id and ntl.subnational_id is null
left join mpi_data m on c.id = m.country_id and m.subnational_id is null
left join income_poverty ip on c.id = ip.country_id and ip.year = ntl.year
left join luminosity_gap lg on c.id = lg.country_id and lg.analysis_level = 'national';

-- The "bright but deprived" view: countries with high lights but high health deprivation
create or replace view bright_but_deprived as
select
  c.name as country_name,
  c.iso3,
  ntl.mean_radiance,
  m.mpi_value,
  m.health_contribution,
  m.d_nutrition,
  m.d_child_mortality,
  m.d_electricity,
  round(cast(m.health_contribution / nullif(m.living_std_contribution, 0) as numeric), 2) as health_to_living_ratio
from countries c
join nighttime_lights ntl on c.id = ntl.country_id and ntl.subnational_id is null
join mpi_data m on c.id = m.country_id and m.subnational_id is null
where ntl.mean_radiance > 5  -- relatively bright
  and m.health_contribution > 0.3  -- but high health deprivation share
order by m.health_contribution desc;
