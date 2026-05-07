-- =====================================================================
-- ADB Research — Schema v2 (long-term, scalable, publishing-aware)
--
-- Design principles (informed by karpathy/autoresearch — "one GPU, one
-- file, one metric" — adapted to "one schema, one indicator-table per
-- granularity, one source registry, one publishing layer"):
--
--  1. Geography is global. ADB DMC is a flag, not the universe.
--  2. Every numeric value lives in a single long-format observation table
--     keyed on (indicator, geo, year). Per-program "wide" panels are
--     materialized views, not source-of-truth.
--  3. Every observation traces to a source.retrieval row (URL + sha256).
--  4. Articles, blogs, working papers cite indicators by id. The audit
--     trail "which value is in which paragraph of which paper" is a SQL
--     join, not a manual exercise.
--  5. The repo (.cache + scripts + generated) remains the byte-
--     reproducibility floor. This DB is a downstream projection.
--
-- Schemas:
--   geo.*       — countries, admin1, regions
--   source.*    — datasets, retrievals, citations
--   obs.*       — observation facts (long format)
--   research.*  — programs (the H/PP/SR/PR register)
--   pub.*       — articles, blogs, working papers, reviews
--   research_meta.*  — sync log + housekeeping
--
-- Convention: lower_snake_case throughout. UUIDs only where
-- entities cross system boundaries (articles, retrievals); else
-- BIGSERIAL. ISO3 stays as the natural key for countries.
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE SCHEMA IF NOT EXISTS geo;
CREATE SCHEMA IF NOT EXISTS source;
CREATE SCHEMA IF NOT EXISTS obs;
CREATE SCHEMA IF NOT EXISTS research;        -- already exists from v1
CREATE SCHEMA IF NOT EXISTS pub;
CREATE SCHEMA IF NOT EXISTS research_meta;   -- already exists

-- =====================================================================
-- geo.* — global geographic dimensions
-- =====================================================================

CREATE TABLE IF NOT EXISTS geo.country (
  iso3              TEXT PRIMARY KEY,
  iso2              TEXT,
  un_m49            INT,
  name              TEXT NOT NULL,
  official_name     TEXT,
  continent         TEXT,
  un_subregion      TEXT,
  un_intermediate_region TEXT,
  -- Rich groupings (boolean flags for fast filtering)
  is_adb_member     BOOLEAN DEFAULT FALSE,
  is_adb_dmc        BOOLEAN DEFAULT FALSE,
  is_adb_pacific    BOOLEAN DEFAULT FALSE,
  is_asean          BOOLEAN DEFAULT FALSE,
  is_oecd           BOOLEAN DEFAULT FALSE,
  is_eu             BOOLEAN DEFAULT FALSE,
  is_g20            BOOLEAN DEFAULT FALSE,
  is_lldc           BOOLEAN DEFAULT FALSE,    -- landlocked developing
  is_sids           BOOLEAN DEFAULT FALSE,    -- small island developing
  is_ldc            BOOLEAN DEFAULT FALSE,    -- least developed
  -- Income classification (latest WB)
  wb_income_group   TEXT,
  -- Geographic
  centroid_lat      REAL,
  centroid_lon      REAL,
  area_km2          REAL,
  population_2024   BIGINT,
  -- Provenance
  retrieved_at      TIMESTAMPTZ DEFAULT NOW(),
  notes             TEXT
);
CREATE INDEX IF NOT EXISTS idx_country_dmc ON geo.country(is_adb_dmc) WHERE is_adb_dmc;
CREATE INDEX IF NOT EXISTS idx_country_subregion ON geo.country(un_subregion);

CREATE TABLE IF NOT EXISTS geo.admin1 (
  -- Composite key keeps ISO3 + the country's own admin code
  iso3              TEXT NOT NULL REFERENCES geo.country(iso3),
  admin1_code       TEXT NOT NULL,            -- e.g. PH-00, BD-A
  admin1_name       TEXT NOT NULL,
  admin1_alt_codes  JSONB,                    -- HASC, GADM, PSA, etc.
  centroid_lat      REAL,
  centroid_lon      REAL,
  area_km2          REAL,
  population_year   INT,
  population        BIGINT,
  population_source TEXT,
  geoboundaries_release TEXT,
  PRIMARY KEY (iso3, admin1_code)
);
CREATE INDEX IF NOT EXISTS idx_admin1_iso ON geo.admin1(iso3);

CREATE TABLE IF NOT EXISTS geo.region (
  id                BIGSERIAL PRIMARY KEY,
  slug              TEXT UNIQUE NOT NULL,     -- 'adb-pacific', 'asean', 'south-asia'
  name              TEXT NOT NULL,
  kind              TEXT NOT NULL,            -- 'adb', 'un_m49', 'wb_lending', 'custom'
  parent_slug       TEXT REFERENCES geo.region(slug)
);

CREATE TABLE IF NOT EXISTS geo.region_member (
  region_id         BIGINT NOT NULL REFERENCES geo.region(id) ON DELETE CASCADE,
  iso3              TEXT NOT NULL REFERENCES geo.country(iso3) ON DELETE CASCADE,
  PRIMARY KEY (region_id, iso3)
);

-- =====================================================================
-- source.* — datasets, retrievals, citations
-- =====================================================================

CREATE TABLE IF NOT EXISTS source.dataset (
  id                BIGSERIAL PRIMARY KEY,
  slug              TEXT UNIQUE NOT NULL,     -- 'wdi', 'rpw-q1-2025', 'doh-nhfr-v2', 'em-dat-2024-04-24'
  name              TEXT NOT NULL,
  publisher         TEXT,                     -- World Bank, DOH, CRED, etc.
  url               TEXT NOT NULL,
  api_endpoint      TEXT,
  license           TEXT,                     -- 'CC BY 4.0', 'CC BY-NC-SA 4.0', etc.
  license_url       TEXT,
  access_model      CHAR(1) CHECK (access_model IN ('A','B','C','D','E','F')),
                                              -- per data-access-audit.md taxonomy
  vintage           TEXT,                     -- "Q1 2025", "v6.GL.02.04", "2024-04-24"
  description_md    TEXT,
  notes             TEXT,
  added_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source.retrieval (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  dataset_id        BIGINT NOT NULL REFERENCES source.dataset(id),
  retrieved_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  retrieved_by      TEXT,                     -- script or human identifier
  url_resolved      TEXT,                     -- the actual URL hit (may include params)
  http_status       INT,
  bytes             BIGINT,
  sha256            TEXT,                     -- of cached payload
  cache_path        TEXT,                     -- relative to repo root
  notes             TEXT
);
CREATE INDEX IF NOT EXISTS idx_retrieval_dataset ON source.retrieval(dataset_id);
CREATE INDEX IF NOT EXISTS idx_retrieval_at ON source.retrieval(retrieved_at DESC);

CREATE TABLE IF NOT EXISTS source.bib_entry (
  id                BIGSERIAL PRIMARY KEY,
  bibtex_key        TEXT UNIQUE NOT NULL,     -- mirrors references.bib
  bibtex_type       TEXT NOT NULL,            -- 'article', 'techreport', etc.
  authors           TEXT,
  title             TEXT NOT NULL,
  journal           TEXT,
  year              INT,
  volume            TEXT,
  number            TEXT,
  pages             TEXT,
  doi               TEXT,
  url               TEXT,
  abstract          TEXT,
  retrieved_at      TIMESTAMPTZ
);

-- =====================================================================
-- research.* — programs (the §15 register, machine-readable)
-- =====================================================================

CREATE TABLE IF NOT EXISTS research.program (
  id                INT PRIMARY KEY,
  slug              TEXT UNIQUE NOT NULL,
  title             TEXT NOT NULL,
  status            TEXT NOT NULL CHECK (status IN ('H','PP','SR','PR','Ret')),
  scoring_total     INT,
  summary           TEXT,
  testable_claim    TEXT,
  falsification     TEXT,
  owner             TEXT,
  notes_md          TEXT,
  has_artifact      BOOLEAN DEFAULT FALSE,
  href              TEXT,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS research.program_status_event (
  id                BIGSERIAL PRIMARY KEY,
  program_id        INT NOT NULL REFERENCES research.program(id),
  status_from       TEXT,
  status_to         TEXT NOT NULL,
  changed_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  changed_by        TEXT,
  rationale_md      TEXT
);

-- =====================================================================
-- obs.* — long-format observation facts (the heart of the system)
-- =====================================================================

CREATE TABLE IF NOT EXISTS obs.indicator (
  id                BIGSERIAL PRIMARY KEY,
  slug              TEXT UNIQUE NOT NULL,     -- 'remit.fragility_index', 'grid.fuel_herfindahl'
  program_id        INT REFERENCES research.program(id),
  domain            TEXT NOT NULL,            -- 'remittance', 'grid', 'air_quality'
  name              TEXT NOT NULL,
  description_md    TEXT,
  unit              TEXT,                     -- '%', 'kg/ha', 'µg/m³', 'index 0-100'
  source_dataset_id BIGINT REFERENCES source.dataset(id),
  methodology_md    TEXT,                     -- formula or pipeline note
  is_composite      BOOLEAN DEFAULT FALSE,
  is_triage         BOOLEAN DEFAULT FALSE,    -- per Constitution §6.4
  added_at          TIMESTAMPTZ DEFAULT NOW(),
  added_by          TEXT
);
CREATE INDEX IF NOT EXISTS idx_indicator_program ON obs.indicator(program_id);
CREATE INDEX IF NOT EXISTS idx_indicator_domain ON obs.indicator(domain);

-- Country-level observations
CREATE TABLE IF NOT EXISTS obs.country_value (
  indicator_id      BIGINT NOT NULL REFERENCES obs.indicator(id) ON DELETE CASCADE,
  iso3              TEXT NOT NULL REFERENCES geo.country(iso3),
  year              INT NOT NULL,
  value_num         DOUBLE PRECISION,
  value_text        TEXT,                     -- for categorical / status values
  retrieval_id      UUID REFERENCES source.retrieval(id),
  PRIMARY KEY (indicator_id, iso3, year)
);
CREATE INDEX IF NOT EXISTS idx_cv_iso ON obs.country_value(iso3, year);

-- ADM1-level observations
CREATE TABLE IF NOT EXISTS obs.admin1_value (
  indicator_id      BIGINT NOT NULL REFERENCES obs.indicator(id) ON DELETE CASCADE,
  iso3              TEXT NOT NULL,
  admin1_code       TEXT NOT NULL,
  year              INT NOT NULL,
  value_num         DOUBLE PRECISION,
  value_text        TEXT,
  retrieval_id      UUID REFERENCES source.retrieval(id),
  PRIMARY KEY (indicator_id, iso3, admin1_code, year),
  FOREIGN KEY (iso3, admin1_code) REFERENCES geo.admin1(iso3, admin1_code)
);
CREATE INDEX IF NOT EXISTS idx_a1v_iso ON obs.admin1_value(iso3, admin1_code);

-- Bilateral / corridor observations (migration, remittance, trade)
CREATE TABLE IF NOT EXISTS obs.corridor_value (
  indicator_id      BIGINT NOT NULL REFERENCES obs.indicator(id) ON DELETE CASCADE,
  source_iso3       TEXT NOT NULL REFERENCES geo.country(iso3),
  dest_iso3         TEXT NOT NULL REFERENCES geo.country(iso3),
  year              INT NOT NULL,
  period_label      TEXT NOT NULL DEFAULT '', -- "2025_1Q" or '' if annual-only
  value_num         DOUBLE PRECISION,
  value_text        TEXT,
  meta              JSONB,                    -- firm, payment-instrument, etc.
  retrieval_id      UUID REFERENCES source.retrieval(id),
  PRIMARY KEY (indicator_id, source_iso3, dest_iso3, year, period_label)
);
CREATE INDEX IF NOT EXISTS idx_corr_src ON obs.corridor_value(source_iso3);
CREATE INDEX IF NOT EXISTS idx_corr_dst ON obs.corridor_value(dest_iso3);

-- =====================================================================
-- pub.* — publishing layer
-- =====================================================================

CREATE TABLE IF NOT EXISTS pub.author (
  id                BIGSERIAL PRIMARY KEY,
  slug              TEXT UNIQUE NOT NULL,     -- 'raymond-adofina'
  full_name         TEXT NOT NULL,
  affiliation       TEXT,
  orcid             TEXT,
  email_public      TEXT,
  bio_md            TEXT,
  added_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pub.article (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug              TEXT UNIQUE NOT NULL,     -- URL-safe
  kind              TEXT NOT NULL CHECK (kind IN ('blog','brief','working_paper','journal','poster','dataset_doc')),
  status            TEXT NOT NULL CHECK (status IN ('draft','internal_review','external_review','published','withdrawn')),
  title             TEXT NOT NULL,
  subtitle          TEXT,
  abstract_md       TEXT,
  body_md           TEXT,                     -- writing happens here
  doi               TEXT,
  zenodo_id         TEXT,
  external_url      TEXT,
  cover_image_url   TEXT,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW(),
  published_at      TIMESTAMPTZ,
  withdrawn_at      TIMESTAMPTZ,
  withdrawn_reason  TEXT,
  -- tagging for global reach
  geographies       TEXT[] DEFAULT ARRAY[]::TEXT[],  -- ['ADB-DMC', 'global', 'south-asia']
  topics            TEXT[] DEFAULT ARRAY[]::TEXT[],  -- ['poverty', 'climate', 'measurement']
  is_featured       BOOLEAN DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_article_status ON pub.article(status);
CREATE INDEX IF NOT EXISTS idx_article_kind ON pub.article(kind);
CREATE INDEX IF NOT EXISTS idx_article_published_at ON pub.article(published_at DESC) WHERE status = 'published';

CREATE TABLE IF NOT EXISTS pub.article_author (
  article_id        UUID NOT NULL REFERENCES pub.article(id) ON DELETE CASCADE,
  author_id         BIGINT NOT NULL REFERENCES pub.author(id),
  author_order      INT NOT NULL,
  is_corresponding  BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (article_id, author_id)
);

CREATE TABLE IF NOT EXISTS pub.article_program (
  article_id        UUID NOT NULL REFERENCES pub.article(id) ON DELETE CASCADE,
  program_id        INT NOT NULL REFERENCES research.program(id),
  PRIMARY KEY (article_id, program_id)
);

-- The audit trail: every cited indicator value
CREATE TABLE IF NOT EXISTS pub.article_indicator_citation (
  id                BIGSERIAL PRIMARY KEY,
  article_id        UUID NOT NULL REFERENCES pub.article(id) ON DELETE CASCADE,
  indicator_id      BIGINT NOT NULL REFERENCES obs.indicator(id),
  iso3              TEXT,                     -- if scoped to a country
  admin1_code       TEXT,                     -- if scoped to ADM1
  year              INT,
  inline_token      TEXT,                     -- {{ind:remit.fragility_index|iso=KGZ}} or similar
  context_md        TEXT,                     -- the surrounding paragraph snippet
  cited_at          TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_aic_article ON pub.article_indicator_citation(article_id);
CREATE INDEX IF NOT EXISTS idx_aic_indicator ON pub.article_indicator_citation(indicator_id);

CREATE TABLE IF NOT EXISTS pub.article_bib_citation (
  article_id        UUID NOT NULL REFERENCES pub.article(id) ON DELETE CASCADE,
  bib_entry_id      BIGINT NOT NULL REFERENCES source.bib_entry(id),
  context_md        TEXT,
  PRIMARY KEY (article_id, bib_entry_id)
);

CREATE TABLE IF NOT EXISTS pub.article_revision (
  id                BIGSERIAL PRIMARY KEY,
  article_id        UUID NOT NULL REFERENCES pub.article(id) ON DELETE CASCADE,
  revision_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  revision_label    TEXT,                     -- 'v1.0', 'pre-print', 'final'
  body_md           TEXT,                     -- frozen snapshot at this point
  abstract_md       TEXT,
  status_at_rev     TEXT,
  notes             TEXT
);

CREATE TABLE IF NOT EXISTS pub.article_review (
  id                BIGSERIAL PRIMARY KEY,
  article_id        UUID NOT NULL REFERENCES pub.article(id) ON DELETE CASCADE,
  review_kind       TEXT NOT NULL CHECK (review_kind IN ('self','internal','red_team','journal','external')),
  reviewer_name     TEXT,
  reviewer_affiliation TEXT,
  review_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  decision          TEXT CHECK (decision IN ('accept','revise','reject','recommend','noted')),
  comments_md       TEXT,
  response_md       TEXT,
  is_public         BOOLEAN DEFAULT FALSE
);

-- Tags: free-form taxonomy for blog discovery
CREATE TABLE IF NOT EXISTS pub.tag (
  slug              TEXT PRIMARY KEY,
  name              TEXT NOT NULL,
  description       TEXT
);

CREATE TABLE IF NOT EXISTS pub.article_tag (
  article_id        UUID NOT NULL REFERENCES pub.article(id) ON DELETE CASCADE,
  tag_slug          TEXT NOT NULL REFERENCES pub.tag(slug) ON DELETE CASCADE,
  PRIMARY KEY (article_id, tag_slug)
);

-- =====================================================================
-- Convenience views in public schema (anon REST surface)
-- =====================================================================

CREATE OR REPLACE VIEW public.countries AS
  SELECT * FROM geo.country ORDER BY iso3;

CREATE OR REPLACE VIEW public.programs AS
  SELECT id, slug, title, status, scoring_total, summary,
         has_artifact, href, owner, updated_at
  FROM research.program ORDER BY id;

CREATE OR REPLACE VIEW public.indicators AS
  SELECT i.id, i.slug, i.domain, i.name, i.unit,
         i.is_composite, i.is_triage,
         p.slug AS program_slug, p.title AS program_title,
         d.slug AS source_slug, d.name AS source_name, d.license
  FROM obs.indicator i
  LEFT JOIN research.program p ON p.id = i.program_id
  LEFT JOIN source.dataset d ON d.id = i.source_dataset_id;

CREATE OR REPLACE VIEW public.observations_country AS
  SELECT cv.indicator_id, i.slug AS indicator_slug, i.unit,
         cv.iso3, c.name AS country, c.un_subregion,
         cv.year, cv.value_num, cv.value_text
  FROM obs.country_value cv
  JOIN obs.indicator i ON i.id = cv.indicator_id
  JOIN geo.country c ON c.iso3 = cv.iso3;

CREATE OR REPLACE VIEW public.observations_admin1 AS
  SELECT av.indicator_id, i.slug AS indicator_slug, i.unit,
         av.iso3, av.admin1_code, a.admin1_name,
         av.year, av.value_num, av.value_text
  FROM obs.admin1_value av
  JOIN obs.indicator i ON i.id = av.indicator_id
  JOIN geo.admin1 a ON a.iso3 = av.iso3 AND a.admin1_code = av.admin1_code;

CREATE OR REPLACE VIEW public.observations_corridor AS
  SELECT cv.indicator_id, i.slug AS indicator_slug, i.unit,
         cv.source_iso3, sc.name AS source_country,
         cv.dest_iso3, dc.name AS dest_country,
         cv.year, cv.period_label, cv.value_num, cv.meta
  FROM obs.corridor_value cv
  JOIN obs.indicator i ON i.id = cv.indicator_id
  JOIN geo.country sc ON sc.iso3 = cv.source_iso3
  JOIN geo.country dc ON dc.iso3 = cv.dest_iso3;

CREATE OR REPLACE VIEW public.articles AS
  SELECT a.id, a.slug, a.kind, a.status, a.title, a.subtitle,
         a.abstract_md, a.doi, a.zenodo_id, a.external_url,
         a.geographies, a.topics, a.is_featured,
         a.published_at, a.created_at, a.updated_at,
         (SELECT array_agg(au.full_name ORDER BY aa.author_order)
            FROM pub.article_author aa
            JOIN pub.author au ON au.id = aa.author_id
            WHERE aa.article_id = a.id) AS authors
  FROM pub.article a
  WHERE a.status = 'published'
  ORDER BY a.published_at DESC NULLS LAST;

CREATE OR REPLACE VIEW public.article_audit AS
  SELECT
    a.slug AS article_slug, a.title, a.kind, a.status,
    aic.iso3, aic.admin1_code, aic.year, aic.inline_token,
    i.slug AS indicator_slug, i.name AS indicator_name, i.unit,
    p.slug AS program_slug,
    d.slug AS source_slug, d.license
  FROM pub.article a
  JOIN pub.article_indicator_citation aic ON aic.article_id = a.id
  JOIN obs.indicator i ON i.id = aic.indicator_id
  LEFT JOIN research.program p ON p.id = i.program_id
  LEFT JOIN source.dataset d ON d.id = i.source_dataset_id;

GRANT USAGE ON SCHEMA geo, source, obs, research, pub, research_meta TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA geo TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA source TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA obs TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA research TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA pub TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA research_meta TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon, authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA geo, source, obs, research, pub, research_meta
  GRANT SELECT ON TABLES TO anon, authenticated;

-- Notify PostgREST so new public-schema views are reachable immediately
NOTIFY pgrst, 'reload schema';
