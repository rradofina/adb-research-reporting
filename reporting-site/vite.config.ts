import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Port 5173 (Vite default; distinct from luminosity-gap on 3005).
// In production (Vercel), the dev server config is ignored — Vercel
// serves the built `dist/` as a static SPA.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: false },
  preview: { port: 5174, strictPort: false },
});
