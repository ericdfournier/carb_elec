#%% Package Imports

import math
import numpy as np
import pandas as pd
import sqlalchemy as sql
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import StringLookup

#%% Import Raw Training Data from PostgreSQL Database

def ImportRaw(sector):
    '''Function to import pre-processed buildind permit training data from
    local postgres database'''

    # Switch on sector
    if sector == 'single_family':
        s = 'sf'
    elif sector == 'multi_family':
        s = 'mf'

    # Extract Single Family Data from
    query = ''' SELECT
                A.megaparcelid,
                A."YearBuilt",
                A."TotalNoOfBuildings",
                A."LotSizeSquareFeet",
                A."TotalBuildingAreaSqFt",
                A."TotalNoOfUnits",
                A."TotalNoOfBedrooms",
                A."TotalLandAssessedValue",
                A."TotalImprovementAssessedValue",
                A."HeatingTypeorSystemStndCode",
                A."AirConditioningTypeorSystemStndCode",
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
                A.x,
                A.y,
                A.panel_size_as_built,
                B.panel_size_existing
            FROM ztrax.model_data AS A
            JOIN ztrax.model_data_{}_inference AS B
                ON A.megaparcelid = B.megaparcelid;'''.format(s)

    endpoint='postgresql://{}:{}@{}?port={}&dbname={}'.format(
        os.getenv('PGUSER'),
        os.getenv('PGPASS'),
        os.getenv('PGHOST'),
        os.getenv('PGPORT'),
        'carb')

    data = pd.read_sql(query, endpoint, index_col = 'megaparcelid')

    return data

#%% Extract Raw Training Data and Parse Fields for Pre-processing Pipeline

sector = 'single_family'
data = ImportRaw(sector)

#%% Data Pre-processing

# TODO: Continue modifying below for recently update "ztrax.model_data" input
# table.

# Impute Missing Values
median_cols = [
    'YearBuilt',
    'TotalNoOfBuildings',
    'LotSizeSquareFeet',
    'TotalBuildingAreaSqFt',
    'TotalNoOfUnits',
    'TotalNoOfBedrooms',
    'TotalLandAssessedValue',
    'TotalImprovementAssessedValue',
    'shorelinedistm',
    'ciscorep',
    'elevationm',
    'slopepct',
    'aspectdeg',
    'lifeexppct']

for col in median_cols:
    nan_ind = data[col].isna()
    data.loc[nan_ind, col] = data[col].median()

fill_cols = [
    'HeatingTypeorSystemStndCode',
    'AirConditioningTypeorSystemStndCode']

for col in fill_cols:
    nan_ind = data[col].isna()
    data.loc[nan_ind, col] = 'NA'

# Specify labels for target feature
labels = {
    '30.0': '0',
    '40.0': '1',
    '60.0': '2',
    '100.0': '3',
    '125.0': '4',
    '150.0': '5',
    '200.0': '6',
    '225.0': '7',
    '320.0': '8',
    '400.0': '9',
    '600.0': '10',
    '800.0': '11',
    '1000.0': '12',
    '1200.0': '13',
    '1400.0': '14'
}

# Drop records with missing values for target feature
data = data.dropna(axis = 0, subset = 'panel_size_existing')

# Recast target feature column to prepare for labeling
data.loc[:,'panel_size_existing'] = data.loc[:,'panel_size_existing'].astype(str)

# Label target features
data.replace({'panel_size_existing':labels}, inplace = True)

# # Cast numeric types as int32
num_columns = data.select_dtypes(include=np.number).columns.tolist()
for col in num_columns:
     data[col] = data[col].astype(np.int32)

#%% Verify No Null Values

data.isna().any()

#%% Training Test Split

train_splits = []
test_splits = []

for _, group_data in data.groupby('panel_size_existing'):
    random_selection = np.random.rand(len(group_data.index)) <= 0.85
    train_splits.append(group_data[random_selection])
    test_splits.append(group_data[~random_selection])

train_data = pd.concat(train_splits).sample(frac=1).reset_index(drop=True)
test_data = pd.concat(test_splits).sample(frac=1).reset_index(drop=True)

print(f'Train split size: {len(train_data.index)}')
print(f'Test split size: {len(test_data.index)}')

#%% Output to Files

train_data_file = './data/train_data.csv'
test_data_file = './data/test_data.csv'

train_data.to_csv(train_data_file, index=False)
test_data.to_csv(test_data_file, index=False)

#%% Define Metadata

