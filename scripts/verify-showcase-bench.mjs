#!/usr/bin/env node
// scripts/verify-showcase-bench.mjs
// Verifies the 20-report showcase registry against committed evidence paths,
// public audit artifacts, route coverage, and quality/depth records.

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const ROOT = process.cwd();
const REGISTRY = path.join(ROOT, "reporting-site", "src", "data", "showcaseReports.ts");
const ROUTES = path.join(ROOT, "reporting-site", "src", "main.tsx");
const QA_DIR = path.join(ROOT, "reporting-site", "qa");
const OUT_JSON = path.join(ROOT, "research", "generated", "showcase-bench-evidence-audit.json");
const OUT_MD = path.join(ROOT, "research", "showcase-bench-evidence-audit.md");

function failConfig(message) {
  console.error(`CONFIG - ${message}`);
  process.exit(2);
}

function read(file) {
  if (!fs.existsSync(file)) failConfig(`missing ${path.relative(ROOT, file)}`);
  return fs.readFileSync(file, "utf8");
}

function extractBalanced(source, marker, openChar, closeChar) {
  const markerIndex = source.indexOf(marker);
  if (markerIndex < 0) failConfig(`marker not found: ${marker}`);
  const assignmentIndex = source.indexOf("=", markerIndex);
  if (assignmentIndex < 0) failConfig(`assignment not found after ${marker}`);
  const start = source.indexOf(openChar, assignmentIndex);
  if (start < 0) failConfig(`opening ${openChar} not found after ${marker}`);

  let depth = 0;
  let quote = null;
  let escaped = false;
  let lineComment = false;
  let blockComment = false;

  for (let i = start; i < source.length; i++) {
    const ch = source[i];
    const next = source[i + 1];

    if (lineComment) {
      if (ch === "\n") lineComment = false;
      continue;
    }
    if (blockComment) {
      if (ch === "*" && next === "/") {
        blockComment = false;
        i++;
      }
      continue;
    }
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === quote) {
        quote = null;
      }
      continue;
    }
    if (ch === "/" && next === "/") {
      lineComment = true;
      i++;
      continue;
    }
    if (ch === "/" && next === "*") {
      blockComment = true;
      i++;
      continue;
    }
    if (ch === "\"" || ch === "'" || ch === "`") {
      quote = ch;
      continue;
    }
    if (ch === openChar) depth++;
    if (ch === closeChar) {
      depth--;
      if (depth === 0) return source.slice(start, i + 1);
    }
  }
  failConfig(`could not find closing ${closeChar} for ${marker}`);
}

function parseLiteral(source, marker, openChar, closeChar) {
  const literal = extractBalanced(source, marker, openChar, closeChar);
  return vm.runInNewContext(`(${literal})`, Object.create(null), { timeout: 1000 });
}

function rel(file) {
  return path.relative(ROOT, file).replace(/\\/g, "/");
}

function existsRel(relativePath) {
  return fs.existsSync(path.join(ROOT, relativePath));
}

function publicPathFromUrl(url) {
  if (!url || !url.startsWith("/")) return null;
  return path.join(ROOT, "reporting-site", "public", ...url.slice(1).split("/"));
}

function countBy(rows, keyFn) {
  const out = {};
  for (const row of rows) {
    const key = keyFn(row) || "missing";
    out[key] = (out[key] || 0) + 1;
  }
  return out;
}

function compact(text, max = 130) {
  const normalized = String(text || "").replace(/\s+/g, " ").trim();
  return normalized.length > max ? `${normalized.slice(0, max - 3)}...` : normalized;
}

function mdCell(value) {
  return String(value ?? "").replace(/\|/g, "\\|").replace(/\r?\n/g, " ");
}

