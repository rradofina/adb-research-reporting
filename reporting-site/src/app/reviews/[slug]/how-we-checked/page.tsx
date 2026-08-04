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
  if (!review) return { title: "How we checked this" };
  return {
    title: `How we checked: ${review.headline || review.title}`,
    description: `${review.counts.citable} of ${review.counts.records} figures have a verified source and a page someone has read.`,
  };
}

export default async function HowWeCheckedPage({
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