CSV_HEADER = [
    'YearBuilt',
    'TotalNoOfBuildings',
    'LotSizeSquareFeet',
    'TotalBuildingAreaSqFt',
    'TotalNoOfUnits',
    'TotalNoOfBedrooms',
    'TotalLandAssessedValue',
    'TotalImprovementAssessedValue',
    'HeatingTypeorSystemStndCode',
    'AirConditioningTypeorSystemStndCode',
    'shorelinedistm',
    'elevationm',
    'slopepct',
    'aspectdeg',
    'ciscorep',
    'dac',
    'lowincome',
    'nondesignated',
    'bufferlowincome',
    'bufferlih',
    'peopcolorpct',
    'lowincpct',
    'unemppct',
    'lingisopct',
    'lesshspct',
    'under5pct',
    'over64pct',
    'lifeexppct',
    'renterhouseholdspct',
    'elecheatinghouseholdspct',
    'bzone',
    'x',
    'y',
    'panel_size_as_built',
    'panel_size_existing'
]

TARGET_FEATURE_NAME = 'panel_size_existing'

TARGET_FEATURE_LABELS = list(labels.values())

NUMERIC_FEATURE_NAMES = [
    'YearBuilt',
    'TotalNoOfBuildings',
    'LotSizeSquareFeet',
    'TotalBuildingAreaSqFt',
    'TotalNoOfUnits',
    'TotalNoOfBedrooms',
    'TotalLandAssessedValue',
    'TotalImprovementAssessedValue',
    'shorelinedistm',
    'elevationm',
    'slopepct',
    'aspectdeg',
    'peopcolorpct',
    'lowincpct',
    'unemppct',
    'lingisopct',
    'lesshspct',
    'under5pct',
    'over64pct',
    'lifeexppct',
    'renterhouseholdspct',
    'elecheatinghouseholdspct',
    'x',
    'y',
    'panel_size_as_built'
]

CATEGORICAL_FEATURES_WITH_VOCABULARY = {
    'HeatingTypeorSystemStndCode': list(data['HeatingTypeorSystemStndCode'].unique()),
    'AirConditioningTypeorSystemStndCode': list(data['AirConditioningTypeorSystemStndCode'].unique()),
    'dac': list(data['dac'].unique()),
    'lowincome': list(data['lowincome'].unique()),
    'nondesignated': list(data['nondesignated'].unique()),
    'bufferlowincome': list(data['bufferlowincome'].unique()),
    'bufferlih': list(data['bufferlih'].unique()),
    'bzone': list(data['bzone'].unique())
}

CATEGORICAL_FEATURE_NAMES = list(CATEGORICAL_FEATURES_WITH_VOCABULARY.keys())

FEATURE_NAMES = NUMERIC_FEATURE_NAMES + CATEGORICAL_FEATURE_NAMES

COLUMN_DEFAULTS = [
    [0] if feature_name in NUMERIC_FEATURE_NAMES + [TARGET_FEATURE_NAME] else ['NA']
    for feature_name in CSV_HEADER
]

NUM_CLASSES = len(TARGET_FEATURE_LABELS)

#%% Random Forest Hyperparamters

# Target column name.
TARGET_FEATURE_NAME = 'panel_size_existing'
# Maximum number of decision trees. The effective number of trained trees can be smaller if early stopping is enabled.
NUM_TREES = 250
# Minimum number of examples in a node.
MIN_EXAMPLES = 6
# Maximum depth of the tree. max_depth=1 means that all trees will be roots.
MAX_DEPTH = 5
# Ratio of the dataset (sampling without replacement) used to train individual trees for the random sampling method.
SUBSAMPLE = 0.65
# Control the sampling of the datasets used to train individual trees.
SAMPLING_METHOD = "RANDOM"
# Ratio of the training dataset used to monitor the training. Require to be >0 if early stopping is enabled.
VALIDATION_RATIO = 0.1

#%% Get Data from CSV

def get_dataset_from_csv(csv_file_path, batch_size, shuffle=False):

    dataset = tf.data.experimental.make_csv_dataset(
        csv_file_path,
        batch_size=batch_size,
        column_names=CSV_HEADER,
        column_defaults=COLUMN_DEFAULTS,
        label_name=TARGET_FEATURE_NAME,
        num_epochs=1,
        header=True,
        shuffle=shuffle,
    )
    return dataset.cache()

#%% Set Fixed Model Hyperparameters

learning_rate = 0.001
dropout_rate = 0.1
batch_size = 265
num_epochs = 50
hidden_units = [64, 64, 64]

#%% Run Experiment

def run_experiment(model):

    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate = learning_rate),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )

    train_dataset = get_dataset_from_csv(train_data_file, batch_size, shuffle=True)
    test_dataset = get_dataset_from_csv(test_data_file, batch_size)

    print('Start training the model...')
    history = model.fit(train_dataset, epochs = num_epochs)
    print('Model training finished')

    _, accuracy = model.evaluate(test_dataset, verbose=0)
    print(f'Test accuracy: {round(accuracy * 100, 2)}%')

    return

#%% Create Model Inputs

