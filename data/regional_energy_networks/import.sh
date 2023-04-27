#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

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

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='ren'
src='./raw/'
out='./'

# Import REN place designation table
file='ren_places.csv'
table='places'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import REN unincorporated area designation table
file='ren_unincorporated.csv'
table='unincorporated_areas'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import REN county designation table
file='ren_counties.csv'
table='counties'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Postprocess tables

table='all_merged'
psql -d carb -a -f '/Users/edf/repos/carb_elec/data/regional_energy_networks/postprocess.sql'

# Write table metadata outputs
table='places'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='unincorporated_areas'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='counties'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='all_merged'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
