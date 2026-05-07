# AI Transparency Note

AI assistance is allowed in this project, but it should be visible, bounded, and
separate from empirical evidence.

## How AI Was Used

AI assisted with:

- brainstorming unconventional ADB-relevant research directions;
- source triage and first-pass literature/source review;
- drafting TypeScript pipeline scripts and UI components;
- writing documentation, caveats, and reproducibility language;
- identifying implementation order and next validation steps.

AI did not serve as an empirical source. Numbers shown in generated artifacts
must come from source APIs, downloaded data, or committed scripts.

## What Must Be Disclosed

Each program should say:

- what was generated or drafted with AI help;
- which outputs were computed by scripts;
- which source links support the claim;
- what was manually checked;
- what remains blocked, unvalidated, or only proposed.

## How To Present This Publicly

Use calm disclosure language:

"AI assisted with source triage, code drafting, and documentation. Empirical
values are generated from the cited data sources through committed scripts.
Preliminary outputs are labeled by claim scope and should not be treated as
publication-ready until the listed validation checks are complete."

Avoid making AI sound like a hidden coauthor or a substitute for review. The
trust point is that the project is auditable: users can see when AI helped and
where the evidence actually comes from.

## Guardrails

- Do not cite AI for facts, data values, or literature claims.
- Do not let AI fill missing source values.
- Do not upgrade a hypothesis to a result because the UI looks polished.
- Do not hide failed runs, missing API keys, or unvalidated schema assumptions.
- Do not publish sensitive or proprietary data through prompts or generated
  artifacts.

## Current Disclosure

The website exposes AI and reproducibility status in:

- `/methodology/reproducibility`
- each `/research/<program>` page under "Reproducibility and AI disclosure"
- the program README files under `research/*`

## Reference Points

- ASEAN AI governance summary on disclosure, data, and purpose: https://seads.adb.org/articles/asean-ai-guidelines-seek-encourage-responsible-use-and-deployment
- OECD AI transparency and explainability principle: https://oecd.ai/en/dashboards/ai-principles/P7
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
