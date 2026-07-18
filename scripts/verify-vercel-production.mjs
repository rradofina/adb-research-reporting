#!/usr/bin/env node

// Local, non-deploying production gate for the linked Vercel project.
// Constitution ref: §11 reproducibility; CLAUDE.md production-push rule.

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const siteRoot = path.join(repoRoot, "reporting-site");
const projectFile = path.join(repoRoot, ".vercel", "project.json");
const productionEnvFile = path.join(repoRoot, ".vercel", ".env.production.local");
const siteConfigFile = path.join(siteRoot, "vercel.json");
const sitePackageFile = path.join(siteRoot, "package.json");

function fail(message) {
  console.error(`VERCEL PRODUCTION GATE FAILED: ${message}`);
  process.exit(1);
}

function readJson(file, label) {
  if (!fs.existsSync(file)) fail(`${label} is missing: ${path.relative(repoRoot, file)}`);
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (error) {
    fail(`${label} is not valid JSON: ${error.message}`);
  }
}

function loadEnvFile(file) {
  if (!fs.existsSync(file)) fail("production environment is missing; run `npx vercel pull --yes --environment=production`");
  const values = {};
  for (const rawLine of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const separator = line.indexOf("=");
    if (separator < 1) continue;
    const key = line.slice(0, separator).trim();
    const rawValue = line.slice(separator + 1).trim();
    try {
      values[key] = rawValue.startsWith('"') ? JSON.parse(rawValue) : rawValue;
    } catch {
      values[key] = rawValue.replace(/^"|"$/g, "");
    }
  }
  return values;
}

const project = readJson(projectFile, "pulled Vercel project settings");
const settings = project.settings || {};
if (settings.rootDirectory !== "reporting-site") {
  fail(`Vercel Root Directory must be reporting-site, found ${settings.rootDirectory ?? "<unset>"}`);
}
if (settings.framework !== "nextjs") {
  fail(`Vercel Framework Preset must be nextjs, found ${settings.framework ?? "<unset>"}`);
}
for (const key of ["buildCommand", "installCommand", "outputDirectory"]) {
  if (settings[key] != null) fail(`Vercel project setting ${key} must use the Next.js default`);
}
if (fs.existsSync(path.join(repoRoot, "vercel.json"))) {
  fail("repository-root vercel.json must not exist when Vercel Root Directory is reporting-site");
}

const siteConfig = readJson(siteConfigFile, "reporting-site/vercel.json");
if (siteConfig.framework !== "nextjs") fail("reporting-site/vercel.json must declare framework nextjs");
for (const key of ["buildCommand", "installCommand", "outputDirectory"]) {
  if (key in siteConfig) fail(`reporting-site/vercel.json must not override ${key}`);
}

const sitePackage = readJson(sitePackageFile, "reporting-site/package.json");
if (!sitePackage.dependencies?.next) fail("Next.js must be a reporting-site production dependency");
if (sitePackage.scripts?.build !== "next build") fail("reporting-site build script must run next build");

const productionEnv = loadEnvFile(productionEnvFile);
const buildEnv = {
  ...process.env,
  ...productionEnv,
  VERCEL: "1",
  VERCEL_ENV: "production",
  NEXT_TELEMETRY_DISABLED: "1",
};
function runNpm(args) {
  if (process.platform === "win32") {
    const command = ["npm", ...args].join(" ");
    execFileSync(process.env.ComSpec || "C:\\Windows\\System32\\cmd.exe", ["/d", "/s", "/c", command], {
      cwd: siteRoot,
      env: buildEnv,
      stdio: "inherit",
    });
    return;
  }
  execFileSync("npm", args, { cwd: siteRoot, env: buildEnv, stdio: "inherit" });
}

console.log("[1/3] Clean install from reporting-site/package-lock.json");
runNpm(["ci"]);

console.log("[2/3] Next.js production build with pulled Vercel production environment");
runNpm(["run", "build"]);

console.log("[3/3] Validate production output and route contracts");
const nextRoot = path.join(siteRoot, ".next");
for (const relative of ["BUILD_ID", "routes-manifest.json", "prerender-manifest.json", "server/app"]) {
  if (!fs.existsSync(path.join(nextRoot, relative))) fail(`Next output is missing .next/${relative}`);
}

const programIndex = readJson(path.join(siteRoot, "public", "programs", "index.json"), "program index");
const prerender = readJson(path.join(nextRoot, "prerender-manifest.json"), "Next prerender manifest");
const routes = readJson(path.join(nextRoot, "routes-manifest.json"), "Next routes manifest");
const prerendered = new Set(Object.keys(prerender.routes || {}));
for (const program of programIndex.programs || []) {
  if (!prerendered.has(`/${program}`)) fail(`program route was not prerendered: /${program}`);
}
for (const route of ["/upgrades", "/showcase/access-map-completeness", "/showcase/psdq-source-disagreement"]) {
  if (!prerendered.has(route)) fail(`required public route was not prerendered: ${route}`);
}

const findingRedirects = (routes.redirects || []).filter((route) => route.source?.startsWith("/findings/"));
if (findingRedirects.length < 90) fail(`expected at least 90 legacy finding redirects, found ${findingRedirects.length}`);

console.log(`VERCEL PRODUCTION GATE PASSED: ${programIndex.programs.length} program routes and ${findingRedirects.length} finding redirects verified.`);
