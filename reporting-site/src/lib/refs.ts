// BibTeX reference loader. Resolves [@key] citations to author-year and
// builds the References section appended to each article.

export interface RefEntry {
  type: string;
  key: string;
  author?: string;
  title?: string;
  journal?: string;
  institution?: string;
  publisher?: string;
  year?: string;
  volume?: string;
  number?: string;
  pages?: string;
  articleno?: string;
  doi?: string;
  url?: string;
  note?: string;
  short: string;  // "Maina et al. 2019"
  long: string;   // full plain-text citation
}

let _cache: Promise<RefEntry[]> | null = null;

export function loadReferences(): Promise<RefEntry[]> {
  if (!_cache) {
    _cache = fetch("/references.json")
      .then((r) => (r.ok ? r.json() : []))
      .catch(() => []);
  }
  return _cache;
}

export function byKey(refs: RefEntry[]): Map<string, RefEntry> {
  return new Map(refs.map((r) => [r.key, r]));
}

/**
 * Replace `[@key]` tokens in HTML body with author-year + numbered
 * superscript link. Returns the rewritten HTML and the ordered list
 * of refs cited (in order of first appearance).
 */
export function resolveCitations(
  html: string,
  refIndex: Map<string, RefEntry>,
): { html: string; cited: { entry: RefEntry; n: number }[] } {
  const seen = new Map<string, number>();
  const cited: { entry: RefEntry; n: number }[] = [];
  const out = html.replace(/\[@([a-zA-Z0-9_-]+)\]/g, (_full, key) => {
    const entry = refIndex.get(key);
    if (!entry) {
      return `<span class="ref-missing">[?${key}]</span>`;
    }
    let n = seen.get(key);
    if (!n) {
      n = seen.size + 1;
      seen.set(key, n);
      cited.push({ entry, n });
    }
    const doi = entry.doi ? `https://doi.org/${entry.doi}` : entry.url || "#";
    return `<a class="ref-cite" href="${doi}" target="_blank" rel="noreferrer" title="${escapeAttr(entry.long)}">${escapeText(entry.short)}<sup>${n}</sup></a>`;
  });
  return { html: out, cited };
}

function escapeAttr(s: string): string {
  return s.replace(/[&"<>]/g, (c) => ({ "&": "&amp;", '"': "&quot;", "<": "&lt;", ">": "&gt;" }[c]!));
}
function escapeText(s: string): string {
  return s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]!));
}

/** Renders the appended "References" section as HTML. */
export function renderReferenceList(cited: { entry: RefEntry; n: number }[]): string {
  if (cited.length === 0) return "";
  const items = cited.map(({ entry, n }) => {
    const doi = entry.doi ? `https://doi.org/${entry.doi}` : entry.url;
    return `<li id="ref-${n}" value="${n}"><span class="ref-author">${escapeText(entry.author || "")}</span> (${entry.year || "n.d."}). <em>${escapeText(entry.title || "")}</em>. ${escapeText(entry.journal || entry.institution || entry.publisher || "")}${entry.volume ? `, ${entry.volume}${entry.number ? `(${entry.number})` : ""}` : ""}${entry.pages ? `, ${entry.pages}` : ""}.${doi ? ` <a href="${doi}" target="_blank" rel="noreferrer">${entry.doi ? `doi:${entry.doi}` : entry.url}</a>` : ""}</li>`;
  }).join("");
  return `<section class="article-references"><h2>References</h2><ol>${items}</ol></section>`;
}
