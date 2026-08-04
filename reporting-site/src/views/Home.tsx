"use client";

/**
 * Home.tsx - institutional research portal.
 *
 * The homepage is organized for external readers: what the lab studies,
 * which evidence pages are ready to inspect, and where the audit trail lives.
 */
import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { programs } from "../data/programs";
import {
  ISSUE_CLOSURE_AS_OF,
  issueClosureDeck,
  issueComputedCount,
  issueHeldBackCount,
  issueHoldBackNotes,
  issueStatusCards,
  issueTotal,
} from "../data/issueClosure";
import {
  getShowcaseReportQuality,
  showcaseReports,
  type ShowcaseReadiness,
} from "../data/showcaseReports";
import type { Maturity } from "../lib/claimTiers";
import type { HeroVisual } from "../lib/evidence";
import "./Home.css";

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
  question: string;
  summary: string;
  findingClaim?: string;
  findingLimit?: string;
  findingRank?: number;
  tone: "blue" | "green" | "red" | "gold";
  programSlug?: string;
}

const ORDER: Maturity[] = ["PR", "SR", "PP", "H", "Ret"];

const publicReportLabels: Record<ShowcaseReadiness, string> = {
  prototype: "Prototype",
  "l3-candidate": "Evidence package",
  "evidence-audit": "Evidence audit",
  "portfolio-proof": "Portfolio proof",
  "owner-gated": "Needs validation",
};

const publicProgramLabels: Record<Maturity, string> = {
  H: "In development",
  PP: "Pipeline prepared",
  SR: "Screening result",
  PR: "Publication-ready",
  Ret: "Retired",
};

