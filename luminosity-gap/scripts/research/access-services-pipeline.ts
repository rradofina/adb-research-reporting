import { createHash } from "crypto";
import { mkdir, readFile, writeFile } from "fs/promises";
import path from "path";
import { intersection } from "polygon-clipping";
import type { MultiPolygon, Polygon } from "polygon-clipping";

type PilotCountry = {
  iso2: string;
  iso3: string;
  name: string;
  centroid: { lat: number; lon: number };
  bbox: { minLon: number; minLat: number; maxLon: number; maxLat: number };
};

type IndicatorValue = {
  indicator: string;
  year: number;
  value: number;
  sourceUrl: string;
};

type PopulationValue = {
  year: number;
  value: number;
  sourceLabel: string;
  sourceUrl: string;
  method: string;
  note?: string;
};

type ServiceCounts = {
  health: number;
  education: number;
  markets: number;
  total: number;
  sourceUrl: string;
  osmTimestamp?: string;
};

type AdminServiceCounts = ServiceCounts & {
  queryMode: "osm_area_iso3166_2" | "bbox_fallback";
  osmAreasTimestamp?: string;
};

type ClimateValues = {
  baselineTasmaxC: number;
  futureTasmaxC: number;
  heatDeltaC: number;
  baselinePrecipMm: number;
  futurePrecipPercentOfBaseline: number;
  precipChangePct: number;
  sourceUrl: string;
};

type PilotResult = {
  iso2: string;
  iso3: string;
  name: string;
  centroid: { lat: number; lon: number };
  bbox: { minLon: number; minLat: number; maxLon: number; maxLat: number };
  population: IndicatorValue;
  landAreaSqKm: IndicatorValue;
  ruralPopulationShare: IndicatorValue;
  services: ServiceCounts;
  climate: ClimateValues;
  metrics: {
    peoplePerHealthFacility: number;
    peoplePerSchool: number;
    peoplePerMarket: number;
    healthFacilitiesPer100k: number;
    schoolsPer100k: number;
    marketsPer100k: number;
    totalMappedServicesPerMillion: number;
    equivalentHealthCatchmentRadiusKm: number;
    equivalentSchoolCatchmentRadiusKm: number;
    serviceLoadScore: number;
    heatStressScore: number;
    rainfallStressScore: number;
    ruralExposureScore: number;
    osmCompletenessRiskScore: number;
    accessStressIndex: number;
    bottleneck: string;
  };
};

type GeoJsonGeometry =
  | { type: "Polygon"; coordinates: number[][][] }
  | { type: "MultiPolygon"; coordinates: number[][][][] };

type GeoJsonFeature = {
  type: "Feature";
  properties: Record<string, unknown>;
  geometry: GeoJsonGeometry;
};

type GeoJsonFeatureCollection = {
  type: "FeatureCollection";
  features: GeoJsonFeature[];
};

type GeoBoundaryMetadata = {
  boundaryID: string;
  boundaryName: string;
  boundaryISO: string;
  boundaryType: string;
  boundaryYearRepresented: string;
  boundaryCanonical?: string;
  boundarySource?: string;
  boundaryLicense?: string;
  boundarySourceURL?: string;
  sourceDataUpdateDate?: string;
  buildDate?: string;
  admUnitCount?: string;
  gjDownloadURL: string;
  simplifiedGeometryGeoJSON?: string;
};

type AdminAccessResult = {
  iso2: string;
  iso3: string;
  countryName: string;
  admin1Code: string;
  admin1Name: string;
  shapeId: string;
  centroid: { lat: number; lon: number };
  bbox: { minLon: number; minLat: number; maxLon: number; maxLat: number };
  approxAreaSqKm: number;
  boundary: {
    boundaryID: string;
    boundaryYearRepresented: string;
    boundarySource?: string;
    boundaryLicense?: string;
    geometrySourceUrl: string;
  };
  population: PopulationValue;
  services: AdminServiceCounts;
  climate: ClimateValues;
  metrics: {
    peoplePerHealthFacility: number;
    peoplePerSchool: number;
    peoplePerMarket: number;
    healthFacilitiesPer100k: number;
    schoolsPer100k: number;
    marketsPer100k: number;
    totalMappedServicesPerMillion: number;
    totalServicesPer1000SqKm: number;
    serviceLoadScore: number;
    heatStressScore: number;
    rainfallStressScore: number;
    osmCompletenessRiskScore: number;
    accessStressIndex: number;
    bottleneck: string;
  };
};

const COUNTRIES: PilotCountry[] = [
  {
    iso2: "PH",
    iso3: "PHL",
    name: "Philippines",
    centroid: { lat: 12.8797, lon: 121.774 },
    bbox: { minLon: 116.9, minLat: 4.5, maxLon: 127.0, maxLat: 21.3 },
  },
  {
    iso2: "BD",
    iso3: "BGD",
    name: "Bangladesh",
    centroid: { lat: 23.685, lon: 90.3563 },
    bbox: { minLon: 88.0, minLat: 20.5, maxLon: 92.8, maxLat: 26.7 },
  },
];

const NEXT_WAVE_COUNTRIES: PilotCountry[] = [
  {
    iso2: "PK",
    iso3: "PAK",
    name: "Pakistan",
    centroid: { lat: 30.3753, lon: 69.3451 },
    bbox: { minLon: 60.8, minLat: 23.6, maxLon: 77.1, maxLat: 37.1 },
  },
  {
    iso2: "NP",
    iso3: "NPL",
    name: "Nepal",
    centroid: { lat: 28.3949, lon: 84.124 },
    bbox: { minLon: 80.0, minLat: 26.3, maxLon: 88.2, maxLat: 30.5 },
  },
  {
    iso2: "LK",
    iso3: "LKA",
    name: "Sri Lanka",
    centroid: { lat: 7.8731, lon: 80.7718 },
    bbox: { minLon: 79.6, minLat: 5.9, maxLon: 82.0, maxLat: 9.9 },
  },
];

const FRONTIER_BATCH_COUNTRIES: PilotCountry[] = [
  {
    iso2: "KH",
    iso3: "KHM",
    name: "Cambodia",
    centroid: { lat: 12.5657, lon: 104.991 },
    bbox: { minLon: 102.3, minLat: 10.3, maxLon: 107.7, maxLat: 14.8 },
  },
  {
    iso2: "LA",
    iso3: "LAO",
    name: "Lao People's Democratic Republic",
    centroid: { lat: 19.8563, lon: 102.4955 },
    bbox: { minLon: 100.1, minLat: 13.9, maxLon: 107.7, maxLat: 22.6 },
  },
  {
    iso2: "TL",
    iso3: "TLS",
    name: "Timor-Leste",
    centroid: { lat: -8.8742, lon: 125.7275 },
    bbox: { minLon: 124.0, minLat: -9.7, maxLon: 127.4, maxLat: -8.1 },
  },
];

const WORLD_BANK_INDICATORS = {
  population: "SP.POP.TOTL",
  landArea: "AG.LND.TOTL.K2",
  ruralShare: "SP.RUR.TOTL.ZS",
};

const OVERPASS_ENDPOINTS = [
  "https://overpass.kumi.systems/api/interpreter",
];

const GEOboundaries_RELEASE = "gbOpen";
const WORLDPOP_YEAR = 2020;
const WORLDPOP_STATS_URL = "https://api.worldpop.org/v1/services/stats";
const PSA_OPENSTAT_POPULATION_URL =
  "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO/0021A6DPAG0.px";
