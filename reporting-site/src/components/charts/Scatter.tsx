import { useState } from "react";
import { C, FONT_MONO, FONT_SANS } from "../../lib/charts/tokens";
import { linear, sqrt, ticks as niceTicks } from "../../lib/charts/scale";
import { useContainerWidth } from "./useContainerWidth";
import { HoverCard, TipRow, TipTitle } from "./Tooltip";

export interface PointDatum {
  label: string;
  x: number;
  y: number;
  size?: number;
  highlight?: boolean;
  tip?: Array<{ k: string; v: string; accent?: boolean }>;
}

interface ScatterProps {
  data: PointDatum[];
  xLabel: string;
  yLabel: string;
  xLog?: boolean;
  yLog?: boolean;
  referenceY?: { value: number; label: string };
  referenceX?: { value: number; label: string };
  /** Label only the highlighted points (keeps the field uncluttered). */
  labelHighlighted?: boolean;
}

function makeScale(min: number, max: number, r0: number, r1: number, log?: boolean) {
  if (log) {
    const l0 = Math.log10(Math.max(min, 1e-6));
    const l1 = Math.log10(Math.max(max, 1e-6));
    const lin = linear(l0, l1, r0, r1);
    return (v: number) => lin(Math.log10(Math.max(v, 1e-6)));
  }
  return linear(min, max, r0, r1);
}

function logTicks(min: number, max: number): number[] {
  const out: number[] = [];
  const lo = Math.floor(Math.log10(Math.max(min, 1e-6)));
  const hi = Math.ceil(Math.log10(Math.max(max, 1e-6)));
  for (let p = lo; p <= hi; p++) out.push(10 ** p);
  return out;
}

