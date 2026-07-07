"use client";

import { useMemo, useState } from "react";

export type EvidenceLedgerMetricKey = "source_inputs_count" | "zero_claim_field_count";

export interface EvidenceLedgerRow {
  ledger_id: string;
  group: string;
  title: string;
  status?: string;
  goal_level?: string;
  method?: string;
  attestation_chain?: string;
  generated_at?: string;
  checked_rows?: number | null;
  source_inputs_count?: number | null;
  zero_claim_fields?: string[];
  zero_claim_field_count?: number | null;
  substantive_finding: string;
  reader_use?: string;
  artifact_path?: string;
  summary_path?: string;
  csv_path?: string;
  non_claim?: string;
}

interface EvidenceLedgerGroupSummaryProps {
  rows: EvidenceLedgerRow[];
  checkedLabel?: string;
  metricKey?: EvidenceLedgerMetricKey;
  metricLabel?: string;
  rowNoun?: string;
  showLatest?: boolean;
}

interface EvidenceLedgerTableProps {
  rows: EvidenceLedgerRow[];
  programSlug: string;
  headingId: string;
  title: string;
  description: string;
  metricKey: EvidenceLedgerMetricKey;
  metricLabel: string;
  allOptionLabel: string;
  allMode?: "all" | "highest-metric";
  allRowLimit?: number;
  groupRowLimit?: number;
  includeReaderUse?: boolean;
}

export function formatLedgerNumber(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "pending";
  return value.toLocaleString();
}

export function formatLedgerPercent(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "pending";
  return `${(value * 100).toFixed(1)}%`;
}

export function formatLedgerDate(value: string | null | undefined) {
  if (!value) return "pending";
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) return value.slice(0, 10);
  return date.toISOString().slice(0, 10);
}

export function titleCaseLedgerText(value: string) {
  return value
    .split(/[-_\s/]+/)
    .filter(Boolean)
    .map((part) => {
      const upper = part.toUpperCase();
      if (
        [
          "ACAG",
          "AI",
          "API",
          "BMKG",
          "CSV",
          "DGHS",
          "GHSL",
          "JSON",
          "L3",
          "OSM",
          "PM25",
          "PPID",
          "PSDQ",
          "PTSP",
          "QA",
        ].includes(upper)
      ) {
        return upper === "PM25" ? "PM2.5" : upper;
      }
      return part.charAt(0).toUpperCase() + part.slice(1);
    })
    .join(" ");
}

function metricValue(row: EvidenceLedgerRow, key: EvidenceLedgerMetricKey) {
  const value = row[key];
  return typeof value === "number" && Number.isFinite(value) ? value : 0;
}

