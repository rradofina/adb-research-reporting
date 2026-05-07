"""One-way sync: <program>/generated/*.json -> Supabase Postgres.

Per CONSTITUTION.md §11, the repo + cache + generated/ are the source of
truth. This script projects them into a queryable Postgres copy.

Idempotent: TRUNCATE + INSERT per table. Safe to re-run.

Run:
    python supabase/sync-to-supabase.py
"""
import json, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

import psycopg2
from psycopg2.extras import execute_batch, Json

ROOT = Path(__file__).resolve().parent.parent

# Load env
for line in (ROOT / ".env.local").read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()


def conn():
    c = psycopg2.connect(
        host=os.environ["SUPABASE_DB_HOST"],
        port=int(os.environ["SUPABASE_DB_PORT"]),
        dbname=os.environ["SUPABASE_DB_NAME"],
        user=os.environ["SUPABASE_DB_USER"],
        password=os.environ["SUPABASE_DB_PASSWORD"],
        sslmode="require",
    )
    c.autocommit = False
    return c


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def log_sync(cur, table, rows, artifact_path):
    cur.execute(
        """INSERT INTO research_meta.sync_log (table_name, rows_loaded, source_artifact, artifact_sha256)
           VALUES (%s, %s, %s, %s)""",
        (table, rows, str(artifact_path.relative_to(ROOT)), sha256(artifact_path)),
    )


def truncate_and_insert(cur, table, columns, rows):
    if not rows:
        return 0
    cur.execute(f"TRUNCATE {table} CASCADE")
    placeholders = ",".join(["%s"] * len(columns))
    cols_sql = ",".join(columns)
    sql = f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders})"
    execute_batch(cur, sql, rows, page_size=500)
    return len(rows)


# ===================================================================
# DMC dimension (hand-authored, must precede other tables with FK)
# ===================================================================

ADB_DMCS = [
    # iso3, iso2, name, subregion, pacific, ca, cau, sa, sea, ea, landlocked
    ("AFG","AF","Afghanistan","South Asia",False,False,False,True,False,False,True),
    ("ARM","AM","Armenia","Caucasus",False,False,True,False,False,False,True),
    ("AZE","AZ","Azerbaijan","Caucasus",False,False,True,False,False,False,True),
    ("BGD","BD","Bangladesh","South Asia",False,False,False,True,False,False,False),
    ("BTN","BT","Bhutan","South Asia",False,False,False,True,False,False,True),
    ("BRN","BN","Brunei Darussalam","Southeast Asia",False,False,False,False,True,False,False),
    ("KHM","KH","Cambodia","Southeast Asia",False,False,False,False,True,False,False),
    ("CHN","CN","China","East Asia",False,False,False,False,False,True,False),
    ("COK","CK","Cook Islands","Pacific",True,False,False,False,False,False,False),
    ("FJI","FJ","Fiji","Pacific",True,False,False,False,False,False,False),
    ("GEO","GE","Georgia","Caucasus",False,False,True,False,False,False,False),
    ("HKG","HK","Hong Kong, China","East Asia",False,False,False,False,False,True,False),
    ("IND","IN","India","South Asia",False,False,False,True,False,False,False),
    ("IDN","ID","Indonesia","Southeast Asia",False,False,False,False,True,False,False),
    ("KAZ","KZ","Kazakhstan","Central Asia",False,True,False,False,False,False,True),
    ("KIR","KI","Kiribati","Pacific",True,False,False,False,False,False,False),
    ("KGZ","KG","Kyrgyz Republic","Central Asia",False,True,False,False,False,False,True),
    ("LAO","LA","Lao PDR","Southeast Asia",False,False,False,False,True,False,True),
    ("MYS","MY","Malaysia","Southeast Asia",False,False,False,False,True,False,False),
    ("MDV","MV","Maldives","South Asia",False,False,False,True,False,False,False),
    ("MHL","MH","Marshall Islands","Pacific",True,False,False,False,False,False,False),
    ("FSM","FM","Micronesia, Fed. Sts.","Pacific",True,False,False,False,False,False,False),
    ("MNG","MN","Mongolia","East Asia",False,False,False,False,False,True,True),
    ("MMR","MM","Myanmar","Southeast Asia",False,False,False,False,True,False,False),
    ("NRU","NR","Nauru","Pacific",True,False,False,False,False,False,False),
    ("NPL","NP","Nepal","South Asia",False,False,False,True,False,False,True),
    ("NIU","NU","Niue","Pacific",True,False,False,False,False,False,False),
    ("PAK","PK","Pakistan","South Asia",False,False,False,True,False,False,False),
    ("PLW","PW","Palau","Pacific",True,False,False,False,False,False,False),
    ("PNG","PG","Papua New Guinea","Pacific",True,False,False,False,False,False,False),
    ("PHL","PH","Philippines","Southeast Asia",False,False,False,False,True,False,False),
    ("WSM","WS","Samoa","Pacific",True,False,False,False,False,False,False),
    ("SLB","SB","Solomon Islands","Pacific",True,False,False,False,False,False,False),
    ("LKA","LK","Sri Lanka","South Asia",False,False,False,True,False,False,False),
    ("TJK","TJ","Tajikistan","Central Asia",False,True,False,False,False,False,True),
    ("THA","TH","Thailand","Southeast Asia",False,False,False,False,True,False,False),
    ("TLS","TL","Timor-Leste","Southeast Asia",False,False,False,False,True,False,False),
    ("TON","TO","Tonga","Pacific",True,False,False,False,False,False,False),
    ("TKM","TM","Turkmenistan","Central Asia",False,True,False,False,False,False,True),
    ("TUV","TV","Tuvalu","Pacific",True,False,False,False,False,False,False),
    ("UZB","UZ","Uzbekistan","Central Asia",False,True,False,False,False,False,True),
    ("VUT","VU","Vanuatu","Pacific",True,False,False,False,False,False,False),
    ("VNM","VN","Viet Nam","Southeast Asia",False,False,False,False,True,False,False),
    ("TWN","TW","Taiwan","East Asia",False,False,False,False,False,True,False),
    ("TPE","TW","Taipei,China","East Asia",False,False,False,False,False,True,False),
]


