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
    <div className="site-page">
      {/* Header */}
      <header className="site-header">
        <div className="site-shell site-header-row">
          <Link to="/" className="site-brand">
            <span className="site-brand-mark" aria-hidden="true">
              A
            </span>
            <span className="site-brand-title">
              ADB AI Research
            </span>
            <span className="site-brand-kicker">
              report bench - public data
            </span>
          </Link>
          <nav className="site-nav">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                "site-nav-link " + (isActive ? "site-nav-link-active" : "")
              }
            >
              Reports
            </NavLink>
            <NavLink
              to="/native-charts"
              className={({ isActive }) =>
                "site-nav-link " + (isActive ? "site-nav-link-active" : "")
              }
            >
              Charts
            </NavLink>
            <NavLink
              to="/deepenings"
              className={({ isActive }) =>
                "site-nav-link " + (isActive ? "site-nav-link-active" : "")
              }
            >
              Deepening checks
            </NavLink>
            <NavLink
              to="/showcase"
              className={({ isActive }) =>
                "site-nav-link " + (isActive ? "site-nav-link-active" : "")
              }
            >
              Showcase
            </NavLink>
            <NavLink
              to="/about"
              className={({ isActive }) =>
                "site-nav-link " + (isActive ? "site-nav-link-active" : "")
              }
            >
              About
            </NavLink>
            <a
              href="https://github.com/rradofina/adb-research-reporting"
              target="_blank"
              rel="noreferrer"
              className="site-nav-link"
            >
              GitHub ↗
            </a>
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="site-shell site-main">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="site-footer">
        <div className="site-shell site-footer-row">
          <div className="site-footer-copy">
            ADB AI Research — public-data measurement-gap research on
            Asian Development Bank developing member economies.
            AI-attested under a written constitution.
          </div>
          <div className="site-footer-links">
            <Link to="/about">About</Link>
            <Link to="/docs">Docs</Link>
            <Link to="/constitution">Constitution</Link>
            <Link to="/license">License</Link>
            <a
              href="https://github.com/rradofina/adb-research-reporting"
              target="_blank"
              rel="noreferrer"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
