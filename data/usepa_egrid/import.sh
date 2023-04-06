#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import USEPA eGRID Attributes
#
# Creates tables:
# - usepa.ba_2021
# - usepa.demo_2021
# - usepa.gen_2021
# - usepa.ggl_2021
# - usepa.nrl_2021
# - usepa.plnt_2021
# - usepa.srl_2021
# - usepa.st_2021
# - usepa.unt_2021
# - usepa.us_2021
#
################################################################################

src='/Users/edf/repos/carb_elec/data/usepa_egrid/'
file='preprocess.py'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='usepa'
tables=('ba_2021'
    'demo_2021'
    'gen_2021'
    'ggl_2021'
    'nrl_2021'
    'plnt_2021'
    'srl_2021'
    'st_2021'
    'unt_2021'
    'us_2021' )

/opt/anaconda3/envs/geo/bin/python $src$file

for table in "${tables[@]}"
do
    ogrinfo -so -ro $dst $schema.$table > $src$table'_ogrinfo.txt'
done
