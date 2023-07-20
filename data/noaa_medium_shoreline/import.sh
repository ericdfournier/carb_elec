#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import NOAA Medium Shoreline Boundaries for the Continental United States
#
# Creates tables:
# - noaa.us_medium_shoreline
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='noaa'
src='./raw/'
out='./'

# Import medium resolution shoreline boundary shapefile
file='us_medium_shoreline.shp'
table='us_medium_shoreline'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt LINESTRING \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -unsetFieldWidth \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Write table metadata outputs
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Export CSV table versions
psql -d carb -a -f 'export.sql'