const CACHE_ROOT = ".cache/research/access-services";
let lastFetchWasCacheHit = false;

const PHILIPPINES_PSA_REGION_CODE_BY_SHAPE_ISO: Record<string, string> = {
  "PH-00": "1",
  "PH-15": "19",
  "PH-01": "27",
  "PH-02": "32",
  "PH-03": "38",
  "PH-40": "48",
  "PH-41": "55",
  "PH-05": "62",
  "PH-06": "69",
  "PH-07": "78",
  "PH-08": "86",
  "PH-09": "94",
  "PH-10": "100",
  "PH-11": "108",
  "PH-12": "115",
  "PH-13": "121",
  "PH-14": "128",
};

function clamp(value: number, min = 0, max = 1): number {
  return Math.min(max, Math.max(min, value));
}

function round(value: number, digits = 2): number {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null
    ? (value as Record<string, unknown>)
    : {};
}

function asArray(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

function asString(value: unknown): string | undefined {
  return typeof value === "string" && value.length > 0 ? value : undefined;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function sleepAfterNetwork(ms: number): Promise<void> {
  if (!lastFetchWasCacheHit) {
    await sleep(ms);
  }
}

async function fetchJson(url: string, init?: RequestInit): Promise<unknown> {
  const method = init?.method ?? "GET";
  const body =
    typeof init?.body === "string"
      ? init.body
      : init?.body instanceof URLSearchParams
        ? init.body.toString()
        : init?.body
          ? String(init.body)
          : "";
  const cacheKey = createHash("sha1")
    .update(JSON.stringify({ url, method, body }))
    .digest("hex");
  const cachePath = path.join(process.cwd(), CACHE_ROOT, `${cacheKey}.json`);

  if (process.env.ACCESS_REFRESH !== "1") {
    try {
      lastFetchWasCacheHit = true;
      return JSON.parse(await readFile(cachePath, "utf8"));
    } catch {
      // Cache misses should fall through to the source request.
    }
  }

  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= 4; attempt += 1) {
    lastFetchWasCacheHit = false;

    try {
      const response = await fetch(url, {
        ...init,
        headers: {
          "User-Agent": "DevelopmentBlindspotsLab/0.1 research pipeline",
          ...(init?.headers ?? {}),
        },
      });

      if (response.ok) {
        const json = await response.json();
        await mkdir(path.dirname(cachePath), { recursive: true });
        await writeFile(cachePath, `${JSON.stringify(json)}\n`);
        return json;
      }

      const body = await response.text();
      lastError = new Error(
        `HTTP ${response.status} for ${url}: ${body.slice(0, 240)}`
      );

      if (![408, 429, 500, 502, 503, 504].includes(response.status)) {
        throw lastError;
      }
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
    }

    await sleep(1500 * attempt);
  }

  throw lastError ?? new Error(`Fetch failed for ${url}`);
}

async function fetchWorldBankIndicator(
  iso3: string,
  indicator: string
): Promise<IndicatorValue> {
  const urls = [
    `https://api.worldbank.org/v2/country/${iso3}/indicator/${indicator}?format=json&per_page=100&date=2020:2025`,
    `https://api.worldbank.org/v2/country/${iso3}/indicator/${indicator}?format=json&per_page=100&mrv=1`,
  ];
  let json: unknown;
  let sourceUrl = urls[0];
  let lastError: Error | undefined;

  for (const url of urls) {
    try {
      json = await fetchJson(url);
      sourceUrl = url;
      break;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
    }
  }

  if (!json) {
    throw lastError ?? new Error(`World Bank fetch failed for ${iso3}/${indicator}`);
  }

  if (!Array.isArray(json) || !Array.isArray(json[1])) {
    throw new Error(`Unexpected World Bank response for ${iso3}/${indicator}`);
  }

  const rows = json[1] as Array<Record<string, unknown>>;
  const row = rows
    .filter((item) => typeof item.value === "number")
    .sort((a, b) => Number(b.date) - Number(a.date))[0];

  if (!row) {
    throw new Error(`No non-null World Bank value for ${iso3}/${indicator}`);
  }

  return {
    indicator,
    year: Number(row.date),
    value: Number(row.value),
    sourceUrl,
  };
}

async function fetchCckpValue(
  iso3: string,
  variable: "tasmax" | "pr" | "prpercnt",
  period: "1995-2014" | "2040-2059",
  scenario: "historical" | "ssp245"
): Promise<{ value: number; sourceUrl: string }> {
  const url = `https://cckpapi.worldbank.org/cckp/v1/cmip6-x0.25_climatology_${variable}_climatology_annual_${period}_median_${scenario}_ensemble_all_mean/${iso3}?format=json`;
  const json = await fetchJson(url);
  const data = asRecord(asRecord(json).data);
  const countryData = asRecord(data[iso3]);
  const value = Object.values(countryData).find(
    (entry) => typeof entry === "number"
  );

  if (typeof value !== "number") {
    throw new Error(`No CCKP value for ${iso3}/${variable}/${period}`);
  }

  return { value, sourceUrl: url };
}

async function fetchClimate(country: PilotCountry): Promise<ClimateValues> {
  const [baselineTasmax, futureTasmax, baselinePrecip, futurePrecipPercent] =
    await Promise.all([
      fetchCckpValue(country.iso3, "tasmax", "1995-2014", "historical"),
      fetchCckpValue(country.iso3, "tasmax", "2040-2059", "ssp245"),
      fetchCckpValue(country.iso3, "pr", "1995-2014", "historical"),
      fetchCckpValue(country.iso3, "prpercnt", "2040-2059", "ssp245"),
    ]);

  return {
    baselineTasmaxC: round(baselineTasmax.value, 2),
    futureTasmaxC: round(futureTasmax.value, 2),
    heatDeltaC: round(futureTasmax.value - baselineTasmax.value, 2),
    baselinePrecipMm: round(baselinePrecip.value, 2),
    futurePrecipPercentOfBaseline: round(futurePrecipPercent.value, 2),
    precipChangePct: round(futurePrecipPercent.value - 100, 2),
    sourceUrl: "https://climateknowledgeportal.worldbank.org/download-data",
  };
}

function overpassSelector(
  category: "health" | "education" | "markets",
  target: string
): string {
  if (category === "health") {
    return `node["amenity"~"^(hospital|clinic|doctors)$"]${target};
  way["amenity"~"^(hospital|clinic|doctors)$"]${target};
  relation["amenity"~"^(hospital|clinic|doctors)$"]${target};`;
  }

  if (category === "education") {
    return `node["amenity"="school"]${target};
  way["amenity"="school"]${target};
  relation["amenity"="school"]${target};`;
  }

  return `node["amenity"="marketplace"]${target};
  way["amenity"="marketplace"]${target};
  relation["amenity"="marketplace"]${target};`;
}

function buildOverpassCountQuery(
  country: PilotCountry,
  category: "health" | "education" | "markets",
  mode: "area" | "bbox"
): string {
  if (mode === "bbox") {
    const bbox = `(${country.bbox.minLat},${country.bbox.minLon},${country.bbox.maxLat},${country.bbox.maxLon})`;

    return `[out:json][timeout:240];
(
  ${overpassSelector(category, bbox)}
);
out count;`;
  }

  return `[out:json][timeout:240];
area["ISO3166-1"="${country.iso2}"]["admin_level"="2"]->.searchArea;
(
  ${overpassSelector(category, "(area.searchArea)")}
);
out count;`;
}

async function fetchOverpassCount(
  country: PilotCountry,
  category: "health" | "education" | "markets"
): Promise<{ count: number; sourceUrl: string; osmTimestamp?: string }> {
  let lastError: Error | undefined;

  for (const mode of ["area", "bbox"] as const) {
    const query = buildOverpassCountQuery(country, category, mode);
    const body = new URLSearchParams({ data: query });

    for (const endpoint of OVERPASS_ENDPOINTS) {
      for (let attempt = 1; attempt <= 3; attempt += 1) {
        try {
          const json = await fetchJson(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body,
          });
          const root = asRecord(json);
          const elements = Array.isArray(root.elements) ? root.elements : [];
          const first = asRecord(elements[0]);
          const tags = asRecord(first.tags);
          const count = Number(tags.total);
          const osm3s = asRecord(root.osm3s);

          if (!Number.isFinite(count)) {
            throw new Error(`Overpass count missing for ${country.name}/${category}`);
          }

          if (count === 0) {
            throw new Error(
              `Suspicious zero Overpass count for ${country.name}/${category}/${mode}`
            );
          }

          return {
            count,
            sourceUrl: endpoint,
            osmTimestamp:
              typeof osm3s.timestamp_osm_base === "string"
                ? osm3s.timestamp_osm_base
                : undefined,
          };
        } catch (error) {
          lastError = error instanceof Error ? error : new Error(String(error));
          await sleep(3000 * attempt);
        }
      }
    }
  }

  throw lastError ?? new Error(`Overpass failed for ${country.name}/${category}`);
}

