#%% Package Imports

import pandas as pd
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
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

#%% Import Permit Data

permits_sql = '''SELECT * FROM permits.panel_upgrades_geocoded'''

permits = gpd.read_postgis(permits_sql,
    engine,
    geom_col = 'centroid',
    index_col = 'id')

permits.rename(columns = {'centroid' : 'geometry'}, inplace = True)
permits.set_geometry('geometry', inplace = True, crs = 3310)
permits_4326 = permits.to_crs('EPSG:4326')

# Format Permit Time Stamp Columns
permits['applied_date'] = pd.to_datetime(permits['applied_date'])
permits['issued_date'] = pd.to_datetime(permits['issued_date'])
permits['finaled_date'] = pd.to_datetime(permits['finaled_date'])

#%% Import CA Boundaries

counties_sql = '''SELECT *
    FROM census.acs_ca_2019_county_geom;'''

counties = gpd.read_postgis(counties_sql,
    engine,
    geom_col = 'geometry')

counties.set_geometry('geometry', inplace = True, crs = 3310)
counties = counties.explode()
counties_4326 = counties.to_crs('EPSG:4326')

#%% Valid Permits Descriptive Stas

permits.info()
permits.describe()

#%% Generate Count Data and Plot Counts

cols = [    'solar_pv_system',
            'main_panel_upgrade',
            'sub_panel_upgrade',
            'battery_storage_system',
            'ev_charger',
            'heat_pump']

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

#%% Monthly Permit Count Time Series Lineplot

cols = [    'issued_date',
            'solar_pv_system',
            'main_panel_upgrade',
            'sub_panel_upgrade',
            'battery_storage_system',
            'ev_charger',
            'heat_pump']

labels = [x.replace('_', ' ').title() for x in cols[1:]]

ts_monthly = permits.loc[:,cols].set_index('issued_date', drop = True).resample('M').agg('sum')

fig, ax = plt.subplots(1,1, figsize = (7,5))
ax.plot(ts_monthly)
ax.legend(labels)
ax.grid(True)
ax.set_xlim(pd.to_datetime('01-01-1996'), pd.to_datetime('7-31-2022'))
ax.set_ylabel('Permits per Month')
ax.set_xlabel('Time')

fig.savefig(root + out + 'Permit_Count_Monthly_Time_Series_Line_Plot.png', dpi = 300, bbox_inches = 'tight')

#%% Plot Monthly Fraction Time Series Stackplot

cols = [    'issued_date',
            'solar_pv_system',
            'main_panel_upgrade',
            'sub_panel_upgrade',
            'battery_storage_system',
            'ev_charger',
            'heat_pump']

labels = [x.replace('_', ' ').title() for x in cols[1:]]

ts_monthly_pct = ts_monthly.divide(ts_monthly.sum(axis=1), axis = 0)

fig, ax = plt.subplots(1,1, figsize = (9,5))
ax.stackplot(ts_monthly_pct.index,
            ts_monthly_pct.values[:,0],
            ts_monthly_pct.values[:,1],
            ts_monthly_pct.values[:,2],
            ts_monthly_pct.values[:,3],
            ts_monthly_pct.values[:,4],
            ts_monthly_pct.values[:,5])
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5))
ax.grid(True)
ax.set_ylim(0,1)
ax.set_xlim(pd.to_datetime('01-01-1996'), pd.to_datetime('7-31-2022'))
ax.set_ylabel('Fraction of Permits per Month')
ax.set_xlabel('Time')

fig.savefig(root + out + 'Permit_Fraction_Monthly_Time_Series_Stackplot.png', dpi = 300, bbox_inches = 'tight')

#%% Plot Density Map for all Valid Permits

# ! Careful - this takes a while for all of the points

# fig, ax = gplt.kdeplot(permits_4326,
#     projection=gcrs.AlbersEqualArea(),
#     cmap='rainbow',
#     fill=True,
#     clip = counties_4326,
#     bw_adjust = 2.0,
#     figsize= (5,8))
# gplt.polyplot(counties_4326,
#     projection=gcrs.AlbersEqualArea(),
#     zorder = 1,
#     linewidth = 0.25,
#     ax = ax)

# plt.show()

# fig.savefig(root + out + 'Permit_Data_Geographic_Distribution_KDE_Map.png', dpi = 300, bbox_inches = 'tight')

#%% Compute Time Differences

cols = [    'solar_pv_system',
            'main_panel_upgrade',
            'sub_panel_upgrade',
            'battery_storage_system',
            'ev_charger',
            'heat_pump']

times = pd.DataFrame()

