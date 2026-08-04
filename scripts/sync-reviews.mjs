#!/usr/bin/env node
// scripts/sync-reviews.mjs
//
// Copies each §2.7 evidence review's reader package and downloadable
// artifacts into reporting-site/public/reviews/{slug}/.
//
// CONSTITUTION.md §2.7 (review provenance), §10 (publication pathway),
// §11 (reproducibility — every synced file carries a SHA-256), §18.2
// (honest labeling: the package's citability counts reach the public surface
// unmodified, so the site cannot present a screened figure as a read one).
//
// A review is any directory with a review.json manifest. Discovery mirrors
// review-factory/factory/topic.py so the two never drift.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const DEST_ROOT = path.join(REPO_ROOT, "reporting-site", "public", "reviews");

const SKIP = new Set([
  "node_modules", ".git", ".cache", ".next", "__pycache__", "tmp",
  "dist", "outputs", "figures", "_archive", "reporting-site", "review-packets",
]);

function discoverReviews(base) {
  const found = [];
  const stack = [base];
  while (stack.length) {
    const dir = stack.pop();
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    if (entries.some((e) => e.isFile() && e.name === "review.json")) {
      const manifest = JSON.parse(
        fs.readFileSync(path.join(dir, "review.json"), "utf8"),
      );
      found.push({ root: dir, slug: manifest.slug ?? path.basename(dir), manifest });
      continue; // a review never nests another review
    }
    for (const e of entries) {
      if (e.isDirectory() && !SKIP.has(e.name) && !e.name.startsWith(".")) {
        stack.push(path.join(dir, e.name));
      }
    }
  }
  return found.sort((a, b) => a.slug.localeCompare(b.slug));
}

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

const reviews = discoverReviews(REPO_ROOT);
if (reviews.length === 0) {
  console.log("No reviews found (no review.json anywhere).");
  process.exit(0);
}

fs.mkdirSync(DEST_ROOT, { recursive: true });
const index = [];

for (const review of reviews) {
  const pkgPath = path.join(review.root, "review-package.json");
  if (!fs.existsSync(pkgPath)) {
    console.warn(
      `! ${review.slug}: no review-package.json — run ` +
        `review-factory/build_package.py --review ${review.slug}`,
    );
    continue;
  }

  const dest = path.join(DEST_ROOT, review.slug);
  fs.mkdirSync(dest, { recursive: true });
  fs.copyFileSync(pkgPath, path.join(dest, "review-package.json"));

  const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));

  // Downloadable artifacts, with hashes so a reader can verify what they got.
  const artifactsSrc = path.join(
    review.root,
    review.manifest.artifacts_dir ?? ".",
  );
  const files = [];
  if (fs.existsSync(artifactsSrc)) {
    const outDir = path.join(dest, "artifacts");
    fs.mkdirSync(outDir, { recursive: true });
    for (const name of fs.readdirSync(artifactsSrc)) {
      const src = path.join(artifactsSrc, name);
      if (!fs.statSync(src).isFile()) continue;
      fs.copyFileSync(src, path.join(outDir, name));
      files.push({
        name,
        ext: path.extname(name).slice(1).toUpperCase(),
        bytes: fs.statSync(src).size,
        sha256: sha256(src),
        href: `/reviews/${review.slug}/artifacts/${name}`,
      });
    }
  }
  fs.writeFileSync(
    path.join(dest, "artifacts.json"),
    JSON.stringify(files, null, 2),
  );

  // Hero image lives in the review folder; copy it so the card and article
  // can show it without reaching outside public/.
  if (pkg.hero_image) {
    const heroSrc = path.join(review.root, pkg.hero_image);
    if (fs.existsSync(heroSrc)) {
      const heroName = path.basename(heroSrc);
      fs.copyFileSync(heroSrc, path.join(dest, heroName));
      pkg.hero_href = `/reviews/${review.slug}/${heroName}`;
      fs.writeFileSync(
        path.join(dest, "review-package.json"),
        JSON.stringify(pkg, null, 2),
      );
    }
  }

  index.push({
    slug: review.slug,
    title: pkg.title,
    content_type: pkg.content_type,
    headline: pkg.headline,
    standfirst: pkg.standfirst,
    topics: pkg.topics,
    hero_href: pkg.hero_href ?? null,
    commissioned_by: pkg.commissioned_by,
    commissioned_date: pkg.commissioned_date,
    attestation_chain: pkg.attestation_chain,
    maturity: pkg.maturity,
    citable: pkg.citable,
    citable_blocker: pkg.citable_blocker,
    counts: pkg.counts,
    generated_at: pkg.generated_at,
  });

  const c = pkg.counts;
  console.log(
    `${review.slug}: ${c.records} records — ${c.citable} citable, ` +
      `${c.provisional} provisional, ${c.unread} unread; ` +
      `${files.length} artifact(s)`,
  );
}

fs.writeFileSync(
  path.join(DEST_ROOT, "index.json"),
  JSON.stringify(index, null, 2),
);
console.log(`\nWrote ${path.relative(REPO_ROOT, DEST_ROOT)}/index.json (${index.length} review(s))`);
