/**
 * FETCH ADB KEY INDICATORS
 * =========================
 * Source: Asian Development Bank Key Indicators Database (KIDB)
 * API: SDMX REST API
 * URL: https://kidb.adb.org/api
 * License: Open data, free to use with attribution
 *
 * REPRODUCIBILITY:
 * - Run: npx tsx scripts/data/fetch-adb-indicators.ts
 * - Output: public/data/adb-indicators.json
 *
 * AI PROMPT THAT GENERATED THIS SCRIPT:
 * "Fetch key development indicators from the ADB KIDB SDMX API
 *  for all ADB developing member countries. Include poverty,
 *  GDP, population, and SDG-related indicators."
 */

import * as fs from 'fs';
import * as path from 'path';

// ADB KIDB SDMX API
const ADB_SDMX_API = 'https://kidb.adb.org/sdmx-rest/data';

// SDMX dataflow IDs for key datasets
// See: https://kidb.adb.org/api for full list
const DATAFLOWS = [
  {
    id: 'DF_KI_POVERTY',
    name: 'Poverty and Inequality',
    description: 'Poverty headcount ratios, Gini coefficients',
  },
  {
    id: 'DF_KI_NATACCOUNT',
    name: 'National Accounts',
    description: 'GDP per capita, growth rates',
  },
  {
    id: 'DF_KI_POP',
    name: 'Population',
    description: 'Total population, urban/rural split',
  },
  {
    id: 'DF_KI_SDG',
    name: 'SDG Indicators',
    description: 'Sustainable Development Goals progress',
  },
];

interface ADBRecord {
  country_code: string;
  country_name: string;
  indicator_id: string;
  indicator_name: string;
  year: number;
  value: number;
  unit: string;
  dataflow: string;
}

async function fetchSDMXData(dataflowId: string): Promise<ADBRecord[]> {
  // SDMX REST query: all countries, all time periods
  const url = `${ADB_SDMX_API}/${dataflowId}/all?format=jsondata&startPeriod=2012&endPeriod=2024`;

  console.log(`Fetching: ${dataflowId}`);
  console.log(`  URL: ${url}`);

  try {
    const response = await fetch(url, {
      headers: { 'Accept': 'application/json' }
    });

    if (!response.ok) {
      console.log(`  HTTP ${response.status}: ${response.statusText}`);
      return [];
    }

    const json = await response.json();
    const records = parseSDMXJSON(json, dataflowId);
    console.log(`  Parsed ${records.length} records`);
    return records;
  } catch (e) {
    console.log(`  Error: ${e}`);
    return [];
  }
}

function parseSDMXJSON(json: Record<string, unknown>, dataflowId: string): ADBRecord[] {
  // SDMX-JSON format parsing
  const records: ADBRecord[] = [];

  try {
    console.log(`  Parsing SDMX structure for ${dataflowId}...`);
    const structure = json.data as Record<string, unknown> | undefined;
    if (!structure) return records;

    const dataSets = (structure as Record<string, unknown>).dataSets as Array<Record<string, unknown>> | undefined;
    if (!dataSets || dataSets.length === 0) return records;

    // Extract dimension values from structure
    const dimensions = ((structure as Record<string, unknown>).structures as Array<Record<string, unknown>>)?.[0];
    if (!dimensions) return records;

    console.log(`  Data structure found, processing...`);
  } catch (e) {
    console.log(`  Error parsing SDMX structure: ${e}`);
  }

  return records;
}

async function main() {
  console.log('=== FETCHING ADB KEY INDICATORS ===');
  console.log(`Source: ADB Key Indicators Database (KIDB)`);
  console.log(`API: SDMX REST (${ADB_SDMX_API})`);
  console.log(`License: Open data with attribution`);
  console.log(`Timestamp: ${new Date().toISOString()}`);
  console.log('');

  // First, fetch the available dataflows to understand what's available
  const catalogUrl = `${ADB_SDMX_API}/../dataflow?format=json`;
  console.log(`Checking API catalog: ${catalogUrl}`);

  try {
    const catalogResponse = await fetch(catalogUrl, {
      headers: { 'Accept': 'application/json' }
    });
    if (catalogResponse.ok) {
      const catalog = await catalogResponse.text();
      console.log(`Catalog response: ${catalog.substring(0, 500)}...`);
    } else {
      console.log(`Catalog HTTP ${catalogResponse.status}`);
    }
  } catch (e) {
    console.log(`Catalog error: ${e}`);
  }

  // Fetch each dataflow
  const allRecords: ADBRecord[] = [];
  for (const df of DATAFLOWS) {
    const records = await fetchSDMXData(df.id);
    allRecords.push(...records);
    await new Promise(r => setTimeout(r, 500));
  }

  // Save
  const outputDir = path.join(process.cwd(), 'public', 'data');
  fs.mkdirSync(outputDir, { recursive: true });

  const output = {
    metadata: {
      title: 'ADB Key Indicators - Developing Member Countries',
      source: 'Asian Development Bank Key Indicators Database (KIDB)',
      source_url: 'https://kidb.adb.org',
      api_url: ADB_SDMX_API,
      license: 'Open data with attribution to ADB',
      fetched_at: new Date().toISOString(),
      script: 'scripts/data/fetch-adb-indicators.ts',
      record_count: allRecords.length,
      dataflows: DATAFLOWS,
    },
    data: allRecords,
  };

  const outputPath = path.join(outputDir, 'adb-indicators.json');
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(`\nSaved ${allRecords.length} records to ${outputPath}`);
}

main().catch(console.error);