for cat in cols:

    ind = permits[cat] == 1

    processing_times = permits.loc[ind,'issued_date'] - permits.loc[ind,'applied_date']
    completion_times = permits.loc[ind,'finaled_date'] - permits.loc[ind,'issued_date']

    # Type conversion to numeric day values
    processing_times = processing_times.dt.days
    completion_times = completion_times.dt.days

    t = pd.concat([processing_times, completion_times], axis = 1)
    t['category'] = cat
    times = pd.concat([times, t], axis = 0)

times.columns = ['permit_application_processing_time', 'project_completion_time', 'category']

# Null illegal values
cols = ['permit_application_processing_time', 'project_completion_time']
neg_ind = times.loc[:, cols] < 0.0
times[neg_ind] = np.nan

times = times.melt(id_vars=['category'],
        var_name='status',
        value_name='time')

times.dropna(inplace = True)

#%% Compute stats

time_stats = times.groupby(['category', 'status']).agg(['mean', 'median'])

#%% Plot Processing Time Distributions

cols = ['permit_application_processing_time',
        'project_completion_time']
legend_labels = [x.replace('_', ' ').title() for x in cols]

cols = ['solar_pv_system',
        'main_panel_upgrade',
        'sub_panel_upgrade',
        'battery_storage_system',
        'ev_charger',
        'heat_pump']
xtick_labels = [x.replace('_', ' ').title() for x in cols]

ytick_labels = ['0.1', '1', '10', '100', '1,000', '10,000']

fig, ax = plt.subplots(1,1, figsize = (8,5))

sns.boxplot(data = times,
    x = 'category',
    y = 'time',
    notch = True,
    hue = 'status',
    ax = ax)
ax.set_yscale('log')
ax.set_ylim(1,10000)
ax.set_yticklabels(ytick_labels)
ax.set_xticklabels(xtick_labels, rotation = 45)
ax.legend(loc = 'upper right')
ax.set_xlabel('Upgrade Category')
ax.set_ylabel('Days')
ax.grid(True)

fig.savefig(root + out + 'Permit_Execution_Time_Distribution_Boxplot_Series.png', dpi = 300, bbox_inches = 'tight')

#%% Compute Estimated Costs

cols = [    'solar_pv_system',
            'main_panel_upgrade',
            'sub_panel_upgrade',
            'battery_storage_system',
            'ev_charger',
            'heat_pump']

costs = pd.DataFrame()

for cat in cols:

    ind = permits[cat] == 1
    c = pd.DataFrame(permits.loc[ind,'estimated_cost'])
    c['category'] = cat
    costs = pd.concat([costs, c], axis = 0)

costs.dropna(inplace = True)
costs['estimated_cost'] = costs['estimated_cost'].replace('[\$,]', '', regex=True).astype(float)

#%% Compute Cost Stats

cost_stats = costs.groupby(['category']).agg(['mean', 'median'])

#%% Plot Cost Distributions

ytick_labels = ['$10',
                '$100',
                '$1,000',
                '$10,000',
                '$100,000',
                '$1,000,000',
                '$10,000,000',
                '$100,000,000']

fig, ax = plt.subplots(1,1,figsize = (7,5))

sns.boxplot(data = costs,
    x = 'category',
    y = 'estimated_cost',
    notch = True,
    ax = ax)
ax.set_yscale('log')
ax.set_yticklabels(ytick_labels)
ax.set_xticklabels(xtick_labels, rotation = 45)
ax.set_ylabel('Estimated Cost')
ax.set_xlabel('Upgrade Category')
ax.grid(True)

fig.savefig(root + out + 'Permit_Estimated_Cost_Distribution_Boxplot_Series.png', dpi = 300, bbox_inches = 'tight')

#%% Join Permit Data to Counties

permits_counties = permits.sjoin(counties.loc[:,['geometry','NAMELSAD']], how = 'inner')
permits_counties_counts = permits_counties.groupby('NAMELSAD')['geometry'].agg('count')
permits_counties_counts = pd.merge(permits_counties_counts, counties.loc[:,['NAMELSAD','geometry']], left_on = 'NAMELSAD', right_on = 'NAMELSAD')
permits_counties_counts.rename(columns = {'geometry_x': 'permit_count', 'geometry_y': 'geometry'}, inplace = True)
data = gpd.GeoDataFrame(permits_counties_counts)

#%% Generate Map Visualization of Permit Counts by County

fig, ax = plt.subplots(1,1, figsize = (5,8))

data.plot(column = 'permit_count',
    ax = ax,
    cmap = 'rainbow',
    scheme = 'fisher_jenks')
counties.boundary.plot(ax=ax, edgecolor = 'black', linewidth = 0.5)
ax.set_axis_off()

fig.savefig(root + out + 'Permit_Counts_by_County_Map.png', dpi = 300, bbox_inches = 'tight')
