"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface ShockCoverage {
  dmc_rows: number;
  rows_with_disaster_event_frequency: number;
  rows_with_sp_coverage: number;
  rows_with_account_ownership: number;
  rows_with_digital_payment_use: number;
  rows_with_government_payment_account_use: number;
  rows_with_active_account: number;
  rows_with_plot_value: number;
  rows_with_two_rail_proxy: number;
  rows_with_payment_use_proxy: number;
  rows_with_account_proxy_only: number;
  rows_with_payment_rail_missing: number;
  rows_with_exposure_missing: number;
  rows_with_findex2025_2024_candidate_row: number;
  rows_where_api_payment_lags_findex2025: number;
  rows_with_large_account_payment_gap: number;
  rows_with_exposure_and_large_account_gap: number;
  observability_tier_counts: Record<string, number>;
  payment_vintage_status_counts: Record<string, number>;
  findex2025_candidate_variable_counts: Record<string, number>;
}

interface PaymentIndicator {
  indicator_code: string;
  short: string;
  label: string;
  source: string;
  url: string;
  api_lastupdated: string;
  dmc_latest_value_count: number;
  latest_reference_years: number[];
  latest_reference_year?: number | null;
  latest_reference_age_years?: number | null;
  source_context?: string;
  retrieval_status?: string;
}

interface FindexInventory {
  source: string;
  download_page_url: string;
  country_csv_url: string;
  g2px_knowledge_url: string;
  retrieval_status: string;
  retrieval_error: string | null;
  http_last_modified: string | null;
  row_filter: string;
  dmc_2024_all_group_rows: number;
  candidate_variable_counts: Record<string, number>;
  use_rule: string;
}

interface ShockRow {
  iso3: string;
  country: string;
  events_per_year_2000_2025: number | null;
  total_events_2000_2025: number | null;
  total_affected_2000_2025: number | null;
  sp_coverage_pct: number | null;
  sp_coverage_year: number | null;
  account_ownership_pct: number | null;
  account_ownership_year: number | null;
  digital_payment_use_pct: number | null;
  digital_payment_use_year: number | null;
  government_payment_account_use_pct: number | null;
  government_payment_account_use_year: number | null;
  active_account_pct: number | null;
  active_account_year: number | null;
  poverty_headcount_215_pct: number | null;
  poverty_year: number | null;
  account_minus_digital_payment_pct: number | null;
  sp_minus_government_payment_account_pct: number | null;
  observability_tier: string;
  payment_vintage_status: string;
  digital_payment_source_context: string;
  digital_payment_age_years: number | null;
  account_to_digital_year_gap: number | null;
  account_gap_flag: string;
  sp_government_payment_gap_flag: string;
  has_findex2025_2024_candidate_row: boolean;
  findex2025_candidate_variable_count: number;
  evidence_flags: string;
  has_disaster_data: boolean;
  has_digital_payment_use: boolean;
  has_government_payment_account_use: boolean;
  has_plot_value: boolean;
}

interface ShockData {
  attestation_chain: string;
  status: string;
  decision: string;
  created_at: string;
  retrieval_started_at: string;
  coverage: ShockCoverage;
  inputs: {
    social_protection_panel: string;
    disaster_panel: string;
    world_bank_payment_indicators: PaymentIndicator[];
    findex_2025_country_level_inventory: FindexInventory;
  };
  source_sanity: {
    unit: string;
    payment_use_caveat: string;
    disaster_caveat: string;
    social_protection_caveat: string;
    use_limit: string;
    findex_2025_inventory_rule: string;
    observability_protocol: string;
  };
  rows: ShockRow[];
  triage_summaries: {
    highest_disaster_exposure_with_payment_use_top12: ShockRow[];
    largest_account_minus_digital_payment_gap_top12: ShockRow[];
    source_observability_watchlist_top12: ShockRow[];
  };
}

type GapMode = "account" | "government";

