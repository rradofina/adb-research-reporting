import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

interface SprintCoverage {
  raw_price_rows_kept: number;
  market_count_before_selection: number;
  selected_market_count: number;
  selected_market_month_cells: number;
  rows_with_price_and_lagged_precipitation: number;
  dry_price_spike_screen_count: number;
  commodity: string;
  unit: string;
  price_years: [number, number];
}

interface Market {
  market_id: string;
  market: string;
  admin1: string;
  admin2: string;
  latitude: number;
  longitude: number;
  observed_months: number;
}

interface MarketClimateRow {
  market_id: string;
  market: string;
  month: string;
  retail_price_npr: number | null;
  price_anomaly_pct: number | null;
  lagged_precipitation_z: number | null;
  dry_price_spike_screen: boolean;
}

interface SprintData {
  attestation_chain: string;
  status: string;
  decision: string;
  coverage: SprintCoverage;
  selected_markets: Market[];
  rows: MarketClimateRow[];
  inputs: {
    hdx_package: {
      price_resource: { url: string; last_modified: string };
      market_resource: { url: string; last_modified: string };
    };
    nasa_power: { base_url: string };
  };
  triage_summaries: {
    top_price_spikes: MarketClimateRow[];
    dry_price_spike_screen_top12: MarketClimateRow[];
  };
}

const REPORT_BATCH = [
  {
    title: "Market-level climate price transmission",
    status: "Prototype report in progress",
    path: "research/topic-sprints/nepal-market-climate-prices-sprint.md",
    href: "/showcase",
  },
  {
    title: "Public data freshness blind spots",
    status: "Prototype report at /showcase/data-freshness",
    path: "research/topic-sprints/wdi-data-freshness-sprint.md",
    href: "/showcase/data-freshness",
  },
  {
    title: "Shock-payment rails after disasters",
    status: "Prototype report at /showcase/shock-payment-rails",
    path: "research/topic-sprints/shock-payment-rails-sprint.md",
    href: "/showcase/shock-payment-rails",
  },
  {
    title: "Remittance corridors after flow weighting",
    status: "Prototype report at /showcase/remittance-flow-weighting",
    path: "remittance-resilience/l2-flow-weighting-sprint.md",
    href: "/showcase/remittance-flow-weighting",
  },
  {
    title: "Public service data quality source disagreement",
    status: "Prototype report at /showcase/psdq-source-disagreement",
    path: "public-service-data-quality/STATUS.md",
    href: "/showcase/psdq-source-disagreement",
  },
  {
    title: "Air-monitoring observability",
    status: "Prototype report at /showcase/air-monitoring-observability",
    path: "air-monitoring/deepened-results.md",
    href: "/showcase/air-monitoring-observability",
  },
  {
    title: "Access map-completeness audit",
    status: "Prototype report at /showcase/access-map-completeness",
    path: "access-services/deepened-results.md",
    href: "/showcase/access-map-completeness",
  },
];

function pct(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value.toFixed(digits)}%`;
}

function colorPrice(value: number | null) {
  if (value === null || Number.isNaN(value)) return "#e5e7eb";
  const v = Math.max(-30, Math.min(30, value));
  if (v >= 0) {
    const t = v / 30;
    return mix("#f7f7f7", "#a50026", t);
  }
  const t = Math.abs(v) / 30;
  return mix("#f7f7f7", "#005f8c", t);
}

function colorRain(value: number | null) {
  if (value === null || Number.isNaN(value)) return "#e5e7eb";
  const v = Math.max(-2.5, Math.min(2.5, value));
  if (v >= 0) return mix("#f7f7f7", "#00695c", v / 2.5);
  return mix("#f7f7f7", "#9c6b02", Math.abs(v) / 2.5);
}

function mix(a: string, b: string, t: number) {
  const pa = parseHex(a);
  const pb = parseHex(b);
  const clamped = Math.max(0, Math.min(1, t));
  const c = pa.map((x, i) => Math.round(x + (pb[i] - x) * clamped));
  return `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
}

function parseHex(hex: string) {
  const clean = hex.replace("#", "");
  return [
    parseInt(clean.slice(0, 2), 16),
    parseInt(clean.slice(2, 4), 16),
    parseInt(clean.slice(4, 6), 16),
  ];
}

