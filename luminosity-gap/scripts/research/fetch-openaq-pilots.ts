import { mkdir, readFile, writeFile } from "fs/promises";
import path from "path";
import readXlsxFile from "read-excel-file/node";

type OpenAQLocation = {
  id?: number;
  name?: string;
  datetimeLast?: string;
  parameters?: Array<{ id?: number; name?: string; displayName?: string }>;
  sensors?: Array<{
    id?: number;
    parameter?: { id?: number; name?: string; displayName?: string };
  }>;
};

type WdiValue = {
  value: number;
  year: number;
  source: string;
};

type WhoCityValidation = {
  status: "computed" | "no_city_pm25";
  citiesWithPm25: number;
  observations: number;
  latestYear: number | null;
  pm25CityMean: number | null;
  pm25CityMedian: number | null;
  pm25CityMax: number | null;
  citiesAboveWhoGuideline: number;
  cityShareAboveWhoGuideline: number | null;
  wdiMinusWhoCityMean: number | null;
  highestPm25City: {
    city: string;
    year: number;
    value: number;
  } | null;
};

const ADB_REGIONAL_MEMBERS = [
  { iso2: "AF", iso3: "AFG", name: "Afghanistan", subregion: "South Asia" },
  { iso2: "AM", iso3: "ARM", name: "Armenia", subregion: "Central and West Asia" },
  { iso2: "AU", iso3: "AUS", name: "Australia", subregion: "The Pacific" },
  { iso2: "AZ", iso3: "AZE", name: "Azerbaijan", subregion: "Central and West Asia" },
  { iso2: "BD", iso3: "BGD", name: "Bangladesh", subregion: "South Asia" },
  { iso2: "BT", iso3: "BTN", name: "Bhutan", subregion: "South Asia" },
  { iso2: "BN", iso3: "BRN", name: "Brunei Darussalam", subregion: "Southeast Asia" },
  { iso2: "KH", iso3: "KHM", name: "Cambodia", subregion: "Southeast Asia" },
  { iso2: "CK", iso3: "COK", name: "Cook Islands", subregion: "The Pacific" },
  { iso2: "CN", iso3: "CHN", name: "China, People's Republic of", subregion: "East Asia" },
  { iso2: "FJ", iso3: "FJI", name: "Fiji", subregion: "The Pacific" },
  { iso2: "GE", iso3: "GEO", name: "Georgia", subregion: "Central and West Asia" },
  { iso2: "HK", iso3: "HKG", name: "Hong Kong, China", subregion: "East Asia" },
  { iso2: "IN", iso3: "IND", name: "India", subregion: "South Asia" },
  { iso2: "ID", iso3: "IDN", name: "Indonesia", subregion: "Southeast Asia" },
  { iso2: "JP", iso3: "JPN", name: "Japan", subregion: "East Asia" },
  { iso2: "KZ", iso3: "KAZ", name: "Kazakhstan", subregion: "Central and West Asia" },
  { iso2: "KI", iso3: "KIR", name: "Kiribati", subregion: "The Pacific" },
  { iso2: "KR", iso3: "KOR", name: "Korea, Republic of", subregion: "East Asia" },
  { iso2: "KG", iso3: "KGZ", name: "Kyrgyz Republic", subregion: "Central and West Asia" },
  { iso2: "LA", iso3: "LAO", name: "Lao People's Democratic Republic", subregion: "Southeast Asia" },
  { iso2: "MY", iso3: "MYS", name: "Malaysia", subregion: "Southeast Asia" },
  { iso2: "MV", iso3: "MDV", name: "Maldives", subregion: "South Asia" },
  { iso2: "MH", iso3: "MHL", name: "Marshall Islands", subregion: "The Pacific" },
  { iso2: "FM", iso3: "FSM", name: "Micronesia, Federated States of", subregion: "The Pacific" },
  { iso2: "MN", iso3: "MNG", name: "Mongolia", subregion: "East Asia" },
  { iso2: "MM", iso3: "MMR", name: "Myanmar", subregion: "Southeast Asia" },
  { iso2: "NR", iso3: "NRU", name: "Nauru", subregion: "The Pacific" },
  { iso2: "NP", iso3: "NPL", name: "Nepal", subregion: "South Asia" },
  { iso2: "NZ", iso3: "NZL", name: "New Zealand", subregion: "The Pacific" },
  { iso2: "NU", iso3: "NIU", name: "Niue", subregion: "The Pacific" },
  { iso2: "PK", iso3: "PAK", name: "Pakistan", subregion: "South Asia" },
  { iso2: "PW", iso3: "PLW", name: "Palau", subregion: "The Pacific" },
  { iso2: "PG", iso3: "PNG", name: "Papua New Guinea", subregion: "The Pacific" },
  { iso2: "PH", iso3: "PHL", name: "Philippines", subregion: "Southeast Asia" },
  { iso2: "WS", iso3: "WSM", name: "Samoa", subregion: "The Pacific" },
  { iso2: "SG", iso3: "SGP", name: "Singapore", subregion: "Southeast Asia" },
  { iso2: "SB", iso3: "SLB", name: "Solomon Islands", subregion: "The Pacific" },
  { iso2: "LK", iso3: "LKA", name: "Sri Lanka", subregion: "South Asia" },
  { iso2: "TW", iso3: "TWN", name: "Taipei,China", subregion: "East Asia" },
  { iso2: "TJ", iso3: "TJK", name: "Tajikistan", subregion: "Central and West Asia" },
  { iso2: "TH", iso3: "THA", name: "Thailand", subregion: "Southeast Asia" },
  { iso2: "TL", iso3: "TLS", name: "Timor-Leste", subregion: "Southeast Asia" },
  { iso2: "TO", iso3: "TON", name: "Tonga", subregion: "The Pacific" },
  { iso2: "TR", iso3: "TUR", name: "Türkiye", subregion: "Central and West Asia" },
  { iso2: "TM", iso3: "TKM", name: "Turkmenistan", subregion: "Central and West Asia" },
  { iso2: "TV", iso3: "TUV", name: "Tuvalu", subregion: "The Pacific" },
  { iso2: "UZ", iso3: "UZB", name: "Uzbekistan", subregion: "Central and West Asia" },
  { iso2: "VU", iso3: "VUT", name: "Vanuatu", subregion: "The Pacific" },
  { iso2: "VN", iso3: "VNM", name: "Viet Nam", subregion: "Southeast Asia" },
];

