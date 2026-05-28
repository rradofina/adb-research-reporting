/**
 * tokens.ts — chart palette, mirrored from the site's CSS custom
 * properties in index.css (:root). SVG presentation attributes can take
 * `var(--x)` directly for solid fills; these hex literals are for the
 * places that need real values (sequential ramp interpolation, canvas-
 * free color math). Keep in sync with index.css.
 */
export const C = {
  paper: "#ffffff",
  paperDeep: "#f4f5f6",
  ink: "#212529",
  inkSoft: "#464f58",
  inkFaint: "#687582",
  rule: "rgba(33,37,41,0.16)",
  ruleSoft: "rgba(33,37,41,0.08)",
  accent: "#007db8", // ADB blue (the `--crimson`/`--accent` token)
  accentStrong: "#005f8c",
  sage: "#5a8227",
  ochre: "#b07d12",
  land: "#e7eaed", // neutral context land (no data)
  landLine: "#cfd4d9",
} as const;

export const FONT_SANS =
  '"Source Sans 3", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
export const FONT_MONO = '"JetBrains Mono", ui-monospace, monospace';

function hexToRgb(hex: string): [number, number, number] {
  const h = hex.replace("#", "");
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}
function rgbToHex([r, g, b]: [number, number, number]): string {
  const c = (n: number) => Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, "0");
  return `#${c(r)}${c(g)}${c(b)}`;
}
function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

/**
 * Sequential light→ADB-blue→deep ramp for choropleths. t in [0,1].
 * Light enough at the bottom that labels read over it; deep at the top.
 */
const RAMP_STOPS: Array<[number, [number, number, number]]> = [
  [0.0, hexToRgb("#eef5fa")],
  [0.5, hexToRgb("#5fa8d0")],
  [1.0, hexToRgb("#005f8c")],
];

export function ramp(t: number): string {
  const x = Math.max(0, Math.min(1, t));
  for (let i = 1; i < RAMP_STOPS.length; i++) {
    const [t1, c1] = RAMP_STOPS[i];
    if (x <= t1) {
      const [t0, c0] = RAMP_STOPS[i - 1];
      const f = (x - t0) / (t1 - t0 || 1);
      return rgbToHex([lerp(c0[0], c1[0], f), lerp(c0[1], c1[1], f), lerp(c0[2], c1[2], f)]);
    }
  }
  return rgbToHex(RAMP_STOPS[RAMP_STOPS.length - 1][1]);
}

/** Pick readable text color (ink vs paper) for a given ramp position. */
export function inkOn(t: number): string {
  return t > 0.62 ? C.paper : C.ink;
}
