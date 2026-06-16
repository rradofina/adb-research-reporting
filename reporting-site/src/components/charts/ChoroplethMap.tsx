import { useId, useState } from "react";
import { C, FONT_MONO, FONT_SANS, ramp } from "../../lib/charts/tokens";
import {
  ASIA_PACIFIC_VIEW,
  featurePath,
  makeProjector,
  viewHeight,
  type GeoCollection,
  type CentroidIndex,
} from "../../lib/charts/geo";
import { useContainerWidth } from "./useContainerWidth";
import { HoverCard, TipRow, TipTitle } from "./Tooltip";

const OCEAN = "#eef2f5";

export interface Callout {
  iso3: string;
  valueText: string;
  name?: string;
  note?: string;
  kind?: "cluster" | "excluded";
  labelDx?: number;
  labelDy?: number;
  anchor?: "start" | "middle" | "end";
}

interface ChoroplethMapProps {
  basemap: GeoCollection;
  centroids: CentroidIndex;
  values: Record<string, number>;
  domain?: [number, number];
  legendLabel: string;
  callouts: Callout[];
  unit?: string;
  tipFor?: (iso3: string) => Array<{ k: string; v: string; accent?: boolean }> | null;
}

export function ChoroplethMap({
  basemap,
  centroids,
  values,
  domain,
  legendLabel,
  callouts,
  unit = "",
  tipFor,
}: ChoroplethMapProps) {
  const [host, width] = useContainerWidth();
  const [hover, setHover] = useState<{ iso3: string; x: number; y: number } | null>(null);
  const gradId = useId();

  const W = width || 820;
  const PAD_TOP = 4;
  const PAD_BOTTOM = 40; // room for bottom-row Pacific callout labels (TON/VUT) + legend
  const mapH = Math.round(viewHeight(ASIA_PACIFIC_VIEW, W));
  const H = mapH + PAD_TOP + PAD_BOTTOM;
  const baseProject = makeProjector(ASIA_PACIFIC_VIEW, W, mapH);
  const project = (lon: number, lat: number): [number, number] => {
    const [px, py] = baseProject(lon, lat);
    return [px, py + PAD_TOP];
  };

  const vals = Object.values(values);
  const dMin = domain?.[0] ?? 0;
  const dMax = domain?.[1] ?? (vals.length ? Math.max(...vals) : 1);
  const tOf = (v: number) => (dMax === dMin ? 0 : (v - dMin) / (dMax - dMin));

  const onEnter = (iso3: string) => (e: React.PointerEvent) => {
    const svg = (e.currentTarget as SVGElement).ownerSVGElement;
    if (!svg) return;
    const box = svg.getBoundingClientRect();
    setHover({ iso3, x: e.clientX - box.left, y: e.clientY - box.top });
  };

  const tipRows = (iso3: string) => {
    if (tipFor) return tipFor(iso3);
    const v = values[iso3];
    return v == null ? null : [{ k: legendLabel, v: `${v.toFixed(1)}${unit}`, accent: true }];
  };

  const hoverName = hover ? centroids.centroids[hover.iso3]?.name ?? hover.iso3 : "";

  // Legend geometry (bottom-left, in-map)
  const legW = Math.min(150, W * 0.32);
  const legX = 14;
  const legY = H - 26; // in the bottom padding band, below the map area

  if (!width) return <div ref={host} style={{ width: "100%", minHeight: 240 }} />;

  return (
    <div ref={host} style={{ position: "relative", width: "100%" }}>
      <svg
        width={W}
        height={H}
        viewBox={`0 0 ${W} ${H}`}
        style={{ display: "block", width: "100%", height: "auto", fontFamily: FONT_SANS, borderRadius: 8 }}
        role="img"
        aria-label="Asia-Pacific choropleth"
      >
        <defs>
          <linearGradient id={`ramp-${gradId}`} x1="0" x2="1" y1="0" y2="0">
            {[0, 0.25, 0.5, 0.75, 1].map((s) => (
              <stop key={s} offset={`${s * 100}%`} stopColor={ramp(s)} />
            ))}
          </linearGradient>
        </defs>

        <rect x={0} y={0} width={W} height={H} fill={OCEAN} />

        {/* basemap: choropleth where data exists, neutral land otherwise */}
        {basemap.features.map((f, i) => {
          const v = values[f.properties.iso3];
          const has = v != null;
          const active = hover?.iso3 === f.properties.iso3;
          return (
            <path
              key={f.properties.iso3 + i}
              d={featurePath(f, project)}
              fill={has ? ramp(tOf(v)) : C.land}
              stroke={active ? C.accentStrong : C.landLine}
              strokeWidth={active ? 1.4 : 0.5}
              onPointerMove={onEnter(f.properties.iso3)}
              onPointerLeave={() => setHover(null)}
            />
          );
        })}

        {/* callout leader lines + markers + halo labels */}
        {callouts.map((c) => {
          const cen = centroids.centroids[c.iso3];
          if (!cen) return null;
          const [mx, my] = project(cen.lon, cen.lat);
          const dx = c.labelDx ?? 14;
          const dy = c.labelDy ?? -10;
          const lx = mx + dx;
          // clamp so the value line (ly+14) and any note (ly+27) stay on-canvas
          const ly = Math.min(Math.max(my + dy, 14), H - 31);
          const anchor = c.anchor ?? (dx < 0 ? "end" : "start");
          const excluded = c.kind === "excluded";
          const v = values[c.iso3];
          const t = v != null ? tOf(v) : 0;
          return (
            <g key={c.iso3} style={{ cursor: "default" }}>
              <line x1={mx} y1={my} x2={lx} y2={ly} stroke={C.inkFaint} strokeWidth={1} />
              <circle
                cx={mx}
                cy={my}
                r={excluded ? 6 : 6.5}
                fill={excluded ? OCEAN : ramp(Math.max(0.35, t))}
                stroke={excluded ? C.ochre : C.accentStrong}
                strokeWidth={excluded ? 1.6 : 1.6}
                strokeDasharray={excluded ? "2.5 2" : undefined}
                onPointerMove={onEnter(c.iso3)}
                onPointerLeave={() => setHover(null)}
              />
              <text
                x={lx}
                y={ly}
                textAnchor={anchor}
                fontFamily={FONT_MONO}
                fontSize={12}
                fontWeight={700}
                fill={C.ink}
                stroke={C.paper}
                strokeWidth={3}
                paintOrder="stroke"
                style={{ strokeLinejoin: "round" }}
              >
                {c.name ?? cen.name}
              </text>
              <text
                x={lx}
                y={ly + 14}
                textAnchor={anchor}
                fontFamily={FONT_MONO}
                fontSize={11.5}
                fontWeight={700}
                fill={excluded ? C.ochre : C.accentStrong}
                stroke={C.paper}
                strokeWidth={3}
                paintOrder="stroke"
                style={{ strokeLinejoin: "round" }}
              >
                {c.valueText}
              </text>
              {c.note && (
                <text
                  x={lx}
                  y={ly + 27}
                  textAnchor={anchor}
                  fontFamily={FONT_SANS}
                  fontSize={9.5}
                  fontStyle="italic"
                  fill={C.inkFaint}
                  stroke={C.paper}
                  strokeWidth={2.6}
                  paintOrder="stroke"
                  style={{ strokeLinejoin: "round" }}
                >
                  {c.note}
                </text>
              )}
            </g>
          );
        })}

        {/* in-map legend */}
        <g>
          <text x={legX} y={legY - 6} fontSize={10.5} fontFamily={FONT_MONO} fill={C.inkSoft}>
            {legendLabel}
          </text>
          <rect x={legX} y={legY} width={legW} height={8} fill={`url(#ramp-${gradId})`} stroke={C.rule} strokeWidth={0.5} />
          <text x={legX} y={legY + 22} fontSize={10} fontFamily={FONT_MONO} fill={C.inkFaint}>
            {dMin.toFixed(0)}
          </text>
          <text x={legX + legW} y={legY + 22} textAnchor="end" fontSize={10} fontFamily={FONT_MONO} fill={C.inkFaint}>
            {dMax.toFixed(0)}{unit}
          </text>
        </g>
      </svg>

      {hover && tipRows(hover.iso3) && (
        <HoverCard x={hover.x} y={hover.y} containerWidth={W} containerHeight={H}>
          <TipTitle>{hoverName}</TipTitle>
          {tipRows(hover.iso3)!.map((t) => (
            <TipRow key={t.k} k={t.k} v={t.v} accent={t.accent} />
          ))}
        </HoverCard>
      )}
    </div>
  );
}
