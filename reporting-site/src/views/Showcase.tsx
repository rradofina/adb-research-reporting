"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";
import {
  getShowcaseReportQuality,
  showcaseReports,
  type ShowcaseReadiness,
} from "../data/showcaseReports";

const publicReadinessLabel: Record<ShowcaseReadiness, string> = {
  prototype: "Prototype evidence",
  "l3-candidate": "Evidence package",
  "evidence-audit": "Evidence audit",
  "portfolio-proof": "Portfolio proof",
  "owner-gated": "Owner-gated source note",
};

function publicStatusLabel(label: string) {
  return label.replace(/^L\d+\s+/i, "");
}

interface SprintCoverage {
  raw_price_rows_kept: number;
  market_count_before_selection: number;
  selected_market_count: number;
  selected_market_month_cells: number;
  rows_with_price_and_lagged_precipitation: number;
  price_spike_screen_count: number;
  dry_price_spike_screen_count: number;
  non_dry_price_spike_screen_count: number;
  wet_price_spike_screen_count: number;
  hot_price_spike_screen_count: number;
  broad_price_wave_month_count: number;
  dry_aligned_cluster_month_count: number;
  commodity_inventory_candidate_series: number;
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
  lagged_temperature_z: number | null;
  price_spike_screen: boolean;
  dry_price_spike_screen: boolean;
  non_dry_price_spike_screen: boolean;
  wet_price_spike_screen: boolean;
  hot_price_spike_screen: boolean;
  weather_alignment_status: string;
}

interface MonthSignal {
  month: string;
  selected_market_count: number;
  priced_market_count: number;
  joined_market_count: number;
  price_spike_count: number;
  price_spike_share: number | null;
  dry_price_spike_count: number;
  non_dry_price_spike_count: number;
  wet_price_spike_count: number;
  hot_price_spike_count: number;
  dry_share_among_price_spikes: number | null;
  median_price_spike_anomaly_pct: number | null;
  top_market: string | null;
  top_market_price_anomaly_pct: number | null;
  signal_class: string;
  plain_english: string;
}

interface CommoditySeries {
  commodity: string;
  category: string;
  unit: string;
  pricetype: string;
  priceflag: string;
  raw_rows: number;
  market_count: number;
  market_month_cells: number;
  year_min: number | null;
  year_max: number | null;
  eligible_for_next_pass: boolean;
  current_sprint_series: boolean;
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
  commodity_inventory: {
    candidate_rule: string;
    total_series: number;
    candidate_series_count: number;
    current_sprint_series: CommoditySeries;
    top_candidate_series: CommoditySeries[];
  };
  rainfall_source_comparison: {
    primary_source: string;
    primary_status: string;
    alternative_source_status: string;
    required_upgrade: string;
  };
  triage_summaries: {
    top_price_spikes: MarketClimateRow[];
    dry_price_spike_screen_top12: MarketClimateRow[];
    month_signal_class_counts: Record<string, number>;
    month_signal_ledger: MonthSignal[];
    top_broad_price_wave_months: MonthSignal[];
    top_dry_aligned_months: MonthSignal[];
  };
}

