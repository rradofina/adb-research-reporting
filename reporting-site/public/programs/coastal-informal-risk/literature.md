# Literature review — low-elevation urban growth

`attestation_chain: ai-first` · Updated 2026-07-19

## Evidence spine

McGranahan, Balk, and Anderson defined the Low Elevation Coastal Zone as the
contiguous coastal land below 10 metres and showed why population concentration
in that zone matters for climate policy [@mcgranahan2007rising]. Neumann and
co-authors later separated demographic change in the LECZ from modeled coastal
flood exposure under sea-level and socioeconomic scenarios
[@neumann2015coastal]. That distinction governs this study: elevation-zone
population is an exposure object, not a flood-probability or loss object.

GHS-UCDB provides a globally harmonized way to study named urban centres. The
database integrates open geospatial sources into comparable centre extents and
multi-temporal attributes [@melchiorri2024ucdb]. The R2024A V1.2 release used
here contains 11,422 quality-controlled urban centres and exposes population
and built-up-surface fields below 5 metres and from 5 to 10 metres
[@jrc2026ucdb]. Fixed 2025 footprints permit within-boundary comparison across
epochs, while also limiting the interpretation: the analysis does not measure
the outward movement of the city boundary.

The IPCC frames coastal risk as the interaction of hazards, exposure,
vulnerability, and adaptation [@ipcc2022coastalcities]. A LECZ count observes
only part of that chain. Storm surge, relative sea level, subsidence, coastal
protection, and social vulnerability can differ sharply among cities at the
same elevation.

Finally, Earth observation does not by itself establish informality. Kuffer and
co-authors show that remotely sensed morphology can support deprived-area
mapping, but slum and inadequate-housing indicators also depend on tenure,
services, durability, and local context [@kuffer2018slumindicator]. The present
study therefore removes “informal” from its measured claim.

## Contribution

The contribution is not a new risk index. It is a reproducible measurement
study that:

1. replaces a national, imputation-heavy proxy with a direct urban-centre LECZ
   object;
2. quantifies 2000–2020 population and built-up change in reported centres;
3. shows how rankings change when the construct becomes spatial;
4. tests the elevation definition and time window;
5. makes blank-field and small-island coverage failures visible.

## Open research gap

A policy-ready next stage would join the centre polygons to local relative
sea-level or storm-surge surfaces, protection standards, subsidence, and
validated settlement-deprivation data. Those additions would create a risk
study; this paper deliberately stops at exposure growth.

