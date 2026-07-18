# Public data freshness blind spots

`attestation_chain: ai-first` · Screening Result · Mode A review complete

## Finding

At the prospectively frozen three-year rule, calendar age and lag from the
indicator's global production frontier send **138 of 709 observed baseline
cells (19.5%)** to different review states. All 138 are calendar-only flags,
equal to 65.1% of the absolute review queue.

The pre-specified domain falsifier narrows the claim. Removing environment and
climate lowers disagreement to 9.2%, below the 10% gate. The supported result
is domain-concentrated: relative clocks materially change review queues where
indicators share slower production cycles, not uniformly across development
data.

![The baseline two-clock classification matrix.](/programs/public-data-freshness/generated/charts/public-data-freshness-04-classification-matrix.svg)

## Research question

How often does a WDI economy × indicator cell that looks old by calendar year
cease to look economy-specifically delayed after the indicator's own source
frontier is taken into account?

## Why it matters

Cross-domain dashboards routinely compare indicators with different production
cycles. A single latest-year badge mixes the age of the underlying observation
with the economy's lag from what the source currently reports elsewhere. This
study separates those quantities without replacing them with a composite
score.

## Evidence design

| Element | Frozen choice |
|---|---|
| Unit | Economy × indicator cell |
| Population | 42 WDI-compatible ADB developing member economies |
| Indicator sets | 9 lower, 18 baseline, 27 upper; balanced across nine domains |
| Source vintage | Public WDI API retrieved 2026-07-19, capped at 2025 |
| Primary rule | Share of observed baseline cells whose calendar and relative three-year review flags disagree |
| Gate | At least 10%, with set-size, threshold, frontier, vintage, and domain-deletion tests |
| Result | Baseline passes; single-domain dependence triggers claim reshaping |

## Full research package

- `paper-charter.md` and `pre-registration.md` freeze the question, indicator
  sets, estimands, sensitivities, and falsifiers before the expanded pull.
- `literature.md` and `literature-prisma.md` document the related-evidence
  landscape and the cell-level gap addressed here.
- `coverage.md`, `results.md`, `sensitivity.md`, and `limitations.md` provide
  the data, findings, robustness checks, and inference boundaries.
- `review-internal.md` and `review-external.md` preserve the AI-first critique
  and adversarial objections without claiming external endorsement.
- `upgrade-gap.md` records the conclusion and the next claim-changing data
  object.
- `REPRODUCE.md` documents the pinned-cache and live-refresh workflows.
- `generated/` contains the row-level panel, summaries, source inventory,
  sensitivity outputs, and 12 PNG/SVG figure pairs.

## Publication surfaces

The working paper leads with the finding and integrates the evidence figures
into the story. Brief, blog, slide, and social variants preserve the same
claim boundary. The evidence page exposes the complete research packet for
readers who want methodology and audit detail.

## Reproduce

```powershell
python public-data-freshness/scripts/build-freshness-panel.py
python public-data-freshness/scripts/build-figure-dossier.py
```

Use `--refresh` on the first command only when intentionally creating a new
WDI source vintage. Vercel is the publication layer; the committed central
research cache and generated evidence files are the research store.

## Non-claims

This is a WDI measurement and coverage diagnostic. It does not rate an
economy, national statistical office, indicator quality, or formal
dissemination timeliness. Missing is not stale; old is not wrong; relative to
frontier is not equivalent to on-time against an official release calendar.
