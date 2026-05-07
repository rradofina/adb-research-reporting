# ADB/ERDI Writing Audit for Blindspots Research Briefs

Date checked: 2026-04-29  
Purpose: align the repository's research presentation with ADB/ERDI/Data Division practice while making AI assistance transparent rather than hidden.

## Sources Checked

1. ADB Handbook of Style and Usage, 2024 edition. Official ADB style source. It points authors to clear, accurate, short prose; Chicago-style publication references; complete source notes for figures and tables; and ADB member-name rules.
   Source: https://www.adb.org/sites/default/files/institutional-document/31385/hsu-2024.pdf

2. ADB Data Library About page. It defines the Data Library as ADB's public-data platform, with machine-readable, shareable, API-accessible datasets; it also states that flagship macro and social data come from publications such as Asian Development Outlook, Key Indicators, and Basic Statistics.
   Source: https://data.adb.org/about

3. ADB Data Library home page. It presents datasets, dashboards, and data stories as separate reading surfaces. This supports a UI split between data catalog, chart-first research briefs, and longer findings.
   Source: https://data.adb.org/

4. ERDD / ERDI training-course page. It describes the Data Division as supporting statistical capacity building, annual publications, methodological research, statistical databases, and data services, including advanced data tools and non-traditional sources for policymaking and research in DMCs.
   Source: https://elearn.adb.org/course/view.php?id=511

5. Key Indicators for Asia and the Pacific 2025. The public page frames the report as updated economic, financial, social, environmental, and SDG indicators, with a Part I analytical theme and Part II statistical tables by economy.
   Source: https://seads.adb.org/publication/key-indicators-asia-and-pacific-2025

6. Key Indicators for Asia and the Pacific 2023. The public page frames the volume around updated statistics, clear parts, regional coverage, and SDG / data-story structure. The PDF acknowledgments identify the Statistics and Data Innovation Unit within ERDI and name Arturo Martinez Jr. as publication lead.
   Source: https://seads.adb.org/publication/key-indicators-asia-and-pacific-2023
   PDF: https://www.adb.org/sites/default/files/publication/900716/ki2023.pdf

7. Mapping Poverty through Data Integration and Artificial Intelligence, special supplement to Key Indicators 2020. The acknowledgments identify Arturo Martinez Jr. as publication lead and coauthor. The structure is especially relevant: foreword, highlights, practical statistical motivation, data requirements, method explanation, figures, notes, and caveats.
   Source: https://www.adb.org/sites/default/files/publication/630406/mapping-poverty-ki2020-supplement.pdf

8. Introduction to Small Area Estimation Techniques: A Practical Guide for National Statistics Offices. The acknowledgments identify Arturo Martinez Jr. as leading publication work and show the Data Division style for practical NSO-facing methods.
   Source: https://www.adb.org/sites/default/files/publication/609476/small-area-estimation-guide-nsos.pdf

9. Practical Guidebook on Data Disaggregation for the Sustainable Development Goals. The guidebook shows the Data Division / UN statistics style: concepts, policy demand, sources, limitations, dissemination, and capacity-development resources.
   Source: https://www.adb.org/sites/default/files/publication/698116/guidebook-data-disaggregation-sdgs.pdf

10. Thegeya, Mitterling, Njoroge, Martinez Jr., Iddawela, Bulan, Durante, Garonita, and Mag-atas, "Evaluating the effectiveness of satellite image super-resolution for road quality monitoring," Scientific Reports, published 16 April 2026. This is a useful current example of Arturo Martinez Jr. / ADB-associated frontier-method writing: it starts from infrastructure data scarcity, tests a plausible AI improvement, reports the limited result plainly, and then identifies the data-fusion path that worked better.
    Source: https://www.nature.com/articles/s41598-026-47749-3

## What ADB/ERDI Writing Looks Like

ADB/ERDI writing is not academic flourish. It is data-service writing:

- Start with what the reader can use: purpose, coverage, data source, and policy relevance.
- Use a short Highlights or key-messages layer before the full method.
- Treat tables and figures as independent objects: title, abbreviations, notes, footnotes, and source below the figure/table.
- State coverage explicitly: economies, years, granularity, update frequency, and missing-data symbols.
- Avoid overclaiming. Distinguish "data show," "screening suggests," "estimates indicate," and "this cannot establish."
- Name units and denominators. Prefer percentages, shares, counts, ratios, and year labels that can be traced.
- Use ADB member names and DMC framing carefully. Do not turn a measurement gap into a country-quality judgment.
- Keep prose plain. The style handbook favors short words, active voice, short paragraphs, precision, and no cliches.

## Arturo Martinez Jr. / Data Division Pattern

The relevant pattern in Arturo Martinez Jr.-associated work is practical statistics for policy use:

- Granularity matters, but the report explains what makes higher granularity feasible and what investment or validation is needed.
- Nontraditional data sources are treated as supplements to official statistics, not replacements.
- The audience includes national statistics offices and policy users, so the method explanation is technical enough to audit but written in a usable order.
- The publications foreground teams, statistical partners, proofreading, data compilation, and source accountability. This is the opposite of a black-box AI output.
- Outputs often pair a data story with statistical tables or appendixes. The story makes the policy signal readable; the tables preserve auditability.

