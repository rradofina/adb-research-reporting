import type { Metadata } from "next";
import Link from "next/link";
import "@/components/reviews/reviews.css";
import { loadTaxonomy } from "@/lib/taxonomy";

export const metadata: Metadata = {
  title: "Topics",
  description:
    "Browse research by subject: climate, health, poverty, agriculture, water, energy and more across Asia and the Pacific.",
};

export default async function TopicsPage() {
  const tax = await loadTaxonomy();
  return (
    <div className="da-article">
      <div className="da-container">
        <p className="da-kicker">Browse</p>
        <h1 className="da-headline">Topics</h1>
        <p className="da-standfirst">
          Research grouped by subject rather than by how it was produced.
        </p>
      </div>
      <div className="da-container">
        <ul className="da-index">
          {tax.sectors.map((s) => (
            <li key={s.slug}>
              <Link href={`/topics/${s.slug}`}>{s.name}</Link>
              <span>{s.count}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
