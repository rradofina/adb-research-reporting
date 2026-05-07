/**
 * Pipeline scaffold — Public Service Data Quality (Program 13)
 *
 * Status (2026-04-25): PHL pilot is RUNNABLE end-to-end via
 *   bash scripts/fetch-nhfr.sh && python scripts/process-disagreement.py
 * which produces generated/public-service-data-quality-PHL.{json,csv}.
 * See results.md for the screening result. The other 3 pilot DMCs
 * (BGD, IND, IDN) remain TODO(owner-approval) below.
 *
 * Original status: AI-drafted scaffold. PHL fetcher implementation is now
 * complete (in scripts/fetch-nhfr.sh + scripts/process-disagreement.py).
 * Other DMCs await owner approval per DMC license/ToS check.
 *
 * Constitution status (CONSTITUTION.md):
 *   - Hypothesis stage. Owner sign-off pending in scoring.md and literature.md.
 *   - To advance past Prepared pipeline (§7.2 gate), this file must:
 *       (a) move to luminosity-gap/scripts/research/public-service-data-quality-pipeline.ts;
 *       (b) be wired into luminosity-gap/package.json as `npm run research:psdq`;
 *       (c) produce a generated/ artifact;
 *       (d) commit cache responses per §11 of the Constitution and
 *           data-access-audit.md §7.
 *
 * The first testable claim (literature.md §4, draft, awaiting owner approval):
 *   In ≥3 ADB DMCs (PHL, BGD, IND, IDN), OSM-mapped health-facility counts
 *   materially disagree with the official national health-facility registry
 *   at ADM1, and the disagreement is systematically larger in rural and
 *   low-HDI ADM1 units than in capital or high-HDI ADM1 units.
 *
 * Falsification: claim retracted if both (a) OSM-vs-official per-capita
 * facility counts agree within ±10% at ADM1 in two or more pilot DMCs and
 * (b) the rural-urban gap in disagreement is not statistically distinguishable
 * from zero.
 *
 * Output schema (planned):
 *   - public-service-data-quality-disagreement.json
 *     [{ iso3, admin1Code, admin1Name, category, osmCount, officialCount,
 *        delta, ratio, population, osmPer100k, officialPer100k,
 *        ruralShare, hdi, retrievedOsm, retrievedOfficial, sources }]
 *   - public-service-data-quality-disagreement.csv  (same shape)
 *   - public-service-data-quality-summary.json     (per-DMC aggregates)
 *
 * Methodology references:
 *   - South et al. 2021 (Wellcome Open Research) — afrihealthsites pattern
 *   - Maina et al. 2019 (Scientific Data) — facility-list assembly
 *   - Sandefur and Glassman 2015 — admin-vs-survey political-economy frame
 *   - Markhof, Wollburg, Zezza 2025 — paired admin-vs-alternate-source
 *     comparison method
 *
 * Data-access-audit references:
 *   - §3.1 WorldPop (use rasters, not stats API; per audit §11 reproducibility)
 *   - §3.2 geoBoundaries gbOpen for ADM1 boundaries
 *   - §3.10 OSM via Overpass — committed cache from access-services pipeline
 *     (.cache/research/access-services/) reused; live live re-fetch only on
 *     opt-in flag
 *   - §11.2 health-ministry facility registries:
 *       PHL DOH NHFR — `nhfr.doh.gov.ph/VActivefacilitiesList` (A-grade, HTML)
 *       BGD DGHS Facility Registry — `hrm.dghs.gov.bd/public/facility-registry` (A-grade, HTML)
 *       IDN SATUSEHAT — `satusehat.kemkes.go.id/data` (B-grade, dashboard)
 *       IND HMIS — `data.gov.in` HMIS dataset slug (A-grade, CSV)
 */

import { createHash } from "crypto";
import { mkdir, readFile, writeFile } from "fs/promises";
import path from "path";

// =====================================================================
// Pilot DMC configuration
// =====================================================================

type AccessModel = "A" | "B" | "C" | "D" | "E";

interface OfficialRegistry {
  /** Human-readable registry name. */
  name: string;
  /** Public URL. Pin in versions.json when first hit. */
  url: string;
  /** Per data-access-audit.md §1 taxonomy. */
  accessModel: AccessModel;
  /** Owner-visible notes about access path and constraints. */
  notes: string;
}

interface PilotDMC {
  iso2: string;
  iso3: string;
  name: string;
  /** Pre-cached from access-services-pipeline runs at versions noted in versions.json. */
  osmCacheKey: string;
  health: OfficialRegistry;
  /** Add other categories (school, market) when health is validated end-to-end. */
}

