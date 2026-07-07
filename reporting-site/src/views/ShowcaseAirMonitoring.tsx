"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";
import ledgerData from "../../public/programs/air-monitoring/generated/air-monitoring-evidence-ledger.json";

const LEDGER_URL = "/programs/air-monitoring/generated/air-monitoring-evidence-ledger.json";

interface HeadlineCounts {
  ledger_rows: number;
  supporting_files_indexed: number;
  economies_in_source_discovery: number;
  economies_with_official_station_source_or_portal: number;
  official_station_rows_audited: number;
  identity_candidate_rows_checked: number;
  validated_same_station_rows: number;
  bmkg_pm25_target_rows: number;
  bmkg_station_specific_inspection_log_rows: number;
  bmkg_station_specific_calibration_certificate_rows: number;
  bmkg_calibration_status_rows: number;
  complete_monitor_grade_rows: number;
  station_radius_ready_economies: number;
  coverage_claim_allowed: boolean;
  claim_allowed_country_rows: number;
  denominator_join_rows: number;
}

interface LedgerRow {
  ledger_id: string;
  title: string;
  group: string;
  status: string;
  method: string;
  attestation_chain: string;
  generated_at: string;
  checked_rows: number;
  source_inputs_count: number;
  zero_claim_fields: string[];
  zero_claim_field_count: number;
  substantive_finding: string;
  reader_use: string;
  artifact_path: string;
  summary_path: string;
  csv_path: string;
  non_claim: string;
}

interface EconomyRow {
  iso3: string;
  country: string;
  official_station_source_or_portal: boolean | null;
  monitor_grade_rows_audited: number;
  identity_candidate_rows: number;
  validated_same_station_rows: number;
  station_radius_coordinate_rows: number;
  station_radius_ready_rows: number;
}

interface EvidenceLedger {
  program: string;
  status: string;
  method: string;
  attestation_chain: string;
  generated_at: string;
  finding: {
    headline: string;
    claim: string;
    maturity: string;
    reader_use: string;
  };
  headline_counts: HeadlineCounts;
  search_protocol: {
    routes: string[];
    negative_finding_rule: string;
    false_negative_risk: string;
  };
  rows: LedgerRow[];
  economy_rows: EconomyRow[];
  outputs: {
    json: string;
    csv: string;
  };
  non_claim: string;
}

const LEDGER = ledgerData as EvidenceLedger;

function formatNumber(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "pending";
  return value.toLocaleString();
}

function shortDate(value: string | null | undefined) {
  if (!value) return "pending";
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) return value.slice(0, 10);
  return date.toISOString().slice(0, 10);
}

function titleCase(value: string) {
  return value
    .split(/[-_\s]+/)
    .filter(Boolean)
    .map((part) => {
      const upper = part.toUpperCase();
      if (["QA", "PM25", "BMKG", "GHSL", "ACAG", "PPID", "PTSP", "API", "CSV", "JSON"].includes(upper)) {
        return upper === "PM25" ? "PM2.5" : upper;
      }
      return part.charAt(0).toUpperCase() + part.slice(1);
    })
    .join(" ");
}

