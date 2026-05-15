/**
 * Home.tsx — simple title + topic list.
 *
 * Replaces the previous editorial multi-section home with a clean
 * one-screen orientation: site title, one-sentence description, list
 * of topics. Each topic links to /{slug} for the unified topic page.
 */
import { Link } from "react-router-dom";
import { programs } from "../data/programs";
import { MaturityChip, type Maturity } from "../lib/claimTiers";

const ORDER: Maturity[] = ["PR", "SR", "PP", "H", "Ret"];

const SECTION_LABEL: Record<Maturity, string> = {
  PR: "Active flagship",
  SR: "Screening result · awaiting re-evaluation",
  PP: "Prepared pipelines",
  H: "Open hypotheses",
  Ret: "Retired",
};

const SECTION_DESC: Record<Maturity, string> = {
  PR: "Publication-Ready under §18 ai-first attestation. The current focused work.",
  SR: "Earned the SR label in an earlier sprint; awaits re-evaluation under the new program loop.",
  PP: "Prepared pipelines waiting for the new program loop to run end-to-end. Source plan and scaffolding committed.",
  H: "Hypothesis-stage. README and literature scan committed; no pipeline yet.",
  Ret: "Retired programs.",
};

export default function Home() {
  // Group programs by maturity, with PR first.
  const grouped: Record<Maturity, typeof programs> = {} as any;
  for (const p of programs) {
    const k = p.status as Maturity;
    if (!grouped[k]) grouped[k] = [] as any;
    grouped[k].push(p);
  }

  return (
    <div className="home-page">
      {/* Hero */}
      <section className="home-hero">
        <h1 className="home-title">
          ADB AI Research
        </h1>
        <p className="home-lede measure-wide-copy">
          Public-data measurement-gap research on Asian Development Bank
          developing member economies. AI-attested under a written
          constitution. Open code, open data.
        </p>
        <div className="home-meta">
          <span>17 topics in the register</span>
          <span>·</span>
          <span>1 active flagship</span>
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

      {/* Topic groups */}
      {ORDER.map((key) => {
        const list = grouped[key];
        if (!list || list.length === 0) return null;
        return (
          <section key={key} className="home-group">
            <h2 className="section-label">
              {SECTION_LABEL[key]}
            </h2>
            <p className="section-desc measure-wide-copy">{SECTION_DESC[key]}</p>
            <ul className="topic-list">
              {list.map((p) => (
                <li key={p.slug}>
                  <Link
                    to={`/${p.slug}`}
                    className="topic-card"
                  >
                    <div className="topic-title-row">
                      <h3 className="topic-title">
                        {p.title}
                      </h3>
                      <MaturityChip status={p.status as Maturity} />
                    </div>
                    <p className="topic-copy measure-fill">
                      {p.summary}
                    </p>
                    {p.note && (
                      <p className="topic-note measure-fill">{p.note}</p>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        );
      })}

      {/* Footer note */}
      <section className="home-footer-note">
        <p>
          Every empirical number on this site traces to a committed script
          and a public source. Every artifact carries an{" "}
          <code className="inline-code-token">attestation_chain</code> field
          recording which review path produced it. See{" "}
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
