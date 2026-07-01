/** @type {import("tailwindcss").Config} */
export default {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      fontFamily: {
        // ADB uses a system-ui body stack with "Ideal Sans" headings.
        // Source Sans 3 is the closest free humanist substitute; we pair it
        // with ADB's exact system-ui fallback so the render degrades the way
        // adb.org does.
        sans: [
          "var(--font-source-sans)",
          "system-ui",
          "-apple-system",
          '"Segoe UI"',
          "Roboto",
          '"Helvetica Neue"',
          "Arial",
          "sans-serif",
        ],
        // Display + serif keys repoint to the same sans so any legacy
        // `font-display` / `font-serif` usage stays on-brand (full ADB
        // corporate identity has no editorial serif).
        display: [
          "var(--font-source-sans)",
          "system-ui",
          "-apple-system",
          '"Segoe UI"',
          "Arial",
          "sans-serif",
        ],
        serif: [
          "var(--font-source-sans)",
          "system-ui",
          "-apple-system",
          '"Segoe UI"',
          "Arial",
          "sans-serif",
        ],
        // Mono: JetBrains Mono — data tables, code, and attestation stamps.
        mono: [
          "var(--font-jetbrains-mono)",
          "ui-monospace",
          "Menlo",
          "Consolas",
          "monospace",
        ],
      },
      colors: {
        // ----- ADB palette (ground-truthed from adb.org computed styles) -----
        // Surfaces — white page, light-grey sunk panels (no warm paper)
        paper: {
          DEFAULT: "#ffffff",
          50: "#ffffff",
          100: "#f8f9fa",
          200: "#f4f5f6",
          300: "#ebedef",
          400: "#d7dbdf",
          500: "#adb5bd",
        },
        // Ink — ADB near-black text + slate shades
        ink: {
          DEFAULT: "#212529",
          50: "#687582",
          100: "#464f58",
          200: "#343b41",
          300: "#2a2f34",
          400: "#212529",
          500: "#16191c",
          // legacy aliases used in older components
          700: "#343b41",
          900: "#212529",
        },
        // "crimson" key is the PRIMARY ACCENT slot — now ADB web blue #007DB8
        crimson: {
          DEFAULT: "#007db8",
          50: "#3aa0d0",
          100: "#007db8",
          200: "#005f8c",
        },
        // "sage" key is the POSITIVE/SECONDARY accent — now ADB green
        sage: {
          DEFAULT: "#5a8227",
          50: "#8aad5a",
          100: "#5a8227",
          200: "#3f5d1a",
          300: "#2c4112",
        },
        // "ochre" key is the WARM HIGHLIGHT — now ADB gold/amber
        ochre: {
          DEFAULT: "#b07d12",
          50: "#fdd886",
          100: "#fbb00e",
          200: "#9c6b02",
        },
        // ADB-named keys for new components
        navy: "#002569",
        sky: "#57caff",
        gold: "#fbb00e",
        slate: {
          DEFAULT: "#687582",
          700: "#464f58",
          900: "#343b41",
        },
        // Semantic chips, ADB-aligned
        signal: {
          urgent: "#d43f16",
          warn: "#9c6b02",
          ok: "#5a8227",
          info: "#007db8",
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
        card: "0 1px 2px rgba(33,37,41,0.06), 0 8px 24px -16px rgba(33,37,41,0.22)",
      },
    },
  },
  plugins: [],
};
