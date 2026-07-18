# Review packet — water-stress-crop-diversification — 2026-07-18

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

- `publication/1-working-paper/water-crop-pressure-cluster.md`  `25ee09b3beb0…`
- `publication/3-brief/water-crop-pressure-cluster.md`  `e0a5aad2e8c1…`
- `publication/4-blog/water-crop-pressure-cluster.md`  `dcb128139e66…`
- `publication/5-social/water-crop-pressure-cluster.md`  `48389710e897…`
- `publication/6-slides/water-crop-pressure-cluster.md`  `d7d1a0db0a43…`
- `publication/6-slides/water-stress-crop-diversification-deck.pptx`  `1e93aff6288c…`

### Program artifacts

- `program/README.md`  `d3a3e607dd0b…`
- `program/STATUS.md`  `433dfa42125b…`
- `program/REPRODUCE.md`  `3b66e6835efb…`
- `program/literature.md`  `d5ebc17ec91e…`
- `program/pre-registration.md`  `b45b8017a0c0…`
- `program/sensitivity.md`  `c5c195a3dfae…`
- `program/sensitivity-runs.json`  `09c1c7693003…`
- `program/coverage.md`  `90a018d38a56…`
- `program/results.md`  `d5f195d47e52…`
- `program/limitations.md`  `8166e9f040e1…`
- `program/upgrade-gap.md`  `2b2dd85a7b04…`
- `program/review-internal.md`  `3f9a60573021…`
- `program/review-external.md`  `01233965c0e6…`
- `program/generated/charts/water-crop-concentration-profiles.png`  `5722b76ee0d0…`
- `program/generated/charts/water-crop-concentration-profiles.svg`  `3f03a13a5679…`
- `program/generated/charts/water-crop-construct-scatter.png`  `672b3332eac6…`
- `program/generated/charts/water-crop-construct-scatter.svg`  `8de47f8888a1…`
- `program/generated/charts/water-denominator-rebase.png`  `5d8212d59495…`
- `program/generated/charts/water-denominator-rebase.svg`  `5735353fa955…`
- `program/generated/charts/water-diagnostic-driver-dominance.png`  `44c6878e6d79…`
- `program/generated/charts/water-diagnostic-driver-dominance.svg`  `fe2413cb94b4…`
- `program/generated/charts/water-diagnostic-sensitivity-membership.png`  `8129f48a5764…`
- `program/generated/charts/water-diagnostic-sensitivity-membership.svg`  `51e4a0fed3d5…`
- `program/generated/charts/water-membership-churn.png`  `195b84d6ca56…`
- `program/generated/charts/water-membership-churn.svg`  `fcbaca0c3c97…`
- `program/generated/charts/water-next-data-object.png`  `761c4fdbd871…`
- `program/generated/charts/water-next-data-object.svg`  `12ae9fdd75c0…`
- `program/generated/charts/water-source-alignment-funnel.png`  `286f74faa351…`
- `program/generated/charts/water-source-alignment-funnel.svg`  `2045bcb33436…`
- `program/generated/charts/water-stress-crop-diversification-thumbnail.json`  `9b6dc402b976…`
- `program/generated/charts/water-stress-crop-diversification-thumbnail.png`  `3b78407e0a8b…`
- `program/generated/charts/water-stress-crop-diversification-thumbnail.svg`  `555a87634003…`
- `program/generated/charts/water-three-gate-validity.png`  `455687902915…`
- `program/generated/charts/water-three-gate-validity.svg`  `baaa497153af…`
- `program/generated/water-construct-diagnostics.csv`  `329ff5d18a1a…`
- `program/generated/water-construct-sensitivity.csv`  `bb36285d6405…`
- `program/generated/water-construct-validation.json`  `f5a171102349…`
- `program/generated/water-stress-crop-adb-panel.csv`  `9c60a3faec99…`
- `program/generated/water-stress-crop-adb-panel.json`  `608ba398496b…`
- `program/generated/water-stress-denominator-deepening.csv`  `019945af2e6c…`
- `program/generated/water-stress-denominator-deepening.json`  `4943b0784fe0…`
- `program/generated/water-stress-denominator-source-audit.json`  `0fce8065cfa9…`
- `program/generated/water-stress-source-readiness-sources.csv`  `7f5e095ccdaa…`
- `program/generated/water-stress-source-readiness.json`  `a56abd17cb42…`
- `program/generated/water-stress-source-variant-rerank.csv`  `7d05dd44bc4f…`
- `program/scripts/audit-water-source-readiness.py`  `ad4c4a46f2ac…`
- `program/scripts/build-construct-validation.py`  `a89ed3d98001…`
- `program/scripts/build-figure-dossier.py`  `a2ec560898af…`
- `program/scripts/build-thumbnail.py`  `879a040a7ab0…`
- `program/scripts/deepen-denominator.py`  `e55c7f3880b4…`
- `program/scripts/process-water-crop.py`  `c04ead7e7f4c…`

### Shared governance

- `shared/CONSTITUTION.md`  `2391ec14922d…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `8e5342b7156c…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `ec0dceabd556…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `ea20ac490253…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T15:19:00.176Z by `scripts/build-review-packet.mjs`.
