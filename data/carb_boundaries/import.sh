#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

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
src='/Users/edf/repos/carb_elec/data/carb_boundaries/raw/'
out='/Users/edf/repos/carb_elec/data/carb_boundaries/'

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
psql -d carb -a -f '/Users/edf/repos/carb_elec/data/carb_boundaries/postprocess.sql'

# Write metadata
table='ca_air_districts'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_air_basins'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
