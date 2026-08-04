/**
 * Layout.tsx — minimal site chrome.
 *
 * Minimal institutional site chrome.
 */
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

function navClass(pathname: string, href: string) {
  const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
  return "site-nav-link " + (active ? "site-nav-link-active" : "");
}

export default function Layout({ children }: { children: ReactNode }) {
  const pathname = usePathname() ?? "/";

  return (
    <div className="site-page">
      {/* Header */}
      <header className="site-header">
        <div className="site-shell site-header-row">
          <Link href="/" className="site-brand">
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
            <Link href="/" className={navClass(pathname, "/")}>
              Home
            </Link>
            <Link href="/research" className={navClass(pathname, "/research")}>
              Research
            </Link>
            <Link href="/explore" className={navClass(pathname, "/explore")}>
              Explore
            </Link>
            <Link href="/review" className={navClass(pathname, "/review")}>
              Review
            </Link>
            <Link href="/showcase" className={navClass(pathname, "/showcase")}>
              Explorations
            </Link>
            <Link href="/about" className={navClass(pathname, "/about")}>
              About
            </Link>
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
        {children}
      </main>

      {/* Footer */}
      <footer className="site-footer">
        <div className="site-shell site-footer-row">
          <div className="site-footer-copy">
            Development Evidence Lab measures what public data can and cannot
            yet prove across Asian Development Bank developing member economies.
            AI assistance is disclosed; every empirical value traces to a
            committed script.
          </div>
          <div className="site-footer-links">
            <Link href="/review">Review desk</Link>
            <Link href="/about">About</Link>
            <Link href="/data-architecture">Data architecture</Link>
            <Link href="/visual-research">Visual standard</Link>
            <Link href="/native-charts">Data visuals</Link>
            <Link href="/deepenings">Evidence checks</Link>
            <Link href="/docs">Docs</Link>
            <Link href="/constitution">Constitution</Link>
            <Link href="/license">License</Link>
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
