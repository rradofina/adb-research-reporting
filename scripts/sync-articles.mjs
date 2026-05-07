#!/usr/bin/env node
// scripts/sync-articles.mjs
// Copies articles from /articles/*.md (source-of-truth) to
// reporting-site/public/articles/ for runtime fetching, and produces
// a public/articles/index.json with frontmatter for the listings page.
//
// Run automatically via `npm run prebuild` in reporting-site.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// Resolve paths relative to the script file, not the cwd that invoked it.
// This lets `npm run prebuild` from reporting-site/ still find ../articles.
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const SRC = path.join(REPO_ROOT, "articles");
const DEST = path.join(REPO_ROOT, "reporting-site", "public", "articles");

if (!fs.existsSync(SRC)) {
  console.log(`No ${SRC}/ directory; nothing to sync.`);
  process.exit(0);
}
fs.mkdirSync(DEST, { recursive: true });

function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!m) return { frontmatter: {}, body: text };
  const frontmatter = parseYamlIsh(m[1]);
  return { frontmatter, body: m[2] };
}

// Tiny YAML-ish parser: handles flat keys, scalar values, simple arrays
// in [] notation, and >- folded blocks. Intentionally limited — keeps
// articles' frontmatter shape disciplined.
function parseYamlIsh(text) {
  const out = {};
  const lines = text.split(/\r?\n/);
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) { i++; continue; }
    const key = m[1];
    let val = m[2];
    if (val === ">" || val === ">-") {
      i++;
      const buf = [];
      while (i < lines.length && /^\s+/.test(lines[i])) {
        buf.push(lines[i].trim());
        i++;
      }
      out[key] = buf.join(" ").trim();
      continue;
    }
    if (val === "" && i + 1 < lines.length && /^\s+-\s/.test(lines[i + 1])) {
      // YAML list of inline objects
      i++;
      const arr = [];
      while (i < lines.length && /^\s+-\s/.test(lines[i])) {
        const inner = lines[i].replace(/^\s+-\s/, "").trim();
        // Inline object {a: b, c: d}
        const obj = {};
        const objMatch = inner.match(/^\{(.*)\}$/);
        if (objMatch) {
          for (const part of objMatch[1].split(",")) {
            const kv = part.split(":").map((s) => s.trim());
            if (kv.length === 2) obj[kv[0]] = kv[1];
          }
          arr.push(obj);
        } else {
          arr.push(inner);
        }
        i++;
      }
      out[key] = arr;
      continue;
    }
    if (val.startsWith("[") && val.endsWith("]")) {
      out[key] = val.slice(1, -1).split(",").map((s) => s.trim()).filter(Boolean);
    } else {
      out[key] = val;
    }
    i++;
  }
  return out;
}

// Collect markdown files: top-level articles/*.md (working papers) plus
// publication-ladder tier subdirectories articles/_brief/, _blog/, _social/,
// _slides/ — see research/factory.md "Publication ladder". Files in tier
// subdirectories are flattened to {slug}.md in the dest dir; the slug must
// be unique across the whole site (typical pattern: tier suffix in slug).
const TIER_DIRS = ["_brief", "_blog", "_social", "_slides"];

const sources = [];
for (const f of fs.readdirSync(SRC).filter((x) => x.endsWith(".md"))) {
  sources.push({ src: path.join(SRC, f), origFilename: f, tier: "working-paper" });
}
for (const dir of TIER_DIRS) {
  const tierPath = path.join(SRC, dir);
  if (!fs.existsSync(tierPath)) continue;
  const tierName = dir.replace(/^_/, "");
  for (const f of fs.readdirSync(tierPath).filter((x) => x.endsWith(".md"))) {
    sources.push({ src: path.join(tierPath, f), origFilename: f, tier: tierName });
  }
}

const index = [];
for (const { src, origFilename, tier } of sources) {
  const { frontmatter, body } = parseFrontmatter(fs.readFileSync(src, "utf8"));
  const slug = frontmatter.slug ?? path.basename(origFilename, ".md");
  const destFilename = tier === "working-paper" ? origFilename : `${slug}.md`;
  const dest = path.join(DEST, destFilename);
  fs.copyFileSync(src, dest);
  index.push({
    slug,
    title: frontmatter.title ?? "(untitled)",
    subtitle: frontmatter.subtitle ?? "",
    kind: frontmatter.kind ?? "blog",
    tier,
    status: frontmatter.status ?? "draft",
    program: frontmatter.program ?? "",
    maturity: frontmatter.maturity ?? "",
    topics: frontmatter.topics ?? [],
    geographies: frontmatter.geographies ?? [],
    abstract: frontmatter.abstract ?? "",
    authors: Array.isArray(frontmatter.authors)
      ? frontmatter.authors.map((a) => (typeof a === "string" ? a : a.name)).filter(Boolean)
      : [],
    published_at: frontmatter.published_at ?? "",
    updated_at: frontmatter.updated_at ?? "",
    doi: frontmatter.doi ?? "",
    file: destFilename,
    attestation_chain: frontmatter.attestation_chain ?? "",
    constitution_ref: frontmatter.constitution_ref ?? "",
    review_external_chain: frontmatter.review_external_chain ?? "",
    review_internal_chain: frontmatter.review_internal_chain ?? "",
  });
}

index.sort((a, b) => (b.updated_at ?? "").localeCompare(a.updated_at ?? ""));

fs.writeFileSync(path.join(DEST, "index.json"), JSON.stringify(index, null, 2));
console.log(`Synced ${sources.length} article(s) → ${DEST}/`);
