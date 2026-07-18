# Reproduce the Sylhet route pilot

`attestation_chain: ai-first`

## Environment

Python 3 with `geopandas`, `networkx`, `numpy`, `pandas`, `pyproj`, `rasterio`,
`scipy`, `shapely`, `matplotlib`, and `Pillow`.

## Build

From the repository root:

```powershell
python flood-market-access/scripts/build-sylhet-route-pilot.py
python flood-market-access/scripts/build-figure-dossier.py
```

The first command retrieves missing raw files into
`.cache/flood-market-access-sylhet-2024/`, records their byte counts and SHA-256
hashes, constructs two historical OSM road graphs, executes 54 sensitivity
variants, and writes:

- `generated/flood-sylhet-route-pilot.json`
- `generated/flood-sylhet-route-sensitivity.csv`
- `generated/flood-sylhet-markets.csv`

The second command rebuilds ten PNG/SVG figures and the thumbnail metadata.

## Expected assertions

- 54 variants are present.
- Every variant has positive modeled disconnection.
- The base road set is `core`; buffer 20 m; population snap 1,000 m; market
  deduplication 100 m.
- Base disconnected share is approximately 41.24%.
- Sensitivity bounds are approximately 38.92% and 43.45%.
- Eight destinations are snapped in the base graph.
- The UNOSAT potentially affected-road layer clipped to the analysis footprint
  is approximately 252 km, close to the product page's rounded 254 km.

Small software-library differences can alter geometry rounding. A material
change in market count, variant count, or headline range requires investigation
before publication.

## Cache and licensing

The raw UNOSAT zip, historical Overpass response, and WorldPop raster are not
committed because of size and source-specific terms. OpenStreetMap-derived data
requires ODbL attribution. The generated JSON records exact retrieval dates,
URLs, hashes, and the historical query text.
