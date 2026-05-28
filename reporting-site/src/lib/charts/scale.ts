/**
 * scale.ts — minimal scale + tick + format helpers (a tiny d3-scale
 * stand-in, no dependency). Linear and sqrt (for bubble area) only.
 */
export type Scale = (v: number) => number;

export function linear(d0: number, d1: number, r0: number, r1: number): Scale {
  const span = d1 - d0 || 1;
  const m = (r1 - r0) / span;
  return (v) => r0 + (v - d0) * m;
}

/** sqrt scale — use for bubble RADIUS so AREA encodes the value. */
export function sqrt(d0: number, d1: number, r0: number, r1: number): Scale {
  const s0 = Math.sqrt(Math.max(0, d0));
  const s1 = Math.sqrt(Math.max(0, d1));
  const span = s1 - s0 || 1;
  const m = (r1 - r0) / span;
  return (v) => r0 + (Math.sqrt(Math.max(0, v)) - s0) * m;
}

function niceStep(span: number, count: number): number {
  const raw = span / Math.max(1, count);
  const mag = 10 ** Math.floor(Math.log10(raw || 1));
  const norm = raw / mag;
  let step: number;
  if (norm < 1.5) step = 1;
  else if (norm < 3) step = 2;
  else if (norm < 7) step = 5;
  else step = 10;
  return step * mag;
}

export function ticks(min: number, max: number, count = 5): number[] {
  if (!isFinite(min) || !isFinite(max) || min === max) return [min];
  const step = niceStep(max - min, count);
  const start = Math.ceil(min / step) * step;
  const out: number[] = [];
  for (let v = start; v <= max + step * 1e-6; v += step) {
    out.push(Math.round(v / step) * step);
  }
  return out;
}

/** Compact number format: 1234567 -> "1.2M", 42.61 -> "42.6". */
export function fmt(n: number, opts: { dp?: number; pct?: boolean } = {}): string {
  if (n == null || !isFinite(n)) return "—";
  const abs = Math.abs(n);
  let s: string;
  if (abs >= 1e12) s = (n / 1e12).toFixed(1) + "T";
  else if (abs >= 1e9) s = (n / 1e9).toFixed(1) + "B";
  else if (abs >= 1e6) s = (n / 1e6).toFixed(1) + "M";
  else if (abs >= 1e3) s = (n / 1e3).toFixed(1) + "k";
  else {
    const dp = opts.dp ?? (abs < 10 ? 1 : 0);
    s = n.toFixed(dp);
  }
  return opts.pct ? s + "%" : s;
}
