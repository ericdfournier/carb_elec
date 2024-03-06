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
from matplotlib.patches import Rectangle


#%% Set Fixed Parameters

figure_dir = '/Users/edf/repos/carb_elec/analyses/manuscript_revisions/fig/'

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
            JOIN corelogic.model_data_mf_inference AS B
                ON A.megaparcelid = B.megaparcelid
            JOIN corelogic.megaparcels_geocoded_geographies AS C
                ON A.megaparcelid = C.megaparcelid;'''

mf = pd.read_sql(query, db_con)

# Set megaparcelid as index
mf.set_index('megaparcelid', drop = True, inplace = True)

#%% Extract Air District Geographic Boundaries

query = ''' SELECT  * FROM carb.ca_air_districts;'''
air_districts = gpd.read_postgis(query, db_con, geom_col = 'geom')

#%% Extract County Boundaries

query = '''SELECT * FROM census.acs_ca_2019_county_geom;'''
counties = gpd.read_postgis(query, db_con, geom_col = 'geometry')

#%% Extract County Air Basin District Geographic Boundaries

query = ''' SELECT  * FROM carb.ca_county_air_basin_districts;'''
county_air_basin_districts = gpd.read_postgis(query, db_con, geom_col = 'geom')

#%% Extract Census Boundaries

query = '''SELECT * FROM census.acs_ca_2019_tr_geom;'''
tracts = gpd.read_postgis(query, db_con, geom_col = 'geometry')

#%% Generate Panel Statistics Table

def PrintPanelStatsTable(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()
    stats = mp[['panel_size_class','panel_size_existing']].groupby('panel_size_class',
        observed = False).agg('count')
    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    total = (~mp['panel_size_existing'].isna()).sum()
    stats['pct'] = stats['count'].divide(total).multiply(100.0)

    if sector == 'multi_family':
        units = mp[['panel_size_class','panel_size_existing','TotalNoOfUnits']].groupby('panel_size_class',
            observed = False)['TotalNoOfUnits'].agg('sum').to_frame()
        total_units = mp.loc[(~mp['panel_size_existing'].isna()), 'TotalNoOfUnits'].sum()
        units['pct_units'] = units['TotalNoOfUnits'].divide(total_units).multiply(100.0)
        stats = pd.merge(stats, units, left_index = True, right_index = True)

    print(stats)

    return stats

#%% Print Panel Statistics Tables

# LBNL Initial Results for Comparison
# Panel Amps	Count	Frequency
# <100	        5,068	9%
# 100	        15,090	26%
# 101-199	    12,185	21%
# 200	        19,109	33%
# 201+	        5,915	10%

sf_stats = PrintPanelStatsTable(sf, 'single_family')
mf_stats = PrintPanelStatsTable(mf, 'multi_family')

#%% Generate DAC Panel Statistics Table

def PrintDACPanelStatsTable(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()
    stats = mp[['panel_size_class','dac','panel_size_existing']].groupby(['panel_size_class', 'dac'],
        observed = False).agg('count')
    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    totals = mp.loc[~mp['panel_size_existing'].isna(),'dac'].to_frame().groupby('dac').value_counts()
    stats['pct'] = stats['count'].divide(totals).multiply(100.0)

    print(stats)

    return stats

#%% Print DAC Panel Statistics Tables

sf_stats = PrintDACPanelStatsTable(sf, 'single_family')
mf_stats = PrintDACPanelStatsTable(mf, 'multi_family')

#%% Generate Permit Count Bar Chart

def PermitCountStatsBarChart(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 5000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '200']
        cols = ['<100','100','101 - 199','200','>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
        cols = ['<90','90','91 - 149','150','>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    direct_all_ind = ~(mp['upgraded_panel_size'].isna())
    direct = mp.loc[direct_all_ind, ['panel_size_class','panel_size_existing']].groupby(['panel_size_class']).agg('count')
    direct.rename(columns = {'panel_size_existing': 'Direct'}, inplace = True)

    direct_dac_ind = ~(mp['upgraded_panel_size'].isna()) & (mp['dac'] == 'Yes')
    direct_dac = mp.loc[direct_dac_ind, ['panel_size_class','panel_size_existing']].groupby(['panel_size_class']).agg('count')
    direct_dac.rename(columns = {'panel_size_existing': 'Direct (DAC)'}, inplace = True)

    direct_nondac_ind = ~(mp['upgraded_panel_size'].isna()) & (mp['dac'] == 'No')
    direct_nondac = mp.loc[direct_nondac_ind, ['panel_size_class','panel_size_existing']].groupby(['panel_size_class']).agg('count')
    direct_nondac.rename(columns = {'panel_size_existing': 'Direct (non-DAC)'}, inplace = True)

    indirect_ind = (mp['main_panel_upgrade'] == 1) &  (mp['upgraded_panel_size'].isna())
    indirect = mp.loc[indirect_ind, ['panel_size_class','panel_size_existing']].groupby(['panel_size_class']).agg('count')
    indirect.rename(columns = {'panel_size_existing':'Indirect'}, inplace = True)

    inferred_ind = mp['permitted_panel_upgrade'] & ~(direct_all_ind) & ~(indirect_ind)
    inferred = mp.loc[inferred_ind, ['panel_size_class','panel_size_existing']].groupby(['panel_size_class']).agg('count')
    inferred.rename(columns = {'panel_size_existing':'Inferred'}, inplace = True)

    stats = pd.concat([direct, direct_dac, direct_nondac, indirect, inferred], axis = 1)

    out = stats.unstack(level = -1).reset_index()
    out.rename(columns = {
        'level_0':'kind',
        0:'count'}, inplace = True)
    out['pct'] = np.nan

    dir_all_ind = out['kind'] == 'Direct'
    dir_dac_ind = out['kind'] == 'Direct (DAC)'
    dir_nondac_ind = out['kind'] == 'Direct (non-DAC)'
    ind_ind = out['kind'] == 'Indirect'
    inf_ind = out['kind'] == 'Inferred'

    dir_all_totals = out.loc[dir_all_ind,'count'].sum()
    dir_dac_totals = out.loc[dir_dac_ind,'count'].sum()
    dir_nondac_totals = out.loc[dir_nondac_ind,'count'].sum()
    ind_totals = out.loc[ind_ind,'count'].sum()
    inf_totals = out.loc[inf_ind,'count'].sum()

    out.loc[dir_all_ind,'pct'] = out.loc[dir_all_ind,'count'] / dir_all_totals
    out.loc[dir_dac_ind,'pct'] = out.loc[dir_dac_ind,'count'] / dir_dac_totals
    out.loc[dir_nondac_ind,'pct'] = out.loc[dir_nondac_ind,'count'] / dir_nondac_totals
    out.loc[ind_ind,'pct'] = out.loc[ind_ind,'count'] / ind_totals
    out.loc[inf_ind,'pct'] = out.loc[inf_ind,'count'] / inf_totals

    out = out[['kind', 'panel_size_class', 'pct']].pivot(index = 'kind', columns = 'panel_size_class', values = 'pct')

    fig, ax = plt.subplots(1,1,figsize = (7,4))
    out[cols].plot(
        kind = 'bar',
        stacked = True,
        ax = ax,
        edgecolor='k')
    ax.vlines(x=[2.5], ymin=[0], ymax=[1], colors='k', ls='--', lw=2)

    ax.set_xticklabels([
        'Direct\nn=({})'.format(direct_all_ind.sum()),
        'Direct\n(DAC)\nn=({})'.format(direct_dac_ind.sum()),
        'Direct\n(non-DAC)\nn=({})'.format(direct_nondac_ind.sum()),
        'Indirect\nn=({})'.format(indirect_ind.sum()),
        'Inferred\nn=({})'.format(inferred_ind.sum())
        ])
    ax.tick_params(axis='x', labelrotation=0)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax.set_ylabel('Share of {} buildings'.format(sector.replace('_', '-')))
    ax.set_xlabel('\nPanel upgrade permit observation type')
    ax.set_yticks(np.arange(0,1.1,0.1))
    ax.set_ylim(0,1)
    ax.set_axisbelow(True)
    ax.grid(True)

    for c in ax.containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax.bar_label(c, labels=labels, label_type='center')

    fig.tight_layout()

    return fig, ax

#%% Generate Permit Count Stats Bar Chart

fig, ax = PermitCountStatsBarChart(sf, 'single_family')
fig.savefig(figure_dir + 'single_family_permit_count_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

fig, ax = PermitCountStatsBarChart(mf, 'multi_family')
fig.savefig(figure_dir + 'multi_family_permit_count_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

#%% Generate Dac vs. NonDAC percentage bar charts

def DACPanelStatsBarChart(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '200']
        cols = ['<100','100','101 - 199','200','>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
        cols = ['<90','90','91 - 149','150','>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()
    stats = mp[['panel_size_class','dac','panel_size_existing']].groupby(['panel_size_class', 'dac'],
        observed = False).agg('count')
    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    totals = mp.loc[~mp['panel_size_existing'].isna(),'dac'].to_frame().groupby('dac').value_counts()
    stats['pct'] = stats['count'].divide(totals)
    stats.reset_index(inplace = True)
    out = stats.pivot(index='dac', columns='panel_size_class', values='pct')

    fig, ax = plt.subplots(1,1,figsize = (4,4))
    out[cols].plot(
        kind='bar',
        stacked=True,
        ax = ax,
        edgecolor='k')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax.set_xlabel('DAC')
    ax.set_ylabel('Share of {} buildings'.format(sector.replace('_', '-')))
    ax.set_yticks(np.arange(0,1.1,0.1))
    ax.set_ylim(0,1)
    ax.set_axisbelow(True)
    ax.grid(True)

    for c in ax.containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax.bar_label(c, labels=labels, label_type='center')

    fig.tight_layout()

    return fig, ax

#%% Generate Data Panel Stats Bar Chart

fig, ax = DACPanelStatsBarChart(sf, 'single_family')
fig.savefig(figure_dir + 'single_family_dac_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

fig, ax = DACPanelStatsBarChart(mf, 'multi_family')
fig.savefig(figure_dir + 'multi_family_dac_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

#%% Generate Vintage Binned Panel Size Ranges

def VintagePanelStatsBarChart(mp, sector):

    bins = [0, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 3000]
    labels = ['<1930', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '>2010']

    mp['vintage_class'] = pd.cut(mp['YearBuilt'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
        cols = ['<100','100','101 - 199','200','>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
        cols = ['<90','90','91 - 149','150','>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    stats = mp[['vintage_class','panel_size_class', 'panel_size_existing']].groupby(['vintage_class','panel_size_class'],
        observed = False).agg('count')

    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    stats.reset_index(inplace = True)
    totals = stats.loc[:,['vintage_class','count']].groupby('vintage_class').agg('sum')

    stats = pd.merge(stats, totals, left_on = 'vintage_class', right_on = 'vintage_class')
    stats['pct'] = stats['count_x'] / stats['count_y']
    out = stats.pivot(index='vintage_class', columns='panel_size_class', values='pct')
    out = out.loc[:,cols]

    fig, ax = plt.subplots(2,1,figsize = (7,5), sharex = True, gridspec_kw={'height_ratios': [3, 1]})
    out[cols].plot(
        kind='bar',
        stacked=True,
        ax = ax[0],
        edgecolor = 'k')

    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].legend(handles[::-1], labels[::-1],loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax[0].set_ylabel('Share of \n{} buildings'.format(sector.replace('_', '-')))
    ax[0].set_yticks(np.arange(0,1.1,0.1))
    ax[0].set_ylim(0,1)
    ax[0].set_axisbelow(True)
    ax[0].grid(True)

    for c in ax[0].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[0].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    tot = totals.divide(totals.sum())

    tot.plot(
        kind = 'bar',
        color = 'lightgray',
        legend = False,
        ax = ax[1],
        edgecolor = 'k')

    ax[1].set_ylabel('Share of \ncategory')
    ax[1].tick_params(axis='x')
    ax[1].set_xlabel('Vintage')
    ax[1].set_axisbelow(True)
    ax[1].grid(True)

    for c in ax[1].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[1].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    fig.tight_layout()

    return fig, ax

#%% Generate Plot

fig, ax = VintagePanelStatsBarChart(sf, 'single_family')
fig.savefig(figure_dir + 'single_family_vintage_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

fig, ax = VintagePanelStatsBarChart(mf, 'multi_family')
fig.savefig(figure_dir + 'multi_family_vintage_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

#%% Generate SqFt Binned Panel Size Ranges

def SqftPanelStatsBarChart(mp, sector):

    if sector == 'single_family':
        bins = [0, 500, 750, 1000, 1250, 1500, 2000, 2500, 3000, 4000, 1000000]
        labels = ['0-499', '500-749', '750-999', '1000-1249', '1250-1499', '1500-1999', '2000-2499', '2500-2999', '3000-3999', '>4000']
    elif sector == 'multi_family':
        bins = [0, 2000, 3000, 4000, 6000, 8000, 10000, 20000, 30000, 40000, 10000000]
        labels = ['0-1999', '2000-2999', '3000-3999', '4000-5999', '6000-7999', '8000-9999', '10000-19999', '20000-29999', '30000-39999', '>40000']

    mp['size_class'] = pd.cut(mp['TotalBuildingAreaSqFt'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
        cols = ['<100','100','101 - 199','200','>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
        cols = ['<90','90','91 - 149','150','>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    stats = mp[['size_class','panel_size_class', 'panel_size_existing']].groupby(['size_class','panel_size_class'],
        observed = False).agg('count')

    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    stats.reset_index(inplace = True)
    totals = stats.loc[:,['size_class','count']].groupby('size_class').agg('sum')

    stats = pd.merge(stats, totals, left_on = 'size_class', right_on = 'size_class')
    stats['pct'] = stats['count_x'] / stats['count_y']
    out = stats.pivot(index='size_class', columns='panel_size_class', values='pct')
    out = out.loc[:,cols]

    fig, ax = plt.subplots(2,1,figsize = (7,5), sharex = True, gridspec_kw={'height_ratios': [3, 1]})
    out[cols].plot(
        kind='bar',
        stacked=True,
        ax = ax[0],
        edgecolor = 'k')

    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].legend(handles[::-1], labels[::-1],loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax[0].set_ylabel('Share of \n{} buildings'.format(sector.replace('_', '-')))
    ax[0].set_yticks(np.arange(0,1.1,0.1))
    ax[0].set_ylim(0,1)
    ax[0].set_axisbelow(True)
    ax[0].grid(True)

    for c in ax[0].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[0].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    tot = totals.divide(totals.sum())

    tot.plot(
        kind = 'bar',
        color = 'lightgray',
        legend = False,
        ax = ax[1],
        edgecolor = 'k')

    ax[1].set_ylabel('Share of \ncategory')
    ax[1].tick_params(axis='x', labelrotation=90)
    ax[1].set_xlabel('Size')
    ax[1].set_axisbelow(True)
    ax[1].grid(True)

    for c in ax[1].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[1].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    fig.tight_layout()

    return fig, ax

#%% Generate Sqft Panel Bar Chart

fig, ax = SqftPanelStatsBarChart(sf, 'single_family')
fig.savefig(figure_dir + 'single_family_sqft_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

fig, ax = SqftPanelStatsBarChart(mf, 'multi_family')
fig.savefig(figure_dir + 'multi_family_sqft_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

#%% Generate Aggregations by Renter Household Pct

def RenterPanelStatsBarChart(mp, sector):

    bins = [0, .10, .20, .30, .40, .50, .60, .70, .80, .90, 1.00]
    labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-100']

    mp['size_class'] = pd.cut(mp['renterhouseholdspct'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
        cols = ['<100','100','101 - 199','200','>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
        cols = ['<90','90','91 - 149','150','>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    stats = mp[['size_class','panel_size_class', 'panel_size_existing']].groupby(['size_class','panel_size_class'],
        observed = False).agg('count')

    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    stats.reset_index(inplace = True)
    totals = stats.loc[:,['size_class','count']].groupby('size_class').agg('sum')

    stats = pd.merge(stats, totals, left_on = 'size_class', right_on = 'size_class')
    stats['pct'] = stats['count_x'] / stats['count_y']
    out = stats.pivot(index='size_class', columns='panel_size_class', values='pct')
    out = out.loc[:,cols]

    fig, ax = plt.subplots(2,1,figsize = (7,5), sharex = True, gridspec_kw={'height_ratios': [3, 1]})
    out[cols].plot(
        kind='bar',
        stacked=True,
        ax = ax[0],
        edgecolor = 'k')

    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].legend(handles[::-1], labels[::-1],loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax[0].set_ylabel('Share of \n{} buildings'.format(sector.replace('_', '-')))
    ax[0].set_yticks(np.arange(0,1.1,0.1))
    ax[0].set_ylim(0,1)
    ax[0].set_axisbelow(True)
    ax[0].grid(True)

    for c in ax[0].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[0].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    tot = totals.divide(totals.sum())

    tot.plot(
        kind = 'bar',
        color = 'lightgray',
        legend = False,
        ax = ax[1],
        edgecolor = 'k')

    ax[1].set_ylabel('Share of \ncategory')
    ax[1].tick_params(axis='x', labelrotation=90)
    ax[1].set_xlabel('Renter Household Percentage')
    ax[1].set_axisbelow(True)
    ax[1].grid(True)

    for c in ax[1].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[1].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    fig.tight_layout()

    return fig, ax

#%% Generate Renter Household Percentage Plots

RenterPanelStatsBarChart(sf, 'single_family')
fig.savefig(figure_dir + 'single_family_renter_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

RenterPanelStatsBarChart(mf, 'multi_family')
fig.savefig(figure_dir + 'multifamily_renter_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

#%% Generate Aggregations by Renter Household Pct

def ClimateZonePanelStatsBarChart(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
        cols = ['<100','100','101 - 199','200','>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
        cols = ['<90','90','91 - 149','150','>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    stats = mp[['bzone','panel_size_class', 'panel_size_existing']].groupby(['bzone','panel_size_class'],
        observed = False).agg('count')

    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    stats.reset_index(inplace = True)
    totals = stats.loc[:,['bzone','count']].groupby('bzone').agg('sum')

    stats = pd.merge(stats, totals, left_on = 'bzone', right_on = 'bzone')
    stats['pct'] = stats['count_x'] / stats['count_y']
    out = stats.pivot(index='bzone', columns='panel_size_class', values='pct')
    out = out.loc[:,cols]

    fig, ax = plt.subplots(2,1,figsize = (10,5), sharex = True, gridspec_kw={'height_ratios': [3, 1]})
    out[cols].plot(
        kind='bar',
        stacked=True,
        ax = ax[0],
        edgecolor = 'k')

    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].legend(handles[::-1], labels[::-1],loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax[0].set_ylabel('Share of \n{} buildings'.format(sector.replace('_', '-')))
    ax[0].set_yticks(np.arange(0,1.1,0.1))
    ax[0].set_ylim(0,1)
    ax[0].set_axisbelow(True)
    ax[0].grid(True)

    for c in ax[0].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[0].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    tot = totals.divide(totals.sum())

    tot.plot(
        kind = 'bar',
        color = 'lightgray',
        legend = False,
        ax = ax[1],
        edgecolor = 'k')

    ax[1].set_ylabel('Share of \ncategory')
    ax[1].tick_params(axis='x', labelrotation=90)
    ax[1].set_xlabel('Building Climate Zone')
    ax[1].set_axisbelow(True)
    ax[1].grid(True)

    for c in ax[1].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[1].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    fig.tight_layout()

    return fig, ax

#%% Generate Building Climate Zone Level Statistics

fig, ax = ClimateZonePanelStatsBarChart(sf, 'single_family')
fig.savefig(figure_dir + 'single_family_climate_zone_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

fig, ax = ClimateZonePanelStatsBarChart(mf, 'multi_family')
fig.savefig(figure_dir + 'multi_family_climate_zone_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

#%% Generate Aggregations by Renter Household Pct

def AirDistrictPanelStatsBarChart(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['<100', '100', '101 - 199', '101 - 199', '200', '>200', '>200']
        cols = ['<100','100','101 - 199','200','>200']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['<90', '90', '91 - 149', '91 - 149', '150', '>150', '>150']
        cols = ['<90','90','91 - 149','150','>150']

    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    stats = mp[['air_district','panel_size_class', 'panel_size_existing']].groupby(['air_district','panel_size_class'],
        observed = False).agg('count')

    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    stats.reset_index(inplace = True)
    totals = stats.loc[:,['air_district','count']].groupby('air_district').agg('sum')

    stats = pd.merge(stats, totals, left_on = 'air_district', right_on = 'air_district')
    stats['pct'] = stats['count_x'] / stats['count_y']
    out = stats.pivot(index='air_district', columns='panel_size_class', values='pct')
    out = out.loc[:,cols]

    fig, ax = plt.subplots(2,1,figsize = (14,5), sharex = True, gridspec_kw={'height_ratios': [3, 1]})
    out[cols].plot(
        kind='bar',
        stacked=True,
        ax = ax[0],
        edgecolor = 'k')

    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].legend(handles[::-1], labels[::-1],loc='center left', bbox_to_anchor=(1, 0.5), title = 'Panel capacity (A)')
    ax[0].set_ylabel('Share of \n{} buildings'.format(sector.replace('_', '-')))
    ax[0].set_yticks(np.arange(0,1.1,0.1))
    ax[0].set_ylim(0,1)
    ax[0].set_axisbelow(True)
    ax[0].grid(True)

    for c in ax[0].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[0].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    tot = totals.divide(totals.sum())

    tot.plot(
        kind = 'bar',
        color = 'lightgray',
        legend = False,
        ax = ax[1],
        edgecolor = 'k')

    ax[1].set_ylabel('Share of \ncategory')
    ax[1].tick_params(axis='x', labelrotation=90)
    ax[1].set_xlabel('Air District')
    ax[1].set_axisbelow(True)
    ax[1].grid(True)

    for c in ax[1].containers:

        # Optional: if the segment is small or 0, customize the labels
        labels = [str(int(np.round(v.get_height(),2)*100)) + '%' if v.get_height() > 0 else '' for v in c]

        # remove the labels parameter if it's not needed for customized labels
        ax[1].bar_label(c, fontsize = 6, labels=labels, label_type='center')

    fig.tight_layout()

    return fig, ax

#%% Generate Air District Disaggregated Results

fig, ax = AirDistrictPanelStatsBarChart(sf, 'single_family')
fig.savefig(figure_dir + 'single_family_air_district_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

fig, ax = AirDistrictPanelStatsBarChart(mf, 'multi_family')
fig.savefig(figure_dir + 'multi_family_air_district_panel_stats_bar_chart.png', bbox_inches = 'tight', dpi = 300)

#%% Generate CES-4.0 to Size and Vintage Correlations Plot

def CEStoVintageSqftCorrelationScatterPlot(mp):

    mp['ciscorep_rounded'] = mp['ciscorep'].round(0)

    median_size_by_ces = mp.groupby('ciscorep_rounded')['TotalBuildingAreaSqFt'].agg('median').reset_index()
    median_vintage_by_ces = mp.groupby('ciscorep_rounded')['YearBuilt'].agg('median').reset_index()

    fig, ax = plt.subplots(1, 2, figsize = (12,5))

    kws = {'facecolor': 'none'}

    sns.regplot(
        data = median_size_by_ces,
        x = 'ciscorep_rounded',
        y = 'TotalBuildingAreaSqFt',
        x_estimator = np.mean,
        order = 1,
        ax = ax[0],
        marker = '+',
        color = 'tab:red',
        fit_reg = True)
    sns.regplot(
        data = median_vintage_by_ces,
        x = 'ciscorep_rounded',
        y = 'YearBuilt',
        x_estimator = np.mean,
        order = 1,
        ax = ax[1],
        marker = '+',
        color = 'tab:green')

    ax[0].add_patch(Rectangle((75, 1000), 25, 1500,
        zorder = 0,
        facecolor = 'tab:orange',
        alpha = 0.25))
    ax[0].add_patch(Rectangle((0, 1000), 75, 1500,
        zorder = 0,
        facecolor = 'tab:blue',
        alpha = 0.25))
    ax[0].set_xlim(0,100)
    ax[0].set_ylim((median_size_by_ces['TotalBuildingAreaSqFt'].min()-50,
        median_size_by_ces['TotalBuildingAreaSqFt'].max()+50))

    ax[1].add_patch(Rectangle((75, 1000), 25, 1500,
        zorder = 0,
        facecolor = 'tab:orange',
        alpha = 0.25))
    ax[1].add_patch(Rectangle((0, 1000), 75, 1500,
        zorder = 0,
        facecolor = 'tab:blue',
        alpha = 0.25))
    ax[1].set_xlim(0,100)
    ax[1].set_ylim((median_vintage_by_ces['YearBuilt'].min()-2,
        median_vintage_by_ces['YearBuilt'].max()+2))

    ax[0].grid(True)
    ax[1].grid(True)

    ax[0].set_ylabel('Median Square Footage')
    ax[0].set_xlabel('CalEnviroScreen 4.0\nComposite Score Percentile')
    ax[1].set_ylabel('Median Vintage Year')
    ax[1].set_xlabel('CalEnviroScreen 4.0\nComposite Score Percentile')

    return fig, ax

#%% Generate Single-Family Correlation Plots

fig, ax = CEStoVintageSqftCorrelationScatterPlot(sf)
