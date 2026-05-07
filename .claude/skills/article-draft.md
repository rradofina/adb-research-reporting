# Skill: Draft a Research Article

## Purpose
Given a program slug + article kind, draft a publication-quality article
in the `pub.article` table with auto-cited indicator values that resolve
against `obs.*` at render time.

## Invocation
> "Draft a `<kind>` for program `<slug>` titled `<title>`. Audience: `<audience>`."

## Article kinds
- `blog` — 600–1,200 words, accessible language, single chart, public-facing
- `brief` — 1,500–2,500 words, ADB Brief style, policy-actionable, 1–2 charts; apply `adb-erdi-paper-framing.md`
- `working_paper` — 6,000–12,000 words, ADBI / ADB Economics Working Paper style, full methodology; apply `adb-erdi-paper-framing.md`
- `journal` — full draft for journal target named per `CONSTITUTION.md` §10.2
- `dataset_doc` — companion documentation for a Zenodo data deposit

## Steps
1. Read the program's `README.md`, `literature.md`, `scoring.md`,
   `results.md`, and `generated/` outputs.
2. If the article kind is `brief`, `working_paper`, or otherwise ADB-facing,
   apply `.claude/skills/adb-erdi-paper-framing.md` before drafting. Return
   the problem statement, key messages, evidence spine, caveat box, policy-use
   paragraph, and figure/table plan before full prose.
3. Identify the 3–7 most cite-worthy indicator values in the program.
   For each, generate an inline citation token of the form:
   `{{ind:<indicator_slug>|iso=<iso3>|year=<year>}}`.
4. Draft the article body in Markdown with citation tokens inline. The
   tokens resolve against `obs.country_value` / `obs.admin1_value` at
   render time — the rendered text is always fresh against the DB, but
   the published `pub.article_revision` snapshot is frozen.
5. INSERT into `pub.article` (status `draft`).
6. INSERT into `pub.article_indicator_citation` for every token.
7. INSERT into `pub.article_program` for the linked program.
8. INSERT into `pub.article_bib_citation` for every BibTeX key cited.
9. Author `pub.article_author` with the appropriate author order.
10. Return: article slug, indicator-citation count, BibTeX-citation count,
   and the URL where it will appear when promoted to `published`.

## Constraints
- Constitution §2.5: AI may draft prose but does not invent empirical
  numbers. Every numeric claim must resolve to an `obs.*` row.
- Constitution §14: banned words list — never use in articles.
- Constitution §13.3: framing is "measurement gap" / "observability gap"
  / "structural exposure" — never "country failing."
- ADB-facing drafts must include the issue being sold, source stack, unit of
  analysis, coverage, caveat ladder, figure/table source notes, and policy-use
  paragraph before conclusions.
- Constitution §10.4: a published article without internal review (per
  §9) must carry a "Not externally reviewed" label visible on first page.
- Constitution §9.3: publication-ready articles need ≥2 external red-team
  reviews logged in `pub.article_review`.

## Stopping criteria
- Draft fits the kind's word target.
- Every numeric claim has a citation token.
- Every method or external-paper reference has a BibTeX citation.

## What this skill does NOT do
- Does not promote `status` past `draft`. The owner advances through
  `internal_review` → `external_review` → `published` after review
  packets are complete.
- Does not mint a DOI. That is a Zenodo step initiated by the owner.
- Does not generate charts. Chart rendering is a separate concern
  (matplotlib / Plotly / etc., committed alongside the article body).
