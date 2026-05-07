/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        // Display: Fraunces — characterful serif with optical-sizing,
        // designed for editorial presence at large sizes.
        display: [
          '"Fraunces"',
          "ui-serif",
          "Georgia",
          "Cambria",
          "Times New Roman",
          "serif",
        ],
        // Body: Source Serif 4 — long-form readability + subtle elegance.
        serif: [
          '"Source Serif 4"',
          '"Source Serif Pro"',
          "ui-serif",
          "Georgia",
          "Cambria",
          "serif",
        ],
        // Mono: JetBrains Mono — clear data tables and metadata stamps.
        mono: [
          '"JetBrains Mono"',
          "ui-monospace",
          "Menlo",
          "Consolas",
          "monospace",
        ],
        // Fallback sans for stamps and meta where serif is too soft.
        sans: [
          '"Source Serif 4"',
          "ui-serif",
          "Georgia",
          "serif",
        ],
      },
      colors: {
        // Paper — warm off-white, a printed page, not a screen
        paper: {
          DEFAULT: "#f6f3ec",
          50: "#fbf9f4",
          100: "#f6f3ec",
          200: "#ece6d6",
          300: "#dcd4be",
          400: "#bcb195",
          500: "#8e8467",
        },
        // Ink — warm-black for body, with shaded variants
        ink: {
          DEFAULT: "#1a1814",
          50: "#5d574b",
          100: "#4a4438",
          200: "#3a342a",
          300: "#2a261e",
          400: "#1a1814",
          500: "#0f0d0a",
          // legacy aliases used in older components (kept so we don't break existing pages)
          700: "#3a342a",
          900: "#1a1814",
        },
        // Crimson — deep editorial accent, used sparingly
        crimson: {
          DEFAULT: "#7a1c20",
          50: "#a8201a",
          100: "#7a1c20",
          200: "#5a161a",
        },
        // Sage — muted teal for data
        sage: {
          DEFAULT: "#3a5a4c",
          50: "#7da595",
          100: "#5a8472",
          200: "#3a5a4c",
          300: "#243a31",
        },
        // Ochre — warm accent for highlights
        ochre: {
          DEFAULT: "#c8893d",
          50: "#dfac72",
          100: "#c8893d",
          200: "#9a682a",
        },
        // Sparing semantic chips
        signal: {
          urgent: "#7a1c20",
          warn: "#9a682a",
          ok: "#3a5a4c",
          info: "#2a3a52",
        },
      },
      letterSpacing: {
        widest: "0.22em",
        widearr: "0.32em",
      },
      maxWidth: {
        prose: "68ch",
        wide: "84ch",
      },
      boxShadow: {
        card: "0 1px 0 rgba(26,24,20,0.06), 0 6px 24px -16px rgba(26,24,20,0.18)",
      },
    },
  },
  plugins: [],
};