async function fetchServices(country: PilotCountry): Promise<ServiceCounts> {
  const health = await fetchOverpassCount(country, "health");
  await sleepAfterNetwork(3500);
  const education = await fetchOverpassCount(country, "education");
  await sleepAfterNetwork(3500);
  const markets = await fetchOverpassCount(country, "markets");

  return {
    health: health.count,
    education: education.count,
    markets: markets.count,
    total: health.count + education.count + markets.count,
    sourceUrl: "https://overpass.kumi.systems/api/interpreter",
    osmTimestamp:
      health.osmTimestamp ?? education.osmTimestamp ?? markets.osmTimestamp,
  };
}

function pressureScore(value: number, good: number, bad: number): number {
  return clamp((value - good) / (bad - good));
}

function chooseBottleneck(scores: Record<string, number>): string {
  return Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0];
}

function computeMetrics(
  population: number,
  landAreaSqKm: number,
  ruralShare: number,
  services: ServiceCounts,
  climate: ClimateValues
): PilotResult["metrics"] {
  const peoplePerHealthFacility = population / Math.max(services.health, 1);
  const peoplePerSchool = population / Math.max(services.education, 1);
  const peoplePerMarket = population / Math.max(services.markets, 1);

  const healthPressure = pressureScore(peoplePerHealthFacility, 5_000, 50_000);
  const schoolPressure = pressureScore(peoplePerSchool, 1_200, 12_000);
  const marketPressure = pressureScore(peoplePerMarket, 15_000, 150_000);
  const serviceLoadScore = clamp(
    healthPressure * 0.45 + schoolPressure * 0.35 + marketPressure * 0.2
  );

  const heatStressScore = clamp(climate.heatDeltaC / 2);
  const rainfallStressScore = clamp(Math.abs(climate.precipChangePct) / 15);
  const ruralExposureScore = clamp(ruralShare / 100);
  const totalMappedServicesPerMillion = (services.total / population) * 1_000_000;
  const osmCompletenessRiskScore = clamp((250 - totalMappedServicesPerMillion) / 250);

  const accessStressIndex = Math.round(
    100 *
      (serviceLoadScore * 0.4 +
        heatStressScore * 0.22 +
        rainfallStressScore * 0.18 +
        ruralExposureScore * 0.12 +
        osmCompletenessRiskScore * 0.08)
  );

  return {
    peoplePerHealthFacility: Math.round(peoplePerHealthFacility),
    peoplePerSchool: Math.round(peoplePerSchool),
    peoplePerMarket: Math.round(peoplePerMarket),
    healthFacilitiesPer100k: round((services.health / population) * 100_000),
    schoolsPer100k: round((services.education / population) * 100_000),
    marketsPer100k: round((services.markets / population) * 100_000),
    totalMappedServicesPerMillion: round(totalMappedServicesPerMillion),
    equivalentHealthCatchmentRadiusKm: round(
      Math.sqrt(landAreaSqKm / Math.max(services.health, 1) / Math.PI)
    ),
    equivalentSchoolCatchmentRadiusKm: round(
      Math.sqrt(landAreaSqKm / Math.max(services.education, 1) / Math.PI)
    ),
    serviceLoadScore: round(serviceLoadScore * 100, 1),
    heatStressScore: round(heatStressScore * 100, 1),
    rainfallStressScore: round(rainfallStressScore * 100, 1),
    ruralExposureScore: round(ruralExposureScore * 100, 1),
    osmCompletenessRiskScore: round(osmCompletenessRiskScore * 100, 1),
    accessStressIndex,
    bottleneck: chooseBottleneck({
      "service load": serviceLoadScore,
      "heat stress": heatStressScore,
      "rainfall change": rainfallStressScore,
      "rural exposure": ruralExposureScore,
      "OSM completeness": osmCompletenessRiskScore,
    }),
  };
}

async function buildPilot(country: PilotCountry): Promise<PilotResult> {
  console.log(`\n=== ${country.name} ===`);
  console.log("Fetching World Bank indicators...");
  const [population, landAreaSqKm, ruralPopulationShare] = await Promise.all([
    fetchWorldBankIndicator(country.iso3, WORLD_BANK_INDICATORS.population),
    fetchWorldBankIndicator(country.iso3, WORLD_BANK_INDICATORS.landArea),
    fetchWorldBankIndicator(country.iso3, WORLD_BANK_INDICATORS.ruralShare),
  ]);

  console.log("Fetching CCKP climate values...");
  const climate = await fetchClimate(country);

  console.log("Fetching OSM national service counts from Overpass...");
  const services = await fetchServices(country);

  const metrics = computeMetrics(
    population.value,
    landAreaSqKm.value,
    ruralPopulationShare.value,
    services,
    climate
  );

  console.log(
    `Computed national access stress index: ${metrics.accessStressIndex} (${metrics.bottleneck})`
  );

  return {
    ...country,
    population,
    landAreaSqKm,
    ruralPopulationShare,
    services,
    climate,
    metrics,
  };
}

function geoBoundaryApiUrl(country: PilotCountry): string {
  return `https://www.geoboundaries.org/api/current/${GEOboundaries_RELEASE}/${country.iso3}/ADM1/`;
}

async function fetchGeoBoundary(country: PilotCountry): Promise<{
  metadata: GeoBoundaryMetadata;
  features: GeoJsonFeature[];
  geometrySourceUrl: string;
}> {
  const metadata = (await fetchJson(geoBoundaryApiUrl(country))) as GeoBoundaryMetadata;
  const geometrySourceUrl = metadata.simplifiedGeometryGeoJSON ?? metadata.gjDownloadURL;
  const geojson = (await fetchJson(geometrySourceUrl)) as GeoJsonFeatureCollection;

  if (!Array.isArray(geojson.features)) {
    throw new Error(`No geoBoundary features for ${country.name}`);
  }

  return {
    metadata,
    features: geojson.features,
    geometrySourceUrl,
  };
}

