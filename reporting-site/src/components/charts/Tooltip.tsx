import type { ReactNode } from "react";
import { C, FONT_MONO, FONT_SANS } from "../../lib/charts/tokens";

/**
 * HoverCard — an absolutely-positioned tooltip box. The parent must be
 * position:relative. x/y are pixel coords within the parent; the card flips
 * left near the right edge and clamps vertically so it never spills off the
 * top or bottom of the chart.
 */
export function HoverCard({
  x,
  y,
  containerWidth,
  containerHeight,
  children,
}: {
  x: number;
  y: number;
  containerWidth: number;
  containerHeight?: number;
  children: ReactNode;
}) {
  const CARD_W = 188;
  const flip = x + CARD_W + 18 > containerWidth;
  const left = flip ? x - CARD_W - 14 : x + 14;
  // translateY(-50%) centres the card on `top`; clamp so neither half leaves
  // the chart box when hovering a point/bar near the top or bottom edge.
  const top = containerHeight ? Math.max(14, Math.min(y, containerHeight - 14)) : y;
  return (
    <div
      role="tooltip"
      style={{
        position: "absolute",
        left: Math.max(2, left),
        top,
        width: CARD_W,
        maxHeight: 220,
        overflow: "hidden",
        transform: "translateY(-50%)",
        pointerEvents: "none",
        background: C.paper,
        border: `1px solid ${C.rule}`,
        boxShadow: "0 6px 24px rgba(33,37,41,0.14)",
        borderRadius: 6,
        padding: "9px 11px",
        fontFamily: FONT_SANS,
        fontSize: 12.5,
        lineHeight: 1.4,
        color: C.ink,
        zIndex: 5,
      }}
    >
      {children}
    </div>
  );
}

export function TipTitle({ children }: { children: ReactNode }) {
  return (
    <div style={{ fontWeight: 700, marginBottom: 4, fontSize: 13.5 }}>{children}</div>
  );
}

export function TipRow({ k, v, accent }: { k: string; v: ReactNode; accent?: boolean }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
      <span style={{ color: C.inkFaint }}>{k}</span>
      <span
        style={{
          fontFamily: FONT_MONO,
          fontWeight: accent ? 700 : 500,
          color: accent ? C.accentStrong : C.inkSoft,
        }}
      >
        {v}
      </span>
    </div>
  );
}
