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

sf = sf.loc[sf['YearBuilt'] <= 2024,:]
mf = mf.loc[mf['YearBuilt'] <= 2024,:]

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

#%% Generate Housing Statistics Table

def PrintHousingStatsTable(mp, sector):

    if sector == 'single_family':
        size_bins = [0, 1000, 2000, 3000, 4000, 5000, 8000, 10000, 20000, 1000000]
        year_bins = [0, 1950, 1978, 2010, 2023]
        data = mp.loc[:,['YearBuilt','TotalBuildingAreaSqFt']]
        data['size_bin'] = pd.cut(mp['TotalBuildingAreaSqFt'],
            bins = size_bins,
            ordered = True)
        data['year_bin'] = pd.cut(mp['YearBuilt'],
            bins = year_bins,
            ordered = True)
        stats = data.groupby(['year_bin', 'size_bin'],
            observed = True)['YearBuilt'].agg('count').unstack(level = [0])
    elif sector == 'multi_family':
        year_bins = [0, 1950, 1978, 2010, 2023]
        units_bins = [0, 10, 25, 50, 100, 250, 500, 1000, 10000]
        data = mp.loc[:,['YearBuilt','TotalNoOfUnits']]
        data['year_bin'] = pd.cut(mp['YearBuilt'],
            bins = year_bins,
            ordered = True)
        data['units_bin'] = pd.cut(mp['TotalNoOfUnits'],
            bins = units_bins,
            ordered = True)
        stats = data.groupby(['year_bin', 'units_bin'],
            observed = True)['YearBuilt'].agg('count').unstack(level = [0])

    print(stats)

    return stats

#%% Generate Housing Statistics Tables

sf_housing_stats = PrintHousingStatsTable(sf, 'single_family')
mf_housing_stats = PrintHousingStatsTable(mf, 'multi_family')

#%% Generate DAC Housing Statistics Table

def PrintDACHousingStatsTable(mp, sector):

    if sector == 'single_family':
        size_bins = [0, 1000, 2000, 3000, 4000, 5000, 8000, 10000, 20000, 1000000]
        year_bins = [0, 1950, 1978, 2010, 2023]
        data = mp.loc[:,['dac', 'YearBuilt', 'TotalBuildingAreaSqFt']]
        data['size_bin'] = pd.cut(mp['TotalBuildingAreaSqFt'],
            bins = size_bins,
            ordered = True)
        data['year_bin'] = pd.cut(mp['YearBuilt'],
            bins = year_bins,
            ordered = True)
        stats_init = data.groupby(['dac','year_bin', 'size_bin'],
            observed = True)['YearBuilt'].agg('count')
        stats = stats_init.unstack(level = [1, 0]).sort_index(level = [2,1])
    elif sector == 'multi_family':
        year_bins = [0, 1950, 1978, 2010, 2023]
        units_bins = [0, 3, 5, 10, 25, 50, 100, 250, 500, 1000]
        data = mp.loc[:,['dac', 'YearBuilt', 'TotalNoOfUnits']]
        data['year_bin'] = pd.cut(mp['YearBuilt'],
            bins = year_bins,
            ordered = True)
        data['units_bin'] = pd.cut(mp['TotalNoOfUnits'],
            bins = units_bins,
            ordered = True)
        stats_init = data.groupby(['dac','year_bin', 'units_bin'],
            observed = True)['YearBuilt'].agg('count')
        stats = stats_init.unstack(level = [1, 0]).sort_index(level = [2,1])

    print(stats)

    return stats

#%% Print DAC Housing Statistics Tables

sf_dac_stats = PrintDACHousingStatsTable(sf, 'single_family')
mf_dac_stats = PrintDACHousingStatsTable(mf, 'multi_family')

#%% Generate Panel Statistics Table

