# Visualization library references

Pinned versions for the visual-first refactor stack. Every hero visual
in this repo is rendered by one of the libraries below, reading
committed data from `generated/*.csv|json` and the basemap files in
`opensrc/world-boundaries/`.

## Static rendering stack (default)

| Library | Version | License | Role | Canonical docs |
|---|---|---|---|---|
| `matplotlib` | 3.10.x | PSF-2.0 (matplotlib license) | Figure composition, typography, PNG/SVG export | https://matplotlib.org/stable/ |
| `geopandas` | 1.1.x | BSD-3-Clause | GeoJSON read, projection, choropleth fills | https://geopandas.org/en/stable/ |
| `pandas` | 2.x | BSD-3-Clause | CSV/JSON read, panel construction | https://pandas.pydata.org/docs/ |
| `shapely` | 2.1.x | BSD-3-Clause | Geometry ops (centroid, simplify) | https://shapely.readthedocs.io/ |
| `pycirclize` | ≥ 1.7 (to be installed) | MIT | Chord/circos diagrams for bilateral-flow visuals | https://moshi4.github.io/pyCirclize/ |

Install (if not already in env):

```bash
pip install matplotlib geopandas pandas shapely pycirclize
```

## Reference design vocabulary

The visual style targets *editorial* readability — the look that
publications like the FT, the New York Times' Upshot, the IMF's
country reports, and Our World in Data use for their static figures.
That look is mostly typography, palette restraint, and annotation —
not a chart library. The recipe:

1. **Typography.** Single sans-serif family across the figure (system
   fallback chain: Inter → IBM Plex Sans → DejaVu Sans). Title at 22–28
   pt, subtitle at 13–14 pt, axis labels at 10–11 pt, footer at 8 pt.
2. **Palette.** One sequential ramp (default `viridis_r`, perceptual
   uniform, colorblind-safe) plus one neutral grey (`#444`) for
   non-data ink. Diverging palettes only when the data are signed.
3. **Whitespace.** 1600×900 native; margins ≥ 60 px; key annotations
   inside the figure (no separate legend block) when possible.
4. **Story focus.** One headline number rendered large, near the
   subject it describes. Other values minimal, in muted color.
5. **Attribution burned in.** Footer line (source + retrieval date +
   `attestation_chain: ai-first under §18`) is part of the image, not
   a separate caption — so a screenshot retains the labeling.

## Why static SVG/PNG, not interactive JS

The visual-first refactor renders **static** images on the home page
and topic-page hero. There is no runtime chart library on the React
side; thumbnails are served as plain `<img>` tags. The reasons:

| Choice | Static (current) | Interactive JS (deferred) |
|---|---|---|
| First contentful paint | One HTTP request per thumbnail; ~30–80 KB; renders instantly | Library JS (~100–300 KB) + data fetch + render pass |
| Reproducibility | sha256-pinned in `manifest.json`; identical bytes on rerun | Re-renders per browser; non-deterministic by design |
| Reviewer drilldown | SVG is text-diffable; opens in any editor | Requires the live site or a snapshot |
| Honest labeling | Attestation footer is burned in | Footer is a DOM element; trivially removable |
| Authoring burden | Each program has one Python script | Each program needs both a Python script and a React component |

If the topic page later needs **interactive** charts (zoom, brush,
filter), the right addition is **Observable Plot** (`@observablehq/plot`),
which renders the same SVG that matplotlib emits and reads the same
committed CSV. That is a Phase 2 decision; Phase 1 (this refactor) is
static.

## Why these libraries, not the alternatives

- **D3.js** — the canonical "beautiful editorial charts" library used by
  the NYT, FT, Reuters. We do not need it because we ship static
  images; D3 buys us interactivity at the cost of a 250 KB JS bundle
  and a non-deterministic render. We borrow D3's *design vocabulary*
  (single-sequential palettes, annotation-led storytelling) without
  the runtime.
- **Plotly / Bokeh / Highcharts** — produce HTML widgets. Same
  argument: we do not need interactivity for thumbnails.
- **Datawrapper / Flourish / Infogram** — third-party SaaS; not
  reproducible from a clean clone per §11.
- **Vega-Lite / Observable Plot** — excellent grammar-of-graphics tools
  but their Node CLIs add complexity for no Phase-1 gain. Candidates
  for Phase 2 interactive charts on the topic page.
- **Cartopy** — geopandas + matplotlib already covers the projections
  we need (PlateCarree / Robinson / Mercator for Asia-Pacific).
- **Folium / Leaflet** — interactive web maps. Phase 2 candidate, same
  reasoning as Plotly.

## Drupal note (raised 2026-05-19)

Drupal is a CMS, not a chart library. The "beautiful charts" the user
noticed on Drupal-built sites are almost always produced by a
JavaScript library embedded in the page (most commonly D3, Highcharts,
or Chart.js). Choosing Drupal would not give us the charts; choosing
the chart library does.

## Reference galleries

Concrete patterns the hero scripts draw from:

- Matplotlib gallery — https://matplotlib.org/stable/gallery/
- The Python Graph Gallery — https://python-graph-gallery.com/
- Geopandas examples — https://geopandas.org/en/stable/gallery/
- pyCirclize examples — https://moshi4.github.io/pyCirclize/getting_started/
- Natural Earth styled examples — https://www.naturalearthdata.com/
- Our World in Data Grapher patterns — https://ourworldindata.org/grapher
  (read the design choices; we do not use the library)
- New York Times Upshot — https://www.nytimes.com/section/upshot
  (read the design choices)
