# Internal review — Sylhet observed-flood route pilot

`attestation_chain: ai-first` · Adversarial pass 2026-07-19

## Verdict

**Advance as PP construct validation; do not promote to decision-grade closure
or impact analysis.** The routed result is reproducible and stable, but the
common closure assumption and market inventory remain unvalidated.

## Finding audit

- The headline traces to the committed script, JSON, sensitivity CSV, public
  sources, retrieval dates, and SHA-256 hashes.
- The 41.24% denominator is baseline-accessible covered population, not the
  entire footprint and not the population of Sylhet District.
- All 54 required variants produce 38.92%–43.45% modeled disconnection.
- The former country proxy is explicitly retired rather than used as supporting
  evidence.

## Defects found and corrected

The first computed graph used the rectangular Overpass query box. The route map
showed markets and possible bypass roads outside the tilted UNOSAT footprint.
The pipeline was corrected to retain only destinations and full road segments
inside the observed analysis polygon, then all 54 variants were recomputed. The
base estimate moved from 41.26% to 41.24%, so the finding survived the spatial
eligibility correction.

Repeated flood–road intersection work also made the first pipeline
unnecessarily slow. Spatial indexing and scenario caching reduced the final
end-to-end route computation to about two minutes without shrinking the grid.

## Remaining threats

1. **Passability:** water intersection is not closure; depth and road/bridge
   elevation are absent.
2. **Destination completeness:** eight OSM markets are not independently
   validated.
3. **Boundary:** real trips can leave and re-enter the footprint.
4. **Population timing:** WorldPop 2020 is modeled and predates the event.
5. **Behavior:** no trip choice, boat travel, market operating status, prices,
   or welfare outcome is observed.
6. **Source disagreement:** the flood SHP yields 144.5 km² versus about 134 km²
   on the product page.

## Presentation audit

The figure sequence communicates the result, sensitivity, denominators, market
gate, source disagreement, road-set alternative, selection effect, and claim
limits. The route map directly caused a model correction, so it is analytical,
not decorative. Text and figures use finding-first titles and keep the
mechanical-counterfactual warning visible.

## Required next gate

An owner-led human review should verify UNOSAT interpretation, OSM/WorldPop
licensing and attribution, the plausibility of the road/passability model, and
the local market inventory. No external reviewer was contacted.
