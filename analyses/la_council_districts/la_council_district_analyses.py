#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import sqlalchemy as sql
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
from matplotlib.colors import LogNorm, Normalize
import seaborn as sns

#%% Set Fixed Parameters

figure_dir = '/Users/edf/repos/carb_elec/analyses/model_data/corelogic/fig/'
tables_dir = '/Users/edf/repos/carb_elec/analyses/model_data/corelogic/csv/'
output_dir = '/Users/edf/repos/carb_elec/analyses/model_data/corelogic/output/'

#%% Read Model Data Set from Pickle

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

query = ''' SELECT  A.*,
                    B.permitted_panel_upgrade,
                    B.observed_panel_upgrade,
                    B.inferred_panel_upgrade,
                    B.any_panel_upgrade,
                    B.panel_size_existing,
                    C.air_district,
                    C.county_name,
                    C.county_air_basin_district_id,
                    C.tract_geoid_2019
            FROM corelogic.model_data AS A
            JOIN corelogic.model_data_sf_inference AS B
                ON A.megaparcelid = B.megaparcelid
            JOIN corelogic.megaparcels_geocoded_geographies AS C
                ON A.megaparcelid = C.megaparcelid;'''

sf = pd.read_sql(query, db_con)

# Set megaparcelid as index
sf.set_index('megaparcelid', drop = True, inplace = True)

#%% Extract Multi-Family Model Data

query = ''' SELECT  A.*,
                    B.permitted_panel_upgrade,
                    B.observed_panel_upgrade,
                    B.inferred_panel_upgrade,
                    B.any_panel_upgrade,
                    B.panel_size_existing,
                    C.air_district,
                    C.county_name,
                    C.county_air_basin_district_id,
                    C.tract_geoid_2019
            FROM corelogic.model_data AS A
            JOIN corelogic.model_data_mf_inference AS B
                ON A.megaparcelid = B.megaparcelid
            JOIN corelogic.megaparcels_geocoded_geographies AS C
                ON A.megaparcelid = C.megaparcelid;'''

mf = pd.read_sql(query, db_con)

# Set megaparcelid as index
mf.set_index('megaparcelid', drop = True, inplace = True)

#%% Drop Parcels with Bogus Vintage Years

sf = sf.loc[sf['YearBuilt'] < 2024,:]
mf = mf.loc[mf['YearBuilt'] < 2024,:]

#%% Extract Census Boundaries

query = '''SELECT * FROM census.acs_ca_2019_tr_geom;'''
tracts = gpd.read_postgis(query, db_con, geom_col = 'geometry')

#%% Reset Database Connection

# Extract Database Connection Parameters from Environment
host = os.getenv('PGHOST')
user = os.getenv('PGUSER')
password = os.getenv('PGPASS')
port = os.getenv('PGPORT')
db = 'edf'

# Establish DB Connection
db_con_string = 'postgresql://' + user + '@' + host + ':' + port + '/' + db
db_con = sql.create_engine(db_con_string)

#%% Extract Council Districts

query = '''SELECT * FROM ladwp.council_districts_2022;'''
cds = gpd.read_postgis(query, db_con, geom_col = 'geom')

#%% Extract CDs

cd5 = cds.loc[cds['district'] == 5,:]
cd6 = cds.loc[cds['district'] == 6,:]
cd8 = cds.loc[cds['district'] == 8,:]
cd11 = cds.loc[cds['district'] == 11,:]

#%% Generate Plot

