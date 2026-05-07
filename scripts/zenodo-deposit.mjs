#!/usr/bin/env node
// scripts/zenodo-deposit.mjs
// Mints a Zenodo DOI per CONSTITUTION.md §10.3, executed under §18.1 as
// owner's delegate (the token is in .env.local, bound to the owner's
// Zenodo account).
//
// Four modes, each gated behind its own flag:
//   --dry-run            POST metadata to a draft, print id + reserved DOI
//   --upload <file>      add a file to an existing draft
//   --publish            publish an existing draft (PERMANENT)
//   --discard            DELETE an existing draft (only if unsubmitted)
//
// After each step the script records state in
//   research/zenodo/<program>.deposition.json
//
// Usage:
//   node scripts/zenodo-deposit.mjs --program public-service-data-quality --dry-run
//   node scripts/zenodo-deposit.mjs --program public-service-data-quality --upload review-packets/public-service-data-quality-2026-04-25.zip
//   node scripts/zenodo-deposit.mjs --program public-service-data-quality --publish

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");

const API = "https://zenodo.org/api";
const SANDBOX = "https://sandbox.zenodo.org/api";

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}
function flag(name) {
  return process.argv.includes(`--${name}`);
}

function loadToken() {
  const envFile = path.join(REPO_ROOT, ".env.local");
  if (!fs.existsSync(envFile)) {
    console.error("FAIL — .env.local not found at repo root");
    process.exit(2);
  }
  const lines = fs.readFileSync(envFile, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const m = line.match(/^\s*ZENODO_TOKEN\s*=\s*(.+?)\s*$/);
    if (m) return m[1].replace(/^["']|["']$/g, "");
  }
  console.error("FAIL — ZENODO_TOKEN missing from .env.local");
  process.exit(2);
}

const program = arg("program");
if (!program) {
  console.error("Usage: --program <slug> [--dry-run|--upload <file>|--publish] [--sandbox] [--id <N>]");
  process.exit(2);
}

const baseApi = flag("sandbox") ? SANDBOX : API;
const token = loadToken();
const metaPath = path.join(REPO_ROOT, "research", "zenodo", `${program}.json`);
const statePath = path.join(REPO_ROOT, "research", "zenodo", `${program}.deposition.json`);

if (!fs.existsSync(metaPath)) {
  console.error(`FAIL — metadata file missing: ${metaPath}`);
  process.exit(2);
}

async function api(method, urlPath, body, contentType) {
  const url = urlPath.startsWith("http") ? urlPath : `${baseApi}${urlPath}`;
  const headers = { Authorization: `Bearer ${token}` };
  let payload;
  if (body) {
    if (contentType === "application/octet-stream") {
      headers["Content-Type"] = "application/octet-stream";
      payload = body;
    } else {
      headers["Content-Type"] = "application/json";
      payload = JSON.stringify(body);
    }
  }
  const r = await fetch(url, { method, headers, body: payload });
  const text = await r.text();
  let json;
  try { json = JSON.parse(text); } catch { json = { _raw: text }; }
  if (!r.ok) {
    console.error(`HTTP ${r.status} ${method} ${url}`);
    console.error(JSON.stringify(json, null, 2));
    process.exit(1);
  }
  return json;
}

function loadState() {
  if (!fs.existsSync(statePath)) return {};
  return JSON.parse(fs.readFileSync(statePath, "utf8"));
}
function saveState(s) {
  fs.writeFileSync(statePath, JSON.stringify(s, null, 2));
}

async function dryRun() {
  const meta = JSON.parse(fs.readFileSync(metaPath, "utf8"));
  if (!meta.metadata) {
    console.error("FAIL — metadata file has no `metadata` key");
    process.exit(2);
  }
  console.log(`[dry-run] POST ${baseApi}/deposit/depositions`);
  const dep = await api("POST", "/deposit/depositions", { metadata: meta.metadata });
  const reservedDoi = dep.metadata?.prereserve_doi?.doi || dep.doi || null;
  const state = {
    program,
    api: baseApi,
    deposition_id: dep.id,
    deposition_url: dep.links?.html,
    self: dep.links?.self,
    bucket: dep.links?.bucket,
    reserved_doi: reservedDoi,
    state: dep.state,
    created: dep.created,
    submitted: dep.submitted,
    published: dep.submitted_at || null,
  };
  saveState(state);
  console.log(`OK — draft deposition created.`);
  console.log(`  id           = ${dep.id}`);
  console.log(`  reserved DOI = ${reservedDoi ?? "(none yet — visible in draft UI)"}`);
  console.log(`  state        = ${dep.state}`);
  console.log(`  edit URL     = ${dep.links?.html}`);
  console.log(`  bucket       = ${dep.links?.bucket}`);
  console.log(`\nstate written to ${path.relative(REPO_ROOT, statePath)}`);
  console.log(`\nNext: review the draft at ${dep.links?.html}; then upload + publish, or discard.`);
}

async function upload(file) {
  const state = loadState();
  if (!state.deposition_id) {
    console.error("FAIL — no deposition_id in state. Run --dry-run first.");
    process.exit(2);
  }
  if (!state.bucket) {
    console.error("FAIL — no bucket URL in state. Re-run --dry-run.");
    process.exit(2);
  }
  if (!fs.existsSync(file)) {
    console.error(`FAIL — file does not exist: ${file}`);
    process.exit(2);
  }
  const data = fs.readFileSync(file);
  const name = path.basename(file);
  const url = `${state.bucket}/${encodeURIComponent(name)}`;
  console.log(`[upload] PUT ${url} (${data.length} bytes)`);
  const r = await api("PUT", url, data, "application/octet-stream");
  console.log(`OK — uploaded ${name}`);
  console.log(`  size     = ${r.size}`);
  console.log(`  checksum = ${r.checksum}`);
  state.uploaded = state.uploaded || [];
  state.uploaded.push({ name, size: r.size, checksum: r.checksum });
  saveState(state);
}

async function publish() {
  const state = loadState();
  if (!state.deposition_id) {
    console.error("FAIL — no deposition_id in state.");
    process.exit(2);
  }
  console.log(`[publish] POST ${baseApi}/deposit/depositions/${state.deposition_id}/actions/publish`);
  const dep = await api("POST", `/deposit/depositions/${state.deposition_id}/actions/publish`);
  state.state = dep.state;
  state.submitted = dep.submitted;
  state.doi = dep.doi || dep.metadata?.doi;
  state.doi_url = dep.doi_url;
  state.published_at = new Date().toISOString();
  state.record_url = dep.links?.record_html;
  saveState(state);
  console.log(`OK — published.`);
  console.log(`  DOI        = ${state.doi}`);
  console.log(`  record URL = ${state.record_url}`);
  console.log(`\nDOI is permanent. Next: write the DOI back into article frontmatter and pre-registration.md.`);
}

async function discard() {
  const state = loadState();
  if (!state.deposition_id) {
    console.error("FAIL — no deposition_id in state.");
    process.exit(2);
  }
  if (state.state !== "unsubmitted") {
    console.error(`FAIL — cannot discard a ${state.state} deposition. Only unsubmitted drafts.`);
    process.exit(2);
  }
  console.log(`[discard] DELETE ${baseApi}/deposit/depositions/${state.deposition_id}`);
  const r = await fetch(`${baseApi}/deposit/depositions/${state.deposition_id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!r.ok && r.status !== 204) {
    console.error(`HTTP ${r.status} DELETE`);
    console.error(await r.text());
    process.exit(1);
  }
  console.log(`OK — draft ${state.deposition_id} discarded.`);
  fs.unlinkSync(statePath);
  console.log(`State file removed.`);
}

const action =
  flag("dry-run") ? "dry-run" :
  process.argv.includes("--upload") ? "upload" :
  flag("publish") ? "publish" :
  flag("discard") ? "discard" :
  null;

if (!action) {
  console.error("Usage: --program <slug> [--dry-run|--upload <file>|--publish|--discard] [--sandbox]");
  process.exit(2);
}

if (action === "dry-run") await dryRun();
else if (action === "upload") await upload(arg("upload"));
else if (action === "publish") await publish();
else if (action === "discard") await discard();
