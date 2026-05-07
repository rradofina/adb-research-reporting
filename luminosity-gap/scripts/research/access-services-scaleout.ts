import { createHash } from "crypto";
import { mkdir, readFile, writeFile } from "fs/promises";
import path from "path";

type AdbEconomy = {
  iso2: string;
  iso3: string;
  name: string;
  subregion: string;
};

type WdiValue = {
  value: number;
  year: number;
  sourceUrl: string;
};

type BoundaryAvailability = {
  status: "available" | "missing" | "error";
  boundaryID: string | null;
  boundaryYearRepresented: string | null;
  admUnitCount: number | null;
  boundarySource: string | null;
  boundaryLicense: string | null;
  sourceUrl: string;
  error: string | null;
};

type ScaleoutEconomy = AdbEconomy & {
  population: WdiValue | null;
  ruralPopulationShare: WdiValue | null;
  landAreaSqKm: WdiValue | null;
  boundaries: {
    adm0: BoundaryAvailability;
    adm1: BoundaryAvailability;
  };
  metrics: {
    sourceReadinessScore: number;
    impactPriorityScore: number;
    scalePriorityScore: number;
    nextPipelineMode:
      | "admin1_screening_candidate"
      | "national_screening_candidate"
      | "source_review_required";
    blockerNotes: string[];
  };
};

const ADB_REGIONAL_MEMBERS: AdbEconomy[] = [
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

const WORLD_BANK_API = "https://api.worldbank.org/v2";
const INDICATORS = {
  population: "SP.POP.TOTL",
  ruralShare: "SP.RUR.TOTL.ZS",
  landArea: "AG.LND.TOTL.K2",
};
const GEOboundaries_RELEASE = "gbOpen";
const CACHE_ROOT = ".cache/research/access-scaleout";
const JSON_OUTPUTS = [
  "src/data/generated/access-services-adb-scaleout.json",
  "public/data/access-services-adb-scaleout.json",
];
const CSV_OUTPUTS = [
  "public/data/access-services-adb-scaleout.csv",
  "research/access-services/generated/access-services-adb-scaleout.csv",
];

function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null
    ? (value as Record<string, unknown>)
    : {};
}

function round(value: number, digits = 2): number {
  const scale = 10 ** digits;
  return Math.round(value * scale) / scale;
}

