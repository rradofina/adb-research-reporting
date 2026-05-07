"""Migrate v1 (per-program wide tables) → v2 (long-format obs.* + geo.* + pub.*).

Idempotent. Safe to re-run. Truncates in dependency order, then re-inserts.

Per CONSTITUTION.md §11, the repo cache + scripts remain source of truth;
this is a downstream projection.
"""
import os, json
from pathlib import Path
from datetime import datetime, timezone

import psycopg2
from psycopg2.extras import execute_batch, Json

ROOT = Path(__file__).resolve().parent.parent
for line in (ROOT / ".env.local").read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()


def conn():
    c = psycopg2.connect(
        host=os.environ["SUPABASE_DB_HOST"], port=int(os.environ["SUPABASE_DB_PORT"]),
        dbname=os.environ["SUPABASE_DB_NAME"], user=os.environ["SUPABASE_DB_USER"],
        password=os.environ["SUPABASE_DB_PASSWORD"], sslmode="require",
    )
    c.autocommit = False
    return c


# =====================================================================
# Country list — global, with ADB DMC flags
# =====================================================================

ADB_DMC_ISO3 = {
    "AFG","ARM","AZE","BGD","BTN","BRN","KHM","CHN","COK","FJI","GEO","HKG",
    "IND","IDN","KAZ","KIR","KGZ","LAO","MYS","MDV","MHL","FSM","MNG","MMR",
    "NRU","NPL","NIU","PAK","PLW","PNG","PHL","WSM","SLB","LKA","TJK","THA",
    "TLS","TON","TKM","TUV","UZB","VUT","VNM","TWN","TPE",
}
ADB_PACIFIC = {"COK","FJI","KIR","MHL","FSM","NRU","NIU","PLW","PNG","WSM","SLB","TON","TUV","VUT"}
ADB_NON_DMC_REGIONAL = {"AUS","NZL","JPN","KOR","SGP"}

