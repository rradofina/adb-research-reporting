# Current research status — operating board

**Principle.** This file is the **board, not the file**. Its job is to point
to the active flagship and to define how a session opens, runs, and closes.
Per-program detail — last completed, next focused work, current blockers,
program-specific runbooks — lives in `{program}/STATUS.md` or in the
program's `README.md`. If you find PSDQ-specific narrative here, move it.

Last updated: 2026-05-07.

## Current focus

| Field | Value |
|---|---|
| Active flagship | `public-service-data-quality` (PR under §18 ai-first; **ai-first finished for current issue** as of 2026-05-07 under Mode A) |
| Per-program board | [`public-service-data-quality/STATUS.md`](../public-service-data-quality/STATUS.md) |
| Operating mode | §18 ACTIVE (AI-First) |
| Default review mode | Mode A (AI-only); see `research/factory.md` |

The active flagship is the only program that may be advanced this session.
Programs in the queue are listed in `research/wip-register.md` and
`CONSTITUTION.md` §15. Do not silently switch programs; if a different
program should become the focus, write the reason here before switching.

## Stage labels

Generic across programs. Use these in chat updates and handoffs.

| Stage | Meaning | Output |
|---|---|---|
| 0. Idea queue | New possible topic, not yet judged | Short idea note |
| 1. Research framing | Question, contribution, audience, literature map | `literature.md`, problem statement |
| 2. Source discovery | Public datasets, licenses, API paths, coverage | source plan, cache plan |
| 3. Pipeline implementation | Fetch/process scripts and generated artifacts | `scripts/`, `.cache/`, `generated/` |
| 4. Results and sensitivity | Main result plus robustness checks | `results.md`, `sensitivity.md` |
| 5. Critique and limits | Red-team review, non-claims, failure modes | `limitations.md`, reviews |
| 6. Publication surface | Article, charts, home hooks, evidence page | `articles/`, `reporting-site/` |
| 7. Review loop and handoff | Review mode chosen + iterated to exit condition | `review-internal.md`, `review-external.md`, updated `{program}/STATUS.md` |
| 8. Blocked or owner-only | Needs owner account, reviewer, or non-AI attestation | explicit blocker in the per-program file |

## Where status, register, backlog, process live

| File | Role |
|---|---|
| `research/STATUS.md` (this file) | The board: active flagship + session protocol |
| `{program}/STATUS.md` | Per-program last-completed / next-work / blockers |
| `research/wip-register.md` | Maturity register (which program at which label) |
| `CONSTITUTION.md` §15 | Program register of record |
| `research/TODO-NEXT-SESSION.md` | Backlog of useful future work (cross-program) |
| `research/factory.md` | Process manual: program loop, publication ladder, review loop |
| `CLAUDE.md` | Operating rules for AI assistants |

If these files disagree, fix the per-program file first for immediate
focus, then propagate to the register or this board only if the underlying
status truly changed.

## Session protocol

**Principle.** A session is a unit of accountable work, not a stream of
edits. It opens by stating what is being done, runs by doing it, and closes
by leaving the board in a state the next session can read.

**At session open:**
1. Read this file, the active flagship's `{program}/STATUS.md`, `CLAUDE.md`,
   and `research/factory.md`.
2. State the active flagship, current stage, and next output in plain language.
3. Continue the next focused work in the per-program board, unless the
   owner redirects.

**During session:**
1. Name the kind of work being done (framing, source, pipeline, results,
   critique, publication, review-loop, handoff).
2. Do not silently switch programs. If a switch is justified, record the
   reason in this file before making it.
3. Run end-of-task hygiene per `CLAUDE.md` after substantive changes
   (gates, build if site changed, browser-check if public surface changed,
   per-program STATUS update).

**At session close:**
1. Update the active flagship's `{program}/STATUS.md`: last completed, next
   focused work, blockers, verification actually run.
2. Update this file only if the active flagship, operating mode, or default
   review mode changed.
3. Update `research/wip-register.md` only if a maturity label changed.

## Current operational notes

- **2026-05-07:** Per-program loop instituted (publication ladder + three
  review modes). 9 programs demoted PR/SR → PP under §16. PSDQ remains
  active flagship. STATUS.md slimmed to a principle-driven board (this
  refactor); PSDQ-specific narrative migrated to
  `public-service-data-quality/STATUS.md`.
- **2026-05-07:** PSDQ completed the full Mode A loop: publication ladder
  built (brief + blog + social + slide deck via Quarto), choropleth
  visualizations added (PHL ADM1, BGD ADM1, PHL ADM3 poverty), 257
  unresolved BARMM Maguindanao NHFR records resolved by deterministic
  barangay-name lookup (residue 8), reviewer packet rebuilt (6.1 MB),
  Mode A self-review + critique-pass + AI second-opinion code review
  iteration closed. PSDQ is **ai-first finished for current issue**.
  Next program from the queue can now enter the loop.
- **2026-05-07:** GitHub-prep cleanup. Repository root now has a
  reader-facing `README.md`, `LICENSE` (MIT for code), and
  `LICENSE-CONTENT` (CC BY 4.0 for research artifacts). `.gitignore`
  rewritten to exclude per-program `.cache/` directories (~8 GB total,
  reproducible from public sources via committed fetch scripts) while
  keeping each cache's `README.md` (regen instructions) committed.
  The 2026-04-25 review packet moved to `_archive/review-packets/`
  (the 2026-05-07 packet stays in `review-packets/` as the current
  one). `luminosity-gap/README.md` now opens with a "legacy" note
  pointing readers to the active `reporting-site/` instead. The repo
  is ready for `git init && git push`.

## Handoff prompt

Use this when starting a fresh session:

```text
Read research/STATUS.md, then the active flagship's {program}/STATUS.md
named in the board. Then read CLAUDE.md and research/factory.md.
Continue the active flagship's next focused work. State the active
program, stage, next output, and verification plan before editing files.
```
