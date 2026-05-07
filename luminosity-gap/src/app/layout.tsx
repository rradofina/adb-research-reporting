import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Development Blindspots Lab | ADB Research",
  description:
    "A source-backed research agenda for finding development risks that conventional indicators miss across ADB member economies.",
  openGraph: {
    title: "Development Blindspots Lab",
    description:
      "Four research programs on climate-adjusted access, real internet performance, air-monitoring gaps, and invisible urbanization.",
    type: "website",
  },
};

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/research", label: "Research" },
  { href: "/data-sources", label: "Data Sources" },
  { href: "/methodology", label: "Methodology" },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="min-h-screen bg-zinc-950 font-sans text-zinc-100 antialiased">
        <div className="flex min-h-screen flex-col">
          <header className="top-0 z-50 border-b border-zinc-800 bg-zinc-950/90 backdrop-blur sm:sticky">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="flex min-h-16 flex-col gap-3 py-3 sm:flex-row sm:items-center sm:justify-between sm:py-0">
                <Link href="/" className="flex items-center gap-3">
                  <span className="grid h-8 w-8 place-items-center rounded-lg border border-zinc-700 bg-zinc-900">
                    <span className="h-3 w-3 rounded-full bg-emerald-400" />
                  </span>
                  <span className="text-base font-semibold tracking-tight text-white sm:text-lg">
                    Development Blindspots Lab
                  </span>
                </Link>
                <nav className="-mx-1 flex max-w-full items-center gap-1 overflow-x-auto pb-1 sm:mx-0 sm:overflow-visible sm:pb-0">
                  {NAV_LINKS.map((link) => (
                    <Link
                      key={link.href}
                      href={link.href}
                      className="shrink-0 whitespace-nowrap rounded-lg px-3 py-2 text-sm text-zinc-400 transition-colors hover:bg-zinc-900 hover:text-zinc-100"
                    >
                      {link.label}
                    </Link>
                  ))}
                </nav>
              </div>
            </div>
          </header>

          <main className="flex-1">{children}</main>

          <footer className="border-t border-zinc-800">
            <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-8 text-sm text-zinc-500 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
              <p>
                Adofina &amp; Martinez (2026). Public-data research agenda for
                ADB member economies.
              </p>
              <div className="flex flex-wrap items-center gap-4">
                <Link
                  href="/research"
                  className="transition-colors hover:text-zinc-300"
                >
                  Research Agenda
                </Link>
                <Link
                  href="/methodology"
                  className="transition-colors hover:text-zinc-300"
                >
                  Methodology
                </Link>
                <Link
                  href="/data-sources"
                  className="transition-colors hover:text-zinc-300"
                >
                  Data Sources
                </Link>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
