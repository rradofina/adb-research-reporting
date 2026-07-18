# Coverage — what is available and what is observed

`attestation_chain: ai-first`

## Source coverage

| Layer | Coverage used | What it contributes | What it lacks |
|---|---|---|---|
| EM-DAT profiles | 38 ADB DMCs, 2000–2025 | Country burden totals | Event geometry in the cached profile workbook |
| GDIS | 609 IDs / 565 disaster numbers / 2,881 DMC locations, 2012–2018 | Administrative units and centroids | True hazard or damage footprint; post-2018 events |
| Light Every Night | Six fixed dates monthly, May 2013–Oct 2014 | Quality-filtered daily radiance | Continuous all-night coverage and welfare outcomes |
| Natural Earth | 1:50m country polygons | Gross coordinate screen | Subnational boundary validation |

## Haiyan observation coverage

The design schedules 108 satellite dates. Availability is evaluated as paired
affected-centroid and Manila-reference observations, not silently filled with
nearby dates. Valid main-specification baseline months range from one to four:
Aklan 1; Capiz 3; Cebu 3; Iloilo 3; Leyte 2; Palawan 3; Samar 4. Only Samar
reaches the four-month minimum in the positive rule.

Coverage loss comes from orbit swath, quality flags, valid-pixel minimums, and
the same-orbit reference requirement. A blank month means no valid scheduled
pair under the frozen rules, not zero luminosity.

## Population denominator warning

The events-per-million inversion uses 2024 WDI population against cumulative
2000–2025 EM-DAT counts. It is an indicative scale check, not an annualized
population-exposure rate. A final rate would require year-specific population,
consistent exposure windows, and event-level denominators.
