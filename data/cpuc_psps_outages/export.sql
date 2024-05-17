-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - cpuc.psps_outages_2013_2023
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy cpuc.psps_outages_2013_2023 to '/Users/edf/repos/carb_elec/dump/csv/cpuc_psps_outages_2013_2023.csv' (format csv, header true);
