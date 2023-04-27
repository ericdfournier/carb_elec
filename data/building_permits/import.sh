#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import DOE Lead Tool Data
#
# Creates tables:
# - permits.raw
#
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='permits'
src='./raw/'
out='./'

# Import raw permit data table
file='raw_permit_data.csv'
table='raw'

ogr2ogr -f $format $dst \
    $src$file\
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Write table metadata output
table='raw'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
