import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { marked } from "marked";
import {
  loadArticleIndex,
  loadArticleBody,
  stripFrontmatter,
  type ArticleMeta,
} from "../lib/articles";
import { loadReferences, byKey, resolveCitations, renderReferenceList } from "../lib/refs";
import { Kicker } from "../components/ui";
import { BRIEF_DETAILS } from "../data/briefs";

marked.setOptions({ gfm: true, breaks: false });

// Programs in the lab register, indexed for the working-paper number
const PROGRAM_NUMBERS: Record<string, number> = {
  "mpi-nighttime-lights": 0,
  "access-services": 1,
  "digital-performance": 2,
  "air-monitoring": 3,
  "invisible-urbanization": 4,
  "climate-health-workdays": 5,
  "coastal-informal-risk": 6,
  "disaster-recovery-lag": 7,
  "flood-market-access": 8,
  "food-price-climate-transmission": 9,
  "grid-reliability-heat": 10,
  "migration-displacement-signals": 11,
  "port-hinterland-friction": 12,
  "public-service-data-quality": 13,
  "remittance-resilience": 14,
  "school-heat-disruption": 15,
  "social-protection-shock-coverage": 16,
  "water-stress-crop-diversification": 17,
};

export default function Article() {
  const { slug = "" } = useParams();
  const [meta, setMeta] = useState<ArticleMeta | null>(null);
  const [html, setHtml] = useState<string>("");
  const [missing, setMissing] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const [index, refs] = await Promise.all([loadArticleIndex(), loadReferences()]);
      const m = index.find((a) => a.slug === slug);
      if (!m) {
        if (!cancelled) setMissing(true);
        return;
      }
      const body = await loadArticleBody(slug);
      if (!body) {
        if (!cancelled) setMissing(true);
        return;
      }
      const stripped = stripFrontmatter(body);
      const rendered = await marked.parse(stripped);
      const rawHtml = typeof rendered === "string" ? rendered : "";
      // Resolve [@bibtex-key] citations + append References section
      const refIndex = byKey(refs);
      const { html: resolved, cited } = resolveCitations(rawHtml, refIndex);
      const finalHtml = resolved + renderReferenceList(cited);
      if (!cancelled) {
        setMeta(m);
        setHtml(finalHtml);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [slug]);

  if (missing) {
    return (
      <div className="py-20 text-center reveal">
        <Kicker>Findings · 404</Kicker>
        <h1 className="display-lg text-3xl mt-4">No paper at /findings/{slug}</h1>
        <Link to="/findings" className="ed-link mt-6 inline-block">
          ← Back to findings
        </Link>
      </div>
    );
  }

  if (!meta) {
    return (
      <div className="py-20 text-center text-ink-faint reveal">Loading…</div>
    );
  }

  const programNo = meta.program ? PROGRAM_NUMBERS[meta.program] : undefined;
  const seriesLine =
    meta.program && meta.program !== "meta"
      ? `The Blindspots Lab Working Paper Series · No. ${programNo ?? "—"} · ${meta.kind}`
      : `The Blindspots Lab · ${meta.kind}`;

  const dateLine = meta.published_at || "n.d.";
  const updatedLine =
    meta.updated_at && meta.updated_at !== meta.published_at
      ? `Updated ${meta.updated_at}`
      : null;
  const brief = meta.program ? BRIEF_DETAILS[meta.program] : undefined;

  return (
    <article className="ed-paper reveal">
      {/* === Cover page === */}
      <header className="ed-paper-cover">
        <div className="ed-paper-series">{seriesLine}</div>
        <div className="ed-paper-date">
          {dateLine}
          {updatedLine ? ` · ${updatedLine}` : ""}
        </div>

        <h1 className="ed-paper-title">{meta.title}</h1>
        {meta.subtitle && <p className="ed-paper-subtitle">{meta.subtitle}</p>}

        <div className="ed-paper-byline">
          {meta.authors.length > 0 && (
            <div className="ed-paper-authors">{meta.authors.join(", ")}</div>
          )}
          <div className="ed-paper-affiliation">Asian Development Bank</div>
        </div>

        {meta.attestation_chain && (
          <div
            className={`ed-paper-attest ed-paper-attest-${meta.attestation_chain}`}
          >
            <span className="ed-paper-attest-label">Attestation chain:</span>{" "}
            <strong>{meta.attestation_chain}</strong>
            {meta.constitution_ref ? ` · ${meta.constitution_ref}` : ""}
            {meta.review_external_chain && (
              <>
                <br />
                <span className="ed-paper-attest-label">Red team:</span>{" "}
                {meta.review_external_chain}
              </>
            )}
            {meta.review_internal_chain && (
              <>
                <br />
                <span className="ed-paper-attest-label">Internal:</span>{" "}
                {meta.review_internal_chain}
              </>
            )}
          </div>
        )}

        {meta.abstract && (
          <section className="ed-paper-abstract">
            <h2>Abstract</h2>
            <p>{meta.abstract}</p>
          </section>
        )}

        {brief && (
          <section className="ed-paper-reading-hook">
            <h2>Read This First</h2>
            <div className="ed-paper-reading-grid">
              <div>
                <span>Question</span>
                <p>{brief.question}</p>
              </div>
              <div>
                <span>What the data show</span>
                <p>{brief.output}</p>
              </div>
              <div>
                <span>Source line</span>
                <p>{brief.sourceNote}</p>
              </div>
              <div>
                <span>Caveat</span>
                <p>{brief.caveat}</p>
              </div>
            </div>
          </section>
        )}

        <dl className="ed-paper-meta">
          {meta.geographies?.length > 0 && (
            <>
              <dt>Geographies</dt>
              <dd>{meta.geographies.join(" · ")}</dd>
            </>
          )}
          {meta.topics?.length > 0 && (
            <>
              <dt>Keywords</dt>
              <dd>{meta.topics.join(" · ")}</dd>
            </>
          )}
          {meta.maturity && (
            <>
              <dt>Claim maturity</dt>
              <dd>{meta.maturity}</dd>
            </>
          )}
          {meta.doi && (
            <>
              <dt>DOI</dt>
              <dd>
                <a
                  href={`https://doi.org/${meta.doi}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  {meta.doi}
                </a>
              </dd>
            </>
          )}
          {meta.program && meta.program !== "meta" && (
            <>
              <dt>Permanent archive</dt>
              <dd>
                <Link to={`/program/${meta.program}/evidence`}>
                  /program/{meta.program}/evidence
                </Link>
              </dd>
            </>
          )}
        </dl>

        <div className="ed-paper-disclaimer">
          The views expressed in this working paper are those of the author and
          do not necessarily reflect the views of the Asian Development Bank.
          The author accepts responsibility for any remaining errors. Published
          under the lab's Constitution at <code>CONSTITUTION.md</code> (§18
          AI-First Operating Mode currently active; see the attestation chain
          above).
        </div>
      </header>

      <hr className="ed-paper-rule" />

      {/* === Body — auto-numbered sections === */}
      <div
        className="ed-paper-body"
        dangerouslySetInnerHTML={{ __html: html }}
      />

      <hr className="ed-paper-rule" />

      {/* === Appendix — link to evidence packet === */}
      {meta.program && meta.program !== "meta" && (
        <section className="ed-paper-appendix">
          <h2>Appendix A — Evidence packet</h2>
          <p>
            The full evidence packet for this paper — pre-registration,
            sensitivity suite (±50% per Constitution §6.6), coverage table,
            internal review, external red-team review, limitations, and the
            committed source code that produced every number — is at the
            permanent self-hosted archive:{" "}
            <Link to={`/program/${meta.program}/evidence`}>
              /program/{meta.program}/evidence
            </Link>
            .
          </p>
          <p>
            A clean clone of the upstream repository at the publication commit
            reproduces every value in this paper without any API key or live
            network call. Per Constitution §11.
          </p>
        </section>
      )}

      <nav className="ed-paper-nav">
        <Link to="/findings">← Back to findings</Link>
        {meta.program && meta.program !== "meta" && (
          <Link to={`/program/${meta.program}/evidence`}>
            Evidence packet →
          </Link>
        )}
      </nav>
    </article>
  );
}
