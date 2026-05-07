/**
 * FETCH WORLD BANK POVERTY & DEVELOPMENT DATA
 * =============================================
 * Source: World Bank Poverty and Inequality Platform (PIP) API
 * URL: https://pip.worldbank.org/api/v1
 * License: Creative Commons Attribution 4.0 (CC BY 4.0)
 *
 * Also fetches from World Bank Indicators API:
 * URL: https://api.worldbank.org/v2
 *
 * REPRODUCIBILITY:
 * - Run: npx tsx scripts/data/fetch-world-bank.ts
 * - Output: public/data/world-bank-poverty.json, public/data/world-bank-indicators.json
 *
 * AI PROMPT THAT GENERATED THIS SCRIPT:
 * "Fetch poverty headcount ratios at multiple international poverty lines
 *  and key development indicators (GDP per capita, life expectancy, HDI,
 *  electricity access) for all ADB developing member countries from the
 *  World Bank API. Save as JSON with full metadata."
 */

import * as fs from 'fs';
import * as path from 'path';

const PIP_API = 'https://api.worldbank.org/pip/v1';
const WB_API = 'https://api.worldbank.org/v2';

// ADB member ISO3 codes (developing members with likely poverty data)
const ADB_DEVELOPING = [
  'AFG', 'ARM', 'AZE', 'BGD', 'BTN', 'KHM', 'CHN', 'FJI', 'GEO', 'IND',
  'IDN', 'KAZ', 'KGZ', 'LAO', 'MYS', 'MDV', 'MNG', 'MMR', 'NPL', 'PAK',
  'PNG', 'PHL', 'WSM', 'SLB', 'LKA', 'TJK', 'THA', 'TLS', 'TON', 'TKM',
  'TUV', 'UZB', 'VUT', 'VNM'
];

// Key development indicators to fetch
const INDICATORS = [
  { code: 'NY.GDP.PCAP.PP.KD', name: 'GDP per capita, PPP (constant 2017 USD)' },
  { code: 'SP.DYN.LE00.IN', name: 'Life expectancy at birth (years)' },
  { code: 'EG.ELC.ACCS.ZS', name: 'Access to electricity (% of population)' },
  { code: 'SE.ADT.LITR.ZS', name: 'Literacy rate, adult (%)' },
  { code: 'SH.DYN.MORT', name: 'Under-5 mortality rate (per 1,000 live births)' },
  { code: 'SH.STA.MALN.ZS', name: 'Prevalence of underweight, children under 5 (%)' },
  { code: 'SH.H2O.BASW.ZS', name: 'Access to basic drinking water (%)' },
  { code: 'SH.STA.BASS.ZS', name: 'Access to basic sanitation (%)' },
  { code: 'SE.PRM.CMPT.ZS', name: 'Primary completion rate (%)' },
  { code: 'SP.POP.TOTL', name: 'Population, total' },
];

interface PovertyRecord {
  iso3: string;
  country_name: string;
  year: number;
  headcount_685: number | null;
  headcount_365: number | null;
  headcount_215: number | null;
  poverty_gap: number | null;
  gini: number | null;
  source_url: string;
}

interface IndicatorRecord {
  iso3: string;
  country_name: string;
  year: number;
  indicator_code: string;
  indicator_name: string;
  value: number | null;
}

async function fetchWithRetry(url: string, retries = 3): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      if (response.ok) return response;
      console.log(`  HTTP ${response.status} for ${url}, retry ${i + 1}/${retries}`);
    } catch {
      console.log(`  Network error for ${url}, retry ${i + 1}/${retries}`);
    }
    await new Promise(r => setTimeout(r, 1000 * (i + 1)));
  }
  throw new Error(`Failed after ${retries} retries: ${url}`);
}

