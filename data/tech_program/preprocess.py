#%% Package Imports

import pandas as pd
from sqlalchemy import create_engine
import os

#%% Read Tech Program Datasets

root = '/Users/edf/repos/carb_elec/data/tech_program/raw/'
os.chdir(root)

#%% Read Excel Data Sets

single_family_raw = pd.read_excel('TECHWorkingDataset_Single-Family_2024-02-21.xlsx')
single_family_dd = pd.read_excel('Data_Dictionary_-_TECH_Working_Data_Set_Single_Family_1Pz9Ezo.xlsx')

multi_family_raw = pd.read_excel('TECHWorkingDataset_Multifamily_2024-02-21.xlsx')
multi_family_dd = pd.read_excel('Data_Dictionary_-_TECH_Working_Data_Set_Multifamily_Ic7isSx.xlsx')

#%% Write to Database

#%% Get DB Connection Parameters

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

#%% Export Tables to Database

single_family_raw.to_sql(
    name = 'single_family_program_data_2024-02-21',
    schema = 'tech',
    con = engine,
    if_exists = 'replace',
    index = False)

single_family_dd.to_sql(
    name = 'single_family_data_dictionary_2024-02-21',
    schema = 'tech',
    con = engine,
    if_exists = 'replace',
    index = False)

single_family_raw.to_sql(
    name = 'multi_family_program_data_2024-02-21',
    schema = 'tech',
    con = engine,
    if_exists = 'replace',
    index = False)

multi_family_dd.to_sql(
    name = 'multi_family_data_dictionary_2024-02-21',
    schema = 'tech',
    con = engine,
    if_exists = 'replace',
    index = False)
