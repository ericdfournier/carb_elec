#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import building permit data
#
# Database: carb
#
# Creates tables:
# - permits.class_definitions
# - permits.combined
# - permits.panel_upgrades
# - permits.panel_upgrades_geocode_arcgis
# - permits.panel_upgrades_geocoded
# - permits.panel_upgrades_geocoded_geographies
# - permits.sampled_counties
# - permits.sampled_places
# - permits.sampled_territories
#
################################################################################

format='PostgreSQL'
pgdatabase='carb'
dst="postgresql://$PGUSER@$PGHOST/$pgdatabase"
out='./'
schema='permits'

src='./raw/permits/'
table=combined

# For a directory to be recognized as a CSV datasource at least half the files in the directory need to have a .csv extension.
# Use -nln $schema.$table to specify the destination table/layer since it does not seem possible
# to append to an existing table when specifying the schema with -lco SCHEMA=$schema, for reasons
# including the fact that -lco options are ignored when appending to an existing layer
# (in spite of this, subsequent files still write to the correct geometry column).
# Setting -doo ACTIVE_SCHEMA=$schema may be another alternative to set the destination schema.
# The -update and -append options are included for clarity but have no tangible effect with Postgres destinations.
# Using --config PG_USE_COPY YES may increase speed of import into existing tables.
ogr2ogr \
	-update \
	-append \
	-f $format $dst \
	$src \
	-nln $schema.$table \
	-emptyStrAsNull \
	-oo X_POSSIBLE_NAMES=longitude \
	-oo Y_POSSIBLE_NAMES=latitude \
	-oo KEEP_GEOM_COLUMNS=NO \
	-a_srs EPSG:4326 \
	-lco GEOMETRY_NAME=centroid_4326 \
	-lco COLUMN_TYPES='estimated_cost=money,applied_date=date,issued_date=date,finaled_date=date' \
	-lco DESCRIPTION="$(date +'%Y-%m-%d') - $(basename $src)" \
	--config PG_USE_COPY YES \
	--debug ON

# Import derived permit class definitions
src='./raw/'
file='class_definitions.csv'
table=class_definitions

ogr2ogr -f $format $dst \
    $src$file \
    -lco SCHEMA=$schema \
    -nln $table  \
    -emptyStrAsNull \
    -lco DESCRIPTION=$table \
    --debug ON

# Perform additional postprocessing on permit records
psql -d carb -a -f 'import_postprocess.sql'

# Modify table records in anticipation of geocoding workflow
psql -d carb -a -f 'geocode_preprocess.sql'

# Geocode from external service and write table back to database
file='geocode.py'
/opt/anaconda3/envs/geo/bin/python $file

# Geocode postprocess
psql -d carb -a -f 'geocode_postprocess.sql'

# Write class definition table metadata output
table="class_definitions"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write combined raw data table metadata output
table="combined"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write panel upgrade permit data table metadata output
table="panel_upgrades"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write panel upgrade arcgis geocoder input table metadata output
table="panel_upgrades_geocode_arcgis"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write panel upgrade arcgis geocoder input table metadata output
table="panel_upgrades_geocoded"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write panel upgrade geocoded geographies table metadata output
table="panel_upgrades_geocoded_geographies"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write sampled counties table metadata output
table="sampled_counties"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write sampled places table metadata output
table="sampled_places"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Write sampled territories table metadata output
table="sampled_territories"
ogrinfo -so -ro $dst $schema.$table > $out$table'_ogrinfo.txt'

# Export CSV Formatted Tables
psql -d carb -a -f 'export.sql'
