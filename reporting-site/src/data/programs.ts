import type { Maturity } from "../lib/claimTiers";

export interface ProgramEntry {
  id: number;
  slug: string;
  title: string;
  status: Maturity;
  summary: string;
  note?: string;
  href?: string;
}

// Snapshot of the issue status register as of 2026-05-07.
// Keep in sync with research/wip-register.md, CONSTITUTION.md §15, and the
// article frontmatter. 9 programs were demoted PR/SR → PP on 2026-05-07
// because their original advancement was a single composite-index screening
// only — see CONSTITUTION.md §16 amendment of 2026-05-07 for rationale.
export const programs: ProgramEntry[] = [
  {
    id: 0,
    slug: "mpi-nighttime-lights",
    title: "MPI × nighttime lights decomposition (Asia-Pacific)",
    status: "H",
    summary:
      "Co-authored with Arturo Martinez Jr. Legacy program; OPHI MPI 2024 data pulled into repo; NTL integration not yet committed. Status provisional pending owner reconciliation.",
  },
  {
    id: 1,
    slug: "access-services",
    title: "When the facility map changes the rank",
    status: "PP",
    summary:
      "Official clinical registries reorder 16 of 17 Philippine regional facility-load ranks and 6 of 8 Bangladesh division ranks built from OSM points. The eight-economy panel is retained as a map-observability and source-validation queue, not a service-access or DMC-performance ranking.",
    href: "/program/access-services",
  },
  {
    id: 2,
    slug: "digital-performance",
    title: "Measured digital development gap",
    status: "PP",
    summary:
      "Ookla Open Data manifest + DuckDB SQL scaffold committed for PHL/BGD. Opt-in parquet download; no aggregated speed/latency claims yet.",
  },
  {
    id: 3,
    slug: "air-monitoring",
    title: "Public monitor QA observability",
    status: "SR",
    summary:
      "Generated evidence ledger indexes 64 air-monitoring summary rows and 214 supporting files. Public sources expose station, method, dashboard, and denominator context, but station-level calibration/inspection/status, validated same-station, complete monitor-grade, and coverage-claim gates remain at zero.",
    href: "/program/air-monitoring",
  },
  {
    id: 4,
    slug: "invisible-urbanization",
    title: "Invisible urbanization",
    status: "SR",
    summary:
      "WDI urban-growth-from-rural-base screening across 41 ADB DMCs. Stable top signal: Papua New Guinea, Solomon Islands, Afghanistan, Lao PDR, and Bangladesh. GHSL built-up-surface integration remains the upgrade-pass.",
    note: "Screening result only; satellite built-up-surface validation not yet done.",
    href: "/program/invisible-urbanization/evidence",
  },
  {
    id: 5,
    slug: "climate-health-workdays",
    title: "When a stable proxy measures the wrong construct",
    status: "PP",
    summary:
      "Across 21 aligned year-and-parameter tests, the inherited PM2.5 × employment proxy shares at most one of its top three economies with the Lancet Countdown heat-related potential work-hours-loss measure. Sixteen tests have zero overlap; five have one.",
    note: "PP construct-validation issue rebuilt 2026-07-18. Potential hours are modelled capacity losses, not observed absence; heat and PM2.5 remain separate pathways.",
    href: "/program/climate-health-workdays",
  },
  {
    id: 6,
    slug: "coastal-informal-risk",
    title: "Coastal informal settlement risk",
    status: "SR",
    summary:
      "Population-scaled urban-informal-pressure proxy for 31 coastal ADB DMCs. Stable top-5: Pakistan, Philippines, China, Bangladesh, Myanmar. Low-elevation coastal zone integration remains the upgrade-pass.",
    note: "Screening result only; WDI slum data are sparse and partly imputed.",
    href: "/program/coastal-informal-risk/evidence",
  },
  {
    id: 7,
    slug: "disaster-recovery-lag",
    title: "Disaster recovery measurement",
    status: "PP",
    summary:
      "The inherited burden top-two fails under three of five metrics. A 108-orbit Typhoon Haiyan pilot then yields zero of seven GDIS centroids with one recovery month across 54 variants. Public access scales; the recovery construct is not yet validated.",
    note: "AI-first construct-validation package. Nighttime radiance is a proxy, not welfare or causal recovery.",
    href: "/disaster-recovery-lag",
  },
  {
    id: 8,
    slug: "flood-market-access",
    title: "Flood-driven service and market isolation",
    status: "SR",
    summary:
      "EM-DAT flood events × WDI rural share × population proxy across 41 ADB DMCs. Stable top-4: India, China, Indonesia, Afghanistan. Road-network disruption remains the upgrade-pass.",
    note: "Screening result only; not yet an all-weather road or market-access model.",
    href: "/program/flood-market-access/evidence",
  },
  {
    id: 9,
    slug: "food-price-climate-transmission",
    title: "Food-price climate transmission",
    status: "SR",
    summary:
      "The unstable composite was dropped. Usable screen: Lao PDR and Pakistan sit jointly high on CPI inflation and agriculture-import exposure for every N from 3 to 10; Bangladesh joins from N=5.",
    note: "Screening result only; climate-to-price transmission is not claimed.",
    href: "/program/food-price-climate-transmission",
  },
  {
    id: 10,
    slug: "grid-reliability-heat",
    title: "When the heat–reliability direction changes with the measure",
    status: "PP",
    summary:
      "The capacity-to-generation top five survives, but 15 exact-year heat–reliability correlations split 8 positive to 7 negative. Fuel concentration is structural exposure; a regional heat-vulnerability ranking is not supported.",
    note: "PP construct-validation story; seven evidence figures and full reproduction trail.",
    href: "/grid-reliability-heat",
  },
  {
    id: 11,
    slug: "migration-displacement-signals",
    title: "When the migration denominator changes the leading set",
    status: "PP",
    summary:
      "The absolute and population-share top fives have zero overlap. Samoa, Tonga, Armenia, Nauru, and Fiji replace India, China, Bangladesh, Afghanistan, and the Philippines; Afghanistan is the near-rank exception, but UNHCR forced-displacement stock equals 81.7% of its UN DESA emigrant stock.",
    note: "PP issue rebuilt around the denominator switch; stock, flow, and migration-purpose limits are explicit.",
    href: "/program/migration-displacement-signals",
  },
  {
    id: 12,
    slug: "port-hinterland-friction",
    title: "Trade volume did not predict observed port delay",
    status: "PP",
    summary:
      "Only Indonesia overlaps between the inherited imports × LPI top five and the main 2025 CPPI-disadvantage top five. Across 20 year, call-threshold, and aggregation specifications, overlap remains zero to two; CPPI still stops at the port boundary.",
    note: "PP construct validation complete; the official LPI 2.0 shipment file is required before any hinterland claim.",
    href: "/program/port-hinterland-friction",
  },
  {
    id: 13,
    slug: "public-service-data-quality",
    title: "Public service data quality",
    status: "PR",
    summary:
      "OSM health-amenity counts compared to DOH NHFR (PHL) and DGHS Facility Registry (BGD). 17.1% (PHL) and 11.8% (BGD) clinical-tier match. 9.8× rural-urban gradient. Now with ADM3 Open Buildings context, road context, PSA SAE poverty overlay, and the BARMM barangay-name resolver (249 of 257 unresolved records resolved).",
    note: "Active flagship. Publication-ready under the ai-first chain and Mode A as of 2026-05-07. Human-final review remains the upgrade path under §18.5.",
    href: "/public-service-data-quality",
  },
  {
    id: 14,
    slug: "remittance-resilience",
    title: "Remittance resilience gaps",
    status: "PP",
    summary:
      "Tonga 42.6 %, Kyrgyz Republic 26.6 %, Nepal 26.2 %, Samoa 24.0 %, Vanuatu 18.8 % -- five economies where remittances are central to GDP and observed RPW corridor costs sit above the SDG 10.c.1 3 % reference line. The repaired baseline top five survive median and flow-weighted checks as a set; the +/-50 % sensitivity common core narrows to four.",
    note: "Demoted PR -> PP on 2026-05-07; reopened for parser repair and flow-weighted corridor-cost deepening.",
    href: "/program/remittance-resilience",
  },
  {
    id: 15,
    slug: "school-heat-disruption",
    title: "School heat disruption",
    status: "PP",
    summary:
      "Cambodia is the single DMC that clears the screen under ±50 % sensitivity — 5.3 M children 0–14, primary pupil-teacher ratio 41.7 (highest in the screen), historical-period tasmax 31.9 °C. Top-5 ranking fails sensitivity; future-period tasmax (2040–2059 SSP2-4.5) would amplify the gradient.",
    note: "Demoted SR → PP on 2026-05-07; awaits the new program loop.",
    href: "/program/school-heat-disruption",
  },
  {
    id: 16,
    slug: "social-protection-shock-coverage",
    title: "Social protection shock coverage",
    status: "PP",
    summary:
      "The inherited ‘stable top five’ is rejected. Vanuatu and Tajikistan outrank two named members but were omitted for missing one proxy leg; all five named economies have documented COVID-19 cash-transfer responses, while zero comparable delivery outcomes are joined.",
    note: "AI-first construct-validation checkpoint completed 2026-07-18; the country ranking is retired.",
    href: "/program/social-protection-shock-coverage",
  },
  {
    id: 17,
    slug: "water-stress-crop-diversification",
    title: "Water stress and crop diversification",
    status: "PP",
    summary:
      "The inherited top four fails direct construct checks: only two published members enter the available-water top five, none enters the crop-HHI top five, and all five crop-concentration leaders lack water-stress rows.",
    note: "AI-first construct-validation checkpoint completed 2026-07-18; the country ranking is retired.",
    href: "/program/water-stress-crop-diversification",
  },
];
