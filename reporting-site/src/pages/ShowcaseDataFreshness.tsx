import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface FreshnessCoverage {
  dmc_count: number;
  indicator_count: number;
  matrix_cells: number;
  missing_cells: number;
  protocol_review_cells: number;
  stale_cells_ge_3_years: number;
  source_context_counts: Record<string, number>;
}

interface IndicatorSummary {
  indicator_code: string;
  indicator_short: string;
  policy_surface: string;
  global_latest_reference_year: number;
  source_calendar_age_years: number;
  source_context: string;
  dmc_count: number;
  dmc_observed_count: number;
  dmc_missing_count: number;
  dmc_protocol_review_count: number;
  dmc_stale_count_ge_3_years: number;
  refresh_status_counts: Record<string, number>;
  median_relative_lag_years: number | null;
}

interface FreshnessRow {
  iso3: string;
  country: string;
  indicator_code: string;
  indicator_short: string;
  indicator_label: string;
  policy_surface: string;
  latest_year: number | null;
  indicator_global_latest_year: number;
  relative_lag_years: number | null;
  calendar_age_years: number | null;
  indicator_source_calendar_age_years: number;
  indicator_source_context: string;
  refresh_status:
    | "latest_for_indicator"
    | "one_reference_year_watch"
    | "protocol_review"
    | "stale_alert"
    | "missing_public_field";
  protocol_review_cell: boolean;
  value: number | null;
  missing: boolean;
  stale_ge_3_years: boolean;
}

interface FreshnessData {
  attestation_chain: string;
  status: string;
  decision: string;
  coverage: FreshnessCoverage;
  indicator_summary: IndicatorSummary[];
  rows: FreshnessRow[];
  sources: {
    world_bank_wdi_api: {
      name: string;
      license_note: string;
      records: Array<{
        code: string;
        label: string;
        policy_surface: string;
        api_lastupdated: string;
        global_latest_reference_year: number;
      }>;
    };
  };
  source_sanity: {
    unit: string;
    relative_lag: string;
    refresh_protocol: string;
    non_applicability_rule: string;
    important_caveat: string;
    use_limit: string;
  };
}

interface EconomySummary {
  iso3: string;
  country: string;
  missing: number;
  stale: number;
  protocolReview: number;
  observed: number;
  maxLag: number;
}

interface SelectedCell {
  row: FreshnessRow;
  country: string;
}

const SORT_OPTIONS = [
  { id: "signal", label: "Signal first" },
  { id: "alpha", label: "A-Z" },
] as const;

type SortOption = (typeof SORT_OPTIONS)[number]["id"];

function formatLag(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  if (value === 0) return "current";
  return `${value} year${value === 1 ? "" : "s"} behind`;
}

function cellFill(row: FreshnessRow | undefined) {
  if (!row || row.missing) return "#d7dde3";
  if (row.refresh_status === "latest_for_indicator") return "#007DB8";
  if (row.refresh_status === "one_reference_year_watch") return "#5A8227";
  if (row.refresh_status === "protocol_review") return "#FBB00E";
  return "#9b2226";
}

function cellText(row: FreshnessRow | undefined) {
  if (!row || row.missing) return "M";
  return String(row.latest_year ?? "M");
}

function formatStatus(status: FreshnessRow["refresh_status"] | undefined) {
  if (status === "latest_for_indicator") return "latest for indicator";
  if (status === "one_reference_year_watch") return "one-reference-year watch";
  if (status === "protocol_review") return "protocol review";
  if (status === "stale_alert") return "stale alert";
  return "missing public field";
}

