#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import numpy as np

import matplotlib.pyplot as plt
import os

#%% Function Definitions

def ImportRaw(sector):
    '''Function to import pre-processed buildind permit training data from
    local postgres database'''

    # Extract Database Connection Parameters from Environment
    host = os.getenv('PGHOST')
    user = os.getenv('PGUSER')
    password = os.getenv('PGPASS')
    port = os.getenv('PGPORT')
    db = 'carb'

    # Establish DB Connection
    db_con_string = 'postgresql://' + user + '@' + host + ':' + port + '/' + db
    db_con = sql.create_engine(db_con_string)

    # Switch on Sector
    if sector == 'single_family':
        query = '''SELECT * FROM la100.sf_training;'''
    elif sector == 'multi_family':
        query = '''SELECT * FROM la100.mf_training;'''
    else:
        raise Exception("Sector must be either 'single-family' or multi_family'")

    raw = pd.read_sql(query, db_con)

    return raw

#%%