def PrintPanelStatsTable(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['0 - 99', '100', '101 - 199', '101 - 199', '200', '>201', '>201']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['0 - 89', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

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
        units['pct'] = units['TotalNoOfUnits'].divide(total_units).multiply(100.0)
        stats = pd.merge(stats, units, left_index = True, right_index = True)

    print(stats)

    return stats

#%% Print Panel Statistics Tables

# LBNL Results for Comparison
# Panel Amps	Count	Frequency
# <100	        5,068	9%
# 100	        15,090	26%
# 101-199	    12,185	21%
# 200	        19,109	33%
# >200	        5,915	10%

sf_stats = PrintPanelStatsTable(sf, 'single_family')
mf_stats = PrintPanelStatsTable(mf, 'multi_family')

#%% Generate DAC Panel Statistics Table

def PrintDACPanelStatsTable(mp, sector):

    if sector == 'single_family':
        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['0 - 99', '100', '101 - 199', '101 - 199', '200', '>201', '>201']
    elif sector == 'multi_family':
        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['0 - 89', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

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

#%% Plot Inferred Upgrades

def ObservedUpgradeRatingsBar(mp, sector, figure_dir):

    fig, ax = plt.subplots(1,1, figsize = (5,5))

    # Compute counts by sector

    if sector == 'single_family':
        obs_ind = mp['observed_panel_upgrade'] == True
        data = mp.loc[obs_ind,:]
        sm = data['panel_size_existing'] < 60.0
        data.loc[sm,'panel_size_existing'] = 60.0
        counts = data.groupby(['dac','panel_size_existing'])['observed_panel_upgrade'].agg('count')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Panel Rating \n[Amps]'
        xlabel = 'Number of Properties'
    elif sector == 'multi_family':
        obs_ind = mp['observed_panel_upgrade'] == True
        data = mp.loc[obs_ind,:]
        counts = data.groupby(['dac', 'panel_size_existing'])['TotalNoOfUnits'].agg('sum')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Load Center Rating per Unit \n[Amps]'
        xlabel = 'Number of Units'

    # Plot Counts

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(rotation = 45)
    ax.legend(title = 'DAC')

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + '{}_observed_upgrade_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

#%% Plot Inferred Upgrade Panel Ratings

ObservedUpgradeRatingsBar(sf, 'single_family', figure_dir)
ObservedUpgradeRatingsBar(mf, 'multi_family', figure_dir)

#%% Plot Inferred Upgrades

def InferredUpgradeRatingsBar(mp, sector, figure_dir):

    # Compute counts by sector

    if sector == 'single_family':
        inferred_ind = mp['inferred_panel_upgrade'] == True
        data = mp.loc[inferred_ind,:]
        counts = data.groupby(['dac','panel_size_existing'])['inferred_panel_upgrade'].agg('count')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Panel Rating \n[Amps]'
        xlabel = 'Number of Properties'
    elif sector == 'multi_family':
        inferred_ind = mp['inferred_panel_upgrade'] == True
        data = mp.loc[inferred_ind,:]
        counts = data.groupby(['dac', 'panel_size_existing'])['TotalNoOfUnits'].agg('sum')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Load Center Rating per Unit \n[Amps]'
        xlabel = 'Number of Units'

    # Plot Counts

    fig, ax = plt.subplots(1,1, figsize = (5,5))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(rotation = 45)
    ax.legend(title = 'DAC')

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + '{}_inferred_upgrade_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

#%% Plot Inferred Upgrade Panel Ratings

InferredUpgradeRatingsBar(sf, 'single_family', figure_dir)
InferredUpgradeRatingsBar(mf, 'multi_family', figure_dir)

#%% Plot as built panel size ratings

def AsBuiltPanelRatingsHist(mp, sector, figure_dir):
    '''Paired DAC / Non-DAC 2D histogram of panel sizes by building
    construction vintage years'''

    fig, ax = plt.subplots(1,2,figsize = (10,10), sharey = True)

    dac_ind = mp['dac'] == 'Yes'
    non_dac_ind = mp['dac'] == 'No'

    dac_sample = mp.loc[dac_ind,:]
    non_dac_sample = mp.loc[non_dac_ind,:]

    if sector == 'single_family':
        ylim = [0, 1220]
        yticks = [30, 60, 100, 125, 150, 200, 225, 320, 400, 600, 800, 1000, 1200]
        bins = 80
        ylabel = 'As-Built Panel Rating \n[Amps]'
        vmin = 0
        vmax = 1000000
    elif sector == 'multi_family':
        ylim = [0, 220]
        yticks = [30, 40, 60, 90, 100, 125, 150, 200]
        bins = 40
        ylabel = 'Average As-Built Load Center Rating Per Unit\n[Amps]'
        vmin = 0
        vmax = 10000

    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_as_built',
        data = dac_sample,
        color = 'tab:orange',
        ax = ax[0],
        bins = bins,
        legend = True,
        label = 'Priority Population',
        cbar = True,
        cbar_kws = {'label':'Number of Properties', 'orientation':'horizontal'},
        vmin = vmin,
        vmax = vmax)

    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_as_built',
        data = non_dac_sample,
        color = 'tab:blue',
        ax = ax[1],
        bins = bins,
        legend = True,
        label = 'Non-Priority Population',
        cbar = True,
        cbar_kws = {'label':'Number of Properties', 'orientation':'horizontal'},
        vmin = vmin,
        vmax = vmax)

    ax[0].set_yticks(yticks)

    ax[0].grid(True)
    ax[1].grid(True)

    ax[0].set_ylabel(ylabel)
    ax[1].set_ylabel('')

    ax[0].set_xlabel('Vintage \n[Year]')
    ax[1].set_xlabel('Vintage \n[Year]')

    ax[0].set_title('Priority Population')
    ax[1].set_title('Non-Priority Population')

    ax[0].set_ylim(ylim)
    ax[1].set_ylim(ylim)

    ax[0].set_xlim(1830, 2025)
    ax[1].set_xlim(1830, 2025)

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + '{}_as_built_panel_ratings_hist.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate As Built Panel Rating Hist

AsBuiltPanelRatingsHist(sf, 'single_family', figure_dir)
AsBuiltPanelRatingsHist(mf, 'multi_family', figure_dir)

#%% Plot As-Built Panel Stats

def AsBuiltPanelRatingsBar(mp, sector, figure_dir):
    '''Simple barplot of as-built panel ratings separated by DAC status'''

    # Compute counts by sector

    if sector == 'single_family':
        counts = mp.groupby(['dac', 'panel_size_as_built'])['panel_size_as_built'].agg('count')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'As-Built Panel Rating \n[Amps]'
        xlabel = 'Number of Properties'
    elif sector == 'multi_family':
        counts = mp.groupby(['dac', 'panel_size_as_built'])['TotalNoOfUnits'].agg('sum')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Average As-Built Load Center Rating per Unit \n[Amps]'
        xlabel = 'Number of Units'

    # Plot Counts

    fig, ax = plt.subplots(1,1, figsize = (5,5))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(rotation = 45)
    ax.legend(title = 'Priority Population')

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + '{}_as_built_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate As-Built Panel Ratings Bar Chart

AsBuiltPanelRatingsBar(sf, 'single_family', figure_dir)
AsBuiltPanelRatingsBar(mf, 'multi_family', figure_dir)

#%% Plot Cumulative Permit Counts

def PermitCountsBar(mp, sector, figure_dir):

    upgrade_stats = mp.loc[mp['permitted_panel_upgrade'] == True].groupby('dac')['panel_size_existing'].agg('count')
    upgrade_stats = pd.DataFrame(upgrade_stats).reset_index()

    fig, ax = plt.subplots(1, 1, figsize = (5,5), sharex = True)

    sns.barplot(data = upgrade_stats,
        y = 'panel_size_existing',
        x = 'dac',
        order = ['No','Yes'],
        label = ['No','Yes'],
        ax = ax)

    if sector == 'single_family':
        ylabel = 'Total Cumulative Panel Upgrade Permits'
    elif sector == 'multi_family':
        ylabel = 'Total Cumulative Load Center Upgrade Permits'

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Priority Population')
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.tight_layout()

    fig.savefig(figure_dir + '{}_cumulative_permit_count_barplot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Permit Count Barchart

PermitCountsBar(sf, 'single_family', figure_dir)
PermitCountsBar(mf, 'multi_family', figure_dir)

#%% Plot Existing panel size ratings

def ExistingPanelRatingsHist(mp, sector, figure_dir):
    '''Function to plot a set of 2d histograms relating the frequency of
    existing panel sizes to vintage year by dac status'''

    dac_ind = (mp['dac'] == 'Yes')
    non_dac_ind = (mp['dac'] == 'No')

    dac_sample = mp.loc[dac_ind,:]
    non_dac_sample = mp.loc[non_dac_ind,:]

    if sector == 'single_family':
        yticks = [30, 60, 100, 125, 150, 200, 225, 320, 400, 600, 800, 1000, 1200]
        ylim = (0, 1220)
        ylabel = 'Existing Panel Rating \n[Amps]'
        bins = 80
        vmin = 0
        vmax = 1000000
    elif sector == 'multi_family':
        yticks = [30, 40, 60, 90, 100, 125, 150, 200]
        ylim = (0, 220)
        ylabel = 'Existing Panel Rating per Unit \n[Amps]'
        bins = 40
        vmin = 0
        vmax = 10000

    fig, ax = plt.subplots(1,2,figsize = (10,10), sharey = True, sharex = True)

    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_existing',
        data = dac_sample,
        color = 'tab:orange',
        ax = ax[0],
        bins = bins,
        legend = True,
        label = 'Yes',
        cbar = True,
        cbar_kws = {'label': 'Number of Properties', 'orientation':'horizontal'},
        vmin = vmin,
        vmax = vmax)

    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_existing',
        data = non_dac_sample,
        color = 'tab:blue',
        ax = ax[1],
        bins = bins,
        legend = True,
        label = 'No',
        cbar = True,
        cbar_kws = {'label':'Number of Properties', 'orientation':'horizontal'},
        vmin = vmin,
        vmax = vmax)

    ax[0].set_yticks(yticks)

    ax[0].grid(True)
    ax[1].grid(True)

    ax[0].set_ylabel(ylabel)
    ax[1].set_ylabel('')

    ax[0].set_xlabel('Vintage \n[Year]')
    ax[1].set_xlabel('Vintage \n[Year]')

    ax[0].set_title('DAC')
    ax[1].set_title('Non-DAC')

    ax[0].set_ylim(ylim)
    ax[1].set_ylim(ylim)

    ax[0].set_xlim(1830, 2025)
    ax[1].set_xlim(1830, 2025)

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + '{}_existing_panel_ratings_hist.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Existing Panel Size Rating 2D-Histogram

