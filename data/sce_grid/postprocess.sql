-- Rename Truncated Fields in 3Phase Circuit Table from Imported Shapefile

ALTER TABLE sce.ica_circuit_segments_3phase RENAME circuit_vo TO circuit_voltage;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME system_nam TO system_name;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME uniform_ge TO uniform_generation;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME ica_overal TO ica_overall_pv;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME ica_over_1 TO ica_overall_load;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME ica_over_2 TO ica_overall_op_flex;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME line_segme TO line_segment_id;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME download_l TO download_link;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME uniform__1 TO uniform_generation_pv_op_flex;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME substati_1 TO substation_voltage;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME circuit_na TO circuit_name;
ALTER TABLE sce.ica_circuit_segments_3phase RENAME shape__len TO shape_length;

-- Rename Truncated Fields in Non3Phase Circuit Table from Imported Shapefile

ALTER TABLE sce.ica_circuit_segments_non3phase RENAME circuit_vo TO circuit_voltage;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME system_nam TO system_name;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME uniform_ge TO uniform_generation;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME ica_overal TO ica_overall_pv;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME ica_over_1 TO ica_overall_load;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME ica_over_2 TO ica_overall_op_flex;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME line_segme TO line_segment_id;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME download_l TO download_link;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME uniform__1 TO uniform_generation_pv_op_flex;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME substati_1 TO substation_voltage;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME circuit_na TO circuit_name;
ALTER TABLE sce.ica_circuit_segments_non3phase RENAME shape__len TO shape_length;

-- Rename Truncated Fields in Ram Circuit Table from Imported Shapefile

ALTER TABLE sce.ram_circuits RENAME substation TO substation_voltage;
ALTER TABLE sce.ram_circuits RENAME sys_name TO system_name;
ALTER TABLE sce.ram_circuits RENAME existing_g TO existing_generation;
ALTER TABLE sce.ram_circuits RENAME queued_gen TO queued_generation;
ALTER TABLE sce.ram_circuits RENAME total_gen TO total_generation;
ALTER TABLE sce.ram_circuits RENAME projected_ TO projected_load;
ALTER TABLE sce.ram_circuits RENAME penetratio TO penetration;
ALTER TABLE sce.ram_circuits RENAME max_remain TO max_remaining_capacity;
ALTER TABLE sce.ram_circuits RENAME percent_15 TO percent_15_penetration;
ALTER TABLE sce.ram_circuits RENAME circuit_na TO circuit_name;
ALTER TABLE sce.ram_circuits RENAME circuit_vo TO circuit_voltage;
ALTER TABLE sce.ram_circuits RENAME sub_name TO substation_name;

-- Rename Truncated Fields in Service Territory Table from Imported Shapefile

ALTER TABLE sce.service_territory RENAME existing_g TO existing_generation;
ALTER TABLE sce.service_territory RENAME queued_gen TO queued_generation;
ALTER TABLE sce.service_territory RENAME total_gen TO total_generation;
ALTER TABLE sce.service_territory RENAME projected_ TO projected_load;
ALTER TABLE sce.service_territory RENAME penetratio TO penetration;

-- Rename Trucated Fields in Substations Table from Imported Shapefile

ALTER TABLE sce.substations RENAME subst_id TO substation_id;
ALTER TABLE sce.substations RENAME sub_name TO substation_name;
ALTER TABLE sce.substations RENAME sys_name TO system_name;
ALTER TABLE sce.substations RENAME sub_type TO substation_type;
ALTER TABLE sce.substations RENAME substation TO substation_voltage;
ALTER TABLE sce.substations RENAME existing_g TO existing_generation;
ALTER TABLE sce.substations RENAME queued_gen TO queued_generation;
ALTER TABLE sce.substations RENAME total_gen TO total_generation;
ALTER TABLE sce.substations RENAME projected_ TO projected_load;
ALTER TABLE sce.substations RENAME penetratio TO penetration;
ALTER TABLE sce.substations RENAME max_remain TO max_remaining_capacity;

-- Rename Truncated Fields in Transmission Circuits Table from Imported Shapefile

ALTER TABLE sce.transmission_circuits RENAME circuit_no TO circuit_number;
ALTER TABLE sce.transmission_circuits RENAME circuit_ty TO circuit_type;
ALTER TABLE sce.transmission_circuits RENAME circuit_vo TO circuit_voltage;
