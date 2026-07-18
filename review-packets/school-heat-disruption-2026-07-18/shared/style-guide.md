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

## 7. Failure mode

A check failure on any of §1, §2, §3, §4 blocks the PR. The author
either:

- edits the offending text;
- explicitly opts out for one occurrence with `<!-- style-guide:allow {rule} -->`
  (logged in the PR description; reviewed by the supervisor);
- or files a decision record under `research/decisions/` to amend
  the rule.

The style guide does not bend silently.
