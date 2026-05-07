# Review packet — public-service-data-quality — 2026-04-25

This is a self-contained snapshot of the evidence the program owner
asks the reviewer to assess. Per CONSTITUTION.md §9.3 and red-team.md.

## How to read this packet

1. Read `shared/CONSTITUTION.md` for the rules every program in the
   lab is governed by. The relevant sections for this review are §6
   (methods), §7 (claim-maturity gates), §9 (review process), §13.3
   (DMC framing), and §14 (taste heuristics).
2. Read `program/README.md` for the program overview.
3. Read `program/literature.md` for the systematic Tier-A/B/C scan.
4. Read `program/pre-registration.md` for the frozen claim, falsification
   condition, and arbitrary-numerics inventory.
5. Read `program/sensitivity.md` and `program/sensitivity-runs.json`
   for the ±50 percent test results.
6. Read `program/results.md` for the screening artifact.
7. Read `program/limitations.md` for what the result cannot establish.
8. Read `program/article-*.md` for the human-readable summary.
9. Optionally re-run the pipeline from a clean clone of the upstream
   repository at the commit hash recorded in `shared/manifest.sha256`.

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

### Program artifacts

- `program/README.md`  `2750a4802876…`
- `program/literature.md`  `ed923acc5cd2…`
- `program/scoring.md`  `ee44d0d49e36…`
- `program/pre-registration.md`  `0b04704f0c17…`
- `program/sensitivity.md`  `d7cf08652578…`
- `program/sensitivity.json`  `641208af1d98…`
- `program/sensitivity-runs.json`  `0cfaa62a91ae…`
- `program/coverage.md`  `533d35d8b4c9…`
- `program/results.md`  `51ea7fd31d17…`
- `program/limitations.md`  `b2e542a01981…`
- `program/review-internal.md`  `457624ccb03b…`
- `program/review-external.md`  `be4a43b3fbd2…`
- `program/SR-to-PR.md`  `692ee564ede8…`
- `program/pipeline.ts`  `b734e213f127…`
- `program/generated/public-service-data-quality-BGD.csv`  `ab7b8a3cec55…`
- `program/generated/public-service-data-quality-BGD.json`  `c953ece060e9…`
- `program/generated/public-service-data-quality-PHL.csv`  `5b1da51865ff…`
- `program/generated/public-service-data-quality-PHL.json`  `56af98aef971…`
- `program/generated/public-service-data-quality-summary.json`  `cdd864383a28…`
- `program/scripts/fetch-nhfr.sh`  `f43f894ada5a…`
- `program/scripts/process-bgd.py`  `f62475980bc1…`
- `program/scripts/process-disagreement.py`  `30b5e4c4fcc2…`
- `program/scripts/process-multi-country.py`  `7e31d826a47b…`
- `program/scripts/sensitivity-bgd.py`  `aa00e4c0b839…`
- `program/scripts/sensitivity.py`  `e908feb944cc…`
- `program/article-measurement-gap-philippines-bangladesh.md`  `636f79fe626c…`

### Shared governance

- `shared/CONSTITUTION.md`  `ab7bfc579832…`
- `shared/CLAUDE.md`  `4bbc14fee394…`
- `shared/references.bib`  `cff3965aa545…`
- `shared/red-team.md`  `e77fccd09e35…`
- `shared/versions.json`  `cd95ff179a33…`
- `shared/manifest.sha256`  `db692480ff8a…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `b4b62e057ec8…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-04-25T14:05:09.628Z by `scripts/build-review-packet.mjs`.
