# Design — how findings are presented

This file governs the reporting site and every public surface. It has the
same standing as `research/factory.md`: AI assistants follow it without
being asked. Language rules live in `research/style-guide.md`; this file
covers structure, layout, and visual presentation.

## The principle

A page exists for a reader with ninety seconds, and it must reward them in
the first viewport: **what was found, why it can be believed, and what it
cannot say.** Everything else — audit trails, methodology, gates, custody
records — is drill-down. The current failure mode is the inverse: pages
that open with process and stack dozens of audit sections a reader must
scroll past to find out whether anything was learned. Auditability is a
property of the *repository*; the *page* is for reading. A page that proves
everything and communicates nothing has failed at its job.

## Reader-first test

Before editing a public page, write the answer to four questions in the work
notes or the program board:

1. **What should the reader remember?** One sentence, with place, unit, and
   maturity label.
2. **What visual proves or challenges that sentence?** One chart, map,
   matrix, or source-disagreement view.
3. **What should make the reader cautious?** Two limits visible before the
   evidence ledger.
4. **Where can an auditor verify it?** One route to scripts, generated files,
   sources, and retrieval records.

If a page cannot answer these, the next move is not polish. It is claim
reshaping, evidence work, or rotation.

## Page anatomy (program and showcase pages)

Every program or showcase page follows this order. Sections 1–4 must fit
in roughly two viewports on desktop.

1. **Finding.** One sentence, with a number and a place, plus the maturity
   label and `attestation_chain` shown plainly. If the honest finding is
   an absence ("no economy in the sample publishes X"), lead with that —
   it is a finding, not an apology.
2. **Hero visual.** The one chart, map, or matrix that carries the
   argument (see `research/JUDGMENT.md` §6). Annotated, sourced on the
   figure, readable at 375 px.
3. **How we know.** The method in three to five plain-language sentences:
   sources, unit, the key transformation, the sensitivity result.
4. **What this does not say.** The two or three limitations a critical
   reader would raise first, stated before they raise them.
5. **Evidence ledger.** *One* compact table indexing every audit, scan,
   wall, and gate artifact: name, date, what it checked, what it found
   (one line), link to the generated artifact. Collapsible detail is
   fine; sequential full-width wall sections are not (see below).
6. **Reproduce.** Commands, manifest link, archive link, retrieval dates.

## The wall-consolidation rule

