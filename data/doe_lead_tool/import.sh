#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

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

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='doe'
src='./raw/'
out='./'

# Import CA census tract level ami data table
file='CA_AMI_Census_Tracts_2018.csv'
table='ca_ami_census_tracts_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -lco COLUMN_TYPES='units=float,hincp*units=float,elep*units=float,gasp*units=float,fulp*units=float,hincp units=float,elep units=float,gasp units=float,fulp units=float,hcount=float,ecount=float,gcount=float,fcount=float,hincp=float,elep=float,gasp=float,fulp=float' \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import CA county and city level ami data table
file='CA_AMI_State_Counties_Cities_2018.csv'
table='ca_ami_state_counties_cities_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -lco COLUMN_TYPES='units=float,hincp*units=float,elep*units=float,gasp*units=float,fulp*units=float,hincp units=float,elep units=float,gasp units=float,fulp units=float,hcount=float,ecount=float,gcount=float,fcount=float,hincp=float,elep=float,gasp=float,fulp=float' \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import census tract level fpl data table
file='CA_FPL_Census_Tracts_2018.csv'
table='ca_fpl_census_tracts_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -lco COLUMN_TYPES='units=float,hincp*units=float,elep*units=float,gasp*units=float,fulp*units=float,hincp units=float,elep units=float,gasp units=float,fulp units=float,hcount=float,ecount=float,gcount=float,fcount=float,hincp=float,elep=float,gasp=float,fulp=float' \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import county and city level fpl data table
file='CA_FPL_State_Counties_Cities_2018.csv'
table='ca_fpl_state_counties_cities_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -lco COLUMN_TYPES='units=float,hincp*units=float,elep*units=float,gasp*units=float,fulp*units=float,hincp units=float,elep units=float,gasp units=float,fulp units=float,hcount=float,ecount=float,gcount=float,fcount=float,hincp=float,elep=float,gasp=float,fulp=float' \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import census tract level smi data table
file='CA_SMI_Census_Tracts_2018.csv'
table='ca_smi_census_tracts_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -lco COLUMN_TYPES='units=float,hincp*units=float,elep*units=float,gasp*units=float,fulp*units=float,hincp units=float,elep units=float,gasp units=float,fulp units=float,hcount=float,ecount=float,gcount=float,fcount=float,hincp=float,elep=float,gasp=float,fulp=float' \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import county and city level smi data table
file='CA_SMI_State_Counties_Cities_2018.csv'
table='ca_smi_state_counties_cities_2018'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -lco COLUMN_TYPES='units=float,hincp*units=float,elep*units=float,gasp*units=float,fulp*units=float,hincp units=float,elep units=float,gasp units=float,fulp units=float,hcount=float,ecount=float,gcount=float,fcount=float,hincp=float,elep=float,gasp=float,fulp=float' \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Write table metadata outputs
table='ca_ami_census_tracts_2018'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_ami_state_counties_cities_2018'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_fpl_census_tracts_2018'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_fpl_state_counties_cities_2018'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_smi_census_tracts_2018'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_smi_state_counties_cities_2018'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Export CSV table versions
psql -d carb -a -f 'export.sql'
