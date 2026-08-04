"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { StoryPackage } from "./types";
import { assetUrl } from "@/lib/storyPackage";
import ShellSwitcher from "./ShellSwitcher";

export default function WorkbenchShell({
  story,
  switcherBase,
}: {
  story: StoryPackage;
  switcherBase?: "explore" | "topic";
}) {
  const [query, setQuery] = useState("");
  const [pattern, setPattern] = useState("");
  const columns = story.workbench_columns || [];
  const sortKey = columns[columns.length - 1]?.key || "label";
  const [sort, setSort] = useState<string>(sortKey);

  const rows = useMemo(() => {
    const q = query.trim().toLowerCase();
    let filtered = story.workbench_rows.filter((row) => {
      const hay = `${row.label} ${row.pattern} ${row.note} ${Object.values(row.values).join(" ")}`.toLowerCase();
      if (q && !hay.includes(q)) return false;
      if (pattern && row.pattern !== pattern) return false;
      return true;
    });
    filtered = [...filtered].sort((a, b) => {
      if (sort === "label") return a.label.localeCompare(b.label);
      const av = a.values[sort];
      const bv = b.values[sort];
      if (typeof av === "number" && typeof bv === "number") return bv - av;
      return String(bv ?? "").localeCompare(String(av ?? ""), undefined, {
        numeric: true,
      });
    });
    return filtered;
  }, [story.workbench_rows, query, pattern, sort]);

  const patterns = useMemo(
    () => Array.from(new Set(story.workbench_rows.map((r) => r.pattern))).sort(),
    [story.workbench_rows],
  );

  const decomp =
    story.figures.find((f) => f.role === "decomposition") ||
    story.figures.find((f) => f.role === "main result") ||
    story.figures[0];
  const decompSrc = decomp
    ? assetUrl(story.slug, decomp.svg || decomp.png)
    : assetUrl(story.slug, story.hero.svg || story.hero.png);

  return (
    <div className="shell-page">
      <Link href="/explore" className="shell-back">
        ← Explore shells
      </Link>
      <ShellSwitcher
        slug={story.slug}
        active="workbench"
        base={switcherBase || "explore"}
      />

      <div className="workbench-shell">
        <div className="workbench-top">
          <div className="workbench-claim">
            <div className="product-kicker" style={{ color: "#72d5d7" }}>
              Evidence workbench · {story.family}
            </div>
            <h1>{story.title}</h1>
            <p>{story.finding}</p>
          </div>
          <div className="workbench-gates">
            {story.zeros_and_gates.map((g) => (
              <div
                className="workbench-gate"
                key={g.label}
                data-status={g.status}
              >
                <b>{g.status}</b>
                <span>{g.label}</span>
                <span style={{ fontWeight: 500, color: "#5c6b76" }}>
                  {g.value}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="workbench-controls">
          <label>
            Search rows
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Filter labels, patterns, notes…"
            />
          </label>
          <label>
            Pattern
            <select
              value={pattern}
              onChange={(e) => setPattern(e.target.value)}
            >
              <option value="">All patterns</option>
              {patterns.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
          <label>
            Sort
            <select value={sort} onChange={(e) => setSort(e.target.value)}>
              <option value="label">Label</option>
              {columns.map((c) => (
                <option key={c.key} value={c.key}>
                  {c.label}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="workbench-result-line">
          Showing {rows.length} of {story.workbench_rows.length} rows · filters
          run in the browser only
        </div>

        <div className="workbench-table-wrap">
          <table className="workbench-table">
            <thead>
              <tr>
                <th>Label</th>
                {columns.map((c) => (
                  <th key={c.key}>{c.label}</th>
                ))}
                <th>Pattern</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id}>
                  <td>
                    <strong>{row.label}</strong>
                  </td>
                  {columns.map((c) => (
                    <td key={c.key}>
                      {c.key === columns[columns.length - 1]?.key ? (
                        <strong>{row.values[c.key]}</strong>
                      ) : (
                        row.values[c.key]
                      )}
                    </td>
                  ))}
                  <td>
                    <span className="workbench-pattern">{row.pattern}</span>
                  </td>
                  <td>{row.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="workbench-side-grid">
          <figure className="shell-figure">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={decompSrc} alt={decomp?.title || story.hero.title} />
            <figcaption>
              <strong>{decomp?.title || story.hero.title}</strong>
              {decomp?.caption || story.hero.caption}
            </figcaption>
          </figure>
          <div className="product-panel">
            <h2>Limits before the ledger closes</h2>
            <ul className="shell-limit-list">
              {story.limits.map((limit) => (
                <li key={limit}>{limit}</li>
              ))}
            </ul>
            <p
              className="product-nonclaim"
              style={{ borderTop: 0, paddingTop: "0.75rem" }}
            >
              {story.non_claim}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
