#!/usr/bin/env python
# coding: utf-8
# Modules
import os
from   glob import glob
import numpy as np
import pandas as pd


# functions
def clean_my_file(file_name):
    
    # read csv
    exp = pd.read_csv(file_name)
    # list of freqs
    
    list_of_freqs = exp.columns[12::].to_list()
    
    # index of first real freq
    index = list_of_freqs.index('-12')
    
    # normalize
    norm_factor = exp[ list_of_freqs[0:index-1] ].iloc[:,-1]
    
    raw_data = exp[ list_of_freqs[index::] ]
    
    # preallocate with zeros
    Zspectra = np.zeros(raw_data.shape)
    
    
    for i in range(raw_data.shape[0]):
        Zspectra[i,:] = raw_data.iloc[i,:] / norm_factor[i]
        
    
    #out[exp.columns[0:11].to_list()] = exp.columns[0:11].copy()
    
    out = exp[ exp.columns[0:11] ].copy()
    
    out['FILE']  = file_name.split('/raw_data/')[1]
    
    Z = pd.DataFrame(Zspectra, columns= list_of_freqs[index::])
    
    out[Z.columns] = Z.copy()
    
    return out

# Load data
PATH = "../raw_data"
EXT = "*.csv"
all_csv_files = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in glob(os.path.join(path, EXT))]

data = pd.DataFrame()

for file in all_csv_files:
    exp = clean_my_file(file)
    data = pd.concat( (data,  exp), sort=False )

print(  data.head(10).to_string()  )

# Save data
path = '../clean_data/acido_CEST_MRI_Iopamidol.parquet.gzip'
data.to_parquet(path, compression='gzip')
print(f'Done saving onto {path}')
