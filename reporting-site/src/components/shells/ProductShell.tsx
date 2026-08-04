import Link from "next/link";
import type { StoryPackage } from "./types";
import { assetUrl } from "@/lib/storyPackage";
import ShellSwitcher from "./ShellSwitcher";

export default function ProductShell({
  story,
  switcherBase,
}: {
  story: StoryPackage;
  switcherBase?: "explore" | "topic";
}) {
  const heroSrc = assetUrl(story.slug, story.hero.svg || story.hero.png);

  return (
    <div className="shell-page">
      <Link href="/explore" className="shell-back">
        ← Explore shells
      </Link>
      <ShellSwitcher
        slug={story.slug}
        active="product"
        base={switcherBase || "explore"}
      />

      <article className="product-shell">
        <div className="product-hero-block">
          <div className="product-kicker">
            Modern research product · {story.family}
          </div>
          <h1>{story.title}</h1>
          <div className="product-meta-row">
            <span className="shell-maturity">{story.maturity}</span>
            <span>attestation: {story.attestation_chain}</span>
            {story.updated_at ? <span>updated {story.updated_at}</span> : null}
          </div>
          <p className="product-finding">{story.finding}</p>
        </div>

        <figure className="shell-figure">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={heroSrc} alt={story.hero.title} />
          <figcaption>
            <strong>{story.hero.title}</strong>
            {story.hero.caption}
            <br />
            Source: {story.hero.source}
          </figcaption>
        </figure>

        <div className="product-metrics">
          {story.metrics.map((m) => (
            <div className="product-metric" key={m.label}>
              <strong>{m.value}</strong>
              <span>
                {m.label}
                {m.detail ? ` · ${m.detail}` : ""}
              </span>
            </div>
          ))}
        </div>

        <div className="product-two-col">
          <div className="product-panel">
            <h2>What this does not say</h2>
            <ul className="shell-limit-list">
              {story.limits.map((limit) => (
                <li key={limit}>{limit}</li>
              ))}
            </ul>
          </div>
          <div className="product-panel">
            <h2>How we know</h2>
            <p>{story.sections.find((s) => s.id === "method")?.body}</p>
            <h2>Downloads</h2>
            <div className="product-downloads">
              {story.downloads.map((d) => (
                <a key={d.href} href={d.href}>
                  {d.label}
                </a>
              ))}
            </div>
          </div>
        </div>

        <p className="product-nonclaim">{story.non_claim}</p>
      </article>
    </div>
  );
}
