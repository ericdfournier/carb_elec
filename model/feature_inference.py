#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
from statsmodels.distributions.empirical_distribution import ECDF
import random
import os

#%% Generate Dataset

# Extract Database Connection Parameters from Environment
host = os.getenv('PGHOST')
user = os.getenv('PGUSER')
password = os.getenv('PGPASS')
port = os.getenv('PGPORT')
db = 'carb'

# Establish DB Connection
db_con_string = 'postgresql://' + user + '@' + host + ':' + port + '/' + db
db_con = sql.create_engine(db_con_string)

# Extract Single Family
query = ''' SELECT megaparcelid,
                   "YearBuilt",
                   sampled,
                   usetype,
                   panel_size_as_built,
                   ciscorep,
                   permit_id,
                   issued_date,
                   solar_pv_system,
                   battery_storage_system,
                   ev_charger,
                   heat_pump,
                   main_panel_upgrade,
                   sub_panel_upgrade,
                   upgraded_panel_size
            FROM ztrax.model_data
            WHERE
                usetype = 'single_family' AND
                sampled = TRUE;'''
mp = pd.read_sql(query, db_con)

# Drop duplicates
mp.drop_duplicates(keep = 'first', inplace = True)

# Set megaparcelid as index
mp.set_index('megaparcelid', drop = True, inplace = True)

#%% Prep Fields

'''Routine to infer the existing panel size for a buildng that did not
receive any previous permitted work. The inference model is based upon
the empirical ECDF which relates the age of the home to the probability
of permitted work by DAC status.'''

# Bin Properties by CES Score
bins = np.arange(0,105,5)
classes = [str(x) for x in np.arange(0,20,1)]
mp['ces_bin'] = pd.cut(
    mp['ciscorep'],
    bins = bins,
    labels = classes)

# Filter Properties with Panel Upgrade Permits
permit_cols = [
    'solar_pv_system',
    'battery_storage_system',
    'ev_charger',
    'heat_pump',
    'main_panel_upgrade',
    'sub_panel_upgrade']
mp[permit_cols] = mp[permit_cols].astype(bool)
mp['permitted_panel_upgrade'] = mp.loc[:,permit_cols].any(axis = 1) == True

mp['issued_date'] = pd.to_datetime(
    mp['issued_date'],
    format = '%Y-%m-%d')

ecdfs = {}

#%% Enter ECDF Generation Loop

# Generate figure axes
fig, ax = plt.subplots(1,1, figsize=(7,7))

# Allocate ECDF sample data array
n = 100
y = np.zeros((len(classes),n))

# Generate color ramp for plotting by CES score bin
palette = sns.color_palette('rainbow', len(classes))

for i, c in enumerate(classes):

    # Filter on CES bin value
    subset_ind = mp['ces_bin'] == c

    # Filter Properties with no construction vintage data
    nan_ind = ~mp.loc[:,'YearBuilt'].isna()

    # Filter Properties with permitted panel upgrades
    perm_ind = mp['permitted_panel_upgrade'] == True

    # Combine indices to master
    master_ind = (subset_ind) & (nan_ind) & (perm_ind)

    # Filter and copy subset data
    data = mp.loc[master_ind,:].copy()

    # Extract Permit Issue Year
    permit_issue_year = data.loc[:,'issued_date'].dt.year

    # Extract Construction Vintage Year
    construction_year = data.loc[:,'YearBuilt']

    # Compute the Current Age of the Properties
    current_year = 2022
    current_age = current_year - construction_year

    # Compute the Age of the Properties in the Year in Which Permits were Issued (if any)
    permit_age = current_age - (current_year - permit_issue_year)

    # Generate ECDFS Based Upon the Age of Properties at the time Their Permits Were Issued for Permitted Properties
    ecdfs[c] = ECDF(permit_age)

    # Generate ECDF Sample Data
    x = np.linspace(min(current_age), max(current_age), n)
    y[i,:] = ecdfs[c](x)

    # Test plot
    ax.step(x, y[i,:], color = palette[i])
    ax.set_xlim((0, 130))

# Style figure
ax.grid(True)
ax.set_xlabel('Home Age')
ax.set_ylabel('Cumulative Probability Density')
ax.set_title('ECDF of Permitted Panel Upgrades\nby CES Percentile Score Range')

#%% Iterate through each CDF and determininstically generate previous upgrade predictions

# Seed random number generator for deterministic output
random.seed(123456)
mp['previous_upgrade'] = False

# Iterate through ecdf dictionary
for c, ecdf in ecdfs.items():

    # Debug
    print('CES Class: {}'.format(c))

    # Filter on CES bin value
    subset_ind = mp['ces_bin'] == c

    # Filter Properties with no construction vintage data
    nan_ind = ~mp.loc[:,'YearBuilt'].isna()

    # Filter Properties without permitted panel upgrades
    perm_ind = mp['permitted_panel_upgrade'] == False

    # Combine indices to master
    master_ind = (subset_ind) & (nan_ind) & (perm_ind)

    # Extract the Current Ages of the DAC Inference Group of Non-Permitted Properties
    data = mp.loc[master_ind,:].copy()

    # Extract Construction Vintage Year
    construction_year = data.loc[:,'YearBuilt']

    # Compute the Current Age of the Properties
    current_year = 2022
    current_age = current_year - construction_year

    # Output the Probability of an Upgrade Based upon the DAC-ECDF
    prob = ecdfs[c](current_age)

    # Pre-allocate boolean choice output array
    upgrade_choices = np.zeros((prob.shape[0])).astype(bool)

    # Iterate through all of the unpermitted properties and assign an inferred upgrade outcome
    for i, p in enumerate(prob):
        upgrade_choices[i] = np.random.choice(
                np.array([False, True]),
                size = 1,
                p = [1.0-p, p])[0]

    # Write upgrade choices back to main dataframe
    mp.loc[master_ind, 'previous_upgrade'] = upgrade_choices

#%% Loop through all records and assign existing panel size from upgrade choice and ladder value

# NOTE: Long runtime on this due to the need to iterate through each of the
# 3 million plus parcels in the dataset. Make sure to pickle output on
# completion...

upgrade_scale = [
    0.,
    30.,
    40.,
    60.,
    100.,
    125.,
    150.,
    200.,
    225.,
    320.,
    400.,
    600.,
    800.,
    1000.,
    1200.,
    1400.]

mp['inferred_panel_upgrade'] = False
valid_ind = ~mp['panel_size_as_built'].isna()

with tqdm(total = mp.shape[0]) as pbar:

    for i, row in mp[valid_ind].iterrows():

        #TODO: Deal with Duplicates from Multiple Permit Occurences (i.e. multiple return rows)

        as_built = mp.loc[i,'panel_size_as_built']
        existing = as_built

        if (row['previous_upgrade'] == True) & (row['permitted_panel_upgrade'] == False):
            level = upgrade_scale.index(as_built)
            existing = upgrade_scale[level + 1]
            mp.loc[i,'inferred_panel_upgrade'] = True
        else:
            mp.loc[i,'panel_size_existing'] = existing

        pbar.update(1)

mp['any_panel_upgrade'] = mp.loc[:,['permitted_panel_upgrade','inferred_panel_upgrade']].any(axis = 1)

# Write output to pickle

mp.to_pickle('/Users/edf/repos/carb_elec/model/model_data.pkl')
