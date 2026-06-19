export type ShowcaseReportStatus = "verified" | "active";

export type ShowcaseAuditKind =
  | "rank-shift"
  | "stacked-blindness"
  | "coverage-funnel"
  | "sensitivity-lanes"
  | "parameter-audit"
  | "tautology-audit"
  | "component-audit";

export interface ShowcaseAudit {
  kind: ShowcaseAuditKind;
  programSlug: string;
  dataUrl: string;
  csvUrl?: string;
  question: string;
  finding: string;
  method: string;
  readerPayoff: string;
  nonClaim: string;
  downloadLabel: string;
}

export interface ShowcaseReport {
  id: number;
  title: string;
  shortTitle: string;
  href: string;
  status: ShowcaseReportStatus;
  statusLabel: string;
  deck: string;
  evidencePath: string;
  visual: string;
  sourceNote: string;
  audit?: ShowcaseAudit;
}

export interface ShowcaseReportDepth {
  operationalUse: string;
  falsifier: string;
  limitation: string;
}

export type ShowcaseReadiness =
  | "prototype"
  | "l3-candidate"
  | "evidence-audit"
  | "owner-gated";

export interface ShowcaseReportQuality {
  readiness: ShowcaseReadiness;
  readinessLabel: string;
  qaSummary: string;
  publicationGap: string;
  nextUpgrade: string;
}