function routeSet() {
  const routeSource = read(ROUTES);
  return new Set(Array.from(routeSource.matchAll(/<Route\s+path="([^"]+)"/g)).map((m) => m[1]));
}

function qaInventory() {
  if (!fs.existsSync(QA_DIR)) return { screenshots: 0, browserChecks: 0 };
  const files = fs.readdirSync(QA_DIR);
  return {
    screenshots: files.filter((name) => /\.(png|jpe?g|webp)$/i.test(name)).length,
    browserChecks: files.filter((name) => /browser-check\.json$/i.test(name)).length,
  };
}

function writeOutputs(audit) {
  fs.mkdirSync(path.dirname(OUT_JSON), { recursive: true });
  fs.writeFileSync(OUT_JSON, `${JSON.stringify(audit, null, 2)}\n`);

  const rows = audit.reports
    .map((row) => [
      row.id,
      row.shortTitle,
      row.readinessLabel,
      row.routeCovered ? "ok" : "missing",
      row.evidenceExists ? "ok" : "missing",
      row.auditDataExists === null ? "n/a" : row.auditDataExists ? "ok" : "missing",
      compact(row.nextUpgrade),
    ]);

  const md = [
    "# Showcase bench evidence audit",
    "",
    "`attestation_chain: ai-first`",
    "",
    `Generated: ${audit.generated_at}`,
    "",
    `Script: \`${audit.script}\``,
    "",
    `Registry: \`${audit.registry}\``,
    "",
    "## Summary",
    "",
    `- Reports in registry: ${audit.summary.reports_total}`,
    `- Verified status rows: ${audit.summary.verified_reports}/${audit.summary.reports_total}`,
    `- Evidence paths present: ${audit.summary.evidence_paths_present}/${audit.summary.reports_total}`,
    `- Static route coverage: ${audit.summary.routes_covered}/${audit.summary.reports_total}`,
    `- Audit JSON artifacts present: ${audit.summary.audit_data_present}/${audit.summary.audit_reports}`,
    `- Declared audit CSV companions present: ${audit.summary.audit_csv_present}/${audit.summary.audit_csv_declared}`,
    `- Depth records present: ${audit.summary.depth_records_present}/${audit.summary.reports_total}`,
    `- Quality records present: ${audit.summary.quality_records_present}/${audit.summary.reports_total}`,
    `- QA screenshot files in reporting-site/qa: ${audit.qa_inventory.screenshots}`,
    `- QA browser-check JSON files in reporting-site/qa: ${audit.qa_inventory.browserChecks}`,
    `- Verification failures: ${audit.failures.length}`,
    "",
    "## Readiness Mix",
    "",
    ...Object.entries(audit.summary.readiness_counts).map(([key, value]) => `- ${key}: ${value}`),
    "",
    "## Report-Level Checks",
    "",
    "| ID | Report | Readiness | Route | Evidence | Audit data | Next upgrade |",
    "|---:|---|---|---|---|---|---|",
    ...rows.map((row) => `| ${row.map(mdCell).join(" | ")} |`),
    "",
    "## Failure List",
    "",
    ...(audit.failures.length ? audit.failures.map((item) => `- ${item}`) : ["- None."]),
    "",
  ].join("\n");
  fs.writeFileSync(OUT_MD, md);
}

function main() {
  const source = read(REGISTRY);
  const routes = routeSet();
  const hasSharedAuditRoute = routes.has("/showcase/:reportSlug");
  const reports = parseLiteral(source, "export const showcaseReports", "[", "]");
  const depth = parseLiteral(source, "export const showcaseReportDepth", "{", "}");
  const quality = parseLiteral(source, "export const showcaseReportQuality", "{", "}");

  const failures = [];
  const seenIds = new Set();
  const seenHrefs = new Set();

  const reportRows = reports.map((report) => {
    const id = Number(report.id);
    const q = quality[String(id)];
    const d = depth[String(id)];
    const evidenceExists = Boolean(report.evidencePath && existsRel(report.evidencePath));
    const auditDataPath = report.audit?.dataUrl ? publicPathFromUrl(report.audit.dataUrl) : null;
    const auditCsvPath = report.audit?.csvUrl ? publicPathFromUrl(report.audit.csvUrl) : null;
    const routeCovered =
      routes.has(report.href) ||
      Boolean(report.audit && hasSharedAuditRoute && String(report.href).startsWith("/showcase/"));

    if (!Number.isInteger(id)) failures.push(`Report has non-integer id: ${report.title}`);
    if (seenIds.has(id)) failures.push(`Duplicate report id: ${id}`);
    seenIds.add(id);
    if (seenHrefs.has(report.href)) failures.push(`Duplicate report href: ${report.href}`);
    seenHrefs.add(report.href);
    for (const field of ["title", "shortTitle", "href", "status", "statusLabel", "deck", "evidencePath", "visual", "sourceNote"]) {
      if (!String(report[field] || "").trim()) failures.push(`Report ${id} missing ${field}`);
    }
    if (!evidenceExists) failures.push(`Report ${id} evidence path missing: ${report.evidencePath}`);
    if (!routeCovered) failures.push(`Report ${id} route not covered: ${report.href}`);
    if (!q) failures.push(`Report ${id} missing quality record`);
    if (!d) failures.push(`Report ${id} missing depth record`);
    if (report.audit?.dataUrl && !fs.existsSync(auditDataPath)) failures.push(`Report ${id} audit data missing: ${report.audit.dataUrl}`);
    if (report.audit?.csvUrl && !fs.existsSync(auditCsvPath)) failures.push(`Report ${id} audit CSV missing: ${report.audit.csvUrl}`);

    return {
      id,
      title: report.title,
      shortTitle: report.shortTitle,
      href: report.href,
      status: report.status,
      statusLabel: report.statusLabel,
      readiness: q?.readiness || null,
      readinessLabel: q?.readinessLabel || null,
      evidencePath: report.evidencePath,
      evidenceExists,
      routeCovered,
      routeKind: routes.has(report.href) ? "explicit" : report.audit ? "shared-audit" : "missing",
      auditDataUrl: report.audit?.dataUrl || null,
      auditDataExists: report.audit?.dataUrl ? fs.existsSync(auditDataPath) : null,
      auditCsvUrl: report.audit?.csvUrl || null,
      auditCsvExists: report.audit?.csvUrl ? fs.existsSync(auditCsvPath) : null,
      depthRecordExists: Boolean(d),
      qualityRecordExists: Boolean(q),
      sourceNotePresent: Boolean(String(report.sourceNote || "").trim()),
      visualPresent: Boolean(String(report.visual || "").trim()),
      nextUpgrade: q?.nextUpgrade || null,
    };
  });

  const sequentialIds = Array.from({ length: reports.length }, (_, i) => i + 1);
  for (const expected of sequentialIds) {
    if (!seenIds.has(expected)) failures.push(`Missing report id in sequence: ${expected}`);
  }

  const auditReports = reportRows.filter((row) => row.auditDataUrl);
  const auditCsvRows = reportRows.filter((row) => row.auditCsvUrl);
  const audit = {
    attestation_chain: "ai-first",
    generated_at: new Date().toISOString(),
    script: "scripts/verify-showcase-bench.mjs",
    registry: rel(REGISTRY),
    routes_file: rel(ROUTES),
    qa_inventory: qaInventory(),
    summary: {
      reports_total: reportRows.length,
      verified_reports: reportRows.filter((row) => row.status === "verified").length,
      audit_reports: auditReports.length,
      audit_csv_declared: auditCsvRows.length,
      evidence_paths_present: reportRows.filter((row) => row.evidenceExists).length,
      routes_covered: reportRows.filter((row) => row.routeCovered).length,
      audit_data_present: auditReports.filter((row) => row.auditDataExists).length,
      audit_csv_present: auditCsvRows.filter((row) => row.auditCsvExists).length,
      depth_records_present: reportRows.filter((row) => row.depthRecordExists).length,
      quality_records_present: reportRows.filter((row) => row.qualityRecordExists).length,
      readiness_counts: countBy(reportRows, (row) => row.readiness),
    },
    reports: reportRows,
    failures,
  };

  writeOutputs(audit);

  if (failures.length) {
    console.error(`FAIL - ${failures.length} showcase-bench verification issue(s).`);
    for (const failure of failures) console.error(`- ${failure}`);
    process.exit(1);
  }
  console.log(
    `OK - ${audit.summary.reports_total} showcase reports verified; ` +
    `${audit.summary.evidence_paths_present}/${audit.summary.reports_total} evidence paths, ` +
    `${audit.summary.audit_data_present}/${audit.summary.audit_reports} audit JSON artifacts.`,
  );
}

main();
