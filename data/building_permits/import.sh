#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

################################################################################
# Import building permit data
#
# Database: carb
#
# Creates tables: permits.permit_processing_combined
################################################################################

format='PostgreSQL'
pgdatabase='carb'
dst="postgresql://$PGUSER@$PGHOST/$pgdatabase"
schema='permits'

src='./raw'

table=permit_processing_combined

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

# Postprocessing using "here document".
# Tabs (not spaces) must be used to indent here documents with <<- redirection operator.
psql -d $pgdatabase <<-EOF
	-- Drop unnecessary columns.
	alter table $schema.$table
		drop ogc_fid,
		drop field_1;

	-- Add column for centroid in NAD83 / California Albers.
	alter table $schema.$table
		add centroid geometry(POINT, 3310);

	-- Set centroid values, ignore those outside of WGS84 bounds.
	update $schema.$table
		set centroid = ST_Transform(centroid_4326, 3310)
		where
			ST_X(centroid_4326) >= -180
			and ST_X(centroid_4326) <= 180
			and ST_Y(centroid_4326) >= -90
			and ST_Y(centroid_4326) <= 90;

	-- Create spatial index on centroid.
	create index on $schema.$table using gist (centroid);
EOF
