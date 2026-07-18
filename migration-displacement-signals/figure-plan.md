# Figure plan — Migration and displacement signals

`attestation_chain: ai-first`

Last updated: 2026-07-18.

| Figure | Reader question | Committed input | Visual role | Removal rule | Required caveat |
|---|---|---|---|---|---|
| Research hero | Does the leading set survive the denominator switch? | `generated/migration-per-population-deepening.json` | Show the two disjoint top fives and zero overlap | Remove if the two sets are not directly comparable at the same top-N | Stock, not flow; share is stock divided by resident population |
| Rank inversion | Where do the ten headline economies move? | `generated/migration-per-population-deepening.json` | Slopegraph for the union of the absolute and share top fives | Remove if labels or crossings are unreadable at 375 px | Three economies lack WDI denominators and are withheld |
| Population-share profile | Which economies are large relative to resident population? | `generated/migration-per-population-deepening.json` | Ranked bar chart for the top 12 population shares | Remove if bar length is allowed to imply current departures | Cumulative diaspora stock can span decades |
| Corridor concentration | How concentrated are the five largest absolute stocks? | `generated/migration-displacement-adb-panel.json`; `sensitivity-runs.json` | Top-2/top-3/top-5 dot plot with 50% reference | Remove if presented as the primary finding | Destination concentration mixes migration purposes and is threshold-sensitive |
| Forced-displacement composition | Is the population-share top five comparable with Afghanistan? | `generated/migration-corridor-type-forced-displacement.json` | Forced-displacement share bars for Afghanistan and the share top five | Remove if residual stock is labeled labor migration | Residual includes labor, family, student, temporary, and unclassified stock |
| Source observability | What can each joined source actually answer? | figure-dossier summary built from all three committed inputs | Coverage funnel plus construct matrix | Remove if missing denominators or unobserved migration purposes are hidden | UNHCR is a forced-displacement falsifier, not a complete purpose classifier |

All public figures must name the unit, vintage, source, exclusions, and
`attestation_chain: ai-first`. Figures carry findings or limits; none is
decorative.
