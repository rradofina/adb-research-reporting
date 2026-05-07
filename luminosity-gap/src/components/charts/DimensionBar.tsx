"use client";

interface DimensionBarProps {
  health: number;
  education: number;
  livingStd: number;
  height?: number;
}

export function DimensionBar({
  health,
  education,
  livingStd,
  height = 8,
}: DimensionBarProps) {
  return (
    <div
      className="w-full rounded-full overflow-hidden flex"
      style={{ height }}
      title={`Health: ${health.toFixed(1)}% | Education: ${education.toFixed(1)}% | Living Standards: ${livingStd.toFixed(1)}%`}
    >
      <div
        className="bg-red-400 transition-all"
        style={{ width: `${health}%` }}
      />
      <div
        className="bg-blue-400 transition-all"
        style={{ width: `${education}%` }}
      />
      <div
        className="bg-emerald-400 transition-all"
        style={{ width: `${livingStd}%` }}
      />
    </div>
  );
}
