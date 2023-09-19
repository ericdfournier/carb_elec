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

# Extract Single Family Data from
query = ''' SELECT  A.*,
                    B.permitted_panel_upgrade,
                    B.ces_bin,
                    B.previous_upgrade,
                    B.inferred_panel_upgrade,
                    B.panel_size_existing,
                    B.any_panel_upgrade
            FROM ztrax.model_data AS A
            JOIN ztrax.model_data_sf_inference AS B
                ON A.megaparcelid = B.megaparcelid;'''
mp = pd.read_sql(query, db_con)

# Set megaparcelid as index
mp.set_index('megaparcelid', drop = True, inplace = True)

#%% Set Fixed Parameters

figure_dir = '/Users/edf/repos/carb_elec/analyses/model_data/fig/'
sector = 'single_family'

#%% Plot SF as built panel size ratings

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
    elif sector == 'multi_family':
        ylim = [0, 220]
        yticks = [30, 40, 60, 90, 100, 125, 150, 200]
        bins = 40
        ylabel = 'Average As-Built Load Center Rating Per Unit\n[Amps]'

    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_as_built',
        data = dac_sample,
        color = 'tab:orange',
        ax = ax[0],
        bins = bins,
        legend = True,
        label = 'DAC',
        cbar = True,
        cbar_kws = {'label':'Number of Properties', 'orientation':'horizontal'},
        vmin=0, vmax=50000)
    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_as_built',
        data = non_dac_sample,
        color = 'tab:blue',
        ax = ax[1],
        bins = bins,
        legend = True,
        label = 'Non-DAC',
        cbar = True,
        cbar_kws = {'label':'Number of Properties', 'orientation':'horizontal'},
        vmin=0, vmax=50000)

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

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + 'sample_{}_as_built_panel_ratings_hist.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate As Built Panel Rating Hist

AsBuiltPanelRatingsHist(mp, sector, figure_dir)

#%% Plot As-Built Panel Stats

def AsBuiltPanelRatingsBar(mp, sector, figure_dir):
    '''Simple barplot of as-built panel ratings separated by DAC status'''

    # Compute counts

    if sector == 'single_family':
        counts = mp.groupby(['dac', 'panel_size_as_built'])['sampled'].agg('count')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'As-Built Panel Rating \n[Amps]'
        xlabel = 'Number of Properties'
    elif sector == 'multi_family':
        # NOTE: Units field missing in current MP structure
        counts = mp.groupby(['dac', 'panel_size_as_built'])['units'].agg('sum')
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

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + 'sample_{}_as_built_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate As-Built Panel Ratings Bar Chart

AsBuiltPanelRatingsBar(mp, sector, figure_dir)

#%% Plot Cumulative Permit Counts

def PermitCountsBar(buildings_ces, sector, figure_dir):

    upgrade_stats = mp.loc[mp['permitted_panel_upgrade'] == True].groupby('dac')['sampled'].agg('count')
    upgrade_stats = pd.DataFrame(upgrade_stats).reset_index()

    fig, ax = plt.subplots(1, 1, figsize = (5,5), sharex = True)

    sns.barplot(data = upgrade_stats,
        y = 'sampled',
        x = 'dac',
        order = ['No','Yes'],
        ax = ax)

    if sector == 'single_family':
        ylabel = 'Total Cumulative Panel Upgrade Permits'
    elif sector == 'multi_family':
        ylabel = 'Total Cumulative Load Center Upgrade Permits'

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('DAC Status')
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.tight_layout()

    fig.savefig(figure_dir + '{}_cumulative_permit_count_barplot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Permit Count Barchart

PermitCountsBar(mp, sector, figure_dir)

#%% Plot Existing panel size ratings

def ExistingPanelRatingsHist(mp, sector, figure_dir):
    '''Function to plot a set of 2d histograms relating the frequency of
    existing panel sizes to vintage year by dac status'''

    dac_ind = (mp['dac'] == 'Yes')
    non_dac_ind = (mp['dac'] == 'No')

    dac_sample = mp.loc[dac_ind,:]
    non_dac_sample = mp.loc[non_dac_ind,:]

    if sector == 'single_family':
        yticks = [30,60,100, 125, 150, 200, 225, 320, 400, 600, 800, 1000, 1200]
        ylim = (0, 1220)
        ylabel = 'Existing Panel Rating \n[Amps]'
        bins = 80
    elif sector == 'multi_family':
        yticks = [30, 40, 60, 90, 100, 125, 150, 200]
        ylim = (0, 220)
        ylabel = 'Existing Average Load Center Rating per Unit \n[Amps]'
        bins = 40

    fig, ax = plt.subplots(1,2,figsize = (10,10), sharey = True, sharex = True)

    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_existing',
        data = dac_sample,
        color = 'tab:orange',
        ax = ax[0],
        bins = bins,
        legend = True,
        label = 'DAC',
        cbar = True,
        cbar_kws = {'label': 'Number of Properties', 'orientation':'horizontal'},
        vmin=0, vmax=50000)
    sns.histplot(x = 'YearBuilt',
        y = 'panel_size_existing',
        data = non_dac_sample,
        color = 'tab:blue',
        ax = ax[1],
        bins = bins,
        legend = True,
        label = 'Non-DAC',
        cbar = True,
        cbar_kws = {'label':'Number of Properties', 'orientation':'horizontal'},
        vmin=0, vmax=50000)

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

