#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion

import matplotlib.pyplot as plt
import os

#%% Class Definitions

class DataFrameSelector(BaseEstimator, TransformerMixin):
    '''Custom class to support the pipeline filtering of input pandas dataframes
    on the basis of attribute field name lists'''

    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y = None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values

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
        query = ''' SELECT * FROM la100.sf_training_full;'''
    elif sector == 'multi_family':
        query = '''SELECT * FROM la100.mf_training_full;'''
    else:
        raise Exception("Sector must be either 'single-family' or multi_family'")

    raw = pd.read_sql(query, db_con)

    return raw

#%% Extract Training Data

sector = 'single_family'
data = ImportRaw(sector)
data.set_index('rowid', drop = True, inplace = True)

#%% Get Feature Types

fill_attribs = ['HeatingTypeorSystemStndCode',
                'AirConditioningTypeorSystemStndCode']
num_attribs = list(data.select_dtypes(include=[np.number]).columns)
cat_attribs = list(data.select_dtypes(include=[object]).columns)
for val in fill_attribs:
    if val in cat_attribs:
        cat_attribs.remove(val)

#%% Construct Preprocessing Pipeline

# TODO; There is an issue with the imputer/one-hot-encoder of the categorical
# variables in the pipeline. The processed output should have all numeric
# values and it does not.

imputer_pipeline = Pipeline([
    ('selector', DataFrameSelector(fill_attribs)),
    ('fill_imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'constant',
        fill_value = 'NA')),
    ('one_hot_encoder', OneHotEncoder(sparse_output = False))
])

numeric_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'median')),
    ('std_scaler', StandardScaler()),
])

categorical_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs)),
    ('imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'most_frequent')),
    ('one_hot_encoder', OneHotEncoder(sparse_output = False)),
])

full_pipeline = FeatureUnion(transformer_list = [
    ('imputer_pipeline', imputer_pipeline),
    ('numeric_pipeline', numeric_pipeline),
    ('categorical_pipeline', categorical_pipeline),
])

data_prepared = full_pipeline.fit_transform(data)