async function fetchJson(url: string): Promise<unknown> {
  const cacheKey = createHash("sha1").update(url).digest("hex");
  const cachePath = path.join(process.cwd(), CACHE_ROOT, `${cacheKey}.json`);

  if (process.env.ACCESS_SCALE_REFRESH !== "1") {
    try {
      return JSON.parse(await readFile(cachePath, "utf8"));
    } catch {
      // Cache misses should use the source endpoint.
    }
  }

  const response = await fetch(url, {
    headers: {
      "User-Agent": "DevelopmentBlindspotsLab/0.1 research pipeline",
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`HTTP ${response.status}: ${body.slice(0, 200)}`);
  }

  const json = await response.json();
  await mkdir(path.dirname(cachePath), { recursive: true });
  await writeFile(cachePath, `${JSON.stringify(json)}\n`);
  return json;
}

async function fetchWorldBankLatestIndicator(
  indicator: string
): Promise<Map<string, WdiValue>> {
  const url = `${WORLD_BANK_API}/country/all/indicator/${indicator}?format=json&per_page=20000&mrv=1`;
  const json = await fetchJson(url);
  const rows = Array.isArray(json) && Array.isArray(json[1]) ? json[1] : [];
  const values = new Map<string, WdiValue>();

  for (const row of rows) {
    const record = asRecord(row);
    const iso3 = typeof record.countryiso3code === "string" ? record.countryiso3code : "";
    const value = typeof record.value === "number" ? record.value : null;
    const year = typeof record.date === "string" ? Number.parseInt(record.date, 10) : NaN;

    if (iso3 && value !== null && Number.isFinite(year)) {
      values.set(iso3, { value, year, sourceUrl: url });
    }
  }

  return values;
}

function boundaryUrl(iso3: string, adminLevel: "ADM0" | "ADM1"): string {
  return `https://www.geoboundaries.org/api/current/${GEOboundaries_RELEASE}/${iso3}/${adminLevel}/`;
}

async function fetchBoundaryAvailability(
  economy: AdbEconomy,
  adminLevel: "ADM0" | "ADM1"
): Promise<BoundaryAvailability> {
  const sourceUrl = boundaryUrl(economy.iso3, adminLevel);

  try {
    const metadata = asRecord(await fetchJson(sourceUrl));
    const boundaryID = typeof metadata.boundaryID === "string" ? metadata.boundaryID : null;
    const admUnitCount = Number(metadata.admUnitCount);

    return {
      status: boundaryID ? "available" : "missing",
      boundaryID,
      boundaryYearRepresented:
        typeof metadata.boundaryYearRepresented === "string"
          ? metadata.boundaryYearRepresented
          : null,
      admUnitCount: Number.isFinite(admUnitCount) ? admUnitCount : null,
      boundarySource:
        typeof metadata.boundarySource === "string" ? metadata.boundarySource : null,
      boundaryLicense:
        typeof metadata.boundaryLicense === "string" ? metadata.boundaryLicense : null,
      sourceUrl,
      error: null,
    };
  } catch (error) {
    return {
      status: "error",
      boundaryID: null,
      boundaryYearRepresented: null,
      admUnitCount: null,
      boundarySource: null,
      boundaryLicense: null,
      sourceUrl,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

function impactPriorityScore(
  population: WdiValue | null,
  ruralShare: WdiValue | null
): number {
  const populationComponent = population
    ? Math.min(100, (Math.log10(population.value) / 9.3) * 100)
    : 0;
  const ruralComponent = ruralShare ? Math.min(100, ruralShare.value) : 35;

  return Math.round(populationComponent * 0.65 + ruralComponent * 0.35);
}

function sourceReadinessScore({
  population,
  ruralPopulationShare,
  landAreaSqKm,
  boundaries,
}: Pick<
  ScaleoutEconomy,
  "population" | "ruralPopulationShare" | "landAreaSqKm" | "boundaries"
>): number {
  return Math.round(
    (boundaries.adm1.status === "available" ? 40 : 0) +
      (boundaries.adm0.status === "available" ? 15 : 0) +
      (population ? 20 : 0) +
      (ruralPopulationShare ? 15 : 0) +
      (landAreaSqKm ? 10 : 0)
  );
}

function buildMetrics(
  economy: AdbEconomy,
  population: WdiValue | null,
  ruralPopulationShare: WdiValue | null,
  landAreaSqKm: WdiValue | null,
  boundaries: ScaleoutEconomy["boundaries"]
): ScaleoutEconomy["metrics"] {
  const blockers: string[] = [];
  if (!population) blockers.push("No latest World Bank population value");
  if (!ruralPopulationShare) blockers.push("No latest World Bank rural-share value");
  if (!landAreaSqKm) blockers.push("No latest World Bank land-area value");
  if (boundaries.adm1.status !== "available") blockers.push("No geoBoundaries ADM1 metadata");
  if (economy.iso3 === "TWN") {
    blockers.push("World Bank WDI coverage may not include Taipei,China");
  }

  const sourceScore = sourceReadinessScore({
    population,
    ruralPopulationShare,
    landAreaSqKm,
    boundaries,
  });
  const impactScore = impactPriorityScore(population, ruralPopulationShare);
  const mode =
    boundaries.adm1.status === "available" && population
      ? "admin1_screening_candidate"
      : population
        ? "national_screening_candidate"
        : "source_review_required";

  return {
    sourceReadinessScore: sourceScore,
    impactPriorityScore: impactScore,
    scalePriorityScore: Math.round(sourceScore * 0.45 + impactScore * 0.55),
    nextPipelineMode: mode,
    blockerNotes: blockers,
  };
}

function summarize(economies: ScaleoutEconomy[]) {
  const topCandidates = [...economies]
    .sort((a, b) => b.metrics.scalePriorityScore - a.metrics.scalePriorityScore)
    .slice(0, 10)
    .map((economy) => ({
      iso3: economy.iso3,
      name: economy.name,
      subregion: economy.subregion,
      population: economy.population?.value ?? null,
      adm1Units: economy.boundaries.adm1.admUnitCount,
      sourceReadinessScore: economy.metrics.sourceReadinessScore,
      impactPriorityScore: economy.metrics.impactPriorityScore,
      scalePriorityScore: economy.metrics.scalePriorityScore,
      nextPipelineMode: economy.metrics.nextPipelineMode,
    }));

  return {
    economiesAssessed: economies.length,
    adm1BoundaryAvailable: economies.filter(
      (economy) => economy.boundaries.adm1.status === "available"
    ).length,
    adm0BoundaryAvailable: economies.filter(
      (economy) => economy.boundaries.adm0.status === "available"
    ).length,
    populationKnown: economies.filter((economy) => economy.population).length,
    ruralShareKnown: economies.filter((economy) => economy.ruralPopulationShare).length,
    landAreaKnown: economies.filter((economy) => economy.landAreaSqKm).length,
    admin1ScreeningCandidates: economies.filter(
      (economy) =>
        economy.metrics.nextPipelineMode === "admin1_screening_candidate"
    ).length,
    sourceReviewRequired: economies.filter(
      (economy) => economy.metrics.nextPipelineMode === "source_review_required"
    ).length,
    topCandidates,
  };
}

function csvEscape(value: unknown): string {
  const text = String(value ?? "");
  if (/[",\r\n]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}

function scaleoutCsv(economies: ScaleoutEconomy[]): string {
  const columns = [
    "iso2",
    "iso3",
    "name",
    "subregion",
    "population_year",
    "population",
    "rural_share_year",
    "rural_share",
    "land_area_year",
    "land_area_sq_km",
    "adm0_status",
    "adm1_status",
    "adm1_units",
    "source_readiness_score",
    "impact_priority_score",
    "scale_priority_score",
    "next_pipeline_mode",
    "blocker_notes",
  ];
  const rows = economies.map((economy) => [
    economy.iso2,
    economy.iso3,
    economy.name,
    economy.subregion,
    economy.population?.year,
    economy.population?.value,
    economy.ruralPopulationShare?.year,
    economy.ruralPopulationShare ? round(economy.ruralPopulationShare.value, 2) : null,
    economy.landAreaSqKm?.year,
    economy.landAreaSqKm?.value,
    economy.boundaries.adm0.status,
    economy.boundaries.adm1.status,
    economy.boundaries.adm1.admUnitCount,
    economy.metrics.sourceReadinessScore,
    economy.metrics.impactPriorityScore,
    economy.metrics.scalePriorityScore,
    economy.metrics.nextPipelineMode,
    economy.metrics.blockerNotes.join("; "),
  ]);

  return [
    columns.join(","),
    ...rows.map((row) => row.map(csvEscape).join(",")),
  ].join("\n");
}

async function writeJson(relativePath: string, data: unknown): Promise<void> {
  const outputPath = path.join(process.cwd(), relativePath);
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(data, null, 2)}\n`);
}

async function writeText(relativePath: string, data: string): Promise<void> {
  const outputPath = path.join(process.cwd(), relativePath);
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, data);
}

async function main(): Promise<void> {
  console.log("=== ACCESS-SERVICES ADB SCALE-OUT READINESS ===");
  console.log("Fetching World Bank indicators...");
  const [populationByIso3, ruralShareByIso3, landAreaByIso3] = await Promise.all([
    fetchWorldBankLatestIndicator(INDICATORS.population),
    fetchWorldBankLatestIndicator(INDICATORS.ruralShare),
    fetchWorldBankLatestIndicator(INDICATORS.landArea),
  ]);

  const economies: ScaleoutEconomy[] = [];
  for (const economy of ADB_REGIONAL_MEMBERS) {
    console.log(`Checking boundaries for ${economy.name}...`);
    const [adm0, adm1] = await Promise.all([
      fetchBoundaryAvailability(economy, "ADM0"),
      fetchBoundaryAvailability(economy, "ADM1"),
    ]);
    const population = populationByIso3.get(economy.iso3) ?? null;
    const ruralPopulationShare = ruralShareByIso3.get(economy.iso3) ?? null;
    const landAreaSqKm = landAreaByIso3.get(economy.iso3) ?? null;
    const boundaries = { adm0, adm1 };

    economies.push({
      ...economy,
      population,
      ruralPopulationShare,
      landAreaSqKm,
      boundaries,
      metrics: buildMetrics(
        economy,
        population,
        ruralPopulationShare,
        landAreaSqKm,
        boundaries
      ),
    });
  }

  const output = {
    metadata: {
      title: "Climate-Adjusted Access to Services - ADB Regional Scale-Out Readiness",
      generatedAt: new Date().toISOString(),
      script: "scripts/research/access-services-scaleout.ts",
      status: "computed_scaleout_readiness",
      coverageScope: "ADB regional member economies listed by ADB ARIC",
      caveat:
        "This artifact measures readiness and priority for scale-out. It does not compute service counts, travel time, or access stress for all economies.",
      method:
        "Checks WDI population/rural/land-area availability and geoBoundaries ADM0/ADM1 metadata for ADB regional member economies; scores source readiness and impact priority to rank where the access-services pipeline can expand next.",
      sources: [
        "https://aric.adb.org/integrationindicators/groupings",
        `${WORLD_BANK_API}/country/all/indicator/${INDICATORS.population}`,
        `${WORLD_BANK_API}/country/all/indicator/${INDICATORS.ruralShare}`,
        `${WORLD_BANK_API}/country/all/indicator/${INDICATORS.landArea}`,
        "https://www.geoboundaries.org/api.html",
      ],
      cacheNote:
        "Responses are cached under .cache/research/access-scaleout unless ACCESS_SCALE_REFRESH=1 is set.",
      exports: {
        json: JSON_OUTPUTS,
        csv: CSV_OUTPUTS,
      },
    },
    summary: summarize(economies),
    economies: economies.sort(
      (a, b) => b.metrics.scalePriorityScore - a.metrics.scalePriorityScore
    ),
  };
  const csv = `${scaleoutCsv(output.economies)}\n`;

  for (const outputPath of JSON_OUTPUTS) {
    await writeJson(outputPath, output);
  }
  for (const outputPath of CSV_OUTPUTS) {
    await writeText(outputPath, csv);
  }

  console.log("Wrote ADB access scale-out readiness outputs.");
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