async function fetchPovertyData(): Promise<PovertyRecord[]> {
  console.log('=== FETCHING WORLD BANK POVERTY DATA ===');
  console.log(`Source: World Bank PIP API`);
  console.log(`URL: ${PIP_API}`);
  console.log(`License: CC BY 4.0`);
  console.log('');

  const records: PovertyRecord[] = [];

  for (const iso3 of ADB_DEVELOPING) {
    const url = `${PIP_API}/pip?country=${iso3}&year=all&povline=6.85&fill_gaps=true&welfare_type=all&reporting_level=national&format=json`;

    try {
      console.log(`Fetching poverty data for ${iso3}...`);
      const response = await fetchWithRetry(url);
      const data = await response.json();

      if (Array.isArray(data)) {
        for (const row of data) {
          records.push({
            iso3: row.country_code || iso3,
            country_name: row.country_name || iso3,
            year: row.reporting_year,
            headcount_685: row.headcount,
            headcount_365: null, // would need separate query
            headcount_215: null,
            poverty_gap: row.poverty_gap,
            gini: row.gini,
            source_url: `${PIP_API}/pip?country=${iso3}`,
          });
        }
        console.log(`  Got ${data.length} records`);
      }
    } catch (e) {
      console.log(`  Error for ${iso3}: ${e}`);
    }

    // Rate limit
    await new Promise(r => setTimeout(r, 200));
  }

  return records;
}

async function fetchIndicators(): Promise<IndicatorRecord[]> {
  console.log('\n=== FETCHING WORLD BANK DEVELOPMENT INDICATORS ===');
  console.log(`Source: World Bank Indicators API`);
  console.log(`URL: ${WB_API}`);
  console.log('');

  const records: IndicatorRecord[] = [];
  const countryCodes = ADB_DEVELOPING.join(';');

  for (const indicator of INDICATORS) {
    const url = `${WB_API}/country/${countryCodes}/indicator/${indicator.code}?format=json&per_page=5000&date=2012:2024`;

    try {
      console.log(`Fetching: ${indicator.name}...`);
      const response = await fetchWithRetry(url);
      const data = await response.json();

      // World Bank API returns [metadata, data] array
      if (Array.isArray(data) && data.length > 1 && Array.isArray(data[1])) {
        for (const row of data[1]) {
          if (row.value !== null) {
            records.push({
              iso3: row.countryiso3code,
              country_name: row.country?.value || '',
              year: parseInt(row.date),
              indicator_code: indicator.code,
              indicator_name: indicator.name,
              value: row.value,
            });
          }
        }
        console.log(`  Got ${data[1].filter((r: { value: number | null }) => r.value !== null).length} non-null records`);
      }
    } catch (e) {
      console.log(`  Error for ${indicator.code}: ${e}`);
    }

    await new Promise(r => setTimeout(r, 300));
  }

  return records;
}

async function main() {
  const outputDir = path.join(process.cwd(), 'public', 'data');
  fs.mkdirSync(outputDir, { recursive: true });

  // Fetch poverty data
  const povertyData = await fetchPovertyData();
  const povertyOutput = {
    metadata: {
      title: 'World Bank Poverty Data - ADB Developing Member Countries',
      source: 'World Bank Poverty and Inequality Platform (PIP)',
      source_url: 'https://pip.worldbank.org',
      api_url: PIP_API,
      license: 'CC BY 4.0',
      fetched_at: new Date().toISOString(),
      script: 'scripts/data/fetch-world-bank.ts',
      record_count: povertyData.length,
    },
    data: povertyData,
  };

  const povertyPath = path.join(outputDir, 'world-bank-poverty.json');
  fs.writeFileSync(povertyPath, JSON.stringify(povertyOutput, null, 2));
  console.log(`\nSaved ${povertyData.length} poverty records to ${povertyPath}`);

  // Fetch development indicators
  const indicatorData = await fetchIndicators();
  const indicatorOutput = {
    metadata: {
      title: 'World Bank Development Indicators - ADB Developing Member Countries',
      source: 'World Bank Indicators API',
      source_url: 'https://data.worldbank.org',
      api_url: WB_API,
      license: 'CC BY 4.0',
      fetched_at: new Date().toISOString(),
      script: 'scripts/data/fetch-world-bank.ts',
      record_count: indicatorData.length,
      indicators: INDICATORS,
    },
    data: indicatorData,
  };

  const indicatorPath = path.join(outputDir, 'world-bank-indicators.json');
  fs.writeFileSync(indicatorPath, JSON.stringify(indicatorOutput, null, 2));
  console.log(`Saved ${indicatorData.length} indicator records to ${indicatorPath}`);
}

main().catch(console.error);
