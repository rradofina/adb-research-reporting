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
        <h1>Reviews, and how much of each one has been checked</h1>
        <p className="review-commission">
          A review synthesises published studies rather than computing its own
          numbers, so it cannot satisfy the repository&rsquo;s
          committed-script rule. §2.7 holds it to the equivalent standard
          instead: verified source identity, plus a page locator someone has
          actually read. Each review below reports how far it has got.
        </p>
      </header>

      {reviews.length === 0 ? (
        <p className="review-section-note">
          No reviews published yet. Scaffold one with{" "}
          <code>python review-factory/new_review.py &lt;slug&gt;</code>.
        </p>
      ) : (
        <ul className="review-list">
          {reviews.map((review) => (
            <li className="review-card" key={review.slug}>
              <h2>
                <Link href={`/reviews/${review.slug}`}>{review.title}</Link>
              </h2>
              <p>
                {review.commissioned_by
                  ? `Commissioned by ${review.commissioned_by} · `
                  : ""}
                {review.commissioned_date} · attestation{" "}
                {review.attestation_chain} · maturity {review.maturity}
              </p>
              <ul className="review-counts">
                <li className="review-count">
                  <b>{review.counts.citable}</b>
                  <span>citable of {review.counts.records}</span>
                </li>
                <li className="review-count">
                  <b>{review.counts.provisional}</b>
                  <span>screened, not read</span>
                </li>
                <li className="review-count">
                  <b>{review.counts.unread}</b>
                  <span>source not retrievable</span>
                </li>
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