function getProperty(feature: GeoJsonFeature, key: string): string {
  const value = feature.properties[key];
  return typeof value === "string" ? value : "";
}

function getFeatureBbox(
  geometry: GeoJsonGeometry
): { minLon: number; minLat: number; maxLon: number; maxLat: number } {
  const points: number[][] =
    geometry.type === "Polygon"
      ? geometry.coordinates.flat()
      : geometry.coordinates.flat(2);

  const lons = points.map((point) => point[0]);
  const lats = points.map((point) => point[1]);

  return {
    minLon: Math.min(...lons),
    minLat: Math.min(...lats),
    maxLon: Math.max(...lons),
    maxLat: Math.max(...lats),
  };
}

function centroidFromBbox(bbox: {
  minLon: number;
  minLat: number;
  maxLon: number;
  maxLat: number;
}): { lat: number; lon: number } {
  return {
    lat: round((bbox.minLat + bbox.maxLat) / 2, 6),
    lon: round((bbox.minLon + bbox.maxLon) / 2, 6),
  };
}

function ringAreaSqKm(ring: number[][]): number {
  if (ring.length < 4) return 0;

  const earthRadiusKm = 6371.0088;
  const lat0 =
    (ring.reduce((sum, point) => sum + point[1], 0) / ring.length / 180) *
    Math.PI;
  const projected = ring.map(([lon, lat]) => {
    const x = ((lon / 180) * Math.PI) * Math.cos(lat0) * earthRadiusKm;
    const y = ((lat / 180) * Math.PI) * earthRadiusKm;
    return [x, y];
  });

  let area = 0;
  for (let index = 0; index < projected.length - 1; index += 1) {
    const [x1, y1] = projected[index];
    const [x2, y2] = projected[index + 1];
    area += x1 * y2 - x2 * y1;
  }

  return Math.abs(area) / 2;
}

function polygonAreaSqKm(polygon: number[][][]): number {
  const [outer, ...holes] = polygon;
  return Math.max(
    0,
    ringAreaSqKm(outer) - holes.reduce((sum, ring) => sum + ringAreaSqKm(ring), 0)
  );
}

function geometryAreaSqKm(geometry: GeoJsonGeometry): number {
  if (geometry.type === "Polygon") {
    return polygonAreaSqKm(geometry.coordinates);
  }

  return geometry.coordinates.reduce(
    (sum, polygon) => sum + polygonAreaSqKm(polygon),
    0
  );
}

type ClipRect = {
  minLon: number;
  minLat: number;
  maxLon: number;
  maxLat: number;
};

function polygonBbox(coordinates: number[][][]): ClipRect {
  const points = coordinates.flat();
  const lons = points.map((point) => point[0]);
  const lats = points.map((point) => point[1]);

  return {
    minLon: Math.min(...lons),
    minLat: Math.min(...lats),
    maxLon: Math.max(...lons),
    maxLat: Math.max(...lats),
  };
}

function splitPolygonIntoTiles(
  coordinates: number[][][],
  targetMaxAreaSqKm = 80_000
): number[][][][] {
  const areaSqKm = polygonAreaSqKm(coordinates);
  const divisions = Math.max(2, Math.ceil(Math.sqrt(areaSqKm / targetMaxAreaSqKm)));
  const bbox = polygonBbox(coordinates);
  const lonStep = (bbox.maxLon - bbox.minLon) / divisions;
  const latStep = (bbox.maxLat - bbox.minLat) / divisions;
  const tiles: number[][][][] = [];

  for (let lonIndex = 0; lonIndex < divisions; lonIndex += 1) {
    for (let latIndex = 0; latIndex < divisions; latIndex += 1) {
      const rect = {
        minLon: bbox.minLon + lonIndex * lonStep,
        maxLon: bbox.minLon + (lonIndex + 1) * lonStep,
        minLat: bbox.minLat + latIndex * latStep,
        maxLat: bbox.minLat + (latIndex + 1) * latStep,
      };
      const clipPolygon: Polygon = [
        [
          [rect.minLon, rect.minLat],
          [rect.maxLon, rect.minLat],
          [rect.maxLon, rect.maxLat],
          [rect.minLon, rect.maxLat],
          [rect.minLon, rect.minLat],
        ],
      ];
      const clippedPolygons = intersection(
        coordinates as Polygon,
        clipPolygon
      ) as MultiPolygon;

      for (const clippedCoordinates of clippedPolygons) {
        if (polygonAreaSqKm(clippedCoordinates) >= 1) {
          tiles.push(clippedCoordinates);
        }
      }
    }
  }

  return tiles;
}

async function fetchPhilippinesAdminPopulations(): Promise<Map<string, PopulationValue>> {
  const shapeEntries = Object.entries(PHILIPPINES_PSA_REGION_CODE_BY_SHAPE_ISO);
  const locationCodes = shapeEntries.map((entry) => entry[1]);
  const shapeIsoByLocationCode = new Map(
    shapeEntries.map(([shapeIso, locationCode]) => [locationCode, shapeIso])
  );

  const query = {
    query: [
      { code: "Parameter", selection: { filter: "item", values: ["0"] } },
      {
        code: "Geographic Location",
        selection: { filter: "item", values: locationCodes },
      },
      { code: "Sex", selection: { filter: "item", values: ["0"] } },
      { code: "Age Group", selection: { filter: "item", values: ["0"] } },
    ],
    response: { format: "JSON" },
  };

  const json = asRecord(
    await fetchJson(PSA_OPENSTAT_POPULATION_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(query),
    })
  );
  const rows = asArray(json.data);
  const sourceLabel =
    asString(json.source) ??
    "Philippine Statistics Authority, 2020 Census of Population and Housing";
  const populations = new Map<string, PopulationValue>();

  for (const rowValue of rows) {
    const row = asRecord(rowValue);
    const key = asArray(row.key);
    const values = asArray(row.values);
    const locationCode = String(key[1]);
    const shapeIso = shapeIsoByLocationCode.get(locationCode);
    const population = Number(values[0]);

    if (!shapeIso || !Number.isFinite(population)) continue;

    populations.set(shapeIso, {
      year: 2020,
      value: population,
      sourceLabel,
      sourceUrl: PSA_OPENSTAT_POPULATION_URL,
      method:
        "Official PSA OpenSTAT 2020 Census total population by region, both sexes, all ages.",
    });
  }

  return populations;
}

function worldPopPayload(coordinates: number[][][]): string {
  return JSON.stringify({
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        properties: {},
        geometry: {
          type: "Polygon",
          coordinates,
        },
      },
    ],
  });
}

function getWorldPopPopulation(json: unknown): number | undefined {
  const data = asRecord(asRecord(json).data);
  const population = Number(data.total_population);
  return Number.isFinite(population) ? population : undefined;
}

