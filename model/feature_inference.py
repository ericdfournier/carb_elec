#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import matplotlib.pyplot as plt
import numpy as np

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
query = ''' SELECT A.*,
            FROM ztrax.megaparcels AS A
            WHERE ST_INTERSECTS(A.centroid, B.geom) AND
                A.usetype = 'single_family';'''
raw = pd.read_sql(query, db_con)
raw.set_index('rowid', drop = True, inplace = True)

return raw

    '''Function to infer the existing panel size for a buildng that did not
    receive any previous permitted work. The inference model is based upon
    the empirical ECDF which relates the age of the home to the probability
    of permitted work by DAC status.'''

    # Filter Properties with no construction vintage data
    nan_ind = ~data.loc[:,'MedianYearBuilt'].isna()

    # Bin Properties by CES Score


    # Filter Properties with Panel Upgrade Permits
    permit_ind = data.loc[:,'permitted_panel_upgrade'] == True

    # Extract Permit Issue Year
    permit_issue_year = data.loc[:,'permit_issue_date'].dt.year

    # Extract Construction Vintage Year
    construction_year = data.loc[:,'MedianYearBuilt'].dt.year

    # Compute the Current Age of the Properties
    current_age = 2022 - construction_year

    # Compute the Age of the Properties in the Year in Which Permits were Issued (if any)
    permit_age = current_age - (2022 - permit_issue_year)

    # Generate ECDFS Based Upon the Age of Properties at the time Their Permits Were Issued for Permitted Properties
    dac_ecdf = ECDF(permit_age.loc[nan_ind & dac_ind & permit_ind])
    non_dac_ecdf = ECDF(permit_age.loc[nan_ind & non_dac_ind & permit_ind])

    # Output DAC ECDF to File for LBNL
    with open('/Users/edf/repos/la100es-panel-upgrades/data/ecdfs/{}_dac_ecdf.pkl'.format(sector), 'wb') as handle:
        pickle.dump(dac_ecdf, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Output non-DAC ECDF to File for LBNL
    with open('/Users/edf/repos/la100es-panel-upgrades/data/ecdfs/{}_non_dac_ecdf.pkl'.format(sector), 'wb') as handle:
        pickle.dump(non_dac_ecdf, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Seed the Random Number Generator to Create Deterministic Outputs
    rs = 12345678
    np.random.seed(rs)

    # Extract the Current Ages of the DAC Inference Group of Non-Permitted Properties
    dac_x = current_age.loc[(nan_ind & dac_ind & ~permit_ind)]

    # Output the Probability of an Upgrade Based upon the DAC-ECDF
    dac_y = dac_ecdf(dac_x)
    dac_upgrade_list = []

    # Infer Upgrade based Upon Pseudo-Random Choice Using the Output Probability
    for pr in dac_y:
        dac_upgrade_list.append(np.random.choice(np.array([False, True]), size = 1, p = [1.0-pr, pr])[0])

    dac_x = dac_x.to_frame()
    dac_x['previous_upgrade'] = dac_upgrade_list

    # Extract the Current Ages of the non-DAC Inference Group of Non-Permitted Properties
    non_dac_x = current_age.loc[(nan_ind & non_dac_ind & ~permit_ind)]

    # Output the Probability of an Upgrade Based upon the non-DAC-ECDF
    non_dac_y = non_dac_ecdf(non_dac_x)
    non_dac_upgrade_list = []

    # Infer Upgrade based Upon Pseudo-Random Choice Using the Output Probability
    for pr in non_dac_y:
        non_dac_upgrade_list.append(np.random.choice(np.array([False, True]), size = 1, p = [1.0-pr, pr])[0])

    non_dac_x = non_dac_x.to_frame()
    non_dac_x['previous_upgrade'] = non_dac_upgrade_list

    # Loop Through and Assess Upgrades for DAC and Non-DAC cohorts
    upgrade_scale = []

    if sector == 'single_family':

        upgrade_scale = [   0.,
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

    elif sector == 'multi_family':

        upgrade_scale = [   0.,
                            40.,
                            60.,
                            90.,
                            150.,
                            200.]

    # DAC Loop
    data['inferred_panel_upgrade'] = False

    for ind, row in dac_x.iterrows():

        as_built = data.loc[ind,'panel_size_as_built']
        existing = as_built

        if (row['previous_upgrade'] == True) & (data.loc[ind, 'permitted_panel_upgrade'] == False):
            level = upgrade_scale.index(as_built)
            existing = upgrade_scale[level + 1]
            data.loc[ind,'inferred_panel_upgrade'] = True

        data.loc[ind,'panel_size_existing'] = existing

    # Non-DAC Loop
    for ind, row in non_dac_x.iterrows():

        as_built = data.loc[ind,'panel_size_as_built']
        existing = as_built

        if (row['previous_upgrade'] == True) & (data.loc[ind, 'permitted_panel_upgrade'] == False):
            level = upgrade_scale.index(as_built)
            existing = upgrade_scale[level + 1]
            data.loc[ind,'inferred_panel_upgrade'] = True

        data.loc[ind,'panel_size_existing'] = existing

    data['panel_upgrade'] = data.loc[:,['permitted_panel_upgrade','inferred_panel_upgrade']].any(axis = 1)

    return data
