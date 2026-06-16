/**
 * NativeCharts.tsx — proof-of-concept: the remittance flagship rendered
 * with native, interactive, themed SVG charts instead of a static Python
 * PNG. Every number comes from the SAME committed pipeline JSON a
 * reviewer downloads on the Data tab (/remittance-resilience?view=data) —
 * no value is hard-coded here. Route: /native-charts.
 */
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { loadPanel, loadBasemap, loadCentroids, type Panel } from "../lib/charts/data";
import type { GeoCollection, CentroidIndex } from "../lib/charts/geo";
import { buildRemittanceModel, SDG_CAP } from "../lib/charts/remittanceModel";
import { ChartFrame, ChoroplethMap, RankedBar, Scatter } from "../components/charts";

const SLUG = "remittance-resilience";

interface Sidecar {
  title: string;
  caption: string;
  headline_number: string | null;
  source: string;
  attestation_chain: string;
}

export default function NativeCharts() {
  const [panel, setPanel] = useState<Panel | null>(null);
  const [basemap, setBasemap] = useState<GeoCollection | null>(null);
  const [centroids, setCentroids] = useState<CentroidIndex | null>(null);
  const [sidecar, setSidecar] = useState<Sidecar | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [showPng, setShowPng] = useState(false);

  useEffect(() => {
    let cancel = false;
    Promise.all([
      loadPanel(SLUG),
      loadBasemap(),
      loadCentroids(),
      fetch(`/programs/${SLUG}/generated/charts/${SLUG}-thumbnail.json`)
        .then((r) => (r.ok ? r.json() : null))
        .catch(() => null),
    ]).then(([p, b, c, s]) => {
      if (cancel) return;
      setPanel(p);
      setBasemap(b);
      setCentroids(c);
      setSidecar(s as Sidecar | null);
      setLoaded(true);
    });
    return () => {
      cancel = true;
    };
  }, []);

  const model = useMemo(() => (panel ? buildRemittanceModel(panel) : null), [panel]);

  const source =
    sidecar?.source || "World Bank WDI + Remittance Prices Worldwide Q1 2025";
  const attestation = sidecar?.attestation_chain || "ai-first";

  return (
    <div style={{ maxWidth: "var(--measure-wide-copy)", margin: "0 auto" }}>
      <header style={{ marginBottom: 24 }}>
        <p className="kicker kicker-crimson">Native charts · proof of concept</p>
        <h1 className="home-title" style={{ marginTop: 8 }}>
          The remittance flagship, rendered natively
        </h1>
        <p className="home-lede measure-wide-copy" style={{ marginTop: 12 }}>
          The same finding as the home-page hero, but drawn in the browser
          from the <em>same committed pipeline JSON</em> a reviewer downloads
          on the{" "}
          <Link to={`/${SLUG}?view=data`} className="token-link">
            Data tab
          </Link>
          {" "}— no value is hard-coded in the page. Hover any country, bar, or
          bubble. Resize the window: the type stays crisp instead of shrinking
          like a flattened image. A native chart that reads the committed data
          is <em>more</em> auditable than a screenshot, not less.
        </p>
        <div style={{ marginTop: 12 }}>
          <label style={{ fontSize: 14, cursor: "pointer", userSelect: "none" }}>
            <input
              type="checkbox"
              checked={showPng}
              onChange={(e) => setShowPng(e.target.checked)}
              style={{ marginRight: 8 }}
            />
            Compare against the current static PNG
          </label>
        </div>
      </header>

      {!loaded && <div className="loading-message">Loading committed data…</div>}

      {loaded && (!model || !basemap || !centroids) && (
        <div className="loading-message">
          Could not load the data/basemap. Run{" "}
          <code className="inline-code-token">node scripts/build-webmap.mjs</code>{" "}
          and confirm{" "}
          <code className="inline-code-token">
            /programs/{SLUG}/generated/{SLUG}-adb-panel.json
          </code>{" "}
          exists.
        </div>
      )}

      {model && basemap && centroids && (
        <div style={{ display: "grid", gap: 28 }}>
          {/* MAP */}
          <ChartFrame
            kicker="Map · dependence"
            title={sidecar?.title || "Five economies where remittances are the economy"}
            subtitle="Choropleth = remittances as a share of GDP (WDI, latest year). The five-economy cluster is the repaired baseline corridor-cost x dependence set. Four remain common across the +/-50% sensitivity suite; Tajikistan is shown separately because only one RPW corridor / one firm priced it."
            headline={{ value: model.headline, label: "of Tonga's GDP comes from remittances" }}
            source={source}
            attestation={attestation}
            program={SLUG}
            note={
              <>
                Pacific micro-states (Tonga, Samoa, Vanuatu) are specks on a
                world map — so they get emphasized markers and leader-line
                labels instead of an unreadable shaded pixel. The
                antimeridian (the map runs into Polynesia past 180°) is handled
                by the projection, not a crop.
              </>
            }
          >
            <ChoroplethMap
              basemap={basemap}
              centroids={centroids}
              values={model.values}
              domain={[0, Math.ceil(model.maxGdp)]}
              legendLabel="Remittances, % of GDP"
              unit="%"
              callouts={model.callouts}
            />
          </ChartFrame>

          {showPng && (
            <figure style={{ margin: 0 }}>
              <div
                style={{
                  fontFamily: "var(--font-mono, monospace)",
                  fontSize: 11,
                  textTransform: "uppercase",
                  letterSpacing: "0.16em",
                  color: "var(--ink-faint)",
                  marginBottom: 8,
                }}
              >
                ▾ Current static PNG (Python / matplotlib export) — for comparison
              </div>
              <img
                src={`/programs/${SLUG}/generated/charts/${SLUG}-thumbnail.png`}
                alt="Current static hero PNG"
                style={{ width: "100%", height: "auto", border: "1px solid var(--rule-soft)", borderRadius: 8 }}
              />
            </figure>
          )}

          {/* SCATTER */}
          <ChartFrame
            kicker="Scatter · the two real dimensions"
            title="Dependence × transfer cost — the two factors, not a composite"
            subtitle="Each bubble is an economy with priced RPW corridors. X = remittances as a share of GDP; Y = average transfer cost; bubble area = number of priced corridors. The cluster sits high on dependence with cost at or above the SDG cap. Per §6.4 the composite triage index is never plotted — only the two underlying measured quantities."
            source={source}
            attestation={attestation}
            program={SLUG}
          >
            <Scatter
              data={model.scatter}
              xLabel="Remittances received, % of GDP →"
              yLabel="Avg transfer cost, % →"
              referenceY={{ value: SDG_CAP, label: `SDG 10.c.1 cap · ${SDG_CAP}%` }}
            />
          </ChartFrame>

          {/* BAR */}
          <ChartFrame
            kicker="Ranked · dependence"
            title="Top-12 economies by remittance share of GDP"
            subtitle="Cluster economies in ADB blue; others muted. Tajikistan ranks first on dependence but is not in the cluster (sparse corridor pricing) — visible here as the unhighlighted leader."
            source={source}
            attestation={attestation}
            program={SLUG}
          >
            <RankedBar data={model.bar} unit="%" />
          </ChartFrame>

          <p style={{ fontSize: 13, color: "var(--ink-faint)", lineHeight: 1.5 }}>
            All three charts above read{" "}
            <code className="inline-code-token">
              {SLUG}-adb-panel.json
            </code>
            . The same three components ({"<ChoroplethMap>"},{" "}
            {"<Scatter>"}, {"<RankedBar>"}) plus the editorial frame cover the
            chart forms used across the other programs — bar, scatter/bubble,
            and Asia-Pacific map. Roll-out per program happens as each reaches
            publication stage.
          </p>
        </div>
      )}
    </div>
  );
}
