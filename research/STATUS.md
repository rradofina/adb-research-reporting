# Current research status — operating board

Last updated: 2026-08-05.

## Current focus

| Field | Value |
|---|---|
| Active flagship | `Task31` — commissioned welfare-loss evidence review, first artifact of the §2.7 review track |
| Stage | 15 of 52 figures read and citable; reader surface rebuilt subject-first |
| Highest-leverage move | **Backfill the six economics journals the search missed** — the literature is measured and present (AER 493, JDE 383, JEEM 380 on-topic works since 2015). Then the owner's naming decision. |
| Per-program board | `research/STATUS.md` |
| Operating mode | §18 ACTIVE; Mode A review |
| Previous flagship | `public-data-freshness` — orphan text slides removed and the source visually checked as a nine-slide, seven-figure PPTX. |

## Review track (§2.7, added 2026-08-04)

Evidence reviews are a second artifact class: their numbers come from
published studies, so §2.2's committed-script rule is inapplicable and §2.7's
verified-identity-plus-locator rule governs instead. Six gates in
`review-factory/gates/` enforce it: verify_citations, resolve_fulltext,
locate_estimates, extract_context, apply_locators, validate_register.

Task31 state: citations 22/22 DOIs resolve (gate exits 0). Locators: 19
confirmed by reading the source prose, 7 read but partly unsupported, 18
unread because no lawful copy served readable text. **19 of 52 figures are
citable under §2.7.**

Four defects found and corrected, each invisible to the five pre-existing
gates: two transposed figures (8,970 for 8,790; "65%" from the "$3.65" poverty
line), one transposed DOI resolving cleanly to a different paper, and one set
of country attributions the source never made (Indonesia and Bangladesh appear
nowhere in the paper credited with their figures).

Three false-alarm classes were also found and fixed in the screen itself,
each of which had been blaming the review for something it did not do:
comma-formatted thousands, Lancet middle-dot decimals ("18·2" for 18.2), and
publisher block pages read as full text. The screen now tries every lawful
copy — repository, PubMed Central, publisher — before calling a source
unreadable.

Open gaps beyond locators: 10 of the 18 journals named in the commissioning
brief have zero records, including the development-economics core (JDE, AER,
REStat, EDCC) and all three field journals; Central Asia rests on one record.

## Decision and queue

The AI-eligible queue now has complete standard research stories and built
decks. Do not reopen a closed issue unless a named public source can change its
claim.

1. **Site name — owner decision, and not a cosmetic one.** "Blindspots Lab"
   appears in 52 files including `CONSTITUTION.md`, `LICENSE-CONTENT`,
   `README.md`, every frozen `review-packets/*/shared/CONSTITUTION.md`, and
   the Zenodo deposition metadata. "Development Evidence Lab" appears only in
   the newer reporting-site chrome. So the **site is the deviation**, not the
   articles. Resolving it means either correcting the site chrome to the
   constitutional name, or amending the Constitution and the content licence
   under §16 — which is owner-only. AI must not rewrite frozen review packets
   or a licence to settle a naming question.
2. **`Task31` remaining sources** — 18 records have no lawful copy that serves
   readable text and need ADB Library access; 3 need a corrected URL.
   Everything lawfully reachable has been read.
3. **`mpi-nighttime-lights`** — 1 of 9 sections, no hero, and no deck; retain
   the owner/coauthor-led path and do not treat it as an AI packaging target
   without owner direction.
4. **Next flagship** — select a new public data object with a rough visual and
   falsifiable claim; do not start from a broad topic essay.

All AI-eligible programs expose 9 of 9 standard sections and a built deck.
`port-hinterland-friction` remains closed at the port boundary until the
qualified shipment-level hinterland source is available.

## Session protocol

At open, read `CLAUDE.md`, `research/JUDGMENT.md`, `research/DESIGN.md`,
`research/factory.md`, `CONSTITUTION.md`, this board, and the active program
board. State the flagship, stage, move, and reason. At close, run the six
research checks, production build, and 1280/375 browser QA for public changes.
Keep program boards within ten finding-first lines.

Formal maturity changes live in `research/wip-register.md`. The repository is
the byte-reproducible source of truth; Supabase is a downstream query
projection, and Vercel serves the static reader surface.
