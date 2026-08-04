import type { Metadata } from "next";
import Link from "next/link";
import "@/components/reviews/reviews.css";
import { loadTaxonomy } from "@/lib/taxonomy";

export const metadata: Metadata = {
  title: "Countries",
  description:
    "Browse research by Asian Development Bank developing member economy.",
};

export default async function CountriesPage() {
  const tax = await loadTaxonomy();
  return (
    <div className="da-article">
      <div className="da-container">
        <p className="da-kicker">Browse</p>
        <h1 className="da-headline">Countries</h1>
        <p className="da-standfirst">
          Research grouped by the developing member economy it studies.
          Regional work that names no single country is not listed here.
        </p>
      </div>
      <div className="da-container">
        <ul className="da-index">
          {tax.countries.map((c) => (
            <li key={c.iso3}>
              <Link href={`/countries/${c.iso3.toLowerCase()}`}>{c.name}</Link>
              <span>{c.count}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
