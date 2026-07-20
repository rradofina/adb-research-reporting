import type { Metadata } from "next";
import Topic from "@/views/Topic";
import { programs } from "@/data/programs";
import { Suspense } from "react";

export function generateStaticParams() {
  return programs.map((program) => ({ slug: program.slug }));
}

function truncate(value: string, limit = 200) {
  if (value.length <= limit) return value;
  return `${value.slice(0, limit).replace(/\s+\S*$/, "")}…`;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const program = programs.find((p) => p.slug === slug);
  if (!program) return {};
  return {
    title: program.title,
    description: truncate(program.summary),
  };
}

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return (
    <Suspense fallback={null}>
      <Topic slug={slug} />
    </Suspense>
  );
}
