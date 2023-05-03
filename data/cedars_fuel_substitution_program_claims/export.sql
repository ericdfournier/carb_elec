-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
 * - cedars.fuel_substitution_program_claims
 *
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy cedars.fuel_substitution_program_claims to '/Users/edf/repos/carb_elec/dump/csv/cedars_fuel_substitution_program_claims.csv' (format csv, header true);
