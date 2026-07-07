"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";
import ledgerData from "../../public/programs/public-service-data-quality/generated/psdq-evidence-ledger.json";

const LEDGER_URL = "/programs/public-service-data-quality/generated/psdq-evidence-ledger.json";
const LEDGER_CSV_URL = "/programs/public-service-data-quality/generated/psdq-evidence-ledger.csv";

interface HeadlineCounts {
  ledger_rows: number;
  supporting_summary_files_indexed: number;
  registry_admin_rows: number;
  rows_with_open_buildings_denominator: number;
  active_clinical_facilities: number;
  osm_health_joined: number;
  registry_minus_osm_clinical: number;
  rows_with_zero_osm_health_features: number;
  share_with_zero_osm_health_features: number;
  rows_where_osm_equals_or_exceeds_registry: number;
  sampled_upazilas: number;
  sampled_facility_rows: number;
  coordinate_ready_facility_rows: number;
  evidence_ladder_stages: number;
  targeted_public_source_rows: number;
  human_gated_handoff_rows: number;
  human_or_source_owner_wall_rows: number;
  ai_actionable_without_human_or_source_owner_rows: number;
  keep_open_only_rows: number;
  external_contacts_made: number;
  rows_allowed_for_closure: number;
  rows_allowed_for_same_facility_reclassification: number;
  rows_allowed_for_map_absence_language: number;
  coordinate_corrections_allowed: number;
}

interface ReaderFirstTest {
  remember: string;
  hero_visual: string;
  cautions: string[];
  audit_route: string;
}

interface DataVisualContract {
  source: string;
  transform: string;
  claim_role: string;
  mobile_proof: string;
  fallback: string;
}

interface LedgerRow {
  ledger_id: string;
  group: string;
  title: string;
  status: string;
  goal_level: string;
  method: string;
  attestation_chain: string;
  generated_at: string;
  checked_rows: number;
  source_inputs_count: number;
  substantive_finding: string;
  reader_use: string;
  artifact_path: string;
  summary_path: string;
  csv_path: string;
  non_claim: string;
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
  reader_first_test: ReaderFirstTest;
  data_to_visual_contract: DataVisualContract;
  rows: LedgerRow[];
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

function formatPercent(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "pending";
  return `${(value * 100).toFixed(1)}%`;
}

function shortDate(value: string | null | undefined) {
  if (!value) return "pending";
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) return value.slice(0, 10);
  return date.toISOString().slice(0, 10);
}

function titleCase(value: string) {
  return value
    .split(/[-_\s/]+/)
    .filter(Boolean)
    .map((part) => {
      const upper = part.toUpperCase();
      if (["AI", "API", "CSV", "DGHS", "JSON", "L3", "OSM", "PSDQ", "QA"].includes(upper)) return upper;
      return part.charAt(0).toUpperCase() + part.slice(1);
    })
    .join(" ");
}

function publicPath(path: string) {
  if (!path) return "";
  const clean = path.replace(/\\/g, "/").replace(/^public-service-data-quality\//, "");
  return `/programs/public-service-data-quality/${clean}`;
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
      checkedRows: items.reduce((sum, item) => sum + (item.checked_rows || 0), 0),
      latest: items
        .map((item) => item.generated_at)
        .filter(Boolean)
        .sort()
        .at(-1),
    }))
    .sort((a, b) => b.items.length - a.items.length || a.group.localeCompare(b.group));
}

