"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

type MetricField = "events_per_year" | "affected" | "damage" | "deaths" | "events_per_million";

interface DisasterMetricDef {
  key: string;
  label: string;
  shortLabel: string;
  field: MetricField;
  unit: string;
  caveat: string;
}

interface DisasterPayload {
  attestation_chain: string;
  generated_at: string;
  headline_top2: string[];
  kill_condition: string;
  metrics_top5: Record<string, string[]>;
  kill_condition_by_metric: Record<
    string,
    {
      top2: string[];
      differs_from_headline_top2: boolean;
      kill_condition_fires: boolean;
    }
  >;
  kill_condition_fires_overall: boolean;
  sources: {
    emdat: {
      vintage: string;
      rows_total: number;
      rows_in_filter: number;
      recompute_equals_committed_panel: boolean;
      note_threshold: string;
    };
    population: {
      lastupdated: string;
      denominator_year: string;
      wall_note: string;
    };
  };
}

interface DisasterRow {
  iso3: string;
  country: string;
  events: number;
  events_per_year: number;
  affected: number;
  deaths: number;
  damage: number;
  population: number | null;
  pop_year: number | null;
  events_per_million: number | null;
}

interface RecoveryCountryRow {
  iso3: string;
  country: string;
  gdis_locations_2000_2018: number;
  gdis_unique_ids_2000_2018: number;
  gdis_unique_disasternos_2000_2018: number;
  gdis_locations_black_marble_window_2012_2018: number;
  gdis_unique_ids_black_marble_window_2012_2018: number;
  gdis_unique_disasternos_black_marble_window_2012_2018: number;
  top_disaster_types_2012_2018: string;
  dominant_admin_levels_2012_2018: string;
  readiness_lane: string;
}

interface RecoveryPayload {
  attestation_chain: string;
  generated_at: string;
  claim_scope: string;
  summary: {
    gdis_locations_total_csv: number;
    gdis_unique_ids_total_csv: number;
    gdis_unique_disasternos_total_csv: number;
    adb_locations_black_marble_window_2012_2018: number;
    adb_unique_ids_black_marble_window_2012_2018: number;
    adb_unique_disasternos_black_marble_window_2012_2018: number;
    countries_with_gdis_viirs_overlap: number;
    current_emdat_rows_in_adb_2000_2025_filter: number;
    current_emdat_has_disaster_identifier: boolean;
    current_emdat_has_month_day: boolean;
    current_emdat_has_location_geometry: boolean;
    black_marble_vnp46a3_time_start: string;
    black_marble_vnp46a3_version: string;
    recovery_curve_ready: boolean;
    top_overlap_countries: RecoveryCountryRow[];
  };
  source_gates: {
    gate: string;
    status: string;
    finding: string;
  }[];
}

const METRICS: DisasterMetricDef[] = [
  {
    key: "events_per_year (committed)",
    label: "Events per year",
    shortLabel: "Events/yr",
    field: "events_per_year",
    unit: "events per year, 2000-2025",
    caveat: "Event frequency reflects EM-DAT inclusion and reporting thresholds.",
  },
  {
    key: "total_affected (committed)",
    label: "Total affected",
    shortLabel: "Affected",
    field: "affected",
    unit: "affected person-events, 2000-2025",
    caveat: "Affected totals sum person-events across events and can exceed population.",
  },
  {
    key: "total_damage_usd_adj (committed)",
    label: "Damage",
    shortLabel: "Damage",
    field: "damage",
    unit: "adjusted US dollars, 2000-2025",
    caveat: "Damage values depend on loss valuation and reporting capacity.",
  },
  {
    key: "total_deaths (DEEPENING)",
    label: "Total deaths",
    shortLabel: "Deaths",
    field: "deaths",
    unit: "recorded deaths, 2000-2025",
    caveat: "Deaths are recomputed from the same EM-DAT workbook as the original panel.",
  },
  {
    key: "events_per_million_pop (DEEPENING, cross-program WDI join)",
    label: "Events per million people",
    shortLabel: "Per million",
    field: "events_per_million",
    unit: "events per million people, 2024 denominator",
    caveat: "The denominator is a cross-program WDI 2024 population join, not the program's original lineage.",
  },
];

