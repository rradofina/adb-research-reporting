import { Link } from "react-router-dom";
import { Kicker, Divider, Numeral } from "../components/ui";

interface DatasetRow {
  slug: string;
  name: string;
  publisher: string;
  url: string;
  license: string;
  access: "A" | "B" | "C" | "D" | "E" | "F";
  programs: string[];
  note?: string;
}

const DATASETS: DatasetRow[] = [
  { slug: "wdi", name: "World Bank WDI", publisher: "World Bank", url: "https://databank.worldbank.org/source/world-development-indicators", license: "CC BY 4.0", access: "A", programs: ["all"], note: "1500+ indicators; REST API; values revise across releases." },
  { slug: "doh-nhfr", name: "DOH National Health Facility Registry v2.0", publisher: "DOH Philippines", url: "https://nhfr.doh.gov.ph/VActivefacilitiesList", license: "Unstated; RA 9485 disclosure", access: "A", programs: ["public-service-data-quality"], note: "44,267 active facilities; JWT issued per landing page." },
  { slug: "dghs-bgd", name: "DGHS Facility Registry", publisher: "DGHS Bangladesh", url: "https://hrm.dghs.gov.bd/public/facility-registry", license: "Unstated; public", access: "A", programs: ["public-service-data-quality"], note: "39,421 active facilities; 8 divisions; no auth required." },
  { slug: "rpw", name: "World Bank Remittance Prices Worldwide Q1 2025", publisher: "World Bank", url: "https://remittanceprices.worldbank.org/data-download", license: "World Bank open", access: "A", programs: ["remittance-resilience"], note: "198,000 corridor-firm-period observations globally." },
  { slug: "undesa", name: "UN DESA International Migrant Stock 2024", publisher: "UN DESA Population Division", url: "https://www.un.org/development/desa/pd/content/international-migrant-stock", license: "CC BY 3.0 IGO", access: "A", programs: ["migration-displacement-signals"] },
  { slug: "emdat", name: "EM-DAT International Disaster Database", publisher: "CRED, UCLouvain", url: "https://data.humdata.org/dataset/emdat-country-profiles", license: "Non-commercial open access", access: "A", programs: ["disaster-recovery-lag"] },
  { slug: "wri-gpp", name: "WRI Global Power Plant Database v1.3.0", publisher: "World Resources Institute", url: "https://github.com/wri/global-power-plant-database", license: "CC BY 4.0", access: "A", programs: ["grid-reliability-heat"], note: "Frozen at v1.3.0 since 2022; pin and document age in any output." },
  { slug: "ophi-mpi", name: "OPHI Global MPI 2024", publisher: "Oxford Poverty and Human Development Initiative", url: "https://ophi.org.uk/global-mpi/2024", license: "CC BY 4.0", access: "A", programs: ["mpi-nighttime-lights"] },
  { slug: "openaq", name: "OpenAQ API v3", publisher: "OpenAQ", url: "https://api.openaq.org/v3/", license: "CC BY 4.0", access: "B", programs: ["air-monitoring"], note: "API key required; cache committed to repo so reruns work without a key." },
  { slug: "who-aaq", name: "WHO Ambient Air Quality Database v6.1", publisher: "World Health Organization", url: "https://www.who.int/data/gho/data/themes/air-pollution", license: "WHO open", access: "A", programs: ["air-monitoring"] },
  { slug: "geoboundaries", name: "geoBoundaries gbOpen", publisher: "Center for Geospatial Analysis, William & Mary", url: "https://www.geoboundaries.org/", license: "CC BY 4.0", access: "A", programs: ["all"] },
  { slug: "ookla", name: "Speedtest by Ookla Global Performance", publisher: "Ookla", url: "https://registry.opendata.aws/speedtest-global-performance/", license: "CC BY-NC-SA 4.0", access: "A", programs: ["digital-performance"], note: "NC-SA blocks commercial redistribution of derived products." },
  { slug: "cckp", name: "World Bank Climate Change Knowledge Portal (CMIP6)", publisher: "World Bank", url: "https://climateknowledgeportal.worldbank.org/", license: "World Bank open", access: "A", programs: ["school-heat-disruption", "climate-health-workdays"], note: "Country-mean climatology; not subnational." },
  { slug: "wb-lpi", name: "World Bank Logistics Performance Index", publisher: "World Bank", url: "https://lpi.worldbank.org/", license: "CC BY 4.0", access: "A", programs: ["port-hinterland-friction"], note: "Survey-based; biennial." },
  { slug: "acled", name: "ACLED Conflict Data", publisher: "ACLED", url: "https://acleddata.com/", license: "CC BY-SA 4.0 non-commercial", access: "B", programs: ["migration-displacement-signals"], note: "OAuth credentials required; non-commercial." },
];

const ACCESS_LABEL: Record<DatasetRow["access"], { label: string; tone: "ink" | "sage" | "ochre" | "crimson" }> = {
  A: { label: "Open URL", tone: "sage" },
  B: { label: "Free API + key", tone: "sage" },
  C: { label: "Account required", tone: "ochre" },
  D: { label: "Rate-limited / drift", tone: "ochre" },
  E: { label: "Per-project approval", tone: "crimson" },
  F: { label: "Restricted / paid", tone: "crimson" },
};