def load_dim_dmc(cur):
    cols = ["iso3","iso2","name","subregion","is_pacific","is_central_asia","is_caucasus","is_south_asia","is_southeast_asia","is_east_asia","is_landlocked"]
    return truncate_and_insert(cur, "research.dim_dmc", cols, ADB_DMCS)


# ===================================================================
# Per-program loaders (each: read JSON in repo, project to table cols)
# ===================================================================

def load_air_monitoring(cur):
    p = ROOT / "luminosity-gap/public/data/air-monitoring-openaq-pilots.json"
    if not p.exists():
        return 0, p
    d = json.loads(p.read_text(encoding="utf-8"))
    # luminosity-gap uses camelCase + nested PM2.5 fields under `countries`
    rows_in = d.get("countries") or d.get("economies") or d.get("rows") or []
    rows = []
    for r in rows_in:
        pm25 = r.get("pm25") or {}
        who = r.get("whoCityPm25") or {}
        # Coerce nested dicts/lists to scalar values where the schema expects scalars
        def _scalar(v):
            return None if isinstance(v, (dict, list)) else v
        highest = who.get("highestCity")
        if isinstance(highest, dict):
            highest = f"{highest.get('city','?')} ({highest.get('valueUgM3','?')} µg/m³)"
        rows.append((
            r.get("iso3"), _scalar(r.get("population")), _scalar(r.get("publicLocations")),
            _scalar(pm25.get("locationsReporting") or r.get("pm25Locations")),
            _scalar(pm25.get("wdiAnnualUgM3") or r.get("pm25_exposure_ugm3")),
            _scalar(pm25.get("aboveWhoGuideline") or r.get("pm25_above_who_guideline_5_ugm3")),
            _scalar(pm25.get("observabilityGapScore") or r.get("pm25_observability_gap_score")),
            _scalar(pm25.get("observabilityStatus") or r.get("pm25_observability_status")),
            _scalar(who.get("meanLatestUgM3")),
            highest,
            datetime.now(timezone.utc),
        ))
    cols = ["iso3","population","public_locations","pm25_locations","pm25_exposure_ugm3","pm25_above_who_guideline_5_ugm3","pm25_observability_gap_score","pm25_observability_status","who_city_pm25_mean","who_highest_pm25_city","retrieved_at"]
    # Filter to known DMCs (skip ADB regional non-DMCs like AUS, NZL, JPN, KOR, SGP)
    valid_iso3 = {d[0] for d in ADB_DMCS}
    rows = [r for r in rows if r[0] in valid_iso3]
    return truncate_and_insert(cur, "research.air_monitoring_dmc", cols, rows), p


