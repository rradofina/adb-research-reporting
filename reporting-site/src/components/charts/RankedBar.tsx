import { useState } from "react";
import { C, FONT_MONO, FONT_SANS } from "../../lib/charts/tokens";
import { linear } from "../../lib/charts/scale";
import { useContainerWidth } from "./useContainerWidth";
import { HoverCard, TipRow, TipTitle } from "./Tooltip";

export interface BarDatum {
  label: string;
  value: number;
  highlight?: boolean;
  tip?: Array<{ k: string; v: string; accent?: boolean }>;
}

interface RankedBarProps {
  data: BarDatum[];
  unit?: string;
  /** Optional reference line value drawn across the bars (e.g. a cap). */
  reference?: { value: number; label: string };
  valueDp?: number;
}

export function RankedBar({ data, unit = "", reference, valueDp }: RankedBarProps) {
  const [host, width] = useContainerWidth();
  const [hover, setHover] = useState<{ i: number; x: number; y: number } | null>(null);

  const rows = data;
  const W = width || 680;
  const rowH = 32;
  const padTop = reference ? 18 : 6;
  const padBottom = 6;
  const H = padTop + rows.length * rowH + padBottom;
  const labelW = Math.min(124, Math.max(72, W * 0.32));
  const valueW = 50;
  const barAreaW = Math.max(40, W - labelW - valueW);
  const max = Math.max(...rows.map((r) => r.value), reference?.value ?? 0);
  const x = linear(0, max, 0, barAreaW);

  return (
    <div ref={host} style={{ position: "relative", width: "100%" }}>
      <svg
        width={W}
        height={H}
        viewBox={`0 0 ${W} ${H}`}
        style={{ display: "block", width: "100%", height: "auto", fontFamily: FONT_SANS }}
        role="img"
      >
        {reference && (
          <g>
            <line
              x1={labelW + x(reference.value)}
              x2={labelW + x(reference.value)}
              y1={padTop - 4}
              y2={H - padBottom}
              stroke={C.ochre}
              strokeWidth={1}
              strokeDasharray="3 3"
            />
            <text
              x={labelW + x(reference.value)}
              y={padTop - 7}
              textAnchor="middle"
              fontSize={10.5}
              fontFamily={FONT_MONO}
              fill={C.ochre}
            >
              {reference.label}
            </text>
          </g>
        )}
        {rows.map((r, i) => {
          const y = padTop + i * rowH;
          const cy = y + rowH / 2;
          const barLen = Math.max(2, x(r.value));
          const on = r.highlight;
          const active = hover?.i === i;
          return (
            <g key={r.label + i}>
              <text
                x={labelW - 9}
                y={cy}
                textAnchor="end"
                dominantBaseline="middle"
                fontFamily={FONT_MONO}
                fontSize={12}
                fontWeight={on ? 700 : 500}
                fill={on ? C.ink : C.inkSoft}
              >
                {r.label}
              </text>
              <rect
                x={labelW}
                y={y + 5}
                width={barLen}
                height={rowH - 10}
                rx={2}
                fill={on ? C.accent : C.inkFaint}
                opacity={on ? 1 : active ? 0.7 : 0.42}
              />
              <text
                x={labelW + barLen + 7}
                y={cy}
                dominantBaseline="middle"
                fontFamily={FONT_MONO}
                fontSize={11.5}
                fontWeight={on ? 700 : 500}
                fill={on ? C.accentStrong : C.inkFaint}
              >
                {r.value.toFixed(valueDp ?? (r.value < 10 ? 1 : 0))}
                {unit}
              </text>
              <rect
                x={0}
                y={y}
                width={W}
                height={rowH}
                fill="transparent"
                onPointerMove={(e) => {
                  const box = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                  setHover({ i, x: e.clientX - box.left, y: cy });
                }}
                onPointerLeave={() => setHover(null)}
              />
            </g>
          );
        })}
      </svg>
      {hover && rows[hover.i]?.tip && (
        <HoverCard x={hover.x} y={hover.y} containerWidth={W}>
          <TipTitle>{rows[hover.i].label}</TipTitle>
          {rows[hover.i].tip!.map((t) => (
            <TipRow key={t.k} k={t.k} v={t.v} accent={t.accent} />
          ))}
        </HoverCard>
      )}
    </div>
  );
}
