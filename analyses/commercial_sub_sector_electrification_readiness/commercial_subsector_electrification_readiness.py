
#%% Package Imports

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import sqlalchemy as sql
import os
import jenkspy

#%% Set Fixed Parameters

sectors = [ 'durable_goods_manufacturing',
            'nondurable_goods_manufacturing',
            'food_processing', # NOTE: This is a category mislabel - "Food Processing" is actually "Food Stores" as represented by Maya in this analysis
            'colleges',
            'healthcare',
            'hotels',
            'miscellaneous',
            'offices',
            'refrigerated_warehouses',
            'restaurants',
            'retail',
            'schools',
            'warehouses']

root = '/Users/edf/repos/carb_elec/analyses/commercial_sub_sector_electrification_readiness'

# Allocate Receiver Data Structures
dtypes = {}
enduses = {}
enduse_coeff = {}
scores = {}
out = {}

#%% Read Manufacturing End-Use Coeefficient CSV Files

# durable goods manufacturing
dtypes[sectors[0]] = {  'NAICS': str,
            'CHP and/or Cogeneration Process': float,
            'Conventional Boiler Use': float,
            'Conventional Electricity Generation': float,
            'Electro-Chemical Processes': float,
            'Facility HVAC': float,
            'Facility Lighting': float,
            'Machine Drive': float,
            'Onsite Transportation': float,
            'Other Facility Support': float,
            'Other Nonprocess Use': float,
            'Other Process Use': float,
            'Process Cooling and Refrigeration': float,
            'Process Heating': float,
            'Total': float }

enduse_coeff[sectors[0]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[0]),
    dtype = dtypes[sectors[0]])

# non-durable goods manufacturing
dtypes[sectors[1]] = dtypes[sectors[0]]
enduse_coeff[sectors[1]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[1]),
    dtype = dtypes[sectors[1]])


#%% Read Commercial End-Use Coefficient CSV File

# commercial food processing
dtypes[sectors[3]] = {    'VALID NAICS': str,
                            'NAICS Ttile': str,
                            'SubCategory': str,
                        	'CEUS SUBCATEGORY': str,
                            'Heat': float,
                            'Cool': float,
                            'WH': float,
                            'Cook': float,
                            'Misc.': float,
                            'Proc.': float,
                            'Total': float}

enduse_coeff[sectors[3]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[3]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[3]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial colleges
enduse_coeff[sectors[4]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[4]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[4]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial healthcare
enduse_coeff[sectors[5]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[5]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[5]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial hotels
enduse_coeff[sectors[6]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[6]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[6]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial miscellaneous
enduse_coeff[sectors[7]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[7]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[7]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial offices
enduse_coeff[sectors[8]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[8]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[8]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial refrigerated warehouses
enduse_coeff[sectors[9]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[9]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[9]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial restaurants
enduse_coeff[sectors[10]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[10]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[10]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial retail
enduse_coeff[sectors[11]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[11]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[11]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial schools
enduse_coeff[sectors[12]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[12]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[12]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

# commercial warehouses
enduse_coeff[sectors[13]] = pd.read_csv(
    root + '/data/inputs/{}.csv'.format(sectors[13]),
    dtype = dtypes[sectors[3]])
enduse_coeff[sectors[13]].rename(columns={'VALID NAICS':'NAICS'}, inplace = True)

#%% Add Routine to Drop Null Records and Clean Up Indexes

for k, v in enduse_coeff.items():

    enduse_coeff[k] = v.dropna(subset = 'NAICS', axis = 0)

#%% Assing Manufacturing End-Uses Scores

#NOTE: Scores should be based upon technological readiness levels (TRL) 1-9 +
# a 10 for commercially available technologies

scores[sectors[0]] = [  6, # 'CHP and/or Cogeneration Process'
                        10, # 'Conventional Boiler Use'
                        10, # 'Conventional Electricity Generation'
                        4, # 'Electro-Chemical Processes'
                        10, # 'Facility HVAC'
                        10, # 'Facility Lighting'
                        9, # 'Machine Drive'
                        10, # 'Onsite Transportation'
                        9, # 'Other Facility Support'
                        6, # 'Other Nonprocess Use'
                        4, # 'Other Process Use'
                        6, # 'Process Cooling and Refrigeration'
                        5] # 'Process Heating'

enduses[sectors[0]] =  [   'CHP and/or Cogeneration Process',
# Combined heat an power is a tricky one. You need to offset the generation of
# electricity from the on-site combustion of natural gas and then figure out an
# end-use technology subsitute for the production and use of steam (in-most
# cases). So from a readiness standpoint it is not so much a question of
# whether substitute technologies exist, but the degree to which the energy
# system/end-use technologies of the building are highly integrated and thus
# would be more costly/distruptive to replace.
#
# Ref - https://erc.uic.edu/wp-content/uploads/sites/633/2024/07/8-24-23-Ohio-Industrial-Decarb-and-CHP-Workshop-Haefke-ver08-22-23.pdf
# Ref -
                                'Conventional Boiler Use',
# Ref - https://www.energy.gov/sites/default/files/2024-04/Large%20Building%20Boiler%20Electrification%20Guidance.pdf
                                'Conventional Electricity Generation',
                                'Electro-Chemical Processes',
                                'Facility HVAC',
                                'Facility Lighting',
                                'Machine Drive',
                                'Onsite Transportation',
                                'Other Facility Support',
                                'Other Nonprocess Use',
                                'Other Process Use',
                                'Process Cooling and Refrigeration',
                                'Process Heating']

scores[sectors[1]] = scores[sectors[0]]
enduses[sectors[1]] = enduses[sectors[0]]

#%% Assign Commercial End-Use Scores

#NOTE: Scores should be based upon technological readiness levels (TRL) 1-9 +
# a 10 for commercially available technologies
scores[sectors[3]] = [  10, # 'Heat'
                        10, # 'Cool'
                        10, # 'WH'
                        8, # 'Cook'
                        7, # 'Misc.'
                        5] # 'Proc.'

enduses[sectors[3]] = [ 'Heat',
                        'Cool',
                        'WH',
                        'Cook',
                        'Misc.',
                        'Proc.']

# commercial colleges
scores[sectors[4]] = scores[sectors[3]]
enduses[sectors[4]] = enduses[sectors[3]]

# commercial healthcare
scores[sectors[5]] = scores[sectors[3]]
enduses[sectors[5]] = enduses[sectors[3]]

# commercial hotels
scores[sectors[6]] = scores[sectors[3]]
enduses[sectors[6]] = enduses[sectors[3]]

# commercial miscellaneous
scores[sectors[7]] = scores[sectors[3]]
enduses[sectors[7]] = enduses[sectors[3]]

# commercial offices
scores[sectors[8]] = scores[sectors[3]]
enduses[sectors[8]] = enduses[sectors[3]]

# commercial refrigerated warehouses
scores[sectors[9]] = scores[sectors[3]]
enduses[sectors[9]] = enduses[sectors[3]]

# commercial restaurants
scores[sectors[10]] = scores[sectors[3]]
enduses[sectors[10]] = enduses[sectors[3]]

# commercial retail
scores[sectors[11]] = scores[sectors[3]]
enduses[sectors[11]] = enduses[sectors[3]]

# commercial schools
scores[sectors[12]] = scores[sectors[3]]
enduses[sectors[12]] = enduses[sectors[3]]

# commercial warehouses
scores[sectors[13]] = scores[sectors[3]]
enduses[sectors[13]] = enduses[sectors[3]]

#%%