def load_access_services(cur):
    import csv
    p = ROOT / "luminosity-gap/research/access-services/generated/access-services-computed-admin1.csv"
    if not p.exists():
        return 0, p
    rows = []
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((
                r["iso3"], r["admin1_code"], r["admin1_name"],
                int(r["population"]) if r.get("population") else None,
                int(r["health_facilities"]) if r.get("health_facilities") else None,
                int(r["schools"]) if r.get("schools") else None,
                int(r["markets"]) if r.get("markets") else None,
                int(r["total_services"]) if r.get("total_services") else None,
                float(r["service_load_score"]) if r.get("service_load_score") else None,
                float(r["osm_completeness_risk_score"]) if r.get("osm_completeness_risk_score") else None,
                float(r["access_stress_index"]) if r.get("access_stress_index") else None,
                r.get("bottleneck"), r.get("service_query_mode"), r.get("osm_timestamp"),
            ))
    cols = ["iso3","admin1_code","admin1_name","population","health_facilities","schools","markets","total_services","service_load_score","osm_completeness_risk_score","access_stress_index","bottleneck","service_query_mode","osm_timestamp"]
    return truncate_and_insert(cur, "research.access_services_admin1", cols, rows), p


def load_simple_panel(cur, json_path, table, col_map):
    """Generic loader for a per-DMC panel: rows is a list of dicts, col_map = {"db_col": "json_field"}."""
    p = ROOT / json_path
    if not p.exists():
        return 0, p
    d = json.loads(p.read_text(encoding="utf-8"))
    rows_in = d.get("rows") or d.get("data") or []
    cols = list(col_map.keys())
    rows = []
    for r in rows_in:
        rows.append(tuple(
            Json(r.get(col_map[c])) if isinstance(r.get(col_map[c]), (dict, list))
            else r.get(col_map[c])
            for c in cols
        ))
    return truncate_and_insert(cur, table, cols, rows), p


def load_psdq(cur):
    n = 0
    last = None
    for iso, fname in [("PHL","public-service-data-quality-PHL.json"), ("BGD","public-service-data-quality-BGD.json")]:
        p = ROOT / "public-service-data-quality" / "generated" / fname
        if not p.exists():
            continue
        last = p
        d = json.loads(p.read_text(encoding="utf-8"))
        rows_in = d.get("rows", [])
        cols = ["iso3","admin1_code","admin1_name","population_2020","osm_health","registry_principal","registry_clinical","registry_all","ratio_osm_to_principal","ratio_osm_to_clinical","ratio_osm_to_all","osm_per_100k","registry_principal_per_100k","registry_clinical_per_100k","osm_timestamp","registry_retrieved_at","registry_source_url"]
        rows = []
        for r in rows_in:
            rows.append(tuple(r.get(c) for c in cols))
        if rows:
            cur.execute(f"DELETE FROM research.psdq_admin1 WHERE iso3 = %s", (iso,))
            placeholders = ",".join(["%s"] * len(cols))
            cols_sql = ",".join(cols)
            execute_batch(cur, f"INSERT INTO research.psdq_admin1 ({cols_sql}) VALUES ({placeholders})", rows, page_size=500)
            n += len(rows)
    return n, last


def load_remittance(cur):
    p = ROOT / "remittance-resilience/generated/remittance-resilience-adb-panel.json"
    if not p.exists():
        return (0, 0), p
    d = json.loads(p.read_text(encoding="utf-8"))
    # main panel
    cols = ["iso3","wdi_remittance_pct_gdp","wdi_year","rpw_period","rpw_corridors_observed","rpw_firms_observed","rpw_mean_cost_pct","rpw_median_cost_pct","rpw_min_cost_pct","rpw_max_cost_pct","fragility_index"]
    rows = [tuple(r.get(c) for c in cols) for r in d.get("rows", [])]
    n_dmc = truncate_and_insert(cur, "research.remittance_dmc", cols, rows)
    # corridors
    cor_cols = ["source_iso3","source","dest_iso3","dest","n_quotes","mean_cost_pct","median_cost_pct","min_cost_pct","max_cost_pct"]
    cor_rows = [tuple(r.get(c) for c in cor_cols) for r in d.get("expensive_corridors_top50", [])]
    n_cor = truncate_and_insert(cur, "research.remittance_corridor", cor_cols, cor_rows)
    return (n_dmc, n_cor), p


