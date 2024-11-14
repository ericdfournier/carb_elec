#%% Import Packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Read Data

os.chdir('/Users/edf/Desktop/')
psps_file = 'psps_results.xlsx'
exposure_file = 'exposure_results.xlsx'

#%% Read in and process PSPS data

psps = pd.read_excel(psps_file)
psps_out = psps.set_index(['ceus_subsector','dac']).unstack()
psps_out.to_csv('psps_out.csv')

#%% Read in and Process Exposure data

exposure = pd.read_excel(exposure_file)
exposure_out = exposure.set_index(['ceus_subsector', 'dac']).unstack()
exposure_out.to_csv('exposure_out.csv')
