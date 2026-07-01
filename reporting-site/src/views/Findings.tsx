"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { supabaseGet, supabaseEnabled } from "../lib/supabase";
import { Kicker, FeatureCard, Divider } from "../components/ui";
import { programs } from "../data/programs";
import { BRIEF_DETAILS } from "../data/briefs";
import { loadArticleIndex, type ArticleMeta } from "../lib/articles";

interface RemoteArticle {
  id: string;
  slug: string;
  kind: string;
  status: string;
  title: string;
  subtitle: string | null;
  abstract_md: string | null;
  doi: string | null;
  geographies: string[] | null;
  topics: string[] | null;
  is_featured: boolean;
  published_at: string | null;
  created_at: string;
  updated_at: string;
  authors: string[] | null;
}

export default function Findings() {
  const [remote, setRemote] = useState<RemoteArticle[] | null>(null);
  const [local, setLocal] = useState<ArticleMeta[] | null>(null);

  useEffect(() => {
    loadArticleIndex().then(setLocal).catch(() => setLocal([]));
    if (!supabaseEnabled) return;
    supabaseGet<RemoteArticle>("articles", "select=*&order=updated_at.desc")
      .then(setRemote)
      .catch((e) => {
        if (process.env.NODE_ENV === "development") {
          console.warn("Supabase article fetch failed; using local articles.", e);
        }
      });
  }, []);

  // Combined view: prefer remote (Supabase) when present; otherwise local.
  const remoteList = remote ?? [];
  const localList = local ?? [];
  const remoteSlugs = new Set(remoteList.map((r) => r.slug));
  const localOnly = localList.filter((a) => !remoteSlugs.has(a.slug));
  const combined: Array<{
    slug: string;
    kind: string;
    status: string;
    title: string;
    abstract: string;
    authors: string[];
    published_at: string;
    doi: string;
    source: "remote" | "local";
  }> = [
    ...remoteList.map((r) => ({
      slug: r.slug,
      kind: r.kind,
      status: r.status,
      title: r.title,
      abstract: r.abstract_md ?? "",
      authors: r.authors ?? [],
      published_at: r.published_at ?? "",
      doi: r.doi ?? "",
      source: "remote" as const,
    })),
    ...localOnly.map((a) => ({
      slug: a.slug,
      kind: a.kind,
      status: a.status,
      title: a.title,
      abstract: a.abstract,
      authors: a.authors,
      published_at: a.published_at,
      doi: a.doi,
      source: "local" as const,
    })),
  ];
  combined.sort((a, b) => (b.published_at || "").localeCompare(a.published_at || ""));

  const programFindings = programs.filter((p) => p.href).slice(0, 9);
  const flagshipBrief = BRIEF_DETAILS["public-service-data-quality"];

  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-12">
        <div className="col-span-12 md:col-span-8">
          <Kicker variant="crimson">Findings — articles, research briefs, working papers</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,5rem)] mt-3">
            Long-form{" "}
            <span className="display-italic" style={{ color: "var(--crimson)" }}>
              writing
            </span>{" "}
            on what the data shows.
          </h1>
          <p className="lede mt-6 max-w-[60ch]">
            Each article carries an audit trail: every cited number resolves
            to an indicator value, an underlying source dataset, and a
            retrieval timestamp. Drafts, research briefs, and working papers all
            share the same citation discipline.
          </p>
        </div>
        <div className="col-span-12 md:col-span-4 md:pl-6 md:border-l md:border-[var(--rule-soft)]">
          <Link href="/findings/measurement-gap-philippines-bangladesh"
            className="block border border-[var(--rule)] bg-paper-200 p-5 group"
          >
            <div className="kicker kicker-crimson">Best first read</div>
            <h2 className="display-md mt-3 text-[1.35rem] group-hover:text-crimson transition-colors">
              Start with the public-service data gap.
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-ink-soft">
              {flagshipBrief.output}
            </p>
            <p className="mt-4 marginalia">
              {flagshipBrief.caveat}
            </p>
            <div className="mt-5 ed-link text-xs uppercase tracking-[0.18em] font-mono">
              Read the flagship article →
            </div>
          </Link>
        </div>
      </header>

      <Divider />

      {combined.length > 0 ? (
        <section>
          <Kicker>{remote && remote.length > 0 ? "Published & drafts" : "Drafts"}</Kicker>
          <div className="rule mt-4" />
          {combined.map((a) => (
            <FeatureCard
              key={a.slug} href={a.source === "local" ? `/findings/${a.slug}` : `/findings/${a.slug}`}
              kicker={`${a.kind}${a.status !== "published" ? ` · ${a.status}` : ""}`}
              title={a.title}
              excerpt={a.abstract}
              meta={[
                a.authors?.join(", "),
                a.published_at ? new Date(a.published_at).toLocaleDateString(undefined, { year: "numeric", month: "short" }) : "",
                a.doi ? `DOI ${a.doi}` : "",
              ]
                .filter(Boolean)
                .join(" · ")}
              accent="crimson"
            />
          ))}
        </section>
      ) : (
        <section>
          <div className="grid grid-cols-12 gap-6 my-10">
            <div className="col-span-12 md:col-span-3">
              <Kicker>Pre-publication</Kicker>
            </div>
            <div className="col-span-12 md:col-span-7 marginalia">
              No articles have been written yet. The findings hub will
              fill out as articles flip from draft to published. In the
              meantime, follow each program for its current results and
              caveats.
            </div>
          </div>
        </section>
      )}

      <Divider />

      <section>
        <div className="mb-10 flex items-baseline justify-between gap-4 flex-wrap">
          <div>
            <Kicker variant="sage">Programs · current screening artifacts</Kicker>
            <h2 className="display-lg text-[clamp(1.6rem,2.5vw,2.4rem)] mt-3">
              Read the programs.
            </h2>
          </div>
          <div className="marginalia max-w-[34ch]">
            Each program's screening artifact is the working substitute for
            an article until the program crosses the SR → PR gate.
          </div>
        </div>

        <div className="rule" />
        {programFindings.map((p, i) => (
          <FeatureCard
            key={p.slug} href={p.href!}
            number={p.id}
            kicker="Program"
            title={p.title}
            excerpt={p.summary}
            meta={p.note ?? ""}
            accent={(["ink", "crimson", "sage", "ochre"] as const)[i % 4]}
          />
        ))}
      </section>
    </div>
  );
}