async function pollWorldPopTask(taskId: string): Promise<number> {
  const taskUrl = `https://api.worldpop.org/v1/tasks/${taskId}`;

  for (let attempt = 1; attempt <= 12; attempt += 1) {
    const json = asRecord(await fetchJson(taskUrl));

    if (json.error === true) {
      throw new Error(
        `WorldPop task ${taskId} failed: ${String(json.error_message ?? "unknown")}`
      );
    }

    const population = getWorldPopPopulation(json);
    if (population !== undefined) {
      return population;
    }

    if (json.status === "finished") {
      throw new Error(`WorldPop task ${taskId} finished without population data`);
    }

    await sleep(2500 * attempt);
  }

  throw new Error(`WorldPop task ${taskId} did not finish in time`);
}

async function fetchWorldPopPolygonPopulation(coordinates: number[][][]): Promise<number> {
  const body = new URLSearchParams({
    dataset: "wpgppop",
    year: String(WORLDPOP_YEAR),
    runasync: "false",
    geojson: worldPopPayload(coordinates),
  });

  const json = asRecord(
    await fetchJson(WORLDPOP_STATS_URL, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    })
  );

  if (json.error === true) {
    throw new Error(`WorldPop failed: ${String(json.error_message ?? "unknown")}`);
  }

  let population = getWorldPopPopulation(json);
  if (population === undefined && typeof json.taskid === "string") {
    population = await pollWorldPopTask(json.taskid);
  }

  if (population === undefined) {
    throw new Error("WorldPop response did not include total_population");
  }

  return Math.round(population);
}

async function fetchWorldPopPolygonPopulationSafe(
  coordinates: number[][][],
  depth = 0
): Promise<{ population: number; polygonRequests: number; split: boolean }> {
  const areaSqKm = polygonAreaSqKm(coordinates);

  if (areaSqKm <= 90_000 || depth >= 4) {
    try {
      return {
        population: await fetchWorldPopPolygonPopulation(coordinates),
        polygonRequests: 1,
        split: depth > 0,
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      if (!message.includes("too large") || depth >= 4) {
        throw error;
      }
    }
  }

  const tiles = splitPolygonIntoTiles(coordinates);
  let population = 0;
  let polygonRequests = 0;

  for (const [index, tile] of tiles.entries()) {
    const result = await fetchWorldPopPolygonPopulationSafe(tile, depth + 1);
    population += result.population;
    polygonRequests += result.polygonRequests;
    if (index < tiles.length - 1) {
      await sleepAfterNetwork(600);
    }
  }

  return { population, polygonRequests, split: true };
}

async function fetchWorldPopPopulation(feature: GeoJsonFeature): Promise<PopulationValue> {
  const polygons =
    feature.geometry.type === "Polygon"
      ? [feature.geometry.coordinates]
      : feature.geometry.coordinates;
  let population = 0;
  let polygonRequests = 0;
  let usedSplitTiles = false;

  for (const [index, coordinates] of polygons.entries()) {
    const result = await fetchWorldPopPolygonPopulationSafe(coordinates);
    population += result.population;
    polygonRequests += result.polygonRequests;
    usedSplitTiles = usedSplitTiles || result.split;
    if (index < polygons.length - 1) {
      await sleepAfterNetwork(900);
    }
  }

  return {
    year: WORLDPOP_YEAR,
    value: population,
    sourceLabel: "WorldPop Global Project population count",
    sourceUrl: `${WORLDPOP_STATS_URL}?dataset=wpgppop&year=${WORLDPOP_YEAR}`,
    method:
      usedSplitTiles
        ? `WorldPop stats API total_population summed over ${polygonRequests} clipped polygon tiles because at least one ADM1 polygon exceeded the API area allowance.`
        : polygons.length === 1
          ? "WorldPop stats API total_population over the geoBoundaries ADM1 polygon."
          : `WorldPop stats API total_population summed over ${polygons.length} polygon parts from the geoBoundaries ADM1 MultiPolygon.`,
  };
}

function overpassAdminAreaQuery(admin1Code: string): string {
  return `[out:json][timeout:240];
area["ISO3166-2"="${admin1Code}"]->.searchArea;
nwr["amenity"~"^(hospital|clinic|doctors)$"](area.searchArea)->.health;
nwr["amenity"="school"](area.searchArea)->.education;
nwr["amenity"="marketplace"](area.searchArea)->.markets;
make count iso="${admin1Code}",
  health=health.count(nodes)+health.count(ways)+health.count(relations),
  education=education.count(nodes)+education.count(ways)+education.count(relations),
  markets=markets.count(nodes)+markets.count(ways)+markets.count(relations);
out;`;
}

function overpassAdminBboxQuery(
  admin1Code: string,
  bbox: { minLon: number; minLat: number; maxLon: number; maxLat: number }
): string {
  const overpassBbox = `(${bbox.minLat},${bbox.minLon},${bbox.maxLat},${bbox.maxLon})`;

  return `[out:json][timeout:240];
nwr["amenity"~"^(hospital|clinic|doctors)$"]${overpassBbox}->.health;
nwr["amenity"="school"]${overpassBbox}->.education;
nwr["amenity"="marketplace"]${overpassBbox}->.markets;
make count iso="${admin1Code}",
  health=health.count(nodes)+health.count(ways)+health.count(relations),
  education=education.count(nodes)+education.count(ways)+education.count(relations),
  markets=markets.count(nodes)+markets.count(ways)+markets.count(relations);
out;`;
}

function parseAdminServices(
  json: unknown,
  queryMode: AdminServiceCounts["queryMode"],
  sourceUrl: string
): AdminServiceCounts {
  const root = asRecord(json);
  const elements = asArray(root.elements);
  const countElement = elements.map(asRecord).find((element) => {
    const tags = asRecord(element.tags);
    return tags.health !== undefined || tags.education !== undefined;
  });
  const tags = asRecord(countElement?.tags);
  const health = Number(tags.health);
  const education = Number(tags.education);
  const markets = Number(tags.markets);
  const osm3s = asRecord(root.osm3s);

  if (![health, education, markets].every(Number.isFinite)) {
    throw new Error("Overpass admin service response did not include all counts");
  }

  return {
    health,
    education,
    markets,
    total: health + education + markets,
    sourceUrl,
    queryMode,
    osmTimestamp: asString(osm3s.timestamp_osm_base),
    osmAreasTimestamp: asString(osm3s.timestamp_areas_base),
  };
}

async function runOverpassAdminQuery(
  query: string,
  queryMode: AdminServiceCounts["queryMode"]
): Promise<AdminServiceCounts> {
  let lastError: Error | undefined;

  for (const endpoint of OVERPASS_ENDPOINTS) {
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        const json = await fetchJson(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({ data: query }),
        });
        return parseAdminServices(json, queryMode, endpoint);
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        await sleep(3500 * attempt);
      }
    }
  }

  throw lastError ?? new Error("Overpass admin query failed");
}

async function fetchAdminServices(
  admin1Code: string,
  bbox: { minLon: number; minLat: number; maxLon: number; maxLat: number }
): Promise<AdminServiceCounts> {
  try {
    const areaResult = await runOverpassAdminQuery(
      overpassAdminAreaQuery(admin1Code),
      "osm_area_iso3166_2"
    );

    if (areaResult.total > 0) {
      return areaResult;
    }
  } catch (error) {
    console.warn(
      `Overpass ISO area query failed for ${admin1Code}; trying bbox fallback. ${
        error instanceof Error ? error.message : String(error)
      }`
    );
  }

  return runOverpassAdminQuery(
    overpassAdminBboxQuery(admin1Code, bbox),
    "bbox_fallback"
  );
}

