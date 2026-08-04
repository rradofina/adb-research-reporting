import type { Metadata } from "next";
import Link from "next/link";
import "@/components/reviews/reviews.css";
import { loadReviewIndex } from "@/lib/reviewPackage";

export const metadata: Metadata = {
  title: "Evidence reviews",
  description:
    "Commissioned evidence reviews under CONSTITUTION.md §2.7, with per-record verification and locator state.",
};

export default async function ReviewsPage() {
  const reviews = await loadReviewIndex();

  return (
    <div className="review-page">
      <header className="review-hero">
        <div className="review-eyebrow">Evidence reviews · §2.7 track</div>
        <h1>Evidence reviews</h1>
        <p className="review-commission">
          Syntheses of published evidence on shocks, welfare, and policy across
          Asia and the Pacific. Each review links a page showing exactly which
          of its figures have been checked against the source, and which have
          not.
        </p>
      </header>

      {reviews.length === 0 ? (
        <p className="review-section-note">
          No reviews published yet. Scaffold one with{" "}
          <code>python review-factory/new_review.py &lt;slug&gt;</code>.
        </p>
      ) : (
        <ul className="da-cards">
          {reviews.map((review) => (
            <li className="da-card" key={review.slug}>
              {review.hero_href && (
                <Link href={`/reviews/${review.slug}`}>
                  <img src={review.hero_href} alt="" />
                </Link>
              )}
              <p className="da-kicker">{review.content_type}</p>
              <h2>
                <Link href={`/reviews/${review.slug}`}>
                  {review.headline || review.title}
                </Link>
              </h2>
              <p>{review.standfirst}</p>
              <ul className="da-tags">
                {review.topics?.map((topic) => (
                  <li className="da-tag" key={topic}>
                    {topic}
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
