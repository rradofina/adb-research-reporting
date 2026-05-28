/**
 * data.ts — load committed pipeline JSON for native charts.
 *
 * Constitution tie-in: native charts read the SAME committed
 * generated/*.json a reviewer can download from the Data tab. A native
 * chart is therefore more auditable than a screenshot — the reader can
 * verify the chart is derived from the exact data, not trust a raster.
 * No numbers are hard-coded here; everything flows from the fetched file.
 */
import type { GeoCollection, CentroidIndex } from "./geo";

export interface PanelRow {
  iso3: string;
  country: string;
  [key: string]: number | string | null;
}

export interface Panel {
  program: string;
  rows: PanelRow[];
  totals?: Record<string, number>;
  expensive_corridors_top50?: Array<Record<string, number | string>>;
  [key: string]: unknown;
}

const panelCache = new Map<string, Promise<Panel | null>>();
let geoCache: Promise<GeoCollection | null> | null = null;
let centroidCache: Promise<CentroidIndex | null> | null = null;

async function getJSON<T>(url: string): Promise<T | null> {
  try {
    const r = await fetch(url);
    return r.ok ? ((await r.json()) as T) : null;
  } catch {
    return null;
  }
}

/** Load a program's panel JSON, e.g. loadPanel("remittance-resilience"). */
export function loadPanel(
  slug: string,
  file = `${slug}-adb-panel.json`,
): Promise<Panel | null> {
  const url = `/programs/${slug}/generated/${file}`;
  if (!panelCache.has(url)) panelCache.set(url, getJSON<Panel>(url));
  return panelCache.get(url)!;
}

export function loadBasemap(): Promise<GeoCollection | null> {
  if (!geoCache) geoCache = getJSON<GeoCollection>("/geo/asia-pacific.geojson");
  return geoCache;
}

export function loadCentroids(): Promise<CentroidIndex | null> {
  if (!centroidCache) centroidCache = getJSON<CentroidIndex>("/geo/asia-pacific-centroids.json");
  return centroidCache;
}

/** Numeric coercion that treats null/"" as missing. */
export function num(v: unknown): number | null {
  if (v == null || v === "") return null;
  const n = typeof v === "number" ? v : Number(v);
  return isFinite(n) ? n : null;
}
