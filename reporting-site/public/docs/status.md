# Current research status — operating board

**Principle.** This file is the **board, not the file**. Its job is to point
to the active flagship and to define how a session opens, runs, and closes.
Per-program detail — last completed, next focused work, current blockers,
program-specific runbooks — lives in `{program}/STATUS.md` or in the
program's `README.md`. If you find PSDQ-specific narrative here, move it.

Last updated: 2026-06-19.

## Current focus

| Field | Value |
|---|---|
| Active flagship | `public-service-data-quality` (PR; ai-first finished 2026-05-07; BGD source-disagreement L3 module, validation sample, automated coded screen, AI public-source review ledger, 8-row candidate-resolution pass, richer public-source tag scan, 23-row coordinate-repair triage, 40-row public-map-gap triage, and 40-row public-map-gap row-evidence ledger added 2026-06-19; next loop is targeted public-map inspection from the row-evidence ledger) |
| Per-program board | [`public-service-data-quality/STATUS.md`](../public-service-data-quality/STATUS.md) |
| Operating mode | §18 ACTIVE (AI-First) |
| Default review mode | Mode A (AI-only); see `research/factory.md` |
| Previous flagship | `remittance-resilience` (PP, L3 flow-weighting repair closed under Mode A in commit `225d4d2`; available for §18.5 owner-led human-final upgrade) |

The active flagship is the only program that may be advanced this session.
Rotation reason recorded in the operational notes below. Programs in the
queue are listed in `research/wip-register.md` and `CONSTITUTION.md` §15.
Do not silently switch programs; rotation requires recording the reason
here before switching.

## Next-up queue