export default function ShowcaseDataFreshness() {
  const [data, setData] = useState<FreshnessData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/topic-sprints/generated/wdi-data-freshness-sprint.json")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((payload: FreshnessData) => setData(payload))
      .catch((err) => setError(String(err)));
  }, []);

  const apiLastUpdated = data?.sources.world_bank_wdi_api.records[0]?.api_lastupdated;
  const mostStaleIndicator = data?.indicator_summary
    .slice()
    .sort((a, b) => b.dmc_stale_count_ge_3_years - a.dmc_stale_count_ge_3_years)[0];
  const mostProtocolIndicator = data?.indicator_summary
    .slice()
    .sort((a, b) => b.dmc_protocol_review_count - a.dmc_protocol_review_count)[0];
  const mostMissingIndicator = data?.indicator_summary
    .slice()
    .sort((a, b) => b.dmc_missing_count - a.dmc_missing_count)[0];
  const sourceContextSummary = data
    ? Object.entries(data.coverage.source_context_counts)
        .map(([label, count]) => `${count} ${label}`)
        .join("; ")
    : "";

  return (
    <article className="showcase-page">
      <header className="showcase-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            When Public Data Are Present but Stale
          </h1>
          <p className="showcase-lede">
            This WDI sprint asks a practical planning question: before a
            dashboard compares economies, can a reader see whether the public
            indicator itself is fresh, stale, or missing?
          </p>
          <div className="showcase-meta">
            <span>{data?.attestation_chain || "ai-first"}</span>
            <span>Program prospectus candidate</span>
            <span>Observability screen, not a ranking</span>
          </div>
        </div>
        <div className="showcase-hero-panel" aria-label="Report evidence summary">
          {data ? (
            <>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.matrix_cells}
                </span>
                <span className="showcase-stat-label">
                  DMC-indicator cells in the public matrix
                </span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.missing_cells}
                </span>
                <span className="showcase-stat-label">missing public fields</span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.stale_cells_ge_3_years}
                </span>
                <span className="showcase-stat-label">
                  strict stale-alert cells
                </span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.protocol_review_cells}
                </span>
                <span className="showcase-stat-label">
                  missing or lagged cells needing protocol review
                </span>
              </div>
            </>
          ) : (
            <span className="showcase-loading">
              {error ? `Could not load sprint JSON: ${error}` : "Loading evidence packet..."}
            </span>
          )}
        </div>
      </header>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">The data gap</p>
          <h2>A policy comparison can look precise while its source years differ.</h2>
          <p>
            WDI is a public workhorse for development dashboards, but a value
            can enter a chart without making its vintage visible. For planners,
            statisticians, and operations teams, the first question is not only
            what the value is. It is whether the value is recent enough for the
            decision being made.
          </p>
        </div>
      </section>

      {data && <FreshnessExplorer data={data} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The missingness is not the same as the staleness.</h2>
          <p>
            The matrix separates blank public fields from late public fields.
            It also compares each indicator with its own latest public
            reference year, so an indicator with an older global production
            cycle is not penalized simply because the whole series updates more
            slowly.
          </p>
        </div>
        <div className="showcase-fact-list">
          {mostStaleIndicator && (
            <div>
              <span>Strict stale-alert indicator</span>
              <strong>
                {mostStaleIndicator.indicator_short}:{" "}
                {mostStaleIndicator.dmc_stale_count_ge_3_years} cells at least
                three relative years behind
              </strong>
            </div>
          )}
          {mostProtocolIndicator && (
            <div>
              <span>Most protocol-review cells</span>
              <strong>
                {mostProtocolIndicator.indicator_short}:{" "}
                {mostProtocolIndicator.dmc_protocol_review_count} missing,
                protocol-review, or stale-alert cells
              </strong>
            </div>
          )}
          {mostMissingIndicator && (
            <div>
              <span>Most missing indicator in the sprint</span>
              <strong>
                {mostMissingIndicator.indicator_short}:{" "}
                {mostMissingIndicator.dmc_missing_count} missing public fields
              </strong>
            </div>
          )}
          {apiLastUpdated && (
            <div>
              <span>API metadata vintage</span>
              <strong>World Bank WDI source update date {apiLastUpdated}</strong>
            </div>
          )}
        </div>
      </section>

      {data && (
        <section className="showcase-section showcase-two-col">
          <div>
            <p className="kicker">Refresh protocol</p>
            <h2>The stricter layer separates source vintage from stale alerts.</h2>
            <p>
              The upgraded sprint keeps missing cells in a review lane rather
              than treating them as zero, and it does not infer
              non-applicability from memory. Observed cells are labeled latest,
              watch, protocol review, or stale alert against the indicator's
              own latest public reference year.
            </p>
          </div>
          <div className="showcase-fact-list">
            <div>
              <span>Protocol-review cells</span>
              <strong>
                {data.coverage.protocol_review_cells} cells are missing,
                two relative years behind, or strict stale alerts
              </strong>
            </div>
            <div>
              <span>Indicator source contexts</span>
              <strong>{sourceContextSummary}</strong>
            </div>
            <div>
              <span>Non-applicability rule</span>
              <strong>{data.source_sanity.non_applicability_rule}</strong>
            </div>
          </div>
        </section>
      )}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What this does not mean</p>
          <h2>A stale WDI cell is not a verdict on an economy.</h2>
          <p>
            A missing or old public WDI value can reflect methodology,
            source-publication cycles, non-applicability, model vintage, or
            how the API releases a series. This report prototype does not rate
            statistical agencies. It shows where a future program should add
            source-specific refresh rules before using a dashboard result.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Reproduce the sprint</p>
          <code>python research/topic-sprints/scripts/sprint-wdi-data-freshness.py</code>
          <a href="/topic-sprints/generated/wdi-data-freshness-sprint.json" download>
            Download sprint JSON
          </a>
          <a href="/topic-sprints/generated/wdi-data-freshness-sprint.csv" download>
            Download sprint CSV
          </a>
          <a href="/topic-sprints/reports/wdi-data-freshness-sprint.md" target="_blank" rel="noreferrer">
            Read sprint note
          </a>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={2} />

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">Operational use</p>
          <h2>Freshness labels can change how a dashboard is read.</h2>
          <p>
            An ADB sector team or a DMC statistics office could use this kind
            of matrix as a source QA layer: flag stale dashboard fields, decide
            which indicators need source-specific refresh notes, and avoid
            treating missing public cells as substantive development results.
          </p>
        </div>
        <div className="showcase-source-box">
          <Link to="/showcase">Market-climate prototype</Link>
          <Link to="/factory">Factory rules</Link>
          <Link to="/status">Research status</Link>
        </div>
      </section>
    </article>
  );
}

