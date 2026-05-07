import { Kicker, Numeral, Divider, PullQuote } from "../components/ui";
import { Link } from "react-router-dom";

const TIERS = [
  {
    n: "I",
    code: "H",
    label: "Hypothesis",
    body: "Idea, gap, proposed metric. May be AI-assisted. Not a finding.",
  },
  {
    n: "II",
    code: "PP",
    label: "Prepared pipeline",
    body: "Script, manifest, SQL exists. Ready to compute. No empirical value claimed yet.",
  },
  {
    n: "III",
    code: "SR",
    label: "Screening result",
    body: "Pipeline has run. Output is preliminary; triage only.",
  },
  {
    n: "IV",
    code: "PR",
    label: "Finished for issue",
    body: "Source retrieval, code, sensitivity, review response, and public archive complete for the stated attestation chain.",
  },
];

export default function Methods() {
  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-14">
        <div className="col-span-12 md:col-span-8">
          <Kicker variant="sage">Methods — Constitution highlights</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,5rem)] mt-3">
            How the{" "}
            <span className="display-italic" style={{ color: "var(--sage)" }}>
              work
            </span>{" "}
            gets done.
          </h1>
          <p className="lede mt-7 max-w-[60ch]">
            The Constitution at the upstream repository is the binding
            document. This page is a plain-language extract for readers; if
            anything here differs, the Constitution wins.
          </p>
        </div>
      </header>

      <Divider />

      {/* Tiers */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-16">
        <header className="col-span-12 lg:col-span-3">
          <Kicker>Claim maturity</Kicker>
          <h2 className="display-md text-[1.7rem] mt-3">Four tiers</h2>
          <p className="marginalia mt-3">
            Each transition has required artifacts. §18 AI-first work is labeled separately from human-final work.
          </p>
        </header>
        <div className="col-span-12 lg:col-span-9 grid sm:grid-cols-2 gap-px bg-[var(--rule-soft)]">
          {TIERS.map((t) => (
            <div key={t.code} className="bg-paper p-6">
              <div className="flex items-baseline gap-4">
                <span className="numeral text-2xl">{t.n}</span>
                <span className="font-mono text-xs uppercase tracking-[0.2em] text-ink-faint">{t.code}</span>
              </div>
              <h3 className="display-md text-[1.4rem] mt-2">{t.label}</h3>
              <p className="mt-3 text-ink-soft leading-relaxed">{t.body}</p>
            </div>
          ))}
        </div>
      </section>

      <Divider />

      {/* Gates */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-16">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="crimson">Gate requirements</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-9">
          <table className="data-table">
            <thead>
              <tr>
                <th>Transition</th>
                <th>Required artifacts</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="font-mono text-sm whitespace-nowrap">H → PP</td>
                <td>literature.md (systematic Tier-A/B/C scan); scoring ≥ 18; first testable claim; falsification condition</td>
              </tr>
              <tr>
                <td className="font-mono text-sm whitespace-nowrap">PP → SR</td>
                <td>Script runs from clean clone; evidence packet; cache committed</td>
              </tr>
              <tr>
                <td className="font-mono text-sm whitespace-nowrap">SR → PR</td>
                <td>Systematic literature review; sensitivity suite at ±50%; internal review; red-team response; public replication archive; attestation chain label. Human-final upgrade requires named external readers.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <Divider />

      <PullQuote attribution="Constitution §6.4">
        Composite indices are triage instruments only. They may appear in
        outputs but must be labeled as such, and must not be the headline
        claim.
      </PullQuote>

      <Divider />

      {/* Taste heuristics */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-16">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="ochre">Taste — what we don't do</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-9 grid sm:grid-cols-2 gap-y-3 gap-x-8 text-ink-soft">
          {/* style-guide:allow banned-words — quoting Constitution §14 verbatim */}
          {/* style-guide:allow dmc-framing — quoting Constitution §13.3 verbatim */}
          {[
            "Headline a composite index",
            "Publish a country ranking as the core finding",
            "Use machine learning to make a weak question look strong",
            "Smooth away outliers that the policy audience cares about",
            "Cite AI as a source of fact",
            "Bundle unrelated findings to make a program look bigger",
            "Present screening results in policy-ready packaging",
            "Recycle a method across programs without checking fit",
            "Use the words \"revolutionary,\" \"unprecedented,\" \"game-changing\"",
            "Promote a finding past its evidence",
            "Frame DMCs as failing — framing is \"measurement gap,\" not \"deficient country\"",
          ].map((line) => (
            <div key={line} className="flex gap-3">
              <span className="numeral text-base shrink-0 leading-tight">·</span>
              <span>{line}</span>
            </div>
          ))}
        </div>
      </section>

      <Divider wide />

      <section className="text-center">
        <Kicker>Continue</Kicker>
        <div className="mt-4 flex flex-wrap justify-center gap-4">
          <Link to="/about#governance" className="ed-link">Constitution &amp; governance</Link>
          <Link to="/about#reproducibility" className="ed-link">Reproducibility</Link>
          <Link to="/about#ai" className="ed-link">AI transparency</Link>
          <Link to="/data" className="ed-link">Data catalog</Link>
        </div>
      </section>
    </div>
  );
}
