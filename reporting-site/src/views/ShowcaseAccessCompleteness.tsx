"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface AccessRegionRow {
  admin1_name: string;
  population_2020?: number;
  osm_health?: number;
  registry_clinical?: number;
  capture_ratio: number;
  osm_people_per_facility: number;
  registry_people_per_facility: number;
  rank_osm: number;
  rank_registry: number;
  rank_shift: number;
}

interface ClusterRow {
  iso3: string;
  country: string;
  worst_adm1_name: string;
  osm_worst_people_per_facility: number;
  capture_ratio_applied: number | null;
  corrected_people_per_facility: number | null;
  correction_source: string;
}

interface AccessDeepening {
  attestation_chain: string;
  generated_at: string;
  sources: Record<string, string>;
  identity_check: {
    access_phl_worst_adm1: string;
    access_phl_worst_ppf: number;
    psdq_armm_pop_over_osm: number;
    match: boolean;
  };
  phl_internal_contradiction: {
    n_regions: number;
    pearson_r_loglog: number;
    pearson_r2_loglog: number;
    spearman_rho: number;
    capture_best: { region: string; ratio: number };
    capture_worst: { region: string; ratio: number };
  };
  phl_correction: {
    worst_on_osm: { region: string; ppf: number };
    worst_on_osm_registry_corrected_ppf: number;
    worst_on_registry: { region: string; ppf: number };
    n_adm1_rank_changed: number;
    n_adm1_total: number;
  };
  phl_rows: AccessRegionRow[];
  bgd_rows: AccessRegionRow[];
  bgd_internal_contradiction: {
    pearson_r_level: number;
    pearson_r2_level: number;
  };
  cluster_worst_adm1_corrected: ClusterRow[];
}

interface CambodiaAuditRow {
  admin1_name: string;
  source_join_status: string;
  population: number;
  osm_health_facilities: number;
  osm_people_per_health_facility: number;
  government_health_centers_2010: number;
  government_health_posts_2010: number;
  government_referral_hospitals_2010: number;
  operational_district_points_2010_context: number;
  government_facilities_2010_included: number;
  government_people_per_facility_2010: number | null;
  osm_to_government_facility_ratio: number | null;
  osm_load_to_government_load_ratio: number | null;
  rank_osm_health_load_joined_only: number | null;
  rank_government_health_load_2010_joined_only: number | null;
  rank_shift_after_2010_inventory: number | null;
  join_note: string;
}

interface AccessCambodiaAudit {
  attestation_chain: string;
  generated_at: string;
  claim_scope: string;
  summary: {
    access_khm_rows: number;
    joined_rows: number;
    unmatched_rows: number;
    unmatched_admin1_names: string[];
    government_facilities_2010_included_total: number;
    operational_district_points_2010_context_total: number;
    osm_health_facilities_access_panel_total: number;
    national_osm_to_government_facility_ratio: number;
    rank_changed_after_2010_inventory: number;
    rank_joined_total: number;
    oddar_meanchey: {
      osm_health_facilities: number;
      government_facilities_2010_included: number;
      osm_people_per_health_facility: number;
      government_people_per_facility_2010: number;
      osm_load_to_government_load_ratio: number;
      rank_osm: number;
      rank_government: number;
    };
    phnom_penh_scope_warning: {
      osm_health_facilities: number;
      government_facilities_2010_included: number;
      osm_to_government_facility_ratio: number;
      note: string;
    };
    largest_osm_load_ratios: Array<{
      admin1_name: string;
      osm_health_facilities: number;
      government_facilities_2010_included: number;
      osm_people_per_health_facility: number;
      government_people_per_facility_2010: number;
      osm_load_to_government_load_ratio: number;
    }>;
  };
  rows: CambodiaAuditRow[];
}

type AccessMode = "flip" | "scatter" | "cluster";

const ACCESS_MODES: Array<{ id: AccessMode; label: string }> = [
  { id: "flip", label: "Rank flip" },
  { id: "scatter", label: "Completeness signal" },
  { id: "cluster", label: "Correction wall" },
];

function formatNumber(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString("en-US", { maximumFractionDigits: 0 });
}

