#%% Package Imports

import pandas as pd
import sqlalchemy as sql
import os

#%% Set Environment

root = '/Users/edf/Desktop/carb/'
file = 'acs_heating_change.json'

#%% Read Data from JSON File

df = pd.read_json(root + file)

#%% Write Table to Database

# DB Connection Parameters

# Extract Database Connection Parameters from Environment
host = os.getenv('PGHOST')
user = os.getenv('PGUSER')
password = os.getenv('PGPASS')
port = os.getenv('PGPORT')
db = 'carb'

# Establish DB Connection
db_con_string = 'postgresql://' + user + '@' + host + ':' + port + '/' + db
db_con = sql.create_engine(db_con_string)

#%% Write Table to Database

cols = ['GEOID', 'prop_electric_change']
df.loc[:,cols].to_sql('acs_ca_2017_2022_proportion_electric_heating_change',
    schema = 'census',
    con = db_con,
    if_exists = 'replace',
    index = False)

#%%
