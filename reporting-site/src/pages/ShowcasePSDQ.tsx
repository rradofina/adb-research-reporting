import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface PsdqExposureRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  join_key: string;
  registry_records: number;
  active_facilities: number;
  active_clinical_facilities: number;
  coordinate_facilities: number;
  osm_health: number;
  osm_hospital: number;
  osm_clinic: number;
  osm_doctors: number;
  osm_to_active_clinical_ratio: number;
  registry_minus_osm_clinical: number;
  registry_gap_share: number;
  buildings_nearest_1km_p85: number;
  buildings_nearest_3km_p85: number;
  buildings_nearest_5km_p85: number;
  underobserved_buildings_3km_p85_proxy: number;
  has_open_buildings_denominator: number;
  has_osm_boundary_match: number;
}

interface PsdqExposureSummary {
  generated_at: string;
  program: string;
  country: string;
  source: string;
  method: string;
  osm: {
    osm_elements: number;
    assigned_features: number;
    unassigned_features: number;
    timestamp_osm_base: string;
    timestamp_areas_base: string;
  };
  exposure: {
    registry_admin_rows: number;
    rows_with_open_buildings_denominator: number;
    active_clinical_facilities: number;
    osm_health_joined: number;
    registry_minus_osm_clinical: number;
    buildings_nearest_3km_p85: number;
    underobserved_buildings_3km_p85_proxy: number;
  };
  top_exposure_gap_upazilas: PsdqExposureRow[];
  non_claim: string;
}

interface PsdqStrataRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  join_key: string;
  active_clinical_facilities: number;
  osm_health: number;
  osm_to_active_clinical_ratio: number | null;
  registry_minus_osm_clinical: number;
  registry_gap_share: number;
  buildings_nearest_3km_p85: number;
  underobserved_buildings_3km_p85_proxy: number;
  has_open_buildings_denominator: number;
  has_osm_boundary_match: number;
  total_road_km?: number;
  classified_surface_share?: number;
  classified_unpaved_share?: number;
  road_context_score?: number;
}

interface PsdqRatioStratum {
  bucket: string;
  label: string;
  row_count: number;
  share_of_registry_rows: number | null;
  active_clinical_facilities: number;
  share_of_active_clinical_facilities: number | null;
  osm_health: number;
  osm_to_active_clinical_ratio: number | null;
  registry_minus_osm_clinical: number;
  buildings_nearest_3km_p85: number;
  underobserved_buildings_3km_p85_proxy: number;
}

interface PsdqSourceStrata {
  generated_at: string;
  goal_level: string;
  status: string;
  coverage: {
    registry_admin_rows: number;
    csv_registry_rows: number;
    rows_with_open_buildings_denominator: number;
    share_with_open_buildings_denominator: number | null;
    registry_rows_with_joined_osm_features: number;
    share_with_joined_osm_features: number | null;
    osm_elements_retrieved: number;
    osm_elements_assigned_to_boundary: number;
    osm_features_joined_to_registry: number;
    osm_features_not_joined_to_registry: number;
    active_clinical_facilities: number;
    osm_health_joined: number;
    registry_minus_osm_clinical: number;
    buildings_nearest_3km_p85: number;
    underobserved_buildings_3km_p85_proxy: number;
    rows_with_road_context: number;
    share_with_road_context: number | null;
    rows_with_surface_context: number;
    share_with_surface_context: number | null;
  };
  validation_strata: {
    rows_missing_open_buildings_denominator: number;
    share_missing_open_buildings_denominator: number | null;
    registry_rows_without_joined_osm_features: number;
    share_without_joined_osm_features: number | null;
    rows_with_zero_osm_health_features: number;
    share_with_zero_osm_health_features: number | null;
    rows_where_osm_equals_or_exceeds_registry: number;
    share_where_osm_equals_or_exceeds_registry: number | null;
    rows_with_zero_gap_or_osm_ge_registry: number;
    share_with_zero_gap_or_osm_ge_registry: number | null;
    rows_with_positive_registry_minus_osm_gap: number;
    rows_eligible_for_road_context: number;
    rows_eligible_for_road_surface_score: number;
    min_classified_surface_km_for_score: number;
    min_classified_surface_share_for_score: number;
  };
  ratio_strata: PsdqRatioStratum[];
  top_lists: {
    top_exposure_gap_upazilas: PsdqStrataRow[];
    top_zero_osm_high_proxy_upazilas: PsdqStrataRow[];
    top_osm_equals_or_exceeds_registry_upazilas: PsdqStrataRow[];
    top_road_context_upazilas: PsdqStrataRow[];
  };
}

