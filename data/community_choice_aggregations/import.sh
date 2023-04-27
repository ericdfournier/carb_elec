#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# California Community Choice Aggregations
#
# Creates tables:
# - cca.places
# - cca.unincorporated_areas
# - cca.counties
# - cca.all_merged
#
################################################################################

# Set environment parameters
format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
schema='cca'
src='./raw/'
out='./'

# Import cca places list
file='cca_places.csv'
table='places'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import cca unincorporate area list
file='cca_unincorporated.csv'
table='unincorporated_areas'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Import cca counties list
file='cca_counties.csv'
table='counties'

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Postprocess tables
psql -d carb -a -f 'postprocess.sql'

# Write table metadata outputs
table='places'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='unincorporated_areas'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='counties'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

table='all_merged'
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
