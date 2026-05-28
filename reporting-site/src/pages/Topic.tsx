/**
 * Topic.tsx — unified topic page.
 *
 * Replaces the previous split between /program/{slug}, /findings/{slug}, and
 * /program/{slug}/evidence with a single page per topic. Tabs (Paper, Brief,
 * Blog, Slides, Data, Evidence) switch the main content; sidebar shows
 * at-a-glance metadata + downloads. URL: /{slug}[?view={tab}].
 */
import { useEffect, useMemo, useRef, useState } from "react";
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
import { RemittanceMapHero } from "../components/charts/RemittanceMapHero";

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

  // Per-(slug, view) HTML cache so re-clicking a tab is instant and the
  // previously-shown content stays visible while the new tab fetches.
  // Stored in a ref so cache hits do not re-render the parent.
  const bodyCache = useRef<Map<string, string>>(new Map());
  const cacheKey = (slug: string, view: View) => `${slug}::${view}`;

  const programEntry = useMemo(
    () => programs.find((p) => p.slug === slug),
    [slug],
  );

  // 1. Load the article index + evidence manifest for this slug.
  // Tier metadata only — does NOT touch bodyHtml, so a slug-stable
  // re-render (e.g. StrictMode double-mount) cannot blank the visible
  // content.
  useEffect(() => {
    let cancelled = false;
    setMissing(false);
    bodyCache.current.clear();
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

  // 2. When the active tab changes, load that tab's markdown body if
  // not cached. The previous tab's HTML stays in bodyHtml until the new
  // body is ready — no flash to a blank/loading state on tab switch.
  useEffect(() => {
    if (view === "data" || view === "evidence") {
      // These tabs render from manifest, not markdown.
      setBodyHtml("");
      setBodyLoading(false);
      return;
    }
    const meta = tiers[view];
    if (!meta) {
      setBodyHtml("");
      setBodyLoading(false);
      return;
    }
    const key = cacheKey(slug, view);
    const cached = bodyCache.current.get(key);
    if (cached !== undefined) {
      // Cache hit: snap to the cached HTML, no async work, no flash.
      setBodyHtml(cached);
      setBodyLoading(false);
      return;
    }

    let cancelled = false;
    setBodyLoading(true);
    (async () => {
      const [refs, body] = await Promise.all([loadReferences(), loadArticleBody(meta.slug)]);
      if (cancelled) return;
      if (!body) {
        bodyCache.current.set(key, "");
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
      bodyCache.current.set(key, finalHtml);
      if (!cancelled) {
        setBodyHtml(finalHtml);
        setBodyLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [slug, view, tiers]);

  function setView(v: View) {
    const next = new URLSearchParams(search);
    if (v === "paper") next.delete("view");
    else next.set("view", v);
    setSearch(next, { replace: true });
  }

  if (missing) {
    return (
      <div className="not-found-page">
        <div className="not-found-code">404</div>
        <h1 className="not-found-title">No topic at /{slug}</h1>
        <Link to="/" className="not-found-link">
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
      <header className="topic-header">
        <Link
          to="/"
          className="topic-back-link"
        >
          ← All topics
        </Link>
        <h1 className="topic-title-page">
          {title}
        </h1>
        {subtitle && (
          <p className="topic-subtitle">{subtitle}</p>
        )}
        <div className="topic-meta">
          <MaturityChip status={status} />
          <span>·</span>
          <span>
            attestation: <code className="inline-code-token">{attestation}</code>
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

      {/* Hero visual (visual-first refactor, 2026-05-19). When the
          program has a rendered hero, show it above the tab strip. The
          same image users clicked from the home gallery. */}
      {manifest?.hero &&
        (() => {
          const hero = manifest.hero;
          const pngHero = (
            <figure className="topic-hero">
              <img
                src={`/programs/${slug}/${hero.png}`}
                alt={hero.title}
                width={hero.dimensions?.width || 1600}
                height={hero.dimensions?.height || 900}
                loading="eager"
              />
              <figcaption className="topic-hero-caption">
                <span className="topic-hero-caption-text">{hero.caption}</span>
                <span className="topic-hero-caption-meta">
                  <span>{hero.visual_form}</span>
                  <span>·</span>
                  <span>{hero.source}</span>
                  <span>·</span>
                  <span>
                    attestation:{" "}
                    <code className="inline-code-token">
                      {hero.attestation_chain}
                    </code>
                  </span>
                </span>
              </figcaption>
            </figure>
          );
          // Remittance flagship: render the native interactive map in place
          // of the static PNG (PNG remains the fallback while data loads).
          return slug === "remittance-resilience" ? (
            <RemittanceMapHero hero={hero} fallback={pngHero} />
          ) : (
            pngHero
          );
        })()}

      {/* Tab strip */}
      <nav className="topic-tabs">
        {TAB_ORDER.filter((t) => availableTabs.has(t)).map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => setView(t)}
            className={
              "topic-tab " + (view === t ? "topic-tab-active" : "")
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
      <div className="topic-grid">
        {/* Main content */}
        <main className="topic-main">
          {view === "paper" || view === "brief" || view === "blog" ? (
            // Render any current bodyHtml even while loading — keeps the
            // previous tab's content visible until the new one is ready,
            // so tab switching does not flash to a blank state.
            bodyHtml ? (
              <div
                className={
                  "prose-article topic-body-narrow " +
                  (bodyLoading ? "topic-body-pending" : "")
                }
                dangerouslySetInnerHTML={{ __html: bodyHtml }}
              />
            ) : bodyLoading ? (
              <div className="loading-message">Loading…</div>
            ) : (
              <div className="loading-message">
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
        <aside className="topic-sidebar">
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
      <div className="topic-panel">
        <h2 className="topic-panel-title">Slide deck (.pptx)</h2>
        <p className="topic-panel-copy">
          The deck is built deterministically from the markdown source via
          Quarto. Charts are regenerated from the same CSVs the working paper
          cites — so the slide chart cannot drift from the paper's chart.
        </p>
        <a
          href={pptxUrl}
          download
          className="download-button"
        >
          Download {slug}-deck.pptx
        </a>
      </div>
      {sourceMeta && (
        <div>
          <div className="topic-section-label">
            Markdown source
          </div>
          {bodyHtml ? (
            <div
              className={
                "prose-article topic-body-narrow " +
                (bodyLoading ? "topic-body-pending" : "")
              }
              dangerouslySetInnerHTML={{ __html: bodyHtml }}
            />
          ) : bodyLoading ? (
            <div className="loading-message">Loading…</div>
          ) : null}
        </div>
      )}
    </div>
  );
}

function DataTab({ manifest, slug }: { manifest: EvidenceManifest | null; slug: string }) {
  if (!manifest) {
    return <div className="loading-message">Loading data…</div>;
  }
  const files = manifest.generated_files || [];
  if (files.length === 0) {
    return <div className="loading-message">No generated data files for this topic.</div>;
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
      <section className="topic-section">
        <div className="topic-section-label">{label}</div>
        <ul className="file-list">
          {items.map((f) => (
            <li key={f.file} className="file-list-item">
              <a
                href={`/programs/${slug}/${f.file}`}
                download
                className="file-link"
              >
                {f.file}
              </a>
              <span className="file-size">{f.size_human}</span>
            </li>
          ))}
        </ul>
      </section>
    ) : null;
  return (
    <div>
      <h2 className="content-title">Generated data and charts</h2>
      <p className="content-copy">
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
    return <div className="loading-message">Loading evidence packet…</div>;
  }
  return (
    <div>
      <h2 className="content-title">Evidence packet</h2>
      <p className="content-copy">
        The full reproducibility bundle: every artifact, every script, every
        generated file, with SHA-256 hashes. A reviewer can reproduce the
        result from a clean clone using the runbook below.
      </p>
      <div className="resource-grid">
        <a
          href={`/_archive/review-packets/${slug}-2026-05-07.zip`}
          download
          className="resource-card"
        >
          <div className="topic-section-label">Reviewer packet</div>
          <div className="resource-title">Download .zip</div>
          <div className="resource-note">~6 MB · all 7 tiers + governance</div>
        </a>
        <a
          href={`/programs/${slug}/${slug}-deck.pptx`}
          download
          className="resource-card"
        >
          <div className="topic-section-label">Slide deck</div>
          <div className="resource-title">Download .pptx</div>
          <div className="resource-note">ADB internal format</div>
        </a>
      </div>
      <section className="topic-section">
        <div className="topic-section-label">
          Documentation files
        </div>
        <ul className="file-list">
          {(manifest.artifacts || []).map((a) => (
            <li key={a.key} className="file-list-item">
              <a
                href={`/programs/${slug}/${a.file}`}
                target="_blank"
                rel="noreferrer"
                className="file-link"
              >
                {a.file}
              </a>
              <span className="file-size">{a.label} · {a.size_human}</span>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <div className="topic-section-label">Permanent URL</div>
        <code className="permanent-url">
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
    <div className="sidebar-stack">
      <section>
        <div className="sidebar-label">At a glance</div>
        <dl className="sidebar-list">
          {published && (
            <div className="sidebar-row">
              <dt>Published</dt>
              <dd>{published}</dd>
            </div>
          )}
          {updated && (
            <div className="sidebar-row">
              <dt>Updated</dt>
              <dd>{updated}</dd>
            </div>
          )}
          <div className="sidebar-row">
            <dt>Attestation</dt>
            <dd>{attestation}</dd>
          </div>
        </dl>
      </section>

      <section>
        <div className="sidebar-label">Available formats</div>
        <ul className="sidebar-list">
          {tiers.paper && <li>Working paper</li>}
          {tiers.brief && <li>One-page brief</li>}
          {tiers.blog && <li>Blog post</li>}
          {tiers.slides && (
            <li>
              Slide deck —{" "}
              <a
                href={`/programs/${slug}/${slug}-deck.pptx`}
                download
                className="token-link"
              >
                .pptx
              </a>
            </li>
          )}
        </ul>
      </section>

      {manifest && (manifest.generated_files || []).length > 0 && (
        <section>
          <div className="sidebar-label">Top data files</div>
          <ul className="sidebar-data-list">
            {(manifest.generated_files || [])
              .filter((f) => f.file.endsWith(".csv") || f.file.endsWith(".json"))
              .slice(0, 5)
              .map((f) => (
                <li key={f.file}>
                  <a
                    href={`/programs/${slug}/${f.file}`}
                    download
                    className="file-link"
                  >
                    {f.file.replace(/^generated\//, "")}
                  </a>
                </li>
              ))}
            {(manifest.generated_files || []).length > 5 && (
              <li>
                <Link
                  to={`/${slug}?view=data`}
                  className="token-link"
                >
                  All {manifest.generated_files.length} →
                </Link>
              </li>
            )}
          </ul>
        </section>
      )}

      <section>
        <div className="sidebar-label">Reproduce</div>
        <ul className="sidebar-data-list">
          <li>
            <a
              href={`/programs/${slug}/REPRODUCE.md`}
              target="_blank"
              rel="noreferrer"
              className="file-link"
            >
              REPRODUCE.md
            </a>
          </li>
          <li>
            <a
              href={`https://github.com/rradofina/adb-research-reporting/tree/main/${slug}`}
              target="_blank"
              rel="noreferrer"
              className="file-link"
            >
              {slug}/ on GitHub
            </a>
          </li>
        </ul>
      </section>
    </div>
  );
}
