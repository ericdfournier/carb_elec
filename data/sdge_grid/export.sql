-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - sdge.gna_area
# - sdge.lnba_ddor_planned_area
# - sdge.ica_circuit_segments_non3phase
# - sdge.ica_circuit_segments_3phase_generation_capacity
# - sdge.ica_circuit_segments_3phase_load_capacity
# - sdge.lbna_ddor_candidate_area
# - sdge.substation_areas
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy sdge.gna_area to '/Users/edf/repos/carb_elec/dump/csv/sdge_gna_area.csv' (format csv, header true);
\copy sdge.lnba_ddor_planned_area to '/Users/edf/repos/carb_elec/dump/csv/sdge_lnba_ddor_planned_area.csv' (format csv, header true);
\copy sdge.ica_circuit_segments_non3phase to '/Users/edf/repos/carb_elec/dump/csv/sdge_ica_circuit_segments_non3phase.csv' (format csv, header true);
\copy sdge.ica_circuit_segments_3phase_generation_capacity to '/Users/edf/repos/carb_elec/dump/csv/sdge_ica_circuit_segments_3phase_generation_capacity.csv' (format csv, header true);
\copy sdge.ica_circuit_segments_3phase_load_capacity to '/Users/edf/repos/carb_elec/dump/csv/sdge_ica_circuit_segments_3phase_load_capacity.csv' (format csv, header true);
\copy sdge.lbna_ddor_candidate_area to '/Users/edf/repos/carb_elec/dump/csv/sdge_lbna_ddor_candidate_area.csv' (format csv, header true);
\copy sdge.substation_areas to '/Users/edf/repos/carb_elec/dump/csv/sdge_substation_areas.csv' (format csv, header true);
