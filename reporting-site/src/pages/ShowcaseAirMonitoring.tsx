import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface ZeroMonitorRow {
  iso3: string;
  country: string;
  subregion: string;
  population: number;
  pm25_exposure_ugm3: number;
  share_of_zero_monitor_pop: number;
  cumulative_share: number;
}

interface ResidualRow {
  iso3: string;
  country: string;
  subregion: string;
  population: number;
  pm25_locations: number;
  people_per_monitor: number;
  pm25_exposure_ugm3: number;
  gap_score: number;
  gdp_pc_year: number | null;
  gdp_pc_current_usd: number | null;
  log10_people_per_monitor_residual: number;
}

interface AirPanelRow {
  iso3: string;
  country: string;
  subregion: string;
  population: number;
  pm25_locations: number;
  pm25_exposure_ugm3: number;
  pm25_above_who_guideline_5_ugm3: boolean;
  pm25_observability_gap_score: number;
  pm25_observability_status: string;
}

interface AirPanelData {
  program: string;
  claim_scope: string;
  sources: {
    openaq_v3: string;
    wdi_pm25: string;
    who_aaq: string;
    retrieved_at: string;
  };
  rows: AirPanelRow[];
}

interface DeepeningData {
  program: string;
  analysis: string;
  claim_scope: string;
  source: {
    name: string;
    file: string;
    inputs: string;
    snapshot: string;
    license: string;
    development_confound_source?: {
      name: string;
      url: string;
      cache: string;
      retrieved_at: string;
      license: string;
    };
  };
  part_a_concentration: {
    zero_monitor_economy_count: number;
    zero_monitor_population_total: number;
    png_share: number;
    timor_share: number;
    png_plus_timor_share: number;
    rows: ZeroMonitorRow[];
    composite_caution: string;
  };
  part_b_confound: {
    wdi_gdp_per_capita_fetched: boolean;
    confound_partial_runnable_from_public_wdi_gdp: boolean;
    rank_correlations_descriptive_only: {
      spearman_gap_vs_pm25: number;
      spearman_gap_vs_log10_population: number;
      spearman_gap_vs_log10_people_per_monitor_withmon: number;
      spearman_log_people_per_monitor_vs_pm25_withmon: number;
      spearman_log_people_per_monitor_vs_log10_gdp_pc_withmon: number;
      spearman_gap_score_vs_log10_gdp_pc_withmon: number;
      spearman_pm25_vs_log10_gdp_pc_withmon: number;
      n_full_exposed_frame: number;
      n_with_monitor_frame: number;
      n_with_monitor_and_gdp_pc: number;
    };
    gdp_partial: {
      method: string;
      intercept: number;
      slope: number;
      all_residuals?: ResidualRow[];
      top_positive_residuals_more_people_per_monitor_than_gdp_predicts: ResidualRow[];
      top_negative_residuals_fewer_people_per_monitor_than_gdp_predicts: ResidualRow[];
      zero_monitor_economies_excluded_from_partial: Array<{
        iso3: string;
        country: string;
        population: number;
        pm25_exposure_ugm3: number;
        gdp_pc_year: number | null;
        gdp_pc_current_usd: number | null;
        partial_status: string;
      }>;
      interpretation_limit: string;
    };
    data_wall: string | null;
  };
  attestation_chain: string;
  generated_at: string;
}

type AirMode = "concentration" | "residual" | "exposure";

const MODES: Array<{ id: AirMode; label: string }> = [
  { id: "concentration", label: "Zero-monitor concentration" },
  { id: "residual", label: "GDP residuals" },
  { id: "exposure", label: "Exposure vs monitor count" },
];

