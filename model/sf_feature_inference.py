#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
import warnings
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
                   "TotalBuildingAreaSqFt",
                   "TotalNoOfUnits",
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

#%% Process Fields

# Set megaparcelid as index
mp.set_index('megaparcelid', drop = True, inplace = True)

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

# Convert issued date to datetime
mp['issued_date'] = pd.to_datetime(
    mp['issued_date'],
    format = '%Y-%m-%d')

#%% Deduplicate Based Upon Unique Megaparcel ID Values

def DeduplicateRecords(mp):

    # specify index and column names
    index = mp.index.unique()
    columns = mp.columns

    # allocate cleaned array with unique mp id index
    clean = pd.DataFrame(
        index = index,
        columns = columns)

    # ensure consistent types in clean version
    clean = clean.astype(mp.dtypes.to_dict())

    # Set up progress bar
    with tqdm(total = clean.shape[0]) as pbar:

        # Iterate over unique mp ids
        for i in clean.index:

            # extract subset of records for mp id
            subset = mp.loc[i,:]

            # Where multiple records found for the same id
            if len(subset.shape) > 1:

                # initialize cleaned ouptut values as first entry in subset
                clean.loc[i,:] = subset.iloc[0]

                # specify permit columns
                permit_cols = [
                        'solar_pv_system',
                        'battery_storage_system',
                        'ev_charger',
                        'heat_pump',
                        'main_panel_upgrade',
                        'sub_panel_upgrade']

                # coalesce permit flag values across subset records
                clean.loc[i, permit_cols] = subset[permit_cols].any()

                # select most recent issue date if non null
                if pd.isnull(subset['issued_date']).all() == False:

                    clean.loc[i,'issued_date'] = subset['issued_date'].dropna().max()

                # coalesce permit id values if non null
                if subset['permit_id'].any():

                    clean.loc[i,'permit_id'] = ', '.join(map(str, subset['permit_id'].dropna().values ))

                # coalesce panel size records if non null
                if subset['upgraded_panel_size'].any():

                    clean.loc[i,'upgraded_panel_size'] = subset['upgraded_panel_size'].dropna().max()

            # if only record found, populate cleaned array and iterate
            else:

                clean.loc[i,:] = subset

            # Increment progress bar
            pbar.update(1)

    return clean

# Run deduplication routine
mp = DeduplicateRecords(mp)

#%% Generate ECDFS by CES Bin in Anticipate of Inference

# Bin Properties by CES Score
bins = np.arange(0,105,5)
classes = [str(x) for x in np.arange(0,20,1)]
mp['ces_bin'] = pd.cut(
    mp['ciscorep'],
    bins = bins,
    labels = classes)

# Generate figure axes
fig, ax = plt.subplots(1,1, figsize=(7,7))

# Allocate ECDF sample data array
n = 100
y = np.zeros((len(classes),n))

# Generate color ramp for plotting by CES score bin
palette = sns.color_palette('rainbow', len(classes))

#Enter ECDF Generation Loop

ecdfs = {}

# Set up progress bar
with tqdm(total = len(classes)) as pbar:

    # Iterate through CES classes
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

        # Increment progress bar
        pbar.update(1)

# Style figure elements
ax.grid(True)
ax.set_xlabel('Home Age')
ax.set_ylabel('Cumulative Probability Density')
ax.set_title('ECDF of Permitted Panel Upgrades\nby CES Percentile Score Range')

#%% Iterate through each CDF and determininstically generate previous upgrade predictions

# Seed random number generator for deterministic output
random.seed(123456)
mp['previous_upgrade'] = False

# Set up progress bar
with tqdm(total = len(ecdfs)) as pbar:

    # Iterate through ecdf dictionary
    for c, ecdf in ecdfs.items():

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

        # Increment progress bar
        pbar.update(1)


#%% Panel upgrade size step function

def UpgradeFromAsBuilt(as_built):
    '''Function to increment as_built panel sizes to a reasonable existing size
    in a sane quantized manner'''

    # specify target panel class size groups
    sm = [
        0.,
        30.,
        40.,
        60.
    ]

    med =  [
        100.,
        125.,
        150.
    ]

    lg = [
        200.,
        225.
    ]

    xl = [
        320.,
        400.
    ]

    xxl = [
        600.,
        800.,
        1000.,
        1200.,
        1400.
    ]

    # switch on class size set intersection
    if (as_built in sm) or (as_built in med):
        existing = 200.
    elif as_built in lg:
        existing = 320.
    elif as_built in xl:
        existing = 600.
    elif as_built in xxl:
        level = xxl.index(as_built)
        existing = xxl[level + 1]
    else:
        warnings.warn("Provided As-Built Panel Size Not Expected!")
        existing = np.nan

    return existing

#%% Upgrade From Permitted Work

def UpgradeFromPermit(as_built, row):

    # If permited upgrade and destination panel size was specified in permit
    if ~np.isnan(row['upgraded_panel_size']):
        existing = row['upgraded_panel_size']
    # Where destination panel size was not specified
    else:
        # If any of the upgrade categories are true set minimum size to 200 amps
        if (row['solar_pv_system']) | (row['battery_storage_system']) | (row['ev_charger']) | (row['main_panel_upgrade']):
                if existing < 200.:
                    existing = 200.
                else:
                    existing = UpgradeFromAsBuilt(as_built)
        # If upgrade destination size
        else:
            existing = UpgradeFromAsBuilt(as_built)

    return existing

#%% Loop through all records and assign existing panel size from upgrade choice and ladder value

# Allocate output fields
mp['inferred_panel_upgrade'] = False

# limit valid indices to only where as_built panel sizes are known
valid_ind = ~mp['panel_size_as_built'].isna()

# set up progress bar
with tqdm(total = valid_ind.shape[0]) as pbar:

    # iterate through valid megaparcel ids
    for i, row in mp[valid_ind].iterrows():

        # get current as_built panel size for future reference
        as_built = mp.loc[i,'panel_size_as_built']

        # If the previous upgrade flag is true and no_permitted_panel_ugprade has
        # ocurred then infer existing panel size by incrementing from as_built
        if (row['previous_upgrade'] == True) & (row['permitted_panel_upgrade'] == False):
            existing = UpgradeFromAsBuilt(as_built)
            mp.loc[i,'panel_size_existing'] = existing
            mp.loc[i,'inferred_panel_upgrade'] = True
        elif row['permitted_panel_upgrade'] == True:
            # Set existing panel size to as_built if no inferred upgrade has occured
            existing = UpgradeFromPermit(as_built, row)
        else:
            mp.loc[i,'panel_size_existing'] = as_built

        # Increment progress bar
        pbar.update(1)

mp['any_panel_upgrade'] = mp.loc[:,['permitted_panel_upgrade','inferred_panel_upgrade']].any(axis = 1)

# Write output to pickle

mp.to_pickle('/Users/edf/repos/carb_elec/model/data/sf_model_data.pkl')
