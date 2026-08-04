#!/usr/bin/env node
// scripts/build-taxonomy.mjs
//
// Maps the repository's free-text article tags onto a subject taxonomy a
// practitioner can navigate, and normalizes geographies to country names.
//
// Why this exists
// ---------------
// The site's information architecture is process-based — Research, Explore,
// Review desk, Explorations — which describes how we work, not what a reader
// came for. Development Asia, the standard the owner named, is subject-based:
// Topics and Countries. Our articles already carry `topics` and `geographies`,
// but the values are 82 free-text tags that mix subjects ("heat", "education")
// with methods ("construct-validation", "OSM", "population-denominator"), and
// geographies that mix ISO3 codes ("BGD"), names ("Nepal"), and groupings
// ("ADB DMCs", "regional").
//
// A reader looking for health research cannot navigate that. This script does
// not throw the existing tags away — method tags are how this shop actually
// thinks — it maps them onto sectors so both views exist.
//
// Output: reporting-site/public/taxonomy.json

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const SITE = path.join(REPO_ROOT, "reporting-site", "public");

// Development Asia uses 22 sectors. These are the ones this repository's
// content actually populates, plus "Data and Measurement" — which is not in
// their list but is genuinely what this shop studies, and pretending otherwise
// would force every piece into a sector that fits it worse.
const SECTORS = {
  "Agriculture": ["agriculture", "crop-diversification", "food-price", "market-prices", "crops", "food-security", "farm"],
  "Climate Change": ["climate", "heat", "climate-health", "warming", "adaptation", "drought", "flood", "cyclone", "disaster", "climate-risk"],
  "Economics": ["labor-capacity", "labour", "employment", "growth", "gdp", "inflation", "prices", "macroeconomic", "trade", "port", "shipping"],
  "Education": ["education", "school-disruption", "school", "learning", "schooling"],
  "Energy": ["energy", "grid", "electricity", "power", "outage", "single-fuel"],
  "Environment": ["pm2.5", "air-quality", "pollution", "environment", "emissions"],
  "Finance Sector Development": ["remittances", "corridor-cost", "finance", "payments", "banking"],
  "Health": ["health", "health-facilities", "mortality", "morbidity", "nutrition"],
  "ICT": ["digital inclusion", "digital", "connectivity", "internet", "mobile"],
  "Poverty": ["poverty", "mpi", "deprivation", "welfare", "livelihoods"],
  "Social Development": ["migration", "migrant-stock", "forced-displacement", "social-protection", "access", "informality", "gender", "inclusion", "exclusion"],
  "Transport": ["road", "market-access", "connectivity-road", "logistics", "hinterland"],
  "Urban Development": ["urbanization", "urban", "settlement", "built-up", "coastal"],
  "Water": ["water", "irrigation", "water-stress", "groundwater"],
  "Data and Measurement": ["measurement", "construct-validation", "data-quality", "measurement-gap", "public data", "population-denominator", "public-service-data-quality", "osm", "methodology", "governance", "freshness", "observability", "coverage"],
};

// ISO3 -> display name, for the codes this repository actually uses.
const COUNTRIES = {
  AFG: "Afghanistan", ARM: "Armenia", BGD: "Bangladesh", BTN: "Bhutan",
  KHM: "Cambodia", CHN: "China", FJI: "Fiji", IND: "India", IDN: "Indonesia",
  KGZ: "Kyrgyz Republic", LAO: "Lao PDR", MYS: "Malaysia", MDV: "Maldives",
  MNG: "Mongolia", MMR: "Myanmar", NRU: "Nauru", NPL: "Nepal", PAK: "Pakistan",
  PNG: "Papua New Guinea", PHL: "Philippines", WSM: "Samoa", LKA: "Sri Lanka",
  TJK: "Tajikistan", THA: "Thailand", TON: "Tonga", TUV: "Tuvalu",
  UZB: "Uzbekistan", VUT: "Vanuatu", VNM: "Viet Nam",
};

// Values that name a grouping rather than a country.
const REGIONAL = new Set([
  "adb dmcs", "adb developing economies", "regional", "asia-pacific",
  "developing asia", "asia and the pacific", "global",
]);

const NAME_TO_ISO = Object.fromEntries(
  Object.entries(COUNTRIES).map(([iso, name]) => [name.toLowerCase(), iso]),
);

function sectorsFor(tags) {
  const found = new Set();
  for (const raw of tags) {
    const tag = String(raw).toLowerCase().trim();
    for (const [sector, keys] of Object.entries(SECTORS)) {
      if (keys.some((k) => tag === k || tag.includes(k) || k.includes(tag))) {
        found.add(sector);
      }
    }
  }
  return [...found].sort();
}

function normalizeGeo(values) {
  const countries = new Set();
  let regional = false;
  for (const raw of values) {
    const v = String(raw).trim();
    if (REGIONAL.has(v.toLowerCase())) { regional = true; continue; }
    const upper = v.toUpperCase();
    if (COUNTRIES[upper]) { countries.add(upper); continue; }
    const iso = NAME_TO_ISO[v.toLowerCase()];
    if (iso) { countries.add(iso); continue; }
    regional = true; // unrecognized: treat as a grouping rather than drop it
  }
  return { countries: [...countries].sort(), regional };
}

const articles = JSON.parse(
  fs.readFileSync(path.join(SITE, "articles", "_index.json"), "utf8"),
);

const bySector = {};
const byCountry = {};
let untagged = 0;

const enriched = articles.map((a) => {
  const sectors = sectorsFor(a.topics || []);
  const { countries, regional } = normalizeGeo(a.geographies || []);
  if (sectors.length === 0) untagged += 1;

  const entry = {
    slug: a.slug,
    title: a.title,
    subtitle: a.subtitle || "",
    program: a.program || null,
    tier: a.tier || a.kind || "",
    maturity: a.maturity || "",
    sectors,
    countries,
    regional,
  };
  for (const s of sectors) (bySector[s] ||= []).push(entry.slug);
  for (const c of countries) (byCountry[c] ||= []).push(entry.slug);
  return entry;
});

const taxonomy = {
  generated_at: new Date().toISOString(),
  sectors: Object.keys(SECTORS)
    .filter((s) => (bySector[s] || []).length > 0)
    .map((s) => ({
      name: s,
      slug: s.toLowerCase().replace(/[^a-z0-9]+/g, "-"),
      count: bySector[s].length,
      slugs: bySector[s],
    }))
    .sort((a, b) => b.count - a.count),
  countries: Object.entries(byCountry)
    .map(([iso, slugs]) => ({
      iso3: iso,
      name: COUNTRIES[iso],
      count: slugs.length,
      slugs,
    }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name)),
  articles: enriched,
};

fs.writeFileSync(
  path.join(SITE, "taxonomy.json"),
  JSON.stringify(taxonomy, null, 2),
);

console.log(
  `taxonomy: ${taxonomy.sectors.length} sectors, ` +
    `${taxonomy.countries.length} countries, ${enriched.length} articles ` +
    `(${untagged} with no sector match)`,
);
for (const s of taxonomy.sectors) console.log(`  ${String(s.count).padStart(3)}  ${s.name}`);
