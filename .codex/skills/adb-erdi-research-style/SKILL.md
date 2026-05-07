---
name: adb-erdi-research-style
description: Write, revise, or review data-led research narratives in the ADB ERDI / ADB Data / Arturo Martinez Jr. statistical communication pattern. Use when Codex is drafting or improving research articles, data stories, evidence pages, chart captions, executive summaries, policy-facing methodology sections, or presentation copy that should explain empirical findings, source limits, and practical development relevance in a clear ADB-style voice.
---

# ADB ERDI Research Style

Use this skill to make research read like a credible ADB/ERDI data product: policy-relevant, source-grounded, chart-forward, cautious about claims, and useful to operational readers. Do not impersonate Arturo Martinez Jr., ADB, or ERDI; adapt the institutional narrative pattern.

## Core Pattern

Use this sequence unless the target format requires a shorter structure:

1. **Problem hook.** Start with the policy problem or decision need, not the model. Show why a planner, national statistics office, or development institution should care.
2. **Data gap.** Explain why conventional data are insufficient: not granular enough, not timely enough, too costly, incomplete, or hard to compare.
3. **Source upgrade.** Introduce the data source or integration step and state why it improves observability. Name the official source, temporal coverage, unit, license/access status, and refresh cadence where available.
4. **Method in plain English.** Explain the method in sequential steps. Use technical labels only after the reader knows the purpose.
5. **Chart/table result.** Put the key chart or table near the claim. Captions should state the unit, period, source, and caveat.
6. **Interpretation.** Say what changed in understanding. Avoid drama; make the result actionable.
7. **Limitations.** State what the result cannot prove, where source coverage is weak, and what would be needed for stronger use.
8. **Use case.** End with how the evidence can support targeting, monitoring, source improvement, or future statistical capacity work.

## Voice Rules

- Prefer measured institutional language: "suggests", "indicates", "can help", "is consistent with", "requires caution".
- Do not use hype superlatives or frontier-status slogans in reader-facing copy.
- Avoid first-person solo claims. Use "the analysis", "the pipeline", "the evidence", "the study", or "the article".
- Use "developing member economies", "DMCs", "economies", or exact geography names according to the repository's DMC framing rules.
- Keep methodology accessible enough for an economist, statistician, operations officer, and data journalist to follow.
- Make every empirical number traceable to a script, table, source URL, and date.

## Article Template

Use these headings or adapt them into prose:

```markdown
## Why This Measurement Problem Matters

## What Existing Data Miss

## Data Sources and Coverage

## Method

## Results

## What the Result Means

## What It Does Not Mean

## Reproduce the Analysis

## Next Statistical Upgrade
```

## Data Story Template

For a shorter web piece, use:

```markdown
Headline: concrete outcome + geography + data lens
Deck: one-sentence result and why it matters

1. Human/policy context
2. Why the old data view is insufficient
3. What source or method was added
4. Main chart/table with one-sentence takeaway
5. Caveat and operational use
6. Resources / evidence packet
```

## Presentation Pattern

Use 6-8 slides:

1. **Decision question.** What decision or monitoring problem is blocked by weak data?
2. **Current visibility.** What official/open sources exist and what do they miss?
3. **Source integration.** What new source or merge fixes the visibility problem?
4. **Method steps.** Three to five numbered steps with no equations unless essential.
5. **Main result.** One chart; headline says what the chart shows, not what to believe.
6. **Robustness and caveats.** Coverage, vintage, uncertainty, non-claims.
7. **Operational interpretation.** How to use it for targeting, monitoring, source improvement, or further validation.
8. **Reproduction.** Public sources, scripts, evidence packet, refresh path.

## Chart Rules

- Use direct titles: "Rows with official poverty source by join type", not generic titles.
- Put unit and year in the subtitle.
- Use restrained color. Highlight only the main comparison or gap.
- Add a note for source exclusions, missing rows, proxy denominators, or uncertainty flags.
- For maps, explicitly state that boundaries/designations do not imply a legal-status judgment.
- Never let a proxy chart imply welfare, demand, access, or impact unless independently measured.

## Claim Hygiene

Before finalizing, check:

- Does the headline come directly from generated artifacts?
- Are source gaps visible, not hidden in footnotes?
- Is the method described before the finding is generalized?
- Are proxy variables named as proxies?
- Is "what this does not mean" included for any public-facing research output?
- Are downloadable evidence files or reproduction commands linked?

## References

Read `references/source-patterns.md` when asked to justify the style, audit a draft against ADB/ERDI examples, or build a new template from the source pattern.