Ordering by Mode-A readiness (cheapest path to "ai-first finished for
current issue" under the publication ladder + review loop). The owner
overrides priority by editing this list.

1. **`public-service-data-quality`** — *current active flagship; PR and
   ai-first finished for current issue 2026-05-07; BGD source-disagreement
   L3 module, validation-sample design, automated coded screen, AI
   public-source review ledger, candidate-resolution pass, public-source tag
   scan, coordinate-repair triage, public-map-gap triage, and public-map-gap
   row-evidence ledger added 2026-06-19*. Current work is targeted public-map
   inspection from the row-evidence ledger, without changing the maturity
   label.
2. **`remittance-resilience`** — L3 flow-weighting repair closed under Mode A
   in commit `225d4d2`. Repaired baseline top five are KGZ, WSM, TON, NPL,
   and VUT; the public KNOMAD flow-weighting L3 module keeps the same
   five-economy set but changes order to KGZ, NPL, VUT, WSM, TON.
   Human-final remains §18.5 owner-led.
3. **`access-services`** — 8-DMC climate-adjusted access pilot done;
   top-4 narrowing {BGD, KHM, LAO, PAK} stable. Travel-time isochrones
   are §18.5 owner-gated, so AI-doable depth is bounded — clean Mode A
   finish.
4. **`migration-displacement-signals`** — top-5 emigrant-stock cluster
   {IND, CHN, BGD, AFG, PHL} stable across alternative definitions;
   article exists at
   `articles/emigrant-stock-corridor-concentration.md`; same gap as
   remittance-resilience.
5. **`climate-health-workdays`** — top-3 set {AFG, IND, BGD} stable; PM
   2.5-cap sensitivity flagged top-5 → top-3 honest narrowing.
6. **`disaster-recovery-lag`** — metric-falsification deepening shows the
   original {CHN, IND} top-two is not robust: it holds for affected and
   damage, but changes under events/year, deaths, and events per million.
   It still lacks an actual recovery-lag metric.
7. **`grid-reliability-heat`** — top-5 single-fuel set {BTN, BRN, MNG,
   NPL, TJK} stable.
8. **`port-hinterland-friction`** — top-5 trade-volume cluster {CHN,
   IND, IDN, THA, VNM} stable.
9. **`social-protection-shock-coverage`** — top-5 {BGD, LAO, MMR, PAK,
   PHL} stable.
10. **`water-stress-crop-diversification`** — top-4 narrowing {AFG, AZE,
   PAK, TKM}; UZB perturbation-sensitive — narrower headline.
11. **`school-heat-disruption`** — honest narrowing to top-1 (KHM only);
    top-5 fails ±50% gate. Smallest-claim flagship candidate.
12. **`food-price-climate-transmission`** — sensitivity-gate failure on
    composite; index needs reformulation before ladder build.
13. **`flood-market-access`** — top-4 {AFG, CHN, IDN, IND} stable; GLOFAS
    modeled-extent is §18.5 owner-gated.
14. **`air-monitoring`** — ground-station coverage vs satellite AOD;
    pipeline ready.
15. **`invisible-urbanization`** — settlement growth vs admin urban
    boundaries; pipeline ready.
16. **`coastal-informal-risk`** — informal coastal settlements vs
    storm-surge exposure; pipeline ready.
17. **`digital-performance`** — broadband coverage vs official
    connectivity claims; folder mostly empty (Stage 1 framing needed).
18. **`mpi-nighttime-lights`** — Program 0, co-authored with Arturo; H
    stage; owner-led not AI-led (different review path).

Promotions and demotions are recorded in `research/wip-register.md`. The
queue position above is a planning order, not a maturity label.

## Stage labels

Generic across programs. Use these in chat updates and handoffs.

| Stage | Meaning | Output |
|---|---|---|
| 0. Idea queue | New possible topic, not yet judged | Short idea note |
| 1. Research framing | Question, contribution, audience, literature map | `literature.md`, problem statement |
| 2. Source discovery | Public datasets, licenses, API paths, coverage | source plan, cache plan |
| 3. Pipeline implementation | Fetch/process scripts and generated artifacts | `scripts/`, `.cache/`, `generated/` |
| 4. Results and sensitivity | Main result plus robustness checks | `results.md`, `sensitivity.md` |
| 5. Critique and limits | Red-team review, non-claims, failure modes | `limitations.md`, reviews |
| 6. Publication surface | Article, charts, home hooks, evidence page | `articles/`, `reporting-site/` |
| 7. Review loop and handoff | Review mode chosen + iterated to exit condition | `review-internal.md`, `review-external.md`, updated `{program}/STATUS.md` |
| 8. Blocked or owner-only | Needs owner account, reviewer, or non-AI attestation | explicit blocker in the per-program file |

## Where status, register, backlog, process live

| File | Role |
|---|---|
| `research/STATUS.md` (this file) | The board: active flagship + session protocol |
| `{program}/STATUS.md` | Per-program last-completed / next-work / blockers |
| `research/wip-register.md` | Maturity register (which program at which label) |
| `CONSTITUTION.md` §15 | Program register of record |
| `research/TODO-NEXT-SESSION.md` | Backlog of useful future work (cross-program) |
| `research/hook-bank.md` | Data-first shortlist for non-generic topic hooks |
| `research/factory.md` | Process manual: program loop, publication ladder, review loop |
| `CLAUDE.md` | Operating rules for AI assistants |

If these files disagree, fix the per-program file first for immediate
focus, then propagate to the register or this board only if the underlying
status truly changed.

## Session protocol

**Principle.** A session is a unit of accountable work, not a stream of
edits. It opens by stating what is being done, runs by doing it, and closes
by leaving the board in a state the next session can read.

**At session open:**
1. Read this file, the active flagship's `{program}/STATUS.md`, `CLAUDE.md`,
   and `research/factory.md`.
2. State the active flagship, current stage, and next output in plain language.
3. Continue the next focused work in the per-program board, unless the
   owner redirects.

**During session:**
1. Name the kind of work being done (framing, source, pipeline, results,
   critique, publication, review-loop, handoff).
2. Do not silently switch programs. If a switch is justified, record the
   reason in this file before making it.
3. Run end-of-task hygiene per `CLAUDE.md` after substantive changes
   (gates, build if site changed, browser-check if public surface changed,
   per-program STATUS update).

**At session close:**
1. Update the active flagship's `{program}/STATUS.md`: last completed, next
   focused work, blockers, verification actually run.
2. Update this file only if the active flagship, operating mode, or default
   review mode changed.
3. Update `research/wip-register.md` only if a maturity label changed.

## Current operational notes

- **2026-06-19 (PSDQ public-map-gap row evidence):** Added
  `public-service-data-quality/scripts/build-bgd-facility-public-map-gap-row-evidence.py`,
  generated `psdq-bgd-facility-validation-public-map-gap-evidence.csv` and
  `psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`, and
  wrote
  `public-service-data-quality/facility-validation-public-map-gap-evidence.md`.
  The no-network pass reads the public-map-gap triage CSV/summary and gives all
  40 open rows a DGHS source note, public profile URL, OSM coordinate-inspection
  URL, OSM feature or absence note, and keep-open reviewer action. It covers
  all 30 priority-1 high-exposure rows. Evidence tiers: 4 source-repair-first
  rows, 3 possible match or buffer-review rows, 15 row-level public-map
  absence-review rows, and 18 upazila-level public-map observability rows. All
  40 rows remain open. This is row-level public-source evidence, not human
  validation, a maturity promotion, or a human-final upgrade. Verification
  passed: row-evidence script rerun, program-script `py_compile`, production
  site build, six deterministic gates, `git diff --check`, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. The mobile row-evidence chart now renders as a
  compact upazila list instead of a cropped wide SVG. Screenshots:
  `reporting-site/qa/showcase-psdq-row-evidence-desktop.png`,
  `reporting-site/qa/showcase-psdq-row-evidence-mobile.png`, and
  `reporting-site/qa/showcase-psdq-row-evidence-mobile-chart.png`. Next PSDQ
  loop is targeted public-map inspection from the row-evidence ledger.
- **2026-06-19 (PSDQ public-map-gap triage):** Added
  `public-service-data-quality/scripts/triage-bgd-facility-public-map-gaps.py`,
  generated `psdq-bgd-facility-validation-public-map-gap.csv` and
  `psdq-bgd-facility-validation-public-map-gap-summary.json`, and wrote
  `public-service-data-quality/facility-validation-public-map-gap.md`. The
  no-network triage reads the AI review ledger, coded-screen CSV,
  coordinate-repair CSV, exposure-ranked table, OSM upazila table, cached
  all-Bangladesh OSM health features, and cached DGHS public DataTables rows.
  It keeps all 40 public-map-gap rows open: 30 priority-1 high-exposure rows,
  18 zero-OSM expected-upazila rows, 2 reused valid-coordinate rows, 2 far
  same-upazila name-signal rows, 1 same-upazila name signal outside 500
  meters, 2 buffer-sensitive 500m-to-1km rows, 3
  OSM-present-not-at-facility rows, and 12
  no-same-upazila-OSM-signal-within-3km rows. The showcase route
  `/showcase/psdq-source-disagreement` now fetches the public-map-gap summary
  JSON, shows the public-map-gap panel and upazila queue, and links the new
  note/downloads. README, REPRODUCE, hook bank, quality audit,
  sync/review-packet inclusion, source-disagreement L3 note, showcase
  registry, and per-program status were updated. This is public-source triage,
  not human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script rerun, new script `py_compile`,
  program-script `py_compile`, production site build, six deterministic gates,
  and agent-browser desktop/mobile QA at 1365px and 375px with no page-level
  horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-map-gap-desktop.png` and
  `reporting-site/qa/showcase-psdq-public-map-gap-mobile.png`. Next PSDQ loop
  is row-level public DGHS/OSM/source evidence for the highest-exposure open
  public-map-gap rows.
- **2026-06-19 (PSDQ coordinate-repair triage):** Added
  `public-service-data-quality/scripts/triage-bgd-facility-coordinate-repairs.py`,
  generated `psdq-bgd-facility-validation-coordinate-repair.csv` and
  `psdq-bgd-facility-validation-coordinate-repair-summary.json`, and wrote
  `public-service-data-quality/facility-validation-coordinate-repair.md`. The
  no-network triage reads the AI review ledger, coded-screen CSV, public
  geoBoundaries ADM3, cached all-Bangladesh OSM health features, and cached
  DGHS public DataTables rows. It keeps all 23 coordinate-repair rows open:
  7 missing coordinates, 2 reused sampled coordinates, 6 other-ADM3
  coordinates near an OSM health feature, 5 other-ADM3 coordinates without a
  nearby OSM health feature, and 3 outside the public ADM3 polygons used here.
  Sixteen usable suspect coordinates fall outside the expected sampled upazila;
  4 are at least 50 kilometers away and the largest measured distance is 351.4
  kilometers. The showcase route `/showcase/psdq-source-disagreement` now
  fetches the coordinate-repair summary JSON, shows a coordinate-repair panel
  and distance ledger, and links the new note/downloads. README, REPRODUCE,
  hook bank, quality audit, sync/review-packet inclusion, source-disagreement
  L3 note, showcase registry, and per-program status were updated. This is
  source-repair triage, not human validation, a maturity promotion, or a
  human-final upgrade. Verification passed: new script `py_compile`,
  production site build, six deterministic gates, and agent-browser
  desktop/mobile QA at 1365px and 375px with no page-level horizontal overflow
  and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-coordinate-repair-desktop.png` and
  `reporting-site/qa/showcase-psdq-coordinate-repair-mobile.png`. This queue
  is now superseded by the public-map-gap triage in the operational note above.
- **2026-06-19 (PSDQ candidate public-source tag scan):** Added
  `public-service-data-quality/scripts/check-bgd-facility-candidate-public-sources.py`,
  generated `psdq-bgd-facility-validation-candidate-public-source-check.csv`
  and
  `psdq-bgd-facility-validation-candidate-public-source-check-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-candidate-public-source-check.md`.
  The scan reads the candidate-resolution CSV, OSM-candidates CSV, pinned
  all-Bangladesh OSM tags, and cached DGHS public DataTables rows. It keeps
  all 8 candidate rows open while separating them into 2 strong same-site OSM
  tag-support rows, 2 same-site type/label conflicts, 2 name-support rows with
  coordinate/function conflicts, and 2 nearby-feature rows without registry-name
  support. The showcase route `/showcase/psdq-source-disagreement` now fetches
  the source-check summary JSON, shows a public-source tag-support panel/chart,
  and links the new note and downloads. README, REPRODUCE, hook bank, quality
  audit, sync/review-packet inclusion, source-disagreement L3 note, and
  per-program status were updated. This is AI public-source evidence scanning,
  not human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, and agent-browser desktop/mobile QA at
  1365px and 375px with no page-level horizontal overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-public-source-check-desktop.png` and
  `reporting-site/qa/showcase-psdq-public-source-check-mobile.png`. This
  source-check queue is now followed by the coordinate-repair and
  public-map-gap triage notes above.
- **2026-06-19 (PSDQ candidate-resolution pass):** Added
  `public-service-data-quality/scripts/resolve-bgd-facility-candidate-rows.py`,
  generated `psdq-bgd-facility-validation-candidate-resolution.csv` and
  `psdq-bgd-facility-validation-candidate-resolution-summary.json`, and wrote
  `public-service-data-quality/facility-validation-candidate-resolution.md`.
  The pass reads the AI review ledger, OSM-candidates CSV, and AI review
  summary, keeps all 8 candidate-resolution rows open, and separates them into
  1 probable alias/campus lane, 2 same-site classification-conflict lanes, 2
  possible aliases, 1 local-script name gap, 1 ambiguous nearby candidate, and
  1 weak nearby OSM signal. The showcase route
  `/showcase/psdq-source-disagreement` now fetches the candidate-resolution
  summary JSON, shows the lane grid/chart, and links the new note and
  downloads. README, REPRODUCE, hook bank, quality audit,
  sync/review-packet inclusion, source-disagreement L3 note, and per-program
  status were updated. This is AI public-source candidate resolution, not
  human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, review-packet rebuild, and agent-browser
  desktop/mobile QA at 1365px and 375px with no page-level horizontal overflow
  and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-candidate-resolution-desktop.png` and
  `reporting-site/qa/showcase-psdq-candidate-resolution-mobile.png`. Rebuilt
  `review-packets/public-service-data-quality-2026-06-18/` plus zip. This
  candidate-resolution queue is now superseded by the richer public-source tag
  scan in the operational note above.
- **2026-06-19 (PSDQ AI public-source review ledger):** Added
  `public-service-data-quality/scripts/review-bgd-facility-validation-flags.py`,
  generated `psdq-bgd-facility-validation-ai-review.csv` and
  `psdq-bgd-facility-validation-ai-review-summary.json`, and wrote
  `public-service-data-quality/facility-validation-ai-review.md`. The ledger
  keeps all 71 flagged sampled DGHS rows open while separating the queue into
  40 public-map-gap checks, 23 coordinate-source repairs, 6 name/type
  resolution rows, and 2 nearby-OSM-without-registry-match rows. The showcase
  route `/showcase/psdq-source-disagreement` now fetches the AI review summary
  JSON, shows an AI public-source review workstream panel/chart, and links the
  new note and downloads. README, REPRODUCE, hook bank, quality audit,
  sync/review-packet inclusion, and per-program status were updated. Rebuilt
  `review-packets/public-service-data-quality-2026-06-18/` plus zip.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, and agent-browser desktop/mobile QA
  with no page-level horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-ai-review-desktop.png` and
  `reporting-site/qa/showcase-psdq-ai-review-mobile.png`. This is AI
  public-source row review, not human validation, a maturity promotion, or a
  human-final upgrade. This queue is now superseded by the candidate-resolution
  pass; next PSDQ loop is public-source confirmation inside those lanes.
- **2026-06-19 (PSDQ automated facility-validation coded screen):** Added
  `public-service-data-quality/scripts/code-bgd-facility-validation-sample.py`,
  generated the coded-screen CSV, OSM-candidates CSV, and coded-summary JSON,
  and wrote `public-service-data-quality/facility-validation-coded-screen.md`.
  The automated screen uses the cached all-Bangladesh OSM health-feature pull
  and geoBoundaries ADM3 to classify the 76 sampled DGHS rows: 40 missing
  public-map points, 23 registry coordinate issues, 5 confirmed same-facility
  matches, 3 probable aliases, 3 classification mismatches, and 2 OSM-only
  candidates. The showcase route `/showcase/psdq-source-disagreement` now
  fetches the coded-summary JSON, shows a grouped coded-screen chart, and
  links the coded-screen downloads. README, REPRODUCE, hook bank, quality
  audit, sync/review-packet inclusion, and per-program status were updated.
  Browser QA passed at 1365px desktop and 375px mobile with no page-level
  horizontal overflow or page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-coded-screen-desktop.png` and
  `reporting-site/qa/showcase-psdq-coded-screen-mobile.png`. This is
  automated public-source triage, not manual validation, a maturity promotion,
  or human-final upgrade. The follow-on AI public-source review ledger was
  completed in the next operational note.
- **2026-06-19 (PSDQ facility-validation sample design):** Added
  `public-service-data-quality/scripts/design-bgd-facility-validation-sample.py`,
  generated the Bangladesh validation-sample JSON, sampled-upazila CSV,
  sampled-facility CSV, and blank coding sheet, and wrote
  `public-service-data-quality/facility-validation-sample.md`. The design
  covers 20 upazilas and 76 DGHS facility rows, with 69 coordinate-ready rows.
  The showcase route `/showcase/psdq-source-disagreement` now fetches the
  sample JSON, shows a validation-sample panel, and links the blank coding
  sheet. README, REPRODUCE, hook bank, quality audit, sync/review-packet
  inclusion, and per-program status were updated. Verification passed:
  validation-sample script and `py_compile`, `npm run build`, six gates, and
  agent-browser desktop/mobile QA with no page-level horizontal overflow or
  page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-validation-sample-desktop.png` and
  `reporting-site/qa/showcase-psdq-validation-sample-mobile.png`. This is a
  sample design, not validation outcomes, a maturity promotion, or human-final
  upgrade. The follow-on automated coded screen was completed in the next
  operational note.
- **2026-06-19 (PSDQ source-disagreement L3 module):** Added
  `public-service-data-quality/scripts/build-bgd-source-disagreement-strata.py`,
  generated `psdq-bgd-source-disagreement-strata.{json,csv}`, and wrote
  `public-service-data-quality/source-disagreement-l3-module.md`. The
  showcase route `/showcase/psdq-source-disagreement` now reads the L3 strata
  JSON, shows ratio buckets and validation residues before the interactive
  workbench, and links the L3 note plus strata downloads. Registry copy,
  hook bank, sync/review-packet inclusion, README, REPRODUCE, and
  per-program status were updated. Rebuilt
  `review-packets/public-service-data-quality-2026-06-18/` plus zip
  (UTC-dated by script). Verification passed: strata script, `npm run build`,
  six gates, and agent-browser desktop/mobile QA with no page-level horizontal
  overflow or page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-l3-desktop.png` and
  `reporting-site/qa/showcase-psdq-l3-mobile.png`. This is an L3 evidence
  module for report #4, not a maturity promotion or human-final upgrade. The
  follow-on validation-sample design was completed in the next operational
  note.
- **2026-06-19 (rotation to PSDQ source-disagreement deepening):** After
  commit `225d4d2` closed the remittance L3 flow-weighting repair, the active
  flagship rotated to `public-service-data-quality` because
  `research/showcase-quality-audit.md` now lists PSDQ source disagreement as
  the next L3 candidate. The work is a focused evidence/public-surface
  deepening of the existing PR program, not a maturity promotion.
- **2026-06-17 (remittance flow-weighting L3 re-close):** Current active
  flagship repair was formalized instead of leaving the showcase report as an
  L2 sprint. Added `remittance-resilience/flow-weighting-l3-module.md` and
  `pre-registration.md` §12 with a 90% corridor-match gate, interpretation
  rule, non-claims, and no maturity promotion. Updated the flow-weighting
  script/generated JSON to `goal_level: L3 sensitivity module`, recording the
  repaired program baseline order (`KGZ`, `WSM`, `TON`, `NPL`, `VUT`), the
  matched-corridor quote order (`KGZ`, `WSM`, `TON`, `VUT`, `NPL`), and the
  flow-weighted order (`KGZ`, `NPL`, `VUT`, `WSM`, `TON`) after matching
  140/142 latest-period RPW corridors to public KNOMAD bilateral-flow
  estimates. Updated results, sensitivity, coverage, limitations, review
  addenda, article, showcase registry, and route copy; rebuilt
  `review-packets/remittance-resilience-2026-06-18/` plus zip. This is an L3
  repair/governance improvement for report #5, not publication-ready or
  human-final status. Closeout verification completed 2026-06-19: production
  site build passed, six gates passed, targeted post-sync contradiction search
  found only historical correction notes, and Chrome/CDP QA on
  `/showcase/remittance-flow-weighting` passed at 1365px and 375px with no
  page-level horizontal overflow. Screenshots:
  `reporting-site/qa/showcase-remittance-l3-desktop.png` and
  `reporting-site/qa/showcase-remittance-l3-mobile.png`.
- **2026-06-17 (showcase readiness ladder):** Added explicit report-readiness
  metadata for all 20 showcase reports in
  `reporting-site/src/data/showcaseReports.ts`: L2 prototype, L3 candidate,
  evidence audit, and owner-gated. The homepage now separates
  screenshot-checked routes from the five L3 candidates, adds one stage chip
  per report card, and shows the next upgrade alongside the visual,
  operational use, falsifier, evidence path, and source stack. `/showcase`
  and dynamic audit route queues now display both surface status and readiness
  stage. New portfolio audit artifact:
  `research/showcase-quality-audit.md`, with stage definitions, current
  distribution, report-by-report publication gaps, and the next deepening
  order. Browser QA saved `home-readiness-desktop.png`,
  `home-readiness-mobile.png`, `showcase-queue-readiness-desktop.png`,
  `showcase-queue-readiness-mobile.png`, and
  `showcase-20-readiness-mobile.png`; checks confirmed 20 home cards, 120
  home fact rows, 20 stage chips, 20 queue rows, readiness labels visible,
  expected audit stats on report #20, and zero page-level horizontal overflow
  at desktop and mobile widths. This is a readiness-governance improvement,
  not a maturity promotion. Follow-up implementation audit found that the
  readiness ladder was global on the homepage and queue, and complete on
  dynamic audit pages 9-20, but not yet visible inside the older static report
  pages 1-8. Added `ShowcaseQualityPanel` and wired it into all eight static
  routes so every report surface now shows current QA stage, operational use,
  falsifier, publication gap, next upgrade, evidence path, and source stack.
  Focused mobile browser QA on `/showcase/remittance-flow-weighting` confirmed
  the shared panel, next-upgrade text, and zero horizontal overflow; build and
  source audit cover the remaining static routes. Screenshot saved:
  `showcase-remittance-readiness-panel-mobile.png`.
- **2026-06-17 (showcase depth-standard pass):** Added bench-level
  `operationalUse`, `falsifier`, and `limitation` metadata for all 20
  showcase reports in `reporting-site/src/data/showcaseReports.ts`. The
  homepage now shows five report-depth rows per card: visual, operational
  use, falsifier, evidence path, and source stack. The dynamic artifact-audit
  route adds operational use and falsifier readouts and carries the limitation
  into the caveat list. Focused browser QA saved
  `home-depth-desktop.png`, `home-depth-mobile.png`, and
  `showcase-20-school-depth-mobile.png`; checks confirmed 20 cards, 100 home
  fact rows, expected audit stats, and zero horizontal overflow at 1440px and
  375px. `npm run build` passed, and the six gates
  (`check-citations`, `check-composite-headline`, `check-wip`,
  `check-dmc-framing`, `check-banned-words`, `check-versions`) passed. This
  improves report-depth coverage but does not close the full showcase goal:
  selected reports still need L3 evidence strengthening and more bespoke
  narrative/visual polishing before publication-ready status.
- **2026-06-17 (20-report showcase batch completed):** Owner directed the
  showcase loop not to stop at reports 9-12, so the report bench was expanded
  to 20 public-data surfaces. `reporting-site/src/data/showcaseReports.ts`
  now registers all 20 reports; reports 9-20 use a new artifact-driven
  route, `reporting-site/src/pages/ShowcaseEvidenceAudit.tsx`, mounted at
  `/showcase/:reportSlug`. The new report set covers grid generation
  concentration, migration denominator switching, MPI/night-light blind
  spots, coastal population-denominator effects, flood index decomposition,
  climate-health cap saturation, food-price coverage traps, social-protection
  dropped legs, water-stress denominator artifacts, invisible-urbanization
  tautology, port inert parameters, and school-heat sensitivity auditing.
  Each new route fetches only its committed public JSON artifact from
  `reporting-site/public/programs/.../generated/` and renders an audit-specific
  visual type: rank bridge, blind/visible stack, coverage funnel, sensitivity
  lane, parameter wall, tautology lane, or component card. Homepage and
  `/showcase` copy now read from the shared registry and present the full
  20-report queue. QA saved desktop and mobile screenshots for home plus all
  new report routes under `reporting-site/qa/` using the `*-20.png` suffix.
  CDP checks confirmed 20 home report cards; for every route 9-20, 3 hero
  stats, expected visual rows, 20 queue rows, no JSON load errors, and no
  page-level horizontal overflow at desktop. A mobile queue auto-placement
  overflow was caught and fixed; the mobile rerun confirmed width `375/375`
  and overflow count 0 for home and all report routes 9-20. `npm run build`
  passed after the fix. These 20 surfaces are still showcase/evidence-audit
  outputs, not maturity-label promotions or publication-ready claims. Next
  loop should critique which 2-3 reports deserve L3 strengthening first,
  rather than adding a 21st surface by default.
- **2026-06-17 (front-page report bench + disaster metric-falsification
  showcase):** Homepage refactored from the older topic-thumbnail gallery
  into a report-first ADB/ERDI showcase bench. New shared report registry
  `reporting-site/src/data/showcaseReports.ts` drives both `/` and the
  `/showcase` queue so the 10-20 report goal does not drift across pages.
  The first viewport now shows the active report queue and target state; the
  older 18-program hero gallery remains below as the evidence archive rather
  than the lead surface. Eighth showcase prototype added and verified at
  `/showcase/disaster-metric-falsification`, reading
  `disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.{json,csv}`.
  Generated evidence shows 1,767 EM-DAT rows in the 2000-2025 DMC filter; the
  pre-registered top-two kill condition fires for 3 of 5 metrics. Original
  CHN+IND holds for affected and damage, but changes to CHN+IDN for
  events/year, IDN+MMR for deaths, and TUV+MHL for events per million. The
  report now uses a mobile-native ranked bar list so narrow viewports do not
  crop chart values. Browser QA saved final home screenshots
  `home-report-refactor-desktop-final.png` and
  `home-report-refactor-mobile-final.png`, plus disaster screenshots
  `showcase-disaster-desktop-verified.png`,
  `showcase-disaster-mobile-verified.png`, and
  `showcase-disaster-mobile-chart-final.png` under `reporting-site/qa/`.
  Checks confirmed 8 report cards, 18 program cards, expected disaster hero
  stats `3/5` and `1,767`, five mobile metric bars, no page-level horizontal
  overflow at 375px, and no browser errors beyond known Vite/React Router
  development warnings. `npm run build`, the five gates, and
  `check-versions` passed. This counts as the eighth verified showcase
  prototype and a publication-surface refactor, not a maturity promotion. The
  next-loop guidance in this note is superseded by the 20-report batch note
  above; current next work is critique and L3 strengthening before adding more
  surfaces.
- **2026-06-16 (access map-completeness showcase prototype):** Seventh
  ADB/ERDI showcase report prototype added at
  `/showcase/access-map-completeness`, reading
  `access-services/generated/access-osm-completeness-deepening.json`,
  `access-services/generated/access-osm-completeness-deepening-phl.csv`, and
  `access-services/generated/access-services-adb-panel.json`. The
  access-services deepening script was rerun on 2026-06-16 and confirms the
  identity check that PSDQ's ARMM population divided by OSM health points
  reproduces the access panel's ARMM people-per-facility value exactly. For
  the Philippines, 16 of 17 ADM1 regions change rank once the denominator
  switches from OSM health points to the official clinical registry; ARMM
  moves from 68,678 people per OSM facility to 4,427 people per registry
  facility, while NCR becomes the highest registry-denominator load. The
  Philippine rank correlation between OSM capture and OSM people-per-facility
  is -0.8105; the log-log R2 is 0.5372. Bangladesh shows the same sign more
  weakly in the available 8-division check. The showcase surface uses a
  desktop rank-flip chart, a completeness scatter with fitted log-log guide,
  a correction-wall chart for the 8-economy cluster, and a mobile-specific
  rank-shift summary after screenshot QA showed the full slope chart cropped
  too much on a narrow viewport. Browser QA saved desktop/mobile first-view
  and evidence-view screenshots under `reporting-site/qa/`; checks confirmed
  expected title, `16/17` and `-0.81` hero stats, 17 rank lines, 34 rank dots,
  17 scatter points, one fitted line, 8 correction-wall bars, 2 corrected
  dots, active mode toggles, no page-level horizontal overflow, and no fresh
  browser errors beyond existing Vite/React Router development warnings.
  `npm run build`, the five gates, and `check-versions` passed before status
  handoff. This counts as the seventh verified showcase prototype, not a
  maturity promotion. The next `access-services` loop is official-registry
  expansion for PAK/KHM/LAO/NPL/LKA/TLS and a public travel-time/friction
  denominator before any access-ranking claim.
- **2026-06-16 (air-monitoring observability showcase prototype):** Sixth
  ADB/ERDI showcase report prototype added at
  `/showcase/air-monitoring-observability`, reading
  `air-monitoring/generated/air-monitoring-concentration-deepening.json` and
  `air-monitoring/generated/air-monitoring-adb-panel.json`. The deepening
  script now fetches/caches public World Bank WDI GDP per capita and replaces
  the earlier false "network blocked" wall with a descriptive GDP-adjusted
  monitor-density check. Current generated evidence shows 13 ADB-region
  economies above the WHO PM2.5 guideline with no visible public PM2.5 monitor
  in the OpenAQ panel; 83.5% of that zero-monitor population is in Papua New
  Guinea and Timor-Leste. The GDP partial frame covers 33 monitored economies,
  with Azerbaijan, Indonesia, Sri Lanka, Myanmar, and Bangladesh showing the
  largest positive monitor-density residuals relative to GDP per capita.
  Browser QA saved desktop and mobile first-view/evidence-view screenshots
  under `reporting-site/qa/`; checks confirmed the expected title, 13
  zero-monitor bars, 33 residual points, 46 exposure-panel points, active mode
  toggles, one fitted GDP line, no browser errors, no page-level horizontal
  overflow, and mobile SVG sizing repaired after visual inspection. `npm run build`,
  the five gates, and `check-versions` passed. This counts as the
  sixth verified showcase prototype, not a maturity promotion. The next
  `air-monitoring` loop should move from national observability screening to
  station catchments with gridded population/PM2.5 and regulatory-inventory
  validation before any stronger monitoring-gap claim.
- **2026-06-16 (remittance flow-weighting showcase prototype):** Fifth
  ADB/ERDI showcase report prototype added at
  `/showcase/remittance-flow-weighting`, reading
  `remittance-resilience/generated/remittance-flow-weighting-sprint.{json,csv}`,
  `remittance-resilience/generated/remittance-median-deepening.{json,csv}`,
  and `remittance-resilience/sensitivity-runs.json`. The remittance repair
  pass fixed the RPW cost-normalization defect, regenerated the main panel,
  sensitivity runs, median-cost deepening, fragility chart, thumbnail, and
  synced site evidence. The repaired baseline top five are `KGZ`, `WSM`,
  `TON`, `NPL`, `VUT`; the common full-suite sensitivity core is `KGZ`,
  `TON`, `VUT`, `WSM`; the maximum top-five entry change is 1 because `PAK`
  replaces `NPL` when the dependence cap is halved. The flow-weighting sprint
  matches 140 of 142 latest-period ADB-DMC-bound RPW corridors to public
  World Bank/KNOMAD 2021 bilateral-flow estimates; flow weighting keeps the
  same five-economy set but changes order to `KGZ`, `NPL`, `VUT`, `WSM`,
  `TON`, with low matched-flow coverage flagged for `KGZ`, `TJK`, `ARM`, and
  `AFG`. Browser QA saved desktop/mobile first-view and evidence-view
  screenshots under `reporting-site/qa/`; checks confirmed the expected
  title, 22 scatter points, 13 side-panel bars, 40 sensitivity cells, working
  mode toggles, no error overlay, no page-level horizontal overflow, mobile
  chart overflow contained inside chart scrollers, and no browser errors
  beyond existing Vite/React Router development warnings. `npm run build`,
  the five gates, and `check-versions` passed. This counts as the fifth
  verified showcase prototype, not a maturity promotion. The active
  remittance program still needs a formal flow-weighting L3 decision and
  rebuilt review packet before it can be re-closed as finished for the
  current issue.
- **2026-06-16 (PSDQ showcase visual uplift):** Fourth ADB/ERDI showcase
  prototype added at `/showcase/psdq-source-disagreement`, reading committed
  PSDQ artifacts
  `public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement.{csv,json}`
  and `public-service-data-quality-summary.json`. The first viewport frames
  the non-generic question "When the Map and Registry Disagree" and shows DGHS
  clinical-registry counts versus OSM health features for the top exposure
  rows. The interactive evidence view is a registry-vs-OSM disagreement
  workbench: 16 ranked upazila rows, an OSM-visible registry-share strip,
  DGHS/OSM counts, an Open Buildings 3 km p85 under-observed-building proxy,
  division filter, focus selector, and metric toggle for exposure proxy, gap
  share, and lowest OSM/registry ratio. Browser QA saved
  `showcase-psdq-desktop.png`, `showcase-psdq-desktop-visual.png`,
  `showcase-psdq-mobile.png`, and `showcase-psdq-mobile-visual.png` under
  `reporting-site/qa/`; checks confirmed the expected title, 16 SVG rows,
  sprint-derived hero stats, working metric toggle, no page-level horizontal
  overflow, mobile chart overflow contained inside the chart scroller, and
  zero page errors. Console output contained only existing Vite/React Router
  development warnings. This is a source-QA visual uplift for a finished PSDQ
  issue, not a facility-access claim, service-quality claim, ground-truth
  judgment, or maturity promotion. Next showcase loop should either repair
  remittance flow-weighting for a showcase-safe corridor report or start the
  next evidence-first topic sprint from `research/hook-bank.md`.
- **2026-06-16 (shock-payment showcase prototype):** Third ADB/ERDI
  showcase prototype added at `/showcase/shock-payment-rails`, reading the
  synced shock-payment rails sprint JSON and rendering an evidence-led report
  on disaster exposure versus observable payment-use rails. The first viewport
  now shows account ownership versus electronic payment use for high-exposure
  rows, rather than a generic dashboard card. The interactive evidence view
  renders a disaster-frequency by electronic-payment-use scatter with 26
  plotted rows plus a concept-gap bar panel for account-minus-payment-use and
  ASPIRE-coverage-minus-government-payment-account-use gaps. Browser QA saved
  screenshots under `reporting-site/qa/` for desktop/mobile first view and
  desktop/mobile visual view; checks confirmed the expected title, one scatter,
  one gap chart, 26 plotted points, 12 bars, sprint-derived hero stats, working
  gap toggle and economy selector, no framework overlay, no page-level
  horizontal overflow, mobile chart overflow contained inside chart scrollers,
  and zero page errors. Console output contained only existing Vite/React
  Router development warnings. This is still a prototype report and program
  prospectus candidate, not a readiness index, public claim, or maturity
  promotion. Next showcase loop is remittance parser/flow-weight repair before
  a showcase-safe remittance report, or PSDQ source-disagreement visual uplift.
- **2026-06-16 (data-freshness showcase prototype):** Second ADB/ERDI
  showcase prototype added at `/showcase/data-freshness`, reading the synced
  WDI data-freshness sprint JSON and rendering an interactive 42-DMC by
  9-indicator source-vintage matrix from the generated artifact. The report
  frame follows the ADB/ERDI pattern: planning problem, hidden data-vintage
  gap, World Bank WDI source upgrade, plain-English relative-lag method,
  visual result, non-claim box, operational use, and reproduce links. Browser
  QA saved screenshots under `reporting-site/qa/` for desktop/mobile first
  view and desktop/mobile matrix view; checks confirmed the expected title,
  one matrix with 378 cells, sprint-derived hero stats, focus-control update,
  no framework overlay, no page-level horizontal overflow, mobile matrix
  overflow contained inside the chart scroller, and zero page errors. Console
  output contained only existing Vite/React Router development warnings. This
  is still a prototype report and program prospectus candidate, not a public
  claim or maturity promotion. Next showcase loop is either shock-payment
  rails report design or L3 packaging of one of the two prototypes.
- **2026-06-16 (ADB/ERDI showcase goal opened):** Owner started a new
  persistent goal to build a 10-20 report ADB/ERDI-aligned research showcase,
  with emotionally compelling but institutionally credible evidence surfaces.
  This explicitly broadens the session from remittance-only repair to a
  goal-directed showcase batch while preserving honest maturity labels.
  `research/factory.md` now has a "Showcase report loop" requiring evidence
  first, ADB/ERDI narrative shape, interactivity only when it clarifies
  evidence, screenshot QA, and no maturity promotion from visual polish alone.
  `research/hook-bank.md` now has an ADB/ERDI showcase queue for the first
  five candidates. First prototype surface added at `/showcase` in
  `reporting-site/`, reading the synced Nepal market-climate sprint JSON and
  rendering a native interactive market-month heatmap. New sync script
  `scripts/sync-topic-sprints.mjs` publishes topic-sprint generated files and
  sprint notes into `reporting-site/public/topic-sprints/`. Browser QA saved
  screenshots under `reporting-site/qa/` and checked desktop/mobile render,
  heatmap render, no framework overlay, no page-level horizontal overflow, and
  working animation control. This is a showcase prototype, not a public claim
  or maturity promotion; next loop is L3 packaging for the Nepal report or
  design of the next showcase surface.
- **2026-06-16 (market-climate new-topic sprint):** Third new-topic L2
  sprint completed under `research/topic-sprints/`. New script
  `research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py`
  fetches WFP Nepal food-price and market CSV resources from HDX, pulls NASA
  POWER monthly point data at selected market coordinates, and writes
  `research/topic-sprints/generated/nepal-market-climate-prices-sprint.csv`,
  `research/topic-sprints/generated/nepal-market-climate-prices-sprint.json`,
  and a visually checked aligned heatmap at
  `research/topic-sprints/generated/charts/nepal-market-climate-prices-heatmap.png`.
  The generated artifact records 2,011 retained WFP rice price rows, 36
  markets before selection, 12 selected markets, 1,008 market-month cells,
  937 rows with both price anomaly and lagged precipitation anomaly, and 26
  dry-price-spike screen cells. Decision: promote "market-level climate price
  transmission" to a program prospectus candidate, not to a causal climate
  claim. This closes the current top-three new-topic L2 sprint batch; next
  action is to choose one promoted prospectus for L3 program packaging or
  start a new L1 shortlist batch.
- **2026-06-16 (shock-payment new-topic sprint):** Second new-topic L2
  sprint completed under `research/topic-sprints/`. New script
  `research/topic-sprints/scripts/sprint-shock-payment-rails.py` joins the
  existing ASPIRE/Findex/WDI social-protection panel, the EM-DAT/HDX disaster
  exposure panel, and fresh World Bank API payment-use indicators. It writes
  `research/topic-sprints/generated/shock-payment-rails-sprint.csv`,
  `research/topic-sprints/generated/shock-payment-rails-sprint.json`, and a
  visually checked two-panel chart at
  `research/topic-sprints/generated/charts/shock-payment-rails-scatter.png`.
  The generated artifact records 42 DMC rows, 38 rows with disaster-event
  frequency, 27 rows with digital-payment-use data, 21 rows with
  government-payment account-use data, and 26 plotted rows. Decision: promote
  "shock-payment rails after disasters" to a program prospectus candidate,
  not to a public claim or readiness index. The next strongest new-topic
  sprint was market-level climate price transmission.
- **2026-06-16 (new-topic creation loop):** Owner clarified that `/goal
  research` means refactoring topic creation and generating stronger **new**
  data-first research topics, not only repairing remittance or other existing
  programs. `research/factory.md` now has a "New-topic creation mode" that
  separates repair hooks from new topics and stores exploratory scripts under
  `research/topic-sprints/` until a hook earns a full program package.
  `research/hook-bank.md` now has a separate new-topic shortlist with public
  datasets, first visuals, non-generic questions, source caveats, AI roles,
  kill/defer conditions, and a new-topic L2 sprint queue. First new-topic L2
  sprint completed: `research/topic-sprints/scripts/sprint-wdi-data-freshness.py`
  pulls selected World Bank WDI series, writes a 42 DMC by 9 indicator
  freshness matrix, and renders
  `research/topic-sprints/generated/charts/wdi-data-freshness-heatmap.png`.
  The generated artifact records 378 cells, 19 missing cells, and 13 cells
  three or more years behind the indicator's own latest public reference
  year. Visual QA and source sanity are recorded in
  `research/topic-sprints/wdi-data-freshness-sprint.md`. Decision: promote
  "public data freshness blind spots" to a program prospectus candidate, not
  to a public claim or maturity label. The goal remains active because more
  top new-topic candidates still need L2 sprints.
- **2026-06-16 (later):** `/goal research` completed its first L1 -> L2
  loop. `research/hook-bank.md` is now a ranked data-first hook bank with 15
  candidates, subjective triage scores, public data objects, first-visual
  plans, non-generic questions, AI roles, and kill/defer conditions. Top
  three L2 candidates are remittance flow weighting, PSDQ district/catchment
  validation, and a road-quality/access pilot. The first L2 sprint was run on
  remittance flow weighting:
  `remittance-resilience/scripts/sprint-flow-weighted-cost.py` joined RPW Q1
  2025 corridor prices to the World Bank/KNOMAD 2021 bilateral remittance
  matrix and WDI remittance-dependence values, wrote CSV/JSON plus a PNG/SVG
  rough visual, and recorded visual/source sanity in
  `remittance-resilience/l2-flow-weighting-sprint.md`. Decision: promote the
  hook into the remittance-resilience L3 repair pass, not into a public claim
  or maturity promotion. The active flagship remains `remittance-resilience`;
  next work is parser repair, regenerated evidence, formal flow-weighting
  integration, publication re-sync, gates, build, and browser check.
- **2026-06-16:** `/goal` sharpened from a generic research-factory reminder
  into an operating bar for non-generic flagship work: one evidence spine,
  program-native visuals, visible caveats, traceable artifacts, and a
  concrete current repair bar for `remittance-resilience`. `research/factory.md`
  now starts with a **data-first hook triage** before the standard loop:
  find the public data object, build the rough visual first, ask what it makes
  visible, reverse-design the research frame from that object, and ditch/defer
  weak hooks that only produce generic rankings or topic summaries. A nested
  goal stack now governs `/goal` and `research/factory.md`: L0 lab, L1 research
  discovery, L2 hook sprint, L3 program package, L4 publication surface, L5
  human-final upgrade. The active flagship remains `remittance-resilience`,
  but the next session should not polish the old Mode A ladder as if complete.
  It should start with the
  May 2026 deepening finding: fix the RPW negative-cost normalization defect
  in `process-remittance.py`, regenerate the panel/sensitivity/median-cost
  artifacts and charts, then attempt the public bilateral-flow weighting
  keystone or record the exact data wall. `research/hook-bank.md` added as
  the `/goal research` output: a data-first candidate list ranked by public
  data object, first visual, non-generic question, AI assist, and kill/defer
  condition. `remittance-resilience/STATUS.md` now carries the active
  repair/deepening plan.
- **2026-05-29 (later, deepening pass — all 18):** Owner-directed real
  deepening across the whole portfolio ("aren't we outputting real data,
  charts, narratives, analysis? add that to the goal — full suite on all").
  After the deep-questions pass, each program now also has a `deepen-*.py`
  script, a generated artifact, and a `deepened-results.md` narrative.
  **Binding rule honored:** every number is computed by a committed script
  from data **already on disk** — the program `.cache/` raw public sources
  (the committed fetch scripts had populated them; outbound network is
  blocked this session) and committed `generated/` panels. No AI-supplied
  figures; owner-gated/uncached keystones are named as walls, not faked.
  Real findings (each traces to its artifact): **grid** — fuel concentration
  is *higher* on generation than capacity (TJK 0.80→1.00; idle thermal
  backup), the screen had the right worry and wrong variable; **migration**
  — re-ranking by share-of-population collapses the entire absolute top-5
  (CHN #2→#39), it was a population ranking; **disaster** — the
  pre-registered kill-condition *fires*: by deaths the top-2 is IDN+MMR, IND
  falls #2→#4; **social-protection** — VUT/TJK enter the top-5 and PHL/BGD
  drop once dropped legs are imputed (completeness artifact);
  **port-hinterland** — the imports-cap parameter is inert (max proxy 1.11 vs
  2.0), half the ±50% pass is hollow; **food-price** — "LAO+PAK stable" is a
  coverage artifact and the import axis is raw materials not food;
  **remittance** — the cluster *survives* a robust median cost (good news),
  but a real normalization bug in `process-remittance.py` (`raw*100 if
  raw<=1`) manufactures the −305% quotes; **access** — the access ranking is
  the inverse of OSM mapping completeness (ρ=−0.81); **invisible-urban** —
  the ±50% sweep is a rank-preserving tautology (Spearman 1.0, 0 inversions);
  **school-heat** — "KHM #1 across every perturbation" is false (loses one
  run, one is all-zeros); **coastal** — dropping population reorders the
  top-5; **climate-health** — at the flagged cap the index collapses to an
  outdoor-labor ranking, and "exposed workers" was ×total-pop not labor
  force; **PSDQ** — principal-tier OSM exceeds the registry (Central Luzon
  117%), so the gap is largely the unmapped-BHS denominator; **water-stress**
  — the top-4 saturate the water term, ordered by yield×rural;
  **air-monitoring** — 83.5% of the "14.3M unmonitored" is PNG+Timor-Leste;
  **mpi-nighttime-lights** (owner-led, not advanced) — 28/30 economies hold a
  majority of MPI in health+education, bounding the eventual NTL axis to
  ~14–31%. Named walls (owner action to close): IMF bilateral remittance
  matrix; FAO AQUASTAT TRWR + FAOSTAT crop areas; WDI employment-to-pop and
  HDI/GDP-per-capita level series; DHS/MICS microdata (PSDQ validation);
  GHSL/DEM/surge + GLOFAS/Sentinel-1 rasters (coastal, flood,
  invisible-urban); Earth Engine OAuth + VIIRS Black Marble (MPI); the
  ~2.6 GB Ookla pull (digital-performance — runnable stub committed, refuses
  to invent). Several deepenings produce real grounds to **revise headlines**
  (disaster, school-heat, port, the size/completeness-artifact clusters); the
  subagents correctly did *not* silently rewrite `results.md`/`pre-
  registration.md` — headline retraction and maturity demotion are left for
  owner review. 5 gates pass; active flagship unchanged; no maturity label
  moved.
- **2026-05-29 (later, deep-questions pass):** Owner-directed deep
  research-questions pass across the whole portfolio ("write all the
  remaining research deeply, ask all questions, no holds barred"). Wrote a
  `{program}/deep-questions.md` for all 18 programs (~42k words) plus a
  portfolio synthesis at `research/deep-questions.md`. These are
  AI-generated research **agendas, not findings** — each asks the specific,
  falsifiable, data-grounded questions the screening result never asked
  (sections: falsifiers/keystone, mechanism, decision-grade estimand,
  frontier, the existential question, data-needs table, keystone). The
  synthesis names seven recurring structural patterns: national-unit vs
  sub-national phenomenon; cluster = data-availability; hollow ±50%
  robustness; title-vs-construct gap; no independent-outcome validation; no
  mechanism; size/reporting as signal. Verified cracks worth acting on:
  `port-hinterland-friction`'s imports-cap parameter is inert (never binds
  below ~$10T imports; largest is $3.11T), so its ±50% pass is partly
  hollow; `disaster-recovery-lag`'s pre-registered kill-condition is
  *already met* (by the deaths metric the top-2 is IDN+CHN, not CHN+IND);
  `school-heat-disruption`'s "KHM #1 across every perturbation" is
  contradicted by its own `sensitivity-runs.json` (one run zeros all 32
  economies; KHM is #2 in another); `water-stress` and `flood-market-access`
  indices contain no diversification / no road-market-flood term despite
  their names; `access-services` likely ranks OSM completeness, contradicting
  sibling `public-service-data-quality` on data already in the repo. No
  empirical claims were made or changed; no maturity labels moved.
  Verification: 5 gates pass (banned-words 454 files, dmc-framing 459);
  `npm run build` clean. Suggested next step (owner): pick one program and
  answer its keystone — most are blocked only by reaching for public data
  already named in the file.
- **2026-05-29 (later):** Native-chart rendering layer added
  (owner-requested proof of concept; "beautiful charts natively…
  maps charts etc"). Program heroes can now render as interactive
  in-browser SVG instead of a static matplotlib PNG, reading the SAME
  committed `generated/*.json` a reviewer downloads on the Data tab — so
  the visual is *more* auditable than a raster, not less. Scope:
  - New deterministic basemap builder `scripts/build-webmap.mjs` →
    committed `reporting-site/public/geo/asia-pacific.geojson` (152 KB;
    Asia+Oceania, Pacific-centered at lon0=125, simplified from the
    vendored Natural Earth 50m) + `asia-pacific-centroids.json`. A
    geometry transform of a public-domain source; introduces no numbers.
  - New primitives in `reporting-site/src/lib/charts/` + components in
    `reporting-site/src/components/charts/` (`ChoroplethMap`, `Scatter`,
    `RankedBar`, `ChartFrame`, tooltip, responsive hook). Themed to the
    rebrand's ADB tokens; `attestation_chain` rendered as real text
    (§18.2) rather than burned into pixels.
  - Showcase at `/native-charts` renders the remittance map + scatter +
    ranked bar from `remittance-resilience-adb-panel.json`, with a toggle
    to compare against the current PNG. Cluster derived from the committed
    panel (top-5 by the triage composite — selection only, never
    headlined, §6.4); headline number + TJK exclusion annotation derived
    from data, not hard-coded.
  - `Topic.tsx` shows the native map as the remittance hero in-context;
    every other program still renders its PNG (slug-guarded), and the
    native hero falls back to the PNG while data loads or on any error —
    no regression for the other 15 programs.
  - Verification: `npm run build` clean; browser-checked 1280 desktop +
    375 mobile, zero console errors, zero horizontal overflow (fixed a
    mobile SVG-overflow bug — charts now scale to their container); five
    gates pass. Publication-surface capability, not a per-program
    advancement; active flagship unchanged. Per-program roll-out happens
    as each program reaches publication stage.
- **2026-05-29:** ADB visual-identity rebrand of `reporting-site`
  (owner-requested; "make the styling and feel like ADB"). Refactored
  the design **primitives** only — every page reads from these via
  semantic classes + CSS vars, so the token layer was the single
  leverage point and no per-page rewrite was needed. Ground-truthed the
  palette/type from the live adb.org computed styles (not guessed):
  white surfaces, near-black text `#212529`, ADB web blue `#007DB8` as
  the one signature accent, ADB green `#5A8227` / gold `#FBB00E`
  secondaries, navy `#002569`. Type switched from the editorial serif
  stack (Fraunces + Source Serif 4) to **Source Sans 3** — the closest
  free substitute for ADB's proprietary Ideal Sans — with ADB's exact
  system-ui fallback; JetBrains Mono kept for data/attestation stamps.
  - Token NAMES kept stable (`--crimson` now holds ADB blue, `--sage`
    green, `--ochre` gold) so the re-skin propagated to all ~40 pages
    + `ui.tsx` without a risky rename.
  - Files: `index.html` (fonts, theme-color), `tailwind.config.js`
    (palette + font stacks), `src/index.css` (`:root` tokens, body +
    heading fonts, display/kicker/lede classes, heatmap → blue scale,
    article bodies serif→sans, drop-caps + justified text retired),
    `public/favicon.svg` (ADB-blue "A" mark), `Layout.tsx` (blue top
    rule, brand mark, blue active-nav), `Home.tsx` (category kicker).
  - Verification: 5 gates pass; `npm run build` 3.56s; browser-checked
    at 1280 desktop + 375 mobile, zero console errors, zero horizontal
    overflow.
  - **Known follow-up (not done here):** the 16 hero thumbnail PNGs are
    still rendered in the old warm palette by the Python pipeline
    (`scripts/thumbnail_lib.py` + per-program `build-thumbnail.py`);
    they now sit inside ADB-blue/white chrome. Full consistency needs
    an ADB-palette pass on the matplotlib stack + a 16-thumbnail
    re-render + `sync-evidence`. Active flagship unchanged.

- **2026-05-20 (later):** Second honesty loop, owner-prompted (loop
  loop loop). Read every program's `limitations.md` and audited each
  thumbnail against its program's own admitted caveats. Eleven more
  fixes shipped:
  - **migration** — Afghanistan's 7.5 M is overwhelmingly refugees
    and post-2021 displaced (per IZA C-3); subtitle now discloses
    "Cumulative STOCK, not annual flow. Afghanistan's 7.5 M is
    overwhelmingly refugees and post-2021 displaced — read as
    structural-pressure, not labor migration."
  - **food-price** — Pakistan's 2023 CPI was FX-driven, not
    climate-driven (per WB Food Crisis Observatory C-4). Subtitle
    now discloses the FX driver and says "the joint exposure here
    is not a climate-transmission claim." Also: Bangladesh
    downgraded to hollow ring marker labeled "(joins from N=5)"
    since the stable claim is LAO+PAK only across N=3..10.
  - **grid-reliability** — Title "Six grids RUN on a single fuel"
    implied generation; WRI is installed capacity. Reframed to
    "Six grids: single-fuel CAPACITY concentration" with explicit
    "Capacity ≠ generation; 2022–2025 solar buildouts not in this
    vintage" disclosure.
  - **water-stress** — TKM's 1,868 % is Amu Darya inflow against
    internal-only renewable denominator, not over-pumping (per
    limitations.md and IWMI C-2). Subtitle now says "Values above
    100 % are not over-pumping per se — the denominator excludes
    transboundary river inflows."
  - **climate-health** — WDI PM2.5 is national mean and conceals
    within-country variance (IND/CHN/IDN labeled ‡); AFG/MMR/KHM/
    LAO/TLS values are monitor-interpolated (labeled †). Inline
    legend explains the markers.
  - **social-protection** — Findex 2021 conducted during pandemic
    elevated account ownership figures; subtitle now discloses
    pandemic-vintage caveat and "Ownership ≠ active use."
  - **invisible-urbanization** — Signal co-produced by real urban
    growth AND delayed statistical reclassification of rural
    settlements (per UN-Habitat C-3); subtitle discloses the two
    are not separable here.
  - **air-monitoring** — Gap-score is HDI-correlated, not
    independent (per HEI C-4); subtitle adds "low-HDI DMCs tend to
    have both more pollution AND fewer monitors."
  - **port-hinterland** — LPI is perception-based survey not
    measured (per LPI team C-1); landlocked DMCs (KAZ, UZB in the
    top-15) are structurally different. Subtitle discloses both.
  - **remittance** — TON/VUT/WSM each have 5–8 RPW corridors only
    with wide sampling uncertainty (per Pacific Community C-4);
    subtitle disclosed alongside the existing TJK exclusion note.
  - Verification re-run: 5 gates pass, `npm run build` 2.89s,
    sync-evidence clean.

- **2026-05-20:** Visual-first refactor honesty pass. Owner pushed
  back on whether the headline numbers were accurate (not just
  whether they traced to a script — whether they meant what the
  visual implied). Self-audit surfaced 10 data-honesty issues across
  the 16 thumbnails. Each was rewritten and re-rendered:
  - **PSDQ** — unified the BGD vs PHL choropleth color scale to a
    shared 0–0.7 (previously per-panel scales made a dark BGD region
    visually equate to a 4× darker PHL region).
  - **remittance-resilience** — TJK (48% remittance/GDP, largest in
    the panel) was silently dropped from the cluster for sparse RPW
    coverage. Now shown on the map with hatched fill and an explicit
    "excluded — only 1 corridor / 1 firm in RPW" annotation.
  - **migration-displacement-signals** — title said "Six corridors
    carry 56M" but visual was 7 origins / 64.7M. Realigned to the
    program's stable 5-origin cluster (IND, CHN, BGD, AFG, PHL),
    53M total; surfaced top-9-destination coverage (91%).
  - **disaster-recovery-lag** — "1.77B affected in China" was
    greater than China's population because EM-DAT counts the same
    person across multiple events. Reframed primary axis as recorded
    disasters per year; total_affected shown as "person-events (may
    double-count)" secondary label.
  - **port-hinterland-friction** — bar of imports ÷ LPI made China
    (mid-pack LPI 3.70) look like the worst-logistics country.
    Replaced with a two-axis bubble scatter: LPI on X, imports on Y
    (log scale). China high-volume / mid-LPI; Bangladesh/Pakistan
    low-volume / low-LPI now clearly distinct.
  - **coastal-informal-risk** — headline mixed China's 1.4B
    population with a color scale of slum %. Single-axis now: 58%
    Myanmar slum-share of urban as headline (consistent with
    color encoding).
  - **air-monitoring** — "14.3M people, 13 economies" sounded
    distributed but PNG + Timor-Leste = 84% of the population. Now
    explicitly surfaced in the subtitle.
  - **access-services** — Oddar Meanchey's 319k people/facility is
    OSM-tag coverage, not actual facility count. Relabeled
    everywhere as "OSM-tagged health amenity" with explicit PSDQ
    cross-reference that OSM under-counts the official registry by
    5–10×.
  - **food-price-climate-transmission** — subtitle said "upper-
    right corner" but data was upper-LEFT (high CPI, moderate
    ag-imports). Rewrote to "clear both axes" framing matching the
    geometry.
  - **climate-health-workdays** — "799 M outdoor workers in India"
    was `outdoor_labor_share × total_population` (counts children
    and retirees). Headline reframed as "55% of India's employment
    is outdoor" with explicit note that the panel multiplies by
    total population, not labor force.
  - Verification re-run: 5 gates pass, `npm run build` 3.19s,
    browser-check 1280 desktop + 375 mobile, zero console errors,
    no horizontal overflow.
- **2026-05-19:** Visual-first refactor shipped end-to-end. Sixteen
  programs (every program with committed panel data) now render a
  1600×900 hero thumbnail PNG+SVG with a sidecar JSON; each thumbnail
  reads only committed `generated/*.csv|json` inputs and burns the
  `attestation_chain: ai-first` line into the image so a screenshot
  retains the labeling. Two programs (`digital-performance`,
  `mpi-nighttime-lights`) render honest placeholder cards.
  - New spec at `research/visual-first-refactor.md` extends the
    factory.md visualization rule with a hero-visual contract.
  - New shared helper at `scripts/thumbnail_lib.py` (figure setup,
    editorial typography, world basemap loader, attestation footer,
    sidecar writer).
  - New `opensrc/` directory with Natural Earth 110m + 50m country
    boundaries (public domain) and `REFERENCES.md` pinning the
    matplotlib + geopandas + pycirclize stack.
  - New per-program scripts: `{program}/scripts/build-thumbnail.py` for
    each of the 16 programs.
  - `scripts/sync-evidence.mjs` extended to publish a `hero` block in
    each `manifest.json` and an aggregated `public/programs/heroes.json`
    so the home page does one fetch.
  - `reporting-site/src/pages/Home.tsx` rewrote as a 16:9 thumbnail
    grid (1 col mobile / 2 col tablet / 3 col desktop), with maturity
    + attestation chips overlaid and a styled placeholder for
    programs without a hero.
  - `reporting-site/src/pages/Topic.tsx` adds a hero header above the
    tab strip with the same image shown on the home grid.
  - Composite-demotion editorial pass on `programs.ts`: six summaries
    (climate-health-workdays, port-hinterland-friction,
    remittance-resilience, school-heat-disruption,
    social-protection-shock-coverage, water-stress-crop-diversification)
    rewritten to lead with a single visceral non-composite number per §6.4.
  - Verification: 5 gates pass (banned-words, dmc-framing, citations,
    composite-headline, wip); `cd reporting-site && npm run build`
    succeeds in 2.37s; browser-checked at 1280×900 desktop and 375×800
    mobile with zero console errors and zero horizontal overflow.
  - Active flagship unchanged (`remittance-resilience`); this is a
    cross-program publication-surface refactor not a per-program
    advancement.
- **2026-05-12:** ADB/ERDI-style polish pass on PSDQ public surfaces under
  the new `/goal` skill's flagship bar. Three live-surface edits to the
  PSDQ article (subtitle, abstract, opening of "# The question") +
  governance alignment in `CLAUDE.md` (hard-walls table: "with Arturo" →
  "by an owner-designated reviewer"). Viewport-verified at 1280px desktop
  and 375px mobile, zero console errors, zero horizontal overflow. Five
  gates pass; `npm run build` succeeds in 2.75s. One edit was reverted
  for honesty: an h1 rewrite on `reporting-site/src/pages/ProgramPSDQ.tsx`
  turned out to be in orphan code (component is not routed; `Topic.tsx`
  serves `/<slug>`). `ProgramPSDQ.tsx` is dead code in the tree — either
  wire it back via the router or delete; out of scope for the polish pass.
  PSDQ remains **ai-first finished for current issue** under the same
  attestation chain. **Next flagship pick is pending owner direction**;
  candidates in the PP queue in `research/wip-register.md`; my read is
  remittance-resilience for Mode-A readiness (top-5 corridor cluster
  already stable across ±50%; article draft exists; gap to PSDQ-grade is
  the full publication ladder + Mode A review loop).
- **2026-05-12:** Goal-skill de-specialized.
  `.claude/skills/goal.md` "Current Flagship" section no longer names
  PSDQ; replaced with a STATUS.md-pointer pattern so the goal doesn't go
  stale on flagship rotation. PSDQ-specific guardrails (e.g., "PSA
  poverty overlay is a context layer") moved to PSDQ's README/STATUS
  where program-specific guardrails belong.
- **2026-05-07:** Per-program loop instituted (publication ladder + three
  review modes). 9 programs demoted PR/SR → PP under §16. PSDQ remains
  active flagship. STATUS.md slimmed to a principle-driven board (this
  refactor); PSDQ-specific narrative migrated to
  `public-service-data-quality/STATUS.md`.
- **2026-05-07:** PSDQ completed the full Mode A loop: publication ladder
  built (brief + blog + social + slide deck via Quarto), choropleth
  visualizations added (PHL ADM1, BGD ADM1, PHL ADM3 poverty), 257
  unresolved BARMM Maguindanao NHFR records resolved by deterministic
  barangay-name lookup (residue 8), reviewer packet rebuilt (6.1 MB),
  Mode A self-review + critique-pass + AI second-opinion code review
  iteration closed. PSDQ is **ai-first finished for current issue**.
  Next program from the queue can now enter the loop.
- **2026-05-07:** GitHub-prep cleanup. Repository root now has a
  reader-facing `README.md`, `LICENSE` (MIT for code), and
  `LICENSE-CONTENT` (CC BY 4.0 for research artifacts). `.gitignore`
  rewritten to exclude per-program `.cache/` directories (~8 GB total,
  reproducible from public sources via committed fetch scripts) while
  keeping each cache's `README.md` (regen instructions) committed.
  The 2026-04-25 review packet moved to `_archive/review-packets/`
  (the 2026-05-07 packet stays in `review-packets/` as the current
  one). `luminosity-gap/README.md` now opens with a "legacy" note
  pointing readers to the active `reporting-site/` instead. The repo
  is ready for `git init && git push`.

## Handoff prompt

Use this when starting a fresh session:

```text
Read research/STATUS.md, then the active flagship's {program}/STATUS.md
named in the board. Then read CLAUDE.md and research/factory.md.
Continue the active flagship's next focused work. State the active
program, stage, next output, and verification plan before editing files.
```