const GAP_OPTIONS: Array<{ id: GapMode; label: string }> = [
  { id: "account", label: "Account vs use" },
  { id: "government", label: "Program vs gov pay" },
];

function formatNumber(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function pct(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value.toFixed(digits)}%`;
}

function pp(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value.toFixed(digits)} pp`;
}

function yearList(years: number[]) {
  return years.slice().sort((a, b) => a - b).join(", ");
}

function tierLabel(tier: string | null | undefined) {
  if (!tier) return "Unclassified";
  const labels: Record<string, string> = {
    two_rail_proxy: "Two-rail proxy",
    payment_use_proxy: "Payment-use proxy",
    account_proxy_only: "Account proxy only",
    payment_rail_missing: "Payment rail missing",
    exposure_missing: "Exposure missing",
  };
  return labels[tier] || tier.replace(/_/g, " ");
}

function vintageLabel(status: string | null | undefined) {
  if (!status) return "Vintage not classified";
  const labels: Record<string, string> = {
    api_payment_use_lags_findex2025: "API lags Findex 2025",
    api_missing_findex2025_candidate: "API missing, Findex candidate",
    older_api_payment_use: "Older payment-use vintage",
    payment_use_missing: "Payment-use missing",
    api_payment_use_current_for_endpoint: "Current for API endpoint",
  };
  return labels[status] || status.replace(/_/g, " ");
}

function tierFill(tier: string | null | undefined) {
  const colors: Record<string, string> = {
    two_rail_proxy: "#007DB8",
    payment_use_proxy: "#FBB00E",
    account_proxy_only: "#8A4F7D",
    payment_rail_missing: "#9B2226",
    exposure_missing: "#d7dde3",
  };
  if (!tier) return "#d7dde3";
  return colors[tier] || "#d7dde3";
}

function gapValue(row: ShockRow, mode: GapMode) {
  return mode === "account"
    ? row.account_minus_digital_payment_pct
    : row.sp_minus_government_payment_account_pct;
}

