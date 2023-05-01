-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - carb.building_permits
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy permits.combined_raw to '/Users/edf/repos/carb_elec/dump/csv/permits_combined_raw.csv' (format csv, header true);
