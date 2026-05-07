export default function Sources() {
  return (
    <div>
      <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
        data-access-audit.md — highlights
      </p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">
        Data sources and how to access them.
      </h1>
      <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
        The authoritative audit lives at <code className="font-mono">data-access-audit.md</code> at
        the repository root (~1,086 lines, ~80 sources across 20 categories,
        plus 50 DMC national statistical agencies, 58 sector ministries and
        regulators, and ~16 municipal and regional aggregators). This page
        summarizes access priorities.
      </p>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">Registration priority</h2>
        <p className="mt-2 text-ink-700">
          Sign up in this order — these four platforms unlock most satellite
          and geospatial layers used across the register.
        </p>
        <div className="mt-4 grid md:grid-cols-2 gap-3">
          <AccountCard
            platform="Google Earth Engine"
            url="developers.google.com/earth-engine/guides/noncommercial_tiers"
            note="Unlocks MAP friction, JRC GSW, Dynamic World, Sentinel-1/2/3/5P, MODIS, ESA WorldCover, CHIRPS, WorldPop, GHSL, Open Buildings, VIIRS Black Marble. Tier selection deadline was April 27, 2026; new projects auto-default to Community tier."
            unlocks={["Programs 3, 4, 5, 6, 8, 10, 11, 15, 17"]}
          />
          <AccountCard
            platform="NASA Earthdata Login (URS)"
            url="urs.earthdata.nasa.gov/users/new"
            note="Black Marble VIIRS, MODIS, GPM IMERG, MERRA-2, SEDAC, GDIS."
            unlocks={["Programs 0, 3, 5, 7, 8"]}
          />
          <AccountCard
            platform="Copernicus Data Space Ecosystem"
            url="dataspace.copernicus.eu"
            note="Full Sentinel-1/2/3/5P archive. Replaces the retired Copernicus Open Access Hub."
            unlocks={["Program 3"]}
          />
          <AccountCard
            platform="Copernicus Climate Data Store"
            url="cds.climate.copernicus.eu/user/register"
            note="ERA5 / ERA5-Land reanalysis via cdsapi."
            unlocks={["Programs 5, 8, 9, 10, 11, 14, 15"]}
          />
        </div>
      </section>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">License compatibility</h2>
        <p className="mt-2 text-ink-700 max-w-3xl">
          Most sources in active use are CC-BY-4.0 (commercial OK with attribution)
          or Copernicus-open. <strong>Three watch-outs:</strong>
        </p>
        <ul className="list-disc mt-3 ml-6 space-y-1 text-ink-700">
          <li><strong>Ookla Open Data</strong> — CC BY-NC-SA-4.0, blocks commercial redistribution.</li>
          <li><strong>ACAG PM2.5 V6</strong> (Dalhousie / WashU) — CC BY-NC-4.0.</li>
          <li><strong>Kyrgyz Republic NSC</strong> open data — CC BY-NC-SA.</li>
        </ul>
        <p className="mt-3 text-ink-700 max-w-3xl">
          DHS, MICS, IPUMS, LandScan raw microdata cannot be redistributed in
          the repository. Only derived aggregates with published documentation
          appear in outputs.
        </p>
      </section>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">Reproducibility hazards</h2>
        <ul className="list-disc mt-3 ml-6 space-y-1 text-ink-700">
          <li>
            <strong>OSM Overpass live</strong> is the only D-grade source in
            active use. Data drifts across hours. Fix: pin Geofabrik dated planet
            extract or switch to Overture (versioned releases).
          </li>
          <li>
            <strong>WorldPop stats API</strong> is rate-limited and flaky;
            migrate to raster + zonal stats locally for consistency.
          </li>
          <li>
            <strong>World Bank WDI</strong> revises historical values across
            releases; record retrieval date, not just calendar year.
          </li>
        </ul>
      </section>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">National agencies by DMC region</h2>
        <p className="mt-2 text-ink-700 max-w-3xl">
          Full list of 50 NSOs across Pacific, Central Asia, Caucasus,
          South Asia, Southeast Asia, and East Asia is in{" "}
          <code className="font-mono">data-access-audit.md</code> §10,
          with Pacific regional meta-sources (SPC SDD, PDH.stat, Pacific
          Data Hub). Best-in-region programmatic access: Bhutan NSB
          Interactive Data Portal, Malaysia OpenDOSM, Indonesia BPS Web
          API, Hong Kong CSD, Philippines PSA OpenSTAT.
        </p>
      </section>
    </div>
  );
}

function AccountCard({
  platform,
  url,
  note,
  unlocks,
}: {
  platform: string;
  url: string;
  note: string;
  unlocks: string[];
}) {
  return (
    <div className="bg-white border border-ink-200 rounded-md p-5">
      <div className="font-semibold">{platform}</div>
      <div className="mt-1 text-xs font-mono text-signal-info break-all">
        {url}
      </div>
      <div className="mt-3 text-sm text-ink-700">{note}</div>
      <div className="mt-3 text-xs text-ink-500">
        Unlocks: {unlocks.join(" · ")}
      </div>
    </div>
  );
}
