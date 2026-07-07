# AGENTS.md

Codex agents in this repository operate a research factory. The governing
stack, in read order:

1. `CLAUDE.md` — operating rules, hard walls, end-of-task hygiene.
2. `research/JUDGMENT.md` — **how to choose what to do.** Read every session.
3. `research/DESIGN.md` — how findings are presented on public surfaces.
4. `research/factory.md` — the process manual (loop, ladder, review modes).
5. `CONSTITUTION.md` — what is allowed; §18 AI-first mode is ACTIVE.
6. `research/STATUS.md` and the active program's `{program}/STATUS.md`.

If instructions conflict, the Constitution and `CLAUDE.md` set the hard floor:
public data, traceability, claim gates, ethics, hard walls, and §18 labels do
not bend. `JUDGMENT`, `DESIGN`, and `factory` guide choices inside that floor.
When a session prompt asks for something outside the stack, raise the conflict
with the owner.

## What a session looks like

1. **Open.** Read the boards. State the active flagship, its stage, and —
   from the move menu in `research/JUDGMENT.md` §4 — the single
   highest-leverage move this session will make, with a one-sentence
   reason. "Deepen evidence" is not the default; it must beat the
   alternatives (reshape claim, publish, critique, improve presentation,
   rotate).
2. **Work.** Make the move. Every empirical number comes from a committed
   script; every artifact carries its honest label. For new topics, start with
   a public data object and a rough visual, not with an essay. For public
   surfaces, lead with the finding and its limits, not the process trail.
3. **Verify.** Run the end-of-task hygiene in `CLAUDE.md` (gates, site
   build, browser check, board updates) without being asked.
4. **Close.** Update the per-program board in the researcher voice
   (`research/JUDGMENT.md` §7): finding or decision first, ten-line
   budget, no artifact inventories.

## The two tests every session must pass

- **Progress test.** By close, the claim moved, the claim changed shape,
  a reader is better off, or a decision was recorded — at least one,
  named explicitly. A new artifact that documents the same blockage
  again passes none of these.
- **Stopping rule.** Never take a third consecutive pass at a wall whose
  claim-enabling counts two prior passes left at zero. Reshape the claim,
  publish the absence as the finding, or escalate and rotate
  (`research/JUDGMENT.md` §2–3).

## Named anti-patterns (all observed here; all banned)

- **Wall-stacking** — adding another audit/scan/gate artifact and a
  matching page section when the previous dozen changed no claim.
- **Scan-grinding** — re-searching the same absence in a new portal
  without naming, in advance, why this source plausibly differs.
- **Status bloat** — appending receipts to boards until cells run to
  thousands of words. Boards state findings and decisions, briefly.
- **Inventory pages** — public pages that enumerate process instead of
  communicating a finding (`research/DESIGN.md`).
- **Blocked-claim tunnel vision** — grinding toward claim X while the
  evidence already supports a stronger, different claim (often the
  documented absence itself).
- **Topic-first essays** — choosing a broad topic and then looking for data to
  decorate it. Research starts from a public data object, a visible pattern,
  and a falsifiable claim.
- **Decorative visuals** — using polish, cards, animations, or maps that do
  not clarify the evidence. A visual earns space only if it carries a finding,
  a limitation, a sensitivity result, or a source disagreement.

## Non-negotiables (unchanged)

- Public data only; no empirical number from model memory.
- Every important number traces to a committed script, generated
  artifact, public source, and retrieval/version record.
- Sensitivity at ±50% for arbitrary numeric choices.
- Composite metrics are triage only, never the headline.
- Honest maturity labels and `attestation_chain: ai-first` on every §18
  artifact; citations by BibTeX key; §14 banned words; §13.3 DMC framing.
- Hard walls in `CLAUDE.md` (owner identity, credentials, external
  reviewer contact, §18 amendments) pause work and ask the owner.

## Project-local skills

- `.codex/skills/adb-erdi-research-style/SKILL.md` — ADB/ERDI narrative
  voice for research copy.
- `.claude/skills/adb-erdi-paper-framing.md` — issue statements, key
  messages, evidence spines, figure plans.
- Do not install project skills machine-wide unless the owner asks.

## Owner intent

One flagship at a time, iterated until it has a standout finding, honest
evidence, and a presentation surface a researcher would be proud to send —
then the next program. Depth over breadth; findings over receipts; the
reader over the audit trail (which the repo preserves regardless).
