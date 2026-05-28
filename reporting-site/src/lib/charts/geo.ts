/**
 * geo.ts — tiny equirectangular projection for the Asia-Pacific basemap.
 *
 * The basemap (public/geo/asia-pacific.geojson) and centroids are already
 * Pacific-centered at lon0=125 by scripts/build-webmap.mjs, so the
 * projection here is a plain linear map from a (lon,lat) view box to
 * pixels. wrapLon is kept as an idempotent guard for any raw coordinate
 * projected directly (it is a no-op on already-wrapped values).
 *
 * Equal-aspect is preserved by deriving the pixel height from the view
 * aspect (see viewHeight), matching the Python hero's set_aspect("equal").
 */
export const LON0 = 125;

export function wrapLon(lon: number): number {
  return LON0 + (((((lon - LON0) % 360) + 540) % 360) - 180);
}

export interface GeoView {
  lonMin: number;
  lonMax: number;
  latMin: number;
  latMax: number;
}

// Frames mainland Asia (Kyrgyz/Nepal) through the Pacific cluster
// (Vanuatu/Tonga/Samoa). Aspect ≈ 16:9.
export const ASIA_PACIFIC_VIEW: GeoView = {
  lonMin: 55,
  lonMax: 196,
  latMin: -28,
  latMax: 51,
};

export type Projector = (lon: number, lat: number) => [number, number];

/** Pixel height that keeps equal-aspect for a given view + pixel width. */
export function viewHeight(view: GeoView, width: number): number {
  const lonSpan = view.lonMax - view.lonMin;
  const latSpan = view.latMax - view.latMin;
  return width * (latSpan / lonSpan);
}

export function makeProjector(view: GeoView, width: number, height: number): Projector {
  const sx = width / (view.lonMax - view.lonMin);
  const sy = height / (view.latMax - view.latMin);
  return (lon: number, lat: number) => [
    (wrapLon(lon) - view.lonMin) * sx,
    (view.latMax - lat) * sy,
  ];
}

export interface GeoFeature {
  type: "Feature";
  properties: { iso3: string; name: string };
  geometry:
    | { type: "Polygon"; coordinates: number[][][] }
    | { type: "MultiPolygon"; coordinates: number[][][][] };
}

export interface GeoCollection {
  type: "FeatureCollection";
  features: GeoFeature[];
  meta?: Record<string, unknown>;
}

export interface Centroid {
  name: string;
  lon: number;
  lat: number;
}
export interface CentroidIndex {
  lon0: number;
  source: string;
  centroids: Record<string, Centroid>;
}

/** Build an SVG path `d` string for a feature's geometry. */
export function featurePath(feature: GeoFeature, project: Projector): string {
  const rings: number[][][] = [];
  const g = feature.geometry;
  if (g.type === "Polygon") rings.push(...g.coordinates);
  else for (const poly of g.coordinates) rings.push(...poly);

  let d = "";
  for (const ring of rings) {
    for (let i = 0; i < ring.length; i++) {
      const [x, y] = project(ring[i][0], ring[i][1]);
      d += (i === 0 ? "M" : "L") + x.toFixed(1) + " " + y.toFixed(1);
    }
    d += "Z";
  }
  return d;
}