function formatNumber(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString("en-US", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function formatMetric(value: number | null | undefined, field: MetricField) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  if (field === "damage") {
    if (value >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(1)}B`;
    if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
    return `$${formatNumber(value)}`;
  }
  if (field === "affected") {
    if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(2)}B`;
    if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
    return formatNumber(value);
  }
  if (field === "events_per_year" || field === "events_per_million") return formatNumber(value, 2);
  return formatNumber(value);
}

function splitCsvLine(line: string) {
  const cells: string[] = [];
  let current = "";
  let quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    if (char === '"') {
      if (quoted && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      cells.push(current);
      current = "";
    } else {
      current += char;
    }
  }
  cells.push(current);
  return cells;
}

function parseDisasterCsv(text: string): DisasterRow[] {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  const headers = splitCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const cells = splitCsvLine(line);
    const row = Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""]));
    const numberOrNull = (value: string) => (value === "" ? null : Number(value));
    return {
      iso3: row.iso3,
      country: row.country,
      events: Number(row.events),
      events_per_year: Number(row.events_per_year),
      affected: Number(row.affected),
      deaths: Number(row.deaths),
      damage: Number(row.damage),
      population: numberOrNull(row.population),
      pop_year: numberOrNull(row.pop_year),
      events_per_million: numberOrNull(row.events_per_million),
    };
  });
}

function valueFor(row: DisasterRow, field: MetricField) {
  return row[field];
}

function rowByIso(rows: DisasterRow[], iso: string) {
  return rows.find((row) => row.iso3 === iso);
}