def ROIPanelStatsBarChart(sf, mf, mask, tracts):

    centroids = tracts.geometry.centroid
    mask_ind = centroids.intersects(mask.unary_union)
    geoids = tracts.loc[mask_ind,'GEOID']

    sf_ind = sf['tract_geoid_2019'].isin(geoids)
    sf_sub = sf.loc[sf_ind,:].copy(deep = True)

    mf_ind = mf['tract_geoid_2019'].isin(geoids)
    mf_sub = mf.loc[mf_ind,:].copy(deep = True)

    panel = 'panel_size_existing'

    sf_bins = [0, 99, 100, 101, 199, 200, 201, 2000]
    sf_labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
    sf_cols = ['<100','100','101 - 199','200','>200']

    mf_bins = [0, 59, 60, 61, 89, 90, 101, 149, 150, 151, 2000]
    mf_labels = ['<60', '60', '61 - 89', '61 - 89', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
    mf_cols = ['<60', '60', '61 - 89', '90','91 - 149','150','>150']

    sf_sub['panel_size_class'] = pd.cut(sf_sub.loc[:,panel],
        bins = sf_bins,
        labels = sf_labels,
        ordered = False).to_frame()

    mf_sub['panel_size_class'] = pd.cut(mf_sub.loc[:,panel],
        bins = mf_bins,
        labels = mf_labels,
        ordered = False).to_frame()

    sf_stats = sf_sub[['panel_size_class',panel]].groupby(['panel_size_class'],
        observed = False).agg('count')
    sf_stats.rename(columns = {panel:'count'}, inplace = True)
    sf_totals = sf_stats.sum()['count']
    sf_stats['pct'] = sf_stats['count'].divide(sf_totals)
    sf_stats.reset_index(inplace = True)
    sf_stats['cat'] = 'Single-Family'
    sf_out = sf_stats.pivot(index = 'cat', columns='panel_size_class', values='pct')

    mf_stats = mf_sub[['panel_size_class',panel]].groupby(['panel_size_class'],
        observed = False).agg('count')
    mf_stats.rename(columns = {panel:'count'}, inplace = True)
    mf_totals = mf_stats.sum()['count']
    mf_stats['pct'] = mf_stats['count'].divide(mf_totals)
    mf_stats.reset_index(inplace = True)
    mf_stats['cat'] = 'Multi-Family'
    mf_out = mf_stats.pivot(index = 'cat', columns='panel_size_class', values='pct')

    fig, ax = plt.subplots(1,2,figsize = (6,4), sharey = True)

    sf_out[sf_cols].plot(
        kind='bar',
        stacked=True,
        ax = ax[0],
        edgecolor='k')

    mf_out[mf_cols].plot(
        kind='bar',
        stacked=True,
        ax = ax[1],
        edgecolor='k')

    # Label SF Axis
    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax[0].set_ylabel('Share of buildings')
    ax[0].set_xlabel(None)
    ax[0].set_yticks(np.arange(0,1.1,0.1))
    ax[0].set_ylim(0,1)
    ax[0].set_axisbelow(True)
    ax[0].grid(True)
    ax[0].tick_params(axis='x', labelrotation=0)

    for c in ax[0].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[0].bar_label(c, labels=labels, label_type='center')

    # Label MF Axis
    handles, labels = ax[1].get_legend_handles_labels()
    ax[1].legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax[1].set_ylabel('Share of buildings')
    ax[1].set_xlabel(None)
    ax[1].set_yticks(np.arange(0,1.1,0.1))
    ax[1].set_ylim(0,1)
    ax[1].set_axisbelow(True)
    ax[1].grid(True)
    ax[1].tick_params(axis='x', labelrotation=0)

    for c in ax[1].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[1].bar_label(c, labels=labels, label_type='center')

    fig.tight_layout()

    return sf_out[sf_cols], mf_out[mf_cols], fig, ax

#%% CD5 Results

cd5_sf, cd5_mf, fig, ax = ROIPanelStatsBarChart(sf, mf, cd5, tracts)

#%% CD6 Results

cd6_sf, cd6_mf, fig, ax = ROIPanelStatsBarChart(sf, mf, cd6, tracts)

#%% CD8 Results

cd8_sf, cd8_mf, fig, ax = ROIPanelStatsBarChart(sf, mf, cd8, tracts)

#%% CD11 Results

cd11_sf, cd11_mf, fig, ax = ROIPanelStatsBarChart(sf, mf, cd11, tracts)
