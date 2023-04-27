#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import CARB Air Quality Management Boundaries
#
# Creates tables:
# - carb.ca_air_basins
# - carb.ca_air_districts
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='carb'
src='./raw/'
out='./'

# Import air basins table
file='CaAirBasin.shp'
table='ca_air_basins'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -unsetFieldWidth \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import air districts table
file='CaAirDistrict.shp'
table='ca_air_districts'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -unsetFieldWidth \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Postprocess tables
psql -d carb -a -f 'postprocess.sql'

# Write table metadata output
table='ca_air_districts'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_air_basins'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
