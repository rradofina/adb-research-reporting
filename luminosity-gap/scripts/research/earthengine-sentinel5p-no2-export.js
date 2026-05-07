// Earth Engine Code Editor script for the air-monitoring pipeline.
//
// Purpose:
// Export annual Sentinel-5P/TROPOMI tropospheric NO2 summaries for ADB regional
// member economies. Run this in the Earth Engine Code Editor after uploading or
// importing an ADB regional-economy boundary feature collection with ISO3 codes.
//
// Required asset:
// - Replace ADB_BOUNDARIES_ASSET with a FeatureCollection containing an `iso3`
//   property matching the OpenAQ/WDI output.
//
// Output:
// - CSV with iso3, country/economy name, and mean tropospheric NO2 column.
// - Join this CSV to src/data/generated/air-monitoring-openaq-pilots.json in a
//   follow-up local script.

var ADB_BOUNDARIES_ASSET = 'users/YOUR_USERNAME/adb_regional_boundaries_iso3';
var YEAR = 2024;

var boundaries = ee.FeatureCollection(ADB_BOUNDARIES_ASSET);
var no2 = ee
  .ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
  .filterDate(YEAR + '-01-01', YEAR + '-12-31')
  .select('tropospheric_NO2_column_number_density');

var annualMean = no2.mean().rename('tropospheric_no2_mol_m2');

var summary = annualMean.reduceRegions({
  collection: boundaries,
  reducer: ee.Reducer.mean(),
  scale: 1113.2,
  tileScale: 4,
});

Export.table.toDrive({
  collection: summary,
  description: 'adb_regional_sentinel5p_no2_' + YEAR,
  fileNamePrefix: 'adb_regional_sentinel5p_no2_' + YEAR,
  fileFormat: 'CSV',
});
