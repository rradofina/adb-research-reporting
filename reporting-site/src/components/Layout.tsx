/**
 * Layout.tsx — minimal site chrome.
 *
 * Drops the editorial chrome (§18 ACTIVE banner, VOL I — № 04, "A
 * MEASUREMENT-GAP PUBLICATION", "The Blindspots Lab" branding) in
 * favor of a simple header (logo + small nav) and a small footer.
 * The brand is "ADB AI Research".
 */
import { Link, NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col bg-paper">
      {/* Header */}
      <header className="border-b border-ink-200 bg-paper">
        <div className="max-w-[1200px] mx-auto px-6 lg:px-10 h-16 flex items-center justify-between gap-6">
          <Link to="/" className="flex items-baseline gap-2 group">
            <span className="text-lg font-semibold tracking-tight text-ink-900">
              ADB AI Research
            </span>
            <span className="hidden sm:inline text-xs uppercase tracking-[0.18em] text-ink-500 group-hover:text-ink-700">
              measurement gaps · public data
            </span>
          </Link>
          <nav className="flex items-center gap-5 text-sm">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                "py-2 text-ink-700 hover:text-ink-900 " +
                (isActive ? "text-ink-900 font-medium" : "")
              }
            >
              Topics
            </NavLink>
            <NavLink
              to="/about"
              className={({ isActive }) =>
                "py-2 text-ink-700 hover:text-ink-900 " +
                (isActive ? "text-ink-900 font-medium" : "")
              }
            >
              About
            </NavLink>
            <a
              href="https://github.com/rradofina/adb-research-reporting"
              target="_blank"
              rel="noreferrer"
              className="py-2 text-ink-700 hover:text-ink-900"
            >
              GitHub ↗
            </a>
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 max-w-[1200px] w-full mx-auto px-6 lg:px-10 py-10 lg:py-14">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="mt-20 border-t border-ink-200 bg-paper">
        <div className="max-w-[1200px] mx-auto px-6 lg:px-10 py-10 grid sm:grid-cols-2 gap-6 text-sm text-ink-600">
          <div className="leading-relaxed max-w-prose">
            ADB AI Research — public-data measurement-gap research on
            Asian Development Bank developing member economies.
            AI-attested under a written constitution.
          </div>
          <div className="flex flex-wrap items-start sm:justify-end gap-x-5 gap-y-2 text-xs uppercase tracking-[0.18em]">
            <Link to="/about" className="hover:text-ink-900">About</Link>
            <Link to="/docs" className="hover:text-ink-900">Docs</Link>
            <Link to="/constitution" className="hover:text-ink-900">Constitution</Link>
            <Link to="/license" className="hover:text-ink-900">License</Link>
            <a
              href="https://github.com/rradofina/adb-research-reporting"
              target="_blank"
              rel="noreferrer"
              className="hover:text-ink-900"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