export default function ShowcaseDisasterMetric() {
  const [data, setData] = useState<DisasterPayload | null>(null);
  const [recovery, setRecovery] = useState<RecoveryPayload | null>(null);
  const [rows, setRows] = useState<DisasterRow[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [metricKey, setMetricKey] = useState(METRICS[0].key);

  useEffect(() => {
    Promise.all([
      fetch("/programs/disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.json").then((r) => {
        if (!r.ok) throw new Error(`JSON HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.csv").then((r) => {
        if (!r.ok) throw new Error(`CSV HTTP ${r.status}`);
        return r.text();
      }),
      fetch("/programs/disaster-recovery-lag/generated/disaster-recovery-lag-recovery-source-readiness.json").then((r) => {
        if (!r.ok) throw new Error(`Recovery JSON HTTP ${r.status}`);
        return r.json();
      }),
    ])
      .then(([payload, csvText, recoveryPayload]: [DisasterPayload, string, RecoveryPayload]) => {
        setData(payload);
        setRows(parseDisasterCsv(csvText));
        setRecovery(recoveryPayload);
      })
      .catch((err) => setError(String(err)));
  }, []);

  const selectedMetric = METRICS.find((metric) => metric.key === metricKey) ?? METRICS[0];
  const selectedStatus = data?.kill_condition_by_metric[selectedMetric.key];
  const fireCount = data
    ? Object.values(data.kill_condition_by_metric).filter((metric) => metric.kill_condition_fires).length
    : 0;

  return (
    <article className="showcase-page disaster-showcase">
      <header className="showcase-hero disaster-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            When the Disaster Top-Two Breaks
          </h1>
          <p className="showcase-lede">
            The original disaster screen treated China and India as a
            metric-robust top-two. The deepening reruns the program's own
            pre-registered kill condition, then checks whether public event
            geography and nighttime-light sources are ready for a true
            recovery-lag metric. The answer is sharper: the top-two breaks,
            and the recovery object is still a source-join problem.
          </p>
          <div className="showcase-meta">
            <span>{data?.attestation_chain || "ai-first"}</span>
            <span>Metric falsification + source-readiness sprint</span>
            <span>Recovery queue, not a country ranking</span>
          </div>
        </div>
        <div className="showcase-hero-panel disaster-hero-panel" aria-label="Disaster metric falsification summary">
          {data ? (
            <>
              <div className="disaster-hero-strip">
                {METRICS.map((metric) => {
                  const status = data.kill_condition_by_metric[metric.key];
                  return (
                    <div key={metric.key} className={status.kill_condition_fires ? "fires" : "holds"}>
                      <span>{metric.shortLabel}</span>
                      <strong>{status.top2.join(" + ")}</strong>
                    </div>
                  );
                })}
              </div>
              <div className="disaster-hero-stats">
                <div>
                  <span className="showcase-stat-value">{fireCount}/5</span>
                  <span className="showcase-stat-label">metrics fire the top-two kill condition</span>
                </div>
                <div>
                  <span className="showcase-stat-value">{formatNumber(data.sources.emdat.rows_in_filter)}</span>
                  <span className="showcase-stat-label">EM-DAT rows in the 2000-2025 DMC filter</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {recovery ? formatNumber(recovery.summary.adb_unique_disasternos_black_marble_window_2012_2018) : "..." }
                  </span>
                  <span className="showcase-stat-label">GDIS disaster numbers in the Black Marble overlap window</span>
                </div>
              </div>
            </>
          ) : (
            <p className="showcase-loading">{error || "Loading disaster falsification evidence..."}</p>
          )}
        </div>
      </header>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Measurement problem</p>
          <h2>A disaster burden claim can be true on one axis and fail on another.</h2>
          <p>
            Disaster screens often mix event counts, affected people, deaths,
            damage, and exposure rates. The policy use changes with the metric.
            A planning team asking about recovery needs to know whether a
            headline is stable across those definitions, or whether it mostly
            reflects the reporting and scale properties of one source column.
          </p>
        </div>
        <div className="showcase-note">
          <strong>Source upgrade.</strong> The script re-aggregates the EM-DAT
          country-profiles workbook from the program cache and asserts equality
          with the committed panel before reporting any ranking. The per-capita
          view adds a clearly labeled World Bank WDI population denominator from
          an on-disk sibling cache. A second script adds a GDIS x Black Marble
          source-readiness queue, while keeping recovery-speed claims blocked.
        </div>
      </section>

      <RecoveryReadinessPanel recovery={recovery} error={error} />

      <section className="showcase-explorer">
        <div className="showcase-explorer-head">
          <div>
            <p className="kicker kicker-crimson">Interactive evidence view</p>
            <h2>Switch the metric and the top-two changes.</h2>
            <p>
              The chart reads from the generated CSV. Red cards are metrics
              where the pre-registered top-two kill condition fires; blue cards
              keep the original China-India top-two set.
            </p>
          </div>
          <div className="showcase-controls disaster-controls">
            {METRICS.map((metric) => (
              <button
                key={metric.key}
                type="button"
                className={metric.key === metricKey ? "active" : ""}
                onClick={() => setMetricKey(metric.key)}
              >
                {metric.shortLabel}
              </button>
            ))}
          </div>
        </div>

        <div className="disaster-evidence-grid">
          <div className="disaster-main-chart">
            {!data || rows.length === 0 ? (
              <p className="showcase-loading">{error || "Loading chart data..."}</p>
            ) : (
              <MetricBarChart data={data} rows={rows} metric={selectedMetric} />
            )}
          </div>
          <div className="disaster-side-panel">
            {!data || rows.length === 0 || !selectedStatus ? (
              <p className="showcase-loading">Loading readout...</p>
            ) : (
              <MetricReadout
                data={data}
                rows={rows}
                metric={selectedMetric}
                status={selectedStatus}
              />
            )}
          </div>
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">What changed after deepening</p>
          <h2>The stronger result is a narrowed claim, not a louder ranking.</h2>
          <p>
            The evidence does not say that one metric is the right disaster
            burden metric. It says the previous metric-robust top-two claim is
            too broad. China remains high on several absolute-burden axes, but
            the second position is metric-dependent, and deaths and per-capita
            event frequency point to different economies.
          </p>
        </div>
        <div className="showcase-note">
          <strong>Non-claim.</strong> None of these metrics measures recovery
          speed. The source-readiness audit shows a public event-geography
          queue, but the current EM-DAT workbook lacks the event identifier,
          date, and geometry fields needed for recovery curves.
        </div>
      </section>

      <ShowcaseQualityPanel reportId={8} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Operational use</p>
          <h2>Use the falsifier before using the screen.</h2>
          <p>
            ADB teams and national statistical users can use this kind of
            metric-falsification view before turning disaster screens into
            targeting or monitoring narratives. If the top group changes under
            a defensible metric, the next step is to narrow the claim, not to
            average the metrics into a composite.
          </p>
        </div>
        <div className="showcase-links">
          <a href="/programs/disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.json" download>
            Download falsification JSON
          </a>
          <a href="/programs/disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.csv" download>
            Download metric CSV
          </a>
          <a href="/programs/disaster-recovery-lag/generated/disaster-recovery-lag-recovery-source-readiness.json" download>
            Download source-readiness JSON
          </a>
          <a href="/programs/disaster-recovery-lag/generated/disaster-recovery-lag-recovery-source-readiness-events.csv" download>
            Download event queue CSV
          </a>
          <a href="/programs/disaster-recovery-lag/deepened-results.md" target="_blank" rel="noreferrer">
            Read deepening note
          </a>
          <Link href="/disaster-recovery-lag?view=evidence">Program evidence</Link>
        </div>
      </section>
    </article>
  );
}

function RecoveryReadinessPanel({
  recovery,
  error,
}: {
  recovery: RecoveryPayload | null;
  error: string | null;
}) {
  if (!recovery) {
    return (
      <section className="disaster-source-bridge">
        <p className="showcase-loading">{error || "Loading recovery source-readiness audit..."}</p>
      </section>
    );
  }

  const bars = recovery.summary.top_overlap_countries.slice(0, 8);
  const max = Math.max(...bars.map((row) => row.gdis_unique_disasternos_black_marble_window_2012_2018), 1);
  const gateClass = (status: string) =>
    status.includes("block") || status.includes("not_ready") ? "blocked" : "usable";

  return (
    <section className="disaster-source-bridge" data-qa="recovery-source-bridge">
      <div className="disaster-source-head">
        <p className="kicker kicker-blue">Recovery source-readiness</p>
        <h2>The source object is a bridge, not a curve.</h2>
        <p>
          GDIS supplies geocoded EM-DAT event locations through 2018, and NASA
          Black Marble monthly lights start in 2012. That creates a visible
          2012-2018 pilot queue, but the current EM-DAT cache is still aggregate
          country-year data.
        </p>
      </div>

      <div className="disaster-source-grid">
        <div className="disaster-gate-grid">
          {recovery.source_gates.map((gate) => (
            <div key={gate.gate} className={`disaster-gate-card ${gateClass(gate.status)}`}>
              <span>{gate.status.replaceAll("_", " ")}</span>
              <strong>{gate.gate}</strong>
              <p>{gate.finding}</p>
            </div>
          ))}
        </div>

        <div className="disaster-overlap-panel">
          <div className="disaster-overlap-head">
            <div>
              <h3>GDIS x Black Marble overlap queue</h3>
              <p>
                2012-2018, ADB DMCs; bars show unique <code>disasterno</code> values.
              </p>
            </div>
            <strong>{formatNumber(recovery.summary.adb_locations_black_marble_window_2012_2018)}</strong>
          </div>
          <div className="disaster-overlap-bars">
            {bars.map((row) => {
              const value = row.gdis_unique_disasternos_black_marble_window_2012_2018;
              return (
                <div key={row.iso3} className="disaster-overlap-row">
                  <div>
                    <strong>{row.iso3}</strong>
                    <span>{row.country}</span>
                  </div>
                  <i>
                    <b style={{ width: `${Math.max(3, (value / max) * 100)}%` }} />
                  </i>
                  <em>{formatNumber(value)}</em>
                  <small>
                    {formatNumber(row.gdis_locations_black_marble_window_2012_2018)} locations{" "}
                    &middot;{" "}
                    {row.top_disaster_types_2012_2018 || "type mix missing"}
                  </small>
                </div>
              );
            })}
          </div>
          <div className="disaster-queue-strip" aria-label="Recovery source-readiness totals">
            <span>
              <strong>{formatNumber(recovery.summary.adb_unique_ids_black_marble_window_2012_2018)}</strong>
              GDIS ids
            </span>
            <span>
              <strong>{formatNumber(recovery.summary.adb_unique_disasternos_black_marble_window_2012_2018)}</strong>
              disaster numbers
            </span>
            <span>
              <strong>{formatNumber(recovery.summary.countries_with_gdis_viirs_overlap)}</strong>
              economies
            </span>
            <span>
              <strong>{recovery.summary.recovery_curve_ready ? "ready" : "blocked"}</strong>
              curve status
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}

function MetricBarChart({
  data,
  rows,
  metric,
}: {
  data: DisasterPayload;
  rows: DisasterRow[];
  metric: DisasterMetricDef;
}) {
  const topIso = data.metrics_top5[metric.key] ?? [];
  const plotted = useMemo(() => {
    const required = new Set([...topIso, ...data.headline_top2]);
    return rows
      .filter((row) => required.has(row.iso3) && valueFor(row, metric.field) !== null)
      .sort((a, b) => Number(valueFor(b, metric.field)) - Number(valueFor(a, metric.field)));
  }, [data.headline_top2, metric.field, rows, topIso]);
  const max = Math.max(...plotted.map((row) => Number(valueFor(row, metric.field))), 1);
  const width = 780;
  const height = 86 + plotted.length * 42;
  const margin = { top: 54, right: 150, bottom: 34, left: 86 };
  const x = (value: number) => margin.left + (value / max) * (width - margin.left - margin.right);

  return (
    <div className="disaster-chart-wrap">
      <svg className="disaster-bar-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`${metric.label} top ranked DMCs`}>
        <text x={margin.left} y={24} className="disaster-chart-title">
          {metric.label}: top five plus original top-two
        </text>
        <text x={margin.left} y={42} className="disaster-chart-subtitle">
          {metric.unit}
        </text>
        {plotted.map((row, index) => {
          const value = Number(valueFor(row, metric.field));
          const y = margin.top + index * 42;
          const original = data.headline_top2.includes(row.iso3);
          const currentTop2 = (data.kill_condition_by_metric[metric.key]?.top2 ?? []).includes(row.iso3);
          return (
            <g key={row.iso3}>
              <text x={margin.left - 12} y={y + 17} textAnchor="end" className="disaster-label">
                {row.iso3}
              </text>
              <rect
                x={margin.left}
                y={y}
                width={Math.max(2, x(value) - margin.left)}
                height={18}
                className={currentTop2 ? "disaster-bar disaster-bar-current" : original ? "disaster-bar disaster-bar-original" : "disaster-bar"}
              />
              <text x={x(value) + 8} y={y + 15} className="disaster-value">
                {formatMetric(value, metric.field)}
              </text>
              <text x={margin.left} y={y + 34} className="disaster-row-note">
                {row.country}
              </text>
            </g>
          );
        })}
        <text x={margin.left} y={height - 8} className="disaster-axis-label">
          Dark red = current top two; outlined blue = original CHN+IND when not current top two
        </text>
      </svg>
      <div className="disaster-mobile-bars" aria-label={`${metric.label} mobile ranked bars`}>
        <h3>{metric.label}</h3>
        <p>{metric.unit}</p>
        {plotted.map((row) => {
          const value = Number(valueFor(row, metric.field));
          const original = data.headline_top2.includes(row.iso3);
          const currentTop2 = (data.kill_condition_by_metric[metric.key]?.top2 ?? []).includes(row.iso3);
          return (
            <div
              key={row.iso3}
              className={
                currentTop2
                  ? "disaster-mobile-bar-row disaster-mobile-bar-current"
                  : original
                    ? "disaster-mobile-bar-row disaster-mobile-bar-original"
                    : "disaster-mobile-bar-row"
              }
            >
              <div>
                <strong>{row.iso3}</strong>
                <span>{formatMetric(value, metric.field)}</span>
              </div>
              <i style={{ width: `${Math.max(3, (value / max) * 100)}%` }} />
              <small>{row.country}</small>
            </div>
          );
        })}
        <p className="disaster-mobile-legend">
          Dark red = current top two. Blue outline = original CHN+IND when not
          current top two.
        </p>
      </div>
    </div>
  );
}

function MetricReadout({
  data,
  rows,
  metric,
  status,
}: {
  data: DisasterPayload;
  rows: DisasterRow[];
  metric: DisasterMetricDef;
  status: DisasterPayload["kill_condition_by_metric"][string];
}) {
  const first = rowByIso(rows, status.top2[0]);
  const second = rowByIso(rows, status.top2[1]);
  return (
    <>
      <p className={status.kill_condition_fires ? "kicker kicker-crimson" : "kicker kicker-blue"}>
        {status.kill_condition_fires ? "Kill condition fires" : "Original top-two holds"}
      </p>
      <h3>{metric.label}</h3>
      <dl className="disaster-readout">
        <div>
          <dt>Top two under this metric</dt>
          <dd>{status.top2.join(" + ")}</dd>
        </div>
        <div>
          <dt>{first?.iso3 || "First"} value</dt>
          <dd>{formatMetric(first ? valueFor(first, metric.field) : null, metric.field)}</dd>
        </div>
        <div>
          <dt>{second?.iso3 || "Second"} value</dt>
          <dd>{formatMetric(second ? valueFor(second, metric.field) : null, metric.field)}</dd>
        </div>
        <div>
          <dt>Original top two</dt>
          <dd>{data.headline_top2.join(" + ")}</dd>
        </div>
      </dl>
      <p>{metric.caveat}</p>
      {metric.field === "events_per_million" && (
        <p>
          Population denominator: {data.sources.population.denominator_year};
          source last updated {data.sources.population.lastupdated}.
        </p>
      )}
      <p>
        EM-DAT recompute status:{" "}
        {data.sources.emdat.recompute_equals_committed_panel ? "matches committed panel" : "does not match panel"}.
      </p>
    </>
  );
}