function FreshnessExplorer({ data }: { data: FreshnessData }) {
  const [sortMode, setSortMode] = useState<SortOption>("signal");
  const [selectedIndicatorCode, setSelectedIndicatorCode] = useState(() => {
    return (
      data.indicator_summary
        .slice()
        .sort((a, b) => b.dmc_stale_count_ge_3_years - a.dmc_stale_count_ge_3_years)[0]
        ?.indicator_code || data.indicator_summary[0]?.indicator_code
    );
  });
  const [selectedCell, setSelectedCell] = useState<SelectedCell | null>(null);

  const rowsByKey = useMemo(() => {
    const map = new Map<string, FreshnessRow>();
    for (const row of data.rows) map.set(`${row.iso3}:${row.indicator_code}`, row);
    return map;
  }, [data.rows]);

  const economySummaries = useMemo(() => {
    const byIso = new Map<string, EconomySummary>();
    for (const row of data.rows) {
      const current = byIso.get(row.iso3) || {
        iso3: row.iso3,
        country: row.country,
        missing: 0,
        stale: 0,
        protocolReview: 0,
        observed: 0,
        maxLag: 0,
      };
      if (row.missing) current.missing += 1;
      else current.observed += 1;
      if (row.stale_ge_3_years) current.stale += 1;
      if (row.protocol_review_cell) current.protocolReview += 1;
      if (row.relative_lag_years !== null) {
        current.maxLag = Math.max(current.maxLag, row.relative_lag_years);
      }
      byIso.set(row.iso3, current);
    }
    const summaries = Array.from(byIso.values());
    if (sortMode === "alpha") {
      return summaries.sort((a, b) => a.country.localeCompare(b.country));
    }
    return summaries.sort((a, b) => {
      const signalA = a.missing * 100 + a.protocolReview * 30 + a.stale * 25 + a.maxLag;
      const signalB = b.missing * 100 + b.protocolReview * 30 + b.stale * 25 + b.maxLag;
      return signalB - signalA || a.country.localeCompare(b.country);
    });
  }, [data.rows, sortMode]);

  const selectedIndicator =
    data.indicator_summary.find((item) => item.indicator_code === selectedIndicatorCode) ||
    data.indicator_summary[0];
  const selectedColumnRows = data.rows.filter(
    (row) => row.indicator_code === selectedIndicator.indicator_code,
  );
  const strongestCell =
    selectedCell ||
    selectedColumnRows
      .slice()
      .sort((a, b) => {
        const scoreA = Number(a.missing) * 100 + Number(a.protocol_review_cell) * 35 + Number(a.stale_ge_3_years) * 30 + (a.relative_lag_years || 0);
        const scoreB = Number(b.missing) * 100 + Number(b.protocol_review_cell) * 35 + Number(b.stale_ge_3_years) * 30 + (b.relative_lag_years || 0);
        return scoreB - scoreA;
      })
      .map((row) => ({ row, country: row.country }))[0];

  return (
    <section className="showcase-section showcase-explorer">
      <div className="showcase-explorer-head">
        <div>
          <p className="kicker">Interactive evidence view</p>
          <h2>Read the source vintage before reading the value.</h2>
          <p>
            Each cell is one ADB DMC by one WDI indicator. The color encodes
            the protocol status: latest, one-reference-year watch, protocol
            review, stale alert, or missing public field.
          </p>
        </div>
        <div className="showcase-controls" aria-label="Freshness matrix controls">
          <div className="showcase-filter-buttons" role="group" aria-label="Sort matrix">
            {SORT_OPTIONS.map((option) => (
              <button
                key={option.id}
                type="button"
                className={sortMode === option.id ? "showcase-control-active" : ""}
                onClick={() => setSortMode(option.id)}
              >
                {option.label}
              </button>
            ))}
          </div>
          <label>
            <span>Focus indicator</span>
            <select
              value={selectedIndicatorCode}
              onChange={(event) => {
                setSelectedIndicatorCode(event.target.value);
                setSelectedCell(null);
              }}
            >
              {data.indicator_summary.map((indicator) => (
                <option key={indicator.indicator_code} value={indicator.indicator_code}>
                  {indicator.indicator_short}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      <div className="freshness-matrix-wrap">
        <FreshnessMatrix
          rowsByKey={rowsByKey}
          economies={economySummaries}
          indicators={data.indicator_summary}
          selectedIndicatorCode={selectedIndicator.indicator_code}
          onSelectCell={(row, country) => setSelectedCell({ row, country })}
        />
      </div>

      <div className="freshness-legend" aria-label="Freshness color legend">
        <span><i style={{ background: "#007DB8" }} /> Latest</span>
        <span><i style={{ background: "#5A8227" }} /> Watch</span>
        <span><i style={{ background: "#FBB00E" }} /> Protocol review</span>
        <span><i style={{ background: "#9b2226" }} /> Stale alert</span>
        <span><i style={{ background: "#d7dde3" }} /> Missing</span>
      </div>

      <div className="showcase-month-readout">
        <div>
          <span>Focus indicator</span>
          <strong>
            {selectedIndicator.indicator_short}: latest public reference year{" "}
            {selectedIndicator.global_latest_reference_year};{" "}
            {selectedIndicator.source_context}
          </strong>
        </div>
        <div>
          <span>Column summary</span>
          <strong>
            {selectedIndicator.dmc_observed_count} observed,{" "}
            {selectedIndicator.dmc_missing_count} missing,{" "}
            {selectedIndicator.dmc_protocol_review_count} protocol-review,{" "}
            {selectedIndicator.dmc_stale_count_ge_3_years} stale-alert
          </strong>
        </div>
        <div>
          <span>Selected cell</span>
          <strong>
            {strongestCell
              ? `${strongestCell.country}: ${strongestCell.row.missing
                  ? "missing public field"
                  : `${strongestCell.row.latest_year}, ${formatLag(strongestCell.row.relative_lag_years)}, ${formatStatus(strongestCell.row.refresh_status)}`}`
              : "Select a cell"}
          </strong>
        </div>
      </div>
    </section>
  );
}

function FreshnessMatrix({
  rowsByKey,
  economies,
  indicators,
  selectedIndicatorCode,
  onSelectCell,
}: {
  rowsByKey: Map<string, FreshnessRow>;
  economies: EconomySummary[];
  indicators: IndicatorSummary[];
  selectedIndicatorCode: string;
  onSelectCell: (row: FreshnessRow, country: string) => void;
}) {
  const labelWidth = 188;
  const cellWidth = 74;
  const cellHeight = 20;
  const headerHeight = 54;
  const width = labelWidth + indicators.length * cellWidth + 18;
  const height = headerHeight + economies.length * cellHeight + 16;
  const selectedIndex = indicators.findIndex(
    (indicator) => indicator.indicator_code === selectedIndicatorCode,
  );

  return (
    <svg
      className="freshness-matrix"
      role="img"
      aria-label="WDI freshness matrix by ADB DMC and indicator"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Latest public reference year by indicator
      </text>
      {indicators.map((indicator, columnIndex) => {
        const x = labelWidth + columnIndex * cellWidth + cellWidth / 2;
        return (
          <g key={indicator.indicator_code}>
            <text
              x={x}
              y={35}
              textAnchor="middle"
              className="freshness-matrix-column"
            >
              {indicator.indicator_short}
            </text>
            <text
              x={x}
              y={49}
              textAnchor="middle"
              className="freshness-matrix-code"
            >
              {indicator.global_latest_reference_year}
            </text>
          </g>
        );
      })}
      {economies.map((economy, rowIndex) => {
        const y = headerHeight + rowIndex * cellHeight;
        return (
          <g key={economy.iso3}>
            <text x={0} y={y + 13} className="showcase-heatmap-label">
              {economy.iso3} {economy.country}
            </text>
            {indicators.map((indicator, columnIndex) => {
              const row = rowsByKey.get(`${economy.iso3}:${indicator.indicator_code}`);
              const x = labelWidth + columnIndex * cellWidth;
              const selected = indicator.indicator_code === selectedIndicatorCode;
              return (
                <g key={`${economy.iso3}-${indicator.indicator_code}`}>
                  <rect
                    x={x}
                    y={y}
                    width={cellWidth - 3}
                    height={cellHeight - 2}
                    rx={1.5}
                    fill={cellFill(row)}
                    className={selected ? "freshness-cell freshness-cell-selected" : "freshness-cell"}
                    onMouseEnter={() => row && onSelectCell(row, economy.country)}
                    onClick={() => row && onSelectCell(row, economy.country)}
                  >
                    <title>
                      {row
                        ? `${economy.country}, ${indicator.indicator_short}: ${
                            row.missing
                              ? "missing public field"
                              : `${row.latest_year}, ${formatLag(row.relative_lag_years)}, ${formatStatus(row.refresh_status)}`
                          }`
                        : `${economy.country}, ${indicator.indicator_short}: missing`}
                    </title>
                  </rect>
                  <text
                    x={x + (cellWidth - 3) / 2}
                    y={y + 12.5}
                    textAnchor="middle"
                    className={row?.missing ? "freshness-cell-label freshness-cell-label-missing" : "freshness-cell-label"}
                    pointerEvents="none"
                  >
                    {cellText(row)}
                  </text>
                </g>
              );
            })}
          </g>
        );
      })}
      {selectedIndex >= 0 && (
        <rect
          x={labelWidth + selectedIndex * cellWidth - 1}
          y={headerHeight - 2}
          width={cellWidth - 1}
          height={economies.length * cellHeight + 1}
          fill="none"
          className="showcase-heatmap-column"
        />
      )}
    </svg>
  );
}
