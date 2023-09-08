#%% Package Imports

import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import numpy as np
import os

#%% Change Working Directory

root = '/Users/edf/repos/carb_elec/analyses/building_permits/'
out = 'fig/'

os.chdir(root)

#%% Get DB Connection Parameters

user = os.environ['PGUSER']
password = os.environ['PGPASSWORD']
host = os.environ['PGHOST']
port = os.environ['PGPORT']
database = 'carb'

#%% Connect to Database

engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(
    user,
    password,
    host,
    port,
    database))

#%% Import Permit Data

permits_sql = '''SELECT
                    perm.*,
                    geo.place_name,
                    geo.county_name,
                    geo.dac,
                    geo.low_income,
                    geo.non_designated,
                    geo.buffer_low_income,
                    geo.bufferlih,
                    geo.air_basin,
                    geo.air_district,
                    mp."usetype",
                    mp."YearBuilt" as vintage_year,
                    mp."TotalBuildingAreaSqFt" as building_sqft
                FROM permits.panel_upgrades_geocoded AS perm
                JOIN permits.panel_upgrades_geocoded_geographies AS geo
                    ON perm.id = geo.id
                JOIN ztrax.megaparcels AS mp
                    ON perm.megaparcelid = mp.megaparcelid'''

permits = gpd.read_postgis(permits_sql,
    engine,
    geom_col = 'centroid',
    index_col = 'id')

permits.rename(columns = {'centroid' : 'geometry'}, inplace = True)
permits.set_geometry('geometry', inplace = True, crs = 3310)

#%% Bin by SF Vintage Year and Size

sf_ind = permits['usetype'] == 'single_family'
sf = permits.loc[sf_ind,:].copy(deep = True)

sf_year_min = sf['vintage_year'].min()
sf_year_max = sf['vintage_year'].max()
sf_year_bins = [
    sf_year_min,
    1800.,
    1850.,
    1900.,
    1920.,
    1940.,
    1960.,
    1980.,
    2000.,
    2010.,
    2020.,
    sf_year_max]

sf['vintage_year_category'] = pd.cut(
    sf['vintage_year'],
    bins = sf_year_bins,
    include_lowest = True)

sf_sqft_min = sf['building_sqft'].min()
sf_sqft_max = sf['building_sqft'].max()
sf_sqft_bins = [
    sf_sqft_min,
    500.,
    1000.,
    1500.,
    2000.,
    2500.,
    3000.,
    4000.,
    5000.,
    8000.,
    10000.,
    20000.,
    sf_sqft_max]

sf['building_sqft_category'] = pd.cut(
    sf['building_sqft'],
    bins = sf_sqft_bins,
    include_lowest = True)

#%% Bin by MF Vintage Year and Size

mf_ind = permits['usetype'] == 'multi_family'
mf = permits.loc[mf_ind,:].copy(deep = True)

mf_year_min = mf['vintage_year'].min()
mf_year_max = mf['vintage_year'].max()
mf_year_bins = [
    mf_year_min,
    1850.,
    1900.,
    1920.,
    1940.,
    1960.,
    1980.,
    2000.,
    2010.,
    2020.,
    mf_year_max]

mf['vintage_year_category'] = pd.cut(
    mf['vintage_year'],
    bins = mf_year_bins,
    include_lowest = True)

mf_sqft_min = mf['building_sqft'].min()
mf_sqft_max = mf['building_sqft'].max()
mf_sqft_bins = [
    mf_sqft_min,
    1000.,
    5000.,
    10000.,
    20000.,
    30000.,
    40000.,
    50000.,
    100000.,
    500000.,
    1000000.,
    mf_sqft_max]

mf['building_sqft_category'] = pd.cut(
    mf['building_sqft'],
    bins = mf_sqft_bins,
    include_lowest = True)

#%% Group By and Generate Counts

group_fields = [
    'air_district',
    'vintage_year_category',
    'building_sqft_category']

count_fields = [
    'solar_pv_system',
    'battery_storage_system',
    'ev_charger',
    'heat_pump',
    'main_panel_upgrade',
    'sub_panel_upgrade']

sf_stats = sf.groupby(group_fields)[count_fields].agg('sum')
mf_stats = mf.groupby(group_fields)[count_fields].agg('sum')

#%% Output to File for Sharing

output_dir = '/Users/edf/repos/carb_elec/analyses/building_permits/output/'

sf_stats.to_csv(output_dir + 'sf_stats.csv')
mf_stats.to_csv(output_dir + 'mf_stats.csv')
