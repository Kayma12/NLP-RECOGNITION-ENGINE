import os
import pickle
from pathlib import Path

from src.cleaning_and_reading import cv_cleaning
with open(os.path.join(os.path.dirname(__file__), 'df_final'), 'rb') as fh:  # you need to use 'rb' to read
    df = pickle.load(fh)


# Drop over laps in BA
'''
'Ref Data Architecture Business analyst And Project Manager',  >> ba. 
'Business Data Analyst â€“ Compliance',
>> IF IT CONTAINS DATA drop from BA
'''
df2 = df[(df.Stream == 'Business Analysis') & (df.Title.str.contains("Data"))].index
df.drop(df2, inplace=True)


df_dup = df[df.duplicated()].index
# remove duplicates by getting their positions
df.drop(df_dup, inplace=True)
# print(df_dup[df_dup['Stream'] == 'Development'])


# Clean each item in the description column

#print(df['Description'].head(1).to_string())
#df['Description'] = df['Description'].apply(cv_cleaning.clean_cv())
df['Description'] =df['Description'].apply(cv_cleaning.clean_cv,1)
#print(df['Description'].to_string())

# this will create a file call clean df after cleaning the descriptions that will store the data frame
# with open(Path(__file__).parent / 'clean_df_final', 'wb') as fh:  # notice that you need the 'wb' for the dump
#     pickle.dump(df, fh)

print('hecho')