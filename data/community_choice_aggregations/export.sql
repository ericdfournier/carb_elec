-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - cca.all_merged
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy cca.all_merged to '/Users/edf/repos/carb_elec/dump/csv/cca_all_merged.csv' (format csv, header true);
