/**
 * PARSE OPHI MPI 2024 DATA TABLES
 * ================================
 * Source: OPHI Global MPI 2024, Oxford University
 * Downloaded from: https://ophi.org.uk/global-mpi/2024
 * License: CC BY 4.0
 *
 * Input: scripts/data/raw/mpi_2024_table1_national.xlsx
 * Output: public/data/mpi-national.json, public/data/mpi-national-adb.json
 *
 * REPRODUCIBILITY:
 * - Download Table 1 from https://ophi.org.uk/global-mpi/2024
 * - Run: npx tsx scripts/data/parse-ophi-mpi.ts
 */

import * as XLSX from 'xlsx';
import * as fs from 'fs';
import * as path from 'path';

const ADB_ISO3 = new Set([
  'AFG', 'ARM', 'AZE', 'BGD', 'BTN', 'BRN', 'KHM', 'CHN', 'FJI', 'GEO',
  'IND', 'IDN', 'KAZ', 'KGZ', 'LAO', 'MYS', 'MDV', 'MHL', 'FSM', 'MNG',
  'MMR', 'NPL', 'PAK', 'PLW', 'PNG', 'PHL', 'WSM', 'SLB', 'LKA', 'TJK',
  'THA', 'TLS', 'TON', 'TKM', 'TUV', 'UZB', 'VUT', 'VNM'
]);

function num(val: unknown): number | null {
  if (val === null || val === undefined || val === '' || val === '..') return null;
  const n = Number(val);
  return isNaN(n) ? null : n;
}