# Minimal global country list (UN M49 majors — extends to all 195+ as needed).
# For now, seed with all ADB members (DMC + non-DMC regional) + key non-Asian
# trading partners we cite (US, UK, EU majors, GCC, RUS, UKR, etc.)
COUNTRIES = [
    # iso3, iso2, name, continent, un_subregion, official_name
    ("AFG","AF","Afghanistan","Asia","Southern Asia","Islamic Republic of Afghanistan"),
    ("ARM","AM","Armenia","Asia","Western Asia","Republic of Armenia"),
    ("AZE","AZ","Azerbaijan","Asia","Western Asia","Republic of Azerbaijan"),
    ("BGD","BD","Bangladesh","Asia","Southern Asia","People's Republic of Bangladesh"),
    ("BTN","BT","Bhutan","Asia","Southern Asia","Kingdom of Bhutan"),
    ("BRN","BN","Brunei Darussalam","Asia","South-eastern Asia","Brunei Darussalam"),
    ("KHM","KH","Cambodia","Asia","South-eastern Asia","Kingdom of Cambodia"),
    ("CHN","CN","China","Asia","Eastern Asia","People's Republic of China"),
    ("COK","CK","Cook Islands","Oceania","Polynesia","Cook Islands"),
    ("FJI","FJ","Fiji","Oceania","Melanesia","Republic of Fiji"),
    ("GEO","GE","Georgia","Asia","Western Asia","Georgia"),
    ("HKG","HK","Hong Kong, China","Asia","Eastern Asia","Hong Kong Special Administrative Region of China"),
    ("IND","IN","India","Asia","Southern Asia","Republic of India"),
    ("IDN","ID","Indonesia","Asia","South-eastern Asia","Republic of Indonesia"),
    ("KAZ","KZ","Kazakhstan","Asia","Central Asia","Republic of Kazakhstan"),
    ("KIR","KI","Kiribati","Oceania","Micronesia","Republic of Kiribati"),
    ("KGZ","KG","Kyrgyz Republic","Asia","Central Asia","Kyrgyz Republic"),
    ("LAO","LA","Lao PDR","Asia","South-eastern Asia","Lao People's Democratic Republic"),
    ("MYS","MY","Malaysia","Asia","South-eastern Asia","Malaysia"),
    ("MDV","MV","Maldives","Asia","Southern Asia","Republic of Maldives"),
    ("MHL","MH","Marshall Islands","Oceania","Micronesia","Republic of the Marshall Islands"),
    ("FSM","FM","Micronesia, Fed. Sts.","Oceania","Micronesia","Federated States of Micronesia"),
    ("MNG","MN","Mongolia","Asia","Eastern Asia","Mongolia"),
    ("MMR","MM","Myanmar","Asia","South-eastern Asia","Republic of the Union of Myanmar"),
    ("NRU","NR","Nauru","Oceania","Micronesia","Republic of Nauru"),
    ("NPL","NP","Nepal","Asia","Southern Asia","Federal Democratic Republic of Nepal"),
    ("NIU","NU","Niue","Oceania","Polynesia","Niue"),
    ("PAK","PK","Pakistan","Asia","Southern Asia","Islamic Republic of Pakistan"),
    ("PLW","PW","Palau","Oceania","Micronesia","Republic of Palau"),
    ("PNG","PG","Papua New Guinea","Oceania","Melanesia","Independent State of Papua New Guinea"),
    ("PHL","PH","Philippines","Asia","South-eastern Asia","Republic of the Philippines"),
    ("WSM","WS","Samoa","Oceania","Polynesia","Independent State of Samoa"),
    ("SLB","SB","Solomon Islands","Oceania","Melanesia","Solomon Islands"),
    ("LKA","LK","Sri Lanka","Asia","Southern Asia","Democratic Socialist Republic of Sri Lanka"),
    ("TJK","TJ","Tajikistan","Asia","Central Asia","Republic of Tajikistan"),
    ("THA","TH","Thailand","Asia","South-eastern Asia","Kingdom of Thailand"),
    ("TLS","TL","Timor-Leste","Asia","South-eastern Asia","Democratic Republic of Timor-Leste"),
    ("TON","TO","Tonga","Oceania","Polynesia","Kingdom of Tonga"),
    ("TKM","TM","Turkmenistan","Asia","Central Asia","Turkmenistan"),
    ("TUV","TV","Tuvalu","Oceania","Polynesia","Tuvalu"),
    ("UZB","UZ","Uzbekistan","Asia","Central Asia","Republic of Uzbekistan"),
    ("VUT","VU","Vanuatu","Oceania","Melanesia","Republic of Vanuatu"),
    ("VNM","VN","Viet Nam","Asia","South-eastern Asia","Socialist Republic of Viet Nam"),
    ("TWN","TW","Taiwan","Asia","Eastern Asia","Taiwan"),
    ("TPE","TW","Taipei,China","Asia","Eastern Asia","Taipei,China"),
    # ADB regional non-DMCs
    ("AUS","AU","Australia","Oceania","Australia and New Zealand","Commonwealth of Australia"),
    ("NZL","NZ","New Zealand","Oceania","Australia and New Zealand","New Zealand"),
    ("JPN","JP","Japan","Asia","Eastern Asia","Japan"),
    ("KOR","KR","Korea, Republic of","Asia","Eastern Asia","Republic of Korea"),
    ("SGP","SG","Singapore","Asia","South-eastern Asia","Republic of Singapore"),
    # Major non-Asian destinations (migration, trade, remittance corridors)
    ("USA","US","United States","Americas","Northern America","United States of America"),
    ("CAN","CA","Canada","Americas","Northern America","Canada"),
    ("GBR","GB","United Kingdom","Europe","Northern Europe","United Kingdom of Great Britain and Northern Ireland"),
    ("DEU","DE","Germany","Europe","Western Europe","Federal Republic of Germany"),
    ("FRA","FR","France","Europe","Western Europe","French Republic"),
    ("ITA","IT","Italy","Europe","Southern Europe","Italian Republic"),
    ("ESP","ES","Spain","Europe","Southern Europe","Kingdom of Spain"),
    ("NLD","NL","Netherlands","Europe","Western Europe","Kingdom of the Netherlands"),
    ("RUS","RU","Russia","Europe","Eastern Europe","Russian Federation"),
    ("UKR","UA","Ukraine","Europe","Eastern Europe","Ukraine"),
    ("ARE","AE","United Arab Emirates","Asia","Western Asia","United Arab Emirates"),
    ("SAU","SA","Saudi Arabia","Asia","Western Asia","Kingdom of Saudi Arabia"),
    ("QAT","QA","Qatar","Asia","Western Asia","State of Qatar"),
    ("KWT","KW","Kuwait","Asia","Western Asia","State of Kuwait"),
    ("BHR","BH","Bahrain","Asia","Western Asia","Kingdom of Bahrain"),
    ("OMN","OM","Oman","Asia","Western Asia","Sultanate of Oman"),
    ("IRN","IR","Iran","Asia","Southern Asia","Islamic Republic of Iran"),
    ("IRQ","IQ","Iraq","Asia","Western Asia","Republic of Iraq"),
    ("ISR","IL","Israel","Asia","Western Asia","State of Israel"),
    ("TUR","TR","Türkiye","Asia","Western Asia","Republic of Türkiye"),
    ("EGY","EG","Egypt","Africa","Northern Africa","Arab Republic of Egypt"),
    ("ZAF","ZA","South Africa","Africa","Sub-Saharan Africa","Republic of South Africa"),
    ("BRA","BR","Brazil","Americas","South America","Federative Republic of Brazil"),
    ("MEX","MX","Mexico","Americas","Central America","United Mexican States"),
]

