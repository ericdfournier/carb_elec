#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import DOE Lead Tool Data
#
# Creates tables:
# - doe.ca_ami_census_tracts_2018
# - doe.ca_ami_state_counties_cities_2018
# - doe.ca_fpl_census_tracts_2018
# - doe.ca_fpl_state_counties_cities_2018
# - doe.ca_smi_census_tracts_2018
# - doe.ca_smi_state_counties_cities_2018
#
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='doe'
src='/Users/edf/repos/carb_elec/data/doe_lead_tool/raw/'
out='/Users/edf/repos/carb_elec/data/doe_lead_tool/'

file='CA_AMI_Census_Tracts_2018.csv'
table='ca_ami_census_tracts_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='CA_AMI_State_Counties_Cities_2018.csv'
table='ca_ami_state_counties_cities_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='CA_FPL_Census_Tracts_2018.csv'
table='ca_fpl_census_tracts_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='CA_FPL_State_Counties_Cities_2018.csv'
table='ca_fpl_state_counties_cities_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='CA_SMI_Census_Tracts_2018.csv'
table='ca_smi_census_tracts_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='CA_SMI_State_Counties_Cities_2018.csv'
table='ca_smi_state_counties_cities_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