export default function DataCatalog() {
  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-12">
        <div className="col-span-12 md:col-span-8">
          <Kicker variant="ochre">Data — sources & licenses</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,4.8rem)] mt-3">
            Where the{" "}
            <span className="display-italic" style={{ color: "var(--ochre)" }}>
              numbers
            </span>{" "}
            come from.
          </h1>
          <p className="lede mt-7 max-w-[60ch]">
            Eighty-plus public datasets across twenty categories, fifty
            ADB regional NSOs, fifty-eight sector ministries, and sixteen
            municipal portals. Every dataset is graded by access model and
            license, and every value here can be retraced.
          </p>
        </div>
        <div className="col-span-12 md:col-span-4 md:pl-6 md:border-l md:border-[var(--rule-soft)] space-y-4">
          <Link
            to="/data/explorer"
            className="block ed-card p-6 group hover:border-ink"
          >
            <Kicker variant="sage">Explorer →</Kicker>
            <h3 className="display-md text-[1.4rem] mt-2 group-hover:text-crimson transition-colors">
              Live SQL view
            </h3>
            <p className="mt-2 marginalia">
              Cross-program vulnerability matrix queryable directly via Supabase REST.
            </p>
          </Link>
          <Link
            to="/data/upgrades"
            className="block ed-card p-6 group hover:border-ink"
          >
            <Kicker variant="ochre">Upgrade matrix →</Kicker>
            <h3 className="display-md text-[1.4rem] mt-2 group-hover:text-crimson transition-colors">
              Better data, lower unit
            </h3>
            <p className="mt-2 marginalia">
              Current source to better source, current unit to target policy unit, topic by topic.
            </p>
          </Link>
        </div>
      </header>

      <Divider />

      {/* Access-model legend */}
      <section className="my-10">
        <Kicker>Access model</Kicker>
        <div className="rule mt-3 mb-4" />
        <ul className="grid sm:grid-cols-3 gap-4 marginalia">
          {(["A", "B", "C", "D", "E", "F"] as const).map((k) => (
            <li key={k} className="flex items-baseline gap-3">
              <span className={"chip chip-" + ACCESS_LABEL[k].tone}>{k}</span>
              <span>{ACCESS_LABEL[k].label}</span>
            </li>
          ))}
        </ul>
      </section>

      <Divider />

      {/* Dataset list */}
      <section className="my-10">
        <Kicker>The catalog</Kicker>
        <div className="rule mt-3" />
        <table className="data-table mt-2">
          <thead>
            <tr>
              <th>№</th>
              <th>Dataset</th>
              <th>Publisher</th>
              <th>License</th>
              <th>Access</th>
              <th>Used by</th>
            </tr>
          </thead>
          <tbody>
            {DATASETS.map((d, i) => (
              <tr key={d.slug}>
                <td className="font-mono text-xs text-ink-faint tabular">{String(i + 1).padStart(2, "0")}</td>
                <td>
                  <a href={d.url} target="_blank" rel="noreferrer" className="ed-link display-md text-base">
                    {d.name}
                  </a>
                  {d.note && <div className="marginalia mt-1">{d.note}</div>}
                </td>
                <td className="text-ink-soft">{d.publisher}</td>
                <td className="font-mono text-xs">{d.license}</td>
                <td>
                  <span className={"chip chip-" + ACCESS_LABEL[d.access].tone}>{d.access}</span>
                </td>
                <td className="font-mono text-xs text-ink-faint">
                  {d.programs.join(", ")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <Divider />

      {/* Highlights */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-16">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="crimson">Watch-outs</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-9 space-y-6">
          <div className="ed-card p-6">
            <h3 className="display-md text-[1.2rem]">Three non-commercial-redistribution sources</h3>
            <p className="mt-2 text-ink-soft leading-relaxed max-w-prose">
              <strong>Ookla Open Data</strong> (CC BY-NC-SA), <strong>ACAG PM2.5 V6</strong>{" "}
              (CC BY-NC), and the <strong>Kyrgyz Republic NSC</strong> open data
              (CC BY-NC-SA) all block commercial redistribution of derived
              products. Fine for ADB and academic publications; flag in any
              commercial-license discussion.
            </p>
          </div>
          <div className="ed-card p-6">
            <h3 className="display-md text-[1.2rem]">OSM Overpass live: the only D-grade source in active use</h3>
            <p className="mt-2 text-ink-soft leading-relaxed max-w-prose">
              OSM is continuously edited; the same query returns different
              results next month. Fix is to pin a Geofabrik dated planet
              extract or switch to Overture Maps (versioned monthly
              releases). Both already documented in the data-access audit.
            </p>
          </div>
          <div className="ed-card p-6">
            <h3 className="display-md text-[1.2rem]">Frozen since 2022: WRI Global Power Plant Database v1.3.0</h3>
            <p className="mt-2 text-ink-soft leading-relaxed max-w-prose">
              No updates since 2022 means the rapid 2022–2025 solar buildouts
              are missing for several DMCs. Use as historical baseline; pair
              with IEA / Ember for current capacity additions.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
