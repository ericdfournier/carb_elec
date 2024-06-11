#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import sqlalchemy as sql
import os

# Extract Database Connection Parameters from Environment
host = os.getenv('PGHOST')
user = os.getenv('PGUSER')
password = os.getenv('PGPASS')
port = os.getenv('PGPORT')
db = 'carb'

# Establish DB Connection
db_con_string = 'postgresql://' + user + '@' + host + ':' + port + '/' + db
db_con = sql.create_engine(db_con_string)

#%% Extract Single Family Model Data

query = '''WITH single_family AS (SELECT
                A."megaparcelid" AS megaparcel_id,
                A."geom" AS geom,
                A."clips" AS corelogic_clip,
                A."usetype" AS usetype,
                A."ciscorep" AS ces4_percentile_score,
                A."sampled" AS in_permit_sample_territory,
                A."panel_size_as_built",
                B."permitted_panel_upgrade",
                B."observed_panel_upgrade",
                B."inferred_panel_upgrade",
                B."any_panel_upgrade",
                B."panel_size_existing",
                C."air_district",
                C."county_name",
                C."county_air_basin_district_id",
                C."tract_geoid_2019"
        FROM corelogic.model_data_20240126 AS A
        JOIN corelogic.model_data_sf_inference_20240126 AS B
            ON A."megaparcelid" = B."megaparcelid"
        JOIN corelogic.corelogic_20240126_varchar_megaparcels_geocoded_geographies AS C
            ON A."megaparcelid" = C."megaparcelid"),
        multi_family AS (SELECT
                A."megaparcelid" AS megaparcel_id,
                A."geom" AS geom,
                A."clips" AS corelogic_clip,
                A."usetype" AS usetype_category,
                A."ciscorep" AS ces4_percentile_score,
                A."sampled" AS in_permit_sample_territory,
                A."panel_size_as_built",
                B."permitted_panel_upgrade",
                B."observed_panel_upgrade",
                B."inferred_panel_upgrade",
                B."any_panel_upgrade",
                B."panel_size_existing",
                C."air_district",
                C."county_name",
                C."county_air_basin_district_id",
                C."tract_geoid_2019"
            FROM corelogic.model_data_20240126 AS A
            JOIN corelogic.model_data_mf_inference_20240126 AS B
                ON A."megaparcelid" = B."megaparcelid"
            JOIN corelogic.corelogic_20240126_varchar_megaparcels_geocoded_geographies AS C
                ON A."megaparcelid" = C."megaparcelid")
            (SELECT * FROM single_family)
                UNION
            (SELECT * FROM multi_family);'''

mp = gpd.read_postgis(
    query,
    db_con,
    geom_col = "geom",
    crs = "EPSG:3310")

#%% Drop Missing Values

mp.dropna(subset = ['corelogic_clip', 'panel_size_existing', 'panel_size_as_built'], inplace = True)

#%% Iterate Through List and Flatten Values

out = mp.explode('corelogic_clip')

#%% Drop Records with Missing Clips

out.dropna(subset = ['corelogic_clip'], inplace = True)

#%% Drop Duplicate Records

out.drop_duplicates(subset = ['corelogic_clip'], inplace = True)

#%% Reset Index

out.reset_index(drop = True, inplace = True)

#%% Integrity Tests

unique_clips = out['corelogic_clip'].nunique()
unique_megaparcel_ids = out['megaparcel_id'].nunique()

#%% Output Full GeoPackage File

gpkg_path = '/Users/edf/Desktop/cec_panel_size_estimate_results/panel_size_estimates_full_geospatial.gpkg'
out.to_file(gpkg_path, driver = "GPKG")

#%% Output Full Non-Geospatial File

csv_path = '/Users/edf/Desktop/cec_panel_size_estimate_results/panel_size_estimates_full_non_geospatial.csv'
csv_cols = out.columns.to_list()
csv_cols.remove('geom')
out[csv_cols].to_csv(csv_path, index = False)