const readerTopicSpecs: ReaderTopicSpec[] = [
  {
    reportId: 6,
    label: "Air quality",
    question: "Can public monitor maps support station-coverage claims?",
    summary:
      "OpenAQ rows, regulator portals, station identity checks, and denominator gates are shown before any coverage language is allowed.",
    findingClaim:
      "Across 8 economy routes, public station, method, dashboard, and denominator records still leave 0 validated same-station QA rows and 0 allowed coverage-claim rows.",
    findingLimit:
      "This is an observability finding, not proof that the monitors are uncalibrated.",
    findingRank: 1,
    tone: "blue",
    programSlug: "air-monitoring",
  },
  {
    reportId: 4,
    label: "Service delivery",
    question: "Which facilities disappear between a registry and a public map?",
    summary:
      "Registry-map disagreement is reviewed row by row before public access maps are trusted.",
    findingClaim:
      "Bangladesh joins 572 DGHS upazila rows and 28,166 active facilities to 3,212 OSM health features, but source-owner repair still ends at 39 wall rows and 0 AI-actionable closures.",
    findingLimit:
      "The result shows public registry-map disagreement, not corrected facility locations.",
    findingRank: 2,
    tone: "red",
    programSlug: "public-service-data-quality",
  },
  {
    reportId: 5,
    label: "Household finance",
    question: "Do corridor costs look different after flow weighting?",
    summary:
      "Remittance prices are checked against observed corridor-flow exposure instead of equal-count averages.",
    findingClaim:
      "Tonga reaches 42.6% of GDP in remittance dependence, so corridor prices are re-read with public bilateral-flow weights instead of equal-count averages.",
    findingLimit:
      "The page measures public corridor-cost exposure, not household resilience.",
    findingRank: 3,
    tone: "green",
    programSlug: "remittance-resilience",
  },
  {
    reportId: 10,
    label: "Migration",
    question: "What changes when emigrant stock is read by population share?",
    summary:
      "UN DESA emigrant stocks are divided by WDI origin population, then checked against UNHCR forced-displacement corridors.",
    findingClaim:
      "Afghanistan is the exception in the denominator switch: UNHCR forced-displacement stock equals 81.7% of its UN DESA emigrant stock.",
    findingLimit:
      "This does not classify labor, family, student, or temporary-work migration.",
    findingRank: 4,
    tone: "blue",
    programSlug: "migration-displacement-signals",
  },
  {
    reportId: 9,
    label: "Energy",
    question: "Can single-fuel generation screens become reliability claims?",
    summary:
      "Generation-fuel concentration is crosswalked to public outage and electricity-service proxies before reliability language is allowed.",
    findingClaim:
      "Public reliability proxies exist for 38 DMCs and overlap 22 generation-ranked rows, but the page stops at source readiness.",
    findingLimit:
      "This is not a power-reliability ranking and does not observe outage events.",
    findingRank: 5,
    tone: "gold",
    programSlug: "grid-reliability-heat",
  },
  {
    reportId: 8,
    label: "Disaster risk",
    question: "When does a disaster metric fail its own test?",
    summary:
      "EM-DAT burden measures are compared before recovery-lag language is reused.",
    tone: "gold",
    programSlug: "disaster-recovery-lag",
  },
  {
    reportId: 3,
    label: "Shock response",
    question: "Is account ownership enough to describe payment rails?",
    summary:
      "Disaster exposure is compared with payment use and social-protection observability.",
    tone: "green",
    programSlug: "social-protection-shock-coverage",
  },
  {
    reportId: 7,
    label: "Access maps",
    question: "Is an access map measuring service access or map completeness?",
    summary:
      "OSM health amenities are checked against official denominator evidence before interpretation.",
    tone: "blue",
    programSlug: "access-services",
  },
  {
    reportId: 14,
    label: "Climate and labor",
    question: "What can a heat-and-work proxy honestly say?",
    summary:
      "Worker denominators, cap choice, and heat-source readiness are separated from workday-loss claims.",
    tone: "red",
    programSlug: "climate-health-workdays",
  },
  {
    reportId: 20,
    label: "Education",
    question: "When is a national heat screen not a school-day measure?",
    summary:
      "School heat evidence stays at source-readiness level until school calendars and locations are joined.",
    tone: "gold",
    programSlug: "school-heat-disruption",
  },
  {
    reportId: 17,
    label: "Water and crops",
    question: "How much of a water-stress result is the denominator?",
    summary:
      "National water-stress rows are checked against available-water and crop-mix source limits.",
    tone: "blue",
    programSlug: "water-stress-crop-diversification",
  },
];

function statusRank(status: Maturity): number {
  const i = ORDER.indexOf(status);
  return i < 0 ? ORDER.length : i;
}

function shortText(value: string, limit = 170) {
  if (value.length <= limit) return value;
  const trimmed = value.slice(0, limit).replace(/\s+\S*$/, "");
  return `${trimmed}...`;
}

function reportStageLabel(readiness: ShowcaseReadiness) {
  return publicReportLabels[readiness];
}

