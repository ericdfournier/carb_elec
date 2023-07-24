-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - noaa.us_medium_shoreline
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy noaa.us_medium_shoreline to '/Users/edf/repos/carb_elec/dump/csv/noaa_us_medium_shoreline.csv' (format csv, header true);