export default function ShowcaseShockPayment() {
  const [data, setData] = useState<ShockData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/topic-sprints/generated/shock-payment-rails-sprint.json")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((payload: ShockData) => setData(payload))
      .catch((err) => setError(String(err)));
  }, []);

  const topExposure = data?.triage_summaries?.highest_disaster_exposure_with_payment_use_top12?.[0];
  const largestGap = data?.triage_summaries?.largest_account_minus_digital_payment_gap_top12?.[0];
  const paymentMetadata = data?.inputs?.world_bank_payment_indicators || [];
  const electronicPaymentMeta = paymentMetadata.find((item) => item.short === "digital_payment_use");
  const findexInventory = data?.inputs?.findex_2025_country_level_inventory;
  const findexCandidateCounts = findexInventory
    ? Object.values(findexInventory.candidate_variable_counts || {})
    : [];

  return (
    <article className="showcase-page">
      <header className="showcase-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            After the Shock, Can the Payment Rail Be Seen?
          </h1>
          <p className="showcase-lede">
            This sprint joins disaster exposure, social-protection coverage,
            account ownership, and payment-use indicators. The report asks a
            narrower question than readiness: which delivery-rail evidence can
            actually be seen, which source is only a proxy, and which newer
            source now needs a proper variable-map before the chart changes?
          </p>
          <div className="showcase-meta">
            <span>{data?.attestation_chain || "ai-first"}</span>
            <span>Program prospectus candidate</span>
            <span>No emergency-transfer claim</span>
          </div>
        </div>
        <div className="showcase-hero-panel shock-hero-panel" aria-label="Shock-payment evidence summary">
          {data ? (
            <>
              <ShockHeroRails data={data} />
              <div className="shock-hero-stats">
                <div>
                  <span className="showcase-stat-value">
                    {data.coverage.rows_with_two_rail_proxy ?? "pending"}
                  </span>
                  <span className="showcase-stat-label">rows with the strongest public proxy bundle</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {data.coverage.rows_with_payment_use_proxy ?? "pending"}
                  </span>
                  <span className="showcase-stat-label">rows with payment use but a missing program leg</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {data.coverage.rows_with_findex2025_2024_candidate_row ?? "pending"}
                  </span>
                  <span className="showcase-stat-label">DMC rows visible in the 2024 Findex candidate file</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {data.coverage.rows_where_api_payment_lags_findex2025 ?? "pending"}
                  </span>
                  <span className="showcase-stat-label">API payment-use rows lagging that source</span>
                </div>
              </div>
            </>
          ) : (
            <span className="showcase-loading">
              {error ? `Could not load sprint JSON: ${error}` : "Loading evidence packet..."}
            </span>
          )}
        </div>
      </header>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">The data gap</p>
          <h2>Account ownership is not the same as an observable payment rail.</h2>
          <p>
            A post-disaster transfer can be designed on paper while the public
            evidence on delivery channels remains thin. Account ownership,
            electronic payment use, government-payment account use, and social
            protection coverage are related concepts, but they are not
            interchangeable measures of whether emergency transfers can reach
            people after an event.
          </p>
        </div>
      </section>

      {data && <ShockRailsExplorer data={data} />}

      {data && findexInventory && (
        <section className="showcase-section showcase-two-col">
          <div>
            <p className="kicker">Source audit</p>
            <h2>The newer source is visible, but not silently swapped in.</h2>
            <p>
              The 2025 Findex country file adds a 2024 source path for account,
              payment, merchant, and G2P candidate variables. This page records
              that source as an audit finding, not a replacement value, until
              the variable glossary is mapped into the generator.
            </p>
          </div>
          <div className="showcase-fact-list">
            <div>
              <span>Findex 2025 inventory result</span>
              <strong>
                {findexInventory.dmc_2024_all_group_rows} DMC rows match 2024/all/all in the country CSV
              </strong>
            </div>
            <div>
              <span>Candidate variable coverage</span>
              <strong>
                {findexCandidateCounts.length
                  ? `${Math.min(...findexCandidateCounts)}-${Math.max(...findexCandidateCounts)} DMC rows across the tracked payment/G2P fields`
                  : "Candidate variable counts pending in this JSON cache"}
              </strong>
            </div>
            <div>
              <span>Current-use rule</span>
              <strong>{findexInventory.use_rule}</strong>
            </div>
          </div>
        </section>
      )}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The public sources separate exposure from delivery observability.</h2>
          <p>
            The sprint makes visible that disaster frequency, digital-payment
            use, social-protection coverage, and account ownership do not form
            one clean measure. That is the research hook: the next program
            should map the 2024 Findex candidate source, test source vintage,
            payment-channel definitions, and
            event-specific validation before any readiness language appears.
          </p>
        </div>
        <div className="showcase-fact-list">
          {topExposure && (
            <div>
              <span>Highest event-frequency row with payment-use data</span>
              <strong>
                {topExposure.country}: {formatNumber(topExposure.events_per_year_2000_2025, 2)}
                {" "}recorded disasters per year, {pct(topExposure.digital_payment_use_pct, 1)}
                {" "}electronic payment use
              </strong>
            </div>
          )}
          {largestGap && (
            <div>
              <span>Largest account-minus-payment-use gap in the sprint</span>
              <strong>
                {largestGap.country}: {pp(largestGap.account_minus_digital_payment_pct, 1)}
              </strong>
            </div>
          )}
          {electronicPaymentMeta && (
            <div>
              <span>Payment-use metadata vintage</span>
              <strong>
                {electronicPaymentMeta.indicator_code} API update {electronicPaymentMeta.api_lastupdated};
                {" "}reference years {yearList(electronicPaymentMeta.latest_reference_years)}
              </strong>
            </div>
          )}
          {(data?.coverage.rows_with_exposure_and_large_account_gap || 0) > 0 && (
            <div>
              <span>High-exposure rows with large account-use gap</span>
              <strong>{data?.coverage.rows_with_exposure_and_large_account_gap} rows trigger the stricter watch flag</strong>
            </div>
          )}
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What this does not mean</p>
          <h2>The report does not show whether emergency payments arrived.</h2>
          <p>
            Electronic payment use is not shock-payment receipt. Government
            payment account use is not an emergency-transfer channel measure.
            ASPIRE coverage pools different social-protection instruments and
            reporting years. EM-DAT affected totals are event records and can
            count the same person across multiple events.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Reproduce the sprint</p>
          <code>python research/topic-sprints/scripts/sprint-shock-payment-rails.py</code>
          <a href="/topic-sprints/generated/shock-payment-rails-sprint.json" download>
            Download sprint JSON
          </a>
          <a href="/topic-sprints/generated/shock-payment-rails-sprint.csv" download>
            Download sprint CSV
          </a>
          <a href="/topic-sprints/reports/shock-payment-rails-sprint.md" target="_blank" rel="noreferrer">
            Read sprint note
          </a>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={3} />

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">Operational use</p>
          <h2>The next data investment is validation, not a score.</h2>
          <p>
            An ADB social protection team, finance ministry, or DMC statistics
            office could use this screen to decide where payment-channel data
            need source notes, where account ownership is too broad a proxy,
            and which event case studies should be checked before a shock
            delivery claim is made.
          </p>
        </div>
        <div className="showcase-source-box">
          <Link href="/showcase">Market-climate prototype</Link>
          <Link href="/showcase/data-freshness">Data-freshness prototype</Link>
          <Link href="/factory">Factory rules</Link>
          <Link href="/status">Research status</Link>
        </div>
      </section>
    </article>
  );
}