interface PsdqCountrySummary {
  iso3: string;
  country: string;
  source: string;
  totals: {
    osm_health: number;
    registry_principal: number;
    registry_clinical: number;
    registry_all: number;
    ratio_osm_to_clinical: number;
  };
  num_admin1: number;
  admin1_min_ratio_clinical: number;
  admin1_max_ratio_clinical: number;
  worst_admin1: string;
  best_admin1: string;
}

interface PsdqNationalSummary {
  generated_at: string;
  claim_scope: string;
  framing_rule: string;
  countries: PsdqCountrySummary[];
}

type MetricMode = "exposure" | "gap" | "ratio";

const METRIC_OPTIONS: Array<{ id: MetricMode; label: string }> = [
  { id: "exposure", label: "Exposure proxy" },
  { id: "gap", label: "Gap share" },
  { id: "ratio", label: "Lowest OSM / registry" },
];

const STRATA_LABELS: Record<string, string> = {
  no_clinical_registry: "No clinical registry",
  zero_osm: "Zero OSM",
  gt0_to_5pct: ">0 to <5%",
  "5_to_10pct": "5 to <10%",
  "10_to_20pct": "10 to <20%",
  "20_to_50pct": "20 to <50%",
  "50_to_100pct": "50 to <100%",
  osm_ge_registry: "OSM >= registry",
};

const ALL_DIVISIONS = "All divisions";

