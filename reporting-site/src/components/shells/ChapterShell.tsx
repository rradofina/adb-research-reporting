"use client";

import Link from "next/link";
import type { StoryPackage } from "./types";
import { assetUrl } from "@/lib/storyPackage";
import ShellSwitcher from "./ShellSwitcher";

export default function ChapterShell({
  story,
  switcherBase,
}: {
  story: StoryPackage;
  switcherBase?: "explore" | "topic";
}) {
  const heroSrc = assetUrl(story.slug, story.hero.svg || story.hero.png);

  return (
    <div className="shell-page chapter-shell">
      <div style={{ padding: "0 1rem" }}>
        <Link href="/explore" className="shell-back">
          ← Explore shells
        </Link>
        <ShellSwitcher
          slug={story.slug}
          active="chapter"
          base={switcherBase || "explore"}
        />
      </div>

      <header className="chapter-hero">
        <div className="chapter-hero-inner">
          <div>
            <div className="chapter-eyebrow">
              Flagship chapter shell · {story.maturity} · attestation{" "}
              {story.attestation_chain}
            </div>
            <h1>{story.title}</h1>
            <p className="chapter-deck">{story.subtitle}</p>
          </div>
          <aside className="chapter-summary">
            <h2>What the evidence says</h2>
            <ol>
              {story.key_messages.map((msg) => (
                <li key={msg}>{msg}</li>
              ))}
            </ol>
          </aside>
        </div>
      </header>

      <section className="chapter-metrics" aria-label="Summary metrics">
        {story.metrics.map((m) => (
          <div className="chapter-metric" key={m.label}>
            <strong>{m.value}</strong>
            <span>{m.label}</span>
          </div>
        ))}
      </section>

      <div className="chapter-body">
        <aside className="chapter-toc" aria-label="On this page">
          <h2>In this reading</h2>
          <nav>
            {story.sections.map((s) => (
              <a key={s.id} href={`#${s.id}`}>
                {s.title}
              </a>
            ))}
            <a href="#limits">Limits</a>
            <a href="#figures">Figures</a>
          </nav>
          <div style={{ marginTop: "1rem" }}>
            <button
              type="button"
              className="shell-switcher-tab"
              onClick={() => {
                if (typeof window !== "undefined") window.print();
              }}
            >
              Print / Save PDF
            </button>
          </div>
        </aside>

        <main className="chapter-article">
          {story.sections.map((section) => (
            <section
              className="chapter-section"
              id={section.id}
              key={section.id}
            >
              <h2>{section.title}</h2>
              <p>{section.body}</p>
              {section.id === "finding" ? (
                <figure className="shell-figure" style={{ marginTop: "1.25rem" }}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={heroSrc} alt={story.hero.title} />
                  <figcaption>
                    <strong>{story.hero.title}</strong>
                    {story.hero.caption}
                  </figcaption>
                </figure>
              ) : null}
            </section>
          ))}

          <section className="chapter-section chapter-limits" id="limits">
            <h2>What this does not say</h2>
            <ul className="shell-limit-list">
              {story.limits.map((limit) => (
                <li key={limit}>{limit}</li>
              ))}
            </ul>
            <p style={{ marginTop: "1rem" }}>{story.non_claim}</p>
          </section>

          <section className="chapter-section" id="figures">
            <h2>Figure spine</h2>
            <div style={{ display: "grid", gap: "1.5rem" }}>
              {story.figures.map((fig) => (
                <figure className="shell-figure" key={fig.id}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={assetUrl(story.slug, fig.svg || fig.png)}
                    alt={fig.title}
                    loading="lazy"
                  />
                  <figcaption>
                    <strong>
                      {fig.title} · {fig.role}
                    </strong>
                    {fig.caption}
                  </figcaption>
                </figure>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
