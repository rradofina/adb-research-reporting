import { useEffect, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { loadReferences, type RefEntry } from "../lib/refs";
import { Kicker, Divider } from "../components/ui";

export default function References() {
  const [refs, setRefs] = useState<RefEntry[] | null>(null);
  const [filter, setFilter] = useState<string>("");
  const [sort, setSort] = useState<"year" | "author">("year");

  useEffect(() => {
    loadReferences().then(setRefs);
  }, []);

  const sortedFiltered = useMemo(() => {
    if (!refs) return [];
    let r = [...refs];
    if (filter) {
      const f = filter.toLowerCase();
      r = r.filter(
        (x) =>
          (x.title || "").toLowerCase().includes(f) ||
          (x.author || "").toLowerCase().includes(f) ||
          (x.journal || "").toLowerCase().includes(f) ||
          x.key.toLowerCase().includes(f),
      );
    }
    r.sort((a, b) => {
      if (sort === "year") {
        return Number(b.year || 0) - Number(a.year || 0);
      }
      return (a.author || "").localeCompare(b.author || "");
    });
    return r;
  }, [refs, filter, sort]);

  if (!refs) {
    return <div className="py-20 text-center text-ink-faint reveal">Loading references…</div>;
  }

  return (
    <div className="reveal">
      <header className="mb-12 pb-8 border-b border-[var(--rule)]">
        <Kicker>Bibliography</Kicker>
        <h1 className="masthead-display text-[clamp(2.4rem,5vw,4.6rem)] mt-3">
          Every paper{" "}
          <span className="display-italic" style={{ color: "var(--ink-faint)" }}>
            cited.
          </span>
        </h1>
        <p className="lede mt-7 max-w-[60ch]">
          The lab cites by BibTeX key from <code className="font-mono not-italic">references.bib</code>{" "}
          per Constitution §5.3. {refs.length} verified entries. Every program
          and article references this bibliography; click any DOI to read the source.
        </p>
      </header>

      {/* Controls */}
      <div className="flex flex-wrap items-center gap-4 mb-10">
        <div className="kicker">Sort</div>
        <div className="flex gap-2">
          {(["year", "author"] as const).map((s) => (
            <button
              key={s}
              onClick={() => setSort(s)}
              className={
                "px-3 py-1.5 text-xs font-mono uppercase tracking-[0.16em] border transition-colors " +
                (sort === s
                  ? "bg-ink text-paper border-ink"
                  : "bg-transparent text-ink-faint border-[var(--rule)] hover:text-ink hover:border-ink")
              }
            >
              {s === "year" ? "Year" : "First author"}
            </button>
          ))}
        </div>
        <input
          type="search"
          placeholder="Filter by author / title / journal…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="ml-auto px-3 py-2 bg-transparent border-b border-[var(--rule)] focus:border-ink outline-none font-serif text-sm w-48 md:w-72"
        />
      </div>

      {/* List */}
      <ol className="space-y-6 max-w-[78ch]">
        {sortedFiltered.map((r, i) => (
          <li key={r.key} className="border-b border-[var(--rule-soft)] pb-5">
            <div className="flex items-baseline gap-3 flex-wrap mb-2">
              <span className="numeral text-base shrink-0">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">
                {r.short}
              </span>
              <span className="font-mono text-[0.66rem] uppercase tracking-[0.16em] text-ink-faint ml-auto">
                {r.type} · {r.year}
              </span>
            </div>
            <h3 className="display-md text-[1.1rem] leading-snug mt-1">
              {r.doi ? (
                <a
                  href={`https://doi.org/${r.doi}`}
                  target="_blank"
                  rel="noreferrer"
                  className="ed-link"
                >
                  {r.title}
                </a>
              ) : r.url ? (
                <a href={r.url} target="_blank" rel="noreferrer" className="ed-link">
                  {r.title}
                </a>
              ) : (
                r.title
              )}
            </h3>
            <p className="marginalia mt-2 leading-relaxed">{r.author}</p>
            <p className="marginalia mt-1">
              {[r.journal || r.institution || r.publisher, r.volume && `vol. ${r.volume}${r.number ? `(${r.number})` : ""}`, r.pages && `pp. ${r.pages}`]
                .filter(Boolean)
                .join(" · ")}
              {r.doi && (
                <>
                  {" · "}
                  <a
                    href={`https://doi.org/${r.doi}`}
                    target="_blank"
                    rel="noreferrer"
                    className="ed-link"
                  >
                    doi:{r.doi}
                  </a>
                </>
              )}
            </p>
            <p className="marginalia mt-2 text-[0.7rem]">
              <code className="font-mono">@{r.key}</code>
            </p>
          </li>
        ))}
      </ol>

      <Divider wide />

      <nav className="flex items-center justify-between flex-wrap gap-4 pb-12">
        <Link to="/findings" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
          ← Findings
        </Link>
        <Link to="/glossary" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
          Glossary →
        </Link>
      </nav>
    </div>
  );
}
