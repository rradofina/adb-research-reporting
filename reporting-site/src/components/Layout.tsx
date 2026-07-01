/**
 * Layout.tsx — minimal site chrome.
 *
 * Minimal institutional site chrome.
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
              D
            </span>
            <span className="site-brand-title">
              Development Evidence Lab
            </span>
            <span className="site-brand-kicker">
              Asia-Pacific public data
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
              Home
            </NavLink>
            <Link to="/#topics" className="site-nav-link">
              Topics
            </Link>
            <NavLink
              to="/showcase"
              className={({ isActive }) =>
                "site-nav-link " + (isActive ? "site-nav-link-active" : "")
              }
            >
              Evidence
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
            Development Evidence Lab presents public-data measurement research
            on Asian Development Bank developing member economies. AI assistance
            is disclosed and empirical values trace to committed scripts.
          </div>
          <div className="site-footer-links">
            <Link to="/about">About</Link>
            <Link to="/native-charts">Data visuals</Link>
            <Link to="/deepenings">Evidence checks</Link>
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
