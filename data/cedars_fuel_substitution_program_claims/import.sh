#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import CEDARS Fuel Substitution Program Claims
#
# Creates tables:
# - cedars.fuel_substitution_program_claims
#
################################################################################

# Set environment parameters
src='./'
out='./'
file='preprocess.py'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cedars'
table='fuel_substitution_program_claims'

# Preprocess input CEDARS data table
/opt/anaconda3/envs/geo/bin/python $src$file

# Output metadata to file
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Export CSV formatted tables
psql -d carb -a -f 'export.sql'
