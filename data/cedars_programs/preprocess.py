#%% Import Packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine

#%% Read Raw Data

root = '/Users/edf/repos/carb_elec/data/cedars_programs/'
cedars = pd.read_csv(root+'raw/cedars_cleaned.csv')

#%% Plot Hist to Establish Measure Cost Threshold

valid_ind = (cedars['Gross Measure Cost'] > 0) * (~np.isinf(cedars['Gross Measure Cost']))
data = np.log10(cedars.loc[valid_ind,'Gross Measure Cost'])

fig, ax = plt.subplots(1,1, figsize=(7,5))
data.plot(
    kind = 'hist',
    bins = 100,
    ax = ax,
    log = True,
    grid = True)
ax.axvline(5, linestyle = '--', color = 'tab:red')
xticks = np.arange(0,8)
xticklabels = ['$10^0$','$10^1$', '$10^2$', '$10^3$', '$10^4$', '$10^5$', '$10^6$', '$10^7$']
ax.set_xticks(xticks, xticklabels)
ax.set_ylabel('Participant Frequency\n[Counts]')
ax.set_xlabel('Gross Measure Cost\n[$]')
ax.set_ylim((0, 10000))
fig.savefig(root+'img/major_minor_threshold_hist_plot.png', bbox_inches = 'tight', dpi = 300)

#%% Split Dataset

thresh = np.power(10,5)
major_ind = (valid_ind) & (cedars['Gross Measure Cost'] > thresh)
cedars_major = cedars.loc[major_ind,:].copy()

minor_ind = (valid_ind) & (cedars['Gross Measure Cost'] <= thresh)
cedars_minor = cedars.loc[minor_ind,:].copy()

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

#%% Write the Cedars Minor Dataframe to PostGIS

cols = cedars_minor.columns.to_list()
cols.remove('Unnamed: 0')

cedars_minor.loc[:,cols].to_sql('fuel_switching_program_participants',
    if_exists = 'replace',
    index = False,
    schema = 'cedars',
    con = engine)
