import Link from "next/link";
import { marked } from "marked";
import type { ReviewArtifact, ReviewPackage, ReviewRecord } from "@/lib/reviewPackage";
import { formatBytes } from "@/lib/reviewPackage";

marked.setOptions({ gfm: true, breaks: false });

function recordState(rec: ReviewRecord): {
  key: "citable" | "provisional" | "unread";
  label: string;
  note: string;
} {
  if (rec.citable) {
    return {
      key: "citable",
      label: "Citable",
      note: "Identity verified and a locator confirmed by reading the page.",
    };
  }
  if (rec.locator) {
    return {
      key: "provisional",
      label: "Screened",
      note: "The figure was found on this page automatically. Nobody has read the surrounding text yet.",
    };
  }
  return {
    key: "unread",
    label: "Unread",
    note: rec.screen_reason || "Source could not be retrieved for screening.",
  };
}

export default function ReviewShell({
  review,
  artifacts,
}: {
  review: ReviewPackage;
  artifacts: ReviewArtifact[];
}) {
  const c = review.counts;
  const clear = c.citable === c.records;
  const manuscriptHtml = marked.parse(
    // Placeholders are substituted by the DOCX/HTML builders, not here.
    review.manuscript_markdown.replace(/<(TABLE|FIGURE):[A-Z0-9_]+>/g, ""),
  ) as string;

  return (
    <div className="review-page">
      <Link href="/reviews" className="review-back">
        ← Evidence reviews
      </Link>

      <header className="review-hero">
        <div className="review-eyebrow">
          Evidence review · attestation {review.attestation_chain} · maturity{" "}
          {review.maturity}
        </div>
        <h1>{review.title}</h1>
        <p className="review-commission">
          {review.commissioned_by
            ? `Commissioned by ${review.commissioned_by} · `
            : ""}
          {review.commissioned_date} · {c.records} evidence records
        </p>
      </header>

      {/* The standing band comes before the prose on purpose. A reader who
          stops after two paragraphs should still leave knowing how much of
          this document has actually been checked. */}
      <section
        className={`review-standing${clear ? " is-clear" : ""}`}
        aria-labelledby="standing-title"
      >
        <h2 id="standing-title">
          {clear
            ? "Every figure in this review has cleared §2.7."
            : `${c.citable} of ${c.records} figures have cleared §2.7.`}
        </h2>
        <p>
          A figure is citable only when its source identity is machine-verified{" "}
          <em>and</em> someone has read the page it came from. Neither half is
          enough on its own: a transposed DOI digit resolves perfectly to the
          wrong paper, and a number located on the right page can still sit in
          an unrelated table.{" "}
          {!clear && review.citable_blocker
            ? `Remaining work: ${review.citable_blocker}`
            : null}
        </p>
        <ul className="review-counts">
          <li className="review-count">
            <b>{c.citable}</b>
            <span>citable — verified and read</span>
          </li>
          <li className="review-count">
            <b>{c.provisional}</b>
            <span>screened — page found, not read</span>
          </li>
          <li className="review-count">
            <b>{c.unread}</b>
            <span>unread — source not retrievable</span>
          </li>
          <li className="review-count">
            <b>{c.identity_by_doi}</b>
            <span>identity confirmed by DOI</span>
          </li>
        </ul>
      </section>

      <h2 className="review-section-title">Gate state</h2>
      <table className="review-gates">
        <thead>
          <tr>
            <th scope="col">Gate</th>
            <th scope="col">Status</th>
            <th scope="col">Value</th>
          </tr>
        </thead>
        <tbody>
          {review.gate_state.map((gate) => (
            <tr key={gate.label}>
              <td>{gate.label}</td>
              <td>
                <span className={`gate-pill ${gate.status}`}>{gate.status}</span>
              </td>
              <td>{gate.value}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {artifacts.length > 0 && (
        <>
          <h2 className="review-section-title">Download</h2>
          <p className="review-section-note">
            Each file carries its SHA-256 so a reader can confirm they have the
            same bytes this page describes.
          </p>
          <ul className="review-downloads">
            {artifacts.map((file) => (
              <li className="review-download" key={file.name}>
                <a href={file.href} download>
                  {file.ext}
                </a>
                <span>
                  {file.name} · {formatBytes(file.bytes)}
                </span>
                {file.sha256 && <code>{file.sha256.slice(0, 32)}…</code>}
              </li>
            ))}
          </ul>
        </>
      )}

      <h2 className="review-section-title">Evidence register</h2>
      <p className="review-section-note">
        Every record the review rests on, with its provenance state. This is the
        table that lets a reader check us rather than trust us.
      </p>
      <div className="review-table-wrap">
        <table className="review-register">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Status</th>
              <th scope="col">Study</th>
              <th scope="col">Geography</th>
              <th scope="col">Estimate</th>
              <th scope="col">Locator</th>
              <th scope="col">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {review.records.map((rec) => {
              const state = recordState(rec);
              return (
                <tr key={rec.id}>
                  <td className="col-id">{rec.id}</td>
                  <td>
                    <span className={`status-dot ${state.key}`} aria-hidden />
                    <span className="status-label">{state.label}</span>
                    <span className="status-note">{state.note}</span>
                  </td>
                  <td>
                    {rec.doi ? (
                      <a href={`https://doi.org/${rec.doi}`}>{rec.study}</a>
                    ) : rec.url ? (
                      <a href={rec.url}>{rec.study}</a>
                    ) : (
                      rec.study
                    )}
                    <span className="status-note">{rec.source}</span>
                  </td>
                  <td>{rec.geography}</td>
                  <td className="col-estimate">{rec.estimate}</td>
                  <td className="col-locator">
                    {rec.locator || <span className="status-note">none</span>}
                  </td>
                  <td>{rec.confidence}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <h2 className="review-section-title">The review</h2>
      <p className="review-section-note">
        Figures below that belong to screened or unread records have not cleared
        §2.7. They are shown because withholding them would misrepresent what
        the draft says; they are not yet citable.
      </p>
      <article
        className="review-prose"
        dangerouslySetInnerHTML={{ __html: manuscriptHtml }}
      />

      <p className="review-nonclaim">{review.non_claim}</p>
      <p className="review-nonclaim">
        Package generated {review.generated_at} from the committed evidence
        register and gate ledgers.
      </p>
    </div>
  );
}