function computeAdminMetrics(
  population: number,
  areaSqKm: number,
  services: AdminServiceCounts,
  climate: ClimateValues
): AdminAccessResult["metrics"] {
  const peoplePerHealthFacility = population / Math.max(services.health, 1);
  const peoplePerSchool = population / Math.max(services.education, 1);
  const peoplePerMarket = population / Math.max(services.markets, 1);

  const healthPressure = pressureScore(peoplePerHealthFacility, 5_000, 50_000);
  const schoolPressure = pressureScore(peoplePerSchool, 1_200, 12_000);
  const marketPressure = pressureScore(peoplePerMarket, 15_000, 150_000);
  const serviceLoadScore = clamp(
    healthPressure * 0.45 + schoolPressure * 0.35 + marketPressure * 0.2
  );

  const totalMappedServicesPerMillion = (services.total / population) * 1_000_000;
  const osmCompletenessRiskScore = clamp((250 - totalMappedServicesPerMillion) / 250);
  const heatStressScore = clamp(climate.heatDeltaC / 2);
  const rainfallStressScore = clamp(Math.abs(climate.precipChangePct) / 15);
  const accessStressIndex = Math.round(
    100 *
      (serviceLoadScore * 0.58 +
        heatStressScore * 0.18 +
        rainfallStressScore * 0.14 +
        osmCompletenessRiskScore * 0.1)
  );

  return {
    peoplePerHealthFacility: Math.round(peoplePerHealthFacility),
    peoplePerSchool: Math.round(peoplePerSchool),
    peoplePerMarket: Math.round(peoplePerMarket),
    healthFacilitiesPer100k: round((services.health / population) * 100_000),
    schoolsPer100k: round((services.education / population) * 100_000),
    marketsPer100k: round((services.markets / population) * 100_000),
    totalMappedServicesPerMillion: round(totalMappedServicesPerMillion),
    totalServicesPer1000SqKm: round((services.total / Math.max(areaSqKm, 1)) * 1000),
    serviceLoadScore: round(serviceLoadScore * 100, 1),
    heatStressScore: round(heatStressScore * 100, 1),
    rainfallStressScore: round(rainfallStressScore * 100, 1),
    osmCompletenessRiskScore: round(osmCompletenessRiskScore * 100, 1),
    accessStressIndex,
    bottleneck: chooseBottleneck({
      "service load": serviceLoadScore,
      "heat stress": heatStressScore,
      "rainfall change": rainfallStressScore,
      "OSM completeness": osmCompletenessRiskScore,
    }),
  };
}

async function buildAdminUnit(
  country: PilotResult,
  boundary: GeoBoundaryMetadata,
  geometrySourceUrl: string,
  feature: GeoJsonFeature,
  philippinesPopulations: Map<string, PopulationValue>
): Promise<AdminAccessResult> {
  const admin1Code = getProperty(feature, "shapeISO");
  const admin1Name = getProperty(feature, "shapeName");
  const shapeId = getProperty(feature, "shapeID");
  const bbox = getFeatureBbox(feature.geometry);
  const centroid = centroidFromBbox(bbox);
  const approxAreaSqKm = round(geometryAreaSqKm(feature.geometry), 2);

  if (!admin1Code || !admin1Name) {
    throw new Error(`Missing ADM1 code or name for ${country.name}`);
  }

  let population: PopulationValue;
  if (country.iso3 === "PHL") {
    const officialPopulation = philippinesPopulations.get(admin1Code);
    if (!officialPopulation) {
      throw new Error(`No PSA population match for ${admin1Code}/${admin1Name}`);
    }
    population = officialPopulation;
  } else {
    population = await fetchWorldPopPopulation(feature);
  }

  const services = await fetchAdminServices(admin1Code, bbox);
  const metrics = computeAdminMetrics(
    population.value,
    approxAreaSqKm,
    services,
    country.climate
  );

  console.log(
    `${country.name} / ${admin1Name}: ${metrics.accessStressIndex} (${metrics.bottleneck})`
  );

  return {
    iso2: country.iso2,
    iso3: country.iso3,
    countryName: country.name,
    admin1Code,
    admin1Name,
    shapeId,
    centroid,
    bbox,
    approxAreaSqKm,
    boundary: {
      boundaryID: boundary.boundaryID,
      boundaryYearRepresented: boundary.boundaryYearRepresented,
      boundarySource: boundary.boundarySource,
      boundaryLicense: boundary.boundaryLicense,
      geometrySourceUrl,
    },
    population,
    services,
    climate: country.climate,
    metrics,
  };
}

function adminOutputSummary(admin1: AdminAccessResult[]) {
  const highest = [...admin1].sort(
    (a, b) => b.metrics.accessStressIndex - a.metrics.accessStressIndex
  )[0];
  const totalPopulation = admin1.reduce(
    (sum, admin) => sum + admin.population.value,
    0
  );
  const totalMappedServices = admin1.reduce(
    (sum, admin) => sum + admin.services.total,
    0
  );
  const bboxFallbackCount = admin1.filter(
    (admin) => admin.services.queryMode === "bbox_fallback"
  ).length;

  return {
    admin1Units: admin1.length,
    totalPopulation,
    totalMappedServices,
    bboxFallbackCount,
    highestStressAdmin: highest
      ? {
          countryName: highest.countryName,
          admin1Name: highest.admin1Name,
          admin1Code: highest.admin1Code,
          accessStressIndex: highest.metrics.accessStressIndex,
          bottleneck: highest.metrics.bottleneck,
        }
      : null,
    populationSources: {
      psaOpenStatRegions: admin1.filter((admin) =>
        admin.population.sourceLabel.includes("Philippine Statistics Authority")
      ).length,
      worldPopStats: admin1.filter((admin) =>
        admin.population.sourceLabel.includes("WorldPop")
      ).length,
    },
  };
}

