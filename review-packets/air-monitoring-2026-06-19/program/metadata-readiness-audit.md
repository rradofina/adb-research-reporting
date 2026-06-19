# Air-Monitoring Metadata-Readiness Audit

attestation_chain: ai-first

This note records the next evidence gate for the air-monitoring observability
report. The existing deepening already shows that the zero-public-monitor
population headline is concentrated in Papua New Guinea and Timor-Leste, and
that monitor-density patterns are strongly confounded with GDP per capita among
economies with at least one public PM2.5 monitor. The next question is whether
the committed evidence package can support station-radius, monitor-grade,
station-vintage, or regulatory-inventory claims.

It cannot yet. The audit finds no station-level OpenAQ cache in the committed
air-monitoring artifacts.

## Reproduce

```bash
python air-monitoring/scripts/build-metadata-readiness-audit.py
```

The script reads:

- `generated/air-monitoring-adb-panel.json`
- `generated/air-monitoring-concentration-deepening.json`

It writes:

- `generated/air-monitoring-metadata-readiness-audit.csv`
- `generated/air-monitoring-metadata-readiness-audit-summary.json`

## Current Result

| Readiness signal | Count or status |
|---|---:|
| Country-panel rows | 50 |
| Countries with public monitor count | 50 |
| Countries with PM2.5 exposure value | 50 |
| Zero-public-monitor economies above the WHO PM2.5 guideline | 13 |
| Monitored economies with GDP residuals | 33 |
| Baseline gap-score top-five rows | 5 |
| Positive GDP-residual queue rows | 10 |
| Unique upgrade-queue rows | 24 |
| Station-level cache files | 0 |
| Station-coordinate rows available | 0 |
| Monitor-grade rows available | 0 |
| Monitor first-seen rows available | 0 |
| Regulatory-inventory rows available | 0 |
| Station-radius analysis ready | false |

## Evidence Gates

| Gate | Status | Rows | Reader use |
|---|---|---:|---|
| Country-level monitor count and PM2.5 exposure | available | 50 | Initial public observability screen |
| Zero-monitor concentration | available | 13 | Shows the regional zero-monitor total is concentrated |
| GDP-confound residual | available | 33 | Separates monitored economies with more or fewer people per monitor than GDP predicts |
| Station coordinates | blocked by missing station-level cache | 0 | Required for station-radius or population-catchment claims |
| Monitor grade and owner | blocked by missing station-level cache | 0 | Required to distinguish reference-grade/regulatory monitors from low-cost public feeds |
| First-seen timestamp or station vintage | blocked by missing station-level cache | 0 | Required to distinguish long-running gaps from snapshot artifacts |
| Regulatory inventory cross-check | not yet collected | 0 | Required before treating OpenAQ-visible zero as no monitor on the ground |

## Upgrade Queue

The audit keeps the upgrade queue narrow. It flags 24 economies because they
fall into at least one of three evidence needs: the original baseline top-five
gap-score group, the top positive GDP-residual group, or the zero-public-monitor
above-guideline group.

The first queue rows are:

| ISO3 | Economy | Queue class | PM2.5 locations | Gap score | GDP residual |
|---|---|---|---:|---:|---:|
| AFG | Afghanistan | baseline top-five and positive GDP residual | 2 | 100 | 0.5973 |
| BGD | Bangladesh | baseline top-five and positive GDP residual | 20 | 100 | 0.8136 |
| MMR | Myanmar | baseline top-five and positive GDP residual | 3 | 95 | 0.9208 |
| UZB | Uzbekistan | baseline top-five and positive GDP residual | 5 | 94 | 0.8023 |
| TJK | Tajikistan | baseline top-five monitor metadata | 5 | 80 | -0.0169 |
| AZE | Azerbaijan | positive GDP residual monitor metadata | 1 | 75 | 1.2252 |
| LKA | Sri Lanka | positive GDP residual monitor metadata | 3 | 72 | 0.9221 |
| IDN | Indonesia | positive GDP residual monitor metadata | 35 | 68 | 0.9956 |

## Interpretation

The audit changes the next report step. The current evidence can support a
public observability screen, a zero-monitor concentration result, and a
GDP-confound residual view. It cannot support station catchments, monitor-grade
validation, station-vintage analysis, or regulatory-inventory claims until a
station-level source is fetched and versioned.

## Non-Claim

This is an AI-first no-network metadata-readiness audit. It uses only the
committed air-monitoring country panel and GDP-confound deepening artifact. It
is not a station-radius analysis, not a monitor-grade validation, not a
regulatory inventory, not proof that no monitor exists outside OpenAQ, not a
pollution ranking, and not a health-impact estimate.

