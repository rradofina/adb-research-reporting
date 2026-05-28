/**
 * build-webmap.mjs — mint a browser-sized Asia-Pacific basemap.
 *
 * Constitution note: this is a deterministic transform of a committed,
 * public-domain source (Natural Earth 50m admin-0, in opensrc/). It
 * introduces NO empirical numbers — it only filters, simplifies, and
 * reprojects geometry the repo already vendors. Output is committed so
 * the web bundle never ships the full 3 MB world file.
 *
 * Inputs (read-only):
 *   opensrc/world-boundaries/ne_50m_admin_0_countries.geojson
 *
 * Outputs (committed, consumed by the reporting site):
 *   reporting-site/public/geo/asia-pacific.geojson       (context land)
 *   reporting-site/public/geo/asia-pacific-centroids.json (iso3 -> point)
 *
 * Pipeline per feature:
 *   1. filter to REGION_UN in {Asia, Oceania}
 *   2. resolve iso3 (ISO_A3, fall back to ADM0_A3 when ISO_A3 == '-99')
 *   3. Pacific-center longitudes at lon0=125 so the antimeridian (the
 *      map runs ~55E..195E into Polynesia) does not tear polygons
 *   4. compute a representative point per country (largest-ring centroid)
 *      — emitted for ALL countries incl. tiny Pacific islands so the map
 *      can place a marker even where the polygon is sub-pixel
 *   5. simplify the basemap polygons: round to 2 dp, decimate long rings,
 *      drop micro-rings and any ring that still spans the dateline
 *
 * Run:  node scripts/build-webmap.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SRC = path.join(ROOT, "opensrc", "world-boundaries", "ne_50m_admin_0_countries.geojson");
const OUT_DIR = path.join(ROOT, "reporting-site", "public", "geo");

const LON0 = 125; // Pacific-centered: AP content lands ~55..195 after wrap
const COORD_DP = 2; // ~1.1 km
const MAX_RING_POINTS = 120; // decimate big coastlines to this many points
const MIN_RING_AREA = 0.03; // deg^2 (~18 km box); smaller islands -> markers only
const MAX_RING_SPAN = 120; // drop rings whose wrapped lon-span exceeds this (dateline artifacts)

/** Pacific-center a longitude into a continuous space around LON0. */
function wrapLon(lon) {
  return LON0 + (((((lon - LON0) % 360) + 540) % 360) - 180);
}

function round(n) {
  const f = 10 ** COORD_DP;
  return Math.round(n * f) / f;
}

/** Signed shoelace area of a ring in (wrapped-lon, lat) space. */
function ringArea(ring) {
  let a = 0;
  for (let i = 0, n = ring.length; i < n; i++) {
    const [x1, y1] = ring[i];
    const [x2, y2] = ring[(i + 1) % n];
    a += x1 * y2 - x2 * y1;
  }
  return a / 2;
}

/** Area-weighted centroid of a ring in (wrapped-lon, lat) space. */
function ringCentroid(ring) {
  let cx = 0, cy = 0, a = 0;
  for (let i = 0, n = ring.length; i < n; i++) {
    const [x1, y1] = ring[i];
    const [x2, y2] = ring[(i + 1) % n];
    const cross = x1 * y2 - x2 * y1;
    a += cross;
    cx += (x1 + x2) * cross;
    cy += (y1 + y2) * cross;
  }
  a /= 2;
  if (Math.abs(a) < 1e-9) {
    // Degenerate ring: fall back to mean of vertices.
    const m = ring.reduce((acc, [x, y]) => [acc[0] + x, acc[1] + y], [0, 0]);
    return [m[0] / ring.length, m[1] / ring.length];
  }
  return [cx / (6 * a), cy / (6 * a)];
}

/** Normalize a geometry to a list of polygons, each [outerRing, ...holes]. */
function toPolygons(geom) {
  if (!geom) return [];
  if (geom.type === "Polygon") return [geom.coordinates];
  if (geom.type === "MultiPolygon") return geom.coordinates;
  return [];
}

function wrapRing(ring) {
  return ring.map(([lon, lat]) => [wrapLon(lon), lat]);
}

