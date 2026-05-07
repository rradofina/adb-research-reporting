import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { marked } from "marked";
import {
  loadEvidenceManifest,
  loadArtifact,
  stripFrontmatter,
  type EvidenceManifest,
  type ArtifactMeta,
  type ScriptFile,
} from "../lib/evidence";
import { programs } from "../data/programs";
import { Kicker, Numeral, Divider } from "../components/ui";
import { highlight } from "../lib/highlight";
import { JsonTable } from "../components/JsonTable";
import { BarChart } from "../components/Chart";

marked.setOptions({ gfm: true, breaks: false });

interface RenderedArtifact {
  meta: ArtifactMeta;
  html: string;
  raw: string;
}

const SLUG_TO_TITLE: Record<string, string> = Object.fromEntries(
  programs.map((p) => [p.slug, p.title]),
);

export default function Evidence() {
  const { slug = "" } = useParams();
  const [manifest, setManifest] = useState<EvidenceManifest | null>(null);
  const [rendered, setRendered] = useState<RenderedArtifact[]>([]);
  const [missing, setMissing] = useState(false);
  const [scriptSources, setScriptSources] = useState<Record<string, string>>({});
  const [sensitivityRuns, setSensitivityRuns] = useState<any | null>(null);
  const [panelData, setPanelData] = useState<any | null>(null);

  useEffect(() => {
    let cancelled = false;
    setManifest(null);
    setRendered([]);
    setMissing(false);
    setScriptSources({});
    setSensitivityRuns(null);
    setPanelData(null);
    (async () => {
      const m = await loadEvidenceManifest(slug);
      if (!m) {
        if (!cancelled) setMissing(true);
        return;
      }
      const mds = m.artifacts.filter((a) => a.file.endsWith(".md"));
      const out: RenderedArtifact[] = [];
      for (const a of mds) {
        const raw = await loadArtifact(slug, a.file);
        if (raw === null) continue;
        const stripped = stripFrontmatter(raw);
        const html = await marked.parse(stripped);
        out.push({ meta: a, html: typeof html === "string" ? html : "", raw });
      }
      // Load all script source files in parallel
      const scripts = m.scripts ?? [];
      const scriptEntries = await Promise.all(
        scripts.map(async (s) => {
          const text = await loadArtifact(slug, s.file);
          return [s.file, text ?? ""] as [string, string];
        }),
      );
      // Load sensitivity-runs.json if present
      const sensRunsArt = m.artifacts.find((a) => a.file === "sensitivity-runs.json");
      let sensRuns: any = null;
      if (sensRunsArt) {
        const raw = await loadArtifact(slug, sensRunsArt.file);
        if (raw) try { sensRuns = JSON.parse(raw); } catch {}
      }
      // Load primary panel JSON (the rows-bearing generated/{slug}-adb-panel.json)
      const panelGen = m.generated_files.find((g) => g.file.endsWith("adb-panel.json")) ?? m.generated_files.find((g) => g.file.endsWith(".json"));
      let panel: any = null;
      if (panelGen) {
        const raw = await loadArtifact(slug, panelGen.file);
        if (raw) try { panel = JSON.parse(raw); } catch {}
      }
      if (!cancelled) {
        setManifest(m);
        setRendered(out);
        setScriptSources(Object.fromEntries(scriptEntries));
        setSensitivityRuns(sensRuns);
        setPanelData(panel);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [slug]);

  const programTitle = SLUG_TO_TITLE[slug] ?? slug;
  const overall = useMemo(() => {
    if (!manifest) return null;
    const chains = new Set(manifest.artifacts.map((a) => a.attestation_chain).filter(Boolean));
    if (chains.size === 1) return [...chains][0];
    if (chains.size > 1) return "mixed";
    return null;
  }, [manifest]);

  if (missing) {
    return (
      <div className="py-20 text-center reveal">
        <Kicker>Evidence · 404</Kicker>
        <h1 className="display-lg text-3xl mt-4">No evidence packet at /program/{slug}/evidence</h1>
        <Link to="/research" className="ed-link mt-6 inline-block">← Back to research index</Link>
      </div>
    );
  }
  if (!manifest) {
    return <div className="py-20 text-center text-ink-faint reveal">Loading evidence packet…</div>;
  }

  const article = manifest.articles[0];
  const programHref = programs.find((p) => p.slug === slug)?.href;

  return (
    <div className="reveal">
      {/* Hero */}
      <header className="mb-12 pb-8 border-b border-[var(--rule)]">
        <div className="flex items-baseline gap-4 flex-wrap mb-4">
          <Kicker variant={overall === "ai-first" ? "ochre" : overall === "human-final" ? "sage" : "default"}>
            Permanent evidence packet
          </Kicker>
          <span className="font-mono text-xs uppercase tracking-[0.18em] text-ink-faint">
            {slug}
          </span>
          {overall && (
            <span
              className="font-mono text-xs uppercase tracking-[0.18em]"
              style={{ color: overall === "ai-first" ? "var(--ochre)" : overall === "human-final" ? "var(--sage)" : "var(--ink)" }}
            >
              ● attestation_chain: {overall}
            </span>
          )}
        </div>
        <h1 className="masthead-display text-[clamp(2.4rem,5vw,4.6rem)] leading-[0.96]">
          {programTitle}
        </h1>
        <div className="mt-7 grid md:grid-cols-12 gap-6">
          <div className="md:col-span-7">
            <p className="lede">
              The full audit trail for the program — pre-registration, sensitivity
              suite, coverage, internal review, external red-team review,
              limitations, source code. The permanent URL of this page is the
              citation handle under <code className="font-mono not-italic">CONSTITUTION.md</code> §10.3
              (self-hosted permanent archive).
            </p>
          </div>
          <aside className="md:col-span-5 md:pl-8 md:border-l md:border-[var(--rule-soft)] marginalia space-y-3">
            <div>
              <div className="kicker mb-1">Permanent URL</div>
              <div className="font-mono text-[0.78rem] break-all">
                {typeof window !== "undefined" ? window.location.origin : ""}
                {manifest.permanent_url}
              </div>
            </div>
            <div>
              <div className="kicker mb-1">Last refresh</div>
              <div className="font-mono">{new Date(manifest.generated_at).toLocaleString()}</div>
            </div>
            <div>
              <div className="kicker mb-1">Artifacts</div>
              <div className="font-mono">
                {manifest.artifacts.length} files · {manifest.generated_files.length} generated outputs
              </div>
            </div>
            {programHref && (
              <div className="pt-2 mt-3 border-t border-[var(--rule-soft)]">
                <Link to={programHref} className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
                  ← Program detail
                </Link>
              </div>
            )}
            {article && (
              <div>
                <Link to={`/findings/${article.slug}`} className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
                  Article: {article.title.length > 38 ? article.title.slice(0, 38) + "…" : article.title} →
                </Link>
              </div>
            )}
          </aside>
        </div>
      </header>

      {/* §18.4 callout — only when any artifact is ai-first */}
      {overall === "ai-first" && (
        <div
          className="mb-12 px-6 py-5"
          style={{
            background: "var(--paper-deep)",
            borderLeft: "3px solid var(--ochre)",
          }}
        >
          <div className="font-mono text-[0.7rem] uppercase tracking-[0.22em] mb-2" style={{ color: "var(--ochre)" }}>
            ● Notice — §18 AI-first attestation chain
          </div>
          <p className="text-ink-soft leading-relaxed max-w-prose">
            This packet is published under <Link to="/about#ai" className="ed-link">CONSTITUTION.md §18 (AI-First Operating Mode)</Link>.
            The literature review, pre-registration, internal review, and red-team
            review are AI-attested rather than human-attested. The red-team review
            is AI-synthesized from the published methodological positions of named
            candidate institutions; <strong>no individual reviewer was contacted</strong>.
            The packet is upgrade-eligible to a <code className="font-mono not-italic">human-final</code> chain
            via §18.5.
          </p>
        </div>
      )}

      <div className="grid grid-cols-12 gap-8 lg:gap-12">
        {/* TOC sidebar */}
        <aside className="col-span-12 lg:col-span-3">
          <div className="lg:sticky lg:top-8 space-y-1">
            <div className="kicker mb-3">Contents</div>
            <ol className="space-y-2 text-sm font-mono">
              {rendered.map((r, i) => (
                <li key={r.meta.key}>
                  <a
                    href={`#${r.meta.key}`}
                    className="flex items-baseline gap-2 text-ink-faint hover:text-ink transition-colors"
                  >
                    <span className="numeral text-xs shrink-0">{String(i + 1).padStart(2, "0")}</span>
                    <span className="leading-tight">{r.meta.label}</span>
                  </a>
                </li>
              ))}
              {panelData?.rows && (
                <li className="pt-2 mt-2 border-t border-[var(--rule-soft)]">
                  <a href="#data" className="flex items-baseline gap-2 text-ink-faint hover:text-ink transition-colors">
                    <span className="numeral text-xs shrink-0">▦</span>
                    <span>Computed data</span>
                  </a>
                </li>
              )}
              {sensitivityRuns && (
                <li>
                  <a href="#sensitivity-runs" className="flex items-baseline gap-2 text-ink-faint hover:text-ink transition-colors">
                    <span className="numeral text-xs shrink-0">±</span>
                    <span>Sensitivity runs</span>
                  </a>
                </li>
              )}
              {manifest.scripts && manifest.scripts.length > 0 && (
                <li>
                  <a href="#code" className="flex items-baseline gap-2 text-ink-faint hover:text-ink transition-colors">
                    <span className="numeral text-xs shrink-0">{`{·}`}</span>
                    <span>Source code</span>
                  </a>
                </li>
              )}
              {manifest.generated_files.length > 0 && (
                <li>
                  <a href="#downloads" className="flex items-baseline gap-2 text-ink-faint hover:text-ink transition-colors">
                    <span className="numeral text-xs shrink-0">↓</span>
                    <span>Downloads</span>
                  </a>
                </li>
              )}
              <li>
                <a href="#manifest" className="flex items-baseline gap-2 text-ink-faint hover:text-ink transition-colors">
                  <span className="numeral text-xs shrink-0">#</span>
                  <span>Citation</span>
                </a>
              </li>
            </ol>
          </div>
        </aside>

        {/* Main column */}
        <div className="col-span-12 lg:col-span-9 space-y-16">
          {rendered.map((r, i) => (
            <section key={r.meta.key} id={r.meta.key} className="scroll-mt-24">
              <header className="mb-6 pb-4 border-b border-[var(--rule-soft)]">
                <div className="flex items-baseline gap-4 flex-wrap">
                  <Numeral n={i + 1} />
                  <Kicker variant={r.meta.attestation_chain === "ai-first" ? "ochre" : r.meta.attestation_chain === "human-final" ? "sage" : "default"}>
                    {r.meta.label}
                  </Kicker>
                  <span className="font-mono text-[0.66rem] text-ink-faint uppercase tracking-[0.18em] ml-auto">
                    {r.meta.size_human}
                  </span>
                </div>
                <div className="mt-3 marginalia flex items-baseline gap-4 flex-wrap">
                  <span>
                    <code className="font-mono">{r.meta.file}</code>
                  </span>
                  <span>·</span>
                  <span>sha256 <code className="font-mono">{r.meta.sha256.slice(0, 12)}…</code></span>
                  {r.meta.attestation_chain && (
                    <>
                      <span>·</span>
                      <span style={{ color: r.meta.attestation_chain === "ai-first" ? "var(--ochre)" : "var(--sage)" }}>
                        {r.meta.attestation_chain}
                      </span>
                    </>
                  )}
                </div>
              </header>
              <div
                className="prose-article max-w-[68ch]"
                dangerouslySetInnerHTML={{ __html: r.html }}
              />
            </section>
          ))}

          {/* Computed data — JSON rendered as table + chart */}
          {panelData?.rows && Array.isArray(panelData.rows) && panelData.rows.length > 0 && (
            <section id="data" className="scroll-mt-24">
              <header className="mb-6 pb-4 border-b border-[var(--rule-soft)]">
                <Kicker variant="sage">Computed data</Kicker>
                <h2 className="display-md text-[1.6rem] mt-3">{panelData.rows.length} rows from the pipeline</h2>
                <p className="mt-2 marginalia max-w-prose">
                  Rendered directly from <code className="font-mono not-italic">generated/{slug}-adb-panel.json</code>.
                  This is the actual JSON the pipeline produced — every number on this page traces here.
                </p>
              </header>

              {/* Top-12 chart based on the headline numeric column */}
              {(() => {
                const sample = panelData.rows[0] as Record<string, unknown>;
                const numericCols = Object.keys(sample).filter(
                  (k) => typeof sample[k] === "number" && k !== "year" && !k.endsWith("_year"),
                );
                // Pick the column that looks like an index (contains "index" or "score" or "ratio")
                const chartCol =
                  numericCols.find((k) => /index|score|ratio|signal|gap/i.test(k)) ??
                  numericCols[0];
                if (!chartCol) return null;
                const chartRows = (panelData.rows as Record<string, unknown>[])
                  .filter((r) => typeof r[chartCol] === "number")
                  .map((r) => ({
                    label: (r.iso3 as string) || (r.country as string) || "",
                    value: r[chartCol] as number,
                  }))
                  .sort((a, b) => b.value - a.value);
                const top = chartRows.slice(0, 12).map((r, i) => ({ ...r, highlight: i < 5 }));
                if (top.length === 0) return null;
                return (
                  <div className="mb-8">
                    <div className="kicker mb-3">Top-12 by <code className="font-mono not-italic">{chartCol}</code></div>
                    <BarChart data={top} />
                  </div>
                );
              })()}

              <details className="ed-details">
                <summary>
                  <span className="font-mono text-xs uppercase tracking-[0.18em]">▸ Full data table — {panelData.rows.length} rows</span>
                </summary>
                <div className="mt-4">
                  <JsonTable rows={panelData.rows as any[]} maxRows={50} />
                </div>
              </details>
            </section>
          )}

          {/* Sensitivity runs JSON rendered as table */}
          {sensitivityRuns && (
            <section id="sensitivity-runs" className="scroll-mt-24">
              <header className="mb-6 pb-4 border-b border-[var(--rule-soft)]">
                <Kicker variant="ochre">Sensitivity — actual runs</Kicker>
                <h2 className="display-md text-[1.6rem] mt-3">±50% perturbation results</h2>
                <p className="mt-2 marginalia max-w-prose">
                  Rendered from <code className="font-mono not-italic">sensitivity-runs.json</code>.
                  Each row is a single sensitivity-suite run, with the perturbed parameter and the result.
                </p>
              </header>
              {sensitivityRuns.common_top5_across_runs && (
                <div className="mb-4 px-4 py-3 font-mono text-sm" style={{ background: "var(--paper-deep)", borderLeft: "3px solid var(--sage)" }}>
                  <span className="kicker mr-3">Common top-5 across runs:</span>
                  {sensitivityRuns.common_top5_across_runs.length > 0
                    ? sensitivityRuns.common_top5_across_runs.join(", ")
                    : "(empty — gate failed)"}
                </div>
              )}
              {Array.isArray(sensitivityRuns.runs) && sensitivityRuns.runs.length > 0 && (
                <details className="ed-details" open>
                  <summary>
                    <span className="font-mono text-xs uppercase tracking-[0.18em]">▸ {sensitivityRuns.runs.length} sensitivity runs</span>
                  </summary>
                  <div className="mt-4">
                    <JsonTable
                      rows={sensitivityRuns.runs.map((r: any) => {
                        // Strip out nested arrays for cleaner table view
                        const flat: Record<string, unknown> = {};
                        for (const [k, v] of Object.entries(r)) {
                          if (Array.isArray(v)) {
                            flat[k] = v.length > 0 && typeof v[0] === "object"
                              ? `[${v.length} entries]`
                              : v.join(", ");
                          } else {
                            flat[k] = v;
                          }
                        }
                        return flat;
                      })}
                      highlightCols={["label"]}
                    />
                  </div>
                </details>
              )}
            </section>
          )}

          {/* Source code rendered with syntax highlighting */}
          {manifest.scripts && manifest.scripts.length > 0 && (
            <section id="code" className="scroll-mt-24">
              <header className="mb-6 pb-4 border-b border-[var(--rule-soft)]">
                <Kicker>Source code</Kicker>
                <h2 className="display-md text-[1.6rem] mt-3">The pipeline, line-for-line</h2>
                <p className="mt-2 marginalia max-w-prose">
                  Every script that produced the numbers above. Click to expand.
                  All hash-pinned in <code className="font-mono not-italic">manifest.sha256</code>;
                  a clean clone runs them without any API key.
                </p>
              </header>
              <div className="space-y-4">
                {manifest.scripts.map((s: ScriptFile) => {
                  const src = scriptSources[s.file] ?? "";
                  return (
                    <details key={s.file} className="ed-details">
                      <summary>
                        <span className="font-mono text-xs uppercase tracking-[0.18em] mr-3">▸ {s.file}</span>
                        <span className="marginalia">
                          {s.language} · {s.lines.toLocaleString()} lines · {s.size_human} · sha256 <code className="font-mono">{s.sha256.slice(0, 12)}…</code>
                        </span>
                      </summary>
                      <pre className="ed-code mt-4">
                        <code dangerouslySetInnerHTML={{ __html: highlight(src, s.language) }} />
                      </pre>
                    </details>
                  );
                })}
              </div>
            </section>
          )}

          {/* Generated downloads (now after data + code, lower priority) */}
          {manifest.generated_files.length > 0 && (
            <section id="downloads" className="scroll-mt-24">
              <header className="mb-6 pb-4 border-b border-[var(--rule-soft)]">
                <Kicker>Downloads</Kicker>
                <h2 className="display-md text-[1.6rem] mt-3">Raw artifacts</h2>
                <p className="mt-2 marginalia max-w-prose">
                  Pipeline outputs as committed. Hash-pinned in
                  <code className="font-mono not-italic"> manifest.sha256 </code>
                  and reproducible from a clean clone per Constitution §11.
                </p>
              </header>
              <ul className="divide-y divide-[var(--rule-soft)]">
                {manifest.generated_files.map((g) => (
                  <li key={g.file} className="py-3 flex items-baseline gap-4 flex-wrap">
                    <a
                      href={`/programs/${slug}/${g.file}`}
                      download
                      className="ed-link font-mono text-sm"
                    >
                      ↓ {g.file}
                    </a>
                    <span className="marginalia">{g.size_human}</span>
                    <span className="marginalia ml-auto">
                      sha256 <code className="font-mono">{g.sha256.slice(0, 16)}…</code>
                    </span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Manifest hashes */}
          <section id="manifest" className="scroll-mt-24">
            <header className="mb-6 pb-4 border-b border-[var(--rule-soft)]">
              <Kicker>Citation</Kicker>
              <h2 className="display-md text-[1.6rem] mt-3">Cite as</h2>
            </header>
            <pre className="overflow-x-auto" style={{
              background: "var(--ink)",
              color: "var(--paper)",
              padding: "1.4rem 1.6rem",
              fontFamily: "JetBrains Mono, monospace",
              fontSize: "0.78rem",
              lineHeight: 1.7,
            }}>{`Adofina, R. (${new Date().getFullYear()}). ${programTitle} — permanent evidence packet.
The Blindspots Lab.
${typeof window !== "undefined" ? window.location.origin : ""}${manifest.permanent_url}
attestation_chain: ${overall ?? "unknown"}
last refresh: ${new Date(manifest.generated_at).toISOString()}`}</pre>
          </section>

          <Divider wide />

          <nav className="flex items-center justify-between flex-wrap gap-4 pb-12">
            <Link to="/research" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
              ← All programs
            </Link>
            <div className="flex gap-4 flex-wrap">
              {programHref && (
                <Link to={programHref} className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
                  Program detail →
                </Link>
              )}
              {article && (
                <Link to={`/findings/${article.slug}`} className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
                  Read the article →
                </Link>
              )}
            </div>
          </nav>
        </div>
      </div>
    </div>
  );
}
