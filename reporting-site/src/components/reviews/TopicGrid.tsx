import Link from "next/link";
import type { TaxonomyArticle } from "@/lib/taxonomy";
import { contentType } from "@/lib/taxonomy";

/** Development Asia card grammar, reused for browse pages: content-type
 *  label, headline, standfirst. No maturity chips, no gate state — those
 *  belong on the piece itself, not on a shelf a reader is scanning. */
export default function TopicGrid({
  articles,
}: {
  articles: TaxonomyArticle[];
}) {
  if (articles.length === 0) {
    return <p className="da-empty">Nothing filed here yet.</p>;
  }
  return (
    <ul className="da-cards">
      {articles.map((a) => (
        <li className="da-card" key={a.slug}>
          <p className="da-kicker">{contentType(a.tier)}</p>
          <h2>
            <Link href={`/${a.program || a.slug}`}>{a.title}</Link>
          </h2>
          {a.subtitle && <p>{a.subtitle}</p>}
          <ul className="da-tags">
            {a.sectors.slice(0, 3).map((s) => (
              <li className="da-tag" key={s}>
                {s}
              </li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
}