LANDLOCKED = {"AFG","ARM","AZE","BTN","KAZ","KGZ","LAO","MNG","NPL","TJK","TKM","UZB"}
LDC = {"AFG","BGD","BTN","KHM","KIR","LAO","MMR","NPL","SLB","TLS","TUV","WSM"}
SIDS = {"COK","FJI","KIR","MHL","FSM","NRU","PLW","PNG","WSM","SLB","TON","TUV","VUT","NIU","MDV"}
ASEAN = {"BRN","KHM","IDN","LAO","MYS","MMR","PHL","SGP","THA","VNM"}
G20 = {"AUS","BRA","CHN","FRA","DEU","IND","IDN","ITA","JPN","KOR","MEX","RUS","SAU","ZAF","TUR","GBR","USA"}
WB_INCOME = {
    "AFG":"low","ARM":"upper-middle","AZE":"upper-middle","BGD":"lower-middle","BTN":"lower-middle","BRN":"high",
    "KHM":"lower-middle","CHN":"upper-middle","FJI":"upper-middle","GEO":"upper-middle","HKG":"high",
    "IND":"lower-middle","IDN":"upper-middle","KAZ":"upper-middle","KGZ":"lower-middle","LAO":"lower-middle",
    "MYS":"upper-middle","MDV":"upper-middle","MNG":"lower-middle","MMR":"lower-middle","NPL":"lower-middle",
    "PAK":"lower-middle","PHL":"lower-middle","LKA":"lower-middle","TJK":"lower-middle","THA":"upper-middle",
    "TLS":"lower-middle","TKM":"upper-middle","UZB":"lower-middle","VNM":"lower-middle",
    "AUS":"high","NZL":"high","JPN":"high","KOR":"high","SGP":"high","USA":"high","CAN":"high","GBR":"high",
    "DEU":"high","FRA":"high","ITA":"high","ESP":"high","NLD":"high",
}


def load_geo_country(cur):
    cur.execute("TRUNCATE geo.country CASCADE")
    rows = []
    for iso3, iso2, name, continent, subregion, off in COUNTRIES:
        rows.append((
            iso3, iso2, name, off, continent, subregion,
            iso3 in ADB_DMC_ISO3 or iso3 in ADB_NON_DMC_REGIONAL,  # is_adb_member
            iso3 in ADB_DMC_ISO3,                                   # is_adb_dmc
            iso3 in ADB_PACIFIC,                                    # is_adb_pacific
            iso3 in ASEAN,                                          # is_asean
            iso3 in {"AUS","NZL","JPN","KOR","USA","CAN","GBR","DEU","FRA","ITA","ESP","NLD"},  # is_oecd (subset)
            iso3 in {"DEU","FRA","ITA","ESP","NLD"},                # is_eu (subset)
            iso3 in G20,                                            # is_g20
            iso3 in LANDLOCKED,                                     # is_lldc
            iso3 in SIDS,                                           # is_sids
            iso3 in LDC,                                            # is_ldc
            WB_INCOME.get(iso3),                                    # wb_income_group
            None, None, None, None,                                 # centroid_lat, lon, area, pop
        ))
    cols = ["iso3","iso2","name","official_name","continent","un_subregion",
            "is_adb_member","is_adb_dmc","is_adb_pacific","is_asean","is_oecd","is_eu","is_g20",
            "is_lldc","is_sids","is_ldc","wb_income_group",
            "centroid_lat","centroid_lon","area_km2","population_2024"]
    placeholders = ",".join(["%s"] * len(cols))
    sql = f"INSERT INTO geo.country ({','.join(cols)}) VALUES ({placeholders})"
    execute_batch(cur, sql, rows, page_size=200)
    return len(rows)


# =====================================================================
# Programs — full §15 register
# =====================================================================

