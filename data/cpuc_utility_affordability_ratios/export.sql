-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - cpuc.ca_2020_aac_tract
 * - cpuc.ca_2020_ar_puma
 * - cpuc.ca_2020_electric_aac_tract
 * - cpuc.ca_2020_electric_ar_puma
 * - cpuc.ca_2020_gas_aac_tract
 * - cpuc.ca_2020_gas_ar_puma
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy cpuc.ca_2020_aac_tract to '/Users/edf/repos/carb_elec/dump/csv/cpuc_2020_aac_tract.csv' (format csv, header true);
\copy cpuc.ca_2020_ar_puma to '/Users/edf/repos/carb_elec/dump/csv/cpuc_2020_ar_puma.csv' (format csv, header true);
\copy cpuc.ca_2020_electric_aac_tract to '/Users/edf/repos/carb_elec/dump/csv/cpuc_2020_electric_aac_tract.csv' (format csv, header true);
\copy cpuc.ca_2020_electric_ar_puma to '/Users/edf/repos/carb_elec/dump/csv/cpuc_2020_electric_ar_puma.csv' (format csv, header true);
\copy cpuc.ca_2020_gas_aac_tract to '/Users/edf/repos/carb_elec/dump/csv/cpuc_2020_gas_aac_tract.csv' (format csv, header true);
\copy cpuc.ca_2020_gas_ar_puma to '/Users/edf/repos/carb_elec/dump/csv/cpuc_2020_gas_ar_puma.csv' (format csv, header true);
