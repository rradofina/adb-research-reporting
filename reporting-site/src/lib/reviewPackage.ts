import { readFile, readdir } from "node:fs/promises";
import path from "node:path";

// Mirrors review-factory/build_package.py. The §2.7 fields are the reason this
// type exists separately from StoryPackage: a review's trustworthiness is
// per-record, so the reader surface has to carry per-record provenance rather
// than one badge for the whole document.

export interface ReviewRecord {
  id: string;
  category: string;
  study: string;
  year: number;
  source: string;
  geography: string;
  subregion: string;
  shock: string;
  welfare_indicator: string;
  estimate: string;
  methodology: string;
  identification: string;
  limitations: string;
  confidence: "High" | "Medium" | "Low" | string;
  doi: string;
  url: string;
  identity_status: string | null;
  identity_route: "doi" | "url";
  locator: string;
  locator_basis: string;
  locator_confirmed: boolean;
  screen_status: string | null;
  screen_reason: string;
  citable: boolean;
}

export interface ReviewGate {
  label: string;
  status: "pass" | "fail" | "partial" | string;
  value: string;
}

export interface ReviewCounts {
  records: number;
  citable: number;
  provisional: number;
  unread: number;
  identity_by_doi: number;
  schema_blocking: number;
}

export interface ReviewArtifact {
  name: string;
  ext: string;
  bytes: number;
  sha256?: string;
  href?: string;
}

export interface ReviewPackage {
  schema_version: number;
  slug: string;
  title: string;
  commissioned_by: string;
  commissioned_date: string;
  attestation_chain: string;
  maturity: string;
  citable: boolean;
  citable_blocker: string;
  generated_at: string;
  counts: ReviewCounts;
  gate_state: ReviewGate[];
  records: ReviewRecord[];
  manuscript_markdown: string;
  source_queue_markdown: string;
  artifacts: ReviewArtifact[];
  non_claim: string;
}

export interface ReviewIndexEntry {
  slug: string;
  title: string;
  commissioned_by: string;
  commissioned_date: string;
  attestation_chain: string;
  maturity: string;
  citable: boolean;
  citable_blocker: string;
  counts: ReviewCounts;
  generated_at: string;
}

const REVIEWS_DIR = path.join(process.cwd(), "public", "reviews");

export async function loadReviewIndex(): Promise<ReviewIndexEntry[]> {
  try {
    const raw = await readFile(path.join(REVIEWS_DIR, "index.json"), "utf8");
    return JSON.parse(raw) as ReviewIndexEntry[];
  } catch {
    return [];
  }
}

export async function loadReview(slug: string): Promise<ReviewPackage | null> {
  try {
    const raw = await readFile(
      path.join(REVIEWS_DIR, slug, "review-package.json"),
      "utf8",
    );
    return JSON.parse(raw) as ReviewPackage;
  } catch {
    return null;
  }
}

export async function loadReviewArtifacts(
  slug: string,
): Promise<ReviewArtifact[]> {
  try {
    const raw = await readFile(
      path.join(REVIEWS_DIR, slug, "artifacts.json"),
      "utf8",
    );
    return JSON.parse(raw) as ReviewArtifact[];
  } catch {
    return [];
  }
}

export async function reviewSlugs(): Promise<string[]> {
  try {
    const entries = await readdir(REVIEWS_DIR, { withFileTypes: true });
    return entries.filter((e) => e.isDirectory()).map((e) => e.name);
  } catch {
    return [];
  }
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
