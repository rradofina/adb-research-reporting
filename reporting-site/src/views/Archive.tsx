"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { loadEvidenceManifest, type EvidenceManifest } from "../lib/evidence";
import { programs } from "../data/programs";
import { Kicker, Numeral, Divider } from "../components/ui";

interface ProgramArchiveRow {
  slug: string;
  title: string;
  manifest: EvidenceManifest | null;
  attestation: string | null;
  artifactCount: number;
  generatedCount: number;
}

const SLUG_TO_TITLE: Record<string, string> = Object.fromEntries(
  programs.map((p) => [p.slug, p.title]),
);

export default function Archive() {
  const [rows, setRows] = useState<ProgramArchiveRow[] | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const indexResp = await fetch("/programs/index.json");
      if (!indexResp.ok) {
        if (!cancelled) setRows([]);
        return;
      }
      const index = (await indexResp.json()) as { programs: string[] };
      const out: ProgramArchiveRow[] = [];
      for (const slug of index.programs) {
        const m = await loadEvidenceManifest(slug);
        const chains = m ? new Set(m.artifacts.map((a) => a.attestation_chain).filter(Boolean)) : new Set();
        const attestation = chains.size === 1 ? [...chains][0] as string : (chains.size > 1 ? "mixed" : null);
        out.push({
          slug,
          title: SLUG_TO_TITLE[slug] ?? slug,
          manifest: m,
          attestation,
          artifactCount: m?.artifacts.length ?? 0,
          generatedCount: m?.generated_files.length ?? 0,
        });
      }
      if (!cancelled) setRows(out);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (!rows) {
    return <div className="py-20 text-center text-ink-faint reveal">Loading archive…</div>;
  }

  // Sort: by attestation chain (ai-first first), then artifact count descending
  const sorted = [...rows].sort((a, b) => {
    const order = (chain: string | null) => chain === "ai-first" ? 1 : chain === "human-final" ? 2 : chain === "mixed" ? 3 : 4;
    const oa = order(a.attestation);
    const ob = order(b.attestation);
    if (oa !== ob) return oa - ob;
    return b.artifactCount - a.artifactCount;
  });

  return (
    <div className="reveal">
      {/* Hero */}
      <header className="mb-12 pb-8 border-b border-[var(--rule)]">
        <Kicker variant="ochre">Archive — permanent evidence packets</Kicker>
        <h1 className="masthead-display text-[clamp(2.6rem,6vw,5rem)] mt-3">
          The{" "}
          <span className="display-italic" style={{ color: "var(--ochre)" }}>
            archive.
          </span>
        </h1>
        <p className="lede mt-7 max-w-[60ch]">
          Every program's permanent evidence packet. The URL plus the
          publication commit SHA is the citation handle under
          <code className="font-mono not-italic"> CONSTITUTION.md </code>
          §10.3 (self-hosted permanent archive). All artifacts are
          hash-pinned in each program's <code className="font-mono not-italic">manifest.json</code>.
        </p>
      </header>

      {/* Table */}
      <section className="mb-16">
        <table className="data-table w-full">
          <thead>
            <tr>
              <th>№</th>
              <th>Program</th>
              <th>Attestation</th>
              <th className="text-right">Artifacts</th>
              <th className="text-right">Generated</th>
              <th>Permanent URL</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((r, i) => (
              <tr key={r.slug}>
                <td className="font-mono text-xs text-ink-faint tabular">
                  {String(i + 1).padStart(2, "0")}
                </td>
                <td>
                  <Link href={`/program/${r.slug}/evidence`} className="ed-link display-md text-base">
                    {r.title}
                  </Link>
                  <div className="marginalia mt-1 font-mono">{r.slug}</div>
                </td>
                <td>
                  {r.attestation ? (
                    <span
                      className="font-mono text-xs uppercase tracking-[0.16em]"
                      style={{
                        color: r.attestation === "ai-first"
                          ? "var(--ochre)"
                          : r.attestation === "human-final"
                            ? "var(--sage)"
                            : "var(--ink)",
                      }}
                    >
                      ● {r.attestation}
                    </span>
                  ) : (
                    <span className="text-ink-faint font-mono text-xs">—</span>
                  )}
                </td>
                <td className="text-right font-mono tabular text-sm">{r.artifactCount}</td>
                <td className="text-right font-mono tabular text-sm">{r.generatedCount}</td>
                <td className="font-mono text-[0.7rem] text-ink-soft">
                  /program/{r.slug}/evidence
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <Divider />

      {/* Citation guidance */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Kicker>How to cite</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-9 max-w-prose">
          <p className="text-ink-soft leading-relaxed">
            Every finished current-issue program's permanent URL is
            <code className="font-mono not-italic">/program/{`{slug}`}/evidence</code>.
            The URL plus the publication commit SHA on
            <code className="font-mono not-italic"> rradofina/adb-research-reporting</code>
            is the citation handle. Each artifact carries its own SHA-256
            in the program's <code className="font-mono not-italic">manifest.json</code>.
          </p>
          <pre
            className="mt-6 overflow-x-auto"
            style={{
              background: "var(--ink)",
              color: "var(--paper)",
              padding: "1.4rem 1.6rem",
              fontFamily: "JetBrains Mono, monospace",
              fontSize: "0.78rem",
              lineHeight: 1.7,
            }}
          >{`Adofina, R. (2026). {Program title} — permanent evidence packet.
The Blindspots Lab.
${typeof window !== "undefined" ? window.location.origin : ""}/program/{slug}/evidence
attestation_chain: ai-first  (or human-final / mixed)
commit: {SHA at publication}`}</pre>
        </div>
      </section>

      <Divider />

      {/* Attestation chain legend */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="ochre">Attestation chain</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-9 grid sm:grid-cols-3 gap-6">
          <div className="ed-card p-6">
            <div className="font-mono text-xs uppercase tracking-[0.18em]" style={{ color: "var(--ochre)" }}>
              ● ai-first
            </div>
            <p className="mt-3 text-ink-soft text-sm leading-relaxed">
              Drafted, attested, and gate-promoted by AI under
              <code className="font-mono not-italic"> CONSTITUTION.md</code> §18.
              Literature, pre-registration, internal review, and red-team
              review are AI-attested rather than human-attested.
            </p>
          </div>
          <div className="ed-card p-6">
            <div className="font-mono text-xs uppercase tracking-[0.18em]" style={{ color: "var(--sage)" }}>
              ● human-final
            </div>
            <p className="mt-3 text-ink-soft text-sm leading-relaxed">
              Every gate-action by the human owner under the pre-§18
              Constitution. Reserved for upgrade-passes from
              <code className="font-mono not-italic"> ai-first</code>.
              Currently zero.
            </p>
          </div>
          <div className="ed-card p-6">
            <div className="font-mono text-xs uppercase tracking-[0.18em] text-ink">
              ● mixed
            </div>
            <p className="mt-3 text-ink-soft text-sm leading-relaxed">
              Some gate-actions AI, some human. The artifact's
              <code className="font-mono not-italic"> review-external.md</code>
              records which.
            </p>
          </div>
        </div>
      </section>

      <Divider wide />

      <nav className="flex items-center justify-between flex-wrap gap-4 pb-12">
        <Link href="/research" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
          ← Programs
        </Link>
        <Link href="/findings" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
          Findings →
        </Link>
      </nav>
    </div>
  );
}
