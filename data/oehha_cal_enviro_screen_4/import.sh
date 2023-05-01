#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import CARB Priority Populations
#
# Creates tables:
# - oehha.ces4
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='oehha'
src='./raw/'
out='./'
gdb='calenviroscreen40gdb_F_2021.gdb'

# Import CES Geodatabase
feature='CES4_final'
table='ca_ces4'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Write table metadata outputs
table='ca_ces4'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Export CSV table versions
psql -d carb -a -f 'export.sql'