export default function Showcase() {
  const [data, setData] = useState<SprintData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/topic-sprints/generated/nepal-market-climate-prices-sprint.json")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((payload: SprintData) => setData(payload))
      .catch((err) => setError(String(err)));
  }, []);

  const topSpike = data?.triage_summaries.top_price_spikes[0];
  const drySpike = data?.triage_summaries.dry_price_spike_screen_top12[0];

  return (
    <article className="showcase-page">
      <header className="showcase-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title">
            When Food Prices Spike, Is the Weather Local?
          </h1>
          <p className="showcase-lede">
            A market-month sprint for Nepal joins WFP rice prices with NASA
            POWER precipitation at market coordinates. The first report asks a
            measured question: which spikes align with local climate anomalies,
            and which look broader than weather?
          </p>
          <div className="showcase-meta">
            <span>{data?.attestation_chain || "ai-first"}</span>
            <span>Program prospectus candidate</span>
            <span>Not a causal claim</span>
          </div>
        </div>
        <div className="showcase-hero-panel" aria-label="Report evidence summary">
          {data ? (
            <>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.selected_market_count}
                </span>
                <span className="showcase-stat-label">markets</span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.rows_with_price_and_lagged_precipitation}
                </span>
                <span className="showcase-stat-label">joined market-months</span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.dry_price_spike_screen_count}
                </span>
                <span className="showcase-stat-label">dry-spike screen cells</span>
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
          <h2>National CPI cannot show the geography of a price shock.</h2>
          <p>
            The policy question is not whether a national food-price index
            moved. For operations teams and statistical users, the question is
            where a price spike appears, whether the local climate record moved
            before it, and what alternative explanations must be ruled out
            before the result is used.
          </p>
        </div>
      </section>

      {data && <MarketClimateExplorer data={data} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The broad price wave is visible before any model is fitted.</h2>
          <p>
            The evidence screen shows synchronized rice price anomalies across
            many markets in 2023-2025, while the precipitation panel remains
            more local and uneven. That contrast is the hook: the next program
            should test local climate alignment against broader market and
            macro explanations.
          </p>
        </div>
        <div className="showcase-fact-list">
          {topSpike && (
            <div>
              <span>Largest price anomaly in the sprint table</span>
              <strong>
                {topSpike.market}, {topSpike.month}:{" "}
                {pct(topSpike.price_anomaly_pct, 1)}
              </strong>
            </div>
          )}
          {drySpike && (
            <div>
              <span>Strongest dry-spike screen example</span>
              <strong>
                {drySpike.market}, {drySpike.month}: rain z{" "}
                {drySpike.lagged_precipitation_z?.toFixed(2)}
              </strong>
            </div>
          )}
          <div>
            <span>Source status</span>
            <strong>Public HDX + NASA POWER APIs; caches synced into the evidence path</strong>
          </div>
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What this does not mean</p>
          <h2>The report does not claim that weather caused the price spikes.</h2>
          <p>
            NASA POWER is modeled point climate data, WFP market rows have
            missing months, and this sprint uses one rice series. A publication
            candidate needs commodity expansion, rainfall-source comparison,
            exchange-rate and import-price checks, fuel-price context, and
            market-access falsifiers.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Reproduce the sprint</p>
          <code>python research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py</code>
          <a href="/topic-sprints/generated/nepal-market-climate-prices-sprint.json" download>
            Download sprint JSON
          </a>
          <a href="/topic-sprints/generated/nepal-market-climate-prices-sprint.csv" download>
            Download sprint CSV
          </a>
          <a href="/topic-sprints/reports/nepal-market-climate-prices-sprint.md" target="_blank" rel="noreferrer">
            Read sprint note
          </a>
        </div>
      </section>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">Showcase queue</p>
          <h2>First batch: five candidates, five prototype surfaces.</h2>
          <p>
            The showcase is deliberately batch-based. Reports enter only after
            the evidence package, visual concept, caveats, and visual QA are
            strong enough to make a reader-facing surface defensible.
          </p>
        </div>
        <div className="showcase-queue">
          {REPORT_BATCH.map((item, index) => (
            <div className="showcase-queue-row" key={item.title}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>
                {item.href ? <Link to={item.href}>{item.title}</Link> : item.title}
              </strong>
              <em>{item.status}</em>
              <code>{item.path}</code>
            </div>
          ))}
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">Portfolio rule</p>
          <h2>Beauty is a gate, not a substitute for evidence.</h2>
          <p>
            This surface is only a prototype report. It promotes no maturity
            label. The next loop must test the falsifiers and harden the
            sources before the result can become a full ADB/ERDI-aligned report
            slot.
          </p>
        </div>
        <div className="showcase-source-box">
          <Link to="/factory">Factory rules</Link>
          <Link to="/status">Research status</Link>
          <Link to="/docs">Governance documents</Link>
        </div>
      </section>
    </article>
  );
}

