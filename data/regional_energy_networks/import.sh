#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# California Regional Energy Networks
#
# Creates tables:
# - ren.places
# - ren.unincorporated_areas
# - ren.counties
# - ren.all_merged
#
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='ren'
src='/Users/edf/repos/carb_elec/data/regional_energy_networks/raw/'
out='/Users/edf/repos/carb_elec/data/regional_energy_networks/'

file='ren_places.csv'
table='places'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='ren_unincorporated.csv'
table='unincorporated_areas'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='ren_counties.csv'
table='counties'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Postprocess tables

table='all_merged'

psql -d carb -a -f '/Users/edf/repos/carb_elec/data/regional_energy_networks/postprocess.sql'

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
