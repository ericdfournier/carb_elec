
#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import sqlalchemy as sql
import os
from sklearn.preprocessing import MinMaxScaler

#%% Instantiate MinMaxScaler

scaler = MinMaxScaler()

#%% Set Environment

root = '/Users/edf/repos/carb_elec/analyses/commercial_sub_sector_electrification_readiness'

#%% Import End-Use Breakdown Data

file = '/data/inputs/commercial_enduses.csv'

enduse_coeff = pd.read_csv(
    root + file)

#%% Compute end-use coefficient standard deviations

cols = ['space_heating', 'space_cooling', 'water_heating', 'cooking', 'miscellaneous', 'processing']
coeff_std = (1 / enduse_coeff.loc[:,cols].std(axis = 1))

scaler = MinMaxScaler()
enduse_coeff['coeff_std'] = scaler.fit_transform(coeff_std.to_frame())

#%% Import End-Use TRL Based Scores

file = '/data/inputs/commercial_scores.csv'

trl_scores = pd.read_csv(
    root + file)

# Flip Directionality of Scores
norm = trl_scores.copy(deep = True)
cols = ['space_heating', 'space_cooling', 'water_heating',
       'cooking', 'miscellaneous', 'processing']
norm.loc[:,cols] = 11

trl_scores.loc[:,cols] = norm.loc[:,cols] - trl_scores.loc[:,cols]

#%% Import Facility Attribute Data

file = '/data/inputs/commercial_facility_stats.csv'

facility_stats = pd.read_csv(
    root + file)

# Normalize Vintage
scaler = MinMaxScaler()
facility_stats['vintage_norm'] = (1 - scaler.fit_transform(facility_stats['median_vintage'].to_frame()))

# Normalize Sqft
scaler = MinMaxScaler()
facility_stats['sqft_norm'] = scaler.fit_transform(facility_stats['median_sqft'].to_frame())

#%% Import Sector Stats Data

file = '/data/inputs/commercial_sector_stats.csv'

sector_stats = pd.read_csv(
    root + file)

# Normalize Usage
scaler = MinMaxScaler()
facility_stats['usage_norm'] = scaler.fit_transform(sector_stats['total_therms'].to_frame())

#%% Generate Scores

output = pd.DataFrame(
    data = facility_stats[['ceus_subsector', 'dac']])
output[['raw_score', 'normalized_score', 'ranking']] = np.nan

#%% Compute Raw + Normalized Scores and Rankings

for i, row in facility_stats.iterrows():

    coeff_cols = ['space_heating', 'space_cooling', 'water_heating',
       'cooking', 'miscellaneous', 'processing']
    coeff_ind = enduse_coeff['ceus_subsector'] == row['ceus_subsector']
    coeff = enduse_coeff.loc[coeff_ind, coeff_cols].values

    score_cols = ['space_heating', 'space_cooling', 'water_heating',
       'cooking', 'miscellaneous', 'processing']
    score_ind = trl_scores['ceus_subsector'] == row['ceus_subsector']
    score = trl_scores.loc[score_ind,score_cols].values

    enduse_std = enduse_coeff.loc[coeff_ind, 'coeff_std'].values[0]

    output.loc[i,'raw_score'] = row['vintage_norm'] + row['sqft_norm'] + row['usage_norm'] + enduse_std + (np.sum(coeff * score))

# Rank Outputs
scaler = MinMaxScaler()
output['normalized_score'] = np.ceil(scaler.fit_transform(output['raw_score'].to_frame()) * 100)
output['ranking'] = output['normalized_score'].rank()

output = output.sort_values(by = 'ceus_subsector')

#%% Compute Average Raw Scores

total = output.loc[:,['ceus_subsector', 'raw_score']].groupby('ceus_subsector').agg('mean')
total['ranking'] = total['raw_score'].rank()

#%% Output to File for Report Formatting

cols = ['ceus_subsector', 'dac', 'raw_score']
output_export = output.loc[:,cols].set_index(['ceus_subsector','dac']).unstack()
output_export.to_csv(root + '/data/postprocessing/commercial_readiness_total_results.csv')
