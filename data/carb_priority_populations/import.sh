#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import CARB Priority Populations
#
# Creates tables:
# - carb.priority_populations_ces4
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='carb'
src='/Users/edf/repos/carb_elec/data/carb_priority_populations/raw/'
out='/Users/edf/repos/carb_elec/data/carb_priority_populations/'
gdb='PriorityPopulationsCES4.gdb'
feature='PriorityPopulationsCES4'
table='priority_populations_ces4'

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