export const showcaseReports: ShowcaseReport[] = [
  {
    id: 1,
    title: "When Food Prices Spike, Is the Weather Local?",
    shortTitle: "Market-level climate price transmission",
    href: "/showcase",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "Nepal market-month rice prices joined to point climate data to separate local weather signals from broader price waves.",
    evidencePath: "research/topic-sprints/nepal-market-climate-prices-sprint.md",
    visual: "Animated market-month price and precipitation heatmaps",
    sourceNote: "WFP food-price rows and NASA POWER point climate API",
  },
  {
    id: 2,
    title: "When Public Data Arrive Late",
    shortTitle: "Public data freshness blind spots",
    href: "/showcase/data-freshness",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "A 42-economy by 9-indicator WDI vintage matrix shows where planning data are current, stale, or missing.",
    evidencePath: "research/topic-sprints/wdi-data-freshness-sprint.md",
    visual: "Interactive economy-indicator freshness matrix",
    sourceNote: "World Bank WDI API retrieval and source-vintage fields",
  },
  {
    id: 3,
    title: "When Account Ownership Is Not a Payment Rail",
    shortTitle: "Shock-payment rails after disasters",
    href: "/showcase/shock-payment-rails",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "Disaster exposure is compared with observable account, payment-use, and social-protection rails before any readiness claim.",
    evidencePath: "research/topic-sprints/shock-payment-rails-sprint.md",
    visual: "Disaster-frequency scatter with payment-rail gap bars",
    sourceNote: "EM-DAT, Findex, ASPIRE, and WDI public indicators",
  },
  {
    id: 4,
    title: "When the Registry and the Map Disagree",
    shortTitle: "Public service data quality source disagreement",
    href: "/showcase/psdq-source-disagreement",
    status: "verified",
    statusLabel: "L3 evidence module",
    deck: "Bangladesh registry-map disagreement is packaged with ratio strata, validation residues, a facility-level sample, automated screening, AI review, candidate-resolution lanes, richer public-source tag checks, coordinate-repair triage, public-map-gap lanes, row-level evidence, a targeted public-map inspection queue, first-row confirmation, 40-row public-source confirmation, a 16-row public-source decision ledger, a 3-row possible same-facility review, a 9-row priority name-conflict review, a 6-row lower-priority name-conflict spot check, a 115-upazila zero-OSM observability review, a 10-stage evidence ladder, 4 source-repair evidence attachments, 4 official-coordinate evidence rows, a 4-row public-explanation search, a 3-row correction-record follow-up, a 3-row no-contact clarification packet, a 3-row registry-vintage review, a 39-row human-gated handoff matrix, a 39-row blank human-validation worksheet, and a 39-row AI closure audit before access maps are trusted.",
    evidencePath: "public-service-data-quality/source-disagreement-l3-module.md",
    visual: "Ranked registry-versus-OSM workbench, ratio-strata ledger, validation sample, coded-screen chart, AI review workstreams, candidate-resolution lanes, public-source tag-support lanes, coordinate-repair distance ledger, public-map-gap upazila queue, row-evidence reviewer queue, targeted public-map inspection cards, first-row confirmation scores, 40-row upazila confirmation lanes, decision-ledger row tracks, possible same-facility evidence gates, priority name-conflict queue cards, lower-priority repeated-candidate spot-check cards, zero-OSM upazila observability bars, 10-stage evidence ladder, source-repair evidence cards, official-coordinate gap cards, public-explanation conflict cards, correction-record follow-up cards, clarification-question cards, registry-vintage gate cards, a human-gated handoff wall, worksheet downloads, and an AI closure-audit wall",
    sourceNote: "DOH NHFR, DGHS registry, OSM, Open Buildings, and PSA context",
  },
  {
    id: 5,
    title: "When Corridor Averages Hide Flow Exposure",
    shortTitle: "Remittance corridors after flow weighting",
    href: "/showcase/remittance-flow-weighting",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "RPW remittance prices are rechecked with public bilateral-flow weights so corridor-cost exposure is not counted equally by default.",
    evidencePath: "remittance-resilience/flow-weighting-l3-module.md",
    visual: "Equal-weighted versus flow-weighted corridor-cost scatter",
    sourceNote: "World Bank RPW, KNOMAD bilateral flows, and WDI remittance dependence",
  },
  {
    id: 6,
    title: "When OpenAQ Is Not the Regulator Map",
    shortTitle: "Air-monitoring observability",
    href: "/showcase/air-monitoring-observability",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "Ground-monitor visibility is compared with PM2.5 exposure, GDP context, OpenAQ station coordinates, regulator-source candidates, official station-table extraction, official/OpenAQ reconciliation, a 13-row candidate review worksheet, public OpenAQ metadata evidence, isMonitor source screening, public-feed source screening, a 169-item one-signal review queue, monitor-grade source-language evidence, and a 14-source monitor-grade source-validation scan before a monitoring-gap claim is widened.",
    evidencePath: "air-monitoring/monitor-grade-source-validation-scan.md",
    visual: "Zero-monitor exposure bars, GDP residual scatter, metadata-readiness wall, OpenAQ coordinate map, regulator-source wall, official-source bars, official/OpenAQ reconciliation ladder, candidate station-crosswalk worksheet, public-evidence attachment, isMonitor source-scan decisions, public-feed source-scan decisions, one-signal review wall, monitor-grade evidence ladder, and monitor-grade source-validation wall",
    sourceNote: "OpenAQ v3 locations, public regulator and official portal station tables/APIs, Bangladesh, Sri Lanka, BMKG, Uzhydromet, NEA, CEA, Brunei, Malaysia, and Tajikistan source-language checks, WHO ambient air quality database, WDI, and committed source artifacts",
  },
  {
    id: 7,
    title: "When Access Maps Measure Mapping Completeness",
    shortTitle: "Access map-completeness audit",
    href: "/showcase/access-map-completeness",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "OSM health amenities are checked against official registry denominators before population-per-facility maps are interpreted.",
    evidencePath: "access-services/deepened-results.md",
    visual: "Rank-flip chart, completeness scatter, and correction wall",
    sourceNote: "OSM, official clinical registries, WorldPop, and sibling PSDQ artifacts",
  },
  {
    id: 8,
    title: "When the Disaster Top-Two Breaks",
    shortTitle: "Disaster metric falsification",
    href: "/showcase/disaster-metric-falsification",
    status: "verified",
    statusLabel: "Prototype report",
    deck: "A pre-registered disaster-burden pair is tested against alternate EM-DAT metrics before any recovery-lag narrative is reused.",
    evidencePath: "disaster-recovery-lag/deepened-results.md",
    visual: "Metric-switch bars for events, affected, damage, deaths, and per-capita burden",
    sourceNote: "EM-DAT country profiles with WDI population denominators",
  },
  {
    id: 9,
    title: "When Power Capacity and Generation Tell Different Stories",
    shortTitle: "Power-fuel concentration audit",
    href: "/showcase/grid-generation-mismatch",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "WRI plant capacity and modeled generation test whether a single-fuel reliability screen survives when output replaces installed megawatts.",
    evidencePath: "grid-reliability-heat/generated/grid-generation-deepening.json",
    visual: "Capacity-versus-generation concentration bridge with coverage gates",
    sourceNote: "WRI Global Power Plant Database, 2017 generation fields, and coverage withholding rules",
    audit: {
      kind: "rank-shift",
      programSlug: "grid-reliability-heat",
      dataUrl: "/programs/grid-reliability-heat/generated/grid-generation-deepening.json",
      csvUrl: "/programs/grid-reliability-heat/generated/grid-generation-deepening.csv",
      question: "Does a capacity-based fuel concentration screen still hold when the denominator is actual reported or modeled generation?",
      finding: "The top-five set survives, but the page keeps the coverage gate visible because low generation coverage is the real limitation.",
      method: "Compute the same fuel-Herfindahl screen on capacity and on 2017 generation, then compare top sets and withheld rows.",
      readerPayoff: "A reliability-looking chart becomes a source-coverage audit before it becomes a claim about reliability.",
      nonClaim: "This is not a power-reliability ranking and does not observe outages, reserve margins, or grid heat stress.",
      downloadLabel: "Download generation audit JSON",
    },
  },
  {
    id: 10,
    title: "When the Largest Diasporas Become Small Islands",
    shortTitle: "Emigration denominator switch",
    href: "/showcase/migration-denominator-switch",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "UN DESA emigrant stocks are divided by WDI origin population, turning an absolute-stock story into a small-economy exposure screen.",
    evidencePath: "migration-displacement-signals/generated/migration-per-population-deepening.json",
    visual: "Absolute rank versus population-share rank bridge",
    sourceNote: "UN DESA International Migrant Stock 2024 and WDI 2024 population denominators",
    audit: {
      kind: "rank-shift",
      programSlug: "migration-displacement-signals",
      dataUrl: "/programs/migration-displacement-signals/generated/migration-per-population-deepening.json",
      csvUrl: "/programs/migration-displacement-signals/generated/migration-per-population-deepening.csv",
      question: "What changes when emigrant stock is read as a share of origin population instead of an absolute count?",
      finding: "None of the absolute top five survives into the population-share top five.",
      method: "Join UN DESA emigrant stock to WDI origin population and rank both the absolute stock and the population share.",
      readerPayoff: "The emotional turn is immediate: the biggest countries stop dominating once exposure is sized by population.",
      nonClaim: "This is not a judgment about whether migration is good or bad, and it is not a fragility ranking.",
      downloadLabel: "Download migration denominator JSON",
    },
  },
  {
    id: 11,
    title: "When Night Lights Cannot See the Poverty Dimension",
    shortTitle: "MPI night-light blind spot",
    href: "/showcase/mpi-nightlight-blindspot",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "MPI deprivation shares are decomposed before any VIIRS join, showing how much of the poverty construct is outside nighttime radiance.",
    evidencePath: "mpi-nighttime-lights/generated/mpi-dimension-decomposition.json",
    visual: "Blind-versus-visible MPI dimension bars",
    sourceNote: "OPHI global MPI microdata-derived table already parsed on disk; VIIRS join remains owner-gated",
    audit: {
      kind: "stacked-blindness",
      programSlug: "mpi-nighttime-lights",
      dataUrl: "/programs/mpi-nighttime-lights/generated/mpi-dimension-decomposition.json",
      csvUrl: "/programs/mpi-nighttime-lights/generated/mpi-dimension-decomposition.csv",
      question: "Before joining night lights, how much of MPI is structurally outside a radiance signal?",
      finding: "Most ADB economies have a majority of MPI weight in health and education dimensions that night lights cannot directly see.",
      method: "Decompose each economy's MPI into dimensions plausibly visible and blind to nighttime radiance.",
      readerPayoff: "The chart turns a flashy satellite idea into a humility test for the poverty construct.",
      nonClaim: "This does not compute a night-lights poverty model or replace the owner-led co-authored MPI track.",
      downloadLabel: "Download MPI decomposition JSON",
    },
  },
  {
    id: 12,
    title: "When Population Size Drives the Coastal Slum Screen",
    shortTitle: "Coastal denominator audit",
    href: "/showcase/coastal-population-denominator",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "An informal coastal risk proxy drops log population to test whether the hook is settlement exposure or country size.",
    evidencePath: "coastal-informal-risk/generated/coastal-drop-population-deepening.json",
    visual: "Headline rank versus no-population rank bridge",
    sourceNote: "WDI urbanization, population, and slum-share fields from the committed coastal panel",
    audit: {
      kind: "rank-shift",
      programSlug: "coastal-informal-risk",
      dataUrl: "/programs/coastal-informal-risk/generated/coastal-drop-population-deepening.json",
      csvUrl: "/programs/coastal-informal-risk/generated/coastal-drop-population-deepening.csv",
      question: "Who remains high once the coastal-informal proxy stops rewarding country population size?",
      finding: "Tuvalu enters the no-population top five and Bangladesh drops out.",
      method: "Recompute the committed index, remove the log-population term, and compare the top sets.",
      readerPayoff: "A small-island signal appears only after the size term is made visible and removable.",
      nonClaim: "This is not a storm-surge exposure result and does not map informal settlements inside inundation zones.",
      downloadLabel: "Download coastal denominator JSON",
    },
  },
  {
    id: 13,
    title: "When a Flood Access Index Measures Event Counts",
    shortTitle: "Flood access decomposition",
    href: "/showcase/flood-component-decomposition",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The flood-market-access proxy is decomposed to show whether it captures rural market access or raw disaster reporting and population size.",
    evidencePath: "flood-market-access/generated/flood-decompose-deepening.json",
    visual: "Index decomposition and per-capita rank flip",
    sourceNote: "Committed flood panel, EM-DAT qualifying-event counts, WDI population, and rural-share terms",
    audit: {
      kind: "rank-shift",
      programSlug: "flood-market-access",
      dataUrl: "/programs/flood-market-access/generated/flood-decompose-deepening.json",
      csvUrl: "/programs/flood-market-access/generated/flood-decompose-deepening.csv",
      question: "Is the flood-market-access proxy a market-access signal or mostly a size-and-reporting signal?",
      finding: "The per-capita version replaces the committed top four completely.",
      method: "Reproduce the index, remove size terms, compute a per-capita alternative, and compare rank correlation.",
      readerPayoff: "The chart makes the index confess what it is actually measuring before a policy story is told.",
      nonClaim: "This contains no roads, travel time, market locations, or modeled flood footprint.",
      downloadLabel: "Download flood decomposition JSON",
    },
  },
  {
    id: 14,
    title: "When Heat Workday Loss Collapses to Labor Share",
    shortTitle: "Climate-health sensitivity repair",
    href: "/showcase/climate-health-measurement-repair",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "A PM2.5 cap saturation check asks whether the pressure index still measures air pollution or mostly outdoor-labor exposure.",
    evidencePath: "climate-health-workdays/generated/climate-health-workdays-deepening.json",
    visual: "Cap-sensitivity lanes and labor-share comparison",
    sourceNote: "WHO PM2.5 exposure, WDI sector employment context, and committed sensitivity parameters",
    audit: {
      kind: "sensitivity-lanes",
      programSlug: "climate-health-workdays",
      dataUrl: "/programs/climate-health-workdays/generated/climate-health-workdays-deepening.json",
      question: "When the PM2.5 cap saturates, does the index become a labor-share ranking?",
      finding: "At the tighter cap, 12 rankable DMCs saturate and the rank correlation with outdoor labor share rises.",
      method: "Recompute the pressure index under the baseline and tighter PM2.5 cap, then compare with outdoor-labor-share rank.",
      readerPayoff: "The repair narrows the story from heat-health burden to a measurement question about the cap.",
      nonClaim: "This is not a causal estimate of lost workdays and does not observe worker-level heat exposure.",
      downloadLabel: "Download climate-health audit JSON",
    },
  },
  {
    id: 15,
    title: "When Vulnerability Is a Coverage Intersection",
    shortTitle: "Food price coverage trap",
    href: "/showcase/food-price-coverage-trap",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The CPI and agricultural-imports screen is audited for dropped economies, fill attempts, and common-vintage instability.",
    evidencePath: "food-price-climate-transmission/generated/food-price-coverage-deepening.json",
    visual: "Indicator coverage funnel and common-vintage top sets",
    sourceNote: "World Bank WDI CPI and agricultural-imports indicators with cache version metadata",
    audit: {
      kind: "coverage-funnel",
      programSlug: "food-price-climate-transmission",
      dataUrl: "/programs/food-price-climate-transmission/generated/food-price-coverage-deepening.json",
      csvUrl: "/programs/food-price-climate-transmission/generated/food-price-coverage-deepening.csv",
      question: "Is the food-price screen identifying vulnerability or the countries that have both public indicators?",
      finding: "The joint universe is smaller than the roster, and common-vintage top sets change by year.",
      method: "Audit coverage for both indicator legs, fill where allowed, and rerun common-vintage intersections.",
      readerPayoff: "The visualization lets missing data sit in the foreground instead of behind a confident top list.",
      nonClaim: "This is not a food-security ranking and does not model household price exposure.",
      downloadLabel: "Download food-price coverage JSON",
    },
  },
  {
    id: 16,
    title: "When Missing a Data Leg Removes the Runner-Up",
    shortTitle: "Social-protection dropped leg",
    href: "/showcase/social-protection-dropped-leg",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "Shock-payment readiness is re-ranked before excluding one-legged observations, exposing economies omitted only because one public indicator is missing.",
    evidencePath: "social-protection-shock-coverage/generated/social-protection-dropped-leg.json",
    visual: "Value rank ledger with missing-leg flags",
    sourceNote: "WDI poverty, ASPIRE social-protection coverage, and Findex account-use legs",
    audit: {
      kind: "rank-shift",
      programSlug: "social-protection-shock-coverage",
      dataUrl: "/programs/social-protection-shock-coverage/generated/social-protection-dropped-leg.json",
      csvUrl: "/programs/social-protection-shock-coverage/generated/social-protection-dropped-leg.csv",
      question: "Which economies would outrank the published headline set if missing one public-data leg did not exclude them?",
      finding: "Two omitted economies outrank the lowest headline member purely because one leg is missing.",
      method: "Rank all economies with at least one leg, flag one-legged cases, then compare to the named headline five.",
      readerPayoff: "The page turns missingness into an observed policy-relevant fact rather than a quiet deletion.",
      nonClaim: "This does not certify shock-payment readiness and does not impute beneficiary-level reach.",
      downloadLabel: "Download social-protection audit JSON",
    },
  },
  {
    id: 17,
    title: "When Water Stress Exceeds 100 Percent",
    shortTitle: "Water denominator artifact",
    href: "/showcase/water-stress-denominator",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The water-crop pressure screen tests whether internal-renewable-water denominators and rural-population multipliers are driving the headline.",
    evidencePath: "water-stress-crop-diversification/generated/water-stress-denominator-deepening.json",
    visual: "Saturated denominator cards and rural counterfactual",
    sourceNote: "WDI water withdrawal, internal renewable water, rural population, and yield-proxy fields",
    audit: {
      kind: "component-audit",
      programSlug: "water-stress-crop-diversification",
      dataUrl: "/programs/water-stress-crop-diversification/generated/water-stress-denominator-deepening.json",
      csvUrl: "/programs/water-stress-crop-diversification/generated/water-stress-denominator-deepening.csv",
      question: "Is the water-crop-pressure top set a water-stress result or a denominator and rural-population artifact?",
      finding: "Four economies exceed 100 percent on the internal-water denominator, while Afghanistan's headline position depends on the rural multiplier.",
      method: "Reproduce the index, inspect saturated water terms, then drop or flatten the rural-population multiplier.",
      readerPayoff: "A dramatic water number becomes a teachable denominator warning.",
      nonClaim: "This is not a crop-diversity analysis and does not use FAOSTAT crop-area or total renewable-water denominators.",
      downloadLabel: "Download water denominator JSON",
    },
  },
  {
    id: 18,
    title: "When Robustness Is Just Multiplication",
    shortTitle: "Invisible urbanization tautology",
    href: "/showcase/invisible-urban-tautology",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The claimed sensitivity sweep is tested as a scalar multiplier, then compared with a real input perturbation.",
    evidencePath: "invisible-urbanization/generated/invisible-urbanization-tautology.json",
    visual: "Rank-preserving multiplier sweep and break-boundary audit",
    sourceNote: "WDI rural share, urban population growth, and committed proxy formula",
    audit: {
      kind: "tautology-audit",
      programSlug: "invisible-urbanization",
      dataUrl: "/programs/invisible-urbanization/generated/invisible-urbanization-tautology.json",
      csvUrl: "/programs/invisible-urbanization/generated/invisible-urbanization-tautology.csv",
      question: "Does the sensitivity sweep test robustness, or does it multiply every row by the same positive scalar?",
      finding: "The 5/10/15 sweep preserves ranks exactly, while a genuine input perturbation can break the top-five boundary.",
      method: "Reproduce the committed proxy, test the scalar sweep, then run a non-uniform input-perturbation falsification.",
      readerPayoff: "The visual makes a comforting robustness check visibly empty.",
      nonClaim: "This does not use satellite built-up area or detect invisible urbanization on the ground.",
      downloadLabel: "Download tautology audit JSON",
    },
  },
  {
    id: 19,
    title: "When a Sensitivity Knob Never Touches the Model",
    shortTitle: "Port hinterland inert parameter",
    href: "/showcase/port-inert-parameter",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The import-cap parameter is audited to see whether any observed DMC ever reaches the cap the robustness test perturbs.",
    evidencePath: "port-hinterland-friction/generated/port-hinterland-inert-parameter.json",
    visual: "Cap binding gauge and top-five invariance lanes",
    sourceNote: "Comtrade/WDI-style import proxy terms from the committed port-hinterland panel",
    audit: {
      kind: "parameter-audit",
      programSlug: "port-hinterland-friction",
      dataUrl: "/programs/port-hinterland-friction/generated/port-hinterland-inert-parameter.json",
      question: "Can a perturbed import cap prove robustness if no observed economy reaches the cap?",
      finding: "At the baseline cap, zero DMCs bind, so the cap perturbation is largely inert.",
      method: "Compare observed import proxy values with the baseline cap and rerun the top five under cap perturbations.",
      readerPayoff: "The page shows the knob detached from the data before anyone claims sensitivity evidence.",
      nonClaim: "This is not a port-performance ranking and does not measure actual hinterland travel time.",
      downloadLabel: "Download port parameter JSON",
    },
  },
  {
    id: 20,
    title: "When Every Perturbation Includes an All-Zero Tie",
    shortTitle: "School heat top-one audit",
    href: "/showcase/school-heat-sensitivity",
    status: "verified",
    statusLabel: "Evidence audit",
    deck: "The school-heat sensitivity file is reread run by run, stripping degenerate and rank-losing cases before keeping the Cambodia top-one claim narrow.",
    evidencePath: "school-heat-disruption/generated/school-heat-sensitivity-audit.json",
    visual: "Sensitivity run ledger with discriminating and failing runs",
    sourceNote: "Committed school-heat sensitivity runs with explicit degenerate and rank-losing labels",
    audit: {
      kind: "sensitivity-lanes",
      programSlug: "school-heat-disruption",
      dataUrl: "/programs/school-heat-disruption/generated/school-heat-sensitivity-audit.json",
      question: "Which sensitivity runs actually discriminate after all-zero ties and rank-losing cases are stripped?",
      finding: "Cambodia is top one in five discriminating runs, but the original every-perturbation language is false.",
      method: "Reread every sensitivity run, classify degenerate and rank-losing cases, and restate only the surviving claim.",
      readerPayoff: "The audit keeps the strong hook by making the claim smaller and more honest.",
      nonClaim: "This is not a classroom heat-exposure measurement and does not observe school calendars or indoor temperatures.",
      downloadLabel: "Download school-heat audit JSON",
    },
  },
];

