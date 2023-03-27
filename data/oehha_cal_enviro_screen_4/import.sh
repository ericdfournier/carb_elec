#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import CARB Priority Populations
#
# Creates tables:
# - oehha.ces4
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='oehha'
src='/Users/edf/repos/carb_elec/data/oehha_cal_enviro_screen_4/raw/'
out='/Users/edf/repos/carb_elec/data/oehha_cal_enviro_screen_4/'
gdb='calenviroscreen40gdb_F_2021.gdb'
feature='CES4_final'
table='ces4'

ogr2ogr -f $format $dst \
    $src$gdb \
    $feature \
    -lco SCHEMA=$schema \
    -nln $table  \
    -nlt MULTISURFACE \
    -t_srs EPSG:3310 \
    -lco GEOMETRY_NAME=geom \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
