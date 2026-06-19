# Review packet — air-monitoring — 2026-06-19

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

- `publication/1-working-paper/pm25-observability-gap-cluster.md`  `f30a4b9edb4a…`

### Program artifacts

- `program/STATUS.md`  `bd4f72e023d1…`
- `program/literature.md`  `60a13d873b48…`
- `program/pre-registration.md`  `4281201e57c5…`
- `program/sensitivity.md`  `051bd9c19243…`
- `program/sensitivity-runs.json`  `b2507d182582…`
- `program/coverage.md`  `891119091e8e…`
- `program/results.md`  `c25ebb1871ca…`
- `program/metadata-readiness-audit.md`  `f7ca860908c6…`
- `program/station-metadata-source-access.md`  `ad49202b861f…`
- `program/regulator-source-inventory.md`  `a3caa8a9937f…`
- `program/regulator-station-extraction.md`  `f362817a1c37…`
- `program/monitor-grade-evidence.md`  `8559a7d7843e…`
- `program/official-openaq-reconciliation.md`  `e22bc653e9c1…`
- `program/official-openaq-candidate-review.md`  `66c351c3de50…`
- `program/limitations.md`  `49d4dcf85900…`
- `program/review-internal.md`  `c96d88072943…`
- `program/review-external.md`  `42b7f2c3bf52…`
- `program/generated/air-monitoring-adb-panel.csv`  `ae5b6892577d…`
- `program/generated/air-monitoring-adb-panel.json`  `5940f570c4db…`
- `program/generated/air-monitoring-concentration-deepening.csv`  `50c52a4d3bea…`
- `program/generated/air-monitoring-concentration-deepening.json`  `414eecf9ff39…`
- `program/generated/air-monitoring-metadata-readiness-audit-summary.json`  `987a6fb62839…`
- `program/generated/air-monitoring-metadata-readiness-audit.csv`  `c7aa9c572539…`
- `program/generated/air-monitoring-monitor-grade-evidence-summary.json`  `25793d7087a8…`
- `program/generated/air-monitoring-monitor-grade-evidence.csv`  `df7e2a3eb887…`
- `program/generated/air-monitoring-official-openaq-candidate-review-summary.json`  `770987d49d80…`
- `program/generated/air-monitoring-official-openaq-candidate-review.csv`  `ecedea01ca17…`
- `program/generated/air-monitoring-official-openaq-reconciliation-summary.json`  `195c17128543…`
- `program/generated/air-monitoring-official-openaq-reconciliation.csv`  `c9e9eff78f0d…`
- `program/generated/air-monitoring-openaq-station-metadata-summary.json`  `c864848a3cef…`
- `program/generated/air-monitoring-openaq-station-metadata.csv`  `7c61c2a0ba4e…`
- `program/generated/air-monitoring-regulator-source-inventory-summary.json`  `52be4c018fa8…`
- `program/generated/air-monitoring-regulator-source-inventory.csv`  `5a4a21ed017a…`
- `program/generated/air-monitoring-regulator-station-extraction-summary.json`  `52da12112b68…`
- `program/generated/air-monitoring-regulator-station-extraction.csv`  `109f03865c05…`
- `program/generated/charts/air-monitoring-thumbnail.json`  `b87f82967eea…`
- `program/generated/charts/air-monitoring-thumbnail.png`  `9ceb5b95e31f…`
- `program/generated/charts/air-monitoring-thumbnail.svg`  `e47dcfcd7bc0…`
- `program/scripts/audit-monitor-grade-evidence.py`  `57f5cac1bf0e…`
- `program/scripts/build-metadata-readiness-audit.py`  `868c73ab91e8…`
- `program/scripts/build-official-openaq-candidate-review.py`  `3c6c54513f78…`
- `program/scripts/build-regulator-source-inventory.py`  `a14135438dc3…`
- `program/scripts/build-thumbnail.py`  `9f0a3f2395e3…`
- `program/scripts/deepen-concentration-and-hdi.py`  `d8dc35e3018b…`
- `program/scripts/extract-regulator-station-evidence.py`  `6dab12a1e816…`
- `program/scripts/fetch-openaq-station-metadata.py`  `52311cd5e082…`
- `program/scripts/reconcile-official-openaq-stations.py`  `849137bed27f…`

### Shared governance

- `shared/CONSTITUTION.md`  `530cb682e2fc…`
- `shared/CLAUDE.md`  `b5db191363fb…`
- `shared/references.bib`  `4940e86a69c9…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `1392c2e89cda…`
- `shared/manifest.sha256`  `db692480ff8a…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `b6dc4c42687c…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-06-19T08:08:04.878Z by `scripts/build-review-packet.mjs`.
