# Public Service Data Quality — operating status

This is the per-program operating state for `public-service-data-quality`.
Repository-level focus and process rules live in `research/STATUS.md`,
`research/factory.md`, and `CLAUDE.md`. This file holds only what is
specific to PSDQ.

Last updated: 2026-06-19.

## Current

| Field | Value |
|---|---|
| Maturity label | PR (under §18 ai-first); **ai-first finished for current issue** as of 2026-05-07 (Mode A exit condition met) |
| Active stage | L3 source-disagreement module plus facility-validation sample, automated coded screen, AI public-source review ledger, and 8-row candidate-resolution pass added; public-source confirmation inside the candidate lanes is the next upgrade; PR maturity label unchanged |
| Active flagship | Yes, as of 2026-06-19 — rotated back in after the remittance L3 flow-weighting repair closed under Mode A. |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | `/program/public-service-data-quality/evidence` |

## Current output target

A reviewer-credible PSDQ source-disagreement package for the showcase bench:
start from the Bangladesh exposure-ranked registry-map visual, package the
matching strata, validation sample, automated coded screen, AI row-review
ledger, and caveats, make the source upgrade clear in the public surface, and
preserve the existing PR maturity label without implying human-final review.

## Last completed

- **2026-06-19:** Added the Bangladesh candidate-resolution pass for the
  PSDQ facility-validation flags. New no-network script
  `scripts/resolve-bgd-facility-candidate-rows.py` reads the AI review ledger,
  OSM-candidates CSV, and AI review summary, then writes
  `generated/psdq-bgd-facility-validation-candidate-resolution.csv` and
  `generated/psdq-bgd-facility-validation-candidate-resolution-summary.json`.
  The pass keeps all 8 candidate-resolution rows open while separating them
  into 1 probable alias/campus lane, 2 same-site classification-conflict lanes,
  2 possible aliases, 1 local-script name gap, 1 ambiguous nearby candidate,
  and 1 weak nearby OSM signal. Added
  `facility-validation-candidate-resolution.md`, updated README, REPRODUCE,
  evidence sync/review-packet inclusion, the L3 note, and
  `/showcase/psdq-source-disagreement`. This is AI public-source candidate
  resolution, not human validation, a maturity promotion, or a human-final
  upgrade. Verification passed: new script and program-script `py_compile`,
  production site build, six deterministic gates, review-packet rebuild, and
  agent-browser desktop/mobile QA at 1365px and 375px with no page-level
  horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-candidate-resolution-desktop.png` and
  `reporting-site/qa/showcase-psdq-candidate-resolution-mobile.png`. Rebuilt
  review packet folder and zip:
  `review-packets/public-service-data-quality-2026-06-18/` and
  `review-packets/public-service-data-quality-2026-06-18.zip`.
- **2026-06-19:** Added the Bangladesh AI public-source review ledger for the
  PSDQ facility-validation flags. New no-network script
  `scripts/review-bgd-facility-validation-flags.py` reads the coded-screen
  CSV, OSM-candidates CSV, and coded-summary JSON, then writes
  `generated/psdq-bgd-facility-validation-ai-review.csv` and
  `generated/psdq-bgd-facility-validation-ai-review-summary.json`. The ledger
  keeps all 71 flagged rows open while separating them into 40 public-map-gap
  checks, 23 coordinate-source repairs, 6 name/type resolution rows, and 2
  nearby-OSM-without-registry-match rows. Added
  `facility-validation-ai-review.md`, updated README, REPRODUCE,
  evidence sync/review-packet inclusion, hook bank, quality audit, and
  `/showcase/psdq-source-disagreement`. This is AI public-source review, not
  human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, and browser QA at 1365px desktop and
  375px mobile with no page-level horizontal overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-ai-review-desktop.png` and
  `reporting-site/qa/showcase-psdq-ai-review-mobile.png`. Rebuilt review
  packet folder and zip:
  `review-packets/public-service-data-quality-2026-06-18/` and
  `review-packets/public-service-data-quality-2026-06-18.zip`.
