#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import CPUC Public Safety Power Shutoff Historical Circuit Level Outage Data
#
# Creates tables:
# - cpuc.psps_outages_2013_2023
#
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cpuc'
src='./raw/'
out='./'

# Import circuit level grid outage data
file='cpuc_psps_2013_2023.csv'
table='psps_outages_2013_2023'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

# Write table metadata outputs
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Postprocess imported database table
psql -d carb -a -f 'postprocess.sql'

# Export CSV table versions
psql -d carb -a -f 'export.sql'