function ledgerPublicPath(programSlug: string, path: string | null | undefined) {
  if (!path) return "";
  if (path.startsWith("/") || /^https?:\/\//.test(path)) return path;
  const clean = path
    .replace(/\\/g, "/")
    .replace(new RegExp(`^${programSlug.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}/`), "");
  return `/programs/${programSlug}/${clean}`;
}

function groupLedgerRows(rows: EvidenceLedgerRow[], metricKey?: EvidenceLedgerMetricKey) {
  const grouped = new Map<string, EvidenceLedgerRow[]>();
  for (const row of rows) {
    const list = grouped.get(row.group) || [];
    list.push(row);
    grouped.set(row.group, list);
  }
  return Array.from(grouped.entries())
    .map(([group, items]) => ({
      group,
      items,
      checkedRows: items.reduce((sum, item) => sum + (item.checked_rows || 0), 0),
      metricTotal: metricKey ? items.reduce((sum, item) => sum + metricValue(item, metricKey), 0) : 0,
      latest: items
        .map((item) => item.generated_at)
        .filter(Boolean)
        .sort()
        .at(-1),
    }))
    .sort((a, b) => {
      if (metricKey && b.metricTotal !== a.metricTotal) return b.metricTotal - a.metricTotal;
      return b.items.length - a.items.length || a.group.localeCompare(b.group);
    });
}

function strongestRows(rows: EvidenceLedgerRow[], metricKey: EvidenceLedgerMetricKey, limit?: number) {
  const sorted = rows
    .slice()
    .sort(
      (a, b) =>
        metricValue(b, metricKey) - metricValue(a, metricKey) ||
        (b.checked_rows || 0) - (a.checked_rows || 0) ||
        a.title.localeCompare(b.title),
    );
  return typeof limit === "number" ? sorted.slice(0, limit) : sorted;
}

export function EvidenceLedgerGroupSummary({
  rows,
  checkedLabel = "checked rows",
  metricKey,
  metricLabel,
  rowNoun = "rows",
  showLatest = false,
}: EvidenceLedgerGroupSummaryProps) {
  const groups = useMemo(() => groupLedgerRows(rows, metricKey), [metricKey, rows]);

  return (
    <div className="air-ledger-group-grid">
      {groups.map((group) => (
        <div className="air-ledger-group" key={group.group}>
          <span>{titleCaseLedgerText(group.group)}</span>
          <strong>
            {formatLedgerNumber(group.items.length)} {rowNoun}
          </strong>
          <p>
            {formatLedgerNumber(group.checkedRows)} {checkedLabel}
            {metricKey && metricLabel ? ` · ${formatLedgerNumber(group.metricTotal)} ${metricLabel}` : ""}
            {showLatest && group.latest ? `; latest ${formatLedgerDate(group.latest)}` : ""}
          </p>
        </div>
      ))}
    </div>
  );
}

export function EvidenceLedgerTable({
  rows,
  programSlug,
  headingId,
  title,
  description,
  metricKey,
  metricLabel,
  allOptionLabel,
  allMode = "all",
  allRowLimit,
  groupRowLimit,
  includeReaderUse = false,
}: EvidenceLedgerTableProps) {
  const [group, setGroup] = useState("all");
  const groupOptions = useMemo(
    () => ["all", ...Array.from(new Set(rows.map((row) => row.group))).sort()],
    [rows],
  );
  const filteredRows = useMemo(() => {
    if (group !== "all") {
      const groupRows = rows.filter((row) => row.group === group);
      return typeof groupRowLimit === "number" ? groupRows.slice(0, groupRowLimit) : groupRows;
    }
    if (allMode === "highest-metric") return strongestRows(rows, metricKey, allRowLimit);
    return typeof allRowLimit === "number" ? rows.slice(0, allRowLimit) : rows;
  }, [allMode, allRowLimit, group, groupRowLimit, metricKey, rows]);

  return (
    <section className="showcase-section air-ledger-section" aria-labelledby={headingId}>
      <div className="showcase-section-copy">
        <p className="kicker kicker-crimson">Evidence ledger</p>
        <h2 id={headingId}>{title}</h2>
        <p>{description}</p>
      </div>
      <div className="air-ledger-toolbar">
        <label>
          Evidence group
          <select value={group} onChange={(event) => setGroup(event.target.value)}>
            {groupOptions.map((option) => (
              <option key={option} value={option}>
                {option === "all" ? allOptionLabel : titleCaseLedgerText(option)}
              </option>
            ))}
          </select>
        </label>
        <span>{formatLedgerNumber(filteredRows.length)} rows shown</span>
      </div>
      <div className="air-ledger-table-wrap">
        <table className="air-ledger-table">
          <thead>
            <tr>
              <th>Evidence row</th>
              <th>Checked</th>
              <th>{metricLabel}</th>
              <th>Finding</th>
              <th>Files</th>
            </tr>
          </thead>
          <tbody>
            {filteredRows.map((row) => (
              <tr key={row.ledger_id}>
                <td data-label="Evidence row">
                  <span>{titleCaseLedgerText(row.group)}</span>
                  <strong>{row.title}</strong>
                </td>
                <td data-label="Checked">{formatLedgerNumber(row.checked_rows)}</td>
                <td data-label={metricLabel}>{formatLedgerNumber(metricValue(row, metricKey))}</td>
                <td data-label="Finding">
                  {row.substantive_finding}
                  {includeReaderUse && row.reader_use ? <strong>{row.reader_use}</strong> : null}
                </td>
                <td data-label="Files">
                  <div className="air-ledger-links">
                    {row.artifact_path ? <a href={ledgerPublicPath(programSlug, row.artifact_path)}>note</a> : null}
                    {row.summary_path ? <a href={ledgerPublicPath(programSlug, row.summary_path)}>json</a> : null}
                    {row.csv_path ? <a href={ledgerPublicPath(programSlug, row.csv_path)}>csv</a> : null}
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