function heroPath(slug: string | undefined, hero: HeroVisual | null | undefined) {
  if (!slug || !hero) return null;
  return `/programs/${slug}/${hero.png}`;
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
      if (!report) return null;
      const quality = getShowcaseReportQuality(report);
      return {
        ...topic,
        report,
        quality,
        publicStage: topic.programSlug
          ? publicProgramLabels[programs.find((program) => program.slug === topic.programSlug)?.status || "H"]
          : reportStageLabel(quality.readiness),
        href: topic.programSlug ? `/${topic.programSlug}` : report.href,
        hero: topic.programSlug ? heroIndex[topic.programSlug] : null,
      };
    })
    .filter((topic): topic is NonNullable<typeof topic> => Boolean(topic));

  const findingTopics = readerTopics
    .filter((topic) => typeof topic.findingRank === "number")
    .sort((a, b) => (a.findingRank ?? 99) - (b.findingRank ?? 99))
    .slice(0, 5);
  const findingTopicHrefs = new Set(findingTopics.map((topic) => topic.href));
  const standardTopics = readerTopics.filter((topic) => !findingTopicHrefs.has(topic.href));
  const primaryFinding = findingTopics[0] ?? readerTopics[0];

  const sortedPrograms = [...programs].sort((a, b) => {
    const sa = statusRank(a.status);
    const sb = statusRank(b.status);
    if (sa !== sb) return sa - sb;
    const ha = heroIndex[a.slug] ? 0 : 1;
    const hb = heroIndex[b.slug] ? 0 : 1;
    if (ha !== hb) return ha - hb;
    return a.id - b.id;
  });

  const visualPrograms = loaded
    ? sortedPrograms.filter((program) => Boolean(heroIndex[program.slug]))
    : [];

  return (
    <div className="home-page home-institutional">
      <section className="home-hero" aria-labelledby="home-title">
        <div className="home-hero-media" aria-hidden="true" />
        <div className="home-hero-content">
          <p className="home-eyebrow">Research findings</p>
          <h1 id="home-title">What public data can and cannot yet prove</h1>
          <p className="home-lede">
            Start with the strongest public-source results. Each card states
            the finding a practitioner can retell, what the evidence still
            cannot support, and where to open the full paper and packet.
          </p>
          <div className="home-actions" aria-label="Primary paths">
            <Link href={primaryFinding?.href ?? "/research"}>
              Open lead finding
            </Link>
            <Link href="/research">Browse all research</Link>
          </div>
          <div className="home-assurance" aria-label="Research standard">
            <span>Maturity labels visible</span>
            <span>AI-first attestation</span>
            <span>Generated visuals only</span>
            <span>Audit trail linked</span>
          </div>
        </div>
        <div className="home-hero-findings" aria-label="Featured research findings">
          {findingTopics.map((topic, index) => {
            // Only the primary card is large enough for a generated chart to
            // stay legible; the secondary cards read better as typography.
            const image = index === 0 ? heroPath(topic.programSlug, topic.hero) : null;
            const attestation = topic.hero?.attestation_chain || "ai-first";
            return (
              <Link
                href={topic.href}
                className={`home-finding-card${index === 0 ? " home-finding-card-primary" : ""}${image ? "" : " home-finding-card-noimage"}`}
                key={topic.href}
              >
                {image && (
                  <img
                    src={image}
                    alt={topic.hero?.title || topic.question}
                    loading={index === 0 ? "eager" : "lazy"}
                    width={topic.hero?.dimensions?.width || 1600}
                    height={topic.hero?.dimensions?.height || 900}
                  />
                )}
                <div className="home-finding-copy">
                  <span>{topic.publicStage} · {attestation}</span>
                  <h3>{topic.label}</h3>
                  <p>{topic.findingClaim ?? topic.report.audit?.finding ?? topic.report.deck}</p>
                  <em>{topic.findingLimit ?? topic.report.audit?.nonClaim ?? topic.quality.publicationGap}</em>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="home-issue-closure" aria-labelledby="home-issue-closure-title">
        <div className="home-issue-closure-copy">
          <p className="home-section-kicker">Program register · {ISSUE_CLOSURE_AS_OF}</p>
          <h2 id="home-issue-closure-title">All {issueTotal} registered programs carry one clear finish label.</h2>
          <p>
            {issueClosureDeck} Finished papers stay separate from screens still
            in progress, so the catalogue never implies that every registered
            idea is already ready to cite.
          </p>
        </div>
        <div className="home-issue-status-grid" aria-label="Current issue classification">
          {issueStatusCards.map((card) => (
            <div className="home-issue-status" key={card.key}>
              <span>{card.label}</span>
              <strong>{card.count}</strong>
            </div>
          ))}
        </div>
        <div className="home-issue-notes">
          <div>
            <span>{issueComputedCount} computed outputs</span>
            <span>{issueHeldBackCount} held back</span>
          </div>
          <ul>
            {issueHoldBackNotes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
          <Link href="/briefs">Open all briefs</Link>
        </div>
      </section>

      <section className="home-review-band" aria-labelledby="home-review-title">
        <div>
          <p className="home-section-kicker">For reviewers</p>
          <h2 id="home-review-title">Check the claim gate before the chart.</h2>
          <p>
            The site is built so a reader can move from a public-facing visual
            into the generated files, method caveats, source records, and
            blocked claims without trusting the page by eye.
          </p>
        </div>
        <div className="home-review-actions">
          <Link href="/review">Open review desk</Link>
          <Link href="/versions">Source ledger</Link>
          <Link href="/factory">Factory rules</Link>
        </div>
      </section>

      <section className="home-browse-section" id="topics" aria-labelledby="home-topic-title">
        <div className="home-section-head">
          <p className="home-section-kicker">Research and publications</p>
          <h2 id="home-topic-title">Browse the remaining research questions.</h2>
          <p>
            The front door now carries the strongest findings. This section
            keeps the rest of the queue accessible by question, with stronger
            claims still gated until the data can support them.
          </p>
        </div>

        <div className="home-topic-grid">
          {standardTopics.map((topic) => (
            <Link href={topic.href}
              className={`home-topic-card home-topic-card-${topic.tone}`}
              key={topic.href}
            >
              <span>{topic.label}</span>
              <h3>{topic.question}</h3>
              <b>{topic.publicStage}</b>
            </Link>
          ))}
        </div>
      </section>

      <section className="home-library-section" id="evidence" aria-labelledby="home-library-title">
        <div className="home-section-head">
          <p className="home-section-kicker">Explorations and audits</p>
          <h2 id="home-library-title">Method experiments and evidence audits stay available without being mistaken for full research papers.</h2>
          <p>
            The visible pages keep internal maturity codes out of the way while
            preserving the route to scripts, generated files, source notes, and
            governance documents.
          </p>
        </div>

        <details className="home-library-details">
          <summary>
            <span>All evidence reports</span>
            <b>{showcaseReports.length}</b>
          </summary>
          <div className="home-report-list">
            {showcaseReports.map((report) => {
              const quality = getShowcaseReportQuality(report);
              return (
                <Link href={report.href} className="home-report-row" key={report.href}>
                  <span>{String(report.id).padStart(2, "0")}</span>
                  <strong>{report.shortTitle}</strong>
                  <em>{reportStageLabel(quality.readiness)}</em>
                  <p>{shortText(report.deck)}</p>
                </Link>
              );
            })}
          </div>
        </details>

        <details className="home-library-details">
          <summary>
            <span>Program pages with generated visuals</span>
            <b>{loaded ? visualPrograms.length : "..."}</b>
          </summary>
          {loaded ? (
            <div className="home-visual-grid">
              {visualPrograms.map((program) => {
                const hero = heroIndex[program.slug];
                const image = heroPath(program.slug, hero);
                if (!hero || !image) return null;
                return (
                  <Link key={program.slug} href={`/${program.slug}`} className="home-visual-card">
                    <img
                      src={image}
                      alt={hero.title}
                      loading="lazy"
                      width={hero.dimensions?.width || 1600}
                      height={hero.dimensions?.height || 900}
                    />
                    <div>
                      <span>{publicProgramLabels[program.status]}</span>
                      <h3>{hero.title}</h3>
                      <p>{shortText(hero.caption || program.summary, 120)}</p>
                    </div>
                  </Link>
                );
              })}
            </div>
          ) : (
            <p className="home-loading-note">Loading generated program visuals...</p>
          )}
        </details>

        <div className="home-standard-note">
          <p>
            The homepage is a publication surface, not a maturity gate. Program
            labels remain governed by the Constitution and factory loop; the
            active board remains{" "}
            <Link href="/status" className="token-link">
              research/STATUS.md
            </Link>
            .
          </p>
        </div>
      </section>
    </div>
  );
}
