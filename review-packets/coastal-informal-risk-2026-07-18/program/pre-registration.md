# Design freeze — low-elevation urban growth

`attestation_chain: ai-first` · Frozen before the GHS-UCDB V1.2 pull on
2026-07-19.

## Question

Which urban centres in ADB developing economies added the most population and
built-up surface inside the low-elevation coastal zone from 2000 to 2020, and
does that settlement-scale pattern resemble the inherited national proxy?

## Unit and population

The unit is a quality-controlled GHS-UCDB fixed-2025-boundary urban centre.
The analysis population is every centre whose country ISO code maps to the
repository's ADB developing-economy roster and whose required 2000 and 2020
LECZ fields are nonmissing. A centre enters the low-elevation analysis when its
population below 10 metres is positive in either endpoint. No missing value is
imputed.

## Primary estimands

1. Absolute change in population below 10 metres, 2000–2020:
   `(EX_L05_POP_2020 + EX_L10_POP_2020) -
   (EX_L05_POP_2000 + EX_L10_POP_2000)`.
2. Absolute change in built-up surface below 10 metres over the same period:
   `(EX_L05_BUS_2020 + EX_L10_BUS_2020) -
   (EX_L05_BUS_2000 + EX_L10_BUS_2000)`.
3. The overlap between the top five centres' economies and the inherited
   national proxy's top-five economy set. This overlap is a falsification
   comparison, not a validation target.

## Sensitivity and alternate views

- **Elevation definition:** below 5 metres versus below 10 metres.
- **Window length (arbitrary numeric choice):** 10, 20, and 30 years ending
  in 2020. These are the required −50%, baseline, and +50% variants around the
  20-year window.
- **Scale:** centre-level absolute change, economy-aggregated absolute change,
  and change in the low-elevation share of centre population.
- **Quantity:** population and built-up surface are reported separately; they
  are never multiplied into a composite index.

## Decision rules

The hook passes to a full program package only if:

1. at least 75% of DMC urban centres in the source have complete 2000/2020
   population and built-up LECZ fields;
2. at least 25 centres have positive below-10-metre population in an endpoint;
3. the hero chart can name centres rather than only economies; and
4. the claim remains descriptive of observed GHSL/LECZ quantities and does
   not infer informality, inadequate protection, legal status, welfare loss,
   or policy failure.

The ranking need not be stable across elevation definitions or time windows.
Instability is a substantive result and must be shown.

## Source and version custody

- GHS-UCDB R2024A thematic files, V1.2, retrieved 2026-07-19.
- Dataset DOI: `10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd`.
- GHS-POP R2023A supplies population; GHS-BUILT-S R2023A supplies built-up
  surface; the LECZ mask is derived from CIESIN/CIDR SEDAC LECZ Version 3.
- Acquisition records the download URL, byte count, SHA-256, archive members,
  and retrieval timestamp.

## Claim limits fixed in advance

Fixed 2025 urban-centre boundaries make the time comparison spatially
consistent but do not reconstruct the historical boundary of the settlement.
The LECZ is an elevation-and-coastal-zone screen, not a flood-depth, storm-
surge, subsidence, protection, or loss model. Remote sensing cannot identify
informal tenure or whether infrastructure and services are adequate.
