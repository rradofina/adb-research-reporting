---
name: visual-first-refactor
description: Hero-visual contract that makes every program's headline finding visually legible at thumbnail size, and turns the home page into a YouTube-style gallery of evidence.
attestation_chain: ai-first
status: active (introduced 2026-05-19)
constitution_refs:
  - "§6.4 composite indices are triage only, never headline"
  - "§13.3 measurement-gap framing"
  - "§14 banned words"
  - "§18.2 honest labeling"
  - "factory.md visualization rule (per-program, not pre-built)"
---

# Visual-first refactor — the hero-visual contract

## Principle

The reader's first contact with a research result should be a single
image that already conveys the finding. Text-led summaries make every
program look like every other program because the visual surface is the
governance dossier, not the evidence. Visual-led summaries force each
program to answer the harder question — *what is the single image that
tells this story?* — which is the same question §6.4 already requires
us to answer with words ("never headline a composite index"), just
posed in pixels.

A research program is therefore not finished for the current issue
until it ships a **hero visual**: one 1600×900 image (PNG + SVG) whose
content is the headline finding, whose caption is composite-free, and
whose attestation chain is overlaid on the artifact itself so a viewer
cannot screenshot it onto a slide without also screenshotting the
labeling.

This document is the contract that operationalizes that principle. It
extends the existing factory.md visualization rule; it does not
replace it.

## What changes for the reader

| Surface | Before | After |
|---|---|---|
| Home page (`/`) | Text-card list grouped by maturity | 16:9 thumbnail grid; click goes to the topic page |
| Topic page (`/{slug}`) | Tabs above article body | Hero visual + 1-line caption above tabs; tabs unchanged |
| Article hero | Inline charts only | Same hero visual reused as the article's opening figure |
| Manifest | No hero entry | `hero: { png, svg, caption_json, attestation_chain }` |

Every other surface — Evidence packet, Data tab, governance docs — is
unchanged. The refactor is additive at the reader-facing surface and
adds one (1) new pipeline step per program (`build-thumbnail.py`).

## The hero-visual contract

A hero visual is the **single image a program is willing to be judged on**.
Every program produces exactly one. The contract is:

| Field | Requirement |
|---|---|
| Dimensions | 1600 × 900 px (16:9), readable when downscaled to 320 × 180 px |
| Formats | Both PNG (lossless, ≤ 500 KB) and SVG (text/vector, no embedded raster) |
| Type | Map, choropleth, chord/sankey, country-cards, small-multiples, ranked-bar — **never** a composite-index ranking |
| Colormap | Perceptual-uniform (`viridis_r` default). No green/red diverging without justification documented in the script. |
| Headline number | One. Large. Composite-free. Traceable to a committed CSV cell. |
| Caption | ≤ 90 chars. No §14 banned words. DMC framing per §13.3. |
| Attribution | Footer line with source + retrieval date + attestation chain. Burned into the image, not just the page caption. |
| Sidecar | `{slug}-thumbnail.json` with `title`, `caption`, `headline_number`, `source`, `attestation_chain: ai-first`, `script`, `inputs[]` (CSV/JSON files the script read), `generated_at`. |
| Script | `{program}/scripts/build-thumbnail.py`, idempotent, reads only committed `generated/*.csv|json`. No new fetches. |

The script is allowed to use the shared `scripts/thumbnail_lib.py`
helper (figure setup, attestation footer, Asia-Pacific map base,
TopoJSON loader) — but the script itself must be checked in, must read
only committed inputs, and must produce identical output on rerun
(verified by sha256 in `manifest.json`).

**What a hero visual is NOT:**

- A composite-index ranking. §6.4 forbids it. If the program's current
  headline is "TKM 79.4 composite", the hero visual must instead show
  the underlying single-axis number (TKM 1,868% freshwater withdrawal).
- A summary table of every result. Tables go in the Data tab.
- A teaser. The hero IS the finding, not a hook to a finding.
- AI-decorative. No stock-photo overlays, no abstract metaphor art, no
  "data visualization" clip-art. Honest geometry only.

## Per-program visual-form catalog (initial set)

