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
  const overlap = capacityTop.filter((iso) => generationTop.includes(iso)).length;
  const rows = unique([...capacityTop, ...generationTop]).map((iso) => {
    const row = details.get(iso) || {};
    const leftRank = capacityTop.indexOf(iso);
    const rightRank = generationTop.indexOf(iso);
    const intensity = leftRank >= 0 && rightRank >= 0 ? Math.abs(leftRank - rightRank) * 18 + 24 : 88;
    return {
      key: iso,
      label: iso,
      sublabel: row.country,
      leftText: rankText(capacityTop, iso, "capacity"),
      rightText: rankText(generationTop, iso, "generation"),
      leftValue: `H ${formatFlexible(row.herfindahl_capacity)}`,
      rightValue: `H ${formatFlexible(row.herfindahl_generation)}`,
      note: `${row.top_fuel_capacity || "capacity fuel"} to ${row.top_fuel_generation || "generation fuel"}`,
      status: statusFromSets(capacityTop.includes(iso), generationTop.includes(iso)),
      intensity,
    };
  });

  return {
    kind: report.audit!.kind,
    stats: [
      { value: `${overlap}/5`, label: "top-five overlap" },
      { value: formatNumber(safeRows(data.rows_withheld_low_coverage).length), label: "low-coverage rows withheld" },
      { value: formatNumber(safeRows(data.rows_by_generation_herfindahl).length), label: "generation-ranked rows" },
    ],
    chartTitle: "Capacity rank is not enough. Generation coverage has to be visible.",
    chartDeck: "The bridge compares the top fuel concentration screen using installed capacity and using reported or modeled generation.",
    leftLabel: "Capacity screen",
    rightLabel: "Generation screen",
    rows,
    readouts: [
      { label: "Capacity top five", value: capacityTop.join(", ") },
      { label: "Generation top five", value: generationTop.join(", ") },
      { label: "Dropped on generation", value: strings(data.dropped_from_cluster_on_generation).join(", ") || "none" },
      { label: "Entered on generation", value: strings(data.entered_cluster_on_generation).join(", ") || "none" },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildMigrationModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const absoluteTop = strings(data.absolute_top5);
  const shareTop = strings(data.share_top5);
  const details = rowByIso(safeRows(data.rows_by_share));
  const rows = unique([...absoluteTop, ...shareTop]).map((iso) => {
    const row = details.get(iso) || {};
    const diff = Math.abs(numberValue(row.rank_absolute) - numberValue(row.rank_share));
    return {
      key: iso,
      label: iso,
      sublabel: row.country,
      leftText: row.rank_absolute ? `#${row.rank_absolute} absolute` : rankText(absoluteTop, iso, "absolute"),
      rightText: row.rank_share ? `#${row.rank_share} share` : rankText(shareTop, iso, "share"),
      leftValue: row.emigrant_stock_2024 ? formatNumber(row.emigrant_stock_2024) : undefined,
      rightValue: row.emigrant_pct_of_population ? formatPct(row.emigrant_pct_of_population, 1) : undefined,
      note: row.population_total ? `population ${formatNumber(row.population_total)}` : undefined,
      status: statusFromSets(absoluteTop.includes(iso), shareTop.includes(iso)),
      intensity: Math.max(30, Math.min(100, diff * 4)),
    };
  });

  return {
    kind: report.audit!.kind,
    stats: [
      { value: `${safeRows(data.survivors_in_both_top5).length}/5`, label: "absolute top-five survivors" },
      { value: formatPct(details.get(shareTop[0])?.emigrant_pct_of_population || 0, 1), label: `${shareTop[0]} emigrant share` },
      { value: formatNumber(safeRows(data.rows_by_share).length), label: "rankable origins" },
    ],
    chartTitle: "The denominator switch changes the story, not just the order.",
    chartDeck: "Absolute emigrant stock favors large origins; population share reveals small-economy exposure.",
    leftLabel: "Absolute stock",
    rightLabel: "Share of origin population",
    rows,
    readouts: [
      { label: "Absolute top five", value: absoluteTop.join(", ") },
      { label: "Population-share top five", value: shareTop.join(", ") },
      { label: "Dropped from headline", value: strings(data.dropped_from_top5_on_share).join(", ") },
      { label: "Entered after denominator switch", value: strings(data.entered_top5_on_share).join(", ") },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildMpiModel(report: ShowcaseReport, data: JsonValue): AuditModel {
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
      { value: formatNumber(safeRows(data.majority_ntl_blind_both_readings).length), label: "majority-blind in both readings" },
    ],
    chartTitle: "The satellite can illuminate places, but not all poverty dimensions.",
    chartDeck: "Each bar decomposes MPI weight into dimensions structurally blind or plausibly visible to nighttime radiance.",
    stackRows: rows,
    readouts: [
      { label: "Median blind dimension share", value: formatPct(data.median_ntl_blind_dim_pct, 1) },
      { label: "Mean blind indicator share", value: formatPct(data.mean_ntl_blind_ind_pct, 1) },
      { label: "Residual check", value: data.decomposition_residual_check?.rule || "dimension shares checked" },
      { label: "NTL data wall", value: String(data.ntl_data_wall || "Owner-gated VIIRS join not computed here.") },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data).concat(String(data.co_authorship || "")),
    generatedAt: data.generated_at,
  };
}

function buildCoastalModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const headlineTop = strings(data.headline_top5);
  const noPopTop = strings(data.nopop_top5);
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
    ],
    chartTitle: "Removing the size term lets the small-island signal appear.",
    chartDeck: "The bridge keeps the original population-scaled top set beside the no-population audit rank.",
    leftLabel: "Population-scaled screen",
    rightLabel: "No-population screen",
    rows,
    readouts: [
      { label: "Headline top five", value: headlineTop.join(", ") },
      { label: "No-population top five", value: noPopTop.join(", ") },
      { label: "Formula check", value: `max error ${formatFlexible(data.formula_check?.max_abs_error_recomputed_vs_committed)}` },
      { label: "Sensitivity note", value: strings(data.sensitivity_check?.top5_members_perturbation_can_move).join(", ") || "no movement listed" },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildFloodModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const rowsAll = safeRows(data.rows);
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

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatFlexible(data.b_strip_size_terms?.spearman_headline_vs_per_capita, 3), label: "Spearman vs per-capita rank" },
      { value: "0/4", label: "top-four survivors per capita" },
      { value: formatFlexible(data.what_the_index_correlates_with?.pearson_index_vs_raw_flood_count, 3), label: "correlation with raw flood count" },
    ],
    chartTitle: "Per-capita framing breaks the original flood-access top four.",
    chartDeck: "The audit contrasts the committed index with a per-capita-per-million version and exposes the event-count term.",
    leftLabel: "Committed proxy",
    rightLabel: "Per-capita alternative",
    rows,
    readouts: [
      { label: "Committed top four", value: committedTop.join(", ") },
      { label: "Per-capita top four", value: perCapTop.join(", ") },
      { label: "Dropped per capita", value: strings(data.b_strip_size_terms?.dropped_per_capita).join(", ") },
      { label: "Index reading", value: data.what_the_index_correlates_with?.reading || "size-and-reporting audit" },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildClimateHealthModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const cap = data.cap_saturation || {};
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

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatNumber(cap.n_pressure_saturated_cap22_5), label: "saturated at tighter cap" },
      { value: formatFlexible(cap.spearman_index_cap22_5_vs_labor_share, 3), label: "rank correlation with labor share" },
      { value: formatNumber(cap.rankable_dmcs), label: "rankable DMCs" },
    ],
    chartTitle: "Tighten the cap and the pressure index drifts toward labor share.",
    chartDeck: "Each lane shows the same economy under baseline PM2.5 cap, tighter cap, and outdoor-labor-share rank.",
    laneRows,
    readouts: [
      { label: "Baseline versus tight-cap Spearman", value: formatFlexible(cap.spearman_index_cap45_vs_cap22_5, 3) },
      { label: "Baseline versus labor-share Spearman", value: formatFlexible(cap.spearman_index_cap45_vs_labor_share, 3) },
      { label: "Denominator wall", value: data.denominator_correction?.wall_note || "labor-force denominator correction documented in artifact" },
      { label: "Parameter pair", value: `baseline cap ${formatFlexible(data.params?.baseline_cap)}; tight cap ${formatFlexible(data.params?.saturating_cap)}` },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildFoodCoverageModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const total = numberValue(data.roster_n);
  const years = Object.entries(data.common_vintage_runs || {}).map(([year, row]) => {
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

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatNumber(data.joint_universe_n), label: "joint indicator universe" },
      { value: formatNumber(droppedCount), label: "roster rows dropped by coverage" },
      { value: formatNumber(years.length), label: "common-vintage reruns" },
    ],
    chartTitle: "The first result is a coverage funnel, not a vulnerability ranking.",
    chartDeck: "The funnel shows how the roster narrows when CPI and agricultural-import legs both have to exist.",
    funnelRows: [
      { label: "ADB roster", value: total, total, note: "starting DMC/economy roster" },
      { label: "Have CPI leg", value: numberValue(data.have_cpi_n), total, note: "consumer price index available" },
      { label: "Have import leg", value: numberValue(data.have_imp_n), total, note: "agricultural-imports indicator available" },
      { label: "Have both legs", value: numberValue(data.joint_universe_n), total, note: "joint universe used by the screen" },
    ],
    coverageYears: years,
    readouts: [
      { label: "Dropped: imports but no CPI", value: strings(data.dropped_have_imp_no_cpi).join(", ") || "none" },
      { label: "Dropped: CPI but no imports", value: strings(data.dropped_have_cpi_no_imp).join(", ") || "none" },
      { label: "Dropped: neither leg", value: strings(data.dropped_neither).join(", ") || "none" },
      { label: "Common across committed N", value: strings(data.committed_common_across_N).join(", ") || "none" },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildSocialProtectionModel(report: ShowcaseReport, data: JsonValue): AuditModel {
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

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatNumber(data.excluded_for_missing_leg_count), label: "excluded rows outrank lowest headline" },
      { value: `${data.lowest_ranked_headline_member?.iso3 || "?"} #${data.lowest_ranked_headline_member?.value_rank || "?"}`, label: "lowest headline member by value rank" },
      { value: strings(data.imputation_variant?.entered_vs_headline).join(", ") || "none", label: "entered under imputation variant" },
    ],
    chartTitle: "Missing one leg can hide a higher-ranked economy.",
    chartDeck: "The ledger shows value rank before the headline filter removes one-legged observations.",
    leftLabel: "Value-ranked order",
    rightLabel: "Headline inclusion",
    rows,
    readouts: [
      { label: "Headline five", value: headline.join(", ") },
      { label: "Excluded but higher than lowest headline", value: safeRows(data.excluded_but_outrank_lowest_headline).map((row) => String(row.iso3)).join(", ") },
      { label: "Imputed top five", value: strings(data.imputation_variant?.imputed_top5).join(", ") },
      { label: "Dropped under imputation", value: strings(data.imputation_variant?.dropped_vs_headline).join(", ") || "none" },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildWaterModel(report: ShowcaseReport, data: JsonValue): AuditModel {
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

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatNumber(over.length), label: "above 100% internal denominator" },
      { value: `#${data.rural_counterfactual?.afg_rank_rural_dropped || "?"}`, label: "AFG rank without rural multiplier" },
      { value: strings(data.rural_counterfactual?.high_withdrawal_set).join(", "), label: "high-withdrawal set" },
    ],
    chartTitle: "The water signal is partly a denominator signal.",
    chartDeck: "Cards separate over-100-percent internal-water denominators from Afghanistan's rural-population multiplier effect.",
    componentCards: cards,
    readouts: [
      { label: "Baseline raw-index top four", value: strings(data.reproduced_baseline_top4_raw_index).join(", ") },
      { label: "Pre-registered headline top four", value: strings(data.prereg_headline_top4_intersection_of_top5).join(", ") },
      { label: "Top four when rural term is dropped", value: strings(data.rural_counterfactual?.top4_rural_dropped).join(", ") },
      { label: "Data walls", value: Object.values(data.data_walls || {}).join(" ") || "AQUASTAT and FAOSTAT extensions documented in artifact." },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildInvisibleUrbanizationModel(report: ShowcaseReport, data: JsonValue): AuditModel {
  const sweep = data.multiplier_sweep_is_rank_preserving || {};
  const boundary = data.genuine_falsification_not_run?.top5_boundary_pair || [];
  const shockPct = data.genuine_falsification_not_run?.input_shock_fraction_to_break_top5_boundary
    ? numberValue(data.genuine_falsification_not_run.input_shock_fraction_to_break_top5_boundary) * 100
    : 0;

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatFlexible(1, 1), label: "Spearman for scalar sweep" },
      { value: formatNumber(sweep.total_rank_inversions_across_sweep), label: "rank inversions across 5/10/15" },
      { value: formatPct(shockPct, 2), label: "shock to break top-five boundary" },
    ],
    chartTitle: "The robustness sweep preserves ranks because it only scales the same score.",
    chartDeck: "The lanes show identical top-five membership under positive scalar multipliers, then place the real input perturbation beside it.",
    laneRows: safeRows(sweep.results).map((row) => ({
      key: String(row.label),
      label: `multiplier ${row.multiplier}`,
      left: `Spearman ${formatFlexible(row.spearman_vs_baseline, 1)}`,
      middle: `${formatNumber(row.pairwise_rank_inversions_vs_baseline)} inversions`,
      right: strings(row.top5).join(", "),
      note: `top score ${formatFlexible(row.top1_score)}`,
      status: "survived",
    })) as LaneRow[],
    componentCards: [
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
    ],
    readouts: [
      { label: "Frozen formula", value: String(data.frozen_formula) },
      { label: "Baseline top five", value: strings(sweep.baseline_top5).join(", ") },
      { label: "All scalar Spearman equal one", value: String(Boolean(sweep.all_spearman_equal_one)) },
      { label: "Reproduction check", value: data.reproduces_committed_signal?.note || "committed column reproduced" },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
    generatedAt: data.generated_at,
  };
}

