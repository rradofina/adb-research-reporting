# CLAUDE.md

This repository produces research under a written constitution. AI assistants
working here are bound by it.

## Governing documents

Before assisting with any task in this repo or any program folder under it, an
AI assistant must have read and must continue to respect the operating stack in
`AGENTS.md`:

1. `CLAUDE.md` — operating rules, hard walls, and end-of-task hygiene.
2. `research/JUDGMENT.md` — how to choose the highest-leverage move.
3. `research/DESIGN.md` — how findings are presented on public surfaces.
4. `research/factory.md` — program loop, publication ladder, review modes.
5. `CONSTITUTION.md` — allowed claims, methods, ethics, taste, and §18.
6. `research/STATUS.md` and the active program's `{program}/STATUS.md`.

Additional standing standards still apply where relevant:

- `luminosity-gap/docs/REPRODUCIBILITY.md` — artifact standards.
- `luminosity-gap/docs/AI_TRANSPARENCY.md` — AI-assistance disclosure.
- Project-local skills in `.codex/skills/` and `.claude/skills/` when a task
  matches their scope.

The Constitution and this file set the hard floor: public data, traceability,
review gates, hard walls, ethics, and §18 labels do not bend. `JUDGMENT` and
`DESIGN` guide choices inside that floor. If session instructions contradict
the stack, raise the contradiction with the human owner before proceeding.

## Operating mode

`CONSTITUTION.md` §18 — AI-First Operating Mode — is **ACTIVE** as of
2026-04-25. While §18 is ACTIVE, AI executes gate-actions previously
reserved to the human owner, with every artifact honestly labeled
`attestation_chain: ai-first`. To revert, the owner flips §18's
status line in a commit titled `constitution: revert §18 AI-first mode`.

## Default end-of-task hygiene (added 2026-05-07)

**Principle.** A change is not done until the verifications that would catch
its likely failure modes have run. Reporting a task as done while leaving its
own checks unrun pushes the cost of catching a regression onto the next
session or onto the owner — which is more expensive than the verification
itself. The verification is therefore part of the task, not a follow-on.

**Operationalization.** When AI has just made a substantive change, run the
following autonomously, without asking. Bundle them in a single verification
pass at the end and report the results compactly.

| Trigger | Action |
|---|---|
| Edited code or markdown under a program folder | Re-run any pipeline script touched, regenerate the evidence packet, refresh the public-site copy via `node scripts/sync-evidence.mjs` and `node scripts/sync-references.mjs` |
| Edited any research artifact, article, or governance file | Run all five gates (`check-banned-words`, `check-dmc-framing`, `check-citations`, `check-composite-headline`, `check-wip`) |
| Edited an evidence-review artifact or its evidence register (§2.7 track) | Run the factory gates in order from `review-factory/gates/`: `verify_citations.py` (must exit 0), `resolve_fulltext.py`, `locate_estimates.py`, `apply_locators.py`, `validate_register.py`. A number without a **confirmed** locator may sit in the register; it may not enter a headline, abstract, table, figure, annotated bibliography, or synthesis sentence. Screen-derived locators are provisional and do not grant citability (§2.7 rule 2) |
| Edited any file under `reporting-site/` or any file the site reads | Run `cd reporting-site && npm run build` to confirm the production bundle still compiles |
| Edited a public surface (program page, article, evidence page, home page) | Browser-check at desktop (1280px) and mobile (375px); confirm zero console errors and zero horizontal-overflow at mobile |
| Substantive change to focus, stage, blocker, or verification status | Update the active `{program}/STATUS.md`; update `research/STATUS.md` only if the active flagship, operating mode, queue, or default review mode changed; set `Last updated` to today where edited |
| Any commit intended for a production push | From the repository root, run `npx vercel pull --yes --environment=production` and then `node scripts/verify-vercel-production.mjs`. The repository-owned gate must exit 0 before pushing; a standalone incremental `npm run build` does not satisfy this release gate. On Linux/CI, also run `npx vercel build --prod` and require exit 0. |

