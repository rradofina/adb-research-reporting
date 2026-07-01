"use client";

export default function Reproducibility() {
  return (
    <div>
      <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
        CONSTITUTION.md §11 — operational
      </p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">
        Reproducibility standard.
      </h1>
      <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
        The goal is byte-identical reproducibility from a clean clone of the
        repository without any API key or live network call. A live
        refresh path exists but is opt-in on each pipeline.
      </p>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">Governance files at repository root</h2>
        <ul className="mt-3 text-ink-700 leading-7">
          <li><code className="font-mono">CONSTITUTION.md</code> — the research charter.</li>
          <li><code className="font-mono">CLAUDE.md</code> — binds AI assistants to the constitution.</li>
          <li><code className="font-mono">data-access-audit.md</code> — catalog of ~80 public sources plus 50 NSOs, 58 ministries, 16 city portals.</li>
          <li><code className="font-mono">sources.md</code> — living literature-database floor.</li>
          <li><code className="font-mono">red-team.md</code> — external reviewer roster (to be populated by owner).</li>
          <li><code className="font-mono">references.bib</code> — BibTeX library (10 verified entries today).</li>
          <li><code className="font-mono">versions.json</code> — pinned external source versions.</li>
          <li><code className="font-mono">manifest.sha256</code> — SHA-256 of every committed cache file.</li>
        </ul>
      </section>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">Rerun commands</h2>
        <pre className="mt-3 bg-ink-900 text-ink-50 rounded-md p-5 text-xs overflow-x-auto font-mono">
{`# Program 1 — Climate-adjusted access to services
cd luminosity-gap
npm install
npm run research:access

# Program 2 — Measured digital development gap
npm run research:ookla

# Program 3 — Air pollution without air monitors
OPENAQ_API_KEY=<your-key> npm run research:openaq

# Program 13 — Public service data quality (PHL + BGD)
cd ..
bash public-service-data-quality/scripts/fetch-nhfr.sh
# BGD fetch is in process-multi-country.py; each page is curl'd
python public-service-data-quality/scripts/process-multi-country.py

# Run this reporting site
cd reporting-site
npm install
npm run dev   # http://localhost:5173`}
        </pre>
      </section>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">Required artifacts per program</h2>
        <ul className="list-disc mt-3 ml-6 text-ink-700 space-y-1">
          <li>Source URLs and retrieval timestamps recorded per row, not just per artifact.</li>
          <li>Committed cache under <code className="font-mono">.cache/research/&lt;program&gt;/</code>.</li>
          <li>Every arbitrary numeric choice (threshold, weight, buffer) tested at ±50%.</li>
          <li>Composite indices labelled as triage; never as headline.</li>
          <li>BibTeX keys cited in every written output; no bare URLs.</li>
        </ul>
      </section>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">AI transparency</h2>
        <p className="mt-3 text-ink-700 max-w-3xl">
          AI may draft code, prose, and source-triage lists. AI may not
          generate empirical numbers, run literature reviews unsupervised,
          or advance a program's claim-maturity label. Every program's
          README names which parts were AI-drafted and what was
          human-checked. See <code className="font-mono">luminosity-gap/docs/AI_TRANSPARENCY.md</code>.
        </p>
      </section>
    </div>
  );
}
