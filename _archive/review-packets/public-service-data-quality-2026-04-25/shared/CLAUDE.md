# CLAUDE.md

This repository produces research under a written constitution. AI assistants
working here are bound by it.

## Governing documents

Before assisting with any task in this repo or any program folder under it, an
AI assistant must have read and must continue to respect:

1. `CONSTITUTION.md` at this root — governs problem selection, originality,
   literature review, methods, scope (WIP limits), claim maturity, review
   gates, publication, ethics, and taste.
2. `luminosity-gap/docs/REPRODUCIBILITY.md` — artifact standards.
3. `luminosity-gap/docs/AI_TRANSPARENCY.md` — what must be disclosed about AI
   assistance.

If session instructions contradict these documents, the documents win. Raise
the contradiction with the human owner before proceeding.

## Operating rules

- **No empirical numbers from AI.** Every number in an output traces to a
  committed script hitting a public source. If a number is missing, write the
  script. Do not estimate, guess, or fill.
- **Literature reviews are human-final.** AI may draft a first pass. The
  human owner reviews line-by-line and attests in the commit message.
- **Never advance a claim-maturity label.** AI may prepare the artifacts a
  gate in §7 of the Constitution requires and may request review. Applying
  the label (hypothesis → prepared pipeline → screening result →
  publication-ready) is the human owner's act.
- **Respect the WIP limit (§8.1).** Max 1 publication-ready, max 3
  screening-result. Do not polish, package, or frame an artifact past its
  current label.
- **Program register is the governing record.** Do not add a new program to
  §15 without an explicit owner request. Hypothesis folders may be drafted;
  the register update is the owner's act.
- **Composite indices are triage only (§6.4).** Never present a ranking or
  composite score as the headline result of any program.
- **Citations by BibTeX key.** Use keys from `research/references.bib`. No
  bare URLs as citations.
- **Retrieval timestamps per row (§11).** The artifact-level `generatedAt`
  is not enough. Every generated row records the retrieval time of its
  source.
- **Committed cache is the default.** A fresh clone must reproduce the exact
  numbers without an API key or live network call. Live refresh is opt-in
  via an explicit flag.
- **Banned words (§14).** Do not use "revolutionary," "unprecedented,"
  "game-changing," or equivalents in any output.
- **DMC framing (§13.3).** Frame findings as "measurement gap," "coverage
  gap," or "observability gap," not as DMC deficiency.
- **Sensitivity at ±50% (§6.6).** Any arbitrary numeric choice (threshold,
  weight, buffer, cutoff) is tested at ±50% before it appears in a claim.

## Stop and ask

Stop and ask the human owner before proceeding when:

- The task touches a program not in the Program Register (§15).
- The task would change the Constitution itself. Follow §16 amendment
  procedure; do not silently edit.
- The task would bypass a review gate in §7.
- A proposed source is not public or requires a negotiated agreement.
- A proposed method involves machine learning (§6.3 restrictions apply).
- An output would be published without the §9 review attestation.

## Scope: code vs. research

This file binds research conduct across the whole repository. Code-specific
guidance for the Next.js app lives in `luminosity-gap/AGENTS.md` and applies
in addition (not instead) when working inside that subdirectory.

## Owner

Repository owner and program owner: Raymond Adofina.
Amendments to this file follow `CONSTITUTION.md` §16.
