import { Link, NavLink, Outlet, useLocation } from "react-router-dom";

const PRIMARY_NAV = [
  { to: "/", label: "Home" },
  { to: "/program/public-service-data-quality", label: "Flagship" },
  { to: "/briefs", label: "Briefs" },
  { to: "/research", label: "Research" },
  { to: "/data/upgrades", label: "Data Upgrades" },
  { to: "/atlas", label: "Atlas" },
  { to: "/findings", label: "Findings" },
  { to: "/methods", label: "Methods" },
  { to: "/how-to-read", label: "Guide" },
  { to: "/about", label: "About" },
];

export default function Layout() {
  const loc = useLocation();
  const isHome = loc.pathname === "/";

  return (
    <div className="min-h-screen flex flex-col">
      {/* §18 ACTIVE banner */}
      <div className="bg-ink text-paper">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12 py-2 flex items-center justify-between flex-wrap gap-3 text-[0.66rem] uppercase tracking-[0.22em] font-mono">
          <div className="flex items-center gap-3">
            <span style={{ color: "var(--ochre)" }}>● §18 ACTIVE</span>
            <span className="hidden md:inline">AI-First · Self-hosted permanent archive (§10.3)</span>
            <span className="hidden lg:inline text-paper/70">— every artifact carries <code className="font-mono not-italic">attestation_chain</code></span>
          </div>
          <Link to="/how-to-read" className="ed-link hover:no-underline" style={{ color: "var(--ochre)" }}>Reader's guide →</Link>
        </div>
      </div>

      {/* Top bar — issue line */}
      <div className="border-b border-[var(--rule)]">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12 flex items-center justify-between text-[0.66rem] uppercase tracking-[0.22em] py-2 text-ink-soft font-mono">
          <div className="flex items-center gap-6">
            <span>Vol. I — № 04</span>
            <span className="hidden md:inline">Apr · 2026</span>
            <span className="hidden md:inline text-ink-faint">Constitution-governed · public data only</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/about#governance" className="ed-link hover:no-underline">Governance</Link>
            <span className="hidden sm:inline">·</span>
            <Link to="/about#reproducibility" className="ed-link hover:no-underline hidden sm:inline">Repro</Link>
          </div>
        </div>
      </div>

      {/* Masthead */}
      <header className="border-b border-[var(--rule)]">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12 py-8 lg:py-12">
          <Link to="/" className="block group">
            <div className="flex items-baseline gap-4 lg:gap-6 flex-wrap">
              <h1 className={(isHome ? "masthead-display text-[clamp(2.6rem,7vw,5.5rem)]" : "display-lg text-[clamp(1.6rem,3vw,2.4rem)]") + " text-ink leading-none"}>
                The <span className="display-italic" style={{ color: "var(--crimson)" }}>Blindspots</span> Lab
              </h1>
              <span className="kicker hidden lg:inline ml-auto self-end">A measurement-gap publication</span>
            </div>
            {isHome && (
              <p className="lede mt-6 max-w-[68ch]">
                A research periodical on what official data misses — across
                Asia-Pacific developing economies and beyond. Public data only.
                Every number traces to a committed script and a public source.
              </p>
            )}
          </Link>
        </div>

        {/* Primary nav */}
        <nav className="border-t border-[var(--rule-soft)]">
          <div className="max-w-[1400px] mx-auto px-3 sm:px-6 lg:px-12 flex flex-wrap md:flex-nowrap items-stretch gap-0 overflow-visible md:overflow-x-auto">
            {PRIMARY_NAV.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  "py-3 px-3 lg:px-5 text-xs sm:text-sm font-mono uppercase tracking-[0.18em] whitespace-nowrap transition-colors " +
                  (isActive
                    ? "text-ink border-b-2 border-[var(--crimson)] -mb-px"
                    : "text-ink-faint hover:text-ink")
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </nav>
      </header>

      {/* Main content */}
      <main className="flex-1 max-w-[1400px] w-full mx-auto px-6 lg:px-12 py-10 lg:py-16">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="mt-20 border-t border-[var(--rule)] bg-paper-deep">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12 py-12 grid md:grid-cols-12 gap-8">
          <div className="md:col-span-5">
            <div className="display-lg text-[1.6rem]">
              The <span className="display-italic" style={{ color: "var(--crimson)" }}>Blindspots</span> Lab
            </div>
            <p className="mt-4 text-ink-soft max-w-prose leading-relaxed">
              An auditable research program: every published number traces to
              a committed script, a public dataset, and a recorded retrieval
              timestamp. The Constitution at the upstream repository is the
              binding document; this site is the publishing surface.
            </p>
          </div>

          <div className="md:col-span-3">
            <div className="kicker mb-3">Sections</div>
            <ul className="space-y-2 text-ink">
              <li><Link to="/research" className="ed-link">Research programs</Link></li>
              <li><Link to="/findings" className="ed-link">Findings & articles</Link></li>
              <li><Link to="/atlas" className="ed-link">DMC atlas</Link></li>
              <li><Link to="/data" className="ed-link">Data catalog</Link></li>
              <li><Link to="/data/upgrades" className="ed-link">Data-source upgrades</Link></li>
              <li><Link to="/data/explorer" className="ed-link">Live data explorer</Link></li>
            </ul>
          </div>

          <div className="md:col-span-4">
            <div className="kicker mb-3">Standards</div>
            <ul className="space-y-2 text-ink">
              <li><Link to="/methods" className="ed-link">Methodology</Link></li>
              <li><Link to="/about#governance" className="ed-link">Constitution & governance</Link></li>
              <li><Link to="/about#reproducibility" className="ed-link">Reproducibility</Link></li>
              <li><Link to="/about#ai" className="ed-link">AI transparency</Link></li>
              <li><Link to="/team" className="ed-link">Team & red team</Link></li>
            </ul>
          </div>

          <div className="md:col-span-12 mt-6 pt-6 border-t border-[var(--rule-soft)] flex flex-wrap items-center justify-between gap-4">
            <div className="marginalia">
              Source code MIT. Data per source license — see <Link to="/data" className="ed-link">Data catalog</Link>.
            </div>
            <div className="marginalia">
              Set in Fraunces & Source Serif 4. Numbers in JetBrains Mono.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
