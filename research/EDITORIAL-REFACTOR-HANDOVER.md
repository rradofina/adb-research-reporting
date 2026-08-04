# Editorial refactor handover — the Development Asia reader arc

Date: 2026-07-31. Author of this handover: AI session under §18 ACTIVE,
at the owner's direction. Intended reader: **the AI model executing the
remainder of this refactor.** Owner: Raymond Adofina.

---

## 0. Read this first

The owner reviewed the public reporting surface and rejected it — not
the visual design (that is explicitly deferred), but the **flow of the
writeups**. The standard the owner named is **Development Asia**
(https://development.asia), ADB's knowledge platform. Its articles open
with a standfirst a busy practitioner can retell, move through
story-led sections in plain language, land a practitioner "so what",
and end with resources. Our research writeups opened with the
apparatus — ledger schemas, stage rules, process headings, recited
zeros — and read like compliance reports.

The owner's instruction for this engagement, verbatim in spirit:
**refactor everything, in detail, no exceptions, no shortcuts.**

That means:

- Every reader-tier writeup in the repository is restructured to the
  reader arc (spec below). Not only the ones that are easy.
- Every rewrite preserves the evidence exactly (constitutional floor,
  §2 of this document). Editorial flow changes; claims never do.
- Every rewrite is verified with the deterministic gates and the
  production build before it counts as done. Reporting a file as done
  without its checks run is a defect, not a saving.
- If a step is ambiguous, resolve it by the principle in the governing
  docs — do not silently skip it and do not invent a lighter version.

Before doing anything, read the governing stack in this order:
`CLAUDE.md` → `research/JUDGMENT.md` → `research/DESIGN.md` →
`research/factory.md` → `CONSTITUTION.md` → `research/STATUS.md` and
the active program board. Then read `research/style-guide.md` §7 — the
binding spec this refactor implements — and this file end to end.

---

## 1. The binding spec — the reader arc

`research/style-guide.md` §7 ("Article flow — the reader arc", added
2026-07-31) is the normative text. Summary for convenience — the
style-guide wording wins on any conflict:

**The arc (section order for every reader-tier body):**

1. **Standfirst.** The frontmatter `subtitle` is one or two sentences
   a reader can retell: what was found, where, why it matters. Never a
   methods note. (The site renders `subtitle` under the title — it IS
   the standfirst.)
2. **Open in the reader's world.** First section = a concrete question,
   place, and stake a practitioner actually has. Never the apparatus
   ("the audited packet", "the ledger verifies", "the primary research
   object is …").
3. **What we found.** Numbers inside sentences that interpret them.
4. **Why it happens / a close-up.** One named example, gradient, or
   mechanism that makes the pattern tangible.
5. **What this means for the reader.** The practitioner "so what".
6. **What this does not say.** All limitations preserved, written as
   reader guidance, before the close.
7. **What would change this finding.** The named public evidence that
   would narrow or overturn it.
8. **How we measured this.** 3–5 plain sentences + reproduce commands +
   evidence-page link. Stage rules, retrieval states, and ledger
   schemas live on the evidence page, not in the body.

**Sentence-level rules:**

- Headings carry the argument — a reader who reads only the headings
  gets the story. Process labels ("Methodology and claim test", "Data
  and coverage", "Results") are forbidden on the reader tier.
- One idea per section; paragraphs of 2–4 sentences.
- Coined internal terms ("claim-permission ladder", "nonclaim
  geometry", "monitor-grade closure", "wall", "gate" as jargon) never
  reach the reader tier without a plain rendering first; by default
  keep them off entirely.
- Every number appears in a sentence that says what it means.
  "0 same-station joins" is a recitation; "not one station could be
  publicly confirmed as the same physical monitor in both sources" is
  a finding.
- The honesty machinery (maturity label, `attestation_chain`,
  nonclaims, §18.4 blocks) is untouched in substance. The arc changes
  how the body reads, never what it claims.

---

## 2. The constitutional floor — what a rewrite may NEVER change

These are absolute. A rewrite that violates any of them is reverted,
not patched.

1. **Every empirical number is byte-identical.** No recomputation, no
   re-rounding, no "about", no "roughly" applied to a precise figure
   (introducing a word like "about" before an exact committed number
   changes the claim — do not). Numbers trace to committed scripts;
   AI never originates or alters one (§2.1, preserved set).
2. **Every figure survives** with its exact path and its alt text
   either identical or improved-without-new-claims. Figures may move
   between sections; none may be dropped or added.
3. **Citations by BibTeX key only** (§5.3). Every `[@key]` in the old
   body appears in the new body. If the article ends with a "keys
   cited above" list, that list must match the body exactly — do not
   list a key the body no longer cites (this defect actually occurred
   once in this session and was fixed; check for it every time).
4. **Frontmatter:** only `title`, `subtitle`, and `updated_at` may
   change. `slug` NEVER changes (it is the URL). `abstract` may be
   lightly clarified but every number in it must survive verbatim;
   when in doubt, leave the abstract alone. All other keys —
   `maturity`, `status`, `attestation_chain`, `constitution_ref`,
   `references`, `program`, `kind`, `tier`, checks — untouched.
5. **§18 honesty blocks stay.** The attestation-chain section, the
   §18.4 "no individual reviewer was contacted" blockquote (verbatim),
   the closing `attestation_chain: ai-first` line, and any
   human-final-upgrade description are preserved. They may be
   repositioned toward the end; they may be compressed only if no
   fact, institution name, or non-claim is lost.
6. **Every limitation / nonclaim survives.** Count the limitation
   bullets before rewriting; count them after. Equal or greater
   (merging two bullets that state the same fact is allowed if both
   facts remain explicit).
7. **§14 banned words:** never introduce a word on the §14 list (see
   `research/style-guide.md` §1). The gate will catch it; do not rely
   on the gate — just do not write them.
8. **§13.3 DMC framing:** findings stay framed as measurement /
   coverage / observability gaps. Never "country X has poor data",
   never a country-performance reading, never a ranking headline.
9. **§6.4 composite discipline:** composite/triage scores never move
   into a headline or standfirst during a rewrite.
10. **Maturity labels and program claims:** a rewrite is a
    presentation pass. It never promotes, demotes, reopens, or
    reshapes a claim. If while rewriting you believe a claim is wrong,
    STOP on that file and flag it to the owner — do not fix it inside
    an editorial pass.

---

## 3. Worked example (already merged — study it)

`articles/pm25-observability-gap-cluster.md` is the reference
implementation. Compare it against git history (`git log -p -1 --
articles/pm25-observability-gap-cluster.md` shows the restructure).

Heading transformation that defines the register:

| Before (process voice) | After (story voice) |
|---|---|
| The finding | The question a dashboard cannot answer |
| Background and research problem | What we checked |
| Data and coverage / Methodology and claim test | What we found: the chain never closes |
| Results | Indonesia shows the pattern up close |
| Sensitivity and robustness | What this means for anyone using station counts |
| Limitations and nonclaims | What this does not say |
| Conclusion and use | What would change this finding |
| Reproduce and inspect | How we measured this |

Sentence transformation that defines the voice:

- Before: "The primary research object is
  `generated/evidence-ledger.json`, built from 64 committed
  public-source summaries."
- After: "The audit consolidates 64 committed public-source summaries
  across a 24-economy discovery frame." (Same fact, reader subject.)

- Before: "It verifies 0 same-station rows, 0 complete monitor-grade
  rows…"
- After: "Not one station completes the chain. The packet verifies
  **zero** same-station confirmations, **zero** complete monitor-grade
  rows…" (Same numbers, interpreted.)

Three more completed references, each preserving a different kind of
governance apparatus:

- `articles/measurement-gap-philippines-bangladesh.md` — heavy
  attestation/acknowledgment machinery retained at the end.
- `articles/remittance-corridors-vulnerability-cluster.md` — a
  set-not-rank result with an internal-audit correction kept on the
  record.
- `articles/food-price-joint-qualifier.md` — a null-ish result with
  retired methods narrated as story ("Two inherited shortcuts,
  retired").

---

## 4. The per-file procedure (run it exactly, every file)

1. **Read the entire file.** No skimming, no rewriting from the title.
2. **Build the inventory before writing** (in your working notes):
   - every numeral with its unit and context;
   - every figure path + alt text;
   - every `[@citation]` key;
   - every limitation/nonclaim bullet;
   - every governance block (§18.4 quote, attestation section,
     closing attestation line);
   - the reproduce commands.
3. **Map old sections → arc sections.** Every old paragraph must have
   a destination (a new section, merged into another, or moved to
   "How we measured this"). Nothing silently disappears.
4. **Rewrite with the Write tool** (full-file replacement). Target
   length: within ±25% of the original body. Shorter is fine only if
   the inventory still checks out.
5. **Set `updated_at`** to today's date. Touch nothing else in
   frontmatter except `title`/`subtitle` per §2.4 above.
6. **Run the number audit** (section 5). Fix any mismatch before
   moving on.
7. **Verify citation parity**: every inventoried key present; any
   trailing "keys cited above" list matches the body.
8. **Batch checkpoint** (after every 3–5 files, and always at session
   end): run the five gates + `node scripts/sync-articles.mjs` +
   `cd reporting-site && npm run build`. All must pass.
9. **Update the tracker** in section 8 of this file (edit this file in
   place — flip the file's row to `done` with the date).
10. **Update the program board** (`{program}/STATUS.md`): one entry —
    "editorial pass to the reader arc; no number, figure, citation,
    claim, or maturity change; gates and build re-passed" — and bump
    `Last updated`. Programs without a board (`program: meta`) log
    nothing per-file; the tracker here is their record.

## 5. The number audit (mandatory, per file)

From the repo root, compare the numeral multiset of the committed
version against the working copy:

```powershell
$old = (git show "HEAD:articles/<file>.md") -join "`n"
$new = Get-Content "articles/<file>.md" -Raw
$rx  = '\d+(?:[.,]\d+)*'
$a = [regex]::Matches($old, $rx) | ForEach-Object Value | Group-Object | Sort-Object Name
$b = [regex]::Matches($new, $rx) | ForEach-Object Value | Group-Object | Sort-Object Name
Compare-Object $a $b -Property Name, Count
```

Empty output = numeral-safe. Non-empty output must be explainable
line-by-line by **dates and section numbers only** (e.g., `updated_at`
change, a §-reference added, a figure moved so its alt text order
changed). Any unexplained numeral difference is a violation: fix it.
Do not rationalize a missing number as "it was redundant" — redundant
numbers are removed only if the same value still appears at least once
with the same meaning.

---

## 6. Scope — EVERYTHING, phase by phase

Never edit `reporting-site/public/**` or `reporting-site/dist/**`
directly: both are generated. Edit sources, then sync
(`node scripts/sync-articles.mjs`; for program-folder files
`node scripts/sync-evidence.mjs` and `node scripts/sync-references.mjs`).

### Phase 1 — top-level working papers (`articles/*.md`, kind: working-paper)

The core of the engagement. 17 files; 4 done this session.

### Phase 2 — meta findings pieces (`articles/*.md`, program: meta)

`joint-vulnerability-cluster.md`, `per-capita-shifts-the-cluster.md`,
`the-first-issue.md`. Same arc; these are cross-program syntheses, so
"What we found" spans programs — keep each number attributed to its
source program.

### Phase 3 — the publication ladder (`articles/_brief`, `_blog`, `_social`, `_slides`, plus the four top-level `pm25-…-{brief,blog,social,deck}.md`)

Per-tier guidance:

- **Briefs** (~16 files): compressed arc — standfirst, what we found,
  what it means, what it does not say, where the evidence lives.
  600–900 words. Same floor rules.
- **Blogs** (~16 files): mostly already in the right voice (verified on
  `_blog/public-service-data-quality.md`). Do a conformance audit per
  file against §1 sentence rules; rewrite only the files that violate
  them. An audit with no change is still logged in the tracker
  ("audited, conforming").
- **Social** (~16 files): hook-first, numbers interpreted, zero coined
  jargon, no thread position wasted on process. Floor rules apply.
- **Slides** (~17 files): **CAUTION.** These feed
  `node scripts/build-slides.mjs` (PPTX builder). Before editing ANY
  `_slides` file, read `scripts/build-slides.mjs` to learn the
  structural contract (slide delimiters, expected headings, figure
  syntax). Rewrite copy *within* that contract, then rebuild the deck
  and verify the PPTX builds and the slide count matches the program
  board's recorded count. If the contract is unclear, flag before
  editing.

### Phase 4 — reader guides (`about-the-lab.md`, `reading-the-program-register.md`)

Genre is guide, not findings. Apply the sentence-level rules (reader
subject, interpreted statements, no process headings) but not the
findings arc. The test: a first-time reader knows what the lab is and
how to read a program page in ninety seconds.

### Phase 5 — program research-story surfaces (the site's `/program/{slug}` pages)

The program pages render section prose sourced from program folders
and synced into `reporting-site/public/programs/{slug}/`. For each of
the ~18 programs:

1. **Trace first.** Open the program's manifest under
   `reporting-site/public/programs/{slug}/manifest.json`, find where
   each rendered section's prose originates in the program folder
   (e.g. `results.md`, story/section files), and confirm the sync path
   (`scripts/sync-evidence.mjs`). Do not assume — trace.
2. Apply the sentence-level rules to reader-facing story sections
   (the nine-section research stories). Auditor-tier artifacts —
   evidence pages, ledgers, `pre-registration.md`, `sensitivity.md`,
   gate notes — are **out of scope**: DESIGN.md licenses the evidence
   page to be exhaustive.
3. After editing any program-folder file: re-run the program's own
   build scripts if prose files feed generated artifacts, then
   `sync-evidence` + `sync-references`, gates, build, and browser QA
   of that program page at 1280 px and 375 px (zero console errors,
   zero horizontal overflow).

### Phase 6 — site copy strings

Headings, labels, and empty-state copy in `reporting-site/src/`
(Home, Research, Briefs, Topic, Layout). Tone pass only under the same
sentence rules; no structural/layout redesign (deferred by owner).
The five gates scan site copy — run them after edits, plus the build
and browser QA.

### Explicitly OUT of scope

- Visual design (colors, typography, layout) — owner deferred ("we
  can always improve the design").
- Maturity labels, WIP register, claim shapes, pipelines, generated
  artifacts, evidence pages.
- `CONSTITUTION.md` §18 (owner-only, §16 procedure).
- Anything behind a hard wall (CLAUDE.md list): owner credentials,
  external reviewers, paywalled sources.

---

## 7. Verification protocol (non-negotiable)

- **Per batch (3–5 files) and at session end**, from the repo root:
  1. `node scripts/check-banned-words.mjs`
  2. `node scripts/check-dmc-framing.mjs`
  3. `node scripts/check-citations.mjs`
  4. `node scripts/check-composite-headline.mjs`
  5. `node scripts/check-wip.mjs`
  6. `node scripts/sync-articles.mjs`
  7. `cd reporting-site && npm run build` — must compile clean.
- **If program folders or site code were touched:** also
  `node scripts/sync-evidence.mjs`, `node scripts/sync-references.mjs`,
  and browser QA at 1280 px and 375 px on every changed public surface
  (zero console errors, zero horizontal overflow).
- **Before any production push:** from the repo root,
  `npx vercel pull --yes --environment=production` then
  `node scripts/verify-vercel-production.mjs` — must exit 0. Never
  push while this gate fails. (A plain `npm run build` does NOT
  satisfy the release gate; see CLAUDE.md production-push rule.)
- **Boards:** update each touched program's `STATUS.md` (entry format
  in §4.10). Update `research/STATUS.md` only if flagship, mode, or
  queue changes — an editorial pass does not.
- **Commits:** small batches, message pattern
  `editorial: reader-arc refactor <files> (style-guide §7); no claim change`.

**Shell gotcha (hit twice this session):** the PowerShell working
directory persists between tool calls. `node scripts/…` fails after a
`cd reporting-site`. Always prefix with the repo root or `cd` back.

**Reference-site gotcha:** development.asia currently serves a 503
maintenance page. Use the Wayback Machine
(`web.archive.org/web/2026/https://development.asia/`) to study the
model. Measured reference points from the 2026-07-25 capture, for
whenever the deferred design pass happens: accent `#E9532B`
(orange-red, article titles/links), band `#01A4CF` (cyan), body `#333`
on white, section fill `#F3F3F3`, footer `#D9D9D9`, Open Sans
headings.

---

## 8. Tracker — update this table in place, one row per file

Status values: `todo`, `in-progress`, `done <date>`,
`audited-conforming <date>`, `flagged <reason>`.

### Phase 1 — working papers

| File | Status |
|---|---|
| articles/pm25-observability-gap-cluster.md | done 2026-07-31 |
| articles/measurement-gap-philippines-bangladesh.md | done 2026-07-31 |
| articles/remittance-corridors-vulnerability-cluster.md | done 2026-07-31 |
| articles/food-price-joint-qualifier.md | done 2026-07-31 |
| articles/access-stress-pilot-cluster.md | done 2026-07-31 |
| articles/coastal-informal-cluster.md | done 2026-07-31 |
| articles/digital-availability-use-gap.md | done 2026-07-31 |
| articles/disaster-burden-cluster.md | done 2026-07-31 |
| articles/emigrant-stock-corridor-concentration.md | done 2026-07-31 |
| articles/flood-market-access-cluster.md | done 2026-07-31 |
| articles/invisible-urbanization-cluster.md | done 2026-07-31 |
| articles/port-friction-trade-volume-cluster.md | done 2026-07-31 |
| articles/public-data-freshness-two-clocks.md | done 2026-07-31 |
| articles/school-heat-honest-narrowing.md | done 2026-07-31 |
| articles/single-fuel-grid-cluster.md | done 2026-07-31 |
| articles/sp-shock-readiness-cluster.md | done 2026-07-31 |
| articles/water-crop-pressure-cluster.md | done 2026-07-31 |
| articles/workday-loss-pressure-cluster.md | done 2026-07-31 |

### Phase 2 — meta findings

| File | Status |
|---|---|
| articles/joint-vulnerability-cluster.md | done 2026-07-31 |
| articles/per-capita-shifts-the-cluster.md | done 2026-07-31 |
| articles/the-first-issue.md | done 2026-07-31 |

### Phase 3 — publication ladder

#### Briefs (compressed reader arc)

| File | Status |
|---|---|
| articles/_brief/access-services.md | done 2026-07-31 |
| articles/_brief/climate-health-workdays.md | done 2026-07-31 |
| articles/_brief/coastal-informal-cluster.md | done 2026-07-31 |
| articles/_brief/digital-availability-use-gap.md | done 2026-07-31 |
| articles/_brief/disaster-recovery-lag.md | done 2026-07-31 |
| articles/_brief/flood-market-access-cluster.md | done 2026-07-31 |
| articles/_brief/food-price-joint-qualifier.md | done 2026-07-31 |
| articles/_brief/grid-reliability-heat.md | done 2026-07-31 |
| articles/_brief/invisible-urbanization-cluster.md | done 2026-07-31 |
| articles/_brief/migration-displacement-signals.md | done 2026-07-31 |
| articles/_brief/port-hinterland-friction.md | done 2026-07-31 |
| articles/_brief/public-data-freshness-two-clocks.md | done 2026-07-31 |
| articles/_brief/public-service-data-quality.md | done 2026-07-31 |
| articles/_brief/remittance-resilience.md | done 2026-07-31 |
| articles/_brief/school-heat-honest-narrowing.md | done 2026-07-31 |
| articles/_brief/sp-shock-readiness-cluster.md | done 2026-07-31 |
| articles/_brief/water-crop-pressure-cluster.md | done 2026-07-31 |
| articles/pm25-observability-gap-cluster-brief.md | done 2026-07-31 |

#### Blogs (sentence-rule audit; rewrite only if violating)

| File | Status |
|---|---|
| articles/_blog/access-services.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/climate-health-workdays.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/coastal-informal-cluster.md | done 2026-07-31 |
| articles/_blog/digital-availability-use-gap.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/disaster-recovery-lag.md | done 2026-07-31 |
| articles/_blog/flood-market-access-cluster.md | done 2026-07-31 |
| articles/_blog/food-price-joint-qualifier.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/grid-reliability-heat.md | done 2026-07-31 |
| articles/_blog/invisible-urbanization-cluster.md | done 2026-07-31 |
| articles/_blog/migration-displacement-signals.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/port-hinterland-friction.md | done 2026-07-31 |
| articles/_blog/public-data-freshness-two-clocks.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/public-service-data-quality.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/remittance-resilience.md | done 2026-07-31 |
| articles/_blog/school-heat-honest-narrowing.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/sp-shock-readiness-cluster.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/_blog/water-crop-pressure-cluster.md | audited-conforming 2026-07-31 (orphan post-FM `updated_at` removed; re-synced) |
| articles/pm25-observability-gap-cluster-blog.md | done 2026-07-31 |

#### Social (hook-first rewrite)

| File | Status |
|---|---|
| articles/_social/access-services.md | done 2026-07-31 |
| articles/_social/climate-health-workdays.md | done 2026-07-31 |
| articles/_social/coastal-informal-cluster.md | done 2026-07-31 |
| articles/_social/digital-availability-use-gap.md | done 2026-07-31 |
| articles/_social/disaster-recovery-lag.md | done 2026-07-31 |
| articles/_social/flood-market-access-cluster.md | done 2026-07-31 |
| articles/_social/food-price-joint-qualifier.md | done 2026-07-31 |
| articles/_social/grid-reliability-heat.md | done 2026-07-31 |
| articles/_social/invisible-urbanization-cluster.md | done 2026-07-31 |
| articles/_social/migration-displacement-signals.md | done 2026-07-31 |
| articles/_social/port-hinterland-friction.md | done 2026-07-31 |
| articles/_social/public-data-freshness-two-clocks.md | done 2026-07-31 |
| articles/_social/public-service-data-quality.md | done 2026-07-31 |
| articles/_social/remittance-resilience.md | done 2026-07-31 |
| articles/_social/school-heat-honest-narrowing.md | done 2026-07-31 |
| articles/_social/sp-shock-readiness-cluster.md | done 2026-07-31 |
| articles/_social/water-crop-pressure-cluster.md | done 2026-07-31 |
| articles/pm25-observability-gap-cluster-social.md | done 2026-07-31 |

#### Slides (structure-preserving copy pass; heading counts frozen)

| File | Status |
|---|---|
| articles/_slides/access-services.md | done 2026-07-31 |
| articles/_slides/air-monitoring.md | done 2026-07-31 |
| articles/_slides/climate-health-workdays.md | done 2026-07-31 |
| articles/_slides/coastal-informal-cluster.md | done 2026-07-31 |
| articles/_slides/digital-availability-use-gap.md | done 2026-07-31 |
| articles/_slides/disaster-recovery-lag.md | done 2026-07-31 |
| articles/_slides/flood-market-access-cluster.md | done 2026-07-31 |
| articles/_slides/food-price-joint-qualifier.md | done 2026-07-31 |
| articles/_slides/grid-reliability-heat.md | done 2026-07-31 |
| articles/_slides/invisible-urbanization-cluster.md | done 2026-07-31 |
| articles/_slides/migration-displacement-signals.md | done 2026-07-31 |
| articles/_slides/port-hinterland-friction.md | done 2026-07-31 |
| articles/_slides/public-data-freshness-two-clocks.md | done 2026-07-31 |
| articles/_slides/public-service-data-quality.md | done 2026-07-31 (PPTX rebuild verified) |
| articles/_slides/remittance-resilience.md | done 2026-07-31 |
| articles/_slides/school-heat-honest-narrowing.md | done 2026-07-31 |
| articles/_slides/sp-shock-readiness-cluster.md | done 2026-07-31 |
| articles/_slides/water-crop-pressure-cluster.md | done 2026-07-31 |
| articles/pm25-observability-gap-cluster-deck.md | done 2026-07-31 |

### Phase 4 — reader guides

| File | Status |
|---|---|
| articles/about-the-lab.md | done 2026-07-31 |
| articles/reading-the-program-register.md | done 2026-07-31 |

### Phase 5 — program story surfaces

| Program slug | Status |
|---|---|
| public-service-data-quality | audited-conforming 2026-07-31 |
| remittance-resilience | done 2026-07-31 |
| migration-displacement-signals | done 2026-07-31 |
| climate-health-workdays | done 2026-07-31 |
| disaster-recovery-lag | done 2026-07-31 |
| grid-reliability-heat | done 2026-07-31 |
| port-hinterland-friction | audited-conforming 2026-07-31 |
| water-stress-crop-diversification | audited-conforming 2026-07-31 |
| social-protection-shock-coverage | audited-conforming 2026-07-31 |
| school-heat-disruption | audited-conforming 2026-07-31 |
| food-price-climate-transmission | audited-conforming 2026-07-31 |
| coastal-informal-risk | audited-conforming 2026-07-31 |
| flood-market-access | audited-conforming 2026-07-31 |
| invisible-urbanization | audited-conforming 2026-07-31 |
| access-services | audited-conforming 2026-07-31 |
| air-monitoring | done 2026-07-31 |
| digital-performance | done 2026-07-31 |
| public-data-freshness | audited-conforming 2026-07-31 |
| mpi-nighttime-lights | audited-conforming 2026-07-31 (no editable story prose; README-only / 1 of 9) |

### Phase 6 — site copy strings

| Surface | Status |
|---|---|
| Home / Research / Briefs / Articles / Layout copy | done 2026-07-31 (tone pass; layout/structure deferred) |

---

## 9. Definition of done (whole engagement)

1. Every tracker row is `done`, `audited-conforming`, or `flagged`
   with an owner-visible reason. Zero `todo` rows remain.
2. All five gates pass from a clean run; `sync-articles`,
   `sync-evidence`, `sync-references` are current; the production
   build compiles; the Vercel production gate exits 0.
3. Browser QA (1280/375, zero console errors, zero overflow) passed on
   every changed public surface, with screenshots where the program
   convention stores them (`reporting-site/qa/`).
4. Every touched program board carries the editorial-pass entry;
   `research/STATUS.md` untouched unless flagship/queue changed.
5. Number audits (§5) ran on every rewritten file with explained-only
   diffs.
6. No claim, number, figure, citation, maturity label, attestation
   label, or nonclaim changed anywhere — verifiable from the diffs.

If any item cannot be completed, it is reported as not done, with the
blocking reason — never reported as done.

---

## 10. Execution close-out (2026-07-31)

**All tracker rows above are `done` or `audited-conforming`.** Zero `todo` rows remain.

Verification at close:

| Check | Result |
|---|---|
| Five gates | All pass (banned words, DMC, citations, composite-headline, WIP) |
| `sync-articles` / `sync-evidence` / `sync-references` | Current (96 articles; 19/19 programs) |
| `cd reporting-site && npm run build` | Clean — 73 routes |
| Browser QA 1280/375 | Pass on 8 routes × 2 widths (0 console errors, 0 horizontal overflow); artifacts in `reporting-site/qa/editorial-refactor-2026-07-31/` |
| Vercel production gate | **Not done this session** — `node scripts/verify-vercel-production.mjs` failed at `npm ci` with `EPERM` unlinking `@next/swc-win32-x64-msvc` (file lock from concurrent Node processes / OS). Re-run after clearing the lock before any production push. A plain production `npm run build` already compiled clean. |

Constitutional floor held: editorial flow only; no claim, maturity, figure-path, or citation-key changes intended.
