import type { Metadata } from "next";
import { notFound } from "next/navigation";
import ReviewShell from "@/components/reviews/ReviewShell";
import "@/components/reviews/reviews.css";
import { loadReview, loadReviewArtifacts, reviewSlugs } from "@/lib/reviewPackage";

export async function generateStaticParams() {
  const slugs = await reviewSlugs();
  return slugs.map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const review = await loadReview(slug);
  if (!review) return { title: "Evidence review" };
  return {
    title: review.title,
    description: `${review.counts.citable} of ${review.counts.records} figures have cleared §2.7 verification.`,
  };
}

export default async function ReviewPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const review = await loadReview(slug);
  if (!review) notFound();
  const artifacts = await loadReviewArtifacts(slug);
  return <ReviewShell review={review} artifacts={artifacts} />;
}