const PARAMETERS = ["pm25", "pm10", "no2", "o3", "so2", "co"];
const JSON_OUTPUTS = [
  "src/data/generated/air-monitoring-openaq-pilots.json",
  "public/data/air-monitoring-openaq-pilots.json",
];
const CSV_OUTPUTS = [
  "research/air-monitoring/generated/openaq-adb-regional-economies.csv",
  "public/data/air-monitoring-openaq-economies.csv",
];
const WORLD_BANK_API = "https://api.worldbank.org/v2";
const POPULATION_INDICATOR = "SP.POP.TOTL";
const PM25_EXPOSURE_INDICATOR = "EN.ATM.PM25.MC.M3";
const WHO_AIR_QUALITY_DATABASE_URL =
  "https://cdn.who.int/media/docs/default-source/air-pollution-documents/air-quality-and-health/who_ambient_air_quality_database_version_2024_(v6.1).xlsx?download=true&sfvrsn=c504c0cd_3";
const WHO_PM25_ANNUAL_GUIDELINE = 5;

function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null
    ? (value as Record<string, unknown>)
    : {};
}

async function loadLocalEnv(): Promise<void> {
  const envPath = path.join(process.cwd(), ".env.local");

  try {
    const content = await readFile(envPath, "utf8");
    for (const rawLine of content.split(/\r?\n/)) {
      const line = rawLine.trim();
      if (!line || line.startsWith("#")) {
        continue;
      }

      const separator = line.indexOf("=");
      if (separator === -1) {
        continue;
      }

      const key = line.slice(0, separator).trim();
      const value = line
        .slice(separator + 1)
        .trim()
        .replace(/^['"]|['"]$/g, "");

      if (key && process.env[key] === undefined) {
        process.env[key] = value;
      }
    }
  } catch {
    // Optional local file. Missing .env.local should keep the explicit blocked-state path.
  }
}

function getApiKey(): string | undefined {
  return process.env.OPENAQ_API_KEY || process.env.NEXT_PUBLIC_OPENAQ_API_KEY;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchOpenAQ(url: string, apiKey: string): Promise<unknown> {
  let lastError = "";

  for (let attempt = 1; attempt <= 3; attempt += 1) {
    const response = await fetch(url, {
      headers: {
        "X-API-Key": apiKey,
        "User-Agent": "DevelopmentBlindspotsLab/0.1 research pipeline",
      },
    });

    if (response.ok) {
      return response.json();
    }

    const body = await response.text();
    lastError = `OpenAQ HTTP ${response.status}: ${body.slice(0, 240)}`;

    if (![408, 429, 500, 502, 503, 504].includes(response.status)) {
      break;
    }

    await sleep(1_500 * attempt);
  }

  throw new Error(lastError);
}

async function fetchWorldBankLatestIndicator(
  indicator: string
): Promise<Map<string, WdiValue>> {
  const url = `${WORLD_BANK_API}/country/all/indicator/${indicator}?format=json&per_page=20000&mrv=1`;
  const response = await fetch(url, {
    headers: {
      "User-Agent": "DevelopmentBlindspotsLab/0.1 research pipeline",
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`World Bank ${indicator} HTTP ${response.status}: ${body.slice(0, 240)}`);
  }

  const json = (await response.json()) as unknown;
  const rows = Array.isArray(json) && Array.isArray(json[1]) ? json[1] : [];
  const values = new Map<string, WdiValue>();

  for (const row of rows) {
    const record = asRecord(row);
    const iso3 = typeof record.countryiso3code === "string" ? record.countryiso3code : "";
    const value = typeof record.value === "number" ? record.value : null;
    const year = typeof record.date === "string" ? Number.parseInt(record.date, 10) : NaN;

    if (iso3 && value !== null && Number.isFinite(year)) {
      values.set(iso3, {
        value,
        year,
        source: url,
      });
    }
  }

  return values;
}

function toNumber(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  if (typeof value === "string") {
    const cleaned = value.trim();
    if (!cleaned || cleaned.toUpperCase() === "NA") {
      return null;
    }
    const parsed = Number.parseFloat(cleaned);
    return Number.isFinite(parsed) ? parsed : null;
  }

  return null;
}

function median(values: number[]): number | null {
  if (values.length === 0) {
    return null;
  }
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  if (sorted.length % 2 === 1) {
    return sorted[middle];
  }

  return (sorted[middle - 1] + sorted[middle]) / 2;
}

function rounded(value: number | null, digits = 2): number | null {
  if (value === null || !Number.isFinite(value)) {
    return null;
  }
  const scale = 10 ** digits;
  return Math.round(value * scale) / scale;
}

async function fetchWhoCityValidation(): Promise<Map<string, WhoCityValidation>> {
  const response = await fetch(WHO_AIR_QUALITY_DATABASE_URL, {
    headers: {
      "User-Agent": "DevelopmentBlindspotsLab/0.1 research pipeline",
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`WHO air quality database HTTP ${response.status}: ${body.slice(0, 240)}`);
  }

  const buffer = Buffer.from(await response.arrayBuffer());
  const sheets = await readXlsxFile(buffer);
  const selectedSheet =
    sheets.find((sheet) => sheet.sheet.includes("Update 2024")) ??
    sheets[sheets.length - 1];

  if (!selectedSheet) {
    throw new Error("WHO air quality database did not include any worksheets");
  }

  const [headerRow, ...dataRows] = selectedSheet.data;
  const headers = headerRow.map((cell) => String(cell ?? "").trim());
  const rows = dataRows.map((cells) =>
    Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? null]))
  ) as Record<string, unknown>[];
  const latestByCity = new Map<
    string,
    {
      iso3: string;
      city: string;
      year: number;
      pm25: number;
    }
  >();
  const observationsByIso3 = new Map<string, number>();

  for (const row of rows) {
    const iso3 = typeof row.iso3 === "string" ? row.iso3.trim() : "";
    const city = typeof row.city === "string" ? row.city.trim() : "";
    const year = toNumber(row.year);
    const pm25 = toNumber(row.pm25_concentration);

    if (!iso3 || !city || year === null || pm25 === null) {
      continue;
    }

    observationsByIso3.set(iso3, (observationsByIso3.get(iso3) ?? 0) + 1);
    const key = `${iso3}::${city.toLowerCase()}`;
    const existing = latestByCity.get(key);
    if (!existing || year > existing.year) {
      latestByCity.set(key, {
        iso3,
        city,
        year,
        pm25,
      });
    }
  }

  const latestByIso3 = new Map<string, Array<{ city: string; year: number; pm25: number }>>();
  for (const item of latestByCity.values()) {
    const current = latestByIso3.get(item.iso3) ?? [];
    current.push({ city: item.city, year: item.year, pm25: item.pm25 });
    latestByIso3.set(item.iso3, current);
  }

  const validation = new Map<string, WhoCityValidation>();
  for (const [iso3, cities] of latestByIso3.entries()) {
    const values = cities.map((item) => item.pm25);
    const highest = [...cities].sort((a, b) => b.pm25 - a.pm25)[0];
    const citiesAbove = values.filter(
      (value) => value > WHO_PM25_ANNUAL_GUIDELINE
    ).length;

    validation.set(iso3, {
      status: "computed",
      citiesWithPm25: cities.length,
      observations: observationsByIso3.get(iso3) ?? values.length,
      latestYear: Math.max(...cities.map((item) => item.year)),
      pm25CityMean: rounded(values.reduce((sum, value) => sum + value, 0) / values.length),
      pm25CityMedian: rounded(median(values)),
      pm25CityMax: rounded(highest.pm25),
      citiesAboveWhoGuideline: citiesAbove,
      cityShareAboveWhoGuideline: rounded((citiesAbove / cities.length) * 100, 1),
      wdiMinusWhoCityMean: null,
      highestPm25City: {
        city: highest.city,
        year: highest.year,
        value: rounded(highest.pm25) ?? highest.pm25,
      },
    });
  }

  return validation;
}

async function fetchLocationsForCountry(
  iso2: string,
  apiKey: string
): Promise<OpenAQLocation[]> {
  const locations: OpenAQLocation[] = [];
  let page = 1;
  const limit = 1000;

  while (page <= 20) {
    const url = `https://api.openaq.org/v3/locations?iso=${iso2}&limit=${limit}&page=${page}`;
    const json = await fetchOpenAQ(url, apiKey);
    const results = asRecord(json).results;
    const batch = Array.isArray(results) ? (results as OpenAQLocation[]) : [];
    locations.push(...batch);

    if (batch.length < limit) {
      break;
    }
    page += 1;
  }

  return locations;
}

function parameterNames(location: OpenAQLocation): string[] {
  const fromParameters =
    location.parameters
      ?.map((parameter) => parameter.name ?? parameter.displayName)
      .filter((name): name is string => Boolean(name)) ?? [];

  const fromSensors =
    location.sensors
      ?.map((sensor) => sensor.parameter?.name ?? sensor.parameter?.displayName)
      .filter((name): name is string => Boolean(name)) ?? [];

  return Array.from(new Set([...fromParameters, ...fromSensors])).map((name) =>
    name.toLowerCase().replace(".", "")
  );
}

function daysSince(dateValue?: string): number | null {
  if (!dateValue) {
    return null;
  }
  const parsed = Date.parse(dateValue);
  if (!Number.isFinite(parsed)) {
    return null;
  }
  return Math.floor((Date.now() - parsed) / 86_400_000);
}

function aggregateLocations(
  country: (typeof ADB_REGIONAL_MEMBERS)[number],
  locations: OpenAQLocation[]
) {
  const parameterCoverage = Object.fromEntries(
    PARAMETERS.map((parameter) => [parameter, 0])
  ) as Record<string, number>;
  let freshLocations = 0;
  let staleLocations = 0;
  let unknownFreshness = 0;

  for (const location of locations) {
    const names = parameterNames(location);
    for (const parameter of PARAMETERS) {
      if (names.includes(parameter)) {
        parameterCoverage[parameter] += 1;
      }
    }

    const age = daysSince(location.datetimeLast);
    if (age === null) {
      unknownFreshness += 1;
    } else if (age <= 90) {
      freshLocations += 1;
    } else {
      staleLocations += 1;
    }
  }

  return {
    ...country,
    status: "computed" as const,
    publicLocations: locations.length,
    freshLocations,
    staleLocations,
    unknownFreshness,
    parameterCoverage,
    freshnessShare:
      locations.length > 0
        ? Math.round((freshLocations / locations.length) * 1000) / 10
        : 0,
  };
}

type CountryAggregation = ReturnType<typeof aggregateLocations>;
type CountryError = (typeof ADB_REGIONAL_MEMBERS)[number] & {
  status: "error" | "api_key_required";
  publicLocations: null;
  freshLocations: null;
  staleLocations: null;
  unknownFreshness: null;
  parameterCoverage: Record<string, number | null>;
  error?: string;
};

type EnrichedCountry = (CountryAggregation | CountryError) & {
  population: WdiValue | null;
  pm25Exposure: (WdiValue & {
    unit: "micrograms_per_cubic_meter";
    aboveWhoGuideline: boolean;
  }) | null;
  whoCityValidation: WhoCityValidation;
  metrics: {
    peoplePerPublicLocation: number | null;
    peoplePerPm25Location: number | null;
    populationInAboveGuidelinePm25Economy: number | null;
    populationWithNoPublicPm25Monitor: number | null;
    pm25ObservabilityGapScore: number | null;
    pm25ObservabilityStatus:
      | "no_population"
      | "no_pm25_exposure"
      | "no_public_pm25_monitor"
      | "sparse_public_pm25_monitoring"
      | "public_pm25_monitoring_present"
      | "below_who_guideline";
  };
};

function emptyCoverage(): Record<string, number | null> {
  return Object.fromEntries(PARAMETERS.map((item) => [item, null]));
}

function countFor(country: CountryAggregation | CountryError, parameter: string): number {
  const value = country.parameterCoverage[parameter];
  return typeof value === "number" ? value : 0;
}

function roundedRatio(numerator: number, denominator: number): number | null {
  if (denominator <= 0) {
    return null;
  }

  return Math.round(numerator / denominator);
}

function pm25GapScore(
  pm25Exposure: number,
  peoplePerPm25Location: number | null,
  pm25LocationCount: number
): number {
  const exposurePressure = Math.min(100, (pm25Exposure / 35) * 100);
  const monitorScarcity =
    pm25LocationCount === 0
      ? 100
      : Math.min(100, ((peoplePerPm25Location ?? 0) / 5_000_000) * 100);

  return Math.round(exposurePressure * 0.65 + monitorScarcity * 0.35);
}

function enrichCountry(
  country: CountryAggregation | CountryError,
  populationByIso3: Map<string, WdiValue>,
  pm25ByIso3: Map<string, WdiValue>,
  whoCityByIso3: Map<string, WhoCityValidation>
): EnrichedCountry {
  const population = populationByIso3.get(country.iso3) ?? null;
  const rawPm25 = pm25ByIso3.get(country.iso3) ?? null;
  const pm25Exposure = rawPm25
    ? {
        ...rawPm25,
        unit: "micrograms_per_cubic_meter" as const,
        aboveWhoGuideline: rawPm25.value > WHO_PM25_ANNUAL_GUIDELINE,
      }
    : null;
  const rawWhoCityValidation = whoCityByIso3.get(country.iso3) ?? {
    status: "no_city_pm25" as const,
    citiesWithPm25: 0,
    observations: 0,
    latestYear: null,
    pm25CityMean: null,
    pm25CityMedian: null,
    pm25CityMax: null,
    citiesAboveWhoGuideline: 0,
    cityShareAboveWhoGuideline: null,
    wdiMinusWhoCityMean: null,
    highestPm25City: null,
  };
  const whoCityValidation: WhoCityValidation = {
    ...rawWhoCityValidation,
    wdiMinusWhoCityMean:
      pm25Exposure && rawWhoCityValidation.pm25CityMean !== null
        ? rounded(pm25Exposure.value - rawWhoCityValidation.pm25CityMean)
        : null,
  };
  const publicLocations =
    typeof country.publicLocations === "number" ? country.publicLocations : 0;
  const pm25Locations = countFor(country, "pm25");
  const peoplePerPublicLocation =
    population && publicLocations > 0
      ? roundedRatio(population.value, publicLocations)
      : null;
  const peoplePerPm25Location =
    population && pm25Locations > 0
      ? roundedRatio(population.value, pm25Locations)
      : null;
  const populationInAboveGuidelinePm25Economy =
    population && pm25Exposure?.aboveWhoGuideline ? population.value : null;
  const populationWithNoPublicPm25Monitor =
    population && pm25Exposure?.aboveWhoGuideline && pm25Locations === 0
      ? population.value
      : null;

  let status: EnrichedCountry["metrics"]["pm25ObservabilityStatus"] =
    "public_pm25_monitoring_present";
  if (!population) {
    status = "no_population";
  } else if (!pm25Exposure) {
    status = "no_pm25_exposure";
  } else if (!pm25Exposure.aboveWhoGuideline) {
    status = "below_who_guideline";
  } else if (pm25Locations === 0) {
    status = "no_public_pm25_monitor";
  } else if ((peoplePerPm25Location ?? 0) > 5_000_000) {
    status = "sparse_public_pm25_monitoring";
  }

  return {
    ...country,
    population,
    pm25Exposure,
    whoCityValidation,
    metrics: {
      peoplePerPublicLocation,
      peoplePerPm25Location,
      populationInAboveGuidelinePm25Economy,
      populationWithNoPublicPm25Monitor,
      pm25ObservabilityGapScore:
        population && pm25Exposure
          ? pm25GapScore(pm25Exposure.value, peoplePerPm25Location, pm25Locations)
          : null,
      pm25ObservabilityStatus: status,
    },
  };
}

function summarizeCountries(countries: EnrichedCountry[]) {
  const computed = countries.filter((country) => country.status === "computed");
  const totalPublicLocations = computed.reduce(
    (sum, country) => sum + (country.publicLocations ?? 0),
    0
  );
  const economiesWithLocations = computed.filter(
    (country) => (country.publicLocations ?? 0) > 0
  ).length;
  const populationKnown = countries.filter((country) => country.population);
  const pm25Known = countries.filter((country) => country.pm25Exposure);
  const whoCityKnown = countries.filter(
    (country) => country.whoCityValidation.status === "computed"
  );
  const totalPopulationKnown = populationKnown.reduce(
    (sum, country) => sum + (country.population?.value ?? 0),
    0
  );
  const populationInZeroLocationEconomies = countries.reduce((sum, country) => {
    if ((country.publicLocations ?? 0) === 0) {
      return sum + (country.population?.value ?? 0);
    }
    return sum;
  }, 0);
  const populationInAboveGuidelinePm25Economies = countries.reduce(
    (sum, country) =>
      sum + (country.metrics.populationInAboveGuidelinePm25Economy ?? 0),
    0
  );
  const populationWithNoPublicPm25Monitor = countries.reduce(
    (sum, country) => sum + (country.metrics.populationWithNoPublicPm25Monitor ?? 0),
    0
  );
  const sparsePm25Economies = countries.filter(
    (country) =>
      country.metrics.pm25ObservabilityStatus ===
      "sparse_public_pm25_monitoring"
  ).length;

  return {
    economiesQueried: countries.length,
    economiesComputed: computed.length,
    economiesWithLocations,
    economiesWithNoLocations: computed.length - economiesWithLocations,
    economiesErrored: countries.length - computed.length,
    totalPublicLocations,
    populationKnownEconomies: populationKnown.length,
    totalPopulationKnown,
    populationInZeroLocationEconomies,
    pm25ExposureKnownEconomies: pm25Known.length,
    whoCityPm25KnownEconomies: whoCityKnown.length,
    whoCityPm25Cities: whoCityKnown.reduce(
      (sum, country) => sum + country.whoCityValidation.citiesWithPm25,
      0
    ),
    whoPm25AnnualGuideline: WHO_PM25_ANNUAL_GUIDELINE,
    populationInAboveGuidelinePm25Economies,
    populationWithNoPublicPm25Monitor,
    sparsePm25MonitoringEconomies: sparsePm25Economies,
  };
}

async function writeJsonOutputs(data: unknown): Promise<void> {
  for (const relativePath of JSON_OUTPUTS) {
    const outputPath = path.join(process.cwd(), relativePath);
    await mkdir(path.dirname(outputPath), { recursive: true });
    await writeFile(outputPath, `${JSON.stringify(data, null, 2)}\n`);
  }
}

function csvCell(value: unknown): string {
  if (value === null || value === undefined) {
    return "";
  }

  const text = String(value);
  if (/[",\n\r]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }

  return text;
}

function countryRowsToCsv(countries: EnrichedCountry[]): string {
  const headers = [
    "iso2",
    "iso3",
    "name",
    "subregion",
    "status",
    "population_year",
    "population",
    "public_locations",
    "pm25_locations",
    "pm10_locations",
    "no2_locations",
    "o3_locations",
    "people_per_public_location",
    "people_per_pm25_location",
    "pm25_exposure_year",
    "pm25_exposure_ugm3",
    "pm25_above_who_guideline_5_ugm3",
    "population_in_above_guideline_pm25_economy",
    "population_with_no_public_pm25_monitor",
    "pm25_observability_gap_score",
    "pm25_observability_status",
    "who_city_pm25_cities",
    "who_city_pm25_mean",
    "who_city_pm25_median",
    "who_city_pm25_max",
    "who_city_pm25_latest_year",
    "who_city_pm25_above_guideline_share",
    "wdi_minus_who_city_pm25_mean",
    "who_highest_pm25_city",
    "unknown_freshness",
  ];

  const rows = countries.map((country) => [
    country.iso2,
    country.iso3,
    country.name,
    country.subregion,
    country.status,
    country.population?.year,
    country.population?.value,
    country.publicLocations,
    country.parameterCoverage.pm25,
    country.parameterCoverage.pm10,
    country.parameterCoverage.no2,
    country.parameterCoverage.o3,
    country.metrics.peoplePerPublicLocation,
    country.metrics.peoplePerPm25Location,
    country.pm25Exposure?.year,
    country.pm25Exposure?.value,
    country.pm25Exposure?.aboveWhoGuideline,
    country.metrics.populationInAboveGuidelinePm25Economy,
    country.metrics.populationWithNoPublicPm25Monitor,
    country.metrics.pm25ObservabilityGapScore,
    country.metrics.pm25ObservabilityStatus,
    country.whoCityValidation.citiesWithPm25,
    country.whoCityValidation.pm25CityMean,
    country.whoCityValidation.pm25CityMedian,
    country.whoCityValidation.pm25CityMax,
    country.whoCityValidation.latestYear,
    country.whoCityValidation.cityShareAboveWhoGuideline,
    country.whoCityValidation.wdiMinusWhoCityMean,
    country.whoCityValidation.highestPm25City
      ? `${country.whoCityValidation.highestPm25City.city} (${country.whoCityValidation.highestPm25City.value})`
      : null,
    country.unknownFreshness,
  ]);

  return [
    headers.map(csvCell).join(","),
    ...rows.map((row) => row.map(csvCell).join(",")),
  ].join("\n");
}

async function writeCsvOutputs(countries: EnrichedCountry[]): Promise<void> {
  const csv = `${countryRowsToCsv(countries)}\n`;
  for (const relativePath of CSV_OUTPUTS) {
    const outputPath = path.join(process.cwd(), relativePath);
    await mkdir(path.dirname(outputPath), { recursive: true });
    await writeFile(outputPath, csv);
  }
}

async function main(): Promise<void> {
  await loadLocalEnv();
  const apiKey = getApiKey();

  if (!apiKey) {
    const output = {
      metadata: {
        title: "OpenAQ Pilot Monitor Aggregation",
        generatedAt: new Date().toISOString(),
        script: "scripts/research/fetch-openaq-pilots.ts",
        status: "api_key_required",
        source: "https://docs.openaq.org/about/about",
        economySource: "https://aric.adb.org/integrationindicators/groupings",
        exports: {
          json: JSON_OUTPUTS,
          csv: CSV_OUTPUTS,
        },
        note:
          "OpenAQ API v3 requires an API key. Set OPENAQ_API_KEY and rerun npm run research:openaq to produce monitor counts for ADB regional member economies.",
      },
      summary: {
        economiesQueried: ADB_REGIONAL_MEMBERS.length,
        economiesComputed: 0,
        economiesWithLocations: 0,
        economiesWithNoLocations: 0,
        economiesErrored: 0,
        totalPublicLocations: 0,
      },
      countries: ADB_REGIONAL_MEMBERS.map((country) => ({
        ...country,
        status: "api_key_required",
        publicLocations: null,
        freshLocations: null,
        staleLocations: null,
        unknownFreshness: null,
        parameterCoverage: emptyCoverage(),
      })),
    };

    await writeJsonOutputs(output);
    console.log("OPENAQ_API_KEY not set; wrote API-key-required output.");
    return;
  }

  console.log("Fetching World Bank indicators and WHO city PM2.5 validation...");
  const [populationByIso3, pm25ByIso3, whoCityByIso3] = await Promise.all([
    fetchWorldBankLatestIndicator(POPULATION_INDICATOR),
    fetchWorldBankLatestIndicator(PM25_EXPOSURE_INDICATOR),
    fetchWhoCityValidation(),
  ]);

  const countries: Array<CountryAggregation | CountryError> = [];
  for (const country of ADB_REGIONAL_MEMBERS) {
    console.log(`Fetching OpenAQ locations for ${country.name}...`);
    try {
      const locations = await fetchLocationsForCountry(country.iso2, apiKey);
      countries.push(aggregateLocations(country, locations));
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      console.warn(`OpenAQ fetch failed for ${country.name}: ${message}`);
      countries.push({
        ...country,
        status: "error",
        publicLocations: null,
        freshLocations: null,
        staleLocations: null,
        unknownFreshness: null,
        parameterCoverage: emptyCoverage(),
        error: message,
      });
    }
  }

  const enrichedCountries = countries.map((country) =>
    enrichCountry(country, populationByIso3, pm25ByIso3, whoCityByIso3)
  );

  const output = {
    metadata: {
      title: "OpenAQ Pilot Monitor Aggregation",
      generatedAt: new Date().toISOString(),
      script: "scripts/research/fetch-openaq-pilots.ts",
      status: "computed",
      coverageScope: "ADB regional member economies, best-effort by ISO2 country code",
      source: "https://api.openaq.org/v3",
      economySource: "https://aric.adb.org/integrationindicators/groupings",
      populationSource: `${WORLD_BANK_API}/country/all/indicator/${POPULATION_INDICATOR}`,
      pm25ExposureSource: `${WORLD_BANK_API}/country/all/indicator/${PM25_EXPOSURE_INDICATOR}`,
      pm25ExposureIndicator: PM25_EXPOSURE_INDICATOR,
      whoCityDatabaseSource: WHO_AIR_QUALITY_DATABASE_URL,
      whoCityDatabasePage:
        "https://www.who.int/publications/m/item/who-ambient-air-quality-database-%28update-jan-2024%29",
      whoPm25AnnualGuideline: WHO_PM25_ANNUAL_GUIDELINE,
      exports: {
        json: JSON_OUTPUTS,
        csv: CSV_OUTPUTS,
      },
      no2ExposureStatus:
        "not_computed_locally; Sentinel-5P/TROPOMI NO2 requires an Earth Engine or Copernicus export step",
      screeningScoreNote:
        "PM2.5 observability gap score is a transparent first-pass national screening score: 65% WDI PM2.5 exposure pressure and 35% public PM2.5 monitor scarcity.",
      caveat:
        "OpenAQ only includes public providers it has discovered or received; absence from OpenAQ is not proof that a monitor does not exist. WDI PM2.5 exposure is national modeled exposure, not local monitor readings.",
    },
    summary: summarizeCountries(enrichedCountries),
    countries: enrichedCountries,
  };

  await writeJsonOutputs(output);
  await writeCsvOutputs(enrichedCountries);

  console.log("Wrote OpenAQ pilot outputs and CSV exports.");
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
