import Link from "next/link";
import type { ShellId } from "./types";
import { SHELL_META } from "./types";

const ORDER: ShellId[] = ["product", "workbench", "chapter"];

export default function ShellSwitcher({
  slug,
  active,
  base = "explore",
}: {
  slug: string;
  active: ShellId;
  base?: "explore" | "topic";
}) {
  function hrefFor(id: ShellId) {
    if (base === "topic") {
      return id === "product" ? `/${slug}` : `/${slug}?shell=${id}`;
    }
    return `/explore/${id}/${slug}`;
  }

  return (
    <div className="shell-switcher">
      <div>
        <div className="shell-switcher-label">Reading mode · same evidence</div>
        <div className="shell-switcher-tabs">
          {ORDER.map((id) => (
            <Link
              key={id}
              href={hrefFor(id)}
              className={
                "shell-switcher-tab" + (id === active ? " is-active" : "")
              }
            >
              {SHELL_META[id].label}
            </Link>
          ))}
          {base === "topic" ? (
            <Link href={`/${slug}?view=classic`} className="shell-switcher-tab">
              Classic UI
            </Link>
          ) : (
            <Link href={`/${slug}`} className="shell-switcher-tab">
              Open topic
            </Link>
          )}
        </div>
      </div>
      <p className="shell-switcher-meta">{SHELL_META[active].when}</p>
    </div>
  );
}
