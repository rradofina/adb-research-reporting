# Skill: ADB/ERDI Paper Framing

## Purpose
Turn a topic, result, or dataset into an ADB/ERDI/Data Division-style
research brief, working paper frame, or methods note. The output should
make the policy problem, measurement gap, data stack, chart logic, caveats,
and references clear enough that the work does not read as generic AI prose.

## Invocation
> "Frame `<program-slug>` as an ADB/ERDI-style brief."

> "Write the problem statement and key messages for `<topic>`."

> "Convert this topic into an ADB working-paper outline."

## Inputs to Read
- The program folder: `README.md`, `literature.md`, `scoring.md`,
  `results.md`, `sensitivity.md`, and `generated/` outputs where present.
- `research/adb-erdi-writing-audit.md`
- `reporting-site/src/data/briefs.ts`
- `reporting-site/src/data/sourceUpgrades.ts`
- Any article draft, evidence packet, chart data, or source list named by
  the user.

## Workflow
1. Classify the output type:
   - ADB Brief: policy-facing, 1-2 core charts, short methods box.
   - Key Indicators-style data story: descriptive statistics, chart-first,
     broad country or subnational coverage.
   - Economics Working Paper: full literature, data, method, results,
     robustness, limitations.
   - Data Division guide/toolkit: operational method for NSOs, ministries,
     or ADB teams.
   - Dataset note: source, unit, coverage, schema, caveats, refresh path.
2. Sell the issue, not the tool:
   - Start with the policy decision at risk.
   - Name the measurement blind spot and current reporting unit.
   - Explain why existing data miss the problem.
   - State the decision that better granularity can improve.
3. State the contribution conservatively:
   - Use "This paper provides a screening measure..." or
     "This brief assembles..." instead of "AI discovers..."
   - Separate descriptive measurement from causal claims.
   - Say what the work does not claim before the reader has to infer it.
4. Build the evidence spine:
   - Population or economies covered.
   - Geography level: country, province, city, district, grid cell,
     road segment, facility, market, port, or school.
   - Years, update frequency, source stack, denominators, missingness,
     retrieval dates, and code/evidence path.
5. Plan figures and tables:
   - One visual should make the issue legible immediately.
   - Every figure needs title, unit, geography, year/period, source line,
     and caveat line.
   - Prefer maps, ranked gap bars, small multiples, and uncertainty or
     coverage panels when granularity is the point.
6. Add the caveat ladder:
   - "This is a screening layer, not an official statistic."
   - "This does not establish causality."
   - "This cannot replace engineering inspection / survey validation /
     administrative verification."
   - "The next step is validation against local administrative data."
7. Write the policy-use paragraph:
   - Name the user: ADB sector team, NSO, ministry, city, province,
     municipality, regulator, or project-preparation team.
   - Name the decision: targeting, prioritization, maintenance planning,
     investment screening, monitoring, or survey design.
   - Name the low-level unit where possible.
8. Apply the reference standard:
   - Use BibTeX keys in repository articles.
   - Use ADB/Chicago-style references in PDF/Word drafts.
   - Do not use a bare URL as the only citation.
   - Add access dates for online databases.

## Output Format
Return these sections before drafting full prose:

1. Problem statement
2. Key messages, 3-5 bullets
3. Evidence spine
4. Proposed section outline
5. Figure and table plan
6. Caveat / non-claim box
7. Policy-use paragraph
8. References and source notes to add

## ADB-Style Templates

### ADB Brief
1. Title
2. Key messages
3. Why this matters
4. What the data show
5. Data and methods
6. Limitations
7. Policy use
8. Next data investment
9. Source notes

### Economics Working Paper
1. Abstract
2. Introduction
3. Related literature
4. Data
5. Empirical or measurement design
6. Results
7. Robustness and sensitivity checks
8. Discussion and policy implications
9. Limitations and future data work

### Data Division Guide or Toolkit
1. Problem and statistical demand
2. Definitions
3. Data requirements
4. Step-by-step method
5. Quality checks
6. Worked example
7. Dissemination guidance
8. Appendix and reproducibility materials

## Red Flags
- Hype language such as "AI proves" or "never before seen" without a
  defensible benchmark.
- Causal language without an identification strategy.
- Unsupported rankings of countries or governments.
- Charts without units, year, geography, source, and caveat.
- No missing-data statement.
- No denominator.
- Bare URLs instead of references.
- No distinction between official statistics, proxy measures, and model
  outputs.
