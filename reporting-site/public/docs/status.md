# Current research status — operating board

**Principle.** This file is the **board, not the file**. Its job is to point
to the active flagship and to define how a session opens, runs, and closes.
Per-program detail — last completed, next focused work, current blockers,
program-specific runbooks — lives in `{program}/STATUS.md` or in the
program's `README.md`. If you find PSDQ-specific narrative here, move it.

Last updated: 2026-05-29.

## Current focus

| Field | Value |
|---|---|
| Active flagship | `remittance-resilience` (PP; **ai-first finished for current issue** as of 2026-05-12 under Mode A; corridor-concentration cluster) |
| Per-program board | [`remittance-resilience/STATUS.md`](../remittance-resilience/STATUS.md) |
| Operating mode | §18 ACTIVE (AI-First) |
| Default review mode | Mode A (AI-only); see `research/factory.md` |
| Previous flagship | `public-service-data-quality` (PR, ai-first finished 2026-05-07; polish-pass viewport-verified 2026-05-12; available for §18.5 owner-led human-final upgrade) |

The active flagship is the only program that may be advanced this session.
Rotation reason recorded in the operational notes below. Programs in the
queue are listed in `research/wip-register.md` and `CONSTITUTION.md` §15.
Do not silently switch programs; rotation requires recording the reason
here before switching.

## Next-up queue

Ordering by Mode-A readiness (cheapest path to "ai-first finished for
current issue" under the publication ladder + review loop). The owner
overrides priority by editing this list.

1. **`remittance-resilience`** — *current active flagship; ai-first
   finished for current issue 2026-05-12*. Top-5 corridor cluster
   {KGZ, NPL, TON, VUT, WSM} stable across ±50% sensitivity. Full
   publication ladder (tiers 1–7) shipped under Mode A in this
   session, with 5 honesty corrections caught and applied. Available
   for §18.5 owner-led human-final upgrade. The next session may
   either polish/upgrade remittance-resilience further, or rotate to
   #2 in this queue.
2. **`access-services`** — 8-DMC climate-adjusted access pilot done;
   top-4 narrowing {BGD, KHM, LAO, PAK} stable. Travel-time isochrones
   are §18.5 owner-gated, so AI-doable depth is bounded — clean Mode A
   finish.
3. **`migration-displacement-signals`** — top-5 emigrant-stock cluster
   {IND, CHN, BGD, AFG, PHL} stable across alternative definitions;
   article exists at
   `articles/emigrant-stock-corridor-concentration.md`; same gap as
   remittance-resilience.
4. **`climate-health-workdays`** — top-3 set {AFG, IND, BGD} stable; PM
   2.5-cap sensitivity flagged top-5 → top-3 honest narrowing.
5. **`disaster-recovery-lag`** — top-2 set {CHN, IND} stable across
   events/affected/damage burden metrics.
6. **`grid-reliability-heat`** — top-5 single-fuel set {BTN, BRN, MNG,
   NPL, TJK} stable.
7. **`port-hinterland-friction`** — top-5 trade-volume cluster {CHN,
   IND, IDN, THA, VNM} stable.
8. **`social-protection-shock-coverage`** — top-5 {BGD, LAO, MMR, PAK,
   PHL} stable.
9. **`water-stress-crop-diversification`** — top-4 narrowing {AFG, AZE,
   PAK, TKM}; UZB perturbation-sensitive — narrower headline.
10. **`school-heat-disruption`** — honest narrowing to top-1 (KHM only);
    top-5 fails ±50% gate. Smallest-claim flagship candidate.
11. **`food-price-climate-transmission`** — sensitivity-gate failure on
    composite; index needs reformulation before ladder build.
12. **`flood-market-access`** — top-4 {AFG, CHN, IDN, IND} stable; GLOFAS
    modeled-extent is §18.5 owner-gated.
13. **`air-monitoring`** — ground-station coverage vs satellite AOD;
    pipeline ready.
14. **`invisible-urbanization`** — settlement growth vs admin urban
    boundaries; pipeline ready.
15. **`coastal-informal-risk`** — informal coastal settlements vs
    storm-surge exposure; pipeline ready.
16. **`digital-performance`** — broadband coverage vs official
    connectivity claims; folder mostly empty (Stage 1 framing needed).
17. **`mpi-nighttime-lights`** — Program 0, co-authored with Arturo; H
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
