-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - carb.ca_air_districts
 * - carb.ca_air_basins
 * - carb.ca_county_air_basin_districts
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy carb.ca_air_basins to '/Users/edf/repos/carb_elec/dump/csv/carb_ca_air_basins.csv' (format csv, header true);
\copy carb.ca_air_districts to '/Users/edf/repos/carb_elec/dump/csv/carb_ca_air_districts.csv' (format csv, header true);
\copy carb.ca_county_air_basin_districts to '/Users/edf/repos/carb_elec/dump/csv/carb_ca_county_air_basin_districts.csv' (format csv, header true);