const PILOTS: PilotDMC[] = [
  {
    iso2: "PH",
    iso3: "PHL",
    name: "Philippines",
    osmCacheKey: "access-services/PHL",
    health: {
      name: "DOH National Health Facility Registry v2.0 (NHFR)",
      url: "https://nhfr.doh.gov.ph/VActivefacilitiesList",
      accessModel: "A",
      notes:
        "HTML-rendered facility list, validated annually each March. " +
        "Scrape with respect for robots.txt and ToS. Cache HTML responses; " +
        "parse facility-by-region tables. NHFR documentation lists fields.",
    },
  },
  {
    iso2: "BD",
    iso3: "BGD",
    name: "Bangladesh",
    osmCacheKey: "access-services/BGD",
    health: {
      name: "DGHS Facility Registry (Central HRIS)",
      url: "https://hrm.dghs.gov.bd/public/facility-registry",
      accessModel: "A",
      notes:
        "Public facility registry under MoHFW. DHIS2 dashboard at " +
        "dashboard.dghs.gov.bd. Coverage ~75% of public facilities, plus " +
        "14,000+ community clinics. Cache HTML/JSON depending on endpoint.",
    },
  },
  {
    iso2: "IN",
    iso3: "IND",
    name: "India",
    osmCacheKey: "access-services/IND", // not yet cached; access-services pilot does not include IND today
    health: {
      name: "MoHFW Health Management Information System (HMIS)",
      url: "https://hmis.mohfw.gov.in/",
      accessModel: "A",
      notes:
        "Government-to-government web app; public facility-count datasets " +
        "available via data.gov.in (search keyword 'HMIS'). Cache the " +
        "specific dataset slug when first identified. Covers 200,000+ " +
        "facilities, 600+ indicators.",
    },
  },
  {
    iso2: "ID",
    iso3: "IDN",
    name: "Indonesia",
    osmCacheKey: "access-services/IDN", // not yet cached; not in access-services pilot
    health: {
      name: "Kemenkes SATUSEHAT (Indonesian Health Data Ecosystem)",
      url: "https://satusehat.kemkes.go.id/data",
      accessModel: "B",
      notes:
        "EMR + facility-integration platform. Some dashboards open; bulk " +
        "facility-list access may need light registration. Verify access " +
        "before relying on it for headline claims.",
    },
  },
];

// =====================================================================
// Type definitions for the disagreement metric
// =====================================================================

type FacilityCategory = "health" | "school" | "market";
type FacilitySource = "osm" | "official";

interface FacilityCount {
  source: FacilitySource;
  iso3: string;
  admin1Code: string;
  admin1Name: string;
  category: FacilityCategory;
  count: number;
  /** ISO-8601 string. Per Constitution §11 every row records retrieval timestamp. */
  retrievedAt: string;
  sourceUrl: string;
  sourceLabel: string;
}

interface DisagreementRow {
  iso3: string;
  admin1Code: string;
  admin1Name: string;
  category: FacilityCategory;
  osmCount: number;
  officialCount: number;
  delta: number; // osm - official (positive: OSM has more)
  ratio: number; // osm / official, NaN-safe
  population: number;
  osmPer100k: number;
  officialPer100k: number;
  ruralShare: number | null;
  hdi: number | null;
  retrievedOsm: string;
  retrievedOfficial: string;
  sourceOsm: string;
  sourceOfficial: string;
}

// =====================================================================
// Cache helper (mirror of access-services-pipeline pattern)
// =====================================================================

const CACHE_ROOT = ".cache/research/public-service-data-quality";

