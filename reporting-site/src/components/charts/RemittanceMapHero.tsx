import { useEffect, useState, type ReactNode } from "react";
import { loadPanel, loadBasemap, loadCentroids } from "../../lib/charts/data";
import { buildRemittanceModel, type RemittanceModel } from "../../lib/charts/remittanceModel";
import type { GeoCollection, CentroidIndex } from "../../lib/charts/geo";
import type { HeroVisual } from "../../lib/evidence";
import { ChoroplethMap } from "./ChoroplethMap";

const SLUG = "remittance-resilience";

/**
 * In-context hero: renders the remittance map natively (interactive SVG)
 * in place of the static PNG on the Topic page. While data/basemap load —
 * or if anything fails — it renders `fallback` (the PNG figure), so the
 * page never regresses. The §18.2 attestation label is shown as real
 * text in the caption, same as the PNG path.
 */
export function RemittanceMapHero({
  hero,
  fallback,
}: {
  hero: HeroVisual;
  fallback: ReactNode;
}) {
  const [model, setModel] = useState<RemittanceModel | null>(null);
  const [basemap, setBasemap] = useState<GeoCollection | null>(null);
  const [centroids, setCentroids] = useState<CentroidIndex | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let cancel = false;
    Promise.all([loadPanel(SLUG), loadBasemap(), loadCentroids()])
      .then(([p, b, c]) => {
        if (cancel) return;
        const m = p ? buildRemittanceModel(p) : null;
        if (!m || !b || !c) {
          setFailed(true);
          return;
        }
        setModel(m);
        setBasemap(b);
        setCentroids(c);
      })
      .catch(() => !cancel && setFailed(true));
    return () => {
      cancel = true;
    };
  }, []);

  if (failed) return <>{fallback}</>;
  if (!model || !basemap || !centroids) return <>{fallback}</>;

  return (
    <figure className="topic-hero">
      <ChoroplethMap
        basemap={basemap}
        centroids={centroids}
        values={model.values}
        domain={model.domain}
        legendLabel="Remittances, % of GDP"
        unit="%"
        callouts={model.callouts}
      />
      <figcaption className="topic-hero-caption">
        <span className="topic-hero-caption-text">{hero.caption}</span>
        <span className="topic-hero-caption-meta">
          <span>Interactive map · native SVG (hover for values)</span>
          <span>·</span>
          <span>{hero.source}</span>
          <span>·</span>
          <span>
            attestation:{" "}
            <code className="inline-code-token">{hero.attestation_chain}</code>
          </span>
        </span>
      </figcaption>
    </figure>
  );
}