function formatNumber(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function pct(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${(value * 100).toFixed(digits)}%`;
}

function metricValue(row: PsdqExposureRow, metric: MetricMode) {
  if (metric === "gap") return row.registry_gap_share;
  if (metric === "ratio") return row.osm_to_active_clinical_ratio;
  return row.underobserved_buildings_3km_p85_proxy;
}

function metricLabel(row: PsdqExposureRow, metric: MetricMode) {
  if (metric === "gap") return pct(row.registry_gap_share, 0);
  if (metric === "ratio") return pct(row.osm_to_active_clinical_ratio, 1);
  return formatNumber(row.underobserved_buildings_3km_p85_proxy);
}

function parseCsv(text: string): PsdqExposureRow[] {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return [];
  const headers = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    const row = Object.fromEntries(headers.map((header, index) => [header, values[index] || ""]));
    const num = (key: string) => Number(row[key] || 0);
    return {
      division_name: row.division_name,
      district_name: row.district_name,
      upazila_name: row.upazila_name,
      join_key: row.join_key,
      registry_records: num("registry_records"),
      active_facilities: num("active_facilities"),
      active_clinical_facilities: num("active_clinical_facilities"),
      coordinate_facilities: num("coordinate_facilities"),
      osm_health: num("osm_health"),
      osm_hospital: num("osm_hospital"),
      osm_clinic: num("osm_clinic"),
      osm_doctors: num("osm_doctors"),
      osm_to_active_clinical_ratio: num("osm_to_active_clinical_ratio"),
      registry_minus_osm_clinical: num("registry_minus_osm_clinical"),
      registry_gap_share: num("registry_gap_share"),
      buildings_nearest_1km_p85: num("buildings_nearest_1km_p85"),
      buildings_nearest_3km_p85: num("buildings_nearest_3km_p85"),
      buildings_nearest_5km_p85: num("buildings_nearest_5km_p85"),
      underobserved_buildings_3km_p85_proxy: num("underobserved_buildings_3km_p85_proxy"),
      has_open_buildings_denominator: num("has_open_buildings_denominator"),
      has_osm_boundary_match: num("has_osm_boundary_match"),
    };
  });
}

function parseCsvLine(line: string) {
  const cells: string[] = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      if (quoted && line[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      cells.push(cell);
      cell = "";
    } else {
      cell += char;
    }
  }
  cells.push(cell);
  return cells;
}

export default function ShowcasePSDQ() {
  const [summary, setSummary] = useState<PsdqExposureSummary | null>(null);
  const [strata, setStrata] = useState<PsdqSourceStrata | null>(null);
  const [national, setNational] = useState<PsdqNationalSummary | null>(null);
  const [rows, setRows] = useState<PsdqExposureRow[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement-summary.json").then((r) => {
        if (!r.ok) throw new Error(`summary HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/public-service-data-quality-summary.json").then((r) => {
        if (!r.ok) throw new Error(`national HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.json").then((r) => {
        if (!r.ok) throw new Error(`strata HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement.csv").then((r) => {
        if (!r.ok) throw new Error(`csv HTTP ${r.status}`);
        return r.text();
      }),
    ])
      .then(([summaryPayload, nationalPayload, strataPayload, csvText]) => {
        setSummary(summaryPayload);
        setNational(nationalPayload);
        setStrata(strataPayload);
        setRows(parseCsv(csvText));
      })
      .catch((err) => setError(String(err)));
  }, []);

  const topRow = summary?.top_exposure_gap_upazilas[0];
  const bangladesh = national?.countries.find((country) => country.iso3 === "BGD");

  return (
    <article className="showcase-page">
      <header className="showcase-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            When the Map and Registry Disagree
          </h1>
          <p className="showcase-lede">
            This PSDQ report uses the Bangladesh facility-registry deepening to
            ask a narrower question: where does a public map under-observe the
            official clinical registry in places with a large nearby building
            denominator?
          </p>
          <div className="showcase-meta">
            <span>ai-first</span>
            <span>L3 source-disagreement module</span>
            <span>Measurement gap, not facility quality</span>
          </div>
        </div>
        <div className="showcase-hero-panel psdq-hero-panel" aria-label="PSDQ evidence summary">
          {summary ? (
            <>
              <PsdqHeroRails rows={summary.top_exposure_gap_upazilas.slice(0, 3)} />
              <div className="psdq-hero-stats">
                <div>
                  <span className="showcase-stat-value">
                    {strata
                      ? `${strata.coverage.rows_with_open_buildings_denominator}/${strata.coverage.registry_admin_rows}`
                      : summary.exposure.registry_admin_rows}
                  </span>
                  <span className="showcase-stat-label">rows with building denominator</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {formatNumber(summary.exposure.underobserved_buildings_3km_p85_proxy)}
                  </span>
                  <span className="showcase-stat-label">under-observed building proxy</span>
                </div>
                {strata && (
                  <>
                    <div>
                      <span className="showcase-stat-value">
                        {formatNumber(strata.validation_strata.rows_with_zero_osm_health_features)}
                      </span>
                      <span className="showcase-stat-label">zero-OSM rows to validate</span>
                    </div>
                    <div>
                      <span className="showcase-stat-value">
                        {formatNumber(strata.validation_strata.rows_where_osm_equals_or_exceeds_registry)}
                      </span>
                      <span className="showcase-stat-label">OSM &gt;= registry rows</span>
                    </div>
                  </>
                )}
              </div>
            </>
          ) : (
            <span className="showcase-loading">
              {error ? `Could not load PSDQ artifacts: ${error}` : "Loading evidence packet..."}
            </span>
          )}
        </div>
      </header>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">The data gap</p>
          <h2>A service-access map can fail before travel time is modeled.</h2>
          <p>
            Facility catchments, service-coverage maps, and road-access
            diagnostics often start by joining a public map to an official
            registry. PSDQ makes the join visible first. The point is not to
            declare a winner between sources; it is to show where the sources
            are too far apart for a planning chart to hide the disagreement.
          </p>
        </div>
      </section>

      {strata && <PsdqValidationPanel strata={strata} />}

      {summary && rows.length > 0 && <PsdqExplorer summary={summary} rows={rows} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The largest planning risk is not only the largest facility gap.</h2>
          <p>
            The L3 source-disagreement view pairs the registry-map disagreement with
            Google Open Buildings p85 denominators near coordinate-ready
            facilities. That makes the visual operational: a small public-map
            ratio matters more where many buildings sit near the facilities
            whose visibility is being checked.
          </p>
        </div>
        <div className="showcase-fact-list">
          {topRow && (
            <div>
              <span>Highest exposure-proxy row</span>
              <strong>
                {topRow.upazila_name}, {topRow.district_name}:{" "}
                {formatNumber(topRow.active_clinical_facilities)} DGHS clinical /{" "}
                {formatNumber(topRow.osm_health)} OSM health;{" "}
                {formatNumber(topRow.underobserved_buildings_3km_p85_proxy)} proxy
              </strong>
            </div>
          )}
          {bangladesh && (
            <div>
              <span>National clinical-tier context</span>
              <strong>
                OSM captures {pct(bangladesh.totals.ratio_osm_to_clinical, 1)} of
                DGHS clinical-tier registry counts in the committed PSDQ panel
              </strong>
            </div>
          )}
          {summary && (
            <div>
              <span>Source retrieval record</span>
              <strong>
                OSM base {summary.osm.timestamp_osm_base}; generated {summary.generated_at}
              </strong>
            </div>
          )}
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What this does not mean</p>
          <h2>A registry-map gap is not a verified access or quality result.</h2>
          <p>
            The exposure proxy is not population, households, service demand,
            poverty, travel time, or proof that either source is ground truth.
            It is a source-quality screen that should trigger facility-level
            matching, registry validation, and source-vintage review before a
            service-access claim is made.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Reproduce the deepening</p>
          <code>python public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py</code>
          <code>python public-service-data-quality/scripts/build-bgd-source-disagreement-strata.py</code>
          <a href="/programs/public-service-data-quality/source-disagreement-l3-module.md" download>
            Download L3 evidence note
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.json" download>
            Download strata JSON
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.csv" download>
            Download strata CSV
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement-summary.json" download>
            Download summary JSON
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement.csv" download>
            Download ranked CSV
          </a>
          <Link to="/public-service-data-quality?view=evidence">
            Read PSDQ evidence packet
          </Link>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={4} />

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">Operational use</p>
          <h2>Use the disagreement screen before drawing the access map.</h2>
          <p>
            A health ministry, statistics office, or ADB operations team could
            use this view as a source-QA gate: identify where registry and
            public-map counts diverge, prioritize validation samples, and keep
            the caveat visible when downstream catchment or road-access
            analysis depends on facility locations.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Related source QA reports</p>
          <Link to="/showcase/access-map-completeness">Access map-completeness audit</Link>
          <Link to="/showcase/remittance-flow-weighting">Remittance flow-weighting module</Link>
          <Link to="/showcase/air-monitoring-observability">Air-monitoring observability</Link>
          <Link to="/factory">Factory rules</Link>
        </div>
      </section>
    </article>
  );
}

