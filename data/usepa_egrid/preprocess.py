#%% Package Imports

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

#%% Set Environment

root = '/Users/edf/repos/carb_elec/data/usepa_egrid/raw/'
os.chdir(root)

#%% Read Egrid Excel Sheets as Dataframes

unt21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'UNT21', skiprows=1, header=0, index_col = 'SEQUNT')
gen21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'GEN21', skiprows=1, header=0, index_col = 'SEQGEN')
plnt21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'PLNT21', skiprows=1, header=0, index_col = 'SEQPLT')
st21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'ST21', skiprows=1, header = 0)
ba21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'BA21', skiprows=1, header = 0)
srl21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'SRL21', skiprows=1, header = 0)
nrl21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'NRL21', skiprows=1, header = 0)
us21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'US21', skiprows=1, header = 0)
ggl21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'GGL21', skiprows=1, header = 0)
demo21 = pd.read_excel('eGRID2021_data.xlsx', sheet_name = 'SRL21', skiprows=1, header = 0)

#%% Get Database Connection Parameters

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

#%% Output Sheet Data to PostGres Tables

unt21.to_sql('unt_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

gen21.to_sql('gen_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

plnt21.to_sql('plnt_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

st21.to_sql('st_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

ba21.to_sql('ba_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

srl21.to_sql('srl_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

nrl21.to_sql('nrl_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

us21.to_sql('us_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

ggl21.to_sql('ggl_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)

demo21.to_sql('demo_2021',
    if_exists = 'replace',
    index = False,
    schema = 'usepa',
    con = engine)
