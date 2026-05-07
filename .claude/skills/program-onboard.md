# Skill: Onboard a New Research Program

## Purpose
Given a program idea, scaffold the full Hypothesis-stage gate package:
folder, README, `literature.md`, `scoring.md`, `pipeline.ts` scaffold,
register row in `CONSTITUTION.md` §15, and entry in `research.program`.

## Invocation
> "Onboard a new program: slug `<slug>`, title `<title>`, domain `<domain>`."

## Steps
1. Create `<repo-root>/<slug>/` with subfolders `scripts/`, `generated/`, `.cache/`.
2. Author `<slug>/README.md` with the program template:
   - Research question
   - Why this is unconventional / marginal contribution
   - First testable claim (DRAFT — owner finalizes per §6.1)
   - Falsification condition (DRAFT)
   - Source stack (cross-reference `data-access-audit.md`)
   - Pilot DMCs
   - Metrics planned
   - Validation plan
   - Known weak points
3. Author `<slug>/literature.md` with the §4 originality protocol scaffold
   (search-record placeholder; invite the systematic-literature-scan
   skill).
4. Author `<slug>/scoring.md` with the §3.3 rubric (six criteria, AI-draft
   scores with rationale, sign-off table empty).
5. Author `<slug>/pipeline.ts` scaffold mirroring `public-service-data-quality/pipeline.ts`:
   pilot DMC config, type definitions, cache helper, TODO(owner-approval)
   per fetcher.
6. Insert a row in `CONSTITUTION.md` §15 Program Register.
7. Append a changelog entry under §16.
8. INSERT into `research.program` via Supabase (or note the SQL for the
   owner to run).
9. Do NOT advance the maturity label. AI cannot per `CLAUDE.md`.

## Constraints
- The first testable claim and falsification condition are AI-drafted
  with a clear "owner finalizes" label. Constitution §6.1 requires
  owner sign-off before any data is pulled.
- Scoring is AI-drafted; total must be ≥18 to pass §3.3 floor; owner
  reviews the six criteria.

## Output
A summary listing all files created with relative paths and line counts,
plus the SQL statement for the `research.program` INSERT.
