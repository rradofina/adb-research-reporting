import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      { source: "/findings", destination: "/", permanent: false },
      { source: "/findings/:slug", destination: "/", permanent: false },
      { source: "/articles", destination: "/", permanent: false },
      { source: "/articles/:slug", destination: "/", permanent: false },
      { source: "/program/:slug/evidence", destination: "/:slug?view=evidence", permanent: false },
      { source: "/program/:slug", destination: "/:slug", permanent: false },
      { source: "/research", destination: "/", permanent: false },
      { source: "/atlas", destination: "/", permanent: false },
      { source: "/dmc/:iso3", destination: "/", permanent: false },
      { source: "/briefs", destination: "/", permanent: false },
      { source: "/methods", destination: "/about", permanent: false },
      { source: "/methodology", destination: "/about", permanent: false },
      { source: "/reproducibility", destination: "/about", permanent: false },
      { source: "/team", destination: "/about", permanent: false },
      { source: "/data", destination: "/", permanent: false },
      { source: "/data/explorer", destination: "/", permanent: false },
      { source: "/data/matrix", destination: "/", permanent: false },
      { source: "/data/upgrades", destination: "/", permanent: false },
      { source: "/archive", destination: "/", permanent: false },
      { source: "/how-to-read", destination: "/about", permanent: false },
      { source: "/glossary", destination: "/about", permanent: false },
      { source: "/references", destination: "/about", permanent: false },
      { source: "/live", destination: "/", permanent: false },
      { source: "/matrix", destination: "/", permanent: false },
      { source: "/upgrades", destination: "/", permanent: false },
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