| Program | Headline finding | Hero visual form | Headline number on the image |
|---|---|---|---|
| `public-service-data-quality` | OSM vs gov-registry health-facility gap | Two-up micro-choropleth (PHL, BGD) | "17.1% PHL · 11.8% BGD clinical-tier match" |
| `remittance-resilience` | Five fragile remittance corridors | Asia-Pacific map; top-5 enlarged | "70.3% of Kyrgyz GDP comes from remittances" |
| `migration-displacement-signals` | Six corridors carry 56M emigrants | Chord diagram (7 origins × 10 destinations) | "18.5M from India · 11.7M from China" |
| `disaster-recovery-lag` | CHN, IND carry the burden | Small-multiples of EM-DAT event timelines | "CHN 25.6 events/yr · 1.77B affected" |
| `water-stress-crop-diversification` | Inherited set matches the raw top four in 2/7 runs; direct crop HHI retains 0/4 | Construct-validation finding card with stated-rule, water, and crop gates | "The stable top four does not survive its own constructs" |
| `grid-reliability-heat` | Single-fuel grids | Stacked bar per country (top 6) | "Bhutan 100% hydro · Brunei 100% gas" |
| `climate-health-workdays` | Outdoor-labor × PM2.5 exposure | Scatter with country dots sized by exposed population | "IND 798.6M outdoor workers in above-WHO-guideline PM2.5" |
| `port-hinterland-friction` | Top-5 trade-volume cluster | Bar with LPI × imports product | "CHN, IND carry 60% of regional import-friction exposure" |
| `social-protection-shock-coverage` | Readiness gap (poverty − SP − accounts) | Diverging bar per country | "PAK: 23% poverty, 22% SP, 21% accounts" |
| `school-heat-disruption` | Top-1 narrowing (KHM only) | Single-country card with timeline | "Cambodia: 5.3M children, PTR 41.7, tasmax 31.9°C" |
| `food-price-climate-transmission` | LAO + PAK persistent high | Two-axis scatter | "Lao PDR and Pakistan: high CPI × high ag-import exposure for N=3..10" |
| `flood-market-access` | Top-4 stable | EM-DAT flood-event map | "India, China, Indonesia, Afghanistan: stable top-4" |
| `coastal-informal-risk` | Top-5 coastal population | Coastline-zoomed dot map | "PAK, PHL, CHN, BGD, MMR: stable top-5" |
| `air-monitoring` | 14.3M people in above-guideline economies with no PM2.5 monitor | OpenAQ station-density choropleth | "14.3M people · 7 economies · 0 public PM2.5 monitors" |
| `invisible-urbanization` | Urban growth from rural base | Slope chart top-5 | "Papua New Guinea, Solomon Islands, Afghanistan, Lao PDR, Bangladesh" |
| `access-services` | 8-DMC climate-adjusted access pilot | Choropleth (the 104 ADM1 units) | "104 ADM1 units · 8 DMCs · climate-adjusted access" |
| `digital-performance` | (no committed data yet) | Placeholder card, honestly labeled | — |
| `mpi-nighttime-lights` | (owner-led, Stage H) | Placeholder card, honestly labeled | — |

The visual form for each program is a starting proposal; the build
script is the final word. If a chord diagram proves too noisy at
thumbnail size, the script falls back to a stacked bar — the contract
requires *a* hero visual, not a specific one.

## How honest labeling is preserved

§18.2 requires every artifact to surface its attestation chain. For the
hero visual that means:

1. **In the image.** The footer line burns "ai-first under
   CONSTITUTION.md §18" into both PNG and SVG. A screenshot of the
   thumbnail without context still carries the label.
2. **In the sidecar.** `{slug}-thumbnail.json` carries
   `attestation_chain: "ai-first"`.
3. **In the manifest.** `manifest.json` exposes the hero block; the
   manifest's own `attestation_chain` field is set per existing rules.
