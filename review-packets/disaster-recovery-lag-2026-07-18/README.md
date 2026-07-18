# Review packet — disaster-recovery-lag — 2026-07-18

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

- `publication/1-working-paper/disaster-burden-cluster.md`  `db0b2897899e…`
- `publication/3-brief/disaster-recovery-lag.md`  `ad99976685fc…`
- `publication/4-blog/disaster-recovery-lag.md`  `d8cf2348e532…`
- `publication/5-social/disaster-recovery-lag.md`  `c7988e8a4da9…`
- `publication/6-slides/disaster-recovery-lag.md`  `e15446073103…`
- `publication/6-slides/disaster-recovery-lag-deck.pptx`  `271d4a01770f…`

### Program artifacts

- `program/README.md`  `a73bf80dece5…`
- `program/STATUS.md`  `fe79c308d08a…`
- `program/REPRODUCE.md`  `552dcc2560ce…`
- `program/literature.md`  `acd8807a9998…`
- `program/pre-registration.md`  `9309580cb4ee…`
- `program/sensitivity.md`  `2a97c6ff643a…`
- `program/sensitivity-runs.json`  `59a72f40cda1…`
- `program/coverage.md`  `695dd751c5a5…`
- `program/results.md`  `af1b4a736779…`
- `program/limitations.md`  `d0012aea152a…`
- `program/upgrade-gap.md`  `a0b27d9f5608…`
- `program/review-internal.md`  `bdb87c1703dd…`
- `program/review-external.md`  `9761ef1170e9…`
- `program/generated/charts/disaster-gdis-geometry-audit.png`  `cb9256dc37d3…`
- `program/generated/charts/disaster-gdis-geometry-audit.svg`  `050a8fe2d6b2…`
- `program/generated/charts/disaster-haiyan-main-series.png`  `eaa886485a36…`
- `program/generated/charts/disaster-haiyan-main-series.svg`  `0f6bb4c48d04…`
- `program/generated/charts/disaster-haiyan-observation-coverage.png`  `427c0eb8b9d8…`
- `program/generated/charts/disaster-haiyan-observation-coverage.svg`  `4740ed6b261e…`
- `program/generated/charts/disaster-haiyan-sensitivity.png`  `4cb37f9ad830…`
- `program/generated/charts/disaster-haiyan-sensitivity.svg`  `203f68feb517…`
- `program/generated/charts/disaster-metric-rank-disagreement.png`  `52196a494ada…`
- `program/generated/charts/disaster-metric-rank-disagreement.svg`  `3ee4a4884bae…`
- `program/generated/charts/disaster-per-capita-inversion.png`  `d7926a2f3f78…`
- `program/generated/charts/disaster-per-capita-inversion.svg`  `8c0497c4b8cf…`
- `program/generated/charts/disaster-recovery-lag-thumbnail.json`  `bcde4a81dfcb…`
- `program/generated/charts/disaster-recovery-lag-thumbnail.png`  `d09505486414…`
- `program/generated/charts/disaster-recovery-lag-thumbnail.svg`  `090a7a7d81e6…`
- `program/generated/charts/disaster-source-ladder.png`  `dbbe3fed2db8…`
- `program/generated/charts/disaster-source-ladder.svg`  `3920ec625225…`
- `program/generated/charts/disaster-two-stage-validity-gate.png`  `f9585ca06b00…`
- `program/generated/charts/disaster-two-stage-validity-gate.svg`  `a0927ecfa361…`
- `program/generated/disaster-recovery-figure-dossier-summary.json`  `79696f3f4822…`
- `program/generated/disaster-recovery-gdis-geometry-audit.csv`  `d2952e66e637…`
- `program/generated/disaster-recovery-gdis-geometry-audit.json`  `a20ba750cc97…`
- `program/generated/disaster-recovery-haiyan-construct-validation.json`  `ae6805ea91d2…`
- `program/generated/disaster-recovery-haiyan-monthly-pilot.csv`  `1b842d363fed…`
- `program/generated/disaster-recovery-haiyan-nightly-pilot.csv`  `c1ef1243f3f5…`
- `program/generated/disaster-recovery-haiyan-source-ledger.csv`  `57010cca13a5…`
- `program/generated/disaster-recovery-lag-adb-panel.csv`  `a420d43afdc5…`
- `program/generated/disaster-recovery-lag-adb-panel.json`  `ce58ac7986b1…`
- `program/generated/disaster-recovery-lag-metric-falsification.csv`  `7dfed7fc769c…`
- `program/generated/disaster-recovery-lag-metric-falsification.json`  `89eff20d8a99…`
- `program/generated/disaster-recovery-lag-recovery-source-readiness-country.csv`  `4cb024f0c8a9…`
- `program/generated/disaster-recovery-lag-recovery-source-readiness-events.csv`  `f6fb98bcb199…`
- `program/generated/disaster-recovery-lag-recovery-source-readiness.json`  `cff7a0603baa…`
- `program/scripts/audit-gdis-geometry.py`  `f8c8a20c22b4…`
- `program/scripts/audit-recovery-source-readiness.py`  `1835b5fb99e3…`
- `program/scripts/build-figure-dossier.py`  `6503553d4054…`
- `program/scripts/build-recovery-construct-evidence.py`  `18ed9bb8b62e…`
- `program/scripts/build-thumbnail.py`  `9de6c04db63a…`
- `program/scripts/deepen-metric-falsification.py`  `83144467a203…`
- `program/scripts/process-disaster.py`  `e7030c69d823…`

### Shared governance

- `shared/CONSTITUTION.md`  `3d159027c3d8…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `45c4b2b508c8…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `aa91083161fc…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `cf1d2f4b3ee3…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T12:33:25.581Z by `scripts/build-review-packet.mjs`.
