/**
 * Home.tsx — visual-first thumbnail gallery.
 *
 * Per `research/visual-first-refactor.md` (2026-05-19), the home page
 * is a grid of 16:9 hero cards. Each card is a click-through to the
 * program's topic page, with:
 *   - the program's hero PNG (1600×900, sha256-pinned by sync-evidence)
 *     when the program has rendered a thumbnail
 *   - an honest placeholder card when it has not (programs still in
 *     Stage 1 framing render the placeholder so the gallery cannot
 *     pretend they're finished — §18.2 honest labeling)
 *
 * Data: one fetch to /programs/heroes.json which the sync-evidence
 * script aggregates from each program's manifest.json.
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { programs } from "../data/programs";
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

  // Sort programs: PR first, then SR/PP/H/Ret. Within a status group,
  // programs with a rendered hero come first, then placeholders.
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

  return (
    <div className="home-page">
      {/* Hero strip */}
      <section className="home-hero">
        <p className="kicker kicker-crimson home-kicker">
          Measurement-gap research
        </p>
        <h1 className="home-title">ADB AI Research</h1>
        <p className="home-lede measure-wide-copy">
          Public-data measurement-gap research on Asian Development Bank
          developing member economies. Every program produces a single
          headline visual you can verify in one image. AI-attested under a
          written constitution. Open code, open data.
        </p>
        <div className="home-meta">
          <span>
            {totalPrograms} programs · {loaded ? heroesRendered : "…"} with
            rendered hero
          </span>
          <span>·</span>
          <Link to="/about" className="token-link">
            About
          </Link>
          <span>·</span>
          <Link to="/docs" className="token-link">
            All documents
          </Link>
          <span>·</span>
          <Link to="/constitution" className="token-link">
            Constitution
          </Link>
          <span>·</span>
          <a
            href="https://github.com/rradofina/adb-research-reporting"
            target="_blank"
            rel="noreferrer"
            className="token-link"
          >
            GitHub →
          </a>
        </div>
      </section>

      {/* Thumbnail grid */}
      <section className="hero-grid">
        {sortedPrograms.map((p) => {
          const hero = heroIndex[p.slug] || null;
          const maturity = p.status as Maturity;
          const heroPng = hero
            ? `/programs/${p.slug}/${hero.png}`
            : null;
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
                <h3 className="hero-card-title">
                  {hero?.title || p.title}
                </h3>
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
      </section>

      {/* Footer note */}
      <section className="home-footer-note">
        <p>
          Every empirical number on this site traces to a committed script
          and a public source. Every hero visual carries an{" "}
          <code className="inline-code-token">attestation_chain</code>{" "}
          burned into the image so a screenshot retains the labeling. See{" "}
          <Link to="/about" className="token-link">
            About
          </Link>{" "}
          for the constitutional model and what AI-first attestation means
          and does not mean.
        </p>
      </section>
    </div>
  );
}
