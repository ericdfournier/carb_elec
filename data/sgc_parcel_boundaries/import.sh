#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import California Statewide Parcel Boundaries
#
# Database: carb
#
# Creates tables:
# - sgc.ca_parcel_boundaries_2014
# - sgc.ca_parcel_boundaries_2014_info
#
# Imports CA_PARCELS_STATEWIDE_INFO layer from geodatabase using the OpenFileGDB (ESRI File Geodatabase) driver.
# Coordinates are already in EPSG:3310 (NAD83 / California Albers) SRS.
#
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='sgc'
src='./raw/Parcels_CA_2014.gdb'
out='./'

layer='CA_PARCELS_STATEWIDE'
table='ca_parcel_boundaries_2014'

ogr2ogr -f $format $dst \
    $src \
    $layer \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt CONVERT_TO_CURVE \
    -dim XY \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    --debug ON

layer='CA_PARCELS_STATEWIDE_INFO'
table='ca_parcel_boundaries_2014_info'

ogr2ogr -f $format $dst \
    $src \
    $layer \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    --debug ON

# Perform additional postprocessing on permit records
psql -d carb -a -f 'postprocess.sql'

# Write table metadata output
table='ca_parcel_boundaries_2014'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_parcel_boundaries_2014_info'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
