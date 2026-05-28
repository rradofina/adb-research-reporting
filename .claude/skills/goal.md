# Skill: /goal

## Invocation
> `/goal`

Print this goal without extra commentary. If it conflicts with
`research/STATUS.md` or the active flagship's `{program}/STATUS.md`, the
STATUS files win.

## Canonical Goal

**Build a credible research factory, not a website full of drafts.**

Codex helps generate, improve, review, document, and present research. Each
output must trace to public sources, committed scripts, generated data, method
notes, limitations, and evidence packets. The system should not just spit out
research; it should iterate on one focused program until a serious reader can
understand it, inspect it, and trust the caveats.

Commitments:

- **Traceable outputs.** Every number traces to a committed script, public
  source, and retrieval/version record. No headline comes from private data.
- **Measurement gaps, not rankings.** Focus on coverage gaps, granularity
  gaps, source-disagreement gaps, and observability gaps. Composite indices
  are triage only, never headlines.
- **Honest attestation.** Every artifact names its chain: `ai-first`,
  `ai-first; owner-spot-checked`, `mixed`, or `human-final`. An `ai-first`
  artifact has not been owner-signed or externally reviewed.

## Website Goal

Pull a reader in quickly, then keep them reading. The first screen should show
one concrete problem: public data can miss important services, and that matters
for planning. The reader path is:

`problem -> data gap -> source upgrade -> method -> result -> caveat -> evidence packet`

The site should feel like a research desk with receipts, not a landing page.
Every claim should drill down to sources, scripts, generated files, and
reproduction notes.

## Current Flagship

The active flagship is the program named in `research/STATUS.md`'s board.
Rotation happens only on owner direction; the next pick comes from the PP
queue in `research/wip-register.md`. Per-program guardrails (specific
non-claims, source caveats, scope limits) live in each program's README,
not here.

Whatever the active flagship is, the bar is the same:

- Strong first-screen hook (finding-led subtitle, not topic-led).
- Generated visuals reused consistently across program page, brief, blog,
  slide deck, and working paper — same CSV everywhere, no hand-exported
  PNGs.
- A readable article that reads like a serious ADB/ERDI-style data story
  or working paper, not a generated stub.
- Visible data sources cited by BibTeX key or source note, with retrieval
  timestamps.
- Reproducible code — every number from a committed script in the
  program's `scripts/`.
- Honest non-claims — residual source-quality gaps stated explicitly,
  `ai-first` attestation, and the owner-only `human-final` upgrade path.

Polish on a finished-for-current-issue flagship is allowed; cross-program
work is not unless the owner redirects.

## Operating Discipline

One flagship at a time. Make one program excellent, review it, strengthen the
evidence, improve writing and visuals, document how it was produced, then move
on. Run the factory loop: source, literature, method, pipeline, critique,
publication, gate. Move to another program only when the current one is
finished for the current issue, blocked by a specific external dependency, or
explicitly deprioritized by the owner.

## Done Standard

Finished for the current issue means the publication ladder exists for every
reader depth: working paper, program page, brief, blog post, social card, slide
deck, and evidence packet; the five repo gates pass; and the chosen review
mode's exit condition has fired.

`human-final` is separate and requires owner-only §18.5 steps: line-by-line
paper reading, real external reviewer contact, owner-designated internal
review, and owner-signed commit. AI can bring the artifact to that edge, but
cannot cross it.
