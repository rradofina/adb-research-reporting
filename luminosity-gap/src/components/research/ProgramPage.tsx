import Link from "next/link";
import type { ResearchProgram } from "@/data/research-programs";
import { AccessServicesPilotEvidence } from "./AccessPilotSummary";
import { PipelineArtifactPanel } from "./PipelineArtifactPanel";
import { ReproducibilityPanel } from "./ReproducibilityPanel";

export function ProgramPage({ program }: { program: ResearchProgram }) {
  return (
    <div className="bg-zinc-950 text-zinc-100">
      <section className="border-b border-zinc-800">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-[minmax(0,1fr)_360px] lg:px-8 lg:py-20">
          <div className="min-w-0">
            <Link
              href="/research"
              className="text-sm font-medium text-zinc-500 transition-colors hover:text-zinc-300"
            >
              Research agenda
            </Link>
            <p className="mt-8 font-mono text-sm uppercase tracking-widest text-zinc-500">
              Program {program.number}
            </p>
            <h1 className="mt-4 max-w-4xl break-words text-3xl font-semibold tracking-tight text-white sm:text-5xl">
              {program.title}
            </h1>
            <p className="mt-6 max-w-3xl text-xl leading-8 text-zinc-300">
              {program.oneLine}
            </p>
            <p className="mt-5 max-w-3xl leading-7 text-zinc-500">
              {program.hypothesis}
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <a
                href="#sources"
                className="rounded-lg px-4 py-2 text-sm font-semibold text-zinc-950 transition-opacity hover:opacity-90"
                style={{ backgroundColor: program.accent }}
              >
                Source stack
              </a>
              <a
                href="#method"
                className="rounded-lg border border-zinc-700 px-4 py-2 text-sm font-semibold text-zinc-200 transition-colors hover:border-zinc-500"
              >
                Method design
              </a>
            </div>
          </div>

          <aside className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-900/60 p-5">
            <div
              className="mb-5 h-1.5 rounded-full"
              style={{ backgroundColor: program.accent }}
            />
            <dl className="space-y-5 text-sm">
              <div>
                <dt className="font-mono uppercase tracking-wider text-zinc-600">
                  Status
                </dt>
                <dd className="mt-1 text-zinc-200">{program.status}</dd>
              </div>
              <div>
                <dt className="font-mono uppercase tracking-wider text-zinc-600">
                  ADB Fit
                </dt>
                <dd className="mt-1 text-zinc-300">{program.adbFit}</dd>
              </div>
              <div>
                <dt className="font-mono uppercase tracking-wider text-zinc-600">
                  Coverage
                </dt>
                <dd className="mt-1 text-zinc-300">{program.coverage}</dd>
              </div>
            </dl>
          </aside>
        </div>
      </section>

      <section className="border-b border-zinc-800">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-12 sm:px-6 lg:grid-cols-3 lg:px-8">
          <SummaryBlock label="Why now" value={program.whyNow} />
          <SummaryBlock label="Wow factor" value={program.wowFactor} />
          <SummaryBlock label="Research gap" value={program.literatureGap[0]} />
        </div>
      </section>

      {program.slug === "access-services" && <AccessServicesPilotEvidence />}
      {program.slug === "digital-performance" && (
        <PipelineArtifactPanel kind="ookla" />
      )}
      {program.slug === "air-monitoring" && (
        <PipelineArtifactPanel kind="openaq" />
      )}

      <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="grid min-w-0 gap-8 lg:grid-cols-[380px_minmax(0,1fr)]">
          <div className="min-w-0">
            <h2 className="text-2xl font-semibold text-white">
              Research Questions
            </h2>
            <p className="mt-3 text-sm leading-6 text-zinc-500">
              These are written as testable questions, not marketing claims. The
              first implementation should produce enough evidence to reject,
              refine, or narrow each one.
            </p>
          </div>
          <div className="grid min-w-0 gap-3 md:grid-cols-2">
            {program.questions.map((question) => (
              <div
                key={question}
                className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-4"
              >
                <p className="text-sm leading-6 text-zinc-300">{question}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-end justify-between gap-6">
            <div>
              <h2 className="text-2xl font-semibold text-white">
                Data Availability
              </h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-500">
                The goal is not perfect coverage on day one. It is enough common
                coverage to build a credible regional comparison and identify
                where data quality itself becomes part of the finding.
              </p>
            </div>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {program.dataAvailability.map((item) => (
              <div
                key={item.label}
                className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
              >
                <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
                  {item.label}
                </p>
                <p className="mt-2 text-sm leading-6 text-zinc-300">
                  {item.value}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="sources" className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-white">Source Stack</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-500">
            Each source is included because it can become a reproducible input
            to an analysis table. The caveats are deliberate: weak data coverage
            is a finding only when it is measured transparently.
          </p>
        </div>
        <div className="max-w-full overflow-x-auto rounded-lg border border-zinc-800">
          <table className="w-full min-w-[980px] text-left text-sm">
            <thead className="bg-zinc-900 text-xs uppercase tracking-wider text-zinc-500">
              <tr>
                <th className="px-4 py-3 font-medium">Dataset</th>
                <th className="px-4 py-3 font-medium">Coverage</th>
                <th className="px-4 py-3 font-medium">Use</th>
                <th className="px-4 py-3 font-medium">Caveat</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800">
              {program.sourceStack.map((source) => (
                <tr key={source.url} className="align-top">
                  <td className="px-4 py-4">
                    <a
                      href={source.url}
                      className="font-medium text-zinc-100 underline decoration-zinc-700 underline-offset-4 hover:decoration-zinc-300"
                      target="_blank"
                      rel="noreferrer"
                    >
                      {source.name}
                    </a>
                    <p className="mt-1 text-xs text-zinc-600">
                      {source.owner} | {source.years} | {source.access}
                    </p>
                  </td>
                  <td className="px-4 py-4 text-zinc-400">{source.coverage}</td>
                  <td className="px-4 py-4 text-zinc-400">{source.use}</td>
                  <td className="px-4 py-4 text-zinc-500">{source.caveat}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section id="method" className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto grid max-w-7xl gap-10 px-4 py-14 sm:px-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] lg:px-8">
          <div className="min-w-0">
            <h2 className="text-2xl font-semibold text-white">
              Method Design
            </h2>
            <ol className="mt-6 space-y-3">
              {program.methodSteps.map((step, index) => (
                <li key={step} className="flex gap-3">
                  <span
                    className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-bold text-zinc-950"
                    style={{ backgroundColor: program.accent }}
                  >
                    {index + 1}
                  </span>
                  <span className="pt-0.5 text-sm leading-6 text-zinc-300">
                    {step}
                  </span>
                </li>
              ))}
            </ol>
          </div>

          <div className="min-w-0">
            <h2 className="text-2xl font-semibold text-white">
              Core Metrics
            </h2>
            <div className="mt-6 space-y-4">
              {program.metrics.map((metric) => (
                <div
                  key={metric.name}
                  className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                >
                  <h3 className="font-semibold text-zinc-100">{metric.name}</h3>
                  <p className="mt-2 text-sm leading-6 text-zinc-400">
                    {metric.definition}
                  </p>
                  <p className="mt-3 font-mono text-xs text-zinc-600">
                    Output: {metric.output}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <ReproducibilityPanel slug={program.slug} />

      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-14 sm:px-6 lg:grid-cols-3 lg:px-8">
        <div>
          <h2 className="text-2xl font-semibold text-white">
            Pilot Economies
          </h2>
          <p className="mt-3 text-sm leading-6 text-zinc-500">
            Start with countries where the source overlap is strong, then widen
            coverage as each pipeline stabilizes.
          </p>
        </div>
        <div className="lg:col-span-2">
          <div className="flex flex-wrap gap-2">
            {program.pilotEconomies.map((economy) => (
              <span
                key={economy}
                className="rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-zinc-300"
              >
                {economy}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-zinc-800">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-14 sm:px-6 lg:grid-cols-2 lg:px-8">
          <div>
            <h2 className="text-2xl font-semibold text-white">
              Implementation Plan
            </h2>
            <ul className="mt-6 space-y-3">
              {program.implementation.map((item) => (
                <li key={item} className="rounded-lg bg-zinc-900/50 p-4 text-sm leading-6 text-zinc-300">
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-white">
              Known Weak Points
            </h2>
            <ul className="mt-6 space-y-3">
              {program.caveats.map((item) => (
                <li key={item} className="rounded-lg border border-zinc-800 p-4 text-sm leading-6 text-zinc-400">
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
}

function SummaryBlock({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-5">
      <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p className="mt-3 text-sm leading-6 text-zinc-300">{value}</p>
    </div>
  );
}