ExistingPanelRatingsHist(sf, 'single_family', figure_dir)
ExistingPanelRatingsHist(mf, 'multi_family', figure_dir)

#%% Joint Distribution Plot

def JointDistributionPlot(mp, sector, figure_dir):

    mp['log_building_sqft'] = mp['TotalBuildingAreaSqFt'].apply(np.log10)

    if sector == 'single_family':

        fig = sns.jointplot(data = mp,
            x = 'YearBuilt',
            y = 'log_building_sqft',
            hue = 'dac',
            palette = ['tab:blue', 'tab:orange'],
            hue_order = ['No', 'Yes'],
            alpha = 0.05,
            marker = '.',
            linewidth = 0
            )
        plt.legend(title = 'DAC', loc='upper left')
        plt.xlim([1830, 2025])
        plt.ylim([2.0, 5.0])
        plt.yticks([2,3,4,5])
        fig.ax_joint.set_yticklabels(['100', '1,000', '10,000', '100,000'])
        fig.ax_joint.set_ylabel('Total Floor Area\n($ft^2$)')
        fig.ax_joint.set_xlabel('Construction Vintage\n(Year)')
        plt.grid()

    elif sector == 'multi_family':

        fig = sns.jointplot(data = mp,
            x = 'YearBuilt',
            y = 'log_building_sqft',
            hue = 'dac',
            palette = ['tab:blue', 'tab:orange'],
            hue_order = ['No', 'Yes'],
            alpha = 0.05,
            marker = '.',
            linewidth = 0
            )
        plt.legend(title = 'DAC', loc='upper left')
        plt.xlim([1860, 2025])
        plt.ylim([2.0, 6.0])
        plt.yticks([2,3,4,5,6])
        fig.ax_joint.set_yticklabels(['100', '1,000', '10,000', '100,000','1,000,000'])
        fig.ax_joint.set_ylabel('Total Floor Area\n($ft^2$)')
        fig.ax_joint.set_xlabel('Construction Vintage\n(Year)')
        plt.grid()

    fig.savefig(figure_dir + '{}_home_size_vintage_jointplot.png'.format(sector), dpi = 500, bbox_inches = 'tight')

    return

#%% Plot Home Size Vintage Jointplot

JointDistributionPlot(sf, 'single_family', figure_dir)
JointDistributionPlot(mf, 'multi_family', figure_dir)

#%% Plot Existing Panel Stats

def ExistingPanelRatingsBar(mp, sector, figure_dir):
    '''Simple barplot of existing panel ratings separated by DAC status'''

    # Compute counts
    if sector == 'single_family':
        counts = mp.groupby(['dac', 'panel_size_existing'])['sampled'].agg('count')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Panel Rating \n[Amps]'
        xlabel = 'Number of Properties'

    elif sector == 'multi_family':
        counts = mp.groupby(['dac', 'panel_size_existing'])['TotalNoOfUnits'].agg('sum')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Panel Rating per Unit \n[Amps]'
        xlabel = 'Number of Units'

    # Plot Counts
    fig, ax = plt.subplots(1,1, figsize = (5,5))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(rotation = 45)
    ax.legend(title = 'DAC')

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + '{}_existing_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Existing Panel Ratings Bar Chart

ExistingPanelRatingsBar(sf, 'single_family', figure_dir)
ExistingPanelRatingsBar(mf, 'multi_family', figure_dir)

#%% Plot Normalized Amps per Sqft for Upgraded and Non-Upgraded Subsets

