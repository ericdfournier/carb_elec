#%% Package Imports

import censusdata
import geopandas as gpd
import pandas as pd
import us
import os
from sqlalchemy import create_engine

#%% Search Function

def SearchData(product, year, search, keyword):

    sample_raw = censusdata.search(
        product,
        year,
        search,
        keyword,
        tabletype = 'profile')

    sample = []
    for s in sample_raw:
        if 'PUERTO RICO' not in s[1]:
            sample.append(s)

    codes = [s[0] for s in sample]
    metadata = pd.DataFrame(sample)
    cols = ['variable', 'table', 'label']
    metadata.columns = cols

    return codes, metadata, sample

#%% Specify Search Parameters

product = 'acs5'
year = 2019
search = 'label'

#%% Find Attributes

population_codes, population_metadata, population_sample = SearchData(
    product,
    year,
    search,
    'population')

income_codes, income_metadata, income_sample = SearchData(
    product,
    year,
    search,
    'income')

housing_codes, housing_metadata, housing_sample = SearchData(
    product,
    year,
    search,
    'housing')

fuel_codes, fuel_metadata, fuel_sample = SearchData(
    product,
    year,
    search,
    'fuel')

#%% Merge Metadata Tables

meta_data = pd.concat([
    population_metadata,
    income_metadata,
    housing_metadata,
    fuel_metadata], axis = 0).reset_index(drop = True);

#%% Construct 10-digit Geoid Fields

def ConstructGeoids(df):
    input = df.index.get_level_values(0)
    geoids = []
    for i in input:
        state_fips = i.geo[0][1]
        county_fips = i.geo[1][1]
        tract_fips = i.geo[2][1]
        geoid = state_fips + county_fips + tract_fips
        geoids.append(geoid)
    return geoids

#%% Construct Names

def ConstructNames(df):
    input = df.index.get_level_values(0)
    names = []
    for i in input:
        name = i.name
        names.append(name)
    return names

#%% Download Data

def DownloadData(product, year, codes, census_api_key):

    data = censusdata.download(
        product,
        year,
        censusdata.censusgeo([('state', us.states.CA.fips),
        ('county', '*'),
        ('tract', '*')]),
        codes,
        tabletype = 'profile',
        key = census_api_key)

    data['GEOID'] = ConstructGeoids(data)
    data['NAME'] = ConstructNames(data)
    data.set_index('GEOID', drop = True, inplace = True)

    return data

#%% Get API Key

census_api_key = os.environ['CENSUS_API_KEY']

#%% Download Datasets

population_data = DownloadData(product, year, population_codes, census_api_key)
income_data = DownloadData(product, year, income_codes, census_api_key)
housing_data = DownloadData(product, year, housing_codes, census_api_key)
fuel_data = DownloadData(product, year, fuel_codes, census_api_key)

#%% Read Tract Geometry Data

tract_url = "https://www2.census.gov/geo/tiger/TIGER2019/TRACT/tl_2019_06_tract.zip"
tract_geom_data = gpd.read_file(tract_url)
tract_geom_data = tract_geom_data.to_crs(3310)

#%% Read PUMA Geometry Data

puma_url = "https://www2.census.gov/geo/tiger/TIGER2019/PUMA/tl_2019_06_puma10.zip"
puma_geom_data = gpd.read_file(puma_url)
puma_geom_data = puma_geom_data.to_crs(3310)

#%% Read County Geometry Data

county_url = "https://www2.census.gov/geo/tiger/TIGER2019/COUNTY/tl_2019_us_county.zip"
county_geom_data = gpd.read_file(county_url)
ca_ind = county_geom_data['STATEFP'] == '06'
county_geom_data = county_geom_data.loc[ca_ind,:].copy()
county_geom_data = county_geom_data.to_crs(3310)

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

#%% Output Tables to Postgres

population_data.to_sql('acs_ca_2019_tr_population',
    if_exists = 'replace',
    index = True,
    schema = 'census',
    con = engine)

income_data.to_sql('acs_ca_2019_tr_income',
    if_exists = 'replace',
    index = True,
    schema = 'census',
    con = engine)

housing_data.to_sql('acs_ca_2019_tr_housing',
    if_exists = 'replace',
    index = True,
    schema = 'census',
    con = engine)

fuel_data.to_sql('acs_ca_2019_tr_fuel',
    if_exists = 'replace',
    index = True,
    schema = 'census',
    con = engine)

meta_data.to_sql('acs_ca_2019_tr_metadata',
    if_exists = 'replace',
    index = False,
    schema = 'census',
    con = engine)

tract_geom_data.to_postgis('acs_ca_2019_tr_geom',
    if_exists = 'replace',
    index = False,
    schema = 'census',
    con = engine)

puma_geom_data.to_postgis('acs_ca_2019_puma_geom',
    if_exists = 'replace',
    index = False,
    schema = 'census',
    con = engine)

county_geom_data.to_postgis('acs_ca_2019_county_geom',
    if_exists = 'replace',
    index = False,
    schema = 'census',
    con = engine)
