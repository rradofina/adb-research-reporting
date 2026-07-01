"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { supabaseGet, supabaseEnabled, type VulnerabilityRow } from "../lib/supabase";
import { Kicker } from "../components/ui";

/**
 * Live SQL view of the cross-program vulnerability matrix, fetched directly
 * from Supabase via the anon key. Demonstrates that the same data is now
 * queryable via REST/GraphQL/SQL outside the static-JSON path.
 *
 * If env is not configured, render an editorial "where to find the same data"
 * panel instead of a scary error — the static path is fully functional.
 */
export default function LiveData() {
  const [rows, setRows] = useState<VulnerabilityRow[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [region, setRegion] = useState<string>("ALL");

  useEffect(() => {
    if (!supabaseEnabled) return;
    const filter = region === "ALL" ? "" : `&subregion=eq.${encodeURIComponent(region)}`;
    supabaseGet<VulnerabilityRow>(
      "vulnerability_matrix",
      `select=iso3,country,subregion,air_obs,climate_health,disaster_evts_yr,food_price,grid_concentration,emigrant_stock,port_friction,remittance_fragility,school_heat,sp_readiness_gap,water_crop&order=iso3${filter}`,
    )
      .then(setRows)
      .catch((e) => setError(String(e)));
  }, [region]);

  const subregions = ["ALL", "South Asia", "Southeast Asia", "East Asia", "Central Asia", "Caucasus", "Pacific"];

  return (
    <div className="reveal">
      <Kicker>Live · queried from Supabase REST</Kicker>
      <h1 className="display-lg mt-3 text-[clamp(2rem,3.6vw,2.6rem)]">
        Live cross-program data.
      </h1>
      <p className="mt-4 lede max-w-3xl">
        This page queries Supabase directly via the public anon key. The static
        JSON pages still work the same way — this view is for when you need
        SQL filtering, sorting, or joins on the live database.
      </p>

      {!supabaseEnabled && <SupabaseOffline />}

      {error && (
        <div
          className="mt-8 px-5 py-4 text-sm"
          style={{
            background: "var(--paper-deep)",
            borderLeft: "3px solid var(--crimson)",
            color: "var(--ink-soft)",
            fontFamily: "JetBrains Mono, monospace",
          }}
        >
          <span className="kicker block mb-1" style={{ color: "var(--crimson)" }}>
            Supabase request failed
          </span>
          {error}
        </div>
      )}

      {supabaseEnabled && (
        <>
          <div className="mt-10 flex items-center gap-3 flex-wrap">
            <span className="kicker">Region filter</span>
            {subregions.map((r) => (
              <button
                key={r}
                onClick={() => setRegion(r)}
                className="chip"
                style={
                  region === r
                    ? { background: "var(--ink)", color: "var(--paper)", borderColor: "var(--ink)" }
                    : {}
                }
              >
                {r}
              </button>
            ))}
            <span className="ml-auto marginalia">
              Backed by <code>public.vulnerability_matrix</code> view in Supabase.
            </span>
          </div>

          {!rows && !error && (
            <div className="mt-12 text-ink-faint">Loading from Supabase…</div>
          )}

          {rows && (
            <div className="mt-8 overflow-x-auto" style={{ borderTop: "1.5px solid var(--ink)", borderBottom: "1.5px solid var(--ink)" }}>
              <table className="data-table tabular w-full">
                <thead>
                  <tr>
                    <th>ISO3</th>
                    <th>Country</th>
                    <th>Subregion</th>
                    <th className="text-right">P3 Air</th>
                    <th className="text-right">P5 Climate-Health</th>
                    <th className="text-right">P7 Disaster</th>
                    <th className="text-right">P9 Food</th>
                    <th className="text-right">P10 Grid</th>
                    <th className="text-right">P11 Emig.</th>
                    <th className="text-right">P12 Port</th>
                    <th className="text-right">P14 Remit</th>
                    <th className="text-right">P15 School</th>
                    <th className="text-right">P16 SP gap</th>
                    <th className="text-right">P17 Water</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r) => (
                    <tr key={r.iso3}>
                      <td className="font-mono text-xs">{r.iso3}</td>
                      <td>{r.country}</td>
                      <td className="text-xs text-ink-faint">{r.subregion ?? "—"}</td>
                      <td className="text-right">{fmt(r.air_obs)}</td>
                      <td className="text-right">{fmt(r.climate_health)}</td>
                      <td className="text-right">{fmt(r.disaster_evts_yr)}</td>
                      <td className="text-right">{fmt(r.food_price)}</td>
                      <td className="text-right">{fmt(r.grid_concentration, 3)}</td>
                      <td className="text-right">{r.emigrant_stock != null ? (r.emigrant_stock / 1e6).toFixed(1) + "M" : "—"}</td>
                      <td className="text-right">{fmt(r.port_friction)}</td>
                      <td className="text-right">{fmt(r.remittance_fragility)}</td>
                      <td className="text-right">{fmt(r.school_heat)}</td>
                      <td className="text-right">{fmt(r.sp_readiness_gap)}</td>
                      <td className="text-right">{fmt(r.water_crop)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      <section className="mt-14 px-6 py-6" style={{ background: "var(--paper-deep)" }}>
        <Kicker>Architecture note</Kicker>
        <p className="mt-3 text-ink-soft leading-relaxed max-w-prose">
          Per <code>CONSTITUTION.md</code> §11, the repository — scripts,
          committed cache, generated JSON, manifest — is the source of truth.
          Supabase is a downstream query layer: a read-only projection of the
          same generated artifacts, refreshed by{" "}
          <code>supabase/sync-to-supabase.py</code>. A clone of the repository
          remains byte-reproducible without Supabase access.
        </p>
      </section>
    </div>
  );
}

function SupabaseOffline() {
  return (
    <div
      className="mt-10 px-6 py-6"
      style={{
        background: "var(--paper-deep)",
        borderLeft: "3px solid var(--ochre)",
      }}
    >
      <Kicker variant="ochre">Supabase layer is offline · static path is fully functional</Kicker>
      <p className="mt-3 text-ink-soft leading-relaxed max-w-prose">
        The Supabase env vars are not set on this deployment, so the live SQL
        view is unavailable here. The live layer is{" "}
        <em>optional</em> — the same numbers are served from committed JSON
        without any database, exactly as Constitution §11 requires.
      </p>
      <ul className="mt-4 marginalia space-y-1.5">
        <li>
          → <Link href="/atlas" className="ed-link">DMC atlas</Link> — every
          country, all 14 indicators, rendered from <code>/public/data/*.json</code>
        </li>
        <li>
          → <Link href="/research" className="ed-link">Research programs</Link> —
          per-program panel data, sensitivity, and evidence packets
        </li>
        <li>
          → <Link href="/data" className="ed-link">Data catalog</Link> — every
          published JSON file with its source license and retrieval timestamp
        </li>
        <li>
          → <Link href="/findings" className="ed-link">Findings</Link> — the working-paper series
        </li>
      </ul>
      <p
        className="mt-4 text-xs"
        style={{ color: "var(--ink-faint)", fontFamily: "JetBrains Mono, monospace" }}
      >
        To enable this page on a deployment, set{" "}
        <code>NEXT_PUBLIC_SUPABASE_URL</code> and{" "}
        <code>NEXT_PUBLIC_SUPABASE_ANON_KEY</code>{" "}
        in the host's env config and redeploy. The anon key is public by
        design — read-only access is governed by Supabase RLS on the
        <code> public.vulnerability_matrix </code> view.
      </p>
    </div>
  );
}

function fmt(v: number | null | undefined, dp = 2) {
  if (v == null) return "—";
  return v.toFixed(dp);
}