async function cachedFetch(url: string, init?: RequestInit): Promise<string> {
  const key = createHash("sha1")
    .update(JSON.stringify({ url, method: init?.method ?? "GET", body: init?.body ?? "" }))
    .digest("hex");
  const cachePath = path.join(process.cwd(), CACHE_ROOT, `${key}.bin`);

  if (process.env.PSDQ_REFRESH !== "1") {
    try {
      return await readFile(cachePath, "utf8");
    } catch {
      // miss
    }
  }

  const response = await fetch(url, {
    ...init,
    headers: {
      "User-Agent": "DevelopmentBlindspotsLab/0.1 public-service-data-quality pipeline",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${url}`);
  }

  const body = await response.text();
  await mkdir(path.dirname(cachePath), { recursive: true });
  await writeFile(cachePath, body);
  return body;
}

// =====================================================================
// OSM facility counts — reuse access-services cache where available
// =====================================================================

async function fetchOSMHealthCounts(_dmc: PilotDMC): Promise<FacilityCount[]> {
  // TODO(owner-approval): wire to access-services-pipeline cache. PHL and BGD
  // are already cached at .cache/research/access-services/. IND and IDN
  // require a fresh cache run. Keep methodology aligned with access-services
  // (same Overpass query templates) so disagreement is apples-to-apples.
  //
  // The access-services pipeline tags each ADM1 row with health/school/market
  // counts; this function reads those rows and projects to FacilityCount[].
  //
  // Implementation order:
  //   1. Read luminosity-gap/src/data/generated/access-services-computed-admin1.json
  //   2. Filter to dmc.iso3
  //   3. Project each row to a FacilityCount with category "health"
  //   4. Set retrievedAt to the row's osm_timestamp field
  return [];
}

// =====================================================================
// Per-DMC official-registry fetchers — to be implemented after owner approves
// scrape pattern and license per data-access-audit.md §6
// =====================================================================

async function fetchOfficialHealthRegistryPHL(): Promise<FacilityCount[]> {
  // IMPLEMENTED 2026-04-25 in shell + Python:
  //   scripts/fetch-nhfr.sh                  — pages through /api/list/v_activefacilities
  //                                            using the JWT issued in the landing page;
  //                                            caches 23 pages of 2000 records each.
  //   scripts/process-disagreement.py        — maps regcode → ADM1, splits NIR by
  //                                            provcode, aggregates by factype.
  // Output: generated/public-service-data-quality-PHL.{json,csv}
  //
  // The DOH NHFR is at https://nhfr.doh.gov.ph/VActivefacilitiesList with API at
  // /api/list/v_activefacilities. Access model A per data-access-audit.md §11.2;
  // license unstated but framed under public-information-disclosure (RA 9485).
  //
  // NHFR field schema (per record):
  //   hfhudcode, hfhudcode_short, hfhudname, factype, ownercode, fhudaddress,
  //   hfhbldgname, regcode, provcode, ctymuncode, bgycode, fhudtelno1,
  //   license, license_validitydate
  //
  // Facility-type taxonomy (44 factypes):
  //   "principal" set: 01,03,04,05,15,17,19,21,22,23,24,51,52,53
  //   "clinical" set: principal + 14,20,27,28,09 (adds BHS, dialysis, etc.)
  //
  // Regcode-to-ADM1 mapping (17 ADM1 + 1 abolished NIR split by provcode):
  //   01-12 -> PH-01 to PH-12 (regions I-XII)
  //   13 -> PH-00 NCR
  //   14 -> PH-15 CAR
  //   16 -> PH-13 Caraga
  //   17 -> PH-41 MIMAROPA
  //   18 -> Negros Island Region (abolished 2017): 18045/18302 -> PH-06,
  //         18046/18061 -> PH-07
  //   19 -> PH-14 BARMM (NHFR uses 19; PSA uses 15)
  //
  // To wire this fetcher into the TypeScript pipeline (when the program advances
  // past Prepared pipeline), port the bash + Python logic to TypeScript using
  // the cachedFetch helper above. Until then, this function returns an empty
  // array; the running pipeline is the bash + Python pair.
  return [];
}

async function fetchOfficialHealthRegistryBGD(): Promise<FacilityCount[]> {
  // TODO(owner-approval): The DGHS Facility Registry at
  // https://hrm.dghs.gov.bd/public/facility-registry exposes a search-and-
  // browse interface; the underlying URL pattern needs inspection to identify
  // a JSON or HTML endpoint we can paginate.
  //
  // Alternative: the DGHS DHIS2 instance at dashboard.dghs.gov.bd may expose
  // facility metadata via a DHIS2 API endpoint (`/api/organisationUnits`).
  // DHIS2 access typically requires a registered account; check whether public
  // read access is enabled before assuming an API path.
  //
  // Map BGD ADM1 to the 8 BGD divisions (BD-A through BD-H) per
  // luminosity-gap access-services-computed-admin1.json schema.
  return [];
}

async function fetchOfficialHealthRegistryIND(): Promise<FacilityCount[]> {
  // TODO(owner-approval): Identify the right HMIS dataset slug on data.gov.in.
  // The "HMIS" keyword search returns multiple dataset versions; pick the one
  // with state-and-district-level facility counts (not service-delivery
  // indicators). Pin slug + retrieval date in versions.json.
  //
  // CSV download path; parse, filter to facility-count rows, aggregate to ADM1
  // = state. India ADM1 = 28 states + 8 UTs.
  return [];
}

async function fetchOfficialHealthRegistryIDN(): Promise<FacilityCount[]> {
  // TODO(owner-approval): SATUSEHAT data dashboard exposes facility metrics.
  // Verify whether (a) bulk facility-list endpoint is public, or (b) only
  // EMR-style aggregates are available. If only (b), this DMC may not be in
  // first-pass scope.
  //
  // Fallback: BPS publishes a Susenas-derived facility count by province, but
  // that is survey-derived, not administrative-registry.
  //
  // Map IDN ADM1 to 38 provinces.
  return [];
}

// =====================================================================
// Disagreement computation
// =====================================================================

function computeDisagreement(
  osmRows: FacilityCount[],
  officialRows: FacilityCount[],
  population: Map<string, { population: number; ruralShare: number | null; hdi: number | null }>
): DisagreementRow[] {
  const out: DisagreementRow[] = [];
  const officialIndex = new Map<string, FacilityCount>();
  for (const row of officialRows) {
    officialIndex.set(`${row.iso3}|${row.admin1Code}|${row.category}`, row);
  }
  for (const osmRow of osmRows) {
    const key = `${osmRow.iso3}|${osmRow.admin1Code}|${osmRow.category}`;
    const officialRow = officialIndex.get(key);
    if (!officialRow) continue;
    const popInfo = population.get(`${osmRow.iso3}|${osmRow.admin1Code}`) ?? {
      population: 0,
      ruralShare: null,
      hdi: null,
    };
    const delta = osmRow.count - officialRow.count;
    const ratio = officialRow.count > 0 ? osmRow.count / officialRow.count : NaN;
    const osmPer100k = popInfo.population > 0 ? (osmRow.count * 100000) / popInfo.population : NaN;
    const officialPer100k =
      popInfo.population > 0 ? (officialRow.count * 100000) / popInfo.population : NaN;

    out.push({
      iso3: osmRow.iso3,
      admin1Code: osmRow.admin1Code,
      admin1Name: osmRow.admin1Name,
      category: osmRow.category,
      osmCount: osmRow.count,
      officialCount: officialRow.count,
      delta,
      ratio,
      population: popInfo.population,
      osmPer100k,
      officialPer100k,
      ruralShare: popInfo.ruralShare,
      hdi: popInfo.hdi,
      retrievedOsm: osmRow.retrievedAt,
      retrievedOfficial: officialRow.retrievedAt,
      sourceOsm: osmRow.sourceUrl,
      sourceOfficial: officialRow.sourceUrl,
    });
  }
  return out;
}

// =====================================================================
// Population denominator — use existing access-services-computed-admin1 data
// (which already has WorldPop ADM1 totals + rural share where available) and
// SHDI from Global Data Lab where HDI is needed.
// =====================================================================

async function loadPopulationAndHDI(
  _dmc: PilotDMC
): Promise<Map<string, { population: number; ruralShare: number | null; hdi: number | null }>> {
  // TODO(owner-approval): wire to luminosity-gap/src/data/generated/
  // access-services-computed-admin1.json for population and ruralShare,
  // and to Global Data Lab SHDI for HDI per ADM1.
  return new Map();
}

// =====================================================================
// Main entrypoint
// =====================================================================

async function main(): Promise<void> {
  // TODO(owner-approval): pilot DMC list is currently AI-suggested
  // (PHL, BGD, IND, IDN). Owner finalizes per scoring.md and CONSTITUTION.md
  // §6.1 before any data is pulled.
  //
  // To run end-to-end after owner approval and per-DMC fetcher implementation:
  //   1. tsx public-service-data-quality/pipeline.ts
  //   2. PSDQ_REFRESH=1 tsx public-service-data-quality/pipeline.ts (live refresh)
  //
  // Or after promotion to Prepared pipeline, wire as:
  //   "research:psdq": "tsx scripts/research/public-service-data-quality-pipeline.ts"
  //   in luminosity-gap/package.json.

  const allDisagreement: DisagreementRow[] = [];

  for (const dmc of PILOTS) {
    if (dmc.iso3 === "PHL") {
      const osm = await fetchOSMHealthCounts(dmc);
      const official = await fetchOfficialHealthRegistryPHL();
      const pop = await loadPopulationAndHDI(dmc);
      allDisagreement.push(...computeDisagreement(osm, official, pop));
    }
    // TODO(owner-approval): enable BGD, IND, IDN once per-DMC fetchers and
    // pilot list are confirmed.
  }

  // TODO(owner-approval): write outputs to
  //   src/data/generated/public-service-data-quality-disagreement.{json,csv}
  // and to public/data/ if/when the program reaches Prepared pipeline and
  // is hosted on the Next.js app.
  //
  // Output naming convention follows other programs (access-services-*,
  // air-monitoring-*, digital-performance-*).
  //
  // The summary JSON should record:
  //   - pilot DMCs computed
  //   - ADM1 rows
  //   - mean and median |delta| per DMC
  //   - rural-vs-urban subset comparison
  //   - HDI-stratified subset comparison
  //   - top-10 highest-disagreement ADM1 rows
  //   - sources, retrieval timestamps, and license notes per DMC
  //
  // None of these claims may carry the "publication-ready" label without
  // passing CONSTITUTION.md §7.2 gates including red-team review.

  console.log(`[psdq pipeline scaffold] processed ${allDisagreement.length} rows.`);
  console.log("This is a scaffold; per-DMC fetchers are TODO(owner-approval).");
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

export {
  PILOTS,
  type DisagreementRow,
  type FacilityCount,
  computeDisagreement,
  fetchOSMHealthCounts,
};
