#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import sqlalchemy as sql
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
import seaborn as sns

#%% DB Connection Parameters

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

query = ''' SELECT * FROM census.acs_ca_2019_tr_geom;'''
tr_geom = gpd.read_postgis(query, db_con, geom_col = 'geometry')
tr_geom['GEOID_INT'] = pd.to_numeric(tr_geom['GEOID'])

#%% Import Proportion Electric Heating Change from File

query = ''' SELECT * FROM census.acs_ca_2017_2022_proportion_electric_heating_change;'''
prop_elec_heating_change = pd.read_sql(query, db_con)

#%% Import Census Tract Level Aggregations from File

existing_tables_dir = '/Users/edf/repos/carb_elec/analyses/manuscript_revisions/csv/existing/'
tr_sf_data = pd.read_csv(existing_tables_dir + 'single_family_census_tract_existing_panel_counts.csv')
tr_mf_data = pd.read_csv(existing_tables_dir + 'multi_family_census_tract_existing_panel_counts.csv')

#%% Merge Data

sf_merge = pd.merge(
    left = tr_geom.loc[:,['geometry', 'GEOID_INT', 'NAMELSAD', 'COUNTYFP']],
    right = tr_sf_data,
    left_on = 'GEOID_INT',
    right_on = 'tract_geoid_2019')

sf_out = gpd.GeoDataFrame(sf_merge, crs = 'EPSG:3310', geometry = sf_merge['geometry'])

mf_merge = pd.merge(
    left = tr_geom.loc[:,['geometry', 'GEOID_INT', 'NAMELSAD', 'COUNTYFP']],
    right = tr_mf_data,
    left_on = 'GEOID_INT',
    right_on = 'tract_geoid_2019')

mf_out = gpd.GeoDataFrame(mf_merge, crs = 'EPSG:3310', geometry = mf_merge['geometry'])

#%% Merge Proportion of Electric Heating to SF/MF Dataframes

sf_merge_final = pd.merge(
    left = sf_merge,
    right = prop_elec_heating_change,
    left_on = 'GEOID_INT',
    right_on = 'GEOID',
    how = 'left'
)

#%% Write to Shapefile for Export to ArcGIS

shp_dir = '/Users/edf/repos/carb_elec/analyses/agol_map_data/shp/'

sf_merge.to_file(shp_dir + 'sf_tract_level_panel_size_estimates.shp')
mf_merge.to_file(shp_dir + 'mf_tract_level_panel_size_estimates.shp')

#%% Write to CSV File for Export

csv_dir = '/Users/edf/repos/carb_elec/analyses/agol_map_data/csv/'

sf_cols = ['GEOID_INT', 'NAMELSAD', 'COUNTYFP', 'tract_geoid_2019',
       '<100', '100', '101 - 199', '200', '>200']
mf_cols = ['GEOID_INT', 'NAMELSAD', 'COUNTYFP', 'tract_geoid_2019',
       '<60', '60', '61 - 89', '90', '91 - 149', '150', '>150']

sf_merge.loc[:,sf_cols].to_csv(csv_dir + 'sf_tract_level_panel_size_estimates.csv')
mf_merge.loc[:,mf_cols].to_csv(csv_dir + 'mf_tract_level_panel_size_estimates.csv')
