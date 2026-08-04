# Current research status — operating board

Last updated: 2026-08-04.

## Current focus

| Field | Value |
|---|---|
| Active flagship | `Task31` — commissioned welfare-loss evidence review, first artifact of the §2.7 review track |
| Stage | Verification complete; locator backfill outstanding |
| Highest-leverage move | **Close the locator gap** — 20 records are reachable only as journal landing pages, so their figures cannot yet enter a headline, table, or synthesis sentence under §2.7. |
| Per-program board | `research/STATUS.md` |
| Operating mode | §18 ACTIVE; Mode A review |
| Previous flagship | `public-data-freshness` — orphan text slides removed and the source visually checked as a nine-slide, seven-figure PPTX. |

## Review track (§2.7, added 2026-08-04)

Evidence reviews are a second artifact class: their numbers come from
published studies, so §2.2's committed-script rule is inapplicable and §2.7's
verified-identity-plus-locator rule governs instead. Two gates enforce it,
`Task31/verify_citations.py` and `Task31/locate_estimates.py`.

Task31 state: citations 22 VERIFIED / 30 NEEDS_LOCATOR / 0 unresolved (gate
passes). Locator 19 LOCATED / 10 INACCESSIBLE / 20 landing-page-only. Three
defects found and corrected — two transposed figures and one transposed DOI
that resolved to the wrong paper. The artifact is **not citable** until the
locator backfill lands; it carries no maturity label.

Open gaps beyond locators: 10 of the 18 journals named in the commissioning
brief have zero records, including the development-economics core (JDE, AER,
REStat, EDCC) and all three field journals; Central Asia rests on one record.

## Decision and queue

The AI-eligible queue now has complete standard research stories and built
decks. Do not reopen a closed issue unless a named public source can change its
claim.

1. **`Task31` locator backfill** — 20 records need full text the screen could
   not reach. Until each has a page/table locator, its figures stay out of
   every headline, table, figure, and synthesis sentence under §2.7.
2. **`mpi-nighttime-lights`** — 1 of 9 sections, no hero, and no deck; retain
   the owner/coauthor-led path and do not treat it as an AI packaging target
   without owner direction.
3. **Next flagship** — select a new public data object with a rough visual and
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