async function buildAdminScreening(countries: PilotResult[]) {
  console.log("\n=== ADM1 ACCESS-SERVICES SCREENING ===");
  const needsPhilippinesPopulation = countries.some(
    (country) => country.iso3 === "PHL"
  );
  const philippinesPopulations = needsPhilippinesPopulation
    ? await fetchPhilippinesAdminPopulations()
    : new Map<string, PopulationValue>();
  if (needsPhilippinesPopulation) {
    console.log("Fetched official Philippines regional population table.");
  }
  const admin1: AdminAccessResult[] = [];

  for (const country of countries) {
    console.log(`\nFetching geoBoundaries ADM1 for ${country.name}...`);
    const boundary = await fetchGeoBoundary(country);
    const features = [...boundary.features].sort((a, b) =>
      getProperty(a, "shapeISO").localeCompare(getProperty(b, "shapeISO"))
    );

    for (const feature of features) {
      const adminName = getProperty(feature, "shapeName");
      console.log(`Fetching population and services for ${country.name} / ${adminName}...`);
      admin1.push(
        await buildAdminUnit(
          country,
          boundary.metadata,
          boundary.geometrySourceUrl,
          feature,
          philippinesPopulations
        )
      );
      await sleepAfterNetwork(1500);
    }
  }

  return {
    metadata: {
      title: "Climate-Adjusted Access to Services - ADM1 Screening",
      generatedAt: new Date().toISOString(),
      script: "scripts/research/access-services-pipeline.ts",
      status: "computed_admin1_screening_index",
      geography: "ADM1",
      caveat:
        "This is an admin-1 screening layer. It is not yet a road-network travel-time surface, flood disruption model, or facility catchment model.",
      method:
        "Joins ADM1 boundaries, population, OSM service counts, and national climate deltas; computes a transparent service-pressure and climate-stress screen for prioritizing deeper travel-time modeling.",
      sources: [
        "https://www.geoboundaries.org/api.html",
        ...(needsPhilippinesPopulation ? [PSA_OPENSTAT_POPULATION_URL] : []),
        `${WORLDPOP_STATS_URL}?dataset=wpgppop&year=${WORLDPOP_YEAR}`,
        "https://overpass-api.de/",
        "https://www.openstreetmap.org/copyright",
        "https://climateknowledgeportal.worldbank.org/download-data",
      ],
      populationCaveat:
        needsPhilippinesPopulation
          ? "Philippines ADM1 population uses official PSA OpenSTAT 2020 regional census values. Non-Philippines ADM1 population uses WorldPop 2020 polygon statistics over geoBoundaries polygons; oversized polygons are summed across clipped tiles when required by the WorldPop API area allowance."
          : "ADM1 population uses WorldPop 2020 polygon statistics over geoBoundaries polygons; oversized polygons are summed across clipped tiles when required by the WorldPop API area allowance.",
      serviceCaveat:
        "OSM service counts depend on mapper coverage and tagging. Counts use OSM admin areas matched by ISO3166-2 where available and fall back to bounding boxes only if the area query fails.",
      cacheNote:
        "Network responses are cached under .cache/research/access-services unless ACCESS_REFRESH=1 is set.",
    },
    summary: adminOutputSummary(admin1),
    admin1,
  };
}

function nextWaveOutputSummary(
  countries: PilotResult[],
  admin1: AdminAccessResult[]
) {
  const adminSummary = adminOutputSummary(admin1);
  const highestNational = [...countries].sort(
    (a, b) => b.metrics.accessStressIndex - a.metrics.accessStressIndex
  )[0];

  return {
    ...adminSummary,
    economiesComputed: countries.length,
    highestNationalStressEconomy: highestNational
      ? {
          name: highestNational.name,
          iso3: highestNational.iso3,
          accessStressIndex: highestNational.metrics.accessStressIndex,
          bottleneck: highestNational.metrics.bottleneck,
        }
      : null,
  };
}

