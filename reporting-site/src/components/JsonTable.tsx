// Renders a JSON array (or top-level array-valued field) as an
// editorial data-table. Used to expose sensitivity-runs.json and
// generated panel JSONs inline on the Evidence page.

interface JsonTableProps {
  rows: Record<string, unknown>[];
  maxRows?: number;
  highlightCols?: string[];
}

function formatCell(v: unknown): string {
  if (v === null || v === undefined) return "—";
  if (typeof v === "number") {
    if (Math.abs(v) < 0.0001 || Math.abs(v) > 1e9) return v.toExponential(2);
    if (Number.isInteger(v)) return v.toLocaleString();
    return Number(v.toFixed(4)).toString();
  }
  if (typeof v === "boolean") return v ? "true" : "false";
  if (Array.isArray(v)) return `[${v.length} items]`;
  if (typeof v === "object") return `{${Object.keys(v as object).length} keys}`;
  const s = String(v);
  return s.length > 64 ? s.slice(0, 60) + "…" : s;
}

export function JsonTable({ rows, maxRows = 50, highlightCols = [] }: JsonTableProps) {
  if (!rows || rows.length === 0) return <div className="marginalia">(empty)</div>;
  const displayRows = rows.slice(0, maxRows);
  const cols = Array.from(
    new Set(displayRows.flatMap((r) => Object.keys(r))),
  );

  return (
    <div className="ed-json-table-wrap">
      <table className="data-table ed-json-table">
        <thead>
          <tr>
            {cols.map((c) => (
              <th
                key={c}
                style={{
                  color: highlightCols.includes(c) ? "var(--crimson)" : undefined,
                  fontWeight: highlightCols.includes(c) ? 600 : undefined,
                }}
              >
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {displayRows.map((r, i) => (
            <tr key={i}>
              {cols.map((c) => (
                <td
                  key={c}
                  className="font-mono text-xs tabular"
                  style={{
                    color: highlightCols.includes(c) ? "var(--crimson)" : undefined,
                  }}
                >
                  {formatCell(r[c])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {rows.length > maxRows && (
        <div className="marginalia mt-2">
          showing {maxRows} of {rows.length} rows
        </div>
      )}
    </div>
  );
}
