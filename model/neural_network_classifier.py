
#%% Package Imports

import pandas as pd
import geopandas as gpd
import sqlalchemy as sql
import numpy as np
from scipy.stats import randint

from sklearn.neural_network import MLPClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay, classification_report, confusion_matrix
from sklearn.tree import export_graphviz

from IPython.display import Image
import graphviz

import matplotlib.pyplot as plt
import os
import pickle

#%% Set Output Environment

root = '/Users/edf/repos/carb_elec/model/saved/'
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
    X, y, test_size=0.33, random_state=69)

y_train = y_train.ravel()

#%% Fit Model and Save Weights

# Specify Hidden Layer Sizes
n = 5
hls = np.repeat(X_train.shape[1], n)

# Set Model Parameters
mlp_clf = MLPClassifier(
    hidden_layer_sizes = hls,
    activation = 'relu',
    solver = 'adam',
    max_iter = 500,
    verbose = True,
    warm_start = True)

# Fit Model
mlp_clf.fit(X_train,y_train)

# Save Weights
filename = 'mlp_clf.pkl'
pickle.dump(mlp_clf, open(filename, 'wb'))

#%% Predict and Evaluate Accuracy on Test Set

predict_train = mlp_clf.predict(X_train)
predict_test = mlp_clf.predict(X_test)

#%% Print Accuracy, Confusion Matrix, and Classificaiton Report

accuracy = accuracy_score(y_test, predict_test)
confusion_mat = confusion_matrix(y_train, predict_train)
clf_report = classification_report(y_train, predict_train)

print(accuracy)
print(confusion_mat)
print(clf_report)

#%% Generate Predictor Names

n1 = passthrough_pipeline['selector'].attribute_names
n2 = list(fill_pipeline['one_hot_encoder'].get_feature_names_out())
n3 = numeric_pipeline['selector'].attribute_names
n4 = list(categorical_pipeline['one_hot_encoder'].get_feature_names_out())
predictor_names = n1 + n2 + n3 + n4

#%% Generate Class Names

class_names = list(np.sort(outputs[output_attrib[0]].unique()))[:-1]

#%% Plot Confusion Matrix

fig, ax = plt.subplots(1,2,figsize=(30,11))

cat_norm = ConfusionMatrixDisplay.from_estimator(
    mlp_clf,
    X_test,
    y_test,
    display_labels=class_names,
    cmap=plt.cm.Blues,
    normalize= 'true',
    ax = ax[0]
)

cat_norm.ax_.set_title('Within-Category Normalized Confusion Matrix')

all_norm = ConfusionMatrixDisplay.from_estimator(
    mlp_clf,
    X_test,
    y_test,
    display_labels=class_names,
    cmap=plt.cm.Reds,
    normalize= 'all',
    ax = ax[1]
)

all_norm.ax_.set_title('Full Normalized Confusion Matrix')

plt.show()
