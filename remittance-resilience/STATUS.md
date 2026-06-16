# Remittance Resilience — operating status

This is the per-program operating state for `remittance-resilience`.
Repository-level focus and process rules live in `research/STATUS.md`,
`research/factory.md`, and `CLAUDE.md`. This file holds only what is
specific to remittance-resilience.

Last updated: 2026-06-16.

## Current

| Field | Value |
|---|---|
| Maturity label | PP (demoted from SR-under-§18 on 2026-05-07; **ai-first finished for current issue** as of 2026-05-12 under Mode A, reopened for a repair/deepening pass after the 2026-05-29 median-cost audit; promotion to higher labels requires §18.5 owner-led steps) |
| Active stage | L3 parser repair complete; L4 flow-weighting showcase prototype built and verified; formal ladder/review re-close next |
| Active flagship | **Yes**, as of 2026-05-12 (rotated in from PSDQ) |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | Pending (will mint at `/program/remittance-resilience/evidence` once the ladder is complete and gates pass) |

## Current output target

Repair and sharpen the remittance-resilience package so it no longer reads as
a generic "fragility index" result. The current repaired version fixes the RPW
negative-cost normalization defect, regenerates the panel/sensitivity/median
artifacts, adds the public KNOMAD corridor-flow sprint, and ships a verified
showcase prototype at `/showcase/remittance-flow-weighting`. The remaining
program-level work is to formalize flow weighting inside the L3/L4 ladder,
rebuild the review packet, and make every tier carry the repaired claim:
baseline five, common sensitivity core of four, Nepal cap-sensitive, same
top-five set after flow weighting but changed order.

## Last completed

- **2026-06-16 (parser repair + flow-weighting showcase):**
  `scripts/process-remittance.py` and `scripts/deepen-median-cost.py` now
  normalize RPW costs by multiplying only nonnegative fractional values in
  `[0, 1]` by 100; already-percentage negative quotes are not scaled again.
  `scripts/sensitivity.py` now reports both the repaired baseline top-five
  and the common top-five set across rows, plus the maximum top-five entry
  change against baseline. Regenerated artifacts show baseline top five
  `KGZ`, `WSM`, `TON`, `NPL`, `VUT`; common full-suite sensitivity core
  `KGZ`, `TON`, `VUT`, `WSM`; and maximum top-five entry change of 1
  (`PAK` replaces `NPL` when the dependence cap is halved). The median-cost
  deepening keeps the same five-economy set. The KNOMAD-flow sprint matches
  140 of 142 latest-period ADB-DMC-bound RPW corridors; flow weighting keeps
  the same top-five set but changes order to `KGZ`, `NPL`, `VUT`, `WSM`,
  `TON`, with low matched-flow coverage flagged for `KGZ`, `TJK`, `ARM`, and
  `AFG`. Publication surfaces repaired this session include the program
  README/results/sensitivity/coverage files, brief/blog/social/slides,
  working paper, review notes, native chart metadata, and reporting-site data
  summaries. New report surface:
  `/showcase/remittance-flow-weighting`, with desktop and mobile screenshots
  saved under `reporting-site/qa/`. Browser QA confirmed expected title,
  22 scatter points, 13 side-panel bars, 40 sensitivity cells, working mode
  toggles, zero page-level horizontal overflow, chart overflow contained
  inside chart scrollers on mobile, no error overlay, and no browser errors
  beyond existing Vite/React Router development warnings. Verification:
  `npm run build` passed; five gates passed; `check-versions` reported no
  source older than 180 days. This is a verified showcase prototype and
  repair pass, not a maturity promotion or human-final closure.
- **2026-06-16 (L2 hook sprint):**
  `scripts/sprint-flow-weighted-cost.py` joined RPW Q1 2025 corridor prices
  to the World Bank/KNOMAD 2021 bilateral remittance matrix and latest
  available WDI remittance-dependence values. The sprint matched 140 of 142
  ADB-DMC-bound latest-period RPW corridors to KNOMAD flows; the missing
  RPW corridors are New Zealand -> Vanuatu and Oman -> Nepal. The equal-
  weighted top group (`KGZ`, `WSM`, `TON`, `VUT`, `NPL`) remains the same
  after flow weighting (`KGZ`, `NPL`, `VUT`, `WSM`, `TON`), but Nepal and
  Vanuatu move upward enough to require repair before further public
  reframing. Visual QA was performed on
  `generated/charts/remittance-flow-weighting-sprint.png`: it renders,
  labels the equal-weighted and flow-weighted axes, shows the SDG 10.c.1 3%
  guide, and carries the source/vintage caveat. The generated JSON now flags
  low matched-flow coverage below 25% for KGZ, TJK, ARM, and AFG. Decision:
  promote the hook to the L3 repair pass, not to a public claim or maturity
  promotion. Sprint note:
  `l2-flow-weighting-sprint.md`.
