#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import USEPA eGRID Attributes
#
# Creates tables:
# - usepa.egrid_ba_2021
# - usepa.egrid_demo_2021
# - usepa.egrid_gen_2021
# - usepa.egrid_ggl_2021
# - usepa.egrid_nrl_2021
# - usepa.egrid_plnt_2021
# - usepa.egrid_srl_2021
# - usepa.egrid_st_2021
# - usepa.egrid_unt_2021
# - usepa.egrid_us_2021
#
################################################################################

# Set environment parameters
file='preprocess.py'
pgdatabase='carb'
dst="postgresql://$PGUSER@$PGHOST/$pgdatabase"
schema='usepa'
src='./raw/'
out='./'

# Run preprocessing/import python script
/opt/anaconda3/envs/geo/bin/python $file

# Write table metadata outputs
tables=('egrid_ba_2021'
    'egrid_demo_2021'
    'egrid_gen_2021'
    'egrid_ggl_2021'
    'egrid_nrl_2021'
    'egrid_plnt_2021'
    'egrid_srl_2021'
    'egrid_st_2021'
    'egrid_unt_2021'
    'egrid_us_2021' )

for table in "${tables[@]}"
do
    ogrinfo -so -ro $dst $schema.$table > $src$table'_ogrinfo.txt'
done

# Export CSV table versions
psql -d carb -a -f 'export.sql'
