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

- `publication/1-working-paper/pm25-observability-gap-cluster.md`  `f30a4b9edb4a…`

### Program artifacts

- `program/STATUS.md`  `4aa3dbef460b…`
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
- `program/official-openaq-candidate-public-evidence.md`  `4a26808ac815…`
- `program/official-openaq-candidate-crosswalk-source-scan.md`  `5dd3c81fcdeb…`
- `program/official-openaq-candidate-public-feed-source-scan.md`  `7a627b81a080…`
- `program/one-signal-review-queue.md`  `df187fe6d954…`
- `program/monitor-grade-source-validation-scan.md`  `b6a20db700f7…`
- `program/monitor-grade-station-review-queue.md`  `b4a6aeab25a2…`
- `program/monitor-grade-station-method-evidence.md`  `fbfac3f8e157…`
- `program/uzbekistan-station-current-method-scan.md`  `3e83cd66bfa3…`
- `program/uzbekistan-method-policy-source-scan.md`  `e4437366159a…`
- `program/uzbekistan-station-specific-source-evidence.md`  `a70f3565c7f0…`
- `program/uzbekistan-status-certification-source-scan.md`  `2467dd4f9979…`
- `program/uzbekistan-blocker-row-followup.md`  `032201fbb6f6…`
- `program/indonesia-georgia-row-method-source-scan.md`  `886896170c19…`
- `program/station-code-status-method-source-scan.md`  `b19e2da4023a…`
- `program/limitations.md`  `443353d0f8d4…`
- `program/review-internal.md`  `c96d88072943…`
- `program/review-external.md`  `42b7f2c3bf52…`
- `program/generated/air-monitoring-adb-panel.csv`  `ae5b6892577d…`
- `program/generated/air-monitoring-adb-panel.json`  `5940f570c4db…`
- `program/generated/air-monitoring-concentration-deepening.csv`  `50c52a4d3bea…`
- `program/generated/air-monitoring-concentration-deepening.json`  `414eecf9ff39…`
- `program/generated/air-monitoring-indonesia-georgia-row-method-source-scan-summary.json`  `54b8cf070976…`
- `program/generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv`  `4a216b54fec0…`
- `program/generated/air-monitoring-metadata-readiness-audit-summary.json`  `987a6fb62839…`
- `program/generated/air-monitoring-metadata-readiness-audit.csv`  `c7aa9c572539…`
- `program/generated/air-monitoring-monitor-grade-evidence-summary.json`  `25793d7087a8…`
- `program/generated/air-monitoring-monitor-grade-evidence.csv`  `df7e2a3eb887…`
- `program/generated/air-monitoring-monitor-grade-source-validation-scan-summary.json`  `8535f7596a82…`
- `program/generated/air-monitoring-monitor-grade-source-validation-scan.csv`  `d2ffe6b2790e…`
- `program/generated/air-monitoring-monitor-grade-station-method-evidence-summary.json`  `f167d18e9d3f…`
- `program/generated/air-monitoring-monitor-grade-station-method-evidence.csv`  `7d671253195e…`
- `program/generated/air-monitoring-monitor-grade-station-review-queue-summary.json`  `bfec8151b994…`
- `program/generated/air-monitoring-monitor-grade-station-review-queue.csv`  `1e4d266e38bb…`
- `program/generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json`  `1c1e1c8b4b35…`
- `program/generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv`  `71cebe893149…`
- `program/generated/air-monitoring-official-openaq-candidate-public-evidence-summary.json`  `fb5141e6223b…`
- `program/generated/air-monitoring-official-openaq-candidate-public-evidence.csv`  `098fc2fb224b…`
- `program/generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json`  `d25aa9915877…`
- `program/generated/air-monitoring-official-openaq-candidate-public-feed-source-scan.csv`  `263ef9cf7bbe…`
- `program/generated/air-monitoring-official-openaq-candidate-review-summary.json`  `770987d49d80…`
- `program/generated/air-monitoring-official-openaq-candidate-review.csv`  `ecedea01ca17…`
- `program/generated/air-monitoring-official-openaq-reconciliation-summary.json`  `195c17128543…`
- `program/generated/air-monitoring-official-openaq-reconciliation.csv`  `c9e9eff78f0d…`
- `program/generated/air-monitoring-one-signal-review-queue-summary.json`  `0c79a09f812e…`
- `program/generated/air-monitoring-one-signal-review-queue.csv`  `4f8ac6dbed7d…`
- `program/generated/air-monitoring-openaq-station-metadata-summary.json`  `c864848a3cef…`
- `program/generated/air-monitoring-openaq-station-metadata.csv`  `7c61c2a0ba4e…`
- `program/generated/air-monitoring-regulator-source-inventory-summary.json`  `52be4c018fa8…`
- `program/generated/air-monitoring-regulator-source-inventory.csv`  `5a4a21ed017a…`
- `program/generated/air-monitoring-regulator-station-extraction-summary.json`  `52da12112b68…`
- `program/generated/air-monitoring-regulator-station-extraction.csv`  `109f03865c05…`
- `program/generated/air-monitoring-station-code-status-method-source-scan-summary.json`  `2d4981bb728a…`
- `program/generated/air-monitoring-station-code-status-method-source-scan.csv`  `2b382f70164f…`
- `program/generated/air-monitoring-uzbekistan-blocker-row-followup-summary.json`  `f28133711283…`
- `program/generated/air-monitoring-uzbekistan-blocker-row-followup.csv`  `282ff688036b…`
- `program/generated/air-monitoring-uzbekistan-method-policy-source-scan-summary.json`  `97268656c32f…`
- `program/generated/air-monitoring-uzbekistan-method-policy-source-scan.csv`  `895513fceb6f…`
- `program/generated/air-monitoring-uzbekistan-station-current-method-scan-summary.json`  `747149f5515d…`
- `program/generated/air-monitoring-uzbekistan-station-current-method-scan.csv`  `8b8d67400a95…`
- `program/generated/air-monitoring-uzbekistan-station-specific-source-evidence-summary.json`  `361bcbf60bbc…`
- `program/generated/air-monitoring-uzbekistan-station-specific-source-evidence.csv`  `d017d5fee3fc…`
- `program/generated/air-monitoring-uzbekistan-status-certification-source-scan-summary.json`  `42967f2db521…`
- `program/generated/air-monitoring-uzbekistan-status-certification-source-scan.csv`  `1e705a3b2feb…`
- `program/generated/charts/air-monitoring-thumbnail.json`  `b87f82967eea…`
- `program/generated/charts/air-monitoring-thumbnail.png`  `9ceb5b95e31f…`
- `program/generated/charts/air-monitoring-thumbnail.svg`  `e47dcfcd7bc0…`
- `program/scripts/audit-monitor-grade-evidence.py`  `57f5cac1bf0e…`
- `program/scripts/audit-monitor-grade-station-method-evidence.py`  `dc668ca9aa39…`
- `program/scripts/audit-official-openaq-candidate-public-evidence.py`  `65df72c733de…`
- `program/scripts/build-metadata-readiness-audit.py`  `868c73ab91e8…`
- `program/scripts/build-monitor-grade-station-review-queue.py`  `6b1630ba0f25…`
- `program/scripts/build-official-openaq-candidate-review.py`  `3c6c54513f78…`
- `program/scripts/build-one-signal-review-queue.py`  `4be11f591ba7…`
- `program/scripts/build-regulator-source-inventory.py`  `a14135438dc3…`
- `program/scripts/build-thumbnail.py`  `9f0a3f2395e3…`
- `program/scripts/deepen-concentration-and-hdi.py`  `d8dc35e3018b…`
- `program/scripts/extract-regulator-station-evidence.py`  `6dab12a1e816…`
- `program/scripts/fetch-openaq-station-metadata.py`  `52311cd5e082…`
- `program/scripts/reconcile-official-openaq-stations.py`  `849137bed27f…`
- `program/scripts/scan-indonesia-georgia-row-method-sources.py`  `52114b8fb72e…`
- `program/scripts/scan-monitor-grade-source-validation.py`  `222cbabff00f…`
- `program/scripts/scan-official-openaq-candidate-crosswalk-sources.py`  `988d701d01a6…`
- `program/scripts/scan-official-openaq-candidate-public-feed-sources.py`  `d2ec39679996…`
- `program/scripts/scan-station-code-status-method-sources.py`  `91ac1b4eb18e…`
- `program/scripts/scan-uzbekistan-blocker-row-followup.py`  `0d2b5def1609…`
- `program/scripts/scan-uzbekistan-method-policy-sources.py`  `e7a213aca655…`
- `program/scripts/scan-uzbekistan-station-current-method-evidence.py`  `5bb39ec0f642…`
- `program/scripts/scan-uzbekistan-station-specific-source-evidence.py`  `b387a3b56c4b…`
- `program/scripts/scan-uzbekistan-status-certification-sources.py`  `8f2feb0905d6…`
- `program/source-inputs/candidate-crosswalk-public-source-seed.csv`  `f8c24b78e130…`
- `program/source-inputs/candidate-public-feed-source-seed.csv`  `65a5cdf1a6c2…`
- `program/source-inputs/indonesia-georgia-row-method-source-seed.csv`  `b80f97d56eb6…`
- `program/source-inputs/monitor-grade-source-validation-seed.csv`  `c0a34b18db10…`
- `program/source-inputs/regulator-source-inventory-seed.csv`  `53c155ad76dd…`
- `program/source-inputs/station-code-status-method-source-seed.csv`  `910d050d8f79…`
- `program/source-inputs/uzbekistan-blocker-row-followup-targets.csv`  `515515fa5f72…`
- `program/source-inputs/uzbekistan-method-policy-source-seed.csv`  `9f1588f0231a…`
- `program/source-inputs/uzbekistan-station-specific-source-seed.csv`  `e0779527d470…`
- `program/source-inputs/uzbekistan-status-certification-source-seed.csv`  `05676fb82e1e…`

### Shared governance

- `shared/CONSTITUTION.md`  `530cb682e2fc…`
- `shared/CLAUDE.md`  `b5db191363fb…`
- `shared/references.bib`  `4940e86a69c9…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `435b5d8d08fb…`
- `shared/manifest.sha256`  `db692480ff8a…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `b6dc4c42687c…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-06-19T14:03:30.607Z by `scripts/build-review-packet.mjs`.
