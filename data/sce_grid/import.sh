#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import SCE Grid Data
#
# Creates tables:
# - sce.ica_circuit_segments_3phase
# - sce.ica_circuit_segments_non3phase
# - sce.ram_circuits
# - sce.service_territory
# - sce.substations
# - sce.transmission_circuits
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='sce'
src='./raw/'
out='./'

# Import ICA 3Phase circuit segments from SCE Geodatabase
file='ica_circuit_segments_3phase.shp'
table='ica_circuit_segments_3phase'

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

# Import ICA non-3Phase circuit segmenets from SCE Geodatabase
file='ica_circuit_segments_non3phase.shp'
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

# Import RAM Circuits from SCE Geodatabase
file='ram_circuits.shp'
table='ram_circuits'

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

# Import Service Territory from SCE Geodatabase
file='service_territory.shp'
table='service_territory'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -lco precision=NO \
    --debug ON

# Import Substations from SCE Geodatabase
file='substations.shp'
table='substations'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt POINT \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import Transmission Circuits from SCE Geodatabase
file='transmission_circuits.shp'
table='transmission_circuits'

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

# Postprocess tables
psql -d carb -a -f 'postprocess.sql'

# Write table metadata outputs
table='ica_circuit_segments_3phase'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_circuit_segments_non3phase'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ram_circuits'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='service_territory'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='substations'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='transmission_circuits'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
