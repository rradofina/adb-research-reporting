export type ReproducibilityProfile = {
  slug: string;
  title: string;
  status: string;
  claimScope: string;
  command: string;
  inputs: string[];
  outputs: string[];
  rerunSteps: string[];
  auditTrail: string[];
  aiDisclosure: string[];
  humanChecks: string[];
  limitations: string[];
};

export const reproducibilityPrinciples = [
  "Every published number must point to a source, a retrieval date or source timestamp, a script, and an output artifact.",
  "Missing data is reported as a finding. It is not silently imputed away for a cleaner map.",
  "Large raw files stay out of git, but their download URLs, filters, schemas, and aggregation commands are committed.",
  "Pilot results are labeled by claim scope: national screening, subnational estimate, facility catchment, or final indicator.",
  "AI can draft and organize, but computed values must come from scripts or source files that can be rerun.",
];

export const aiTransparencyRules = [
  "Disclose where AI assisted literature search, source triage, code drafting, UI copy, and documentation.",
  "Do not cite AI as a source of empirical facts. Cite the underlying dataset, paper, institution, or API instead.",
  "Keep AI-generated hypotheses separate from measured findings until the pipeline produces evidence.",
  "Record blocked steps plainly, such as missing API keys, not-yet-downloaded rasters, or unvalidated schema assumptions.",
  "Use human review gates for source relevance, code execution, output plausibility, and final claims.",
];

export const transparencyReferences = [
  {
    name: "ADB Responsible AI technical controls challenge",
    url: "https://challenges.adb.org/en/challenges/extensible-responsible-ai-technical-controls-evaluator?lang=en",
    use: "Auditable responsible-AI controls and standardized scorecards are aligned with the trust layer used here.",
  },
  {
    name: "ASEAN Guide on AI Governance and Ethics summary",
    url: "https://seads.adb.org/articles/asean-ai-guidelines-seek-encourage-responsible-use-and-deployment",
    use: "Supports disclosure of AI use, data used, and purpose in Southeast Asian policy context.",
  },
  {
    name: "OECD AI transparency and explainability principle",
    url: "https://oecd.ai/en/dashboards/ai-principles/P7",
    use: "Frames clear explanation of data, logic, and factors behind AI-supported outputs.",
  },
  {
    name: "NIST AI Risk Management Framework",
    url: "https://www.nist.gov/itl/ai-risk-management-framework",
    use: "Provides the govern, map, measure, and manage risk structure behind the AI disclosure checklist.",
  },
  {
    name: "The Turing Way reproducible research guide",
    url: "https://book.the-turing-way.org/",
    use: "Grounds the reproducibility checklist in open, documented, collaborative data-science practice.",
  },
];

