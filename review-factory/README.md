# Review factory

Shared machinery for `CONSTITUTION.md` §2.7 evidence-review programs.

## Why this exists

The repository's primary-analysis programs satisfy §2.2 by computing every
number from a committed script hitting a public dataset. An evidence review
cannot: its sources are published studies, and no script can recompute another
team's estimate.

§2.7 defines the equivalent obligation — **verified source identity, a page
locator, and a retrieval timestamp** — and this folder is the machinery that
enforces it. Task 31 was produced before any of this existed. Three defects
survived every gate the repository had: two transposed figures, and a DOI
whose transposed digit resolved cleanly to a real paper by different authors on
an unrelated topic. None were exotic. They were the ordinary consequence of a
register nothing checked.

## What a review is

Any directory containing a `review.json` manifest and an evidence module.
Discovery scans the repository, so adding a review is adding a folder.

```
Task31/
  review.json            manifest: slug, title, paths, maturity, citability
  evidence_data.py       EVIDENCE, REFERENCES, ANNOTATED_IDS
  review_protocol.md     design, scope, eligibility, search strategy
  review_manuscript.md   the prose
  SOURCE-QUEUE.md        what blocks citability
  outputs/               DOCX, PDF, XLSX, HTML
```

Gate outputs (`verification_ledger.json`, `locator_ledger.json`,
`fulltext_map.json`, `locators.json`) are written beside the review they
describe, never beside the factory.

## The gates

Run in this order. Each takes `--review SLUG`, or infers it when only one
review exists.

| Gate | Question it answers |
|---|---|
| `verify_citations.py` | Does every DOI resolve to a work whose journal, year, and first author match the register? Exits non-zero if not. |
| `resolve_fulltext.py` | Is there a lawful open-access copy of each source, and where? Never circumvents a paywall. |
| `locate_estimates.py` | Do the numbers the review attributes to a source actually appear in it? |
| `apply_locators.py` | Record the pages the screen found — as **provisional**, never as confirmed. |
| `validate_register.py` | Which records are citable, and does the manuscript quote any that are not? |

## The one rule that matters

A record is citable only when **both** halves of §2.7 hold: verified identity
*and* a confirmed locator. Neither alone is enough, and the reasons are
symmetric:

- A resolving citation can be the wrong citation. A transposed DOI digit
  resolves perfectly.
- A located number can be the wrong number. It can sit in an unrelated table
  on the same page.

`apply_locators.py` therefore writes screen results as `confirmed: false`.
They tell a reader which page to open. They do not grant citability — only
someone reading the surrounding text does that. Laundering a screen result
into a citation would reproduce exactly the failure this factory exists to
prevent.

## Starting a new review

```bash
python review-factory/new_review.py food-systems \
    --title "Food-System Shocks and Nutrition Outcomes in Asia and the Pacific" \
    --commissioned-by "..."
```

The scaffold starts with **zero** evidence records, deliberately. A review that
begins with model-recalled citations begins with the defect §2.7 exists to
catch.

## Honest limits

- The locator screen reads what it can lawfully fetch. Paywalled and
  bot-blocked sources are reported `INACCESSIBLE`, never silently passed.
- `LOCATED` is weak evidence of correctness; `NOT_FOUND` is strong evidence of
  a problem. The asymmetry is deliberate and is stated in every report.
- Nothing here establishes that a study's method is sound, only that the review
  represents the study accurately. Method critique is §9 review work, not a
  gate.