function ShockHeroRails({ data }: { data: ShockData }) {
  const rows = data.rows
    .filter((row) => row.has_plot_value && (row.events_per_year_2000_2025 || 0) >= 3)
    .sort((a, b) => (b.account_minus_digital_payment_pct || 0) - (a.account_minus_digital_payment_pct || 0))
    .slice(0, 3);

  return (
    <div className="shock-hero-rails" aria-label="Account ownership compared with digital payment use">
      <p className="showcase-source-title">Where ownership exceeds use</p>
      {rows.map((row) => (
        <div className="shock-hero-row" key={row.iso3}>
          <div>
            <strong>{row.iso3}</strong>
            <span>{tierLabel(row.observability_tier)}</span>
          </div>
          <div className="shock-hero-bars" aria-label={`${row.country} account and digital payment use`}>
            <i
              className="shock-hero-account"
              style={{ width: `${Math.max(3, row.account_ownership_pct || 0)}%` }}
            />
            <i
              className="shock-hero-digital"
              style={{ width: `${Math.max(3, row.digital_payment_use_pct || 0)}%` }}
            />
          </div>
          <em>{formatNumber(row.events_per_year_2000_2025, 1)} events/yr</em>
        </div>
      ))}
      <div className="shock-hero-key">
        <span><i className="shock-hero-account" /> Account ownership</span>
        <span><i className="shock-hero-digital" /> Electronic payment use</span>
      </div>
    </div>
  );
}

