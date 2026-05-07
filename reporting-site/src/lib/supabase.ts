/**
 * Lightweight Supabase REST client for the reporting site.
 *
 * No npm dep — uses fetch + the project URL + anon key from import.meta.env.
 * Reads only public-schema views (read-only by construction).
 *
 * The website still reads /data/*.json by default (faster, no network round-trip,
 * works offline). Use this client when you need cross-program SQL joins or
 * dynamic filtering that's awkward in static JSON.
 */
const URL = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const ANON = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

export const supabaseEnabled = Boolean(URL && ANON);

export async function supabaseGet<T = unknown>(
  view: string,
  query: string = "select=*",
): Promise<T[]> {
  if (!supabaseEnabled) throw new Error("Supabase not configured");
  const r = await fetch(`${URL}/rest/v1/${view}?${query}`, {
    headers: {
      apikey: ANON!,
      Authorization: `Bearer ${ANON}`,
    },
  });
  if (!r.ok) {
    const body = await r.text();
    throw new Error(`Supabase ${r.status}: ${body.slice(0, 200)}`);
  }
  return r.json();
}

export interface VulnerabilityRow {
  iso3: string;
  country: string;
  subregion: string | null;
  air_obs: number | null;
  climate_health: number | null;
  disaster_evts_yr: number | null;
  food_price: number | null;
  grid_concentration: number | null;
  emigrant_stock: number | null;
  port_friction: number | null;
  remittance_fragility: number | null;
  school_heat: number | null;
  sp_readiness_gap: number | null;
  water_crop: number | null;
}
