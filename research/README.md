# Research operations

Cross-cutting research-operations scaffolding. Programs at the repository
root reference templates and gates here. This folder is governance-only —
no empirical artifacts live here.

## Contents

| Folder / file | Purpose | Constitution refs |
|---|---|---|
| `templates/` | Per-artifact templates copied into program folders | §4, §5, §6, §9 |
| `adb-paper-packages/` | ADB-facing package notes for the strongest topics before full drafting | §13.3, §14 |
| `gates/` | Promotion-request templates (H→PP, PP→SR, SR→PR) | §7 |
| `decisions/` | Architecture-decision records for irreversible methodological choices | §6, §7 |
| `zenodo/` | Zenodo deposition metadata template + checklist | §10 |
| `wip-register.md` | Current claim-maturity register; enforces §8.1 cap | §8.1 |
| `STATUS.md` | Current operating board: active focus, stage, next output, blockers, handoff prompt | §7, §8, §18 |
| `factory.md` | Codex-operated research-factory workflow and scale rules | §2, §4, §5, §6, §11, §18 |
| `coverage-matrix.md` | Per-program × per-DMC coverage table | §13 |
| `style-guide.md` | Banned words, DMC framing, citation discipline | §13.3, §14 |
| `adb-erdi-writing-audit.md` | ADB/ERDI/Data Division writing pattern, problem framing, chart/source-note rules | §13.3, §14 |
| `adb-paper-package-priorities.md` | Priority memo for turning the strongest topics into ADB-facing paper packages | §13.3, §14 |
| `google-granular-data-upgrades.md` | Google-released or Google-hosted granular public data worth using, with caveats | §2.2, §2.3, §11 |
| `originality-register.md` | Originality level and marginal-contribution standard by program | §2.3, §3.1, §3.3, §8.3 |

## How to use

When a program reaches a gate, the owner copies the relevant templates
into the program folder (e.g., `migration-displacement-signals/literature.md`),
fills them in, and references them from the gate request in `gates/`.

The `scripts/` folder at the repository root contains the deterministic
checks that CI runs against any output that touches a gate.

For ADB-facing briefs, working papers, methods notes, or dataset notes,
apply `.claude/skills/adb-erdi-paper-framing.md` before expanding prose.
The current first package set is in `adb-paper-packages/`.
