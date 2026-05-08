# Codex-operated research factory

This repository should work as a research factory, not as an autonomous truth
machine. Codex can generate and revise research packages quickly, but each
claim still has to pass the repository gates: public data, reproducible
scripts, cited literature, sensitivity checks, explicit limitations, and
human-final judgment before external submission.

## What the factory produces

Each program should eventually contain the same artifact set:

| Artifact | Purpose |
|---|---|
| `README.md` | Program status, headline, source map, and reproduce commands |
| `literature.md` | Tiered related-literature scan and marginal contribution |
| `pre-registration.md` | Question, exclusion rules, indicators, and decision rules |
| `scoring.md` | Constitution rubric score and promotion evidence |
| `coverage.md` | Country/source coverage and missingness disclosure |
| `results.md` | Main tables, charts, and plain-language finding |
| `sensitivity.md` | Robustness checks and alternate specifications |
| `limitations.md` | What the artifact cannot support |
| `review-internal.md` | Internal critique and required fixes |
| `review-external.md` | External-review target questions |
| `article.md` | Reader-facing article or paper draft |

Generated data belongs in `generated/`. Raw public-source caches belong in
`.cache/` only when the source license allows committed cache storage.

## Standard loop

1. **Frame the question.** Define the policy-relevant measurement gap and the
   exact unit of analysis.
2. **Scan the literature.** Separate established findings, known datasets,
   common methods, and the new contribution.
3. **Pre-register the method.** Write the indicator definitions, exclusions,
   transformations, and promotion thresholds before reading the result.
4. **Fetch public data.** Record source URL, license, retrieval date, version,
   and cache hash where applicable.
5. **Run a deterministic pipeline.** Produce `generated/*.json` and `*.csv`
   from committed scripts.
6. **Build charts and tables.** Prefer direct quantities over composite
   headlines. If a triage metric is unavoidable, label it as triage.
7. **Run sensitivity.** Test alternate denominators, thresholds, country
   inclusion rules, and stale-source risk.
8. **Red-team the claim.** Ask what would make the conclusion false, weaker,
   or merely descriptive.
9. **Publish the packet.** Sync the article, evidence links, references, and
   site route only after the gates pass.

## Publication ladder (added 2026-05-07)

**Principle.** A research result is finished when a reader at any depth —
peer reviewer, policy user, general reader, social — can find an honest
version of it that fits their attention budget. Each tier of the ladder
serves a distinct attention budget; together they discharge the program's
obligation to make its result legible to the audiences §1 names. A program
that produces only the deepest tier has not finished, because most of the
intended audiences cannot read it. A program that produces only the
shallowest tier has not finished, because the reader who wants to verify
cannot drill down. Honest summaries at every depth, linked, is the
finished state.

**Operationalization.** A program is not "done" until every tier below
exists. AI generates each tier deterministically from the same evidence
packet, in order. Each tier links back to the next deeper one so a reader
can drill from a tweet down to the committed script.

**Visualization rule.** Visualization is **per-program, not pre-built**.
Each program identifies the 1–2 visualizations its argument actually
needs (a choropleth, a Sankey of corridors, a small-multiples panel,
etc.) and those components are built when first needed and reused when a
later program needs them. Speculative viz libraries violate the
simplicity rule (CLAUDE.md "Doing tasks") and produce sites that look
generic; per-program viz produces sites that look like the work. Each
visualization should be defined by a Python code block (Quarto-rendered
on the slide deck and brief charts) and a matching React component (on
the program page), both reading the same generated CSV — so the same
chart appears at every reader-depth and cannot drift between tiers.

| Tier | Format | Length | Path | Audience |
|---|---|---|---|---|
| 1. Working paper | Markdown article | 2,000–6,000 words | `articles/{program-slug-or-cluster}.md` | Peer reviewer, methodological reader |
| 2. Program page | React page on the reporting site | n/a | `reporting-site/src/pages/Program{Name}.tsx` | Policy user navigating the lab site |
| 3. Brief | One-page summary | ~500 words, single chart | `articles/_brief/{slug}.md` | ADB-facing decision audience |
| 4. Blog post | Reader-facing narrative post | ~600–900 words | `articles/_blog/{slug}.md` | General development-economics reader |
| 5. Social card | Tweet-length summary + one chart | ≤ 280 chars + alt text | `articles/_social/{slug}.md` | Social distribution |
| 6. Slide deck | Markdown source built to `.pptx` | 8–15 slides | source `articles/_slides/{slug}.md`, built `reporting-site/public/programs/{slug}/{slug}-deck.pptx` | ADB internal presentation, country-team briefing, government counterpart meeting |
| 7. Evidence packet | Full reproducibility bundle | n/a | `reporting-site/public/programs/{slug}/` | Reviewer who wants to rerun |

