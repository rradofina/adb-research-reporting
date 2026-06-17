import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface FlowCoverageFlag {
  iso3: string;
  country: string;
  matched_rpw_corridors: number;
  flow_coverage_share: number;
}

interface FlowRow {
  iso3: string;
  country: string;
  wdi_remittance_pct_gdp: number | null;
  wdi_year: number | null;
  rpw_period: string | null;
  rpw_corridors_observed: number;
  matched_rpw_corridors: number;
  total_knomad_inbound_flow_usd_million: number | null;
  matched_flow_usd_million: number | null;
  flow_coverage_share: number | null;
  quote_mean_cost_pct: number | null;
  quote_median_cost_pct: number | null;
  flow_weighted_mean_cost_pct: number | null;
  flow_minus_quote_cost_pct: number | null;
  fragility_quote_mean: number | null;
  fragility_flow_weighted: number | null;
  quote_rank: number | null;
  flow_weighted_rank: number | null;
}

interface FlowData {
  attestation_chain: string;
  goal_level: string;
  hook: string;
  status: string;
  decision: string;
  created_at: string;
  sources: {
    rpw: { name: string; version: string; url: string; local_file: string };
    knomad: { name: string; indicator: string; year: number; url: string; local_file: string };
    wdi: { name: string; local_file: string };
  };
  method: {
    unit: string;
    cost_statistics: string[];
    flow_units: string;
    normalization_note: string;
  };
  source_sanity: {
    rpw: string;
    knomad: string;
    wdi: string;
    use_limit: string;
  };
  coverage: {
    latest_rpw_period: string;
    rpw_corridors_latest_period: number;
    matched_rpw_corridors: number;
    unmatched_rpw_corridors: number;
    low_matched_flow_coverage_flags_lt_25pct: FlowCoverageFlag[];
  };
  ranking_test: {
    quote_top5: string[];
    flow_weighted_top5: string[];
    dropped_from_top5_after_flow_weighting: string[];
    entered_top5_after_flow_weighting: string[];
  };
  rows: FlowRow[];
  missing_corridors: Array<{ source_iso3: string; dest_iso3: string; source: string; dest: string }>;
}

interface MedianData {
  headline_top5_mean: string[];
  robust_top5_median_quote: string[];
  robust_top5_median_corridor: string[];
  dropped_on_median_quote: string[];
  entered_on_median_quote: string[];
  panel_negative_quotes: number;
  panel_total_quotes: number;
  rows_by_frag_mean: Array<{
    iso3: string;
    country: string;
    mean_cost: number;
    median_quote: number;
    median_corr: number;
    n_corridors: number;
    n_quotes: number;
    n_neg_quotes: number;
  }>;
}

interface SensitivityRun {
  label: string;
  top10: Array<{ iso3: string; country: string; fragility: number }>;
}

interface SensitivityData {
  generated_at: string;
  common_top5_across_runs: string[];
  runs: SensitivityRun[];
}

type MetricMode = "delta" | "rank" | "coverage";

const METRIC_OPTIONS: Array<{ id: MetricMode; label: string }> = [
  { id: "delta", label: "Flow-cost delta" },
  { id: "rank", label: "Rank movement" },
  { id: "coverage", label: "Coverage risk" },
];

const BASELINE_TOP5 = new Set(["KGZ", "NPL", "TON", "VUT", "WSM"]);

function formatNumber(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function pct(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value.toFixed(digits)}%`;
}

function share(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${(value * 100).toFixed(digits)}%`;
}

