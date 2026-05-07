import { Link } from "react-router-dom";
import { useState } from "react";
import { DMCS, SUBREGIONS } from "../lib/dmcs";
import { Kicker, Numeral, Divider } from "../components/ui";

export default function Atlas() {
  const [filter, setFilter] = useState<string>("ALL");
  const [q, setQ] = useState("");

  const filtered = DMCS.filter(
    (d) =>
      (filter === "ALL" || d.subregion === filter) &&
      (q === "" ||
        d.name.toLowerCase().includes(q.toLowerCase()) ||
        d.iso3.toLowerCase().includes(q.toLowerCase())),
  );

  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-12">
        <div className="col-span-12 md:col-span-8">
          <Kicker variant="sage">Atlas — by economy</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,4.8rem)] mt-3">
            Forty-five{" "}
            <span className="display-italic" style={{ color: "var(--sage)" }}>
              dossiers.
            </span>
          </h1>
          <p className="lede mt-6 max-w-[60ch]">
            One profile per ADB regional economy. Every program's view of
            that economy in a single page — fragility scores, distribution
            ranks, source notes, and links to the underlying programs.
          </p>
        </div>
        <div className="col-span-12 md:col-span-4 md:pl-6 md:border-l md:border-[var(--rule-soft)] marginalia">
          The roster covers all 45 ADB regional members. Country-profile
          coverage scales with each program's DMC list — most programs
          carry 38–44 of the 45.
        </div>
      </header>

      <Divider />

      {/* Controls */}
      <div className="flex flex-wrap items-center gap-4 mb-10">
        <div className="kicker">Filter</div>
        <div className="flex flex-wrap gap-2">
          {["ALL", ...SUBREGIONS].map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={
                "px-3 py-1.5 text-xs font-mono uppercase tracking-[0.16em] border transition-colors " +
                (filter === s
                  ? "bg-ink text-paper border-ink"
                  : "bg-transparent text-ink-faint border-[var(--rule)] hover:text-ink hover:border-ink")
              }
            >
              {s === "ALL" ? "All" : s}
            </button>
          ))}
        </div>
        <input
          type="search"
          placeholder="Find a country…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="ml-auto px-3 py-2 bg-transparent border-b border-[var(--rule)] focus:border-ink outline-none font-serif text-sm w-48 md:w-64"
        />
      </div>

      {/* Subregion sections */}
      {SUBREGIONS.map((sub) => {
        const list = filtered.filter((d) => d.subregion === sub);
        if (list.length === 0) return null;
        return (
          <section key={sub} className="py-10 border-b border-[var(--rule-soft)]">
            <div className="grid grid-cols-12 gap-6 lg:gap-10">
              <header className="col-span-12 lg:col-span-3 lg:sticky lg:top-8 self-start">
                <Kicker>Region</Kicker>
                <h2 className="display-md text-[1.7rem] mt-2">{sub}</h2>
                <p className="marginalia mt-2">
                  {list.length} {list.length === 1 ? "economy" : "economies"}
                </p>
              </header>
              <ul className="col-span-12 lg:col-span-9 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-[var(--rule-soft)]">
                {list.map((d, i) => (
                  <li key={d.iso3} className="bg-paper">
                    <Link
                      to={`/dmc/${d.iso3}`}
                      className="group block px-5 py-6 transition-colors hover:bg-paper-deep h-full"
                    >
                      <div className="flex items-baseline justify-between gap-4">
                        <div className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">
                          {d.iso3}
                        </div>
                        <div className="numeral text-base">
                          {String(i + 1).padStart(2, "0")}
                        </div>
                      </div>
                      <h3 className="display-md text-[1.25rem] mt-3 group-hover:text-crimson transition-colors leading-tight">
                        {d.name}
                      </h3>
                      <div className="mt-2 marginalia">{d.subregion}</div>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        );
      })}

      {filtered.length === 0 && (
        <div className="py-20 text-center text-ink-faint">
          No economies match — try a different filter.
        </div>
      )}
    </div>
  );
}
