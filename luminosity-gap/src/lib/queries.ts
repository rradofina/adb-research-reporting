import { supabase } from './supabase';

export interface CountryMPI {
  iso3: string;
  name: string;
  adb_region: string;
  survey_year: number;
  mpi_value: number;
  headcount_ratio: number;
  intensity: number;
  health_contribution: number;
  education_contribution: number;
  living_std_contribution: number;
  d_nutrition: number | null;
  d_child_mortality: number | null;
  d_years_schooling: number | null;
  d_school_attendance: number | null;
  d_cooking_fuel: number | null;
  d_sanitation: number | null;
  d_drinking_water: number | null;
  d_electricity: number | null;
  d_housing: number | null;
  d_assets: number | null;
}

export async function getCountryMPIData(): Promise<CountryMPI[]> {
  const { data, error } = await supabase
    .from('mpi_data')
    .select(`
      survey_year,
      mpi_value,
      headcount_ratio,
      intensity,
      health_contribution,
      education_contribution,
      living_std_contribution,
      d_nutrition,
      d_child_mortality,
      d_years_schooling,
      d_school_attendance,
      d_cooking_fuel,
      d_sanitation,
      d_drinking_water,
      d_electricity,
      d_housing,
      d_assets,
      countries (
        iso3,
        name,
        adb_region
      )
    `)
    .is('subnational_id', null)
    .order('mpi_value', { ascending: false });

  if (error) {
    console.error('Error fetching MPI data:', error);
    return [];
  }

  return (data || []).map((row: Record<string, unknown>) => {
    const country = row.countries as Record<string, string> | null;
    return {
      iso3: country?.iso3 || '',
      name: country?.name || '',
      adb_region: country?.adb_region || '',
      survey_year: row.survey_year as number,
      mpi_value: row.mpi_value as number,
      headcount_ratio: row.headcount_ratio as number,
      intensity: row.intensity as number,
      health_contribution: row.health_contribution as number,
      education_contribution: row.education_contribution as number,
      living_std_contribution: row.living_std_contribution as number,
      d_nutrition: row.d_nutrition as number | null,
      d_child_mortality: row.d_child_mortality as number | null,
      d_years_schooling: row.d_years_schooling as number | null,
      d_school_attendance: row.d_school_attendance as number | null,
      d_cooking_fuel: row.d_cooking_fuel as number | null,
      d_sanitation: row.d_sanitation as number | null,
      d_drinking_water: row.d_drinking_water as number | null,
      d_electricity: row.d_electricity as number | null,
      d_housing: row.d_housing as number | null,
      d_assets: row.d_assets as number | null,
    };
  });
}
