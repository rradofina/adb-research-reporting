# Measured Digital Development Gap

## Purpose

Separate official connectivity from usable connectivity. A person can be
counted as an internet user or be inside nominal coverage while still having
slow, unstable, high-latency, or unmeasured access.

## First Testable Claim

In selected ADB member economies, official internet-use or broadband indicators
overstate the share of people who have connection quality good enough for
school, telehealth, cloud work, digital finance, or platform commerce.

## Source Stack

- Speedtest by Ookla Open Data: fixed and mobile tile-level download speed,
  upload speed, latency, test counts, devices, and quadkeys.
- ITU ICT statistics: official country-level connectivity and subscription
  indicators.
- World Bank WDI `IT.NET.USER.ZS`: reproducible official internet-use baseline.
- WorldPop or GHSL population grids: population-weighted performance metrics.
- Overture places and transportation: context around schools, clinics, towns,
  firms, and corridors.
- ADB Data Library: regional metadata and ADB-relevant ICT/economic indicators.

## Pilot Economies

Philippines, Indonesia, India, Bangladesh, Nepal, Pakistan, Thailand, Viet Nam,
Kazakhstan, and Georgia.

## First Implementation Pass

1. Download one recent mobile and fixed Ookla quarter for pilot economies.
2. Convert tiles to GeoParquet if needed and keep fixed/mobile schemas separate.
3. Intersect tiles with population grids and admin boundaries.
4. Compute population-weighted download, upload, latency, tests, and devices.
5. Define threshold scenarios for online learning, telehealth, and cloud work.
6. Join official internet-use and subscription indicators.
7. Classify regions as usable, low-quality, unmeasured, or high-performing.

## Current Pipeline Artifact

Run:

```bash
npm run research:ookla
```

Current outputs:

- `src/data/generated/digital-performance-ookla-pilots.json`
- `public/data/digital-performance-ookla-pilots.json`
- `research/digital-performance/generated/ookla-mobile-2026-q1.sql`
- `research/digital-performance/generated/ookla-fixed-2026-q1.sql`

The script writes a download manifest and DuckDB SQL for Philippines and
Bangladesh bounding-box aggregation. It does not download global Ookla parquet
files by default because those files are large. To download, set:

```bash
OOKLA_DOWNLOAD=1 npm run research:ookla
```

The generated SQL can be run with DuckDB and `httpfs` support.

## Reproducibility and AI Transparency

Claim scope: prepared pipeline. The repo has a manifest and SQL scaffold, but
it does not yet claim final speed, latency, device, or test-density results.

Rerun command:

```bash
npm run research:ookla
```

Optional large download:

```bash
OOKLA_DOWNLOAD=1 npm run research:ookla
```

Evidence packet:

- Inputs: Ookla fixed/mobile quarterly open-data URLs and pilot economy
  bounding boxes.
- Outputs: generated JSON manifests and DuckDB SQL under
  `research/digital-performance/generated/`.
- Source metadata: year, quarter, access mode, and pilot filters are written
  into the manifest.
- UI disclosure: the program page states that the Ookla pipeline is ready, not
  that measured aggregates are complete.

AI assistance disclosure:

- AI helped draft the manifest script, DuckDB SQL scaffold, UI panel, and
  documentation.
- AI did not generate or estimate speed-test values.
- The SQL must be validated against the actual Ookla parquet schema after a
  download run.

Human checks completed:

- Manifest generation ran locally.
- The generated status artifact is rendered on the digital-performance page.
- Lint and build passed after wiring the artifact into the UI.

## Metrics

- Usable Connectivity Share: population in tiles meeting quality and
  measurement-density thresholds.
- Official-Performance Gap: official access minus measured usable access.
- Measurement Desert: population in places with too few tests or devices to
  judge quality.

## Validation

- Compare fixed and mobile separately.
- Check capital versus non-capital regions and island/interior regions.
- Treat low test density as a separate result, not as zero connectivity.
- Test thresholds against multiple use cases rather than one arbitrary speed
  cutoff.

## Known Weak Points

Ookla data is not a random sample. It is strongest as a quality and measurement
availability layer, not as a perfect census of connectivity. The measurement
desert metric is therefore essential, not optional.
