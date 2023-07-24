#!/usr/bin/env bash
set -ue  # Set nounset and errexit Bash shell attributes.

# Set working directory
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $dir

################################################################################
# Import STRM Digital Elevation Model Raster Data Layers
#
# Database: carb
#
# Creates tables:
# - srtm.ca_elevation
# - srtm.ca_slope
#
# Inpnut GeoTIFF is already in EPSG:3310 (NAD83 / California Albers) SRS.
#
################################################################################

format='PostgreSQL'
dst="postgresql://$PGUSER@$PGHOST/carb"
dbase='carb'
schema='srtm'
out='./'

# Set elevation raster parameters
src='./raw/ca_elevation.tif'
table='ca_elevation'

# Import elevation raster geotiff
raster2pgsql -s 3310 -I -e -M $src -F -t 100x100 $schema.$table | psql -d $dbase

# Write table metadata output
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'

# Set slope raster parameters
src='./raw/ca_slope.tif'
table='ca_slope'

# Import slope raster geotiff
raster2pgsql -s 3310 -I -e -M $src -F -t 100x100 $schema.$table | psql -d $dbase

# Write table metadata output
ogrinfo -so -ro $dst $schema.$table > $out$table'_orginfo.txt'
