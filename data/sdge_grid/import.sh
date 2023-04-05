#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import SDGE Grid Data
#
# Creates tables:
# - sdge.lnba_ddor_planned_area
# - sdge.ica_circuit_segments_non3phase
# - sdge.ica_circuit_segments_3phase_generation_capacity
# - sdge.ica_circuit_segments_3phase_load_capacity
# - sdge.lbna_ddor_candidate_area
# - sdge.substation_areas
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='sdge'
src='/Users/edf/repos/carb_elec/data/sdge_grid/raw/'
out='/Users/edf/repos/carb_elec/data/sdge_grid/'
file='GNA_Area.shp'
table='gna_area'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='LNBA_DDOR_Planned_Area.shp'
table='lnba_ddor_planned_area'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='non3ph_circuit_segment.shp'
table='ica_circuit_segments_non3phase'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTILINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='Generation_Capacity_MW_(ICA).shp'
table='ica_circuit_segments_3phase_generation_capacity'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTILINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='Load_Capacity_MW_(LCA).shp'
table='ica_circuit_segments_3phase_load_capacity'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTILINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='LNBA_DDOR_Candidate_Area.shp'
table='lbna_ddor_candidate_area'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='Substations.shp'
table='substation_areas'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
