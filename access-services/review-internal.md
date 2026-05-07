# Internal review — Access to Services

`attestation_chain: ai-first`. §18 critique-pass. Closed 2026-04-27.

## Critique

1. 8 DMCs is a thin pilot. The headline doesn't extend to the 42
   other ADB DMCs — explicitly out-of-scope.
2. OSM facility-count is a proxy for service availability. Travel-
   time isochrones to nearest facility (via OpenRouteService or
   similar) is the actionable measure.
3. Population-weighted aggregation rewards large-population countries;
   per-capita ADM1 stress would surface different DMCs.

## Responses

1. Documented in `coverage.md`. §18.5 upgrade-pass extends to all 50.
2. Travel-time isochrones are the §18.5 upgrade-pass.
3. Honest narrowing — top-4 survives both aggregations.
