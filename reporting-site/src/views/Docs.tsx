"use client";

/**
 * Docs.tsx — index of in-site governance documents.
 *
 * Lists every document in scripts/sync-docs.mjs's DOCS array. Each
 * entry links to /{name} for in-site rendering, with a parallel
 * GitHub link for the canonical source.
 */
import Link from "next/link";

const SECTIONS: Array<{
  label: string;
  blurb: string;
  items: Array<{ slug: string; title: string; description: string; githubPath: string }>;
}> = [
  {
    label: "Governance",
    blurb: "Binding rules. Read in this order if it's your first visit.",
    items: [
      {
        slug: "constitution",
        title: "Constitution",
        description: "§1–§18. Mission, principles, problem selection, originality, methods, claim-maturity gates, review process, publication, reproducibility, ethics, AI-First Operating Mode.",
        githubPath: "CONSTITUTION.md",
      },
      {
        slug: "operating-rules",
        title: "Operating rules (CLAUDE.md)",
        description: "Rules AI assistants follow in this repository: end-of-task hygiene, hard walls vs. soft barriers, default research-factory loop.",
        githubPath: "CLAUDE.md",
      },
      {
        slug: "factory",
        title: "Factory manual",
        description: "Per-program loop, publication ladder (7 tiers), three review modes, visualization rule, status conventions.",
        githubPath: "research/factory.md",
      },
      {
        slug: "agents",
        title: "Agent rules",
        description: "Default operating mode and focus rule for AI agents.",
        githubPath: "AGENTS.md",
      },
    ],
  },
  {
    label: "Operating state",
    blurb: "Live status of the lab. Updated at the end of every substantial session.",
    items: [
      {
        slug: "status",
        title: "Operating board",
        description: "Active flagship, current stage, session protocol.",
        githubPath: "research/STATUS.md",
      },
      {
        slug: "wip-register",
        title: "WIP register",
        description: "Every program's current maturity label and the promotion / demotion log.",
        githubPath: "research/wip-register.md",
      },
      {
        slug: "red-team",
        title: "Red-team roster",
        description: "External reviewer roster + outreach template.",
        githubPath: "red-team.md",
      },
    ],
  },
  {
    label: "Sources and reproducibility",
    blurb: "Where the data comes from and how to verify it.",
    items: [
      {
        slug: "data-access-audit",
        title: "Data-access audit",
        description: "Per-program source inventory: URLs, license terms, access model, retrieval patterns.",
        githubPath: "data-access-audit.md",
      },
      {
        slug: "sources",
        title: "Sources index",
        description: "Lightweight sources index linking each program to its upstream public-data feeds.",
        githubPath: "sources.md",
      },
      {
        slug: "versions",
        title: "Source version pins",
        description: "JSON record of every upstream source pinned by the lab. The §11 reproducibility manifest.",
        githubPath: "versions.json",
      },
      {
        slug: "manifest",
        title: "File-hash manifest",
        description: "SHA-256 of every committed file. Reviewers verify their regenerated cache against this.",
        githubPath: "manifest.sha256",
      },
    ],
  },
  {
    label: "Repository and license",
    blurb: "Repo orientation and the legal footer.",
    items: [
      {
        slug: "repo-readme",
        title: "Repository README",
        description: "Layout overview, governance pointers, citation pattern.",
        githubPath: "README.md",
      },
      {
        slug: "license",
        title: "License — code (MIT)",
        description: "Covers source code: scripts, React/TypeScript components, build configs.",
        githubPath: "LICENSE",
      },
      {
        slug: "license-content",
        title: "License — research content (CC BY 4.0)",
        description: "Covers research artifacts: markdown articles, generated CSVs, charts, narrative documents, CONSTITUTION.md.",
        githubPath: "LICENSE-CONTENT",
      },
    ],
  },
];

export default function Docs() {
  return (
    <div className="docs-index page-narrow">
      <h1 className="page-title">All documents</h1>
      <p className="page-intro">
        Every binding document the lab operates under is readable here.
        Same content as the upstream GitHub repository — anyone visiting
        the site can read the rules without leaving for a code host.
      </p>

      {SECTIONS.map((section) => (
        <section key={section.label} className="page-section">
          <h2 className="section-label">
            {section.label}
          </h2>
          <p className="section-desc">{section.blurb}</p>
          <ul className="page-card-list">
            {section.items.map((item) => (
              <li key={item.slug}>
                <Link href={`/${item.slug}`}
                  className="page-card"
                >
                  <div className="page-card-row">
                    <span className="page-card-title">
                      {item.title}
                    </span>
                    <span className="page-card-path">
                      {item.githubPath}
                    </span>
                  </div>
                  <p className="page-card-copy">
                    {item.description}
                  </p>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}