- **2026-06-19:** Added the automated Bangladesh facility-validation coded
  screen for the PSDQ source-disagreement L3 module. New no-network script
  `scripts/code-bgd-facility-validation-sample.py` reads the 76-row validation
  sheet, cached all-Bangladesh OSM health-feature pull, and geoBoundaries ADM3,
  then writes `generated/psdq-bgd-facility-validation-coded-screen.csv`,
  `generated/psdq-bgd-facility-validation-osm-candidates.csv`, and
  `generated/psdq-bgd-facility-validation-coded-summary.json`. The automated
  screen codes 40 rows as missing public-map points, 23 as registry coordinate
  issues, 5 as confirmed same-facility matches, 3 as probable aliases, 3 as
  classification mismatches, and 2 as OSM-only candidates. Added
  `facility-validation-coded-screen.md`, updated the L3 note, README,
  REPRODUCE, evidence sync/review-packet inclusion, showcase registry, hook
  bank, quality audit, and `/showcase/psdq-source-disagreement`. The route now
  fetches the coded-summary JSON, shows a grouped coded-screen chart, and
  links the coded-screen downloads. This is automated triage, not manual
  validation, a maturity promotion, or a human-final upgrade. Browser QA
  passed at 1365px desktop and 375px mobile with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-coded-screen-desktop.png` and
  `reporting-site/qa/showcase-psdq-coded-screen-mobile.png`.
- **2026-06-19:** Added the Bangladesh facility-validation sample design for
  the PSDQ source-disagreement L3 module. New no-network script
  `scripts/design-bgd-facility-validation-sample.py` reads the L3 strata,
  exposure-ranked disagreement table, and DGHS facility-coordinate extract,
  then writes `generated/psdq-bgd-facility-validation-sample.json`,
  `generated/psdq-bgd-facility-validation-sample-upazilas.csv`,
  `generated/psdq-bgd-facility-validation-sample-facilities.csv`, and
  `generated/psdq-bgd-facility-validation-coding-sheet.csv`. The design
  covers 20 sampled upazilas and 76 DGHS facility rows; 69 sampled facility
  rows are coordinate-ready. Added `facility-validation-sample.md`, updated
  the source-disagreement L3 note, README, REPRODUCE, evidence sync and
  review-packet inclusion, showcase registry, hook bank, quality audit, and
  `/showcase/psdq-source-disagreement`. The route now fetches the sample JSON,
  shows a validation-sample panel, and links the blank coding sheet. This is
  not a validation outcome, maturity promotion, or human-final upgrade.
  Verification completed so far: sample script and `py_compile` passed;
  `npm run build` passed; six deterministic gates passed; browser QA passed at
  1365px desktop and 375px mobile with no page-level horizontal overflow and
  no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-validation-sample-desktop.png` and
  `reporting-site/qa/showcase-psdq-validation-sample-mobile.png`.