PROGRAMS = [
    (0,"mpi-nighttime-lights","MPI × nighttime lights decomposition (Asia-Pacific)","H",None,
     "Co-authored with Arturo Martinez Jr. Legacy program; OPHI MPI 2024 data pulled into repo; NTL integration not yet committed.",
     None,None,"Adofina / Martinez",False,None),
    (1,"access-services","Climate-adjusted access to services","SR",None,
     "104 ADM1 units across 8 ADB DMCs computed.",None,None,"Adofina",True,"/program/access-services"),
    (2,"digital-performance","Measured digital development gap","PP",None,
     "Ookla Open Data manifest + DuckDB SQL scaffold for PHL/BGD.",None,None,"Adofina",False,None),
    (3,"air-monitoring","Air pollution without air monitors","SR",None,
     "OpenAQ + WDI + WHO observability screen across 50 ADB regional economies.",None,None,"Adofina",True,"/program/air-monitoring"),
    (4,"invisible-urbanization","Invisible urbanization","H",None,
     "Source-backed method plan only; awaits Earth Engine onboarding.",None,None,"Adofina",False,None),
    (5,"climate-health-workdays","Climate-health workday loss","H",None,
     "WDI outdoor-labor × PM2.5 composite across 44 DMCs.",None,None,"Adofina",True,"/program/climate-health-workdays"),
    (6,"coastal-informal-risk","Coastal informal settlement risk","H",None,
     "Awaits Earth Engine onboarding (LECZ × built-up).",None,None,"Adofina",False,None),
    (7,"disaster-recovery-lag","Disaster recovery lag","H",None,
     "EM-DAT 2000-2025 burden layer for 38 DMCs.",None,None,"Adofina",True,"/program/disaster-recovery-lag"),
    (8,"flood-market-access","Flood-driven service and market isolation","H",None,
     "Awaits Earth Engine onboarding (JRC GSW × MAP friction × roads).",None,None,"Adofina",False,None),
    (9,"food-price-climate-transmission","Food-price climate transmission","H",None,
     "WDI macro composite; CHIRPS climate-transmission TODO.",None,None,"Adofina",True,"/program/food-price-climate-transmission"),
    (10,"grid-reliability-heat","Grid reliability under heat","H",None,
     "WRI Global Power Plant DB + WDI for 39 DMCs.",None,None,"Adofina",True,"/program/grid-reliability-heat"),
    (11,"migration-displacement-signals","Migration and displacement signals","H",None,
     "UN DESA 2024 bilateral stock for 44 DMCs.",None,None,"Adofina",True,"/program/migration-displacement-signals"),
    (12,"port-hinterland-friction","Port-hinterland trade friction","H",None,
     "WB LPI × WDI imports composite.",None,None,"Adofina",True,"/program/port-hinterland-friction"),
    (13,"public-service-data-quality","Public service data quality","H",24,
     "OSM-mapped facility counts vs DOH NHFR (PHL) and DGHS Facility Registry (BGD). Multi-DMC pilot.",
     "OSM-mapped facility counts disagree materially with the official national facility registry, with the disagreement systematically larger in rural and low-HDI ADM1 units.",
     "Claim retracted if OSM-vs-official agree within ±10% in two or more pilot DMCs AND the rural-urban gap is null.",
     "Adofina",True,"/program/public-service-data-quality"),
    (14,"remittance-resilience","Remittance resilience gaps","H",None,
     "RPW Q1 2025 × WDI remittance dependence composite.",None,None,"Adofina",True,"/program/remittance-resilience"),
    (15,"school-heat-disruption","School heat disruption","H",None,
     "CCKP historical tasmax × WDI children × PTR for 32 DMCs.",None,None,"Adofina",True,"/program/school-heat-disruption"),
    (16,"social-protection-shock-coverage","Social protection shock coverage","H",None,
     "WDI ASPIRE × Findex × poverty for 44 DMCs.",None,None,"Adofina",True,"/program/social-protection-shock-coverage"),
    (17,"water-stress-crop-diversification","Water stress and crop concentration","H",None,
     "WDI water × yield × rural composite.",None,None,"Adofina",True,"/program/water-stress-crop-diversification"),
]


def load_programs(cur):
    cur.execute("TRUNCATE research.program CASCADE")
    cols = ["id","slug","title","status","scoring_total","summary",
            "testable_claim","falsification","owner","has_artifact","href"]
    placeholders = ",".join(["%s"] * len(cols))
    execute_batch(cur, f"INSERT INTO research.program ({','.join(cols)}) VALUES ({placeholders})",
                  PROGRAMS, page_size=50)
    return len(PROGRAMS)


# =====================================================================
# Datasets — source registry
# =====================================================================

DATASETS = [
    ("wdi","World Bank World Development Indicators","World Bank","https://databank.worldbank.org/source/world-development-indicators",
     "https://api.worldbank.org/v2/","CC BY 4.0","https://datacatalog.worldbank.org/public-licenses","A","ongoing",
     "1500+ indicators across 200+ economies via REST API."),
    ("doh-nhfr","DOH National Health Facility Registry v2.0","Department of Health, Philippines","https://nhfr.doh.gov.ph/VActivefacilitiesList",
     "https://nhfr.doh.gov.ph/api/list/v_activefacilities","Unstated; public-information disclosure (RA 9485)",None,"A","2026-04-25 retrieval",
     "44,267 active facilities; JWT issued per landing page."),
    ("dghs-facility-registry","DGHS Facility Registry","Directorate General of Health Services, Bangladesh","https://hrm.dghs.gov.bd/public/facility-registry",
     "https://hrm.dghs.gov.bd/public/facility-registry/facilities/datatable/json","Unstated; public",None,"A","2026-04-25",
     "39,421 active facilities across 8 divisions; no auth required."),
    ("rpw-q1-2025","World Bank Remittance Prices Worldwide Q1 2025","World Bank","https://remittanceprices.worldbank.org/data-download",
     None,"World Bank open with attribution",None,"A","2025-Q1",
     "198,000 corridor-firm-period observations globally."),
    ("undesa-migrant-stock-2024","UN DESA International Migrant Stock 2024","UN DESA Population Division","https://www.un.org/development/desa/pd/content/international-migrant-stock",
     None,"CC BY 3.0 IGO","https://creativecommons.org/licenses/by/3.0/igo/","A","2024",
     "Bilateral migrant-stock 1990-2024."),
    ("emdat-2026-04-24","EM-DAT International Disaster Database","CRED, UCLouvain","https://data.humdata.org/dataset/emdat-country-profiles",
     None,"EM-DAT terms; non-commercial open access",None,"A","2026-04-24","Country profiles via HDX mirror."),
    ("wri-gpp-v1.3","WRI Global Power Plant Database v1.3.0","World Resources Institute","https://github.com/wri/global-power-plant-database",
     None,"CC BY 4.0",None,"A","v1.3.0 (frozen 2022)","30K+ plants worldwide."),
    ("ophi-mpi-2024","OPHI Global MPI 2024","Oxford Poverty and Human Development Initiative","https://ophi.org.uk/global-mpi/2024",
     None,"CC BY 4.0",None,"A","2024","112 economies; dimension decomposition."),
    ("openaq-v3","OpenAQ API v3","OpenAQ","https://api.openaq.org/v3/",
     "https://api.openaq.org/v3/","CC BY 4.0",None,"B","ongoing","Public air-monitor metadata; API key required."),
    ("who-aaq-v6.1","WHO Ambient Air Quality Database v6.1","World Health Organization","https://www.who.int/data/gho/data/themes/air-pollution",
     None,"WHO open",None,"A","v6.1","City-level PM2.5/PM10/NO2."),
    ("geoboundaries-gbopen","geoBoundaries gbOpen","Center for Geospatial Analysis, William & Mary","https://www.geoboundaries.org/",
     "https://www.geoboundaries.org/api/current/gbOpen/","CC BY 4.0",None,"A","ongoing","ADM0/ADM1/ADM2 for 200+ economies."),
    ("ookla-open-data","Speedtest by Ookla Global Performance","Ookla","https://registry.opendata.aws/speedtest-global-performance/",
     "s3://ookla-open-data/parquet/performance/","CC BY-NC-SA 4.0",None,"A","quarterly","Tile-level fixed/mobile speed."),
    ("ccmpa-data360","World Bank Data360 (incl. CCKP)","World Bank","https://data360.worldbank.org/",
     "https://cckpapi.worldbank.org/cckp/v1/","World Bank open",None,"A","ongoing","CCKP CMIP6 climatology."),
    ("dim-acled","ACLED Conflict Data","ACLED","https://acleddata.com/",
     "https://api.acleddata.com/","CC BY-SA 4.0 non-commercial",None,"B","ongoing","Conflict events; OAuth credentials required."),
    ("wb-lpi","World Bank Logistics Performance Index","World Bank","https://lpi.worldbank.org/",
     "https://api.worldbank.org/v2/","CC BY 4.0",None,"A","2018/2023","Survey-based LPI sub-indicators."),
]


