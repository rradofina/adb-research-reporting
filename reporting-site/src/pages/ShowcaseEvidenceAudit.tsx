import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  findShowcaseReportBySlug,
  getShowcaseReportDepth,
  getShowcaseReportQuality,
  showcaseReports,
  type ShowcaseAuditKind,
  type ShowcaseReport,
} from "../data/showcaseReports";
import NotFound from "./NotFound";

type JsonValue = Record<string, any>;

interface Stat {
  value: string;
  label: string;
}

interface Fact {
  label: string;
  value: string;
}

interface SpineItem {
  label: string;
  title: string;
  body: string;
}

interface RankRow {
  key: string;
  label: string;
  sublabel?: string;
  leftText: string;
  rightText: string;
  leftValue?: string;
  rightValue?: string;
  note?: string;
  status: "survived" | "entered" | "dropped" | "flag";
  intensity: number;
}

interface StackRow {
  key: string;
  label: string;
  blind: number;
  visible: number;
  note: string;
}

interface FunnelRow {
  label: string;
  value: number;
  total: number;
  note: string;
}

interface CoverageYear {
  year: string;
  nBoth: number;
  top5: string[];
  top8: string[];
}

interface LaneRow {
  key: string;
  label: string;
  left: string;
  middle: string;
  right: string;
  note: string;
  status: "survived" | "entered" | "dropped" | "flag";
}

interface ParameterRow {
  key: string;
  label: string;
  value: string;
  note: string;
  status: "survived" | "flag";
}

interface ComponentCard {
  key: string;
  value: string;
  label: string;
  note: string;
  status: "survived" | "flag" | "dropped";
}

interface AuditModel {
  kind: ShowcaseAuditKind;
  stats: Stat[];
  chartTitle: string;
  chartDeck: string;
  leftLabel?: string;
  rightLabel?: string;
  rows?: RankRow[];
  stackRows?: StackRow[];
  funnelRows?: FunnelRow[];
  coverageYears?: CoverageYear[];
  laneRows?: LaneRow[];
  parameterRows?: ParameterRow[];
  componentCards?: ComponentCard[];
  readouts: Fact[];
  sourceFacts: Fact[];
  caveats: string[];
  generatedAt?: string;
}

