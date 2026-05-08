/**
 * Topic.tsx — unified topic page.
 *
 * Replaces the previous split between /program/{slug}, /findings/{slug}, and
 * /program/{slug}/evidence with a single page per topic. Tabs (Paper, Brief,
 * Blog, Slides, Data, Evidence) switch the main content; sidebar shows
 * at-a-glance metadata + downloads. URL: /{slug}[?view={tab}].
 */
import { useEffect, useMemo, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { marked } from "marked";
import {
  loadArticleIndex,
  loadArticleBody,
  stripFrontmatter,
  type ArticleMeta,
} from "../lib/articles";
import { loadReferences, byKey, resolveCitations, renderReferenceList } from "../lib/refs";
import { loadEvidenceManifest, type EvidenceManifest } from "../lib/evidence";
import { programs } from "../data/programs";
import { MaturityChip } from "../lib/claimTiers";

marked.setOptions({ gfm: true, breaks: false });

type View = "paper" | "brief" | "blog" | "slides" | "data" | "evidence";

const TIER_TO_VIEW: Record<string, View> = {
  "working-paper": "paper",
  brief: "brief",
  blog: "blog",
  social: "blog", // social card folds into blog tab as "Short version"
  slides: "slides",
};

const TAB_ORDER: View[] = ["paper", "brief", "blog", "slides", "data", "evidence"];
const TAB_LABEL: Record<View, string> = {
  paper: "Paper",
  brief: "Brief",
  blog: "Blog post",
  slides: "Slides",
  data: "Data",
  evidence: "Evidence",
};

function bytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(2)} MB`;
}

export default function Topic() {
  const { slug = "" } = useParams();
  const [search, setSearch] = useSearchParams();
  const view = (search.get("view") as View) || "paper";

  const [tiers, setTiers] = useState<Record<View, ArticleMeta | undefined>>({} as any);
  const [bodyHtml, setBodyHtml] = useState<string>("");
  const [bodyLoading, setBodyLoading] = useState(false);
  const [manifest, setManifest] = useState<EvidenceManifest | null>(null);
  const [missing, setMissing] = useState(false);

  const programEntry = useMemo(
    () => programs.find((p) => p.slug === slug),
    [slug],
  );

  // 1. Load the article index + reference list once and bucket by tier for this slug.
  useEffect(() => {
    let cancelled = false;
    setBodyHtml("");
    setMissing(false);
    (async () => {
      const index = await loadArticleIndex();
      const forSlug = index.filter((a) => a.program === slug);
      if (forSlug.length === 0 && !programEntry) {
        if (!cancelled) setMissing(true);
        return;
      }
      const buckets: Record<View, ArticleMeta | undefined> = {} as any;
      for (const a of forSlug) {
        const v = TIER_TO_VIEW[a.tier as string] || TIER_TO_VIEW[a.kind as string];
        if (v && !buckets[v]) buckets[v] = a;
      }
      if (!cancelled) setTiers(buckets);
    })();
    (async () => {
      const m = await loadEvidenceManifest(slug);
      if (!cancelled) setManifest(m);
    })();
    return () => {
      cancelled = true;
    };
  }, [slug, programEntry]);

  // 2. When the active tab changes, load that tab's markdown body.
  useEffect(() => {
    let cancelled = false;
    setBodyHtml("");
    if (view === "data" || view === "evidence") return; // these tabs render from manifest, not markdown
    if (view === "slides") {
      // Slides tab: short framing + .pptx download. The markdown source is also rendered below.
    }
    const meta = tiers[view];
    if (!meta) return;
    setBodyLoading(true);
    (async () => {
      const [refs, body] = await Promise.all([loadReferences(), loadArticleBody(meta.slug)]);
      if (cancelled) return;
      if (!body) {
        setBodyHtml("");
        setBodyLoading(false);
        return;
      }
      const stripped = stripFrontmatter(body);
      const rendered = await marked.parse(stripped);
      const raw = typeof rendered === "string" ? rendered : "";
      const refIndex = byKey(refs);
      const { html: resolved, cited } = resolveCitations(raw, refIndex);
      const finalHtml = resolved + renderReferenceList(cited);
      if (!cancelled) {
        setBodyHtml(finalHtml);
        setBodyLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [view, tiers]);

  function setView(v: View) {
    const next = new URLSearchParams(search);
    if (v === "paper") next.delete("view");
    else next.set("view", v);
    setSearch(next, { replace: true });
  }

  if (missing) {
    return (
      <div className="py-16 text-center">
        <div className="text-xs uppercase tracking-[0.2em] text-ink-500">404</div>
        <h1 className="mt-3 text-2xl font-semibold">No topic at /{slug}</h1>
        <Link to="/" className="mt-6 inline-block text-sm underline underline-offset-4">
          ← Back to all topics
        </Link>
      </div>
    );
  }

  const paper = tiers.paper;
  const title = paper?.title || programEntry?.title || slug;
  const subtitle = paper?.subtitle || programEntry?.summary || "";
  const status = (paper?.maturity as any) || programEntry?.status || "H";
  const attestation = paper?.attestation_chain || "ai-first";
  const authors = paper?.authors || ["Raymond Adofina"];
  const published = paper?.published_at;
  const updated = paper?.updated_at;
  const availableTabs = new Set<View>(["paper", "data", "evidence"]);
  if (tiers.brief) availableTabs.add("brief");
  if (tiers.blog) availableTabs.add("blog");
  if (tiers.slides) availableTabs.add("slides");

  return (
    <article className="topic-page">
      {/* Header */}
      <header className="border-b border-ink-200 pb-8 mb-8">
        <Link
          to="/"
          className="inline-block text-xs uppercase tracking-[0.2em] text-ink-500 hover:text-ink-700"
        >
          ← All topics
        </Link>
        <h1 className="mt-4 text-3xl md:text-4xl font-semibold tracking-tight max-w-4xl leading-tight">
          {title}
        </h1>
        {subtitle && (
          <p className="mt-4 text-ink-600 leading-relaxed max-w-3xl">{subtitle}</p>
        )}
        <div className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-ink-500">
          <MaturityChip status={status} />
          <span>·</span>
          <span>
            attestation: <code className="font-mono">{attestation}</code>
          </span>
          {updated && (
            <>
              <span>·</span>
              <span>updated {updated}</span>
            </>
          )}
          {authors.length > 0 && (
            <>
              <span>·</span>
              <span>{authors.join(", ")}</span>
            </>
          )}
        </div>
      </header>

      {/* Tab strip */}
      <nav className="topic-tabs mb-8 flex flex-wrap gap-1 border-b border-ink-200">
        {TAB_ORDER.filter((t) => availableTabs.has(t)).map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => setView(t)}
            className={
              "py-3 px-4 text-sm font-medium transition-colors -mb-px border-b-2 " +
              (view === t
                ? "border-ink-900 text-ink-900"
                : "border-transparent text-ink-500 hover:text-ink-700 hover:border-ink-300")
            }
          >
            {TAB_LABEL[t]}
          </button>
        ))}
      </nav>

      {/* Two-column layout. min-w-0 on grid items lets them shrink below
           their content's intrinsic width on narrow viewports — without
           it, a long inline code path or a wide image makes the column
           overflow the viewport. */}
      <div className="topic-grid grid gap-10 lg:grid-cols-[minmax(0,1fr)_320px]">
        {/* Main content */}
        <main className="min-w-0">
          {view === "paper" || view === "brief" || view === "blog" ? (
            bodyLoading ? (
              <div className="py-12 text-ink-500 text-sm">Loading…</div>
            ) : bodyHtml ? (
              <div
                className="prose-article max-w-[68ch]"
                dangerouslySetInnerHTML={{ __html: bodyHtml }}
              />
            ) : (
              <div className="py-12 text-ink-500 text-sm">
                No {TAB_LABEL[view].toLowerCase()} version yet for this topic.
              </div>
            )
          ) : null}

          {view === "slides" && (
            <SlidesTab slug={slug} sourceMeta={tiers.slides} bodyHtml={bodyHtml} bodyLoading={bodyLoading} />
          )}

          {view === "data" && <DataTab manifest={manifest} slug={slug} />}

          {view === "evidence" && <EvidenceTab manifest={manifest} slug={slug} />}
        </main>

        {/* Sidebar */}
        <aside className="topic-sidebar text-sm">
          <Sidebar
            slug={slug}
            tiers={tiers}
            manifest={manifest}
            published={published}
            updated={updated}
            attestation={attestation}
          />
        </aside>
      </div>
    </article>
  );
}

function SlidesTab({
  slug,
  sourceMeta,
  bodyHtml,
  bodyLoading,
}: {
  slug: string;
  sourceMeta: ArticleMeta | undefined;
  bodyHtml: string;
  bodyLoading: boolean;
}) {
  const pptxUrl = `/programs/${slug}/${slug}-deck.pptx`;
  return (
    <div>
      <div className="border border-ink-200 bg-paper-50 p-6 mb-6">
        <h2 className="text-lg font-semibold mb-2">Slide deck (.pptx)</h2>
        <p className="text-sm text-ink-600 leading-relaxed">
          The deck is built deterministically from the markdown source via
          Quarto. Charts are regenerated from the same CSVs the working paper
          cites — so the slide chart cannot drift from the paper's chart.
        </p>
        <a
          href={pptxUrl}
          download
          className="mt-4 inline-block rounded border border-ink-900 bg-ink-900 text-paper px-4 py-2 text-sm font-medium hover:bg-ink-700"
        >
          Download {slug}-deck.pptx
        </a>
      </div>
      {sourceMeta && (
        <div>
          <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-3">
            Markdown source
          </div>
          {bodyLoading ? (
            <div className="py-12 text-ink-500 text-sm">Loading…</div>
          ) : (
            <div
              className="prose-article max-w-[68ch]"
              dangerouslySetInnerHTML={{ __html: bodyHtml }}
            />
          )}
        </div>
      )}
    </div>
  );
}

function DataTab({ manifest, slug }: { manifest: EvidenceManifest | null; slug: string }) {
  if (!manifest) {
    return <div className="py-12 text-ink-500 text-sm">Loading data…</div>;
  }
  const files = manifest.generated_files || [];
  if (files.length === 0) {
    return <div className="py-12 text-ink-500 text-sm">No generated data files for this topic.</div>;
  }
  // Bucket: charts vs CSVs vs JSON
  const charts = files.filter((f) => f.file.includes("/charts/"));
  const csvs = files.filter((f) => f.file.endsWith(".csv"));
  const jsons = files.filter((f) => f.file.endsWith(".json"));
  const other = files.filter(
    (f) => !charts.includes(f) && !csvs.includes(f) && !jsons.includes(f),
  );
  const Section = ({ label, items }: { label: string; items: typeof files }) =>
    items.length > 0 ? (
      <section className="mb-8">
        <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-3">{label}</div>
        <ul className="space-y-1.5">
          {items.map((f) => (
            <li key={f.file} className="text-sm">
              <a
                href={`/programs/${slug}/${f.file}`}
                download
                className="text-ink-900 underline underline-offset-4 hover:text-crimson font-mono text-xs"
              >
                {f.file}
              </a>
              <span className="ml-2 text-ink-500">{f.size_human}</span>
            </li>
          ))}
        </ul>
      </section>
    ) : null;
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-2">Generated data and charts</h2>
      <p className="text-sm text-ink-600 mb-8 max-w-prose">
        Every file below is a deterministic output of a committed script.
        Click to download. The full audit trail (manifest, SHA-256 hashes,
        retrieval timestamps) is on the Evidence tab.
      </p>
      <Section label="Charts" items={charts} />
      <Section label="CSVs" items={csvs} />
      <Section label="JSON" items={jsons} />
      <Section label="Other" items={other} />
    </div>
  );
}

function EvidenceTab({ manifest, slug }: { manifest: EvidenceManifest | null; slug: string }) {
  if (!manifest) {
    return <div className="py-12 text-ink-500 text-sm">Loading evidence packet…</div>;
  }
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-2">Evidence packet</h2>
      <p className="text-sm text-ink-600 mb-6 max-w-prose">
        The full reproducibility bundle: every artifact, every script, every
        generated file, with SHA-256 hashes. A reviewer can reproduce the
        result from a clean clone using the runbook below.
      </p>
      <div className="grid sm:grid-cols-2 gap-4 mb-8">
        <a
          href={`/_archive/review-packets/${slug}-2026-05-07.zip`}
          download
          className="block rounded border border-ink-300 hover:border-ink-900 p-4 transition-colors"
        >
          <div className="text-xs uppercase tracking-[0.18em] text-ink-500">Reviewer packet</div>
          <div className="mt-1 font-medium">Download .zip</div>
          <div className="mt-1 text-xs text-ink-500">~6 MB · all 7 tiers + governance</div>
        </a>
        <a
          href={`/programs/${slug}/${slug}-deck.pptx`}
          download
          className="block rounded border border-ink-300 hover:border-ink-900 p-4 transition-colors"
        >
          <div className="text-xs uppercase tracking-[0.18em] text-ink-500">Slide deck</div>
          <div className="mt-1 font-medium">Download .pptx</div>
          <div className="mt-1 text-xs text-ink-500">ADB internal format</div>
        </a>
      </div>
      <section className="mb-8">
        <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-3">
          Documentation files
        </div>
        <ul className="space-y-1.5">
          {(manifest.artifacts || []).map((a) => (
            <li key={a.key} className="text-sm">
              <a
                href={`/programs/${slug}/${a.file}`}
                target="_blank"
                rel="noreferrer"
                className="text-ink-900 underline underline-offset-4 hover:text-crimson font-mono text-xs"
              >
                {a.file}
              </a>
              <span className="ml-2 text-ink-500">{a.label} · {a.size_human}</span>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-2">Permanent URL</div>
        <code className="font-mono text-sm break-all">
          {manifest.permanent_url}
        </code>
      </section>
    </div>
  );
}

function Sidebar({
  slug,
  tiers,
  manifest,
  published,
  updated,
  attestation,
}: {
  slug: string;
  tiers: Record<View, ArticleMeta | undefined>;
  manifest: EvidenceManifest | null;
  published?: string;
  updated?: string;
  attestation: string;
}) {
  return (
    <div className="space-y-6 lg:sticky lg:top-6">
      <section>
        <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-2">At a glance</div>
        <dl className="text-sm space-y-2">
          {published && (
            <div className="flex justify-between gap-3">
              <dt className="text-ink-500">Published</dt>
              <dd className="font-mono">{published}</dd>
            </div>
          )}
          {updated && (
            <div className="flex justify-between gap-3">
              <dt className="text-ink-500">Updated</dt>
              <dd className="font-mono">{updated}</dd>
            </div>
          )}
          <div className="flex justify-between gap-3">
            <dt className="text-ink-500">Attestation</dt>
            <dd className="font-mono">{attestation}</dd>
          </div>
        </dl>
      </section>

      <section>
        <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-2">Available formats</div>
        <ul className="text-sm space-y-1">
          {tiers.paper && <li>Working paper</li>}
          {tiers.brief && <li>One-page brief</li>}
          {tiers.blog && <li>Blog post</li>}
          {tiers.slides && (
            <li>
              Slide deck —{" "}
              <a
                href={`/programs/${slug}/${slug}-deck.pptx`}
                download
                className="underline underline-offset-4 hover:text-crimson"
              >
                .pptx
              </a>
            </li>
          )}
        </ul>
      </section>

      {manifest && (manifest.generated_files || []).length > 0 && (
        <section>
          <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-2">Top data files</div>
          <ul className="text-xs space-y-1">
            {(manifest.generated_files || [])
              .filter((f) => f.file.endsWith(".csv") || f.file.endsWith(".json"))
              .slice(0, 5)
              .map((f) => (
                <li key={f.file}>
                  <a
                    href={`/programs/${slug}/${f.file}`}
                    download
                    className="font-mono text-ink-700 underline underline-offset-4 hover:text-crimson break-all"
                  >
                    {f.file.replace(/^generated\//, "")}
                  </a>
                </li>
              ))}
            {(manifest.generated_files || []).length > 5 && (
              <li>
                <Link
                  to={`/${slug}?view=data`}
                  className="text-ink-500 underline underline-offset-4"
                >
                  All {manifest.generated_files.length} →
                </Link>
              </li>
            )}
          </ul>
        </section>
      )}

      <section>
        <div className="text-xs uppercase tracking-[0.18em] text-ink-500 mb-2">Reproduce</div>
        <ul className="text-xs space-y-1">
          <li>
            <a
              href={`/programs/${slug}/REPRODUCE.md`}
              target="_blank"
              rel="noreferrer"
              className="text-ink-700 underline underline-offset-4 font-mono"
            >
              REPRODUCE.md
            </a>
          </li>
          <li>
            <a
              href={`https://github.com/rradofina/adb-research-reporting/tree/main/${slug}`}
              target="_blank"
              rel="noreferrer"
              className="text-ink-700 underline underline-offset-4 font-mono"
            >
              {slug}/ on GitHub
            </a>
          </li>
        </ul>
      </section>
    </div>
  );
}
