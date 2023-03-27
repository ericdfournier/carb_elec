#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import CEC Building Climate Zones
#
# Creates tables:
# - cec.building_climate_zones_2021
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cec'
src='/Users/edf/repos/carb_elec/data/cec_climate_zones/raw/'
out='/Users/edf/repos/carb_elec/data/cec_climate_zones/'
file='ca_building_climate_zones.geojson'
table='ca_building_climate_zones_2021'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
