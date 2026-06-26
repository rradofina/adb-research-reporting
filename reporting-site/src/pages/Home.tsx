/**
 * Home.tsx - reader-facing research portal.
 *
 * The homepage leads with the public value proposition and topic pathways.
 * Dense evidence, readiness labels, and archive surfaces remain available
 * lower on the page for reviewers who need the full research trail.
 */
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { programs } from "../data/programs";
import {
  getShowcaseReportQuality,
  showcaseReports,
  verifiedShowcaseReports,
} from "../data/showcaseReports";
import { MaturityChip, maturityLabels, type Maturity } from "../lib/claimTiers";
import type { HeroVisual } from "../lib/evidence";

interface HeroIndexEntry {
  slug: string;
  hero: HeroVisual | null;
}

interface HeroIndex {
  generated_at: string;
  heroes: HeroIndexEntry[];
}

interface ReaderTopicSpec {
  reportId: number;
  label: string;
  audience: string;
  hook: string;
  evidence: string;
  tone: "blue" | "green" | "red" | "gold";
  featured?: boolean;
}

const ORDER: Maturity[] = ["PR", "SR", "PP", "H", "Ret"];

const readerTopicSpecs: ReaderTopicSpec[] = [
  {
    reportId: 6,
    label: "Current flagship",
    audience: "Air quality and observability",
    hook: "Where public monitor maps are visible, and where station-coverage claims still fail.",
    evidence: "OpenAQ, regulator portals, station identity, monitor-grade, GHSL, and ACAG gates.",
    tone: "blue",
    featured: true,
  },
  {
    reportId: 4,
    label: "Service delivery",
    audience: "Public service data quality",
    hook: "What happens when the official registry and the public map disagree.",
    evidence: "Facility registries, OSM, Open Buildings, row-level review ledgers, and human-gated handoff files.",
    tone: "red",
  },
  {
    reportId: 5,
    label: "Household finance",
    audience: "Remittance corridor costs",
    hook: "How corridor rankings change when prices are weighted by observed flow exposure.",
    evidence: "World Bank RPW, KNOMAD bilateral flows, WDI remittance dependence, and sensitivity checks.",
    tone: "green",
  },
  {
    reportId: 8,
    label: "Disaster risk",
    audience: "Recovery lag evidence",
    hook: "Why disaster burden screens need event geography before recovery language is used.",
    evidence: "EM-DAT, GDIS geocoded events, Black Marble metadata, and recovery-source readiness.",
    tone: "gold",
  },
  {
    reportId: 3,
    label: "Shock response",
    audience: "Payment rails after disasters",
    hook: "Where account ownership, payment use, and social-protection coverage diverge.",
    evidence: "EM-DAT, Findex, ASPIRE, WDI, and a public rail-observability ledger.",
    tone: "green",
  },
  {
    reportId: 7,
    label: "Access maps",
    audience: "Health facility map completeness",
    hook: "When a service-access map is really measuring whether facilities are mapped.",
    evidence: "OSM, official clinical registries, WorldPop, Cambodia HDX/MoH/OCHA sources, and PSDQ context.",
    tone: "blue",
  },
  {
    reportId: 14,
    label: "Climate and labor",
    audience: "Heat, air pollution, and workdays",
    hook: "How cap choice and worker denominators change what a workday-loss proxy can say.",
    evidence: "WDI PM2.5, WDI employment denominators, CCKP heat metadata, and source-readiness walls.",
    tone: "red",
  },
  {
    reportId: 20,
    label: "Education",
    audience: "School heat disruption",
    hook: "Why a national heat screen is not yet a school-day disruption measure.",
    evidence: "WDI, CCKP, OSM school counts, UNICEF source pointers, and school-day join gates.",
    tone: "gold",
  },
  {
    reportId: 17,
    label: "Water and crops",
    audience: "Water stress denominator checks",
    hook: "Where national water-stress rankings change after the denominator is repaired.",
    evidence: "WDI, AQUASTAT, FAOSTAT crop-mix rows, and basin-level non-claims.",
    tone: "blue",
  },
];