- **2026-06-19:** Added the Bangladesh source-disagreement L3 evidence module
  for the showcase bench. New no-network script
  `scripts/build-bgd-source-disagreement-strata.py` reads the existing BGD
  exposure-ranked disagreement and road-context artifacts, then writes
  `generated/psdq-bgd-source-disagreement-strata.{json,csv}` with ratio
  buckets, validation residues, and top validation rows. Added
  `source-disagreement-l3-module.md`, updated `REPRODUCE.md`, `README.md`,
  evidence sync/review-packet inclusion, the showcase registry, the hook bank,
  and `/showcase/psdq-source-disagreement`. The route now fetches the strata
  JSON, shows the validation ledger before the interactive workbench, and links
  directly to the L3 note and downloads. Rebuilt review packet folder and zip:
  `review-packets/public-service-data-quality-2026-06-18/` and
  `review-packets/public-service-data-quality-2026-06-18.zip` (UTC-dated by
  the packet script). Verification completed: strata script passed;
  `npm run build` passed; six deterministic gates passed; browser QA
  passed at 1365px desktop and 375px mobile with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-l3-desktop.png` and
  `reporting-site/qa/showcase-psdq-l3-mobile.png`. This is not a maturity
  promotion and not a human-final upgrade.
- **2026-06-19:** Reopened PSDQ as the active flagship for the showcase
  source-disagreement L3 deepening loop after the remittance flow-weighting
  repair was committed as `225d4d2`. The next output is not a new maturity
  promotion. It is a tighter evidence spine around
  `/showcase/psdq-source-disagreement`: matching strata, validation notes,
  source caveats, and a public-surface QA pass.
- **2026-06-16:** Added a showcase-native PSDQ source-disagreement visual
  uplift at `/showcase/psdq-source-disagreement`. The surface reads the
  committed Bangladesh exposure-ranked disagreement CSV/JSON and the PSDQ
  national summary from `reporting-site/public/programs/public-service-data-quality/generated/`.
  It frames the registry-map problem as source QA before service-access
  mapping, not as a facility-quality, access, or ground-truth claim. The
  interactive workbench ranks upazila rows by Open Buildings under-observed
  proxy, registry gap share, or lowest OSM/registry ratio, with division and
  focus controls. Browser QA captured desktop/mobile first-view and visual
  screenshots under `reporting-site/qa/`; checks confirmed 16 rendered SVG
  rows, working metric toggle, no page-level horizontal overflow, mobile chart
  overflow contained in the chart scroller, and zero page errors. Console
  output contained only existing Vite/React Router development warnings.
  Maturity label unchanged.
- **2026-05-12:** ADB/ERDI-style polish pass on PSDQ public surfaces under
  the new `/goal` skill's flagship bar. Three live-surface edits + one
  governance alignment, no claim change. **Live edits** (shipped to the
  site via `articles/measurement-gap-philippines-bangladesh.md` →
  `reporting-site/public/articles/`, verified in viewport at 1280px and
  375px): (1) article subtitle tightened from a dense two-sentence
  tongue-twister using the stale "screening result" label to a
  finding+benchmark formulation matching the working-paper convention; (2)
  article abstract restructured to lead with the 17.1% / 11.8% headline
  numbers and the 9.8× within-country gradient (NCR 63.5% vs BARMM 6.5%)
  before the upgrade-pass and attestation context; (3) article opening of
  "# The question" rewritten from textbook-pedagogical ("Two questions sit
  underneath any planning exercise") to stakes-led ADB/ERDI register
  ("Project teams that build facility catchments, service-coverage maps,
  and travel-time isochrones routinely combine public maps with official
  registries… A planner who treats the gap as noise will treat coverage
  problems as present-but-small when they are present-and-systematic").
  The Topic.tsx page renders the article-frontmatter `title` as h1 and
  `subtitle` as the prominently-displayed hook beneath it — so the
  finding-led hook lives in the subtitle, with the descriptive title above
  matching ADB working-paper convention. **Governance alignment**:
  `CLAUDE.md` hard-walls table line 78 changed from "real internal review
  with Arturo" to "real internal review by an owner-designated reviewer"
  — aligns with `/goal` skill's standing wording, makes the human-final
  hard-wall structural rather than personnel-specific.
  **Non-shipping edit (reverted)**: I initially also edited the h1 +
  subhead on `reporting-site/src/pages/ProgramPSDQ.tsx`, but viewport
  verification revealed `ProgramPSDQ.tsx` is orphan code — not imported
  by the router; the live `/<slug>` route is served by Topic.tsx. The
  ProgramPSDQ edit was reverted to its pre-pass state to keep the diff
  history honest. All five gates pass; `sync-articles.mjs` re-synced 25
  articles; `npm run build` succeeds in 4.80s. Mode A exit condition
  unchanged; PSDQ remains **ai-first finished for current issue** under
  the same attestation chain.
- **2026-05-07:** Browser-checked the three PSDQ public surfaces
  (`/program/public-service-data-quality`, the article, and the evidence
  page) at desktop (1280px) and mobile (375px). All three render the new
  poverty-overlay numbers correctly: 1,642 ADM3 rows, 1,632 joined (1,597
  SAE + 35 OpenSTAT), 10 explicit source-missing. Console: 0 errors. Fixed
  one mobile regression on the Evidence page (rendered-markdown tables and
  inline `<code>` were not constrained); added ~10 lines of additive CSS to
  `reporting-site/src/index.css` giving rendered-markdown tables
  `overflow-x: auto` and inline `<code>` `overflow-wrap: anywhere`. After
  fix: document width 376 ≈ viewport 375, 33/33 markdown tables now
  scrollable, 436/436 inline `<code>` blocks now wrap. All five gates pass;
  `npm run build` succeeds in 7.00s.
- **2026-05-05:** Owner manually downloaded the official PSA 2023 SAE
  workbook and seeded the deterministic cache via
  `python scripts/fetch-phl-sae-poverty.py --sae-xlsx <path>`. Generated
  `psdq-phl-admin3-poverty-context.{csv,json}`: 1,597 SAE rows + 35
  OpenSTAT direct-estimate rows joined, 10 ADM3 rows still source-missing
  and not imputed.
- **Earlier:** Hardened the PSA fetcher (`sites/default`, `system/files`,
  `www` variants; Cloudflare blocker recorded as source-status). Added
  `SOURCE-ACTION.md`, `REPRODUCE.md`, `upgrade-gap.md`. Updated the public
  program page with a poverty-source-status panel that distinguishes SAE,
  OpenSTAT direct-estimate, and source-missing rows. Updated the
  reader-facing working paper to reflect the ADM3/upazila granular
  upgrade, Bangladesh road context, and the reproducibility runbook.

## Next focused work

Current loop:

1. Use the 8-row candidate-resolution pass in
   `generated/psdq-bgd-facility-validation-candidate-resolution-summary.json`
   and `generated/psdq-bgd-facility-validation-candidate-resolution.csv` as
   the immediate worklist.
2. Public-source confirm the alias/campus, classification-conflict,
   possible-alias, local-script name-gap, ambiguous, and weak-nearby lanes;
   then move to coordinate-source repair rows and high-exposure public-map-gap
   checks.
3. Use only public DGHS rows and OSM/Overpass evidence. Do not use private
   facility lists or owner-only credentials. Stop if validation requires
   non-public access.
4. Record reviewer notes row by row and compare any public-source labels with the
   automated coded-screen labels before changing any source-disagreement
   claim.
5. If public evidence is insufficient, keep the row unresolved rather than
   forcing a same-facility or missing-map code.
6. Rerun sync/build/gates/browser QA after any public-surface change.

Historical publication-ladder closeout remains below for context.

The current flagship has the working paper, program page, and evidence
packet. The publication ladder defined in `research/factory.md` requires
four more tiers before PSDQ counts as "finished for current issue" under
the new loop standard:

1. **PSDQ brief** — **done 2026-05-07**: `articles/_brief/public-service-data-quality.md`,
   ~600 words including frontmatter, single chart (PHL ADM1 choropleth SVG).
   Slug `public-service-data-quality-brief`, available at
   `/findings/public-service-data-quality-brief`. Verified at desktop and
   mobile (chart 712px / 277px respectively, zero overflow). All gates pass.
   Co-amendment: extended `scripts/sync-articles.mjs` to recurse into
   publication-ladder tier subdirectories (`articles/_brief/`, `_blog/`,
   `_social/`, `_slides/`) and tag each entry with a `tier` field in
   `index.json`.
2. **PSDQ blog post** — **done 2026-05-07**:
   `articles/_blog/public-service-data-quality.md`, ~750 words narrative
   for the general dev-econ reader. Same chart as the brief (PHL ADM1
   choropleth SVG) under the visualization-rule single-source-of-truth
   principle. Slug `public-service-data-quality-blog`, available at
   `/findings/public-service-data-quality-blog`. Verified at desktop and
   mobile, all gates pass. Cites Macharia 2025, Sandefur & Glassman 2015,
   South et al. 2021, Maina et al. 2019.
3. **PSDQ social card** — **done 2026-05-07**:
   `articles/_social/public-service-data-quality.md`. Tweet body 252/280
   chars: "Two maps of the same country don't agree…". Same chart as
   brief and blog (PHL ADM1 choropleth SVG). Includes alt text describing
   the visual gradient and links back to brief, blog, working paper, and
   evidence packet. Slug `public-service-data-quality-social`, available
   at `/findings/public-service-data-quality-social`. All gates pass.
4. **PSDQ slide deck** — **done 2026-05-07**:
   - Source: `articles/_slides/public-service-data-quality.md` (Quarto
     markdown, 11 slides, attestation chain `ai-first`).
   - Build: `scripts/build-slides.mjs` regenerates the choropleths via
     `build-choropleth.py` (single source of truth — same charts as
     brief, blog, social, program page), then runs `quarto render
     --to pptx` and moves the artifact into the program's public folder.
   - Output: `reporting-site/public/programs/public-service-data-quality/public-service-data-quality-deck.pptx`
     (~702 KB with embedded charts).
   - Quarto 1.9.37 installed via winget at `C:\Program Files\Quarto\bin`.
     Build passes 5/5 gates.
   - Slide content covers: question · headline · PHL choropleth ·
     BGD choropleth · ±50% sensitivity · ADM3 poverty overlay ·
     why-it-matters · explicit non-claims · reproducibility ·
     attestation chain.
4. **Reviewer-ready source/method packet**: bundled `results.md`,
   `sensitivity.md`, `limitations.md`, the poverty-context CSV, the
   manifest, and a one-page cover letter — refresh from the 2026-04-25
   packet at `review-packets/`.
5. **Reviewer-ready packet** — **done 2026-05-07**:
   `review-packets/public-service-data-quality-2026-05-07/` (folder, 90
   files: 6 publication-tier + 75 program + 9 shared) and `.zip`
   (6.1 MB, emailable). The packet bundles the full publication ladder
   (working paper, brief, blog, social card, slide deck `.pptx` + source)
   plus all program artifacts (literature, pre-reg, sensitivity,
   limitations, reviews, generated CSVs, choropleth charts, scripts) plus
   shared governance (Constitution, references.bib, red-team.md outreach
   template, versions.json, manifest.sha256). Cover README orients the
   reviewer by attention budget (2 min, 10 min, 20 min, 90 min). Built
   by extended `scripts/build-review-packet.mjs` (now recurses into
   generated/ subfolders, includes publication-ladder tiers, includes
   the built `.pptx`). Co-amendment in `build-choropleth.py`: added
   geometry simplification (0.005° ADM1, 0.001° ADM3) so SVG file sizes
   are publishable (1.0 MB and 4.3 MB respectively, down from 336 MB
   and 357 MB at full PSA/NAMRIA precision).
6. **Resolve the 257 unresolved Philippines NHFR records** — **done
   2026-05-07** (249 of 257 resolved, residue 8): all 257 were in BARMM
   Maguindanao ctymuncode prefixes PH19087* and PH19088*, a code-vintage
   mismatch where NHFR uses an older PSGC numbering and PSA/NAMRIA 2023
   has reassigned the same barangays to modern ADM3 polygons. New
   resolver `scripts/inspect-barmm-codes.py` extracts the barangay name
   from each NHFR facility name (the prefix before "BARANGAY HEALTH
   STATION", "RURAL HEALTH UNIT", etc.), looks the name up in PSA/NAMRIA
   2023 ADM4 within ADM2 PH19087+PH19088, and takes the parent ADM3.
   Per ctymuncode the resolution is the majority winner — every resolved
   group had unanimous votes (share = 1.0). 17 of 18 ctymuncode groups
   resolved; 249 of 257 records assigned to a specific ADM3. Resolver
   wired into `scripts/build-phl-admin3-open-buildings-context.py` as
   the `barmm_barangay_name_resolved` rule. Audit trail at
   `generated/psdq-phl-nhfr-barmm-ctymun-resolution.json`. New ADM3 match
   rate is 99.98% overall and 99.98% for clinical-tier records (was
   99.42% / 99.31%). The remaining 8 records are all in a single
   ctymuncode (1908807) whose facility names do not contain a recognizable
   barangay name (e.g., "ABPI-SAMAMA MEDICAL LYING IN CLINIC AND
   HOSPITAL"); they are kept explicitly unresolved as a source-quality
   residue and are not imputed. Updated docs: `README.md`,
   `upgrade-gap.md`, working paper, this file.
6. **PSDQ choropleth map** — Python build **done 2026-05-07**:
   `scripts/build-choropleth.py` produces three publication-ready
   maps as PNG + SVG:
   - `generated/charts/psdq-choropleth-phl-adm1.{png,svg}` — Philippines
     OSM/NHFR clinical-tier ratio per ADM1 (17 regions). Includes the
     DOH-NHFR ↔ PSA-PSGC code mapping (six regions use different codes
     across the two systems).
   - `generated/charts/psdq-choropleth-bgd-adm1.{png,svg}` — Bangladesh
     OSM/DGHS clinical-tier ratio per ADM1 (8 divisions).
   - `generated/charts/psdq-choropleth-phl-adm3-poverty.{png,svg}` —
     PHL ADM3 official 2023 poverty incidence (1,632 of 1,642 polygons
     joined to PSA SAE + OpenSTAT direct; 10 explicit source-missing).
   Synced to `reporting-site/public/programs/public-service-data-quality/generated/charts/`.
   Sub-steps status:
   - **Done 2026-05-07**: Embedded the three choropleth SVGs into the
     PSDQ program page as a "Spatial picture" section between the
     header and the granularity-upgrade section. Verified at desktop
     (1280px, two-column grid for ADM1 maps + full-width ADM3 poverty)
     and mobile (375px, single-column stack, zero horizontal overflow,
     zero console errors). Production build passes (84 modules, 537 KB
     JS / 46 KB CSS). Same SVG files load on both surfaces; alt text
     describes the visual story; captions cite the underlying CSV.
   - **Pending**: Use the same script's logic as the chart in the
     Quarto slide deck (Tier 6) and the brief (Tier 3). The slide-deck
     and brief should call the same Python via Quarto code blocks, not
     a separate render. The React component upgrade (`react-simple-maps`
     for interactivity) is deferred until a program needs zoom/pan; the
     static SVG is sufficient for PSDQ.

Then the **review loop** (`research/factory.md`):

6. Owner picks review mode (Mode A, B, or C). Default is Mode A.
7. AI runs the chosen mode's review steps and iterates to convergence.
8. Exit condition: AI self-convergence under Mode A; spot-check approval
   + AI self-convergence under Mode B; owner final-final under Mode C.

Only after the exit condition fires does AI move to the next program.

### Mode A iteration — done 2026-05-07

Owner picked Mode A (AI-only review, the §18 default). Iteration ran
in three passes:

1. **§9.1 self-review + §9.2 critique-pass** — added 2026-05-07
   addendum to `review-internal.md`. 8 critique points raised against
   the new artifacts; written responses to each. One self-found
   correction (B.8 named the wrong top-5 ranking list — fixed in the
   same iteration).
2. **§9.3 red-team synthesis (continued)** — added 2026-05-07
   addendum to `review-external.md`. 6 candidate-institution
   objections on the new artifacts (KEMRI, HeiGIT, WB DECDG, OPHI,
   PIDS, BIDS) with written responses. §18.4 explicit non-claim
   reproduced verbatim.
3. **AI second-opinion code review** (Mode A optional step) —
   `feature-dev:code-reviewer` sub-agent in an independent session
   reviewed the new code and flagged 3 critical + 4 important issues.
   Resolved 3/3 critical and 3/4 important in the same iteration:
   - BARMM crosswalk now enforces a 0.75 winner-share floor
     (`barmm_resolver_admission_stats` records admitted/dropped/
     skipped per crosswalk load)
   - `inspect-barmm-codes.py` warnings are now scoped, not module-wide
   - `retrieved_at` reads from `versions.json` (stable across clean
     clones), not file mtime
   - `build-choropleth.py` now fails loudly on unjoined polygons
     (`_check_join_or_fail`) instead of producing all-grey maps
   - `build-slides.mjs` now uses `execFileSync` with argv (no shell
     interpolation)
   - `build-review-packet.mjs` now exits non-zero if `versions.json`
     missing
   - exposure_proxy=0 collapse documented inline
4. **`limitations.md` §7 added** — 6 new unresolved-residue items
   carried over from the addendum (8-record BARMM residue, regex
   pattern set, simplification tolerances, PSA workbook re-host,
   caveat-loss across tiers, BGD ADM1 N=8).

Exit condition: AI cannot find a further substantive critique on the
listed artifacts. PSDQ is **ai-first finished for current issue**
under Mode A. The artifact remains upgrade-eligible to human-final
via §18.5 (owner-only steps: line-by-line paper reading, real
reviewer contact, owner-signed commit).

The 2026-05-07 review packet at
`review-packets/public-service-data-quality-2026-05-07/` (and `.zip`,
6.1 MB) reflects this state. The reviewer who receives this packet
sees both the 2026-04-25 reviews and the 2026-05-07 Mode A addenda
in `review-internal.md` and `review-external.md`.

## Current blockers

- **10 ADM3 rows still without a source match** in the Philippines poverty
  overlay: Special Geographic Area rows, City of San Juan, Palawan Kalayaan.
  Kept explicit and non-imputed.
- **257 unresolved Philippines NHFR records** after direct-code + PSA PSGC
  correspondence resolution. Below human-final threshold; needs targeted
  source review before any human-final claim.
- **Human-final maturity** is owner-only per §18.5: line-by-line paper
  reading, external reviewer contact (Macharia / Zipf / PIDS / BIDS),
  internal review with Arturo, owner-signed commit. Cannot be reached
  through AI-only review (Mode A).
- **India and Indonesia extensions** are scope-gated until a public
  facility-registry path exists (India) or owner-provisioned SATUSEHAT
  access exists (Indonesia).

## Handoff prompt

Use this to continue a fresh session focused on PSDQ:

```text
Read research/STATUS.md and public-service-data-quality/STATUS.md, plus
CLAUDE.md and research/factory.md. PSDQ is the active flagship. Continue
the publication-ladder build and the review-loop steps listed in
public-service-data-quality/STATUS.md. State the chosen review mode
before iterating; default is Mode A under §18 ACTIVE.
```