def create_model_inputs():
    inputs = {}
    for feature_name in FEATURE_NAMES:
        if feature_name in NUMERIC_FEATURE_NAMES:
            inputs[feature_name] = layers.Input(
                name=feature_name, shape=(), dtype=tf.float32
            )
        else:
            inputs[feature_name] = layers.Input(
                name=feature_name, shape=(), dtype=tf.string
            )

    return inputs

#%% Encode Inputs

def encode_inputs(inputs, use_embedding = False):

    encoded_features = []

    for feature_name in inputs:
        if feature_name in CATEGORICAL_FEATURE_NAMES:

            vocabulary = CATEGORICAL_FEATURES_WITH_VOCABULARY[feature_name]
            # Create a lookup to convert string values to an integer indices.
            # Since we are not using a mask token nor expecting any out of vocabulary
            # (oov) token, we set mask_token to None and  num_oov_indices to 0.
            lookup = StringLookup(
                vocabulary = vocabulary,
                mask_token = None,
                num_oov_indices = 0,
                output_mode = 'int' if use_embedding else 'binary',
            )
            if use_embedding:
                # Convert the string input values into integer indices.
                encoded_feature = lookup(inputs[feature_name])
                embedding_dims = int(math.sqrt(len(vocabulary)))
                # Create an embedding layer with the specified dimensions.
                embedding = layers.Embedding(
                    input_dim = len(vocabulary), output_dim = embedding_dims
                )
                # Convert the index values to embedding representations.
                encoded_feature = embedding(encoded_feature)
            else:
                # Convert the string input values into a one hot encoding.
                encoded_feature = lookup(tf.expand_dims(inputs[feature_name], -1))
        else:
            # Use the numerical features as-is.
            encoded_feature = tf.expand_dims(inputs[feature_name], -1)

        encoded_features.append(encoded_feature)

    all_features = layers.concatenate(encoded_features)

    return all_features

#%% Create Random Forest Model

# TODO: Create Random Forest Model as new experimental architecture to
# consolidate workflow using the following as guide:
# https://keras.io/examples/structured_data/classification_with_tfdf/

def create_random_forest_model():

    inputs = create_model_inputs()
    features = encode_inputs(inputs)

    model = tfdf.keras.RandomForestModel(inputs = inputs, outputs = )

    return model

#%% Create RNN Model

def create_rnn_model():
    inputs = create_model_inputs()
    features = encode_inputs(inputs)

    for units in hidden_units:
        features = layers.Dense(units)(features)
        features = layers.BatchNormalization()(features)
        features = layers.ReLU()(features)
        features = layers.Dropout(dropout_rate)(features)

    outputs = layers.Dense(units = NUM_CLASSES, activation='softmax')(features)
    model = keras.Model(inputs = inputs, outputs=outputs)

    return model

rnn_model = create_rnn_model()
keras.utils.plot_model(rnn_model, show_shapes=True, rankdir='LR')

#%% Create Wide and Deep Model

def create_wide_and_deep_model():

    inputs = create_model_inputs()
    wide = encode_inputs(inputs)
    wide = layers.BatchNormalization()(wide)

    deep = encode_inputs(inputs, use_embedding=True)
    for units in hidden_units:
        deep = layers.Dense(units)(deep)
        deep = layers.BatchNormalization()(deep)
        deep = layers.ReLU()(deep)
        deep = layers.Dropout(dropout_rate)(deep)

    merged = layers.concatenate([wide, deep])
    outputs = layers.Dense(units=NUM_CLASSES, activation='softmax')(merged)
    model = keras.Model(inputs=inputs, outputs=outputs)

    return model

wide_and_deep_model = create_wide_and_deep_model()
keras.utils.plot_model(wide_and_deep_model, show_shapes=True, rankdir='LR')

#%% Create Cross Deep Model

def create_deep_and_cross_model():

    inputs = create_model_inputs()
    x0 = encode_inputs(inputs, use_embedding=True)

    cross = x0
    for _ in hidden_units:
        units = cross.shape[-1]
        x = layers.Dense(units)(cross)
        cross = x0 * x + cross
    cross = layers.BatchNormalization()(cross)

    deep = x0
    for units in hidden_units:
        deep = layers.Dense(units)(deep)
        deep = layers.BatchNormalization()(deep)
        deep = layers.ReLU()(deep)
        deep = layers.Dropout(dropout_rate)(deep)

    merged = layers.concatenate([cross, deep])
    outputs = layers.Dense(units=NUM_CLASSES, activation='softmax')(merged)
    model = keras.Model(inputs=inputs, outputs=outputs)

    return model

deep_and_cross_model = create_deep_and_cross_model()
keras.utils.plot_model(deep_and_cross_model, show_shapes=True, rankdir='LR')

#%% Run Baseline Experiment

run_experiment(rnn_model)

#%% Run Wide and Deep Model

run_experiment(wide_and_deep_model)

#%% Run Cross-Deep Model

run_experiment(deep_and_cross_model)
