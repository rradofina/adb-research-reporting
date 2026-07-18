import type { NextConfig } from "next";
import { readFileSync } from "node:fs";

type LegacyArticle = {
  slug: string;
  program?: string;
  tier?: string;
  kind?: string;
};

const VIEW_BY_TIER: Record<string, string> = {
  "working-paper": "paper",
  brief: "brief",
  blog: "blog",
  social: "blog",
  slides: "slides",
  deck: "slides",
};

const articleIndex = JSON.parse(
  readFileSync(new URL("./public/articles/_index.json", import.meta.url), "utf8"),
) as LegacyArticle[];

const legacyFindingRedirects = articleIndex
  .filter((article) => article.program)
  .map((article) => ({
    source: `/findings/${article.slug}`,
    destination: `/${article.program}?view=${VIEW_BY_TIER[article.tier || article.kind || ""] || "paper"}`,
    permanent: false,
  }));

const nextConfig: NextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      ...legacyFindingRedirects,
      { source: "/findings", destination: "/", permanent: false },
      { source: "/articles", destination: "/", permanent: false },
      { source: "/program/:slug/evidence", destination: "/:slug?view=evidence", permanent: false },
      { source: "/program/:slug", destination: "/:slug", permanent: false },
      { source: "/atlas", destination: "/", permanent: false },
      { source: "/dmc/:iso3", destination: "/", permanent: false },
      { source: "/methodology", destination: "/about", permanent: false },
      { source: "/reproducibility", destination: "/about", permanent: false },
      { source: "/team", destination: "/about", permanent: false },
      { source: "/data", destination: "/", permanent: false },
      { source: "/data/upgrades", destination: "/upgrades", permanent: false },
      { source: "/data/explorer", destination: "/", permanent: false },
      { source: "/data/matrix", destination: "/", permanent: false },
      { source: "/live", destination: "/", permanent: false },
      { source: "/matrix", destination: "/", permanent: false },
    ];
  },
  async headers() {
    return [
      {
        source: "/data/:path*",
        headers: [{ key: "Cache-Control", value: "public, max-age=300, s-maxage=600" }],
      },
      {
        source: "/programs/:path*",
        headers: [{ key: "Cache-Control", value: "public, max-age=300, s-maxage=600" }],
      },
    ];
  },
};

export default nextConfig;