function MarketClimateExplorer({ data }: { data: SprintData }) {
  const months = useMemo(
    () => Array.from(new Set(data.rows.map((row) => row.month))).sort(),
    [data.rows],
  );
  const [selectedIndex, setSelectedIndex] = useState(() =>
    Math.max(0, months.indexOf("2024-05")),
  );
  const [playing, setPlaying] = useState(false);
  const selectedMonth = months[selectedIndex] || months[0];

  useEffect(() => {
    if (!playing || months.length === 0) return;
    const id = window.setInterval(() => {
      setSelectedIndex((current) => (current + 1) % months.length);
    }, 900);
    return () => window.clearInterval(id);
  }, [playing, months.length]);

  const rowsByMarketMonth = useMemo(() => {
    const map = new Map<string, MarketClimateRow>();
    for (const row of data.rows) map.set(`${row.market_id}:${row.month}`, row);
    return map;
  }, [data.rows]);

  const selectedRows = useMemo(() => {
    return data.selected_markets
      .map((market) => rowsByMarketMonth.get(`${market.market_id}:${selectedMonth}`))
      .filter((row): row is MarketClimateRow => Boolean(row));
  }, [data.selected_markets, rowsByMarketMonth, selectedMonth]);

  const highestPrice = selectedRows
    .filter((row) => row.price_anomaly_pct !== null)
    .sort((a, b) => (b.price_anomaly_pct || 0) - (a.price_anomaly_pct || 0))[0];
  const driest = selectedRows
    .filter((row) => row.lagged_precipitation_z !== null)
    .sort((a, b) => (a.lagged_precipitation_z || 0) - (b.lagged_precipitation_z || 0))[0];

  return (
    <section className="showcase-section showcase-explorer">
      <div className="showcase-explorer-head">
        <div>
          <p className="kicker">Interactive evidence view</p>
          <h2>Scrub the same market-month table the sprint generated.</h2>
          <p>
            The top panel is rice price anomaly. The bottom panel is
            previous-month precipitation anomaly. The highlighted column is the
            selected month.
          </p>
        </div>
        <div className="showcase-controls" aria-label="Heatmap controls">
          <button type="button" onClick={() => setPlaying((v) => !v)}>
            {playing ? "Pause" : "Play"}
          </button>
          <label>
            <span>{selectedMonth}</span>
            <input
              type="range"
              min={0}
              max={Math.max(0, months.length - 1)}
              value={selectedIndex}
              onChange={(event) => {
                setSelectedIndex(Number(event.target.value));
                setPlaying(false);
              }}
            />
          </label>
        </div>
      </div>

      <div className="showcase-heatmap-wrap">
        <EvidenceHeatmap
          rowsByMarketMonth={rowsByMarketMonth}
          markets={data.selected_markets}
          months={months}
          selectedMonth={selectedMonth}
          field="price_anomaly_pct"
          title="Rice price anomaly, percent above/below market-month median"
          color={colorPrice}
        />
        <EvidenceHeatmap
          rowsByMarketMonth={rowsByMarketMonth}
          markets={data.selected_markets}
          months={months}
          selectedMonth={selectedMonth}
          field="lagged_precipitation_z"
          title="Previous-month precipitation anomaly, z-score at market point"
          color={colorRain}
        />
      </div>

      <div className="showcase-month-readout">
        <div>
          <span>Selected month</span>
          <strong>{selectedMonth}</strong>
        </div>
        <div>
          <span>Highest rice price anomaly</span>
          <strong>
            {highestPrice
              ? `${highestPrice.market}: ${pct(highestPrice.price_anomaly_pct, 1)}`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Driest lagged precipitation signal</span>
          <strong>
            {driest
              ? `${driest.market}: z ${driest.lagged_precipitation_z?.toFixed(2)}`
              : "missing"}
          </strong>
        </div>
      </div>
    </section>
  );
}

function EvidenceHeatmap({
  rowsByMarketMonth,
  markets,
  months,
  selectedMonth,
  field,
  title,
  color,
}: {
  rowsByMarketMonth: Map<string, MarketClimateRow>;
  markets: Market[];
  months: string[];
  selectedMonth: string;
  field: "price_anomaly_pct" | "lagged_precipitation_z";
  title: string;
  color: (value: number | null) => string;
}) {
  const labelWidth = 104;
  const cellWidth = 11;
  const cellHeight = 18;
  const titleHeight = 28;
  const width = labelWidth + months.length * cellWidth + 10;
  const height = titleHeight + markets.length * cellHeight + 24;
  const selectedX = labelWidth + months.indexOf(selectedMonth) * cellWidth;

  return (
    <svg
      className="showcase-heatmap"
      role="img"
      aria-label={title}
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
    >
      <text x={0} y={16} className="showcase-heatmap-title">
        {title}
      </text>
      {months.map((month, i) => {
        if (!month.endsWith("-01")) return null;
        const x = labelWidth + i * cellWidth;
        return (
          <text key={month} x={x} y={height - 4} className="showcase-heatmap-year">
            {month.slice(0, 4)}
          </text>
        );
      })}
      {markets.map((market, rowIndex) => {
        const y = titleHeight + rowIndex * cellHeight;
        return (
          <g key={market.market_id}>
            <text x={0} y={y + 12} className="showcase-heatmap-label">
              {market.market}
            </text>
            {months.map((month, columnIndex) => {
              const row = rowsByMarketMonth.get(`${market.market_id}:${month}`);
              const value = row ? row[field] : null;
              const isSelected = month === selectedMonth;
              return (
                <rect
                  key={`${market.market_id}-${month}`}
                  x={labelWidth + columnIndex * cellWidth}
                  y={y}
                  width={cellWidth}
                  height={cellHeight - 1}
                  fill={color(value)}
                  className={isSelected ? "showcase-heatmap-cell-selected" : "showcase-heatmap-cell"}
                />
              );
            })}
          </g>
        );
      })}
      <rect
        x={selectedX}
        y={titleHeight - 1}
        width={cellWidth}
        height={markets.length * cellHeight + 1}
        fill="none"
        className="showcase-heatmap-column"
      />
    </svg>
  );
}
