#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter
import seaborn as sns

#%% Read Model Data Set from Pickle

data_path = '/Users/edf/repos/carb_elec/model/data/sf_model_data.pkl'
mp = pd.read_pickle(data_path)

#%% Set DAC Status

mp['dac_status'] = 'Non-DAC'
dac_ind = mp['ciscorep'] >= 75.0
mp.loc[dac_ind,'dac_status'] = 'DAC'

#%% Set Fixed Parameters

figure_dir = '/Users/edf/repos/carb_elec/analyses/model_data/fig/'
sector = 'single_family'

#%% Plot SF as built panel size ratings

def AsBuiltPanelRatingsHist(mp, sector, figure_dir):
    '''Paired DAC / Non-DAC 2D histogram of panel sizes by building
    construction vintage years'''

    fig, ax = plt.subplots(1,2,figsize = (10,10), sharey = True)

    dac_ind = mp['dac_status'] == 'DAC'
    non_dac_ind = mp['dac_status'] == 'Non-DAC'

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
        counts = mp.groupby(['dac_status', 'panel_size_as_built'])['sampled'].agg('count')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'As-Built Panel Rating \n[Amps]'
        xlabel = 'Number of Properties'
    elif sector == 'multi_family':
        # NOTE: Units field missing in current MP structure
        counts = mp.groupby(['dac_status', 'panel_size_as_built'])['units'].agg('sum')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Average As-Built Load Center Rating per Unit \n[Amps]'
        xlabel = 'Number of Units'

    # Plot Counts

    fig, ax = plt.subplots(1,1, figsize = (5,5))

    counts.plot.barh(ax = ax, color = ['tab:orange', 'tab:blue'])

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(rotation = 45)

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + 'sample_{}_as_built_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate As-Built Panel Stats

AsBuiltPanelRatingsBar(mp, sector, figure_dir)

#TODO: Stopping Point!!!

#%%