function formatNumber(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function pct(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${(value * 100).toFixed(digits)}%`;
}

function signed(value: number | null | undefined, digits = 3) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value >= 0 ? "+" : ""}${value.toFixed(digits)}`;
}

function log10(value: number) {
  return Math.log(value) / Math.LN10;
}

function clamp(value: number, min: number, max: number) {
  return Math.max(min, Math.min(max, value));
}

function zeroByIso(rows: ZeroMonitorRow[], iso: string) {
  return rows.find((row) => row.iso3 === iso);
}

function residualByIso(rows: ResidualRow[], iso: string) {
  return rows.find((row) => row.iso3 === iso);
}

export default function ShowcaseAirMonitoring() {
  const [deepening, setDeepening] = useState<DeepeningData | null>(null);
  const [panel, setPanel] = useState<AirPanelData | null>(null);
  const [mode, setMode] = useState<AirMode>("concentration");
  const [focusIso, setFocusIso] = useState("PNG");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/programs/air-monitoring/generated/air-monitoring-concentration-deepening.json").then((r) => {
        if (!r.ok) throw new Error(`deepening HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-adb-panel.json").then((r) => {
        if (!r.ok) throw new Error(`panel HTTP ${r.status}`);
        return r.json();
      }),
    ])
      .then(([deepeningPayload, panelPayload]) => {
        setDeepening(deepeningPayload);
        setPanel(panelPayload);
      })
      .catch((err) => setError(String(err)));
  }, []);

  const zeroRows = deepening?.part_a_concentration.rows ?? [];
  const residualRows =
    deepening?.part_b_confound.gdp_partial.top_positive_residuals_more_people_per_monitor_than_gdp_predicts ?? [];
  const allResidualRows = useMemo(() => {
    if (!deepening) return [];
    const allRows = deepening.part_b_confound.gdp_partial.all_residuals;
    if (allRows && allRows.length > 0) return allRows;
    const positives = deepening.part_b_confound.gdp_partial.top_positive_residuals_more_people_per_monitor_than_gdp_predicts;
    const negatives = deepening.part_b_confound.gdp_partial.top_negative_residuals_fewer_people_per_monitor_than_gdp_predicts;
    const map = new Map<string, ResidualRow>();
    [...positives, ...negatives].forEach((row) => map.set(row.iso3, row));
    return Array.from(map.values());
  }, [deepening]);

  const focusZero = deepening ? zeroByIso(zeroRows, focusIso) : undefined;
  const focusResidual = residualByIso(residualRows, focusIso) || residualByIso(allResidualRows, focusIso);
  const focusPanel = panel?.rows.find((row) => row.iso3 === focusIso);
  const focusOptions = mode === "residual" ? residualRows : zeroRows;

  useEffect(() => {
    if (!deepening) return;
    if (mode === "residual" && !residualRows.some((row) => row.iso3 === focusIso)) {
      setFocusIso(residualRows[0]?.iso3 ?? "AZE");
    }
    if (mode !== "residual" && !zeroRows.some((row) => row.iso3 === focusIso)) {
      setFocusIso("PNG");
    }
  }, [deepening, focusIso, mode, residualRows, zeroRows]);

  return (
    <article className="showcase-page air-showcase">
      <header className="showcase-hero air-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            When the Monitor Gap Is Mostly Two Economies
          </h1>
          <p className="showcase-lede">
            The air-monitoring pass starts with a public-source observability
            problem: OpenAQ shows no public PM2.5 monitor for 13 ADB-region
            economies above the WHO annual guideline. The report asks whether
            that regional headline is really regional, then tests how much of
            the monitor-density pattern is explained by GDP per capita.
          </p>
          <div className="showcase-meta">
            <span>{deepening?.attestation_chain || "ai-first"}</span>
            <span>L2/L3 evidence sprint</span>
            <span>Observability screen, not a pollution ranking</span>
          </div>
        </div>
        <div className="showcase-hero-panel air-hero-panel" aria-label="Air-monitoring evidence summary">
          {deepening ? (
            <>
              <AirHeroConcentration data={deepening} />
              <div className="air-hero-stats">
                <div>
                  <span className="showcase-stat-value">
                    {deepening.part_a_concentration.zero_monitor_economy_count}
                  </span>
                  <span className="showcase-stat-label">zero-public-monitor economies above the WHO PM2.5 guideline</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {pct(deepening.part_a_concentration.png_plus_timor_share)}
                  </span>
                  <span className="showcase-stat-label">of that population is in Papua New Guinea and Timor-Leste</span>
                </div>
              </div>
            </>
          ) : (
            <p className="showcase-loading">{error || "Loading air-monitoring evidence..."}</p>
          )}
        </div>
      </header>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Measurement problem</p>
          <h2>The regional total hides the unit that matters.</h2>
          <p>
            A dashboard can say 13 economies have no public PM2.5 monitor
            visible in OpenAQ while exposure exceeds the WHO annual guideline.
            That is a useful starting point, but it is not yet a planning
            statement. Papua New Guinea alone carries nearly three quarters of
            the population in that zero-monitor group, while most remaining
            economies are small island states.
          </p>
        </div>
        <div className="showcase-note">
          <p>
            <strong>Data gap.</strong> OpenAQ is a public monitor-visibility
            source, not a complete regulatory inventory. WDI PM2.5 is a
            modeled exposure series. The report therefore treats the result as
            a public observability screen, not as proof that no monitor exists
            on the ground.
          </p>
        </div>
      </section>

      <section className="showcase-explorer">
        <div className="showcase-explorer-head">
          <div>
            <p className="kicker kicker-crimson">Interactive evidence view</p>
            <h2>Split the headline before using it.</h2>
            <p>
              The first view decomposes the zero-monitor population. The second
              view adds GDP per capita and asks which monitored economies have
              more people per public monitor than their income level predicts.
              The third view returns to the original observability panel.
            </p>
          </div>
          <div className="showcase-controls">
            {MODES.map((option) => (
              <button
                key={option.id}
                className={option.id === mode ? "active" : ""}
                onClick={() => setMode(option.id)}
                type="button"
              >
                {option.label}
              </button>
            ))}
            <label>
              Focus economy
              <select value={focusIso} onChange={(event) => setFocusIso(event.target.value)}>
                {focusOptions.map((row) => (
                  <option key={row.iso3} value={row.iso3}>
                    {row.country}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>

        <div className="air-evidence-grid">
          <div className="air-main-chart">
            {!deepening || !panel ? (
              <p className="showcase-loading">{error || "Loading chart data..."}</p>
            ) : mode === "concentration" ? (
              <ZeroMonitorChart rows={zeroRows} focusIso={focusIso} />
            ) : mode === "residual" ? (
              <GdpResidualChart
                rows={allResidualRows}
                positiveRows={residualRows}
                focusIso={focusIso}
                intercept={deepening.part_b_confound.gdp_partial.intercept}
                slope={deepening.part_b_confound.gdp_partial.slope}
              />
            ) : (
              <ExposureMonitorChart rows={panel.rows} focusIso={focusIso} />
            )}
          </div>
          <div className="air-side-panel">
            {mode === "concentration" ? (
              <ZeroMonitorPanel row={focusZero} deepening={deepening} />
            ) : mode === "residual" ? (
              <ResidualPanel row={focusResidual} deepening={deepening} />
            ) : (
              <ExposurePanel row={focusPanel} panel={panel} />
            )}
          </div>
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">What changed after deepening</p>
          <h2>The stronger question is not “who has the worst air.”</h2>
          <p>
            The upgraded sprint changes the frame. The zero-monitor total is a
            Papua New Guinea and Timor-Leste concentration story. Among
            monitored economies, GDP per capita explains a substantial part of
            public monitor density: the Spearman correlation between the
            gap-score and log GDP per capita is{" "}
            {deepening
              ? deepening.part_b_confound.rank_correlations_descriptive_only.spearman_gap_score_vs_log10_gdp_pc_withmon.toFixed(3)
              : "loading"}
            . The residual view is therefore a source-improvement list, not a
            league table.
          </p>
        </div>
        <div className="showcase-note">
          <p>
            <strong>Non-claim.</strong> The GDP residual is descriptive. It
            does not identify why a monitor network is thin, whether a monitor
            is regulatory grade, or how city-level exposure differs from the
            national WDI value.
          </p>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={6} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Operational use</p>
          <h2>Use it as a monitor-inventory QA list.</h2>
          <p>
            For a country team, regulator, or statistics office, this screen
            can prioritize where to audit public monitor inventories, classify
            monitor grade, and compare OpenAQ visibility with national
            regulator records. The next statistical upgrade is subnational:
            monitor catchments, gridded PM2.5, urban population exposure, and
            station metadata freshness.
          </p>
        </div>
        <div className="showcase-links">
          <a href="/programs/air-monitoring/generated/air-monitoring-concentration-deepening.json" download>
            Deepening JSON
          </a>
          <a href="/programs/air-monitoring/generated/air-monitoring-concentration-deepening.csv" download>
            Zero-monitor CSV
          </a>
          <a href="/programs/air-monitoring/generated/air-monitoring-adb-panel.json" download>
            Source panel JSON
          </a>
          <Link to="/air-monitoring?view=evidence">Program evidence</Link>
        </div>
      </section>
    </article>
  );
}

function AirHeroConcentration({ data }: { data: DeepeningData }) {
  const top = data.part_a_concentration.rows.slice(0, 3);
  const restShare = 1 - top.reduce((sum, row) => sum + row.share_of_zero_monitor_pop, 0);
  const segments = [
    ...top.map((row) => ({
      key: row.iso3,
      label: row.iso3,
      share: row.share_of_zero_monitor_pop,
      background: row.iso3 === "PNG" ? "#007db8" : row.iso3 === "TLS" ? "#5a8227" : "#fbb00e",
      color: row.iso3 === "FJI" ? "#212529" : "#ffffff",
    })),
    { key: "REST", label: "REST", share: Math.max(0, restShare), background: "#9b2226", color: "#ffffff" },
  ];
  let x = 0;
  return (
    <div className="air-hero-stack-wrap">
      <div className="air-hero-stack" aria-label="Zero-monitor population share">
        {segments.map((segment) => {
          const width = segment.share * 100;
          const style = {
            left: `${x}%`,
            width: `${width}%`,
            background: segment.background,
            color: segment.color,
          };
          x += width;
          return (
            <span key={segment.key} className={`air-stack-segment air-stack-${segment.key.toLowerCase()}`} style={style}>
              {segment.label}
            </span>
          );
        })}
      </div>
      <p>
        PNG is {pct(data.part_a_concentration.png_share)}. PNG + Timor-Leste
        is {pct(data.part_a_concentration.png_plus_timor_share)}.
      </p>
    </div>
  );
}

function ZeroMonitorChart({ rows, focusIso }: { rows: ZeroMonitorRow[]; focusIso: string }) {
  const width = 760;
  const rowH = 36;
  const margin = { top: 34, right: 110, bottom: 34, left: 150 };
  const height = margin.top + margin.bottom + rows.length * rowH;
  const x = (value: number) => margin.left + value * (width - margin.left - margin.right);

  return (
    <div className="air-chart-wrap">
      <svg className="air-zero-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Zero-monitor population concentration chart">
        <text x={margin.left} y={18} className="air-chart-title">
          Zero-monitor population share
        </text>
        <line x1={margin.left} x2={x(1)} y1={height - margin.bottom + 4} y2={height - margin.bottom + 4} className="air-axis" />
        {[0, 0.25, 0.5, 0.75, 1].map((tick) => (
          <g key={tick}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top - 8} y2={height - margin.bottom + 4} className="air-grid" />
            <text x={x(tick)} y={height - 10} textAnchor="middle" className="air-tick">
              {pct(tick, 0)}
            </text>
          </g>
        ))}
        {rows.map((row, index) => {
          const y = margin.top + index * rowH;
          const barW = Math.max(2, x(row.share_of_zero_monitor_pop) - margin.left);
          const isFocus = row.iso3 === focusIso;
          const isTop2 = row.iso3 === "PNG" || row.iso3 === "TLS";
          return (
            <g key={row.iso3} className={isFocus ? "is-focus" : ""}>
              <text x={margin.left - 12} y={y + 18} textAnchor="end" className="air-label">
                {row.iso3}
              </text>
              <rect
                x={margin.left}
                y={y + 4}
                width={barW}
                height={22}
                rx={2}
                className={isTop2 ? "air-zero-bar air-zero-top2" : "air-zero-bar"}
              />
              <circle cx={x(row.cumulative_share)} cy={y + 15} r={isFocus ? 5 : 3.5} className="air-cumulative-dot" />
              <text x={margin.left + barW + 8} y={y + 18} className="air-value">
                {pct(row.share_of_zero_monitor_pop)}
              </text>
            </g>
          );
        })}
        <text x={x(0.8351)} y={margin.top - 14} textAnchor="middle" className="air-callout">
          PNG + TLS = 83.5%
        </text>
      </svg>
    </div>
  );
}

function GdpResidualChart({
  rows,
  positiveRows,
  focusIso,
  intercept,
  slope,
}: {
  rows: ResidualRow[];
  positiveRows: ResidualRow[];
  focusIso: string;
  intercept: number;
  slope: number;
}) {
  const width = 780;
  const height = 480;
  const margin = { top: 34, right: 34, bottom: 58, left: 72 };
  const valid = rows.filter((row) => row.gdp_pc_current_usd && row.people_per_monitor > 0);
  const xs = valid.map((row) => log10(row.gdp_pc_current_usd || 1));
  const ys = valid.map((row) => log10(row.people_per_monitor));
  const xMin = Math.floor(Math.min(...xs) * 10) / 10;
  const xMax = Math.ceil(Math.max(...xs) * 10) / 10;
  const yMin = Math.floor(Math.min(...ys) * 10) / 10;
  const yMax = Math.ceil(Math.max(...ys) * 10) / 10;
  const x = (value: number) => margin.left + ((value - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
  const y = (value: number) => height - margin.bottom - ((value - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom);
  const topSet = new Set(positiveRows.slice(0, 5).map((row) => row.iso3));

  return (
    <div className="air-chart-wrap">
      <svg className="air-residual-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="GDP residual chart for public PM2.5 monitor density">
        <text x={margin.left} y={20} className="air-chart-title">
          Monitor density against GDP per capita
        </text>
        {[3, 4, 5].map((tick) => (
          <g key={`x-${tick}`}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={height - margin.bottom} className="air-grid" />
            <text x={x(tick)} y={height - 22} textAnchor="middle" className="air-tick">
              {tick === 3 ? "$1k" : tick === 4 ? "$10k" : "$100k"}
            </text>
          </g>
        ))}
        {[5, 6, 7].map((tick) => (
          <g key={`y-${tick}`}>
            <line x1={margin.left} x2={width - margin.right} y1={y(tick)} y2={y(tick)} className="air-grid" />
            <text x={margin.left - 10} y={y(tick) + 4} textAnchor="end" className="air-tick">
              {tick === 5 ? "100k" : tick === 6 ? "1M" : "10M"}
            </text>
          </g>
        ))}
        <line x1={margin.left} x2={width - margin.right} y1={height - margin.bottom} y2={height - margin.bottom} className="air-axis" />
        <line x1={margin.left} x2={margin.left} y1={margin.top} y2={height - margin.bottom} className="air-axis" />
        <line
          x1={x(xMin)}
          y1={y(intercept + slope * xMin)}
          x2={x(xMax)}
          y2={y(intercept + slope * xMax)}
          className="air-fit-line"
        />
        {valid.map((row) => {
          const px = x(log10(row.gdp_pc_current_usd || 1));
          const py = y(log10(row.people_per_monitor));
          const isFocus = row.iso3 === focusIso;
          const isTop = topSet.has(row.iso3);
          return (
            <g key={row.iso3}>
              <circle
                cx={px}
                cy={py}
                r={isFocus ? 8 : isTop ? 6 : 4}
                className={isTop ? "air-residual-point air-residual-top" : "air-residual-point"}
              />
              {(isFocus || isTop) && (
                <text x={px + 8} y={py - 8} className="air-point-label">
                  {row.iso3}
                </text>
              )}
            </g>
          );
        })}
        <text x={width / 2} y={height - 6} textAnchor="middle" className="air-axis-label">
          GDP per capita, current US$ (log scale)
        </text>
        <text transform={`translate(18 ${height / 2}) rotate(-90)`} textAnchor="middle" className="air-axis-label">
          people per public PM2.5 monitor (log scale)
        </text>
      </svg>
    </div>
  );
}

function ExposureMonitorChart({ rows, focusIso }: { rows: AirPanelRow[]; focusIso: string }) {
  const plotted = rows.filter((row) => row.population > 0 && row.pm25_exposure_ugm3 > 0);
  const width = 780;
  const height = 480;
  const margin = { top: 34, right: 38, bottom: 58, left: 70 };
  const xMin = 0;
  const xMax = 50;
  const yMin = -0.1;
  const yMax = 3.4;
  const x = (value: number) => margin.left + ((value - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
  const y = (locations: number) => {
    const logValue = locations === 0 ? 0 : log10(locations + 1);
    return height - margin.bottom - ((logValue - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom);
  };

  return (
    <div className="air-chart-wrap">
      <svg className="air-exposure-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="PM2.5 exposure versus public monitor count">
        <text x={margin.left} y={20} className="air-chart-title">
          Exposure versus public PM2.5 monitor count
        </text>
        {[5, 15, 30, 45].map((tick) => (
          <g key={`x-${tick}`}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={height - margin.bottom} className="air-grid" />
            <text x={x(tick)} y={height - 22} textAnchor="middle" className="air-tick">
              {tick}
            </text>
          </g>
        ))}
        {[0, 1, 2, 3].map((tick) => (
          <g key={`y-${tick}`}>
            <line x1={margin.left} x2={width - margin.right} y1={height - margin.bottom - ((tick - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom)} y2={height - margin.bottom - ((tick - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom)} className="air-grid" />
            <text x={margin.left - 10} y={height - margin.bottom - ((tick - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom) + 4} textAnchor="end" className="air-tick">
              {tick === 0 ? "0" : `10^${tick}`}
            </text>
          </g>
        ))}
        <line x1={x(5)} x2={x(5)} y1={margin.top} y2={height - margin.bottom} className="air-guide" />
        {plotted.map((row) => {
          const isZero = row.pm25_locations === 0;
          const isFocus = row.iso3 === focusIso;
          const radius = clamp(Math.sqrt(row.population) / 2200, 3.5, 16);
          return (
            <g key={row.iso3}>
              <circle
                cx={x(row.pm25_exposure_ugm3)}
                cy={y(row.pm25_locations)}
                r={isFocus ? radius + 3 : radius}
                className={isZero ? "air-exposure-point air-zero-point" : "air-exposure-point"}
              />
              {(isFocus || row.iso3 === "PNG" || row.iso3 === "TLS") && (
                <text
                  x={x(row.pm25_exposure_ugm3) + (row.iso3 === "TLS" ? 28 : 8)}
                  y={y(row.pm25_locations) + (row.iso3 === "TLS" ? 16 : -8)}
                  className="air-point-label"
                >
                  {row.iso3}
                </text>
              )}
            </g>
          );
        })}
        <text x={width / 2} y={height - 6} textAnchor="middle" className="air-axis-label">
          WDI PM2.5 exposure, micrograms per cubic meter
        </text>
        <text transform={`translate(18 ${height / 2}) rotate(-90)`} textAnchor="middle" className="air-axis-label">
          public PM2.5 monitor locations in OpenAQ (log count)
        </text>
      </svg>
    </div>
  );
}

function ZeroMonitorPanel({ row, deepening }: { row: ZeroMonitorRow | undefined; deepening: DeepeningData | null }) {
  if (!deepening || !row) return <p className="showcase-loading">Choose a zero-monitor economy.</p>;
  return (
    <>
      <p className="kicker kicker-blue">Selected zero-monitor economy</p>
      <h3>{row.country}</h3>
      <dl className="air-readout">
        <div>
          <dt>Population in zero-monitor group</dt>
          <dd>{formatNumber(row.population)}</dd>
        </div>
        <div>
          <dt>Share of zero-monitor population</dt>
          <dd>{pct(row.share_of_zero_monitor_pop)}</dd>
        </div>
        <div>
          <dt>PM2.5 exposure</dt>
          <dd>{row.pm25_exposure_ugm3.toFixed(1)} µg/m3</dd>
        </div>
        <div>
          <dt>Source snapshot</dt>
          <dd>{deepening.source.snapshot}</dd>
        </div>
      </dl>
      <p>
        The regional total is {formatNumber(deepening.part_a_concentration.zero_monitor_population_total)} people,
        but the first two rows account for {pct(deepening.part_a_concentration.png_plus_timor_share)} of it.
      </p>
    </>
  );
}

function ResidualPanel({ row, deepening }: { row: ResidualRow | undefined; deepening: DeepeningData | null }) {
  if (!deepening || !row) return <p className="showcase-loading">Choose a residual row.</p>;
  return (
    <>
      <p className="kicker kicker-blue">GDP-adjusted monitor-density residual</p>
      <h3>{row.country}</h3>
      <dl className="air-readout">
        <div>
          <dt>Residual</dt>
          <dd>{signed(row.log10_people_per_monitor_residual)}</dd>
        </div>
        <div>
          <dt>People per monitor</dt>
          <dd>{formatNumber(row.people_per_monitor)}</dd>
        </div>
        <div>
          <dt>GDP per capita</dt>
          <dd>${formatNumber(row.gdp_pc_current_usd, 0)} ({row.gdp_pc_year})</dd>
        </div>
        <div>
          <dt>PM2.5 exposure</dt>
          <dd>{row.pm25_exposure_ugm3.toFixed(1)} µg/m3</dd>
        </div>
      </dl>
      <p>
        Positive residuals mean the economy has more people per visible public
        PM2.5 monitor than the simple GDP-per-capita relationship predicts.
      </p>
    </>
  );
}

function ExposurePanel({ row, panel }: { row: AirPanelRow | undefined; panel: AirPanelData | null }) {
  if (!panel || !row) return <p className="showcase-loading">Choose an economy.</p>;
  return (
    <>
      <p className="kicker kicker-blue">Original observability panel</p>
      <h3>{row.country}</h3>
      <dl className="air-readout">
        <div>
          <dt>PM2.5 locations in OpenAQ</dt>
          <dd>{formatNumber(row.pm25_locations)}</dd>
        </div>
        <div>
          <dt>PM2.5 exposure</dt>
          <dd>{row.pm25_exposure_ugm3.toFixed(1)} µg/m3</dd>
        </div>
        <div>
          <dt>Gap score</dt>
          <dd>{formatNumber(row.pm25_observability_gap_score)}</dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>{row.pm25_observability_status.replaceAll("_", " ")}</dd>
        </div>
      </dl>
      <p>
        The score is a triage composite. It helps decide where to audit public
        monitor visibility; it is not an official assessment of air quality or
        monitoring performance.
      </p>
    </>
  );
}