def AreaNormalizedComparisonKDE(mp, sector, figure_dir):

    if sector == 'single_family':

        # SF plot data

        mp['building_sqft_log10'] = np.log10(mp['TotalBuildingAreaSqFt'])
        mp['existing_amps_per_sqft_log10'] = np.log10(mp['panel_size_existing'] / mp['TotalBuildingAreaSqFt'])

        non_dacs_ind = mp['dac'] == 'No'
        dacs_ind = mp['dac'] == 'Yes'

        non_dacs = mp.loc[non_dacs_ind,:]
        dacs = mp.loc[dacs_ind,:]

        # Generate SF Plot

        bw = 0.75

        fig1 = sns.jointplot(data = non_dacs,
            x = 'building_sqft_log10',
            y = 'existing_amps_per_sqft_log10',
            hue = 'permitted_panel_upgrade',
            palette = ['lightblue', 'tab:blue'],
            kind = 'kde',
            bw_method = bw)

        upgrade_ind = non_dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = non_dacs['permitted_panel_upgrade'] == False

        fig1.ax_joint.axhline(non_dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'tab:blue', linestyle = ':')
        fig1.ax_joint.axvline(non_dacs.loc[upgrade_ind, 'building_sqft_log10'].mean(), color = 'tab:blue', linestyle = ':')

        fig1.ax_joint.axhline(non_dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'lightblue', linestyle = ':')
        fig1.ax_joint.axvline(non_dacs.loc[non_upgrade_ind, 'building_sqft_log10'].mean(), color = 'lightblue', linestyle = ':')

        ylim = (-2.0, 0.0)
        yticks = [-2, -1, 0]
        ytick_labels = ['0.01', '0.1', '1.0']

        xlim = (2.0, 4.0)
        xticks = [2, 3, 4]
        xtick_labels = ['100', '1,000', '10,000']

        fig1.ax_marg_x.set_xlim(xlim)
        fig1.ax_marg_x.set_xticks(xticks)
        fig1.ax_marg_x.set_xticklabels(xtick_labels)
        fig1.ax_joint.set_xlabel('Property Size\n [$ft^2$]')

        fig1.ax_marg_y.set_ylim(ylim)
        fig1.ax_marg_y.set_yticks(yticks)
        fig1.ax_marg_y.set_yticklabels(ytick_labels)
        fig1.ax_joint.set_ylabel('Rated Panel Capacity\n [$Amps / ft^2$]')

        fig2 = sns.jointplot(data = dacs,
            x = 'building_sqft_log10',
            y = 'existing_amps_per_sqft_log10',
            hue = 'permitted_panel_upgrade',
            palette = ['navajowhite', 'tab:orange'],
            kind = 'kde',
            bw_method = bw)

        upgrade_ind = dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = (dacs['permitted_panel_upgrade'] == False) & ~(np.isinf(dacs['existing_amps_per_sqft_log10']))

        fig2.ax_joint.axhline(dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'tab:orange', linestyle = ':')
        fig2.ax_joint.axvline(dacs.loc[upgrade_ind, 'building_sqft_log10'].mean(), color = 'tab:orange', linestyle = ':')

        fig2.ax_joint.axhline(dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'navajowhite', linestyle = ':')
        fig2.ax_joint.axvline(dacs.loc[non_upgrade_ind, 'building_sqft_log10'].mean(), color = 'navajowhite', linestyle = ':')

        fig2.ax_marg_x.set_xlim(xlim)
        fig2.ax_marg_x.set_xticks(xticks)
        fig2.ax_marg_x.set_xticklabels(xtick_labels)
        fig2.ax_joint.set_xlabel('Property Size\n [$ft^2$]')

        fig2.ax_marg_y.set_ylim(ylim)
        fig2.ax_marg_y.set_yticks(yticks)
        fig2.ax_marg_y.set_yticklabels(ytick_labels)
        fig2.ax_joint.set_ylabel('Rated Panel Capacity\n [$Amps / ft^2$]')

        fig1.savefig(figure_dir + '{}_non_dac_permitted_upgrade_amps_per_sqft_jointplot.png'.format(sector), bbox_inches = 'tight', dpi = 500)
        fig2.savefig(figure_dir + '{}_dac_permitted_upgrade_amps_per_sqft_jointplot.png'.format(sector), bbox_inches = 'tight', dpi = 500)

        # Print SF Stats

        upgrade_ind = dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = (dacs['permitted_panel_upgrade'] == False) & ~(np.isinf(dacs['existing_amps_per_sqft_log10']))

        print(dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean())
        print(dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean())

        upgrade_ind = non_dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = (non_dacs['permitted_panel_upgrade'] == False) & ~(np.isinf(non_dacs['existing_amps_per_sqft_log10']))

        print(non_dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean())
        print(non_dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean())

    elif sector == 'multi_family':

        # MF plot data

        buildings_ces['avg_unit_sqft_log10'] = np.log10(buildings_ces['avg_unit_sqft'])
        buildings_ces['existing_amps_per_sqft_log10'] = np.log10(buildings_ces['panel_size_existing'] / mp['avg_unit_sqft'])

        non_dacs_ind = buildings_ces['dac_status'] == 'Non-DAC'
        dacs_ind = buildings_ces['dac_status'] == 'DAC'

        non_dacs = buildings_ces.loc[non_dacs_ind,:]
        dacs = buildings_ces.loc[dacs_ind,:]

        # Generate MF Plots

        bw = 0.75

        fig1 = sns.jointplot(data = non_dacs,
            x = 'avg_unit_sqft_log10',
            y = 'existing_amps_per_sqft_log10',
            hue = 'permitted_panel_upgrade',
            palette = ['lightblue', 'tab:blue'],
            kind = 'kde',
            bw_method = bw)

        upgrade_ind = non_dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = non_dacs['permitted_panel_upgrade'] == False

        fig1.ax_joint.axhline(non_dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'tab:blue', linestyle = ':')
        fig1.ax_joint.axvline(non_dacs.loc[upgrade_ind, 'avg_unit_sqft_log10'].mean(), color = 'tab:blue', linestyle = ':')

        fig1.ax_joint.axhline(non_dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'lightblue', linestyle = ':')
        fig1.ax_joint.axvline(non_dacs.loc[non_upgrade_ind, 'avg_unit_sqft_log10'].mean(), color = 'lightblue', linestyle = ':')

        ylim = (-2.0, 0.0)
        yticks = [-2, -1, 0]
        ytick_labels = ['0.01', '0.1', '1.0']

        xlim = (2.0, 4.0)
        xticks = [2, 3, 4]
        xtick_labels = ['100', '1,000', '10,000']

        fig1.ax_marg_x.set_xlim(xlim)
        fig1.ax_marg_x.set_xticks(xticks)
        fig1.ax_marg_x.set_xticklabels(xtick_labels)
        fig1.ax_joint.set_xlabel('Average Unit Size\n [$ft^2$]')

        fig1.ax_marg_y.set_ylim(ylim)
        fig1.ax_marg_y.set_yticks(yticks)
        fig1.ax_marg_y.set_yticklabels(ytick_labels)
        fig1.ax_joint.set_ylabel('Rated Panel Capacity\n [$Amps / ft^2$]')

        fig2 = sns.jointplot(data = dacs,
            x = 'avg_unit_sqft_log10',
            y = 'existing_amps_per_sqft_log10',
            hue = 'permitted_panel_upgrade',
            palette = ['navajowhite', 'tab:orange'],
            kind = 'kde',
            bw_method = bw)

        upgrade_ind = dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = (dacs['permitted_panel_upgrade'] == False) & ~(np.isinf(dacs['existing_amps_per_sqft_log10']))

        fig2.ax_joint.axhline(dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'tab:orange', linestyle = ':')
        fig2.ax_joint.axvline(dacs.loc[upgrade_ind, 'avg_unit_sqft_log10'].mean(), color = 'tab:orange', linestyle = ':')

        fig2.ax_joint.axhline(dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean(), color = 'navajowhite', linestyle = ':')
        fig2.ax_joint.axvline(dacs.loc[non_upgrade_ind, 'avg_unit_sqft_log10'].mean(), color = 'navajowhite', linestyle = ':')

        fig2.ax_marg_x.set_xlim(xlim)
        fig2.ax_marg_x.set_xticks(xticks)
        fig2.ax_marg_x.set_xticklabels(xtick_labels)
        fig2.ax_joint.set_xlabel('Average Unit Size\n [$ft^2$]')

        fig2.ax_marg_y.set_ylim(ylim)
        fig2.ax_marg_y.set_yticks(yticks)
        fig2.ax_marg_y.set_yticklabels(ytick_labels)
        fig2.ax_joint.set_ylabel('Rated Panel Capacity\n [$Amps / ft^2$]')

        fig1.savefig(figure_dir + 'multi_family_non_dac_permitted_upgrade_amps_per_sqft_jointplot.png', bbox_inches = 'tight', dpi = 500)
        fig2.savefig(figure_dir + 'multi_family_dac_permitted_upgrade_amps_per_sqft_jointplot.png', bbox_inches = 'tight', dpi = 500)

        # Print MF Stats

        upgrade_ind = dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = (dacs['permitted_panel_upgrade'] == False) & ~(np.isinf(dacs['existing_amps_per_sqft_log10']))

        print(dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean())
        print(dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean())

        upgrade_ind = non_dacs['permitted_panel_upgrade'] == True
        non_upgrade_ind = (non_dacs['permitted_panel_upgrade'] == False) & ~(np.isinf(non_dacs['existing_amps_per_sqft_log10']))

        print(non_dacs.loc[upgrade_ind, 'existing_amps_per_sqft_log10'].mean())
        print(non_dacs.loc[non_upgrade_ind, 'existing_amps_per_sqft_log10'].mean())

    return

