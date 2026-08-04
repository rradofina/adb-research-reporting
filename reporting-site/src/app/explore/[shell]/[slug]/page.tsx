import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import StoryShellRouter from "@/components/shells/StoryShellRouter";
import "@/components/shells/shells.css";
import { isShellId } from "@/lib/storyPackage";
import { loadStoryServer } from "@/lib/loadStoryServer";

const PILOTS = [
  "public-data-freshness",
  "remittance-resilience",
  "climate-health-workdays",
  "public-service-data-quality",
] as const;

const SHELLS = ["product", "workbench", "chapter"] as const;

export function generateStaticParams() {
  return SHELLS.flatMap((shell) =>
    PILOTS.map((slug) => ({ shell, slug })),
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ shell: string; slug: string }>;
}): Promise<Metadata> {
  const { shell, slug } = await params;
  const story = await loadStoryServer(slug);
  if (!story || !isShellId(shell)) return { title: "Explore shell" };
  return {
    title: `${story.title} · ${shell}`,
    description: story.finding_short,
  };
}

export default async function ExploreShellPage({
  params,
}: {
  params: Promise<{ shell: string; slug: string }>;
}) {
  const { shell, slug } = await params;
  if (!isShellId(shell)) notFound();

  const story = await loadStoryServer(slug);
  if (!story) {
    return (
      <div className="shell-page" style={{ padding: "2rem 0" }}>
        <Link href="/explore" className="shell-back">
          ← Explore shells
        </Link>
        <h1>No story package for {slug}</h1>
        <p className="product-nonclaim">
          Add <code>{slug}/story.json</code> in the program folder (synced to{" "}
          <code>public/programs/{slug}/story.json</code>).
        </p>
      </div>
    );
  }

  return <StoryShellRouter story={story} shell={shell} base="explore" />;
}
