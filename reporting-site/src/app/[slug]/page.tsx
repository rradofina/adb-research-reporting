import Topic from "@/views/Topic";
import { programs } from "@/data/programs";
import { Suspense } from "react";

export function generateStaticParams() {
  return programs.map((program) => ({ slug: program.slug }));
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