Audit/scan/gate artifacts **never render as stacked page sections.** They
render as rows in the evidence ledger, driven by a generated JSON index —
not hand-written JSX. One row per artifact; the row's "what it found"
column must state the substantive outcome ("all 22 stations report BAM
method text; no calibration certificates found"), not the artifact's
existence ("scan completed; 8 sources retrieved").

Consequences, effective immediately:

- `ShowcaseAirMonitoring.tsx` (≈16,900 lines of stacked walls) is the
  canonical violation and is the first refactor target: reduce to the
  six-part anatomy above with a data-driven ledger. `ShowcasePSDQ.tsx`
  (≈7,900 lines) is second.
- New walls added to any page as sections are a design regression even if
  the underlying research artifact is sound.
- Page-size guideline: a view component past ~800 lines is a signal that
  content belongs in generated data, the evidence packet, or a
  sub-route — not further prose in TSX.

## One page, one point

- **Home** leads with findings — the three to five strongest, each as a
  one-sentence claim with its hero visual and maturity label. Process,
  governance, and constitution pages remain available but subordinate in
  the navigation. A research lab's front door shows research.
- **Program page** makes one finding legible (anatomy above).
- **Showcase page** makes one measurement problem visible. It is a
  narrative surface, not a second evidence dump; it links to the program
  page for depth.
- **Evidence page** is for the auditor: full packet, manifest, checksums.
  This is the only page allowed to be exhaustive, and even it should be
  a structured index, not prose.
- **Navigation** serves two readers explicitly: the *reader path*
  (Findings → Program → Article) and the *auditor path* (Program →
  Evidence → Repo). Neither path should have to wade through the other's
  material.

## Visual system

- **Figure spine, not figure quota.** The working paper follows
  `research/VISUAL-RESEARCH-STANDARD.md`: one hero plus every distinct
  coverage, heterogeneity, sensitivity, uncertainty, falsification, or
  limitation figure the evidence earns. Shallow surfaces reuse the hero;
  the canonical article carries the full empirical sequence.
- **One system, everywhere.** All charts go through the shared components
  (`ChartFrame`, `RankedBar`, `Scatter`, `ChoroplethMap`, …). A new chart
  form is added to the shared set with consistent typography, spacing,
  and palette — never improvised inline per page.
- **Annotation over legend.** Label the point that matters on the figure.
  The reader should get the argument from the chart before the caption.
- **Restraint.** One accent color for the finding, muted context for
  everything else. Tables get typographic hierarchy, not zebra-stripe
  decoration. Empty states ("no evidence found") are designed states,
  not blank cells — in a measurement-gap lab, absence is often the
  hero and deserves deliberate visual treatment (hatched regions,
  explicit "no public record" marks).
- **Honesty in form.** Maturity labels and `attestation_chain` are part
  of the visual hierarchy near the headline — not footer fine print, and
  not styled as warnings to be dismissed. Triage metrics are visually
  distinguished from headline metrics.
- **Every surface passes the existing QA bar** (CLAUDE.md hygiene):
  1280 px and 375 px checks, zero console errors, zero horizontal
  overflow, readable chart labels at mobile widths.

## Data-to-visual contract

Every hero visual has a contract before it lands on a public page:

- **Source.** The exact generated CSV or JSON that feeds it.
- **Transform.** The script or component logic that turns source rows into
  marks, colors, bins, and annotations.
- **Claim role.** Whether the visual supports the headline, shows a limit,
  displays sensitivity, or indexes source disagreement.
- **Mobile proof.** A 375 px screenshot where labels, marks, caveats, and
  controls are legible without horizontal scrolling.
- **Fallback.** A plain table or text summary for readers who cannot use the
  interactive view.

Decorative media, generic cards, and map panels without a claim role do not
count. A visual that does not help the reader decide what the evidence means
is removed or moved to a drill-down page.

## Design review checklist

Run this checklist before closing any public-surface session:

- First viewport states the finding, maturity label, and `attestation_chain`.
- Hero visual is visible without scrolling on desktop and quickly visible on
  mobile.
- Caveats appear before the reader reaches the ledger.
- The evidence ledger is data-driven, not hand-written page sections.
- Tables have stable widths and wrap long labels at 375 px.
- Interactive controls expose evidence or sensitivity; they are not decoration.
- Page source stays small enough to review. A component over about 800 lines
  needs a data extraction, a shared component, or a sub-route.

## Standing design backlog (first targets)

1. **Done 2026-07-07:** Refactor `ShowcaseAirMonitoring.tsx` to the
   six-part anatomy with a generated evidence-ledger index; the ~65 wall
   artifacts become ledger rows.
2. **Done 2026-07-07:** Apply the same refactor to `ShowcasePSDQ.tsx`; the
   route now reads `psdq-evidence-ledger.{json,csv}` and treats the 28
   source-disagreement artifacts as ledger rows.
3. **Done 2026-07-07:** Reworked `Home.tsx` to lead with five ranked
   findings (claim + hero visual + label), with process/reviewer links
   demoted below the first viewport and verified at 1280 px and 375 px.
4. **Done 2026-07-07:** Added `reporting-site/src/components/EvidenceLedger.tsx`
   and updated the air-monitoring and PSDQ ledger builders to emit standard
   `{program}/generated/evidence-ledger.{json,csv}` aliases. Both showcase
   routes now use the shared component for group cards, filtering, file links,
   and responsive ledger tables.
5. **Done 2026-07-07:** Audited the active program route. All
   `/program/{slug}` and `/program/{slug}/evidence` links redirect to the
   generic `Topic.tsx` surface; 16 of 18 topics have paper + hero +
   evidence surfaces, `mpi-nighttime-lights` has evidence but no paper/hero,
   and `digital-performance` has only the register summary. Fixed the
   shared topic shell so a topic opens to the best available surface
   (paper, then evidence, then overview) instead of an empty Paper tab.
   Remaining per-topic deviations are now presentation moves, not route
   bugs.
6. **Done 2026-07-07:** Added a shared current-issue closure contract
   (`reporting-site/src/data/issueClosure.ts`) and used it on Home,
   Research, and Briefs. The public issue now classifies all 18 topics
   consistently: 7 finished, 8 screening-only, 1 prospectus, 1 prepared
   pipeline, and 1 hypothesis. Articles and reader-guide copy were
   reconciled to the same labels without promoting any program through
   the constitutional WIP register. Browser QA also exposed the old
   `/research`, `/briefs`, `/how-to-read`, `/glossary`, `/archive`,
   `/data/upgrades`, `/methods`, and `/references` redirects; those
   existing views are now real App Router pages.