**Production-push rule.** Do not push a production-bound commit while the
Vercel production gate is failing. The local gate uses the linked Vercel
project's pulled production settings, performs a clean locked install, runs the
production build with production environment values, and validates the route
manifests. This makes project-root, framework detection, dependency resolution,
environment, and output behavior explicit before a cost-bearing deployment. A
raw `vercel build --prod` is additionally mandatory on Linux/CI. Vercel's local
Next output assembler has a Windows path-separator defect for nested static App
Router routes, so Windows release work uses the repository gate rather than
waiving or remotely testing a failing check. If a Git-triggered deployment
still fails despite the gate, inspect that deployment's Vercel build log,
repair the mismatch, rerun the full gate, and only then push the fix.

The next section lists the **hard walls** that genuinely require owner action
and should pause work, vs. soft barriers that are part of normal AI work.

## Hard walls vs. soft barriers (added 2026-05-07)

**Principle.** Pause for the owner only when proceeding would commit
something the owner alone can give: their identity, their attestation, their
money, or a third-party action only they can take. Otherwise, the step is
part of the work — asking only slows the owner down without giving them a
real choice. Asking too often is its own form of opacity, because it shifts
decisions out of the audit trail and into chat.

**Operationalization.**

**Hard walls — pause and ask the owner.** AI cannot get around these without
breaking the Constitution.

- Source files behind a Cloudflare browser challenge or paywall (PSA SAE was
  the canonical example).
- API access requiring an account or key on the owner's identity (SATUSEHAT,
  India HMIS, Earth Engine OAuth, Google Cloud, Zenodo, GitHub auth on the
  owner's account).
- Emailing or otherwise contacting an external reviewer (forbidden under
  §18.4 explicit non-claim).
- Human-final attestation (§18.5) — every step of it: line-by-line paper
  reading by the owner, real internal review by an owner-designated reviewer,
  owner-signed commit.
- Any change to `CONSTITUTION.md` §18 itself (follow §16 amendment procedure).

**Soft barriers — these are part of the work, do not stop to ask.**

- Running the gates after editing.
- Building the site after editing.
- Browser-checking a UI change.
- Updating `research/STATUS.md` after substantive work.
- Regenerating a generated artifact after the script that produced it changed.
- Demoting a maturity label that no longer reflects the artifact (this is an
  honesty correction, not a promotion; promotion remains gated).
- Choosing the simplest defensible method (§6.3) without owner ratification
  when no method is currently committed.
- Adding a Constitution clause reference to the header of a new script
  (always permitted, always desirable).

The above is the operational instantiation of the principle at the top of
this section. When a new edge case arises that is not in the table, decide
by the principle, not by analogy to a row.

## Default research-factory loop

The default working style is **one flagship program at a time**. Unless the
owner explicitly asks for a broad sweep, do not spread effort thinly across
many programs. Pick the current highest-leverage program and iterate until it
has a standout evidence package, clear reader-facing article, reproducible
pipeline, strong limitations section, and passing gates.

At session open, read the boards and choose a move from
`research/JUDGMENT.md` §4. State the active flagship, stage, move, and reason
before making substantive changes. "Deepen evidence" is not the default; it
has to beat claim reshaping, publishing, critique, presentation, or rotation.

For each focused program, loop through:

1. **Source upgrade.** Look for better public datasets, fresher versions,
   higher-resolution units, licenses, and retrieval timestamps.
2. **Literature upgrade.** Verify the related literature, method precedent,
   and marginal contribution. Do not rely on plausible summaries without
   source-grounding.
3. **Method upgrade.** Pre-register assumptions, exclusions, denominators,
   transformations, and sensitivity variants before changing the headline.
4. **Pipeline upgrade.** Make every empirical number come from committed
   scripts and generated artifacts, never from model memory.
5. **Critique upgrade.** Red-team the result, write down what would weaken
   it, and revise the claim until it is honest.
6. **Publication upgrade.** Improve the article, charts, evidence page, and
   UI hooks so a reader can understand the result without trusting the AI.
7. **Gate upgrade.** Run the deterministic checks and update status labels
   only when the artifact actually satisfies the gate.

Move to the next program only when the current program is either finished for
the current issue, blocked by a specific external dependency, or explicitly
deprioritized by the owner. The factory workflow lives in
`research/factory.md`; use it as the operating checklist.

At the start of each session, read `research/STATUS.md` and state the active
program, stage, and next output before making substantive changes. At the end
of each substantial session, update `research/STATUS.md` if the focus, stage,
next output, blocker list, or verification status changed.

