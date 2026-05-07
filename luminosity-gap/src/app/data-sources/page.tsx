import type { Metadata } from "next";
import { researchPrograms, sharedResearchSources } from "@/data/research-programs";

export const metadata: Metadata = {
  title: "Data Sources | Development Blindspots Lab",
  description:
    "Open data inventory for four ADB research programs on access, digital performance, air monitoring, and urbanization.",
};

export default function DataSourcesPage() {
  return (
    <div className="bg-zinc-950 text-zinc-100">
      <section className="border-b border-zinc-800">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <p className="font-mono text-sm uppercase tracking-widest text-zinc-500">
            Source inventory
          </p>
          <h1 className="mt-4 max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            Public data that can support the four blindspot programs.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-zinc-400">
            The data strategy is to use global or broad regional datasets for
            comparability, then label coverage gaps instead of pretending that
            every economy has equal source quality.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-semibold text-white">
          Program Coverage Map
        </h2>
        <div className="mt-6 grid gap-5 lg:grid-cols-2">
          {researchPrograms.map((program) => (
            <div
              key={program.slug}
              className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5"
            >
              <div
                className="mb-4 h-1.5 w-20 rounded-full"
                style={{ backgroundColor: program.accent }}
              />
              <h3 className="text-xl font-semibold text-white">
                {program.title}
              </h3>
              <p className="mt-2 text-sm leading-6 text-zinc-500">
                {program.coverage}
              </p>
              <div className="mt-5 grid gap-2">
                {program.dataAvailability.map((item) => (
                  <div
                    key={item.label}
                    className="rounded-lg border border-zinc-800 bg-zinc-950 p-3"
                  >
                    <p className="font-mono text-[11px] uppercase tracking-wider text-zinc-600">
                      {item.label}
                    </p>
                    <p className="mt-1 text-sm text-zinc-300">{item.value}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-white">
              Deduplicated Source List
            </h2>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-500">
              This is the cross-program data spine. Every dataset below appears
              in at least one program page with a concrete use and caveat.
            </p>
          </div>

          <div className="overflow-x-auto rounded-lg border border-zinc-800">
            <table className="w-full min-w-[1040px] text-left text-sm">
              <thead className="bg-zinc-950 text-xs uppercase tracking-wider text-zinc-500">
                <tr>
                  <th className="px-4 py-3 font-medium">Source</th>
                  <th className="px-4 py-3 font-medium">Owner</th>
                  <th className="px-4 py-3 font-medium">Years</th>
                  <th className="px-4 py-3 font-medium">Access</th>
                  <th className="px-4 py-3 font-medium">Caveat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800">
                {sharedResearchSources.map((source) => (
                  <tr key={source.url} className="align-top">
                    <td className="px-4 py-4">
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noreferrer"
                        className="font-medium text-zinc-100 underline decoration-zinc-700 underline-offset-4 hover:decoration-zinc-300"
                      >
                        {source.name}
                      </a>
                      <p className="mt-1 text-xs text-zinc-600">
                        {source.coverage}
                      </p>
                    </td>
                    <td className="px-4 py-4 text-zinc-400">{source.owner}</td>
                    <td className="px-4 py-4 text-zinc-400">{source.years}</td>
                    <td className="px-4 py-4 text-zinc-400">{source.access}</td>
                    <td className="px-4 py-4 text-zinc-500">
                      {source.caveat}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}
