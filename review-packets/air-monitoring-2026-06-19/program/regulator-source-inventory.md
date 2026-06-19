# Regulator-source inventory discovery pass

`attestation_chain: ai-first`

This pass moves the air-monitoring program from OpenAQ-only station metadata
toward national-source validation. It does not validate monitor grade or prove
that any economy has, or does not have, a monitor outside OpenAQ. It records
which public regulator, official portal, government project, or development
partner sources should be inspected before the article makes any stronger
station-coverage claim.

## Why this measurement problem matters

The OpenAQ station-source pass made the public sensor geography visible, but
OpenAQ is not a national regulator inventory. A zero row in OpenAQ may mean no
public feed is present in OpenAQ, not that the economy has no station. The next
reader-facing claim therefore needs a source audit: does a regulator or
official portal expose station metadata, station counts, PM2.5 measurement
status, or monitor-grade distinctions?

## Source added

The seed file `source-inputs/regulator-source-inventory-seed.csv` records one
first-pass source candidate or targeted-search gap for each of the 24
non-panel-context economies in the metadata upgrade queue. The script
`scripts/build-regulator-source-inventory.py` joins that seed back to
`generated/air-monitoring-openaq-station-metadata-summary.json`, checks URL
retrieval status, and writes:

- `generated/air-monitoring-regulator-source-inventory.csv`
- `generated/air-monitoring-regulator-source-inventory-summary.json`

The source list is intentionally conservative. A candidate source is a source
to inspect, not validated station coverage.

## What the discovery pass found

Generated at `2026-06-19T06:50:40Z`, the pass covers all 24 upgrade-queue
economies.

| Gate | Count |
|---|---:|
| Upgrade-queue economies targeted | 24 |
| Official regulator or portal source candidates | 11 |
| Official station inventory or air-quality portal candidates | 9 |
| Official station-count claim rows | 6 |
| Monitor-grade classification rows | 0 |
| Zero-OpenAQ economies targeted | 13 |
| Zero-OpenAQ economies with official inventory or portal candidate | 1 |
| Zero-OpenAQ economies with official regulator page but no station inventory found | 2 |
| Zero-OpenAQ economies with development-partner monitoring reference | 1 |
| Zero-OpenAQ economies still targeted-search gaps | 9 |
| URL rows tested | 13 |
| URL rows retrieved by script | 10 |
| URL rows with retrieval errors | 3 |

High-signal source candidates include:

- Bangladesh Department of Environment, [Ambient Air Quality in Bangladesh](https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-doe/2024/12/014a6e225cf849098389d835538afdc9.pdf), with a national monitoring-network table and PM2.5 coverage.
- Uzbekistan Uzhydromet, [Interactive map of atmospheric air quality](https://monitoring.meteo.uz/en/map), with stationary pollution observation points, automatic stations, and PM2.5 categories.
- Georgia National Environment Agency, [ambient air-quality monitoring station notice](https://nea.gov.ge/En/News/1287), with an official network count and PM2.5 monitoring statement.
- Sri Lanka Central Environmental Authority, [Air Quality Monitoring](https://www.cea.lk/web/en/air-quality), with automated ambient stations, PM2.5 pollutant coverage, and sensor units under test.
- Indonesia BMKG, [PM2.5 particulate concentration portal](https://www.bmkg.go.id/kualitas-udara/pm25), with current official PM2.5 location readings.
- Malaysia Department of Environment, [MyEQMS](https://eqms.doe.gov.my/), with an official ambient air-quality monitoring portal.
- Tajikistan Hydrometeorology Agency, [official air-pollution explanation](https://www.meteo.tj/en/news/2026/04/04/-351), with an official Dushanbe monitoring-station statement.
- Brunei Department of Environment, Parks and Recreation, [air-quality management page](https://www.env.gov.bn/SitePages/Air%20Quality%20Management%20in%20Brunei%20Darussalam.aspx), with a PM2.5 monitoring signal, although scripted retrieval needs follow-up.

## Interpretation

The source-discovery result changes the next loop. The strongest near-term
path is not a wider map; it is reconciliation. Bangladesh, Georgia, Sri Lanka,
Uzbekistan, Tajikistan, Indonesia, Malaysia, Myanmar, and Brunei now have
candidate official or government source paths to inspect against OpenAQ rows.
The evidence is still not ready for monitor-grade language because no source
in this pass gives a complete reference-grade or regulatory-grade
classification for the OpenAQ station rows.

For the 13 zero-OpenAQ economies, the result is mixed. Brunei has an official
air-quality portal candidate. Fiji and Palau have official environmental
regulator pages but no station inventory found in this pass. Vanuatu has a
development-partner monitoring reference, not a regulator station inventory.
Nine zero-OpenAQ economies remain targeted-search gaps. Those gaps are not
evidence that monitors do not exist; they are the next source-collection work
queue.

## What this does not mean

- It is not a regulator-validated station inventory.
- It is not monitor-grade or reference-grade validation.
- It is not proof that zero-OpenAQ economies have no monitor.
- It is not a reconciliation between official station counts and OpenAQ rows.
- It is not station-radius or population-catchment coverage.

## Reproduce

```bash
python air-monitoring/scripts/fetch-openaq-station-metadata.py
python air-monitoring/scripts/build-regulator-source-inventory.py
```

The next step is to extract station tables or portal data from the official
candidate sources, normalize station names and coordinates, and compare them
against OpenAQ station rows before widening the public claim.
