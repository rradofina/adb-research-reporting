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
      <section className="home-hero pb-10 mb-12 border-b border-ink-200">
        <h1 className="text-4xl md:text-5xl font-semibold tracking-tight leading-tight">
          ADB AI Research
        </h1>
        <p className="mt-5 text-lg text-ink-600 leading-relaxed max-w-[1050px]">
          Public-data measurement-gap research on Asian Development Bank
          developing member economies. AI-attested under a written
          constitution. Open code, open data.
        </p>
        <div className="mt-6 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs uppercase tracking-[0.18em] text-ink-500">
          <span>17 topics in the register</span>
          <span>·</span>
          <span>1 active flagship</span>
          <span>·</span>
          <Link to="/about" className="underline underline-offset-4 hover:text-ink-900">
            About
          </Link>
          <span>·</span>
          <Link to="/docs" className="underline underline-offset-4 hover:text-ink-900">
            All documents
          </Link>
          <span>·</span>
          <Link to="/constitution" className="underline underline-offset-4 hover:text-ink-900">
            Constitution
          </Link>
          <span>·</span>
          <a
            href="https://github.com/rradofina/adb-research-reporting"
            target="_blank"
            rel="noreferrer"
            className="underline underline-offset-4 hover:text-ink-900"
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
          <section key={key} className="home-group mb-12">
            <h2 className="text-sm uppercase tracking-[0.2em] text-ink-500">
              {SECTION_LABEL[key]}
            </h2>
            <p className="mt-2 text-sm text-ink-600 max-w-[1050px]">{SECTION_DESC[key]}</p>
            <ul className="mt-6 space-y-1">
              {list.map((p) => (
                <li key={p.slug}>
                  <Link
                    to={`/${p.slug}`}
                    className="topic-card block group py-5 px-4 -mx-4 rounded transition-colors hover:bg-paper-50"
                  >
                    <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                      <h3 className="text-lg font-semibold text-ink-900 group-hover:text-crimson transition-colors">
                        {p.title}
                      </h3>
                      <MaturityChip status={p.status as Maturity} />
                    </div>
                    <p className="mt-2 text-sm text-ink-600 leading-relaxed max-w-none">
                      {p.summary}
                    </p>
                    {p.note && (
                      <p className="mt-2 text-xs text-ink-500 italic max-w-none">{p.note}</p>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        );
      })}

      {/* Footer note */}
      <section className="mt-16 pt-8 border-t border-ink-200 text-sm text-ink-600">
        <p className="leading-relaxed">
          Every empirical number on this site traces to a committed script
          and a public source. Every artifact carries an{" "}
          <code className="font-mono text-xs">attestation_chain</code> field
          recording which review path produced it. See{" "}
          <Link to="/about" className="underline underline-offset-4">
            About
          </Link>{" "}
          for the constitutional model and what AI-first attestation means
          and does not mean.
        </p>
      </section>
    </div>
  );
}
