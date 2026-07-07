# Codex-operated research factory

This repository should work as a research factory, not as an autonomous truth
machine. Codex can generate and revise research packages quickly, but each
claim still has to pass the repository gates: public data, reproducible
scripts, cited literature, sensitivity checks, explicit limitations, and
human-final judgment before external submission.

This manual defines the *steps*. `research/JUDGMENT.md` defines *how to
choose among them* and is read first; `research/DESIGN.md` defines how
results are presented. The factory's output is **claims a reader can trust
and understand** — artifacts, scripts, and gates are the receipts, never
the product.

## What progress means

A session advanced the factory only if the claim moved, the claim changed
shape honestly, a reader-facing surface improved, or a kill/defer/rotate
decision was recorded (`research/JUDGMENT.md` §1). Producing another
committed artifact against an unmoved blocker is not progress and must not
be reported as "last completed" work in the boards as if it were.

## Stopping rule and dead ends

The stopping rule in `research/JUDGMENT.md` §2 is part of this loop, not
an exception to it: after two passes leave the same claim-enabling counts
at zero, the third session must reshape the claim, publish the documented
absence as the finding (§2.6 of the Constitution treats null results as
legitimate outputs — for a measurement-gap lab they are often the *core*
output), or write a five-line blocker note and rotate. A systematic search
that finds nothing, with sources and retrieval recorded, is a completed
piece of evidence about observability — package it that way rather than
treating it as a corridor toward a claim the public record cannot support.

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

## Data-first hook triage

**Principle.** A program earns attention only when public data reveal a
specific, visual, non-generic measurement problem. The factory should not begin
by producing a polished essay around a broad topic. It should begin by finding
the data object that makes the topic legible: a map, corridor network, scatter,
ranked gap, small multiple, timeline, source-disagreement table, or comparable
visual structure. The research question is then reverse-designed from what the
data can honestly show.

**Operationalization.** Before a new or revived program enters the full
standard loop, run a hook triage:

1. **Find the public data object.** Name the dataset, source institution,
   access route, license, unit of analysis, period, and retrieval path.
2. **Build the rough visual first.** Use a committed script to produce the
   simplest chart/table/map that exposes the structure. This may be ugly; it
   must be traceable.
3. **Ask the hook question.** What is visible here that the conventional data
   view misses? What is the decision problem? What is the exact unit where the
   gap appears?
4. **Reverse-design the research frame.** Write the question, contribution,
   method, caveat, and publication plan around the observed data structure, not
   around the initial topic label.
5. **Ditch or defer weak hooks.** If the best visual is only a country ranking,
   a composite leaderboard, a generic trend line, or a topic summary, write a
   short defer note and move on. Do not spend publication-ladder effort trying
   to make a weak hook look important.

Hook triage is exploratory. It may inspect public data and build screening
artifacts, but it does not authorize a headline claim, maturity promotion, or
publication-ready language. The first testable claim, falsification condition,
source notes, limitations, sensitivity checks, and evidence packet still have
to be written before the result can leave the screening lane.

### New-topic creation mode

Use this mode when the owner asks to create or refactor research topics rather
than deepen the current flagship.

1. **Separate repair from creation.** Existing-program repair hooks can be
   useful, but they are not new topics unless they introduce a new evidence
   question or source object.
2. **Require a source object per topic.** Every candidate must name the public
   dataset, unit, period or expected vintage, access route, likely license,
   and source caveat before it receives a rank.
3. **Require a visual object per topic.** Every candidate must name the first
   chart, map, matrix, network, small multiple, or source-disagreement table.
   Topics without a visual object stay in brainstorming notes, not in the hook
   bank.
4. **Run sprints outside program folders first.** Store exploratory new-topic
   scripts and outputs under `research/topic-sprints/` until a hook earns a
   full program package. This prevents a rough sprint from being mistaken for
   a maturity label or publication surface.
5. **Promote only by evidence.** A new-topic L2 sprint can promote a hook to a
   program prospectus candidate only when a committed script produces a rough
   table or visual and the sprint note records source sanity, visual QA,
   caveats, and a kill/defer decision.
6. **Keep failures.** If a hook fails, record why. A failed data pull, generic
   visual, blocked license, or uninteresting chart is useful selection
   evidence.

## Nested goal levels

Use a goal stack so a session does not confuse discovery, evidence-building,
and publication polish.

