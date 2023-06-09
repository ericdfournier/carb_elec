#%% Package Imports

import seaborn as sns
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer

#%% Load Data

df = sns.load_dataset('penguins')
print(df.head())
print(df.info())
print(df.isnull().sum())

#%% 

# Create a SimpleImputer Class
imputer = SimpleImputer(missing_values=np.NaN, strategy='mean')

# Fit the columns to the object
columns = ['bill_depth_mm', 'bill_length_mm', 'flipper_length_mm', 'body_mass_g']
imputer=imputer.fit(df[columns])

# Transform the DataFrames column with the fitted data
df[columns]=imputer.transform(df[columns])
