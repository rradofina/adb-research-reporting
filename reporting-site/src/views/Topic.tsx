"use client";

/**
 * Topic.tsx — unified topic page.
 *
 * Replaces the previous split between /program/{slug}, /findings/{slug}, and
 * /program/{slug}/evidence with a single page per topic. Tabs (Overview,
 * Paper, Brief, Blog, Slides, Data, Evidence) switch the main content; sidebar shows
 * at-a-glance metadata + downloads. URL: /{slug}[?view={tab}].
 */
import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { marked } from "marked";
import {
  loadArticleIndex,
  loadArticleBody,
  stripFrontmatter,
  type ArticleMeta,
} from "../lib/articles";
import { loadReferences, byKey, resolveCitations, renderReferenceList } from "../lib/refs";
import {
  loadArtifact,
  loadEvidenceManifest,
  type EvidenceManifest,
  type HeroVisual,
  type ResearchStorySection,
} from "../lib/evidence";
import { programs } from "../data/programs";
import { MaturityChip } from "../lib/claimTiers";
import { RemittanceMapHero } from "../components/charts/RemittanceMapHero";

marked.setOptions({ gfm: true, breaks: false });

type View = "overview" | "paper" | "brief" | "blog" | "slides" | "data" | "evidence";

const TIER_TO_VIEW: Record<string, View> = {
  "working-paper": "paper",
  brief: "brief",
  blog: "blog",
  social: "blog", // social card folds into blog tab as "Short version"
  slides: "slides",
};

