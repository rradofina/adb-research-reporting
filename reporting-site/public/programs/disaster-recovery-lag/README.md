# Disaster Recovery Lag

## Research Question

Which places appear to recover slowly after disasters, even when national GDP or
headline reconstruction indicators rebound?

## Why This Is Unconventional

Disaster recovery is often measured through losses and aid flows. This track
looks for lagging recovery signals in public geospatial and socioeconomic data.

## Available Data

- EM-DAT disaster events and impacts
- IDMC displacement data
- VIIRS nighttime lights as a proxy benchmark
- GHSL built-up change
- World Bank WDI macro and poverty indicators
- OpenStreetMap road and service restoration proxies where edit history is useful

## First Pipeline

1. Select recent major disaster events in ADB economies.
2. Build before/after proxy panels using lights, settlement, and population data.
3. Compare recovery proxies with event severity and socioeconomic exposure.

## Outputs

- `generated/disaster-recovery-lag-pilots.csv`
- Event-level recovery-lag dashboard
- Caveat register for proxy interpretation

## Reproducibility Notes

Proxy recovery is not a welfare measure. Treat it as a triage layer until
validated against household, infrastructure, or official recovery data.
