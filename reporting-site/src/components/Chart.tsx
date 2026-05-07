// Hand-rolled SVG bar chart in the lab palette. No external deps.

interface BarRow {
  label: string;
  value: number;
  highlight?: boolean;
}

interface BarChartProps {
  data: BarRow[];
  unit?: string;
  height?: number;
  maxBars?: number;
}

export function BarChart({ data, unit = "", height = 240, maxBars = 12 }: BarChartProps) {
  const rows = data.slice(0, maxBars);
  if (rows.length === 0) return null;
  const max = Math.max(...rows.map((r) => r.value));
  const labelWidth = 80;
  const valueWidth = 60;
  const chartWidth = 100; // percent
  const rowHeight = (height - 20) / rows.length;

  return (
    <div className="ed-chart" style={{ background: "var(--paper)" }}>
      <svg viewBox={`0 0 800 ${height}`} preserveAspectRatio="none" style={{ width: "100%", height: "auto" }}>
        {rows.map((r, i) => {
          const y = 10 + i * rowHeight;
          const barLen = (r.value / max) * (800 - labelWidth - valueWidth - 30);
          const color = r.highlight ? "var(--crimson)" : "var(--ink)";
          return (
            <g key={i}>
              <text
                x={labelWidth - 8}
                y={y + rowHeight / 2 + 4}
                textAnchor="end"
                fontFamily="JetBrains Mono, monospace"
                fontSize="11"
                fill="var(--ink-faint)"
              >
                {r.label}
              </text>
              <rect
                x={labelWidth}
                y={y + 2}
                width={Math.max(barLen, 1)}
                height={rowHeight - 4}
                fill={color}
                opacity={r.highlight ? 1 : 0.78}
              />
              <text
                x={labelWidth + barLen + 6}
                y={y + rowHeight / 2 + 4}
                fontFamily="JetBrains Mono, monospace"
                fontSize="10"
                fill="var(--ink-soft)"
              >
                {typeof r.value === "number" ? r.value.toFixed(2).replace(/\.?0+$/, "") : r.value}
                {unit ? ` ${unit}` : ""}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