export function Scatter({
  data,
  xLabel,
  yLabel,
  xLog,
  yLog,
  referenceY,
  referenceX,
  labelHighlighted = true,
}: ScatterProps) {
  const [host, width] = useContainerWidth();
  const [hover, setHover] = useState<{ i: number; x: number; y: number } | null>(null);

  const W = width || 680;
  const H = Math.max(300, Math.min(480, W * 0.6));
  const m = { top: 14, right: 18, bottom: 44, left: 52 };
  const plotW = Math.max(40, W - m.left - m.right);
  const plotH = Math.max(40, H - m.top - m.bottom);

  const xs = data.map((d) => d.x);
  const ys = data.map((d) => d.y);
  const xMinRaw = Math.min(...xs, referenceX?.value ?? Infinity);
  const xMaxRaw = Math.max(...xs, referenceX?.value ?? -Infinity);
  const yMinRaw = Math.min(...ys, referenceY?.value ?? Infinity);
  const yMaxRaw = Math.max(...ys, referenceY?.value ?? -Infinity);
  const pad = (lo: number, hi: number) => {
    const s = (hi - lo) * 0.08 || 1;
    return [lo - s, hi + s] as const;
  };
  const [xMin, xMax] = xLog ? [Math.max(xMinRaw, 1e-6), xMaxRaw] : pad(Math.min(0, xMinRaw), xMaxRaw);
  const [yMin, yMax] = yLog ? [Math.max(yMinRaw, 1e-6), yMaxRaw] : pad(Math.min(0, yMinRaw), yMaxRaw);

  const sx = makeScale(xMin, xMax, m.left, m.left + plotW, xLog);
  const sy = makeScale(yMin, yMax, m.top + plotH, m.top, yLog);

  const sizes = data.map((d) => d.size ?? 0);
  const sizeMax = Math.max(...sizes, 1);
  const rOf = sqrt(0, sizeMax, 5, 17);
  const radius = (d: PointDatum) => (d.size != null ? rOf(d.size) : 6.5);

  const xTicks = xLog ? logTicks(xMin, xMax) : niceTicks(xMin, xMax, 6);
  const yTicks = yLog ? logTicks(yMin, yMax) : niceTicks(yMin, yMax, 5);
  const fmtT = (v: number) => (Math.abs(v) >= 1000 ? `${v / 1000}k` : `${+v.toFixed(1)}`);

  return (
    <div ref={host} style={{ position: "relative", width: "100%" }}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ display: "block", width: "100%", height: "auto", fontFamily: FONT_SANS }} role="img">
        {/* grid + y ticks */}
        {yTicks.map((t) => (
          <g key={`y${t}`}>
            <line x1={m.left} x2={m.left + plotW} y1={sy(t)} y2={sy(t)} stroke={C.ruleSoft} strokeWidth={1} />
            <text x={m.left - 8} y={sy(t)} textAnchor="end" dominantBaseline="middle" fontSize={10.5} fontFamily={FONT_MONO} fill={C.inkFaint}>
              {fmtT(t)}
            </text>
          </g>
        ))}
        {/* x ticks */}
        {xTicks.map((t) => (
          <g key={`x${t}`}>
            <text x={sx(t)} y={m.top + plotH + 16} textAnchor="middle" fontSize={10.5} fontFamily={FONT_MONO} fill={C.inkFaint}>
              {fmtT(t)}
            </text>
          </g>
        ))}
        {/* reference lines */}
        {referenceY && (
          <g>
            <line x1={m.left} x2={m.left + plotW} y1={sy(referenceY.value)} y2={sy(referenceY.value)} stroke={C.ochre} strokeWidth={1.2} strokeDasharray="4 3" />
            <text x={m.left + plotW} y={sy(referenceY.value) - 5} textAnchor="end" fontSize={10.5} fontFamily={FONT_MONO} fill={C.ochre}>
              {referenceY.label}
            </text>
          </g>
        )}
        {referenceX && (
          <line x1={sx(referenceX.value)} x2={sx(referenceX.value)} y1={m.top} y2={m.top + plotH} stroke={C.ochre} strokeWidth={1.2} strokeDasharray="4 3" />
        )}
        {/* axis titles */}
        <text x={m.left + plotW / 2} y={H - 6} textAnchor="middle" fontSize={11.5} fill={C.inkSoft}>
          {xLabel}
        </text>
        <text transform={`translate(13 ${m.top + plotH / 2}) rotate(-90)`} textAnchor="middle" fontSize={11.5} fill={C.inkSoft}>
          {yLabel}
        </text>
        {/* points */}
        {data.map((d, i) => {
          const on = d.highlight;
          const active = hover?.i === i;
          return (
            <g key={d.label + i}>
              <circle
                cx={sx(d.x)}
                cy={sy(d.y)}
                r={radius(d)}
                fill={on ? C.accent : C.inkFaint}
                fillOpacity={on ? 0.82 : 0.34}
                stroke={on ? C.accentStrong : "none"}
                strokeWidth={active ? 2 : 1}
              />
              {labelHighlighted && on && (
                <text
                  x={sx(d.x) + radius(d) + 4}
                  y={sy(d.y)}
                  dominantBaseline="middle"
                  fontSize={11}
                  fontFamily={FONT_MONO}
                  fontWeight={700}
                  fill={C.ink}
                >
                  {d.label}
                </text>
              )}
              <circle
                cx={sx(d.x)}
                cy={sy(d.y)}
                r={radius(d) + 7}
                fill="transparent"
                onPointerMove={(e) => {
                  const box = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                  setHover({ i, x: e.clientX - box.left, y: e.clientY - box.top });
                }}
                onPointerLeave={() => setHover(null)}
              />
            </g>
          );
        })}
      </svg>
      {hover && data[hover.i]?.tip && (
        <HoverCard x={hover.x} y={hover.y} containerWidth={W}>
          <TipTitle>{data[hover.i].label}</TipTitle>
          {data[hover.i].tip!.map((t) => (
            <TipRow key={t.k} k={t.k} v={t.v} accent={t.accent} />
          ))}
        </HoverCard>
      )}
    </div>
  );
}