export const reproducibilityProfiles: ReproducibilityProfile[] = [
  {
    slug: "access-services",
    title: "Climate-Adjusted Access to Services",
    status: "Computed national, multi-batch ADM1, and regional readiness artifacts exist",
    claimScope:
      "National and admin-1 screening for 104 ADM1 units across Philippines, Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste, plus ADB regional scale-out readiness for 50 regional member economies. It is not yet a road-network travel-time or facility-catchment result.",
    command: "npm run research:access",
    inputs: [
      "World Bank WDI population, land area, and rural-share indicators",
      "World Bank CCKP baseline and SSP2-4.5 tasmax/precipitation summaries",
      "OpenStreetMap service counts queried through Overpass",
      "geoBoundaries gbOpen ADM1 boundaries for Philippines, Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste",
      "Philippine Statistics Authority OpenSTAT 2020 regional population",
      "WorldPop 2020 stats API population totals for Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste ADM1 polygons, with clipped-tile summation for polygons over the API area allowance",
      "ADB ARIC regional member-economy grouping for the scale-out list",
    ],
    outputs: [
      "src/data/generated/access-services-pilots.json",
      "public/data/access-services-pilots.json",
      "src/data/generated/access-services-admin1.json",
      "public/data/access-services-admin1.json",
      "public/data/access-services-admin1.csv",
      "research/access-services/generated/access-services-admin1.csv",
      "src/data/generated/access-services-nextwave-admin1.json",
      "public/data/access-services-nextwave-admin1.json",
      "public/data/access-services-nextwave-admin1.csv",
      "research/access-services/generated/access-services-nextwave-admin1.csv",
      "src/data/generated/access-services-frontier-admin1.json",
      "public/data/access-services-frontier-admin1.json",
      "public/data/access-services-frontier-admin1.csv",
      "research/access-services/generated/access-services-frontier-admin1.csv",
      "src/data/generated/access-services-computed-admin1.json",
      "public/data/access-services-computed-admin1.json",
      "public/data/access-services-computed-admin1.csv",
      "research/access-services/generated/access-services-computed-admin1.csv",
      "src/data/generated/access-services-adb-scaleout.json",
      "public/data/access-services-adb-scaleout.json",
      "public/data/access-services-adb-scaleout.csv",
      "research/access-services/generated/access-services-adb-scaleout.csv",
    ],
    rerunSteps: [
      "Install dependencies with npm install.",
      "Run npm run research:access from the repo root.",
      "Check generatedAt, source URLs, OSM timestamps, population methods, and economy/admin records in the JSON outputs.",
      "Run npm run lint and npm run build before treating the output as web-ready.",
    ],
    auditTrail: [
      "The script writes source URLs and retrieval metadata into the generated JSON.",
      "Overpass results include OSM and OSM-area timestamps so a future run can explain service-count changes.",
      "The admin output records whether service counts used OSM ISO3166-2 admin areas or a bbox fallback.",
      "The next-wave output records whether WorldPop population was queried as a single polygon or summed over clipped tiles.",
      "The frontier output records the same source/method fields for Cambodia, Lao PDR, and Timor-Leste, and the combined output concatenates all computed ADM1 batches.",
      "The regional scale-out output records boundary availability, WDI availability, readiness scores, blocker notes, and export paths.",
      "The UI labels the result as an ADM1 screening index and shows caveats beside the map and tables.",
    ],
    aiDisclosure: [
      "AI assisted with source triage, TypeScript pipeline drafting, metric naming, UI composition, and documentation.",
      "AI did not invent the pilot values; the current values are generated by the committed script.",
      "AI-assisted judgment is still present in the first-pass index weights and should be reviewed before publication.",
    ],
    humanChecks: [
      "Pipeline executed locally for both countries.",
      "Next-wave ADM1 run executed locally for Pakistan, Nepal, and Sri Lanka.",
      "Frontier ADM1 run executed locally for Cambodia, Lao PDR, and Timor-Leste.",
      "Generated JSON was wired into the app rather than hard-coded in cards.",
      "Lint, production build, HTTP checks, and Chrome screenshots were run.",
    ],
    limitations: [
      "Facility counts depend on OSM mapping completeness.",
      "The current index has no road graph, flood passability model, or facility capacity layer yet.",
      "Bangladesh, Pakistan, Nepal, Sri Lanka, Cambodia, Lao PDR, and Timor-Leste ADM1 population uses WorldPop 2020 polygon statistics; Philippines ADM1 population uses official PSA 2020 regional census values, so cross-country comparisons should be framed as screening rather than official harmonized statistics.",
      "Four Pakistan ADM1 WorldPop values are summed over clipped tiles because the full polygons exceed the API area allowance.",
      "One frontier service-count row used bounding-box fallback after the OSM admin-area query was not usable.",
      "The ADB scale-out artifact is readiness evidence only; it does not compute service counts or stress scores for all regional economies.",
      "The combined ADM1 artifact is a concatenation of batches, not a guarantee that every ADB economy has been computed.",
      "The next reproducibility upgrade is grid-level travel-time output with explicit flood and heat scenario parameters.",
    ],
  },
  {
    slug: "digital-performance",
    title: "Measured Digital Development Gap",
    status: "Download manifest and SQL artifact exist",
    claimScope:
      "Pipeline preparation for Philippines and Bangladesh. No final Ookla aggregate has been claimed yet.",
    command: "npm run research:ookla",
    inputs: [
      "Ookla Open Data quarterly fixed and mobile tile URLs",
      "Pilot bounding boxes for Philippines and Bangladesh",
      "DuckDB SQL templates for local aggregation",
    ],
    outputs: [
      "src/data/generated/digital-performance-ookla-pilots.json",
      "public/data/digital-performance-ookla-pilots.json",
      "research/digital-performance/generated/ookla-mobile-2026-q1.sql",
      "research/digital-performance/generated/ookla-fixed-2026-q1.sql",
    ],
    rerunSteps: [
      "Run npm run research:ookla for the manifest-only default.",
      "Set OOKLA_YEAR and OOKLA_QUARTER to reproduce another release.",
      "Set OOKLA_DOWNLOAD=1 only when ready to download large global parquet files.",
      "Run the generated SQL in DuckDB with httpfs and then validate the parquet schema.",
    ],
    auditTrail: [
      "The generated manifest records release year, quarter, access mode, and pilot filters.",
      "The SQL files are committed so aggregation assumptions can be reviewed before downloading large data.",
      "The web page states that this is prepared, not a completed Ookla result.",
    ],
    aiDisclosure: [
      "AI assisted with the manifest script, DuckDB SQL scaffold, and UI explanation.",
      "AI did not fabricate speed, latency, test, or device metrics.",
      "The generated SQL still needs schema validation against the downloaded Ookla parquet release.",
    ],
    humanChecks: [
      "Manifest generation was executed locally.",
      "The digital-performance page renders the generated pipeline status.",
      "Lint and build passed after wiring the artifact into the UI.",
    ],
    limitations: [
      "Ookla is user-initiated test data, not a random sample.",
      "Large parquet files were intentionally not downloaded by default.",
      "Population weighting and measurement-desert metrics are not computed yet.",
    ],
  },
  {
    slug: "air-monitoring",
    title: "Air Pollution Without Air Monitors",
    status: "Computed OpenAQ monitor aggregation exists",
    claimScope:
      "Best-effort OpenAQ public-location metadata, World Bank population denominators, WDI PM2.5 national exposure, and WHO city PM2.5 validation for ADB regional member economies. This is a national screening layer, not yet local distance-to-monitor exposure.",
    command: "npm run research:openaq",
    inputs: [
      "OpenAQ API v3 location metadata",
      "ISO2 filters for ADB regional member economies listed by ADB ARIC",
      "World Bank WDI population indicator SP.POP.TOTL",
      "World Bank WDI PM2.5 exposure indicator EN.ATM.PM25.MC.M3",
      "WHO Ambient Air Quality Database V6.1 city PM2.5, PM10, and NO2 workbook",
      "Parameter coverage fields for PM2.5, PM10, NO2, O3, SO2, and CO",
    ],
    outputs: [
      "src/data/generated/air-monitoring-openaq-pilots.json",
      "public/data/air-monitoring-openaq-pilots.json",
      "public/data/air-monitoring-openaq-economies.csv",
      "research/air-monitoring/generated/openaq-adb-regional-economies.csv",
      "scripts/research/earthengine-sentinel5p-no2-export.js",
    ],
    rerunSteps: [
      "Keep OPENAQ_API_KEY available in the local environment or .env.local.",
      "Run npm run research:openaq from the repo root.",
      "Inspect total public locations, fresh/stale counts, parameters, and generatedAt in the JSON output.",
      "If the key is missing or invalid, keep the blocked state rather than filling placeholder monitor values.",
    ],
    auditTrail: [
      "The current artifact records computed status, generatedAt, source API, ADB regional-economy source, WDI source URLs, WHO city database source, summary counts, and per-economy monitor/population/exposure/validation metrics.",
      "The app displays public monitor metadata separately from any future satellite exposure model.",
      "The source caveat states that OpenAQ absence is not proof that a monitor does not exist.",
    ],
    aiDisclosure: [
      "AI assisted with the API script, blocked-state handling, and UI copy.",
      "AI did not estimate monitor counts or PM2.5 exposure; monitor counts come from OpenAQ and PM2.5 exposure comes from World Bank WDI.",
      "NO2 satellite exposure is explicitly marked as not computed locally; an Earth Engine Sentinel-5P export scaffold has been added but not run.",
    ],
    humanChecks: [
      "The key-backed OpenAQ path was executed locally across 50 ADB regional economies and generated computed output.",
      "The air-monitoring page renders the computed best-effort regional monitor metadata.",
      "Lint and build passed after adding the panel.",
    ],
    limitations: [
      "OpenAQ coverage is only public/provider-discovered monitoring data.",
      "The current output is national screening, not local distance-to-monitor exposure.",
      "NO2 and PM2.5 satellite exposure layers are not wired into the pipeline yet.",
    ],
  },
  {
    slug: "invisible-urbanization",
    title: "Invisible Urbanization",
    status: "Research design documented; no computed artifact yet",
    claimScope:
      "Source-backed method proposal only. No building-growth claims are made by the current app.",
    command: "Not implemented yet",
    inputs: [
      "Google Open Buildings 2.5D Temporal",
      "Dynamic World built-up probabilities",
      "GHSL settlement layers",
      "WorldPop/GHSL population denominators",
      "Overture and Microsoft building/transport layers",
    ],
    outputs: [
      "research/invisible-urbanization/README.md",
      "Program design page at /research/invisible-urbanization",
    ],
    rerunSteps: [
      "Create an Earth Engine export script for annual building summaries.",
      "Define admin/grid units before computing growth metrics.",
      "Commit only summary tables, schemas, and lightweight map artifacts.",
      "Label outputs as preliminary until building detections are validated against known settlements.",
    ],
    auditTrail: [
      "The current page separates hypothesis, source stack, method, and caveats.",
      "No visual time-lapse or building metric is presented as computed evidence yet.",
      "Future artifacts should include Earth Engine asset IDs and export dates.",
    ],
    aiDisclosure: [
      "AI assisted with source triage, idea framing, page structure, and documentation.",
      "AI did not generate building detections or settlement-change statistics.",
      "The method needs domain review before being used for planning claims.",
    ],
    humanChecks: [
      "Source links and caveats were reviewed at the page-content level.",
      "No computational validation has been performed because the pipeline is not yet implemented.",
      "Lint and build cover the page only, not empirical outputs.",
    ],
    limitations: [
      "Building presence does not equal occupancy.",
      "Google temporal coverage does not include every ADB economy.",
      "Urban-boundary comparisons require national-definition review.",
    ],
  },
];

export function getReproducibilityProfile(slug: string): ReproducibilityProfile {
  const profile = reproducibilityProfiles.find((item) => item.slug === slug);

  if (!profile) {
    throw new Error(`Unknown reproducibility profile: ${slug}`);
  }

  return profile;
}
