# Skill: /goal

## Invocation
> `/goal`

> `/goal research`

Print this goal without extra commentary. If it conflicts with
`research/STATUS.md` or the active flagship's `{program}/STATUS.md`, the
STATUS files win.

## Canonical Goal

**Make one flagship evidence package hard to dismiss.**

This repository is not trying to look like a research lab. It is trying to
produce one serious, auditable research package at a time. A good output has a
specific data spine:

`public data object -> revealing visual -> non-generic question -> deterministic method -> direct result -> named caveat -> evidence packet`

The work is not done when there is an article, a chart, or a page. It is done
when a skeptical reader can follow the number back to the source, rerun the
script, understand exactly what the result does not prove, and still see why
the measurement gap matters for a DMC policy user.

Commitments:

- **Specificity over template.** No first screen, chart, summary, or slide is
  acceptable if it could fit another program after swapping nouns.
- **Traceable outputs.** Every empirical number traces to a committed script,
  public source, generated artifact, and retrieval/version record.
- **Measurement gaps, not rankings.** Lead with coverage gaps, granularity
  gaps, source-disagreement gaps, corridor gaps, and observability gaps.
  Composite metrics are triage devices only.
- **Honest attestation.** Every artifact names its chain: `ai-first`,
  `ai-first; owner-spot-checked`, `mixed`, or `human-final`. An `ai-first`
  artifact has not been owner-signed or externally reviewed.

## Nested Goal Stack

Use goals as a stack, not as one flat command. Each session should name the
lowest active level it is working on and the exit condition for that level.

| Level | Goal | Output | Exit condition |
|---|---|---|---|
| L0 — Lab | Build a credible data-first research factory | Governed repo, gates, status board | Constitution and gates still hold |
| L1 — Research Discovery | Find non-generic public-data hooks | `research/hook-bank.md` | Hook has public data object, first visual, question, AI role, kill/defer condition |
| L2 — Hook Sprint | Test one hook fast | rough script + generated visual/table + defer/promote note | Visual reveals a specific measurement gap, or hook is ditched |
| L3 — Program Package | Turn a surviving hook into evidence | program folder artifacts, pipeline, sensitivity, limitations | numbers trace to scripts and public sources; caveats are explicit |
| L4 — Publication Surface | Make the evidence readable at every depth | article, program page, brief, blog, social, deck, evidence packet | ladder passes gates, build, and browser checks |
| L5 — Human-Final Upgrade | Convert ai-first work to owner-attested work | owner review, real external comments, signed commit | §18.5 owner-only steps complete |

Do not jump from L1 to L4. A beautiful page cannot rescue a weak hook. Do not
stay at L1 forever either; once a hook looks promising, run an L2 sprint and
let the data decide whether it deserves a program package.

## Files to Monitor

Read these files as the goal stack changes. Do not rely on chat memory when a
file below is the source of record.

| Goal level | Files to monitor | What to check |
|---|---|---|
| Always | `research/STATUS.md`, `CLAUDE.md`, `CONSTITUTION.md`, `research/factory.md` | active flagship, session protocol, hard walls, verification rules, current operating mode |
| L1 — Research Discovery | `research/hook-bank.md`, `research/originality-register.md`, `research/TODO-NEXT-SESSION.md`, `research/deep-questions.md` | candidate hooks, public data objects, first visuals, originality risk, ditch/defer conditions |
| L2 — Hook Sprint | selected program folder, `{program}/scripts/`, `{program}/generated/`, `{program}/deep-questions.md`, `{program}/deepened-results.md` | whether the rough data object and visual reveal a specific measurement gap |
| L3 — Program Package | `{program}/README.md`, `literature.md`, `pre-registration.md`, `coverage.md`, `results.md`, `sensitivity.md`, `limitations.md`, `review-internal.md`, `review-external.md` | claim, method, source coverage, sensitivity, caveats, review objections |
| L4 — Publication Surface | `articles/`, `articles/_brief/`, `articles/_blog/`, `articles/_social/`, `articles/_slides/`, `reporting-site/src/`, `reporting-site/public/programs/` | whether the public version matches the evidence and looks program-specific |
| Labels and rotation | `research/wip-register.md`, `CONSTITUTION.md` §15, active `{program}/STATUS.md` | maturity label, promotion/demotion history, next focused work, blockers |

Current active program details live in the per-program board named by
`research/STATUS.md`. For the current flagship, that is
`remittance-resilience/STATUS.md`. If that file and this goal disagree, the
program status file wins for program-specific next work.

## Data-First Hook Loop

Default to data-first discovery, then work backward into the research frame.
Do not start by writing a generic topic essay. Start by asking whether public
data can produce a concrete object a reader can see: a map, corridor network,
scatter, ranked gap, small multiple, timeline, or source-disagreement table.

The loop is:

1. Pull or reuse a public dataset with license, retrieval date, and script path.
2. Build the simplest honest chart or table that exposes the structure.
3. Ask the hook question: "What is visible here that was not visible in the
   conventional source, and why would a DMC policy user care?"
