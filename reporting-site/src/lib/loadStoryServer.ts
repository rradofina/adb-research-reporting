import { readFile } from "node:fs/promises";
import path from "node:path";
import type { StoryPackage } from "@/components/shells/types";

export async function loadStoryServer(
  slug: string,
): Promise<StoryPackage | null> {
  const filePath = path.join(
    process.cwd(),
    "public",
    "programs",
    slug,
    "story.json",
  );
  try {
    const raw = await readFile(filePath, "utf8");
    return JSON.parse(raw) as StoryPackage;
  } catch {
    return null;
  }
}
