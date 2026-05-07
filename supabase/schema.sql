-- ADB Research — Supabase schema
--
-- Pattern: Supabase is a downstream query/collab layer.
-- Source of truth: scripts/ + .cache/ + generated/*.json in the repo.
-- This schema mirrors the generated artifacts; loaded by sync-to-supabase.py.
--
-- Per CONSTITUTION.md §11: byte-reproducibility comes from the repo, not this DB.
-- Treat tables here as a read-optimized projection.
--
-- Schemas:
--   research.*       — per-program panels and dimensions
--   research_meta.*  — provenance, source pins, sync log

CREATE SCHEMA IF NOT EXISTS research;
CREATE SCHEMA IF NOT EXISTS research_meta;

-- ===================================================================
-- Dimensions
-- ===================================================================

CREATE TABLE IF NOT EXISTS research.dim_dmc (
  iso3            TEXT PRIMARY KEY,
  iso2            TEXT,
  name            TEXT NOT NULL,
  subregion       TEXT,
  is_pacific      BOOLEAN,
  is_central_asia BOOLEAN,
  is_caucasus     BOOLEAN,
  is_south_asia   BOOLEAN,
  is_southeast_asia BOOLEAN,
  is_east_asia    BOOLEAN,
  is_landlocked   BOOLEAN
);

CREATE TABLE IF NOT EXISTS research.dim_program (
  id              INT PRIMARY KEY,
  slug            TEXT UNIQUE NOT NULL,
  title           TEXT NOT NULL,
  status          TEXT,
  summary         TEXT,
  has_artifact    BOOLEAN
);

-- ===================================================================
-- Provenance (research_meta)
-- ===================================================================

CREATE TABLE IF NOT EXISTS research_meta.source_pin (
  id              SERIAL PRIMARY KEY,
  source_key      TEXT NOT NULL,
  source_name     TEXT,
  source_url      TEXT,
  license         TEXT,
  retrieved_at    TIMESTAMPTZ,
  pinned_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  notes           TEXT
);

CREATE TABLE IF NOT EXISTS research_meta.sync_log (
  id              SERIAL PRIMARY KEY,
  table_name      TEXT NOT NULL,
  rows_loaded     INT NOT NULL,
  loaded_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  source_artifact TEXT,
  artifact_sha256 TEXT
);

-- ===================================================================
-- Per-program panels (one row per DMC unless otherwise noted)
-- Each table mirrors the JSON output schema in <program>/generated/
-- ===================================================================

-- Program 1 — Climate-adjusted access to services (ADM1-level, not DMC-level)
CREATE TABLE IF NOT EXISTS research.access_services_admin1 (
  iso3                TEXT NOT NULL,
  admin1_code         TEXT NOT NULL,
  admin1_name         TEXT,
  population          BIGINT,
  health_facilities   INT,
  schools             INT,
  markets             INT,
  total_services      INT,
  service_load_score  REAL,
  osm_completeness_risk_score REAL,
  access_stress_index REAL,
  bottleneck          TEXT,
  service_query_mode  TEXT,
  osm_timestamp       TIMESTAMPTZ,
  PRIMARY KEY (iso3, admin1_code)
);

-- Program 3 — Air pollution observability (per DMC)
CREATE TABLE IF NOT EXISTS research.air_monitoring_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  population          BIGINT,
  public_locations    INT,
  pm25_locations      INT,
  pm25_exposure_ugm3  REAL,
  pm25_above_who_guideline_5_ugm3 BOOLEAN,
  pm25_observability_gap_score REAL,
  pm25_observability_status TEXT,
  who_city_pm25_mean  REAL,
  who_highest_pm25_city TEXT,
  retrieved_at        TIMESTAMPTZ
);

-- Program 5 — Climate-health workdays
CREATE TABLE IF NOT EXISTS research.climate_health_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  emp_agri_pct        REAL,
  emp_industry_pct    REAL,
  outdoor_labor_share_pct REAL,
  pm25_exposure_ugm3  REAL,
  pm25_year           INT,
  urban_pop_pct       REAL,
  population_total    BIGINT,
  exposed_outdoor_millions REAL,
  workday_loss_pressure_index REAL
);

-- Program 7 — Disaster recovery lag (burden layer)
CREATE TABLE IF NOT EXISTS research.disaster_burden_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  total_events_2000_2025 INT,
  total_affected      BIGINT,
  total_deaths        BIGINT,
  total_damage_usd_adj NUMERIC,
  events_per_year     REAL,
  type_distribution   JSONB,
  biggest_event       JSONB,
  years_covered       INT
);

-- Program 9 — Food-price climate transmission (macro)
CREATE TABLE IF NOT EXISTS research.food_price_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  cpi_inflation_pct   REAL,
  cpi_year            INT,
  ag_imports_pct_merch REAL,
  food_production_index REAL,
  food_price_vulnerability REAL
);

-- Program 10 — Grid reliability under heat
CREATE TABLE IF NOT EXISTS research.grid_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  plant_count         INT,
  total_capacity_mw   REAL,
  top_fuel            TEXT,
  top_fuel_share      REAL,
  fuel_herfindahl     REAL,
  wdi_elec_access_pct REAL,
  wdi_elec_access_year INT,
  wdi_energy_use_kgoe_per_capita REAL,
  fuel_mix_capacity_mw JSONB
);

-- Program 11 — Migration & displacement (per DMC stock)
CREATE TABLE IF NOT EXISTS research.migration_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  immigrant_stock_2024 BIGINT,
  emigrant_stock_2024  BIGINT,
  net_migrant_stock_2024 BIGINT,
  top_origins         JSONB,
  top_destinations    JSONB
);

-- Program 12 — Port-hinterland trade friction
CREATE TABLE IF NOT EXISTS research.port_friction_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  lpi_overall         REAL,
  lpi_overall_year    INT,
  lpi_infrastructure  REAL,
  lpi_customs         REAL,
  imports_usd         NUMERIC,
  imports_usd_year    INT,
  friction_exposure_index REAL
);

-- Program 13 — Public service data quality (per ADM1, multi-DMC)
CREATE TABLE IF NOT EXISTS research.psdq_admin1 (
  iso3                TEXT NOT NULL,
  admin1_code         TEXT NOT NULL,
  admin1_name         TEXT,
  population_2020     BIGINT,
  osm_health          INT,
  registry_principal  INT,
  registry_clinical   INT,
  registry_all        INT,
  ratio_osm_to_principal REAL,
  ratio_osm_to_clinical REAL,
  ratio_osm_to_all    REAL,
  osm_per_100k        REAL,
  registry_principal_per_100k REAL,
  registry_clinical_per_100k REAL,
  osm_timestamp       TIMESTAMPTZ,
  registry_retrieved_at DATE,
  registry_source_url TEXT,
  PRIMARY KEY (iso3, admin1_code)
);

-- Program 14 — Remittance resilience
CREATE TABLE IF NOT EXISTS research.remittance_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  wdi_remittance_pct_gdp REAL,
  wdi_year            INT,
  rpw_period          TEXT,
  rpw_corridors_observed INT,
  rpw_firms_observed  INT,
  rpw_mean_cost_pct   REAL,
  rpw_median_cost_pct REAL,
  rpw_min_cost_pct    REAL,
  rpw_max_cost_pct    REAL,
  fragility_index     REAL
);

-- Program 14 — top expensive corridors (RPW)
CREATE TABLE IF NOT EXISTS research.remittance_corridor (
  source_iso3         TEXT NOT NULL,
  source              TEXT,
  dest_iso3           TEXT NOT NULL,
  dest                TEXT,
  n_quotes            INT,
  mean_cost_pct       REAL,
  median_cost_pct     REAL,
  min_cost_pct        REAL,
  max_cost_pct        REAL,
  PRIMARY KEY (source_iso3, dest_iso3)
);

-- Program 15 — School heat disruption
CREATE TABLE IF NOT EXISTS research.school_heat_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  primary_pupil_teacher_ratio REAL,
  ptr_year            INT,
  pop_0_14_pct        REAL,
  pop_total           BIGINT,
  children_0_14_millions REAL,
  annual_tasmax_1995_2014_celsius REAL,
  school_heat_pressure_index REAL
);

-- Program 16 — Social protection shock coverage
CREATE TABLE IF NOT EXISTS research.social_protection_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  sp_coverage_pct     REAL,
  sp_coverage_year    INT,
  findex_account_pct  REAL,
  findex_year         INT,
  poverty_headcount_215_pct REAL,
  poverty_year        INT,
  poverty_gap_pct     REAL,
  shock_payment_readiness_gap REAL
);

-- Program 17 — Water stress × crop concentration
CREATE TABLE IF NOT EXISTS research.water_crop_dmc (
  iso3                TEXT PRIMARY KEY REFERENCES research.dim_dmc(iso3),
  water_withdrawal_pct_resources REAL,
  water_withdrawal_year INT,
  agri_land_pct       REAL,
  arable_land_pct     REAL,
  cereal_yield_kg_per_ha REAL,
  rural_population_pct REAL,
  water_crop_pressure_index REAL
);

-- ===================================================================
-- Cross-program convenience view (rebuild after each sync)
-- ===================================================================

CREATE OR REPLACE VIEW research.v_vulnerability_matrix AS
SELECT
  d.iso3,
  d.name AS country,
  d.subregion,
  ah.pm25_observability_gap_score        AS air_obs,
  ch.workday_loss_pressure_index         AS climate_health,
  db.events_per_year                     AS disaster_evts_yr,
  fp.food_price_vulnerability            AS food_price,
  g.fuel_herfindahl                      AS grid_concentration,
  m.emigrant_stock_2024                  AS emigrant_stock,
  pf.friction_exposure_index             AS port_friction,
  rm.fragility_index                     AS remittance_fragility,
  sh.school_heat_pressure_index          AS school_heat,
  sp.shock_payment_readiness_gap         AS sp_readiness_gap,
  wc.water_crop_pressure_index           AS water_crop
FROM research.dim_dmc d
LEFT JOIN research.air_monitoring_dmc ah USING (iso3)
LEFT JOIN research.climate_health_dmc ch USING (iso3)
LEFT JOIN research.disaster_burden_dmc db USING (iso3)
LEFT JOIN research.food_price_dmc fp USING (iso3)
LEFT JOIN research.grid_dmc g USING (iso3)
LEFT JOIN research.migration_dmc m USING (iso3)
LEFT JOIN research.port_friction_dmc pf USING (iso3)
LEFT JOIN research.remittance_dmc rm USING (iso3)
LEFT JOIN research.school_heat_dmc sh USING (iso3)
LEFT JOIN research.social_protection_dmc sp USING (iso3)
LEFT JOIN research.water_crop_dmc wc USING (iso3);

-- ===================================================================
-- Read access for the website (anon role)
-- ===================================================================

GRANT USAGE ON SCHEMA research TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA research TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA research_meta TO anon, authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA research GRANT SELECT ON TABLES TO anon, authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA research_meta GRANT SELECT ON TABLES TO anon, authenticated;
