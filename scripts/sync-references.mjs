#!/usr/bin/env node
// scripts/sync-references.mjs
// Parses references.bib at the repo root and writes a structured
// references.json into reporting-site/public/. The Article + Evidence
// pages consume this to render [@bibtex-key] as proper paper-style
// citations with author-year and clickable DOI footnotes.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const SRC = path.join(REPO_ROOT, "references.bib");
const DEST = path.join(REPO_ROOT, "reporting-site", "public", "references.json");

if (!fs.existsSync(SRC)) {
  console.error("references.bib missing");
  process.exit(1);
}

const text = fs.readFileSync(SRC, "utf8");

function cleanLatexValue(v) {
  return v
    .replace(/\\([&%$_#])/g, "$1")
    .replace(/\\'/g, "'")
    .replace(/\\url\{([^{}]+)\}/g, "$1")
    .replace(/\{([^{}]+)\}/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function cleanAuthorField(v) {
  return v
    .replace(/\\([&%$_#])/g, "$1")
    .replace(/\\'/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

function displayAuthor(author = "") {
  return author.replace(/[{}]/g, "").replace(/\s+/g, " ").trim();
}

function parseBibtex(src) {
  const entries = [];
  // Match @type{key, ... } including nested braces.
  const re = /@(\w+)\s*\{\s*([^,\s]+)\s*,([\s\S]*?)\n\}/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const type = m[1].toLowerCase();
    const key = m[2];
    const body = m[3];
    const fields = {};
    // Parse fields. Each field: name = {value} or name = "value".
    const fieldRe = /(\w+)\s*=\s*(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|"[^"]*")\s*,?/g;
    let f;
    while ((f = fieldRe.exec(body)) !== null) {
      let v = f[2];
      if (v.startsWith("{") && v.endsWith("}")) v = v.slice(1, -1);
      else if (v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1);
      const fieldName = f[1].toLowerCase();
      fields[fieldName] = fieldName === "author" ? cleanAuthorField(v) : cleanLatexValue(v);
    }
    entries.push({ type, key, ...fields });
  }
  return entries;
}

function shortAuthor(author) {
  if (!author) return "";
  const protectedOnly = author.trim().match(/^\{(.+)\}$/);
  if (protectedOnly) return displayAuthor(protectedOnly[1]);
  // BibTeX authors are "and"-separated. Take first author's last name.
  const list = author.split(/\s+and\s+/);
  if (list.length === 0) return "";
  const first = list[0].trim();
  const protectedCorporate = first.match(/^\{(.+)\}$/);
  if (protectedCorporate) return displayAuthor(protectedCorporate[1]);
  const lastName = first.includes(",") ? first.split(",")[0].trim() : first.trim().split(/\s+/).pop();
  if (list.length === 1) return lastName;
  if (list.length === 2) {
    const second = list[1].trim();
    const protectedSecond = second.match(/^\{(.+)\}$/);
    const sLast = second.includes(",") ? second.split(",")[0].trim() : second.trim().split(/\s+/).pop();
    return `${lastName} and ${protectedSecond ? displayAuthor(protectedSecond[1]) : sLast}`;
  }
  return `${lastName} et al.`;
}

function authorYear(e) {
  return `${shortAuthor(e.author)} ${e.year || "n.d."}`;
}

const entries = parseBibtex(text);
console.log(`parsed ${entries.length} entries`);

// Enrich each entry with rendered short and long citations.
const enriched = entries.map((e) => {
  const authorDisplay = displayAuthor(e.author);
  return {
    ...e,
    author: authorDisplay,
    short: authorYear(e),
    long: [
      authorDisplay,
      e.year ? `(${e.year})` : "",
      e.title ? `"${e.title}."` : "",
      e.journal || e.institution || e.publisher || "",
      e.volume ? `${e.volume}${e.number ? `(${e.number})` : ""}` : "",
      e.pages ? `pp. ${e.pages}` : "",
      e.doi ? `DOI: ${e.doi}` : "",
    ].filter(Boolean).join(" "),
  };
});

fs.mkdirSync(path.dirname(DEST), { recursive: true });
fs.writeFileSync(DEST, JSON.stringify(enriched, null, 2));
console.log(`wrote ${DEST}`);