function pp(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value >= 0 ? "+" : ""}${value.toFixed(digits)} pp`;
}

function hasCosts(row: FlowRow) {
  return row.quote_mean_cost_pct !== null && row.flow_weighted_mean_cost_pct !== null;
}

function rowByIso(rows: FlowRow[], iso: string) {
  return rows.find((row) => row.iso3 === iso);
}

function compactSet(items: string[] | undefined) {
  return items && items.length > 0 ? items.join(", ") : "none";
}

export default function ShowcaseRemittanceFlow() {
  const [flow, setFlow] = useState<FlowData | null>(null);
  const [median, setMedian] = useState<MedianData | null>(null);
  const [sensitivity, setSensitivity] = useState<SensitivityData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/programs/remittance-resilience/generated/remittance-flow-weighting-sprint.json").then((r) => {
        if (!r.ok) throw new Error(`flow HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/remittance-resilience/generated/remittance-median-deepening.json").then((r) => {
        if (!r.ok) throw new Error(`median HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/remittance-resilience/sensitivity-runs.json").then((r) => {
        if (!r.ok) throw new Error(`sensitivity HTTP ${r.status}`);
        return r.json();
      }),
    ])
      .then(([flowPayload, medianPayload, sensitivityPayload]) => {
        setFlow(flowPayload);
        setMedian(medianPayload);
        setSensitivity(sensitivityPayload);
      })
      .catch((err) => setError(String(err)));
  }, []);

  const nepal = flow ? rowByIso(flow.rows, "NPL") : undefined;
  const vanuatu = flow ? rowByIso(flow.rows, "VUT") : undefined;
  const matchedLabel = flow
    ? `${flow.coverage.matched_rpw_corridors}/${flow.coverage.rpw_corridors_latest_period}`
    : "";

  return (
    <article className="showcase-page">
      <header className="showcase-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            When Every Corridor Is Not the Same Corridor
          </h1>
          <p className="showcase-lede">
            The repaired remittance pass joins World Bank RPW Q1 2025 corridor
            price quotes to World Bank/KNOMAD 2021 bilateral remittance-flow
            estimates. The report asks a measurement question before it asks a
            policy question: what changes when observed corridors are weighted
            by estimated flows rather than counted equally?
          </p>
          <div className="showcase-meta">
            <span>{flow?.attestation_chain || "ai-first"}</span>
            <span>L3 repair pass in progress</span>
            <span>Flow-weighted sensitivity, not a risk rating</span>
          </div>
        </div>
        <div className="showcase-hero-panel remittance-hero-panel" aria-label="Remittance evidence summary">
          {flow ? (
            <>
              <RemittanceHeroRanks data={flow} />
              <div className="remittance-hero-stats">
                <div>
                  <span className="showcase-stat-value">{matchedLabel}</span>
                  <span className="showcase-stat-label">latest-period RPW corridors matched to KNOMAD flows</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {flow.ranking_test.flow_weighted_top5.length}/5
                  </span>
                  <span className="showcase-stat-label">baseline top-five economies still in the flow-weighted top five</span>
                </div>
              </div>
            </>
          ) : (
            <span className="showcase-loading">
              {error ? `Could not load remittance artifacts: ${error}` : "Loading evidence packet..."}
            </span>
          )}
        </div>
      </header>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">The data gap</p>
          <h2>RPW sees quoted corridors, not household exposure.</h2>
          <p>
            Remittance price data are observed by corridor and firm. Counting
            every observed corridor equally is transparent, but it can
            overstate small corridors and understate corridors carrying more
            estimated flows. The source upgrade does not solve the household
            exposure problem. It makes the weighting assumption visible.
          </p>
        </div>
      </section>

      {flow && <RemittanceExplorer data={flow} sensitivity={sensitivity} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The set survives flow weighting, but the story changes inside it.</h2>
          <p>
            The flow-weighted top five contain the same five economies as the
            equal-weighted screen, but their ordering changes. Nepal moves
            upward because matched higher-flow corridors carry higher observed
            costs in the sprint; Vanuatu also rises. That is the report hook:
            the finding is about the cost measure, not a generic remittance
            dependence leaderboard.
          </p>
        </div>
        <div className="showcase-fact-list">
          {nepal && (
            <div>
              <span>Nepal after flow weighting</span>
              <strong>
                {pct(nepal.quote_mean_cost_pct, 1)} equal-weighted cost to{" "}
                {pct(nepal.flow_weighted_mean_cost_pct, 1)} flow-weighted cost;{" "}
                rank {nepal.quote_rank} to {nepal.flow_weighted_rank}
              </strong>
            </div>
          )}
          {vanuatu && (
            <div>
              <span>Vanuatu after flow weighting</span>
              <strong>
                {pct(vanuatu.quote_mean_cost_pct, 1)} equal-weighted cost to{" "}
                {pct(vanuatu.flow_weighted_mean_cost_pct, 1)} flow-weighted cost;{" "}
                rank {vanuatu.quote_rank} to {vanuatu.flow_weighted_rank}
              </strong>
            </div>
          )}
          {median && (
            <div>
              <span>Median-cost check</span>
              <strong>
                Median-over-quotes top five: {compactSet(median.robust_top5_median_quote)};{" "}
                entries changed: {compactSet(median.entered_on_median_quote)}
              </strong>
            </div>
          )}
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What this does not mean</p>
          <h2>This is not a household remittance-price estimate.</h2>
          <p>
            KNOMAD flows are 2021 analytic estimates, while RPW prices are Q1
            2025 quotes. The join does not observe which providers households
            used, which fee schedule applied, or whether a corridor's matched
            flow coverage captures the whole market. Four economies in the
            sprint have matched-flow coverage below 25 percent and need source
            validation before any stronger claim.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Reproduce the repair pass</p>
          <code>python remittance-resilience/scripts/process-remittance.py</code>
          <code>python remittance-resilience/scripts/sprint-flow-weighted-cost.py</code>
          <a href="/programs/remittance-resilience/generated/remittance-flow-weighting-sprint.json" download>
            Download flow-weighting JSON
          </a>
          <a href="/programs/remittance-resilience/generated/remittance-flow-weighting-sprint.csv" download>
            Download flow-weighting CSV
          </a>
          <Link to="/remittance-resilience?view=evidence">
            Read remittance evidence packet
          </Link>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={5} />

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">Operational use</p>
          <h2>Use the weighting screen to choose corridors for validation.</h2>
          <p>
            A central bank, statistics office, or ADB country team could use
            this screen to identify where quoted costs, flow concentration, and
            coverage uncertainty point to a small validation sample. The next
            data investment is corridor-level verification, not a composite
            country ranking.
          </p>
        </div>
        <div className="showcase-source-box">
          <Link to="/showcase">Market-climate prototype</Link>
          <Link to="/showcase/data-freshness">Data-freshness prototype</Link>
          <Link to="/showcase/shock-payment-rails">Shock-payment prototype</Link>
          <Link to="/showcase/psdq-source-disagreement">PSDQ prototype</Link>
          <Link to="/factory">Factory rules</Link>
        </div>
      </section>
    </article>
  );
}

function RemittanceHeroRanks({ data }: { data: FlowData }) {
  const rows = data.ranking_test.flow_weighted_top5
    .map((iso) => rowByIso(data.rows, iso))
    .filter((row): row is FlowRow => Boolean(row && row.quote_rank && row.flow_weighted_rank));
  const width = 300;
  const height = 188;
  const leftX = 78;
  const rightX = 218;
  const y = (rank: number) => 42 + (rank - 1) * 27;

  return (
    <div className="remittance-hero-ranks">
      <p className="showcase-source-title">Equal-weighted rank to flow-weighted rank</p>
      <svg
        className="remittance-rank-svg"
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        role="img"
        aria-label="Top five rank changes after flow weighting"
      >
        <text x={leftX} y={18} textAnchor="middle" className="remit-axis-title">Equal</text>
        <text x={rightX} y={18} textAnchor="middle" className="remit-axis-title">Flow</text>
        <line x1={leftX} y1={30} x2={leftX} y2={160} className="remit-rank-axis" />
        <line x1={rightX} y1={30} x2={rightX} y2={160} className="remit-rank-axis" />
        {[1, 2, 3, 4, 5].map((rank) => (
          <g key={rank}>
            <text x={leftX - 16} y={y(rank) + 4} textAnchor="end" className="remit-tick">{rank}</text>
            <text x={rightX + 16} y={y(rank) + 4} className="remit-tick">{rank}</text>
          </g>
        ))}
        {rows.map((row) => {
          const selected = row.iso3 === "NPL" || row.iso3 === "VUT";
          const y1 = y(row.quote_rank || 1);
          const y2 = y(row.flow_weighted_rank || 1);
          return (
            <g key={row.iso3}>
              <path
                d={`M ${leftX} ${y1} C ${leftX + 42} ${y1}, ${rightX - 42} ${y2}, ${rightX} ${y2}`}
                className={selected ? "remit-rank-line remit-rank-line-selected" : "remit-rank-line"}
              />
              <circle cx={leftX} cy={y1} r={5} className={selected ? "remit-rank-dot-selected" : "remit-rank-dot"} />
              <circle cx={rightX} cy={y2} r={5} className={selected ? "remit-rank-dot-selected" : "remit-rank-dot"} />
              <text x={rightX + 29} y={y2 + 4} className={selected ? "remit-rank-label remit-rank-label-selected" : "remit-rank-label"}>
                {row.iso3}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function RemittanceExplorer({
  data,
  sensitivity,
}: {
  data: FlowData;
  sensitivity: SensitivityData | null;
}) {
  const plotRows = useMemo(() => data.rows.filter(hasCosts), [data.rows]);
  const [selectedIso, setSelectedIso] = useState("NPL");
  const [metric, setMetric] = useState<MetricMode>("delta");
  const selectedRow = rowByIso(data.rows, selectedIso) || rowByIso(data.rows, "NPL") || plotRows[0];

  return (
    <section className="showcase-section showcase-explorer">
      <div className="showcase-explorer-head">
        <div>
          <p className="kicker">Interactive evidence view</p>
          <h2>Make the weighting assumption visible.</h2>
          <p>
            The scatter compares equal-weighted RPW corridor cost with the
            KNOMAD-flow-weighted cost. The side panel switches between cost
            delta, rank movement, and low matched-flow coverage.
          </p>
        </div>
        <div className="showcase-controls" aria-label="Remittance explorer controls">
          <div className="showcase-filter-buttons remittance-filter-buttons" role="group" aria-label="Select remittance metric">
            {METRIC_OPTIONS.map((option) => (
              <button
                key={option.id}
                type="button"
                className={metric === option.id ? "showcase-control-active" : ""}
                onClick={() => setMetric(option.id)}
              >
                {option.label}
              </button>
            ))}
          </div>
          <label>
            <span>Focus economy</span>
            <select value={selectedIso} onChange={(event) => setSelectedIso(event.target.value)}>
              {plotRows
                .slice()
                .sort((a, b) => a.country.localeCompare(b.country))
                .map((row) => (
                  <option key={row.iso3} value={row.iso3}>
                    {row.country}
                  </option>
                ))}
            </select>
          </label>
        </div>
      </div>

      <div className="remittance-visual-grid">
        <div className="remittance-chart-wrap">
          <FlowScatter rows={plotRows} selectedIso={selectedRow?.iso3} onSelect={setSelectedIso} />
        </div>
        <div className="remittance-chart-wrap">
          <FlowSidePanel rows={plotRows} mode={metric} selectedIso={selectedRow?.iso3} onSelect={setSelectedIso} />
        </div>
      </div>

      <div className="freshness-legend remittance-legend" aria-label="Remittance chart legend">
        <span><i style={{ background: "#007DB8" }} /> Repaired baseline top five</span>
        <span><i style={{ background: "#9b2226" }} /> Matched-flow coverage below 25%</span>
        <span><i style={{ background: "#FBB00E" }} /> Selected economy</span>
        <span><i style={{ background: "#e5edf3" }} /> Other rankable DMCs</span>
      </div>

      <div className="showcase-month-readout">
        <div>
          <span>Selected economy</span>
          <strong>
            {selectedRow
              ? `${selectedRow.country}: remittances ${pct(selectedRow.wdi_remittance_pct_gdp, 1)} of GDP (${selectedRow.wdi_year || "year missing"})`
              : "Select an economy"}
          </strong>
        </div>
        <div>
          <span>Equal-weighted versus flow-weighted cost</span>
          <strong>
            {selectedRow
              ? `${pct(selectedRow.quote_mean_cost_pct, 1)} to ${pct(selectedRow.flow_weighted_mean_cost_pct, 1)} (${pp(selectedRow.flow_minus_quote_cost_pct, 1)})`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Matched-flow coverage</span>
          <strong>
            {selectedRow
              ? `${share(selectedRow.flow_coverage_share, 1)} coverage; ${selectedRow.matched_rpw_corridors}/${selectedRow.rpw_corridors_observed} observed corridors matched`
              : "missing"}
          </strong>
        </div>
      </div>

      {sensitivity && <SensitivityStrip data={sensitivity} selectedIso={selectedRow?.iso3} />}

      <p className="remittance-method-note">
        Source method: {data.method.normalization_note} RPW costs are public
        quoted corridor prices; KNOMAD flows are 2021 estimates in US$ million.
        Missing RPW corridor-flow joins in this sprint:{" "}
        {data.missing_corridors.map((row) => `${row.source_iso3}->${row.dest_iso3}`).join(", ")}.
      </p>
    </section>
  );
}

function FlowScatter({
  rows,
  selectedIso,
  onSelect,
}: {
  rows: FlowRow[];
  selectedIso?: string;
  onSelect: (iso3: string) => void;
}) {
  const width = 640;
  const height = 440;
  const margin = { top: 36, right: 34, bottom: 62, left: 68 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const maxValue = Math.ceil(
    Math.max(
      12,
      ...rows.map((row) => Math.max(row.quote_mean_cost_pct || 0, row.flow_weighted_mean_cost_pct || 0)),
    ) / 5,
  ) * 5;
  const maxFlow = Math.max(1, ...rows.map((row) => row.matched_flow_usd_million || 0));
  const x = (value: number) => margin.left + (value / maxValue) * plotWidth;
  const y = (value: number) => margin.top + (1 - value / maxValue) * plotHeight;
  const radius = (flow: number | null) => 5 + (Math.log10((flow || 0) + 1) / Math.log10(maxFlow + 1)) * 15;
  const ticks = Array.from({ length: Math.floor(maxValue / 5) + 1 }, (_, index) => index * 5);
  const labelRows = new Set([
    ...rows
      .filter((row) => BASELINE_TOP5.has(row.iso3))
      .map((row) => row.iso3),
    selectedIso || "",
    "MMR",
    "MYS",
  ]);

  return (
    <svg
      className="remittance-flow-scatter"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Equal-weighted versus flow-weighted remittance corridor costs"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Equal-weighted cost and flow-weighted cost
      </text>
      <line x1={margin.left} y1={margin.top} x2={margin.left} y2={margin.top + plotHeight} className="shock-axis" />
      <line x1={margin.left} y1={margin.top + plotHeight} x2={margin.left + plotWidth} y2={margin.top + plotHeight} className="shock-axis" />
      <line x1={x(0)} y1={y(0)} x2={x(maxValue)} y2={y(maxValue)} className="remit-diagonal" />
      {ticks.map((tick) => (
        <g key={tick}>
          <line x1={margin.left} x2={margin.left + plotWidth} y1={y(tick)} y2={y(tick)} className="shock-grid" />
          <line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={margin.top + plotHeight} className="shock-grid" />
          <text x={margin.left - 10} y={y(tick) + 4} textAnchor="end" className="showcase-heatmap-year">
            {tick}%
          </text>
          <text x={x(tick)} y={margin.top + plotHeight + 19} textAnchor="middle" className="showcase-heatmap-year">
            {tick}%
          </text>
        </g>
      ))}
      <text x={margin.left + plotWidth / 2} y={height - 15} textAnchor="middle" className="shock-axis-label">
        Equal-weighted mean RPW cost, Q1 2025
      </text>
      <text x={18} y={margin.top + plotHeight / 2} textAnchor="middle" className="shock-axis-label" transform={`rotate(-90 18 ${margin.top + plotHeight / 2})`}>
        KNOMAD-flow-weighted mean RPW cost
      </text>
      <text x={x(maxValue) - 4} y={y(maxValue) + 14} textAnchor="end" className="remit-diagonal-label">
        no change line
      </text>
      {rows.map((row) => {
        const selected = row.iso3 === selectedIso;
        const lowCoverage = (row.flow_coverage_share || 0) < 0.25;
        const top5 = BASELINE_TOP5.has(row.iso3);
        const cx = x(row.quote_mean_cost_pct || 0);
        const cy = y(row.flow_weighted_mean_cost_pct || 0);
        return (
          <g key={row.iso3}>
            <circle
              cx={cx}
              cy={cy}
              r={radius(row.matched_flow_usd_million)}
              fill={selected ? "#FBB00E" : lowCoverage ? "#9b2226" : top5 ? "#007DB8" : "#e5edf3"}
              stroke={selected ? "#7a4d00" : top5 ? "#003f5f" : lowCoverage ? "#5a1114" : "#6b879d"}
              strokeWidth={selected ? 3 : top5 || lowCoverage ? 1.5 : 1}
              opacity={selected || top5 || lowCoverage ? 0.95 : 0.78}
              className="remit-point"
              onMouseEnter={() => onSelect(row.iso3)}
              onClick={() => onSelect(row.iso3)}
            >
              <title>
                {`${row.country}: equal ${pct(row.quote_mean_cost_pct, 2)}, flow-weighted ${pct(row.flow_weighted_mean_cost_pct, 2)}, coverage ${share(row.flow_coverage_share, 1)}`}
              </title>
            </circle>
            {labelRows.has(row.iso3) && (
              <text
                x={cx + radius(row.matched_flow_usd_million) + 5}
                y={cy + 4}
                className={selected ? "shock-label shock-label-selected" : "shock-label"}
              >
                {row.iso3}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

function FlowSidePanel({
  rows,
  mode,
  selectedIso,
  onSelect,
}: {
  rows: FlowRow[];
  mode: MetricMode;
  selectedIso?: string;
  onSelect: (iso3: string) => void;
}) {
  if (mode === "rank") {
    return <FlowRankChart rows={rows} selectedIso={selectedIso} onSelect={onSelect} />;
  }
  return <FlowBars rows={rows} mode={mode} selectedIso={selectedIso} onSelect={onSelect} />;
}

function FlowBars({
  rows,
  mode,
  selectedIso,
  onSelect,
}: {
  rows: FlowRow[];
  mode: Exclude<MetricMode, "rank">;
  selectedIso?: string;
  onSelect: (iso3: string) => void;
}) {
  const width = 440;
  const rowHeight = 27;
  const margin = { top: 52, right: 56, bottom: 26, left: 58 };
  const displayRows =
    mode === "delta"
      ? rows
          .slice()
          .sort((a, b) => Math.abs(b.flow_minus_quote_cost_pct || 0) - Math.abs(a.flow_minus_quote_cost_pct || 0))
          .slice(0, 13)
      : rows
          .slice()
          .sort((a, b) => (a.flow_coverage_share || 0) - (b.flow_coverage_share || 0))
          .slice(0, 13);
  const height = margin.top + displayRows.length * rowHeight + margin.bottom;
  const plotWidth = width - margin.left - margin.right;
  const values = displayRows.map((row) =>
    mode === "delta" ? row.flow_minus_quote_cost_pct || 0 : row.flow_coverage_share || 0,
  );
  const minValue = mode === "delta" ? Math.min(-7, ...values) : 0;
  const maxValue = mode === "delta" ? Math.max(5, ...values) : 1;
  const x = (value: number) => margin.left + ((value - minValue) / (maxValue - minValue)) * plotWidth;
  const zeroX = x(0);
  const title = mode === "delta" ? "Flow-weighted cost minus equal-weighted cost" : "Lowest matched-flow coverage";
  const subtitle = mode === "delta" ? "Percentage-point difference; sorted by absolute movement" : "Share of KNOMAD inbound flow represented by matched RPW corridors";

  return (
    <svg
      className="remittance-flow-bars"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label={title}
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        {title}
      </text>
      <text x={0} y={35} className="showcase-heatmap-year">
        {subtitle}
      </text>
      {mode === "delta" && <line x1={zeroX} x2={zeroX} y1={margin.top - 8} y2={height - margin.bottom + 2} className="remit-zero-line" />}
      {mode === "coverage" && <line x1={x(0.25)} x2={x(0.25)} y1={margin.top - 8} y2={height - margin.bottom + 2} className="remit-threshold-line" />}
      {displayRows.map((row, index) => {
        const y = margin.top + index * rowHeight;
        const value = mode === "delta" ? row.flow_minus_quote_cost_pct || 0 : row.flow_coverage_share || 0;
        const selected = row.iso3 === selectedIso;
        const lowCoverage = (row.flow_coverage_share || 0) < 0.25;
        const barX = mode === "delta" ? Math.min(zeroX, x(value)) : margin.left;
        const barWidth = mode === "delta" ? Math.abs(x(value) - zeroX) : x(value) - margin.left;
        return (
          <g key={row.iso3}>
            <text x={0} y={y + 14} className={selected ? "remit-bar-label remit-bar-label-selected" : "remit-bar-label"}>
              {row.iso3}
            </text>
            <rect x={margin.left} y={y} width={plotWidth} height={17} fill="#eef2f5" />
            <rect
              x={barX}
              y={y}
              width={Math.max(1, barWidth)}
              height={17}
              fill={selected ? "#FBB00E" : lowCoverage ? "#9b2226" : value >= 0 ? "#007DB8" : "#5A8227"}
              className="shock-gap-bar"
              onMouseEnter={() => onSelect(row.iso3)}
              onClick={() => onSelect(row.iso3)}
            >
              <title>{`${row.country}: ${mode === "delta" ? pp(value, 2) : share(value, 1)}`}</title>
            </rect>
            <text x={width - 6} y={y + 14} textAnchor="end" className="shock-gap-value">
              {mode === "delta" ? pp(value, 1) : share(value, 0)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function FlowRankChart({
  rows,
  selectedIso,
  onSelect,
}: {
  rows: FlowRow[];
  selectedIso?: string;
  onSelect: (iso3: string) => void;
}) {
  const displayRows = rows
    .filter((row) => row.quote_rank !== null && row.flow_weighted_rank !== null)
    .sort((a, b) => (a.flow_weighted_rank || 99) - (b.flow_weighted_rank || 99))
    .slice(0, 12);
  const width = 440;
  const height = 410;
  const leftX = 118;
  const rightX = 300;
  const top = 48;
  const rowGap = 27;
  const y = (rank: number) => top + (rank - 1) * rowGap;

  return (
    <svg
      className="remittance-rank-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Rank movement after flow weighting"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Rank movement after weighting
      </text>
      <text x={0} y={35} className="showcase-heatmap-year">
        Lower rank number is higher in the screen; top 12 by flow-weighted rank
      </text>
      <text x={leftX} y={62} textAnchor="middle" className="remit-axis-title">Equal</text>
      <text x={rightX} y={62} textAnchor="middle" className="remit-axis-title">Flow</text>
      <line x1={leftX} x2={leftX} y1={top + 20} y2={height - 20} className="remit-rank-axis" />
      <line x1={rightX} x2={rightX} y1={top + 20} y2={height - 20} className="remit-rank-axis" />
      {displayRows.map((row) => {
        const selected = row.iso3 === selectedIso;
        const top5 = BASELINE_TOP5.has(row.iso3);
        const y1 = y(row.quote_rank || 1) + 36;
        const y2 = y(row.flow_weighted_rank || 1) + 36;
        return (
          <g
            key={row.iso3}
            className="remit-rank-row"
            onMouseEnter={() => onSelect(row.iso3)}
            onClick={() => onSelect(row.iso3)}
          >
            <path
              d={`M ${leftX} ${y1} C ${leftX + 70} ${y1}, ${rightX - 70} ${y2}, ${rightX} ${y2}`}
              className={selected ? "remit-rank-line remit-rank-line-selected" : top5 ? "remit-rank-line remit-rank-line-top5" : "remit-rank-line"}
            />
            <circle cx={leftX} cy={y1} r={5} className={selected ? "remit-rank-dot-selected" : "remit-rank-dot"} />
            <circle cx={rightX} cy={y2} r={5} className={selected ? "remit-rank-dot-selected" : "remit-rank-dot"} />
            <text x={leftX - 12} y={y1 + 4} textAnchor="end" className="remit-tick">
              {row.quote_rank}
            </text>
            <text x={rightX + 12} y={y2 + 4} className="remit-tick">
              {row.flow_weighted_rank}
            </text>
            <text x={rightX + 45} y={y2 + 4} className={selected ? "remit-rank-label remit-rank-label-selected" : "remit-rank-label"}>
              {row.iso3}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function SensitivityStrip({
  data,
  selectedIso,
}: {
  data: SensitivityData;
  selectedIso?: string;
}) {
  const common = new Set(data.common_top5_across_runs);
  const width = 930;
  const rowHeight = 30;
  const labelWidth = 170;
  const cellWidth = 58;
  const height = 48 + data.runs.length * rowHeight + 14;

  return (
    <div className="remittance-sensitivity-wrap">
      <svg
        className="remittance-sensitivity-strip"
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        role="img"
        aria-label="Repaired sensitivity top-five composition by run"
      >
        <text x={0} y={18} className="showcase-heatmap-title">
          Repaired sensitivity composition
        </text>
        <text x={0} y={36} className="showcase-heatmap-year">
          Common across all rows: {data.common_top5_across_runs.join(", ")}. Nepal is not in the common core after parser repair.
        </text>
        {data.runs.map((run, rowIndex) => {
          const y = 50 + rowIndex * rowHeight;
          const topFive = run.top10.slice(0, 5);
          return (
            <g key={run.label}>
              <text x={0} y={y + 16} className="showcase-heatmap-label">
                {run.label}
              </text>
              {topFive.map((item, cellIndex) => {
                const selected = item.iso3 === selectedIso;
                const inCommon = common.has(item.iso3);
                const isNepal = item.iso3 === "NPL";
                const isPak = item.iso3 === "PAK";
                return (
                  <g key={`${run.label}-${item.iso3}`}>
                    <rect
                      x={labelWidth + cellIndex * cellWidth}
                      y={y}
                      width={cellWidth - 4}
                      height={21}
                      rx={2}
                      fill={selected ? "#FBB00E" : inCommon ? "#007DB8" : isNepal ? "#f7c948" : isPak ? "#9b2226" : "#d7dde3"}
                      opacity={selected || inCommon ? 0.95 : 0.78}
                    />
                    <text
                      x={labelWidth + cellIndex * cellWidth + (cellWidth - 4) / 2}
                      y={y + 14}
                      textAnchor="middle"
                      className={selected || inCommon || isPak ? "remit-sensitivity-cell-light" : "remit-sensitivity-cell"}
                    >
                      {item.iso3}
                    </text>
                  </g>
                );
              })}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
