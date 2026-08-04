import type { ShellId, StoryPackage } from "./types";
import ProductShell from "./ProductShell";
import WorkbenchShell from "./WorkbenchShell";
import ChapterShell from "./ChapterShell";
import "./shells.css";

export default function StoryShellRouter({
  story,
  shell,
  base = "topic",
}: {
  story: StoryPackage;
  shell: ShellId;
  base?: "explore" | "topic";
}) {
  if (shell === "workbench") {
    return <WorkbenchShell story={story} switcherBase={base} />;
  }
  if (shell === "chapter") {
    return <ChapterShell story={story} switcherBase={base} />;
  }
  return <ProductShell story={story} switcherBase={base} />;
}