def load_dim_program(cur):
    cur.execute("TRUNCATE research.dim_program")
    rows = [
        (0,"mpi-nighttime-lights","MPI × nighttime lights","H",None,False),
        (1,"access-services","Climate-adjusted access to services","SR","104 ADM1 across 8 DMCs",True),
        (2,"digital-performance","Measured digital development gap","PP","Ookla manifest + DuckDB scaffold",False),
        (3,"air-monitoring","Air pollution without air monitors","SR","50 ADB regional economies",True),
        (4,"invisible-urbanization","Invisible urbanization","H",None,False),
        (5,"climate-health-workdays","Climate-health workday loss","H","outdoor labor × PM2.5",True),
        (6,"coastal-informal-risk","Coastal informal settlement risk","H",None,False),
        (7,"disaster-recovery-lag","Disaster recovery lag","H","EM-DAT 2000-2025 burden",True),
        (8,"flood-market-access","Flood market access","H",None,False),
        (9,"food-price-climate-transmission","Food-price climate transmission","H","WDI macro composite",True),
        (10,"grid-reliability-heat","Grid reliability under heat","H","WRI GPP fuel concentration",True),
        (11,"migration-displacement-signals","Migration & displacement","H","UN DESA 2024 bilateral",True),
        (12,"port-hinterland-friction","Port-hinterland trade friction","H","WB LPI × imports",True),
        (13,"public-service-data-quality","Public service data quality","H","OSM vs DOH NHFR + DGHS — multi-DMC",True),
        (14,"remittance-resilience","Remittance resilience","H","RPW Q1 2025 × WDI",True),
        (15,"school-heat-disruption","School heat disruption","H","CCKP × WDI",True),
        (16,"social-protection-shock-coverage","Social protection","H","ASPIRE × Findex × poverty",True),
        (17,"water-stress-crop-diversification","Water stress × crop","H","WDI water-crop composite",True),
    ]
    cols = ["id","slug","title","status","summary","has_artifact"]
    return truncate_and_insert(cur, "research.dim_program", cols, rows)


# ===================================================================
# Main
# ===================================================================