function PsdqValidationPanel({ strata }: { strata: PsdqSourceStrata }) {
  const zeroOsmRow = strata.top_lists.top_zero_osm_high_proxy_upazilas[0];
  const counterExample = strata.top_lists.top_osm_equals_or_exceeds_registry_upazilas[0];
  const roadRow = strata.top_lists.top_road_context_upazilas[0];

  return (
    <section className="showcase-section psdq-validation-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Source validation stack</p>
          <h2>The useful result is the QA ledger behind the map.</h2>
          <p>
            The L3 module does not ask a reader to trust a chart by eye. It
            exposes the rows that can support an exposure screen, the rows that
            still need source validation, and the counterexamples where OSM
            equals or exceeds the registry count.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Open Buildings coverage</span>
            <strong>
              {formatNumber(strata.coverage.rows_with_open_buildings_denominator)} of{" "}
              {formatNumber(strata.coverage.registry_admin_rows)} registry rows have the denominator
            </strong>
          </div>
          <div>
            <span>OSM feature-join residue</span>
            <strong>
              {formatNumber(strata.validation_strata.registry_rows_without_joined_osm_features)} rows
              have no joined OSM feature row; {formatNumber(strata.coverage.osm_features_not_joined_to_registry)} OSM features
              stay outside registry rows
            </strong>
          </div>
          <div>
            <span>Counterexample guardrail</span>
            <strong>
              {formatNumber(strata.validation_strata.rows_where_osm_equals_or_exceeds_registry)} rows have OSM
              counts equal to or above the active registry count
            </strong>
          </div>
          <div>
            <span>Road context eligibility</span>
            <strong>
              {formatNumber(strata.validation_strata.rows_eligible_for_road_surface_score)} rows meet the
              classified-road threshold for the road-context score
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-strata-chart-wrap">
        <PsdqStrataChart strata={strata.ratio_strata} />
      </div>

      <div className="showcase-month-readout psdq-validation-readout">
        <div>
          <span>Zero-OSM validation row</span>
          <strong>
            {zeroOsmRow
              ? `${zeroOsmRow.upazila_name}, ${zeroOsmRow.district_name}: ${formatNumber(zeroOsmRow.active_clinical_facilities)} DGHS clinical and ${formatNumber(zeroOsmRow.underobserved_buildings_3km_p85_proxy)} proxy`
              : "No zero-OSM row in the current artifact"}
          </strong>
        </div>
        <div>
          <span>OSM-above-registry row</span>
          <strong>
            {counterExample
              ? `${counterExample.upazila_name}, ${counterExample.district_name}: ${formatNumber(counterExample.osm_health)} OSM / ${formatNumber(counterExample.active_clinical_facilities)} DGHS`
              : "No OSM-above-registry row in the current artifact"}
          </strong>
        </div>
        <div>
          <span>Road-context top row</span>
          <strong>
            {roadRow
              ? `${roadRow.upazila_name}, ${roadRow.district_name}: score ${formatNumber(roadRow.road_context_score)}`
              : "Road-context artifact not loaded"}
          </strong>
        </div>
      </div>
    </section>
  );
}

