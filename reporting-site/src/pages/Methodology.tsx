export default function Methodology() {
  return (
    <div>
      <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
        CONSTITUTION.md — highlights
      </p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">
        How research is done here.
      </h1>

      <Section title="Principles">
        <ul className="list-disc ml-6 space-y-1">
          <li>Public data only.</li>
          <li>Every number traces to a committed script and a recorded retrieval timestamp.</li>
          <li>Original contribution or no contribution — dated landscape scan per program.</li>
          <li>Simple, defensible, falsifiable. Composite indices are triage only.</li>
          <li>AI is never a source of fact. When §18 AI-first mode is active, the attestation chain is labeled instead of hidden.</li>
          <li>A weak result reported honestly is worth more than a strong result that cannot be defended.</li>
        </ul>
      </Section>

      <Section title="Claim maturity (§7)">
        <div className="grid md:grid-cols-4 gap-3 mt-2 text-sm">
          <Tier tier="H" label="Hypothesis" body="Idea, gap, proposed metric. May be AI-assisted. Not a finding." />
          <Tier tier="PP" label="Prepared pipeline" body="Script, manifest, SQL exists. No empirical value claimed." />
          <Tier tier="SR" label="Screening result" body="Pipeline has run. Triage only." />
          <Tier tier="PR" label="Finished for issue" body="Source retrieval, code, sensitivity, review response, and archive complete for the stated chain." />
        </div>
      </Section>

      <Section title="Gate requirements between tiers">
        <table className="data-table w-full text-sm bg-white border border-ink-200 rounded-md mt-2">
          <thead>
            <tr className="text-left">
              <th>Transition</th>
              <th>Required artifacts</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>H → PP</td><td>literature.md; scoring ≥18; first testable claim; falsification condition</td></tr>
            <tr><td>PP → SR</td><td>Script runs on clean clone; evidence packet; committed cache</td></tr>
            <tr><td>SR → PR</td><td>Systematic literature review; sensitivity suite; internal review; red-team response; public archive; attestation chain label</td></tr>
          </tbody>
        </table>
      </Section>

      <Section title="Scope discipline (§8)">
        <p>
          Normal human-final work-in-progress limit: <strong>max 1 finished paper</strong>,{" "}
          <strong>max 3 at screening result</strong>. §18 AI-first work is labeled separately.
        </p>
      </Section>

      <Section title="Taste heuristics (§14) — things we do not do">
        <ul className="list-disc ml-6 space-y-1">
          <li>Headline a composite index or country ranking.</li>
          <li>Use machine learning to make a weak question look strong.</li>
          <li>Smooth away outliers that the policy audience cares about.</li>
          <li>Cite AI as a source of fact.</li>
          {/* style-guide:allow banned-words — quoting Constitution §14 verbatim */}
          {/* style-guide:allow dmc-framing — quoting Constitution §13.3 verbatim */}
          <li>Use the words "revolutionary", "unprecedented", "game-changing".</li>
          <li>Frame DMCs as failing — framing is "measurement gap", not "deficient country".</li>
          <li>Promote a finding past its evidence.</li>
        </ul>
      </Section>

      <Section title="Authority">
        <p>
          The Constitution at the repository root (<code className="font-mono">CONSTITUTION.md</code>)
          is the authoritative document. This page is a plain-language
          extract for readers. If anything here differs from the Constitution,
          the Constitution wins.
        </p>
      </Section>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-10">
      <h2 className="text-lg font-semibold uppercase tracking-wider text-ink-500">
        {title}
      </h2>
      <div className="mt-3 text-ink-700 leading-relaxed max-w-4xl">
        {children}
      </div>
    </section>
  );
}

function Tier({ tier, label, body }: { tier: string; label: string; body: string }) {
  return (
    <div className="bg-white border border-ink-200 rounded-md p-4">
      <div className="text-xs uppercase tracking-wider text-ink-500 tabular">{tier}</div>
      <div className="mt-1 font-semibold">{label}</div>
      <div className="mt-1 text-xs text-ink-700">{body}</div>
    </div>
  );
}
