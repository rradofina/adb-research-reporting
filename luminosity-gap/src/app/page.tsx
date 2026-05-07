import Link from "next/link";
import { researchPrograms } from "@/data/research-programs";
import { AccessPilotSummary } from "@/components/research/AccessPilotSummary";

const PRINCIPLES = [
  {
    label: "Measure blind spots",
    value:
      "The target is not what every dashboard already shows. The target is the gap between official visibility and lived conditions.",
  },
  {
    label: "Use open data first",
    value:
      "Every program starts from source-backed data that can be re-run for many ADB member economies.",
  },
  {
    label: "Treat missingness as evidence",
    value:
      "A weak monitor network, sparse speed tests, or incomplete facility data is not hidden. It becomes part of the result.",
  },
  {
    label: "Build operational metrics",
    value:
      "The output should be useful for project design: where to invest, where to validate, and where not to trust aggregate indicators.",
  },
];

export default function Home() {
  const flagship = researchPrograms[0];

  return (
    <div className="bg-zinc-950 text-zinc-100">
      <section className="border-b border-zinc-800">
        <div className="mx-auto grid max-w-7xl gap-12 px-4 py-16 sm:px-6 lg:grid-cols-[1fr_420px] lg:px-8 lg:py-24">
          <div>
            <p className="font-mono text-sm uppercase tracking-widest text-zinc-500">
              ADB Research // Adofina &amp; Martinez (2026)
            </p>
            <h1 className="mt-5 max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-6xl">
              Find the development risks that conventional indicators miss.
            </h1>
            <p className="mt-6 max-w-3xl text-lg leading-8 text-zinc-400">
              This replaces the old nighttime-lights angle with a deeper
              research agenda: climate-adjusted access, real internet
              performance, air-quality observability, and invisible
              urbanization across ADB member economies.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/research"
                className="rounded-lg bg-emerald-400 px-5 py-3 text-center text-sm font-semibold text-zinc-950 transition-opacity hover:opacity-90"
              >
                Open the research agenda
              </Link>
              <Link
                href={flagship.href}
                className="rounded-lg border border-zinc-700 px-5 py-3 text-center text-sm font-semibold text-zinc-200 transition-colors hover:border-zinc-500"
              >
                Start with access under climate stress
              </Link>
            </div>
          </div>

          <aside className="rounded-lg border border-zinc-800 bg-zinc-900/70 p-5">
            <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
              Current judgment
            </p>
            <h2 className="mt-3 text-2xl font-semibold text-white">
              Nighttime lights should become a benchmark, not the headline.
            </h2>
            <p className="mt-4 text-sm leading-6 text-zinc-400">
              Lights are useful but conventional. The stronger project is a
              blindspots lab: show where people, risks, or service failures are
              undercounted by standard indicators.
            </p>
            <div className="mt-6 grid gap-3">
              <MiniMetric label="Flagship candidate" value="Climate access" />
              <MiniMetric label="Cleanest data story" value="Internet speed" />
              <MiniMetric label="Strongest invisible-risk story" value="Air monitors" />
              <MiniMetric label="Most visual story" value="Building growth" />
            </div>
          </aside>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h2 className="text-3xl font-semibold text-white">
              Four Research Programs
            </h2>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-500">
              Each program has an ADB-relevant question, public source stack,
              implementation plan, caveats, and pilot economy list.
            </p>
          </div>
          <Link
            href="/data-sources"
            className="text-sm font-medium text-zinc-400 transition-colors hover:text-zinc-200"
          >
            View full source inventory
          </Link>
        </div>

        <div className="grid gap-5 lg:grid-cols-2">
          {researchPrograms.map((program) => (
            <Link
              key={program.slug}
              href={program.href}
              className="group rounded-lg border border-zinc-800 bg-zinc-900/40 p-6 transition-colors hover:border-zinc-600"
            >
              <div
                className="mb-5 h-1.5 w-20 rounded-full"
                style={{ backgroundColor: program.accent }}
              />
              <div className="flex flex-wrap items-center gap-3">
                <span className="font-mono text-xs text-zinc-600">
                  {program.number}
                </span>
                <span className="rounded-full border border-zinc-800 px-2 py-1 text-xs text-zinc-500">
                  {program.status}
                </span>
              </div>
              <h3 className="mt-4 text-2xl font-semibold text-white">
                {program.title}
              </h3>
              <p className="mt-3 text-sm leading-6 text-zinc-400">
                {program.oneLine}
              </p>
              {program.slug === "access-services" && <AccessPilotSummary />}
              <p className="mt-5 text-sm font-medium text-zinc-300">
                Read program details <span className="text-zinc-600">/</span>
              </p>
            </Link>
          ))}
        </div>
      </section>

      <section className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-semibold text-white">
            How This Becomes Real Research
          </h2>
          <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
            {PRINCIPLES.map((principle) => (
              <div
                key={principle.label}
                className="rounded-lg border border-zinc-800 bg-zinc-950 p-5"
              >
                <h3 className="font-semibold text-zinc-100">
                  {principle.label}
                </h3>
                <p className="mt-3 text-sm leading-6 text-zinc-500">
                  {principle.value}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

function MiniMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-3">
      <p className="font-mono text-[11px] uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p className="mt-1 text-sm font-medium text-zinc-200">{value}</p>
    </div>
  );
}
