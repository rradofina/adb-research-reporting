# Review packet — food-price-climate-transmission — 2026-07-19

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

- `publication/1-working-paper/food-price-joint-qualifier.md`  `15520ae77b42…`
- `publication/3-brief/food-price-joint-qualifier.md`  `522c858b0a67…`
- `publication/4-blog/food-price-joint-qualifier.md`  `d3e89e205cbb…`
- `publication/5-social/food-price-joint-qualifier.md`  `1de1473a7b96…`
- `publication/6-slides/food-price-joint-qualifier.md`  `9a1b76087ea0…`
- `publication/6-slides/food-price-climate-transmission-deck.pptx`  `4109d8abb61e…`

### Program artifacts

- `program/README.md`  `3bd70a713392…`
- `program/STATUS.md`  `5c2cb533e451…`
- `program/REPRODUCE.md`  `d44cdf03d129…`
- `program/literature.md`  `a570bb49963b…`
- `program/pre-registration.md`  `e211d7c43a8c…`
- `program/sensitivity.md`  `dc2381037f1b…`
- `program/sensitivity-runs.json`  `a41270157d0a…`
- `program/coverage.md`  `2a4a4a059b50…`
- `program/results.md`  `a417f10638a7…`
- `program/limitations.md`  `21e20996f878…`
- `program/upgrade-gap.md`  `44c3dae24f95…`
- `program/review-internal.md`  `c935db3c7a7c…`
- `program/review-external.md`  `71d54f7f4800…`
- `program/generated/charts/food-price-annual-alignment.png`  `d07f6924ea58…`
- `program/generated/charts/food-price-annual-alignment.svg`  `b81f923bc15c…`
- `program/generated/charts/food-price-claim-gates.png`  `5948471c128c…`
- `program/generated/charts/food-price-claim-gates.svg`  `28dc77c0be42…`
- `program/generated/charts/food-price-climate-transmission-thumbnail.json`  `573ce179f6d3…`
- `program/generated/charts/food-price-climate-transmission-thumbnail.png`  `9d4892e48ca3…`
- `program/generated/charts/food-price-climate-transmission-thumbnail.svg`  `9c90aea91610…`
- `program/generated/charts/food-price-macro-market-mismatch.png`  `a1b5b9e1608b…`
- `program/generated/charts/food-price-macro-market-mismatch.svg`  `604262689f6f…`
- `program/generated/charts/food-price-method-correction.png`  `bfe71ec9416f…`
- `program/generated/charts/food-price-method-correction.svg`  `54e3e902d8c8…`
- `program/generated/charts/food-price-rain-lag-sensitivity.png`  `037607cf561b…`
- `program/generated/charts/food-price-rain-lag-sensitivity.svg`  `ab7c7a1ed477…`
- `program/generated/charts/food-price-source-alignment-funnel.png`  `a5d5383d23c7…`
- `program/generated/charts/food-price-source-alignment-funnel.svg`  `2e90074c74d9…`
- `program/generated/charts/food-price-spike-alignment.png`  `a53fec47e9b5…`
- `program/generated/charts/food-price-spike-alignment.svg`  `61e2050a30cf…`
- `program/generated/charts/food-price-threshold-sensitivity.png`  `d07d8e5564df…`
- `program/generated/charts/food-price-threshold-sensitivity.svg`  `e5f38db32a2e…`
- `program/generated/charts/food-price-wave-timeline.png`  `afa6f9c21278…`
- `program/generated/charts/food-price-wave-timeline.svg`  `f4b83bc605cd…`
- `program/generated/food-price-adb-panel.csv`  `f74255f3dfdd…`
- `program/generated/food-price-adb-panel.json`  `04bbba27fa2f…`
- `program/generated/food-price-construct-validation.json`  `89caa8e649ca…`
- `program/generated/food-price-coverage-deepening.csv`  `d8e99888ef53…`
- `program/generated/food-price-coverage-deepening.json`  `99c101471db8…`
- `program/generated/food-price-coverage-food-import-audit.json`  `610c9bc6e58b…`
- `program/generated/food-price-food-import-rerank.csv`  `a2e38f87eb7b…`
- `program/generated/food-price-food-import-source-readiness-sources.csv`  `ffb17054ad78…`
- `program/generated/food-price-food-import-source-readiness.json`  `2dd854bf3e16…`
- `program/generated/food-price-market-month-corrected.csv`  `2b2d895d18f6…`
- `program/generated/food-price-market-year.csv`  `f4d4d650688c…`
- `program/generated/food-price-reformulated-adb-panel.csv`  `e83193c417aa…`
- `program/generated/food-price-reformulated-adb-panel.json`  `25615ae4f88f…`
- `program/generated/food-price-threshold-sensitivity.csv`  `c9e5d3fc49cb…`
- `program/scripts/audit-food-import-source-readiness.py`  `624d8f6af61e…`
- `program/scripts/build-construct-validation.py`  `e4cfba7d93cf…`
- `program/scripts/build-figure-dossier.py`  `0cadc4fb560a…`
- `program/scripts/build-thumbnail.py`  `8546dc2d42ed…`
- `program/scripts/deepen-coverage-artifact.py`  `0fb4365cad86…`
- `program/scripts/process-food.py`  `cfd1ad80870a…`
- `program/scripts/reformulated.py`  `1ce4719e07a0…`

### Shared governance

- `shared/CONSTITUTION.md`  `e8176d8973fe…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `c5ccc7b5018b…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `0a213e10e598…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `e97d7b67ed40…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T17:19:45.955Z by `scripts/build-review-packet.mjs`.
