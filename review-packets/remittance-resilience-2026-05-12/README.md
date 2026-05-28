# Review packet — remittance-resilience — 2026-05-12

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
   caches and code are under `program/scripts/` and `program/generated/`.

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

- `publication/1-working-paper/remittance-corridors-vulnerability-cluster.md`  `5a2956875f5e…`
- `publication/3-brief/remittance-resilience.md`  `d65189ab03f6…`
- `publication/4-blog/remittance-resilience.md`  `81186e50e3ca…`
- `publication/5-social/remittance-resilience.md`  `1e304fce0be4…`
- `publication/6-slides/remittance-resilience.md`  `64ca34433d91…`
- `publication/6-slides/remittance-resilience-deck.pptx`  `29104f8b44eb…`

### Program artifacts

- `program/README.md`  `34d80a0b9246…`
- `program/STATUS.md`  `a27460926ab4…`
- `program/literature.md`  `cdfe684e08a4…`
- `program/pre-registration.md`  `b61b73a91490…`
- `program/sensitivity.md`  `1c8067588528…`
- `program/sensitivity-runs.json`  `b0956097af26…`
- `program/coverage.md`  `136538fe62ed…`
- `program/results.md`  `67d433266d71…`
- `program/limitations.md`  `d89f030f1ace…`
- `program/review-internal.md`  `e08c42f065b9…`
- `program/review-external.md`  `92c9a411ba28…`
- `program/generated/charts/remittance-fragility-scatter.png`  `7924f1c5b433…`
- `program/generated/charts/remittance-fragility-scatter.svg`  `ecdc0eea6589…`
- `program/generated/remittance-resilience-adb-panel.csv`  `faa7f03767bd…`
- `program/generated/remittance-resilience-adb-panel.json`  `1c9ab2b8f2cc…`
- `program/scripts/build-fragility-chart.py`  `d8bf9dbd88b2…`
- `program/scripts/process-remittance.py`  `32905baae5f1…`
- `program/scripts/sensitivity.py`  `8477df07f460…`

### Shared governance

- `shared/CONSTITUTION.md`  `530cb682e2fc…`
- `shared/CLAUDE.md`  `b5db191363fb…`
- `shared/references.bib`  `4940e86a69c9…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `cd95ff179a33…`
- `shared/manifest.sha256`  `db692480ff8a…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `b6dc4c42687c…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-05-12T01:48:08.621Z by `scripts/build-review-packet.mjs`.
