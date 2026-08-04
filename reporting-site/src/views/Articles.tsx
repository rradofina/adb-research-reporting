"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { supabaseGet, supabaseEnabled } from "../lib/supabase";

interface Article {
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

export default function Articles() {
  const [items, setItems] = useState<Article[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!supabaseEnabled) {
      setError("Supabase not configured.");
      return;
    }
    supabaseGet<Article>("articles", "select=*&order=updated_at.desc")
      .then(setItems)
      .catch((e) => setError(String(e)));
  }, []);

  return (
    <div>
      <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Findings library</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">
        Working papers, briefs, and shorter reads.
      </h1>
      <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
        Long-form research for practitioners and reviewers. Every number
        traces to a public source, a committed script, and a retrieval
        timestamp — so a reader can check the claim without trusting the
        pipeline on faith.
      </p>

      {error && (
        <div className="mt-6 bg-signal-urgent/10 border border-signal-urgent text-signal-urgent rounded-md p-4 text-sm">
          {error}
        </div>
      )}

      {!items && !error && <div className="mt-12 text-ink-500">Loading…</div>}

      {items && items.length === 0 && (
        <div className="mt-10 bg-white border border-ink-200 rounded-md p-6 text-ink-700">
          No published articles yet. The first draft seed is{" "}
          <code className="font-mono">about-development-blindspots-lab</code> (status: draft).
          Articles appear here once their <code className="font-mono">pub.article.status</code>{" "}
          flips to <code className="font-mono">published</code>.
        </div>
      )}

      {items && items.length > 0 && (
        <section className="mt-10 grid md:grid-cols-2 gap-5">
          {items.map((a) => (
            <article
              key={a.id}
              className="bg-white border border-ink-200 rounded-md p-6 hover:border-ink-500 transition"
            >
              <div className="flex items-center justify-between gap-3">
                <span className="text-xs uppercase tracking-wider text-ink-500">{a.kind}</span>
                {a.is_featured && (
                  <span className="text-xs uppercase bg-signal-info/10 text-signal-info rounded px-2 py-0.5">
                    featured
                  </span>
                )}
              </div>
              <h2 className="mt-3 text-xl font-semibold">{a.title}</h2>
              {a.subtitle && <p className="mt-1 text-ink-700">{a.subtitle}</p>}
              {a.abstract_md && (
                <p className="mt-3 text-sm text-ink-700 line-clamp-3">{a.abstract_md}</p>
              )}
              <div className="mt-4 text-xs text-ink-500 flex flex-wrap gap-2">
                {a.authors?.map((au) => (
                  <span key={au} className="bg-ink-100 px-2 py-0.5 rounded">
                    {au}
                  </span>
                ))}
                {a.topics?.map((t) => (
                  <span key={t} className="bg-signal-info/10 text-signal-info px-2 py-0.5 rounded">
                    #{t}
                  </span>
                ))}
              </div>
              {a.doi && (
                <div className="mt-3 text-xs">
                  <a
                    href={`https://doi.org/${a.doi}`}
                    target="_blank"
                    rel="noreferrer"
                    className="font-mono text-signal-info underline"
                  >
                    DOI: {a.doi}
                  </a>
                </div>
              )}
              <div className="mt-3 text-xs text-ink-500">
                Updated{" "}
                {new Date(a.updated_at).toLocaleDateString(undefined, {
                  year: "numeric",
                  month: "short",
                  day: "numeric",
                })}
              </div>
            </article>
          ))}
        </section>
      )}

      <section className="mt-12 bg-white border border-ink-200 rounded-md p-6 text-sm">
        <h2 className="font-semibold">How publishing works here</h2>
        <p className="mt-2 text-ink-700 leading-relaxed">
          Articles draft in <code className="font-mono">pub.article.body_md</code>{" "}
          using inline citation tokens like{" "}
          <code className="font-mono">{"{{ind:remit.fragility_index|iso=KGZ}}"}</code>{" "}
          which resolve at render time against <code className="font-mono">obs.country_value</code>.
          Numbers stay fresh against the database; published versions are
          frozen as <code className="font-mono">pub.article_revision</code>{" "}
          snapshots. External red-team reviews are logged in{" "}
          <code className="font-mono">pub.article_review</code>; a publication-
          ready article requires ≥2 external reviews per Constitution §9.3.
        </p>
      </section>
    </div>
  );
}
