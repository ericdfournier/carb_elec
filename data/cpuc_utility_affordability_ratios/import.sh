#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import CPUC Utility Affordability Metrics
#
# Creates tables:
# - cpuc.ca_2020_aac_tract
# - cpuc.ca_2020_electric_aac_tract
# - cpuc.ca_2020_gas_aac_tract
# - cpuc.ca_2020_ar_puma
# - cpuc.ca_2020_electric_ar_puma
# - cpcu.ca_2020_gas_ar_puma
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cpuc'
src='./raw/'
out='./'

# Import tract level aac shapefile
file='Tract_AAC_2020_20220718.shp'
table='ca_2020_aac_tract'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

# Import tract level electric aac results data table
file='2020_Electric_AAC_Results.csv'
table='ca_2020_electric_aac_tract'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

# Import tract level gas aac results data table
file='2020_Gas_AAC_Results.csv'
table='ca_2020_gas_aac_tract'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

# Import puma level ar shapefile
file='PUMA_AR.shp'
table='ca_2020_ar_puma'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

# Import puma level eletric ar shapefile
file='Electric_PUMA_AR2020.shp'
table='ca_2020_electric_ar_puma'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

# Import puma level gas ar shapefile
file='Gas_PUMA_AR2020.shp'
table='ca_2020_gas_ar_puma'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table \
    -nlt MULTIPOLYGON \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

# Write table metadata outputs
table='ca_2020_aac_tract'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_2020_electric_aac_tract'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_2020_gas_aac_tract'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_2020_ar_puma'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_2020_electric_ar_puma'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='ca_2020_gas_ar_puma'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Export CSV table versions
psql -d carb -a -f 'export.sql'