The 2026 road-quality super-resolution article is especially important for this repository's tone. It does not say "AI makes road monitoring solved." It asks whether a specific technical upgrade improves prediction, reports that visual enhancement did not improve the classification task, and then points to contextual covariates and validation as the more useful path. That is the standard: test the frontier method, say when it fails, and show what data investment actually improves the policy screen.

## Problem-Selling Formula

ADB-facing writing should sell the problem in this order:

1. Policy decision at risk: what investment, targeting, monitoring, or service decision is currently weak.
2. Measurement blind spot: what the official or public data cannot see at the needed unit.
3. Existing data unit: country, province, city, municipality, grid cell, facility, road segment, market, school, or port.
4. Available source stack: the public, official, modeled, remote-sensing, survey, or administrative sources used.
5. Contribution: what this paper adds as a measurement screen, data integration, validation, or decision-support layer.
6. Non-claim: what it does not prove, rank, replace, or establish causally.
7. Next data investment: what validation, administrative linkage, survey, or local data partnership would make it stronger.

Standard opening paragraph template:

`[Policy problem] depends on decisions made at [unit], but most comparable data are still reported at [higher unit] or with [lag / missingness / proxy limitation]. This brief assembles [source stack] to measure [specific gap] across [coverage] during [period]. The result is a screening layer for [decision/user], not an official statistic or causal estimate. It identifies where [next validation / data partnership] would most improve targeting and monitoring.`

## ADB/ERDI Paper Archetypes

Use the right form for the maturity of the topic:

- ADB Brief: best for a policy-facing result with one strong chart, clear caveats, and an action-oriented next step.
- Key Indicators-style data story: best for descriptive indicators, comparative tables, regional context, and chart-first public communication.
- ADB Economics Working Paper: best when there is a defensible method, literature contribution, robustness section, and enough data to sustain a full argument.
- Data Division guide/toolkit: best when the contribution is a method that NSOs, ministries, or ADB sector teams could reproduce.
- Dataset note: best when the main value is coverage, harmonization, schema, granularity, and refreshability.

## Reference and Source Standard to Use Here

For ADB-facing research briefs:

- Use BibTeX keys in repository articles where the renderer resolves references.
- For ADB-style PDF or Word drafts, use ADB/Chicago footnote form:
  `Asian Development Bank. Year. Title in Italics.`
- For external books and papers:
  `Author. Year. Title in Italics. Publisher.`
- For journal articles:
  `Author. Year. Title of Article. Journal Title. Volume (Issue). pages.`
- For online databases, give the database name and access date:
  `World Bank. World Development Indicators (accessed DD Month YYYY).`
- Never use a bare URL as the only reference. A URL is retrieval aid, not the citation.
- Every chart and table needs a source note directly underneath it.

Figure/table source note template:

`Source: Author calculations using [dataset/source], [years], accessed [date]. Notes: Unit = [unit]; coverage = [economies/geographies]; missing data = [rule]; values are [official/modelled/proxy/screening] and should not be interpreted as [non-claim].`

## One-Page Brief Structure

Use the same structure for every topic:

1. Title: topic name, not a hype headline.
2. Status chip: Publication-ready, Screening result, Prepared pipeline, or Hypothesis.
3. Question: one sentence.
4. Chart: the one visual that makes the signal legible before reading.
5. What is finished: exact claim or exact non-claim.
6. Source stack: datasets, years, granularity, and retrieval path.
7. Caveat: the most important reason not to overread the result.
8. Next step: what would move the topic to the next maturity level.
9. Links: write-up and evidence packet.

## Chart Rules

Each topic should have one primary chart. Use the chart type that fits the claim:

- Stable top-set claim: horizontal bar chart plus "set stability" note.
- Coverage gap: two-bar registry-vs-map comparison or gap bar.
- Pipeline-only topic: no fake chart; show a pipeline-state panel.
- Hypothesis topic: no data chart; show source stack and missing empirical layer.
- Cross-program scan: matrix or small multiples, labeled as triage only.

Every chart must include:

- Units.
- Year or period.
- Geography.
- Source line.
- Caveat line if the data are imputed, sparse, modeled, or proxy-only.

## Anti-AI-Doubt Checklist

To remove doubt that the work is "just AI," every page should surface the audit trail:

- Public source names and retrieval dates.
- Code path or evidence-packet link.
- Sensitivity status: passed, narrowed, failed, or not applicable.
- Attestation chain: ai-first, mixed, or human-final.
- Clear non-claims.
- Reference list or source note.
- No unsupported ranking language.

## UI Implication

The site should not make readers hunt through long write-ups to understand maturity. The correct UX is:

- Home: issue-level summary.
- Research Briefs: all topics, finish state, chart, caveat, next step.
- Research: domain index.
- Findings: long-form write-ups.
- Evidence packet: audit trail.
- Data catalog: source and generated-data access.

This is why the new `Research Briefs` route label exists.

## Repository Writing Skill

Use `.claude/skills/adb-erdi-paper-framing.md` before drafting ADB-facing briefs, working papers, methods notes, or dataset notes. The skill forces the issue statement, key messages, evidence spine, figure/table plan, caveat box, policy-use paragraph, and source notes to exist before prose expansion.
