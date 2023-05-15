-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - permits.combined
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy permits.combined to '/Users/edf/repos/carb_elec/dump/csv/permits_combined.csv' (format csv, header true);
