# Owner-led review brief — Sylhet observed-flood route pilot

`attestation_chain: ai-first` · No external reviewer contacted

## Review decision requested

Should the issue remain a PP construct-validation pilot, or is there sufficient
human-verified source and domain evidence to advance it under Constitution
§18.5?

## Please verify

1. **UNOSAT interpretation:** confirm that the downloaded flood and analysis
   shapefiles are the intended layers for product 3888 and that the 144.5 km²
   versus “about 134 km²” disagreement is represented fairly.
2. **Passability model:** judge whether any-water-plus-buffer removal is
   acceptable as a stress-test counterfactual and not as observed closure.
3. **Market inventory:** compare the eight deduplicated OSM destinations with a
   local or official market registry, including informal markets and event-day
   operation.
4. **Boundary:** assess whether restricting roads and markets to the UNOSAT
   footprint is appropriate or whether a larger, fully observed flood surface is
   needed to represent outbound bypasses.
5. **Population:** confirm the WorldPop product, vintage, license, and use of the
   unconstrained raster.
6. **OpenStreetMap:** verify ODbL attribution and the historical Overpass query.
7. **Claim language:** confirm that “modeled disconnection” is never shortened
   to closure, isolation, impact, or welfare loss without qualification.

## Reproduce before review

```powershell
python flood-market-access/scripts/build-sylhet-route-pilot.py
python flood-market-access/scripts/build-figure-dossier.py
```

Expected base result: 345,718 modeled people disconnected, 41.24% of
baseline-accessible population; 38.92%–43.45% across 54 variants.

## Hard wall

Reviewer identity and outreach require owner action. This repository records the
brief but does not name, contact, or simulate an external reviewer.
