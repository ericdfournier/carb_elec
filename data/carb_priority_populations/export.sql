-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - carb.priority_populations
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy carb.priority_populations_ces4 to '/Users/edf/repos/carb_elec/dump/csv/carb_priority_populations_ces4.csv' (format csv, header true);
