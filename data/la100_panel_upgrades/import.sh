#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import USEPA eGRID Attributes
#
# Creates tables:
# - la100.sf_training
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
pgdatabase='carb'
dst="postgresql://$PGUSER@$PGHOST/$pgdatabase"
schema='la100'
src='./raw/'
out='./'

# Import la100 panel upgrade training data table
file='la100es_sf_electricity_service_panel_capacity_analysis_2023-07-31.geojson'
table='sf_training'

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