function simplifyRing(ring) {
  // round + drop consecutive duplicates
  let pts = ring.map(([x, y]) => [round(x), round(y)]);
  const dedup = [];
  for (const p of pts) {
    const last = dedup[dedup.length - 1];
    if (!last || last[0] !== p[0] || last[1] !== p[1]) dedup.push(p);
  }
  pts = dedup;
  // decimate long rings (keep first/last, even stride)
  if (pts.length > MAX_RING_POINTS) {
    const stride = Math.ceil(pts.length / MAX_RING_POINTS);
    const out = [];
    for (let i = 0; i < pts.length; i += stride) out.push(pts[i]);
    if (out[out.length - 1] !== pts[pts.length - 1]) out.push(pts[pts.length - 1]);
    pts = out;
  }
  return pts;
}

function lonSpan(ring) {
  let min = Infinity, max = -Infinity;
  for (const [x] of ring) { if (x < min) min = x; if (x > max) max = x; }
  return max - min;
}

function resolveIso3(p) {
  const iso = p.ISO_A3 && p.ISO_A3 !== "-99" ? p.ISO_A3 : p.ADM0_A3;
  return iso || "UNK";
}

function main() {
  const src = JSON.parse(fs.readFileSync(SRC, "utf8"));
  const ap = src.features.filter((f) =>
    ["Asia", "Oceania"].includes(f.properties?.REGION_UN),
  );

  const centroids = {};
  const outFeatures = [];

  for (const f of ap) {
    const iso3 = resolveIso3(f.properties);
    const name = f.properties.NAME_LONG || f.properties.NAME || iso3;
    const polys = toPolygons(f.geometry);
    if (polys.length === 0) continue;

    // --- centroid from the largest outer ring (wrapped space) ---
    let best = null;
    let bestArea = -1;
    for (const rings of polys) {
      const outer = wrapRing(rings[0]);
      const area = Math.abs(ringArea(outer));
      if (area > bestArea) { bestArea = area; best = outer; }
    }
    if (best) {
      const [lon, lat] = ringCentroid(best);
      centroids[iso3] = { name, lon: round(lon), lat: round(lat) };
    }

    // --- simplified basemap polygons ---
    const keptPolys = [];
    for (const rings of polys) {
      const outer = wrapRing(rings[0]);
      if (Math.abs(ringArea(outer)) < MIN_RING_AREA) continue; // micro-island
      if (lonSpan(outer) > MAX_RING_SPAN) continue; // dateline tear
      const simpOuter = simplifyRing(outer);
      if (simpOuter.length < 4) continue;
      const ringSet = [simpOuter];
      for (let h = 1; h < rings.length; h++) {
        const hole = wrapRing(rings[h]);
        if (Math.abs(ringArea(hole)) < MIN_RING_AREA) continue;
        const simpHole = simplifyRing(hole);
        if (simpHole.length >= 4) ringSet.push(simpHole);
      }
      keptPolys.push(ringSet);
    }
    if (keptPolys.length === 0) continue;

    outFeatures.push({
      type: "Feature",
      properties: { iso3, name },
      geometry:
        keptPolys.length === 1
          ? { type: "Polygon", coordinates: keptPolys[0] }
          : { type: "MultiPolygon", coordinates: keptPolys },
    });
  }

  fs.mkdirSync(OUT_DIR, { recursive: true });
  const fc = {
    type: "FeatureCollection",
    meta: {
      source: "Natural Earth 50m admin-0 (public domain), via opensrc/world-boundaries",
      transform: "scripts/build-webmap.mjs",
      lon0: LON0,
      note: "Pacific-centered, Asia+Oceania only, simplified for web. Not for analysis.",
    },
    features: outFeatures,
  };
  const geoPath = path.join(OUT_DIR, "asia-pacific.geojson");
  const cenPath = path.join(OUT_DIR, "asia-pacific-centroids.json");
  fs.writeFileSync(geoPath, JSON.stringify(fc));
  fs.writeFileSync(
    cenPath,
    JSON.stringify({ lon0: LON0, source: fc.meta.source, centroids }, null, 0),
  );

  const kb = (p) => (fs.statSync(p).size / 1024).toFixed(0);
  console.log(`basemap features: ${outFeatures.length} / ${ap.length} AP`);
  console.log(`centroids: ${Object.keys(centroids).length}`);
  console.log(`asia-pacific.geojson: ${kb(geoPath)} KB`);
  console.log(`asia-pacific-centroids.json: ${kb(cenPath)} KB`);
  // Spot-check the cluster economies are present as centroids.
  for (const iso of ["TON", "KGZ", "NPL", "WSM", "VUT", "TJK", "IND", "CHN"]) {
    const c = centroids[iso];
    console.log(`  ${iso}: ${c ? `${c.lon},${c.lat} (${c.name})` : "MISSING"}`);
  }
}

main();
