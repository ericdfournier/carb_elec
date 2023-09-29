
#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import numpy as np
from scipy.stats import randint

from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay, classification_report, confusion_matrix
from sklearn.tree import export_graphviz
from sklearn.model_selection import cross_validate

from IPython.display import Image
import graphviz

import matplotlib.pyplot as plt
import os
import pickle

#%% Set Output Environment

root = '/Users/edf/repos/carb_elec/model/runs/'
os.chdir(root)

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

    query = ''' SELECT  A.megaparcelid,
                        A."YearBuilt",
                        A."LotSizeSquareFeet",
                        A."TotalBuildingAreaSqFt",
                        A."TotalNoOfBedrooms",
                        A."TotalLandAssessedValue",
                        A."TotalImprovementAssessedValue",
                        A."HeatingTypeorSystemStndCode",
                        A."AirConditioningTypeorSystemStndCode",
                        A.sampled,
                        A.usetype,
                        A.shorelinedistm,
                        A.elevationm,
                        A.slopepct,
                        A.aspectdeg,
                        A.ciscorep,
                        A.dac,
                        A.lowincome,
                        A.nondesignated,
                        A.bufferlowincome,
                        A.bufferlih,
                        A.peopcolorpct,
                        A.lowincpct,
                        A.unemppct,
                        A.lingisopct,
                        A.lesshspct,
                        A.under5pct,
                        A.over64pct,
                        A.lifeexppct,
                        A.renterhouseholdspct,
                        A.elecheatinghouseholdspct,
                        A.bzone,
                        A.panel_size_as_built,
                        B.panel_size_existing
                FROM ztrax.model_data AS A
                JOIN ztrax.model_data_sf_inference AS B
                    ON A.megaparcelid = B.megaparcelid
                WHERE A.usetype = '{}';'''.format(sector)

    raw = pd.read_sql(query, db_con)

    return raw

#%% Extract Training Data

sector = 'single_family'
data = ImportRaw(sector)
data.set_index('megaparcelid', drop = True, inplace = True)

#%% Drop Corrupt Records and Check Null Counts

data.dropna(
    subset = ['panel_size_as_built', 'panel_size_existing'],
    inplace = True
    )

data.isna().sum(axis = 0)

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
                        'lifeexppct',
                        'renterhouseholdspct',
                        'elecheatinghouseholdspct']

fill_attribs = ['HeatingTypeorSystemStndCode',
                'AirConditioningTypeorSystemStndCode']

num_attribs = list(data.select_dtypes(include=[np.number]).columns)
for val in passthrough_attribs:
    if (val in num_attribs):
        num_attribs.remove(val)

cat_attribs = list(data.select_dtypes(include=[object]).columns)
for val in fill_attribs:
    if (val in cat_attribs):
        cat_attribs.remove(val)

num_attribs.remove(output_attrib[0])

#%% Split Inputs from Outputs

inputs = data[passthrough_attribs + fill_attribs + num_attribs + cat_attribs]
outputs = data[output_attrib]

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

X = input_pipeline.fit_transform(inputs)

#%% Construct Ouput Feature Pipleine

output_pipeline = Pipeline([
    ('selector', DataFrameSelector(output_attrib)),
    ('imputer', SimpleImputer(missing_values = np.nan,
        strategy = 'most_frequent')),
    ('ordinal_encoder', OrdinalEncoder())
])

y = output_pipeline.fit_transform(outputs)

#%% Training Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=69,
    stratify = y)

y_train = y_train.ravel()
y_test = y_test.ravel()

#%% Random Forest Model Parameter Search

rnd_clf = RandomForestClassifier(
    n_estimators = 500,
    max_depth = 50,
    verbose = 1,
    warm_start = True)

#%% Model Fit with Best Parameters

rnd_clf.fit(X_train, y_train)

#%% Predict and Evaluate Accuracy on Test Set

predict_train = rnd_clf.predict(X_train)
predict_test = rnd_clf.predict(X_test)

#%% Print Accuracy, Confusion Matrix, and Classificaiton Report

accuracy = accuracy_score(y_test, predict_test)
confusion_mat = confusion_matrix(y_train, predict_train)
clf_report = classification_report(y_train, predict_train)

print(accuracy)
print(confusion_mat)
print(clf_report)

#%% Construct Attribute Field Name List

n1 = passthrough_pipeline['selector'].attribute_names
n2 = list(fill_pipeline['one_hot_encoder'].get_feature_names_out())
n3 = numeric_pipeline['selector'].attribute_names
n4 = list(categorical_pipeline['one_hot_encoder'].get_feature_names_out())

class_names = n1 + n2 + n3 + n4

#%% Plot Confusion Matrix

np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
titles_options = [
    ("Confusion matrix, without normalization", None),
    ("Normalized confusion matrix", "true"),
]

fig, ax = plt.subplots(1,1,figsize = (10,10))

for title, normalize in titles_options:
    disp = ConfusionMatrixDisplay.from_estimator(
        rnd_clf,
        X_test,
        y_test,
        display_labels=class_names,
        cmap=plt.cm.Blues,
        normalize=normalize,
        ax = ax
    )
    disp.ax_.set_title(title)

    print(title)
    print(disp.confusion_matrix)

plt.show()
