-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - ren.all_merged
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy ren.all_merged to '/Users/edf/repos/carb_elec/dump/csv/ren_all_merged.csv' (format csv, header true);
