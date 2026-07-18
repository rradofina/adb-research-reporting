# Review packet — school-heat-disruption — 2026-07-18

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

- `publication/1-working-paper/school-heat-honest-narrowing.md`  `2764858669d0…`
- `publication/3-brief/school-heat-honest-narrowing.md`  `7755cba1068f…`
- `publication/4-blog/school-heat-honest-narrowing.md`  `b72a96c6e360…`
- `publication/5-social/school-heat-honest-narrowing.md`  `f90599382116…`
- `publication/6-slides/school-heat-honest-narrowing.md`  `ad22e25582bf…`
- `publication/6-slides/school-heat-disruption-deck.pptx`  `c77373956131…`

### Program artifacts

- `program/README.md`  `8ac11f34e714…`
- `program/STATUS.md`  `8515b97c5156…`
- `program/REPRODUCE.md`  `ad0af453c052…`
- `program/literature.md`  `7fe4a8801e30…`
- `program/pre-registration.md`  `e676a2b36153…`
- `program/sensitivity.md`  `45ee4cca092a…`
- `program/sensitivity-runs.json`  `d7a97e6435b3…`
- `program/coverage.md`  `54897de24dd5…`
- `program/results.md`  `2102ad2aeec8…`
- `program/limitations.md`  `0b40e079d7e4…`
- `program/upgrade-gap.md`  `936c43a99732…`
- `program/review-internal.md`  `166fb2f9194c…`
- `program/review-external.md`  `ab620e6c178e…`
- `program/generated/charts/school-driver-dominance.png`  `3cdd78243eee…`
- `program/generated/charts/school-driver-dominance.svg`  `66f2aee558f1…`
- `program/generated/charts/school-enrollment-share-proxy.png`  `4f6a70292e32…`
- `program/generated/charts/school-enrollment-share-proxy.svg`  `394e62c91378…`
- `program/generated/charts/school-hazard-burden-composition.png`  `e8f6ebcbe140…`
- `program/generated/charts/school-hazard-burden-composition.svg`  `05de1218387d…`
- `program/generated/charts/school-heat-disruption-thumbnail.json`  `0e663326f05c…`
- `program/generated/charts/school-heat-disruption-thumbnail.png`  `85fac52abb55…`
- `program/generated/charts/school-heat-disruption-thumbnail.svg`  `1fb6192da1bd…`
- `program/generated/charts/school-heatwave-affected-ranking.png`  `342df05fed8f…`
- `program/generated/charts/school-heatwave-affected-ranking.svg`  `246da8de8065…`
- `program/generated/charts/school-next-data-object.png`  `f7616522b111…`
- `program/generated/charts/school-next-data-object.svg`  `304b319d923f…`
- `program/generated/charts/school-proxy-outcome-scatter.png`  `10130c95de68…`
- `program/generated/charts/school-proxy-outcome-scatter.svg`  `3ebdb14ee7a1…`
- `program/generated/charts/school-sensitivity-run-verdicts.png`  `624577bc7221…`
- `program/generated/charts/school-sensitivity-run-verdicts.svg`  `1a9984c948eb…`
- `program/generated/charts/school-source-alignment-funnel.png`  `40b46e8140d4…`
- `program/generated/charts/school-source-alignment-funnel.svg`  `d9297130ccd6…`
- `program/generated/charts/school-three-gate-validity.png`  `2caaa678616e…`
- `program/generated/charts/school-three-gate-validity.svg`  `a1a837af0895…`
- `program/generated/school-construct-correlations.csv`  `39dc54744d75…`
- `program/generated/school-construct-diagnostics.csv`  `6d55432fe349…`
- `program/generated/school-construct-validation.json`  `8d716c541c9d…`
- `program/generated/school-heat-adb-panel.csv`  `6a1175de1977…`
- `program/generated/school-heat-adb-panel.json`  `b70493fb7926…`
- `program/generated/school-heat-khm-pak-source-readiness.csv`  `efdb7947f43d…`
- `program/generated/school-heat-sensitivity-audit.json`  `af3754f02ce8…`
- `program/generated/school-heat-source-audit.json`  `11eac671a5c6…`
- `program/generated/school-heat-source-readiness-sources.csv`  `1581ef38d274…`
- `program/generated/school-heat-source-readiness.json`  `8263d07701a4…`
- `program/scripts/audit-school-heat-source-readiness.py`  `2d45428329d8…`
- `program/scripts/build-construct-validation.py`  `941326fcde11…`
- `program/scripts/build-figure-dossier.py`  `41c38b17b228…`
- `program/scripts/build-thumbnail.py`  `354a8941d24a…`
- `program/scripts/deepen-sensitivity-audit.py`  `df38679531d6…`
- `program/scripts/process-school-heat.py`  `773c22d9aebb…`

### Shared governance

- `shared/CONSTITUTION.md`  `f88d70f832bb…`
- `shared/CLAUDE.md`  `dd1331fb033c…`
- `shared/references.bib`  `68123a7b8e23…`
- `shared/red-team.md`  `fd096b32dcc1…`
- `shared/versions.json`  `3d1f9d72daeb…`
- `shared/manifest.sha256`  `afdcc374ad9f…`
- `shared/style-guide.md`  `aa146af42a4a…`
- `shared/wip-register.md`  `64d345e2f998…`
- `shared/coverage-matrix.md`  `0f3e6dca6109…`

## Manifest

The full SHA-256 of every file in this packet is at `packet-manifest.sha256`.

— Generated 2026-07-18T16:18:00.959Z by `scripts/build-review-packet.mjs`.