function pct(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${(value * 100).toFixed(digits)}%`;
}

function signed(value: number) {
  return value > 0 ? `+${value}` : `${value}`;
}

function regionByName(rows: AccessRegionRow[], name: string) {
  return rows.find((row) => row.admin1_name === name);
}

function cambodiaRowByName(rows: CambodiaAuditRow[], name: string) {
  return rows.find((row) => row.admin1_name === name);
}

export default function ShowcaseAccessCompleteness() {
  const [data, setData] = useState<AccessDeepening | null>(null);
  const [cambodia, setCambodia] = useState<AccessCambodiaAudit | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [cambodiaError, setCambodiaError] = useState<string | null>(null);
  const [mode, setMode] = useState<AccessMode>("flip");
  const [focus, setFocus] = useState("ARMM");

  useEffect(() => {
    fetch("/programs/access-services/generated/access-osm-completeness-deepening.json")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((payload: AccessDeepening) => setData(payload))
      .catch((err) => setError(String(err)));
  }, []);

  useEffect(() => {
    fetch("/programs/access-services/generated/access-cambodia-health-facility-source-audit.json")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((payload: AccessCambodiaAudit) => setCambodia(payload))
      .catch((err) => setCambodiaError(String(err)));
  }, []);

  const sortedRegions = useMemo(
    () => [...(data?.phl_rows ?? [])].sort((a, b) => a.rank_osm - b.rank_osm),
    [data],
  );
  const focusRegion = data ? regionByName(data.phl_rows, focus) ?? data.phl_rows[0] : undefined;

  return (
    <article className="showcase-page access-showcase">
      <header className="showcase-hero access-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">Public-data evidence note</p>
          <h1 className="showcase-title showcase-title-wide">
            When the Access Gap Is the Map Gap
          </h1>
          <p className="showcase-lede">
            The access screen counts people per OpenStreetMap health point. A
            Philippines registry join shows why that is risky: the screen's
            worst-access region is also the worst-mapped region, and the
            regional order nearly flips once the official registry denominator
            is used. A Cambodia source pass now tests the largest unresolved
            row against a public HDX/MoH/OCHA facility inventory.
          </p>
          <div className="showcase-meta">
            <span>{data?.attestation_chain || "ai-first"}</span>
            <span>Evidence audit</span>
            <span>Triage screen, not an access ranking</span>
          </div>
        </div>
        <div className="showcase-hero-panel access-hero-panel" aria-label="Access completeness evidence summary">
          {data ? (
            <>
              <AccessHeroBars data={data} />
              <div className="access-hero-stats">
                <div>
                  <span className="showcase-stat-value">
                    {data.phl_correction.n_adm1_rank_changed}/{data.phl_correction.n_adm1_total}
                  </span>
                  <span className="showcase-stat-label">Philippine regions re-rank after correction</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {data.phl_internal_contradiction.spearman_rho.toFixed(2)}
                  </span>
                  <span className="showcase-stat-label">rank correlation between mapping capture and OSM load</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {cambodia
                      ? `${cambodia.summary.oddar_meanchey.osm_health_facilities} to ${cambodia.summary.oddar_meanchey.government_facilities_2010_included}`
                      : "--"}
                  </span>
                  <span className="showcase-stat-label">Oddar Meanchey OSM points versus 2010 public-source facilities</span>
                </div>
              </div>
            </>
          ) : (
            <p className="showcase-loading">{error || "Loading access-completeness evidence..."}</p>
          )}
        </div>
      </header>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Measurement problem</p>
          <h2>Counting mapped clinics is not the same as measuring access.</h2>
          <p>
            The original screen was useful as a triage device because it made
            public service visibility concrete. The deeper question is whether
            high people-per-facility values reveal service scarcity or a thin
            public map. For the Philippines and Bangladesh, the sibling PSDQ
            program has the official-registry denominator needed to test that
            distinction.
          </p>
        </div>
        <div className="showcase-note">
          <strong>Source upgrade.</strong> The report joins the access panel's
          OSM health-point numerator to PSDQ registry capture rates from DOH
          NHFR and the Bangladesh DGHS registry, then adds a Cambodia HDX
          public-facility source audit for the largest unresolved row. No
          modeled number is supplied by AI; the scripts recompute the panels
          from public source files and committed artifacts.
        </div>
      </section>

      <section className="showcase-explorer">
        <div className="showcase-explorer-head">
          <div>
            <p className="kicker kicker-crimson">Interactive evidence view</p>
            <h2>The result changes when the denominator changes.</h2>
            <p>
              The rank-flip view compares OSM people-per-facility with
              registry people-per-facility for all Philippine regions. The
              scatter asks whether the OSM access score is mostly a mapping
              completeness signal. The correction wall shows which cross-country
              extremes can and cannot be corrected from data already on disk.
            </p>
          </div>
          <div className="showcase-controls">
            {ACCESS_MODES.map((option) => (
              <button
                key={option.id}
                type="button"
                className={option.id === mode ? "active" : ""}
                onClick={() => setMode(option.id)}
              >
                {option.label}
              </button>
            ))}
            {mode !== "cluster" && (
              <label>
                Focus region
                <select value={focus} onChange={(event) => setFocus(event.target.value)}>
                  {sortedRegions.map((row) => (
                    <option key={row.admin1_name} value={row.admin1_name}>
                      {row.admin1_name}
                    </option>
                  ))}
                </select>
              </label>
            )}
          </div>
        </div>

        <div className="access-evidence-grid">
          <div className="access-main-chart">
            {!data ? (
              <p className="showcase-loading">{error || "Loading chart data..."}</p>
            ) : mode === "flip" ? (
              <RankFlipChart rows={data.phl_rows} focus={focus} />
            ) : mode === "scatter" ? (
              <CompletenessScatter rows={data.phl_rows} focus={focus} />
            ) : (
              <ClusterCorrectionChart rows={data.cluster_worst_adm1_corrected} cambodia={cambodia} />
            )}
          </div>
          <div className="access-side-panel">
            {!data ? (
              <p className="showcase-loading">Loading readout...</p>
            ) : mode === "cluster" ? (
              <ClusterReadout data={data} cambodia={cambodia} />
            ) : (
              <RegionReadout row={focusRegion} data={data} />
            )}
          </div>
        </div>
      </section>

      <section className="showcase-section access-cambodia-source" data-access-cambodia-source>
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Cambodia source extension</p>
          <h2>Oddar Meanchey stops being a wall and becomes a testable source row.</h2>
          <p>
            The new audit retrieves the public HDX Cambodia Health Facilities
            package, parses government health centers, health posts, and
            referral hospitals, and joins those counts to the Cambodia ADM1
            OSM panel. It does not make a travel-time claim, and it does not
            treat a 2010 public-facility inventory as a complete current
            clinical registry.
          </p>
        </div>
        {cambodia ? (
          <div className="access-source-grid">
            <div className="access-source-stats" aria-label="Cambodia source audit summary">
              <div>
                <span>{cambodia.summary.joined_rows}/{cambodia.summary.access_khm_rows}</span>
                <p>Cambodia ADM1 rows joined to the 2010 source</p>
              </div>
              <div>
                <span>{formatNumber(cambodia.summary.government_facilities_2010_included_total)}</span>
                <p>health centers, posts, and referral hospitals counted</p>
              </div>
              <div>
                <span>{cambodia.summary.rank_changed_after_2010_inventory}/{cambodia.summary.rank_joined_total}</span>
                <p>joined rows re-rank after the denominator changes</p>
              </div>
              <div>
                <span>{cambodia.summary.oddar_meanchey.osm_load_to_government_load_ratio.toFixed(2)}x</span>
                <p>Oddar Meanchey OSM load versus 2010 public-source load</p>
              </div>
            </div>
            <div className="showcase-note access-source-warning">
              <strong>Source-scope warning.</strong> Phnom Penh has{" "}
              {formatNumber(cambodia.summary.phnom_penh_scope_warning.osm_health_facilities)}
              {" "}OSM health points versus{" "}
              {formatNumber(cambodia.summary.phnom_penh_scope_warning.government_facilities_2010_included)}
              {" "}facilities in the 2010 public inventory. That is a scope and
              vintage mismatch, not proof that either source is the full health
              system.
            </div>
          </div>
        ) : (
          <p className="showcase-loading">{cambodiaError || "Loading Cambodia source audit..."}</p>
        )}
      </section>

      {cambodia && (
        <section className="showcase-explorer access-cambodia-ledger">
          <div className="showcase-explorer-head">
            <div>
              <p className="kicker kicker-blue">Public-source ledger</p>
              <h2>The Cambodia row changes, but the access claim still waits.</h2>
              <p>
                The chart compares the highest Cambodia OSM people-per-health-
                point rows with the 2010 public-facility denominator. Some
                extreme OSM values collapse; others stay high; one row needs a
                boundary-year crosswalk.
              </p>
            </div>
          </div>
          <div className="access-evidence-grid">
            <div className="access-main-chart">
              <CambodiaFacilityLedger audit={cambodia} />
            </div>
            <div className="access-side-panel">
              <CambodiaSourceReadout audit={cambodia} />
            </div>
          </div>
        </section>
      )}

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">What changed after deepening</p>
          <h2>The headline moved from access ranking to source audit.</h2>
          <p>
            The stronger report is not "which region has the worst access."
            It is a reproducible warning about public-source measurement: for
            the Philippines, the region flagged by the OSM screen is the same
            region with the lowest OSM capture against the official clinical
            registry. The screen becomes useful only when it is read as a
            map-completeness-aware triage layer. Cambodia extends that lesson:
            the most dramatic unresolved value drops when a public facility
            source is counted, but the source vintage and scope still stop an
            access claim.
          </p>
        </div>
        <div className="showcase-note">
          <strong>Non-claim.</strong> Registry and public-facility counts are
          not functioning capacity, service quality, travel time, staffing, or
          utilization. The correction removes one map-coverage confound; it
          does not turn the screen into an official access statistic.
        </div>
      </section>

      <ShowcaseQualityPanel reportId={7} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Operational use</p>
          <h2>Use the screen to choose where source validation comes first.</h2>
          <p>
            ADB sector teams, national statistics offices, and health ministries
            can use this kind of join to decide whether a service-access screen
            is ready for targeting, or whether registry matching, map audits,
            and travel-time denominators must be added before the evidence is
            used for planning.
          </p>
        </div>
        <div className="showcase-links">
          <a href="/programs/access-services/generated/access-osm-completeness-deepening.json" download>
            Download deepening JSON
          </a>
          <a href="/programs/access-services/generated/access-osm-completeness-deepening-phl.csv" download>
            Download Philippine correction CSV
          </a>
          <a href="/programs/access-services/generated/access-cambodia-health-facility-source-audit.json" download>
            Download Cambodia source audit JSON
          </a>
          <a href="/programs/access-services/generated/access-cambodia-health-facility-source-audit.csv" download>
            Download Cambodia source audit CSV
          </a>
          <a href="/programs/access-services/generated/access-services-adb-panel.json" download>
            Download original access panel
          </a>
          <Link href="/access-services?view=evidence">Program evidence</Link>
        </div>
      </section>
    </article>
  );
}

function AccessHeroBars({ data }: { data: AccessDeepening }) {
  const osm = data.phl_correction.worst_on_osm.ppf;
  const corrected = data.phl_correction.worst_on_osm_registry_corrected_ppf;
  const max = osm;
  const correctedWidth = Math.max(7, (corrected / max) * 100);

  return (
    <div className="access-hero-bars">
      <div>
        <span>ARMM on OSM screen</span>
        <strong>{formatNumber(osm)}</strong>
        <div className="access-hero-bar">
          <i style={{ width: "100%" }} />
        </div>
      </div>
      <div>
        <span>Same ARMM on registry denominator</span>
        <strong>{formatNumber(corrected)}</strong>
        <div className="access-hero-bar access-hero-bar-muted">
          <i style={{ width: `${correctedWidth}%` }} />
        </div>
      </div>
      <p>
        {data.identity_check.match ? "Identity check passed" : "Identity check failed"}:
        PSDQ population divided by OSM health points reproduces the access
        panel's ARMM value.
      </p>
    </div>
  );
}

function RankFlipChart({ rows, focus }: { rows: AccessRegionRow[]; focus: string }) {
  const sorted = [...rows].sort((a, b) => a.rank_osm - b.rank_osm);
  const mobileRows = useMemo(() => {
    const byShift = [...rows].sort((a, b) => Math.abs(b.rank_shift) - Math.abs(a.rank_shift));
    const picked = new Map<string, AccessRegionRow>();
    const armm = regionByName(rows, "ARMM");
    if (armm) picked.set(armm.admin1_name, armm);
    for (const row of byShift) {
      picked.set(row.admin1_name, row);
      if (picked.size >= 6) break;
    }
    return [...picked.values()];
  }, [rows]);
  const width = 760;
  const rowGap = 27;
  const margin = { top: 58, right: 168, bottom: 36, left: 168 };
  const height = margin.top + margin.bottom + rowGap * (rows.length - 1);
  const leftX = 260;
  const rightX = 500;
  const y = (rank: number) => margin.top + (rank - 1) * rowGap;

  return (
    <div className="access-chart-wrap">
      <div className="access-mobile-rank-summary" aria-label="Mobile rank-shift summary">
        <p>Largest rank shifts after registry correction</p>
        {mobileRows.map((row) => (
          <div key={row.admin1_name} className={row.admin1_name === focus ? "is-focus" : ""}>
            <span>{row.admin1_name}</span>
            <strong>
              {row.rank_osm} to {row.rank_registry}
            </strong>
            <i style={{ width: `${Math.max(8, Math.min(100, Math.abs(row.rank_shift) * 7))}%` }} />
            <em>{signed(row.rank_shift)}</em>
          </div>
        ))}
      </div>
      <svg className="access-rank-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Philippine access rank flip after registry correction">
        <text x={leftX} y={22} textAnchor="middle" className="access-chart-title">
          OSM screen rank
        </text>
        <text x={rightX} y={22} textAnchor="middle" className="access-chart-title">
          Registry-corrected rank
        </text>
        <text x={leftX} y={42} textAnchor="middle" className="access-chart-subtitle">
          1 = highest people per OSM health point
        </text>
        <text x={rightX} y={42} textAnchor="middle" className="access-chart-subtitle">
          1 = highest people per registry facility
        </text>
        <line x1={leftX} x2={leftX} y1={margin.top - 10} y2={height - margin.bottom + 8} className="access-axis" />
        <line x1={rightX} x2={rightX} y1={margin.top - 10} y2={height - margin.bottom + 8} className="access-axis" />
        {sorted.map((row) => {
          const isFocus = row.admin1_name === focus;
          const worsens = row.rank_registry < row.rank_osm;
          return (
            <g key={row.admin1_name} className={isFocus ? "is-focus" : ""}>
              <line
                x1={leftX}
                y1={y(row.rank_osm)}
                x2={rightX}
                y2={y(row.rank_registry)}
                className={worsens ? "access-rank-line access-rank-worse" : "access-rank-line"}
              />
              <circle cx={leftX} cy={y(row.rank_osm)} r={isFocus ? 5 : 3.5} className="access-rank-dot" />
              <circle cx={rightX} cy={y(row.rank_registry)} r={isFocus ? 5 : 3.5} className="access-rank-dot" />
              <text x={leftX - 12} y={y(row.rank_osm) + 4} textAnchor="end" className="access-rank-label">
                {row.rank_osm}. {row.admin1_name}
              </text>
              <text x={rightX + 12} y={y(row.rank_registry) + 4} className="access-rank-label">
                {row.rank_registry}. {row.admin1_name}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function CompletenessScatter({ rows, focus }: { rows: AccessRegionRow[]; focus: string }) {
  const width = 760;
  const height = 440;
  const margin = { top: 46, right: 34, bottom: 70, left: 86 };
  const xMin = Math.log10(0.055);
  const xMax = Math.log10(0.7);
  const yMin = Math.log10(10000);
  const yMax = Math.log10(80000);
  const x = (ratio: number) =>
    margin.left + ((Math.log10(ratio) - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
  const y = (ppf: number) =>
    height - margin.bottom - ((Math.log10(ppf) - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom);
  const labels = new Set([focus, "ARMM", "NCR", "Central Luzon", "Zamboanga Peninsula"]);
  const fit = useMemo(() => {
    const xs = rows.map((row) => Math.log10(row.capture_ratio));
    const ys = rows.map((row) => Math.log10(row.osm_people_per_facility));
    const meanX = xs.reduce((sum, value) => sum + value, 0) / xs.length;
    const meanY = ys.reduce((sum, value) => sum + value, 0) / ys.length;
    const sxx = xs.reduce((sum, value) => sum + (value - meanX) ** 2, 0);
    const sxy = xs.reduce((sum, value, index) => sum + (value - meanX) * (ys[index] - meanY), 0);
    const slope = sxy / sxx;
    const intercept = meanY - slope * meanX;
    const left = 0.06;
    const right = 0.66;
    return {
      x1: x(left),
      y1: y(10 ** (intercept + slope * Math.log10(left))),
      x2: x(right),
      y2: y(10 ** (intercept + slope * Math.log10(right))),
    };
  }, [rows]);

  return (
    <div className="access-chart-wrap">
      <svg className="access-scatter-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="OSM access load against OSM registry capture">
        <text x={margin.left} y={22} className="access-chart-title">
          OSM load rises where OSM capture is thin
        </text>
        {[0.07, 0.1, 0.2, 0.4, 0.65].map((tick) => (
          <g key={tick}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={height - margin.bottom} className="access-grid" />
            <text x={x(tick)} y={height - 22} textAnchor="middle" className="access-tick">
              {pct(tick, 0)}
            </text>
          </g>
        ))}
        {[10000, 20000, 40000, 70000].map((tick) => (
          <g key={tick}>
            <line x1={margin.left} x2={width - margin.right} y1={y(tick)} y2={y(tick)} className="access-grid" />
            <text x={margin.left - 10} y={y(tick) + 4} textAnchor="end" className="access-tick">
              {formatNumber(tick)}
            </text>
          </g>
        ))}
        <line x1={margin.left} x2={width - margin.right} y1={height - margin.bottom} y2={height - margin.bottom} className="access-axis" />
        <line x1={margin.left} x2={margin.left} y1={margin.top} y2={height - margin.bottom} className="access-axis" />
        <line x1={fit.x1} y1={fit.y1} x2={fit.x2} y2={fit.y2} className="access-fit-line" />
        {rows.map((row) => {
          const isFocus = row.admin1_name === focus;
          const isHigh = ["ARMM", "NCR"].includes(row.admin1_name);
          return (
            <g key={row.admin1_name} className={isFocus ? "is-focus" : ""}>
              <circle
                cx={x(row.capture_ratio)}
                cy={y(row.osm_people_per_facility)}
                r={isFocus ? 7 : isHigh ? 6 : 4}
                className={isHigh ? "access-scatter-point access-scatter-highlight" : "access-scatter-point"}
              />
              {labels.has(row.admin1_name) && (
                <text x={x(row.capture_ratio) + 8} y={y(row.osm_people_per_facility) - 8} className="access-point-label">
                  {row.admin1_name}
                </text>
              )}
            </g>
          );
        })}
        <text x={width / 2} y={height - 8} textAnchor="middle" className="access-axis-label">
          OSM capture of official clinical registry, log scale
        </text>
        <text transform={`translate(22 ${height / 2}) rotate(-90)`} textAnchor="middle" className="access-axis-label">
          people per OSM health point, log scale
        </text>
      </svg>
    </div>
  );
}

function ClusterCorrectionChart({ rows, cambodia }: { rows: ClusterRow[]; cambodia: AccessCambodiaAudit | null }) {
  const width = 760;
  const height = 430;
  const margin = { top: 50, right: 150, bottom: 52, left: 88 };
  const max = Math.max(...rows.map((row) => row.osm_worst_people_per_facility));
  const x = (value: number) => margin.left + (value / max) * (width - margin.left - margin.right);
  const y = (index: number) => margin.top + index * 39;

  return (
    <div className="access-chart-wrap">
      <svg className="access-cluster-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Cluster worst-unit correction wall">
        <text x={margin.left} y={22} className="access-chart-title">
          The largest access-screen numbers are the least correctable
        </text>
        {[100000, 200000, 300000].map((tick) => (
          <g key={tick}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top - 14} y2={height - margin.bottom} className="access-grid" />
            <text x={x(tick)} y={height - 18} textAnchor="middle" className="access-tick">
              {formatNumber(tick)}
            </text>
          </g>
        ))}
        {rows.map((row, index) => {
          const yy = y(index);
          const corrected = row.corrected_people_per_facility;
          const cambodiaPartial =
            row.iso3 === "KHM"
              ? cambodia?.summary.oddar_meanchey.government_people_per_facility_2010 ?? null
              : null;
          const shownCorrection = corrected ?? cambodiaPartial;
          const label = corrected
            ? `${formatNumber(corrected)} corrected`
            : cambodiaPartial
              ? `${formatNumber(cambodiaPartial)} HDX partial`
              : "no registry join";
          return (
            <g key={row.iso3}>
              <text x={margin.left - 12} y={yy + 14} textAnchor="end" className="access-rank-label">
                {row.iso3}
              </text>
              <rect
                x={margin.left}
                y={yy}
                width={Math.max(2, x(row.osm_worst_people_per_facility) - margin.left)}
                height={16}
                className={
                  corrected
                    ? "access-cluster-bar"
                    : cambodiaPartial
                      ? "access-cluster-bar access-cluster-partial"
                      : "access-cluster-bar access-cluster-wall"
                }
              />
              {shownCorrection && (
                <circle
                  cx={x(shownCorrection)}
                  cy={yy + 8}
                  r={5}
                  className={corrected ? "access-corrected-dot" : "access-partial-dot"}
                />
              )}
              <text x={x(row.osm_worst_people_per_facility) + 8} y={yy + 13} className="access-point-label">
                {label}
              </text>
            </g>
          );
        })}
        <text x={width / 2} y={height - 6} textAnchor="middle" className="access-axis-label">
          people per health facility in worst ADM1 unit
        </text>
      </svg>
    </div>
  );
}

function CambodiaFacilityLedger({ audit }: { audit: AccessCambodiaAudit }) {
  const rows = useMemo(
    () =>
      [...audit.rows]
        .sort((a, b) => b.osm_people_per_health_facility - a.osm_people_per_health_facility)
        .slice(0, 10),
    [audit.rows],
  );
  const mobileRows = rows.slice(0, 6);
  const width = 820;
  const rowGap = 34;
  const margin = { top: 62, right: 182, bottom: 52, left: 154 };
  const height = margin.top + margin.bottom + rowGap * rows.length;
  const max = Math.max(...rows.map((row) => row.osm_people_per_health_facility));
  const x = (value: number) => margin.left + (value / max) * (width - margin.left - margin.right);
  const barWidth = (value: number) => Math.max(2, x(value) - margin.left);
  const oddar = cambodiaRowByName(audit.rows, "Oddar Meanchey");

  return (
    <div className="access-chart-wrap">
      <div className="access-cambodia-mobile" aria-label="Mobile Cambodia public-source ledger">
        <p>Cambodia OSM load versus 2010 public-source load</p>
        {mobileRows.map((row) => (
          <div key={row.admin1_name} className={row.admin1_name === "Oddar Meanchey" ? "is-focus" : ""}>
            <span>{row.admin1_name}</span>
            <strong>
              {row.government_people_per_facility_2010
                ? `${formatNumber(row.osm_people_per_health_facility)} to ${formatNumber(row.government_people_per_facility_2010)}`
                : "needs crosswalk"}
            </strong>
            <i style={{ width: `${Math.max(6, Math.min(100, (row.osm_people_per_health_facility / max) * 100))}%` }} />
          </div>
        ))}
      </div>
      <svg className="access-cambodia-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Cambodia OSM health load against 2010 public health facility source">
        <text x={margin.left} y={24} className="access-chart-title">
          Cambodia: OSM denominator versus 2010 public-facility source
        </text>
        <text x={margin.left} y={44} className="access-chart-subtitle">
          Top rows by OSM people per health point; shorter blue bar uses health centers, posts, and referral hospitals
        </text>
        {[100000, 200000, 300000].map((tick) => (
          <g key={tick}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top - 12} y2={height - margin.bottom + 6} className="access-grid" />
            <text x={x(tick)} y={height - 18} textAnchor="middle" className="access-tick">
              {formatNumber(tick)}
            </text>
          </g>
        ))}
        <g>
          <rect x={margin.left} y={margin.top - 35} width={18} height={8} className="access-cambodia-osm" />
          <text x={margin.left + 24} y={margin.top - 28} className="access-tick">
            OSM people per health point
          </text>
          <rect x={margin.left + 214} y={margin.top - 35} width={18} height={8} className="access-cambodia-gov" />
          <text x={margin.left + 238} y={margin.top - 28} className="access-tick">
            2010 public-source people per facility
          </text>
        </g>
        {rows.map((row, index) => {
          const y0 = margin.top + index * rowGap;
          const isOddar = row.admin1_name === "Oddar Meanchey";
          const publicLoad = row.government_people_per_facility_2010;
          return (
            <g key={row.admin1_name} className={isOddar ? "is-focus" : ""}>
              <text x={margin.left - 12} y={y0 + 15} textAnchor="end" className="access-rank-label">
                {row.admin1_name}
              </text>
              <rect
                x={margin.left}
                y={y0}
                width={barWidth(row.osm_people_per_health_facility)}
                height={11}
                className="access-cambodia-osm"
              />
              {publicLoad ? (
                <rect
                  x={margin.left}
                  y={y0 + 14}
                  width={barWidth(publicLoad)}
                  height={11}
                  className="access-cambodia-gov"
                />
              ) : (
                <line
                  x1={margin.left}
                  x2={margin.left + 85}
                  y1={y0 + 19}
                  y2={y0 + 19}
                  className="access-cambodia-missing"
                />
              )}
              <text x={x(row.osm_people_per_health_facility) + 8} y={y0 + 9} className="access-point-label">
                {formatNumber(row.osm_people_per_health_facility)}
              </text>
              <text
                x={publicLoad ? x(publicLoad) + 8 : margin.left + 92}
                y={y0 + 23}
                className="access-point-label"
              >
                {publicLoad ? formatNumber(publicLoad) : "needs crosswalk"}
              </text>
            </g>
          );
        })}
        <text x={width / 2} y={height - 8} textAnchor="middle" className="access-axis-label">
          people per health point or public-source facility
        </text>
        {oddar && (
          <text x={width - margin.right + 30} y={margin.top + 14} className="access-chart-subtitle">
            Oddar: {formatNumber(oddar.osm_health_facilities)} OSM / {formatNumber(oddar.government_facilities_2010_included)} public
          </text>
        )}
      </svg>
    </div>
  );
}

function CambodiaSourceReadout({ audit }: { audit: AccessCambodiaAudit }) {
  const oddar = audit.summary.oddar_meanchey;
  const tbong = audit.summary.unmatched_admin1_names.join(", ");
  return (
    <>
      <p className="kicker kicker-blue">Cambodia source readout</p>
      <h3>{formatNumber(oddar.osm_people_per_health_facility)} falls to {formatNumber(oddar.government_people_per_facility_2010)}</h3>
      <dl className="access-readout">
        <div>
          <dt>Oddar OSM health points</dt>
          <dd>{formatNumber(oddar.osm_health_facilities)}</dd>
        </div>
        <div>
          <dt>Oddar public-source facilities</dt>
          <dd>{formatNumber(oddar.government_facilities_2010_included)}</dd>
        </div>
        <div>
          <dt>Rows with rank changes</dt>
          <dd>{audit.summary.rank_changed_after_2010_inventory}/{audit.summary.rank_joined_total}</dd>
        </div>
        <div>
          <dt>Boundary crosswalk gap</dt>
          <dd>{tbong || "none"}</dd>
        </div>
      </dl>
      <p>
        The audit improves the evidence because it supplies a public source
        for Cambodia's biggest unresolved row. It also withholds the access
        claim because the source is 2010, public-sector scoped, and not a
        travel-time or service-capacity denominator.
      </p>
    </>
  );
}

function RegionReadout({ row, data }: { row?: AccessRegionRow; data: AccessDeepening }) {
  if (!row) return <p className="showcase-loading">Choose a Philippine region.</p>;
  const ratio = row.osm_people_per_facility / row.registry_people_per_facility;
  return (
    <>
      <p className="kicker kicker-blue">Selected Philippine region</p>
      <h3>{row.admin1_name}</h3>
      <dl className="access-readout">
        <div>
          <dt>OSM people per facility</dt>
          <dd>{formatNumber(row.osm_people_per_facility)}</dd>
        </div>
        <div>
          <dt>Registry people per facility</dt>
          <dd>{formatNumber(row.registry_people_per_facility)}</dd>
        </div>
        <div>
          <dt>OSM capture of registry</dt>
          <dd>{pct(row.capture_ratio)}</dd>
        </div>
        <div>
          <dt>Rank shift</dt>
          <dd>{signed(row.rank_shift)}</dd>
        </div>
      </dl>
      <p>
        The OSM denominator makes this row look {ratio.toFixed(1)}x larger than
        the registry denominator. Across all {data.phl_internal_contradiction.n_regions}
        {" "}regions, the access ordering is strongly inverse to OSM capture
        (Spearman rho {data.phl_internal_contradiction.spearman_rho.toFixed(2)}).
      </p>
    </>
  );
}

function ClusterReadout({ data, cambodia }: { data: AccessDeepening; cambodia: AccessCambodiaAudit | null }) {
  const correctable = data.cluster_worst_adm1_corrected.filter((row) => row.corrected_people_per_facility);
  const uncorrectable = data.cluster_worst_adm1_corrected.length - correctable.length;
  const phl = data.cluster_worst_adm1_corrected.find((row) => row.iso3 === "PHL");
  const bgd = data.cluster_worst_adm1_corrected.find((row) => row.iso3 === "BGD");
  return (
    <>
      <p className="kicker kicker-blue">Cross-economy correction wall</p>
      <h3>{uncorrectable} of 8 worst-unit rows cannot be corrected from PSDQ yet</h3>
      <dl className="access-readout">
        <div>
          <dt>Correctable rows</dt>
          <dd>{correctable.map((row) => row.iso3).join(", ")}</dd>
        </div>
        <div>
          <dt>Philippines national correction</dt>
          <dd>{formatNumber(phl?.osm_worst_people_per_facility)} to {formatNumber(phl?.corrected_people_per_facility)}</dd>
        </div>
        <div>
          <dt>Bangladesh national correction</dt>
          <dd>{formatNumber(bgd?.osm_worst_people_per_facility)} to {formatNumber(bgd?.corrected_people_per_facility)}</dd>
        </div>
        {cambodia && (
          <div>
            <dt>Cambodia HDX partial check</dt>
            <dd>
              {formatNumber(cambodia.summary.oddar_meanchey.osm_people_per_health_facility)} to{" "}
              {formatNumber(cambodia.summary.oddar_meanchey.government_people_per_facility_2010)}
            </dd>
          </div>
        )}
      </dl>
      <p>
        The uncorrectable rows are not evidence that the access screen is wrong.
        Cambodia now has a public-source partial check, but Pakistan and Lao
        still need comparable registry sources before the cross-economy ordering
        can be treated as an access result.
      </p>
    </>
  );
}