- **2026-05-29 (deepening pass, now binding for next work):**
  `scripts/deepen-median-cost.py` recomputed the screen on median corridor
  costs using the cached RPW Q1 2025 workbook and WDI remittance-dependence
  series. The cluster membership {KGZ, TON, WSM, VUT, NPL} survived both
  median-over-quotes and median-of-corridor-medians; Samoa and Tonga swapped
  rank only. The pass also found a real upstream defect in
  `scripts/process-remittance.py`: `raw*100 if raw<=1 else raw` multiplies
  already-percentage negative values again, manufacturing extreme minima such
  as -305% for Pakistan. The defect does not drive the top-five cluster, but
  it corrupts `min_cost_pct` and any quote-pool statistic that uses those
  negatives. The highest-value unresolved keystone is still volume-weighting:
  test whether the cluster survives when each corridor is weighted by actual
  bilateral remittance flow rather than counted equally.
- **2026-05-12 (end of session):** Full Mode A publication-ladder
  build + review-loop close. Six tiers built or polished and one
  governance loop fired. **Tier 1 (working paper):** subtitle and
  opening rewritten (planner-action-led with explicit rank-vs-set
  paragraph), maturity label corrected to PP, abstract reframed,
  fragility-index source-note added explaining the 21-vs-20 panel
  distinction. Five substantive honesty corrections found by Mode A
  self-critique and applied to all live artifacts: (a) Pacific
  small-sample claim from "5–8 corridors per DMC" → actual per-DMC
  counts (KGZ=1, TON/VUT/WSM=2, NPL=8); (b) SDG 10.c.1 reference
  value from incorrect 5% → correct 3%, with multipliers recalibrated
  (3.5×, 2.7×, 2.5×, 3.2×, 2.2×); (c) Pearson ρ between dependence
  and cost axes from "+0.18 across 44 rankable DMCs" → "−0.22 across
  21 DMCs with both axes observed" — sign was flipped; (d) "44
  rankable DMCs" → "21 DMCs with both axes observed", with chart
  visualizing 20 (Fiji excluded as negative-mean outlier); (e)
  per-DMC corridor counts reflected in the per-tier copy across
  brief, blog, social, and slide deck. **Tier 2 (program page):
  ** lives at `/<slug>` via Topic.tsx (article `program:` field).
  **Per-program visualization:**
  `remittance-resilience/scripts/build-fragility-chart.py`
  (≈150 lines) reads `generated/remittance-resilience-adb-panel.csv`
  and emits PNG+SVG; chart shows 20 rankable DMCs in dependence ×
  cost space with five red bubbles for the stable top-5 set, bubble
  size = RPW corridors observed (Pacific entries and KGZ visibly
  small), pre-registered caps and SDG reference as guidelines.
  **Tier 3 (brief, ~600 words):**
  `articles/_brief/remittance-resilience.md`, slug
  `remittance-resilience-brief`. **Tier 4 (blog, ~900 words):
  ** `articles/_blog/remittance-resilience.md`, slug
  `remittance-resilience-blog`. **Tier 5 (social card, 274/280):
  ** `articles/_social/remittance-resilience.md`. **Tier 6
  (slide deck):** Quarto source at
  `articles/_slides/remittance-resilience.md` builds to
  `reporting-site/public/programs/remittance-resilience/remittance-resilience-deck.pptx`
  (226.7 KB) via `scripts/build-slides.mjs remittance-resilience`.
  Co-amendment to `scripts/build-slides.mjs`: generalized chart-script
  lookup to find any `build-*.py` with "chart" or "choropleth" in the
  filename, so each program can ship its own per-program chart-build
  script without modifying the slide-build orchestrator.
  **Tier 7 (evidence packet):** built via
  `scripts/build-review-packet.mjs --program remittance-resilience`
  at `review-packets/remittance-resilience-2026-05-12/` (33 files; 6
  publication-tier + 18 program + 9 shared) + zip (590 KB, emailable).
  **Mode A review loop:** §9.1 + §9.2 critique-pass addendum to
  `review-internal.md` §6–§7 (six self-critique points raised and
  responded to in writing; optional AI second-opinion code review
  honestly recorded as skipped); §9.3 red-team synthesis addendum to
  `review-external.md` §9–§10 against six candidate institutions
  (KNOMAD, WB PSDG, IZA migration cluster, Pacific Community SDD,
  Nepal Rastra Bank, OSCE Academy in Bishkek), each with synthesized
  objection plus written response, §18.4 explicit non-claim applies
  verbatim. **Exit condition:** AI cannot find a further substantive
  self-critique on the listed artifacts. remittance-resilience is
  **ai-first finished for current issue** as of 2026-05-12 under
  Mode A. Five gates pass; `npm run build` succeeds in 3.13s.
  Upgrade-eligible to human-final via §18.5 owner-led steps
  (volume-weighted corridor costs, household receipt concentration,
  real external reviewer contact, owner-designated internal review,
  owner-signed commit).
