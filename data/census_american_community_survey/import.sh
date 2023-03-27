#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

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
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

src='/Users/edf/repos/carb_elec/data/census_american_community_survey/'
file='download.py'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='census'
tables=('acs_ca_2019_tr_population'
    'acs_ca_2019_tr_income'
    'acs_ca_2019_tr_housing'
    'acs_ca_2019_tr_fuel'
    'acs_ca_2019_tr_metadata'
    'acs_ca_2019_tr_geom'
    'acs_ca_2019_puma_geom'
    'acs_ca_2019_county_geom' )

/opt/anaconda3/envs/geo/bin/python $src$file

for table in "${tables[@]}"
do
    ogrinfo -so -ro $dst $schema.$table > $src$table'_ogrinfo.txt'
done
