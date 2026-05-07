import { Link } from "react-router-dom";
import { Kicker, PullQuote, Divider, Chip } from "../components/ui";

export default function About() {
  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-14">
        <div className="col-span-12 md:col-span-8">
          <Kicker variant="crimson">About the lab</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,5.2rem)] mt-3">
            Measure the{" "}
            <span className="display-italic" style={{ color: "var(--crimson)" }}>
              gap.
            </span>
          </h1>
          <p className="lede mt-7 max-w-[58ch]">
            The Blindspots Lab studies the difference between official data
            and reality across Asian Development Bank developing member
            economies. Public data only. Every number traces to a committed
            script. The current issue is labeled as AI-first under §18, with
            human-final upgrade paths kept separate.
          </p>
        </div>
        <div className="col-span-12 md:col-span-4 md:pl-6 md:border-l md:border-[var(--rule-soft)] marginalia">
          <div className="kicker mb-3">Lead author</div>
          <p>Raymond Adofina · ADB</p>
          <p className="mt-1">In partnership with Arturo Martinez Jr.</p>
        </div>
      </header>

      <Divider wide />

      {/* Mission */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 mb-16">
        <header className="col-span-12 lg:col-span-3">
          <Kicker>Mission</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-7">
          <p className="dropcap text-lg leading-relaxed text-ink">
            Most development research treats published statistics as ground
            truth and does causal inference on top. We do the opposite. For
            each measurement that policymakers and lenders rely on, we ask
            how wrong it could be — and which direction. The answer is
            rarely "small and random." Hidden bias in measurement is itself
            policy-actionable, and almost always under-studied.
          </p>
          <p className="text-lg leading-relaxed text-ink-soft mt-6 max-w-prose">
            We focus on Asian Development Bank developing member economies
            because the data ecosystem there is uniquely uneven — extremely
            rich for some (Philippines, Bangladesh, India, Indonesia,
            Thailand) and uniquely thin for others (Pacific small islands,
            Central Asia, Caucasus, Myanmar). A single methodology applied
            consistently across both ends of that spectrum surfaces
            measurement problems that within-country studies cannot.
          </p>
        </div>
      </section>

      <Divider />

      {/* Governance */}
      <section id="governance" className="grid grid-cols-12 gap-6 lg:gap-10 my-16 scroll-mt-32">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="crimson">Governance</Kicker>
          <h2 className="display-md text-[1.6rem] mt-3">The Constitution</h2>
        </header>
        <div className="col-span-12 lg:col-span-7">
          <p className="text-ink-soft leading-relaxed">
            A single document at the upstream repository binds every program:
            principles (public data only, auditable end-to-end, original
            contribution or no contribution, AI as assistant), claim
            maturity tiers, gate requirements between tiers, scope
            discipline, taste heuristics ("things we don't do"), publication
            pathway, and ethics.
          </p>
          <ul className="mt-6 space-y-3 text-ink-soft">
            <li className="flex gap-3">
              <span className="numeral text-base">·</span>
              <span><strong>Maturity tiers.</strong> Hypothesis → Prepared pipeline → Screening result → Publication-ready. Each transition has required artifacts.</span>
            </li>
            <li className="flex gap-3">
              <span className="numeral text-base">·</span>
              <span><strong>Work-in-progress limit.</strong> Normal mode caps human-final work at 1 finished paper and 3 screening-result programs. §18 AI-first work is labeled separately.</span>
            </li>
            <li className="flex gap-3">
              <span className="numeral text-base">·</span>
              <span><strong>Composite indices are triage only.</strong> They never headline a program. Headline claims are narrow and falsifiable.</span>
            </li>
            <li className="flex gap-3">
              <span className="numeral text-base">·</span>
              <span><strong>External red-team review.</strong> Human-final publication claims need named external readers; AI-first claims disclose that the red-team step is synthesized from public methodological positions.</span>
            </li>
          </ul>
        </div>
      </section>

      <Divider />

      <PullQuote attribution="Constitution §14 — Taste heuristics">
        Things we do not do: headline a composite index, publish a
        country ranking as the core finding, use machine learning to
        make a weak question look strong, smooth away outliers that the
        policy audience cares about, cite AI as a source of fact.
      </PullQuote>

      <Divider />

      {/* Reproducibility */}
      <section id="reproducibility" className="grid grid-cols-12 gap-6 lg:gap-10 my-16 scroll-mt-32">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="sage">Reproducibility</Kicker>
          <h2 className="display-md text-[1.6rem] mt-3">Auditable end-to-end</h2>
        </header>
        <div className="col-span-12 lg:col-span-7">
          <p className="text-ink-soft leading-relaxed">
            Every empirical value here traces to (a) a committed script,
            (b) a committed or publicly pinnable source, and (c) a
            recorded retrieval timestamp. A fresh clone of the upstream
            repository reproduces the exact same numbers without any API
            key or live network call.
          </p>
          <div className="mt-6 grid sm:grid-cols-2 gap-x-6 gap-y-4 marginalia">
            <div>
              <div className="kicker mb-1">Versions pinning</div>
              <p>versions.json at repo root pins every external version ID.</p>
            </div>
            <div>
              <div className="kicker mb-1">Cache hashes</div>
              <p>manifest.sha256 records SHA-256 of every committed cache file.</p>
            </div>
            <div>
              <div className="kicker mb-1">Environment lock</div>
              <p>Dockerfile / devcontainer fixes Node, tsx, DuckDB, Python.</p>
            </div>
            <div>
              <div className="kicker mb-1">CI fixture</div>
              <p>CI runs each pipeline against a small fixture DMC on every PR.</p>
            </div>
          </div>
        </div>
      </section>

      <Divider />

      {/* AI transparency */}
      <section id="ai" className="grid grid-cols-12 gap-6 lg:gap-10 my-16 scroll-mt-32">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="ochre">AI transparency</Kicker>
          <h2 className="display-md text-[1.6rem] mt-3">Bounded, not invisible</h2>
        </header>
        <div className="col-span-12 lg:col-span-7">
          <p className="text-ink-soft leading-relaxed">
            AI assists with code drafting, prose, and source triage. It does
            not invent empirical numbers or cite itself as evidence. Under
            §18, some gate actions are AI-first rather than human-final, so
            the site labels the attestation chain and keeps the upgrade path
            visible instead of implying supervisor or external signoff.
          </p>
          <div className="mt-6 flex gap-2 flex-wrap">
            <Chip variant="ochre">AI may draft</Chip>
            <Chip variant="ochre">AI may not invent numbers</Chip>
            <Chip variant="ochre">Attestation chain visible</Chip>
            <Chip variant="ochre">Human-final kept separate</Chip>
          </div>
        </div>
      </section>

      <Divider wide />

      <section className="text-center">
        <Kicker>Index</Kicker>
        <h2 className="display-md text-[1.6rem] mt-3">Continue reading</h2>
        <div className="mt-6 flex flex-wrap justify-center gap-4">
          <Link to="/briefs" className="ed-link">All research briefs</Link>
          <Link to="/research" className="ed-link">Research register</Link>
          <Link to="/methods" className="ed-link">Methods in detail</Link>
          <Link to="/team" className="ed-link">Team & red team</Link>
          <Link to="/data" className="ed-link">Data catalog</Link>
        </div>
      </section>
    </div>
  );
}