def PermitTimeSeries(buildings_ces, sector, figure_dir):
    '''Plot annual total and cumulative total panel upgrade permits
    separated by DAC status'''

    # Generate Time Series of Permits by DAC Status

    upgrade_ind = buildings_ces['panel_related_permit'] == True
    permit_ts = buildings_ces.loc[upgrade_ind].groupby([pd.Grouper(key='permit_issue_date', axis=0, freq='1Y'), 'dac_status'])['apn'].agg('count')
    permit_ts = permit_ts.reset_index()
    permit_ts = permit_ts.rename(columns = {'apn': 'permit_count'})

    dac_vals = permit_ts['dac_status'] == 'DAC'
    non_dac_vals = permit_ts['dac_status'] == 'Non-DAC'

    print('DAC Average Annual Permit Counts: {}'.format(permit_ts.loc[dac_vals,'permit_count'].mean()))
    print('DAC Average Annual Rates of Change: {}'.format(permit_ts.loc[dac_vals,'permit_count'].pct_change().mean()))
    print('\n')
    print('Non-DAC Average Annual Permit Counts: {}'.format(permit_ts.loc[non_dac_vals,'permit_count'].mean()))
    print('Non-DAC Average Annual Rates of Change: {}'.format(permit_ts.loc[non_dac_vals,'permit_count'].pct_change().mean()))

    # Generate Cumsum of Permits by DAC Status

    permit_cs = buildings_ces.loc[upgrade_ind].groupby([pd.Grouper(key='permit_issue_date', axis=0, freq='1Y'), 'dac_status'])['apn'].agg('count')
    permit_cs = permit_cs.sort_index()
    dac_vals = permit_cs.loc(axis = 0)[:,'DAC'].cumsum()
    non_dac_vals = permit_cs.loc(axis = 0)[:,'Non-DAC'].cumsum()
    permit_cs = pd.concat([dac_vals, non_dac_vals], axis = 0).sort_index()
    permit_cs = permit_cs.reset_index()
    permit_cs = permit_cs.rename(columns = {'apn': 'permit_count'})

    dac_vals = permit_cs['dac_status'] == 'DAC'
    non_dac_vals = permit_cs['dac_status'] == 'Non-DAC'

    print('DAC Cumulative Permit Counts: {}'.format(permit_cs.loc[dac_vals,'permit_count'].sum()))
    print('DAC Average Annual Rates of Change: {}'.format(permit_cs.loc[dac_vals,'permit_count'].pct_change().mean()))
    print('\n')
    print('Non-DAC Cumulative Permit Counts: {}'.format(permit_cs.loc[non_dac_vals,'permit_count'].mean()))
    print('Non-DAC Average Annual Rates of Change: {}'.format(permit_cs.loc[non_dac_vals,'permit_count'].pct_change().mean()))

    # Plot Time Series of Permit Counts and Cumulative Sums

    fig, ax = plt.subplots(2, 1, figsize = (8,8), sharex = True)

    hue_order = ['Non-DAC', 'DAC']

    sns.lineplot(x = 'permit_issue_date',
        y = 'permit_count',
        hue = 'dac_status',
        hue_order = hue_order,
        data = permit_ts,
        ax = ax[0])

    l1 = ax[0].lines[0]
    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]

    ax[0].fill_between(x1, y1, color="tab:blue", alpha=0.3)

    l2 = ax[0].lines[1]
    x2 = l2.get_xydata()[:, 0]
    y2 = l2.get_xydata()[:, 1]

    ax[0].fill_between(x2, y2, color="tab:orange", alpha=0.3)
    ax[0].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    sns.lineplot(x = 'permit_issue_date',
        y = 'permit_count',
        hue = 'dac_status',
        hue_order = hue_order,
        data = permit_cs,
        ax = ax[1])

    l1 = ax[1].lines[0]
    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]
    ax[1].fill_between(x1, y1, color="tab:blue", alpha=0.3)

    l2 = ax[1].lines[1]
    x2 = l2.get_xydata()[:, 0]
    y2 = l2.get_xydata()[:, 1]
    ax[1].fill_between(x2, y2, color="tab:orange", alpha=0.3)

    ax[1].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax[1].margins(x=0, y=0)

    ax[0].grid(True)
    ax[1].grid(True)

    ax[1].set_xlabel('Permit Issue Date \n[Year]')
    ax[0].set_ylabel('Panel Upgrades in Sample Area \n[Annual]')
    ax[1].set_ylabel('Panel Upgrades in Sample Area \n[Cumulative]')

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + 'ladwp_{}_permit_time_series_plot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

