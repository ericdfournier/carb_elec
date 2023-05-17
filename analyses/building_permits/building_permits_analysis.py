#%% Package Imports

import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
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

#%% Read permit table from database

sql = '''SELECT centroid,
            permit_number,
            permit_class,
            permit_type,
            estimated_cost,
            applied_date,
            issued_date,
            finaled_date,
            address,
            parcel_number,
            file_name,
            id,
            solar_pv_system,
            battery_storage_system,
            ev_charger,
            heat_pump,
            main_panel_upgrade,
            sub_panel_upgrade,
            upgraded_panel_size
        FROM permits.combined'''

permits = gpd.read_postgis(sql,
    engine,
    geom_col='centroid',
    index_col = 'id')

#%% Generate Count Data and Plot Counts

cols = ['solar_pv_system',
        'main_panel_upgrade',
        'sub_panel_upgrade',
        'heat_pump',
        'ev_charger',
        'battery_storage_system']

data = permits[cols].sum(axis=0)

xtick_labels = [x.replace('_', ' ').title() for x in cols]

fig, ax = plt.subplots(1,1, figsize=(7,7))

sns.barplot(x = data.index, y = data.values, order = cols)
ax.grid(True)
plt.xticks(rotation=90)
ax.set_xticklabels(xtick_labels)
ax.set_ylabel('Count Frequency')
ax.set_xlabel('Upgrade Category')
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

fig.savefig(root + out + 'Upgrade_Category.png', dpi = 300, bbox_inches = 'tight')

#%% Generate Combinations Table

combinations = permits.groupby(cols)['file_name'].agg('count').reset_index()
combinations.rename(columns = {'file_name':'count'}, inplace = True)

#%% Plot Main Panel Upgrade Size Distribution

fig, ax = plt.subplots(1,1, figsize=(7,5))
ind = permits['main_panel_upgrade'] == True
cols = ['upgraded_panel_size']
data = permits.loc[ind,:].groupby(cols)[cols].agg('count')
sns.barplot(x = data.index, y = data.values.ravel(), ax = ax)
ax.set_xticklabels(data.index.get_level_values(0).astype(int), rotation=45, horizontalalignment='right')
ax.set_title('Main Panel Upgrade Sizes')
ax.set_ylabel('Count Frequency')
ax.set_xlabel('Panel Size [Amps]')
ax.grid(True)
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

fig.savefig(root + out + 'Main_Panel_Upgrade_Size_Distributions.png', dpi = 300, bbox_inches = 'tight')

#%% Plot Sub Panel Upgrade Size Distribution

fig, ax = plt.subplots(1,1, figsize=(7,5))
ind = permits['sub_panel_upgrade'] == True
cols = ['upgraded_panel_size']
data = permits.loc[ind,:].groupby(cols)[cols].agg('count')
sns.barplot(x = data.index, y = data.values.ravel())
ax.set_xticklabels(data.index.get_level_values(0).astype(int), rotation=45, horizontalalignment='right')
ax.set_title('Sub-Panel Upgrade Sizes')
ax.set_ylabel('Count Frequency')
ax.set_xlabel('Panel Size [Amps]')
ax.grid(True)
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

fig.savefig(root + out + 'Sub-Panel_Upgrade_Size_Distribution.png', dpi = 300, bbox_inches = 'tight')