## Operating rules under §18 ACTIVE

These rules are AI-permitted under §18:

- **Literature review finalization (§5.2).** AI completes the systematic
  Tier-A/B/C scan, fetches each cited paper from its DOI, summarizes
  the main result section, and finalizes `literature.md`. The
  attestation in the commit message reads
  *"Lit attest under §18 AI-first: AI completed Tier-A/B/C scan and read
  each cited paper's main-result section"* — never *"I have read
  line-by-line"* without further qualification.
- **Pre-registration freeze (§6.1, §6.2).** AI freezes
  `pre-registration.md` §10 with the AI signature line and the
  upcoming commit hash. The frozen pre-registration is binding for the
  next pipeline run.
- **Claim-maturity promotions (§7.2).** AI applies labels in
  `CONSTITUTION.md` §15 and `research/wip-register.md` when the gate
  artifacts are complete and pass the deterministic checks in
  `scripts/`. The promotion commit's message names the gate (e.g.
  `promote PSDQ to PR under §18: gate artifacts complete; ai-first attestation`).
- **Self-review and internal review (§9.1, §9.2).** AI writes both
  the self-review and a critique-pass internal review under
  `review-internal.md`. The critique-pass deliberately argues against
  the artifact; the response addresses each critique in writing.
- **Red-team synthesis (§9.3 under §18.4).** AI populates
  `review-external.md` with synthesized objections from named
  candidate institutions' published methodological positions, citing
  specific papers in `references.bib` for each objection. The file
  carries the §18.4 explicit non-claim verbatim: *"No individual
  reviewer was contacted under §18. The objections above are
  AI-synthesized from each institution's public methodological stance,
  not actual reviewer feedback."*
- **Program register updates (§15).** AI adds new programs and
  promotes existing ones in `CONSTITUTION.md` §15 and
  `research/wip-register.md`.

These rules remain non-suspendable under §18 (the
"non-suspendable preserved set"):

- **No empirical numbers from AI.** Every number traces to a committed
  script hitting a public source.
- **Sensitivity at ±50% (§6.6).** A deterministic computation, not an
  attestation. Always run.
- **Permanent-archive minting (§10.3, self-hosted default since 2026-04-26).**
  AI mints the permanent archive at `/program/{slug}/evidence` plus
  `/archives/{slug}-{date}.zip` deterministically as part of a normal
  commit. Optional Zenodo deposition remains owner-only because it
  uses the owner's third-party Zenodo account credentials.
- **Reproducibility from clean clone (§11).** Manifest, versions,
  per-row retrieval timestamps. No exceptions under §18.
- **Public data only (§2.1).** §18 does not unlock private data.
- **Auditable end-to-end (§2.2).** §18 does not weaken the audit trail.
- **Composite indices are triage only (§6.4).** Never headline.
- **Citations by BibTeX key (§5.3).** No bare URLs in research outputs.
- **Banned words (§14).** Never use the §14 list.
- **DMC framing (§13.3).** Measurement gap / coverage gap / observability gap.
- **Ethics in full (§13).** Personal-identifier discipline, policy-impact
  caution, fairness in DMC framing, author attribution.
- **Honest labeling (§18.2).** Every §18 artifact carries
  `attestation_chain: ai-first` in its frontmatter / YAML preamble.
  The reporting site, every `results.md`, every article, and the
  Zenodo metadata surfaces this label prominently. Silently producing
  an `ai-first` artifact without the label is a §18.2 violation.

## Stop and ask

Stop and ask the human owner before proceeding only when:

- The task would touch a non-suspendable rule (the preserved set above).
- The task would require impersonating the owner to a third-party
  identity provider (Zenodo, GitHub auth on the owner's account, email
  to a named external reviewer, etc.).
- The task would change `CONSTITUTION.md` §18 itself. Follow §16
  amendment procedure.

## Scope: code vs. research

This file binds research conduct across the whole repository. Code-specific
guidance for the Next.js app lives in `luminosity-gap/AGENTS.md` and applies
in addition (not instead) when working inside that subdirectory.

## Owner

Repository owner and program owner: Raymond Adofina.
Amendments to this file follow `CONSTITUTION.md` §16.