**Slide-deck rule.**

*Principle.* The source of record for the deck is the markdown file under
`articles/_slides/`, not the `.pptx`. The `.pptx` is a built artifact,
regenerated deterministically from the markdown source on every publication
sync. `.pptx` is not text-diffable, so review and gate enforcement happen
on the markdown source — the same banned-words / DMC-framing / citation /
composite-headline gates that apply to other research artifacts apply to
the slide source. Charts on slides are generated by code blocks that read
the same committed CSVs the working paper reads; a slide's chart cannot
contain a number that the underlying script did not produce.

*Operationalization.* Build tool is **Quarto** (`quarto-cli`).

- Source: `articles/_slides/{slug}.md` (Quarto-flavored markdown with
  YAML frontmatter `format: pptx` and a `reference-doc:` line pointing
  at the ADB slide template once one exists).
- Build: `quarto render articles/_slides/{slug}.md --to pptx --output
  reporting-site/public/programs/{slug}/{slug}-deck.pptx` (added to
  publication-sync scripts).
- Charts on slides are written as Python code blocks that read the
  program's generated CSVs (e.g.
  `public-service-data-quality/generated/psdq-phl-admin3-poverty-context.csv`)
  and emit a matplotlib or plotnine figure. The same CSV the working
  paper cites is the same CSV the slide's chart loads. No hand-exported
  PNGs.
- Citations on slides use the same `references.bib` as the working
  paper. Quarto's pandoc backbone resolves them.
- Same Quarto source can also render `--to revealjs` for an HTML deck
  hosted at `/program/{slug}/deck` and `--to pdf` for archival. One
  source, three outputs. The publication ladder lists `.pptx` as the
  primary output; the others are optional.

