import type { ShellId, StoryPackage } from "@/components/shells/types";

export async function loadStoryPackage(
  slug: string,
): Promise<StoryPackage | null> {
  try {
    const res = await fetch(`/programs/${slug}/story.json`, {
      cache: "no-store",
    });
    if (!res.ok) return null;
    return (await res.json()) as StoryPackage;
  } catch {
    return null;
  }
}

export function assetUrl(slug: string, relativePath: string): string {
  if (relativePath.startsWith("/")) return relativePath;
  return `/programs/${slug}/${relativePath}`;
}

export function isShellId(value: string): value is ShellId {
  return value === "product" || value === "workbench" || value === "chapter";
}
