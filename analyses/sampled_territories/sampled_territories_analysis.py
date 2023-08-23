#%% Package Imports

import pandas as pd
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
from sqlalchemy import create_engine
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
from tqdm import tqdm
import os

#%% Change Working Directory

root = '/Users/edf/repos/carb_elec/analyses/sampled_territories/'
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

#%% Import Sampled Territory Megaparcel Data

megaparcels_sql = '''
    SELECT "PropertyLandUseStndCodes",
        "MedianYearBuilt",
        "TotalBuildingAreaSqFt",
        "megaparcelid",
        "sampled",
        "centroid"
    FROM ztrax.megaparcels
    WHERE "sampled" = TRUE;
    '''

megaparcels = gpd.read_postgis(megaparcels_sql,
    engine,
    geom_col = 'centroid',
    index_col = 'megaparcelid')

#%% Extract Samples

sf_ind = megaparcels['PropertyLandUseStndCodes'].map(lambda x: 'RR101' in x)
sf = megaparcels.loc[sf_ind, :]

#%% Extract MF Sample

mf_ind = megaparcels['PropertyLanduseStndCodes'].map(lambda x: 'RR')

#%% Plot Distributions

def SizeVintageJointPlot(data, title):

    g = sns.jointplot(
        y = 'TotalBuildingAreaSqFt',
        x = 'MedianYearBuilt',
        data = sf,
        marker = '.',
        kind = 'reg',
        line_kws={"color": "red"},
        scatter_kws={'alpha':0.05},
        height = 10
    )

    g.ax_joint.set_yscale('log')
    g.ax_joint.set_xlim((1900,2023))
    g.ax_joint.set_ylim(100,100000)
    g.ax_joint.grid(True, which = 'both')

    plt.tick_params(axis='y', which='minor')
    g.ax_joint.yaxis.set_minor_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    g.ax_joint.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    g.ax_joint.tick_params(axis='y', which = 'minor', labelsize = 7, rotation = 45)
    g.ax_marg_y.axis('off')
    g.ax_marg_x.axis('off')

    g.ax_joint.set_xlabel('Construction Vintage Year')
    g.ax_joint.set_ylabel('Building Square Footage')

    g.savefig(out + title, bbox_inches = 'tight', dpi = 300)

    return

#%% Generate SF Plot

SizeVintageJointPlot(sf, 'sf_joint_plot.png')

# %% Compute Difference Stats

old_ind = (sf['MedianYearBuilt'] < 1920)
new_ind = (sf['MedianYearBuilt'] > 2000)

old_median = sf.loc[old_ind, 'TotalBuildingAreaSqFt'].median()
new_median = sf.loc[new_ind, 'TotalBuildingAreaSqFt'].median()

diff = (new_median - old_median ) / old_median