| Level | Purpose | Typical work | Do not advance until |
|---|---|---|---|
| L0 — Lab | Keep the research factory honest | Governance, gates, status, process edits | The repo still enforces public data, traceability, labels, and gates |
| L1 — Research Discovery | Build the hook bank | Scan public datasets, compare candidate joins, write hook cards | Each candidate has data object, first visual, question, AI role, and kill/defer condition |
| L2 — Hook Sprint | Test one candidate quickly | Fetch/reuse data, write rough script, emit first visual/table | The visual reveals a specific measurement gap or the hook is ditched |
| L3 — Program Package | Build reproducible evidence | Program artifacts, deterministic pipeline, sensitivity, limitations | Important numbers trace to scripts, sources, generated artifacts, and retrieval records |
| L4 — Publication Surface | Make the package legible | Article, program page, brief, blog, social card, deck, evidence packet | Gates pass; site builds; public surfaces are checked where relevant |
| L5 — Human-Final Upgrade | Owner-attested release | Owner line review, real reviewer comments, owner-signed commit | §18.5 owner-only steps are complete |

The factory can move downward only when the current level's exit condition is
met. Weak hooks should stop at L2 with a defer note. Strong hooks should not
skip L3 just because a visual looks compelling.

## Showcase report loop

Use this loop when the owner asks for a 10-20 report ADB/ERDI-aligned
showcase. The showcase is not a shortcut around the program ladder. It is an
additional reader-facing quality gate for the strongest L2/L3 candidates.

1. **Batch, do not flood.** Work in batches of 3-5 candidates. Keep a larger
   hook bank, but build only the strongest surfaces.
2. **Evidence first.** A report candidate needs a public-source pipeline,
   generated table or JSON, retrieval/source record, sprint or program note,
   and source caveats before it receives a showcase surface.
3. **Visual concept first viewport.** The first screen should make the
   measurement problem visible through evidence: source disagreement,
   market-month heatmaps, catchment maps, before/after states, timelines,
   corridor flows, or interactive small multiples. Do not use decorative
   visuals to compensate for weak data.
4. **ADB/ERDI narrative shape.** Each report starts with the policy problem,
   explains the data gap, introduces the source upgrade, explains the method
   in plain language, shows the chart, names what the result does and does not
   mean, and ends with an operational use case.
5. **Interactivity must clarify evidence.** Animation, sliders, or toggles are
   allowed only when they expose time, geography, source disagreement, or
   sensitivity. They are not a maturity promotion.
6. **Screenshot QA is mandatory.** Every showcase surface needs desktop and
   mobile screenshots, no console errors, no page-level horizontal overflow,
   readable chart labels, visible caveats, and working controls before it can
   count as a report prototype.
7. **Promotion remains honest.** A showcase prototype can be visually strong
   while still being only a Program Prospectus candidate. It does not become a
   public claim until L3/L4 program gates and review loop requirements are
   satisfied.

## Standard loop

Once hook triage produces a specific data object worth developing:

1. **Frame the question.** Define the policy-relevant measurement gap and the
   exact unit of analysis, using the hook visual as the starting object.
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
9. **Re-check the claim's shape.** If the evidence now supports a different
   claim than the one framed in step 1 — narrower, negative, or an
   absence-of-evidence finding — restate the claim before polishing
   anything. Polishing surfaces around a claim the evidence no longer
   supports is the most expensive mistake this loop can make.
10. **Publish the packet.** Sync the article, evidence links, references, and
    site route only after the gates pass. Presentation follows
    `research/DESIGN.md`: finding first, one hero visual, evidence ledger —
    never stacked audit walls.

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
Test <topic> as a research hook before creating a full program package. Use
public data only. First write the hook card from research/JUDGMENT.md §5:
source object, first visual, possible claim, decision user, falsifier,
landscape gap, and stop condition. Then write or reuse one committed script
that produces the rough visual or table. Create a program package only if the
visual exposes a specific measurement problem; otherwise write a defer note in
research/topic-sprints/. Do not write a headline claim until generated
artifacts, source notes, caveats, and sensitivity checks exist. Run the
repository gates before marking anything as Screening Result or Publication
Ready.
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

Every substantial session should start by reading the stack in `AGENTS.md`,
then the active program board. At open, state the active flagship, stage, move
from `research/JUDGMENT.md` §4, and reason. At close, update the active
program board if the focus, stage, next output, blockers, or verification
status changed; update `research/STATUS.md` only if the lab-level board
changed.

**Board hygiene.** Boards are read, not archived-to. A status cell or
"last completed" entry states the finding or decision first and stays
within ten lines; artifact inventories live in the program folder and git
history (`research/JUDGMENT.md` §7). When a board entry outgrows the
budget, the entry is summarized down, not the budget up.

## Scale rule

Scaling means more standardized packages, not lower standards. A large backlog
is acceptable under Section 18 acceleration only if public labels stay honest:
Hypothesis, Program Prospectus, Screening Result, Publication Ready, Finished
for current issue, or Human-final accepted.

Codex is the operating engine for drafts, scripts, checks, and revisions. The
repository remains the engine of record because it preserves the evidence,
methods, generated artifacts, and governance history.