function main() {
  console.log('=== PARSING OPHI MPI 2024 DATA ===');
  console.log('Source: OPHI Global MPI 2024');
  console.log('License: CC BY 4.0');
  console.log(`Timestamp: ${new Date().toISOString()}\n`);

  const filePath = path.join(process.cwd(), 'scripts', 'data', 'raw', 'mpi_2024_table1_national.xlsx');

  if (!fs.existsSync(filePath)) {
    console.error('File not found:', filePath);
    console.error('Download from: https://ophi.org.uk/global-mpi/2024');
    process.exit(1);
  }

  const wb = XLSX.readFile(filePath);

  // ============================================================
  // Sheet 1.1: MPI headline values (row 9+ has data, col layout:)
  //   0: ISO numeric, 1: ISO3, 2: Country, 3: Region,
  //   4: Survey, 5: Year, 6: MPI, 7: Headcount, 8: Intensity,
  //   9: Vulnerable, 10: Severe, 11: Destitute MPI, 12: Destitute headcount
  // ============================================================
  const s1 = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1, defval: null }) as unknown[][];

  // ============================================================
  // Sheet 1.2: Censored headcount ratios (deprivation rates among the poor)
  //   0-5: same as above, 6: MPI,
  //   7: Nutrition, 8: Child mortality, 9: Years of schooling,
  //   10: School attendance, 11: Cooking fuel, 12: Sanitation,
  //   13: Drinking water, 14: Electricity, 15: Housing, 16: Assets
  // ============================================================
  const s2 = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[1]], { header: 1, defval: null }) as unknown[][];

  // ============================================================
  // Sheet 1.3: Contribution of deprivations (% each indicator contributes to MPI)
  //   0-6: same, 7: Health contrib, 8: Education contrib, 9: Living std contrib,
  //   10: Nutrition, 11: Child mortality, 12: Years of schooling,
  //   13: School attendance, 14: Cooking fuel, 15: Sanitation,
  //   16: Drinking water, 17: Electricity, 18: Housing, 19: Assets
  // ============================================================
  const s3 = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[2]], { header: 1, defval: null }) as unknown[][];

  // Build lookup maps for sheets 2 and 3 by ISO3 code
  const DATA_START = 9; // Row 9 is first data row (0-indexed)

  const s2Map = new Map<string, unknown[]>();
  for (let i = DATA_START; i < s2.length; i++) {
    const row = s2[i];
    if (row && row[1]) s2Map.set(String(row[1]).trim(), row);
  }

  const s3Map = new Map<string, unknown[]>();
  for (let i = DATA_START; i < s3.length; i++) {
    const row = s3[i];
    if (row && row[1]) s3Map.set(String(row[1]).trim(), row);
  }

  console.log(`Sheet 1.1: ${s1.length} rows`);
  console.log(`Sheet 1.2: ${s2.length} rows (${s2Map.size} countries)`);
  console.log(`Sheet 1.3: ${s3.length} rows (${s3Map.size} countries)`);

  // Parse all countries
  interface Record {
    iso3: string;
    country: string;
    world_region: string;
    survey: string;
    survey_year: string;
    mpi_value: number | null;
    headcount_ratio: number | null;
    intensity: number | null;
    vulnerable_pct: number | null;
    severe_pct: number | null;
    health_contribution_pct: number | null;
    education_contribution_pct: number | null;
    living_std_contribution_pct: number | null;
    censored_nutrition: number | null;
    censored_child_mortality: number | null;
    censored_years_schooling: number | null;
    censored_school_attendance: number | null;
    censored_cooking_fuel: number | null;
    censored_sanitation: number | null;
    censored_drinking_water: number | null;
    censored_electricity: number | null;
    censored_housing: number | null;
    censored_assets: number | null;
    contrib_nutrition_pct: number | null;
    contrib_child_mortality_pct: number | null;
    contrib_years_schooling_pct: number | null;
    contrib_school_attendance_pct: number | null;
    contrib_cooking_fuel_pct: number | null;
    contrib_sanitation_pct: number | null;
    contrib_drinking_water_pct: number | null;
    contrib_electricity_pct: number | null;
    contrib_housing_pct: number | null;
    contrib_assets_pct: number | null;
    is_adb_member: boolean;
  }

  const records: Record[] = [];

  for (let i = DATA_START; i < s1.length; i++) {
    const r1 = s1[i];
    if (!r1 || !r1[1]) continue;

    const iso3 = String(r1[1]).trim();
    if (!iso3 || iso3.length !== 3) continue;

    const r2 = s2Map.get(iso3) || [];
    const r3 = s3Map.get(iso3) || [];

    records.push({
      iso3,
      country: String(r1[2] || '').trim(),
      world_region: String(r1[3] || '').trim(),
      survey: String(r1[4] || '').trim(),
      survey_year: String(r1[5] || '').trim(),

      // Sheet 1.1: Headline
      mpi_value: num(r1[6]),
      headcount_ratio: num(r1[7]),
      intensity: num(r1[8]),
      vulnerable_pct: num(r1[9]),
      severe_pct: num(r1[10]),

      // Sheet 1.3: Dimension contributions
      health_contribution_pct: num(r3[7]),
      education_contribution_pct: num(r3[8]),
      living_std_contribution_pct: num(r3[9]),

      // Sheet 1.2: Censored headcount ratios (deprivation rates)
      censored_nutrition: num(r2[7]),
      censored_child_mortality: num(r2[8]),
      censored_years_schooling: num(r2[9]),
      censored_school_attendance: num(r2[10]),
      censored_cooking_fuel: num(r2[11]),
      censored_sanitation: num(r2[12]),
      censored_drinking_water: num(r2[13]),
      censored_electricity: num(r2[14]),
      censored_housing: num(r2[15]),
      censored_assets: num(r2[16]),

      // Sheet 1.3: Individual indicator contributions
      contrib_nutrition_pct: num(r3[10]),
      contrib_child_mortality_pct: num(r3[11]),
      contrib_years_schooling_pct: num(r3[12]),
      contrib_school_attendance_pct: num(r3[13]),
      contrib_cooking_fuel_pct: num(r3[14]),
      contrib_sanitation_pct: num(r3[15]),
      contrib_drinking_water_pct: num(r3[16]),
      contrib_electricity_pct: num(r3[17]),
      contrib_housing_pct: num(r3[18]),
      contrib_assets_pct: num(r3[19]),

      is_adb_member: ADB_ISO3.has(iso3),
    });
  }

  console.log(`\nParsed ${records.length} country records`);
  const adbRecords = records.filter(r => r.is_adb_member);
  console.log(`ADB members found: ${adbRecords.length}`);

  // Save all countries
  const outputDir = path.join(process.cwd(), 'public', 'data');
  fs.mkdirSync(outputDir, { recursive: true });

  const metadata = {
    title: 'Global MPI 2024 - National Results with Dimension Decomposition',
    source: 'OPHI Global MPI 2024',
    source_url: 'https://ophi.org.uk/global-mpi/2024',
    download_url: 'https://ophi.org.uk/sites/default/files/2024-10/Table%201%20National%20Results%20MPI%202024.xlsx',
    license: 'CC BY 4.0',
    citation: 'Alkire, S., Kanagaratnam, U. and Suppa, N. (2024). The global Multidimensional Poverty Index (MPI) 2024.',
    parsed_at: new Date().toISOString(),
    script: 'scripts/data/parse-ophi-mpi.ts',
    total_countries: records.length,
    adb_members: adbRecords.length,
    sheets_used: ['1.1 National MPI Results', '1.2 Censored Headcounts', "1.3 Contribut'n of Deprivations"],
  };

  fs.writeFileSync(
    path.join(outputDir, 'mpi-national.json'),
    JSON.stringify({ metadata, data: records }, null, 2)
  );
  console.log(`Saved all ${records.length} countries to public/data/mpi-national.json`);

  fs.writeFileSync(
    path.join(outputDir, 'mpi-national-adb.json'),
    JSON.stringify({ metadata: { ...metadata, title: metadata.title + ' (ADB Members)' }, data: adbRecords }, null, 2)
  );
  console.log(`Saved ${adbRecords.length} ADB members to public/data/mpi-national-adb.json`);

  // Print ADB summary — the core research data
  console.log('\n=== ADB MEMBER MPI DIMENSION DECOMPOSITION ===');
  console.log('Country'.padEnd(22), 'MPI'.padEnd(8), 'Health%'.padEnd(10), 'Edu%'.padEnd(10), 'Living%'.padEnd(10));
  console.log('-'.repeat(60));

  for (const r of adbRecords.sort((a, b) => (b.mpi_value || 0) - (a.mpi_value || 0))) {
    const mpi = r.mpi_value !== null ? r.mpi_value.toFixed(3) : 'N/A';
    const h = r.health_contribution_pct !== null ? r.health_contribution_pct.toFixed(1) : 'N/A';
    const e = r.education_contribution_pct !== null ? r.education_contribution_pct.toFixed(1) : 'N/A';
    const l = r.living_std_contribution_pct !== null ? r.living_std_contribution_pct.toFixed(1) : 'N/A';
    console.log(`${r.iso3} ${r.country.padEnd(18)} ${mpi.padEnd(8)} ${h.padEnd(10)} ${e.padEnd(10)} ${l.padEnd(10)}`);
  }
}

main();
