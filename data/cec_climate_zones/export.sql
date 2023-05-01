-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - cec.ca_building_climate_zones_2021
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy cec.ca_building_climate_zones_2021 to '/Users/edf/repos/carb_elec/dump/csv/cec_ca_building_climate_zones_2021.csv' (format csv, header true);