const TAB_ORDER: View[] = ["overview", "paper", "brief", "blog", "slides", "data", "evidence"];
const TAB_LABEL: Record<View, string> = {
  overview: "Overview",
  paper: "Research",
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

function isView(value: string | null): value is View {
  return !!value && TAB_ORDER.includes(value as View);
}

export default function Topic({ slug }: { slug: string }) {
  const router = useRouter();
  const search = useSearchParams();
  const requestedView = isView(search?.get("view")) ? (search?.get("view") as View) : null;

  const [tiers, setTiers] = useState<Record<View, ArticleMeta | undefined>>({} as any);
  const [bodyHtml, setBodyHtml] = useState<string>("");
  const [bodyLoading, setBodyLoading] = useState(false);
  const [manifest, setManifest] = useState<EvidenceManifest | null>(null);
  const [missing, setMissing] = useState(false);
  const [metadataLoaded, setMetadataLoaded] = useState(false);

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
    setMetadataLoaded(false);
    bodyCache.current.clear();
    (async () => {
      const [index, m] = await Promise.all([loadArticleIndex(), loadEvidenceManifest(slug)]);
      const forSlug = index.filter((a) => a.program === slug);
      if (forSlug.length === 0 && !programEntry) {
        if (!cancelled) {
          setMissing(true);
          setMetadataLoaded(true);
        }
        return;
      }
      const buckets: Record<View, ArticleMeta | undefined> = {} as any;
      for (const a of forSlug) {
        const v = TIER_TO_VIEW[a.tier as string] || TIER_TO_VIEW[a.kind as string];
        if (v && !buckets[v]) buckets[v] = a;
      }
      if (!cancelled) {
        setTiers(buckets);
        setManifest(m);
        setMetadataLoaded(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [slug, programEntry]);

  const paper = tiers.paper;
  const title = paper?.title || programEntry?.title || slug;
  const subtitle = paper?.subtitle || programEntry?.summary || "";
  // The constitutional register is authoritative. Article frontmatter is
  // descriptive metadata and must never silently promote a public page.
  const status = programEntry?.status || (paper?.maturity as any) || "H";
  const attestation = paper?.attestation_chain || "ai-first";
  const authors = (paper?.authors || ["Raymond Adofina"]).map((author) =>
    author.replace(/^\{\s*name:\s*([^,}]+).*\}$/, "$1").trim(),
  );
  const published = paper?.published_at;
  const updated = paper?.updated_at;
  const availableTabs = new Set<View>();
  if (!metadataLoaded) {
    availableTabs.add("paper");
  } else {
    if (programEntry && !tiers.paper) availableTabs.add("overview");
    if (tiers.paper || manifest?.story?.some((section) => section.available)) availableTabs.add("paper");
    if (tiers.brief) availableTabs.add("brief");
    if (tiers.blog) availableTabs.add("blog");
    if (manifest?.resources?.deck) availableTabs.add("slides");
    if ((manifest?.generated_files || []).length > 0) availableTabs.add("data");
    if (manifest && ((manifest.artifacts || []).length > 0 || (manifest.scripts || []).length > 0)) {
      availableTabs.add("evidence");
    }
    if (availableTabs.size === 0) availableTabs.add("overview");
  }
  const defaultView: View = !metadataLoaded
    ? "paper"
    : tiers.paper || manifest?.story?.some((section) => section.available)
      ? "paper"
      : manifest && ((manifest.artifacts || []).length > 0 || (manifest.generated_files || []).length > 0)
        ? "evidence"
        : "overview";
  const view: View = requestedView && availableTabs.has(requestedView) ? requestedView : defaultView;

  // 2. When the active tab changes, load that tab's markdown body if
  // not cached. The previous tab's HTML stays in bodyHtml until the new
  // body is ready — no flash to a blank/loading state on tab switch.
  useEffect(() => {
    if (view === "overview" || view === "data" || view === "evidence") {
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
      // Quarto consumes standalone image sizing attributes such as
      // `{width=91%}` when it builds the PPTX. Strip those generated layout
      // tokens from the browser-only slide source before Marked attaches them
      // to the image paragraph as visible text.
      const previewSource = view === "slides"
        ? stripped.replace(/\{(?:width|height)=[^}]+\}\s*$/gm, "")
        : stripped;
      const rendered = await marked.parse(previewSource);
      const raw = typeof rendered === "string" ? rendered : "";
      // Quarto slide sources use paths relative to articles/_slides so the
      // PPTX builder can read local chart files. In the topic route those same
      // paths would resolve under /<program>/generated and break. Normalize
      // them only for the slide-source preview; the markdown and deck build
      // keep their deterministic local paths.
      const webReady = view === "slides"
        ? raw
            .replace(
              /src="\.\.\/\.\.\/([^/]+)\/generated\//g,
              'src="/programs/$1/generated/',
            )
        : raw;
      const refIndex = byKey(refs);
      const { html: resolved, cited } = resolveCitations(webReady, refIndex);
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

  if (missing) {
    return (
      <div className="not-found-page">
        <div className="not-found-code">404</div>
        <h1 className="not-found-title">No topic at /{slug}</h1>
        <Link href="/" className="not-found-link">
          ← Back to all topics
        </Link>
      </div>
    );
  }

  function setView(v: View) {
    const next = new URLSearchParams(search?.toString() ?? "");
    if (v === defaultView) next.delete("view");
    else next.set("view", v);
    const query = next.toString();
    router.replace(query ? `/${slug}?${query}` : `/${slug}`, { scroll: false });
  }

  return (
    <article className="topic-page">
      {/* Header */}
      <header className="topic-header">
        <Link href="/"
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

      {view === "paper" && manifest?.story ? (
        <ResearchPackageIndex story={manifest.story} />
      ) : null}

      {/* Two-column layout. min-w-0 on grid items lets them shrink below
           their content's intrinsic width on narrow viewports — without
           it, a long inline code path or a wide image makes the column
           overflow the viewport. */}
      <div className="topic-grid">
        {/* Main content */}
        <main className="topic-main">
          {view === "overview" && (
            <OverviewTab
              program={programEntry}
              manifest={manifest}
              slug={slug}
              hasPaper={!!tiers.paper}
            />
          )}

          {view === "paper" ? (
            <ResearchStory
              slug={slug}
              manifest={manifest}
              hero={manifest?.hero || null}
              summaryHtml={bodyHtml}
              summaryLoading={bodyLoading}
            />
          ) : view === "brief" || view === "blog" ? (
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
            ) : !metadataLoaded ? (
              <div className="loading-message">Loading topic…</div>
            ) : (
              <div className="loading-message">
                No {TAB_LABEL[view].toLowerCase()} version yet for this topic.
              </div>
            )
          ) : null}

          {view === "slides" && (
            <SlidesTab
              slug={slug}
              pptxUrl={manifest?.resources?.deck || null}
              sourceMeta={tiers.slides}
              bodyHtml={bodyHtml}
              bodyLoading={bodyLoading}
            />
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

interface LoadedStorySection extends ResearchStorySection {
  html: string;
}

function TopicHeroFigure({ slug, hero }: { slug: string; hero: HeroVisual }) {
  const pngHero = (
    <figure className="topic-hero research-inline-figure">
      <Image
        src={`/programs/${slug}/${hero.png}`}
        alt={hero.title}
        width={hero.dimensions?.width || 1600}
        height={hero.dimensions?.height || 900}
        priority
      />
      <figcaption className="topic-hero-caption">
        <span className="topic-hero-caption-text">{hero.caption}</span>
        <span className="topic-hero-caption-meta">
          <span>{hero.visual_form}</span>
          <span>·</span>
          <span>{hero.source}</span>
          <span>·</span>
          <span>
            attestation: <code className="inline-code-token">{hero.attestation_chain}</code>
          </span>
        </span>
      </figcaption>
    </figure>
  );

  return slug === "remittance-resilience" ? (
    <RemittanceMapHero hero={hero} fallback={pngHero} />
  ) : (
    pngHero
  );
}

function splitNarrativeForHero(html: string) {
  const resultsHeading = /<h([12])(?:\s[^>]*)?>\s*(?:Results|Findings|The finding|Main result)\s*<\/h\1>/i.exec(html);
  if (resultsHeading?.index !== undefined) {
    const splitAt = resultsHeading.index + resultsHeading[0].length;
    return { before: html.slice(0, splitAt), after: html.slice(splitAt) };
  }
  const openingParagraph = html.indexOf("</p>");
  if (openingParagraph >= 0) {
    const splitAt = openingParagraph + 4;
    return { before: html.slice(0, splitAt), after: html.slice(splitAt) };
  }
  return { before: "", after: html };
}

function ResearchPackageIndex({ story }: { story: ResearchStorySection[] }) {
  const availableCount = story.filter((section) => section.available).length;
  const completeCount = story.filter((section) => section.state === "present").length;
  return (
    <section className="research-story-status" aria-labelledby="research-package-title">
      <div>
        <div className="topic-section-label">Research package</div>
        <h2 id="research-package-title">The full evidence spine, with gaps left visible.</h2>
        <p>
          {availableCount} of {story.length} standard sections have a file; {completeCount} contain no template markers.
          The article, chart, method, literature, limitations, and reproduction trail are kept in one reader journey.
        </p>
      </div>
      <ol aria-label="Research section availability">
        {story.map((section) => (
          <li key={section.key} className={section.state === "present" ? "is-available" : section.available ? "is-draft" : "is-missing"}>
            <a href={`#research-${section.key}`}>{section.title}</a>
            <span>{section.state === "present" ? "Present" : section.available ? "Draft" : "Not yet"}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}

function ResearchStory({
  slug,
  manifest,
  hero,
  summaryHtml,
  summaryLoading,
}: {
  slug: string;
  manifest: EvidenceManifest | null;
  hero: HeroVisual | null;
  summaryHtml: string;
  summaryLoading: boolean;
}) {
  const [sections, setSections] = useState<LoadedStorySection[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    const story = manifest?.story || [];
    if (!manifest) {
      setLoading(true);
      return;
    }
    (async () => {
      setLoading(true);
      const refs = await loadReferences();
      const refIndex = byKey(refs);
      const loaded = await Promise.all(
        story.map(async (section) => {
          const documents = await Promise.all(
            section.artifacts.map(async (artifact) => {
              const source = await loadArtifact(slug, artifact.file);
              if (!source) return "";
              const withoutFrontmatter = stripFrontmatter(source)
                .replace(/^#\s+[^\r\n]+\r?\n+/, "")
                .trim();
              const rendered = await marked.parse(withoutFrontmatter);
              const raw = typeof rendered === "string" ? rendered : "";
              // Program story artifacts keep generated figures relative to
              // the program directory so they remain portable in the repo.
              // Resolve those paths against the public program mount here.
              const webReady = raw.replace(
                /src="generated\//g,
                `src="/programs/${slug}/generated/`,
              );
              const { html, cited } = resolveCitations(webReady, refIndex);
              return `<div class="research-story-document">${html}${renderReferenceList(cited)}</div>`;
            }),
          );
          return { ...section, html: documents.filter(Boolean).join("") };
        }),
      );
      if (!cancelled) {
        setSections(loaded);
        setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [manifest, slug]);

  if (!manifest || loading) {
    return <div className="loading-message">Loading the research package…</div>;
  }

  const narrative = summaryHtml ? splitNarrativeForHero(summaryHtml) : null;
  const heroIsInNarrative = Boolean(hero && narrative);

  return (
    <div className="research-story">
      {narrative ? (
        <section className="research-story-section" id="research-summary">
          <div className="topic-section-label">Research summary</div>
          <div
            className={"prose-article topic-body-narrow " + (summaryLoading ? "topic-body-pending" : "")}
            dangerouslySetInnerHTML={{ __html: narrative.before }}
          />
          {hero ? <TopicHeroFigure slug={slug} hero={hero} /> : null}
          <div
            className={"prose-article topic-body-narrow " + (summaryLoading ? "topic-body-pending" : "")}
            dangerouslySetInnerHTML={{ __html: narrative.after }}
          />
        </section>
      ) : summaryLoading ? (
        <div className="loading-message">Loading research summary…</div>
      ) : null}

      {sections.map((section) => (
        <section className="research-story-section" id={`research-${section.key}`} key={section.key}>
          <div className="research-story-heading">
            <div className="topic-section-label">{section.title}</div>
            <span>{section.state === "present" ? "Present" : section.available ? "Draft section" : "Evidence gap"}</span>
          </div>
          {section.key === "results" && hero && !heroIsInNarrative ? (
            <TopicHeroFigure slug={slug} hero={hero} />
          ) : null}
          {section.available && section.html ? (
            <div className="prose-article topic-body-narrow" dangerouslySetInnerHTML={{ __html: section.html }} />
          ) : (
            <div className="research-story-missing">
              This program does not yet contain a committed {section.title.toLowerCase()} section.
              Treat the page at its displayed maturity level; this gap is part of the next research pass.
            </div>
          )}
        </section>
      ))}
    </div>
  );
}

function OverviewTab({
  program,
  manifest,
  slug,
  hasPaper,
}: {
  program: (typeof programs)[number] | undefined;
  manifest: EvidenceManifest | null;
  slug: string;
  hasPaper: boolean;
}) {
  return (
    <div className="topic-overview">
      <h2 className="content-title">Current state</h2>
      {program?.summary ? (
        <p className="content-copy topic-overview-summary">{program.summary}</p>
      ) : (
        <p className="content-copy">No program summary is registered for this topic yet.</p>
      )}
      {program?.note ? <p className="topic-overview-note">{program.note}</p> : null}
      <div className="topic-overview-metrics" aria-label="Topic evidence status">
        <div>
          <span>Article</span>
          <strong>{hasPaper ? "available" : "not yet"}</strong>
        </div>
        <div>
          <span>Hero visual</span>
          <strong>{manifest?.hero ? "available" : "not yet"}</strong>
        </div>
        <div>
          <span>Evidence files</span>
          <strong>{(manifest?.artifacts || []).length.toLocaleString()}</strong>
        </div>
        <div>
          <span>Generated outputs</span>
          <strong>{(manifest?.generated_files || []).length.toLocaleString()}</strong>
        </div>
      </div>
      <div className="topic-overview-actions">
        {(manifest?.artifacts || []).length > 0 || (manifest?.scripts || []).length > 0 ? (
          <Link href={`/${slug}?view=evidence`} className="token-link">
            Open evidence packet
          </Link>
        ) : null}
        {(manifest?.generated_files || []).length > 0 ? (
          <Link href={`/${slug}?view=data`} className="token-link">
            Open generated data
          </Link>
        ) : null}
      </div>
    </div>
  );
}

function SlidesTab({
  slug,
  pptxUrl,
  sourceMeta,
  bodyHtml,
  bodyLoading,
}: {
  slug: string;
  pptxUrl: string | null;
  sourceMeta: ArticleMeta | undefined;
  bodyHtml: string;
  bodyLoading: boolean;
}) {
  if (!pptxUrl) {
    return <div className="loading-message">No generated slide deck is available for this topic.</div>;
  }
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
      {(manifest.resources?.reviewer_packet || manifest.resources?.deck || manifest.resources?.reproduce) ? (
        <div className="resource-grid">
          {manifest.resources?.reviewer_packet ? (
            <a href={manifest.resources.reviewer_packet} download className="resource-card">
              <div className="topic-section-label">Reviewer packet</div>
              <div className="resource-title">Download .zip</div>
              <div className="resource-note">Frozen review bundle</div>
            </a>
          ) : null}
          {manifest.resources?.deck ? (
            <a href={manifest.resources.deck} download className="resource-card">
              <div className="topic-section-label">Slide deck</div>
              <div className="resource-title">Download .pptx</div>
              <div className="resource-note">Generated presentation</div>
            </a>
          ) : null}
          {manifest.resources?.reproduce ? (
            <a href={manifest.resources.reproduce} target="_blank" rel="noreferrer" className="resource-card">
              <div className="topic-section-label">Reproduce</div>
              <div className="resource-title">Open runbook</div>
              <div className="resource-note">Committed commands and environment</div>
            </a>
          ) : null}
        </div>
      ) : (
        <p className="research-story-missing">
          No packaged downloads are published for this topic yet. The documentation and generated files below are the available evidence surface.
        </p>
      )}
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
          {manifest?.resources?.deck && (
            <li>
              Slide deck —{" "}
              <a
                href={manifest.resources.deck}
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
                <Link href={`/${slug}?view=data`}
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
          {manifest?.resources?.reproduce ? (
            <li>
              <a
                href={manifest.resources.reproduce}
                target="_blank"
                rel="noreferrer"
                className="file-link"
              >
                Reproduction runbook
              </a>
            </li>
          ) : null}
          <li>
            <a
              href={manifest?.resources?.repository || `https://github.com/rradofina/adb-research-reporting/tree/main/${slug}`}
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
