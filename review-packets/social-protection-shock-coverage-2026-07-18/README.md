# Review packet — social-protection-shock-coverage — 2026-07-18

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

- `publication/1-working-paper/sp-shock-readiness-cluster.md`  `65d93a37ae36…`
- `publication/3-brief/sp-shock-readiness-cluster.md`  `93fd7a267dfd…`
- `publication/4-blog/sp-shock-readiness-cluster.md`  `8123319d9ce7…`
- `publication/5-social/sp-shock-readiness-cluster.md`  `73d7cfaa08d0…`
- `publication/6-slides/sp-shock-readiness-cluster.md`  `bc7f92239e2d…`
- `publication/6-slides/social-protection-shock-coverage-deck.pptx`  `6ea4cd826428…`

### Program artifacts

- `program/README.md`  `6bb42512b02a…`
- `program/STATUS.md`  `651b2132d035…`
- `program/REPRODUCE.md`  `914a5ec0c2be…`
- `program/literature.md`  `c829bc1323dd…`
- `program/pre-registration.md`  `e06a3c5a58db…`
- `program/sensitivity.md`  `b59dfe465a49…`
- `program/sensitivity-runs.json`  `28230511fd42…`
- `program/coverage.md`  `cc6b31a63607…`
- `program/results.md`  `41ddc6418ac7…`
- `program/limitations.md`  `9b0017ec1afa…`
- `program/upgrade-gap.md`  `b8d3f5c8d2b6…`
- `program/review-internal.md`  `f5eadf43ea8d…`
- `program/review-external.md`  `018f639d2908…`
- `program/generated/charts/social-protection-shock-coverage-thumbnail.json`  `429f5c3b093a…`
- `program/generated/charts/social-protection-shock-coverage-thumbnail.png`  `1849c3b11bd9…`
- `program/generated/charts/social-protection-shock-coverage-thumbnail.svg`  `2f6451ea0ca4…`
- `program/generated/charts/sp-covid-response-matrix.png`  `c72ad10bab6b…`
- `program/generated/charts/sp-covid-response-matrix.svg`  `1c89527bb2cf…`
- `program/generated/charts/sp-dropped-leg-ranking.png`  `6c9388c35458…`
- `program/generated/charts/sp-dropped-leg-ranking.svg`  `2247b9b88543…`
- `program/generated/charts/sp-membership-churn.png`  `112c9e2dbd3b…`
- `program/generated/charts/sp-membership-churn.svg`  `d332853824c4…`
- `program/generated/charts/sp-poverty-dominance.png`  `34cb7c30560e…`
- `program/generated/charts/sp-poverty-dominance.svg`  `325bb920d1ba…`
- `program/generated/charts/sp-proxy-vs-response-breadth.png`  `7618b0ddebc4…`
- `program/generated/charts/sp-proxy-vs-response-breadth.svg`  `9fe062c5f709…`
- `program/generated/charts/sp-source-alignment-funnel.png`  `dfababc035dd…`
- `program/generated/charts/sp-source-alignment-funnel.svg`  `08e6fa62250e…`
- `program/generated/charts/sp-three-gate-validity.png`  `3cf876895936…`
- `program/generated/charts/sp-three-gate-validity.svg`  `bc956e74d596…`
- `program/generated/charts/sp-vintage-profile.png`  `abd4ace7fe36…`
- `program/generated/charts/sp-vintage-profile.svg`  `5570d3dc84bc…`
- `program/generated/social-protection-adb-panel.csv`  `04f364cbcc7b…`
- `program/generated/social-protection-adb-panel.json`  `322ede16eb27…`
- `program/generated/social-protection-covid-response-diagnostics.csv`  `fa7720c797d5…`
- `program/generated/social-protection-covid-response-validation.json`  `aba1f2074c95…`
- `program/generated/social-protection-dropped-leg-source-audit.json`  `a24302c0caff…`
- `program/generated/social-protection-dropped-leg.csv`  `151b9eee82f3…`
- `program/generated/social-protection-dropped-leg.json`  `6255d1e86e92…`
- `program/generated/social-protection-social-safety-net-rerank.csv`  `dba2380d337e…`
- `program/generated/social-protection-source-readiness-sources.csv`  `6aaac12dfcad…`
- `program/generated/social-protection-source-readiness.json`  `12fe0666b9ac…`
- `program/scripts/audit-social-protection-source-readiness.py`  `ff787106d373…`
- `program/scripts/build-covid-response-validation.py`  `9205096380d1…`
- `program/scripts/build-figure-dossier.py`  `cb4b6aaf65af…`
- `program/scripts/build-thumbnail.py`  `59e357c13620…`
- `program/scripts/deepen-include-partial.py`  `3ab5d8765bb2…`
- `program/scripts/process-sp.py`  `f2d95f2c9d05…`

### Shared governance

- `shared/CONSTITUTION.md`  `3d159027c3d8…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `4431cb26311a…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `9915030b8517…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `62b5a5d86575…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T14:40:52.201Z by `scripts/build-review-packet.mjs`.
