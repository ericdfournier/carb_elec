-- Stop processing if an error occurs.
\set ON_ERROR_STOP on

/*==============================================================================
 * Export tables:
# - sce.ica_circuit_segments_3phase
# - sce.ica_circuit_segments_non3phase
# - sce.ram_circuits
# - sce.service_territory
# - sce.substations
# - sce.transmission_circuits
#
 * Warning: COPY TO (and \copy to) will overwrite existing files.
==============================================================================*/

\copy sce.ica_circuit_segments_3phase to '/Users/edf/repos/carb_elec/dump/csv/sce_ica_circuit_segments_3phase.csv' (format csv, header true);
\copy sce.ica_circuit_segments_non3phase to '/Users/edf/repos/carb_elec/dump/csv/sce_ica_circuit_segments_non3phase.csv' (format csv, header true);
\copy sce.ram_circuits to '/Users/edf/repos/carb_elec/dump/csv/sce_ram_circuits.csv' (format csv, header true);
\copy sce.service_territory to '/Users/edf/repos/carb_elec/dump/csv/sce_service_territory.csv' (format csv, header true);
\copy sce.substations to '/Users/edf/repos/carb_elec/dump/csv/sce_substations.csv' (format csv, header true);
\copy sce.transmission_circuits to '/Users/edf/repos/carb_elec/dump/csv/sce_transmission_circuits.csv' (format csv, header true);
