import type { Metadata } from "next";
import { notFound } from "next/navigation";
import TopicGrid from "@/components/reviews/TopicGrid";
import "@/components/reviews/reviews.css";
import { articlesFor, loadTaxonomy } from "@/lib/taxonomy";

export async function generateStaticParams() {
  const tax = await loadTaxonomy();
  return tax.sectors.map((s) => ({ topic: s.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ topic: string }>;
}): Promise<Metadata> {
  const { topic } = await params;
  const tax = await loadTaxonomy();
  const sector = tax.sectors.find((s) => s.slug === topic);
  if (!sector) return { title: "Topic" };
  return {
    title: sector.name,
    description: `${sector.count} research outputs on ${sector.name} across Asia and the Pacific.`,
  };
}

export default async function TopicPage({
  params,
}: {
  params: Promise<{ topic: string }>;
}) {
  const { topic } = await params;
  const tax = await loadTaxonomy();
  const sector = tax.sectors.find((s) => s.slug === topic);
  if (!sector) notFound();

  return (
    <div className="da-article">
      <div className="da-container">
        <p className="da-kicker">Topic</p>
        <h1 className="da-headline">{sector.name}</h1>
        <p className="da-standfirst">
          {sector.count} research {sector.count === 1 ? "output" : "outputs"}{" "}
          across Asia and the Pacific.
        </p>
      </div>
      <div className="da-container-wide">
        <TopicGrid articles={articlesFor(tax, sector.slugs)} />
      </div>
    </div>
  );
}
