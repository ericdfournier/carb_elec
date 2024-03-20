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

# Extract Single Family Data from Model Data Table
query = ''' SELECT megaparcelid,
                   "YearBuilt",
                   "TotalBuildingAreaSqFt",
                   "TotalNoOfUnits",
                   sampled,
                   usetype,
                   panel_size_as_built,
                   ciscorep,
                   issued_date,
                   solar_pv_system,
                   battery_storage_system,
                   ev_charger,
                   heat_pump,
                   main_panel_upgrade,
                   sub_panel_upgrade,
                   upgraded_panel_size
            FROM corelogic.model_data
            WHERE usetype = 'single_family';'''

mp = pd.read_sql(query, db_con)

#%% Process Fields

# Set megaparcelid as index
mp.set_index('megaparcelid', drop = True, inplace = True)

# Null out bogus vintage years
invalid_ind = mp['YearBuilt'] > 2024
mp.loc[invalid_ind,'YearBuilt'] = np.nan

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

#%% Generate ECDFS by CES Bin in Anticipate of Inference

# Bin Properties by CES Score
bins = np.arange(0,105,5)
classes = [str(x) for x in np.arange(0,100,5)]
mp['ces_bin'] = pd.cut(
    mp['ciscorep'],
    bins = bins,
    labels = classes)

# Generate figure axes
fig, ax = plt.subplots(1,1, figsize=(5,5))

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

        # Filter Properties without a valid permit issue date
        date_ind = ~mp['issued_date'].isna()

        # Combine indices to master
        master_ind = (subset_ind) & (nan_ind) & (perm_ind) & (date_ind)

        # Filter and copy subset data
        data = mp.loc[master_ind,:].copy()

        # Extract Permit Issue Year
        permit_issue_year = data.loc[:,'issued_date'].dt.year

        # Extract Construction Vintage Year
        construction_year = data.loc[:,'YearBuilt']

        # Compute the Current Age of the Properties
        current_year = 2024
        current_age = current_year - construction_year

        # Compute the Age of the Properties in the Year in Which Permits were Issued (if any)
        permit_age = current_age - (current_year - permit_issue_year)

        # Generate ECDFS Based Upon the Age of Properties at the time Their Permits Were Issued for Permitted Properties
        ecdfs[c] = ECDF(permit_age)

        # Generate ECDF Sample Data
        x = np.linspace(current_age.min(), current_age.max(), n)
        y[i,:] = ecdfs[c](x)

        # Test plot
        ax.step(x, y[i,:], color = palette[i])

        # Increment progress bar
        pbar.update(1)

# Style figure elements
ax.grid(True)
ax.set_xlabel('Home Age')
ax.set_ylabel('Cumulative Probability Density')
ax.set_title('ECDFs of Permitted Panel Upgrades\nby CES Percentile Score Range')
ax.set_xlim((0, 130))

labels = []
values = mp['ces_bin'].cat.categories.to_list()

for i, x in enumerate(values):
    if i < len(values)-1:
        label = '[' + str(values[i]) + ', ' + str(values[i+1]) + ')'
    else:
        label = '[' + values[i] +  ', 100]'
    labels.append(label)

ax.legend(labels, loc = 'center left', bbox_to_anchor=(1.0, 0.5))
ax.get_legend().set_title("CES Percentile\nScore Range")

# Save figure to file
fig.savefig('/Users/edf/repos/carb_elec/model/corelogic/fig/sf_ecdfs.png',
    bbox_inches = 'tight',
    dpi = 300)

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
    if as_built in sm:
        # Small size upgrades decided via random choice over three options
        # since the timing of the upgrade is unknown and requirements will vary
        # in time. The probabilities are weighted based upon the size
        # distribution of observed panel upgrades in the permit database.
        existing = np.random.choice(
            [100., 125., 150., 200.], # Choice options
            p = [0.14, 0.10, 0.01, 0.75]) # Choice probabilities
    elif as_built in med:
        # medium size upgrades decided via random choice over two options since
        # 225 Amp panels have been growing in popularity recently
        existing = np.random.choice(
            [200., 225.],
            p = [0.75, 0.25])
    elif as_built in lg:
        existing = 400.
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

    # Set observed to false as default
    observed = False

    # If permited upgrade and destination panel size was specified in permit
    if ~np.isnan(row['upgraded_panel_size']):

        existing = row['upgraded_panel_size']
        valid_panels = [30, 60, 100, 125, 150, 200, 225, 320, 400, 600, 800, 1000, 1200]
        observed = True

        # If the existing panel size is not in the valid set, take the closest
        # value and mark it as the product of inference
        if existing not in valid_panels:

            existing = min(valid_panels, key=lambda x:abs(x - existing))
            observed = False

    # Where destination panel size was not specified
    else:
        # If any of the upgrade categories are true set minimum size to 200 amps
        if (row['solar_pv_system']) | (row['battery_storage_system']) | (row['ev_charger']) | (row['main_panel_upgrade']):
                if as_built < 200.:
                    existing = 200.
                else:
                    existing = UpgradeFromAsBuilt(as_built)
        # If upgrade destination size
        else:
            existing = UpgradeFromAsBuilt(as_built)

    return existing, observed

#%% Loop through all records and assign existing panel size from upgrade choice and ladder value

# Allocate output fields
mp['inferred_panel_upgrade'] = False
mp['observed_panel_upgrade'] = False

# limit valid indices to only where as_built panel sizes are known
valid_ind = ~mp['panel_size_as_built'].isna()

# set up progress bar
with tqdm(total = valid_ind.shape[0]) as pbar:

    # iterate through valid megaparcel ids
    for i, row in mp.loc[valid_ind,:].iterrows():

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
            existing, observed = UpgradeFromPermit(as_built, row)
            mp.loc[i,'panel_size_existing'] = existing
            mp.loc[i,'observed_panel_upgrade'] = observed
        else:
            mp.loc[i,'panel_size_existing'] = as_built

        # Increment progress bar
        pbar.update(1)

mp['any_panel_upgrade'] = mp.loc[:,['permitted_panel_upgrade','inferred_panel_upgrade']].any(axis = 1)

# Write Output to PostGIS

output_cols = [
    'ces_bin',
    'permitted_panel_upgrade',
    'observed_panel_upgrade',
    'inferred_panel_upgrade',
    'any_panel_upgrade',
    'panel_size_existing']

mp.loc[:,output_cols].to_sql(
    name = 'model_data_sf_inference',
    con = db_con,
    if_exists = 'replace',
    schema = 'corelogic',
    index = True)