function publicPath(path: string) {
  if (!path) return "";
  const clean = path.replace(/\\/g, "/").replace(/^air-monitoring\//, "");
  return `/programs/air-monitoring/${clean}`;
}

function strongestRows(rows: LedgerRow[]) {
  return rows
    .filter((row) => row.zero_claim_field_count > 0)
    .slice()
    .sort((a, b) => b.zero_claim_field_count - a.zero_claim_field_count || b.checked_rows - a.checked_rows)
    .slice(0, 8);
}

function groupRows(rows: LedgerRow[]) {
  const grouped = new Map<string, LedgerRow[]>();
  for (const row of rows) {
    const list = grouped.get(row.group) || [];
    list.push(row);
    grouped.set(row.group, list);
  }
  return Array.from(grouped.entries())
    .map(([group, items]) => ({
      group,
      items,
      zeroFields: items.reduce((sum, item) => sum + item.zero_claim_field_count, 0),
      checkedRows: items.reduce((sum, item) => sum + (item.checked_rows || 0), 0),
    }))
    .sort((a, b) => b.zeroFields - a.zeroFields || a.group.localeCompare(b.group));
}

function EvidenceMatrix({ counts }: { counts?: HeadlineCounts }) {
  const items = [
    {
      label: "Source discovery",
      value: counts?.economies_with_official_station_source_or_portal,
      max: counts?.economies_in_source_discovery,
      suffix: `of ${formatNumber(counts?.economies_in_source_discovery)} economies`,
      detail: "official station source or portal found",
      tone: "context",
    },
    {
      label: "Station rows audited",
      value: counts?.official_station_rows_audited,
      max: counts?.official_station_rows_audited,
      suffix: "rows",
      detail: "monitor-grade evidence audit scope",
      tone: "context",
    },
    {
      label: "Same-station validation",
      value: counts?.validated_same_station_rows,
      max: counts?.identity_candidate_rows_checked,
      suffix: `of ${formatNumber(counts?.identity_candidate_rows_checked)} candidates`,
      detail: "official/OpenAQ identity rows validated",
      tone: "blocked",
    },
    {
      label: "BMKG station QA",
      value: counts?.bmkg_station_specific_calibration_certificate_rows,
      max: counts?.bmkg_pm25_target_rows,
      suffix: `of ${formatNumber(counts?.bmkg_pm25_target_rows)} targets`,
      detail: "station-specific calibration certificates",
      tone: "blocked",
    },
    {
      label: "Monitor grade",
      value: counts?.complete_monitor_grade_rows,
      max: counts?.official_station_rows_audited,
      suffix: "complete rows",
      detail: "claim-ready grade classifications",
      tone: "blocked",
    },
    {
      label: "Coverage claim",
      value: counts?.claim_allowed_country_rows,
      max: counts?.economies_in_source_discovery,
      suffix: "allowed country rows",
      detail: counts?.coverage_claim_allowed ? "coverage claim allowed" : "coverage claim blocked",
      tone: "blocked",
    },
  ];

  return (
    <div className="air-ledger-matrix" aria-label="Evidence gate matrix">
      {items.map((item) => {
        const max = item.max && item.max > 0 ? item.max : 1;
        const value = item.value ?? 0;
        const width = value === 0 ? 2 : Math.max(6, Math.min(100, (value / max) * 100));
        return (
          <div className={`air-ledger-gate air-ledger-gate-${item.tone}`} key={item.label}>
            <div>
              <span>{item.label}</span>
              <strong>{formatNumber(item.value)}</strong>
            </div>
            <div className="air-ledger-bar" aria-hidden="true">
              <i style={{ width: `${width}%` }} />
            </div>
            <p>
              {item.suffix} · {item.detail}
            </p>
          </div>
        );
      })}
    </div>
  );
}

function FindingStats({ counts }: { counts?: HeadlineCounts }) {
  const stats = [
    ["Ledger rows", counts?.ledger_rows],
    ["Supporting files", counts?.supporting_files_indexed],
    ["Denominator rows", counts?.denominator_join_rows],
    ["Claim-ready economies", counts?.station_radius_ready_economies],
  ];

  return (
    <div className="air-ledger-stat-grid">
      {stats.map(([label, value]) => (
        <div className="air-ledger-stat" key={label as string}>
          <span>{label}</span>
          <strong>{formatNumber(value as number | undefined)}</strong>
        </div>
      ))}
    </div>
  );
}

function SourceRouteList({ routes }: { routes: string[] }) {
  return (
    <div className="air-source-route-grid">
      {routes.map((route) => (
        <span key={route}>{route}</span>
      ))}
    </div>
  );
}

function GroupSummary({ rows }: { rows: LedgerRow[] }) {
  const groups = groupRows(rows);
  return (
    <div className="air-ledger-group-grid">
      {groups.map((group) => (
        <div className="air-ledger-group" key={group.group}>
          <span>{titleCase(group.group)}</span>
          <strong>{formatNumber(group.items.length)} ledger rows</strong>
          <p>
            {formatNumber(group.checkedRows)} checked rows · {formatNumber(group.zeroFields)} zero claim fields
          </p>
        </div>
      ))}
    </div>
  );
}

function EconomyStrip({ rows }: { rows: EconomyRow[] }) {
  const visibleRows = rows
    .slice()
    .sort((a, b) => b.monitor_grade_rows_audited - a.monitor_grade_rows_audited)
    .slice(0, 12);

  return (
    <div className="air-economy-strip" aria-label="Economy evidence rows">
      {visibleRows.map((row) => (
        <div className="air-economy-row" key={row.iso3}>
          <div>
            <strong>{row.iso3}</strong>
            <span>{row.country}</span>
          </div>
          <dl>
            <div>
              <dt>grade audit</dt>
              <dd>{formatNumber(row.monitor_grade_rows_audited)}</dd>
            </div>
            <div>
              <dt>identity candidates</dt>
              <dd>{formatNumber(row.identity_candidate_rows)}</dd>
            </div>
            <div>
              <dt>validated</dt>
              <dd>{formatNumber(row.validated_same_station_rows)}</dd>
            </div>
          </dl>
        </div>
      ))}
    </div>
  );
}

function EvidenceLedgerTable({ rows }: { rows: LedgerRow[] }) {
  const [group, setGroup] = useState("all");
  const groupOptions = useMemo(
    () => ["all", ...Array.from(new Set(rows.map((row) => row.group))).sort()],
    [rows],
  );
  const filteredRows = useMemo(
    () => (group === "all" ? strongestRows(rows) : rows.filter((row) => row.group === group).slice(0, 12)),
    [group, rows],
  );

  return (
    <section className="showcase-section air-ledger-section" aria-labelledby="air-ledger-heading">
      <div className="showcase-section-copy">
        <p className="kicker kicker-crimson">Evidence ledger</p>
        <h2 id="air-ledger-heading">The audit trail is now one table, not a wall stack.</h2>
        <p>
          Each row is generated from a committed summary JSON. The public page
          shows the strongest claim-relevant rows first, then lets the reader
          switch by evidence group.
        </p>
      </div>
      <div className="air-ledger-toolbar">
        <label>
          Evidence group
          <select value={group} onChange={(event) => setGroup(event.target.value)}>
            {groupOptions.map((option) => (
              <option key={option} value={option}>
                {option === "all" ? "Highest zero-gate rows" : titleCase(option)}
              </option>
            ))}
          </select>
        </label>
        <span>{formatNumber(filteredRows.length)} rows shown</span>
      </div>
      <div className="air-ledger-table-wrap">
        <table className="air-ledger-table">
          <thead>
            <tr>
              <th>Evidence row</th>
              <th>Checked</th>
              <th>Zero fields</th>
              <th>Finding</th>
              <th>Files</th>
            </tr>
          </thead>
          <tbody>
            {filteredRows.map((row) => (
              <tr key={row.ledger_id}>
                <td>
                  <span>{titleCase(row.group)}</span>
                  <strong>{row.title}</strong>
                </td>
                <td>{formatNumber(row.checked_rows)}</td>
                <td>{formatNumber(row.zero_claim_field_count)}</td>
                <td>{row.substantive_finding}</td>
                <td>
                  <div className="air-ledger-links">
                    {row.artifact_path && <a href={publicPath(row.artifact_path)}>note</a>}
                    <a href={publicPath(row.summary_path)}>json</a>
                    {row.csv_path && <a href={publicPath(row.csv_path)}>csv</a>}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default function ShowcaseAirMonitoring() {
  const ledger = LEDGER;
  const counts = ledger.headline_counts;
  const routes = ledger.search_protocol.routes;
  const rows = ledger.rows;

  return (
    <article className="showcase-page air-ledger-page">
      <header className="showcase-hero air-ledger-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">Evidence-gap finding</p>
          <h1 className="showcase-title showcase-title-wide">
            Public monitor QA evidence is not publicly verifiable.
          </h1>
          <p className="showcase-lede">
            The strongest air-monitoring result is not a population-coverage
            claim. It is a narrower public-evidence finding: source routes,
            station lists, dashboard status, and denominator geometry are
            visible, but the station-level calibration, inspection,
            same-station, and monitor-grade gates needed for coverage claims
            remain at zero in the audited packet.
          </p>
          <div className="showcase-meta">
            <span>{ledger.attestation_chain}</span>
            <span>{ledger.finding.maturity}</span>
            <span>No station-radius coverage claim</span>
          </div>
        </div>
        <div className="showcase-hero-panel air-ledger-panel" aria-label="Air-monitoring QA evidence summary">
          <EvidenceMatrix counts={counts} />
          <FindingStats counts={counts} />
        </div>
      </header>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Finding</p>
          <h2>It is an observability result, not a monitor map.</h2>
          <p>{ledger.finding.claim}</p>
        </div>
        <div className="air-ledger-finding">
          <span>Claim permission</span>
          <strong>{counts?.coverage_claim_allowed ? "Coverage claim allowed" : "Coverage claim blocked"}</strong>
          <p>
            {formatNumber(counts?.claim_allowed_country_rows)} allowed country
            rows after {formatNumber(counts?.denominator_join_rows)} denominator
            join rows and {formatNumber(counts?.identity_candidate_rows_checked)}
            identity candidates.
          </p>
        </div>
      </section>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">How we know</p>
          <h2>The ledger separates context from claim-enabling evidence.</h2>
          <p>
            The generated packet indexes {formatNumber(counts.supporting_files_indexed)} supporting
            files into {formatNumber(counts.ledger_rows)} ledger rows. It
            keeps positive source context visible while showing which gates
            do not close.
          </p>
        </div>
        <GroupSummary rows={rows} />
      </section>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Search protocol</p>
          <h2>A zero counts only when the searched route is named.</h2>
          <p>{ledger.search_protocol.negative_finding_rule}</p>
        </div>
        <SourceRouteList routes={routes} />
      </section>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker">Economy rows</p>
          <h2>Station evidence appears, but validated same-station joins do not.</h2>
          <p>
            The economy strip shows the highest monitor-grade audit scopes.
            The repeated zero is the validated identity column, not the
            existence of stations or station context.
          </p>
        </div>
        <EconomyStrip rows={ledger.economy_rows} />
      </section>

      <EvidenceLedgerTable rows={rows} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Limits</p>
          <h2>Absence in public routes is not absence in the world.</h2>
          <p>{ledger.search_protocol.false_negative_risk}</p>
        </div>
        <div className="showcase-note">
          <p>
            <strong>Non-claim.</strong> {ledger.non_claim}
          </p>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={6} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Reproduce</p>
          <h2>The page is generated from the committed ledger, not hand-entered counts.</h2>
          <p>
            Rerun the ledger builder, then let the reporting-site prebuild sync
            copy the generated JSON and CSV into the public evidence directory.
          </p>
          <pre className="air-ledger-command">
            <code>python air-monitoring\scripts\build-evidence-ledger.py</code>
          </pre>
        </div>
        <div className="showcase-links">
          <a href="/programs/air-monitoring/results.md">Results note</a>
          <a href="/programs/air-monitoring/sensitivity.md">Sensitivity note</a>
          <a href={LEDGER_URL}>Evidence ledger JSON</a>
          <a href="/programs/air-monitoring/generated/air-monitoring-evidence-ledger.csv">Evidence ledger CSV</a>
          <Link href="/program/air-monitoring/evidence">Program evidence archive</Link>
        </div>
      </section>
    </article>
  );
}
