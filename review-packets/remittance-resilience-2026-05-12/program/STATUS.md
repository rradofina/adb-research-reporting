# Remittance Resilience — operating status

This is the per-program operating state for `remittance-resilience`.
Repository-level focus and process rules live in `research/STATUS.md`,
`research/factory.md`, and `CLAUDE.md`. This file holds only what is
specific to remittance-resilience.

Last updated: 2026-05-12.

## Current

| Field | Value |
|---|---|
| Maturity label | PP (demoted from SR-under-§18 on 2026-05-07; **ai-first finished for current issue** as of 2026-05-12 under Mode A — see Last completed below; promotion to higher labels requires §18.5 owner-led steps) |
| Active stage | Stage 7 — Review loop closed under Mode A (2026-05-12) |
| Active flagship | **Yes**, as of 2026-05-12 (rotated in from PSDQ) |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | Pending (will mint at `/program/remittance-resilience/evidence` once the ladder is complete and gates pass) |

## Current output target

A reviewer-credible remittance-resilience evidence package matching the
PSDQ-grade bar — working paper, program page, brief, blog post, social
card, slide deck, and evidence packet — that a reader can understand,
inspect, and cite at every depth, with the right caveats. The headline
frame is **corridor-concentration risk as a measurement gap**, not a
country ranking: which DMCs depend on remittance flows that travel
through few-and-expensive corridors, where "few-and-expensive" is the
disagreement between official cost statistics and corridor-weighted
exposure.

## Last completed

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
- `sensitivity.md` — ±50% suite outputs; top-5 set {KGZ, NPL, TON, VUT,
  WSM} stable across every perturbation including
  multiplicative→additive aggregation switch.
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

## Next focused work

Build the publication ladder + close the Mode A review loop. In order:

1. **Audit the existing working paper** (`articles/remittance-corridors-vulnerability-cluster.md`) against the goal-skill's ADB/ERDI-style bar. The PSDQ pass found three recurring polish targets — opening register, headline placement, subtitle density. Apply equivalent polish before downstream tiers inherit it.
2. **Per-program visualization.** The argument needs probably 1–2 charts: a corridor-cost distribution (e.g., violin or strip plot by destination DMC, sorted by dependence) and/or a Sankey of origin→destination corridor concentration. Write a Python build script (mirroring PSDQ's `build-choropleth.py`) that reads `generated/remittance-resilience-adb-panel.csv` and emits PNG + SVG. Reused by every downstream tier.
3. **Tier 2 — program page.** Add `reporting-site/public/programs/remittance-resilience/` with synced generated artifacts; the live `/<slug>` route is served by `Topic.tsx` automatically once the article frontmatter has the right slug.
4. **Tier 3 — brief.** `articles/_brief/remittance-resilience.md` (~500 words, single chart).
5. **Tier 4 — blog post.** `articles/_blog/remittance-resilience.md` (~750 words, narrative for dev-econ reader).
6. **Tier 5 — social card.** `articles/_social/remittance-resilience.md` (≤280 chars + alt text).
7. **Tier 6 — slide deck.** `articles/_slides/remittance-resilience.md` (Quarto markdown, 8–15 slides, charts from the same Python script via Quarto code blocks). Built to `.pptx` via `scripts/build-slides.mjs`.
8. **Tier 7 — evidence packet.** Built by `scripts/build-review-packet.mjs` once tiers 1–6 are in.
9. **Mode A review loop.** §9.1 self-review + §9.2 critique-pass + §9.3 AI red-team synthesis (KNOMAD, WB M&R, ADBI, IOM) + optional AI second-opinion code review. Iterate until self-convergence.
10. **End-of-task hygiene each iteration.** Five gates + `npm run build` + viewport-check at 1280 / 375 + per-program STATUS update.

## Current blockers

- None at AI-first depth. Owner-gated upgrades for §18.5 human-final:
  - Real KNOMAD / WB M&R / IOM reviewer contact (not AI synthesis).
  - Owner line-by-line read of the working paper and re-attestation.
  - Owner-designated internal review.

## Handoff prompt

Use this to continue a fresh session focused on remittance-resilience:

```text
Read research/STATUS.md and remittance-resilience/STATUS.md, plus
CLAUDE.md and research/factory.md. remittance-resilience is the active
flagship as of 2026-05-12 (rotated in from PSDQ). Continue the
publication-ladder build listed in remittance-resilience/STATUS.md.
State the chosen review mode before iterating; default is Mode A under
§18 ACTIVE.
```
