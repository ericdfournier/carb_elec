#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import CPUC Utility Affordability Metrics
#
# Creates tables:
# - cpuc.2020_aac_tract
# - cpuc.2020_electric_aac_tract
# - cpuc.2020_gas_aac_tract
# - cpuc.2020_ar_puma
# - cpuc.2020_electric_ar_puma
# - cpcu.2020_gas_ar_puma
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cpuc'
src='/Users/edf/repos/carb_elec/data/cpuc_utility_affordability_ratios/raw/'
out='/Users/edf/repos/carb_elec/data/cpuc_utility_affordability_ratios/'
file='Tract_AAC_2020_20220718.shp'
table='2020_aac_tract'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='2020_Electric_AAC_Results.csv'
table='2020_electric_aac_tract'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='2020_Gas_AAC_Results.csv'
table='2020_gas_aac_tract'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    -oo AUTODETECT_TYPE=YES \
    -oo AUTODETECT_SIZE_LIMIT=0 \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='PUMA_AR.shp'
table='2020_ar_puma'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='Electric_PUMA_AR2020.shp'
table='2020_electric_ar_puma'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='Gas_PUMA_AR2020.shp'
table='2020_gas_ar_puma'

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

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
