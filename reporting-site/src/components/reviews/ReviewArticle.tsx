import Link from "next/link";
import { marked } from "marked";
import type { ReviewArtifact, ReviewPackage } from "@/lib/reviewPackage";
import { formatBytes } from "@/lib/reviewPackage";

marked.setOptions({ gfm: true, breaks: false });

/**
 * Development Asia article grammar: content-type label, headline a practitioner
 * can retell, standfirst, hero, then prose. Topic tags, not process tags.
 *
 * The provenance apparatus lives at /reviews/{slug}/how-we-checked, not here.
 * That split is deliberate and it is the only way the two requirements
 * reconcile: a reader wants an article, and §2.7 requires that nobody mistake
 * a screened figure for a read one. So the article carries one honest sentence
 * about how much has been checked, with a link — the way a newsroom carries a
 * methodology note — rather than opening with a gate table.
 */
export default function ReviewArticle({
  review,
  artifacts,
}: {
  review: ReviewPackage;
  artifacts: ReviewArtifact[];
}) {
  const c = review.counts;
  const html = marked.parse(
    review.manuscript_markdown.replace(/<(TABLE|FIGURE):[A-Z0-9_]+>/g, ""),
  ) as string;

  return (
    <article className="da-article">
      <div className="da-container">
        <p className="da-kicker">{review.content_type}</p>
        <h1 className="da-headline">{review.headline}</h1>
        {review.standfirst && (
          <p className="da-standfirst">{review.standfirst}</p>
        )}

        <ul className="da-tags">
          {review.topics?.map((topic) => (
            <li key={topic} className="da-tag">
              {topic}
            </li>
          ))}
          {review.countries?.map((country) => (
            <li key={country} className="da-tag da-tag-geo">
              {country}
            </li>
          ))}
        </ul>

        <p className="da-byline">
          {review.commissioned_by
            ? `Commissioned by ${review.commissioned_by}`
            : "Development Evidence Lab"}
          <span aria-hidden> · </span>
          <time dateTime={review.commissioned_date}>
            {review.commissioned_date}
          </time>
        </p>
      </div>

      {review.hero_href && (
        <figure className="da-hero">
          {/* Generated chart, not a stock photo: it is the finding, so it is
              the image. */}
          <img src={review.hero_href} alt={review.hero_caption || ""} />
          {review.hero_caption && (
            <figcaption>{review.hero_caption}</figcaption>
          )}
        </figure>
      )}

      <div className="da-container">
        {/* One sentence, then a link. Not a table. */}
        <aside className="da-checked">
          <p>
            <strong>How much of this has been checked:</strong>{" "}
            {c.citable} of {c.records} figures have a verified source
            <em> and</em> a page someone has read. {c.provisional} more were
            located automatically but not yet read, and {c.unread} come from
            sources we could not retrieve.{" "}
            <Link href={`/reviews/${review.slug}/how-we-checked`}>
              See the full evidence register →
            </Link>
          </p>
        </aside>

        <div
          className="da-body"
          dangerouslySetInnerHTML={{ __html: html }}
        />

        {artifacts.length > 0 && (
          <section className="da-resources">
            <h2>Resources</h2>
            <ul>
              {artifacts.map((f) => (
                <li key={f.name}>
                  <a href={f.href} download>
                    {f.ext}
                  </a>{" "}
                  <span>
                    {f.name} · {formatBytes(f.bytes)}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}

        <p className="da-nonclaim">{review.non_claim}</p>
      </div>
    </article>
  );
}
