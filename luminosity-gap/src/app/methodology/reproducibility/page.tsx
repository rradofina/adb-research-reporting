import type { Metadata } from "next";
import Link from "next/link";
import {
  aiTransparencyRules,
  reproducibilityPrinciples,
  reproducibilityProfiles,
  transparencyReferences,
} from "@/data/reproducibility";

export const metadata: Metadata = {
  title: "Reproducibility and AI Transparency | Development Blindspots Lab",
  description:
    "Reproducibility, audit trail, and AI-assistance disclosure standard for the research programs.",
};

const COMMON_COMMANDS = [
  "npm install",
  "npm run research:access",
  "npm run research:ookla",
  "OPENAQ_API_KEY=<key> npm run research:openaq",
  "npm run lint",
  "npm run build",
];

const CLAIM_LABELS = [
  {
    label: "Hypothesis",
    body: "A research idea or possible gap. It can be AI-assisted, but it must not be presented as a finding.",
  },
  {
    label: "Prepared pipeline",
    body: "A script, manifest, or SQL file exists. It is useful, but no empirical result is claimed yet.",
  },
  {
    label: "Screening result",
    body: "A script has produced data for pilot economies. It can guide next work, but it is not yet a final indicator.",
  },
  {
    label: "Publication-ready result",
    body: "Source retrieval, code, sensitivity checks, external caveats, and claim scope have all been reviewed.",
  },
];

export default function ReproducibilityPage() {
  return (
    <div className="bg-zinc-950 text-zinc-100">
      <section className="border-b border-zinc-800">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <Link
            href="/methodology"
            className="text-sm font-medium text-zinc-500 transition-colors hover:text-zinc-300"
          >
            Methodology
          </Link>
          <p className="mt-8 font-mono text-sm uppercase tracking-widest text-emerald-400">
            Reproducibility standard
          </p>
          <h1 className="mt-4 max-w-4xl break-words text-3xl font-semibold tracking-tight text-white sm:text-5xl">
            Make the research rerunnable, source-visible, and honest about AI
            assistance.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-zinc-400">
            The trust strategy is not to hide AI use. It is to disclose where AI
            helped, keep empirical claims tied to scripts and sources, and show
            the exact boundary between a hypothesis, a prepared pipeline, and a
            measured result.
          </p>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-8 px-4 py-14 sm:px-6 lg:grid-cols-[360px_minmax(0,1fr)] lg:px-8">
        <div className="min-w-0">
          <h2 className="text-2xl font-semibold text-white">
            Operating Rules
          </h2>
          <p className="mt-3 text-sm leading-6 text-zinc-500">
            These are the rules that should hold for every program page,
            generated data artifact, and working research folder.
          </p>
        </div>
        <div className="grid min-w-0 gap-4 md:grid-cols-2">
          <RuleList title="Reproducibility" items={reproducibilityPrinciples} />
          <RuleList title="AI transparency" items={aiTransparencyRules} />
        </div>
      </section>

      <section className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
          <div className="mb-8 max-w-3xl">
            <h2 className="text-2xl font-semibold text-white">
              Claim Labels
            </h2>
            <p className="mt-3 text-sm leading-6 text-zinc-500">
              The app should label research maturity explicitly so a polished UI
              never makes a weak result look stronger than it is.
            </p>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {CLAIM_LABELS.map((item) => (
              <article
                key={item.label}
                className="rounded-lg border border-zinc-800 bg-zinc-950 p-5"
              >
                <h3 className="font-semibold text-zinc-100">{item.label}</h3>
                <p className="mt-3 text-sm leading-6 text-zinc-500">
                  {item.body}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-white">
              Program Trust Records
            </h2>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-500">
              Each program gets a compact audit record: what command reruns it,
              what data it uses, what AI helped with, and what is still blocked.
            </p>
          </div>
          <Link
            href="/research"
            className="text-sm font-medium text-zinc-400 transition-colors hover:text-zinc-200"
          >
            Open research programs
          </Link>
        </div>

        <div className="space-y-5">
          {reproducibilityProfiles.map((profile) => (
            <article
              key={profile.slug}
              className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5"
            >
              <div className="grid gap-5 lg:grid-cols-[260px_minmax(0,1fr)]">
                <div className="min-w-0">
                  <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
                    {profile.status}
                  </p>
                  <h3 className="mt-2 text-xl font-semibold text-white">
                    {profile.title}
                  </h3>
                  <p className="mt-3 font-mono text-xs leading-5 text-emerald-300">
                    {profile.command}
                  </p>
                </div>
                <div className="grid min-w-0 gap-4 md:grid-cols-3">
                  <MiniList title="Claim scope" items={[profile.claimScope]} />
                  <MiniList title="Outputs" items={profile.outputs} mono />
                  <MiniList title="Current limits" items={profile.limitations} />
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="border-y border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-14 sm:px-6 lg:grid-cols-[360px_minmax(0,1fr)] lg:px-8">
          <div className="min-w-0">
            <h2 className="text-2xl font-semibold text-white">
              Rerun Checklist
            </h2>
            <p className="mt-3 text-sm leading-6 text-zinc-500">
              These commands are the minimum local check before calling the
              current site reproducible. Data requiring credentials or large
              downloads remains explicitly marked.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-5">
            <ul className="space-y-3">
              {COMMON_COMMANDS.map((command) => (
                <li
                  key={command}
                  className="font-mono text-xs leading-6 text-zinc-300"
                >
                  {command}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-3xl">
          <h2 className="text-2xl font-semibold text-white">
            External Reference Points
          </h2>
          <p className="mt-3 text-sm leading-6 text-zinc-500">
            The disclosure design is anchored to reproducible-research and
            responsible-AI guidance rather than a one-off note hidden in the
            README.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {transparencyReferences.map((reference) => (
            <a
              key={reference.url}
              href={reference.url}
              target="_blank"
              rel="noreferrer"
              className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5 transition-colors hover:border-zinc-600"
            >
              <h3 className="font-semibold text-zinc-100">{reference.name}</h3>
              <p className="mt-3 text-sm leading-6 text-zinc-500">
                {reference.use}
              </p>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}

function RuleList({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5">
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

function MiniList({
  title,
  items,
  mono,
}: {
  title: string;
  items: string[];
  mono?: boolean;
}) {
  return (
    <div className="min-w-0">
      <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
        {title}
      </p>
      <ul className="mt-2 space-y-2">
        {items.map((item) => (
          <li
            key={item}
            className={`text-sm leading-6 text-zinc-400 ${
              mono ? "font-mono text-xs" : ""
            }`}
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
