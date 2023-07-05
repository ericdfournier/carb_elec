#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import CEC Utility Service Territory Boundaries
#
# Creates tables:
# - cec.ca_electric_load_serving_entities_2022
# - cec.ca_electric_utilities_2022
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cec'
src='./raw/'
out='./'

# Read load serving entitie service territory shapefile
file='electric_load_serving_entity_territories.shp'
table='ca_electric_load_serving_entities_2022'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -select 'id,OBJECTID,Acronym,Utility,Type,URL,Phone,Address,HIFLD_ID' \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Read utility service territory shapefile
file='electric_utility_service_territories.shp'
table='ca_electric_utilities_2022'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -select 'id,OBJECTID,Acronym,Utility,Type,URL,Phone,Address,HIFLD_ID' \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Write table metadata outputs
table='ca_electric_load_serving_entities_2022'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Write table metadata outputs
table='ca_electric_utilities_2022'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Export CSV formatted tables
psql -d carb -a -f 'export.sql'