function PsdqStrataChart({ strata }: { strata: PsdqRatioStratum[] }) {
  const width = 1040;
  const rowHeight = 38;
  const headerHeight = 58;
  const bottom = 20;
  const height = headerHeight + strata.length * rowHeight + bottom;
  const labelX = 0;
  const barX = 210;
  const barWidth = 250;
  const activeX = 500;
  const osmX = 650;
  const proxyX = 780;
  const maxRows = Math.max(1, ...strata.map((row) => row.row_count));

  return (
    <svg
      className="psdq-strata-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Bangladesh PSDQ ratio strata and validation buckets"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Ratio strata used as validation gates
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: DGHS registry upazila row; source: generated PSDQ L3 strata JSON
      </text>
      <text x={barX} y={54} className="psdq-chart-head">
        Rows
      </text>
      <text x={activeX} y={54} className="psdq-chart-head">
        DGHS clinical
      </text>
      <text x={osmX} y={54} className="psdq-chart-head">
        OSM health
      </text>
      <text x={proxyX} y={54} className="psdq-chart-head">
        Under-observed proxy
      </text>

      {strata.map((row, index) => {
        const y = headerHeight + index * rowHeight;
        const rowWidth = (row.row_count / maxRows) * barWidth;
        return (
          <g key={row.bucket}>
            <text x={labelX} y={y + 16} className="psdq-row-label">
              {STRATA_LABELS[row.bucket] || row.label}
            </text>
            <rect x={barX} y={y} width={barWidth} height={18} fill="#eef2f5" />
            <rect
              x={barX}
              y={y}
              width={Math.max(1, rowWidth)}
              height={18}
              fill={strataBucketColor(row.bucket)}
            >
              <title>{`${row.label}: ${formatNumber(row.row_count)} rows`}</title>
            </rect>
            <text x={barX + barWidth + 12} y={y + 14} className="psdq-value">
              {formatNumber(row.row_count)}
            </text>
            <text x={activeX} y={y + 14} className="psdq-value">
              {formatNumber(row.active_clinical_facilities)}
            </text>
            <text x={osmX} y={y + 14} className="psdq-value">
              {formatNumber(row.osm_health)}
            </text>
            <text x={proxyX} y={y + 14} className="psdq-value">
              {formatNumber(row.underobserved_buildings_3km_p85_proxy)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function strataBucketColor(bucket: string) {
  if (bucket === "zero_osm") return "#9b2226";
  if (bucket === "osm_ge_registry") return "#5A8227";
  if (bucket === "no_clinical_registry") return "#6c757d";
  return "#007DB8";
}

function PsdqHeroRails({ rows }: { rows: PsdqExposureRow[] }) {
  const maxClinical = Math.max(1, ...rows.map((row) => row.active_clinical_facilities));
  return (
    <div className="psdq-hero-rails" aria-label="Top PSDQ registry-map rows">
      <p className="showcase-source-title">Registry visible on the public map</p>
      {rows.map((row) => (
        <div className="psdq-hero-row" key={row.join_key}>
          <div>
            <strong>{row.upazila_name}</strong>
            <span>{row.district_name}</span>
          </div>
          <div className="psdq-hero-bars" aria-label={`${row.upazila_name} registry and OSM counts`}>
            <i
              className="psdq-registry-bar"
              style={{ width: `${Math.max(3, (row.active_clinical_facilities / maxClinical) * 100)}%` }}
            />
            <i
              className="psdq-osm-bar"
              style={{ width: `${Math.max(2, (row.osm_health / maxClinical) * 100)}%` }}
            />
          </div>
          <em>{pct(row.osm_to_active_clinical_ratio, 0)}</em>
        </div>
      ))}
      <div className="shock-hero-key">
        <span><i className="psdq-registry-key" /> DGHS clinical registry</span>
        <span><i className="psdq-osm-key" /> OSM health features</span>
      </div>
    </div>
  );
}

function PsdqExplorer({
  summary,
  rows,
}: {
  summary: PsdqExposureSummary;
  rows: PsdqExposureRow[];
}) {
  const [metric, setMetric] = useState<MetricMode>("exposure");
  const [division, setDivision] = useState(ALL_DIVISIONS);
  const [selectedJoinKey, setSelectedJoinKey] = useState("");

  const divisions = useMemo(
    () => [
      ALL_DIVISIONS,
      ...Array.from(new Set(rows.map((row) => row.division_name))).sort((a, b) => a.localeCompare(b)),
    ],
    [rows],
  );

  const filteredRows = useMemo(() => {
    const pool = rows.filter((row) => {
      const inDivision = division === ALL_DIVISIONS || row.division_name === division;
      return inDivision && row.has_open_buildings_denominator === 1 && row.active_clinical_facilities >= 20;
    });
    return pool.sort((a, b) => {
      if (metric === "ratio") {
        return (
          a.osm_to_active_clinical_ratio - b.osm_to_active_clinical_ratio ||
          b.active_clinical_facilities - a.active_clinical_facilities
        );
      }
      return metricValue(b, metric) - metricValue(a, metric);
    });
  }, [division, metric, rows]);

  const displayRows = filteredRows.slice(0, 16);
  const selectedRow =
    filteredRows.find((row) => row.join_key === selectedJoinKey) ||
    displayRows[0] ||
    filteredRows[0];

  return (
    <section className="showcase-section showcase-explorer">
      <div className="showcase-explorer-head">
        <div>
          <p className="kicker">Interactive evidence view</p>
          <h2>Rank the gap by the question being asked.</h2>
          <p>
            The chart keeps the source disagreement visible. Blue cells are the
            OSM-visible share of the DGHS clinical registry; red cells are the
            registry share not visible in the public-map count. The bar on the
            right is the 3 km p85 under-observed building proxy.
          </p>
        </div>
        <div className="showcase-controls" aria-label="PSDQ explorer controls">
          <div className="showcase-filter-buttons psdq-filter-buttons" role="group" aria-label="Select PSDQ metric">
            {METRIC_OPTIONS.map((option) => (
              <button
                key={option.id}
                type="button"
                className={metric === option.id ? "showcase-control-active" : ""}
                onClick={() => {
                  setMetric(option.id);
                  setSelectedJoinKey("");
                }}
              >
                {option.label}
              </button>
            ))}
          </div>
          <label>
            <span>Division</span>
            <select
              value={division}
              onChange={(event) => {
                setDivision(event.target.value);
                setSelectedJoinKey("");
              }}
            >
              {divisions.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span>Focus upazila</span>
            <select
              value={selectedRow?.join_key || ""}
              onChange={(event) => setSelectedJoinKey(event.target.value)}
            >
              {filteredRows.slice(0, 80).map((row) => (
                <option key={row.join_key} value={row.join_key}>
                  {row.upazila_name}, {row.district_name}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      <div className="psdq-chart-wrap">
        <PsdqDisagreementChart
          rows={displayRows}
          metric={metric}
          selectedJoinKey={selectedRow?.join_key}
          onSelect={setSelectedJoinKey}
        />
      </div>

      <div className="freshness-legend psdq-legend" aria-label="PSDQ source legend">
        <span><i style={{ background: "#007DB8" }} /> OSM-visible registry share</span>
        <span><i style={{ background: "#9b2226" }} /> Registry share not visible in OSM count</span>
        <span><i style={{ background: "#FBB00E" }} /> Selected row</span>
        <span><i style={{ background: "#5A8227" }} /> Under-observed building proxy</span>
      </div>

      <div className="showcase-month-readout">
        <div>
          <span>Selected upazila</span>
          <strong>
            {selectedRow
              ? `${selectedRow.upazila_name}, ${selectedRow.district_name}, ${selectedRow.division_name}`
              : "Select a row"}
          </strong>
        </div>
        <div>
          <span>Registry and public-map counts</span>
          <strong>
            {selectedRow
              ? `${formatNumber(selectedRow.active_clinical_facilities)} DGHS clinical; ${formatNumber(selectedRow.osm_health)} OSM health; ${pct(selectedRow.osm_to_active_clinical_ratio, 1)} OSM / registry`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Exposure proxy</span>
          <strong>
            {selectedRow
              ? `${formatNumber(selectedRow.underobserved_buildings_3km_p85_proxy)} of ${formatNumber(selectedRow.buildings_nearest_3km_p85)} p85 buildings`
              : "missing"}
          </strong>
        </div>
      </div>

      <p className="psdq-method-note">
        Source method: {summary.method} Non-claim: {summary.non_claim}
      </p>
    </section>
  );
}

function PsdqDisagreementChart({
  rows,
  metric,
  selectedJoinKey,
  onSelect,
}: {
  rows: PsdqExposureRow[];
  metric: MetricMode;
  selectedJoinKey?: string;
  onSelect: (joinKey: string) => void;
}) {
  const width = 1040;
  const rowHeight = 40;
  const headerHeight = 58;
  const bottom = 22;
  const height = headerHeight + rows.length * rowHeight + bottom;
  const labelWidth = 232;
  const cellCount = 24;
  const cellSize = 8;
  const cellGap = 2;
  const stripX = labelWidth + 8;
  const stripWidth = cellCount * cellSize + (cellCount - 1) * cellGap;
  const ratioX = stripX + stripWidth + 32;
  const countX = ratioX + 86;
  const barX = countX + 152;
  const barWidth = 210;
  const maxProxy = Math.max(1, ...rows.map((row) => row.underobserved_buildings_3km_p85_proxy));

  return (
    <svg
      className="psdq-disagreement-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Bangladesh PSDQ registry-map source disagreement by upazila"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Source disagreement workbench
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Rows shown: 20+ DGHS clinical facilities and an Open Buildings denominator; sorted by {metric}
      </text>
      <text x={stripX} y={54} className="psdq-chart-head">
        OSM-visible registry share
      </text>
      <text x={ratioX} y={54} className="psdq-chart-head">
        OSM / reg
      </text>
      <text x={countX} y={54} className="psdq-chart-head">
        DGHS / OSM
      </text>
      <text x={barX} y={54} className="psdq-chart-head">
        Under-observed building proxy
      </text>

      {rows.map((row, rowIndex) => {
        const y = headerHeight + rowIndex * rowHeight;
        const visibleCells = Math.max(
          0,
          Math.min(cellCount, Math.floor(row.osm_to_active_clinical_ratio * cellCount)),
        );
        const selected = row.join_key === selectedJoinKey;
        const proxyWidth = (row.underobserved_buildings_3km_p85_proxy / maxProxy) * barWidth;
        return (
          <g
            key={row.join_key}
            className="psdq-chart-row"
            onMouseEnter={() => onSelect(row.join_key)}
            onClick={() => onSelect(row.join_key)}
          >
            <rect
              x={0}
              y={y - 6}
              width={width}
              height={rowHeight - 4}
              fill={selected ? "rgba(251, 176, 14, 0.13)" : "transparent"}
            />
            <text x={0} y={y + 10} className={selected ? "psdq-row-label psdq-row-selected" : "psdq-row-label"}>
              {row.upazila_name}
            </text>
            <text x={0} y={y + 26} className="psdq-row-sub">
              {row.district_name}, {row.division_name}
            </text>
            {Array.from({ length: cellCount }).map((_, cellIndex) => (
              <rect
                key={`${row.join_key}-${cellIndex}`}
                x={stripX + cellIndex * (cellSize + cellGap)}
                y={y}
                width={cellSize}
                height={18}
                rx={1.5}
                fill={cellIndex < visibleCells ? "#007DB8" : "#9b2226"}
                opacity={cellIndex < visibleCells ? 0.95 : 0.38}
              >
                <title>
                  {`${row.upazila_name}: ${pct(row.osm_to_active_clinical_ratio, 1)} OSM / registry`}
                </title>
              </rect>
            ))}
            <text x={ratioX} y={y + 13} className={selected ? "psdq-value psdq-row-selected" : "psdq-value"}>
              {pct(row.osm_to_active_clinical_ratio, 1)}
            </text>
            <text x={countX} y={y + 13} className="psdq-value">
              {formatNumber(row.active_clinical_facilities)} / {formatNumber(row.osm_health)}
            </text>
            <rect x={barX} y={y} width={barWidth} height={18} fill="#eef2f5" />
            <rect
              x={barX}
              y={y}
              width={Math.max(1, proxyWidth)}
              height={18}
              fill={selected ? "#FBB00E" : "#5A8227"}
            />
            <text x={barX + barWidth + 12} y={y + 13} className="psdq-value">
              {metricLabel(row, metric)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
