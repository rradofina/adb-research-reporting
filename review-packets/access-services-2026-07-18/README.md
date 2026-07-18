# Review packet — access-services — 2026-07-18

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

- `publication/1-working-paper/access-stress-pilot-cluster.md`  `13e51d4b6c04…`
- `publication/3-brief/access-services.md`  `be3804a968a5…`
- `publication/4-blog/access-services.md`  `d028e132c861…`
- `publication/5-social/access-services.md`  `59062cd5434c…`
- `publication/6-slides/access-services.md`  `b9f1c8b7b5f0…`
- `publication/6-slides/access-services-deck.pptx`  `720b8af62b75…`

### Program artifacts

- `program/STATUS.md`  `54f679641e2d…`
- `program/REPRODUCE.md`  `e897374f96b5…`
- `program/literature.md`  `1fba620f8c34…`
- `program/pre-registration.md`  `818034969d2e…`
- `program/sensitivity.md`  `50db644bc9d9…`
- `program/sensitivity-runs.json`  `2f97b0c4a47b…`
- `program/coverage.md`  `8e02951387c0…`
- `program/results.md`  `7a516f16379d…`
- `program/limitations.md`  `088c25388c9d…`
- `program/upgrade-gap.md`  `9e474c6124f7…`
- `program/review-internal.md`  `8c659dbb5ce2…`
- `program/review-external.md`  `9864e97c673e…`
- `program/generated/access-cambodia-health-facility-source-audit.csv`  `5089ddfc9672…`
- `program/generated/access-cambodia-health-facility-source-audit.json`  `5aa098378fa9…`
- `program/generated/access-cambodia-health-facility-source-names.csv`  `6ddc1d7522f9…`
- `program/generated/access-figure-dossier-summary.json`  `bd71ac1bd274…`
- `program/generated/access-osm-completeness-deepening-phl.csv`  `a2d0fe9480dc…`
- `program/generated/access-osm-completeness-deepening.json`  `7cb18fad6eda…`
- `program/generated/access-services-adb-panel.csv`  `0f8014e158c2…`
- `program/generated/access-services-adb-panel.json`  `f3aa05ff388e…`
- `program/generated/charts/access-cambodia-source-disagreement.png`  `041244349f8b…`
- `program/generated/charts/access-cambodia-source-disagreement.svg`  `6c7661c33147…`
- `program/generated/charts/access-cross-economy-registry-readiness.png`  `1496dfb1c82d…`
- `program/generated/charts/access-cross-economy-registry-readiness.svg`  `96c205474273…`
- `program/generated/charts/access-phl-completeness-signal.png`  `65007b49df2e…`
- `program/generated/charts/access-phl-completeness-signal.svg`  `96788cb67a17…`
- `program/generated/charts/access-phl-rank-shift.png`  `e3a9c2004ab5…`
- `program/generated/charts/access-phl-rank-shift.svg`  `3bc98904a71a…`
- `program/generated/charts/access-services-thumbnail.json`  `d2d11217d72b…`
- `program/generated/charts/access-services-thumbnail.png`  `7795ebab4d7a…`
- `program/generated/charts/access-services-thumbnail.svg`  `af3ab36d3370…`
- `program/scripts/audit-cambodia-health-facility-source.py`  `80039dbd0e00…`
- `program/scripts/build-figure-dossier.py`  `8f2bdedbf098…`
- `program/scripts/build-thumbnail.py`  `6818a3bbf487…`
- `program/scripts/deepen-osm-completeness.py`  `ef7f5acf8358…`

### Shared governance

- `shared/CONSTITUTION.md`  `3d159027c3d8…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `4940e86a69c9…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `5137e5e94b4f…`
- `shared/manifest.sha256`  `db692480ff8a…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `b6dc4c42687c…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T09:42:15.127Z by `scripts/build-review-packet.mjs`.
