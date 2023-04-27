#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import Census Attributes and Geometries
#
# Creates tables:
# - census.acs_ca_2019_tr_population
# - census.acs_ca_2019_tr_income
# - census.acs_ca_2019_tr_housing
# - census.acs_ca_2019_tr_fuel
# - census.acs_ca_2019_tr_metadata
# - census.acs_ca_2019_tr_geom
# - census.acs_ca_2019_puma_geom
# - census.acs_ca_2019_county_geom
# - census.acs_ca_2019_unincorporated_geom (Note: Computed as symmetric
#   difference of the county and place geometry layers)
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
src='./'
file='download.py'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='census'
tables=('acs_ca_2019_tr_population'
    'acs_ca_2019_tr_income'
    'acs_ca_2019_tr_housing'
    'acs_ca_2019_tr_fuel'
    'acs_ca_2019_tr_metadata'
    'acs_ca_2019_tr_geom'
    'acs_ca_2019_place_geom'
    'acs_ca_2019_puma_geom'
    'acs_ca_2019_county_geom' )


# Download data via python Census API
/opt/anaconda3/envs/geo/bin/python $src$file

# Write table metadata outputs
for table in "${tables[@]}"
do
    ogrinfo -so -ro $dst $schema.$table > $src$table'_ogrinfo.txt'
done

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='census'
src='./raw/'
out='./'

# Import to unincorporated geometry table
file='acs_ca_2019_unincorporated_geom.geojson'
table='acs_ca_2019_unincorporated_geom'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Postprocess tables
psql -d carb -a -f 'postprocess.sql'

# Output Metadata
table='acs_ca_2019_unincorporated_geom'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
