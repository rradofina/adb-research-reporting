#!/usr/bin/env node
// scripts/build-slides.mjs
// Builds the slide deck for a single program: regenerates the charts from
// the latest committed CSVs, then runs `quarto render` to produce the
// .pptx into reporting-site/public/programs/{slug}/.
//
// Implements the slide-deck rule in research/factory.md: source of record is
// markdown in articles/_slides/, resolved by exact filename or its `program`
// frontmatter. The .pptx is regenerated from that source. Charts are refreshed
// first so the deck cannot drift from the working paper's figure spine.

import { execSync, execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");

const slug = process.argv[2] || "public-service-data-quality";
const slidesDir = path.join(REPO_ROOT, "articles", "_slides");
const programDir = path.join(REPO_ROOT, slug);
const destDir = path.join(REPO_ROOT, "reporting-site", "public", "programs", slug);
const destPptx = path.join(destDir, `${slug}-deck.pptx`);

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Prefer the program-slug filename, then resolve the unique slide source whose
// frontmatter declares `program: <slug>`. Older publication ladders use
// finding-oriented filenames, so requiring filename equality left valid decks
// permanently unbuilt.
function findSlideSource() {
  const exact = path.join(slidesDir, `${slug}.md`);
  if (fs.existsSync(exact)) return exact;
  if (!fs.existsSync(slidesDir)) return null;
  const programLine = new RegExp(`^program:\\s*["']?${escapeRegExp(slug)}["']?\\s*$`, "m");
  const candidates = fs.readdirSync(slidesDir)
    .filter((file) => file.endsWith(".md"))
    .map((file) => path.join(slidesDir, file))
    .filter((file) => programLine.test(fs.readFileSync(file, "utf8")));
  if (candidates.length > 1) {
    console.error(`Multiple slide sources declare program: ${slug}`);
    for (const candidate of candidates) console.error(`  - ${path.relative(REPO_ROOT, candidate)}`);
    process.exit(1);
  }
  return candidates[0] || null;
}

const slideSrc = findSlideSource();

// Find the program's chart-build script. Convention: `scripts/build-*.py`
// whose filename contains "chart", "figure", or "choropleth". This lets a
// new program ship its own build-*.py without modifying this script.
function findChartScript() {
  const fixed = path.join(programDir, "scripts", "build-choropleth.py");
  if (fs.existsSync(fixed)) return fixed;
  const scriptsDir = path.join(programDir, "scripts");
  if (!fs.existsSync(scriptsDir)) return null;
  const candidates = fs.readdirSync(scriptsDir)
    .filter((f) => f.startsWith("build-") && f.endsWith(".py"))
    .filter((f) => ["chart", "figure", "choropleth"].some((token) => f.toLowerCase().includes(token)));
  return candidates.length > 0 ? path.join(scriptsDir, candidates[0]) : null;
}
const chartScript = findChartScript();

if (!slideSrc || !fs.existsSync(slideSrc)) {
  console.error(`No slide source found for program: ${slug}`);
  process.exit(1);
}

console.log(`Slide source: ${path.relative(REPO_ROOT, slideSrc)}`);

// Locate Quarto. Prefer PATH, fall back to the standard Windows install
// path because the current shell may not have refreshed PATH after install.
function findQuarto() {
  try {
    execSync("quarto --version", { stdio: "ignore" });
    return "quarto";
  } catch {}
  const candidates = [
    "C:\\Program Files\\Quarto\\bin\\quarto.exe",
    "/usr/local/bin/quarto",
    "/opt/quarto/bin/quarto",
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  console.error("Quarto not found on PATH or standard install paths.");
  console.error("Install via `winget install Posit.Quarto` or download from quarto.org.");
  process.exit(1);
}

const quarto = findQuarto();
console.log(`Using quarto at: ${quarto === "quarto" ? "PATH" : quarto}`);

// Step 1 — regenerate charts from latest CSVs (so the slide chart cannot
// drift from the working paper's chart). execFileSync passes argv as a
// list — slug-bearing paths are not interpolated into a shell string, so
// odd characters in slug cannot inject.
if (chartScript && fs.existsSync(chartScript)) {
  console.log(`\n[1/2] Regenerating charts via ${path.relative(REPO_ROOT, chartScript)}`);
  execFileSync("python", [chartScript], { stdio: "inherit", cwd: REPO_ROOT });
} else {
  console.log(`\n[1/2] No build-*chart/figure/choropleth*.py for ${slug}; skipping chart refresh.`);
}

// Step 2 — Quarto render in place, then move to final destination.
// Quarto resolves --output-dir relative to the input file's directory and
// strips path components in some versions, so the most reliable approach
// is to render next to the source and then move the artifact ourselves.
fs.mkdirSync(destDir, { recursive: true });
console.log(`\n[2/2] Quarto render → ${path.relative(REPO_ROOT, destPptx)}`);

const slideDir = path.dirname(slideSrc);
const renderBase = `.build-${slug}`;
const renderSrc = path.join(slideDir, `${renderBase}.md`);
const intermediatePptx = path.join(slideDir, `${renderBase}.pptx`);

// Web-root paths are correct on the site but not in a local Quarto render.
// Rewrite only the transient render copy. Pandoc treats Markdown image alt
// text as a visible PowerPoint caption, so keep the authored alt text in the
// repository source while omitting the duplicate caption in the built deck.
const authored = fs.readFileSync(slideSrc, "utf8");
const renderable = authored
  .replaceAll(`/programs/${slug}/`, `../../${slug}/`)
  .replace(/!\[[^\]]*\](\([^\r\n]+?\))(\{[^\r\n}]*\})?/g, (_match, target, attrs = "") => `![]${target}${attrs}`);
fs.writeFileSync(renderSrc, renderable, "utf8");

try {
  execFileSync(quarto, ["render", renderSrc, "--to", "pptx"], { stdio: "inherit", cwd: REPO_ROOT });

  if (!fs.existsSync(intermediatePptx)) {
    console.error(`\nQuarto did not produce ${intermediatePptx}. Check output above.`);
    process.exit(1);
  }

  fs.copyFileSync(intermediatePptx, destPptx);
} finally {
  if (fs.existsSync(intermediatePptx)) fs.unlinkSync(intermediatePptx);
  if (fs.existsSync(renderSrc)) fs.unlinkSync(renderSrc);
}

const size = fs.statSync(destPptx).size;
const sizeKb = (size / 1024).toFixed(1);
console.log(`\nDone. ${path.relative(REPO_ROOT, destPptx)} (${sizeKb} KB)`);