The choice of Quarto rather than Marp or plain pandoc is itself a
principle-driven choice: only Quarto gives charts-from-code, native
`.pptx` editability, and multi-format output from one source — the three
properties needed for the slide tier to satisfy the ladder principle
("legibility at every reader's attention budget, drilling down to the
committed script") rather than just produce a visually acceptable deck.

Every tier carries the same maturity label and the same `attestation_chain`
preamble as the underlying evidence packet (§18.2 honest-labeling). The
brief, blog, and social tiers are AI-doable end-to-end; the working paper and
program page are AI-doable but should be reviewed by the owner before social
distribution.

A program counts as **finished for the current issue** only when all six
tiers exist and pass the five gates. A program counts as **human-final** only
when the §18.5 owner-only steps are also done.

## Review loop (added 2026-05-07; revised 2026-05-07 to add AI-only mode)

**Principle.** Every artifact must honestly state which review path produced
it; the label has to match the path. Review depth forms a monotonic ladder —
AI self-critique, AI second-opinion, owner spot-check, owner full review,
external reviewer — and a label at any rung implies every rung below it has
been done. AI-only paths cannot reach human-final because the labeling rule
forbids it (§18.2), not because AI is incapable of further iteration. The
choice of review path is therefore not a choice about quality of work; it is
a choice about which label the artifact is allowed to carry, which in turn
is what tells a reader how much trust the artifact has earned.

**Operationalization.** Once the publication ladder exists for a program,
the work enters the review loop. There are three review modes; the owner
picks per program. The mode chosen determines the artifact's
`attestation_chain` and label, and must be recorded honestly in the
program's README header per §18.2.

### Mode A — AI-only review (default under §18 ACTIVE)

The full review is done by AI: §9.1 self-review, §9.2 internal critique-pass
(AI argues against the artifact and answers each critique in writing), and
§9.3 red-team review (AI synthesizes objections from candidate institutions'
public methodological positions, with the §18.4 explicit non-claim quoted
verbatim). Optionally a separate AI agent (different model, different
session, or a specialist sub-agent like `code-reviewer`) does an additional
pass for independence.

1. AI publishes the full ladder (tiers 1–6).
2. AI runs §9.1 self-review and writes `review-internal.md`.
3. AI runs §9.2 critique-pass and appends responses.
4. AI runs §9.3 red-team synthesis and writes `review-external.md` with the
   §18.4 non-claim verbatim.
5. Optionally: AI dispatches the artifact to an independent AI agent for a
   second-opinion review; result appended to `review-external.md` clearly
   labeled "AI second-opinion review, independent session."
6. AI iterates on every critique it raised against itself. Default end-of-task
   hygiene runs each iteration (gates + build + browser-check + STATUS).
7. When AI cannot find a further substantive critique, the program reaches
   **"ai-first finished for current issue."** Move to the next program.

The artifact's `attestation_chain` stays `ai-first`. The label is honest:
this artifact has not been read by a human reviewer or by the owner. It
**cannot reach human-final** through this mode — that requires Mode C.

### Mode B — Spot-check review

The owner reads selected tiers (typically: working paper, program page, and
the limitations section) but defers the rest to AI self-review. Mode A's
steps 1–6 still run; the owner adds comments on whatever they read. AI
iterates on those comments plus its own critique-pass.

The artifact's `attestation_chain` is `ai-first; owner-spot-checked: tiers
{list}; date {YYYY-MM-DD}`. The label is honest: partial owner oversight,
not full owner review. Cannot reach human-final.

### Mode C — Full owner review (for human-final aspiration)

The owner reads each tier in order and writes comments. AI iterates on
every comment. Repeat until the owner says **final-final**. Combined with
the §18.5 owner-only steps (line-by-line paper reading, actual external
reviewer contact, internal review with Arturo, owner-signed commit), the
artifact can reach **human-final**.

### Choosing a mode

Default is Mode A. The owner picks Mode B or C in the program's README
header at the start of the loop. The mode can be upgraded mid-loop (A → B,
B → C) but never silently downgraded. A downgrade requires updating the
program's README and `attestation_chain`.

### Exit condition and program advancement

AI **never** advances to the next program just because the current one
looks finished. The exit condition depends on mode:

- **Mode A**: AI cannot find a further substantive self-critique, OR the
  owner explicitly defers the program with "OK to move on under Mode A."
- **Mode B**: spot-check tiers are owner-approved AND AI cannot find a
  further substantive self-critique on the rest.
- **Mode C**: owner says final-final.

If the owner does not respond within a session under any mode, AI continues
iterating on its own self-review until it converges or the owner returns.
Convergence under Mode A is a legitimate exit; under Modes B and C the
owner's word is required.

## How this changes the SR labels (note added 2026-05-07)

Programs that received the SR label under §18 by way of a single
composite-index screening run + ±50% sensitivity have been demoted back to
PP (Prepared Pipeline) — see `research/wip-register.md` and `CONSTITUTION.md`
§16 amendment of 2026-05-07. The artifacts are not deleted; they are
reclassified as starting material until the new program loop (publication
ladder + owner-review loop) is run on each. PSDQ remains the only program at
PR maturity and is the active flagship.

## Codex prompt to start a program

```text
Create a new research program package for <topic>. Use public data only.
First draft the research question, literature map, data-source plan,
pre-registration, and reproducibility plan. Do not write a headline claim
until the generated artifacts exist. Run the repository gates before marking
anything as Screening Result or Publication Ready.
```

## Factory commands

Create a new skeleton:

```bash
node scripts/new-program.mjs <slug> "<Program title>"
```

Run the common gates:

```bash
node scripts/check-citations.mjs
node scripts/check-composite-headline.mjs
node scripts/check-wip.mjs
node scripts/check-dmc-framing.mjs
node scripts/check-banned-words.mjs
node scripts/check-versions.mjs
```

Sync publication references:

```bash
node scripts/sync-references.mjs
```

## Where status lives

Use separate files for separate kinds of memory:

| File | Role |
|---|---|
| `research/STATUS.md` | Current focus, stage, next output, blockers, and handoff prompt |
| `research/wip-register.md` | Formal claim-maturity register and promotion history |
| `research/TODO-NEXT-SESSION.md` | Backlog of useful future work |
| `research/README.md` | Map of research-operations files |

Every substantial session should start by reading `research/STATUS.md` and
end by updating it if the focus, stage, next output, or blockers changed.

## Scale rule

Scaling means more standardized packages, not lower standards. A large backlog
is acceptable under Section 18 acceleration only if public labels stay honest:
Hypothesis, Program Prospectus, Screening Result, Publication Ready, Finished
for current issue, or Human-final accepted.

Codex is the operating engine for drafts, scripts, checks, and revisions. The
repository remains the engine of record because it preserves the evidence,
methods, generated artifacts, and governance history.
