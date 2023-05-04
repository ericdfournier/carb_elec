-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - hud.ca_2022_county_income_limits
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy hud.ca_2022_county_income_limits to '/Users/edf/repos/carb_elec/dump/csv/hud_ca_2022_county_income_limits.csv' (format csv, header true);