function statusRank(status: Maturity): number {
  const i = ORDER.indexOf(status);
  return i < 0 ? ORDER.length : i;
}

export default function Home() {
  const [heroIndex, setHeroIndex] = useState<Record<string, HeroVisual | null>>({});
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    fetch("/programs/heroes.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((data: HeroIndex | null) => {
        if (!data) {
          setLoaded(true);
          return;
        }
        const map: Record<string, HeroVisual | null> = {};
        for (const entry of data.heroes) {
          map[entry.slug] = entry.hero;
        }
        setHeroIndex(map);
        setLoaded(true);
      })
      .catch(() => setLoaded(true));
  }, []);

  const reportById = useMemo(
    () => new Map(showcaseReports.map((report) => [report.id, report])),
    [],
  );

  const readerTopics = readerTopicSpecs
    .map((topic) => {
      const report = reportById.get(topic.reportId);
      return report ? { ...topic, report, quality: getShowcaseReportQuality(report) } : null;
    })
    .filter((topic): topic is NonNullable<typeof topic> => Boolean(topic));

  const sortedPrograms = [...programs].sort((a, b) => {
    const sa = statusRank(a.status as Maturity);
    const sb = statusRank(b.status as Maturity);
    if (sa !== sb) return sa - sb;
    const ha = heroIndex[a.slug] ? 0 : 1;
    const hb = heroIndex[b.slug] ? 0 : 1;
    if (ha !== hb) return ha - hb;
    return a.id - b.id;
  });

  const heroesRendered = Object.values(heroIndex).filter(Boolean).length;
  const verifiedCount = verifiedShowcaseReports.length;
  const l3CandidateCount = showcaseReports.filter(
    (report) => getShowcaseReportQuality(report).readiness === "l3-candidate",
  ).length;

  return (
    <div className="home-page home-portal">
      <section className="home-portal-hero" aria-labelledby="home-portal-title">
        <div className="home-portal-hero-inner">
          <p className="home-portal-kicker">Public-data measurement research</p>
          <h1 id="home-portal-title">ADB AI Research</h1>
          <p className="home-portal-lede">
            Evidence packages for policy questions where the first problem is not the model, but whether the public data are complete enough to support the claim.
          </p>
          <div className="home-portal-actions" aria-label="Primary paths">
            <Link to="/showcase/air-monitoring-observability">Read the air-monitoring flagship</Link>
            <a href="#topics">Browse topics</a>
          </div>
          <div className="home-portal-readout" aria-label="Research bench status">
            <span>
              <strong>{verifiedCount}</strong>
              verified report routes
            </span>
            <span>
              <strong>{l3CandidateCount}</strong>
              L3 candidates
            </span>
            <span>
              <strong>{loaded ? heroesRendered : "..."}</strong>
              program visuals
            </span>
          </div>
        </div>
      </section>

      <section className="home-topic-section" id="topics" aria-labelledby="home-topic-title">
        <div className="home-section-head home-topic-head">
          <p className="kicker">Topics</p>
          <h2 id="home-topic-title">Start with the measurement problem.</h2>
          <p>
            Each topic opens with the policy question, the public-source gap, and the evidence that is already reproducible. Stronger claims stay behind the gates until the data support them.
          </p>
        </div>

        <div className="home-topic-grid">
          {readerTopics.map((topic) => (
            <Link
              to={topic.report.href}
              className={`home-topic-card home-topic-card-${topic.tone}${topic.featured ? " home-topic-card-featured" : ""}`}
              key={topic.report.href}
            >
              <span className="home-topic-label">{topic.label}</span>
              <h3>{topic.audience}</h3>
              <p>{topic.hook}</p>
              <span className="home-topic-evidence">{topic.evidence}</span>
              <span className="home-topic-status">{topic.quality.readinessLabel}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="home-report-section" aria-labelledby="home-report-batch">
        <div className="home-section-head">
          <p className="kicker">Report bench</p>
          <h2 id="home-report-batch">The full queue stays visible.</h2>
          <p>
            The report bench keeps the audit trail close to the public story: every route links back to a committed artifact, source note, and next evidence upgrade.
          </p>
        </div>
        <div className="home-report-list">
          {showcaseReports.map((report) => {
            const quality = getShowcaseReportQuality(report);
            return (
              <Link to={report.href} className="home-report-row" key={report.href}>
                <span>{String(report.id).padStart(2, "0")}</span>
                <strong>{report.shortTitle}</strong>
                <em>{quality.readinessLabel}</em>
                <p>{report.deck}</p>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="home-standard-band" aria-labelledby="home-standard-title">
        <div>
          <p className="kicker">Research standard</p>
          <h2 id="home-standard-title">The public surface makes the claim smaller before it makes it useful.</h2>
        </div>
        <div className="home-standard-list">
          <p>
            No empirical number on this site comes from model memory. The path from claim to script, generated artifact, public source, and status note remains available from the evidence pages.
          </p>
          <p>
            Visuals are used to show source disagreement, missing denominators, sensitivity, and claim gates. They are not treated as proof of publication readiness.
          </p>
        </div>
      </section>

      <section className="home-program-section" aria-labelledby="home-program-archive">
        <div className="home-section-head">
          <p className="kicker">Program archive</p>
          <h2 id="home-program-archive">Program pages carry the deeper evidence trail.</h2>
          <p>
            The archive preserves maturity labels, attestation chips, generated hero visuals, and reproduction links for the broader research factory.
          </p>
          <div className="home-meta">
            <span>
              {programs.length} programs - {loaded ? heroesRendered : "..."} with rendered hero visuals
            </span>
            <span>-</span>
            <Link to="/about" className="token-link">
              About
            </Link>
            <span>-</span>
            <Link to="/docs" className="token-link">
              Documents
            </Link>
            <span>-</span>
            <a
              href="https://github.com/rradofina/adb-research-reporting"
              target="_blank"
              rel="noreferrer"
              className="token-link"
            >
              GitHub
            </a>
          </div>
        </div>

        <div className="hero-grid home-program-grid">
          {sortedPrograms.map((p) => {
            const hero = heroIndex[p.slug] || null;
            const maturity = p.status as Maturity;
            const heroPng = hero ? `/programs/${p.slug}/${hero.png}` : null;
            return (
              <Link
                key={p.slug}
                to={`/${p.slug}`}
                className={`hero-card${hero ? "" : " hero-card-empty"}`}
              >
                <div className="hero-card-thumb">
                  {hero && heroPng ? (
                    <img
                      src={heroPng}
                      alt={hero.title}
                      loading="lazy"
                      width={hero.dimensions?.width || 1600}
                      height={hero.dimensions?.height || 900}
                    />
                  ) : (
                    <div className="hero-card-placeholder">
                      <span className="hero-card-placeholder-label">Hero pending</span>
                      <span className="hero-card-placeholder-status">{maturityLabels[maturity]}</span>
                    </div>
                  )}
                  <div className="hero-card-chips">
                    <MaturityChip status={maturity} />
                    {hero && (
                      <span
                        className="attestation-chip"
                        title="attestation_chain set per CONSTITUTION.md section 18.2"
                      >
                        {hero.attestation_chain}
                      </span>
                    )}
                  </div>
                </div>
                <div className="hero-card-body">
                  <h3 className="hero-card-title">{hero?.title || p.title}</h3>
                  <p className="hero-card-caption">{hero?.caption || p.summary}</p>
                  {hero?.headline_number && (
                    <p className="hero-card-headline-number">{hero.headline_number}</p>
                  )}
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="home-footer-note">
        <p>
          The homepage is a publication surface, not a maturity gate. The active board remains{" "}
          <Link to="/status" className="token-link">
            research/STATUS.md
          </Link>
          ; program labels remain governed by the Constitution and factory loop.
        </p>
      </section>
    </div>
  );
}