def main():
    c = conn()
    try:
        cur = c.cursor()

        n = load_dim_dmc(cur); print(f"  dim_dmc: {n}")
        n = load_dim_program(cur); print(f"  dim_program: {n}")

        n, p = load_air_monitoring(cur)
        print(f"  air_monitoring_dmc: {n}")
        if n: log_sync(cur, "research.air_monitoring_dmc", n, p)

        n, p = load_access_services(cur)
        print(f"  access_services_admin1: {n}")
        if n: log_sync(cur, "research.access_services_admin1", n, p)

        n, p = load_simple_panel(cur, "climate-health-workdays/generated/climate-health-workdays-adb-panel.json", "research.climate_health_dmc",
            {"iso3":"iso3","emp_agri_pct":"emp_agri_pct","emp_industry_pct":"emp_industry_pct","outdoor_labor_share_pct":"outdoor_labor_share_pct","pm25_exposure_ugm3":"pm25_exposure_ugm3","pm25_year":"pm25_year","urban_pop_pct":"urban_pop_pct","population_total":"population_total","exposed_outdoor_millions":"exposed_outdoor_millions","workday_loss_pressure_index":"workday_loss_pressure_index"})
        print(f"  climate_health_dmc: {n}")
        if n: log_sync(cur, "research.climate_health_dmc", n, p)

        n, p = load_simple_panel(cur, "disaster-recovery-lag/generated/disaster-recovery-lag-adb-panel.json", "research.disaster_burden_dmc",
            {"iso3":"iso3","total_events_2000_2025":"total_events_2000_2025","total_affected":"total_affected","total_deaths":"total_deaths","total_damage_usd_adj":"total_damage_usd_adj","events_per_year":"events_per_year","type_distribution":"type_distribution","biggest_event":"biggest_event","years_covered":"years_covered"})
        print(f"  disaster_burden_dmc: {n}")
        if n: log_sync(cur, "research.disaster_burden_dmc", n, p)

        n, p = load_simple_panel(cur, "food-price-climate-transmission/generated/food-price-adb-panel.json", "research.food_price_dmc",
            {"iso3":"iso3","cpi_inflation_pct":"cpi_inflation_pct","cpi_year":"cpi_year","ag_imports_pct_merch":"ag_imports_pct_merch","food_production_index":"food_production_index","food_price_vulnerability":"food_price_vulnerability"})
        print(f"  food_price_dmc: {n}")
        if n: log_sync(cur, "research.food_price_dmc", n, p)

        n, p = load_simple_panel(cur, "grid-reliability-heat/generated/grid-reliability-heat-adb-panel.json", "research.grid_dmc",
            {"iso3":"iso3","plant_count":"plant_count","total_capacity_mw":"total_capacity_mw","top_fuel":"top_fuel","top_fuel_share":"top_fuel_share","fuel_herfindahl":"fuel_herfindahl","wdi_elec_access_pct":"wdi_elec_access_pct","wdi_elec_access_year":"wdi_elec_access_year","wdi_energy_use_kgoe_per_capita":"wdi_energy_use_kgoe_per_capita","fuel_mix_capacity_mw":"fuel_mix_capacity_mw"})
        print(f"  grid_dmc: {n}")
        if n: log_sync(cur, "research.grid_dmc", n, p)

        n, p = load_simple_panel(cur, "migration-displacement-signals/generated/migration-displacement-adb-panel.json", "research.migration_dmc",
            {"iso3":"iso3","immigrant_stock_2024":"immigrant_stock_2024","emigrant_stock_2024":"emigrant_stock_2024","net_migrant_stock_2024":"net_migrant_stock_2024","top_origins":"top_origins","top_destinations":"top_destinations"})
        print(f"  migration_dmc: {n}")
        if n: log_sync(cur, "research.migration_dmc", n, p)

        n, p = load_simple_panel(cur, "port-hinterland-friction/generated/port-hinterland-friction-adb-panel.json", "research.port_friction_dmc",
            {"iso3":"iso3","lpi_overall":"lpi_overall","lpi_overall_year":"lpi_overall_year","lpi_infrastructure":"lpi_infrastructure","lpi_customs":"lpi_customs","imports_usd":"imports_usd","imports_usd_year":"imports_usd_year","friction_exposure_index":"friction_exposure_index"})
        print(f"  port_friction_dmc: {n}")
        if n: log_sync(cur, "research.port_friction_dmc", n, p)

        (nd, nc), p = load_remittance(cur)
        print(f"  remittance_dmc: {nd}, remittance_corridor: {nc}")
        if nd: log_sync(cur, "research.remittance_dmc", nd, p)
        if nc: log_sync(cur, "research.remittance_corridor", nc, p)

        n, p = load_simple_panel(cur, "school-heat-disruption/generated/school-heat-adb-panel.json", "research.school_heat_dmc",
            {"iso3":"iso3","primary_pupil_teacher_ratio":"primary_pupil_teacher_ratio","ptr_year":"ptr_year","pop_0_14_pct":"pop_0_14_pct","pop_total":"pop_total","children_0_14_millions":"children_0_14_millions","annual_tasmax_1995_2014_celsius":"annual_tasmax_1995_2014_celsius","school_heat_pressure_index":"school_heat_pressure_index"})
        print(f"  school_heat_dmc: {n}")
        if n: log_sync(cur, "research.school_heat_dmc", n, p)

        n, p = load_simple_panel(cur, "social-protection-shock-coverage/generated/social-protection-adb-panel.json", "research.social_protection_dmc",
            {"iso3":"iso3","sp_coverage_pct":"sp_coverage_pct","sp_coverage_year":"sp_coverage_year","findex_account_pct":"findex_account_pct","findex_year":"findex_year","poverty_headcount_215_pct":"poverty_headcount_215_pct","poverty_year":"poverty_year","poverty_gap_pct":"poverty_gap_pct","shock_payment_readiness_gap":"shock_payment_readiness_gap"})
        print(f"  social_protection_dmc: {n}")
        if n: log_sync(cur, "research.social_protection_dmc", n, p)

        n, p = load_psdq(cur)
        print(f"  psdq_admin1: {n}")
        if n: log_sync(cur, "research.psdq_admin1", n, p)

        n, p = load_simple_panel(cur, "water-stress-crop-diversification/generated/water-stress-crop-adb-panel.json", "research.water_crop_dmc",
            {"iso3":"iso3","water_withdrawal_pct_resources":"water_withdrawal_pct_resources","water_withdrawal_year":"water_withdrawal_year","agri_land_pct":"agri_land_pct","arable_land_pct":"arable_land_pct","cereal_yield_kg_per_ha":"cereal_yield_kg_per_ha","rural_population_pct":"rural_population_pct","water_crop_pressure_index":"water_crop_pressure_index"})
        print(f"  water_crop_dmc: {n}")
        if n: log_sync(cur, "research.water_crop_dmc", n, p)

        c.commit()
        print("\nSync complete.")

        # Quick verification
        cur.execute("SELECT COUNT(*) FROM research.v_vulnerability_matrix")
        print(f"  v_vulnerability_matrix rows: {cur.fetchone()[0]}")
        cur.execute("SELECT iso3, country, port_friction, remittance_fragility, grid_concentration FROM research.v_vulnerability_matrix WHERE iso3 IN ('PHL','BGD','IND','PAK','TKM') ORDER BY iso3")
        print("  sample:")
        for r in cur.fetchall():
            print(f"    {r}")
    except Exception as e:
        c.rollback()
        raise
    finally:
        c.close()


if __name__ == "__main__":
    main()
