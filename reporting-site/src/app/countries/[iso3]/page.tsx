import type { Metadata } from "next";
import { notFound } from "next/navigation";
import TopicGrid from "@/components/reviews/TopicGrid";
import "@/components/reviews/reviews.css";
import { articlesFor, loadTaxonomy } from "@/lib/taxonomy";

export async function generateStaticParams() {
  const tax = await loadTaxonomy();
  return tax.countries.map((c) => ({ iso3: c.iso3.toLowerCase() }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ iso3: string }>;
}): Promise<Metadata> {
  const { iso3 } = await params;
  const tax = await loadTaxonomy();
  const country = tax.countries.find((c) => c.iso3.toLowerCase() === iso3);
  if (!country) return { title: "Country" };
  return {
    title: country.name,
    description: `${country.count} research outputs studying ${country.name}.`,
  };
}

export default async function CountryPage({
  params,
}: {
  params: Promise<{ iso3: string }>;
}) {
  const { iso3 } = await params;
  const tax = await loadTaxonomy();
  const country = tax.countries.find((c) => c.iso3.toLowerCase() === iso3);
  if (!country) notFound();

  return (
    <div className="da-article">
      <div className="da-container">
        <p className="da-kicker">Country</p>
        <h1 className="da-headline">{country.name}</h1>
        <p className="da-standfirst">
          {country.count} research {country.count === 1 ? "output" : "outputs"}{" "}
          studying {country.name}.
        </p>
      </div>
      <div className="da-container-wide">
        <TopicGrid articles={articlesFor(tax, country.slugs)} />
      </div>
    </div>
  );
}