export const verifiedShowcaseReports = showcaseReports.filter(
  (report) => report.status === "verified",
);

export const showcaseAuditReports = showcaseReports.filter(
  (report): report is ShowcaseReport & { audit: ShowcaseAudit } => Boolean(report.audit),
);

export const showcaseReportDepth: Record<number, ShowcaseReportDepth> = {
  1: {
    operationalUse: "Screen market-months where local climate checks should precede national food-price interpretation.",
    falsifier: "If spikes stay synchronized after local rainfall, commodity, import, exchange-rate, and fuel checks, the local-weather hook weakens.",
    limitation: "One rice series, uneven WFP market coverage, and modeled NASA POWER point climate cannot establish causality.",
  },
  2: {
    operationalUse: "Help statisticians and operations teams see which dashboard indicators are too stale for current comparison.",
    falsifier: "If lag patterns disappear after indicator-specific update schedules are applied, the freshness concern is overstated.",
    limitation: "Freshness is not statistical-agency performance; indicators have different revision calendars and reporting duties.",
  },
  3: {
    operationalUse: "Separate account ownership from active digital-payment and social-protection rails before shock-transfer planning.",
    falsifier: "If verified shock-payment channel data show high delivery through the same populations, the proxy gap narrows.",
    limitation: "Findex and ASPIRE are public proxies with vintage mismatch; they do not observe emergency transfers arriving.",
  },
  4: {
    operationalUse: "Target registry, map, and building-footprint validation where service-access analysis depends on facility visibility.",
    falsifier: "If facility-level audits show registry and OSM differences are mostly duplicate naming or harmless classification, the gap weakens.",
    limitation: "Source disagreement is not a service-quality or travel-time result and does not prove facilities are absent.",
  },
  5: {
    operationalUse: "Help remittance teams decide when equal-weighted corridor prices hide exposure in high-flow corridors.",
    falsifier: "If corridor flow weights are too sparse, stale, or inconsistent with observed transactions, the flow-weighted comparison cannot lead.",
    limitation: "Bilateral flows are estimates and do not observe household remittance transactions or informal channels.",
  },
  6: {
    operationalUse: "Prioritize where OpenAQ station-coordinate checks, source-level method review, station-level monitor-grade classification, and regulator-inventory checks should accompany satellite or modeled PM2.5 use.",
    falsifier: "If regulatory inventories or local station lists fill the apparent zero-monitor gaps, the public-source gap shrinks.",
    limitation: "Ground-monitor visibility is not pollution ranking, compliance assessment, or monitor siting adequacy; the reconciliation audit has candidate rows but zero validated joins, and source-validation still leaves complete monitor-grade classification plus catchment coverage at zero.",
  },
  7: {
    operationalUse: "Flag geographies where OSM health amenities are too incomplete to support access or catchment planning.",
    falsifier: "If official registry joins do not change local facility-load ranks, the map-completeness concern is weaker.",
    limitation: "OSM completeness is not actual service availability, capacity, quality, or travel-time access.",
  },
  8: {
    operationalUse: "Prevent recovery-lag narratives from reusing a disaster burden pair that fails under alternate metrics.",
    falsifier: "If a true event-level recovery-lag metric restores the same priority pair, the metric-falsification warning narrows.",
    limitation: "EM-DAT burden screens do not measure recovery speed, reconstruction, household loss, or service restoration.",
  },
  9: {
    operationalUse: "Show energy teams when capacity-based fuel concentration should be checked against actual generation coverage.",
    falsifier: "If outage, reserve-margin, or heat-stress data do not align with fuel concentration, reliability language should be removed.",
    limitation: "Fuel-Herfindahl values are triage metrics and do not observe outages, dispatch constraints, or grid resilience.",
  },
  10: {
    operationalUse: "Help migration analysts choose whether absolute stock or population-share exposure is the policy denominator.",
    falsifier: "If corridor composition or remittance/refugee splits point to a different exposure unit, the share ranking should not lead.",
    limitation: "Emigrant stock shares are not welfare, fragility, or migration-quality measures.",
  },
  11: {
    operationalUse: "Keep night-light poverty work from overclaiming before the blind MPI dimensions are visible.",
    falsifier: "If an owner-led VIIRS join predicts health and education deprivation independently, the blind-spot warning can be narrowed.",
    limitation: "The page computes MPI-side decomposition only; it does not run a night-light model.",
  },
  12: {
    operationalUse: "Distinguish small-economy coastal informal-settlement questions from country-size-driven proxy rankings.",
    falsifier: "If GHSL, DEM, and surge-footprint overlays do not confirm no-population entrants, the proxy should be downgraded.",
    limitation: "The screen does not locate informal settlements inside coastal hazard zones.",
  },
  13: {
    operationalUse: "Stop flood-market-access claims when the proxy is mostly event counts and population size.",
    falsifier: "If road-network flood isolation produces the same priority set, the access claim gains support.",
    limitation: "The current artifact contains no road network, market point, travel time, or flood footprint.",
  },
  14: {
    operationalUse: "Help health and labor teams see when a cap choice turns a pollution-pressure proxy into a labor-share proxy.",
    falsifier: "If labor-force denominators and heat-exposure data keep the same ranking after cap changes, the repair is less material.",
    limitation: "The index is not a causal lost-workday estimate and does not observe worker heat exposure.",
  },
  15: {
    operationalUse: "Show food-price analysts whether the vulnerability screen is driven by countries with both public indicators.",
    falsifier: "If household or market price data keep the same high-risk group after missing-data repair, the coverage warning narrows.",
    limitation: "The joint CPI/imports screen is not a food-security or household-exposure ranking.",
  },
  16: {
    operationalUse: "Make missing social-protection or payment legs visible before excluding economies from shock-readiness screens.",
    falsifier: "If payment-channel and beneficiary data validate the headline five after one-leg repair, the missingness concern weakens.",
    limitation: "The public legs do not certify emergency payment delivery, identity readiness, or beneficiary reach.",
  },
  17: {
    operationalUse: "Warn water and agriculture teams when internal-water denominators create above-100-percent stress artifacts.",
    falsifier: "If total renewable water and crop-area denominators preserve the same priority set, the denominator warning narrows.",
    limitation: "The current proxy is not crop diversification and omits basin, crop-area, and transboundary water detail.",
  },
  18: {
    operationalUse: "Prevent scalar sensitivity sweeps from being treated as robustness evidence for urbanization proxies.",
    falsifier: "If a satellite built-up layer and classification history confirm the same top set, the topic can be rebuilt.",
    limitation: "The artifact uses WDI rural share and urban growth only; it does not observe invisible urban expansion.",
  },
  19: {
    operationalUse: "Show transport teams when a sensitivity parameter is inert because observed import proxies never reach the cap.",
    falsifier: "If actual hinterland travel-time or logistics data change under the parameter, the sensitivity test becomes meaningful.",
    limitation: "The proxy is not port performance, hinterland friction, or logistics reliability by itself.",
  },
  20: {
    operationalUse: "Keep the school-heat claim to the runs that discriminate after all-zero and rank-losing cases are removed.",
    falsifier: "If school geocodes, calendars, and enrollment denominators change the top-one result, the national proxy should be replaced.",
    limitation: "The artifact does not observe classrooms, indoor temperatures, school calendars, or enrolled pupils exposed to heat.",
  },
};