function ShockRailsExplorer({ data }: { data: ShockData }) {
  const plotRows = useMemo(
    () => data.rows.filter((row) => row.has_plot_value && row.events_per_year_2000_2025 !== null && row.digital_payment_use_pct !== null),
    [data.rows],
  );
  const defaultIso =
    data.triage_summaries.largest_account_minus_digital_payment_gap_top12[0]?.iso3 ||
    plotRows[0]?.iso3 ||
    "";
  const [selectedIso, setSelectedIso] = useState(defaultIso);
  const [gapMode, setGapMode] = useState<GapMode>("account");

  const selectedRow =
    data.rows.find((row) => row.iso3 === selectedIso) ||
    data.triage_summaries.largest_account_minus_digital_payment_gap_top12[0] ||
    plotRows[0];
  const barRows = useMemo(() => {
    return data.rows
      .filter((row) => gapValue(row, gapMode) !== null && Number.isFinite(gapValue(row, gapMode)))
      .sort((a, b) => (gapValue(b, gapMode) || 0) - (gapValue(a, gapMode) || 0))
      .slice(0, 12);
  }, [data.rows, gapMode]);

  return (
    <section className="showcase-section showcase-explorer">
      <div className="showcase-explorer-head">
        <div>
          <p className="kicker">Interactive evidence view</p>
          <h2>Separate exposure, coverage, ownership, and use.</h2>
          <p>
            The scatter plots disaster-event frequency against electronic
            payment use. Bubble size reflects affected event records, and fill
            marks the source-observability tier. The bar panel shows concept
            gaps that should not be collapsed into an index.
          </p>
        </div>
        <div className="showcase-controls" aria-label="Shock-payment explorer controls">
          <div className="showcase-filter-buttons" role="group" aria-label="Select concept gap">
            {GAP_OPTIONS.map((option) => (
              <button
                key={option.id}
                type="button"
                className={gapMode === option.id ? "showcase-control-active" : ""}
                onClick={() => setGapMode(option.id)}
              >
                {option.label}
              </button>
            ))}
          </div>
          <label>
            <span>Focus economy</span>
            <select value={selectedIso} onChange={(event) => setSelectedIso(event.target.value)}>
              {plotRows
                .slice()
                .sort((a, b) => a.country.localeCompare(b.country))
                .map((row) => (
                  <option key={row.iso3} value={row.iso3}>
                    {row.country}
                  </option>
                ))}
            </select>
          </label>
        </div>
      </div>

      <div className="shock-visual-grid">
        <div className="shock-chart-wrap">
          <ShockScatter
            rows={plotRows}
            selectedIso={selectedRow?.iso3}
            onSelect={setSelectedIso}
          />
        </div>
        <div className="shock-chart-wrap">
          <ShockGapBars
            rows={barRows}
            mode={gapMode}
            selectedIso={selectedRow?.iso3}
            onSelect={setSelectedIso}
          />
        </div>
      </div>

      <div className="freshness-legend shock-legend" aria-label="Shock-payment legend">
        <span><i style={{ background: tierFill("two_rail_proxy") }} /> Two-rail proxy</span>
        <span><i style={{ background: tierFill("payment_use_proxy") }} /> Payment-use proxy</span>
        <span><i style={{ background: tierFill("payment_rail_missing") }} /> Rail missing</span>
        <span><i style={{ background: "#FBB00E" }} /> Selected economy</span>
      </div>

      <div className="showcase-month-readout">
        <div>
          <span>Selected economy</span>
          <strong>
            {selectedRow
              ? `${selectedRow.country}: ${formatNumber(selectedRow.events_per_year_2000_2025, 2)} recorded disasters per year`
              : "Select an economy"}
          </strong>
        </div>
        <div>
          <span>Account ownership versus electronic payment use</span>
          <strong>
            {selectedRow
              ? `${pct(selectedRow.account_ownership_pct, 1)} ownership; ${pct(selectedRow.digital_payment_use_pct, 1)} use; ${pp(selectedRow.account_minus_digital_payment_pct, 1)} gap`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Source-observability tier</span>
          <strong>
            {selectedRow
              ? `${tierLabel(selectedRow.observability_tier)}; ${vintageLabel(selectedRow.payment_vintage_status)}`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Social protection versus government-payment account use</span>
          <strong>
            {selectedRow
              ? `${pct(selectedRow.sp_coverage_pct, 1)} coverage; ${pct(selectedRow.government_payment_account_use_pct, 1)} gov-payment account use; ${pp(selectedRow.sp_minus_government_payment_account_pct, 1)} gap`
              : "missing"}
          </strong>
        </div>
      </div>
      <ShockObservabilityLedger data={data} onSelect={setSelectedIso} selectedIso={selectedRow?.iso3} />
    </section>
  );
}

type LedgerState = "on" | "warn" | "candidate" | "missing";

interface LedgerLeg {
  id: string;
  label: string;
  title: string;
  state: (row: ShockRow) => LedgerState;
}

const LEDGER_LEGS: LedgerLeg[] = [
  {
    id: "shock",
    label: "Shock",
    title: "EM-DAT disaster-frequency leg",
    state: (row) => (row.events_per_year_2000_2025 != null ? "on" : "missing"),
  },
  {
    id: "sp",
    label: "SP",
    title: "ASPIRE social-protection coverage leg",
    state: (row) => (row.sp_coverage_pct != null ? "on" : "missing"),
  },
  {
    id: "account",
    label: "Acct",
    title: "Account-ownership leg",
    state: (row) => {
      if (row.account_ownership_pct == null) return "missing";
      return (row.account_to_digital_year_gap || 0) >= 3 ? "warn" : "on";
    },
  },
  {
    id: "use",
    label: "Use",
    title: "Electronic-payment-use leg",
    state: (row) => {
      if (row.digital_payment_use_pct == null) return "missing";
      const status = row.payment_vintage_status || "";
      return status.includes("lags") || status.includes("older")
        ? "warn"
        : "on";
    },
  },
  {
    id: "gov",
    label: "Gov pay",
    title: "Government-payment account-use leg",
    state: (row) => (row.government_payment_account_use_pct != null ? "on" : "missing"),
  },
  {
    id: "findex",
    label: "2024",
    title: "Findex 2025 country file has a 2024 all/all candidate row",
    state: (row) => (row.has_findex2025_2024_candidate_row ? "candidate" : "missing"),
  },
];

function legClass(state: LedgerState) {
  return `shock-leg shock-leg-${state}`;
}

function legStyle(state: LedgerState) {
  if (state === "on") {
    return { background: "#007DB8", borderColor: "#007DB8", color: "#ffffff" };
  }
  if (state === "warn") {
    return { background: "#FBB00E", borderColor: "#d89a00", color: "#2b2408" };
  }
  if (state === "candidate") {
    return { background: "#5A8227", borderColor: "#5A8227", color: "#ffffff" };
  }
  return { background: "#e8edf2", borderColor: "#d7dde3", color: "#5d6874" };
}

function legTitle(row: ShockRow, leg: LedgerLeg) {
  const state = leg.state(row);
  if (leg.id === "use") {
    return `${row.country}: ${leg.title}; ${pct(row.digital_payment_use_pct, 1)}; ${vintageLabel(row.payment_vintage_status)}`;
  }
  if (leg.id === "account") {
    return `${row.country}: ${leg.title}; ${pct(row.account_ownership_pct, 1)}; account-to-use vintage gap ${formatNumber(row.account_to_digital_year_gap, 0)} years`;
  }
  if (leg.id === "findex") {
    return `${row.country}: ${state === "candidate" ? row.findex2025_candidate_variable_count || 0 : 0} tracked candidate variables present`;
  }
  return `${row.country}: ${leg.title}; ${state}`;
}

function ShockObservabilityLedger({
  data,
  selectedIso,
  onSelect,
}: {
  data: ShockData;
  selectedIso?: string;
  onSelect: (iso3: string) => void;
}) {
  const watchRows = data.triage_summaries.source_observability_watchlist_top12 || [];
  const rows = watchRows.length
    ? watchRows
    : data.rows
        .slice()
        .sort((a, b) => (b.events_per_year_2000_2025 || 0) - (a.events_per_year_2000_2025 || 0))
        .slice(0, 12);

  return (
    <div className="shock-ledger-wrap">
      <div className="shock-ledger-head">
        <div>
          <p className="kicker">Source observability ledger</p>
          <h3>Top exposed rows, checked leg by leg.</h3>
        </div>
        <p>
          Yellow means the leg exists but carries a vintage or source-mapping
          warning. Green is the 2024 Findex candidate source, not a replacement
          value.
        </p>
      </div>
      <div className="shock-ledger-scroll">
        <div className="shock-ledger-grid" role="table" aria-label="Shock-payment evidence legs by economy">
          <div className="shock-ledger-row shock-ledger-row-head" role="row">
            <span>Economy</span>
            {LEDGER_LEGS.map((leg) => (
              <span key={leg.id} title={leg.title}>{leg.label}</span>
            ))}
            <span>Tier</span>
          </div>
          {rows.map((row) => (
            <button
              key={row.iso3}
              type="button"
              className={row.iso3 === selectedIso ? "shock-ledger-row shock-ledger-selected" : "shock-ledger-row"}
              onClick={() => onSelect(row.iso3)}
              role="row"
            >
              <span className="shock-ledger-country">
                <strong>{row.iso3}</strong>
                <em>{row.country}</em>
              </span>
              {LEDGER_LEGS.map((leg) => {
                const state = leg.state(row);
                return (
                  <span
                    key={leg.id}
                    className={legClass(state)}
                    style={legStyle(state)}
                    title={legTitle(row, leg)}
                  >
                    {state === "missing" ? "MISS" : state === "candidate" ? "CAND" : state === "warn" ? "WARN" : "OK"}
                  </span>
                );
              })}
              <span className="shock-ledger-tier" style={{ borderColor: tierFill(row.observability_tier) }}>
                {tierLabel(row.observability_tier)}
              </span>
            </button>
          ))}
        </div>
      </div>
      <div className="freshness-legend shock-legend" aria-label="Shock-payment ledger legend">
        <span><i style={{ background: "#007DB8" }} /> Evidence leg present</span>
        <span><i style={{ background: "#FBB00E" }} /> Vintage or mapping warning</span>
        <span><i style={{ background: "#5A8227" }} /> Findex 2024 candidate</span>
        <span><i style={{ background: "#e8edf2" }} /> Missing public leg</span>
      </div>
    </div>
  );
}

function ShockScatter({
  rows,
  selectedIso,
  onSelect,
}: {
  rows: ShockRow[];
  selectedIso?: string;
  onSelect: (iso3: string) => void;
}) {
  const width = 690;
  const height = 430;
  const margin = { top: 34, right: 28, bottom: 58, left: 62 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const maxEvents = Math.max(1, ...rows.map((row) => row.events_per_year_2000_2025 || 0));
  const maxAffected = Math.max(1, ...rows.map((row) => row.total_affected_2000_2025 || 0));
  const x = (value: number | null) => margin.left + ((value || 0) / maxEvents) * plotWidth;
  const y = (value: number | null) => margin.top + (1 - (value || 0) / 100) * plotHeight;
  const r = (value: number | null) => 4 + (Math.log10((value || 0) + 1) / Math.log10(maxAffected + 1)) * 16;
  const labelRows = new Set(
    rows
      .slice()
      .sort((a, b) => (b.events_per_year_2000_2025 || 0) - (a.events_per_year_2000_2025 || 0))
      .slice(0, 6)
      .map((row) => row.iso3),
  );
  if (selectedIso) labelRows.add(selectedIso);

  return (
    <svg
      className="shock-scatter"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Disaster event frequency by electronic payment use"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Disaster frequency and electronic payment use
      </text>
      <line x1={margin.left} y1={margin.top} x2={margin.left} y2={margin.top + plotHeight} className="shock-axis" />
      <line x1={margin.left} y1={margin.top + plotHeight} x2={margin.left + plotWidth} y2={margin.top + plotHeight} className="shock-axis" />
      {[0, 25, 50, 75, 100].map((tick) => (
        <g key={tick}>
          <line x1={margin.left} x2={margin.left + plotWidth} y1={y(tick)} y2={y(tick)} className="shock-grid" />
          <text x={margin.left - 10} y={y(tick) + 4} textAnchor="end" className="showcase-heatmap-year">
            {tick}%
          </text>
        </g>
      ))}
      {[0, 5, 10, 15, 20, 25].map((tick) => (
        <g key={tick}>
          <line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={margin.top + plotHeight} className="shock-grid" />
          <text x={x(tick)} y={margin.top + plotHeight + 19} textAnchor="middle" className="showcase-heatmap-year">
            {tick}
          </text>
        </g>
      ))}
      <text x={margin.left + plotWidth / 2} y={height - 12} textAnchor="middle" className="shock-axis-label">
        Recorded disasters per year, 2000-2025
      </text>
      <text x={16} y={margin.top + plotHeight / 2} textAnchor="middle" className="shock-axis-label" transform={`rotate(-90 16 ${margin.top + plotHeight / 2})`}>
        Electronic payment use (% age 15+)
      </text>
      {rows.map((row) => {
        const selected = row.iso3 === selectedIso;
        return (
          <g key={row.iso3}>
            <circle
              cx={x(row.events_per_year_2000_2025)}
              cy={y(row.digital_payment_use_pct)}
              r={r(row.total_affected_2000_2025)}
              fill={tierFill(row.observability_tier)}
              stroke={selected ? "#FBB00E" : "#ffffff"}
              strokeWidth={selected ? 3 : 1.3}
              className="shock-point"
              onMouseEnter={() => onSelect(row.iso3)}
              onClick={() => onSelect(row.iso3)}
            >
              <title>
                {`${row.country}: ${formatNumber(row.events_per_year_2000_2025, 2)} events/year, ${pct(row.digital_payment_use_pct, 1)} payment use, ${tierLabel(row.observability_tier)}, ${vintageLabel(row.payment_vintage_status)}, ${pct(row.sp_coverage_pct, 1)} ASPIRE coverage`}
              </title>
            </circle>
            {labelRows.has(row.iso3) && (
              <text
                x={x(row.events_per_year_2000_2025) + r(row.total_affected_2000_2025) + 4}
                y={y(row.digital_payment_use_pct) + 3}
                className={selected ? "shock-label shock-label-selected" : "shock-label"}
              >
                {row.iso3}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

function ShockGapBars({
  rows,
  mode,
  selectedIso,
  onSelect,
}: {
  rows: ShockRow[];
  mode: GapMode;
  selectedIso?: string;
  onSelect: (iso3: string) => void;
}) {
  const width = 470;
  const rowHeight = 25;
  const margin = { top: 44, right: 38, bottom: 24, left: 100 };
  const height = margin.top + rows.length * rowHeight + margin.bottom;
  const plotWidth = width - margin.left - margin.right;
  const maxGap = Math.max(1, ...rows.map((row) => gapValue(row, mode) || 0));
  const title =
    mode === "account"
      ? "Account ownership minus electronic payment use"
      : "ASPIRE coverage minus government-payment account use";

  return (
    <svg
      className="shock-gap-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label={title}
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        {title}
      </text>
      <text x={0} y={34} className="showcase-heatmap-year">
        Percentage-point gap; diagnostic only
      </text>
      {rows.map((row, index) => {
        const value = gapValue(row, mode) || 0;
        const y = margin.top + index * rowHeight;
        const selected = row.iso3 === selectedIso;
        return (
          <g key={row.iso3}>
            <text x={0} y={y + 14} className="showcase-heatmap-label">
              {row.iso3} {row.country}
            </text>
            <rect
              x={margin.left}
              y={y}
              width={plotWidth}
              height={17}
              fill="#eef2f5"
            />
            <rect
              x={margin.left}
              y={y}
              width={(value / maxGap) * plotWidth}
              height={17}
              fill={selected ? "#FBB00E" : mode === "account" ? "#007DB8" : "#5A8227"}
              className="shock-gap-bar"
              onMouseEnter={() => onSelect(row.iso3)}
              onClick={() => onSelect(row.iso3)}
            >
              <title>{`${row.country}: ${pp(value, 1)}`}</title>
            </rect>
            <text x={margin.left + plotWidth + 8} y={y + 14} className="shock-gap-value">
              {value.toFixed(0)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
