import { notFound, redirect } from "next/navigation";
import articleIndex from "../../../../public/articles/_index.json";

type LegacyArticle = {
  slug: string;
  program?: string;
  tier?: string;
  kind?: string;
};

const VIEW_BY_TIER: Record<string, string> = {
  "working-paper": "paper",
  brief: "brief",
  blog: "blog",
  social: "blog",
  slides: "slides",
  deck: "slides",
};

const articles = articleIndex as LegacyArticle[];

export function generateStaticParams() {
  return articles.map((article) => ({ slug: article.slug }));
}

export default async function LegacyFindingPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const article = articles.find((candidate) => candidate.slug === slug);

  if (!article?.program) notFound();

  const view = VIEW_BY_TIER[article.tier || article.kind || ""] || "paper";
  redirect(`/${article.program}?view=${view}`);
}