- **2026-05-12 (earlier in session):** Working-paper audit against
  the goal-skill's ADB/ERDI-style bar + targeted polish pass. Three edits to
  `articles/remittance-corridors-vulnerability-cluster.md`, no claim
  change: (1) frontmatter `maturity: PR` → `maturity: PP` (honesty
  correction — the wip-register has remittance-resilience at PP after
  the 2026-05-07 demotion of all SR-under-§18 programs; the article
  frontmatter had not been updated); (2) `updated_at: 2026-04-26` →
  `2026-05-12`; (3) opening of "# The question" rewritten from
  metaphor-led ("Two indicators travel poorly") to planner-action-led
  ("A finance or development planner deciding where to look first for
  corridor-cost interventions…") with an explicit rank-vs-set
  paragraph at the end of the section that pre-empts the most common
  misreading. Slug-routing verified: `Topic.tsx` looks up articles by
  `a.program === slug` (frontmatter `program: remittance-resilience`
  field), independent of the article's own `slug`; the live
  `/remittance-resilience` URL will resolve. Five gates pass;
  `npm run build` succeeds in 3.51s.

## What exists today (Stage 0–5 starting material)

- `README.md` — overview, top-10 fragility table, three patterns
  (Pacific small islands, Central Asia, Myanmar's 28.16% transfer cost).
- `literature.md` — landscape scan.
- `pre-registration.md` — first testable claim + falsification condition.
- `scoring.md` — §3.3 rubric score.
- `coverage.md` — DMC and source coverage.
- `sensitivity.md` — repaired ±50% suite outputs; baseline top five
  {KGZ, WSM, TON, NPL, VUT}, common full-suite core
  {KGZ, TON, VUT, WSM}, maximum top-five entry change of 1.
- `results.md` — main result.
- `limitations.md` — non-claims (composite triage, not headline; missing
  outbound-cost validation; Russia-route corridor concentration).
- `review-internal.md` — §9.1 + §9.2 AI critique-pass (initial, under
  the old single-screening SR labeling).
- `review-external.md` — §9.3 AI synthesis from candidate-institution
  positions (KNOMAD, World Bank Migration & Remittances, ADBI, IOM).
- `scripts/process-remittance.py` — pulls RPW Q1 2025 + WDI BX.TRF…GD.ZS,
  emits `generated/remittance-resilience-adb-panel.{csv,json}`.
- `.cache/rpw_dataset_2011_2025_q1.xlsx` (49 MB; git-ignored) and
  `.cache/wdi_remittance_pct_gdp.json`.
- `articles/remittance-corridors-vulnerability-cluster.md` — Tier 1
  working paper draft.
- `deep-questions.md` — AI-generated research agenda identifying the
  volume-weighting question as the keystone.
- `scripts/deepen-median-cost.py` and
  `generated/remittance-median-deepening.{json,csv}` — robust-cost deepening
  that keeps the same cluster but identifies the cost-normalization repair.

## Next focused work

Finish the formal L3/L4 re-close before calling remittance done:

1. **Promote the flow-weighting sprint into formal program evidence.**
   Decide whether `scripts/sprint-flow-weighted-cost.py` remains an L2 sprint
   or becomes a named L3 sensitivity module. If it becomes L3, add the
   decision rule and coverage thresholds to `pre-registration.md` or a clearly
   dated addendum.
2. **Rebuild the full review packet.** The showcase and public tiers are
   repaired, but the Mode A packet should be rebuilt after the flow-weighting
   status is settled so the archive reflects the 2026-06-16 evidence.
3. **Run a final contradiction audit.** Search all remittance public surfaces
   for superseded wording: "all five stable in every row", SDG 5% benchmark,
   and "5-8 corridors". Historical audit notes may mention old errors only
   when they are clearly marked as corrected.
4. **Then continue the showcase goal.** Once the remittance packet is no
   longer internally contradictory, continue the 10-20 report queue from
   `research/hook-bank.md` with the next data-first candidate batch.

## Current blockers

- None at AI-first depth for the parser repair and median-cost update.
  The corridor-volume-weighting keystone depends on a public bilateral
  remittance-flow source; treat a failed fetch as a named data wall, not as
  permission to infer weights. Owner-gated upgrades for §18.5 human-final:
  - Real KNOMAD / WB M&R / IOM reviewer contact (not AI synthesis).
  - Owner line-by-line read of the working paper and re-attestation.
  - Owner-designated internal review.

## Handoff prompt

Use this to continue a fresh session focused on remittance-resilience:

```text
Read research/STATUS.md and remittance-resilience/STATUS.md, plus
CLAUDE.md and research/factory.md. remittance-resilience is the active
flagship as of 2026-05-12 (rotated in from PSDQ). Start with the
repair/deepening pass listed in remittance-resilience/STATUS.md: cost-parser
fix, regenerated evidence, then the corridor-volume-weighting keystone if the
public bilateral flow source can be retrieved. State the chosen review mode
before iterating; default is Mode A under §18 ACTIVE.
```
