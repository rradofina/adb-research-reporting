# Review packet — migration-displacement-signals — 2026-07-18

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

- `publication/1-working-paper/emigrant-stock-corridor-concentration.md`  `bdc8c07ba4ba…`
- `publication/3-brief/migration-displacement-signals.md`  `1ffc2d169d97…`
- `publication/4-blog/migration-displacement-signals.md`  `46ae5402c312…`
- `publication/5-social/migration-displacement-signals.md`  `70b6bf792992…`
- `publication/6-slides/migration-displacement-signals.md`  `49896a381e7d…`
- `publication/6-slides/migration-displacement-signals-deck.pptx`  `2038dc67e8c7…`

### Program artifacts

- `program/README.md`  `4f39f10324ff…`
- `program/STATUS.md`  `b5cfcbea4499…`
- `program/REPRODUCE.md`  `bae25604eafd…`
- `program/literature.md`  `fd54da3d32be…`
- `program/pre-registration.md`  `a4e16a63a4d3…`
- `program/sensitivity.md`  `67e4dccf997c…`
- `program/sensitivity-runs.json`  `faf48c72d2d6…`
- `program/coverage.md`  `fdd7c3bde1c9…`
- `program/results.md`  `94b3a7e73a33…`
- `program/limitations.md`  `0e35ad4f2d62…`
- `program/upgrade-gap.md`  `9ddf3c07f07d…`
- `program/review-internal.md`  `75bdccef961b…`
- `program/review-external.md`  `9db43ec30dfc…`
- `program/generated/charts/migration-corridor-concentration.png`  `6098b269eb17…`
- `program/generated/charts/migration-corridor-concentration.svg`  `91ea0247cf2d…`
- `program/generated/charts/migration-displacement-signals-thumbnail.json`  `efd667d07f2a…`
- `program/generated/charts/migration-displacement-signals-thumbnail.png`  `ef5750d72ba5…`
- `program/generated/charts/migration-displacement-signals-thumbnail.svg`  `b563c392a76d…`
- `program/generated/charts/migration-forced-displacement-composition.png`  `b056b2e71b18…`
- `program/generated/charts/migration-forced-displacement-composition.svg`  `c784a7fdc782…`
- `program/generated/charts/migration-population-share-profile.png`  `b88f6189ef13…`
- `program/generated/charts/migration-population-share-profile.svg`  `d1d8cb920288…`
- `program/generated/charts/migration-rank-inversion.png`  `5a51fa8dbf3c…`
- `program/generated/charts/migration-rank-inversion.svg`  `92c1e984577e…`
- `program/generated/charts/migration-source-observability.png`  `d8f8dbca4793…`
- `program/generated/charts/migration-source-observability.svg`  `3487c9ed15ee…`
- `program/generated/migration-corridor-type-forced-displacement-corridors.csv`  `70998777d268…`
- `program/generated/migration-corridor-type-forced-displacement-country.csv`  `6ff9eb3fa756…`
- `program/generated/migration-corridor-type-forced-displacement.json`  `f020dd9b7cfc…`
- `program/generated/migration-denominator-corridor-type-audit.json`  `dabb5f57fbab…`
- `program/generated/migration-displacement-adb-panel.csv`  `cb352b1210d8…`
- `program/generated/migration-displacement-adb-panel.json`  `4e8e764d53ed…`
- `program/generated/migration-figure-dossier-summary.json`  `35c48553d3a8…`
- `program/generated/migration-per-population-deepening.csv`  `9e281a3686e8…`
- `program/generated/migration-per-population-deepening.json`  `32004108249e…`
- `program/scripts/audit-corridor-type-forced-displacement.py`  `fabb4b73c637…`
- `program/scripts/build-figure-dossier.py`  `384b4e11ea3a…`
- `program/scripts/build-thumbnail.py`  `590b8cbdfce7…`
- `program/scripts/deepen-per-population.py`  `a4c84783857a…`
- `program/scripts/process-migration.py`  `9126e859fac6…`
- `program/scripts/sensitivity.py`  `eee090642bda…`

### Shared governance

- `shared/CONSTITUTION.md`  `3d159027c3d8…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `2867252d6623…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `ba2f6bda824b…`
- `shared/manifest.sha256`  `db692480ff8a…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `b6dc4c42687c…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T10:25:05.983Z by `scripts/build-review-packet.mjs`.
