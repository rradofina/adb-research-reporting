# Style guide

Governed by `CONSTITUTION.md` §13.3 and §14. Enforced by deterministic
scripts in `/scripts/`. CI runs the checks on every PR.

---

## 1. Banned words (§14)

The following words are forbidden in any output, including README,
results, articles, briefs, and the reporting site copy.

- revolutionary
- unprecedented
- game-changing / game changing
- groundbreaking
- breakthrough (when used as marketing language; technical use in
  a measurement-sensor context is OK if the script flags a false
  positive — author addresses inline)
- world-class
- cutting-edge
- state-of-the-art
- best-in-class
- transformative (as marketing; technical "transform"/transformation
  in a methodology sense is OK)
- paradigm shift / paradigm-shifting

The check script is `scripts/check-banned-words.mjs`. It runs on
`{slug}/results.md`, `{slug}/README.md`, `articles/**/*.md`, and the
reporting site's copy files.

---

## 2. DMC framing (§13.3)

Findings are framed as **measurement gap**, **coverage gap**, or
**observability gap** — not as DMC deficiency.

Forbidden framings:

- "Country X has poor data."
- "The {region} lacks proper records."
- "Country Y is failing on …"
- "Underdeveloped statistical capacity in …" (use "thin observation
  layer in …" or "sparse public-data coverage in …")
- "{Country} is behind on …" (use "{Country} carries less public
  data on … in our dataset")

Allowed framings:

- "The measurement gap for X in {country} is …"
- "Public-data coverage for Y in {country} is sparse for the period
  studied, so …"
- "The observability gap between {public maps} and {administrative
  registry} in {country} is …"
- "ADB DMCs cluster into {n} groups by data infrastructure: …"

The check script is `scripts/check-dmc-framing.mjs`. It looks for
forbidden phrases and flags them; the author resolves inline.

---

## 3. Citation discipline (CLAUDE.md, §5.3)

- Cite by BibTeX key from `/references.bib`. Never cite by bare URL
  in the body of an output.
- The first time a key is cited, the renderer renders the full author-
  year (e.g., "Sandefur and Glassman 2015 [@sandefur2015badata]").
- Subsequent citations of the same key render as "[@key]" only.
- A URL may appear in the body only inside a `<details>` block as
  retrieval-aid context, never as the citation itself.

The check script is `scripts/check-citations.mjs`.

---

## 4. Composite-index discipline (§6.4)

A composite index may appear in an output but must:

- not headline the article;
- not produce a country ranking as the headline finding;
- be labeled "screening only" wherever it appears.

The check script is `scripts/check-composite-headline.mjs`.

---

## 5. AI transparency (§12, AI_TRANSPARENCY.md)

Every output names which parts were AI-drafted and what was
human-checked. The reporting site's "About" page already encodes the
limits.

In any program README:

```markdown
## AI assistance

- Literature review first pass: AI-drafted, owner-finalized at
  commit {hash}.
- Pre-registration: AI-drafted, owner-frozen at commit {hash}.
- Sensitivity table: AI-drafted from owner-specified parameter ranges,
  owner-verified at commit {hash}.
- Pipeline code: AI-drafted, owner-reviewed at commit {hash}.
- Article body: AI-drafted, owner line-edited at commit {hash}.
```

---

## 6. Outputs that the style guide governs

- `{slug}/README.md`
- `{slug}/results.md`
- `{slug}/limitations.md`
- `articles/**/*.md`
- `reporting-site/src/pages/**/*.tsx` (copy strings)
- Any committed PDF (rare; flagged for manual review)

---

## 7. Article flow — the reader arc (added 2026-07-31)

**Principle.** An article is written for the reader's question, not the
pipeline's audit trail. The model is the editorial arc used by Development
Asia (ADB's knowledge platform): a standfirst a busy practitioner can
retell, story-led sections in plain language, and a closing "so what."
Rigor lives in the frontmatter, the evidence page, and a methods box — not
in the reader's path. An article whose body reads like a compliance report
has failed even if every gate passes.

**The arc.** Every reader-tier article (working paper body, brief, blog)
follows this order:

1. **Standfirst.** The `subtitle` is one or two sentences a reader can
   retell: what was found, where, and why it matters. Never a methods
   note ("A 24-economy audit stops before…" is a methods note).
2. **Open in the reader's world.** The first section sets a concrete
   scene or question a practitioner actually has — a place, a stake, a
   decision that depends on the answer. It never opens with the
   apparatus ("the audited packet", "the ledger verifies").
3. **What we found.** Numbers appear inside sentences that interpret
   them. "0 same-station joins" is a recitation; "not one station could
   be publicly confirmed as the same physical monitor in both sources"
   is a finding.
4. **Why it happens / a close-up.** One section that makes the pattern
   tangible — a named example, a gradient, a mechanism.
5. **What this means for the reader.** The practitioner "so what": what a
   planner, analyst, or program officer should do differently.
6. **What this does not say.** Limitations stay mandatory and appear
   before the close — written as reader guidance, not as a legal list.
7. **What would change this finding.** The named public evidence that
   would narrow or overturn it (§6.7 stopping rule, reader-facing).
8. **How we measured this.** Three to five plain sentences plus the
   reproduce commands and the evidence-page link. Everything deeper —
   stage rules, retrieval states, ledger schemas — belongs on the
   evidence page, not in the body.

**Sentence-level rules.**

- Section headings carry the argument: a reader who reads only the
  headings gets the story. Process labels ("Methodology and claim
  test", "Data and coverage") are not headings on the reader tier.
- One idea per section; paragraphs of two to four sentences.
- Coined internal terms ("claim-permission ladder", "nonclaim
  geometry", "monitor-grade closure") never reach the reader tier
  without a plain-language rendering first — and by default they stay
  off it entirely.
- The honesty machinery (maturity label, `attestation_chain`,
  nonclaims) is untouched by this section: it is surfaced in
  frontmatter and near the headline, exactly as before. The arc changes
  how the body reads, never what it claims.

This section governs new articles immediately and existing articles as
they are next touched. §1–§4 checks apply unchanged.

---

## 8. Failure mode

A check failure on any of §1, §2, §3, §4 blocks the PR. The author
either:

- edits the offending text;
- explicitly opts out for one occurrence with `<!-- style-guide:allow {rule} -->`
  (logged in the PR description; reviewed by the supervisor);
- or files a decision record under `research/decisions/` to amend
  the rule.

The style guide does not bend silently.
