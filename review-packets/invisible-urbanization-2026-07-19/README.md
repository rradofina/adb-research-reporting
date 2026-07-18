# Review packet — invisible-urbanization — 2026-07-19

This is a self-contained snapshot of the evidence the program owner
asks the reviewer to assess. Per CONSTITUTION.md §9.3 and red-team.md.

## How to read this packet (suggested order, by attention budget)

**If you have 2 minutes:** `publication/5-social/` (the tweet card).

**If you have 10 minutes:** `publication/3-brief/` (one-page brief).

**If you have 20 minutes:** `publication/4-blog/` (~750-word narrative
post for a general dev-econ reader) or `publication/6-slides/*.pptx`
(the ADB internal slide deck — open in PowerPoint or LibreOffice).

**If you have 90 minutes (full review):**

1. Read `shared/CONSTITUTION.md` for the rules every program in the
   lab is governed by. The relevant sections for this review are §6
   (methods), §7 (claim-maturity gates), §9 (review process), §13.3
   (DMC framing), §14 (taste heuristics), and §18 (AI-First Operating
   Mode — currently active; affects attestation chain).
2. Read `program/README.md` for the program overview, then
   `program/STATUS.md` for the current operating state.
3. Read `program/literature.md` for the systematic Tier-A/B/C scan.
4. Read `program/pre-registration.md` for the frozen claim,
   falsification condition, and arbitrary-numerics inventory.
5. Read `program/sensitivity.md` and `program/sensitivity-runs.json`
   for the ±50 percent test results.
6. Read `program/results.md` for the screening artifact.
7. Read `program/limitations.md` and `program/upgrade-gap.md` for
   what the result cannot establish and what blocks human-final.
8. Read `publication/1-working-paper/*.md` for the long-form paper.
9. Optionally re-run the pipeline per `program/REPRODUCE.md`. Source
   seeds, code, and generated outputs are under `program/source-inputs/`,
   `program/scripts/`, and `program/generated/`.

## What the program owner asks of you

- Read the artifacts in this packet.
- Flag issues on measurement, identification, reproducibility, or
  framing (per Constitution §13.3 — measurement gap, not DMC deficiency).
- Optionally write a short response. The owner commits your written
  comments verbatim alongside written responses, per §9.3.
- Disclose any conflict of interest (per red-team.md §conflict-of-interest).

Estimated reading time: 90–120 minutes for the program artifacts
without re-running the pipeline. Turnaround per red-team.md is 4 weeks
from acceptance.

Credit is by acknowledgment in the published article. You are not an
author. Compensation, if any, follows institutional norms.

## Files in this packet

### Publication ladder

The publication ladder (`research/factory.md`) requires every program to
have an honest version of its result at every reader-depth. This packet
includes all six text/binary tiers (the React program page on the lab
website is Tier 2 and is not included here).

- `publication/1-working-paper/invisible-urbanization-cluster.md`  `1cb737dfee89…`
- `publication/3-brief/invisible-urbanization-cluster.md`  `fd8cc724340b…`
- `publication/4-blog/invisible-urbanization-cluster.md`  `2cf897b7abfd…`
- `publication/5-social/invisible-urbanization-cluster.md`  `e7ecc19775d8…`
- `publication/6-slides/invisible-urbanization-cluster.md`  `f93fbda90710…`

### Program artifacts