function buildPortModel(report: ShowcaseReport, data: JsonValue): AuditModel {
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

  return {
    kind: report.audit!.kind,
    stats: [
      { value: formatNumber(data.dmcs_reaching_cap_baseline), label: "DMCs reaching baseline cap" },
      { value: formatFlexible(data.max_proxy_observed, 3), label: "max observed proxy" },
      { value: `$${formatFlexible(data.imports_to_reach_cap_usd_trillions, 1)}T`, label: "imports needed to reach cap" },
    ],
    chartTitle: "A perturbed cap cannot test much if the observed data never touch it.",
    chartDeck: "The cap lanes keep the top five beside the number of rows that actually bind under each cap.",
    parameterRows: capRows,
    componentCards: [
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
    ],
    readouts: [
      { label: "Baseline top five", value: strings(data.baseline_top5).join(", ") },
      { label: "Committed-panel top five", value: strings(data.committed_panel_top5).join(", ") },
      { label: "Import-volume top five", value: strings(data.import_volume_top5).join(", ") },
      { label: "Volume top-five same order?", value: String(Boolean(data.friction_top5_equals_volume_top5_order)) },
    ],
    sourceFacts: sourceFacts(report, data),
    caveats: baseCaveats(report, data),
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
            <h2>Trust comes from the source trail, not the chart style.</h2>
            <p>
              The visual uses the generated artifact named below, and the
              caveats remain in the reading path. That keeps the emotional
              force of the chart tied to a reproducible source record.
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
  if (model.rows) {
    return <RankAuditVisual model={model} />;
  }
  if (model.stackRows) {
    return <StackedBlindnessVisual model={model} />;
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
    </div>
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
