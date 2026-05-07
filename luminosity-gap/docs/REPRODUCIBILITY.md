# Reproducibility Standard

This project should be readable as a research artifact, not only as a web app.
Every claim needs a visible chain from source to script to generated output.

## Claim Maturity Labels

- Hypothesis: a research idea, literature gap, or proposed metric. It can be
  AI-assisted, but it is not a finding.
- Prepared pipeline: a download script, manifest, SQL file, or source plan
  exists. The repo is ready to compute, but no empirical value is claimed.
- Screening result: a script has run and produced pilot data. The output can
  guide next work, but it remains preliminary.
- Publication-ready result: source retrieval, code, sensitivity checks,
  caveats, and claim scope have all been reviewed.

## Minimum Evidence Packet

Every computed table or map should document:

- source name, owner, URL, license/access note, and retrieval date or source
  timestamp;
- exact command used to generate the artifact;
- input filters such as ISO code, year, quarter, bounding box, scenario, or
  admin level;
- output path and schema;
- known caveats and what the result should not be used to claim;
- human checks performed after generation.

## Current Rerun Commands

```bash
npm install
npm run research:access
npm run research:ookla
npm run research:openaq
npm run lint
npm run build
```

## Program Status

| Program | Current artifact | Claim scope |
| --- | --- | --- |
| Climate-Adjusted Access to Services | `src/data/generated/access-services-pilots.json`, `src/data/generated/access-services-admin1.json`, `src/data/generated/access-services-nextwave-admin1.json`, `src/data/generated/access-services-frontier-admin1.json`, `src/data/generated/access-services-computed-admin1.json`, and `src/data/generated/access-services-adb-scaleout.json` | National and ADM1 screening result for 104 ADM1 units across 8 ADB economies, plus ADB regional scale-out readiness; not yet travel-time access |
| Measured Digital Development Gap | Ookla manifest JSON and DuckDB SQL | Prepared pipeline; no final speed aggregates yet |
| Air Pollution Without Air Monitors | OpenAQ API-run JSON and CSV | Best-effort public monitor metadata, population denominators, WDI PM2.5 exposure, and WHO city PM2.5 validation for ADB regional member economies |
| Invisible Urbanization | Research README and method page | Hypothesis and source-backed design only |

## Handling Large Data

Do not commit raw global rasters, full Ookla parquet files, or large vector
extracts. Commit the reproducible retrieval path instead:

- source URL or API endpoint;
- exact query/filter;
- schema or expected columns;
- summary output location;
- local cache path convention when needed.

## Review Gates

Before a result is presented as more than a pilot:

1. Rerun the script from a clean shell.
2. Confirm source URLs and timestamps still work.
3. Compare output magnitude against at least one independent reference or
   plausibility check.
4. Run `npm run lint` and `npm run build`.
5. Update the relevant `research/<program>/README.md` with the run date,
   source status, and limitations.

## Reference Points

- The Turing Way: https://book.the-turing-way.org/
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- OECD AI transparency and explainability principle: https://oecd.ai/en/dashboards/ai-principles/P7
- ADB Responsible AI technical controls challenge: https://challenges.adb.org/en/challenges/extensible-responsible-ai-technical-controls-evaluator?lang=en