4. **On the home page.** Every thumbnail card overlays a small
   `ai-first` chip in the same style as the maturity chip. Cards for
   programs without a hero render an honest placeholder ("hero pending
   — Stage 1 framing in progress") rather than a fake image.

This means the home page itself becomes a §18.2 instrument: the visual
gallery cannot pretend a program is finished when it is not, because the
placeholder cards look like placeholders.

## Composite-demotion editorial pass

The refactor forces a one-time editorial pass on every program's
public-facing summary. The rule: each summary in `programs.ts` and the
manifest must lead with a single visceral non-composite number, not an
index score. This is a §6.4 honesty correction the visual-first
refactor surfaces; it is not a new rule.

Example demotions (illustrative — exact wording per script):

| Before (composite-led) | After (non-composite-led) |
|---|---|
| "Top index: TKM 79.4, PAK 75.3, AZE 54.4" | "The published set is the raw top four in 2 of 7 saved runs" |
| "AFG 55.7 (26M exposed); IND 53.1 (798.6M exposed)" | "798.6M outdoor workers in India breathe above-WHO-guideline PM2.5" |
| "Top friction exposure: CHN (1.45), IND (0.94)" | "CHN and IND account for 60% of regional import-friction exposure" |

Composite indices remain in `results.md` as triage tools (§6.4
permitted use). They are removed from the public summary because the
public summary is a headline, and §6.4 forbids composite headlines.

## What this does NOT do

- **Does not change the pipeline.** Existing fetch/process/sensitivity
  scripts are untouched. The hero visual reads only committed
  `generated/*.csv|json`. The contract adds exactly one new script per
  program (`build-thumbnail.py`).
- **Does not introduce JS chart libraries at runtime.** Heroes are
  static SVG+PNG. The React site renders them with `<img>` and `<picture>`
  tags. No d3, no recharts, no recompile cost.
- **Does not unlock private data.** §2.1 still holds.
- **Does not weaken the audit trail.** Hero scripts go through the same
  five gates as all other research artifacts.
- **Does not retire the existing per-program React pages.** The Topic
  tabs continue to render `paper`, `brief`, `blog`, `slides`, `data`,
  `evidence` exactly as today.

## Rollout sequencing

1. **Spec.** This document. (Done with this commit.)
2. **Shared helper.** `scripts/thumbnail_lib.py` — single matplotlib
   helper module reused across all 16 hero scripts.
3. **`opensrc/` reference folder.** Vetted open-source visualization
   sources (d3-chord geometry, world-atlas TopoJSON, matplotlib
   gallery pointers, pycirclize). Permits AI to consult patterns
   offline without re-deriving every visual primitive.
4. **Pilot heroes** (in this order, by data-readiness):
   1. `public-service-data-quality` — choropleths already exist.
   2. `remittance-resilience` — current active flagship.
   3. `migration-displacement-signals` — chord diagram pilot.
5. **Home page rewrite + topic hero header.** The visible artifact.
6. **Sweep the remaining 14 programs.** One thumbnail script each.
   Skip `digital-performance` (no committed data) and
   `mpi-nighttime-lights` (owner-led, Arturo co-authored).
7. **Composite-demotion editorial pass** on `programs.ts` and manifests.
8. **Verification.** Sync evidence + references, all 5 gates,
   `npm run build`, browser-check 1280px + 375px, STATUS.md update.

## Verification gate

The five gates apply per usual. In addition, the visual-first refactor
introduces one new check that runs locally during the
end-of-task hygiene pass (it is not a separate gate script yet — added
to the verification suite once stable):

> Every program at PR or PP must have a `hero` block in its
> `manifest.json` with both PNG and SVG present, sha256-matched to the
> on-disk file. If the hero is missing, the home-page card renders a
> placeholder (honest labeling §18.2).

Programs at H, SR, or Ret may render placeholder cards without penalty.

## Why this is allowed under §18

§18 ACTIVE permits AI to: build visualizations from committed scripts,
write the spec doc, run the build pipeline, render the artifacts,
update the React site, run the gates, and commit. None of the
non-suspendable rules are touched:

- No empirical numbers from AI memory (every headline number reads
  from a CSV cell traced to a committed fetch script).
- ±50% sensitivity still applies to the underlying claims, not to the
  pixels.
- Permanent-archive minting unchanged (`/program/{slug}/evidence` +
  `/archives/{slug}-{date}.zip`).
- Public data only.
- DMC framing (§13.3) and banned words (§14) gated.
- Honest labeling (§18.2) is the *core* of this refactor.

Zenodo deposition remains owner-only. So does §18.5 owner-led
human-final.

## Amendment

This document follows the same amendment procedure as the rest of the
factory (`CONSTITUTION.md` §16). The owner reverts the visual-first
refactor by deleting `scripts/thumbnail_lib.py` and reverting
`Home.tsx` to the text-card list; the `build-thumbnail.py` scripts
remain (they are honest pipeline artifacts) but become unused.
