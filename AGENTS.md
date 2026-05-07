# AGENTS.md

Codex agents working in this repository must follow `CLAUDE.md`,
`CONSTITUTION.md`, `research/STATUS.md`, and `research/factory.md`.

## Default Mode

Treat the repo as a Codex-operated research factory. The default is not to
generate many shallow research outputs. The default is to focus on one
flagship program, iterate on its data, literature, method, reproducibility,
article, charts, UI, and critique until the evidence package is genuinely
strong, then move to the next program.

## Focus Rule

Unless the owner asks for a broad scan:

1. Read `research/STATUS.md` and identify the current focus and stage.
2. Improve that program through the full loop in `CLAUDE.md`.
3. Run the relevant scripts in `scripts/`.
4. Update reader-facing publication surfaces in `reporting-site/`.
5. Leave status labels honest: Hypothesis, Program Prospectus, Screening
   Result, Publication Ready, Finished for current issue, or Human-final
   accepted.
6. Update `research/STATUS.md` before handoff when the focus, stage, next
   output, blocker list, or verification status changed.

## Non-Negotiables

- No empirical number may come from model memory.
- Public data only.
- Every important number must trace to a committed script, generated artifact,
  public source, and retrieval/version record.
- Composite metrics may be used only as triage and may not be the headline.
- Do not move to another program just because a draft exists; first critique,
  reproduce, strengthen, and explain the current result.
- Use `research/factory.md` when creating or reviving a program.

## Current Owner Intent

The owner wants the system to behave like an iterative research factory:
Codex should improve its own outputs, review them, understand the methods and
limitations, and keep polishing the focused program until it has a clear
reader-facing result with credible evidence and a strong publication surface.

## Project-Local Skills

This repository keeps project-specific skills inside the repo, not in the
global Codex skills directory.

- Use `.codex/skills/adb-erdi-research-style/SKILL.md` when writing or
  revising ADB/ERDI/Data Division-style research narratives, data stories,
  chart captions, evidence pages, or presentation copy.
- Use `.claude/skills/adb-erdi-paper-framing.md` as the older project-local
  framing companion for issue statements, key messages, evidence spines,
  figure plans, caveat boxes, and source notes.
- Do not install these project-specific writing skills into
  `C:\Users\Raymond\.codex\skills` unless the owner explicitly asks for a
  machine-wide skill.
