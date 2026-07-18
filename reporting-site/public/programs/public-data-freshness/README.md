# Public data freshness blind spots

`attestation_chain: ai-first` · Active flagship · Mode A review

**Status:** Hypothesis with a qualified L2 hook. The expanded L3 test is
prospectively frozen but has not yet run.

## Research question

How often does a development-data cell that looks old by calendar year cease to
look economy-specifically delayed after the indicator's own global production
frontier is taken into account?

## Why this belongs in the factory

ADB country teams, ERDI data producers, and dashboard users routinely combine
indicators with different production cycles. A 2020 PM2.5 estimate and a 2023
electricity-access estimate can both be the latest available observations for
their respective series. Showing only the reference year can therefore mix two
different phenomena: an indicator-wide production lag and an economy-specific
publication gap. The program tests whether separating those quantities changes
which cells deserve review. It does not score national statistical systems.

## Qualified hook card

| Field | Decision |
|---|---|
| Source object | World Bank WDI public API; economy × indicator × reference-year observations, retrieved as a pinned snapshot. ADB *Basic Statistics 2026* supplies the regional policy-domain frame, not the empirical values. |
| First visual | Economy-by-indicator heatmap that decomposes calendar age into indicator-wide production age and economy-specific relative lag. |
| Possible claim | A material share of calendar-old WDI cells in the ADB developing-member sample reflects indicator-wide production cycles rather than economy-specific relative delay. |
| Decision user | ADB/ERDI dashboard designers and country teams deciding which data cells need a freshness warning or source follow-up. |
| Falsifier | Classification disagreement stays below 10% under the 9-, 18-, and 27-indicator sets and the 1.5-, 3-, and 4.5-year thresholds. |
| Landscape gap | Existing work measures statistical-system performance, indicator-level WDI suitability, aggregate data availability, or macro-series dissemination. It does not expose this two-part age decomposition at the ADB economy × cross-domain indicator cell used by a dashboard reader. |
| Stop condition | Defer the program if the decomposition adds little classification information, if results reverse across the pre-specified indicator sets, or if source metadata cannot distinguish observed from missing cells without unsupported assumptions. |

## Prospective indicator design

The baseline has 18 indicators: two pre-selected indicators in each of nine
policy domains. Sensitivity uses one per domain (9; −50%) and three per domain
(27; +50%). Selection is frozen in `pre-registration.md`; later results cannot
swap codes to improve the story.

## Public data plan

| Source | Role | Unit | Access and license | Retrieval plan |
|---|---|---|---|---|
| World Bank WDI API | Values, reference years, source notes, global frontier | Economy × indicator × year | Public API; World Bank open-data terms | One cached JSON response per frozen indicator, with URL, retrieval time, byte count, and SHA-256 |
| World Bank WDI monitoring framework | Method precedent and indicator-level comparison | Indicator | Public technical note and monitoring download | Pin publication/vintage in source inventory |
| ADB Basic Statistics 2026 | External policy-domain relevance frame | Regional publication and metadata | Public CSV/metadata; CC BY 3.0 IGO | Cache the published CSV and dataset metadata |

## First testable claim

Across the baseline 18-indicator matrix, at least 10% of observed cells change
review status when freshness is classified relative to the indicator's global
production frontier rather than by calendar age alone.

## Falsification condition

The claim is retracted if disagreement is below 10% in the baseline and both
indicator-set sensitivity runs, or if the direction is driven by a single
domain whose exclusion removes the result.

## Reproduce

```powershell
python public-data-freshness/scripts/build-freshness-panel.py
python public-data-freshness/scripts/build-figure-dossier.py
```

The commands become operative only after the frozen pipeline is committed.

## Current gate

The program remains Hypothesis until the expanded pipeline runs from the
committed freeze, the evidence packet is complete, and the claim survives its
pre-specified sensitivities. The completed L2 sprint remains at
`research/topic-sprints/wdi-data-freshness-sprint.md`.
