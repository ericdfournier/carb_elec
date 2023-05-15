#%% Package Imports

import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm

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

#%% Convert Array Field

ps = pd.Series(index = permits.index, dtype = int)

for i, r in tqdm(permits.iterrows()):
    if r['upgraded_panel_size'] == None:
        ps[i] = np.NaN
    elif r['upgraded_panel_size'] == []:
        ps[i] = np.NaN
    else:
        ps[i] = pd.to_numeric(r['upgraded_panel_size'][0])

#%% Overwrite with Numeric Values

permits['upgraded_panel_size'] = ps

#%% Generate Count Data

cols = ['solar_pv_system',
        'main_panel_upgrade',
        'sub_panel_upgrade',
        'heat_pump',
        'ev_charger',
        'battery_storage_system']

permits['measure_category'] = (permits.loc[:,cols] == 1).idxmax(1)

#%% Plot Counts

data = permits.groupby('measure_category')['measure_category'].agg('count')

xtick_labels = [x.replace('_', ' ').title() for x in cols]

fig, ax = plt.subplots(1,1, figsize=(7,7))

sns.barplot(x = data.index, y = data.values, order = cols)
ax.set_yscale('log')
ax.grid(True)
plt.xticks(rotation=90)
ax.set_xticklabels(xtick_labels)
ax.set_yticklabels([None, None, '10,000', '100,000', '1,000,000'])
ax.set_ylabel('Count Frequency')
ax.set_xlabel('Upgrade Category')

#%% Plot Main Panel Upgrade Size Distribution

ind = permits['main_panel_upgrade'] == True
cols = ['upgraded_panel_size']
data = permits.loc[ind,:].groupby(cols)[cols].agg('count')
chart = sns.barplot(x = data.index, y = data.values.ravel())
chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
ax.set_title('Main Panel Upgrade Sizes')
ax.set_ylabel('Count Frequency')
ax.set_xlabel('Panel Size [Amps]')

#%% Plot Sub Panel Upgrade Size Distribution

ind = permits['sub_panel_upgrade'] == True
cols = ['upgraded_panel_size']
data = permits.loc[ind,:].groupby(cols)[cols].agg('count')
chart = sns.barplot(x = data.index, y = data.values.ravel())
chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
ax.set_title('Sub-Panel Upgrade Sizes')
ax.set_ylabel('Count Frequency')
ax.set_xlabel('Panel Size [Amps]')
