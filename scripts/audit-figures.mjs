#!/usr/bin/env node
// Deterministic inventory of logical research figures.
// PNG/SVG exports of the same basename count as one figure.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const PROGRAM_INDEX = path.join(REPO_ROOT, "reporting-site", "public", "programs", "index.json");
const OUTPUT = path.join(REPO_ROOT, "research", "generated", "figure-audit.json");
const VISUAL_EXTENSIONS = new Set([".png", ".svg", ".webp", ".jpg", ".jpeg"]);
const DATA_EXTENSIONS = new Set([".csv", ".tsv", ".json", ".geojson", ".parquet"]);

function walkFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walkFiles(file));
    else files.push(file);
  }
  return files;
}

function relative(file, root) {
  return path.relative(root, file).replaceAll(path.sep, "/");
}

function logicalAssets(files, root, extensions) {
  const groups = new Map();
  for (const file of files) {
    const extension = path.extname(file).toLowerCase();
    if (!extensions.has(extension)) continue;
    const rel = relative(file, root);
    const key = rel.slice(0, -extension.length);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(extension.slice(1));
  }
  return [...groups.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([file, formats]) => ({ file, formats: [...new Set(formats)].sort() }));
}

function articleFiles() {
  return walkFiles(path.join(REPO_ROOT, "articles")).filter((file) => file.endsWith(".md"));
}

function articleVisuals(slug) {
  const matches = [];
  for (const file of articleFiles()) {
    const text = fs.readFileSync(file, "utf8");
    if (!new RegExp(`^program:\\s*${slug}\\s*$`, "m").test(text)) continue;
    const urls = [...text.matchAll(/!\[[^\]]*\]\(([^)\s]+)[^)]*\)/g)].map((match) => match[1]);
    const programUrls = urls.filter((url) => url.includes(`/programs/${slug}/generated/charts/`));
    if (programUrls.length === 0) continue;
    matches.push({
      article: relative(file, REPO_ROOT),
      tier: path.dirname(relative(file, path.join(REPO_ROOT, "articles"))) === "."
        ? "working-paper"
        : path.basename(path.dirname(file)).replace(/^_/, ""),
      references: programUrls,
    });
  }
  return matches;
}

if (!fs.existsSync(PROGRAM_INDEX)) {
  console.error(`Missing program index: ${PROGRAM_INDEX}`);
  process.exit(1);
}

const index = JSON.parse(fs.readFileSync(PROGRAM_INDEX, "utf8"));
const programs = [];

for (const slug of index.programs) {
  const programRoot = path.join(REPO_ROOT, slug);
  const generatedRoot = path.join(programRoot, "generated");
  const generatedFiles = walkFiles(generatedRoot);
  const figures = logicalAssets(
    generatedFiles.filter((file) => relative(file, generatedRoot).startsWith("charts/")),
    generatedRoot,
    VISUAL_EXTENSIONS,
  ).map((figure) => ({
    ...figure,
    role: figure.file.endsWith(`${slug}-thumbnail`) ? "hero" : "evidence",
  }));
  const dataObjects = logicalAssets(
    generatedFiles.filter((file) => !relative(file, generatedRoot).startsWith("charts/")),
    generatedRoot,
    DATA_EXTENSIONS,
  );
  const articles = articleVisuals(slug);
  const workingPaperReferences = articles
    .filter((article) => article.tier === "working-paper")
    .reduce((sum, article) => sum + article.references.length, 0);

  programs.push({
    slug,
    logical_figure_count: figures.length,
    evidence_figure_count: figures.filter((figure) => figure.role === "evidence").length,
    has_hero: figures.some((figure) => figure.role === "hero"),
    generated_data_object_count: dataObjects.length,
    working_paper_figure_references: workingPaperReferences,
    status: figures.length === 0 ? "no-visual" : figures.every((figure) => figure.role === "hero") ? "hero-only" : "multiple-figures",
    figures,
    article_references: articles,
  });
}

const summary = {
  programs: programs.length,
  with_multiple_figures: programs.filter((program) => program.status === "multiple-figures").length,
  hero_only: programs.filter((program) => program.status === "hero-only").length,
  with_no_visual: programs.filter((program) => program.status === "no-visual").length,
  working_papers_with_figure_references: programs.filter((program) => program.working_paper_figure_references > 0).length,
};

fs.mkdirSync(path.dirname(OUTPUT), { recursive: true });
fs.writeFileSync(OUTPUT, `${JSON.stringify({
  audit_date: new Date().toISOString().slice(0, 10),
  attestation_chain: "ai-first",
  definition: "One logical figure per basename; PNG/SVG/JPEG/WebP exports count once.",
  summary,
  programs,
}, null, 2)}\n`);

console.log(`Figure audit: ${summary.programs} programs`);
console.log(`  multiple figures: ${summary.with_multiple_figures}`);
console.log(`  hero only: ${summary.hero_only}`);
console.log(`  no visual: ${summary.with_no_visual}`);
console.log(`  working papers with figure references: ${summary.working_papers_with_figure_references}`);
console.log(`Wrote ${OUTPUT}`);