function pct(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value.toFixed(digits)}%`;
}

function count(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString();
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

function colorSignal(signalClass: string) {
  if (signalClass === "broad_price_wave_not_local_dryness") return "#007DB8";
  if (signalClass === "dry_aligned_cluster") return "#5A8227";
  if (signalClass === "mixed_or_sparse_price_spike_screen") return "#FBB00E";
  return "#d8dde3";
}

function signalLabel(signalClass: string) {
  if (signalClass === "broad_price_wave_not_local_dryness") return "broad wave";
  if (signalClass === "dry_aligned_cluster") return "dry cluster";
  if (signalClass === "mixed_or_sparse_price_spike_screen") return "mixed";
  return "no spike";
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
  const topBroadWave = data?.triage_summaries.top_broad_price_wave_months[0];

  return (
    <article className="showcase-page">
      <header className="showcase-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">Public-data evidence note</p>
          <h1 className="showcase-title">
            When Food Prices Spike, Is the Weather Local?
          </h1>
          <p className="showcase-lede">
            A market-month sprint for Nepal joins WFP rice prices with local
            NASA POWER climate lags. The report now counts the uncomfortable
            part of the hook: most price-spike cells do not line up with a dry
            local rainfall lag.
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
                  {data.coverage.price_spike_screen_count}
                </span>
                <span className="showcase-stat-label">rice price-spike cells</span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.non_dry_price_spike_screen_count}
                </span>
                <span className="showcase-stat-label">not dry-aligned</span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.dry_price_spike_screen_count}
                </span>
                <span className="showcase-stat-label">dry-aligned cells</span>
              </div>
              <div>
                <span className="showcase-stat-value">
                  {data.coverage.broad_price_wave_month_count}
                </span>
                <span className="showcase-stat-label">broad-wave months</span>
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

      {data && <FalsifierLedger data={data} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The broad price wave is now counted before any model is fitted.</h2>
          <p>
            The evidence screen still shows synchronized rice price anomalies
            across many markets in 2023-2025. The stronger result is that the
            generated ledger separates those broad months from the small set of
            dry-aligned clusters, so the next program has a concrete falsifier
            instead of only a striking heatmap.
          </p>
        </div>
        <div className="showcase-fact-list">
          {topBroadWave && (
            <div>
              <span>Broadest non-dry month</span>
              <strong>
                {topBroadWave.month}: {topBroadWave.price_spike_count} price-spike markets,{" "}
                {topBroadWave.dry_price_spike_count} dry-aligned
              </strong>
            </div>
          )}
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
          {data && (
            <div>
              <span>Expansion queue</span>
              <strong>
                {data.coverage.commodity_inventory_candidate_series} WFP commodity series clear
                the next-pass coverage rule
              </strong>
            </div>
          )}
        </div>
      </section>

      {data && <SourceAudit data={data} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What this does not mean</p>
          <h2>The report does not claim that weather caused the price spikes.</h2>
          <p>
            NASA POWER is modeled point climate data, WFP market rows have
            missing months, and this sprint still leads with one rice series.
            The broad-wave ledger weakens a simple local-dryness story, but it
            does not identify the alternative driver. A publication candidate
            needs commodity expansion, rainfall-source comparison, exchange-rate
            and import-price checks, fuel-price context, and market-access
            falsifiers.
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

      <ShowcaseQualityPanel reportId={1} />

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">Evidence library</p>
          <h2>
            {showcaseReports.length} report surfaces with source paths and caveats.
          </h2>
          <p>
            Reports enter this library only after the evidence package, visual
            concept, caveats, and visual QA are strong enough for a
            reader-facing surface. The stage label is descriptive, not a claim
            promotion.
          </p>
        </div>
        <div className="showcase-queue">
          {showcaseReports.map((item, index) => (
            <div className="showcase-queue-row" key={item.href}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>
                <Link href={item.href}>{item.shortTitle}</Link>
              </strong>
              <em>
                {publicStatusLabel(item.statusLabel)} - {publicReadinessLabel[getShowcaseReportQuality(item).readiness]}
              </em>
              <code>{item.evidencePath}</code>
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
          <Link href="/factory">Factory rules</Link>
          <Link href="/status">Research status</Link>
          <Link href="/docs">Governance documents</Link>
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
  const initialMonth = data.triage_summaries.top_broad_price_wave_months[0]?.month || "2025-09";
  const [selectedIndex, setSelectedIndex] = useState(() =>
    Math.max(0, months.indexOf(initialMonth)),
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
  const signalByMonth = useMemo(() => {
    return new Map(data.triage_summaries.month_signal_ledger.map((row) => [row.month, row]));
  }, [data.triage_summaries.month_signal_ledger]);
  const selectedSignal = signalByMonth.get(selectedMonth);

  return (
    <section className="showcase-section showcase-explorer">
      <div className="showcase-explorer-head">
        <div>
          <p className="kicker">Interactive evidence view</p>
          <h2>Scrub the same market-month table the sprint generated.</h2>
          <p>
            The top panel is rice price anomaly. The bottom panel is
            previous-month precipitation anomaly. The strip underneath counts
            the falsifier: whether each month looks broad, dry-aligned, mixed,
            or quiet.
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
        <SignalStrip
          signals={data.triage_summaries.month_signal_ledger}
          months={months}
          selectedMonth={selectedMonth}
        />
      </div>

      <div className="showcase-signal-legend" aria-label="Signal legend">
        <span><i style={{ background: colorSignal("broad_price_wave_not_local_dryness") }} /> Broad price wave, not local dryness</span>
        <span><i style={{ background: colorSignal("dry_aligned_cluster") }} /> Dry-aligned cluster</span>
        <span><i style={{ background: colorSignal("mixed_or_sparse_price_spike_screen") }} /> Mixed or sparse spike</span>
        <span><i style={{ background: colorSignal("no_price_spike_screen") }} /> No price-spike screen</span>
      </div>

      <div className="showcase-month-readout">
        <div>
          <span>Selected month</span>
          <strong>{selectedMonth}</strong>
        </div>
        <div>
          <span>Price-spike markets</span>
          <strong>
            {selectedSignal
              ? `${selectedSignal.price_spike_count} of ${selectedSignal.selected_market_count}`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Dry-aligned price spikes</span>
          <strong>
            {selectedSignal
              ? `${selectedSignal.dry_price_spike_count} dry, ${selectedSignal.non_dry_price_spike_count} not dry`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Month signal</span>
          <strong>
            {selectedSignal ? signalLabel(selectedSignal.signal_class) : "missing"}
          </strong>
        </div>
        <div>
          <span>Highest market and driest lag</span>
          <strong>
            {highestPrice && driest
              ? `${highestPrice.market} ${pct(highestPrice.price_anomaly_pct, 1)}; ${driest.market} z ${driest.lagged_precipitation_z?.toFixed(2)}`
              : "missing"}
          </strong>
        </div>
      </div>
    </section>
  );
}

function SignalStrip({
  signals,
  months,
  selectedMonth,
}: {
  signals: MonthSignal[];
  months: string[];
  selectedMonth: string;
}) {
  const signalByMonth = new Map(signals.map((row) => [row.month, row]));
  const labelWidth = 104;
  const cellWidth = 11;
  const width = labelWidth + months.length * cellWidth + 10;
  const height = 92;
  const chartTop = 30;
  const chartHeight = 42;
  const selectedX = labelWidth + months.indexOf(selectedMonth) * cellWidth;

  return (
    <svg
      className="showcase-signal-strip"
      role="img"
      aria-label="Monthly price-spike signal classification"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
    >
      <text x={0} y={16} className="showcase-heatmap-title">
        Month signal ledger: price-spike breadth and dry-lag alignment
      </text>
      <text x={0} y={chartTop + chartHeight - 1} className="showcase-heatmap-label">
        Spike count
      </text>
      {months.map((month, i) => {
        const signal = signalByMonth.get(month);
        const countValue = signal?.price_spike_count || 0;
        const denom = Math.max(1, signal?.selected_market_count || 1);
        const barHeight = Math.max(3, (countValue / denom) * chartHeight);
        const x = labelWidth + i * cellWidth;
        const y = chartTop + chartHeight - barHeight;
        return (
          <rect
            key={month}
            x={x}
            y={y}
            width={cellWidth - 1}
            height={barHeight}
            fill={colorSignal(signal?.signal_class || "no_price_spike_screen")}
            opacity={month === selectedMonth ? 1 : 0.86}
          />
        );
      })}
      {months.map((month, i) => {
        if (!month.endsWith("-01")) return null;
        const x = labelWidth + i * cellWidth;
        return (
          <text key={month} x={x} y={height - 6} className="showcase-heatmap-year">
            {month.slice(0, 4)}
          </text>
        );
      })}
      <rect
        x={selectedX}
        y={chartTop - 2}
        width={cellWidth}
        height={chartHeight + 4}
        fill="none"
        className="showcase-heatmap-column"
      />
    </svg>
  );
}

function FalsifierLedger({ data }: { data: SprintData }) {
  const broadRows = data.triage_summaries.top_broad_price_wave_months.slice(0, 8);
  const dryRows = data.triage_summaries.top_dry_aligned_months.slice(0, 4);

  return (
    <section className="showcase-section showcase-falsifier-section">
      <div className="showcase-section-copy">
        <p className="kicker">Falsifier ledger</p>
        <h2>The page now asks what else could explain the spike.</h2>
        <p>
          The month ledger is generated from the same market-month rows as the
          heatmap. It does not explain the broad price waves; it makes the
          non-climate alternative visible enough to research next.
        </p>
      </div>
      <div className="showcase-ledger-grid" aria-label="Broad price-wave ledger">
        <div className="showcase-ledger-row showcase-ledger-row-head">
          <span>Month</span>
          <span>Price-spike markets</span>
          <span>Dry lag</span>
          <span>Wet or hot lag</span>
          <span>Largest market signal</span>
        </div>
        {broadRows.map((row) => (
          <div className="showcase-ledger-row" key={row.month}>
            <span data-label="Month">
              <i style={{ background: colorSignal(row.signal_class) }} />
              {row.month}
            </span>
            <strong data-label="Price-spike markets">
              {row.price_spike_count} of {row.selected_market_count}
            </strong>
            <strong data-label="Dry lag">{row.dry_price_spike_count}</strong>
            <strong data-label="Wet or hot lag">{row.wet_price_spike_count + row.hot_price_spike_count}</strong>
            <em data-label="Largest market signal">
              {row.top_market}: {pct(row.top_market_price_anomaly_pct, 1)}
            </em>
          </div>
        ))}
      </div>
      <div className="showcase-dry-ledger">
        <span>Dry-aligned cluster months</span>
        <strong>
          {dryRows.length > 0
            ? dryRows
                .map((row) => `${row.month} (${row.dry_price_spike_count} dry of ${row.price_spike_count})`)
                .join("; ")
            : "none under the generated screen"}
        </strong>
      </div>
    </section>
  );
}

function SourceAudit({ data }: { data: SprintData }) {
  const candidates = data.commodity_inventory.top_candidate_series.slice(0, 8);

  return (
    <section className="showcase-section showcase-source-audit-section">
      <div className="showcase-section-copy">
        <p className="kicker">Source and expansion audit</p>
        <h2>The current chart is rice-only; the source file is not.</h2>
        <p>
          The sprint now records the commodity expansion queue from the full WFP
          CSV. This keeps the page from pretending a one-series result is a food
          system result, while showing that the next loop has enough public rows
          to move beyond rice.
        </p>
      </div>
      <div className="showcase-source-audit-grid">
        <div className="showcase-source-audit-panel">
          <span>Rainfall source check</span>
          <strong>{data.rainfall_source_comparison.primary_source}</strong>
          <p>{data.rainfall_source_comparison.required_upgrade}</p>
          <code>{data.rainfall_source_comparison.alternative_source_status}</code>
        </div>
        <div className="showcase-source-audit-panel">
          <span>Commodity inventory rule</span>
          <strong>{data.commodity_inventory.candidate_series_count} candidate series</strong>
          <p>{data.commodity_inventory.candidate_rule}</p>
          <code>
            Current: {data.commodity_inventory.current_sprint_series.commodity},{" "}
            {data.commodity_inventory.current_sprint_series.market_month_cells} cells
          </code>
        </div>
      </div>
      <div className="showcase-commodity-grid" aria-label="Commodity expansion candidates">
        {candidates.map((row) => (
          <div className="showcase-commodity-row" key={`${row.commodity}-${row.unit}`}>
            <span>{row.current_sprint_series ? "current" : row.category}</span>
            <strong>{row.commodity}</strong>
            <em>
              {row.market_count} markets; {count(row.market_month_cells)} market-month cells; {row.unit}
            </em>
          </div>
        ))}
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
