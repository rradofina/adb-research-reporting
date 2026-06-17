/**
 * Home.tsx - report-first entry surface.
 *
 * The owner-directed showcase loop now needs the first page to explain the
 * evidence-led report batch before it exposes the older program thumbnail
 * archive. Program heroes remain below as the drilldown inventory.
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { programs } from "../data/programs";
import {
  getShowcaseReportDepth,
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

const ORDER: Maturity[] = ["PR", "SR", "PP", "H", "Ret"];

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
  const totalPrograms = programs.length;
  const verifiedCount = verifiedShowcaseReports.length;
  const l3CandidateCount = showcaseReports.filter(
    (report) => getShowcaseReportQuality(report).readiness === "l3-candidate",
  ).length;

  return (
    <div className="home-page home-showcase-page">
      <section className="home-showcase-hero">
        <div className="home-showcase-copy">
          <p className="kicker kicker-crimson home-kicker">
            ADB/ERDI evidence showcase
          </p>
          <h1 className="home-showcase-title">
            Reports built backward from data.
          </h1>
          <p className="home-showcase-lede">
            The report bench starts with public-source evidence, then a
            first-viewport visualization, caveats, and reproducibility links.
            Current target: a complete 20-report set, not a broad list of
            generic ideas.
          </p>
          <div className="home-showcase-actions" aria-label="Primary links">
            <Link to="/showcase">Open first report</Link>
            <Link to="/status">Research status</Link>
            <Link to="/factory">Factory rules</Link>
          </div>
        </div>
        <div className="home-showcase-panel" aria-label="Showcase status">
          <div className="home-panel-stats">
            <div>
              <span className="home-showcase-stat">{verifiedCount}</span>
              <span>screenshot-checked</span>
            </div>
            <div>
              <span className="home-showcase-stat">{l3CandidateCount}</span>
              <span>L3 candidates</span>
            </div>
            <div>
              <span className="home-showcase-stat">
                {loaded ? heroesRendered : "..."}
              </span>
              <span>archive visuals</span>
            </div>
          </div>
          <div className="home-panel-reports">
            <span className="home-panel-label">Current queue</span>
            {showcaseReports.slice(0, 4).map((report) => (
              <Link to={report.href} key={report.href}>
                <strong>
                  {String(report.id).padStart(2, "0")} {report.shortTitle}
                </strong>
                <span>{report.statusLabel}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="home-report-section" aria-labelledby="home-report-batch">
        <div className="home-section-head">
          <p className="kicker">Current report batch</p>
          <h2 id="home-report-batch">
            {showcaseReports.length} reports are shaped around evidence.
          </h2>
          <p>
            Each slot below names the question hook, the visual object, and
            the committed source path. These are prototype reports and visual
            QA surfaces; they do not promote maturity labels by themselves.
          </p>
        </div>
        <div className="home-report-grid">
          {showcaseReports.map((report) => {
            const depth = getShowcaseReportDepth(report);
            const quality = getShowcaseReportQuality(report);
            return (
              <Link to={report.href} className="home-report-card" key={report.href}>
                <span className="home-report-number">
                  {String(report.id).padStart(2, "0")}
                </span>
                <span className="home-report-status">{report.statusLabel}</span>
                <span className={`home-report-stage home-report-stage-${quality.readiness}`}>
                  {quality.readinessLabel}
                </span>
                <h3>{report.shortTitle}</h3>
                <p>{report.deck}</p>
                <dl className="home-report-facts">
                  <div>
                    <dt>Visual</dt>
                    <dd>{report.visual}</dd>
                  </div>
                  <div>
                    <dt>Operational use</dt>
                    <dd>{depth.operationalUse}</dd>
                  </div>
                  <div>
                    <dt>Falsifier</dt>
                    <dd>{depth.falsifier}</dd>
                  </div>
                  <div>
                    <dt>Next upgrade</dt>
                    <dd>{quality.nextUpgrade}</dd>
                  </div>
                  <div>
                    <dt>Evidence</dt>
                    <dd>{report.evidencePath}</dd>
                  </div>
                  <div>
                    <dt>Source stack</dt>
                    <dd>{report.sourceNote}</dd>
                  </div>
                </dl>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="home-standard-band" aria-labelledby="home-standard-title">
        <div>
          <p className="kicker">Research standard</p>
          <h2 id="home-standard-title">The site should make the claim smaller, not louder.</h2>
        </div>
        <div className="home-standard-list">
          <p>
            No empirical number on this surface comes from model memory. The
            reader should be able to drill from every report to a script,
            generated artifact, public source, and status note.
          </p>
          <p>
            Strong visuals are treated as a quality gate. They must reveal
            source disagreement, time, geography, sensitivity, or metric
            choice. They are not evidence of publication readiness.
          </p>
        </div>
      </section>

      <section className="home-program-section" aria-labelledby="home-program-archive">
        <div className="home-section-head">
          <p className="kicker">Program evidence archive</p>
          <h2 id="home-program-archive">The older topic gallery is now the drilldown layer.</h2>
          <p>
            Program cards remain available because they carry maturity labels,
            attestation chips, and generated hero visuals. The showcase reports
            above decide which pieces deserve deeper research-loop effort next.
          </p>
          <div className="home-meta">
            <span>
              {totalPrograms} programs - {loaded ? heroesRendered : "..."} with
              rendered hero visuals
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
                      <span className="hero-card-placeholder-label">
                        Hero pending
                      </span>
                      <span className="hero-card-placeholder-status">
                        {maturityLabels[maturity]}
                      </span>
                    </div>
                  )}
                  <div className="hero-card-chips">
                    <MaturityChip status={maturity} />
                    {hero && (
                      <span
                        className="attestation-chip"
                        title="attestation_chain set per CONSTITUTION.md §18.2"
                      >
                        {hero.attestation_chain}
                      </span>
                    )}
                  </div>
                </div>
                <div className="hero-card-body">
                  <h3 className="hero-card-title">{hero?.title || p.title}</h3>
                  <p className="hero-card-caption">
                    {hero?.caption || p.summary}
                  </p>
                  {hero?.headline_number && (
                    <p className="hero-card-headline-number">
                      {hero.headline_number}
                    </p>
                  )}
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="home-footer-note">
        <p>
          The homepage is a publication surface, not a maturity gate. The
          active research board remains <Link to="/status" className="token-link">research/STATUS.md</Link>;
          program labels remain governed by the Constitution and factory loop.
        </p>
      </section>
    </div>
  );
}
