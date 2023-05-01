-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - pge.ica_feeder_detail
# - pge.ica_feeder_load_profile
# - pge.ica_feeder_not_available
# - pge.ica_line_detail
# - pge.ica_substation_load_profile
# - pge.ica_substation
# - pge.ica_tranmission_line
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy pge.ica_feeder_detail to '/Users/edf/repos/carb_elec/dump/csv/pge_ica_feeder_detail.csv' (format csv, header true);
\copy pge.ica_feeder_load_profile to '/Users/edf/repos/carb_elec/dump/csv/pge_ica_feeder_load_profile.csv' (format csv, header true);
\copy pge.ica_feeder_not_available to '/Users/edf/repos/carb_elec/dump/csv/pge_ica_feeder_not_available.csv' (format csv, header true);
\copy pge.ica_line_detail to '/Users/edf/repos/carb_elec/dump/csv/pge_ica_line_detail.csv' (format csv, header true);
\copy pge.ica_substation_load_profile to '/Users/edf/repos/carb_elec/dump/csv/pge_ica_substation_load_profile.csv' (format csv, header true);
\copy pge.ica_substation to '/Users/edf/repos/carb_elec/dump/csv/pge_ica_substation.csv' (format csv, header true);
\copy pge.ica_transmission_line to '/Users/edf/repos/carb_elec/dump/csv/pge_ica_transmission_line.csv' (format csv, header true);
