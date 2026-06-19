# L2 Hook Sprint: WDI Data Freshness Matrix

`attestation_chain: ai-first`
Date: 2026-06-16
Goal level: L2 hook sprint

## Decision

Promote this as a new program prospectus candidate.

The hook is not a public finding yet. It is a topic-creation result: a public
data matrix and rough visual show that the freshness of core development
signals is uneven across indicators and economies before any policy comparison
begins.

## Question Tested

Can a public World Development Indicators freshness matrix reveal where a
planning dashboard is weakened by stale or missing public indicator vintages,
not by the indicator value itself?

## Public Data Object

The sprint pulls selected World Bank World Development Indicators through the
public API. Each cell is one ADB DMC by one indicator. The sprint records the
latest public reference year with a non-null value, then compares it with that
indicator's own latest public reference year in the same API pull.

This relative lag rule matters. PM2.5 has an older global reference year than
unemployment or internet use, so the chart should not punish PM2.5 for being
globally older by design. It asks instead: within each indicator, which DMCs
have stale or missing public fields?

## Generated Artifacts

| Artifact | Path |
|---|---|
| Script | `research/topic-sprints/scripts/sprint-wdi-data-freshness.py` |
| CSV | `research/topic-sprints/generated/wdi-data-freshness-sprint.csv` |
| JSON | `research/topic-sprints/generated/wdi-data-freshness-sprint.json` |
| Rough chart | `research/topic-sprints/generated/charts/wdi-data-freshness-heatmap.png` and `.svg` |

Reproduce:

```powershell
python research/topic-sprints/scripts/sprint-wdi-data-freshness.py
```

## Data Sanity Checks

The script produced a 42 DMC by 9 indicator matrix, or 378 cells. It records
19 missing cells and 13 cells that are 3 or more years behind the indicator's
own latest public reference year.

The 2026-06-20 protocol pass adds a stricter source-review layer. It keeps
the original 13 strict stale-alert cells, but also labels missing public
fields and cells two relative reference years behind as protocol-review cells.
That produces 39 protocol-review cells in the current generated JSON. The
same pass records the indicator-level source context derived from the WDI API
pull: 3 near-current global series, 5 standard-lag global series, and 1 older
global production vintage. All 9 indicator records in this pass were retrieved
from the live WDI API rather than cache fallback.

The selected indicators are not a final theory of development measurement.
They are deliberately broad enough for topic triage: population, health
spending, primary enrollment, unemployment, electricity access, internet use,
PM2.5 exposure, agriculture value added, and remittances as a share of GDP.

The API metadata in the generated JSON records World Bank source update date
`2026-04-08` for the pulled WDI series.

## Visual QA

The heatmap rendered as a nonblank PNG and SVG. It is readable enough for
topic triage: rows are ADB DMC ISO3 codes, columns are selected WDI
indicators, cell text is the latest reference year, and `M` marks a missing
public WDI value in the pulled series. The note explicitly says this is an
observability screen, not a score of national statistical performance.

What the chart makes visible:

- Some missingness is concentrated in small island economies, which turns the
  topic toward public-data coverage and source design rather than country
  comparison.
- Internet use and remittances create the clearest freshness contrast because
  several DMC cells are well behind those indicators' latest public reference
  years.
- PM2.5 looks uniformly old by calendar year, but not stale in the relative
  matrix because the indicator's own latest public reference year is older.
  That distinction is the main methodological hook.

## Protocol Upgrade

The protocol upgrade does not infer non-applicability from memory. Missing
public WDI cells remain coverage-review cells until indicator documentation or
source-specific metadata can justify exclusion. Observed cells are classified
from the committed script as:

- `latest_for_indicator` when the DMC has the indicator's latest public
  reference year;
- `one_reference_year_watch` when the DMC is one relative reference year
  behind;
- `protocol_review` when the DMC is two relative reference years behind;
- `stale_alert` when the DMC is three or more relative reference years behind;
- `missing_public_field` when the pulled WDI series has no public value for the
  DMC.

This creates a better L3 handoff because the next program package can separate
true stale alerts from missingness, watch-list cells, older global production
vintages, and unresolved non-applicability questions.

## What This Does Not Mean

This is not evidence that an economy has weak statistical capacity. It is a
public-source observability test for one dashboard source. A stale WDI field
can come from indicator methodology, source update cycles, country reporting,
modeling vintages, or how the World Bank publishes the series.

This is also not an indicator-quality index. It is a screening matrix for
where a future program should inspect source-specific update rules and whether
policy-facing dashboards need freshness labels.

## Prospectus If Promoted

Working title:

**When Development Data Are Public but Stale**

First program question:

Which policy-relevant WDI indicators create hidden planning risk because the
latest public value for a DMC is old, missing, or out of sync with the
indicator's global update cycle?

First L3 tasks:

1. Expand the indicator set by policy domain and pre-register inclusion rules.
2. Separate true missingness from non-applicability and model-vintage limits.
3. Add source-specific refresh expectations, not only reference-year lags.
4. Test whether adding freshness labels changes cross-program screening
   conclusions already in the repo.
5. Build a publication visual that lets readers toggle value, latest year,
   and source-refresh risk.