def load_datasets(cur):
    cur.execute("TRUNCATE source.dataset CASCADE")
    cols = ["slug","name","publisher","url","api_endpoint","license","license_url","access_model","vintage","description_md"]
    placeholders = ",".join(["%s"] * len(cols))
    execute_batch(cur, f"INSERT INTO source.dataset ({','.join(cols)}) VALUES ({placeholders})",
                  DATASETS, page_size=50)
    cur.execute("SELECT slug, id FROM source.dataset")
    return dict(cur.fetchall())


# =====================================================================
# Indicators — register every metric we compute
# =====================================================================

def load_indicators(cur, dataset_ids, program_ids):
    """Register one row per indicator the system produces."""
    cur.execute("TRUNCATE obs.indicator CASCADE")

    indicators = [
        # (slug, program_slug, domain, name, unit, source_dataset_slug, methodology, is_composite, is_triage)
        ("psdq.osm_clinical_ratio","public-service-data-quality","measurement",
         "OSM ÷ NHFR/DGHS clinical-tier facility ratio","ratio","wdi",
         "OSM amenity=hospital/clinic/doctors counts ÷ official-registry clinical-tier (hospitals + main clinics + RHU + BHS + dialysis).",
         False, True),
        ("psdq.osm_principal_ratio","public-service-data-quality","measurement",
         "OSM ÷ NHFR/DGHS principal-tier facility ratio","ratio","wdi",
         "OSM ÷ official-registry principal-tier (hospitals + main clinics + RHU + city/municipal health office).",
         False, True),
        ("remit.fragility_index","remittance-resilience","finance",
         "Remittance fragility index","index 0-100","rpw-q1-2025",
         "min(WDI %GDP/25, 1) × min(RPW mean cost/15, 1) × 100. Triage.",
         True, True),
        ("remit.wdi_pct_gdp","remittance-resilience","finance",
         "Personal remittances received","% GDP","wdi",
         "WDI BX.TRF.PWKR.DT.GD.ZS, latest available year.",
         False, False),
        ("remit.rpw_mean_cost","remittance-resilience","finance",
         "Mean inbound remittance corridor cost","%","rpw-q1-2025",
         "Mean of cc1 total cost % across all RPW corridors with this DMC as destination, latest period.",
         False, False),
        ("grid.fuel_herfindahl","grid-reliability-heat","energy",
         "Fuel-mix concentration (Herfindahl)","unit interval","wri-gpp-v1.3",
         "Sum of squared fuel-share-of-capacity. 1.0 = single-fuel grid.",
         True, True),
        ("grid.total_capacity_mw","grid-reliability-heat","energy",
         "Total installed capacity","MW","wri-gpp-v1.3",
         "Sum of WRI GPP plant capacities for the country.",
         False, False),
        ("disaster.events_per_year","disaster-recovery-lag","disaster",
         "Disaster events per year (2000-2025 avg)","events/yr","emdat-2026-04-24",
         "Total events / years covered, EM-DAT 2000-2025.",
         False, False),
        ("disaster.total_affected","disaster-recovery-lag","disaster",
         "Total people affected","persons","emdat-2026-04-24",
         "Sum of EM-DAT 'Total Affected' field, 2000-2025.",
         False, False),
        ("migration.emigrant_stock","migration-displacement-signals","migration",
         "International migrant stock (origin)","persons","undesa-migrant-stock-2024",
         "UN DESA bilateral; sum across all destinations where origin = this country (countries only, no aggregates).",
         False, False),
        ("migration.immigrant_stock","migration-displacement-signals","migration",
         "International migrant stock (destination)","persons","undesa-migrant-stock-2024",
         "UN DESA bilateral; sum across all origins where destination = this country.",
         False, False),
        ("port.friction_exposure","port-hinterland-friction","trade",
         "Friction-exposure index","index","wb-lpi",
         "(5 - LPI overall) × min(sqrt(imports_B)/50, 2.0). Triage.",
         True, True),
        ("port.lpi_overall","port-hinterland-friction","trade",
         "Logistics Performance Index — overall","1-5","wb-lpi",
         "WB LPI overall score, latest survey.",
         False, False),
        ("water.stress_index","water-stress-crop-diversification","environment",
         "Water-crop pressure index","index","wdi",
         "min(water_withdrawal/100, 1.5) × min(3000/yield, 1.0) × rural_pct/100, × 100.",
         True, True),
        ("water.withdrawal_pct","water-stress-crop-diversification","environment",
         "Freshwater withdrawal","% of internal resources","wdi",
         "WDI ER.H2O.FWTL.ZS. Values >100% indicate transboundary dependence.",
         False, False),
        ("school.heat_pressure","school-heat-disruption","education",
         "School-heat pressure index","index","ccmpa-data360",
         "min(max(tasmax-25,0)/15,1) × (pop_0_14/100) × min(PTR/40, 1.5) × 100.",
         True, True),
        ("school.tasmax_historical","school-heat-disruption","environment",
         "Annual mean daily max temperature (1995-2014)","°C","ccmpa-data360",
         "CCKP CMIP6 historical climatology.",
         False, False),
        ("sp.shock_readiness_gap","social-protection-shock-coverage","social_protection",
         "Shock-payment readiness gap","index","wdi",
         "(poverty/100) × (1 - mean(SP_coverage, account_ownership)) × 100. Triage.",
         True, True),
        ("food.price_vulnerability","food-price-climate-transmission","food_security",
         "Food-price macro vulnerability","index","wdi",
         "min(CPI/20,1.5) × min(ag_imp/25,1.5) × max((110-fp_index)/20,0,1.5) × 100. Triage.",
         True, True),
        ("ch.workday_pressure","climate-health-workdays","health",
         "Workday-loss pressure (outdoor × PM2.5)","index","wdi",
         "(outdoor_labor_share/100) × min(max(PM2.5-5,0)/45, 1) × 100. Triage.",
         True, True),
        ("air.observability_gap","air-monitoring","environment",
         "PM2.5 observability gap score","index 0-100","wdi",
         "0.65 × WDI PM2.5 exposure pressure + 0.35 × public-monitor scarcity. Triage.",
         True, True),
        ("access.stress_index","access-services","social_services",
         "Access-stress composite (ADM1)","index 0-100","wdi",
         "Composite of service-load + climate stress + OSM-completeness risk per ADM1. Triage.",
         True, True),
    ]

    rows = []
    for slug, prog_slug, dom, name, unit, src_slug, method, is_comp, is_tri in indicators:
        rows.append((
            slug, program_ids.get(prog_slug), dom, name, unit,
            dataset_ids.get(src_slug), method, is_comp, is_tri,
            "sync-script-v2",
        ))
    cols = ["slug","program_id","domain","name","unit","source_dataset_id","methodology_md","is_composite","is_triage","added_by"]
    placeholders = ",".join(["%s"] * len(cols))
    execute_batch(cur, f"INSERT INTO obs.indicator ({','.join(cols)}) VALUES ({placeholders})",
                  rows, page_size=100)
    cur.execute("SELECT slug, id FROM obs.indicator")
    return dict(cur.fetchall())


