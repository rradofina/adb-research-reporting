# Review packet — flood-market-access — 2026-07-19

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

- `publication/1-working-paper/flood-market-access-cluster.md`  `5c27f11c6962…`
- `publication/3-brief/flood-market-access-cluster.md`  `db395a689bf9…`
- `publication/4-blog/flood-market-access-cluster.md`  `466e3cd08422…`
- `publication/5-social/flood-market-access-cluster.md`  `b7b6a6b3d9b2…`
- `publication/6-slides/flood-market-access-cluster.md`  `20eda8ca5832…`

### Program artifacts

- `program/README.md`  `25032c028c4f…`
- `program/STATUS.md`  `57af9fe6d634…`
- `program/REPRODUCE.md`  `21669b5898cb…`
- `program/literature.md`  `38e8d9213f22…`
- `program/pre-registration.md`  `e11c75b74928…`
- `program/sensitivity.md`  `8d1560cfb1a9…`
- `program/sensitivity-runs.json`  `f16efdae049e…`
- `program/coverage.md`  `cd5b79d1264e…`
- `program/results.md`  `0c7c97051e85…`
- `program/limitations.md`  `6c8083ab8169…`
- `program/review-internal.md`  `1a6b88f70361…`
- `program/review-external.md`  `f1c44c32a472…`
- `program/generated/charts/flood-market-access-thumbnail.json`  `db0013b8a9c7…`
- `program/generated/charts/flood-market-access-thumbnail.png`  `0eedf51f4d6b…`
- `program/generated/charts/flood-market-access-thumbnail.svg`  `ab891224919f…`
- `program/generated/charts/flood-sylhet-access-split.png`  `cc03de193ae3…`
- `program/generated/charts/flood-sylhet-access-split.svg`  `819bbd3a5034…`
- `program/generated/charts/flood-sylhet-claim-gates.png`  `19b0d0786d68…`
- `program/generated/charts/flood-sylhet-claim-gates.svg`  `d7f8b2e91ad9…`
- `program/generated/charts/flood-sylhet-coverage-funnel.png`  `172daa237632…`
- `program/generated/charts/flood-sylhet-coverage-funnel.svg`  `53a4c751e938…`
- `program/generated/charts/flood-sylhet-market-gate.png`  `4d8c687d9582…`
- `program/generated/charts/flood-sylhet-market-gate.svg`  `a3f75b012cbc…`
- `program/generated/charts/flood-sylhet-road-set.png`  `36503721f34d…`
- `program/generated/charts/flood-sylhet-road-set.svg`  `715dc6502114…`
- `program/generated/charts/flood-sylhet-route-map.png`  `1d0c371ebc38…`
- `program/generated/charts/flood-sylhet-route-map.svg`  `1bb4af695649…`
- `program/generated/charts/flood-sylhet-sensitivity.png`  `cb49c55e2755…`
- `program/generated/charts/flood-sylhet-sensitivity.svg`  `5bb3a71cdc9f…`
- `program/generated/charts/flood-sylhet-source-disagreement.png`  `fb23c04c0c1d…`
- `program/generated/charts/flood-sylhet-source-disagreement.svg`  `3233d20204f6…`
- `program/generated/charts/flood-sylhet-survivor-selection.png`  `08df4f2235d6…`
- `program/generated/charts/flood-sylhet-survivor-selection.svg`  `706e70094b9b…`
- `program/generated/flood-access-source-readiness-links.csv`  `dbf7972d20cc…`
- `program/generated/flood-access-source-readiness-sources.csv`  `1e1f408ac5c7…`
- `program/generated/flood-access-source-readiness.json`  `1c6f98da9181…`
- `program/generated/flood-decompose-deepening.csv`  `4d3ed00c3684…`
- `program/generated/flood-decompose-deepening.json`  `0fefced0bedc…`
- `program/generated/flood-decomposition-access-source-audit.json`  `b8421c50cc9e…`
- `program/generated/flood-market-access-adb-panel.csv`  `7744172ee7f5…`
- `program/generated/flood-market-access-adb-panel.json`  `447562ca8692…`
- `program/generated/flood-sylhet-markets.csv`  `5bebbd00d041…`
- `program/generated/flood-sylhet-route-pilot.json`  `be82658d5a65…`
- `program/generated/flood-sylhet-route-sensitivity.csv`  `da48bddcfc29…`
- `program/scripts/audit-access-source-readiness.py`  `0235d7043106…`
- `program/scripts/build-figure-dossier.py`  `3a8ef4fea860…`
- `program/scripts/build-sylhet-route-pilot.py`  `ae20a00fcc6b…`
- `program/scripts/build-thumbnail.py`  `e2c7cd21cf0c…`
- `program/scripts/deepen-decompose.py`  `3fede7aba76c…`

### Shared governance

- `shared/CONSTITUTION.md`  `e8176d8973fe…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `796aafac2ac4…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `0a213e10e598…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `192c861faf9a…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T18:40:18.252Z by `scripts/build-review-packet.mjs`.
