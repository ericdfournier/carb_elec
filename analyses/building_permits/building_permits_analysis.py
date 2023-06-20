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

permits_sql = '''SELECT A.*,
                    B.place_name,
                    B.county_name,
                    B.dac,
                    B.low_income,
                    B.non_designated,
                    B.buffer_low_income,
                    B.bufferlih
                FROM permits.panel_upgrades_geocoded AS A
                JOIN permits.panel_upgrades_geocoded_geographies AS B
                    ON A.id = B.id'''

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

places_sql = '''SELECT *
    FROM census.acs_ca_2019_place_geom;'''

places = gpd.read_postgis(places_sql,
    engine,
    geom_col = 'geometry')

places.set_geometry('geometry', inplace = True, crs = 3310)
places = places.explode()
places_4326 = places.to_crs('EPSG:4326')

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

county_counts = pd.DataFrame(permits.groupby('county_name')['geometry'].agg('count'))
county_counts.rename(columns = {'geometry' : 'permit_counts'}, inplace = True)
data = gpd.GeoDataFrame(pd.merge(counties.loc[:,['geometry', 'NAMELSAD']], county_counts, left_on = 'NAMELSAD', right_on = 'county_name'))

#%% Generate Map Visualization of Permit Counts by County and Aggregate Counts for Visualization

fig, ax = plt.subplots(1,1, figsize = (5,8))

data.plot(column = 'permit_counts',
    ax = ax,
    cmap = 'rainbow',
    scheme = 'fisher_jenks')
counties.boundary.plot(ax=ax, edgecolor = 'black', linewidth = 0.5)
ax.set_axis_off()

fig.savefig(root + out + 'Permit_Counts_by_County_Map.png', dpi = 300, bbox_inches = 'tight')

#%% Join Permit Data to Places and Aggregate Counts for Visualization

place_counts = pd.DataFrame(permits.groupby('place_name')['geometry'].agg('count'))
place_counts.rename(columns = {'geometry' : 'permit_counts'}, inplace = True)
data = gpd.GeoDataFrame(pd.merge(places.loc[:,['geometry', 'NAMELSAD']], place_counts, left_on = 'NAMELSAD', right_on = 'place_name'))

#%% Generate Map Visualization of Permit Counts by Place

fig, ax = plt.subplots(1,1, figsize = (5,8))

counties.dissolve().plot(ax = ax, facecolor = 'white', edgecolor = 'black', linewidth = 0.5)
data.plot(column = 'permit_counts',
    ax = ax,
    cmap = 'rainbow',
    scheme = 'fisher_jenks')
places.boundary.plot(ax=ax, edgecolor = 'black', linewidth = 0.1)
ax.set_axis_off()

fig.savefig(root + out + 'Permit_Counts_by_Place_Map.png', dpi = 300, bbox_inches = 'tight')

#%% Generate Priority Population Category Counts

cols = ['dac',
        'low_income',
       'non_designated',
       'buffer_low_income',
       'bufferlih']

dac_counts = permits.groupby(cols)['geometry'].agg('count')

#%% Generate DAC vs Non-DAC Counts for each category

cols = [    'solar_pv_system',
            'main_panel_upgrade',
            'sub_panel_upgrade',
            'battery_storage_system',
            'ev_charger',
            'heat_pump']

times = pd.DataFrame()

dac_counts = pd.Series(index = cols)
non_dac_counts = pd.Series(index = cols)

for cat in cols:

    dac_ind = permits['dac'] == 'Yes'
    cat_ind = permits[cat] == 1

    dac_counts[cat] = ((dac_ind) & (cat_ind)).sum()
    non_dac_counts[cat] = ((~dac_ind) & (cat_ind)).sum()

counts_by_dac = pd.merge(dac_counts.rename('dac_counts'),
    non_dac_counts.rename('non_dac_counts'), left_index = True, right_index = True)

#%% Plot Counts by DAC Status

xtick_labels = [x.replace('_', ' ').title() for x in cols]

fig, ax = plt.subplots(1,1, figsize = (7,5))

counts_by_dac.plot.bar(stacked=True, ax = ax, color=[ 'tab:orange','tab:blue'])
ax.set_xticklabels(xtick_labels)
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax.grid(True)
ax.legend(['DAC Counts','Non-DAC Counts'])
ax.set_xlabel('Upgrade Category')
ax.set_ylabel('Count Frequency')

fig.savefig(root + out + 'Upgrade_Category_by_DAC_Status.png', dpi = 300, bbox_inches = 'tight')

#%% Compute Percents

dac_pct = (counts_by_dac['dac_counts'] / counts_by_dac.sum(axis = 1)) * 100.0
non_dac_pct = (counts_by_dac['non_dac_counts'] / counts_by_dac.sum(axis = 1)) * 100.0
pct_by_dac = pd.merge(dac_pct.rename('dac_pct'), non_dac_pct.rename('non_dac_pct'), left_index = True, right_index = True).round(0)
