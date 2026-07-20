import type { Metadata } from "next";
import ShowcaseEvidenceAudit from "@/views/ShowcaseEvidenceAudit";
import { showcaseReports } from "@/data/showcaseReports";

const EXPLICIT_SHOWCASE_ROUTES = new Set([
  "access-map-completeness",
  "air-monitoring-observability",
  "data-freshness",
  "disaster-metric-falsification",
  "psdq-source-disagreement",
  "remittance-flow-weighting",
  "shock-payment-rails",
]);

export function generateStaticParams() {
  return showcaseReports
    .map((report) => report.href.match(/^\/showcase\/([^/]+)$/)?.[1])
    .filter((slug): slug is string => Boolean(slug))
    .filter((slug) => !EXPLICIT_SHOWCASE_ROUTES.has(slug))
    .map((reportSlug) => ({ reportSlug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ reportSlug: string }>;
}): Promise<Metadata> {
  const { reportSlug } = await params;
  const report = showcaseReports.find((r) => r.href === `/showcase/${reportSlug}`);
  if (!report) return {};
  return {
    title: report.title,
    description: report.deck,
  };
}

export default async function Page({
  params,
}: {
  params: Promise<{ reportSlug: string }>;
}) {
  const { reportSlug } = await params;
  return <ShowcaseEvidenceAudit reportSlug={reportSlug} />;
}
