import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { programs } from "../data/programs";
import { BRIEF_DETAILS } from "../data/briefs";
import { Kicker, FeatureCard, Divider, PullQuote, Chip, StatBlock, Bar } from "../components/ui";
import { INDICATORS, loadIndicator, type IndicatorRow } from "../lib/indicators";

interface Highlight {
  iso3: string;
  country: string;
  value: number;
  programSlug: string;
  programTitle: string;
  unit: string;
  metricLabel: string;
}

export default function Home() {
  const [highlights, setHighlights] = useState<Highlight[]>([]);

  useEffect(() => {
    Promise.all(
      INDICATORS.map(async (def) => {
        try {
          const rows = await loadIndicator(def);
          const valid = rows.filter((r) => r.value !== null) as Required<IndicatorRow>[];
          if (valid.length === 0) return null;
          valid.sort((a, b) => (b.value as number) - (a.value as number));
          const top = valid[0];
          const country =
            top.raw && (top.raw as any).country ?
              (top.raw as any).country :
              top.iso3;
          return {
            iso3: top.iso3,
            country: typeof country === "string" ? country : top.iso3,
            value: top.value as number,
            programSlug: def.programSlug,
            programTitle: def.programTitle,
            unit: def.unit,
            metricLabel: def.metricLabel,
          };
        } catch {
          return null;
        }
      }),
    ).then((arr) => setHighlights(arr.filter(Boolean) as Highlight[]));
  }, []);

  const featuredFindings = programs
    .filter((p) => p.href)
    .sort((a, b) => Number(Boolean(BRIEF_DETAILS[b.slug]?.flagship)) - Number(Boolean(BRIEF_DETAILS[a.slug]?.flagship)) || a.id - b.id)
    .slice(0, 6);
  const flagshipProgram = programs.find((p) => p.slug === "public-service-data-quality");
  const flagshipBrief = BRIEF_DETAILS["public-service-data-quality"];
  const startHere = [
    {
      number: "01",
      eyebrow: "Click hook",
      title: "Start with the gap a planner can see",
      body: "The flagship page opens with the health-facility registry gap before it asks the reader to inspect methods or caveats.",
      to: flagshipProgram?.href ?? "/program/public-service-data-quality",
      cta: "Open flagship page",
    },
    {
      number: "02",
      eyebrow: "Read-through hook",
      title: "Move from question to evidence",
      body: "The article follows the ADB/ERDI pattern: problem, data gap, source upgrade, chart result, caveat, and reproducibility path.",
      to: "/findings/measurement-gap-philippines-bangladesh",
      cta: "Read article",
    },
    {
      number: "03",
      eyebrow: "Proof layer",
      title: "Check the source packet",
      body: "The evidence page exposes generated files, source notes, and the completed PSA manual-download record.",
      to: "/program/public-service-data-quality/evidence",
      cta: "Inspect evidence",
    },
  ];
  const counts: Record<string, number> = { H: 0, PP: 0, SR: 0, PR: 0, Ret: 0 };
  programs.forEach((p) => (counts[p.status] += 1));

  return (
    <div className="reveal">
      {/* Hero feature — executive first screen */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 items-start">
        <div className="col-span-12 lg:col-span-7">
          <Kicker variant="crimson">Start here · Flagship measurement gap</Kicker>
          <h2 className="masthead-display text-[clamp(2.4rem,7vw,5.6rem)] mt-4">
            When public maps miss services, planning starts{" "}
            <span className="display-italic" style={{ color: "var(--crimson)" }}>
              blind
            </span>{" "}
            .
          </h2>
          <p className="lede mt-7 max-w-[58ch]">
            {flagshipBrief.output} The point is not to shame a map or rank a
            country. It is to show where a public data layer is too thin for
            service planning, then let the reader inspect the evidence.
          </p>
          <div className="mt-8 mb-6 px-6 py-5" style={{ background: "var(--paper-deep)", borderLeft: "3px solid var(--crimson)" }}>
            <div className="flex items-baseline gap-3 mb-2 font-mono text-[0.66rem] uppercase tracking-[0.22em]" style={{ color: "var(--crimson)" }}>
              <span>● Recommended first story</span>
            </div>
            <Link to="/program/public-service-data-quality" className="block group">
              <h3 className="display-md text-[1.4rem] group-hover:text-crimson transition-colors">
                Public service data quality: the registry sees many more clinical facilities than the public map.
              </h3>
              <p className="mt-3 text-ink-soft leading-relaxed">
                This is the strongest entry point because the hook, chart,
                source upgrade, caveat, and evidence packet all sit in one
                reader path.
              </p>
            </Link>
          </div>
          <div className="mt-2 flex flex-wrap items-center gap-3">
            <Link
              to="/program/public-service-data-quality"
              className="inline-flex items-center gap-2 px-6 py-3 text-sm uppercase tracking-[0.18em] font-mono bg-ink text-paper hover:bg-crimson transition-colors"
            >
              Open flagship page
            </Link>
            <Link
              to="/briefs"
              className="inline-flex items-center gap-2 px-6 py-3 text-sm uppercase tracking-[0.18em] font-mono border border-[var(--rule)] text-ink hover:border-ink transition-colors"
            >
              Browse briefs
            </Link>
            <Link to="/findings/the-first-issue" className="ml-2 ed-link text-sm">Issue editorial →</Link>
            <Link to="/how-to-read" className="ml-2 ed-link text-sm">Reader's guide →</Link>
          </div>
        </div>

        <aside className="col-span-12 lg:col-span-5 lg:pl-10 lg:border-l lg:border-[var(--rule)]">
          <FlagshipHookVisual />
          <div className="kicker mb-4 mt-6">Three-click reading path</div>
          <div className="border border-[var(--rule)] bg-paper">
            {startHere.map((item) => (
              <Link
                key={item.number}
                to={item.to}
                className="grid grid-cols-[3.5rem_minmax(0,1fr)] gap-4 border-b border-[var(--rule-soft)] p-5 last:border-b-0 group"
              >
                <div className="font-mono text-sm tabular text-ink-faint">{item.number}</div>
                <div className="min-w-0">
                  <div className="font-mono text-[0.66rem] uppercase tracking-[0.2em] text-ink-faint">
                    {item.eyebrow}
                  </div>
                  <div className="mt-2 display-md text-[1.1rem] group-hover:text-crimson transition-colors">
                    {item.title}
                  </div>
                  <p className="mt-2 text-sm leading-relaxed text-ink-soft">
                    {item.body}
                  </p>
                  <div className="mt-3 ed-link text-xs uppercase tracking-[0.18em] font-mono">
                    {item.cta} →
                  </div>
                </div>
              </Link>
            ))}
          </div>
          <p className="mt-4 marginalia">
            This mirrors the ADB data-story pattern: hook the policy problem,
            show the data gap, then let the evidence packet carry the trust.
          </p>
        </aside>
      </section>

      <Divider wide />

      {/* Evidence snapshot */}
      <section className="grid grid-cols-12 gap-6 my-10">
        <div className="col-span-12 md:col-span-4">
          <Kicker>What to tell a first-time reader</Kicker>
          <h2 className="display-lg text-[clamp(1.6rem,2.6vw,2.4rem)] mt-3">
            The site is a research desk, not a landing page.
          </h2>
        </div>
        <div className="col-span-12 md:col-span-8 grid gap-4 sm:grid-cols-3">
          <ExecutiveCard
            label="Strongest claim"
            value="Granular evidence"
            note="PSDQ now moves below country and ADM1 summaries into city/municipality and upazila views."
          />
          <ExecutiveCard
            label="Best proof"
            value="Sources visible"
            note="Each serious page shows source notes, non-claims, generated files, and reproducibility links."
          />
          <ExecutiveCard
            label="How to browse"
            value="Brief → evidence → methods"
            note="Briefs explain the argument; program pages show charts; methods pages show how to trust it."
          />
        </div>
      </section>

      <Divider wide />

      {/* Pull quote */}
      <section className="grid grid-cols-12 gap-6 my-10">
        <div className="col-span-12 lg:col-span-3 lg:col-start-2">
          <Kicker>Editor's note</Kicker>
        </div>
        <div className="col-span-12 lg:col-span-7">
          <PullQuote attribution="Constitution §2.4 — Taste">
            A weak result reported honestly is worth more than a strong
            result that cannot be defended.
          </PullQuote>
        </div>
      </section>

      <Divider wide />

      {/* Featured research */}
      <section>
        <div className="grid grid-cols-12 gap-6 mb-10">
          <div className="col-span-12 md:col-span-4">
            <Kicker>Sec. 1</Kicker>
            <h2 className="display-lg text-[clamp(1.8rem,3vw,2.8rem)] mt-3">Featured research</h2>
          </div>
          <div className="col-span-12 md:col-span-7 md:col-start-6 marginalia md:pl-6 md:border-l md:border-[var(--rule-soft)]">
            Sixteen of eighteen programs in the register currently carry a
            computed screening or finished-issue artifact. Each program targets a different
            measurement-gap question; their findings sit on top of an
            auditable cache of public-source data that anyone can rerun.
          </div>
        </div>

        <div className="rule" />
        {featuredFindings.map((p) => (
          <FeatureCard
            key={p.slug}
            to={p.href!}
            number={p.id}
            kicker={statusToKicker(p.status)}
            title={p.title}
            excerpt={p.summary}
            meta={p.note ?? ""}
            accent={accentForId(p.id)}
          />
        ))}
        <div className="mt-8 text-right">
          <Link to="/research" className="ed-link text-sm uppercase tracking-[0.18em] font-mono">
            All eighteen programs →
          </Link>
        </div>
      </section>

      <Divider wide />

      {/* Programs status */}
      <section className="grid grid-cols-12 gap-6">
        <div className="col-span-12 md:col-span-4">
          <Kicker>Sec. 2</Kicker>
          <h2 className="display-lg text-[clamp(1.6rem,2.5vw,2.4rem)] mt-3">
            Maturity register
          </h2>
          <p className="mt-4 text-ink-soft leading-relaxed max-w-prose">
            Every program has a status — from hypothesis through
            finished for the current issue. Human-final publication status is
            separate and requires the §18.5 upgrade path.
          </p>
        </div>

        <div className="col-span-12 md:col-span-8 grid grid-cols-2 lg:grid-cols-5 gap-px bg-[var(--rule)] border border-[var(--rule)]">
          <Status label="Hypothesis" value={counts.H} />
          <Status label="Prepared" value={counts.PP} />
          <Status label="Screening" value={counts.SR} />
          <Status label="Finished" value={counts.PR} />
          <Status label="Retired" value={counts.Ret} />
        </div>
      </section>

      <Divider wide />

      {/* Atlas teaser */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 items-end">
        <div className="col-span-12 lg:col-span-6">
          <Kicker>Sec. 3</Kicker>
          <h2 className="display-lg text-[clamp(1.8rem,3vw,2.8rem)] mt-3">
            The DMC{" "}
            <span className="display-italic" style={{ color: "var(--sage)" }}>
              atlas
            </span>
          </h2>
          <p className="mt-5 text-ink-soft max-w-prose leading-relaxed">
            Pick a country and read every program's view of it on a single
            dossier. Same data, organised by place rather than by topic —
            the cross-program signature that makes a single DMC's
            structural exposure readable.
          </p>
          <Link
            to="/atlas"
            className="mt-6 inline-flex items-center gap-2 ed-link text-sm uppercase tracking-[0.18em] font-mono"
          >
            Open the atlas →
          </Link>
        </div>

        <div className="col-span-12 lg:col-span-6 grid grid-cols-2 gap-3">
          {["PHL", "BGD", "IND", "PAK", "TKM", "KGZ", "TON", "VUT"].map((iso) => (
            <Link
              key={iso}
              to={`/dmc/${iso}`}
              className="group ed-card p-5"
            >
              <div className="font-mono text-xs text-ink-faint tabular">{iso}</div>
              <div className="display-md text-[1.2rem] mt-1 group-hover:text-crimson transition-colors">
                {dmcQuickName(iso)}
              </div>
            </Link>
          ))}
        </div>
      </section>

      <Divider wide />

      {/* Methods footer */}
      <section className="grid grid-cols-12 gap-6">
        <div className="col-span-12 md:col-span-6">
          <Kicker>How we work</Kicker>
          <h3 className="display-md text-[1.6rem] mt-3">
            Auditable, end-to-end.
          </h3>
          <p className="mt-4 text-ink-soft max-w-prose leading-relaxed">
            Every value here traces to a committed script and a recorded
            retrieval timestamp. We use AI as a drafting assistant; we do
            not let it invent empirical numbers or cite itself as evidence.
            The current issue is AI-first, so the chain is visible instead
            of implied as human-final.
          </p>
          <div className="mt-6 flex gap-2 flex-wrap">
            <Chip>Public data only</Chip>
            <Chip variant="crimson">Constitution-governed</Chip>
            <Chip variant="sage">Reproducible</Chip>
            <Chip variant="ochre">AI as assistant</Chip>
          </div>
        </div>
        <div className="col-span-12 md:col-span-6 md:pl-6 md:border-l md:border-[var(--rule-soft)] grid grid-cols-2 gap-6">
          <StatBlock label="Programs registered" value="18" note="8 finished for the issue; 8 screening; 1 pipeline; 1 hypothesis." />
          <StatBlock label="Economies covered" value="45" note="ADB regional members; extends globally." />
          <StatBlock label="Sources cataloged" value="80+" note="In the data-access audit, by license." />
          <StatBlock label="Findings indexed" value={String(highlights.length)} unit="ind." note="Cross-program metric coverage today." />
        </div>
      </section>
    </div>
  );
}

function Status({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-paper p-5">
      <div className="kicker">{label}</div>
      <div className="display-lg text-[2.2rem] mt-2 tabular">{value}</div>
    </div>
  );
}

function ExecutiveCard({ label, value, note }: { label: string; value: string; note: string }) {
  return (
    <div className="border border-[var(--rule)] bg-paper p-5">
      <div className="kicker">{label}</div>
      <div className="display-md text-[1.25rem] mt-3">{value}</div>
      <p className="mt-3 text-sm leading-relaxed text-ink-soft">{note}</p>
    </div>
  );
}

function FlagshipHookVisual() {
  return (
    <div className="border border-[var(--rule)] bg-paper p-5">
      <div className="kicker kicker-crimson">Immediate visual hook</div>
      <h3 className="display-md text-[1.35rem] mt-3">
        OSM captures only a slice of official clinical registries.
      </h3>
      <div className="mt-5 space-y-5">
        <ClinicalCoverageBar country="Philippines" ratio={0.171} label="17.1%" />
        <ClinicalCoverageBar country="Bangladesh" ratio={0.118} label="11.8%" />
      </div>
      <div className="mt-6 grid grid-cols-3 gap-px bg-[var(--rule-soft)] border border-[var(--rule-soft)]">
        <MiniStep label="Problem" value="Registry-map gap" />
        <MiniStep label="Upgrade" value="ADM3/upazila context" />
        <MiniStep label="Caveat" value="Not service access" />
      </div>
      <p className="mt-4 marginalia">
        Source: generated PSDQ summary and article evidence packet. The metric
        is a registry-observability gap, not a measure of actual facilities or
        service quality.
      </p>
    </div>
  );
}

function ClinicalCoverageBar({
  country,
  ratio,
  label,
}: {
  country: string;
  ratio: number;
  label: string;
}) {
  return (
    <div>
      <div className="flex items-baseline justify-between gap-4">
        <div className="font-mono text-[0.7rem] uppercase tracking-[0.16em] text-ink-faint">
          {country}
        </div>
        <div className="display-md text-[1.15rem] tabular">{label}</div>
      </div>
      <div className="mt-2">
        <Bar fraction={ratio} accent="crimson" height={8} />
      </div>
      <div className="mt-1 text-xs text-ink-faint">
        OSM health features as share of clinical-tier official registry
      </div>
    </div>
  );
}

function MiniStep({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-paper-200 p-3">
      <div className="font-mono text-[0.62rem] uppercase tracking-[0.16em] text-ink-faint">
        {label}
      </div>
      <div className="mt-2 text-sm leading-tight text-ink">{value}</div>
    </div>
  );
}

function statusToKicker(s: string) {
  return ({ H: "Hypothesis", PP: "Prepared", SR: "Screening result", PR: "Finished" }[s] ?? "Status").toUpperCase();
}

function accentForId(id: number): "ink" | "crimson" | "sage" | "ochre" {
  const colors = ["ink", "crimson", "sage", "ochre"] as const;
  return colors[id % colors.length];
}

function dmcQuickName(iso: string) {
  return ({ PHL: "Philippines", BGD: "Bangladesh", IND: "India", PAK: "Pakistan", TKM: "Turkmenistan", KGZ: "Kyrgyz Rep.", TON: "Tonga", VUT: "Vanuatu" } as Record<string, string>)[iso] ?? iso;
}
