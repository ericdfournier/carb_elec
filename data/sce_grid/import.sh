#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

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

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='sce'
src='/Users/edf/repos/carb_elec/data/sce_grid/raw/'
out='/Users/edf/repos/carb_elec/data/sce_grid/'
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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='service_territory.shp'
table='service_territory'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -lco precision=NO \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Postprocess tables

psql -d carb -a -f '/Users/edf/repos/carb_elec/data/sce_grid/postprocess.sql'
