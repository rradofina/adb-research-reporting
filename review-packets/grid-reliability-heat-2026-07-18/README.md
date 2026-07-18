# Review packet — grid-reliability-heat — 2026-07-18

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

- `publication/1-working-paper/single-fuel-grid-cluster.md`  `516f78d431a1…`
- `publication/3-brief/grid-reliability-heat.md`  `c0d77fe3bb3a…`
- `publication/4-blog/grid-reliability-heat.md`  `3a33417f3588…`
- `publication/5-social/grid-reliability-heat.md`  `78922e6e7a1c…`
- `publication/6-slides/grid-reliability-heat.md`  `1f7a07d03866…`
- `publication/6-slides/grid-reliability-heat-deck.pptx`  `11a35cfec87a…`

### Program artifacts

- `program/README.md`  `38be96f42df7…`
- `program/STATUS.md`  `a8dbbb74fc13…`
- `program/REPRODUCE.md`  `d33fc1797187…`
- `program/literature.md`  `1a0fdd822dc2…`
- `program/pre-registration.md`  `3d38b30de6da…`
- `program/sensitivity.md`  `cdeeb491fd4e…`
- `program/sensitivity-runs.json`  `9dd103358dd0…`
- `program/coverage.md`  `bc00bffb7d77…`
- `program/results.md`  `37ba6c09342a…`
- `program/limitations.md`  `9aa313d51c67…`
- `program/upgrade-gap.md`  `fe1c87bc00a5…`
- `program/review-internal.md`  `23fbd1fcab5e…`
- `program/review-external.md`  `4ab04a1745d6…`
- `program/generated/charts/grid-capacity-generation-concentration.png`  `604a0da45d1f…`
- `program/generated/charts/grid-capacity-generation-concentration.svg`  `b48425bcd38f…`
- `program/generated/charts/grid-generation-reliability-association.png`  `d30affebe856…`
- `program/generated/charts/grid-generation-reliability-association.svg`  `f1325bd9ddfd…`
- `program/generated/charts/grid-heat-reliability-correlation-matrix.png`  `50b41b26c4f7…`
- `program/generated/charts/grid-heat-reliability-correlation-matrix.svg`  `4a29c518dbea…`
- `program/generated/charts/grid-heat-reliability-sensitivity.png`  `97a7056e9835…`
- `program/generated/charts/grid-heat-reliability-sensitivity.svg`  `0309b3439ad9…`
- `program/generated/charts/grid-reliability-heat-thumbnail.json`  `cd6d85741183…`
- `program/generated/charts/grid-reliability-heat-thumbnail.png`  `4d1a3e35ae12…`
- `program/generated/charts/grid-reliability-heat-thumbnail.svg`  `6c2d4e124d35…`
- `program/generated/charts/grid-reliability-proxy-vintages.png`  `13ac4aedc1ee…`
- `program/generated/charts/grid-reliability-proxy-vintages.svg`  `d8b81785ddb3…`
- `program/generated/charts/grid-source-alignment-funnel.png`  `b74f6931d25c…`
- `program/generated/charts/grid-source-alignment-funnel.svg`  `9ce8c47cec5c…`
- `program/generated/charts/grid-two-gate-validation.png`  `cf3f4996edf5…`
- `program/generated/charts/grid-two-gate-validation.svg`  `86956f69cebb…`
- `program/generated/grid-figure-dossier-summary.json`  `b76f2cd6e721…`
- `program/generated/grid-generation-deepening.csv`  `ae31e1d43e4c…`
- `program/generated/grid-generation-deepening.json`  `b3cdd7ca7391…`
- `program/generated/grid-generation-reliability-diagnostics.csv`  `3367822321b6…`
- `program/generated/grid-generation-reliability-source-audit.json`  `f3fea3956d10…`
- `program/generated/grid-heat-reliability-construct-validation.json`  `232863c0cebd…`
- `program/generated/grid-heat-reliability-diagnostics.csv`  `fcbb968c32d5…`
- `program/generated/grid-heat-reliability-exact-year-crosswalk.csv`  `6bc763fb095c…`
- `program/generated/grid-heat-reliability-source-ledger.json`  `9de87f527fea…`
- `program/generated/grid-public-reliability-proxy-readiness-country.csv`  `cbe56da40c78…`
- `program/generated/grid-public-reliability-proxy-readiness-indicators.csv`  `7f6f51d2caba…`
- `program/generated/grid-public-reliability-proxy-readiness.json`  `7b663f752713…`
- `program/generated/grid-reliability-heat-adb-panel.csv`  `e81a9d7e3d44…`
- `program/generated/grid-reliability-heat-adb-panel.json`  `361c7097879f…`
- `program/scripts/audit-public-reliability-proxies.py`  `4f528dae655c…`
- `program/scripts/build-figure-dossier.py`  `3d252d857a52…`
- `program/scripts/build-joint-heat-reliability-evidence.py`  `5344eaee0f56…`
- `program/scripts/build-thumbnail.py`  `0bf7e408ee65…`
- `program/scripts/deepen-generation.py`  `efb399755bec…`
- `program/scripts/process-grid.py`  `387977307876…`

### Shared governance

- `shared/CONSTITUTION.md`  `3d159027c3d8…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `6bf7bb912f07…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `2cae2815afb2…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `609180ce2fab…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T13:14:20.543Z by `scripts/build-review-packet.mjs`.
