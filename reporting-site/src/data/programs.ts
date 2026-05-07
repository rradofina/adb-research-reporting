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

// Snapshot of the issue status register as of 2026-04-27.
// Keep in sync with the article frontmatter and evidence packets.
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
    title: "Climate-adjusted access to services",
    status: "SR",
    summary:
      "104 ADM1 units across 8 ADB DMCs (PHL, BGD, PAK, NPL, LKA, KHM, LAO, TLS) computed as a national-and-ADM1 screening index from World Bank WDI, CCKP, geoBoundaries, WorldPop stats, PSA OpenSTAT, and OSM/Overpass. Not yet a travel-time raster.",
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
    title: "Air pollution without air monitors",
    status: "SR",
    summary:
      "OpenAQ v3 + WDI PM2.5 + WHO AAQ v6.1 observability screen across 50 ADB regional economies. 7 economies flagged for sparse PM2.5 monitoring; 14.3M people live in above-guideline PM2.5 economies with no public PM2.5 monitor.",
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
    title: "Climate-health workday loss",
    status: "PR",
    summary:
      "WDI outdoor-labor share × PM2.5 exposure for 44 ADB DMCs. AFG 55.7 (26M exposed); IND 53.1 (798.6M exposed outdoor workers in above-WHO-guideline PM2.5); BGD 44.6 (93M); PAK 41.5 (123M). Heat exposure (CCKP tasmax) NOT yet included.",
    note: "Finished for current issue under AI-first; heat layer remains the human-final upgrade path.",
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
    title: "Disaster recovery lag",
    status: "PR",
    summary:
      "EM-DAT (CRED) burden layer 2000–2025 for 38 ADB DMCs. CHN: 25.6 events/yr, 1.77B affected. IND: 15.5/yr, 1.15B. PHL: 14.9/yr. IDN: 15.7/yr. NOT yet a recovery-lag metric — that requires event-timestamped indicator-recovery curves.",
    note: "Finished for current issue under AI-first; recovery-lag curves remain the upgrade path.",
    href: "/program/disaster-recovery-lag",
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
    title: "Grid reliability under heat",
    status: "PR",
    summary:
      "WRI Global Power Plant DB v1.3.0 + WDI electricity access for 39 ADB DMCs. 7,071 plants, 39 fuel-concentration profiles. Single-fuel grids: BTN 100% Hydro, BRN 100% Gas, NPL 95%, MNG 89% Coal, TJK 88% Hydro, KAZ 85% Coal. NOT yet a heat-stress reliability metric — that requires ERA5 × outage data.",
    note: "Finished for current issue under AI-first; heat-reliability outage data remain the upgrade path.",
    href: "/program/grid-reliability-heat",
  },
  {
    id: 11,
    slug: "migration-displacement-signals",
    title: "Migration and displacement signals",
    status: "PR",
    summary:
      "UN DESA International Migrant Stock 2024 per ADB DMC. IND 18.5M emigrants (top dest UAE, US); CHN 11.7M; BGD 8.7M; AFG 7.5M (Iran, Pakistan); PHL 7.0M (US, Canada); PAK 6.9M (Saudi, UAE); MMR 4.3M (Thailand).",
    note: "Finished for current issue under AI-first; displacement-flow extensions remain the upgrade path.",
    href: "/program/migration-displacement-signals",
  },
  {
    id: 12,
    slug: "port-hinterland-friction",
    title: "Port-hinterland trade friction",
    status: "PR",
    summary:
      "WB LPI (Logistics Performance Index) × WDI imports USD across ADB DMCs. Top friction exposure: CHN (1.45), IND (0.94), IDN (0.66), VNM (0.63), THA (0.54). Landlocked DMCs (AFG, UZB, KGZ, TJK, LAO, MNG) have structurally different story.",
    note: "Finished for current issue under AI-first; port and inland-node data remain the upgrade path.",
    href: "/program/port-hinterland-friction",
  },
  {
    id: 13,
    slug: "public-service-data-quality",
    title: "Public service data quality",
    status: "PR",
    summary:
      "OSM health-amenity counts compared to DOH NHFR (PHL) and DGHS Facility Registry (BGD). The flagship now adds PHL ADM3 Open Buildings context, BGD upazila settlement/road context, and an owner-downloaded official Philippines PSA SAE poverty overlay.",
    note: "Flagship paper. Finished for current issue under AI-first; human-final review remains the upgrade path.",
    href: "/program/public-service-data-quality",
  },
  {
    id: 14,
    slug: "remittance-resilience",
    title: "Remittance resilience gaps",
    status: "PR",
    summary:
      "WDI BX.TRF.PWKR.DT.GD.ZS dependence × RPW Q1 2025 inbound transfer cost across 44 ADB DMCs. Top 5 fragile: Kyrgyz Republic (70.3), Samoa (51.0), Tonga (50.1), Vanuatu (47.7), Nepal (44.9). Tonga at 42.6% remittance dependence is striking.",
    note: "Flagship paper. Finished for current issue under AI-first; volume-weighted corridor costs remain the upgrade path.",
    href: "/program/remittance-resilience",
  },
  {
    id: 15,
    slug: "school-heat-disruption",
    title: "School heat disruption",
    status: "SR",
    summary:
      "WDI school-age share × Primary PTR × CCKP historical tasmax per 32 ADB DMCs. Top pressure: KHM 14.2 (5.3M children, 31.9°C, PTR 41.7). BGD 6.8 (48.6M). IND 6.3 (357M children). Future-period tasmax (2040-2059 SSP2-4.5) would amplify meaningfully.",
    note: "Screening result only; heat-learning functional form remains the upgrade path.",
    href: "/program/school-heat-disruption",
  },
  {
    id: 16,
    slug: "social-protection-shock-coverage",
    title: "Social protection shock coverage",
    status: "PR",
    summary:
      "WDI ASPIRE SP coverage × Findex account ownership × poverty for ADB DMCs. Top readiness gap: PAK 18.0 (23% poverty, 22% SP, 21% accounts); VUT 13.6 (19.5% poverty, 30% SP); MMR 7.1; LAO 5.7 (only 2% SP coverage).",
    note: "Finished for current issue under AI-first; adequacy and delivery-speed data remain the upgrade path.",
    href: "/program/social-protection-shock-coverage",
  },
  {
    id: 17,
    slug: "water-stress-crop-diversification",
    title: "Water stress and crop concentration",
    status: "SR",
    summary:
      "WDI water × yield × rural composite. Turkmenistan at 1,868% freshwater withdrawal (rel. to internal resources — transboundary-reliant), Pakistan 326%, Uzbekistan 263%, Azerbaijan 161%. Top index: TKM 79.4, PAK 75.3, AZE 54.4.",
    note: "Screening result only; basin and crop-calendar data remain the upgrade path.",
    href: "/program/water-stress-crop-diversification",
  },
];
