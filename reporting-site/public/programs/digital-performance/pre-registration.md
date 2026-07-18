# Prospective design freeze

`attestation_chain: ai-first` · Prospective pre-analysis record · 2026-07-19

This design was frozen after inspecting the public ITU DataHub catalogue and
response schemas, but before downloading or inspecting the ADB developing-member
observations. It is a prospective design record for the first data object, not a
promise that the resulting claim will survive.

## Decision question

Do official 4G/LTE population-coverage estimates and observed internet use tell
the same connectivity story across ADB developing member economies?

## Primary estimand

For economy *i* and year *t*:

`availability-use gap = 4G/LTE population coverage (%) - individuals using the Internet (%)`

The two values must refer to the same economy and calendar year. Positive values
mean that nominal network availability exceeds reported recent use. They do not
identify the reason for non-use.

## Primary population and period

- The repository's established 44-economy ADB developing-member roster.
- Annual ITU DataHub observations from 2012 through 2024.
- The headline cross-section is the latest year through 2024 with exact-year
  pairs for at least half of the roster (22 economies).
- If no year passes that coverage floor, the cross-section is not published and
  source comparability becomes the result.

The 2024 cap avoids treating the incomplete 2025 reporting cycle as a settled
cross-section. It is a vintage rule, not a performance threshold.

## Source objects

1. ITU DataHub `i271GA` (`codeID 19306`): percentage of the population within
   range of at least a 4G/LTE mobile-cellular signal, whether or not they
   subscribe or use it.
2. ITU DataHub `i99H` (`codeID 11624`): percentage of individuals who used the
   Internet from any location in the previous three months, through a fixed or
   mobile network.

Secondary source objects, inspected only after the primary design above was
frozen, test plausible correlates without being allowed to redefine the primary
headline:

3. ITU DataHub `i271mb_5GB_GNI` (`codeID 36056`): the data-only mobile
   broadband 5 GB basket as a percentage of GNI per capita.
4. ITU DataHub rural and urban disaggregations of internet use (`codeID 9291`
   and `9300`): used to calculate the urban-minus-rural use gap where the same
   economy and year are reported.

The API responses, catalogue metadata, retrieval time, URL, byte count, and
SHA-256 digest will be cached locally and inventoried by the committed script.

## Decision rules

- Never carry a value forward or backward to manufacture an exact-year pair.
- Never impute a missing economy or year.
- Show signed gaps and both components; do not publish a composite score.
- Report the full paired sample and the excluded roster.
- Keep ITU estimates, administrative reports, and survey-based observations in
  the same descriptive panel but preserve their source notes for audit.
- Treat negative gaps as possible cross-source or measurement disagreement, not
  as impossible values to delete.
- Do not infer affordability, service quality, speed, digital skills, welfare,
  or causal effects from the gap.

## Robustness and sensitivity

- Re-select the headline year at sample-coverage floors of 25%, 50%, and 75% of
  the 44-economy roster. These are the required ±50% checks around the 50% rule.
- Recompute the cross-section on observations whose source string identifies an
  ITU estimate and on all reported observations; report whether the sign and
  broad ordering change.
- Compare economy gaps over time only on exact-year pairs and show the changing
  sample explicitly.
- Associate the primary gap with the 5 GB affordability measure and the
  urban-minus-rural use gap only on exact economy-year matches. Correlations are
  descriptive and must carry their sample size.
- Audit 3G/LTE hierarchy where both series exist; 4G coverage greater than 3G
  coverage is a source-consistency flag, not silently repaired.

## Falsification and stopping rules

- If the latest qualified cross-section has no material spread, retire the
  cross-economy gap story.
- If the headline year changes under the 25%/50%/75% coverage floors and the
  finding reverses, publish the sample-instability result instead.
- If fewer than 22 economies have any exact-year pair through 2024, stop before
  article production and publish the comparability limitation.
- Ookla is admitted only for a separate, conditional-on-test performance job.
  It cannot validate adoption or explain this availability-use gap.

## AI-first freeze

| Field | Value |
|---|---|
| Frozen by | §18 AI-first under `CONSTITUTION.md` §18.1 |
| Date frozen | 2026-07-19, before the first accepted pipeline run |
| Freeze commit | The promotion commit containing this file; resolve with `git log -- digital-performance/pre-registration.md` |
| First testable claim | The latest qualified exact-year cross-section has a positive median `i271GA - i99H` difference, with both components reported separately. |
| Falsification condition | The claim is retired or reshaped if the qualified cross-section lacks material spread, the sign reverses under the 25%/50%/75% sample-floor rule, or fewer than 22 roster economies form a pair. |
| Attestation chain | `ai-first` |

The rules above were written prospectively. Later results may report whether
they passed, but may not rewrite the rules without preserving this version as
a retracted or superseded design.
