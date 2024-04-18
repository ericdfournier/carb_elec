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
from tqdm import tqdm

#%% Set Fixed Parameters

table_dir = '/Users/edf/repos/carb_elec/analyses/carb_crosstab_data/csv/'

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

#%% Merge SF and MF data

mp = pd.concat([sf, mf], axis = 0)

#%% Generate Breaks and Labels for Aggregations

luse_codes = {
    'Single-Family Detached': [100,109,148,160,163],
    'Single-Family Attached': [102],
    '2-4 Unit Residential': [115,151,165],
    '5+ Unit Residential': [103,106,131,132,133],
    'Mobile/Manufactured Homes': [135, 137, 138]
}

sqft_bins = [
    0,
    250,
    500,
    750,
    1000,
    1250,
    1500,
    2000,
    2500,
    3000,
    4000,
    5000,
    sf['TotalBuildingAreaSqFt'].max() + 1
]

sqft_labels = [
    '0 - 249',
    '250 - 499',
    '500 - 749',
    '750 - 999',
    '1,000 - 1,249',
    '1,250 - 1,499',
    '1,500 - 1,999',
    '2,000 -  2,499',
    '2,500 - 2,999',
    '3,000 - 3,999',
    '4,000 - 4,999',
    '>= 5,000'
]

vintage_bins = [
    0,
    1950,
    1960,
    1970,
    1980,
    1990,
    2000,
    2010,
    2020,
    sf['YearBuilt'].max() + 1
]

vintage_labels = [
    'Pre- 1950',
    '1950 - 1959',
    '1960 - 1969',
    '1970 - 1979',
    '1980 - 1989',
    '1990 - 1999',
    '2000 - 2010',
    '2010 - 2020',
    'Post - 2020'
]

#%% Flag Usetypes

for i, r in tqdm(mp['PropertyLandUseStndCodes'].items(), total = mp.shape[0]):
    for k, v in luse_codes.items():
        if bool(set(r) & set(v)):
            match = k
            break
    mp.loc[i,'carb_luse_code'] = match

#%% Bin Square Footages

mp['carb_sqft_bin'] = pd.cut(
    mp['TotalBuildingAreaSqFt'],
    bins = sqft_bins,
    labels = sqft_labels
)

#%% Bin Vintage Years

mp['carb_vintage_bin'] = pd.cut(
    mp['YearBuilt'],
    bins = vintage_bins,
    labels = vintage_labels
)

#%% Generate Aggregated Counts

ind = ~mp['panel_size_existing'].isna() & ~(mp['carb_luse_code'] == 'Mobile/Manufactured Homes')
cols = [
    'tract_geoid_2019',
    'carb_luse_code',
    'carb_vintage_bin',
    'carb_sqft_bin',
    'panel_size_existing'
]
#%% Perform Aggregations and Filter Output for Empty Values

out_series = mp.loc[ind, cols].groupby(cols[:3], observed = False).value_counts()
out_df = out_series.to_frame().reset_index(inplace = False)
out_df_filtered = out_df.loc[out_df['count'] != 0,:]
final = out_df_filtered.reset_index(inplace = False, drop = True)

#%% Sort Values before Writing to File

final_sorted = final.sort_values(
    by = cols,
    ascending = True,
    axis = 0,
    inplace = False).reset_index(drop = True, inplace = False)

#%% Write Sorted Output to File

final_sorted.to_csv(table_dir + 'carb_panel_size_estimate_crosstabulation_output.csv', index = False)
