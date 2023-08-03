#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import USEPA EJ Screen Tract Level Data
#
# Creates tables:
# - usepa.ej_screen_ca_2023_tr
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='usepa'
src='./raw/'
out='./'

# Import climate zone table
file='EJScreen_CA.geojson'
table='ej_screen_ca_2023_tr'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt PROMOTE_TO_MULTI \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Write table metadata outputs
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Export CSV formatted tables
# psql -d carb -a -f 'export.sql'
