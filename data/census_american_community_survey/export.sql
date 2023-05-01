-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - census.acs_ca_2019_county_geom
 * - census.acs_ca_2019_place_geom
 * - census.acs_ca_2019_puma_geom
 * - census.acs_ca_2019_unincorporated_geom
 * - census.acs_ca_2019_tr_fuel
 * - census.acs_ca_2019_tr_housing
 * - census.acs_ca_2019_tr_income
 * - census.acs_ca_2019_tr_metadata
 * - census.acs_ca_2019_tr_population
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy census.acs_ca_2019_county_geom to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_county_geom.csv' (format csv, header true);
\copy census.acs_ca_2019_place_geom to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_place_geom.csv' (format csv, header true);
\copy census.acs_ca_2019_puma_geom to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_puma_geom.csv' (format csv, header true);
\copy census.acs_ca_2019_unincorporated_geom to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_unincorporated_geom.csv' (format csv, header true);
\copy census.acs_ca_2019_tr_fuel to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_tr_fuel.csv' (format csv, header true);
\copy census.acs_ca_2019_tr_housing to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_tr_housing.csv' (format csv, header true);
\copy census.acs_ca_2019_tr_income to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_tr_income.csv' (format csv, header true);
\copy census.acs_ca_2019_tr_metadata to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_tr_metadata.csv' (format csv, header true);
\copy census.acs_ca_2019_tr_population to '/Users/edf/repos/carb_elec/dump/csv/census_acs_ca_2019_tr_population.csv' (format csv, header true);
