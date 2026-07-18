# Review packet — coastal-informal-risk — 2026-07-18

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

- `publication/1-working-paper/coastal-informal-cluster.md`  `5797c14cee5e…`
- `publication/3-brief/coastal-informal-cluster.md`  `f1c6ad5597db…`
- `publication/4-blog/coastal-informal-cluster.md`  `adae1de1da61…`
- `publication/5-social/coastal-informal-cluster.md`  `8cdf07690458…`
- `publication/6-slides/coastal-informal-cluster.md`  `3e075404be6c…`

### Program artifacts

- `program/README.md`  `05b197c7e496…`
- `program/STATUS.md`  `9c6eb08ce947…`
- `program/REPRODUCE.md`  `558c4ee23240…`
- `program/literature.md`  `eeba808b6c4b…`
- `program/pre-registration.md`  `bfc629584d41…`
- `program/sensitivity.md`  `c997fb2d5445…`
- `program/sensitivity-runs.json`  `378638d93e01…`
- `program/coverage.md`  `0ed1d34b32c5…`
- `program/results.md`  `35040fdefb91…`
- `program/limitations.md`  `46e55f94fb2f…`
- `program/review-internal.md`  `f79e659118fb…`
- `program/review-external.md`  `a02836d77fea…`
- `program/generated/charts/coastal-informal-risk-01-growth-hero.png`  `866412fdbc3a…`
- `program/generated/charts/coastal-informal-risk-01-growth-hero.svg`  `2ada42cfd8fd…`
- `program/generated/charts/coastal-informal-risk-02-centre-dumbbell.png`  `d9bb0ac6558f…`
- `program/generated/charts/coastal-informal-risk-02-centre-dumbbell.svg`  `d80f229aaed9…`
- `program/generated/charts/coastal-informal-risk-03-proxy-falsification.png`  `ba8b198f0c34…`
- `program/generated/charts/coastal-informal-risk-03-proxy-falsification.svg`  `1a14b17df86d…`
- `program/generated/charts/coastal-informal-risk-04-economy-aggregation.png`  `fb0d4fa73497…`
- `program/generated/charts/coastal-informal-risk-04-economy-aggregation.svg`  `ac940b9a9f58…`
- `program/generated/charts/coastal-informal-risk-05-elevation-sensitivity.png`  `e6bd1e6038a1…`
- `program/generated/charts/coastal-informal-risk-05-elevation-sensitivity.svg`  `b5e39889de3a…`
- `program/generated/charts/coastal-informal-risk-06-window-sensitivity.png`  `63f9f42f733c…`
- `program/generated/charts/coastal-informal-risk-06-window-sensitivity.svg`  `8e6513720bb6…`
- `program/generated/charts/coastal-informal-risk-07-population-built-corroboration.png`  `ae587ec7411d…`
- `program/generated/charts/coastal-informal-risk-07-population-built-corroboration.svg`  `287202393255…`
- `program/generated/charts/coastal-informal-risk-08-absolute-versus-share.png`  `4af2f7ca4f8c…`
- `program/generated/charts/coastal-informal-risk-08-absolute-versus-share.svg`  `8335daaa675a…`
- `program/generated/charts/coastal-informal-risk-09-change-direction.png`  `c7be7956917d…`
- `program/generated/charts/coastal-informal-risk-09-change-direction.svg`  `b8e5e1ec6fcf…`
- `program/generated/charts/coastal-informal-risk-10-growth-concentration.png`  `d46f6c486f4f…`
- `program/generated/charts/coastal-informal-risk-10-growth-concentration.svg`  `14d576ba472e…`
- `program/generated/charts/coastal-informal-risk-11-coverage-funnel.png`  `54273b97baf0…`
- `program/generated/charts/coastal-informal-risk-11-coverage-funnel.svg`  `3a4ea90a89ed…`
- `program/generated/charts/coastal-informal-risk-12-method-and-claim-gate.png`  `c2dbf908318f…`
- `program/generated/charts/coastal-informal-risk-12-method-and-claim-gate.svg`  `5499f4a23f3b…`
- `program/generated/charts/coastal-informal-risk-thumbnail.json`  `fcecfb693ed5…`
- `program/generated/charts/coastal-informal-risk-thumbnail.png`  `e4ae00517c44…`
- `program/generated/charts/coastal-informal-risk-thumbnail.svg`  `f758919842e9…`
- `program/generated/charts/coastal-rough-lecz-growth.png`  `992ab2bbac3e…`
- `program/generated/charts/coastal-rough-lecz-growth.svg`  `7eaa7a6b1629…`
- `program/generated/charts/coastal-rough-proxy-comparison.png`  `7dd232bd0d77…`
- `program/generated/charts/coastal-rough-proxy-comparison.svg`  `5f72f69457a5…`
- `program/generated/coastal-denominator-spatial-source-audit.json`  `b07f7bcb2ce4…`
- `program/generated/coastal-drop-population-deepening.csv`  `fef76facafab…`
- `program/generated/coastal-drop-population-deepening.json`  `bf2f9e233e5d…`
- `program/generated/coastal-ghs-ucdb-inventory.json`  `14f96830ad80…`
- `program/generated/coastal-ghs-ucdb-members.csv`  `d64cd8a32410…`
- `program/generated/coastal-informal-risk-adb-panel.csv`  `f9c6a2269daf…`
- `program/generated/coastal-informal-risk-adb-panel.json`  `3ddbca76d4dc…`
- `program/generated/coastal-informal-risk-figure-dossier.json`  `d08889252db4…`
- `program/generated/coastal-lecz-growth-diagnostics.json`  `de0ff398289c…`
- `program/generated/coastal-lecz-sensitivity-runs.json`  `2d0f18ee5c5f…`
- `program/generated/coastal-lecz-urban-centre-panel.csv`  `8c951c87d7a4…`
- `program/generated/coastal-spatial-source-readiness-links.csv`  `773ae8ad72ae…`
- `program/generated/coastal-spatial-source-readiness-sources.csv`  `9a80ff48a775…`
- `program/generated/coastal-spatial-source-readiness.json`  `7cf362f2ff3d…`
- `program/scripts/acquire-ghs-ucdb.py`  `b774ae22548d…`
- `program/scripts/audit-coastal-spatial-source-readiness.py`  `b90003c87f0f…`
- `program/scripts/build-figure-dossier.py`  `1ef97c1b4a4d…`
- `program/scripts/build-lecz-growth-object.py`  `467f962bd1cf…`
- `program/scripts/build-thumbnail.py`  `e25122dc6650…`
- `program/scripts/deepen-drop-population.py`  `c4ef14419307…`

### Shared governance

- `shared/CONSTITUTION.md`  `25b8610c5a82…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `6c99b9e1378a…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `0a213e10e598…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `83f1c415aa64…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T19:55:35.692Z by `scripts/build-review-packet.mjs`.
