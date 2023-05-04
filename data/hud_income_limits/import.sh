#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import Housing and Urban Development County Income Limits
#
# Creates tables:
# - hud.ca_2022_county_income_limits
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='hud'
src='./raw/'
out='./'

# Import tract level aac shapefile
file='2022-income-limits.csv'
table='ca_2022_county_income_limits'

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

# Export CSV table versions
psql -d carb -a -f 'export.sql'
