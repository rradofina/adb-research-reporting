/**
 * Doc.tsx — generic markdown viewer for in-site governance documents.
 *
 * The lab's binding documents (Constitution, operating rules, factory
 * manual, license, etc.) should be readable directly on the site.
 * scripts/sync-docs.mjs copies them into reporting-site/public/docs/
 * at build time; this page fetches one and renders it with the same
 * prose styling as research articles.
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { marked } from "marked";

marked.setOptions({ gfm: true, breaks: false });

interface DocInfo {
  file: string;
  title: string;
  blurb: string;
}

interface DocProps {
  name: string;
}

const DOC_REGISTRY: Record<string, DocInfo> = {
  constitution: {
    file: "constitution.md",
    title: "Constitution",
    blurb: "The lab's binding rules: §1–§18. Governs problem selection, originality, methods, claim-maturity gates, review process, publication pathway, reproducibility, ethics, and the AI-First Operating Mode (§18).",
  },
  "operating-rules": {
    file: "operating-rules.md",
    title: "Operating rules (CLAUDE.md)",
    blurb: "Rules AI assistants follow when working in this repository: end-of-task hygiene, hard walls vs. soft barriers, default research-factory loop.",
  },
  agents: {
    file: "agents.md",
    title: "Agent rules (AGENTS.md)",
    blurb: "Default operating mode and focus rule for any AI agent working in the repository.",
  },
  factory: {
    file: "factory.md",
    title: "Factory manual",
    blurb: "Process documentation for the per-program loop: standard artifact set, publication ladder (7 tiers), review-loop modes (A/B/C), visualization rule, status/register conventions.",
  },
  status: {
    file: "status.md",
    title: "Operating board",
    blurb: "Current research status: active flagship, current stage, session protocol. Updated at the end of every substantial session.",
  },
  "wip-register": {
    file: "wip-register.md",
    title: "WIP register",
    blurb: "Claim-maturity register: every program's current label (PR / SR / PP / H / Ret) and the promotion / demotion log.",
  },
  "red-team": {
    file: "red-team.md",
    title: "Red-team roster",
    blurb: "External red-team reviewer roster + outreach template. Per CONSTITUTION.md §9.3 and §18.4.",
  },
  "data-access-audit": {
    file: "data-access-audit.md",
    title: "Data-access audit",
    blurb: "Per-program source inventory: URLs, license terms, access model, retrieval patterns. The lab's source registry.",
  },
  sources: {
    file: "sources.md",
    title: "Sources index",
    blurb: "Lightweight sources index linking each program to its upstream public-data feeds.",
  },
  "repo-readme": {
    file: "repo-readme.md",
    title: "Repository README",
    blurb: "Reader orientation for the repository layout: governance pointers, structure, publication ladder, gates, reproducibility, license, citation pattern.",
  },
  license: {
    file: "license.txt",
    title: "License — code (MIT)",
    blurb: "MIT License. Covers the source code in this repository: scripts, React/TypeScript components, build configs.",
  },
  "license-content": {
    file: "license-content.txt",
    title: "License — research content (CC BY 4.0)",
    blurb: "Creative Commons Attribution 4.0 International. Covers research artifacts: markdown articles, generated CSVs, charts, narrative documents, CONSTITUTION.md.",
  },
  versions: {
    file: "versions.json",
    title: "Source version pins",
    blurb: "JSON record of every upstream source pinned by the lab: URL, license, retrieval date, totalRecordCount, pagination details. The §11 reproducibility manifest.",
  },
  manifest: {
    file: "manifest.sha256",
    title: "File-hash manifest",
    blurb: "SHA-256 of every committed file at the canonical retrieval. Reviewers verify their regenerated cache against this manifest.",
  },
};

export default function Doc({ name }: DocProps) {
  const info = DOC_REGISTRY[name];
  const [body, setBody] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [missing, setMissing] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setBody("");
    setMissing(false);
    setLoading(true);
    if (!info) {
      setMissing(true);
      setLoading(false);
      return;
    }
    (async () => {
      const r = await fetch(`/docs/${info.file}`);
      if (!r.ok) {
        if (!cancelled) {
          setMissing(true);
          setLoading(false);
        }
        return;
      }
      const text = await r.text();
      if (cancelled) return;
      // .txt and .json render as preformatted; .md renders through marked.
      if (info.file.endsWith(".md")) {
        const rendered = await marked.parse(text);
        if (!cancelled) {
          setBody(typeof rendered === "string" ? rendered : "");
          setLoading(false);
        }
      } else {
        const safe = text.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]!));
        if (!cancelled) {
          setBody(`<pre class="doc-pre">${safe}</pre>`);
          setLoading(false);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [name, info]);

  if (missing || !info) {
    return (
      <div className="py-16 text-center">
        <div className="text-xs uppercase tracking-[0.2em] text-ink-500">404</div>
        <h1 className="mt-3 text-2xl font-semibold">No document at /{name}</h1>
        <Link to="/docs" className="mt-6 inline-block text-sm underline underline-offset-4">
          ← All documents
        </Link>
      </div>
    );
  }

  return (
    <article className="doc-page max-w-[68ch]">
      <div className="mb-8 pb-6 border-b border-ink-200">
        <Link
          to="/docs"
          className="inline-block text-xs uppercase tracking-[0.2em] text-ink-500 hover:text-ink-700"
        >
          ← All documents
        </Link>
        <h1 className="mt-4 text-3xl md:text-4xl font-semibold tracking-tight">
          {info.title}
        </h1>
        <p className="mt-3 text-ink-600 leading-relaxed">{info.blurb}</p>
        <p className="mt-3 text-xs text-ink-500 font-mono">
          Source:{" "}
          <a
            href={`https://github.com/rradofina/adb-research-reporting/blob/main/${sourcePathForFile(info.file)}`}
            target="_blank"
            rel="noreferrer"
            className="underline underline-offset-4 hover:text-ink-900"
          >
            {sourcePathForFile(info.file)}
          </a>{" "}
          on GitHub
        </p>
      </div>
      {loading ? (
        <div className="py-12 text-ink-500 text-sm">Loading…</div>
      ) : (
        <div
          className="prose-article max-w-none"
          dangerouslySetInnerHTML={{ __html: body }}
        />
      )}
    </article>
  );
}

function sourcePathForFile(file: string): string {
  // Inverse of the mapping in scripts/sync-docs.mjs.
  const inverse: Record<string, string> = {
    "constitution.md": "CONSTITUTION.md",
    "operating-rules.md": "CLAUDE.md",
    "agents.md": "AGENTS.md",
    "repo-readme.md": "README.md",
    "license.txt": "LICENSE",
    "license-content.txt": "LICENSE-CONTENT",
    "factory.md": "research/factory.md",
    "status.md": "research/STATUS.md",
    "wip-register.md": "research/wip-register.md",
    "red-team.md": "red-team.md",
    "data-access-audit.md": "data-access-audit.md",
    "sources.md": "sources.md",
    "versions.json": "versions.json",
    "manifest.sha256": "manifest.sha256",
  };
  return inverse[file] || file;
}
