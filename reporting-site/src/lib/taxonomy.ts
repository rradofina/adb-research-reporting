import { readFile } from "node:fs/promises";
import path from "node:path";

export interface TaxonomyArticle {
  slug: string;
  title: string;
  subtitle: string;
  program: string | null;
  tier: string;
  maturity: string;
  sectors: string[];
  countries: string[];
  regional: boolean;
}

export interface SectorEntry {
  name: string;
  slug: string;
  count: number;
  slugs: string[];
}

export interface CountryEntry {
  iso3: string;
  name: string;
  count: number;
  slugs: string[];
}

export interface Taxonomy {
  generated_at: string;
  sectors: SectorEntry[];
  countries: CountryEntry[];
  articles: TaxonomyArticle[];
}

export async function loadTaxonomy(): Promise<Taxonomy> {
  try {
    const raw = await readFile(
      path.join(process.cwd(), "public", "taxonomy.json"),
      "utf8",
    );
    return JSON.parse(raw) as Taxonomy;
  } catch {
    return { generated_at: "", sectors: [], countries: [], articles: [] };
  }
}

export function articlesFor(tax: Taxonomy, slugs: string[]): TaxonomyArticle[] {
  const set = new Set(slugs);
  return tax.articles.filter((a) => set.has(a.slug));
}

/** Reader-facing label for the publication tier. Development Asia puts a
 *  content-type label on every card; these are ours, in their register. */
export function contentType(tier: string): string {
  const map: Record<string, string> = {
    "working-paper": "Working Paper",
    brief: "Policy Brief",
    blog: "Insight",
    social: "Insight",
    slides: "Presentation",
    deck: "Presentation",
  };
  return map[tier] || "Research";
}