export const showcaseReportQuality: Record<number, ShowcaseReportQuality> = {
  1: {
    readiness: "prototype",
    readinessLabel: "L2 prototype",
    qaSummary: "Public sprint artifact, interactive heatmap, caveats, screenshots, and build/gates are in place.",
    publicationGap: "Needs commodity expansion, alternative rainfall source, and non-climate price falsifiers before a program claim.",
    nextUpgrade: "Convert the Nepal sprint into an L3 market-price package with commodity, import, fuel, and rainfall-source checks.",
  },
  2: {
    readiness: "prototype",
    readinessLabel: "L2 prototype",
    qaSummary: "WDI freshness matrix has a public API artifact, interactive matrix, caveats, screenshots, and build/gates.",
    publicationGap: "Needs indicator-specific refresh expectations and non-applicability rules before a statistical-capacity brief.",
    nextUpgrade: "Write the freshness inclusion protocol and rerun the matrix with source-specific refresh cadence labels.",
  },
  3: {
    readiness: "prototype",
    readinessLabel: "L2 prototype",
    qaSummary: "Shock-payment rails joins public disaster, payment-use, and social-protection proxies with a checked visual surface.",
    publicationGap: "Needs payment-channel metadata, ID/source vintage checks, and event-case validation before readiness language.",
    nextUpgrade: "Add a payment-channel source scan and rerun the sprint with vintage and emergency-transfer non-claim checks.",
  },
  4: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "BGD source-disagreement route reads formal L3 strata, a deterministic 20-upazila sample, an automated 76-row public-source coded screen, an AI review ledger, an 8-row candidate-resolution pass, a richer public-source tag scan, a 23-row coordinate-repair triage, a 40-row public-map-gap triage, a 40-row row-evidence ledger, a 40-row targeted public-map inspection packet, a 12-row first-source pass, a 40-row public-source confirmation pass, a 16-row public-source decision ledger, a 3-row possible same-facility review, a 9-row priority name-conflict review, a 6-row lower-priority name-conflict spot check, a 115-upazila zero-OSM observability review, a 4-row source-repair public-evidence attachment, a 4-row official-coordinate evidence pass, a 4-row public-explanation search, a 3-row correction-record follow-up, a 3-row no-contact clarification packet, a 3-row registry-vintage review, a 39-row human-gated handoff matrix, a 39-row blank human-validation worksheet, and a 39-row AI closure audit.",
    publicationGap: "Needs owner-only source-owner contact or human validation for possible same-facility candidates, priority and lower-priority name-conflict candidates, zero-OSM facility-row absence decisions, the Durgapur same-name cross-district coordinate conflict, and shared-coordinate Narayanganj records before stronger access-map use.",
    nextUpgrade: "Advance the next decision-ledger class only through public evidence, or stop at owner-only source-owner contact and human location validation when identity/location evidence is required.",
  },
  5: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "Flow-weighting L3 module and remittance program artifacts make this one of the strongest repair-to-publication candidates.",
    publicationGap: "Needs owner-led human-final validation and non-public transaction or central-bank validation before stronger public use.",
    nextUpgrade: "Validate corridor rows against central-bank or transaction sources where available; keep the L3 module as a sensitivity result until then.",
  },
  6: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "Air-monitoring has deepening artifacts, a metadata-readiness audit, an OpenAQ station-metadata source pass, regulator-source discovery, official station-source extraction, official/OpenAQ reconciliation audit, a 13-row candidate station-crosswalk review worksheet, public OpenAQ metadata evidence for those candidates, public source scans that screen the 6 OpenAQ isMonitor rows and the 7 not-isMonitor public-feed rows as not join-ready, a 169-item one-signal review queue, monitor-grade evidence audit, a 14-source monitor-grade source-validation scan, and a bespoke observability report with concentration, residual, exposure, gate, coordinate, source-wall, candidate-reconciliation, review-queue, public-evidence, source-scan, public-feed, one-signal, grade-evidence, and source-validation panels.",
    publicationGap: "Needs validated station crosswalk rows, station-level complete monitor-grade classification across sources, and gridded population/PM2.5 denominator validation before station-radius or catchment language.",
    nextUpgrade: "Turn source-level method/current-status clues into station-level classifications where public evidence permits, resolve remaining one-signal rows with source-owner crosswalk or method documentation, then add catchment denominators only if the source comparison survives.",
  },
  7: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "Access map-completeness has registry comparison artifacts and a strong source-audit visual surface.",
    publicationGap: "Needs additional official registry joins and a travel-time or catchment denominator before access language.",
    nextUpgrade: "Extend registry joins for the priority economies and add a public friction/travel-time validation plan.",
  },
  8: {
    readiness: "l3-candidate",
    readinessLabel: "L3 candidate",
    qaSummary: "Disaster metric-falsification has a bespoke route and clear kill-condition evidence across alternate burden metrics.",
    publicationGap: "Needs event-timestamped recovery curves and exposure denominators before any recovery-lag claim.",
    nextUpgrade: "Build a recovery-lag source plan and event-level recovery proxy before reusing the disaster hook as a report.",
  },
  9: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route compares capacity and generation concentration and keeps generation coverage visible.",
    publicationGap: "Needs outage, reserve-margin, dispatch, or heat-stress evidence before reliability framing.",
    nextUpgrade: "Search for public outage/reserve-margin proxies and decide whether the fuel-concentration result can graduate.",
  },
  10: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route shows the denominator switch from absolute emigrant stock to population-share exposure.",
    publicationGap: "Needs corridor composition, remittance/refugee split, and literature scan before a migration report.",
    nextUpgrade: "Build a corridor-type falsifier that separates labor, refugee, family, and remittance-relevant migration signals.",
  },
  11: {
    readiness: "owner-gated",
    readinessLabel: "Owner-gated",
    qaSummary: "MPI-side decomposition is public and checked, but the night-light join is explicitly owner-gated.",
    publicationGap: "Needs owner-led Earth Engine/VIIRS access and coauthor attestation before advancing beyond decomposition.",
    nextUpgrade: "Keep as a transparent methods note until owner-led NTL ingestion and coauthored review are cleared.",
  },
  12: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route exposes how dropping population changes the coastal informal-risk proxy.",
    publicationGap: "Needs settlement footprints, elevation, and surge-zone overlay before coastal exposure language.",
    nextUpgrade: "Choose a one-coast pilot and join GHSL or equivalent settlement data to a public coastal hazard layer.",
  },
  13: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route decomposes the flood-market-access proxy and shows the per-capita rank break.",
    publicationGap: "Needs roads, markets or services, flood footprint, and travel-time logic before access framing.",
    nextUpgrade: "Build a one-DMC flooded-network pilot or demote the proxy to a source-method caution note.",
  },
  14: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route shows cap saturation and labor-share drift in the climate-health workday proxy.",
    publicationGap: "Needs labor-force denominator repair and heat exposure evidence before workday-loss interpretation.",
    nextUpgrade: "Replace total-population exposure with labor-force denominators and document cap sensitivity as the lead chart.",
  },
  15: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route foregrounds indicator coverage and common-vintage instability in the food-price screen.",
    publicationGap: "Needs household or market price exposure evidence before vulnerability language.",
    nextUpgrade: "Join a market-price or household-expenditure source for one DMC and keep WDI coverage as the source audit.",
  },
  16: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route makes missing social-protection/payment legs visible before exclusion.",
    publicationGap: "Needs payment-channel or beneficiary delivery data before shock-readiness interpretation.",
    nextUpgrade: "Search public payment-channel metadata and rebuild the screen as coverage-versus-payment-rail observability.",
  },
  17: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route exposes internal-water denominator artifacts and the rural multiplier effect.",
    publicationGap: "Needs total-renewable-water, basin, and crop-area data before water-crop diversification framing.",
    nextUpgrade: "Rebuild the water screen around AQUASTAT/FAOSTAT or demote the current index to a denominator caution.",
  },
  18: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route shows the scalar robustness sweep is rank-preserving and not real sensitivity evidence.",
    publicationGap: "Needs satellite/built-up layer and classification history before invisible-urbanization framing.",
    nextUpgrade: "Select one pilot geography and replace the WDI-only proxy with GHSL or settlement-layer evidence.",
  },
  19: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route shows the import-cap sensitivity knob is largely inert in observed data.",
    publicationGap: "Needs actual hinterland travel-time, logistics, or port-performance source before friction language.",
    nextUpgrade: "Search for public port/hinterland travel-time proxies and decide whether the cap audit becomes a methods note.",
  },
  20: {
    readiness: "evidence-audit",
    readinessLabel: "Evidence audit",
    qaSummary: "Artifact route narrows school-heat sensitivity to discriminating runs and names degenerate/rank-losing cases.",
    publicationGap: "Needs school geocodes, calendars, enrollment, and local heat exposure before school-disruption claims.",
    nextUpgrade: "Pick a public school-location pilot or keep the current route as a sensitivity-audit caution.",
  },
};

export function getShowcaseReportDepth(report: ShowcaseReport) {
  return showcaseReportDepth[report.id];
}

export function getShowcaseReportQuality(report: ShowcaseReport) {
  return showcaseReportQuality[report.id];
}

export function findShowcaseReportBySlug(slug: string) {
  return showcaseReports.find((report) => report.href === `/showcase/${slug}`);
}
