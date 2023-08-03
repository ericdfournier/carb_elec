#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.tree import export_graphviz

from IPython.display import Image
import graphviz

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
    def feature_names_in_(self, X):
        return X.columns.to_list()

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

#%% Get Training Feature Types

output_attrib = ['panel_size_existing']

passthrough_attribs = [ 'slopepct',
                        'peopcolorpct',
                        'lowincpct',
                        'unemppct',
                        'lingisopct',
                        'lesshspct',
                        'under5pct',
                        'over64pct',
                        'lifeexppct']

fill_attribs = ['HeatingTypeorSystemStndCode',
                'AirConditioningTypeorSystemStndCode']

num_attribs = list(data.select_dtypes(include=[np.number]).columns)
for val in passthrough_attribs:
    if (val in num_attribs) or (val in output_attrib):
        num_attribs.remove(val)

cat_attribs = list(data.select_dtypes(include=[object]).columns)
for val in fill_attribs:
    if (val in cat_attribs) or (val in output_attrib):
        cat_attribs.remove(val)

#%% Construct Training Feature Pipeline

passthrough_pipeline = Pipeline([
    ('selector', DataFrameSelector(passthrough_attribs)),
    ('passthrough_imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'median')),
])

fill_pipeline = Pipeline([
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

input_pipeline = FeatureUnion(transformer_list = [
    ('passthrough_pipeline', passthrough_pipeline),
    ('fill_pipeline', fill_pipeline),
    ('numeric_pipeline', numeric_pipeline),
    ('categorical_pipeline', categorical_pipeline),
])

X = input_pipeline.fit_transform(data)

#%% Construct Ouput Feature Pipleine

output_pipeline = Pipeline([
    ('selector', DataFrameSelector(output_attrib)),
    ('imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'most_frequent')),
    ('ordinal_encoder', OrdinalEncoder())
])

y = output_pipeline.fit_transform(data)

#%% Training Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

#%% Random Forest Model Parameterization

rnd_clf = RandomForestClassifier(
    n_estimators = 500,
    max_leaf_nodes = 16,
    n_jobs = -1)

rnd_clf.fit(X_train, y_train)

#%% Predict and Evaluate Accuracy on Test Set

y_pred = rnd_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

#%% Construct Attribute Field Name List

n1 = passthrough_pipeline['selector'].attribute_names
n2 = list(fill_pipeline['one_hot_encoder'].get_feature_names_out())
n3 = numeric_pipeline['selector'].attribute_names
n4 = list(categorical_pipeline['one_hot_encoder'].get_feature_names_out())

field_names = n1 + n2 + n3 + n4

#%% Export the first three decision trees from the forest

for i in range(3):
    tree = rnd_clf.estimators_[i]
    dot_data = export_graphviz(tree,
                               feature_names=field_names,
                               filled=True,
                               max_depth=2,
                               impurity=False,
                               proportion=True)
    graph = graphviz.Source(dot_data)
    display(graph)
