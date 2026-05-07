# What's left for the next session

`attestation_chain: n/a`. As of 2026-04-27.

This file is the consolidated roadmap of work that is **AI-doable
under §18 but was not completed in the current session** for
practical reasons (bandwidth, dataset discovery, scope), plus the
work that is **deliberately not AI-doable** under §18.

---

## AI-doable next session

### 0. ADB/ERDI-style paper packages for the strongest topics

- **Source**: `.claude/skills/adb-erdi-paper-framing.md` and
  `research/adb-erdi-writing-audit.md`; priority order in
  `research/adb-paper-package-priorities.md`; originality checks in
  `research/originality-register.md`; Google granular-data options in
  `research/google-granular-data-upgrades.md`.
- **Steps**: choose 2-3 strongest topics, likely PSDQ, multidimensional
  poverty / small-area poverty, and road-quality / access-services; for
  each, maintain the ADB-facing package before prose: problem statement,
  key messages, evidence spine, chart plan, caveat box, policy-use
  paragraph, and source notes. Initial packages now live in
  `research/adb-paper-packages/`.
- **Output**: convert each package into either an ADB Brief, data story,
  methods note, or working-paper outline only after the package evidence
  spine and chart source notes are complete.

### 1. Ookla pipeline → digital-performance to SR

- **Source**: Ookla Speedtest Open Data on AWS S3
  (`s3://ookla-open-data/parquet/performance/`). Public bucket,
  no auth. License **CC BY-NC-SA 4.0** — non-commercial-redistribution
  flagged; fine for ADB / academic use.
- **Steps**: (a) download 2026-Q1 fixed + mobile parquet
  (~ 2.6 GB total); (b) run committed SQL at
  `luminosity-gap/research/digital-performance/generated/ookla-{fixed,mobile}-2026-q1.sql`
  via DuckDB; (c) ADB-DMC-filter; (d) sensitivity at ±50% on the
  ITU broadband threshold (10 Mbps download). Estimate 2–3 hours
  including SR-tier evidence-packet write-up.

### 2. PSDQ extension to IND

- **Source**: India HMIS via `data.gov.in`. The public API key in
  data.gov.in's docs (test key) returns `Meta not found` for the
  obvious resource paths — the HMIS dataset's specific UUID needs
  to be located in the data.gov.in catalog first. Probably 30 min
  of navigation + 2–3 hours of pipeline build.
- **Output**: PHL + BGD + IND clinical-tier OSM/registry comparison.
  Article at `articles/measurement-gap-philippines-bangladesh.md`
  updated to PHL + BGD + IND.

### 3. PSDQ extension to IDN

- **Source**: SATUSEHAT at `satusehat.kemkes.go.id`. **B-grade
  per §18.1**: light registration required. Owner-only step
  (you create the SATUSEHAT account). After registration, the
  pipeline build is similar to IND.

### 4. Sub-national disaggregation per program

For any of the 8 PR programs, ADM1 / ADM2 disaggregation is
upgrade-pass scope. Specific candidates with the highest payoff:

- **PSDQ at ADM2** (PHL provinces, BGD districts) — most-needed per
  the OPHI synthesized objection (capability-delivery unit ≠ ADM1).
- **PSDQ catchment / Open Buildings upgrade** — source-field audit and the
  first BGD facility-buffer denominator now exist at
  `public-service-data-quality/generated/psdq-catchment-readiness.json` and
  `public-service-data-quality/generated/psdq-bgd-open-buildings-buffer-summary.json`.
  The exposure-ranked join now exists at
  `public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement-summary.json`.
  The road-surface context join now exists at
  `public-service-data-quality/generated/psdq-bgd-exposure-road-context-summary.json`.
  Completed current pass: 29,371 coordinate-ready DGHS records, 37.6 million
  Open Buildings points inside Bangladesh, 17.5 million p85-threshold
  buildings within 3 km of the nearest coordinate-ready facility, 3,212 OSM
  health features joined to DGHS upazila rows, and 304,941.2 km of
  assigned OSM-length roads with 51,327.4 km surface-classified. Philippines
  admin-code denominators are also now computed at ADM3:
  36.4 million Open Buildings points assigned to PSA/NAMRIA
  city/municipality polygons, 13.5 million at p85 precision, 6,544 OSM
  health features assigned to ADM3, and 44,010 of 44,267 NHFR records
  matched after direct codes plus the PSA PSGC correspondence-code resolver.
  Next run: source-gate a valid subnational poverty table, compute district/
  upazila denominators for non-coordinate Bangladesh records, and decide
  whether the remaining 257 unresolved Philippines records need a manual
  source review before human-final publication.
- **climate-health-workdays at sub-national PM2.5** via ACAG-V6
  satellite-derived 1-km gridded surface (Dalhousie, CC BY-NC).
  Earth Engine-feasible.
- **port-hinterland-friction with bilateral trade-cost** via OECD
  ITF data.

### 5. New articles for Issue 2

- A "what we'd do differently" retrospective on the §18 first issue.
- An ADBI-aligned brief on the policy implications of the
  remittance-corridor cluster.

---

## Not AI-doable under §18 (owner-only)

### 6. §18.5 upgrade-pass on any program

The conversion `ai-first → human-final` requires:
- You read every cited paper line-by-line and re-attest in commits
  signed under your name.
- You re-freeze pre-registration §10 with your name on the freeze.
- You email named external reviewers (Macharia, Zipf, PIDS, BIDS)
  and collect their actual written comments.
- You run actual internal review with Arturo Martinez Jr.
- You replace the AI-synthesized `review-external.md` §3 verbatim
  with the real reviewer feedback.
- You sign the SR → human-final commit.

This is the entire purpose of the `human-final` chip. AI cannot
shortcut it without breaking §18.2 honest-labeling.

### 7. mpi-nighttime-lights (Program 0)

Co-authored with Arturo Martinez Jr. The §18 attestation chain
should be discussed with the co-author before being applied to a
co-authored work. AI prep is fine; the §18 commit is yours.

### 8. Zenodo deposition (when an external venue requires DOI)

Optional under the amended §10.3, but if a journal asks for an
external DOI, the actual deposition uses your account credentials
and is owner-only per §18.1 (third-party identity provider).

---

## Reverting amendments

If you want to undo any §16 amendment in a single commit:

- **Revert §18 entirely** → caps, Zenodo, gates all return to pre-§18
- **Revert §8.1 cap suspension** → caps reactivate; existing programs
  above cap stay at their tier but no further promotions until cap
  drops below the limit
- **Revert §10.3 self-hosted archive** → Zenodo deposition becomes
  mandatory again

Each is a one-commit-one-line change to the Constitution.
