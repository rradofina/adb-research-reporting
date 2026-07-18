import {
  getShowcaseReportDepth,
  getShowcaseReportQuality,
  showcaseReports,
  type ShowcaseReadiness,
} from "../data/showcaseReports";

interface ShowcaseQualityPanelProps {
  reportId: number;
}

const publicReadinessLabel: Record<ShowcaseReadiness, string> = {
  prototype: "Prototype evidence",
  "l3-candidate": "Evidence package",
  "evidence-audit": "Evidence audit",
  "portfolio-proof": "Portfolio proof",
  "owner-gated": "Owner-gated source note",
};

export function ShowcaseQualityPanel({ reportId }: ShowcaseQualityPanelProps) {
  const report = showcaseReports.find((item) => item.id === reportId);
  if (!report) return null;

  const depth = getShowcaseReportDepth(report);
  const quality = getShowcaseReportQuality(report);

  return (
    <section className="showcase-section showcase-two-col showcase-quality-panel">
      <div className="showcase-section-copy">
        <p className="kicker kicker-crimson">Current QA stage</p>
        <h2>
          {publicReadinessLabel[quality.readiness]}: {report.shortTitle}
        </h2>
        <p>{quality.qaSummary}</p>
      </div>
      <div className="showcase-fact-list showcase-quality-facts">
        <div>
          <span>Technical stage</span>
          <strong>{quality.readinessLabel}</strong>
        </div>
        <div>
          <span>Operational use</span>
          <strong>{depth.operationalUse}</strong>
        </div>
        <div>
          <span>Falsifier</span>
          <strong>{depth.falsifier}</strong>
        </div>
        <div>
          <span>Publication gap</span>
          <strong>{quality.publicationGap}</strong>
        </div>
        <div>
          <span>Next upgrade</span>
          <strong>{quality.nextUpgrade}</strong>
        </div>
        <div>
          <span>Evidence path</span>
          <strong>{report.evidencePath}</strong>
        </div>
        <div>
          <span>Source stack</span>
          <strong>{report.sourceNote}</strong>
        </div>
      </div>
    </section>
  );
}
