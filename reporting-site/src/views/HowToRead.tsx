"use client";

import Link from "next/link";
import { Kicker, Numeral, Divider } from "../components/ui";

export default function HowToRead() {
  return (
    <div className="reveal">
      <header className="mb-12 pb-8 border-b border-[var(--rule)]">
        <Kicker variant="ochre">Reader's guide</Kicker>
        <h1 className="masthead-display text-[clamp(2.4rem,5vw,4.6rem)] mt-3">
          How to{" "}
          <span className="display-italic" style={{ color: "var(--ochre)" }}>
            read
          </span>{" "}
          this site.
        </h1>
        <p className="lede mt-7 max-w-[60ch]">
          A periodical of measurement-gap research. Constitution-governed,
          AI-attested under §18, every number traces to a public source and
          a committed script. Five things to know before you click around.
        </p>
      </header>

      {/* Section 1: Site layout */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Numeral n={1} />
          <h2 className="display-md text-[1.6rem] mt-2">Site layout</h2>
        </header>
        <div className="col-span-12 lg:col-span-9">
          <table className="data-table w-full how-to-read-route-table">
            <colgroup>
              <col style={{ width: "38%" }} />
              <col />
            </colgroup>
            <thead>
              <tr>
                <th>Route</th>
                <th>What's there</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><Link href="/" className="ed-link font-mono">/</Link></td>
                <td>Magazine cover for the current issue. Featured findings.</td>
              </tr>
              <tr>
                <td><Link href="/briefs" className="ed-link font-mono">/briefs</Link></td>
                <td><strong>Start here</strong> — research briefs: one page per topic with status, chart, source stack, caveat, next step.</td>
              </tr>
              <tr>
                <td><Link href="/findings" className="ed-link font-mono">/findings</Link></td>
                <td>The articles hub. Long-form working papers, research briefs, and issue notes.</td>
              </tr>
              <tr>
                <td><Link href="/findings/the-first-issue" className="ed-link font-mono">/findings/the-first-issue</Link></td>
                <td>Issue editorial introducing the current finished and screening programs.</td>
              </tr>
              <tr>
                <td><Link href="/research" className="ed-link font-mono">/research</Link></td>
                <td>All 18 programs grouped by domain. Each has a maturity chip.</td>
              </tr>
              <tr>
                <td><span className="font-mono text-sm">/program/{`{slug}`}</span></td>
                <td>Canonical topic page. Opens the best available surface: paper first, then evidence, then a register overview.</td>
              </tr>
              <tr>
                <td><span className="font-mono text-sm">/program/{`{slug}`}/evidence</span></td>
                <td>Redirects to the topic Evidence tab: pre-registration, sensitivity, reviews, limitations, source data, and hash-pinned files.</td>
              </tr>
              <tr>
                <td><Link href="/atlas" className="ed-link font-mono">/atlas</Link></td>
                <td>45 ADB DMCs by subregion. Click any to see all programs' view of that economy.</td>
              </tr>
              <tr>
                <td><span className="font-mono text-sm">/dmc/{`{ISO3}`}</span></td>
                <td>Country dossier — every program's metric for one DMC, with rank-distribution dots.</td>
              </tr>
              <tr>
                <td><Link href="/data" className="ed-link font-mono">/data</Link></td>
                <td>Catalog of every public dataset used. Access-grade chips (A–F).</td>
              </tr>
              <tr>
                <td><Link href="/data/matrix" className="ed-link font-mono">/data/matrix</Link></td>
                <td>Cross-program vulnerability matrix.</td>
              </tr>
              <tr>
                <td><Link href="/archive" className="ed-link font-mono">/archive</Link></td>
                <td>Permanent-archive index. Citation handles for every program.</td>
              </tr>
              <tr>
                <td><Link href="/methods" className="ed-link font-mono">/methods</Link></td>
                <td>Claim-maturity tiers, gate requirements, taste heuristics.</td>
              </tr>
              <tr>
                <td><Link href="/about" className="ed-link font-mono">/about</Link></td>
                <td>The lab itself: mission, governance, AI transparency.</td>
              </tr>
              <tr>
                <td><Link href="/team" className="ed-link font-mono">/team</Link></td>
                <td>Authors and red-team roster.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <Divider />

      {/* Section 2: Maturity tiers */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Numeral n={2} />
          <h2 className="display-md text-[1.6rem] mt-2">Maturity tiers</h2>
        </header>
        <div className="col-span-12 lg:col-span-9">
          <p className="text-ink-soft leading-relaxed max-w-prose">
            Every program carries one of four labels (Constitution §7.1).
            The label tells you what the program promises.
          </p>
          <ul className="mt-6 space-y-4 text-ink-soft">
            <li className="flex gap-4">
              <span className="font-mono text-xs uppercase tracking-[0.18em] shrink-0 mt-1 w-12">H</span>
              <div><strong>Hypothesis.</strong> An idea. May be AI-assisted. <em>Not a finding.</em> Don't quote any number.</div>
            </li>
            <li className="flex gap-4">
              <span className="font-mono text-xs uppercase tracking-[0.18em] shrink-0 mt-1 w-12">PP</span>
              <div><strong>Prepared Pipeline.</strong> A script that runs end-to-end. <em>Engineering exists; nothing has been concluded.</em></div>
            </li>
            <li className="flex gap-4">
              <span className="font-mono text-xs uppercase tracking-[0.18em] shrink-0 mt-1 w-12">SR</span>
              <div><strong>Screening Result.</strong> The pipeline ran. Output is preliminary, triage only. Quotable as "screening signal" with `limitations.md` caveats. <em>Not policy-actionable.</em></div>
            </li>
            <li className="flex gap-4">
              <span className="font-mono text-xs uppercase tracking-[0.18em] shrink-0 mt-1 w-12">PR</span>
              <div><strong>Publication-ready.</strong> Internal PR code. Full evidence package: literature synthesis, sensitivity where applicable, review response, and permanent archive. Quotable only with the AI-first attestation caveat unless upgraded to human-final.</div>
            </li>
          </ul>
        </div>
      </section>

      <Divider />

      {/* Section 3: Attestation chain */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Numeral n={3} />
          <h2 className="display-md text-[1.6rem] mt-2">The chip beside every label</h2>
        </header>
        <div className="col-span-12 lg:col-span-9">
          <p className="text-ink-soft leading-relaxed max-w-prose">
            Beside every maturity label you'll see a colored chip — orange,
            sage, or grey. That's the <em>attestation chain</em>.
          </p>
          <ul className="mt-6 space-y-3 text-ink-soft">
            <li className="flex items-baseline gap-3">
              <span className="font-mono text-xs uppercase tracking-[0.18em]" style={{ color: "var(--ochre)" }}>● ai-first</span>
              <span>Drafted, attested, gate-promoted by AI under <Link href="/about#ai" className="ed-link">Constitution §18</Link>. Literature reviews, pre-registrations, internal review, red-team review are all AI-attested. <strong>No human has line-by-line read every cited paper. No external reviewer was contacted.</strong></span>
            </li>
            <li className="flex items-baseline gap-3">
              <span className="font-mono text-xs uppercase tracking-[0.18em]" style={{ color: "var(--sage)" }}>● human-final</span>
              <span>Every gate-action by the human owner per the pre-§18 Constitution. Currently zero programs.</span>
            </li>
            <li className="flex items-baseline gap-3">
              <span className="font-mono text-xs uppercase tracking-[0.18em] text-ink">● mixed</span>
              <span>Some gate-actions AI, some human. <code className="font-mono not-italic">review-external.md</code> records which.</span>
            </li>
          </ul>
          <p className="mt-6 text-ink-soft leading-relaxed max-w-prose">
            Read the chip honestly. A finding labeled <code className="font-mono not-italic">PR · ai-first</code>{" "}
            means: publication-ready under the disclosed AI-first chain, not peer reviewed or supervisor-attested.
            Convert it to <code className="font-mono not-italic">human-final</code>{" "}
            via the §18.5 upgrade-pass paths in each program's
            <code className="font-mono not-italic"> review-external.md </code> §5.
          </p>
        </div>
      </section>

      <Divider />

      {/* Section 4: Reproducibility */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Numeral n={4} />
          <h2 className="display-md text-[1.6rem] mt-2">Reproducing any number</h2>
        </header>
        <div className="col-span-12 lg:col-span-9 max-w-prose">
          <p className="text-ink-soft leading-relaxed">
            Every empirical value on this site traces to a committed script
            hitting a public source. Constitution §11 makes this binding.
          </p>
          <p className="text-ink-soft leading-relaxed mt-4">
            To reproduce any program's headline locally:
          </p>
          <pre className="mt-4 overflow-x-auto" style={{
            background: "var(--ink)",
            color: "var(--paper)",
            padding: "1.4rem 1.6rem",
            fontFamily: "JetBrains Mono, monospace",
            fontSize: "0.78rem",
            lineHeight: 1.7,
          }}>{`# 1. Clone the upstream repo (when published)
git clone https://github.com/rradofina/adb-research

# 2. Run the program's pipeline
python {program-slug}/scripts/process-{slug}.py

# 3. Run the sensitivity suite
python {program-slug}/scripts/sensitivity.py

# 4. Verify cache hashes match
node scripts/verify-manifest.mjs`}</pre>
          <p className="text-ink-soft leading-relaxed mt-6">
            No API keys are required for the current reproduction paths — cache files are
            committed and hash-pinned in <code className="font-mono not-italic">manifest.sha256</code>.
            Live refresh is opt-in
            per pipeline.
          </p>
          <p className="text-ink-soft leading-relaxed mt-4">
            To inspect a program's full audit trail without running anything,
            open <code className="font-mono not-italic">/{`{slug}`}?view=evidence</code> — that page
            renders every artifact (literature review, pre-registration,
            sensitivity, coverage, results, internal review, red-team
            review, limitations) inline, with per-file SHA-256.
          </p>
        </div>
      </section>

      <Divider />

      {/* Section 5: Honest non-claims */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Numeral n={5} />
          <h2 className="display-md text-[1.6rem] mt-2">What this site is not</h2>
        </header>
        <div className="col-span-12 lg:col-span-9 max-w-prose">
          <p className="text-ink-soft leading-relaxed">
            The Constitution's taste heuristics (§14) and DMC framing (§13.3)
            are honored throughout:
          </p>
          <ul className="mt-4 space-y-2 text-ink-soft">
            <li>· This is <strong>not a country ranking</strong>. Composite indices appear as triage instruments only.</li>
            <li>· The framing is <strong>measurement gap, coverage gap, observability gap</strong> — not DMC deficiency.</li>
            <li>· No claim is presented past its evidence. Honest narrowings are surfaced, not buried.</li>
            <li>· Prepared-pipeline programs may contain computed screens, but those screens are not treated as final research; missing evidence upgrades remain explicit.</li>
            <li>· The digital-performance screening paper reports an executed ITU availability–use measurement study; the inherited Ookla speed route remains a separate, unrun quality upgrade.</li>
            <li>· The hypothesis program (mpi-nighttime-lights) remains owner-led until the external nighttime-lights track is reconciled with this repository.</li>
            <li>· Every <code className="font-mono not-italic">ai-first</code> chip is labeled honestly. A reader who wants <code className="font-mono not-italic">human-final</code> work has the upgrade-pass paths documented per program.</li>
          </ul>
        </div>
      </section>

      <Divider wide />

      <nav className="flex items-center justify-between flex-wrap gap-4 pb-12">
        <Link href="/research" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
          → Browse the research catalogue
        </Link>
        <div className="flex gap-4 flex-wrap">
          <Link href="/research" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">All programs</Link>
          <Link href="/archive" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">Archive</Link>
          <Link href="/methods" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">Methods</Link>
        </div>
      </nav>
    </div>
  );
}