#%% Generate Area Normalized KDE and Stats

# CAUTION - Long run time...
#AreaNormalizedComparisonKDE(sf, 'single_family', figure_dir)
#AreaNormalizedComparisonKDE(mf, 'multi_family', figure_dir)

#%% Distribution of Destination Panel Sizes for Permitted Upgrades

def PermittedUpgradePanelSizeDistribution(mp, sector, figure_dir):

    perm_ind = ~mp['upgraded_panel_size'].isna()

    data = mp.loc[perm_ind, ['dac','panel_size_existing']]

    counts = data.groupby(['dac','panel_size_existing'])['panel_size_existing'].agg('count')
    counts = counts.unstack(level= 0)
    counts.index = counts.index.astype(int)

    fig, ax = plt.subplots(1,1,figsize=(5,5))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.set_ylabel('Upgraded Panel Size')
    ax.set_xlabel('Number of Properties')
    ax.grid(True)
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.legend(title = 'DAC')

    plt.xticks(rotation = 45)

    fig.savefig(figure_dir + '{}_permitted_upgrade_panel_size_distribution.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Permitted Panel Upgrade Distribution Plot

PermittedUpgradePanelSizeDistribution(sf, 'single_family', figure_dir)
PermittedUpgradePanelSizeDistribution(mf, 'multi_family', figure_dir)

#%% Distribution of Destination Panel Sizes for Inferred Upgrades

def InferredUpgradePanelSizeDistribution(mp, sector, figure_dir):

    infer_ind = mp['inferred_panel_upgrade'] == True

    data = mp.loc[infer_ind, ['dac','panel_size_existing']]

    counts = data.groupby(['dac','panel_size_existing'])['panel_size_existing'].agg('count')
    counts = counts.unstack(level= 0)
    counts.index = counts.index.astype(int)

    fig, ax = plt.subplots(1,1,figsize=(5,5))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.set_ylabel('Upgraded Panel Size')
    ax.set_xlabel('Number of Properties')
    ax.grid(True)
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax.legend(title = 'DAC')

    plt.xticks(rotation = 45)

    fig.savefig(figure_dir + '{}_inferred_upgrade_panel_size_distribution.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Inferred Panel Upgrade Distribution Plot

InferredUpgradePanelSizeDistribution(sf, 'single_family', figure_dir)
InferredUpgradePanelSizeDistribution(mf, 'multi_family', figure_dir)

#%% Generate Maps by Air District

def PlotLikelyUpgradeRequirementsByAirDistrict(mp, sector, figure_dir, air_districts):

    # Mask counties with insufficient counts
    mask = mp.groupby('air_district')['panel_size_existing'].agg('count')
    mask.loc[mask < 100] = np.nan
    mask = mask[mask.isna()].index.values

    # Generate Air District Upgrade Needs Map
    air_district_stats = mp.groupby(['air_district','panel_size_existing', 'dac'])['panel_size_existing'].agg('count')
    air_district_stats = air_district_stats.to_frame()
    air_district_stats.rename(columns = {'panel_size_existing':'counts'}, inplace = True)
    air_district_stats.reset_index(inplace = True)

    # Drop masked counties
    drop_ind = air_district_stats.loc[air_district_stats['air_district'].isin(mask)].index
    air_district_stats.drop(drop_ind, inplace = True)

    if sector == 'single_family':

        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['0 - 99', '100', '101 - 199', '101 - 199', '200', '>201', '>201']

    elif sector == 'multi_family':

        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['0 - 89', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

    air_district_stats['panel_size_class'] = pd.cut(air_district_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    if sector == 'single_family':

        bins = [0, 99, 199, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    elif sector == 'multi_family':

        bins = [0, 89, 149, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    air_district_stats['upgrade_required'] = pd.cut(air_district_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    # Compute Upgrade Requirement Stats

    air_district_upgrade_requirements = air_district_stats.groupby(['air_district','dac','upgrade_required'])['counts'].agg('sum').to_frame()
    air_district_upgrade_requirements['percentage'] = air_district_upgrade_requirements.divide(air_district_upgrade_requirements.groupby(['air_district', 'dac']).agg('sum')).multiply(100.).round(2)

    # Merge Stats with Air District Boundaries

    dac_air_district_likely_upgrades = air_district_upgrade_requirements.loc(axis=0)[:,'Yes','Likely'].reset_index()
    non_dac_air_district_likely_upgrades = air_district_upgrade_requirements.loc(axis=0)[:,'No','Likely'].reset_index()

    # Merge on Spatial Data

    dac_air_district_data = air_districts[['geom','name']].merge(dac_air_district_likely_upgrades, left_on = 'name', right_on = 'air_district')
    non_dac_air_district_data = air_districts[['geom','name']].merge(non_dac_air_district_likely_upgrades, left_on = 'name', right_on = 'air_district')

    # Generate plot elements

    fig, ax = plt.subplots(2,2, figsize = (30,30))
    ax = ax.ravel()
    fs = 8

    # Plot DAC Counts

    air_districts.boundary.plot(
        ax = ax[0],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [100, 1000, 10000, 100000, 1000000]
    labels = ['0 - 100', '100 - 1,000', '1,000 - 10,000', '10,000 - 100,000','100,000 - 1,000,000']

    dac_air_district_data.plot(ax = ax[0],
        column = 'counts',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Counts',
            'labels': labels,
            'loc':'best'})

    ax[0].set_title('Count of DAC\n {} Properties \n Likely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = dac_air_district_data[['geom','counts']].copy()
    centroids['geom'] = dac_air_district_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['counts'] = centroids['counts'].map(str)

    centroids.apply(lambda x: ax[0].annotate(
        text=x['counts'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[0].axis('Off')

    # Plot DAC Percentages

    air_districts.boundary.plot(
        ax = ax[1],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [10, 20, 30, 40]
    labels = ['0 - 10', '10 - 20', '20 - 30', '30 - 40']

    dac_air_district_data.plot(ax = ax[1],
        column = 'percentage',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Percentages',
            'labels': labels,
            'loc':'best'})

    ax[1].set_title('Percentage of DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = dac_air_district_data[['geom','percentage']].copy()
    centroids['geom'] = dac_air_district_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['percentage'] = centroids['percentage'].map(str)

    centroids.apply(lambda x: ax[1].annotate(
        text=x['percentage'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[1].axis('Off')

    # Plot Non-DAC Counts

    air_districts.boundary.plot(
        ax = ax[2],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [100, 1000, 10000, 100000, 1000000]
    labels = ['0 - 100', '100 - 1,000', '1,000 - 10,000', '10,000 - 100,000','100,000 - 1,000,000']

    non_dac_air_district_data.plot(ax = ax[2],
        column = 'counts',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Counts',
            'labels': labels,
            'loc':'best'})

    ax[2].set_title('Count of Non-DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = non_dac_air_district_data[['geom','counts']].copy()
    centroids['geom'] = non_dac_air_district_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['counts'] = centroids['counts'].map(str)

    centroids.apply(lambda x: ax[2].annotate(
        text=x['counts'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[2].axis('Off')

    # Plot Non-DAC Percentages

    air_districts.boundary.plot(
        ax = ax[3],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [10, 20, 30, 40]
    labels = ['0 - 10', '10 - 20', '20 - 30', '30 - 40']

    non_dac_air_district_data.plot(ax = ax[3],
        column = 'percentage',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Percentages',
            'labels': labels,
            'loc':'best'})

    ax[3].set_title('Percentage of Non-DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = non_dac_air_district_data[['geom','percentage']].copy()
    centroids['geom'] = non_dac_air_district_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['percentage'] = centroids['percentage'].map(str)

    centroids.apply(lambda x: ax[3].annotate(
        text=x['percentage'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[3].axis('Off')

    fig.savefig(figure_dir + '{}_likely_panel_ugprade_requirements_by_air_district.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return air_district_upgrade_requirements

#%% Generate Upgrade Requirements

sf_air_district_upgrade_requirements = PlotLikelyUpgradeRequirementsByAirDistrict(sf, 'single_family', figure_dir, air_districts)
mf_air_district_upgrade_requirements = PlotLikelyUpgradeRequirementsByAirDistrict(sf, 'multi_family', figure_dir, air_districts)

#%% Plot Total Counts and Percentages by County District Basin Boundaries

def PlotLikelyUpgradeRequirementsByCDB(mp, sector, figure_dir, county_air_basin_districts):

    # Mask counties with insufficient counts
    mask = mp.groupby( 'county_air_basin_district_id')['panel_size_existing'].agg('count')
    mask.loc[mask < 100] = np.nan
    mask = mask[mask.isna()].index.values

    # Generate Air District Upgrade Needs Map
    cdb_stats = mp.groupby(['county_air_basin_district_id','panel_size_existing', 'dac'])['panel_size_existing'].agg('count')
    cdb_stats = cdb_stats.to_frame()
    cdb_stats.rename(columns = {'panel_size_existing':'counts'}, inplace = True)
    cdb_stats.reset_index(inplace = True)

    # Drop masked counties
    drop_ind = cdb_stats.loc[cdb_stats['county_air_basin_district_id'].isin(mask)].index
    cdb_stats.drop(drop_ind, inplace = True)

    if sector == 'single_family':

        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['0 - 99', '100', '101 - 199', '101 - 199', '200', '>201', '>201']

    elif sector == 'multi_family':

        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['0 - 89', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

    cdb_stats['panel_size_class'] = pd.cut(cdb_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    if sector == 'single_family':

        bins = [0, 99, 199, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    elif sector == 'multi_family':

        bins = [0, 89, 149, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    cdb_stats['upgrade_required'] = pd.cut(cdb_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    # Compute Upgrade Requirement Stats

    cdb_upgrade_requirements = cdb_stats.groupby(['county_air_basin_district_id','dac','upgrade_required'])['counts'].agg('sum').to_frame()
    cdb_upgrade_requirements['percentage'] = cdb_upgrade_requirements.divide(cdb_upgrade_requirements.groupby(['county_air_basin_district_id', 'dac']).agg('sum')).multiply(100.).round(2)

    # Merge Stats with Air District Boundaries

    dac_cdb_likely_upgrades = cdb_upgrade_requirements.loc(axis=0)[:,'Yes','Likely'].reset_index()
    non_dac_cdb_likely_upgrades = cdb_upgrade_requirements.loc(axis=0)[:,'No','Likely'].reset_index()

    # Merge on Spatial Data

    dac_cdb_data = county_air_basin_districts[['geom','coabdis_id',]].merge(dac_cdb_likely_upgrades, left_on = 'coabdis_id', right_on = 'county_air_basin_district_id')
    non_dac_cdb_data = county_air_basin_districts[['geom','coabdis_id',]].merge(non_dac_cdb_likely_upgrades, left_on = 'coabdis_id', right_on = 'county_air_basin_district_id')

    # Generate plot elements

    fig, ax = plt.subplots(2,2, figsize = (30,30))
    ax = ax.ravel()
    fs = 8

    # Plot DAC Counts

    county_air_basin_districts.boundary.plot(
        ax = ax[0],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [100, 1000, 10000, 100000, 1000000]
    labels = ['0 - 100', '100 - 1,000', '1,000 - 10,000', '10,000 - 100,000','100,000 - 1,000,000']

    dac_cdb_data.plot(ax = ax[0],
        column = 'counts',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Counts',
            'labels': labels,
            'loc':'best'})

    ax[0].set_title('Count of DAC\n {} Properties \n Likely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = dac_cdb_data[['geom','counts']].copy()
    centroids['geom'] = dac_cdb_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['counts'] = centroids['counts'].map(str)

    centroids.apply(lambda x: ax[0].annotate(
        text=x['counts'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[0].axis('Off')

    # Plot DAC Percentages

    county_air_basin_districts.boundary.plot(
        ax = ax[1],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    labels = ['0 - 10', '10 - 20', '20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 90']

    dac_cdb_data.plot(ax = ax[1],
        column = 'percentage',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Percentages',
            'labels': labels,
            'loc':'best'})

    ax[1].set_title('Percentage of DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = dac_cdb_data[['geom','percentage']].copy()
    centroids['geom'] = dac_cdb_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['percentage'] = centroids['percentage'].map(str)

    centroids.apply(lambda x: ax[1].annotate(
        text=x['percentage'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[1].axis('Off')

    # Plot Non-DAC Counts

    county_air_basin_districts.boundary.plot(
        ax = ax[2],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [100, 1000, 10000, 100000, 1000000]
    labels = ['0 - 100', '100 - 1,000', '1,000 - 10,000', '10,000 - 100,000','100,000 - 1,000,000']

    non_dac_cdb_data.plot(ax = ax[2],
        column = 'counts',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Counts',
            'labels': labels,
            'loc':'best'})

    ax[2].set_title('Count of Non-DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = non_dac_cdb_data[['geom','counts']].copy()
    centroids['geom'] = non_dac_cdb_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['counts'] = centroids['counts'].map(str)

    centroids.apply(lambda x: ax[2].annotate(
        text=x['counts'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[2].axis('Off')

    # Plot Non-DAC Percentages

    county_air_basin_districts.boundary.plot(
        ax = ax[3],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    labels = ['0 - 10', '10 - 20', '20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 90']

    non_dac_cdb_data.plot(ax = ax[3],
        column = 'percentage',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Percentages',
            'labels': labels,
            'loc':'best'})

    ax[3].set_title('Percentage of Non-DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = non_dac_cdb_data[['geom','percentage']].copy()
    centroids['geom'] = non_dac_cdb_data['geom'].centroid

    centroids['coords'] = centroids['geom'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['percentage'] = centroids['percentage'].map(str)

    centroids.apply(lambda x: ax[3].annotate(
        text=x['percentage'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[3].axis('Off')

    fig.savefig(figure_dir + '{}_likely_panel_ugprade_requirements_by_county_air_basin_district.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return cdb_upgrade_requirements

#%% Generate County Air Basin District Level Overview Map

sf_cdb_upgrade_requirements = PlotLikelyUpgradeRequirementsByCDB(sf, 'single_family', figure_dir, county_air_basin_districts)
mf_cdb_upgrade_requirements = PlotLikelyUpgradeRequirementsByCDB(mf, 'multi_family', figure_dir, county_air_basin_districts)

#%% Plot Total Counts and Percentages by Census Tract

def PlotLikelyUpgradeRequirementsByTract(mp, sector, figure_dir, tracts):

    # Mask counties with insufficient counts
    mask = mp.groupby('tract_geoid_2019')['panel_size_existing'].agg('count')
    mask.loc[mask < 10] = np.nan
    mask = mask[mask.isna()].index.values

    # Generate Tract Upgrade Needs Map data
    tr_stats = mp.groupby(['tract_geoid_2019','panel_size_existing'])['panel_size_existing'].agg('count')
    tr_stats = tr_stats.to_frame()
    tr_stats.rename(columns = {'panel_size_existing':'counts'}, inplace = True)
    tr_stats.reset_index(inplace = True)

    # Drop masked tracts
    drop_ind = tr_stats.loc[tr_stats['tract_geoid_2019'].isin(mask)].index
    tr_stats.drop(drop_ind, inplace = True)

    if sector == 'single_family':

        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['0 - 99', '100', '101 - 199', '101 - 199', '200', '>201', '>201']

    elif sector == 'multi_family':

        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['0 - 89', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

    tr_stats['panel_size_class'] = pd.cut(tr_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    if sector == 'single_family':

        bins = [0, 99, 199, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    elif sector == 'multi_family':

        bins = [0, 89, 149, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    tr_stats['upgrade_required'] = pd.cut(tr_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    # Compute Upgrade Requirement Stats

    tr_upgrade_requirements = tr_stats.groupby(['tract_geoid_2019','upgrade_required'])['counts'].agg('sum').to_frame()
    tr_upgrade_requirements['percentage'] = tr_upgrade_requirements.divide(tr_upgrade_requirements.groupby(['tract_geoid_2019',]).agg('sum')).multiply(100.).round(2)

    # Merge Stats with tract Boundaries

    tr_likely_upgrades = tr_upgrade_requirements.loc(axis=0)[:,'Likely'].reset_index()

    # Merge on Spatial Data

    tr_data = tracts[['geometry','GEOID']].merge(tr_likely_upgrades, left_on = 'GEOID', right_on = 'tract_geoid_2019')

    # Generate plot elements

    fig, ax = plt.subplots(2,2, figsize = (30,30))
    ax = ax.ravel()
    fs = 4

    # Plot Counts

    tracts.boundary.plot(
        ax = ax[0],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [250, 500, 750, 1000, 1250, 1500, 1750]
    labels = ['0 - 250', '250 - 500', '500 - 750', '750 - 1,000', '1,000 - 1,250', '1,250 - 1,500', '1,500 - 1,750']

    tr_data.plot(ax = ax[0],
        column = 'counts',
        edgecolor = 'lightgrey',
        linewidth = 0.01,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Counts',
            'labels': labels,
            'loc':'best'})

    ax[0].set_title('Total Count of {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))
    ax[0].axis('Off')

    # Plot Percentage

    tracts.boundary.plot(
        ax = ax[1],
        edgecolor = 'lightgrey',
        linewidth = 1.0,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0
    )

    bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0 - 10', '10 - 20', '20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 90', '90 - 100']

    tr_data.plot(ax = ax[1],
        column = 'percentage',
        edgecolor = 'lightgrey',
        linewidth = 0.01,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Percentage',
            'labels':labels,
            'loc':'best'})

    ax[1].set_title('Total Percentage of {} Properties \nLikely Requiring Panel Upgrade'.format(sector.replace('_',' ').title()))
    ax[1].axis('Off')

    fig.savefig(figure_dir + '{}_likely_panel_ugprade_requirements_by_tract.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return tr_upgrade_requirements

#%% Plot Upgrade Requirements by Tract

sf_tr_upgrade_requirements = PlotLikelyUpgradeRequirementsByTract(sf, 'single_family', figure_dir, tracts)
mf_tr_upgrade_requirements = PlotLikelyUpgradeRequirementsByTract(mf, 'multi_family', figure_dir, tracts)

#%% Generate Maps by County

def PlotLikelyUpgradeRequirementsByCounty(mp, sector, figure_dir, counties):

    # Mask counties with insufficient counts
    mask = mp.groupby('county_name')['panel_size_existing'].agg('count')
    mask.loc[mask < 100] = np.nan
    mask = mask[mask.isna()].index.values

    # Generate County Upgrade Needs Map
    county_stats = mp.groupby(['county_name','panel_size_existing', 'dac'])['panel_size_existing'].agg('count')
    county_stats = county_stats.to_frame()
    county_stats.rename(columns = {'panel_size_existing':'counts'}, inplace = True)
    county_stats.reset_index(inplace = True)

    # Drop masked counties
    drop_ind = county_stats.loc[county_stats['county_name'].isin(mask)].index
    county_stats.drop(drop_ind, inplace = True)

    if sector == 'single_family':

        bins = [0, 99, 100, 101, 199, 200, 201, 2000]
        labels = ['0 - 99', '100', '101 - 199', '101 - 199', '200', '>201', '>201']

    elif sector == 'multi_family':

        bins = [0, 89, 90, 91, 149, 150, 151, 2000]
        labels = ['0 - 89', '90', '91 - 149', '91 - 149', '150', '>150', '>150']

    county_stats['panel_size_class'] = pd.cut(county_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    if sector == 'single_family':

        bins = [0, 99, 199, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    elif sector == 'multi_family':

        bins = [0, 89, 149, 2000]
        labels = ['Likely', 'Potentially', 'Unlikely']

    county_stats['upgrade_required'] = pd.cut(county_stats['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()

    # Compute Upgrade Requirement Stats

    county_upgrade_requirements = county_stats.groupby(['county_name','dac','upgrade_required'])['counts'].agg('sum').to_frame()
    county_upgrade_requirements['percentage'] = county_upgrade_requirements.divide(county_upgrade_requirements.groupby(['county_name', 'dac']).agg('sum')).multiply(100.).round(2)

    # Merge Stats with County Boundaries

    dac_county_likely_upgrades = county_upgrade_requirements.loc(axis=0)[:,'Yes','Likely'].reset_index()
    non_dac_county_likely_upgrades = county_upgrade_requirements.loc(axis=0)[:,'No','Likely'].reset_index()

    # Merge on Spatial Data

    dac_county_data = counties[['geometry','NAMELSAD']].merge(dac_county_likely_upgrades, left_on = 'NAMELSAD', right_on = 'county_name')
    non_dac_county_data = counties[['geometry','NAMELSAD']].merge(non_dac_county_likely_upgrades, left_on = 'NAMELSAD', right_on = 'county_name')

    # Generate plot elements

    fig, ax = plt.subplots(2,2, figsize = (30,30))
    ax = ax.ravel()
    fs = 8

    # Plot DAC Counts

    counties.boundary.plot(
        ax = ax[0],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [100, 1000, 10000, 100000, 1000000]
    labels = ['0 - 100', '100 - 1,000', '1,000 - 10,000', '10,000 - 100,000','100,000 - 1,000,000']

    dac_county_data.plot(ax = ax[0],
        column = 'counts',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Counts',
            'labels': labels,
            'loc':'best'})

    ax[0].set_title('Count of DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = dac_county_data[['geometry','counts']].copy()
    centroids['geometry'] = dac_county_data['geometry'].centroid

    centroids['coords'] = centroids['geometry'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['counts'] = centroids['counts'].map(str)
    centroids.drop(centroids[centroids['counts'] == 'nan'].index, inplace = True)

    centroids.apply(lambda x: ax[0].annotate(
        text=x['counts'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[0].axis('Off')

    # Plot DAC Percentage

    counties.boundary.plot(
        ax = ax[1],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [10, 20, 30, 40, 50, 60, 70, 80]
    labels = ['0 - 10', '10 - 20', '20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80']

    dac_county_data.plot(ax = ax[1],
        column = 'percentage',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Percentage',
            'labels': labels,
            'loc':'best'})

    ax[1].set_title('Percentage of DAC\n {} Properties \nLikely Requiring Panel Upgrade'.format(sector.replace('_',' ').title()))

    centroids = dac_county_data[['geometry','percentage']].copy()
    centroids['geometry'] = dac_county_data['geometry'].centroid

    centroids['coords'] = centroids['geometry'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['percentage'] = centroids['percentage'].map(str)
    centroids.drop(centroids[centroids['percentage'] == 'nan'].index, inplace = True)

    centroids.apply(lambda x: ax[1].annotate(
        text=x['percentage'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[1].axis('Off')

    # Plot Non-DAC Counts

    counties.boundary.plot(
        ax = ax[2],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [100, 1000, 10000, 100000, 1000000]
    labels = ['0 - 100', '100 - 1,000', '1,000 - 10,000', '10,000 - 100,000','100,000 - 1,000,000']

    non_dac_county_data.plot(ax = ax[2],
        column = 'counts',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Counts',
            'labels': labels,
            'loc':'best'})

    ax[2].set_title('Count of Non-DAC\n {} Properties \nLikely Requiring Panel Upgrades'.format(sector.replace('_',' ').title()))

    centroids = non_dac_county_data[['geometry','counts']].copy()
    centroids['geometry'] = non_dac_county_data['geometry'].centroid

    centroids['coords'] = centroids['geometry'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['counts'] = centroids['counts'].map(str)
    centroids.drop(centroids[centroids['counts'] == 'nan'].index, inplace = True)

    centroids.apply(lambda x: ax[2].annotate(
        text=x['counts'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[2].axis('Off')

    # Plot Non-DAC Percentage

    counties.boundary.plot(
        ax = ax[3],
        edgecolor = 'lightgrey',
        linewidth = 1,
        facecolor = 'darkgrey',
        hatch = '////',
        zorder= 0)

    bins = [10, 20, 30, 40, 50, 60, 70, 80]
    labels = ['0 - 10', '10 - 20', '20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80']

    non_dac_county_data.plot(ax = ax[3],
        column = 'percentage',
        edgecolor = 'lightgrey',
        linewidth = 1,
        zorder = 1,
        cmap = 'RdYlGn_r',
        k = 10,
        scheme = 'user_defined',
        classification_kwds = {'bins': bins},
        legend = True,
        legend_kwds = {
            'title':'Percentage',
            'labels': labels,
            'loc':'best'})

    ax[3].set_title('Percentage of Non-DAC\n {} Properties \nLikely Requiring Panel Upgrade'.format(sector.replace('_',' ').title()))

    centroids = non_dac_county_data[['geometry','percentage']].copy()
    centroids['geometry'] = non_dac_county_data['geometry'].centroid

    centroids['coords'] = centroids['geometry'].apply(lambda x: x.representative_point().coords[:])
    centroids['coords'] = [coords[0] for coords in centroids['coords']]
    centroids['percentage'] = centroids['percentage'].map(str)
    centroids.drop(centroids[centroids['percentage'] == 'nan'].index, inplace = True)

    centroids.apply(lambda x: ax[3].annotate(
        text=x['percentage'],
        xy=x['coords'],
        ha='center',
        color = 'black',
        fontsize = fs), axis=1)

    ax[3].axis('Off')

    fig.savefig(figure_dir + '{}_likely_panel_ugprade_requirements_by_county.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return county_upgrade_requirements

#%% Generate County Level Upgrade Requirements Map

sf_county_upgrade_requirements = PlotLikelyUpgradeRequirementsByCounty(sf, 'single_family', figure_dir, counties)
mf_county_upgrade_requirements = PlotLikelyUpgradeRequirementsByCounty(mf, 'multi_family', figure_dir, counties)
