#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import PGE Grid Data
#
# Creates tables:
# - pge.ica_feeder_detail
# - pge.ica_feeder_load_profile
# - pge.ica_feeder_not_available
# - pge.ica_line_detail
# - pge.ica_substation_load_profile
# - pge.ica_substation
# - pge.ica_tranmission_line
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='pge'
src='/Users/edf/repos/carb_elec/data/pge_grid/raw/'
out='/Users/edf/repos/carb_elec/data/pge_grid/'
gdb='ICADisplay.gdb'
feature='FeederDetail'
table='ica_feeder_detail'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTILINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

feature='FeederLoadProfile'
table='ica_feeder_load_profile'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

feature='ICANotAvailable'
table='ica_feeder_not_available'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTILINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

feature='LineDetail'
table='ica_line_detail'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTILINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

feature='Substations'
table='ica_substation'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt POINT \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

feature='SubstationLoadProfile'
table='ica_substation_load_profile'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

feature='TransmissionLines'
table='ica_transmission_line'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTILINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