4. Work backward from that visual into the research question, unit of analysis,
   source-gap statement, method, caveat, and publication ladder.
5. If the visual only supports a generic ranking, a composite leaderboard, or a
   topic summary, write a short defer/ditch note and move to the next candidate.

This discovery loop is exploratory. It may inspect public data and build
screening visuals, but it does not publish a headline claim until the method,
limitations, source notes, sensitivity checks, and evidence packet exist.

## `/goal research`

Use `/goal research` when the owner asks for a better list of topics, hooks, or
research directions. The output is not another generic backlog. It is a
**hook bank**: a ranked list of candidate data objects that could become strong
research only if the data produce a non-generic visual question.

The hook bank lives at `research/hook-bank.md` and each candidate should state:

- the public data object to fetch or reuse;
- the first visual to build;
- the non-generic question the visual could answer;
- why the hook is stronger than a country ranking or topic summary;
- how AI can help without supplying empirical numbers;
- the kill/defer condition.

AI can help as a scout, critic, and chart planner: it can search public data
catalogs, map candidate source joins, propose visual encodings, draft
falsifiers, and compare candidate hooks. AI cannot be the source of empirical
values, cannot invent unavailable data, and cannot promote a topic without the
repository's normal gates.

## Public Surface Goal

The reporting site should feel like a research desk with receipts, not a
landing page and not a card gallery. The first viewport for a program should
show the actual evidence object:

- a finding-led title tied to a named unit, place, and period;
- one program-native visual that reads the same generated data as the evidence
  packet;
- the caveat that most constrains the finding;
- visible links to data, method, sources, attestation, and reproduction notes.

The reader path is:

`data hook -> policy decision -> data blind spot -> source upgrade -> method -> result -> limitation -> reuse`

## Current Flagship

The active flagship is the program named in `research/STATUS.md`'s board.
Rotation happens only on owner direction; the next pick comes from the PP
queue in `research/wip-register.md`. Per-program guardrails (specific
non-claims, source caveats, scope limits) live in each program's README,
not here.

Whatever the active flagship is, the bar is the same:

- The opening says what decision or measurement problem is blocked, not just
  what topic the program studies.
- The headline uses a direct quantity or stable cluster. If a composite
  appears, it is named as triage and kept out of the main claim.
- The visuals are program-native. They should expose the argument's structure:
  corridor flows for remittances, source coverage for service data, fuel mix for
  grid reliability, station coverage for air monitoring, and so on.
- Generated visuals are reused consistently across program page, brief, blog,
  slide deck, and working paper. Same CSV everywhere, no hand-exported numbers.
- The writing follows the ADB/ERDI evidence pattern: policy hook, data gap,
  source upgrade, plain-English method, chart result, interpretation,
  limitations, operational use.
- Visible data sources are cited by BibTeX key or source note, with retrieval
  timestamps.
- Reproducible code lives in the program's `scripts/`; every important number
  comes from a generated artifact.
- Honest non-claims are prominent: source gaps, proxy limits, `ai-first`
  attestation, and the owner-only `human-final` upgrade path.

## Current Repair Bar

If the active flagship is still `remittance-resilience`, treat the May 2026
deepening pass as the live agenda. The program should no longer be polished as
if the first Mode A ladder settled everything. The next good version should:

- fix the RPW cost-normalization defect for negative percentage values in
  `process-remittance.py`;
- rerun the main panel, sensitivity suite, median-cost deepening, charts, and
  evidence sync;
- inspect every article, brief, blog, social, slide, README, result, limitation,
  review, and site surface touched by the changed cost fields;
- attempt the public bilateral-flow / corridor-volume weighting keystone, or
  record the exact data wall if the source cannot be retrieved;
- shift the reader-facing frame from "fragility ranking" to
  "equal-weighted corridor-cost screen, robust to median cost but not yet
  flow-weighted";
- make the first visual feel remittance-specific: corridor concentration,
  dependence versus cost with sample-size encoding, flow-weighted cost if
  available, or sender-economy concentration.

## Operating Discipline

One flagship at a time. Make one program excellent, review it, strengthen the
evidence, improve writing and visuals, document how it was produced, then move
on. Run the factory loop: source, literature, method, pipeline, critique,
publication, gate.

Do not move on because the page exists. Move on only when the current flagship
is finished for the current issue, blocked by a specific external dependency,
or explicitly deprioritized by the owner.

## Done Standard

Finished for the current issue means the publication ladder exists for every
reader depth: working paper, program page, brief, blog post, social card, slide
deck, and evidence packet; the five repo gates pass; any site change builds and
browser-checks cleanly; the active program's `STATUS.md` tells the next session
what changed, what remains uncertain, and what would falsify the current frame;
and the chosen review mode's exit condition has fired.

`human-final` is separate and requires owner-only §18.5 steps: line-by-line
paper reading, real external reviewer contact, owner-designated internal
review, and owner-signed commit. AI can bring the artifact to that edge, but
cannot cross it.
