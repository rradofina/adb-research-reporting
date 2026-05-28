# opensrc — vetted open-source reference material

This directory holds open-source data files and reference pointers used
by the research factory's visualization scripts. It is **read-only
input**: nothing in here is generated; nothing in here is changed by
pipeline runs.

## Why this exists

The visual-first refactor (see `research/visual-first-refactor.md`)
requires each program to render a hero visual from committed data. Many
of those visuals need a world or Asia-Pacific basemap, and several
chart types (chord diagrams, choropleths, small-multiples) depend on
geometry primitives shipped by open-source libraries. Keeping the data
files in-repo means:

1. Hero visuals reproduce from a clean clone with no network access
   (per `CONSTITUTION.md` §11 reproducibility).
2. Per-row retrieval timestamps and sha256 hashes pin the source.
3. AI agents have a local source-of-truth for boundary geometry rather
   than hitting an external CDN on every render.

## Contents

| Path | Contents | Source | License | Retrieved |
|---|---|---|---|---|
| `world-boundaries/ne_110m_admin_0_countries.geojson` | 177 country polygons, ~110 m resolution. Includes ISO_A3, ADM0_A3, NAME, ISO_A2, CONTINENT, REGION_UN, SUBREGION. 838 KB. | Natural Earth via [nvkelso/natural-earth-vector v5.1.2](https://github.com/nvkelso/natural-earth-vector/tree/v5.1.2) | Public domain | 2026-05-19 |
| `world-boundaries/ne_50m_admin_0_countries.geojson` | 242 country polygons, ~50 m resolution. Includes small Pacific island states (Tonga, Samoa, Maldives) absent from the 110m file. 3.1 MB. | Same | Public domain | 2026-05-19 |
| `world-boundaries/countries-110m.json` | TopoJSON of 177 country polygons with numeric UN M49 IDs. ~108 KB. | [world-atlas v2.0.2](https://github.com/topojson/world-atlas) | ISC | 2026-05-19 |
| `REFERENCES.md` | Visualization-library citations with versions and doc URLs. | n/a | n/a | n/a |

## What is NOT here

- **Whole library clones.** d3, matplotlib, geopandas, pycirclize are
  installed via npm/pip and version-pinned in the visualization stack
  (see `research/visual-first-refactor.md` for the pinned set). Their
  source is too large and changes too fast to vendor.
- **Per-country admin boundaries.** Those belong in per-program
  `.cache/geo/` (e.g.,
  `public-service-data-quality/.cache/geo/geoBoundaries-BGD-ADM1.geojson`),
  not here. This folder holds *global* basemap data only.
- **Generated derivatives.** Every transform of these files (filtered
  Asia-Pacific subset, simplified geometry, etc.) is produced
  on-the-fly by `scripts/thumbnail_lib.py` from these inputs.

## How to refresh

If a Natural Earth release changes (the version tag is pinned in the
table above), re-download with:

```bash
python -c "
import urllib.request, hashlib
for fname in ['ne_110m_admin_0_countries.geojson','ne_50m_admin_0_countries.geojson']:
    url = f'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/{fname}'
    urllib.request.urlretrieve(url, f'opensrc/world-boundaries/{fname}')
    with open(f'opensrc/world-boundaries/{fname}','rb') as fh:
        print(fname, hashlib.sha256(fh.read()).hexdigest())
"
```

Bump the version tag in the URL and in this README's "Retrieved" row.
Hero scripts pick up the new geometry on the next render.

## Citation in artifacts

Hero visuals that use these files cite Natural Earth in their footer:

```text
Source: ... Natural Earth (1:50m, public domain).
```

The shared helper `scripts/thumbnail_lib.py` writes the footer
automatically; per-program scripts do not need to assemble the citation
string by hand.
