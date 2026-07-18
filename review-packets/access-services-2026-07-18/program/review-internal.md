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

## 2026-07-18 claim-reshape critique pass

The earlier response to objections 2 and 3 was not sufficient. Testing a
second aggregation while retaining the same OSM denominator cannot establish
robust access ranks. The committed registry deepening now shows that 16 of 17
Philippine regional ranks change, so the old headline is retired.

Further critique and resolution:

1. **Could registry counts simply be another imperfect source?** Yes. The
   paper does not declare the registry a full access measure; it uses the
   registry to show that the OSM denominator cannot sustain the exact rank.
2. **Is the completeness association causal?** No. The paper calls it a
   source signal and reports both rank movement and correlation without causal
   language.
3. **Does Cambodia validate the result?** No. The 2010-versus-2026 comparison
   is reported as source/vintage disagreement. Phnom Penh's reversed count
   relationship is made visible as a warning.
4. **Is the 50% reshape threshold arbitrary?** Yes. The decision is rerun at
   25% and 75%; the Philippine conclusion is unchanged.
5. **Can the eight-economy rank be corrected?** No. Only two economies have a
   comparable registry correction in the committed module. The readiness wall
   makes this missingness part of the public result.

Decision: current PP package passes the AI critique loop only with the new
map-observability framing and explicit non-claims. It does not qualify for
human-final or for service-access language.