function EvidenceMatrix({ counts }: { counts: HeadlineCounts }) {
  const items = [
    {
      label: "Registry scope",
      value: counts.registry_admin_rows,
      max: counts.registry_admin_rows,
      suffix: "DGHS upazila rows",
      detail: `${formatNumber(counts.active_clinical_facilities)} active clinical facilities`,
      tone: "context",
    },
    {
      label: "Joined public map",
      value: counts.osm_health_joined,
      max: counts.active_clinical_facilities,
      suffix: "joined OSM health features",
      detail: `${formatNumber(counts.registry_minus_osm_clinical)} registry-minus-OSM clinical gap`,
      tone: "context",
    },
    {
      label: "Zero-OSM rows",
      value: counts.rows_with_zero_osm_health_features,
      max: counts.registry_admin_rows,
      suffix: `${formatPercent(counts.share_with_zero_osm_health_features)} of registry rows`,
      detail: "active registry facilities, no joined OSM health feature",
      tone: "blocked",
    },
    {
      label: "Validation sample",
      value: counts.sampled_facility_rows,
      max: counts.sampled_facility_rows,
      suffix: `${formatNumber(counts.sampled_upazilas)} sampled upazilas`,
      detail: `${formatNumber(counts.coordinate_ready_facility_rows)} coordinate-ready rows`,
      tone: "context",
    },
    {
      label: "Human/source-owner wall",
      value: counts.human_or_source_owner_wall_rows,
      max: counts.human_gated_handoff_rows,
      suffix: `of ${formatNumber(counts.human_gated_handoff_rows)} handoff rows`,
      detail: "requires source-owner or human-location evidence",
      tone: "blocked",
    },
    {
      label: "AI-actionable closure",
      value: counts.ai_actionable_without_human_or_source_owner_rows,
      max: counts.human_or_source_owner_wall_rows,
      suffix: "rows",
      detail: "closure, reclassification, map absence, and coordinate correction all remain blocked",
      tone: "blocked",
    },
  ];

  return (
    <div className="air-ledger-matrix" aria-label="PSDQ evidence-gate matrix">
      {items.map((item) => {
        const max = item.max && item.max > 0 ? item.max : 1;
        const width = item.value === 0 ? 2 : Math.max(6, Math.min(100, (item.value / max) * 100));
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

function FindingStats({ counts }: { counts: HeadlineCounts }) {
  const stats = [
    ["Ledger rows", counts.ledger_rows],
    ["Summary files", counts.supporting_summary_files_indexed],
    ["Evidence stages", counts.evidence_ladder_stages],
    ["External contacts", counts.external_contacts_made],
  ];

  return (
    <div className="air-ledger-stat-grid">
      {stats.map(([label, value]) => (
        <div className="air-ledger-stat" key={label as string}>
          <span>{label}</span>
          <strong>{formatNumber(value as number)}</strong>
        </div>
      ))}
    </div>
  );
}

function EvidencePath({ counts }: { counts: HeadlineCounts }) {
  const steps = [
    {
      title: "Source disagreement",
      value: counts.registry_admin_rows,
      detail: "DGHS registry rows joined to OSM and Open Buildings context",
    },
    {
      title: "Facility sample",
      value: counts.sampled_facility_rows,
      detail: "sampled facility rows, not validation outcomes",
    },
    {
      title: "Public-source review",
      value: counts.targeted_public_source_rows,
      detail: "targeted rows with DGHS profile and OSM API retrieval",
    },
    {
      title: "Handoff wall",
      value: counts.human_or_source_owner_wall_rows,
      detail: "rows requiring source-owner or human-location evidence",
    },
    {
      title: "AI closure",
      value: counts.ai_actionable_without_human_or_source_owner_rows,
      detail: "rows actionable without human or source-owner evidence",
    },
  ];

  return (
    <div className="psdq-evidence-path" aria-label="PSDQ evidence path">
      {steps.map((step, index) => (
        <article key={step.title}>
          <span>{String(index + 1).padStart(2, "0")}</span>
          <strong>{formatNumber(step.value)}</strong>
          <h3>{step.title}</h3>
          <p>{step.detail}</p>
        </article>
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
          <strong>{formatNumber(group.items.length)} rows</strong>
          <p>
            {formatNumber(group.checkedRows)} checked or indexed rows
            {group.latest ? `; latest ${shortDate(group.latest)}` : ""}
          </p>
        </div>
      ))}
    </div>
  );
}

function Limits({ cautions }: { cautions: string[] }) {
  return (
    <div className="psdq-limit-grid">
      {cautions.map((caution) => (
        <div key={caution}>
          <span>Caution</span>
          <p>{caution}</p>
        </div>
      ))}
    </div>
  );
}

function DataContract({ contract }: { contract: DataVisualContract }) {
  const rows = [
    ["Source", contract.source],
    ["Transform", contract.transform],
    ["Claim role", contract.claim_role],
    ["Mobile proof", contract.mobile_proof],
    ["Fallback", contract.fallback],
  ];
  return (
    <dl className="psdq-contract-list">
      {rows.map(([label, value]) => (
        <div key={label}>
          <dt>{label}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}

function EvidenceLedgerTable({ rows }: { rows: LedgerRow[] }) {
  const [group, setGroup] = useState("all");
  const groupOptions = useMemo(
    () => ["all", ...Array.from(new Set(rows.map((row) => row.group))).sort()],
    [rows],
  );
  const filteredRows = useMemo(
    () => (group === "all" ? rows : rows.filter((row) => row.group === group)),
    [group, rows],
  );

  return (
    <section className="showcase-section air-ledger-section" aria-labelledby="psdq-ledger-heading">
      <div className="showcase-section-copy">
        <p className="kicker kicker-crimson">Evidence ledger</p>
        <h2 id="psdq-ledger-heading">The audit trail is one generated table.</h2>
        <p>
          The old page stacked every wall and scan as its own section. This
          table is generated from committed summaries and keeps the substantive
          finding, reader use, and download links in one place.
        </p>
      </div>
      <div className="air-ledger-toolbar">
        <label>
          Evidence group
          <select value={group} onChange={(event) => setGroup(event.target.value)}>
            {groupOptions.map((option) => (
              <option key={option} value={option}>
                {option === "all" ? "All evidence rows" : titleCase(option)}
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
              <th>Sources</th>
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
                <td>{formatNumber(row.source_inputs_count)}</td>
                <td>
                  {row.substantive_finding}
                  <strong>{row.reader_use}</strong>
                </td>
                <td>
                  <div className="air-ledger-links">
                    {row.artifact_path && <a href={publicPath(row.artifact_path)}>note</a>}
                    {row.summary_path && <a href={publicPath(row.summary_path)}>json</a>}
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

export default function ShowcasePSDQ() {
  const ledger = LEDGER;
  const counts = ledger.headline_counts;

  return (
    <article className="showcase-page air-ledger-page psdq-ledger-page">
      <header className="showcase-hero air-ledger-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">Source-disagreement finding</p>
          <h1 className="showcase-title showcase-title-wide">
            Registry-map disagreement is visible; row repair is human-gated.
          </h1>
          <p className="showcase-lede">{ledger.finding.claim}</p>
          <div className="showcase-meta">
            <span>{ledger.attestation_chain}</span>
            <span>{ledger.finding.maturity}</span>
            <span>No access or ground-truth claim</span>
          </div>
        </div>
        <div className="showcase-hero-panel air-ledger-panel" aria-label="PSDQ evidence summary">
          <EvidenceMatrix counts={counts} />
          <FindingStats counts={counts} />
        </div>
      </header>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Finding</p>
          <h2>A strong source-quality signal, not a facility truth label.</h2>
          <p>{ledger.finding.reader_use}</p>
        </div>
        <div className="air-ledger-finding">
          <span>Claim permission</span>
          <strong>Keep-open only</strong>
          <p>
            {formatNumber(counts.keep_open_only_rows)} rows remain keep-open
            only; {formatNumber(counts.rows_allowed_for_closure)} closure rows,
            {formatNumber(counts.rows_allowed_for_same_facility_reclassification)}
            {" "}same-facility reclassifications, and{" "}
            {formatNumber(counts.coordinate_corrections_allowed)} coordinate
            corrections are allowed by current public evidence.
          </p>
        </div>
      </section>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">Hero visual</p>
          <h2>The evidence path ends at a wall, and that is the result.</h2>
          <p>
            The path begins with registry-map disagreement and ends with a
            no-contact closure audit. The key result is the last number:
            current public evidence leaves {formatNumber(counts.ai_actionable_without_human_or_source_owner_rows)}
            {" "}rows actionable without human or source-owner evidence.
          </p>
        </div>
        <EvidencePath counts={counts} />
      </section>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">How we know</p>
          <h2>Twenty-eight summary artifacts now read as one packet.</h2>
          <p>
            The generated ledger indexes {formatNumber(counts.supporting_summary_files_indexed)}
            {" "}committed summary files into {formatNumber(counts.ledger_rows)}
            {" "}rows. The groups below show where the evidence supports
            source-disagreement language and where it blocks stronger row-level
            conclusions.
          </p>
        </div>
        <GroupSummary rows={ledger.rows} />
      </section>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Limits first</p>
          <h2>The caveats appear before the ledger.</h2>
          <p>{ledger.reader_first_test.remember}</p>
        </div>
        <Limits cautions={ledger.reader_first_test.cautions} />
      </section>

      <EvidenceLedgerTable rows={ledger.rows} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker">Data-to-visual contract</p>
          <h2>The page renders the generated ledger, not hand-entered counts.</h2>
          <p>
            The public surface uses one source file and keeps the fallback
            evidence table visible for readers who want to audit the claim.
          </p>
        </div>
        <DataContract contract={ledger.data_to_visual_contract} />
      </section>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Non-claim</p>
          <h2>This does not decide which source is correct.</h2>
          <p>{ledger.non_claim}</p>
        </div>
        <div className="showcase-note">
          <p>
            The operational use is source improvement and validation targeting:
            which rows need source-owner clarification, human location review,
            or a better public correction record before the research can move
            from observability to row-level repair.
          </p>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={4} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Reproduce</p>
          <h2>Rebuild the ledger from committed public-data summaries.</h2>
          <p>
            Rerun the PSDQ ledger builder, then let the reporting-site prebuild
            sync copy the generated JSON and CSV into the public evidence
            directory.
          </p>
          <pre className="air-ledger-command">
            <code>python public-service-data-quality/scripts/build-evidence-ledger.py</code>
          </pre>
        </div>
        <div className="showcase-links">
          <a href="/programs/public-service-data-quality/source-disagreement-l3-module.md">
            L3 evidence note
          </a>
          <a href="/programs/public-service-data-quality/facility-validation-evidence-ladder.md">
            Evidence ladder note
          </a>
          <a href={LEDGER_URL}>Evidence ledger JSON</a>
          <a href={LEDGER_CSV_URL}>Evidence ledger CSV</a>
          <Link href="/public-service-data-quality?view=evidence">Program evidence packet</Link>
        </div>
      </section>
    </article>
  );
}