# Plot Cumulative Permit Counts
def PermitCountsBar(buildings_ces, sector, figure_dir):

    upgrade_ind = buildings_ces['panel_related_permit'] == True
    upgrade_data = buildings_ces.loc[upgrade_ind,:].copy()
    upgrade_stats = upgrade_data.groupby('dac_status')['apn'].agg('count')
    upgrade_stats = pd.DataFrame(upgrade_stats).reset_index()

    fig, ax = plt.subplots(1, 1, figsize = (5,5), sharex = True)

    sns.barplot(data = upgrade_stats,
        y = 'apn',
        x = 'dac_status',
        order = ['Non-DAC','DAC'],
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

    fig.savefig(figure_dir + 'ladwp_{}_cumulative_permit_count_barplot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Function to Map the Cumulative Total Number of Permits by Tract

def PermitCountsMap(buildings_ces, ces4, ladwp, sector, figure_dir):
    '''Function to map the cumulative total number of buildings with
    panel upgrade pemits by census tract and DAC status'''

    # Count the Total Number of Buildings in the Permit Data Tracts

    tracts = buildings_ces['census_tract'].unique()
    ind = ces4['tract'].isin(tracts)

    permits_per_tract = buildings_ces.groupby(['census_tract'])['apn'].agg('count')
    permits_per_tract_ces = pd.merge(ces4.loc[:,['geom','tract']], permits_per_tract, left_on = 'tract', right_index = True)

    # Plot Census Tracts with Permit Data

    fig, ax = plt.subplots(1, 1, figsize = (10,10))

    dac_ind = ces4['ciscorep'] >= 75.0
    non_dac_ind = ces4['ciscorep'] < 75.0

    ces4.loc[~(dac_ind | non_dac_ind)].boundary.plot(ax = ax, edgecolor = 'k', linewidth = 0.5)
    ces4.loc[dac_ind].boundary.plot(ax = ax, color = 'tab:orange', linewidth = 0.5)
    ces4.loc[non_dac_ind].boundary.plot(ax = ax, color = 'tab:blue', linewidth = 0.5)
    ladwp.boundary.plot(ax = ax, edgecolor = 'black', linewidth = 1.5)

    if sector == 'single_family':
        title = 'Single Family Properties\nPermitted Panel Upgrades\n[Counts]\n'
        bins = [100,250,500,750,1000,1500,2000]
        labels = ["1-100", "100-250", "250-500", "500-750","750-1000", "1000-1500", "1500-2000","2000+"]
    elif sector == 'multi_family':
        title = 'Multi-Family Properties\nPermitted Panel Upgrades\n[Counts]\n'
        bins = [100,250,500,750,1000,1500,2000]
        labels = ["1-100", "100-250", "250-500", "500-750","750-1000", "1000-1500", "1500+"]

    permits_per_tract_ces.plot(ax = ax,
        column = 'apn',
        k = 7,
        cmap = 'bone_r',
        scheme = 'user_defined',
        classification_kwds = {'bins' : bins},
        legend = True,
        legend_kwds = {'title': title,
                        'loc': 'lower left',
                        "labels": labels})

    ax.set_ylim((-480000,-405000))
    ax.set_xlim((120000,170000))
    ax.set_axis_off()

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + 'ladwp_{}_permit_geographic_distribution_map.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Function to Animate Permit Histogram by Vintage Year

def PermitCountsHistAnimation(buildings_ces, figure_dir):
    '''Generate a vintage year based permit frequency count histogram
    for each unique year in the permit dataset interval.'''

    def AnimateFunc(num):
        '''Animation worker function'''

        hue_order = [ 'Non-DAC','DAC']

        ax.clear()
        test_years = buildings_ces['permit_issue_date'].dt.year.unique()
        test_years = np.sort(test_years)
        y = test_years[num+1]
        ind = buildings_ces['permit_issue_date'].dt.year == y
        data = buildings_ces.loc[ind]
        year = data.loc[:,'year_built'].dt.year
        data.loc[:,'year_built'] = year.values

        sns.histplot(x = 'year_built',
            data = data,
            hue = 'dac_status',
            kde = True,
            legend = True,
            hue_order = hue_order,
            ax = ax,
            bins = np.arange(1900,2020,2))

        ax.grid(True)
        ax.set_title(str(y))
        ax.set_xlim(1900,2020)
        ax.set_ylim(0,1500)
        ax.set_xlabel('Year Built')
        ax.set_ylabel('Count')

        return

    fig = plt.figure()
    ax = plt.axes()

    numDataPoints = buildings_ces['permit_issue_date'].dt.year.unique().shape[0]-1

    line_ani = animation.FuncAnimation(fig,
        AnimateFunc,
        interval=1000,
        frames=numDataPoints)

    plt.show()

    f = figure_dir + 'ladwp_panel_permits_histogram_animation.gif'
    writergif = animation.PillowWriter(fps=numDataPoints/16)
    line_ani.save(f, writer=writergif)

    return

#%% Plot ECDF for As-Built Year by DAC Status

def PermitVintageYearECDF(buildings_ces, sector, figure_dir):
    '''Function to plot the empirical cdf's for permitted panel upgrade
    by the vintage year of the property and DAC status'''

    nan_ind = ~buildings_ces.loc[:,'year_built'].isna()
    dac_ind = buildings_ces.loc[:,'dac_status'] == 'DAC'
    non_dac_ind = buildings_ces.loc[:,'dac_status'] == 'Non-DAC'
    permit_ind = buildings_ces.loc[:,'permitted_panel_upgrade'] == True
    permit_issue_year = buildings_ces.loc[:,'permit_issue_date'].dt.year
    construction_year = buildings_ces.loc[:,'year_built'].dt.year
    current_age = 2022 - construction_year
    permit_age = current_age - (2022 - permit_issue_year)

    fig, ax = plt.subplots(1,1,figsize = (8,5))

    sns.ecdfplot(data=permit_age.loc[nan_ind & dac_ind & permit_ind], ax=ax, color = 'tab:orange')
    sns.ecdfplot(data=permit_age.loc[nan_ind & non_dac_ind & permit_ind], ax=ax, color = 'tab:blue')

    if sector == 'single_family':
        ylabel = 'Proportion of Properties\nwith Permitted Panel Upgrades'
    elif sector == 'multi_family':
        ylabel = 'Proportion of Properties\nwith Permitted Panel Upgrades'

    ax.set_xlabel('Age of Property')
    ax.set_ylabel(ylabel)
    ax.autoscale(enable=True, axis='x', tight = True)
    range_max = permit_age.max()
    interval = 10
    x_ticks = np.arange(0.0, range_max, interval)
    y_ticks = np.arange(0.0, 1.1, 0.1)
    ax.set_xticks(x_ticks)
    ax.autoscale(enable=True, axis='x', tight=True)
    ax.grid(True)
    ax.set_ylim(0.0,1.0)
    ax.set_xlim(0.0, 150)
    ax.set_yticks(y_ticks)

    ax.legend(['DAC', 'Non-DAC'])

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + 'ladwp_{}_vintage_empirical_cdf_plot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Diagnostic Plot of Change Statistics

def ExistingPanelRatingsChangeCountsBar(panel_stats_ces_geo, sector, figure_dir):
    '''Function to generate a paired barchart showing the count of homes
    having received upgrades by DAC Status'''

    total_permit_counts = panel_stats_ces_geo.groupby('dac_status')['upgrade_count'].agg('sum').reset_index()

    fig, ax = plt.subplots(1,1, figsize=(5,5))

    sns.barplot(x = 'dac_status',
        y = 'upgrade_count',
        data = total_permit_counts,
        order = ['Non-DAC', 'DAC'],
        ax = ax)

    if sector == 'single_family':
        ylabel = 'Total Number of Panel Upgrades \n[Units]'
    elif sector == 'multi_family':
        ylabel = 'Total Number of Load Center Upgrades \n[Units]'

    ax.set_ylabel(ylabel)
    ax.set_xlabel('DAC Status')
    ax.grid(True)

    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + 'ladwp_{}_panel_upgrade_total_counts_barplot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Diagnostic Plot of Change Statistics

def ExistingPanelRatingsChangeAmpsBox(panel_stats_ces_geo, sector, figure_dir):
    '''Function to generate a pairwise set of boxplots showing the magnitude
    in amps of the upgrades from as-built to existing by DAC status'''

    fig, ax = plt.subplots(1,1, figsize=(5,5))

    sns.boxplot(x = 'dac_status',
        y = 'upgrade_delta_amps',
        data = panel_stats_ces_geo,
        ax = ax)

    if sector == 'single_family':
        ylabel = 'Change in Mean Panel Rating \n(As-built -> Existing) \n[Amps]'
    elif sector == 'multi_family':
        ylabel = 'Change in Mean Load Center Rating \n(As-built -> Existing) \n[Amps]'

    ax.set_ylabel(ylabel)
    ax.set_xlabel('DAC Status')
    ax.grid(True)

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + 'ladwp_{}_panel_upgrade_deltas_boxplots.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Diagnostic Plot of Change Statistics

def ExistingPanelRatingsChangeAmpsScatter(panel_stats_ces_geo, sector, figure_dir):
    '''Function to generate a scatterplot of the change in the mean panel size
    from as-built to existing condition by DAC status.'''

    fig, ax = plt.subplots(1,1, figsize=(5,5))

    sns.scatterplot(x = 'mean_panel_size_as_built',
        y = 'upgrade_delta_amps',
        hue = 'dac_status',
        data = panel_stats_ces_geo,
        ax = ax,
        alpha = 0.5)

    if sector == 'single_family':
        ylabel = 'Change in Mean Panel Rating\n(As-built -> Existing) \n[Amps]'
        xlabel = 'Mean Panel Rating \n (As-built) [Amps]'
    elif sector == 'multi_family':
        ylabel = 'Change in Mean Load Center Rating\n(As-built -> Existing) \n[Amps]'
        xlabel = 'Mean Panel Rating \n (As-built) [Amps]'

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.grid(True)

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + 'ladwp_{}_panel_upgrade_deltas_vs_ces_scatterplot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Diagnostic Plot of Change Statistics

def ExistingPanelRatingsChangeAmpsHist(panel_stats_ces_geo, sector, figure_dir):
    '''Function to generate a pairwise histogram of the change in the mean panel size
    from as-built to existing condition by DAC status.'''

    fig, ax = plt.subplots(1,1, figsize=(5,5))

    sns.histplot(x = 'mean_panel_size_existing',
        hue = 'dac_status',
        data = panel_stats_ces_geo,
        bins = 30,
        ax = ax)

    if sector == 'single_family':
        xlabel = 'Mean Panel Rating \n (Existing) \n[Amps]'
        n = 200
    elif sector == 'multi_family':
        n = 150
        xlabel = 'Mean Load Center Rating \n (Existing) \n[Amps]'

    ax.axvline(n, color = 'r', linestyle = '--', linewidth = 2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Census Tracts \n[Counts]')
    ax.grid(True)

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + 'ladwp_{}_panel_upgrade_existing_means_histplot.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Diagnostic Map Plot

def ExistingPanelRatingsMap(panel_stats_ces_geo, ces4, ladwp, sector, figure_dir):
    '''Function generate a census tract level map of the average existing
    panel size ratings'''

    fig, ax = plt.subplots(1,1, figsize=(10,10))

    dac_ind = ces4['ciscorep'] >= 75.0
    non_dac_ind = ces4['ciscorep'] < 75.0

    ces4.loc[~(dac_ind | non_dac_ind)].boundary.plot(ax = ax, edgecolor = 'k', linewidth = 0.5)
    ces4.loc[dac_ind].boundary.plot(ax = ax, color = 'tab:orange', linewidth = 0.5)
    ces4.loc[non_dac_ind].boundary.plot(ax = ax, color = 'tab:blue', linewidth = 0.5)
    ladwp.boundary.plot(ax = ax, edgecolor = 'black', linewidth = 1.5)

    if sector == 'single_family':
        bins = [30,60,100,125,150,200,300,400]
        labels = ["0-30","30-60", "60-100", "100-125", "125-150", "150-200", "200-300", "300-400"]
    elif sector == 'multi_family':
        bins = [30, 40, 60, 90, 100, 125, 150]
        labels = ["0-30","30-40", "40-60", "60-90", "90-100", "100-125", "125-150", "150-200"]

    panel_stats_ces_geo.plot(column = 'mean_panel_size_existing',
        ax = ax,
        scheme='user_defined',
        classification_kwds = {'bins' : bins},
        k = 10,
        cmap='bone_r',
        legend = True,
        legend_kwds = {'title': 'Mean Panel Rating\nExisting [Amps]',
                        'loc': 'lower left',
                        "labels": labels})

    ax.set_ylim((-480000,-405000))
    ax.set_xlim((120000,170000))
    ax.set_axis_off()

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + 'ladwp_{}_panel_ratings_existing_geographic_distribution_map.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Generate Change Percentage Plot

def ExistingPanelRatingsChangePctMap(panel_stats_ces_geo, ces4, ladwp, figure_dir):
    '''Function to plot the percentage change in mean panel sizes from
    as-built to existing condition by census tract and DAC status'''

    fig, ax = plt.subplots(1,1, figsize = (10,10))

    dac_ind = ces4['ciscorep'] >= 75.0
    non_dac_ind = ces4['ciscorep'] < 75.0

    ces4.loc[~(dac_ind | non_dac_ind)].boundary.plot(ax = ax, edgecolor = 'k', linewidth = 0.5)
    ces4.loc[dac_ind].boundary.plot(ax = ax, color = 'tab:orange', linewidth = 0.5)
    ces4.loc[non_dac_ind].boundary.plot(ax = ax, color = 'tab:blue', linewidth = 0.5)
    ladwp.boundary.plot(ax = ax, edgecolor = 'black', linewidth = 1.5)
    panel_stats_ces_geo.plot(column = 'upgrade_delta_pct',
        scheme = 'userdefined',
        k = 7,
        cmap = 'bone_r',
        classification_kwds = {'bins' : [10,25,50,75,100,200]},
        legend = True,
        legend_kwds = {'title': 'Change in Mean Panel Rating\nFrom As-Built -> Existing\n[Percent Change]\n',
                        'loc': 'lower left'},
        ax = ax)

    ax.set_ylim((-480000,-405000))
    ax.set_xlim((120000,170000))
    ax.set_axis_off()

    fig.tight_layout()
    fig.patch.set_facecolor('white')

    fig.savefig(figure_dir + 'ladwp_panel_ratings_delta_geographic_distribution_quiver_map.png', bbox_inches = 'tight', dpi = 300)

    return

#%% Plot SF Existing panel size ratings

def ExistingPanelRatingsHist(buildings_ces, ces4, ladwp, sector, figure_dir):
    '''Function to plot a set of 2d histograms relating the frequency of
    existing panel sizes to vintage year by dac status'''

    dac_ind = (buildings_ces['dac_status'] == 'DAC')
    non_dac_ind = (buildings_ces['dac_status'] == 'Non-DAC')

    dac_sample = buildings_ces.loc[dac_ind,:]
    non_dac_sample = buildings_ces.loc[non_dac_ind,:]

    dac_sample['year_built_int'] = dac_sample['year_built'].dt.year
    non_dac_sample['year_built_int'] = non_dac_sample['year_built'].dt.year

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

    sns.histplot(x = 'year_built_int',
        y = 'panel_size_existing',
        data = dac_sample,
        color = 'tab:orange',
        ax = ax[0],
        bins = bins,
        legend = True,
        label = 'DAC',
        cbar = True,
        cbar_kws = {'label': 'Number of Properties', 'orientation':'horizontal'},
        vmin=0, vmax=4000)
    sns.histplot(x = 'year_built_int',
        y = 'panel_size_existing',
        data = non_dac_sample,
        color = 'tab:blue',
        ax = ax[1],
        bins = bins,
        legend = True,
        label = 'Non-DAC',
        cbar = True,
        cbar_kws = {'label':'Number of Properties', 'orientation':'horizontal'},
        vmin=0, vmax=4000)

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

    fig.savefig(figure_dir + 'ladwp_{}_existing_panel_ratings_hist.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

def JointDistributionPlot(buildings_ces, sector, figure_dir):

    buildings_ces['log_building_sqft'] = buildings_ces['building_sqft'].apply(np.log10)

    if sector == 'single_family':

        fig = sns.jointplot(data = buildings_ces,
            x = 'year_built',
            y = 'log_building_sqft',
            hue = 'dac_status',
            palette = ['tab:blue', 'tab:orange'],
            hue_order = ['Non-DAC', 'DAC'],
            alpha = 0.1,
            marker = '.',
            linewidth = 0
            )
        plt.legend(loc='upper left')
        plt.xlim(pd.to_datetime([1830, 2025], format = '%Y'))
        plt.ylim([2.0, 5.0])
        plt.yticks([2,3,4,5])
        fig.ax_joint.set_yticklabels(['100', '1,000', '10,000', '100,000'])
        fig.ax_joint.set_ylabel('Building Size\n($ft^2$)')
        fig.ax_joint.set_xlabel('Construction Vintage\n(Year)')
        plt.grid()

    elif sector == 'multi_family':

        fig = sns.jointplot(data = buildings_ces,
            x = 'year_built',
            y = 'log_building_sqft',
            hue = 'dac_status',
            palette = ['tab:blue', 'tab:orange'],
            hue_order = ['Non-DAC', 'DAC'],
            alpha = 0.1,
            marker = '.',
            linewidth = 0
            )
        plt.legend(loc='upper left')
        plt.xlim(pd.to_datetime([1860, 2025], format = '%Y'))
        plt.ylim([2.0, 6.0])
        plt.yticks([2,3,4,5,6])
        fig.ax_joint.set_yticklabels(['100', '1,000', '10,000', '100,000','1,000,000'])
        fig.ax_joint.set_ylabel('Building Size\n($ft^2$)')
        fig.ax_joint.set_xlabel('Construction Vintage\n(Year)')
        plt.grid()

    fig.savefig(figure_dir + 'ladwp_{}_home_size_vintage_jointplot.png'.format(sector), dpi = 500, bbox_inches = 'tight')

    return

#%% Plot Existing Panel Stats

def ExistingPanelRatingsBar(buildings_ces, sector, figure_dir):
    '''Simple barplot of existing panel ratings separated by DAC status'''

    # Compute counts
    if sector == 'single_family':
        counts = buildings_ces.groupby(['dac_status', 'panel_size_existing'])['apn'].agg('count')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Panel Rating \n[Amps]'
        xlabel = 'Number of Properties'
    elif sector == 'multi_family':
        counts = buildings_ces.groupby(['dac_status', 'panel_size_existing'])['units'].agg('sum')
        counts = counts.unstack(level= 0)
        counts.index = counts.index.astype(int)
        ylabel = 'Existing Average Load Center Rating \n[Amps]'
        xlabel = 'Number of Units'

    # Plot Counts
    fig, ax = plt.subplots(1,1, figsize = (5,5))

    counts.plot.barh(ax = ax, color = ['tab:orange', 'tab:blue'])

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.xticks(rotation = 45)

    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    fig.patch.set_facecolor('white')
    fig.tight_layout()

    fig.savefig(figure_dir + 'ladwp_{}_existing_panel_ratings_barchart.png'.format(sector), bbox_inches = 'tight', dpi = 300)

    return

#%% Plot Normalized Amps per Sqft for Upgraded and Non-Upgraded Subsets

def AreaNormalizedComparisonKDE(buildings_ces, sector, figure_dir):

    if sector == 'single_family':

        # SF plot data

        buildings_ces['building_sqft_log10'] = np.log10(buildings_ces['building_sqft'])
        buildings_ces['existing_amps_per_sqft_log10'] = np.log10(buildings_ces['panel_size_existing'] / buildings_ces['building_sqft'])

        non_dacs_ind = buildings_ces['dac_status'] == 'Non-DAC'
        dacs_ind = buildings_ces['dac_status'] == 'DAC'

        non_dacs = buildings_ces.loc[non_dacs_ind,:]
        dacs = buildings_ces.loc[dacs_ind,:]

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

        fig1.savefig(figure_dir + 'ladwp_{}_non_dac_permitted_upgrade_amps_per_sqft_jointplot.png'.format(sector), bbox_inches = 'tight', dpi = 500)
        fig2.savefig(figure_dir + 'ladwp_{}_dac_permitted_upgrade_amps_per_sqft_jointplot.png'.format(sector), bbox_inches = 'tight', dpi = 500)

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
        buildings_ces['existing_amps_per_sqft_log10'] = np.log10(buildings_ces['panel_size_existing'] / buildings_ces['avg_unit_sqft'])

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
