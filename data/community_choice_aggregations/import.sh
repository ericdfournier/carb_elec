#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# California Community Choice Aggregations
#
# Creates tables:
# - cca.places
# - cca.unincorporated_areas
# - cca.counties
# - cca.all_merged
#
# Converts SRS to EPSG:3310 (NAD83 / California Albers).
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cca'
src='/Users/edf/repos/carb_elec/data/community_choice_aggregations/raw/'
out='/Users/edf/repos/carb_elec/data/community_choice_aggregations/'
file='cca_places.csv'
table='places'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='cca_unincorporated.csv'
table='unincorporated_areas'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

file='cca_counties.csv'
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

psql -d carb -a -f '/Users/edf/repos/carb_elec/data/community_choice_aggregations/postprocess.sql'

ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