- `program/README.md`  `09683722c554…`
- `program/STATUS.md`  `5bdd67a6ac7b…`
- `program/REPRODUCE.md`  `24d7479cbaf2…`
- `program/literature.md`  `1dd7dcf8f2c1…`
- `program/pre-registration.md`  `253bf7d42a20…`
- `program/sensitivity.md`  `7db7814d7293…`
- `program/sensitivity-runs.json`  `02aa097117e9…`
- `program/coverage.md`  `1f39b50b30ab…`
- `program/results.md`  `9b70ad1befe2…`
- `program/limitations.md`  `b33fd6710105…`
- `program/review-internal.md`  `8b03661aa35a…`
- `program/review-external.md`  `1cd14e8c5715…`
- `program/generated/charts/invisible-urbanization-01-definition-gap-hero.png`  `4d15d1976a5d…`
- `program/generated/charts/invisible-urbanization-01-definition-gap-hero.svg`  `b270116afba0…`
- `program/generated/charts/invisible-urbanization-02-selected-definition-dumbbell.png`  `08a7e60704d0…`
- `program/generated/charts/invisible-urbanization-02-selected-definition-dumbbell.svg`  `b3493e15f917…`
- `program/generated/charts/invisible-urbanization-03-definition-gap-over-time.png`  `2bdfe975e791…`
- `program/generated/charts/invisible-urbanization-03-definition-gap-over-time.svg`  `3673644513a5…`
- `program/generated/charts/invisible-urbanization-04-focus-trajectories.png`  `3b7508810f3f…`
- `program/generated/charts/invisible-urbanization-04-focus-trajectories.svg`  `800fc8b3ce4d…`
- `program/generated/charts/invisible-urbanization-05-administrative-scale-sensitivity.png`  `66198eebf7a8…`
- `program/generated/charts/invisible-urbanization-05-administrative-scale-sensitivity.svg`  `60e1f914ad20…`
- `program/generated/charts/invisible-urbanization-06-embedded-share-over-time.png`  `780e3dd7dbe9…`
- `program/generated/charts/invisible-urbanization-06-embedded-share-over-time.svg`  `785815313bb0…`
- `program/generated/charts/invisible-urbanization-07-transition-waterfall.png`  `f4d2bbb4ad26…`
- `program/generated/charts/invisible-urbanization-07-transition-waterfall.svg`  `e87847ca3cd2…`
- `program/generated/charts/invisible-urbanization-08-country-embedded-shares.png`  `fc68ffe50634…`
- `program/generated/charts/invisible-urbanization-08-country-embedded-shares.svg`  `225a6fbbf7bf…`
- `program/generated/charts/invisible-urbanization-09-country-time-heatmap.png`  `1820409f375a…`
- `program/generated/charts/invisible-urbanization-09-country-time-heatmap.svg`  `dd2ae3a5d0ce…`
- `program/generated/charts/invisible-urbanization-10-coverage-funnel.png`  `8e6f5764145d…`
- `program/generated/charts/invisible-urbanization-10-coverage-funnel.svg`  `2a74d66df75b…`
- `program/generated/charts/invisible-urbanization-11-method-and-claim-gate.png`  `688222fca00c…`
- `program/generated/charts/invisible-urbanization-11-method-and-claim-gate.svg`  `9e37f793a9e4…`
- `program/generated/charts/invisible-urbanization-rough-definition-gap.png`  `dc2aca43f040…`
- `program/generated/charts/invisible-urbanization-rough-definition-gap.svg`  `e946cc51c8e1…`
- `program/generated/charts/invisible-urbanization-rough-scale-sensitivity.png`  `13b6455e985c…`
- `program/generated/charts/invisible-urbanization-rough-scale-sensitivity.svg`  `34760d6e1a41…`
- `program/generated/charts/invisible-urbanization-thumbnail.json`  `4f6d7775876b…`
- `program/generated/charts/invisible-urbanization-thumbnail.png`  `b7ccc8f65e11…`
- `program/generated/charts/invisible-urbanization-thumbnail.svg`  `d4158e6da093…`
- `program/generated/invisible-urbanization-adb-panel.csv`  `072153aff9fe…`
- `program/generated/invisible-urbanization-adb-panel.json`  `92d95ce09f11…`
- `program/generated/invisible-urbanization-boundary-readiness.csv`  `7e31e6794bee…`
- `program/generated/invisible-urbanization-definition-gap-panel.csv`  `f1005fe9d7e3…`
- `program/generated/invisible-urbanization-definition-gap.json`  `3b7518bce26a…`
- `program/generated/invisible-urbanization-embedded-urban-panel.csv`  `d6ea8ff8c860…`
- `program/generated/invisible-urbanization-figure-dossier.json`  `3d1bde6953df…`
- `program/generated/invisible-urbanization-ghsl-duc-inventory.json`  `18190e77e558…`
- `program/generated/invisible-urbanization-ghsl-duc-members.csv`  `9bc4662227dc…`
- `program/generated/invisible-urbanization-level2-transitions.csv`  `653c6a65df76…`
- `program/generated/invisible-urbanization-source-audit.json`  `3fa4bb4fce26…`
- `program/generated/invisible-urbanization-source-readiness-sources.csv`  `a7c344385777…`
- `program/generated/invisible-urbanization-source-readiness.json`  `23d493123499…`
- `program/generated/invisible-urbanization-tautology.csv`  `5667b23479bd…`
- `program/generated/invisible-urbanization-tautology.json`  `edb000c25688…`
- `program/generated/invisible-urbanization-transition-diagnostics.json`  `b4b365a8ab2d…`
- `program/scripts/acquire-ghsl-duc.py`  `0b1e8fefb2ac…`
- `program/scripts/audit-urban-source-readiness.py`  `dad0442688bf…`
- `program/scripts/build-definition-gap-object.py`  `2c700d770d4e…`
- `program/scripts/build-figure-dossier.py`  `54e045d46baa…`
- `program/scripts/build-thumbnail.py`  `27df37ad08a7…`
- `program/scripts/build-transition-diagnostics.py`  `b03e5f8a2b60…`
- `program/scripts/deepen-tautology.py`  `338bd8ec0b16…`

### Shared governance

- `shared/CONSTITUTION.md`  `e8176d8973fe…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `de4c1a7723bb…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `0a213e10e598…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `83f1c415aa64…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T19:21:12.568Z by `scripts/build-review-packet.mjs`.