function numberValue(value: unknown): number {
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatNumber(value: unknown, digits = 0): string {
  const parsed = numberValue(value);
  return parsed.toLocaleString("en-US", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function formatFlexible(value: unknown, digits = 2): string {
  const parsed = numberValue(value);
  if (Math.abs(parsed) >= 100) return formatNumber(parsed, 0);
  if (Math.abs(parsed) >= 10) return formatNumber(parsed, 1);
  return formatNumber(parsed, digits);
}

function formatPct(value: unknown, digits = 1): string {
  return `${formatNumber(value, digits)}%`;
}

function strings(value: unknown): string[] {
  return Array.isArray(value) ? value.map((item) => String(item)) : [];
}

function safeRows(value: unknown): JsonValue[] {
  return Array.isArray(value) ? (value as JsonValue[]) : [];
}

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

function rankText(list: string[], iso: string, suffix: string) {
  const index = list.indexOf(iso);
  return index >= 0 ? `#${index + 1} ${suffix}` : "outside top set";
}

function rowByIso(rows: JsonValue[]) {
  return new Map(rows.map((row) => [String(row.iso3), row]));
}

function statusFromSets(left: boolean, right: boolean): RankRow["status"] {
  if (left && right) return "survived";
  if (!left && right) return "entered";
  if (left && !right) return "dropped";
  return "flag";
}

function sourceFacts(report: ShowcaseReport, data: JsonValue): Fact[] {
  const facts: Fact[] = [
    { label: "Evidence path", value: report.evidencePath },
    { label: "Source stack", value: report.sourceNote },
  ];
  if (report.audit?.csvUrl) {
    facts.push({ label: "CSV companion", value: report.audit.csvUrl });
  }
  if (data.attestation_chain) {
    facts.push({ label: "Attestation", value: String(data.attestation_chain) });
  }
  if (data.generated_at) {
    facts.push({ label: "Generated", value: String(data.generated_at) });
  }
  if (data.claim_scope) {
    facts.push({ label: "Claim scope", value: String(data.claim_scope) });
  }
  return facts;
}

function baseCaveats(report: ShowcaseReport, data: JsonValue) {
  const depth = getShowcaseReportDepth(report);
  const quality = getShowcaseReportQuality(report);
  const caveats = [
    report.audit?.nonClaim || "This report does not widen the claim beyond the evidence artifact.",
    depth.limitation,
    quality.publicationGap,
  ];
  if (data.claim_scope) caveats.push(String(data.claim_scope));
  return unique(caveats);
}

function buildGridModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const capacityTop = strings(data.capacity_top5);
  const generationTop = strings(data.generation_top5);
  const details = rowByIso(safeRows(data.rows_by_generation_herfindahl));
  const readiness = data.reliability_proxy_readiness || {};
  const readinessSummary = readiness.summary || {};
  const readinessRows = rowByIso(safeRows(readiness.country_rows));
  const indicatorRecords = safeRows(readiness.indicator_records);
  const highProxyRows = safeRows(readiness.high_generation_proxy_rows);
  const noAdbIndicatorCount = indicatorRecords.filter((row) => numberValue(row.adb_dmcs_with_latest) === 0).length;
  const overlap = capacityTop.filter((iso) => generationTop.includes(iso)).length;
  const rows = unique([...capacityTop, ...generationTop]).map((iso) => {
    const row = details.get(iso) || {};
    const proxyRow = readinessRows.get(iso) || {};
    const leftRank = capacityTop.indexOf(iso);
    const rightRank = generationTop.indexOf(iso);
    const intensity = leftRank >= 0 && rightRank >= 0 ? Math.abs(leftRank - rightRank) * 18 + 24 : 88;
    const proxyCount = numberValue(proxyRow.proxy_indicator_count);
    return {
      key: iso,
      label: iso,
      sublabel: row.country,
      leftText: rankText(capacityTop, iso, "capacity"),
      rightText: rankText(generationTop, iso, "generation"),
      leftValue: `H ${formatFlexible(row.herfindahl_capacity)}`,
      rightValue: `H ${formatFlexible(row.herfindahl_generation)}`,
      note: `${row.top_fuel_capacity || "capacity fuel"} to ${row.top_fuel_generation || "generation fuel"}${
        proxyCount ? `; ${proxyCount} public proxy fields` : ""
      }`,
      status: statusFromSets(capacityTop.includes(iso), generationTop.includes(iso)),
      intensity,
    };
  });
  const hasReadiness = Boolean(data.reliability_proxy_readiness);
  const sourceTrail = sourceFacts(report, data);
  if (readiness.retrieved_at) {
    sourceTrail.push({ label: "Reliability proxy retrieval", value: String(readiness.retrieved_at) });
  }
  if (readiness.world_bank_api_base) {
    sourceTrail.push({ label: "Proxy API base", value: String(readiness.world_bank_api_base) });
  }

  return {
    kind: report.audit!.kind,
    stats: hasReadiness ? [
      { value: formatNumber(readinessSummary.dmcs_with_any_reliability_proxy), label: "DMCs with public proxy" },
      { value: formatNumber(readinessSummary.dmcs_with_generation_and_any_proxy), label: "generation + proxy rows" },
      { value: formatNumber(readinessSummary.high_generation_concentration_and_proxy_rows), label: "high-concentration proxy rows" },
      { value: String(readinessSummary.proxy_latest_year_span || "mixed"), label: "proxy vintage span" },
    ] : [
      { value: `${overlap}/5`, label: "top-five overlap" },
      { value: formatNumber(strings(data.rows_withheld_low_coverage).length), label: "low-coverage rows withheld" },
      { value: formatNumber(safeRows(data.rows_by_generation_herfindahl).length), label: "generation-ranked rows" },
    ],
    chartTitle: hasReadiness
      ? "The fuel bridge now has a second wall: public reliability proxy coverage."
      : "Capacity rank is not enough. Generation coverage has to be visible.",
    chartDeck: hasReadiness
      ? "The bridge still compares capacity and generation concentration, while the cards show whether public outage or electricity-service proxies exist before any reliability claim is made."
      : "The bridge compares the top fuel concentration screen using installed capacity and using reported or modeled generation.",
    leftLabel: "Capacity screen",
    rightLabel: "Generation screen",
    rows,
    componentCards: hasReadiness ? [
      {
        key: "proxy-coverage",
        value: `${formatNumber(readinessSummary.dmcs_with_any_reliability_proxy)}/${formatNumber(readinessSummary.adb_dmc_roster_n)}`,
        label: "Public proxy present",
        note: "At least one firm-outage, Doing Business, Enterprise Survey legacy, or B-READY electricity-service proxy exists.",
        status: "survived",
      },
      {
        key: "generation-proxy",
        value: formatNumber(readinessSummary.dmcs_with_generation_and_any_proxy),
        label: "Both layers ready",
        note: "Rows with WRI generation concentration and at least one public reliability proxy.",
        status: "survived",
      },
      {
        key: "high-generation-proxy",
        value: formatNumber(readinessSummary.high_generation_concentration_and_proxy_rows),
        label: "High H plus proxy",
        note: `Generation Herfindahl at or above ${formatFlexible(readinessSummary.high_generation_herfindahl_threshold, 1)} with at least one proxy field.`,
        status: "flag",
      },
      {
        key: "negative-source-result",
        value: formatNumber(noAdbIndicatorCount),
        label: "Queried indicators with zero ADB rows",
        note: "Cataloged outage-count or outage-duration endpoints were kept in the audit even when they returned no usable ADB-DMC observations.",
        status: "dropped",
      },
      {
        key: "bready",
        value: formatNumber(readinessSummary.dmcs_with_bready_utility_proxy),
        label: "B-READY utility rows",
        note: "Recent utility-service scores exist for a smaller 2024 country set and cannot replace outage records.",
        status: "flag",
      },
    ] : undefined,
    readouts: [
      { label: "Capacity top five", value: capacityTop.join(", ") },
      { label: "Generation top five", value: generationTop.join(", ") },
      { label: "Dropped on generation", value: strings(data.dropped_from_cluster_on_generation).join(", ") || "none" },
      { label: "Entered on generation", value: strings(data.entered_cluster_on_generation).join(", ") || "none" },
      ...(hasReadiness ? [
        { label: "Proxy indicators queried", value: formatNumber(readinessSummary.indicators_queried) },
        { label: "Indicators with ADB rows", value: formatNumber(readinessSummary.indicators_with_adb_proxy_rows) },
        { label: "High-concentration queue", value: highProxyRows.map((row) => row.iso3).join(", ") || "none" },
        { label: "Withheld generation but proxy present", value: formatNumber(readinessSummary.withheld_generation_but_proxy_rows) },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: baseCaveats(report, data).concat(hasReadiness ? [String(readiness.claim_scope || "")] : []),
    generatedAt: data.generated_at,
  };
}

function buildMigrationModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const absoluteTop = strings(data.absolute_top5);
  const shareTop = strings(data.share_top5);
  const details = rowByIso(safeRows(data.rows_by_share));
  const falsifier = data.corridor_type_falsifier || {};
  const falsifierSummary = falsifier.summary || {};
  const forcedRows = rowByIso(safeRows(falsifier.country_rows));
  const topForcedCorridor = safeRows(falsifier.top_forced_corridors)[0] || {};
  const hasFalsifier = Boolean(data.corridor_type_falsifier);
  const rows = unique([...absoluteTop, ...shareTop]).map((iso) => {
    const row = details.get(iso) || {};
    const forced = forcedRows.get(iso) || {};
    const diff = Math.abs(numberValue(row.rank_absolute) - numberValue(row.rank_share));
    const forcedPct = forced.forced_abroad_pct_of_emigrant_stock;
    return {
      key: iso,
      label: iso,
      sublabel: row.country,
      leftText: row.rank_absolute ? `#${row.rank_absolute} absolute` : rankText(absoluteTop, iso, "absolute"),
      rightText: row.rank_share ? `#${row.rank_share} share` : rankText(shareTop, iso, "share"),
      leftValue: row.emigrant_stock_2024 ? formatNumber(row.emigrant_stock_2024) : undefined,
      rightValue: row.emigrant_pct_of_population ? formatPct(row.emigrant_pct_of_population, 1) : undefined,
      note: row.population_total
        ? `population ${formatNumber(row.population_total)}${
          forcedPct !== undefined ? `; forced-displacement share ${formatPct(forcedPct, 1)}` : ""
        }`
        : undefined,
      status: statusFromSets(absoluteTop.includes(iso), shareTop.includes(iso)),
      intensity: Math.max(30, Math.min(100, diff * 4)),
    };
  });
  const sourceTrail = sourceFacts(report, data);
  if (falsifier.retrieved_at) {
    sourceTrail.push({ label: "UNHCR retrieval", value: String(falsifier.retrieved_at) });
  }
  if (falsifier.source?.docs) {
    sourceTrail.push({ label: "UNHCR API docs", value: String(falsifier.source.docs) });
  }

  return {
    kind: report.audit!.kind,
    stats: hasFalsifier ? [
      { value: `${safeRows(data.survivors_in_both_top5).length}/5`, label: "absolute top-five survivors" },
      { value: formatPct(falsifierSummary.afghanistan_forced_abroad_pct_of_emigrant_stock, 1), label: "AFG forced-displacement share" },
      { value: formatNumber(falsifierSummary.forced_displacement_majority_origins), label: "forced-majority origins" },
      { value: formatNumber(falsifierSummary.substantial_forced_displacement_component_origins), label: "substantial component rows" },
    ] : [
      { value: `${safeRows(data.survivors_in_both_top5).length}/5`, label: "absolute top-five survivors" },
      { value: formatPct(details.get(shareTop[0])?.emigrant_pct_of_population || 0, 1), label: `${shareTop[0]} emigrant share` },
      { value: formatNumber(safeRows(data.rows_by_share).length), label: "rankable origins" },
    ],
    chartTitle: hasFalsifier
      ? "The denominator switch reveals islands, then the UNHCR layer isolates Afghanistan."
      : "The denominator switch changes the story, not just the order.",
    chartDeck: hasFalsifier
      ? "The bridge shows how absolute stock becomes population-share exposure. The cards separate forced-displacement-majority stock from diaspora stock where public UNHCR data can see it."
      : "Absolute emigrant stock favors large origins; population share reveals small-economy exposure.",
    leftLabel: "Absolute stock",
    rightLabel: "Share of origin population",
    rows,
    componentCards: hasFalsifier ? [
      {
        key: "afg-exception",
        value: formatPct(falsifierSummary.afghanistan_forced_abroad_pct_of_emigrant_stock, 1),
        label: "AFG forced-displacement share",
        note: "UNHCR forced-displacement stock abroad as a share of Afghanistan's UN DESA emigrant stock.",
        status: "flag",
      },
      {
        key: "share-top-five",
        value: `${strings(falsifierSummary.share_top5_forced_displacement_majority).length}/5`,
        label: "Share top-five forced-majority",
        note: "The Samoa, Tonga, Armenia, Nauru, and Fiji share-top-five set is not forced-displacement-majority in UNHCR data.",
        status: "survived",
      },
      {
        key: "origins",
        value: formatNumber(falsifierSummary.origins_queried),
        label: "UNHCR origins queried",
        note: "One origin-asylum query per UN DESA origin in the migration panel.",
        status: "survived",
      },
      {
        key: "substantial",
        value: formatNumber(falsifierSummary.substantial_forced_displacement_component_origins),
        label: "Substantial forced component",
        note: "Origins where forced-displacement stock is at least 10% of UN DESA emigrant stock.",
        status: "flag",
      },
      {
        key: "top-corridor",
        value: `${topForcedCorridor.origin_iso3 || "?"}->${topForcedCorridor.asylum_iso3 || "?"}`,
        label: "Largest forced corridor",
        note: `${formatNumber(topForcedCorridor.forced_displacement_abroad)} people in the UNHCR 2024 forced-displacement fields.`,
        status: "flag",
      },
    ] : undefined,
    readouts: [
      { label: "Absolute top five", value: absoluteTop.join(", ") },
      { label: "Population-share top five", value: shareTop.join(", ") },
      { label: "Dropped from headline", value: strings(data.dropped_from_top5_on_share).join(", ") },
      { label: "Entered after denominator switch", value: strings(data.entered_top5_on_share).join(", ") },
      ...(hasFalsifier ? [
        { label: "Absolute top-five forced-majority", value: strings(falsifierSummary.absolute_top5_forced_displacement_majority).join(", ") || "none" },
        { label: "Share top-five forced-majority", value: strings(falsifierSummary.share_top5_forced_displacement_majority).join(", ") || "none" },
        { label: "AFG forced stock abroad", value: formatNumber(falsifierSummary.afghanistan_forced_abroad_2024) },
        { label: "Largest forced corridor", value: `${topForcedCorridor.origin_iso3 || "?"}->${topForcedCorridor.asylum_iso3 || "?"} (${formatNumber(topForcedCorridor.forced_displacement_abroad)})` },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: baseCaveats(report, data).concat(hasFalsifier ? [String(falsifier.claim_scope || "")] : []),
    generatedAt: data.generated_at,
  };
}

function buildMpiModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const sourceAudit = data.ntl_source_readiness || {};
  const sourceSummary = sourceAudit.summary || {};
  const hasSourceAudit = Boolean(data.ntl_source_readiness);
  const sourceTrail = sourceFacts(report, data);
  if (sourceAudit.retrieved_at) {
    sourceTrail.push({ label: "CMR retrieval", value: String(sourceAudit.retrieved_at) });
  }
  if (sourceSummary.current_collection_ids) {
    sourceTrail.push({ label: "Black Marble current IDs", value: Object.entries(sourceSummary.current_collection_ids).map(([key, value]) => `${key} ${value}`).join("; ") });
  }
  const rows = safeRows(data.rows_by_ntl_blind_dimension)
    .slice(0, 10)
    .map((row) => ({
      key: String(row.iso3),
      label: `${row.iso3} ${row.country}`,
      blind: numberValue(row.ntl_blind_dim_pct),
      visible: numberValue(row.ntl_visible_dim_pct),
      note: `${row.survey || "survey"} ${row.survey_year || ""}; MPI ${formatFlexible(row.mpi_value, 4)}`,
    }));

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatNumber(data.n_adb_economies), label: "ADB economies scoped" },
      { value: formatPct(data.mean_ntl_blind_dim_pct, 1), label: "mean dimension share blind to NTL" },
      hasSourceAudit
        ? { value: formatNumber(sourceSummary.current_collection_candidates), label: "current Black Marble collections" }
        : { value: formatNumber(safeRows(data.majority_ntl_blind_both_readings).length), label: "majority-blind in both readings" },
    ],
    chartTitle: hasSourceAudit
      ? "The MPI blind spot is visible before the raster join."
      : "The satellite can illuminate places, but not all poverty dimensions.",
    chartDeck: hasSourceAudit
      ? "Bars show what nighttime radiance cannot see inside MPI; cards show that public Black Marble metadata exists while the analysis-ready join is still absent."
      : "Each bar decomposes MPI weight into dimensions structurally blind or plausibly visible to nighttime radiance.",
    stackRows: rows,
    componentCards: hasSourceAudit ? [
      {
        key: "collections",
        value: formatNumber(sourceSummary.current_collection_candidates),
        label: "Current Black Marble collections",
        note: Object.entries(sourceSummary.current_collection_ids || {}).map(([key, value]) => `${key}: ${value}`).join("; "),
        status: "survived",
      },
      {
        key: "start-date",
        value: String(sourceSummary.earliest_current_collection_start || "").slice(0, 10),
        label: "Current collection start",
        note: "Earliest time_start among the current v2 VNP46A3/VNP46A4 CMR collection rows.",
        status: "survived",
      },
      {
        key: "sample-links",
        value: `${formatNumber(sourceSummary.sample_granules_with_https_data_links)}/${formatNumber(sourceSummary.sample_granules_checked)}`,
        label: "Samples with HTTPS data links",
        note: "Latest sample granule metadata was checked for each current collection; no raster was downloaded.",
        status: "survived",
      },
      {
        key: "analysis-ready",
        value: sourceSummary.analysis_ready_raster_join ? "ready" : "not joined",
        label: "Analysis-ready raster join",
        note: "No authenticated pull, zonal statistic, population weighting, subnational MPI crosswalk, or flare mask is committed here.",
        status: "flag",
      },
    ] : undefined,
    readouts: [
      { label: "Median blind dimension share", value: formatPct(data.median_ntl_blind_dim_pct, 1) },
      { label: "Mean blind indicator share", value: formatPct(data.mean_ntl_blind_ind_pct, 1) },
      { label: "Residual check", value: data.decomposition_residual_check?.rule || "dimension shares checked" },
      { label: "NTL data wall", value: String(data.ntl_data_wall || "Owner-gated VIIRS join not computed here.") },
      ...(hasSourceAudit ? [
        { label: "Latest monthly sample", value: String(sourceSummary.latest_sample_granule_start?.VNP46A3 || "") },
        { label: "Latest yearly sample", value: String(sourceSummary.latest_sample_granule_start?.VNP46A4 || "") },
        { label: "Owner-gated next step", value: strings(sourceSummary.owner_gated_or_unfinished_steps).join(" ") },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: baseCaveats(report, data).concat(String(data.co_authorship || ""), hasSourceAudit ? String(sourceAudit.claim_scope || "") : ""),
    generatedAt: data.generated_at,
  };
}

function buildCoastalModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const headlineTop = strings(data.headline_top5);
  const noPopTop = strings(data.nopop_top5);
  const readiness = data.coastal_source_readiness || {};
  const readinessSummary = readiness.summary || {};
  const hasReadiness = Boolean(readinessSummary.spatial_source_layers_checked);
  const rows = safeRows(data.rows)
    .slice(0, 8)
    .map((row) => ({
      key: String(row.iso3),
      label: String(row.iso3),
      sublabel: row.country,
      leftText: `#${row.rank_headline} headline`,
      rightText: `#${row.rank_nopop} no-pop`,
      leftValue: formatFlexible(row.headline_index),
      rightValue: formatFlexible(row.nopop_score),
      note: `${formatPct(row.urban_pct, 1)} urban; slum ${formatPct(row.slum_pct_used, 1)}${row.slum_imputed ? " imputed" : ""}`,
      status: statusFromSets(headlineTop.includes(String(row.iso3)), noPopTop.includes(String(row.iso3))),
      intensity: Math.max(22, Math.min(100, Math.abs(numberValue(row.rank_shift_headline_to_nopop)) * 18 + 20)),
    }));

  return {
    kind: report.audit!.kind,
    stats: [
      { value: strings(data.entered_top5_when_pop_removed).join(", ") || "none", label: "entered without population" },
      { value: strings(data.dropped_from_top5_when_pop_removed).join(", ") || "none", label: "dropped without population" },
      { value: `${data.china_rank_headline}->${data.china_rank_nopop}`, label: "China rank shift" },
      ...(hasReadiness ? [
        { value: formatNumber(readinessSummary.wri_coastal_tif_links), label: "WRI coastal GeoTIFF links" },
      ] : []),
    ],
    chartTitle: "The small-island signal appears before the spatial overlay exists.",
    chartDeck: "The bridge keeps the population-scaled rank beside the no-population rank, while the source wall shows the settlement, elevation, and surge inputs are not yet joined.",
    leftLabel: "Population-scaled screen",
    rightLabel: "No-population screen",
    rows,
    componentCards: hasReadiness ? [
      {
        key: "ghsl",
        value: formatNumber(readinessSummary.ghsl_built_settlement_link_candidates),
        label: "GHSL built links",
        note: "GHS_BUILT_S metadata candidates are visible on the GHSL/JRC download page; no settlement raster tile is pulled.",
        status: "survived",
      },
      {
        key: "nasadem",
        value: String(readinessSummary.nasadem_concept_id || "missing"),
        label: "NASADEM concept",
        note: `${formatNumber(readinessSummary.nasadem_sample_https_data_links)} sample HTTPS data links in CMR; ${formatNumber(readinessSummary.nasadem_sample_protected_https_data_links)} are protected data links.`,
        status: "survived",
      },
      {
        key: "aqueduct",
        value: `${formatNumber(readinessSummary.wri_coastal_tif_links)}/${formatNumber(readinessSummary.wri_coastal_links)}`,
        label: "Aqueduct coastal files",
        note: "WRI Aqueduct Floods v2 inuncoast links are visible, but no return period or GeoTIFF is selected.",
        status: "survived",
      },
      {
        key: "overlay",
        value: readinessSummary.analysis_ready_overlay ? "ready" : "not joined",
        label: "Analysis-ready overlay",
        note: "No settlement, elevation, coastal hazard, population, or informality-mask raster intersection is computed.",
        status: "flag",
      },
    ] : undefined,
    readouts: [
      { label: "Headline top five", value: headlineTop.join(", ") },
      { label: "No-population top five", value: noPopTop.join(", ") },
      { label: "Formula check", value: `max error ${formatFlexible(data.formula_check?.max_abs_error_recomputed_vs_committed)}` },
      { label: "Sensitivity note", value: strings(data.sensitivity_check?.top5_members_perturbation_can_move).join(", ") || "no movement listed" },
      ...(hasReadiness ? [
        { label: "Spatial source layers checked", value: formatNumber(readinessSummary.spatial_source_layers_checked) },
        { label: "Return-period tokens visible", value: strings(readinessSummary.wri_coastal_return_period_tokens).join(", ") },
        { label: "Analysis-ready overlay", value: readinessSummary.analysis_ready_overlay ? "ready" : "not joined" },
        { label: "Unfinished spatial steps", value: strings(readinessSummary.owner_gated_or_unfinished_steps).join(" ") },
      ] : []),
    ],
    sourceFacts: sourceFacts(report, data).concat(hasReadiness ? [
      { label: "Spatial source audit", value: String(readiness.claim_scope || "") },
    ] : []),
    caveats: baseCaveats(report, data).concat(hasReadiness ? [
      String(readiness.claim_scope || ""),
      String(data.coastal_data_wall || ""),
    ] : []),
    generatedAt: data.generated_at,
  };
}

function buildFloodModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const rowsAll = safeRows(data.rows);
  const readiness = data.access_source_readiness || {};
  const sourceSummary = readiness.summary || {};
  const hasSourceWall = Boolean(readiness.summary);
  const committedRank = new Map(
    [...rowsAll]
      .sort((a, b) => numberValue(b.index_committed) - numberValue(a.index_committed))
      .map((row, index) => [String(row.iso3), index + 1]),
  );
  const perCapRank = new Map(
    [...rowsAll]
      .sort((a, b) => numberValue(b.index_per_capita_per_million) - numberValue(a.index_per_capita_per_million))
      .map((row, index) => [String(row.iso3), index + 1]),
  );
  const details = rowByIso(rowsAll);
  const committedTop = strings(data.a_headline?.top4_committed);
  const perCapTop = strings(data.b_strip_size_terms?.top4_per_capita_per_million);
  const rows = unique([...committedTop, ...perCapTop]).map((iso) => {
    const row = details.get(iso) || {};
    const leftRank = committedRank.get(iso) || 0;
    const rightRank = perCapRank.get(iso) || 0;
    return {
      key: iso,
      label: iso,
      sublabel: row.country,
      leftText: leftRank ? `#${leftRank} committed` : "outside committed rank",
      rightText: rightRank ? `#${rightRank} per-capita` : "outside per-capita rank",
      leftValue: formatFlexible(row.index_committed),
      rightValue: formatFlexible(row.index_per_capita_per_million, 3),
      note: `${formatNumber(row.flood_events_2000_2025)} flood events; rural ${formatPct(row.rural_pct, 1)}`,
      status: statusFromSets(committedTop.includes(iso), perCapTop.includes(iso)),
      intensity: Math.max(30, Math.min(100, Math.abs(leftRank - rightRank) * 4)),
    };
  });

  const sourceTrail = sourceFacts(report, data);
  if (readiness.retrieved_at) {
    sourceTrail.push({ label: "Access source-wall retrieval", value: String(readiness.retrieved_at) });
  }
  if (sourceSummary.road_extract_total_pbf_links_visible !== undefined) {
    sourceTrail.push({
      label: "Road-source visibility",
      value: `${formatNumber(sourceSummary.road_extract_total_pbf_links_visible)} Geofabrik .osm.pbf links; ${formatNumber(sourceSummary.road_extract_latest_pbf_links_visible)} latest`,
    });
  }
  if (sourceSummary.market_csv_size_mb !== undefined) {
    sourceTrail.push({
      label: "Market-source visibility",
      value: `HDX/WFP CSV ${formatFlexible(sourceSummary.market_csv_size_mb, 1)} MB; coordinate fields in sampled header: ${String(sourceSummary.market_coordinate_fields_visible_in_sample_header)}`,
    });
  }
  if (sourceSummary.gfd_earth_engine_dataset_id_visible !== undefined) {
    sourceTrail.push({
      label: "Flood-footprint catalog",
      value: `GFD dataset ID visible=${String(sourceSummary.gfd_earth_engine_dataset_id_visible)}; parsed events=${formatNumber(sourceSummary.gfd_earth_engine_event_count_parsed)}`,
    });
  }

  const caveats = baseCaveats(report, data);
  if (data.flood_data_wall) caveats.push(String(data.flood_data_wall));
  if (readiness.claim_scope) caveats.push(String(readiness.claim_scope));

  return {
    kind: report.audit!.kind,
    stats: hasSourceWall ? [
      { value: formatFlexible(data.b_strip_size_terms?.spearman_headline_vs_per_capita, 3), label: "Spearman vs per-capita rank" },
      { value: "0/4", label: "top-four survivors per capita" },
      { value: formatNumber(sourceSummary.road_extract_latest_pbf_links_visible), label: "latest road extracts visible" },
      { value: "0", label: "routed access joins computed" },
    ] : [
      { value: formatFlexible(data.b_strip_size_terms?.spearman_headline_vs_per_capita, 3), label: "Spearman vs per-capita rank" },
      { value: "0/4", label: "top-four survivors per capita" },
      { value: formatFlexible(data.what_the_index_correlates_with?.pearson_index_vs_raw_flood_count, 3), label: "correlation with raw flood count" },
    ],
    chartTitle: hasSourceWall
      ? "The country-rank bridge now sits beside an empty route object."
      : "Per-capita framing breaks the original flood-access top four.",
    chartDeck: hasSourceWall
      ? "The bridge shows the rank break; the cards show public road, market, population, and flood-footprint sources before any route is claimed."
      : "The audit contrasts the committed index with a per-capita-per-million version and exposes the event-count term.",
    leftLabel: "Committed proxy",
    rightLabel: "Per-capita alternative",
    rows,
    componentCards: hasSourceWall ? [
      {
        key: "road-extracts",
        value: formatNumber(sourceSummary.road_extract_latest_pbf_links_visible),
        label: "Latest OSM extracts visible",
        note: `${formatNumber(sourceSummary.road_extract_total_pbf_links_visible)} Geofabrik .osm.pbf links are visible, but no road graph or bridge-edge table is built.`,
        status: "flag",
      },
      {
        key: "market-csv",
        value: `${formatNumber(sourceSummary.market_csv_resources)} CSV`,
        label: "WFP market source visible",
        note: `The sampled HDX/WFP header has market and price fields; coordinate fields visible in sample=${String(sourceSummary.market_coordinate_fields_visible_in_sample_header)}.`,
        status: sourceSummary.market_coordinate_fields_visible_in_sample_header ? "flag" : "dropped",
      },
      {
        key: "worldpop",
        value: `${formatNumber(sourceSummary.worldpop_panel_iso_with_rows)}/${formatNumber(rowsAll.length)}`,
        label: "Flood-panel economies with WorldPop rows",
        note: `${formatNumber(sourceSummary.worldpop_panel_rows)} panel rows are visible through the catalog; no raster or population-weighted settlement layer is downloaded.`,
        status: "flag",
      },
      {
        key: "flood-footprint",
        value: formatNumber(sourceSummary.gfd_earth_engine_event_count_parsed),
        label: "GFD catalog events parsed",
        note: `Dataset ID visible=${String(sourceSummary.gfd_earth_engine_dataset_id_visible)} for 2000-2018, but no observed flood raster or road-edge overlay is exported.`,
        status: "flag",
      },
      {
        key: "access-join",
        value: "not joined",
        label: "Road-market-flood object",
        note: "No market geocoding, flooded-edge cut, routed travel time, or population-weighted access-loss estimate is computed.",
        status: "dropped",
      },
    ] : undefined,
    readouts: [
      { label: "Committed top four", value: committedTop.join(", ") },
      { label: "Per-capita top four", value: perCapTop.join(", ") },
      { label: "Dropped per capita", value: strings(data.b_strip_size_terms?.dropped_per_capita).join(", ") },
      ...(hasSourceWall ? [
        { label: "Access source layers checked", value: formatNumber(sourceSummary.access_source_layers_checked) },
        { label: "Analysis-ready network join", value: String(sourceSummary.analysis_ready_network_join) },
      ] : []),
      { label: "Index reading", value: data.what_the_index_correlates_with?.reading || "size-and-reporting audit" },
    ],
    sourceFacts: sourceTrail,
    caveats: unique(caveats),
    generatedAt: data.generated_at,
  };
}

function buildClimateHealthModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const cap = data.cap_saturation || {};
  const sourceAudit = data.labor_heat_source_readiness || {};
  const sourceSummary = sourceAudit.summary || {};
  const hasSourceAudit = Boolean(data.labor_heat_source_readiness);
  const top3Observed = safeRows(sourceAudit.top3_observed_denominator_rows);
  const top3ByIso = rowByIso(top3Observed);
  const india = top3ByIso.get("IND") || {};
  const afg = top3ByIso.get("AFG") || {};
  const rows = safeRows(cap.rows).slice(0, 9);
  const laneRows = rows.map((row) => ({
    key: String(row.iso3),
    label: `${row.iso3} ${row.country}`,
    left: `baseline #${row.rank_cap45}`,
    middle: `tight cap #${row.rank_cap22_5}`,
    right: `labor #${row.rank_labor}`,
    note: `PM2.5 ${formatFlexible(row.pm25_ugm3, 1)}; outdoor labor ${formatPct(row.outdoor_labor_share_pct, 1)}`,
    status: numberValue(row.pressure_cap22_5) >= 1 ? "flag" : "survived",
  })) as LaneRow[];
  const sourceTrail = sourceFacts(report, data);
  if (sourceAudit.retrieved_at) {
    sourceTrail.push({ label: "Source-audit retrieval", value: String(sourceAudit.retrieved_at) });
  }
  if (sourceAudit.sources?.wdi_indicators) {
    sourceTrail.push({ label: "Observed WDI denominator", value: strings(sourceAudit.sources.wdi_indicators).join(", ") });
  }
  if (sourceAudit.sources?.world_bank_cckp_api_base) {
    sourceTrail.push({ label: "CCKP tasmax API", value: String(sourceAudit.sources.world_bank_cckp_api_base) });
  }
  const componentCards = hasSourceAudit ? [
    {
      key: "wdi-denominator",
      value: `${formatNumber(sourceSummary.wdi_denominator_rows_joined)}/${formatNumber(sourceSummary.rankable_dmcs)}`,
      label: "Observed WDI denominator joined",
      note: "Employment-to-population 15+, total population, and ages 0-14 share derive employed 15+ persons before applying outdoor employment share.",
      status: "survived",
    },
    {
      key: "india-denominator",
      value: `${formatNumber(india.observed_exposed_outdoor_worker_millions, 2)}M`,
      label: "India observed outdoor workers",
      note: `The old total-population formula is ${formatNumber(india.published_exposed_outdoor_millions_x_total_pop, 1)}M, or ${formatFlexible(india.published_to_observed_worker_ratio, 2)}x the observed employed-15+ count.`,
      status: "flag",
    },
    {
      key: "afg-denominator",
      value: `${formatFlexible(afg.published_to_observed_worker_ratio, 2)}x`,
      label: "AFG total-population overstatement",
      note: `${formatNumber(afg.published_exposed_outdoor_millions_x_total_pop, 1)}M becomes ${formatNumber(afg.observed_exposed_outdoor_worker_millions, 2)}M after WDI 15+ employment and age-share denominators.`,
      status: "flag",
    },
    {
      key: "cckp-source",
      value: `${formatNumber(sourceSummary.cckp_baseline_and_future_rows)}/${formatNumber(sourceSummary.rankable_dmcs)}`,
      label: "CCKP tasmax rows visible",
      note: `National tasmax source rows parse for baseline and SSP2-4.5 future periods; delta range ${formatFlexible(sourceSummary.cckp_tasmax_delta_min_c, 2)}-${formatFlexible(sourceSummary.cckp_tasmax_delta_max_c, 2)} C.`,
      status: "survived",
    },
    {
      key: "worker-heat-join",
      value: "0",
      label: "Worker heat-loss joins",
      note: "No gridded heat/WBGT, worker locations, work-hour schedule, or observed lost-workday outcome is joined.",
      status: "dropped",
    },
  ] as ComponentCard[] : undefined;

  return {
    kind: report.audit!.kind,
    stats: hasSourceAudit ? [
      { value: formatNumber(cap.n_pressure_saturated_cap22_5), label: "saturated at tighter cap" },
      { value: `${formatNumber(sourceSummary.wdi_denominator_rows_joined)}/${formatNumber(sourceSummary.rankable_dmcs)}`, label: "observed WDI denominators" },
      { value: `${formatFlexible(sourceSummary.india_published_to_observed_worker_ratio, 2)}x`, label: "India total-pop overstatement" },
      { value: String(sourceSummary.analysis_ready_heat_workday_loss), label: "analysis-ready heat loss" },
    ] : [
      { value: formatNumber(cap.n_pressure_saturated_cap22_5), label: "saturated at tighter cap" },
      { value: formatFlexible(cap.spearman_index_cap22_5_vs_labor_share, 3), label: "rank correlation with labor share" },
      { value: formatNumber(cap.rankable_dmcs), label: "rankable DMCs" },
    ],
    chartTitle: hasSourceAudit
      ? "The cap problem now sits beside the denominator repair and the heat-source wall."
      : "Tighten the cap and the pressure index drifts toward labor share.",
    chartDeck: hasSourceAudit
      ? "Lanes show how rank moves as the PM2.5 cap tightens. Cards show the observed WDI worker denominator and which heat-workday joins still do not exist."
      : "Each lane shows the same economy under baseline PM2.5 cap, tighter cap, and outdoor-labor-share rank.",
    laneRows,
    componentCards,
    readouts: [
      { label: "Baseline versus tight-cap Spearman", value: formatFlexible(cap.spearman_index_cap45_vs_cap22_5, 3) },
      { label: "Baseline versus labor-share Spearman", value: formatFlexible(cap.spearman_index_cap45_vs_labor_share, 3) },
      {
        label: "Denominator wall",
        value: data.denominator_correction_observed?.wall_note || data.denominator_correction?.wall_note || "labor-force denominator correction documented in artifact",
      },
      { label: "Parameter pair", value: `baseline cap ${formatFlexible(data.params?.baseline_cap)}; tight cap ${formatFlexible(data.params?.saturating_cap)}` },
      ...(hasSourceAudit ? [
        { label: "WDI denominator vintages", value: `emp/pop ${sourceSummary.wdi_employment_to_population_latest_year_span}; population ${sourceSummary.wdi_population_latest_year_span}; ages 0-14 ${sourceSummary.wdi_pop_0_14_latest_year_span}` },
        { label: "Top-3 observed denominator joined", value: `${formatNumber(sourceSummary.top3_denominator_rows_joined)}/3` },
        { label: "India observed outdoor worker count", value: `${formatNumber(sourceSummary.india_observed_exposed_outdoor_worker_millions, 2)}M` },
        { label: "CCKP baseline/future rows", value: `${formatNumber(sourceSummary.cckp_baseline_tasmax_rows)}/${formatNumber(sourceSummary.cckp_future_tasmax_rows)}` },
        { label: "Worker heat-exposure join", value: sourceSummary.worker_heat_exposure_join_built ? "joined" : "not joined" },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: unique(baseCaveats(report, data).concat([
      data.climate_health_data_wall,
      sourceAudit.claim_scope,
      ...(sourceSummary.owner_gated_or_unfinished_steps || []),
    ].filter(Boolean).map(String))),
    generatedAt: data.generated_at,
  };
}

function buildFoodCoverageModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const sourceAudit = data.food_import_source_readiness || {};
  const sourceSummary = sourceAudit.summary || {};
  const hasSourceAudit = Boolean(data.food_import_source_readiness);
  const total = numberValue(data.roster_n);
  const yearSource = hasSourceAudit
    ? sourceAudit.common_vintage_runs_food_import_live_cpi || {}
    : data.common_vintage_runs || {};
  const years = Object.entries(yearSource)
    .sort(([a], [b]) => Number(b) - Number(a))
    .slice(0, hasSourceAudit ? 8 : 7)
    .map(([year, row]) => {
    const record = row as JsonValue;
    return {
      year,
      nBoth: numberValue(record.n_both),
      top5: strings(record.top5),
      top8: strings(record.top8),
    };
  });
  const droppedCount =
    safeRows(data.dropped_have_imp_no_cpi).length +
    safeRows(data.dropped_have_cpi_no_imp).length +
    safeRows(data.dropped_neither).length;
  const oldCommon = strings(sourceSummary.original_raw_ag_common_across_n || data.committed_common_across_N);
  const foodCommon = strings(sourceSummary.food_import_common_across_n_same_cached_cpi);
  const foodTop10SameCpi = strings(sourceAudit.runs?.food_import_same_cached_cpi?.["10"]);
  const foodTop10LiveCpi = strings(sourceAudit.runs?.food_import_live_cpi?.["10"]);
  const enteredFood = strings(sourceSummary.entered_when_food_import_replaces_raw_ag);
  const sourceTrail = sourceFacts(report, data);
  if (sourceAudit.retrieved_at) {
    sourceTrail.push({ label: "Source-audit retrieval", value: String(sourceAudit.retrieved_at) });
  }
  if (sourceAudit.sources?.wdi_indicators) {
    sourceTrail.push({ label: "WDI indicators checked", value: strings(sourceAudit.sources.wdi_indicators).join(", ") });
  }
  if (sourceAudit.sources?.hdx_wfp_package_api) {
    sourceTrail.push({ label: "WFP package metadata", value: String(sourceAudit.sources.hdx_wfp_package_api) });
  }
  const componentCards = hasSourceAudit ? [
    {
      key: "old-raw-ag",
      value: formatNumber(sourceSummary.raw_ag_import_latest_rows),
      label: "Raw-ag import rows",
      note: `The old leg is agricultural raw materials, not food imports; its stable common set is ${oldCommon.join(", ") || "none"}.`,
      status: "flag",
    },
    {
      key: "food-import",
      value: formatNumber(sourceSummary.food_import_latest_rows),
      label: "Food-import rows",
      note: `The true food-import leg lifts the CPI x import joint universe to ${formatNumber(sourceSummary.joint_cached_cpi_food_import_rows)} rows; ${enteredFood.join(", ") || "no economies"} enter eligibility.`,
      status: "survived",
    },
    {
      key: "stable-set",
      value: foodCommon.join(", ") || "none",
      label: "Stable set after repair",
      note: `Using the same cached CPI leg, the top-8 set is ${strings(sourceAudit.runs?.food_import_same_cached_cpi?.["8"]).join(", ") || "empty"} and top-10 is ${foodTop10SameCpi.join(", ") || "empty"}.`,
      status: "dropped",
    },
    {
      key: "wfp-market",
      value: `${formatNumber(sourceSummary.wfp_csv_size_mb, 1)} MB`,
      label: "WFP market CSV visible",
      note: `${formatNumber(sourceSummary.wfp_csv_resources)} CSV resource is visible through HDX, but only metadata and a header sample are inspected here.`,
      status: "flag",
    },
    {
      key: "local-exposure",
      value: "0",
      label: "Market-climate joins",
      note: "No market-month price panel, commodity basket, household food-expenditure denominator, or local climate shock is joined.",
      status: "dropped",
    },
  ] as ComponentCard[] : undefined;

  return {
    kind: report.audit!.kind,
    stats: hasSourceAudit ? [
      { value: `${formatNumber(sourceSummary.joint_cached_cpi_food_import_rows)}/${formatNumber(sourceSummary.original_joint_universe_n)}`, label: "food/raw joint rows" },
      { value: formatNumber(sourceSummary.food_import_latest_rows), label: "WDI food-import rows" },
      { value: foodCommon.join(", ") || "none", label: "stable set after repair" },
      { value: `${formatNumber(sourceSummary.wfp_csv_size_mb, 1)} MB`, label: "WFP CSV not joined" },
    ] : [
      { value: formatNumber(data.joint_universe_n), label: "joint indicator universe" },
      { value: formatNumber(droppedCount), label: "roster rows dropped by coverage" },
      { value: formatNumber(years.length), label: "common-vintage reruns" },
    ],
    chartTitle: hasSourceAudit
      ? "The old stable pair disappears when the import leg is actually food."
      : "The first result is a coverage funnel, not a vulnerability ranking.",
    chartDeck: hasSourceAudit
      ? "Bars compare the old raw-materials import leg with the true WDI food-import leg. Cards show why WFP market prices are still a source wall, not a joined climate-price model."
      : "The funnel shows how the roster narrows when CPI and agricultural-import legs both have to exist.",
    funnelRows: hasSourceAudit ? [
      { label: "ADB roster", value: total, total, note: "starting DMC/economy roster" },
      { label: "Old CPI x raw-ag joint", value: numberValue(sourceSummary.original_joint_universe_n), total, note: "old joint universe behind LAO+PAK" },
      { label: "Have food-import leg", value: numberValue(sourceSummary.food_import_latest_rows), total, note: "WDI TM.VAL.FOOD.ZS.UN latest value" },
      { label: "CPI x food-import joint", value: numberValue(sourceSummary.joint_cached_cpi_food_import_rows), total, note: "same cached CPI leg; food-import repair" },
    ] : [
      { label: "ADB roster", value: total, total, note: "starting DMC/economy roster" },
      { label: "Have CPI leg", value: numberValue(data.have_cpi_n), total, note: "consumer price index available" },
      { label: "Have import leg", value: numberValue(data.have_imp_n), total, note: "agricultural-imports indicator available" },
      { label: "Have both legs", value: numberValue(data.joint_universe_n), total, note: "joint universe used by the screen" },
    ],
    coverageYears: years,
    componentCards,
    readouts: [
      ...(hasSourceAudit ? [
        { label: "Old raw-ag common across N", value: oldCommon.join(", ") || "none" },
        { label: "Food-import common across N", value: foodCommon.join(", ") || "none" },
        { label: "Food-import top-10, same CPI", value: foodTop10SameCpi.join(", ") || "empty" },
        { label: "Food-import top-10, live CPI", value: foodTop10LiveCpi.join(", ") || "empty" },
        { label: "Rows entering food-import eligibility", value: enteredFood.join(", ") || "none" },
        { label: "WFP header fields sampled", value: strings(sourceAudit.wfp_detail?.header_fields).slice(0, 6).join(", ") || "none" },
        { label: "Analysis-ready food-price exposure", value: String(sourceSummary.analysis_ready_food_price_exposure) },
      ] : [
        { label: "Dropped: imports but no CPI", value: strings(data.dropped_have_imp_no_cpi).join(", ") || "none" },
        { label: "Dropped: CPI but no imports", value: strings(data.dropped_have_cpi_no_imp).join(", ") || "none" },
        { label: "Dropped: neither leg", value: strings(data.dropped_neither).join(", ") || "none" },
        { label: "Common across committed N", value: strings(data.committed_common_across_N).join(", ") || "none" },
      ]),
    ],
    sourceFacts: sourceTrail,
    caveats: unique(baseCaveats(report, data).concat([
      data.food_price_data_wall,
      sourceAudit.claim_scope,
      ...(sourceSummary.owner_gated_or_unfinished_steps || []),
    ].filter(Boolean).map(String))),
    generatedAt: data.generated_at,
  };
}

function buildSocialProtectionModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const sourceAudit = data.social_protection_source_readiness || {};
  const sourceSummary = sourceAudit.summary || {};
  const hasSourceAudit = Boolean(data.social_protection_source_readiness);
  const headline = strings(data.headline_five);
  const excluded = new Set(safeRows(data.excluded_but_outrank_lowest_headline).map((row) => String(row.iso3)));
  const rows = safeRows(data.value_ranked_order)
    .slice(0, 9)
    .map((row) => {
      const iso = String(row.iso3);
      const headlineRank = headline.indexOf(iso);
      return {
        key: iso,
        label: iso,
        sublabel: row.country,
        leftText: `#${row.rank} value rank`,
        rightText: headlineRank >= 0 ? `#${headlineRank + 1} headline` : "excluded from headline",
        leftValue: formatFlexible(row.gap),
        rightValue: String(row.legs_present || "missing legs"),
        note: row.in_headline_five ? "included in headline five" : "not in named headline five",
        status: excluded.has(iso) ? "flag" : statusFromSets(true, headlineRank >= 0),
        intensity: excluded.has(iso) ? 92 : headlineRank >= 0 ? 44 : 70,
      };
    }) as RankRow[];
  const safetyTop5 = strings(sourceSummary.safety_net_variant_top5);
  const oldTop5 = strings(sourceSummary.old_value_top5);
  const safetyEntered = strings(sourceSummary.safety_net_entered_vs_headline);
  const safetyDropped = strings(sourceSummary.safety_net_dropped_vs_headline);
  const sourceTrail = sourceFacts(report, data);
  if (sourceAudit.retrieved_at) {
    sourceTrail.push({ label: "Source-audit retrieval", value: String(sourceAudit.retrieved_at) });
  }
  if (sourceAudit.sources?.wdi_indicators) {
    sourceTrail.push({ label: "WDI indicators checked", value: strings(sourceAudit.sources.wdi_indicators).join(", ") });
  }
  const componentCards = hasSourceAudit ? [
    {
      key: "all-sp",
      value: formatNumber(sourceSummary.all_sp_latest_rows),
      label: "All-SP coverage rows",
      note: "The old coverage leg is all social protection and labor coverage, not emergency cash-transfer delivery.",
      status: "flag",
    },
    {
      key: "safety-net",
      value: safetyTop5.join(", ") || "none",
      label: "Safety-net variant top five",
      note: `${formatNumber(sourceSummary.safety_net_headline_overlap_count)} of the named headline five remain; this is a source-object stress test, not a replacement headline.`,
      status: "flag",
    },
    {
      key: "poverty-line",
      value: "$3.00",
      label: "Current WDI poverty line",
      note: "Current SI.POV.DDAY metadata says $3.00/day 2021 PPP while older program prose says $2.15/day 2017 PPP.",
      status: "flag",
    },
    {
      key: "account-proxy",
      value: formatNumber(sourceSummary.account_latest_rows),
      label: "Findex account rows",
      note: "Account ownership is availability of an account, not active payment-rail use or last-mile delivery.",
      status: "flag",
    },
    {
      key: "delivery-object",
      value: "0",
      label: "Shock-payment delivery joins",
      note: "No emergency program registry, beneficiary roster, payment rail, delivery-speed record, or shock-event trigger is joined; the delivery object is not joined.",
      status: "dropped",
    },
  ] as ComponentCard[] : undefined;

  return {
    kind: report.audit!.kind,
    stats: hasSourceAudit ? [
      { value: formatNumber(data.excluded_for_missing_leg_count), label: "one-legged rows outrank headline tail" },
      { value: formatNumber(sourceSummary.safety_net_headline_overlap_count), label: "headline overlap under safety-net leg" },
      { value: formatNumber(sourceSummary.safety_net_latest_rows), label: "safety-net coverage rows" },
      { value: String(sourceSummary.analysis_ready_shock_payment_coverage), label: "analysis-ready delivery object" },
    ] : [
      { value: formatNumber(data.excluded_for_missing_leg_count), label: "excluded rows outrank lowest headline" },
      { value: `${data.lowest_ranked_headline_member?.iso3 || "?"} #${data.lowest_ranked_headline_member?.value_rank || "?"}`, label: "lowest headline member by value rank" },
      { value: strings(data.imputation_variant?.entered_vs_headline).join(", ") || "none", label: "entered under imputation variant" },
    ],
    chartTitle: hasSourceAudit
      ? "Changing the source object changes the whole top set."
      : "Missing one leg can hide a higher-ranked economy.",
    chartDeck: hasSourceAudit
      ? "The rank ledger still shows the dropped-leg problem. The cards add the source wall: all-SP is not shock-payment delivery, the narrower safety-net variant reorders the set, and no beneficiary payment object is joined."
      : "The ledger shows value rank before the headline filter removes one-legged observations.",
    leftLabel: "Value-ranked order",
    rightLabel: "Headline inclusion",
    rows,
    componentCards,
    readouts: [
      { label: "Headline five", value: headline.join(", ") },
      { label: "Excluded but higher than lowest headline", value: safeRows(data.excluded_but_outrank_lowest_headline).map((row) => String(row.iso3)).join(", ") },
      { label: "Imputed top five", value: strings(data.imputation_variant?.imputed_top5).join(", ") },
      { label: "Dropped under imputation", value: strings(data.imputation_variant?.dropped_vs_headline).join(", ") || "none" },
      ...(hasSourceAudit ? [
        { label: "Old value top five", value: oldTop5.join(", ") || "none" },
        { label: "Safety-net variant top five", value: safetyTop5.join(", ") || "none" },
        { label: "Entered under safety-net leg", value: safetyEntered.join(", ") || "none" },
        { label: "Dropped under safety-net leg", value: safetyDropped.join(", ") || "none" },
        { label: "Poverty metadata label", value: String(sourceSummary.poverty_indicator_current_name || "not parsed") },
        { label: "Delivery object built", value: String(sourceSummary.analysis_ready_shock_payment_coverage) },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: unique(baseCaveats(report, data).concat([
      data.social_protection_data_wall,
      sourceAudit.claim_scope,
      ...(sourceSummary.owner_gated_or_unfinished_steps || []),
    ].filter(Boolean).map(String))),
    generatedAt: data.generated_at,
  };
}

function buildWaterModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const sourceAudit = data.water_source_readiness || {};
  const sourceSummary = sourceAudit.summary || {};
  const hasSourceAudit = Boolean(data.water_source_readiness);
  const over = safeRows(data.over_100pct_internal_denominator);
  const cards: ComponentCard[] = over.map((row) => ({
    key: String(row.iso3),
    value: formatPct(row.withdrawal_pct_internal, 0),
    label: `${row.iso3} internal-water withdrawal denominator`,
    note: `water term ${formatFlexible(row.water_term)}; saturated at ceiling`,
    status: "flag",
  }));
  if (data.afghanistan_inversion) {
    cards.push({
      key: "AFG",
      value: formatPct(data.afghanistan_inversion.withdrawal_pct, 1),
      label: "AFG withdrawal below cap",
      note: `rank falls to #${data.rural_counterfactual?.afg_rank_rural_dropped} when rural multiplier is dropped`,
      status: "dropped",
    });
  }
  const availableTop5 = strings(sourceSummary.available_stress_top5);
  const cropTop5 = strings(sourceSummary.crop_hhi_top5);
  const sourceVariantTop5 = strings(sourceSummary.source_variant_top5);
  const sourceTrail = sourceFacts(report, data);
  if (sourceAudit.retrieved_at) {
    sourceTrail.push({ label: "Source-audit retrieval", value: String(sourceAudit.retrieved_at) });
  }
  if (sourceAudit.sources?.wdi_indicators) {
    sourceTrail.push({ label: "WDI indicators checked", value: strings(sourceAudit.sources.wdi_indicators).join(", ") });
  }
  if (sourceAudit.sources?.faostat_domain) {
    sourceTrail.push({ label: "FAOSTAT source", value: `${sourceAudit.sources.faostat_domain}; ${sourceAudit.sources.faostat_element || "Area harvested"}` });
  }
  if (hasSourceAudit) {
    cards.push(
      {
        key: "available-stress",
        value: availableTop5.join(", ") || "none",
        label: "Available-water stress top five",
        note: "WDI/AQUASTAT water stress uses available freshwater resources rather than the old internal-only denominator.",
        status: "flag",
      },
      {
        key: "crop-mix",
        value: cropTop5.join(", ") || "none",
        label: "FAOSTAT crop-HHI top five",
        note: `${formatNumber(sourceSummary.crop_mix_country_rows)} economies have usable 2024 harvested-area crop-mix rows.`,
        status: "flag",
      },
      {
        key: "source-variant",
        value: sourceVariantTop5.join(", ") || "none",
        label: "Source-upgraded national variant",
        note: `${formatNumber(sourceSummary.source_variant_overlap_old_raw_top4)} of the old raw top four remain; this is a diagnostic variant, not a headline ranking.`,
        status: "survived",
      },
      {
        key: "faostat-rows",
        value: formatNumber(sourceSummary.faostat_area_harvested_rows),
        label: "FAOSTAT Area harvested rows",
        note: `${formatNumber(sourceSummary.faostat_aggregate_rows_excluded)} aggregate rows excluded before crop-share calculation.`,
        status: "survived",
      },
      {
        key: "basin-overlay",
        value: String(sourceSummary.analysis_ready_basin_crop_overlay),
        label: "Basin/crop overlay",
        note: "No basin allocation, crop-water requirement, irrigation command area, GRACE depletion, or subnational rural exposure is joined.",
        status: "dropped",
      },
    );
  }

  return {
    kind: report.audit!.kind,
    stats: hasSourceAudit ? [
      { value: formatNumber(sourceSummary.internal_over100_count), label: "above 100% internal denominator" },
      { value: formatNumber(sourceSummary.available_stress_latest_rows), label: "available-water stress rows" },
      { value: formatNumber(sourceSummary.crop_mix_country_rows), label: "FAOSTAT crop-mix rows" },
      { value: String(sourceSummary.analysis_ready_basin_crop_overlay), label: "analysis-ready basin/crop overlay" },
    ] : [
      { value: formatNumber(over.length), label: "above 100% internal denominator" },
      { value: `#${data.rural_counterfactual?.afg_rank_rural_dropped || "?"}`, label: "AFG rank without rural multiplier" },
      { value: strings(data.rural_counterfactual?.high_withdrawal_set).join(", "), label: "high-withdrawal set" },
    ],
    chartTitle: hasSourceAudit
      ? "The source upgrade separates water stress from crop mix."
      : "The water signal is partly a denominator signal.",
    chartDeck: hasSourceAudit
      ? "Cards keep the old internal-denominator artifact visible, then add WDI/AQUASTAT available-water stress, FAOSTAT harvested-area crop concentration, and the missing basin/crop overlay."
      : "Cards separate over-100-percent internal-water denominators from Afghanistan's rural-population multiplier effect.",
    componentCards: cards,
    readouts: [
      { label: "Baseline raw-index top four", value: strings(data.reproduced_baseline_top4_raw_index).join(", ") },
      { label: "Pre-registered headline top four", value: strings(data.prereg_headline_top4_intersection_of_top5).join(", ") },
      { label: "Top four when rural term is dropped", value: strings(data.rural_counterfactual?.top4_rural_dropped).join(", ") },
      { label: "Data walls", value: Object.values(data.data_walls || {}).join(" ") || "AQUASTAT and FAOSTAT extensions documented in artifact." },
      ...(hasSourceAudit ? [
        { label: "Available-water stress top five", value: availableTop5.join(", ") || "none" },
        { label: "FAOSTAT crop-HHI top five", value: cropTop5.join(", ") || "none" },
        { label: "Source-upgraded variant top five", value: sourceVariantTop5.join(", ") || "none" },
        { label: "Overlap with old raw top four", value: formatNumber(sourceSummary.source_variant_overlap_old_raw_top4) },
        { label: "Overlap with pre-registered top four", value: formatNumber(sourceSummary.source_variant_overlap_prereg_top4) },
        { label: "Basin/crop overlay built", value: String(sourceSummary.analysis_ready_basin_crop_overlay) },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: unique(baseCaveats(report, data).concat([
      data.water_crop_data_wall,
      sourceAudit.claim_scope,
      ...(sourceSummary.owner_gated_or_unfinished_steps || []),
    ].filter(Boolean).map(String))),
    generatedAt: data.generated_at,
  };
}

function buildInvisibleUrbanizationModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const sourceAudit = data.urban_source_readiness || {};
  const sourceSummary = sourceAudit.summary || {};
  const hasSourceAudit = Boolean(data.urban_source_readiness);
  const sweep = data.multiplier_sweep_is_rank_preserving || {};
  const boundary = data.genuine_falsification_not_run?.top5_boundary_pair || [];
  const shockPct = data.genuine_falsification_not_run?.input_shock_fraction_to_break_top5_boundary
    ? numberValue(data.genuine_falsification_not_run.input_shock_fraction_to_break_top5_boundary) * 100
    : 0;
  const sourceTrail = sourceFacts(report, data);
  if (sourceAudit.retrieved_at) {
    sourceTrail.push({ label: "Urban source audit retrieval", value: String(sourceAudit.retrieved_at) });
  }
  if (sourceAudit.sources?.wdi_indicators) {
    sourceTrail.push({ label: "WDI indicators checked", value: strings(sourceAudit.sources.wdi_indicators).join(", ") });
  }
  if (sourceAudit.sources?.ghsl_pages) {
    sourceTrail.push({ label: "GHSL metadata pages", value: strings(sourceAudit.sources.ghsl_pages).join("; ") });
  }

  const componentCards: ComponentCard[] = [
    {
      key: "formula",
      value: "2 WDI terms",
      label: "source structure",
      note: data.signal_is_two_wdi_series_multiplied?.satellite_or_builtup_field_in_sources
        ? "satellite field present"
        : "no satellite or built-up field in sources",
      status: "flag",
    },
    {
      key: "boundary",
      value: boundary.join(" / "),
      label: "top-five boundary pair",
      note: `${formatPct(shockPct, 2)} non-uniform input shock breaks the boundary`,
      status: "dropped",
    },
  ];

  if (hasSourceAudit) {
    componentCards.push(
      {
        key: "wdi-definition",
        value: sourceSummary.wdi_urban_definition_is_national ? "national definitions" : "not confirmed",
        label: "WDI urban definition",
        note: "WDI urban share is defined by national statistical offices; this is not a common built-up boundary.",
        status: "flag",
      },
      {
        key: "ghsl-pages",
        value: `${formatNumber(sourceSummary.ghsl_public_metadata_pages_reachable)}/${formatNumber(sourceSummary.ghsl_public_metadata_pages_checked)}`,
        label: "GHSL/SMOD metadata pages",
        note: "Built-up surface, SMOD, download-catalog, and Earth Engine metadata pages are visible; no raster is downloaded.",
        status: "survived",
      },
      {
        key: "adm2-boundaries",
        value: `${formatNumber(sourceSummary.top5_geoboundaries_adm2_reachable_rows)}/${formatNumber(sourceSummary.top5_geoboundaries_adm2_metadata_rows)}`,
        label: "Top-five ADM2 boundary metadata",
        note: `Boundary-year span ${sourceSummary.top5_boundary_year_min || "?"}-${sourceSummary.top5_boundary_year_max || "?"}; geometries are not intersected.`,
        status: "survived",
      },
      {
        key: "builtup-overlay",
        value: String(sourceSummary.analysis_ready_builtup_boundary_overlay),
        label: "Built-up/boundary overlay",
        note: "No GHSL raster export, SMOD grid, boundary intersection, classification-history ledger, or zonal statistic is built.",
        status: "dropped",
      },
    );
  }

  return {
    kind: report.audit!.kind,
    stats: hasSourceAudit ? [
      { value: `${formatNumber(sourceSummary.ghsl_public_metadata_pages_reachable)}/${formatNumber(sourceSummary.ghsl_public_metadata_pages_checked)}`, label: "GHSL metadata pages reachable" },
      { value: `${formatNumber(sourceSummary.top5_geoboundaries_adm2_reachable_rows)}/${formatNumber(sourceSummary.top5_geoboundaries_adm2_metadata_rows)}`, label: "top-five ADM2 metadata rows" },
      { value: String(sourceSummary.analysis_ready_builtup_boundary_overlay), label: "built-up/boundary overlay" },
    ] : [
      { value: formatFlexible(1, 1), label: "Spearman for scalar sweep" },
      { value: formatNumber(sweep.total_rank_inversions_across_sweep), label: "rank inversions across 5/10/15" },
      { value: formatPct(shockPct, 2), label: "shock to break top-five boundary" },
    ],
    chartTitle: hasSourceAudit
      ? "The source wall shows what the WDI proxy still cannot see."
      : "The robustness sweep preserves ranks because it only scales the same score.",
    chartDeck: hasSourceAudit
      ? "The lanes keep the empty scalar-sweep result beside GHSL, SMOD, and boundary metadata, while the analysis-ready overlay remains false."
      : "The lanes show identical top-five membership under positive scalar multipliers, then place the real input perturbation beside it.",
    laneRows: safeRows(sweep.results).map((row) => ({
      key: String(row.label),
      label: `multiplier ${row.multiplier}`,
      left: `Spearman ${formatFlexible(row.spearman_vs_baseline, 1)}`,
      middle: `${formatNumber(row.pairwise_rank_inversions_vs_baseline)} inversions`,
      right: strings(row.top5).join(", "),
      note: `top score ${formatFlexible(row.top1_score)}`,
      status: "survived",
    })) as LaneRow[],
    componentCards,
    readouts: [
      { label: "Frozen formula", value: String(data.frozen_formula) },
      { label: "Baseline top five", value: strings(sweep.baseline_top5).join(", ") },
      { label: "All scalar Spearman equal one", value: String(Boolean(sweep.all_spearman_equal_one)) },
      { label: "Reproduction check", value: data.reproduces_committed_signal?.note || "committed column reproduced" },
      ...(hasSourceAudit ? [
        { label: "WDI urban definition is national", value: String(sourceSummary.wdi_urban_definition_is_national) },
        { label: "GHSL metadata pages reachable", value: `${formatNumber(sourceSummary.ghsl_public_metadata_pages_reachable)}/${formatNumber(sourceSummary.ghsl_public_metadata_pages_checked)}` },
        { label: "Top-five ADM2 boundary metadata", value: `${formatNumber(sourceSummary.top5_geoboundaries_adm2_reachable_rows)}/${formatNumber(sourceSummary.top5_geoboundaries_adm2_metadata_rows)}` },
        { label: "Boundary year span", value: `${sourceSummary.top5_boundary_year_min || "?"}-${sourceSummary.top5_boundary_year_max || "?"}` },
        { label: "Built-up/boundary overlay built", value: String(sourceSummary.analysis_ready_builtup_boundary_overlay) },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: unique(baseCaveats(report, data).concat([
      data.invisible_urbanization_data_wall,
      sourceAudit.claim_scope,
      ...(sourceSummary.owner_gated_or_unfinished_steps || []),
    ].filter(Boolean).map(String))),
    generatedAt: data.generated_at,
  };
}

function buildPortModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const sourceAudit = data.port_source_readiness || {};
  const sourceSummary = sourceAudit.summary || {};
  const hasSourceAudit = Boolean(data.port_source_readiness);
  const capRows = Object.entries(data.cap_perturbation || {}).map(([cap, row]) => {
    const record = row as JsonValue;
    const truncated = strings(record.rows_truncated);
    return {
      key: cap,
      label: `cap ${cap}`,
      value: strings(record.top5).join(", "),
      note: `${formatNumber(record.overlap_with_baseline)}/5 overlap; truncated rows ${truncated.join(", ") || "none"}`,
      status: truncated.length ? "flag" : "survived",
    };
  }) as ParameterRow[];
  const sourceTrail = sourceFacts(report, data);
  if (sourceAudit.retrieved_at) {
    sourceTrail.push({ label: "Port source audit retrieval", value: String(sourceAudit.retrieved_at) });
  }
  if (sourceAudit.sources?.wdi_indicators) {
    sourceTrail.push({ label: "WDI indicators checked", value: strings(sourceAudit.sources.wdi_indicators).join(", ") });
  }
  const containerTop5 = safeRows(sourceSummary.container_port_traffic_top5).map((row) => String(row.iso3)).join(", ");
  const componentCards: ComponentCard[] = [
    {
      key: "baseline",
      value: `${formatNumber(data.dmcs_reaching_cap_baseline)}`,
      label: "rows binding at baseline cap",
      note: `baseline divisor ${formatFlexible(data.baseline_params?.divisor)}; cap ${formatFlexible(data.baseline_params?.cap)}`,
      status: "flag",
    },
    {
      key: "binding",
      value: strings(data.binding_cap_test?.rows_truncated).join(", ") || "none",
      label: "rows binding in forced binding test",
      note: `CHN index capped from ${formatFlexible(data.binding_cap_test?.chn_index_uncapped)} to ${formatFlexible(data.binding_cap_test?.chn_index_capped)}`,
      status: "survived",
    },
  ];

  if (hasSourceAudit) {
    componentCards.push(
      {
        key: "wdi-stack",
        value: `${formatNumber(sourceSummary.wdi_metadata_records_reachable)}/${formatNumber(sourceSummary.wdi_indicators_requested)}`,
        label: "WDI source stack",
        note: "LPI, imports, container port traffic, and freight-proxy metadata resolve through public WDI.",
        status: "survived",
      },
      {
        key: "container-traffic",
        value: `${formatNumber(sourceSummary.rankable_rows_with_container_port_traffic)}/${formatNumber(sourceSummary.rankable_dmc_count)}`,
        label: "rankable rows with container traffic",
        note: `Container-traffic top five: ${containerTop5 || "not available"}. Throughput is not travel time.`,
        status: "flag",
      },
      {
        key: "freight-proxy",
        value: `${formatNumber(sourceSummary.rankable_rows_with_any_actual_freight_proxy)}/${formatNumber(sourceSummary.rankable_dmc_count)}`,
        label: "rankable rows with freight proxy",
        note: "Air, rail, road, or container throughput is visible for the rankable rows, but it remains a proxy layer.",
        status: "flag",
      },
      {
        key: "travel-time",
        value: String(sourceSummary.analysis_ready_hinterland_travel_time),
        label: "hinterland travel-time join",
        note: "No port-to-inland OD network, route impedance, corridor travel-time surface, or port-performance table is joined.",
        status: "dropped",
      },
    );
  }

  return {
    kind: report.audit!.kind,
    stats: hasSourceAudit ? [
      { value: `${formatNumber(sourceSummary.wdi_metadata_records_reachable)}/${formatNumber(sourceSummary.wdi_indicators_requested)}`, label: "WDI source records reachable" },
      { value: `${formatNumber(sourceSummary.rankable_rows_with_container_port_traffic)}/${formatNumber(sourceSummary.rankable_dmc_count)}`, label: "rankable rows with container TEU" },
      { value: String(sourceSummary.analysis_ready_hinterland_travel_time), label: "hinterland travel-time join" },
    ] : [
      { value: formatNumber(data.dmcs_reaching_cap_baseline), label: "DMCs reaching baseline cap" },
      { value: formatFlexible(data.max_proxy_observed, 3), label: "max observed proxy" },
      { value: `$${formatFlexible(data.imports_to_reach_cap_usd_trillions, 1)}T`, label: "imports needed to reach cap" },
    ],
    chartTitle: hasSourceAudit
      ? "The cap is inert; the harder evidence object is still missing."
      : "A perturbed cap cannot test much if the observed data never touch it.",
    chartDeck: hasSourceAudit
      ? "The cap lanes stay on the page, then the source wall separates visible WDI throughput and freight proxies from the missing port-performance and hinterland travel-time join."
      : "The cap lanes keep the top five beside the number of rows that actually bind under each cap.",
    parameterRows: capRows,
    componentCards,
    readouts: [
      { label: "Baseline top five", value: strings(data.baseline_top5).join(", ") },
      { label: "Committed-panel top five", value: strings(data.committed_panel_top5).join(", ") },
      { label: "Import-volume top five", value: strings(data.import_volume_top5).join(", ") },
      { label: "Volume top-five same order?", value: String(Boolean(data.friction_top5_equals_volume_top5_order)) },
      ...(hasSourceAudit ? [
        { label: "WDI metadata records reachable", value: `${formatNumber(sourceSummary.wdi_metadata_records_reachable)}/${formatNumber(sourceSummary.wdi_indicators_requested)}` },
        { label: "Rankable rows with container traffic", value: `${formatNumber(sourceSummary.rankable_rows_with_container_port_traffic)}/${formatNumber(sourceSummary.rankable_dmc_count)}` },
        { label: "Rankable rows with any freight proxy", value: `${formatNumber(sourceSummary.rankable_rows_with_any_actual_freight_proxy)}/${formatNumber(sourceSummary.rankable_dmc_count)}` },
        { label: "Baseline top five with any freight proxy", value: `${formatNumber(sourceSummary.baseline_top5_with_any_actual_freight_proxy)}/5` },
        { label: "Container traffic top five", value: containerTop5 || "not available" },
        { label: "Direct port performance built", value: String(sourceSummary.analysis_ready_direct_port_performance) },
        { label: "Hinterland travel-time join", value: String(sourceSummary.analysis_ready_hinterland_travel_time) },
      ] : []),
    ],
    sourceFacts: sourceTrail,
    caveats: unique(baseCaveats(report, data).concat([
      data.port_hinterland_data_wall,
      sourceAudit.claim_scope,
      ...(sourceSummary.owner_gated_or_unfinished_steps || []),
    ].filter(Boolean).map(String))),
    generatedAt: data.generated_at,
  };
}

function buildSchoolHeatModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const counts = data.counts || {};
  const laneRows = safeRows(data.per_run).map((row) => {
    let status: LaneRow["status"] = "survived";
    if (row.all_zero) status = "dropped";
    else if (!row.khm_is_top1) status = "flag";
    return {
      key: String(row.label),
      label: String(row.label).replaceAll("_", " "),
      left: row.top_iso ? `top ${row.top_iso}` : "no top economy",
      middle: `KHM #${row.khm_rank}`,
      right: row.discriminating ? "discriminating" : "all-zero tie",
      note: String(row.verdict || ""),
      status,
    };
  }) as LaneRow[];

  return {
    kind: report.audit!.kind,
    stats: [
      { value: `${counts.khm_top1_among_discriminating}/${counts.discriminating}`, label: "KHM top-one among discriminating runs" },
      { value: formatNumber(counts.degenerate_all_zero), label: "degenerate all-zero runs" },
      { value: formatNumber(counts.rank_losing_for_khm), label: "rank-losing runs" },
    ],
    chartTitle: "The narrow claim survives only after bad runs are named.",
    chartDeck: "The run ledger separates discriminating KHM top-one runs from an all-zero tie and a rank-losing perturbation.",
    laneRows,
    readouts: [
      { label: "File claim common top five", value: strings(data.file_claim_common_top5_across_runs).join(", ") },
      { label: "Degenerate labels", value: strings(data.degenerate_labels).join(", ") || "none" },
      { label: "Rank-losing labels", value: strings(data.rank_losing_labels).join(", ") || "none" },
      { label: "KHM top-one labels", value: strings(data.khm_top1_labels).join(", ") || "none" },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildAuditModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  switch (report.audit?.programSlug) {
    case "grid-reliability-heat":
      return buildGridModel(report, data);
    case "migration-displacement-signals":
      return buildMigrationModel(report, data);
    case "mpi-nighttime-lights":
      return buildMpiModel(report, data);
    case "coastal-informal-risk":
      return buildCoastalModel(report, data);
    case "flood-market-access":
      return buildFloodModel(report, data);
    case "climate-health-workdays":
      return buildClimateHealthModel(report, data);
    case "food-price-climate-transmission":
      return buildFoodCoverageModel(report, data);
    case "social-protection-shock-coverage":
      return buildSocialProtectionModel(report, data);
    case "water-stress-crop-diversification":
      return buildWaterModel(report, data);
    case "invisible-urbanization":
      return buildInvisibleUrbanizationModel(report, data);
    case "port-hinterland-friction":
      return buildPortModel(report, data);
    case "school-heat-disruption":
      return buildSchoolHeatModel(report, data);
    default:
      return {
        kind: report.audit?.kind || "rank-shift",
        stats: [],
        chartTitle: report.title,
        chartDeck: report.deck,
        readouts: [],
        sourceFacts: sourceFacts(report, data),
        caveats: baseCaveats(report, data),
        generatedAt: data.generated_at,
      };
  }
}

function buildEvidenceSpine(report: ShowcaseReport, model: AuditModel | null): SpineItem[] {
  const depth = getShowcaseReportDepth(report);
  const quality = getShowcaseReportQuality(report);

  return [
    {
      label: "Decision problem",
      title: "What the reader needs to decide",
      body: depth.operationalUse,
    },
    {
      label: "Measurement doubt",
      title: report.audit?.question || report.title,
      body: report.audit?.readerPayoff || report.deck,
    },
    {
      label: "Test added",
      title: model?.chartTitle || report.visual,
      body: report.audit?.method || "The report is loaded from the committed evidence artifact before the visual is drawn.",
    },
    {
      label: "Publication gate",
      title: quality.readinessLabel,
      body: quality.publicationGap,
    },
  ];
}

function buildClaimLadder(report: ShowcaseReport): SpineItem[] {
  const depth = getShowcaseReportDepth(report);
  const quality = getShowcaseReportQuality(report);

  return [
    {
      label: "Finding now allowed",
      title: "Current evidence result",
      body: report.audit?.finding || report.deck,
    },
    {
      label: "Claim not allowed",
      title: "Boundary kept on page",
      body: report.audit?.nonClaim || "The report does not widen the claim beyond the generated evidence artifact.",
    },
    {
      label: "Falsifier",
      title: "What could weaken it",
      body: depth.falsifier,
    },
    {
      label: "Next upgrade",
      title: "How it graduates",
      body: quality.nextUpgrade,
    },
  ];
}

export default function ShowcaseEvidenceAudit() {
  const { reportSlug = "" } = useParams();
  const report = findShowcaseReportBySlug(reportSlug);
  const [data, setData] = useState<JsonValue | null>(null);
  const [error, setError] = useState<string | null>(null);

  const dataUrl = report?.audit?.dataUrl;

  useEffect(() => {
    if (!dataUrl) return;
    setData(null);
    setError(null);
    fetch(dataUrl)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then((payload: JsonValue) => setData(payload))
      .catch((err) => setError(String(err)));
  }, [dataUrl]);

  const model = useMemo(() => {
    if (!report || !report.audit || !data) return null;
    return buildAuditModel(report, data);
  }, [report, data]);

  if (!report || !report.audit) return <NotFound />;

  const depth = getShowcaseReportDepth(report);
  const quality = getShowcaseReportQuality(report);
  const evidenceSpine = buildEvidenceSpine(report, model);
  const claimLadder = buildClaimLadder(report);
  const nextReport =
    showcaseReports.find((item) => item.id === report.id + 1) ||
    showcaseReports.find((item) => item.id === 1);
  const previousReport =
    showcaseReports.find((item) => item.id === report.id - 1) ||
    showcaseReports[showcaseReports.length - 1];
  const heroChecks = [
    { label: "Use", body: depth.operationalUse },
    { label: "Falsifier", body: depth.falsifier },
    { label: "Gate", body: quality.publicationGap },
  ];

  return (
    <article className={`showcase-page audit-showcase audit-${report.audit.kind}`}>
      <header className="showcase-hero audit-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI evidence audit {String(report.id).padStart(2, "0")}</p>
          <h1 className="showcase-title showcase-title-wide audit-title">{report.title}</h1>
          <p className="showcase-lede">{report.deck}</p>
          <div className="showcase-meta">
            <span>{report.statusLabel}</span>
            <span>{report.audit.programSlug}</span>
            <span>{quality.readinessLabel}</span>
            <span>{report.audit.kind.replaceAll("-", " ")}</span>
            <span>not a widened claim</span>
          </div>
          <div className="audit-hero-brief" aria-label="Audit decision spine">
            {heroChecks.map((item) => (
              <article key={item.label}>
                <span>{item.label}</span>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
        </div>
        <div className="showcase-hero-panel audit-hero-panel" aria-label="Report evidence summary">
          {model ? (
            <>
              {model.stats.map((stat) => (
                <div key={`${stat.label}-${stat.value}`}>
                  <span className="showcase-stat-value">{stat.value}</span>
                  <span className="showcase-stat-label">{stat.label}</span>
                </div>
              ))}
              <div className="audit-hero-route">
                <span>Evidence artifact</span>
                <code>{report.audit.dataUrl}</code>
                <span>Source stack</span>
                <p>{report.sourceNote}</p>
              </div>
            </>
          ) : (
            <span className="showcase-loading">
              {error ? `Could not load evidence JSON: ${error}` : "Loading evidence packet..."}
            </span>
          )}
        </div>
      </header>

      <section className="showcase-section showcase-two-col audit-question">
        <div>
          <p className="kicker">Research hook</p>
          <h2>{report.audit.question}</h2>
          <p>{report.audit.readerPayoff}</p>
        </div>
        <div className="audit-finding-box">
          <span>Current audit finding</span>
          <strong>{report.audit.finding}</strong>
          <p>{report.audit.method}</p>
        </div>
      </section>

      <section className="showcase-section audit-spine-section">
        <div className="showcase-section-copy">
          <p className="kicker">Evidence spine</p>
          <h2>Start with the decision, then show the measurement break.</h2>
          <p>
            Each audit report is held to the same ADB/ERDI sequence: decision
            problem, data doubt, plain-language test, and the gate that still
            prevents publication-level language.
          </p>
        </div>
        <div className="audit-spine-grid">
          {evidenceSpine.map((item, index) => (
            <div className="audit-spine-card" key={item.label}>
              <span>{String(index + 1).padStart(2, "0")} / {item.label}</span>
              <strong>{item.title}</strong>
              <p>{item.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="showcase-section audit-evidence-section">
        <div className="showcase-explorer-head">
          <div>
            <p className="kicker">Evidence visual</p>
            <h2>{model?.chartTitle || "Loading the generated artifact."}</h2>
            <p>{model?.chartDeck || "The page is reading the committed JSON artifact before drawing the report surface."}</p>
          </div>
          <div className="audit-nav-card">
            <Link to={previousReport.href}>Previous report</Link>
            <Link to={nextReport.href}>Next report</Link>
          </div>
        </div>
        {model ? <AuditVisual model={model} /> : <div className="audit-loading-block">Loading artifact visual...</div>}
      </section>

      {model && (
        <section className="showcase-section showcase-two-col audit-claim-section">
          <div>
            <p className="kicker">Claim ladder</p>
            <h2>{report.audit.finding}</h2>
            <div className="audit-claim-ladder">
              {claimLadder.map((item) => (
                <div key={item.label}>
                  <span>{item.label}</span>
                  <strong>{item.title}</strong>
                  <p>{item.body}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="showcase-fact-list audit-readouts">
            <div>
              <span>Current QA stage</span>
              <strong>{quality.readinessLabel}</strong>
            </div>
            <div>
              <span>QA summary</span>
              <strong>{quality.qaSummary}</strong>
            </div>
            <div>
              <span>Operational use</span>
              <strong>{depth.operationalUse}</strong>
            </div>
            <div>
              <span>Falsifier</span>
              <strong>{depth.falsifier}</strong>
            </div>
            <div>
              <span>Next upgrade</span>
              <strong>{quality.nextUpgrade}</strong>
            </div>
            {model.readouts.map((fact) => (
              <div key={fact.label}>
                <span>{fact.label}</span>
                <strong>{fact.value}</strong>
              </div>
            ))}
          </div>
        </section>
      )}

      {model && (
        <section className="showcase-section showcase-two-col">
          <div>
            <p className="kicker">Limits and reproducibility</p>
            <h2>Trust comes from the source trail.</h2>
            <p>
              The evidence path below names the generated artifact, companion
              table, source stack, attestation chain, and caveats before the
              reader treats the result as usable.
            </p>
            <div className="audit-caveat-list">
              {model.caveats.filter(Boolean).map((caveat) => (
                <p key={caveat}>{caveat}</p>
              ))}
            </div>
          </div>
          <div className="showcase-source-box audit-source-box">
            <p className="showcase-source-title">Reproduce this report slot</p>
            {model.sourceFacts.map((fact) => (
              <div className="audit-source-row" key={fact.label}>
                <span>{fact.label}</span>
                <code>{fact.value}</code>
              </div>
            ))}
            <a href={report.audit.dataUrl} download>
              {report.audit.downloadLabel}
            </a>
            {report.audit.csvUrl && (
              <a href={report.audit.csvUrl} download>
                Download CSV companion
              </a>
            )}
            <Link to={`/${report.audit.programSlug}`}>Open program evidence page</Link>
          </div>
        </section>
      )}

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">Full report queue</p>
          <h2>Twenty slots, one evidence rule.</h2>
          <p>
            The batch now includes the original bespoke report surfaces and the
            artifact-driven audit reports. Every entry names a committed
            evidence path and keeps the visual tied to public data.
          </p>
        </div>
        <div className="showcase-queue audit-queue">
          {showcaseReports.map((item) => (
            <div className="showcase-queue-row" key={item.href}>
              <span>{String(item.id).padStart(2, "0")}</span>
              <strong>
                <Link to={item.href}>{item.shortTitle}</Link>
              </strong>
              <em>
                {item.statusLabel} - {getShowcaseReportQuality(item).readinessLabel}
              </em>
              <code>{item.evidencePath}</code>
            </div>
          ))}
        </div>
      </section>
    </article>
  );
}

function AuditVisual({ model }: { model: AuditModel }) {
  if (model.rows && model.componentCards) {
    return (
      <div className="audit-visual-grid">
        <RankAuditVisual model={model} />
        <ComponentVisual model={model} />
      </div>
    );
  }
  if (model.stackRows && model.componentCards) {
    return (
      <div className="audit-visual-grid">
        <StackedBlindnessVisual model={model} />
        <ComponentVisual model={model} />
      </div>
    );
  }
  if (model.rows) {
    return <RankAuditVisual model={model} />;
  }
  if (model.stackRows) {
    return <StackedBlindnessVisual model={model} />;
  }
  if (model.funnelRows && model.componentCards) {
    return (
      <div className="audit-visual-grid audit-coverage-source-grid">
        <div className="audit-coverage-panels">
          <CoverageFunnelPanels model={model} />
        </div>
        <ComponentVisual model={model} />
      </div>
    );
  }
  if (model.funnelRows) {
    return <CoverageFunnelVisual model={model} />;
  }
  if (model.parameterRows) {
    return <ParameterVisual model={model} />;
  }
  if (model.laneRows && model.componentCards) {
    return (
      <div className="audit-visual-grid">
        <LaneVisual model={model} />
        <ComponentVisual model={model} />
      </div>
    );
  }
  if (model.laneRows) {
    return <LaneVisual model={model} />;
  }
  if (model.componentCards) {
    return <ComponentVisual model={model} />;
  }
  return <div className="audit-loading-block">No visual model available for this artifact.</div>;
}

function RankAuditVisual({ model }: { model: AuditModel }) {
  return (
    <div className="audit-rank-visual">
      <div className="audit-rank-header">
        <span>{model.leftLabel || "Original"}</span>
        <span>audit movement</span>
        <span>{model.rightLabel || "Audit"}</span>
      </div>
      {model.rows?.map((row) => (
        <div className={`audit-rank-row audit-status-${row.status}`} key={row.key}>
          <div className="audit-rank-side">
            <strong>{row.leftText}</strong>
            {row.leftValue && <span>{row.leftValue}</span>}
          </div>
          <div className="audit-rank-track">
            <div>
              <b>{row.label}</b>
              {row.sublabel && <span>{row.sublabel}</span>}
            </div>
            <i style={{ width: `${Math.max(12, Math.min(100, row.intensity))}%` }} />
            {row.note && <small>{row.note}</small>}
          </div>
          <div className="audit-rank-side audit-rank-side-right">
            <strong>{row.rightText}</strong>
            {row.rightValue && <span>{row.rightValue}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

function StackedBlindnessVisual({ model }: { model: AuditModel }) {
  return (
    <div className="audit-stack-visual">
      <div className="audit-stack-legend">
        <span><i className="blind" /> NTL-blind MPI weight</span>
        <span><i className="visible" /> Plausibly visible weight</span>
      </div>
      {model.stackRows?.map((row) => (
        <div className="audit-stack-row" key={row.key}>
          <div>
            <strong>{row.label}</strong>
            <span>{row.note}</span>
          </div>
          <div className="audit-stack-bar" aria-label={`${row.label}: ${formatPct(row.blind, 1)} blind`}>
            <i className="blind" style={{ width: `${Math.max(0, Math.min(100, row.blind))}%` }}>
              {formatPct(row.blind, 0)}
            </i>
            <i className="visible" style={{ width: `${Math.max(0, Math.min(100, row.visible))}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

function CoverageFunnelVisual({ model }: { model: AuditModel }) {
  return (
    <div className="audit-visual-grid">
      <CoverageFunnelPanels model={model} />
    </div>
  );
}

function CoverageFunnelPanels({ model }: { model: AuditModel }) {
  return (
    <>
      <div className="audit-funnel">
        {model.funnelRows?.map((row) => (
          <div className="audit-funnel-row" key={row.label}>
            <div>
              <strong>{row.label}</strong>
              <span>{row.note}</span>
            </div>
            <div className="audit-funnel-bar">
              <i style={{ width: `${Math.max(4, (row.value / Math.max(1, row.total)) * 100)}%` }} />
            </div>
            <b>{formatNumber(row.value)}</b>
          </div>
        ))}
      </div>
      <div className="audit-year-wall">
        {model.coverageYears?.map((year) => (
          <div key={year.year}>
            <span>{year.year}</span>
            <strong>{formatNumber(year.nBoth)} with both legs</strong>
            <p>Top 5: {year.top5.join(", ") || "none"}</p>
            <p>Top 8: {year.top8.join(", ") || "none"}</p>
          </div>
        ))}
      </div>
    </>
  );
}

function LaneVisual({ model }: { model: AuditModel }) {
  return (
    <div className="audit-lane-visual">
      {model.laneRows?.map((row) => (
        <div className={`audit-lane-row audit-status-${row.status}`} key={row.key}>
          <div className="audit-lane-name">
            <strong>{row.label}</strong>
            <span>{row.note}</span>
          </div>
          <div className="audit-lane-cells">
            <span>{row.left}</span>
            <span>{row.middle}</span>
            <span>{row.right}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

function ParameterVisual({ model }: { model: AuditModel }) {
  return (
    <div className="audit-visual-grid">
      <div className="audit-parameter-wall">
        {model.parameterRows?.map((row) => (
          <div className={`audit-parameter-row audit-status-${row.status}`} key={row.key}>
            <span>{row.label}</span>
            <strong>{row.value}</strong>
            <p>{row.note}</p>
          </div>
        ))}
      </div>
      <ComponentVisual model={model} />
    </div>
  );
}

function ComponentVisual({ model }: { model: AuditModel }) {
  return (
    <div className="audit-component-grid">
      {model.componentCards?.map((card) => (
        <div className={`audit-component-card audit-status-${card.status}`} key={card.key}>
          <span>{card.label}</span>
          <strong>{card.value}</strong>
          <p>{card.note}</p>
        </div>
      ))}
    </div>
  );
}
