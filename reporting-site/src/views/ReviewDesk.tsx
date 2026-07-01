import Link from "next/link";
import {
  getShowcaseReportQuality,
  showcaseReports,
  type ShowcaseReadiness,
} from "../data/showcaseReports";

const readinessLabel: Record<ShowcaseReadiness, string> = {
  prototype: "Prototype evidence",
  "l3-candidate": "Evidence package",
  "evidence-audit": "Evidence audit",
  "owner-gated": "Owner-gated source note",
};

const reviewSteps = [
  {
    label: "Question",
    title: "Start with the measurement problem",
    copy:
      "Every report should tell you what official or public data cannot currently show, before it introduces a method.",
  },
  {
    label: "Evidence",
    title: "Open the generated files",
    copy:
      "The chart is not the evidence. Use the CSV, JSON, source notes, and retrieval records to inspect the underlying rows.",
  },
  {
    label: "Limits",
    title: "Read the non-claim before the result",
    copy:
      "The site should state what the method does not prove, where source coverage fails, and which claim remains blocked.",
  },
  {
    label: "Reproduce",
    title: "Follow the script path",
    copy:
      "A claim is not reviewable unless the route points back to committed scripts and a reproducible evidence packet.",
  },
];

const quickLinks = [
  {
    href: "/showcase/air-monitoring-observability",
    label: "Featured evidence",
    title: "Air-monitoring observability",
    copy: "Station visibility, source reconciliation, and explicit coverage-claim gates.",
  },
  {
    href: "/air-monitoring?view=evidence",
    label: "Evidence packet",
    title: "Air-monitoring files",
    copy: "Generated data, documentation, source walls, and audit artifacts.",
  },
  {
    href: "/constitution",
    label: "Governance",
    title: "Research constitution",
    copy: "Public-data, reproducibility, claim-maturity, and AI-disclosure rules.",
  },
  {
    href: "/versions",
    label: "Source record",
    title: "Version ledger",
    copy: "Source, retrieval, and version records for reproducible checks.",
  },
];

function shortText(value: string, limit = 260) {
  if (value.length <= limit) return value;
  const trimmed = value.slice(0, limit).replace(/\s+\S*$/, "");
  return `${trimmed}...`;
}

export default function ReviewDesk() {
  const evidencePackages = showcaseReports.filter((report) => {
    const readiness = getShowcaseReportQuality(report).readiness;
    return readiness === "l3-candidate" || readiness === "evidence-audit";
  });
  const blockedReports = showcaseReports.filter(
    (report) => getShowcaseReportQuality(report).readiness === "owner-gated",
  );
  const activeReport = showcaseReports.find((report) => report.id === 6);
  const activeQuality = activeReport ? getShowcaseReportQuality(activeReport) : null;

  return (
    <article className="review-page">
      <header className="review-hero">
        <div>
          <p className="review-kicker">Researcher review desk</p>
          <h1>Audit the evidence before trusting the claim.</h1>
          <p>
            This route is for economists, statisticians, operations staff, and
            reviewers who want to check whether a report has a real public-data
            spine. It foregrounds the question, the files, the caveats, and the
            blocked claim gates.
          </p>
          <div className="review-hero-actions">
            <Link href="/showcase/air-monitoring-observability">
              Inspect featured report
            </Link>
            <Link href="/showcase">Browse evidence library</Link>
          </div>
        </div>
        <aside className="review-hero-panel" aria-label="Current review status">
          <span>Current flagship</span>
          <strong>Air-monitoring observability</strong>
          <p>
            The package is strong enough to inspect, but still blocks station
            coverage, people-served, and monitor-grade claims until station
            identity and grade evidence close.
          </p>
        </aside>
      </header>

      <section className="review-stat-grid" aria-label="Evidence library status">
        <div>
          <span>Report surfaces</span>
          <strong>{showcaseReports.length}</strong>
          <p>Reader-facing pages with evidence links and caveats.</p>
        </div>
        <div>
          <span>Evidence packages</span>
          <strong>{evidencePackages.length}</strong>
          <p>Routes with mature evidence packets or audit-grade source walls.</p>
        </div>
        <div>
          <span>Owner-gated items</span>
          <strong>{blockedReports.length}</strong>
          <p>Publicly visible, but awaiting owner-only access or validation.</p>
        </div>
      </section>

      <section className="review-section">
        <div className="review-section-head">
          <p className="review-kicker">How to read a page</p>
          <h2>Use the same four checks on every report.</h2>
        </div>
        <div className="review-step-grid">
          {reviewSteps.map((step) => (
            <div className="review-step" key={step.label}>
              <span>{step.label}</span>
              <h3>{step.title}</h3>
              <p>{step.copy}</p>
            </div>
          ))}
        </div>
      </section>

      {activeReport && activeQuality && (
        <section className="review-section review-active">
          <div className="review-section-head">
            <p className="review-kicker">Active package</p>
            <h2>{activeReport.shortTitle}</h2>
            <p>
              This package asks whether public monitor visibility, regulator
              station lists, and denominator joins can support coverage claims.
              The current answer is useful but deliberately gated: source
              reconciliation is visible, while station-radius coverage remains
              blocked.
            </p>
          </div>
          <div className="review-active-grid">
            <div>
              <span>Review stage</span>
              <strong>{readinessLabel[activeQuality.readiness]}</strong>
              <p>{shortText(activeQuality.qaSummary)}</p>
            </div>
            <div>
              <span>Publication gap</span>
              <strong>Claim remains gated</strong>
              <p>{shortText(activeQuality.publicationGap)}</p>
            </div>
            <div>
              <span>Next useful check</span>
              <strong>Close one blocked row</strong>
              <p>{shortText(activeQuality.nextUpgrade)}</p>
            </div>
          </div>
        </section>
      )}

      <section className="review-section">
        <div className="review-section-head">
          <p className="review-kicker">Start points</p>
          <h2>Open the path that matches your review depth.</h2>
        </div>
        <div className="review-link-grid">
          {quickLinks.map((item) => (
            <Link href={item.href} className="review-link-card" key={item.href}>
              <span>{item.label}</span>
              <strong>{item.title}</strong>
              <p>{item.copy}</p>
            </Link>
          ))}
        </div>
      </section>

      <section className="review-section">
        <div className="review-section-head">
          <p className="review-kicker">Evidence library</p>
          <h2>Current reports by review stage.</h2>
        </div>
        <div className="review-report-table">
          {showcaseReports.map((report) => {
            const quality = getShowcaseReportQuality(report);
            return (
              <Link href={report.href} className="review-report-row" key={report.href}>
                <span>{String(report.id).padStart(2, "0")}</span>
                <strong>{report.shortTitle}</strong>
                <em>{readinessLabel[quality.readiness]}</em>
                <p>{shortText(quality.publicationGap, 210)}</p>
              </Link>
            );
          })}
        </div>
      </section>
    </article>
  );
}