# =====================================================================
# Migrate observations from research.* to obs.*
# =====================================================================

def migrate_observations(cur, ind_ids):
    """Pivot wide tables into long obs.country_value / obs.admin1_value."""
    cur.execute("TRUNCATE obs.country_value, obs.admin1_value, obs.corridor_value")
    n = 0

    # Map (research_table.column → indicator_slug, default_year)
    # Year defaults to "latest" placeholder 2024 unless we have a year column.
    country_pivots = [
        # (table, value_column, indicator_slug, year_column_or_default)
        ("research.psdq_admin1", None, None, None),  # ADM1 — handled separately
        ("research.remittance_dmc", "fragility_index", "remit.fragility_index", "wdi_year"),
        ("research.remittance_dmc", "wdi_remittance_pct_gdp", "remit.wdi_pct_gdp", "wdi_year"),
        ("research.remittance_dmc", "rpw_mean_cost_pct", "remit.rpw_mean_cost", 2025),
        ("research.grid_dmc", "fuel_herfindahl", "grid.fuel_herfindahl", "wdi_elec_access_year"),
        ("research.grid_dmc", "total_capacity_mw", "grid.total_capacity_mw", 2022),
        ("research.disaster_burden_dmc", "events_per_year", "disaster.events_per_year", 2025),
        ("research.disaster_burden_dmc", "total_affected", "disaster.total_affected", 2025),
        ("research.migration_dmc", "emigrant_stock_2024", "migration.emigrant_stock", 2024),
        ("research.migration_dmc", "immigrant_stock_2024", "migration.immigrant_stock", 2024),
        ("research.port_friction_dmc", "friction_exposure_index", "port.friction_exposure", "lpi_overall_year"),
        ("research.port_friction_dmc", "lpi_overall", "port.lpi_overall", "lpi_overall_year"),
        ("research.water_crop_dmc", "water_crop_pressure_index", "water.stress_index", "water_withdrawal_year"),
        ("research.water_crop_dmc", "water_withdrawal_pct_resources", "water.withdrawal_pct", "water_withdrawal_year"),
        ("research.school_heat_dmc", "school_heat_pressure_index", "school.heat_pressure", 2024),
        ("research.school_heat_dmc", "annual_tasmax_1995_2014_celsius", "school.tasmax_historical", 2014),
        ("research.social_protection_dmc", "shock_payment_readiness_gap", "sp.shock_readiness_gap", "poverty_year"),
        ("research.food_price_dmc", "food_price_vulnerability", "food.price_vulnerability", "cpi_year"),
        ("research.climate_health_dmc", "workday_loss_pressure_index", "ch.workday_pressure", "pm25_year"),
        ("research.air_monitoring_dmc", "pm25_observability_gap_score", "air.observability_gap", 2024),
    ]

    for table, val_col, ind_slug, year_col in country_pivots:
        if not val_col or not ind_slug:
            continue
        ind_id = ind_ids.get(ind_slug)
        if not ind_id:
            continue
        if isinstance(year_col, int):
            sql = f"SELECT iso3, %s::int AS year, {val_col} FROM {table} WHERE {val_col} IS NOT NULL"
            cur.execute(sql, (year_col,))
        else:
            sql = f"SELECT iso3, COALESCE({year_col}, 2024) AS year, {val_col} FROM {table} WHERE {val_col} IS NOT NULL"
            cur.execute(sql)
        rows = [(ind_id, iso3, year, float(val) if val is not None else None) for iso3, year, val in cur.fetchall()]
        # Skip rows with iso3 not in geo.country
        cur.execute("SELECT iso3 FROM geo.country")
        valid_iso3 = {r[0] for r in cur.fetchall()}
        rows = [r for r in rows if r[1] in valid_iso3]
        if rows:
            cur2 = cur.connection.cursor()
            execute_batch(cur2,
                "INSERT INTO obs.country_value (indicator_id, iso3, year, value_num) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                rows, page_size=500)
            cur2.close()
            n += len(rows)

    # Migrate ADM1 — psdq_admin1 + access_services_admin1
    cur.execute("SELECT iso3, admin1_code FROM research.psdq_admin1")
    cur.execute("""SELECT iso3, admin1_code, ratio_osm_to_clinical FROM research.psdq_admin1
                   WHERE ratio_osm_to_clinical IS NOT NULL""")
    psdq_rows = cur.fetchall()
    if psdq_rows and ind_ids.get("psdq.osm_clinical_ratio"):
        # First, ensure ADM1 dimension rows exist for all psdq ADM1
        cur.execute("SELECT iso3, admin1_code, admin1_name, population_2020 FROM research.psdq_admin1")
        adm1_rows = []
        for iso3, code, name, pop in cur.fetchall():
            adm1_rows.append((iso3, code, name, 2020, pop))
        cur.execute("TRUNCATE geo.admin1 CASCADE")
        execute_batch(cur,
            "INSERT INTO geo.admin1 (iso3, admin1_code, admin1_name, population_year, population) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            adm1_rows)
        # Also ingest from access_services_admin1 (different ADM1 codes likely)
        cur.execute("""SELECT iso3, admin1_code, admin1_name, 2020, population FROM research.access_services_admin1""")
        execute_batch(cur,
            "INSERT INTO geo.admin1 (iso3, admin1_code, admin1_name, population_year, population) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            cur.fetchall())

        ind_id = ind_ids["psdq.osm_clinical_ratio"]
        rows = [(ind_id, iso3, code, 2024, float(v)) for iso3, code, v in psdq_rows]
        execute_batch(cur,
            "INSERT INTO obs.admin1_value (indicator_id, iso3, admin1_code, year, value_num) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            rows, page_size=500)
        n += len(rows)

    # access-services access_stress_index
    cur.execute("""SELECT iso3, admin1_code, access_stress_index FROM research.access_services_admin1
                   WHERE access_stress_index IS NOT NULL""")
    access_rows = cur.fetchall()
    if access_rows and ind_ids.get("access.stress_index"):
        ind_id = ind_ids["access.stress_index"]
        rows = [(ind_id, iso3, code, 2024, float(v)) for iso3, code, v in access_rows]
        execute_batch(cur,
            "INSERT INTO obs.admin1_value (indicator_id, iso3, admin1_code, year, value_num) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            rows, page_size=500)
        n += len(rows)

    return n


# =====================================================================
# Author + first article (seed pub.*)
# =====================================================================

def seed_publishing(cur, prog_ids):
    cur.execute("TRUNCATE pub.author, pub.article CASCADE")

    cur.execute("""INSERT INTO pub.author (slug, full_name, affiliation, bio_md)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                ("raymond-adofina", "Raymond Adofina", "Asian Development Bank",
                 "Data analyst working on measurement-gap research for ADB DMCs."))
    author_id = cur.fetchone()[0]

    cur.execute("""INSERT INTO pub.article
        (slug, kind, status, title, subtitle, abstract_md, body_md,
         geographies, topics, is_featured)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        ("about-development-blindspots-lab",
         "blog",
         "draft",
         "About the Development Blindspots Lab",
         "Constitution-governed measurement-gap research for ADB DMCs and beyond",
         "An overview of the research agenda, governance, and current program register. Public-data-only; reproducibility-first.",
         """## What this is

The Development Blindspots Lab is a Constitution-governed research program
that targets a single class of question across many domains: **where does
official data diverge from reality, and what does that mean for policy?**

## Programs at a glance

- 14 of 17 programs have a computed screening artifact today.
- Coverage spans ADB DMCs in the Pacific, Central Asia, Caucasus, and
  South / Southeast / East Asia — with global headers (data corridors,
  migration partners) ready to plug in as the work scales beyond ADB.

## Governance

- The Constitution at repository root is the binding document.
- Public data only; every number traces to a committed script and
  cached source.
- AI assists with drafting; humans hold every claim-maturity gate
  and every published number.

## Where to look

- **/matrix** — cross-program vulnerability heatmap
- **/live** — Supabase-backed live SQL view
- **/methodology** — Constitution highlights
- **/sources** — data-access audit
- **/reproducibility** — rerun commands

This is the v1 reporting site. The program register, sources, and
methodology pages are the entry points for both ADB readers and the
research community.""",
         ["ADB-DMC", "global"],
         ["measurement", "poverty", "data-quality"],
         True))
    article_id = cur.fetchone()[0]

    cur.execute("INSERT INTO pub.article_author (article_id, author_id, author_order, is_corresponding) VALUES (%s,%s,1,true)",
                (article_id, author_id))

    # Link to all programs
    for pid in prog_ids.values():
        if pid is not None:
            cur.execute("INSERT INTO pub.article_program (article_id, program_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                        (article_id, pid))

    return author_id, article_id


def main():
    c = conn()
    try:
        cur = c.cursor()

        n = load_geo_country(cur);  print(f"  geo.country: {n}")
        n = load_programs(cur);     print(f"  research.program: {n}")
        cur.execute("SELECT slug, id FROM research.program")
        prog_ids = dict(cur.fetchall())
        ds_ids = load_datasets(cur); print(f"  source.dataset: {len(ds_ids)}")
        ind_ids = load_indicators(cur, ds_ids, prog_ids); print(f"  obs.indicator: {len(ind_ids)}")
        n = migrate_observations(cur, ind_ids); print(f"  obs.country_value + obs.admin1_value: {n}")
        author_id, article_id = seed_publishing(cur, prog_ids)
        print(f"  pub.author: 1, pub.article: 1 (id={article_id})")

        c.commit()

        # Refresh PostgREST schema cache
        cur.execute("NOTIFY pgrst, 'reload schema'")

        # Sanity check
        cur.execute("SELECT COUNT(*) FROM geo.country WHERE is_adb_dmc")
        print(f"  ADB DMC count: {cur.fetchone()[0]}")
        cur.execute("SELECT COUNT(*) FROM obs.indicator")
        print(f"  Indicators registered: {cur.fetchone()[0]}")
        cur.execute("SELECT COUNT(*) FROM obs.country_value")
        print(f"  Country observations: {cur.fetchone()[0]}")
        cur.execute("SELECT COUNT(*) FROM obs.admin1_value")
        print(f"  ADM1 observations: {cur.fetchone()[0]}")

        # Sample query: top fragility-index DMCs via the long-format table
        cur.execute("""
            SELECT c.iso3, c.name, cv.value_num
            FROM obs.country_value cv
            JOIN obs.indicator i ON i.id = cv.indicator_id
            JOIN geo.country c ON c.iso3 = cv.iso3
            WHERE i.slug = 'remit.fragility_index'
            ORDER BY cv.value_num DESC NULLS LAST LIMIT 5
        """)
        print("\nSample: top 5 remittance fragility (via obs.country_value):")
        for r in cur.fetchall(): print(f"  {r}")

    except Exception:
        c.rollback()
        raise
    finally:
        c.close()


if __name__ == "__main__":
    main()
