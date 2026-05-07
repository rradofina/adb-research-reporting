import type { Metadata } from "next";
import Link from "next/link";
import { researchPrograms } from "@/data/research-programs";
import {
  aiTransparencyRules,
  reproducibilityPrinciples,
} from "@/data/reproducibility";

export const metadata: Metadata = {
  title: "Methodology | Development Blindspots Lab",
  description:
    "Implementation methodology for four source-backed ADB research programs.",
};

const PIPELINE_STEPS = [
  {
    title: "Boundary and economy spine",
    body: "Create one ADB member-economy list, ISO codes, admin hierarchy, and reporting calendar. Every dataset joins to this spine before any claims are made.",
  },
  {
    title: "Source coverage audit",
    body: "Profile each source by geography, year, resolution, license, update cadence, and missingness. Missing coverage is recorded as evidence, not hidden.",
  },
  {
    title: "Reproducible extraction",
    body: "Use Earth Engine for heavy raster summaries, DuckDB spatial/PostGIS for vector joins, and static Parquet/CSV outputs for repeatable review.",
  },
  {
    title: "Population weighting",
    body: "Report people affected, not only area affected. WorldPop or GHSL population grids become the denominator for all core metrics.",
  },
  {
    title: "Uncertainty labels",
    body: "Separate observed values, modeled values, sparse-measurement areas, and unavailable data. The interface must show confidence and caveats.",
  },
  {
    title: "Operational validation",
    body: "Compare outputs with official indicators, known projects, subnational human-development measures, monitoring station metadata, and country case studies.",
  },
];

const QUALITY_GATES = [
  "No headline claim without a named source, year, geography, and reproducible script.",
  "No regional ranking unless coverage is comparable enough for that ranking.",
  "No imputation that hides a measurement desert. Sparse data must stay visible.",
  "No country-level conclusion when the evidence only supports a pilot-region claim.",
  "No live dashboard layer unless its raw source, transformation, and caveat are documented.",
];

export default function MethodologyPage() {
  return (
    <div className="bg-zinc-950 text-zinc-100">
      <section className="border-b border-zinc-800">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <p className="font-mono text-sm uppercase tracking-widest text-zinc-500">
            Research discipline
          </p>
          <h1 className="mt-4 max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            A source-first methodology for turning unconventional ideas into
            defensible ADB research.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-zinc-400">
            This site is now a four-program research agenda, not a finished
            empirical result. The current work establishes the hypotheses,
            source stacks, implementation design, and quality gates needed
            before producing final indicators.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[360px_1fr]">
          <div>
            <h2 className="text-2xl font-semibold text-white">
              Common Pipeline
            </h2>
            <p className="mt-3 text-sm leading-6 text-zinc-500">
              Each program uses the same evidence chain so the work can scale
              from a country pilot to a multi-economy comparison.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {PIPELINE_STEPS.map((step, index) => (
              <div
                key={step.title}
                className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5"
              >
                <p className="font-mono text-xs text-zinc-600">
                  Step {index + 1}
                </p>
                <h3 className="mt-2 font-semibold text-zinc-100">
                  {step.title}
                </h3>
                <p className="mt-3 text-sm leading-6 text-zinc-500">
                  {step.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
          <div className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h2 className="text-2xl font-semibold text-white">
                Program-Specific Designs
              </h2>
              <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-500">
                The four ideas are intentionally different, but each has a
                clear data stack, measurable output, and first implementation
                path.
              </p>
            </div>
            <Link
              href="/data-sources"
              className="text-sm font-medium text-zinc-400 transition-colors hover:text-zinc-200"
            >
              Review source inventory
            </Link>
          </div>

          <div className="grid gap-5 lg:grid-cols-2">
            {researchPrograms.map((program) => (
              <article
                key={program.slug}
                className="rounded-lg border border-zinc-800 bg-zinc-950 p-5"
              >
                <div
                  className="mb-5 h-1.5 w-20 rounded-full"
                  style={{ backgroundColor: program.accent }}
                />
                <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
                  Program {program.number}
                </p>
                <h3 className="mt-2 text-xl font-semibold text-white">
                  {program.title}
                </h3>
                <p className="mt-3 text-sm leading-6 text-zinc-400">
                  {program.hypothesis}
                </p>

                <div className="mt-5 grid gap-3">
                  <MethodBlock
                    label="First metric"
                    value={program.metrics[0].definition}
                  />
                  <MethodBlock
                    label="First pilots"
                    value={program.pilotEconomies.slice(0, 5).join(", ")}
                  />
                  <MethodBlock label="Main caveat" value={program.caveats[0]} />
                </div>

                <Link
                  href={program.href}
                  className="mt-5 inline-flex text-sm font-medium text-zinc-300 transition-colors hover:text-white"
                >
                  Open full method
                </Link>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[360px_minmax(0,1fr)]">
          <div className="min-w-0">
            <h2 className="text-2xl font-semibold text-white">
              Quality Gates
            </h2>
            <p className="mt-3 text-sm leading-6 text-zinc-500">
              These rules keep the work from becoming a polished but weak
              dashboard. The point is to be ambitious and still falsifiable.
            </p>
          </div>

          <div className="space-y-3">
            {QUALITY_GATES.map((gate) => (
              <div
                key={gate}
                className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-4 text-sm leading-6 text-zinc-300"
              >
                {gate}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-14 sm:px-6 lg:grid-cols-[360px_minmax(0,1fr)] lg:px-8">
          <div className="min-w-0">
            <h2 className="text-2xl font-semibold text-white">
              Reproducibility and AI Disclosure
            </h2>
            <p className="mt-3 text-sm leading-6 text-zinc-500">
              The research should be transparent about both computational
              evidence and AI assistance. AI use is not hidden; it is logged and
              bounded so empirical claims still point to sources and scripts.
            </p>
            <Link
              href="/methodology/reproducibility"
              className="mt-5 inline-flex text-sm font-medium text-zinc-300 transition-colors hover:text-white"
            >
              Open full transparency standard
            </Link>
          </div>

          <div className="grid min-w-0 gap-4 md:grid-cols-2">
            <MethodList
              title="Reproducibility rules"
              items={reproducibilityPrinciples.slice(0, 4)}
            />
            <MethodList
              title="AI transparency rules"
              items={aiTransparencyRules.slice(0, 4)}
            />
          </div>
        </div>
      </section>

      <section className="border-t border-zinc-800">
        <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-semibold text-white">
            Implementation Order
          </h2>
          <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <OrderCard
              title="1. Research pages"
              body="Done here: every program has a dedicated page, source table, metric design, pilot list, and caveat set."
            />
            <OrderCard
              title="2. Source folders"
              body="Done here: every program has a folder under /research with a README that describes the build path."
            />
            <OrderCard
              title="3. Data pipelines"
              body="Next build step: add download and aggregation scripts for one flagship pilot before scaling."
            />
            <OrderCard
              title="4. Evidence app"
              body="After computed tables exist, replace static methodology cards with maps, charts, and downloadable outputs."
            />
          </div>
        </div>
      </section>
    </div>
  );
}

function MethodBlock({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/60 p-3">
      <p className="font-mono text-[11px] uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p className="mt-1 text-sm leading-6 text-zinc-400">{value}</p>
    </div>
  );
}

function MethodList({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-5">
      <h3 className="font-semibold text-zinc-100">{title}</h3>
      <ul className="mt-4 space-y-3">
        {items.map((item) => (
          <li key={item} className="text-sm leading-6 text-zinc-500">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function OrderCard({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5">
      <h3 className="font-semibold text-zinc-100">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-zinc-500">{body}</p>
    </div>
  );
}
