-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - oehha.ca_ces4
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy oehha.ces4 to '/Users/edf/repos/carb_elec/dump/csv/oehha_ca_ces4.csv' (format csv, header true);
