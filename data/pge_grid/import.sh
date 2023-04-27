#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

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

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='pge'
src='./raw/'
out='./'
gdb='ICADisplay.gdb'

# Import Feeder Circuit Details from PGE Grid Geodatabase
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

# Import Feeder Load Profiles from PGE Grid Geodatabase
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

# Import ICA Not Available Layer from PGE Grid Geodatabase
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

# Import Line Details from PGE Grid Geodatabase
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

# Import Substations from PGE Grid Geodatabase
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

# Import Substation Load Profiles from PGE Grid Geodatabase
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

# Import Transmission Lines from PGE Grid Geodatabase
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

# Write table metadata outputs
table='ica_feeder_detail'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_feeder_load_profile'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_feeder_not_available'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_line_detail'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_substation'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_substation_load_profile'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ica_transmission_line'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
