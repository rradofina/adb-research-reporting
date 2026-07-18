# Migration and displacement signals

`attestation_chain: ai-first`

This program studies how the interpretation of international migrant stock
changes with the denominator and with migration type. The current issue uses
three public objects:

1. UN DESA International Migrant Stock 2024 origin-destination stock;
2. World Bank WDI 2024 resident population; and
3. UNHCR Refugee Data Finder 2024 forced-displacement categories.

The main result is a denominator switch: the absolute and population-share
top fives have zero overlap. Afghanistan is the near-rank exception, but its
emigrant stock is forced-displacement-majority in the UNHCR crosswalk.

Start with:

- `paper-charter.md` — question, audience, claim, and stopping rule;
- `results.md` — full chart-led result;
- `limitations.md` — stock, denominator, source, and interpretation limits;
- `REPRODUCE.md` — refresh and figure-only commands; and
- `generated/migration-figure-dossier-summary.json` — compact machine-readable
  finding and figure manifest.

The program does not estimate current migration flows, migration propensity,
labor-migration purpose, internal displacement, welfare, or causal drivers.
