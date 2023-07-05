-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - cec.ca_electric_utilities_2022
 * - cec.ca_electric_load_serving_entities_2022
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy cec.ca_electric_utilities_2022 to '/Users/edf/repos/carb_elec/dump/csv/cec_ca_electric_utilities_2022.csv' (format csv, header true);
\copy cec.ca_electric_load_serving_entities_2022 to '/Users/edf/repos/carb_elec/dump/csv/cec_ca_electric_load_serving_entities_2022.csv' (format csv, header true);
