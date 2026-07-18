# Review packet — climate-health-workdays — 2026-07-18

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

- `publication/1-working-paper/workday-loss-pressure-cluster.md`  `1b3157c9231d…`
- `publication/3-brief/climate-health-workdays.md`  `7be455751659…`
- `publication/4-blog/climate-health-workdays.md`  `ef85c43110ee…`
- `publication/5-social/climate-health-workdays.md`  `eaef4ad1ccbb…`
- `publication/6-slides/climate-health-workdays.md`  `927f6b836411…`
- `publication/6-slides/climate-health-workdays-deck.pptx`  `67963de8c8e6…`

### Program artifacts

- `program/README.md`  `ef38ebd1c1e3…`
- `program/STATUS.md`  `621f4874eb89…`
- `program/REPRODUCE.md`  `d791f330a788…`
- `program/literature.md`  `f5f61c11f276…`
- `program/pre-registration.md`  `c18b31d4a075…`
- `program/sensitivity.md`  `6f9be4ed63b9…`
- `program/sensitivity-runs.json`  `f87bc78bf7e2…`
- `program/coverage.md`  `1436b72d18c0…`
- `program/results.md`  `8f36d53a5ea6…`
- `program/limitations.md`  `f73a4f31612f…`
- `program/upgrade-gap.md`  `d2717af8dd9b…`
- `program/review-internal.md`  `b0faa74dd964…`
- `program/review-external.md`  `8592d9549e37…`
- `program/generated/charts/climate-construct-rank-disagreement.png`  `6da62880082e…`
- `program/generated/charts/climate-construct-rank-disagreement.svg`  `d10b5de27fea…`
- `program/generated/charts/climate-construct-sensitivity.png`  `eb7d9609ed82…`
- `program/generated/charts/climate-construct-sensitivity.svg`  `ee536d8add6e…`
- `program/generated/charts/climate-health-workdays-thumbnail.json`  `ba4dad56cb00…`
- `program/generated/charts/climate-health-workdays-thumbnail.png`  `bce16af09a99…`
- `program/generated/charts/climate-health-workdays-thumbnail.svg`  `5707df001d40…`
- `program/generated/charts/climate-heat-loss-profile-2024.png`  `a457dd632042…`
- `program/generated/charts/climate-heat-loss-profile-2024.svg`  `86cee027ade9…`
- `program/generated/charts/climate-heat-loss-rate-vs-scale.png`  `a9d4fb3cd61c…`
- `program/generated/charts/climate-heat-loss-rate-vs-scale.svg`  `e9ac36470470…`
- `program/generated/charts/climate-heat-loss-sector-composition.png`  `7ab58afaa6b6…`
- `program/generated/charts/climate-heat-loss-sector-composition.svg`  `1f7c24f03b25…`
- `program/generated/charts/climate-source-coverage.png`  `e5305c280ed4…`
- `program/generated/charts/climate-source-coverage.svg`  `120a01025116…`
- `program/generated/charts/climate-worker-denominator-repair.png`  `acc2395e3ccb…`
- `program/generated/charts/climate-worker-denominator-repair.svg`  `a00fe47b891b…`
- `program/generated/climate-health-construct-validation.json`  `68ec241cfef7…`
- `program/generated/climate-health-figure-dossier-summary.json`  `d26714d186dd…`
- `program/generated/climate-health-heat-workloss-panel.csv`  `a59157e72b16…`
- `program/generated/climate-health-heat-workloss-panel.json`  `98fbd2c32ef7…`
- `program/generated/climate-health-labor-denominator-observed.csv`  `b6e3415023c6…`
- `program/generated/climate-health-labor-heat-source-readiness-sources.csv`  `f34e8d83a892…`
- `program/generated/climate-health-labor-heat-source-readiness.json`  `3b1757b44b86…`
- `program/generated/climate-health-proxy-heat-comparison.csv`  `7bf3ec543fcf…`
- `program/generated/climate-health-workdays-adb-panel.csv`  `61a5208f3a80…`
- `program/generated/climate-health-workdays-adb-panel.json`  `faaad5d34ac8…`
- `program/generated/climate-health-workdays-deepening.json`  `54c4d634ccf2…`
- `program/generated/climate-health-workdays-denominator-source-audit.json`  `aef4f94129d5…`
- `program/scripts/audit-labor-heat-source-readiness.py`  `1952d4fe8c6d…`
- `program/scripts/build-figure-dossier.py`  `b6b6d609f91f…`
- `program/scripts/build-heat-workloss-evidence.py`  `1a3a392a749a…`
- `program/scripts/build-thumbnail.py`  `df2e847cc2e0…`
- `program/scripts/deepen-cap-and-laborforce.py`  `04762105e0ee…`
- `program/scripts/process-climate-health.py`  `2fbf28b5d821…`
- `program/scripts/sensitivity.py`  `fee2b3305a89…`

### Shared governance

- `shared/CONSTITUTION.md`  `3d159027c3d8…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `a359a542c508…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `37654d8d1155…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `b6dc4c42687c…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T11:32:39.005Z by `scripts/build-review-packet.mjs`.
