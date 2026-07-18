# Data sources and coverage

`attestation_chain: ai-first` · 2026-07-19

## Analytical population

The study uses the established 42-economy WDI-compatible ADB developing-member
roster and a prospectively frozen cross-domain indicator design.

| Layer | Indicators | Possible cells | Observed | Missing | Observed share |
|---|---:|---:|---:|---:|---:|
| Lower sensitivity set | 9 | 378 | 355 | 23 | 93.9% |
| Baseline | 18 | 756 | 709 | 47 | 93.8% |
| Upper sensitivity set | 27 | 1,134 | 1,006 | 128 | 88.7% |

The unit is one economy × indicator cell. The pipeline selects the latest
non-null observation through 2025. It does not carry values across years,
interpolate, or impute missing cells.

![The frozen upper set yields 1,006 observed cells; the baseline supplies the primary 709-cell analysis.](/programs/public-data-freshness/generated/charts/public-data-freshness-01-coverage-funnel.svg)

## Source custody

Empirical values and indicator metadata come from one cached public World Bank
WDI API response per frozen code. Each raw gzip object has a provenance
sidecar recording URL, retrieval time, raw and compressed bytes, and SHA-256
digests. The committed source inventory links each generated row to its
response hash.

ADB *Basic Statistics 2026* supplies a public cross-domain relevance frame,
not any panel value. Its dataset page was available, but the direct CSV and
metadata download paths returned a Cloudflare challenge to noninteractive
clients on 2026-07-19. The access wall is recorded; no empirical value was
inferred from the unavailable file.

## Indicator coverage

The baseline has two pre-selected indicators in each of nine domains. The
upper set adds one per domain. Frozen code `EN.ATM.CO2E.PC` returned an archived
or unavailable WDI response and remains a disclosed 42-cell source failure.
It was not replaced after results were seen.

Baseline missingness is concentrated in labor and social conditions (14 of 84
cells) and poverty and inequality (11 of 84). No baseline domain observes less
than 83.3% of its possible cells.

## Group coverage diagnostic

The 12-economy Pacific small-island group has 182 observed and 34 missing
baseline cells, an observed share of 84.3%. The other 30 economies have 527
observed and 13 missing cells, an observed share of 97.6%. This grouped
diagnostic is descriptive and does not support economy rankings.

## Version boundary

The snapshot was retrieved on 2026-07-19 and capped at reference year 2025.
WDI can revise historical values and metadata. Reproduction against the
committed cache reconstructs this result; a live refresh creates a new source
vintage that must be compared by digest.
