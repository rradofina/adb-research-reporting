"use client";

/**
 * About.tsx — simple one-pager.
 *
 * What the site is, the constitutional model, what AI-first attestation
 * means, license, citation pattern.
 */
import Link from "next/link";

export default function About() {
  return (
    <div className="about-page page-narrow">
      <h1 className="page-title">About this site</h1>

      <section className="page-section prose-article">
        <p>
          <strong>Development Evidence Lab</strong> is a public-data research
          lab producing measurement-gap research on Asian Development Bank
          developing member economies (DMCs). Every empirical number on this site
          traces to a committed script and a public source. Every
          artifact carries an <code>attestation_chain</code> field that
          records which review path produced it.
        </p>

        <h2>The constitutional model</h2>
        <p>
          The lab is governed by a written{" "}
          <Link href="/constitution">Constitution</Link>. It defines what
          counts as evidence (§2), how a research program enters the
          register (§3), the originality protocol (§4), the literature
          standard (§5), the methods discipline (§6), the claim-maturity
          gates (§7), the work-in-progress cap (§8), the internal and
          external review process (§9), the publication pathway (§10),
          and the reproducibility standard (§11). The full text is
          on this site, not only on the code host.
        </p>
        <p>
          Each program in the lab follows a standard evidence-packet
          template — a literature scan, a frozen pre-registration, a
          deterministic pipeline, a sensitivity suite at ±50 percent on
          every arbitrary numeric, an internal critique-pass, a red-team
          synthesis, and a written limitations section. The publication
          ladder makes the result legible at every reader-depth (working
          paper, brief, blog post, social card, slide deck) from one
          source-of-truth code path.
        </p>

        <h2>What AI-first attestation means</h2>
        <p>
          The lab is currently in <strong>§18 AI-First Operating Mode</strong> (active
          since 2026-04-25). Under §18, AI executes gate-actions
          previously reserved to the human owner. This is an operating
          choice, not a quality claim.
        </p>
        <p>
          Every artifact records the actual review path that produced it:
        </p>
        <ul>
          <li>
            <strong><code>ai-first</code></strong> — AI ran the §9.1 self-review,
            §9.2 critique-pass, and §9.3 red-team synthesis (synthesizing
            objections from candidate institutions' published methodological
            positions, with the §18.4 explicit non-claim quoted verbatim).
            No actual reviewer was contacted. <strong>Most artifacts here today
            carry this label.</strong>
          </li>
          <li>
            <strong><code>ai-first; owner-spot-checked</code></strong> — owner read
            selected tiers; AI did the rest.
          </li>
          <li>
            <strong><code>human-final</code></strong> — owner read each tier
            line-by-line, contacted at least one external reviewer,
            ran an internal review with the named co-author, and
            signed the promotion commit. <em>No artifact on this site
            currently carries this label.</em>
          </li>
        </ul>
        <p>
          AI-only review paths cannot reach <code>human-final</code> because
          the labeling rule (§18.2) forbids it, not because AI is
          incapable of further iteration. The label tells a reader how
          much trust the artifact has earned.
        </p>

        <h2>Public data only</h2>
        <p>
          §2.1 of the Constitution requires that all empirical claims be
          derivable from publicly accessible sources. No private,
          proprietary, or negotiated data is used for headline claims. If
          a private dataset is used for validation, the headline claim
          must still be reproducible without it. Every program's source
          inventory, license, and retrieval timestamp is in{" "}
          <code>versions.json</code> at the repository root.
        </p>

        <h2>Reproducibility</h2>
        <p>
          A reviewer who clones the repository can rehydrate every cache
          (~8 GB of public data downloads, scripted) and rerun every
          pipeline. The fetch scripts, processing scripts, and
          generated outputs (CSVs, JSON, charts) are committed. The{" "}
          <code>manifest.sha256</code> at the repository root records the
          hash of every committed file at the canonical retrieval. Per
          §11, no number that cannot trace this way appears in any
          output.
        </p>

        <h2>License</h2>
        <p>
          Two licenses, standard for a research repository that bundles
          code and scholarly content:
        </p>
        <ul>
          <li>
            <strong>Code</strong> (scripts, React/TypeScript source, build
            configs) — MIT License. See{" "}
            <Link href="/license">LICENSE</Link>.
          </li>
          <li>
            <strong>Research artifacts</strong> (markdown articles,
            generated CSVs, charts, narrative documents, the Constitution
            itself) — Creative Commons Attribution 4.0 International.
            See <Link href="/license-content">LICENSE-CONTENT</Link>.
          </li>
        </ul>
        <p>
          Consistent with ADB's modern open-publishing practice. The lab
          is not an official ADB publication; the license choice is the
          lab's, recorded under §13.4 of the Constitution.
        </p>

        <h2>Citation pattern</h2>
        <p>
          When citing work from this site before any program reaches{" "}
          <code>human-final</code>, please name the artifact's
          attestation chain explicitly:
        </p>
        <blockquote>
          Adofina, R. (2026). <em>The OSM-vs-registry gap in Philippine
          and Bangladeshi health facilities</em>. Development Evidence Lab working
          paper, ai-first attestation under CONSTITUTION.md §18.
          Available at <code>/public-service-data-quality</code> on this
          site. CC BY 4.0.
        </blockquote>
        <p>
          The lab updates artifact attestation chains as programs
          progress through the review-loop modes. Always cite the
          version you actually read.
        </p>

        <h2>Owner</h2>
        <p>
          Repository owner: Raymond Adofina. Co-author on Program 0
          (mpi-nighttime-lights): Arturo Martinez Jr. The lab is not
          affiliated with ADB at the institutional level; it is a
          personal research project that takes ADB DMC measurement
          questions as its primary subject.
        </p>
      </section>

      <div className="page-footer-links">
        <Link href="/" className="token-link">
          ← Back to topics
        </Link>
        <Link href="/docs" className="token-link">
          Browse all documents →
        </Link>
      </div>
    </div>
  );
}
