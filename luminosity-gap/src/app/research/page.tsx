import type { Metadata } from "next";
import Link from "next/link";
import { researchPrograms } from "@/data/research-programs";
import { AccessPilotSummary } from "@/components/research/AccessPilotSummary";

export const metadata: Metadata = {
  title: "Research Agenda | Development Blindspots Lab",
  description:
    "Four source-backed research programs for measuring development blind spots across ADB member economies.",
};

export default function ResearchAgendaPage() {
  return (
    <div className="bg-zinc-950 text-zinc-100">
      <section className="border-b border-zinc-800">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
          <p className="font-mono text-sm uppercase tracking-widest text-zinc-500">
            Research agenda
          </p>
          <h1 className="mt-4 max-w-4xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            Four ways to measure what conventional development indicators miss.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-zinc-400">
            The old nighttime-lights idea becomes a benchmark, not the project.
            These programs look for blind spots in access, digital quality, air
            monitoring, and settlement growth using open geospatial and
            statistical data.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-5 lg:grid-cols-2">
          {researchPrograms.map((program) => (
            <Link
              key={program.slug}
              href={program.href}
              className="group rounded-lg border border-zinc-800 bg-zinc-900/50 p-6 transition-colors hover:border-zinc-600"
            >
              <div
                className="mb-5 h-1.5 w-24 rounded-full"
                style={{ backgroundColor: program.accent }}
              />
              <div className="flex items-center gap-3">
                <span className="font-mono text-xs text-zinc-600">
                  {program.number}
                </span>
                <span className="rounded-full border border-zinc-800 px-2 py-1 text-xs text-zinc-500">
                  {program.status}
                </span>
              </div>
              <h2 className="mt-4 text-2xl font-semibold text-white">
                {program.title}
              </h2>
              <p className="mt-3 text-sm leading-6 text-zinc-400">
                {program.oneLine}
              </p>
              {program.slug === "access-services" && <AccessPilotSummary />}
              <p className="mt-5 text-sm font-medium text-zinc-300">
                Open program <span className="text-zinc-600">/</span>
              </p>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
