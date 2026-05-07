# Port-Hinterland Friction

## Research Question

Which inland regions are most exposed to trade and food-price shocks because
their port, road, and border connections are fragile or indirect?

## Why This Is Unconventional

Trade analysis often stops at country-level imports and port volumes. This track
looks at the inland geography of dependence: which populations are far from
robust logistics paths.

## Available Data

- OpenStreetMap roads, rail, ports, and border crossings
- WorldPop population grids
- World Bank Logistics Performance Index
- UN Comtrade national import dependence indicators
- WFP market and food-price data where available
- geoBoundaries administrative geometries

## First Pipeline

1. Map ports and major inland transport links for selected ADB economies.
2. Compute simple distance/friction to ports and borders by ADM1/ADM2.
3. Combine with food/import dependence indicators.

## Outputs

- `generated/port-hinterland-friction-pilots.csv`
- Hinterland exposure ranking and route-friction map
- Source manifest for OSM extract dates

## Reproducibility Notes

Start with geometric friction, then graduate to routable network travel-time
only after the road graph is validated.
