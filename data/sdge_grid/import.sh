#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

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

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='sdge'
src='./raw/'
out='./'

# Import GNA Area shapefile
file='GNA_Area.shp'
table='gna_area'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import DDOR Planned Area shapefile
file='LNBA_DDOR_Planned_Area.shp'
table='lnba_ddor_planned_area'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import ICA non-3Phase Circuit Segments shapefile
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

# Import ICA Generation Capacity shapefile
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

# Import ICA Load Capcity shapefile
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

# Import DDOR Candidate Area sahpefile
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

# Import Substation Areas shapefile
file='Substations.shp'
table='substation_areas'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Write table metadata outputs
table='gna_area'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='lnba_ddor_planned_area'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_circuit_segments_non3phase'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_circuit_segments_3phase_generation_capacity'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_circuit_segments_3phase_load_capacity'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='lbna_ddor_candidate_area'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='substation_areas'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
