-- Public-schema proxy views for the website.
--
-- The `research` schema is the canonical store. Supabase REST exposes only
-- `public` and `graphql_public` by default; these views surface the research
-- panels under stable public-schema names so the anon key can read them
-- without any dashboard configuration.
--
-- All views are read-only by construction (the underlying tables are not
-- modified through them).

CREATE OR REPLACE VIEW public.research_programs AS
  SELECT * FROM research.dim_program ORDER BY id;

CREATE OR REPLACE VIEW public.research_dmcs AS
  SELECT * FROM research.dim_dmc ORDER BY iso3;

CREATE OR REPLACE VIEW public.vulnerability_matrix AS
  SELECT * FROM research.v_vulnerability_matrix;

CREATE OR REPLACE VIEW public.access_services_admin1 AS
  SELECT * FROM research.access_services_admin1;

CREATE OR REPLACE VIEW public.air_monitoring AS
  SELECT * FROM research.air_monitoring_dmc;

CREATE OR REPLACE VIEW public.climate_health AS
  SELECT * FROM research.climate_health_dmc;

CREATE OR REPLACE VIEW public.disaster_burden AS
  SELECT * FROM research.disaster_burden_dmc;

CREATE OR REPLACE VIEW public.food_price AS
  SELECT * FROM research.food_price_dmc;

CREATE OR REPLACE VIEW public.grid_concentration AS
  SELECT * FROM research.grid_dmc;

CREATE OR REPLACE VIEW public.migration_stock AS
  SELECT * FROM research.migration_dmc;

CREATE OR REPLACE VIEW public.port_friction AS
  SELECT * FROM research.port_friction_dmc;

CREATE OR REPLACE VIEW public.psdq_admin1 AS
  SELECT * FROM research.psdq_admin1;

CREATE OR REPLACE VIEW public.remittance AS
  SELECT * FROM research.remittance_dmc;

CREATE OR REPLACE VIEW public.remittance_corridor AS
  SELECT * FROM research.remittance_corridor;

CREATE OR REPLACE VIEW public.school_heat AS
  SELECT * FROM research.school_heat_dmc;

CREATE OR REPLACE VIEW public.social_protection AS
  SELECT * FROM research.social_protection_dmc;

CREATE OR REPLACE VIEW public.water_crop AS
  SELECT * FROM research.water_crop_dmc;

CREATE OR REPLACE VIEW public.sync_log AS
  SELECT * FROM research_meta.sync_log ORDER BY loaded_at DESC;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon, authenticated;
