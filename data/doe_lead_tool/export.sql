-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - doe.ca_ami_census_tracts_2018
# - doe.ca_ami_state_counties_cities_2018
# - doe.ca_fpl_census_tracts_2018
# - doe.ca_fpl_state_counties_cities_2018
# - doe.ca_smi_census_tracts_2018
# - doe.ca_smi_state_counties_cities_2018
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy doe.ca_ami_census_tracts_2018 to '/Users/edf/repos/carb_elec/dump/csv/doe_ca_ami_census_tracts_2018.csv' (format csv, header true);
\copy doe.ca_ami_state_counties_cities_2018 to '/Users/edf/repos/carb_elec/dump/csv/doe_ca_ami_state_counties_cities_2018.csv' (format csv, header true);
\copy doe.ca_fpl_census_tracts_2018 to '/Users/edf/repos/carb_elec/dump/csv/doe_ca_fpl_census_tracts_2018.csv' (format csv, header true);
\copy doe.ca_fpl_state_counties_cities_2018 to '/Users/edf/repos/carb_elec/dump/csv/doe_ca_fpl_state_counties_cities_2018.csv' (format csv, header true);
\copy doe.ca_smi_census_tracts_2018 to '/Users/edf/repos/carb_elec/dump/csv/doe_ca_smi_census_tracts_2018.csv' (format csv, header true);
\copy doe.ca_smi_state_counties_cities_2018 to '/Users/edf/repos/carb_elec/dump/csv/doe_ca_smi_state_counties_cities_2018.csv' (format csv, header true);
