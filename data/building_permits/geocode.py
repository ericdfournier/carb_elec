#!/usr/bin/env python3

"""Geocode ladwp electricity premises 2017-2021 data

Source table: accounts.ladwp_electricity_premises_2017_2021

Create table: accounts.ladwp_electricity_premises_2017_2021_geocode_arcgis

Geocodes with the ArcGIS geocoding service (findAddressCandidates) using geopy.

The required packages must be installed in the executing Python environment.

This script assumes that Postgres default connection parameters have been set
using the PGHOST and PGUSER environment variables.
"""

__author__ = 'Eric D Fournier'

#%% Imports.

import functools  # For partial function.
import json
import os
import numpy as np

from sqlalchemy import create_engine
#from geoalchemy2 import Geometry  # Enable PostGIS support.

import geopy.geocoders  # For access to options object.
from geopy.geocoders import ArcGIS
from geopy.extra.rate_limiter import RateLimiter

import pandas as pd
import geopandas as gpd

from tqdm import tqdm
tqdm.pandas()  # Enable the use of progress_apply().

#%% Set session variables

# Set database connection parameters from environment variables. Will raise KeyError if not set.
user = os.environ['PGUSER']
password = 'VSWYFW66' #os.environ['PGPASSWORD']
host = os.environ['PGHOST']
port = os.environ['PGPORT']
database = 'carb'
dst_schema = 'permits'
dst_table = 'panel_upgrades_geocode_arcgis'

#%% Set geocoder optional parameters
# Choose if existing table should be overwritten via if_exists parameter to geopandas.to_postgis().
# Options 'fail' (default), 'replace', or 'append'.
if_exists = 'fail'

# Choose verbosity via echo parameter to sqlalchemy.create_engine().
# Option True to echo query or 'debug' to echo query + result set output.
echo = False

#%% Configure geocoder

# Set options to apply to all geocoders.
geopy.geocoders.options.default_timeout = 10

# Instantiate ArcGIS geocoder object.
geolocator = ArcGIS()

# Wrap geocode function in rate limiter.
geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds = 0.5,
    max_retries = 5,
    error_wait_seconds = 10)

# Set geocode function to include all attribute fields in the response from the ArcGIS geocoder.
out_fields = '*'
geocode = functools.partial(geocode, out_fields=out_fields)

#%% Create Database Connection String

engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(
    user,
    password,
    host,
    port,
    database))

#%%  Read table into output DataFrame

# Read query_address column from src table into a new pandas df.
# Select only those with prem_id values with null centroids and with rs_cd values not in the exclude list (or null rs_cd, to catch stragglers).
with engine.connect() as conn:
    df = pd.read_sql_query('''
        SELECT	id,
				query_address
        FROM permits.panel_upgrades
		WHERE (ST_ISEMPTY(centroid) OR
			  valid_centroid IS FALSE) AND
              query_address IS NOT NULL;
        ''',
        conn
    )

# Convert object types to string types if possible.
df = df.convert_dtypes()

#%%  Geocode using geopy

query = df['query_address']
location = query.progress_apply(geocode)

#%% Process result fields

# Extract coordinates.
longitude = location.apply(lambda loc: loc.longitude if loc else None)
latitude = location.apply(lambda loc: loc.latitude if loc else None)

#%% Process Outputs

# Construct GeoSeries of Shapely Point objects.
gs_4326 = gpd.points_from_xy(longitude, latitude, crs=4326)

# Transform CRS to NAD83 / California Albers (EPSG:3310).
gs_3310 = gs_4326.to_crs(crs=3310)

# Create GeoDataFrame.
output_gdf = gpd.GeoDataFrame(df, geometry=gs_3310)

# Rename geometry column from default of 'geometry'.
output_gdf.rename_geometry('centroid', inplace=True)

# Save location.address property.
address = location.apply(lambda loc: loc.address if loc else None)
output_gdf['address'] = address

# Save location.raw dictionary as JSON. Unless it's properly serialized it will be save as invalid JSON (with single quotes instead of double quotes).
raw = location.apply(lambda loc: json.dumps(loc.raw) if loc else None)
output_gdf['raw'] = raw

# Save score.
score = location.apply(lambda loc: loc.raw['score'] if loc else None)
output_gdf['score'] = score

#%% Write geodataframe to database

# When just using pandas/GeoPandas engine.begin() or connection.commit() is not necessary, and even the context manager is overkill.
with engine.connect() as conn:
    output_gdf.to_postgis(dst_table, conn, schema=dst_schema, if_exists=if_exists, index=False)
