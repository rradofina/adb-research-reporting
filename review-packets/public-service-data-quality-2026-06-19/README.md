# Review packet — public-service-data-quality — 2026-06-19

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

- `publication/1-working-paper/measurement-gap-philippines-bangladesh.md`  `b7f70d129de9…`
- `publication/3-brief/public-service-data-quality.md`  `521a1f296dfa…`
- `publication/4-blog/public-service-data-quality.md`  `15a70fdb85fc…`
- `publication/5-social/public-service-data-quality.md`  `fde6d94aa491…`
- `publication/6-slides/public-service-data-quality.md`  `dc0de43c8d43…`
- `publication/6-slides/public-service-data-quality-deck.pptx`  `aaa9f818e2db…`

### Program artifacts

- `program/README.md`  `7bc164f3c386…`
- `program/STATUS.md`  `2a6463cd4666…`
- `program/REPRODUCE.md`  `625d80e8fde6…`
- `program/SOURCE-ACTION.md`  `bd763bbd155b…`
- `program/literature.md`  `f94f6c0f5cbf…`
- `program/scoring.md`  `ee44d0d49e36…`
- `program/pre-registration.md`  `5f699ba0185e…`
- `program/sensitivity.md`  `d7cf08652578…`
- `program/sensitivity.json`  `641208af1d98…`
- `program/sensitivity-runs.json`  `0cfaa62a91ae…`
- `program/leave-one-out-runs.json`  `bc403c4974cd…`
- `program/coverage.md`  `533d35d8b4c9…`
- `program/results.md`  `c5f1cd46169d…`
- `program/source-disagreement-l3-module.md`  `251d859f6263…`
- `program/facility-validation-sample.md`  `426a18b29d9e…`
- `program/facility-validation-coded-screen.md`  `7842413f6f2b…`
- `program/facility-validation-ai-review.md`  `dec4cb84cca8…`
- `program/facility-validation-candidate-resolution.md`  `d8296dac16c9…`
- `program/facility-validation-candidate-public-source-check.md`  `de5cdfed79c2…`
- `program/facility-validation-coordinate-repair.md`  `faa04e0448fc…`
- `program/facility-validation-public-map-gap.md`  `ac3eeaed6a0e…`
- `program/facility-validation-public-map-gap-evidence.md`  `adb93b914cf5…`
- `program/facility-validation-public-map-inspection.md`  `1fa15c8872f6…`
- `program/facility-validation-public-source-confirmation.md`  `d3beb6947d5d…`
- `program/facility-validation-public-source-confirmation-targeted-rows.md`  `faf2b45c8069…`
- `program/facility-validation-public-source-decision-ledger.md`  `56c44623050e…`
- `program/facility-validation-source-repair-public-evidence.md`  `cbcb871decd1…`
- `program/facility-validation-source-repair-official-coordinate-evidence.md`  `4d556f3556d9…`
- `program/facility-validation-source-repair-public-explanation-evidence.md`  `8ad9950749bd…`
- `program/facility-validation-source-repair-correction-record-followup.md`  `4b37713944e8…`
- `program/facility-validation-source-repair-clarification-packet.md`  `91a32ab47b16…`
- `program/facility-validation-source-repair-registry-vintage-review.md`  `67d76bb31bcf…`
- `program/limitations.md`  `8ac5d2ea407f…`
- `program/upgrade-gap.md`  `207d3df3b8ba…`
- `program/catchment-upgrade.md`  `4f85675317f0…`
- `program/review-internal.md`  `cb2bbe4bbbb4…`
- `program/review-external.md`  `f31d1316c488…`
- `program/SR-to-PR.md`  `692ee564ede8…`
- `program/pipeline.ts`  `b734e213f127…`
- `program/generated/charts/psdq-choropleth-bgd-adm1.png`  `e69a477f522d…`
- `program/generated/charts/psdq-choropleth-bgd-adm1.svg`  `a0df26d7dd9c…`
- `program/generated/charts/psdq-choropleth-phl-adm1.png`  `5b207091ce58…`
- `program/generated/charts/psdq-choropleth-phl-adm1.svg`  `ca715a4f27e7…`
- `program/generated/charts/psdq-choropleth-phl-adm3-poverty.png`  `2750b4a7ed3a…`
- `program/generated/charts/psdq-choropleth-phl-adm3-poverty.svg`  `7f3c6562261e…`
- `program/generated/charts/public-service-data-quality-thumbnail.json`  `2f1769da5850…`
- `program/generated/charts/public-service-data-quality-thumbnail.png`  `bf3401947870…`
- `program/generated/charts/public-service-data-quality-thumbnail.svg`  `6c02a6095771…`
- `program/generated/psdq-bgd-admin-coordinate-summary.csv`  `cc339ef87c91…`
- `program/generated/psdq-bgd-admin-coordinate-summary.json`  `d828e2320b7a…`
- `program/generated/psdq-bgd-exposure-ranked-disagreement-summary.json`  `401761ffe105…`
- `program/generated/psdq-bgd-exposure-ranked-disagreement.csv`  `5749807fd3be…`
- `program/generated/psdq-bgd-exposure-road-context-summary.json`  `77c69ffd16dd…`
- `program/generated/psdq-bgd-exposure-road-context.csv`  `58f3527759b5…`
- `program/generated/psdq-bgd-facility-coordinate-extract.csv`  `6e7cfef0f458…`
- `program/generated/psdq-bgd-facility-coordinate-summary.json`  `b031bc152cbc…`
- `program/generated/psdq-bgd-facility-validation-ai-review-summary.json`  `3f636b7dbdc0…`
- `program/generated/psdq-bgd-facility-validation-ai-review.csv`  `9170cf0d2a6d…`
- `program/generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json`  `87806dd61a88…`
- `program/generated/psdq-bgd-facility-validation-candidate-public-source-check.csv`  `bfb3a66f6297…`
- `program/generated/psdq-bgd-facility-validation-candidate-resolution-summary.json`  `5b176dcc92a6…`
- `program/generated/psdq-bgd-facility-validation-candidate-resolution.csv`  `9a9dde9e93fa…`
- `program/generated/psdq-bgd-facility-validation-coded-screen.csv`  `ff3da51e9bf2…`
- `program/generated/psdq-bgd-facility-validation-coded-summary.json`  `0c9c01426078…`
- `program/generated/psdq-bgd-facility-validation-coding-sheet.csv`  `cdb9950c61c8…`
- `program/generated/psdq-bgd-facility-validation-coordinate-repair-summary.json`  `34eb05ae6939…`
- `program/generated/psdq-bgd-facility-validation-coordinate-repair.csv`  `158436c4bcfe…`
- `program/generated/psdq-bgd-facility-validation-osm-candidates.csv`  `d0347d049cde…`
- `program/generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`  `ca2de90a8b7b…`
- `program/generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv`  `aaf0b7c65aec…`
- `program/generated/psdq-bgd-facility-validation-public-map-gap-summary.json`  `5d12b68e7986…`
- `program/generated/psdq-bgd-facility-validation-public-map-gap.csv`  `23e4596a3c58…`
- `program/generated/psdq-bgd-facility-validation-public-map-inspection-summary.json`  `f6a3a27b28b9…`
- `program/generated/psdq-bgd-facility-validation-public-map-inspection.csv`  `a2063fd5f93b…`
- `program/generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json`  `94c6a5aa9ad7…`
- `program/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`  `1b455324303d…`
- `program/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`  `8ac529c940b2…`
- `program/generated/psdq-bgd-facility-validation-public-source-confirmation.csv`  `4b5ec40f1ec4…`
- `program/generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`  `1458a1245c6a…`
- `program/generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`  `33e2dbe9ae92…`
- `program/generated/psdq-bgd-facility-validation-sample-facilities.csv`  `866de878eae2…`
- `program/generated/psdq-bgd-facility-validation-sample-upazilas.csv`  `d5d76eb5d54d…`
- `program/generated/psdq-bgd-facility-validation-sample.json`  `114abfa96b17…`
- `program/generated/psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json`  `da3b31db9e9b…`
- `program/generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv`  `416f483f5f9a…`
- `program/generated/psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json`  `87bbeec1e7d4…`
- `program/generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv`  `fa076c3a4ee9…`
- `program/generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json`  `6db904700fd0…`
- `program/generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv`  `79a4ce630e2e…`
- `program/generated/psdq-bgd-facility-validation-source-repair-public-evidence-summary.json`  `c0ad65ff5535…`
- `program/generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv`  `23e5d7f403c6…`
- `program/generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json`  `02e52d9a9b25…`
- `program/generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv`  `3d6ac1c8d091…`
- `program/generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json`  `fa8402ed534e…`
- `program/generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv`  `3c0faef63e13…`
- `program/generated/psdq-bgd-open-buildings-admin-summary.csv`  `cff1ea1d4979…`
- `program/generated/psdq-bgd-open-buildings-buffer-summary.json`  `92c84b2b88b2…`
- `program/generated/psdq-bgd-open-buildings-facility-buffers.csv`  `fbb0213342e1…`
- `program/generated/psdq-bgd-open-buildings-tile-manifest.csv`  `f4d8f5fd21ed…`
- `program/generated/psdq-bgd-open-buildings-tile-manifest.json`  `0c0018f61371…`
- `program/generated/psdq-bgd-osm-health-upazila.csv`  `879772625a73…`
- `program/generated/psdq-bgd-road-surface-summary.json`  `e7a8156723b1…`
- `program/generated/psdq-bgd-road-surface-upazila.csv`  `258c5e14e3c1…`
- `program/generated/psdq-bgd-source-disagreement-strata.csv`  `187deae55eb1…`
- `program/generated/psdq-bgd-source-disagreement-strata.json`  `d4ec3023cb62…`
- `program/generated/psdq-catchment-readiness.json`  `aee3865ea916…`
- `program/generated/psdq-phl-admin3-open-buildings-context-summary.json`  `d66fb5bb6f6b…`
- `program/generated/psdq-phl-admin3-open-buildings-context.csv`  `7bb77ffee06c…`
- `program/generated/psdq-phl-admin3-poverty-context-summary.json`  `7e9b1a2f42b9…`
- `program/generated/psdq-phl-admin3-poverty-context.csv`  `cf89539b8dac…`
- `program/generated/psdq-phl-nhfr-barmm-ctymun-resolution.json`  `1768925b8d00…`
- `program/generated/psdq-phl-open-buildings-tile-manifest.csv`  `e177291d3298…`
- `program/generated/psdq-phl-open-buildings-tile-manifest.json`  `126de2872511…`
- `program/generated/psdq-tier-decomposition.csv`  `10f78609dd54…`
- `program/generated/psdq-tier-decomposition.json`  `0a9afc1c25d3…`
- `program/generated/public-service-data-quality-BGD.csv`  `ab7b8a3cec55…`
- `program/generated/public-service-data-quality-BGD.json`  `c953ece060e9…`
- `program/generated/public-service-data-quality-PHL.csv`  `5b1da51865ff…`
- `program/generated/public-service-data-quality-PHL.json`  `56af98aef971…`
- `program/generated/public-service-data-quality-summary.json`  `cdd864383a28…`
- `program/scripts/attach-bgd-facility-source-repair-public-evidence.py`  `2e280e1f8992…`
- `program/scripts/audit-catchment-readiness.py`  `bb030f0c65e0…`
- `program/scripts/build-bgd-exposure-ranked-disagreement.py`  `1171943a92b8…`
- `program/scripts/build-bgd-facility-extract.py`  `bc7a0a7751e3…`
- `program/scripts/build-bgd-facility-public-map-gap-row-evidence.py`  `dc3093edc317…`
- `program/scripts/build-bgd-facility-public-source-decision-ledger.py`  `0e2072550236…`
- `program/scripts/build-bgd-facility-source-repair-clarification-packet.py`  `ed8d86fb6be1…`
- `program/scripts/build-bgd-facility-source-repair-registry-vintage-review.py`  `97613087ef3b…`
- `program/scripts/build-bgd-road-surface-context.py`  `dd5e729be664…`
- `program/scripts/build-bgd-source-disagreement-strata.py`  `e6e8c541d683…`
- `program/scripts/build-choropleth.py`  `afee4e2effe2…`
- `program/scripts/build-phl-admin3-open-buildings-context.py`  `baa57e9a5e75…`
- `program/scripts/build-phl-admin3-poverty-context.py`  `2e07dbbb486a…`
- `program/scripts/build-thumbnail.py`  `a967e9acc16e…`
- `program/scripts/check-bgd-facility-candidate-public-sources.py`  `c2c271028066…`
- `program/scripts/code-bgd-facility-validation-sample.py`  `3d82c1452223…`
- `program/scripts/compute-bgd-open-buildings-facility-buffers.py`  `b8916cab9fe7…`
- `program/scripts/confirm-bgd-facility-public-map-first-rows.py`  `5282973a0b76…`
- `program/scripts/confirm-bgd-facility-public-map-targeted-rows.py`  `fd7f5d132a4b…`
- `program/scripts/deepen-tier-decomposition.py`  `ffd440ac9868…`
- `program/scripts/design-bgd-facility-validation-sample.py`  `c7eca1cd58ce…`
- `program/scripts/download-bgd-open-buildings-points.py`  `2fad4159cad8…`
- `program/scripts/download-phl-open-buildings-points.py`  `5d030fc8df99…`
- `program/scripts/explain-bgd-facility-source-repair-official-coordinates.py`  `0a278a740cd8…`
- `program/scripts/fetch-bgd-public-facilities.py`  `299e5597f30d…`
- `program/scripts/fetch-nhfr.sh`  `f43f894ada5a…`
- `program/scripts/fetch-phl-sae-poverty.py`  `70452d5894f4…`
- `program/scripts/followup-bgd-facility-source-repair-correction-records.py`  `c68ed7cfb160…`
- `program/scripts/inspect-barmm-codes.py`  `c039e8b9d3a1…`
- `program/scripts/inspect-bgd-facility-public-map-targets.py`  `0dbeeec23fde…`
- `program/scripts/leave-one-out.py`  `b6bb16c5473a…`
- `program/scripts/prepare-bgd-open-buildings-manifest.py`  `fe8847a9bc43…`
- `program/scripts/prepare-phl-open-buildings-manifest.py`  `b051509beab2…`
- `program/scripts/process-bgd.py`  `12886ad8bf46…`
- `program/scripts/process-disagreement.py`  `b8e60d278ff4…`
- `program/scripts/process-multi-country.py`  `6256f065f18c…`
- `program/scripts/resolve-bgd-facility-candidate-rows.py`  `2d859452774e…`
- `program/scripts/review-bgd-facility-validation-flags.py`  `c9aa5e6653f9…`
- `program/scripts/search-bgd-facility-source-repair-public-explanations.py`  `e1682e4a0a18…`
- `program/scripts/sensitivity-bgd.py`  `2665382bf7e4…`
- `program/scripts/sensitivity.py`  `8c1597d71737…`
- `program/scripts/triage-bgd-facility-coordinate-repairs.py`  `827f77cd987c…`
- `program/scripts/triage-bgd-facility-public-map-gaps.py`  `85b362caf768…`

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

— Generated 2026-06-19T02:53:52.487Z by `scripts/build-review-packet.mjs`.