async function writeJson(relativePath: string, data: unknown): Promise<void> {
  const outputPath = path.join(process.cwd(), relativePath);
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(data, null, 2)}\n`);
}

function csvEscape(value: unknown): string {
  const text = String(value ?? "");
  if (/[",\r\n]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}

async function writeText(relativePath: string, data: string): Promise<void> {
  const outputPath = path.join(process.cwd(), relativePath);
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, data);
}

function adminCsv(admin1: AdminAccessResult[]): string {
  const columns = [
    "country_name",
    "iso3",
    "admin1_code",
    "admin1_name",
    "population_year",
    "population",
    "population_source",
    "health_facilities",
    "schools",
    "markets",
    "total_services",
    "people_per_health_facility",
    "people_per_school",
    "people_per_market",
    "total_mapped_services_per_million",
    "service_load_score",
    "osm_completeness_risk_score",
    "access_stress_index",
    "bottleneck",
    "service_query_mode",
    "osm_timestamp",
    "centroid_lat",
    "centroid_lon",
    "approx_area_sq_km",
  ];
  const rows = admin1.map((admin) => [
    admin.countryName,
    admin.iso3,
    admin.admin1Code,
    admin.admin1Name,
    admin.population.year,
    admin.population.value,
    admin.population.sourceLabel,
    admin.services.health,
    admin.services.education,
    admin.services.markets,
    admin.services.total,
    admin.metrics.peoplePerHealthFacility,
    admin.metrics.peoplePerSchool,
    admin.metrics.peoplePerMarket,
    admin.metrics.totalMappedServicesPerMillion,
    admin.metrics.serviceLoadScore,
    admin.metrics.osmCompletenessRiskScore,
    admin.metrics.accessStressIndex,
    admin.metrics.bottleneck,
    admin.services.queryMode,
    admin.services.osmTimestamp ?? "",
    admin.centroid.lat,
    admin.centroid.lon,
    admin.approxAreaSqKm,
  ]);

  return [
    columns.join(","),
    ...rows.map((row) => row.map(csvEscape).join(",")),
  ].join("\n");
}

async function main(): Promise<void> {
  console.log("=== ACCESS-SERVICES PILOT PIPELINE ===");
  console.log("Pilots: Philippines and Bangladesh");
  console.log(
    "Sources: World Bank WDI, World Bank CCKP, OpenStreetMap/Overpass, geoBoundaries, PSA OpenSTAT, WorldPop"
  );

  const countries: PilotResult[] = [];
  for (const country of COUNTRIES) {
    countries.push(await buildPilot(country));
  }

  const nationalOutput = {
    metadata: {
      title: "Climate-Adjusted Access to Services - Pilot Screening",
      generatedAt: new Date().toISOString(),
      script: "scripts/research/access-services-pipeline.ts",
      status: "computed_screening_index",
      caveat:
        "This is a first national screening index. It is not yet a travel-time raster or facility catchment model.",
      sources: [
        "https://api.worldbank.org/v2",
        "https://climateknowledgeportal.worldbank.org/download-data",
        "https://overpass.kumi.systems/api/interpreter",
        "https://www.openstreetmap.org/copyright",
      ],
      method:
        "Counts mapped health, school, and market services; joins country population, land area, rural share, and climate deltas; computes a transparent access stress index for pilot prioritization.",
    },
    countries,
  };

  const adminOutput = await buildAdminScreening(countries);
  const csv = `${adminCsv(adminOutput.admin1)}\n`;

  console.log("\n=== NEXT-WAVE ADM1 ACCESS-SERVICES SCREENING ===");
  console.log("Next wave: Pakistan, Nepal, Sri Lanka");
  const nextWaveCountries: PilotResult[] = [];
  for (const country of NEXT_WAVE_COUNTRIES) {
    nextWaveCountries.push(await buildPilot(country));
  }
  const nextWaveAdminOutput = await buildAdminScreening(nextWaveCountries);
  const nextWaveOutput = {
    ...nextWaveAdminOutput,
    metadata: {
      ...nextWaveAdminOutput.metadata,
      title: "Climate-Adjusted Access to Services - Next-Wave ADM1 Screening",
      status: "computed_nextwave_admin1_screening_index",
      caveat:
        "This is a next-wave admin-1 screening layer for Pakistan, Nepal, and Sri Lanka. It is not yet a road-network travel-time surface, flood disruption model, or facility catchment model.",
      method:
        "Computes national screening metrics and ADM1 service-pressure metrics for tractable high-readiness ADB economies using WDI, CCKP, geoBoundaries, WorldPop, and OSM/Overpass.",
      populationCaveat:
        "ADM1 population uses WorldPop 2020 polygon statistics over geoBoundaries polygons; oversized polygons are summed across clipped tiles when required by the WorldPop API area allowance. National population uses latest available World Bank WDI values.",
      selectionNote:
        "Pakistan, Nepal, and Sri Lanka were selected as a tractable next wave: high source readiness, policy relevance, and small enough ADM1 counts for reproducible local runs. Larger high-priority economies such as India, PRC, Indonesia, and Viet Nam should run as separate batches.",
    },
    summary: nextWaveOutputSummary(nextWaveCountries, nextWaveAdminOutput.admin1),
    countries: nextWaveCountries,
  };
  const nextWaveCsv = `${adminCsv(nextWaveOutput.admin1)}\n`;

  console.log("\n=== FRONTIER ADM1 ACCESS-SERVICES SCREENING ===");
  console.log("Frontier batch: Cambodia, Lao PDR, Timor-Leste");
  const frontierCountries: PilotResult[] = [];
  for (const country of FRONTIER_BATCH_COUNTRIES) {
    frontierCountries.push(await buildPilot(country));
  }
  const frontierAdminOutput = await buildAdminScreening(frontierCountries);
  const frontierOutput = {
    ...frontierAdminOutput,
    metadata: {
      ...frontierAdminOutput.metadata,
      title: "Climate-Adjusted Access to Services - Frontier ADM1 Screening",
      status: "computed_frontier_admin1_screening_index",
      caveat:
        "This is a frontier admin-1 screening layer for Cambodia, Lao PDR, and Timor-Leste. It is not yet a road-network travel-time surface, flood disruption model, or facility catchment model.",
      method:
        "Computes national screening metrics and ADM1 service-pressure metrics for a tractable Mekong and island-state batch using WDI, CCKP, geoBoundaries, WorldPop, and OSM/Overpass.",
      populationCaveat:
        "ADM1 population uses WorldPop 2020 polygon statistics over geoBoundaries polygons; oversized polygons are summed across clipped tiles when required by the WorldPop API area allowance. National population uses latest available World Bank WDI values.",
      selectionNote:
        "Cambodia, Lao PDR, and Timor-Leste were selected as the next computed batch because they are high-readiness ADB economies with manageable ADM1 counts and different access-risk geographies from the South Asia pilots.",
    },
    summary: nextWaveOutputSummary(frontierCountries, frontierAdminOutput.admin1),
    countries: frontierCountries,
  };
  const frontierCsv = `${adminCsv(frontierOutput.admin1)}\n`;

  const computedAdmin1 = [
    ...adminOutput.admin1,
    ...nextWaveOutput.admin1,
    ...frontierOutput.admin1,
  ];
  const computedCountryNames = Array.from(
    new Set(computedAdmin1.map((admin) => admin.countryName))
  );
  const computedAdmin1Output = {
    metadata: {
      title: "Climate-Adjusted Access to Services - Computed ADM1 Coverage",
      generatedAt: new Date().toISOString(),
      script: "scripts/research/access-services-pipeline.ts",
      status: "computed_multi_batch_admin1_screening_index",
      geography: "ADM1",
      caveat:
        "This combined artifact merges computed ADM1 screening batches. It is not yet a road-network travel-time surface, flood disruption model, or facility catchment model.",
      method:
        "Concatenates the pilot, next-wave, and frontier ADM1 outputs generated by the same access-services pipeline so the current computed coverage can be audited as one table.",
      populationCaveat:
        "Population methods are recorded per row. Philippines uses PSA OpenSTAT 2020 regional census values; other ADM1 rows use WorldPop 2020 polygon statistics, tiled where required by the WorldPop API area allowance.",
      serviceCaveat:
        "OSM service counts depend on mapper coverage and tagging. Counts use OSM admin areas matched by ISO3166-2 where available and fall back to bounding boxes only if the area query fails.",
      sourceOutputs: [
        "src/data/generated/access-services-admin1.json",
        "src/data/generated/access-services-nextwave-admin1.json",
        "src/data/generated/access-services-frontier-admin1.json",
      ],
    },
    summary: {
      ...adminOutputSummary(computedAdmin1),
      economiesComputed: computedCountryNames.length,
      economies: computedCountryNames,
      batches: [
        {
          name: "pilot",
          economies: countries.map((country) => country.name),
          admin1Units: adminOutput.summary.admin1Units,
        },
        {
          name: "next_wave",
          economies: nextWaveCountries.map((country) => country.name),
          admin1Units: nextWaveOutput.summary.admin1Units,
        },
        {
          name: "frontier",
          economies: frontierCountries.map((country) => country.name),
          admin1Units: frontierOutput.summary.admin1Units,
        },
      ],
    },
    admin1: computedAdmin1,
  };
  const computedAdmin1Csv = `${adminCsv(computedAdmin1Output.admin1)}\n`;

  await writeJson("src/data/generated/access-services-pilots.json", nationalOutput);
  await writeJson("public/data/access-services-pilots.json", nationalOutput);
  await writeJson("src/data/generated/access-services-admin1.json", adminOutput);
  await writeJson("public/data/access-services-admin1.json", adminOutput);
  await writeText("public/data/access-services-admin1.csv", csv);
  await writeText("research/access-services/generated/access-services-admin1.csv", csv);
  await writeJson(
    "src/data/generated/access-services-nextwave-admin1.json",
    nextWaveOutput
  );
  await writeJson(
    "public/data/access-services-nextwave-admin1.json",
    nextWaveOutput
  );
  await writeText("public/data/access-services-nextwave-admin1.csv", nextWaveCsv);
  await writeText(
    "research/access-services/generated/access-services-nextwave-admin1.csv",
    nextWaveCsv
  );
  await writeJson(
    "src/data/generated/access-services-frontier-admin1.json",
    frontierOutput
  );
  await writeJson(
    "public/data/access-services-frontier-admin1.json",
    frontierOutput
  );
  await writeText("public/data/access-services-frontier-admin1.csv", frontierCsv);
  await writeText(
    "research/access-services/generated/access-services-frontier-admin1.csv",
    frontierCsv
  );
  await writeJson(
    "src/data/generated/access-services-computed-admin1.json",
    computedAdmin1Output
  );
  await writeJson(
    "public/data/access-services-computed-admin1.json",
    computedAdmin1Output
  );
  await writeText(
    "public/data/access-services-computed-admin1.csv",
    computedAdmin1Csv
  );
  await writeText(
    "research/access-services/generated/access-services-computed-admin1.csv",
    computedAdmin1Csv
  );

  console.log("\nWrote src/data/generated/access-services-pilots.json");
  console.log("Wrote public/data/access-services-pilots.json");
  console.log("Wrote src/data/generated/access-services-admin1.json");
  console.log("Wrote public/data/access-services-admin1.json");
  console.log("Wrote public/data/access-services-admin1.csv");
  console.log("Wrote research/access-services/generated/access-services-admin1.csv");
  console.log("Wrote src/data/generated/access-services-nextwave-admin1.json");
  console.log("Wrote public/data/access-services-nextwave-admin1.json");
  console.log("Wrote public/data/access-services-nextwave-admin1.csv");
  console.log(
    "Wrote research/access-services/generated/access-services-nextwave-admin1.csv"
  );
  console.log("Wrote src/data/generated/access-services-frontier-admin1.json");
  console.log("Wrote public/data/access-services-frontier-admin1.json");
  console.log("Wrote public/data/access-services-frontier-admin1.csv");
  console.log(
    "Wrote research/access-services/generated/access-services-frontier-admin1.csv"
  );
  console.log("Wrote src/data/generated/access-services-computed-admin1.json");
  console.log("Wrote public/data/access-services-computed-admin1.json");
  console.log("Wrote public/data/access-services-computed-admin1.csv");
  console.log(
    "Wrote research/access-services/generated/access-services-computed-admin1.csv"
  );
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
