#!/usr/bin/python3

import pandas as pd

# Dataset downloaded from
# https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc
# as dataset_arrests.csv

DATASET_FILE="./dataset_arrests.csv"
OUTPUT_FILE="integrated_dataset.csv"

df = pd.read_csv('./dataset_arrests.csv')
columns_to_drop = ['ARREST_KEY', 'ARREST_DATE', 'PD_CD',
                   'KY_CD', 'LAW_CODE', 'ARREST_PRECINCT',
                   'JURISDICTION_CODE', 'X_COORD_CD', 'Y_COORD_CD',
                   'Latitude', 'Longitude', 'New Georeferenced Column']
df = df.drop(columns=columns_to_drop)

# Updating Level of Offense Column
df.loc[df['LAW_CAT_CD'] == 'F', 'LAW_CAT_CD'] = 'Felony'
df.loc[df['LAW_CAT_CD'] == 'M', 'LAW_CAT_CD'] = 'Misdemeanor'
df.loc[df['LAW_CAT_CD'] == 'V', 'LAW_CAT_CD'] = 'Violation'

# Updating Borough of Arrest
df.loc[df['ARREST_BORO'] == 'Q', 'ARREST_BORO'] = 'Queens'
df.loc[df['ARREST_BORO'] == 'B', 'ARREST_BORO'] = 'Bronx'
df.loc[df['ARREST_BORO'] == 'S', 'ARREST_BORO'] = 'Staten Island'
df.loc[df['ARREST_BORO'] == 'K', 'ARREST_BORO'] = 'Brooklyn'
df.loc[df['ARREST_BORO'] == 'M', 'ARREST_BORO'] = 'Manhattan'

df.to_csv(OUTPUT_FILE, index=False)