// Hand-rolled syntax highlighter for Python + JS/TS using the lab's
// editorial palette. No external dependencies. Output is HTML with
// classes ed-tok-* that resolve to var(--ink), var(--crimson),
// var(--ochre), var(--sage), var(--ink-faint) in index.css.

const PY_KEYWORDS = new Set([
  "and", "as", "assert", "async", "await", "break", "class", "continue",
  "def", "del", "elif", "else", "except", "finally", "for", "from",
  "global", "if", "import", "in", "is", "lambda", "nonlocal", "not",
  "or", "pass", "raise", "return", "try", "while", "with", "yield",
  "True", "False", "None",
]);

const JS_KEYWORDS = new Set([
  "abstract", "as", "async", "await", "break", "case", "catch", "class",
  "const", "continue", "debugger", "default", "delete", "do", "else",
  "enum", "export", "extends", "false", "finally", "for", "from",
  "function", "if", "implements", "import", "in", "instanceof",
  "interface", "let", "new", "null", "of", "package", "private",
  "protected", "public", "return", "static", "super", "switch", "this",
  "throw", "true", "try", "type", "typeof", "undefined", "var", "void",
  "while", "with", "yield",
]);

function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));
}

interface Token { type: string; value: string; }

function tokenizePython(src: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  while (i < src.length) {
    const rest = src.slice(i);

    // Comment to end of line
    if (rest.startsWith("#")) {
      const end = rest.indexOf("\n");
      const len = end === -1 ? rest.length : end;
      tokens.push({ type: "comment", value: rest.slice(0, len) });
      i += len;
      continue;
    }

    // Triple-quoted strings
    const tq = rest.match(/^("""[\s\S]*?"""|'''[\s\S]*?''')/);
    if (tq) {
      tokens.push({ type: "string", value: tq[1] });
      i += tq[1].length;
      continue;
    }

    // Single/double quoted strings (with escape handling)
    const sq = rest.match(/^("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')/);
    if (sq) {
      tokens.push({ type: "string", value: sq[1] });
      i += sq[1].length;
      continue;
    }

    // Numbers
    const num = rest.match(/^-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/);
    if (num) {
      tokens.push({ type: "number", value: num[0] });
      i += num[0].length;
      continue;
    }

    // Identifiers / keywords
    const id = rest.match(/^[A-Za-z_][A-Za-z0-9_]*/);
    if (id) {
      const word = id[0];
      if (PY_KEYWORDS.has(word)) {
        tokens.push({ type: "keyword", value: word });
      } else if (/^[A-Z]/.test(word)) {
        tokens.push({ type: "type", value: word });
      } else {
        tokens.push({ type: "ident", value: word });
      }
      i += word.length;
      continue;
    }

    // Whitespace + newline (preserve)
    const ws = rest.match(/^\s+/);
    if (ws) {
      tokens.push({ type: "ws", value: ws[0] });
      i += ws[0].length;
      continue;
    }

    // Punctuation, operators
    tokens.push({ type: "punct", value: rest[0] });
    i++;
  }
  return tokens;
}

function tokenizeJs(src: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  while (i < src.length) {
    const rest = src.slice(i);

    // Line comment
    if (rest.startsWith("//")) {
      const end = rest.indexOf("\n");
      const len = end === -1 ? rest.length : end;
      tokens.push({ type: "comment", value: rest.slice(0, len) });
      i += len;
      continue;
    }

    // Block comment
    if (rest.startsWith("/*")) {
      const end = rest.indexOf("*/");
      const len = end === -1 ? rest.length : end + 2;
      tokens.push({ type: "comment", value: rest.slice(0, len) });
      i += len;
      continue;
    }

    // Template literal
    if (rest.startsWith("`")) {
      // Find unescaped closing backtick
      let j = 1;
      while (j < rest.length) {
        if (rest[j] === "\\") { j += 2; continue; }
        if (rest[j] === "`") { j++; break; }
        j++;
      }
      tokens.push({ type: "string", value: rest.slice(0, j) });
      i += j;
      continue;
    }

    // Single/double quoted strings
    const sq = rest.match(/^("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')/);
    if (sq) {
      tokens.push({ type: "string", value: sq[1] });
      i += sq[1].length;
      continue;
    }

    // Numbers
    const num = rest.match(/^-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/);
    if (num) {
      tokens.push({ type: "number", value: num[0] });
      i += num[0].length;
      continue;
    }

    // Identifiers / keywords
    const id = rest.match(/^[A-Za-z_$][A-Za-z0-9_$]*/);
    if (id) {
      const word = id[0];
      if (JS_KEYWORDS.has(word)) {
        tokens.push({ type: "keyword", value: word });
      } else if (/^[A-Z]/.test(word)) {
        tokens.push({ type: "type", value: word });
      } else {
        tokens.push({ type: "ident", value: word });
      }
      i += word.length;
      continue;
    }

    // Whitespace
    const ws = rest.match(/^\s+/);
    if (ws) {
      tokens.push({ type: "ws", value: ws[0] });
      i += ws[0].length;
      continue;
    }

    tokens.push({ type: "punct", value: rest[0] });
    i++;
  }
  return tokens;
}

export function highlight(src: string, language: "python" | "javascript"): string {
  const tokens = language === "python" ? tokenizePython(src) : tokenizeJs(src);
  return tokens
    .map((t) => {
      if (t.type === "ws" || t.type === "punct") return escapeHtml(t.value);
      return `<span class="ed-tok-${t.type}">${escapeHtml(t.value)}</span>`;
    })
    .join("");
}