ExistingPanelRatingsHist(mp, sector, figure_dir)

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
        plt.legend(loc='upper left')
        plt.xlim([1830, 2025])
        plt.ylim([2.0, 5.0])
        plt.yticks([2,3,4,5])
        fig.ax_joint.set_yticklabels(['100', '1,000', '10,000', '100,000'])
        fig.ax_joint.set_ylabel('Building Size\n($ft^2$)')
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
        plt.legend(loc='upper left')
        plt.xlim([1860, 2025])
        plt.ylim([2.0, 6.0])
        plt.yticks([2,3,4,5,6])
        fig.ax_joint.set_yticklabels(['100', '1,000', '10,000', '100,000','1,000,000'])
        fig.ax_joint.set_ylabel('Building Size\n($ft^2$)')
        fig.ax_joint.set_xlabel('Construction Vintage\n(Year)')
        plt.grid()

    fig.savefig(figure_dir + '{}_home_size_vintage_jointplot.png'.format(sector), dpi = 500, bbox_inches = 'tight')

    return

#%% Plot Home Size Vintage Jointplot

# CAUTION - Long run-time...
JointDistributionPlot(mp, sector, figure_dir)

#%% Generate Statistic Table

def PrintStatsTable(mp, sector):

    bins = [0, 99, 100, 101, 199, 200, 201, 2000]
    labels = ['0 - 99', '100', '101 - 199', '101 - 199', '200', '>201', '>201']
    mp['panel_size_class'] = pd.cut(mp['panel_size_existing'],
        bins = bins,
        labels = labels,
        ordered = False).to_frame()
    stats = mp[['panel_size_class','panel_size_existing']].groupby('panel_size_class',
        observed = False).agg('count')
    stats.rename(columns = {'panel_size_existing':'count'}, inplace = True)
    total = (~mp['panel_size_existing'].isna()).sum()
    stats['pct'] = stats['count'].divide(total).multiply(100.0)

    print(stats.to_markdown())

    return stats

#%% Print Stats Table

# LBNL Results for Comparison
# Panel Amps	Count	Frequency
# <100	        5,068	9%
# 100	        15,090	26%
# 101-199	    12,185	21%
# 200	        19,109	33%
# >200	        5,915	10%

stats = PrintStatsTable(mp, sector)

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
        counts = mp.groupby(['dac', 'panel_size_existing'])['units'].agg('sum')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Average Load Center Rating \n[Amps]'
        xlabel = 'Number of Units'

    # Plot Counts
    fig, ax = plt.subplots(1,1, figsize = (5,5))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(rotation = 45)

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + '{}_existing_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Existing Panel Ratings Bar Chart

ExistingPanelRatingsBar(mp, sector, figure_dir)

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

        fig1.savefig(figure_dir + 'ladwp_multi_family_non_dac_permitted_upgrade_amps_per_sqft_jointplot.png', bbox_inches = 'tight', dpi = 500)
        fig2.savefig(figure_dir + 'ladwp_multi_family_dac_permitted_upgrade_amps_per_sqft_jointplot.png', bbox_inches = 'tight', dpi = 500)

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
AreaNormalizedComparisonKDE(mp, sector, figure_dir)

#%% Distribution of Destination Panel Sizes for Permitted Upgrades

def PermittedUpgradePanelSizeDistribution(mp, sector, figure_dir):

    perm_ind = ~mp['upgraded_panel_size'].isna()

    data = mp.loc[perm_ind, ['dac','upgraded_panel_size']]
    data.loc[data['upgraded_panel_size'] < 60.0, ['upgraded_panel_size']] = 60.0

    counts = data.groupby(['dac','upgraded_panel_size'])['upgraded_panel_size'].agg('count')
    counts = counts.unstack(level= 0)
    counts.index = counts.index.astype(int)

    fig, ax = plt.subplots(1,1,figsize=(7,7))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.set_ylabel('Upgraded Panel Size')
    ax.set_xlabel('Upgrade Permit Count Frequency')
    ax.grid(True)
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    plt.xticks(rotation = 45)

    fig.savefig('{}_permitted_upgrade_panel_size_distribution.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Permitted Panel Upgrade Distribution Plot

PermittedUpgradePanelSizeDistribution(mp, sector, figure_dir)

#%% Distribution of Destination Panel Sizes for Inferred Upgrades

def InferredUpgradePanelSizeDistribution(mp, sector, figure_dir):

    infer_ind = mp['inferred_panel_upgrade'] == True

    data = mp.loc[infer_ind, ['dac','panel_size_existing']]
    data.loc[data['panel_size_existing'] < 60.0, ['panel_size_existing']] = 60.0

    counts = data.groupby(['dac','panel_size_existing'])['panel_size_existing'].agg('count')
    counts = counts.unstack(level= 0)
    counts.index = counts.index.astype(int)

    fig, ax = plt.subplots(1,1,figsize=(7,7))

    counts.plot.barh(ax = ax, color = ['tab:blue', 'tab:orange'])

    ax.set_ylabel('Upgraded Panel Size')
    ax.set_xlabel('Inferred Upgrade Count Frequency')
    ax.grid(True)
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    plt.xticks(rotation = 45)

    fig.savefig('{}_inferred_upgrade_panel_size_distribution.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Inferred Panel Upgrade Distribution Plot

InferredUpgradePanelSizeDistribution(mp, sector, figure_dir)
